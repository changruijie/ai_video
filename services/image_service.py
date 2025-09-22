"""
image_service 只关心“我要一张图”，
至于是阿里万相还是别的模型，由 provider 决定。
"""
import os
from typing import Literal
from providers.ali_dashscope import AliImageProvider
from providers.mock import MockImageProvider

def get_image_provider(provider: Literal["ali", "mock"] = "ali"):
    # 统一入口；切换厂商只改这里的默认值或读取配置
    if provider == "ali":
        return AliImageProvider()
    return MockImageProvider()

def render_scene(prompt: str, out_path: str, size: str = "1024x1024", provider: str = "ali") -> str:
    """
    根据文本描述生成一张图片，保存到 out_path。
    - prompt: 文本提示词
    - size:   e.g., "1024x1024"
    - provider: "ali"（万相）或 "mock"
    """
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    p = get_image_provider(provider)
    return p.generate_image(prompt, out_path, size=size)
