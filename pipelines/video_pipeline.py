import os
from services.text_service import make_storyboard
from services.image_service import render_scene
from services.video_service import stitch_images_to_video
from utils.file_manager import ensure_dir

def run_pipeline(topic: str, workdir: str = "data/output") -> dict:
    ensure_dir(workdir)

    # 1) 文本 → 分镜
    sb = make_storyboard(topic, n_shots=4)

    # 2) 为每个镜头生成一张占位图（真实项目这里调用你的图生模型）
    imgs = []
    for shot in sb.shots:
        # mock：用纯色图占位，实际应保存 render_scene 的图片结果
        path = os.path.join(workdir, f"shot_{shot.idx}.png")
        if not os.path.exists(path):
            # 简单占位：生成 640x360 纯色图
            from PIL import Image, ImageDraw
            im = Image.new("RGB", (640, 360), (30*shot.idx % 255, 80, 140))
            d = ImageDraw.Draw(im); d.text((20,20), shot.description, fill=(255,255,255))
            im.save(path)
        imgs.append(path)

    # 3) 合成视频
    out_video = os.path.join(workdir, f"{topic}_demo.mp4")
    stitch_images_to_video(imgs, out_video, fps=24, dur=1.2)

    return {"title": sb.title, "shots": [s.model_dump() for s in sb.shots], "video": out_video, "images": imgs}
