"""
视频合成服务：
把多张图片合成一段视频，可选叠加一轨旁白音频。
"""
import os
from typing import List, Optional
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from utils.file_manager import ensure_dir

def stitch_images_to_video(
    image_paths: List[str],
    out_path: str,
    fps: int = 24,
    dur: float = 1.5,
    audio_path: Optional[str] = None
) -> str:
    ensure_dir(os.path.dirname(out_path))
    clips = [ImageClip(p).set_duration(dur) for p in image_paths]
    video = concatenate_videoclips(clips, method="compose")
    if audio_path and os.path.exists(audio_path):
        video = video.set_audio(AudioFileClip(audio_path))
    video.write_videofile(out_path, fps=fps)
    return out_path
