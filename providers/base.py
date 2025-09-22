# 定义所有“能力”的抽象接口，service 只依赖它而不是某个厂商 SDK
from abc import ABC, abstractmethod
from typing import Optional

class ImageProvider(ABC):
    @abstractmethod
    def generate_image(self, prompt: str, out_path: str, size: str = "1024x1024") -> str:
        """根据文本 prompt 生成图片，保存到 out_path，返回文件路径。"""
        raise NotImplementedError

class TTSProvider(ABC):
    @abstractmethod
    def synthesize_speech(self, text: str, out_path: str, voice: Optional[str] = None) -> str:
        """把文本转语音，保存到 out_path，返回文件路径。"""
        raise NotImplementedError
