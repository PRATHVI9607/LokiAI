"""
MediaConverter — convert video/audio files using ffmpeg.
ffmpeg must be installed and on PATH.
"""

import logging
import shutil
import subprocess
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

AUDIO_FORMATS = {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma", ".opus"}
VIDEO_FORMATS = {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".ts"}
IMAGE_FORMATS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".svg"}


class MediaConverter:
    def __init__(self):
        self._ffmpeg = shutil.which("ffmpeg")

    def _check_ffmpeg(self) -> bool:
        return self._ffmpeg is not None

    def convert(self, input_path: str, output_format: str,
                output_path: Optional[str] = None, quality: str = "medium") -> dict:
        """Convert a media file to a different format."""
        if not self._check_ffmpeg():
            return {
                "success": False,
                "message": "ffmpeg is not installed. Install it from https://ffmpeg.org/download.html and add to PATH.",
            }

        src = Path(input_path).expanduser().resolve()
        if not src.exists():
            return {"success": False, "message": f"File not found: {src}"}

        ext = output_format.lower().strip(".")
        if output_path:
            dst = Path(output_path).expanduser().resolve()
        else:
            dst = src.with_suffix(f".{ext}")

        if dst == src:
            return {"success": False, "message": "Input and output are the same file."}

        # Quality presets
        quality_flags: list[str] = []
        src_ext = src.suffix.lower()
        if src_ext in VIDEO_FORMATS or f".{ext}" in VIDEO_FORMATS:
            quality_map = {"low": ["-crf", "28"], "medium": ["-crf", "23"], "high": ["-crf", "18"]}
            quality_flags = quality_map.get(quality, quality_map["medium"])

        cmd = [self._ffmpeg, "-i", str(src), "-y"] + quality_flags + [str(dst)]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if result.returncode != 0:
                err = result.stderr[-300:] if result.stderr else "Unknown error"
                return {"success": False, "message": f"Conversion failed: {err}"}
            size_mb = round(dst.stat().st_size / 1048576, 2)
            return {
                "success": True,
                "message": f"Converted to {dst.name} ({size_mb} MB).",
                "data": {"input": str(src), "output": str(dst), "size_mb": size_mb},
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "message": "Conversion timed out (> 5 minutes)."}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def get_info(self, file_path: str) -> dict:
        """Get media file metadata using ffprobe."""
        if not self._check_ffmpeg():
            return {"success": False, "message": "ffmpeg not installed."}
        probe = shutil.which("ffprobe")
        if not probe:
            return {"success": False, "message": "ffprobe not found."}
        src = Path(file_path).expanduser().resolve()
        if not src.exists():
            return {"success": False, "message": f"File not found: {src}"}
        try:
            result = subprocess.run(
                [probe, "-v", "quiet", "-print_format", "json", "-show_streams", "-show_format", str(src)],
                capture_output=True, text=True, timeout=10,
            )
            return {"success": True, "message": f"Media info for {src.name}", "data": {"json": result.stdout}}
        except Exception as e:
            return {"success": False, "message": str(e)}
