import asyncio
import os
from abc import ABC, abstractmethod
from typing import Optional, Union, Dict, List
import logging

import cv2
import numpy as np


class VideoPostProcessor:
    def __init__(self, video_processors: List["VideoProcessor"]):
        self.video_processors = video_processors

    async def execute(self):
        """Execute processing for each VideoProcessor in the list concurrently."""
        await asyncio.gather(*(vp.process() for vp in self.video_processors))


class VideoProcessor(ABC):
    def __init__(
        self,
        session_id: str,
        video_filenames: Union[str, List[str]],
        sessions_path: str,
        output_dir: str,
        filters: Optional[List] = None,
        group_filters: Optional[List] = None,
    ):
        self.session_id = session_id
        if isinstance(video_filenames, str):
            self.video_filenames = [video_filenames]
        else:
            self.video_filenames = video_filenames
        self.sessions_path = sessions_path
        self.output_dir = output_dir
        self.filters = filters or []
        self.group_filters = group_filters or []
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    async def process(self, batch_size: int = 5):
        pass

    async def process_videos(self, batch_size: int = 5):
        tasks = []
        for filename in self.video_filenames:
            input_path = os.path.join(self.sessions_path, self.session_id, filename)
            tasks.append(self._process_single_video(input_path, filename, batch_size))
        await asyncio.gather(*tasks)

    async def _process_single_video(self, input_path: str, filename: str, batch_size: int):
        loop = asyncio.get_event_loop()
        cap = await loop.run_in_executor(None, cv2.VideoCapture, input_path)
        if not cap.isOpened():
            self.logger.error(f"Cannot open video file: {input_path}")
            raise FileNotFoundError(f"Cannot open video file: {input_path}")

        await self.setup_output(filename, cap)

        batch_frames = []
        global_frame_index = 0

        while True:
            ret, frame = await loop.run_in_executor(None, cap.read)
            if not ret:
                if batch_frames:
                    await self.process_batch(batch_frames, global_frame_index - len(batch_frames))
                break

            batch_frames.append(frame)
            if len(batch_frames) == batch_size:
                await self.process_batch(batch_frames, global_frame_index - len(batch_frames))
                batch_frames = []

            global_frame_index += 1

        cap.release()
        await self.finalize_output()

    async def process_batch(self, batch_frames: List[np.ndarray], start_frame_index: int):
        """Process a batch of frames sequentially."""
        for i, frame in enumerate(batch_frames):
            frame_index = start_frame_index + i
            try:
                for filter in self.filters:
                    frame = await self.apply_filter(filter, frame, frame_index)

                if self.group_filters:
                    for group_filter in self.group_filters:
                        result = await self.apply_group_filter(group_filter, frame)
                        self.collect_participant_data(result)

                await self.handle_frame_output(frame)
            except Exception as e:
                self.logger.exception(f"Failed to process frame {frame_index}: {e}")

    async def apply_filter(self, filter, frame: np.ndarray, frame_index: int):
        if asyncio.iscoroutinefunction(filter.process):
            return await filter.process(ndarray=frame, frame_index=frame_index)
        else:
            return await asyncio.get_event_loop().run_in_executor(
                None, filter.process, frame, frame_index
            )

    async def apply_group_filter(self, group_filter, frame: np.ndarray):
        if asyncio.iscoroutinefunction(group_filter.process_individual_frame):
            return await group_filter.process_individual_frame(original=None, ndarray=frame)
        else:
            return await asyncio.get_event_loop().run_in_executor(
                None, group_filter.process_individual_frame, None, frame
            )

    @abstractmethod
    async def setup_output(self, filename: str, cap: cv2.VideoCapture):
        pass

    @abstractmethod
    async def handle_frame_output(self, frame: np.ndarray):
        pass

    def collect_participant_data(self, data):
        """Default implementation does nothing."""
        pass

    @abstractmethod
    async def finalize_output(self):
        pass
