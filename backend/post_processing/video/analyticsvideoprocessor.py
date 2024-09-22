import asyncio
import csv
import os
from typing import *
import re
import cv2
import numpy as np

from post_processing.post_processing_data import PostProcessingData
from post_processing.video.post_processing import VideoPostProcessing
from post_processing.video.video_processor import VideoProcessor


class AnalyticsVideoProcessor(VideoProcessor):
    def __init__(
        self,
        session_id: str,
        video_filenames: Union[str, List[str]],
        sessions_path: str,
        output_dir: str,
        filters: Optional[List] = None,
        group_filters: Optional[List] = None,
        external_tool: bool = False,
    ):
        super().__init__(session_id, video_filenames, sessions_path, output_dir, filters, group_filters)
        self.external_tool = external_tool
        self.participant_data = {}
        self.post_processing = None

        if external_tool:
            self.post_processing = VideoPostProcessing()

    async def process(self, batch_size: int = 5):
        """Process videos either with an external tool or in-memory."""
        if self.external_tool:
            recording_list = self.prepare_recording_list()
            await self.process_with_external_tool(recording_list)
        else:
            await self.process_videos(batch_size)

        if self.group_filters:
            self.aggregate_group_filter_data()

    async def setup_output(self, filename: str, cap: cv2.VideoCapture):
        participant_id = self.extract_participant_id(filename)
        self.participant_data[participant_id] = []

    async def handle_frame_output(self, frame: np.ndarray):
        """Analytics processor doesn't need to write frames."""
        pass

    def collect_participant_data(self, data):
        """Collect data for each participant."""
        participant_id = data.get('participant_id', 'unknown')
        if participant_id not in self.participant_data:
            self.participant_data[participant_id] = []
        self.participant_data[participant_id].append(data)

    async def finalize_output(self):
        """Finalize processing by generating CSV files."""
        if not self.external_tool:
            tasks = []
            for participant_id, data in self.participant_data.items():
                output_csv = os.path.join(self.output_dir, f"{participant_id}_data.csv")
                tasks.append(self.generate_csv(data, output_csv))
            await asyncio.gather(*tasks)
        else:
            pass

    async def generate_csv(self, data: List[dict], output_path: str):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._write_csv, data, output_path)

    def _write_csv(self, data: List[dict], output_path: str):
        headers = data[0].keys() if data else []
        with open(output_path, 'w', newline='') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=headers)
            csvwriter.writeheader()
            for row in data:
                csvwriter.writerow(row)

    def extract_participant_id(self, filename: str) -> str:
        """Extract participant ID from filename using regex."""
        match = re.match(r"(\w+)_.*", filename)
        return match.group(1) if match else "unknown"

    async def process_with_external_tool(self, recording_list: List["PostProcessingData"]):
        existing_process = self.post_processing.check_existing_process()
        if existing_process.get("is_processing"):
            self.logger.warning("Existing process detected. Waiting...")
            while existing_process.get("is_processing"):
                await asyncio.sleep(5)
                existing_process = self.post_processing.check_existing_process()

        self.post_processing.recording_list = recording_list
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.post_processing.execute)

        while True:
            existing_process = self.post_processing.check_existing_process()
            if not existing_process.get("is_processing"):
                break
            await asyncio.sleep(1)

        tasks = []
        for recording_data in recording_list:
            for group_filter in self.group_filters:
                output_csv = os.path.join(self.output_dir, f"{os.path.splitext(recording_data.filename)[0]}.csv")
                tasks.append(self.extract_and_collect_data(group_filter, output_csv, recording_data.participant_id))
        await asyncio.gather(*tasks)

    async def extract_and_collect_data(self, group_filter, output_csv: str, participant_id: str):
        extracted_data = await group_filter.extract_post_process(output_csv)
        self.participant_data[participant_id] = extracted_data

    def aggregate_group_filter_data(self):
        all_data = list(self.participant_data.values())
        for group_filter in self.group_filters:
            results = group_filter.aggregate(all_data)

            output_csv_path = os.path.join(self.output_dir, f"{group_filter.name}_aggregated_results.csv")

            with open(output_csv_path, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)

                if isinstance(results, Iterable) and not isinstance(results, (str, bytes)):
                    headers = ['Participant ID', 'Aggregated Result']
                    csvwriter.writerow(headers)

                    for participant_id, result in zip(self.participant_data.keys(), results):
                        csvwriter.writerow([participant_id, result])
                else:
                    headers = ['Aggregated Result']
                    csvwriter.writerow(headers)
                    csvwriter.writerow([results])

    def prepare_recording_list(self) -> List["PostProcessingData"]:
        """Prepares the recording list for external processing."""
        recording_list = []
        for filename in self.video_filenames:
            participant_id = self.extract_participant_id(filename)
            recording_data = PostProcessingData(
                type="video",
                filename=filename,
                session_id=self.session_id,
                participant_id=participant_id,
            )
            recording_list.append(recording_data)
        return recording_list