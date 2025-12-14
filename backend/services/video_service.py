"""Video Service - Video creation and processing."""

import os
import subprocess
from typing import List
import cv2

from ..config import AUDIO_DIR, OUTPUT_DIR, VIDEO_DIR


def images_to_video(image_list: List[str], video_path: str, fps: int = 24):
    """Create video from list of image paths."""
    if not image_list:
        raise ValueError("No images provided")
    
    frame = cv2.imread(image_list[0])
    if frame is None:
        raise ValueError(f"Cannot read image: {image_list[0]}")
    
    height, width, _ = frame.shape
    video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    
    for img_path in image_list:
        frame = cv2.imread(img_path)
        if frame is not None:
            video.write(frame)
    
    video.release()
    cv2.destroyAllWindows()
    print(f"[images_to_video] Created: {video_path}")


def merge_video_audio(video_path: str, audio_path: str, output_path: str):
    """Merge video and audio using ffmpeg with H.264 codec for browser compatibility."""
    # Re-encode to H.264 (libx264) which is browser-compatible
    command = (
        f'ffmpeg -y -i "{video_path}" -i "{audio_path}" '
        f'-c:v libx264 -preset fast -crf 23 -pix_fmt yuv420p '
        f'-c:a aac -b:a 128k "{output_path}"'
    )
    subprocess.run(command, shell=True, check=True)
    print(f"[merge_video_audio] Created: {output_path}")


def cleanup_files(video_id: str):
    """Clean up temporary files."""
    for f in AUDIO_DIR.glob(f"audio_{video_id}_*.flac"):
        f.unlink()
    
    for f in OUTPUT_DIR.glob(f"*_{video_id}_*.png"):
        f.unlink()
    for f in OUTPUT_DIR.glob(f"char_*_{video_id}.png"):
        f.unlink()
    
    print(f"[cleanup_files] Cleaned up files for {video_id}")
