from __future__ import annotations
import logging
import os
import subprocess

from ..post_processing_interface import PostProcessingInterface
from .producer import PostVideoProducer

class VideoPostProcessing(PostProcessingInterface):
    """Executes post-processing experiments' video by running its producer and consumer."""

    _logger: logging.Logger
    _producer: PostVideoProducer

    def __init__(self) -> None:
        """Initialize new VideoPostProcessing."""
        super().__init__()
        self._logger = logging.getLogger("VideoPostProcessing")

    def execute(self) -> None:
        """Execute video post-processing."""
        self.run_consumer()
        self._producer = PostVideoProducer()
        self._producer.publish(self.recording_list)
    
    def check_existing_process(self) -> bool:
        """Check whether there are FeatureExtraction subprocesses running."""
        proc = subprocess.Popen(["ps", "aux"],
                                stdout = subprocess.PIPE,
                                stdin =subprocess.PIPE)
        proc2 = subprocess.Popen(["grep", "FeatureExtraction"], 
                                 stdin=proc.stdout, 
                                 stdout=subprocess.PIPE)
        proc3 = subprocess.Popen(["grep", "out_dir"], 
                                 stdin=proc2.stdout, 
                                 stdout=subprocess.PIPE)
        out = proc3.stdout.readlines()
        count = len(out)
        if count <= 0:
            return False
        else:
            for line in out:
                self._logger.info(line)
            return True

    def run_consumer(self) -> subprocess:
        """Run consumer subprocess."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        consumer = subprocess.Popen(
                [
                    "python",
                    os.path.join(
                        current_dir,
                        "consumer.py"
                    )
                ]
            )
        self._logger.info(f"[PID {consumer.pid}]. Run: consumer.py")
        return consumer
