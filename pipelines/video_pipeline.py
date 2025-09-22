# pipelines/video_pipeline.py
import os
from typing import Literal
from services.text_service import make_storyboard
from services.image_service import render_scene
from services.audio_service import tts_line
from services.video_service import stitch_images_to_video
from utils.file_manager import ensure_dir

def run_pipeline(
    topic: str,
    workdir: str = "data/output",
    provider: Literal["ali", "mock"] = "ali",
    with_tts: bool = False
) -> dict:
    """
    整体流水线：
    1) 文本→分镜
    2) 逐镜生图（默认阿里万相）
    3) 可选：合成旁白
    4) 合成视频
    """
    ensure_dir(workdir)

    # 1) 分镜
    sb = make_storyboard(topic, n_shots=4)

    # 2) 对每个镜头生成图片
    images = []
    for shot in sb.shots:
        img_path = os.path.join(workdir, f"{topic}_shot_{shot.idx}.png")
        prompt = shot.description
        images.append(render_scene(prompt, img_path, size="1024x1024", provider=provider))

    # 3) 可选：旁白（把分镜合成一段旁白文本）
    audio = None
    if with_tts:
        all_text = "；".join([s.description for s in sb.shots])
        audio = os.path.join(workdir, f"{topic}_narration.mp3")
        tts_line(all_text, audio)

    # 4) 合成视频
    out_video = os.path.join(workdir, f"{topic}_demo.mp4")
    stitch_images_to_video(images, out_video, fps=24, dur=1.2, audio_path=audio)

    return {
        "title": sb.title,
        "shots": [s.model_dump() for s in sb.shots],
        "images": images,
        "video": out_video
    }
