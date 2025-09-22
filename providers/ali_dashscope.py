from typing import Optional
import os
from providers.base import ImageProvider, TTSProvider
from config import settings
from utils.logger import logger

# DashScope SDK（阿里万相/通义）：
# pip install dashscope
try:
    from dashscope import ImageSynthesis  # 万相图像
    import dashscope
except Exception as e:
    ImageSynthesis = None
    logger.warning("dashscope SDK 未安装或导入失败：%s", e)

class AliImageProvider(ImageProvider):
    """阿里万相 图片生成。"""

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.DASHSCOPE_API_KEY
        self.model = model or settings.ALI_IMAGE_MODEL
        if not self.api_key:
            raise RuntimeError("DASHSCOPE_API_KEY 未配置，请在 .env 中设置。")

        # 设置全局 key（SDK 要求）
        if 'dashscope' in globals():
            dashscope.api_key = self.api_key

    def generate_image(self, prompt: str, out_path: str, size: str = "1024x1024") -> str:
        """
        调用万相生图接口：
        - prompt: 文本描述
        - size:   例如 "1024x1024" / "720x1280"
        - out_path: 图片保存路径
        """
        if ImageSynthesis is None:
            raise RuntimeError("未找到 dashscope SDK，请先 pip install dashscope")

        logger.info(f"[ALI-WANXIANG] prompt={prompt}, size={size}")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        # 注意：不同版本 SDK 或模型参数名可能略有差异，
        # 这里提供一个通用调用方式，具体可按你账号支持的模型微调。
        rsp = ImageSynthesis.call(
            model=self.model,
            prompt=prompt,
            size=size,
            n=1,            # 生成张数
            # style='photorealistic',  # 如模型支持，也可传风格
            # seed=12345,             # 可重复性
        )

        # 解析返回，保存第一张到 out_path
        # 一般 rsp.output[0].image_url 或 rsp.output[0].b64_image
        # 这里给出两种兼容示例：
        if hasattr(rsp, "output") and rsp.output and hasattr(rsp.output[0], "image_url"):
            # 方式一：返回 URL，下载保存
            import requests
            img_url = rsp.output[0].image_url
            with requests.get(img_url, stream=True) as r:
                r.raise_for_status()
                with open(out_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
        elif hasattr(rsp, "output") and rsp.output and hasattr(rsp.output[0], "b64_image"):
            # 方式二：返回 base64，解码保存
            import base64
            img_b64 = rsp.output[0].b64_image
            with open(out_path, "wb") as f:
                f.write(base64.b64decode(img_b64))
        else:
            raise RuntimeError(f"万相返回结构不符合预期：{rsp}")

        logger.info(f"[ALI-WANXIANG] saved: {out_path}")
        return out_path


class AliTTSProvider(TTSProvider):
    """
    阿里语音合成占位。你可以：
    1）接阿里云 NLS 语音合成（需要另装 SDK/配置 APPKEY）
    2）暂时返回一个 mock 文件
    这里先给出简单 mock，方便流程跑通。
    """

    def synthesize_speech(self, text: str, out_path: str, voice: Optional[str] = None) -> str:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        # TODO: 如接入 NLS，这里替换为真实 TTS
        # 现在用纯静音 + 打印日志占位
        from moviepy.editor import AudioClip
        import numpy as np

        duration = max(2.0, min(len(text) * 0.08, 30.0))  # 文本长度估算时长
        def make_frame(t):
            return np.zeros((1,), dtype=np.float32)  # 静音

        ac = AudioClip(make_frame, duration=duration, fps=44100)
        ac.write_audiofile(out_path, fps=44100, nbytes=2, bitrate="192k")
        logger.info(f"[ALI-TTS-MOCK] generated silent audio: {out_path}")
        return out_path
