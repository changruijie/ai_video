"""
    OpenAI / DashScope / ComfyUI调用封装
"""
# -------------------- 占位 AI 客户端（未来替换真实 SDK） --------------------
class AIClient:
    """占位类：封装外部模型调用，生产环境请替换为真实实现（Stable Diffusion、TTS、DashScope 等）"""

    def generate_image_placeholder(self, text: str, out_path: Path, size=(1280, 720)) -> Path:
        # 生成占位图片，轻量且稳定
        logger.debug('AIClient.generate_image_placeholder -> %s', out_path)
        img = Image.new('RGB', size, color=(40, 40, 40))
        draw = ImageDraw.Draw(img)
        try:
        font = ImageFont.truetype('arial.ttf', 36)
        except Exception:
        font = ImageFont.load_default()
        # 简单换行
        max_chars = 30
        s = text.strip() or '镜头'
        lines = [s[i:i+max_chars] for i in range(0, len(s), max_chars)]
        total_h = sum(font.getsize(line)[1] + 6 for line in lines)
        y = (size[1] - total_h) // 2
        for line in lines:
        w, h = draw.textsize(line, font=font)
        x = (size[0] - w) // 2
        draw.text((x, y), line, fill=(230, 230, 230), font=font)
        y += h + 6
        out_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(out_path)
        return out_path


def synthesize_audio_placeholder(self, text: str, out_path: Path, duration_s: float):
    # 生成静音 wav，避免依赖 TTS 服务
    logger.debug('AIClient.synthesize_audio_placeholder -> %s', out_path)
    samplerate = 22050
    n_frames = int(duration_s * samplerate)
    n_channels = 1
    sampwidth = 2
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out_path), 'w') as wf:
    wf.setnchannels(n_channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(samplerate)
    silence = struct.pack('<h', 0) * n_frames
    wf.writeframes(silence)
    return out_path