"""Screen recorder using mss + OpenCV — captures frames in a background thread."""

import logging
import threading
import time
from datetime import datetime
from pathlib import Path

import cv2
import mss
import numpy as np

from utils.config import Config

logger = logging.getLogger(__name__)


class VideoRecorder:
    """Captures the primary monitor at ~N FPS and writes an MP4 on stop."""

    def __init__(self) -> None:
        self._running = False
        self._thread: threading.Thread | None = None
        self._output_path: str = ""

    def start(self) -> str:
        """Begin recording. Returns the planned output file path."""
        video_dir = Path(Config.VIDEO_DIR)
        video_dir.mkdir(parents=True, exist_ok=True)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._output_path = str(video_dir / f"test_run_{ts}.mp4")
        self._running = True
        self._thread = threading.Thread(target=self._capture_loop, daemon=True)
        self._thread.start()
        logger.info("Video recording started → %s", self._output_path)
        return self._output_path

    def stop(self) -> str:
        """Stop recording and finalise the MP4 file."""
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=10)
        logger.info("Video recording stopped → %s", self._output_path)
        return self._output_path

    def _capture_loop(self) -> None:
        """Internal loop that grabs screenshots and writes frames."""
        fps = Config.VIDEO_FPS
        interval = 1.0 / fps
        writer: cv2.VideoWriter | None = None

        try:
            with mss.mss() as sct:
                monitor = sct.monitors[1]  # primary monitor
                while self._running:
                    t0 = time.monotonic()
                    img = sct.grab(monitor)
                    frame = np.array(img)
                    # mss returns BGRA — convert to BGR for OpenCV
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                    if writer is None:
                        h, w, _ = frame.shape
                        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                        writer = cv2.VideoWriter(self._output_path, fourcc, fps, (w, h))
                        logger.info("Video writer initialised: %dx%d @ %d FPS", w, h, fps)

                    writer.write(frame)
                    elapsed = time.monotonic() - t0
                    sleep_time = max(0, interval - elapsed)
                    if sleep_time > 0:
                        time.sleep(sleep_time)
        except Exception:
            logger.exception("Video capture error")
        finally:
            if writer is not None:
                writer.release()
                logger.info("Video file finalised: %s", self._output_path)
