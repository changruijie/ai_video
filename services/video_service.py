import os
from moviepy.editor import ImageClip, concatenate_videoclips
from utils.file_manager import ensure_dir

def stitch_images_to_video(image_paths: list[str], out_path: str, fps: int = 24, dur: float = 1.5) -> str:
    ensure_dir(os.path.dirname(out_path))
    clips = [ImageClip(p).set_duration(dur) for p in image_paths]
    video = concatenate_videoclips(clips, method="compose")
    video.write_videofile(out_path, fps=fps)
    return out_path
