from typing import Dict, Any

class AIClient:
    def __init__(self, provider: str = "mock", **kwargs):
        self.provider = provider
        self.kwargs = kwargs

    def gen_text(self, prompt: str) -> str:
        # TODO: 接入 OpenAI / DashScope / 自建服务
        return f"[MOCK-TEXT] {prompt}"

    def gen_image(self, prompt: str, size: str = "512x512") -> str:
        # 返回伪路径或URL
        return f"file://fake_image_{hash(prompt)%10000}.png"

    def tts(self, text: str) -> str:
        return f"file://fake_audio_{hash(text)%10000}.wav"
