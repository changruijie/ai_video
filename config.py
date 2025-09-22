# config.py
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # 运行目录
    WORK_DIR: str = Field(default="data")
    TMP_DIR: str = Field(default="data/tmp")
    OUTPUT_DIR: str = Field(default="data/output")

    # ===== 阿里 DashScope（万相/通义）配置 =====
    # 控制台获取的 API Key（注意不要提交到仓库）
    DASHSCOPE_API_KEY: str | None = Field(default=None)

    # 万相图像模型名（示例，具体以你账号支持的模型为准）
    # 可选：'wanx-v1' / 'wanx2.1' / 'wanx-style' ...
    ALI_IMAGE_MODEL: str = Field(default="wanx-v1")

    # 语音合成（若走阿里云 NLS，通常需要另一个 AK/SK/APPKEY；这里先占位）
    ALI_TTS_ENABLED: bool = Field(default=False)
    ALI_TTS_VOICE: str = Field(default="zhixiaoyun")   # 示例音色，占位
    ALI_TTS_SPEECH_RATE: int = Field(default=0)        # 语速（-500~500，占位）
    ALI_TTS_PITCH_RATE: int = Field(default=0)         # 音调

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
