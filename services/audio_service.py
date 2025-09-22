"""
音频服务（TTS）。同样通过 provider 解耦。
"""
from typing import Literal
from providers.ali_dashscope import AliTTSProvider
from providers.mock import MockTTSProvider
from config import settings

def get_tts_provider(provider: Literal["ali", "mock"] = "mock"):
    # 如果你在 .env 开启了 ALI_TTS_ENABLED，就默认选 ali
    if settings.ALI_TTS_ENABLED:
        return AliTTSProvider()
    # 否则默认 mock，避免因为没配好 TTS 而阻塞流程
    return MockTTSProvider()

def tts_line(text: str, out_path: str, provider: str | None = None) -> str:
    p = get_tts_provider()
    return p.synthesize_speech(text, out_path)
