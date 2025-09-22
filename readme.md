## 1、项目框架
app.py                  # FastAPI 入口
config.py               # 读取环境变量/配置
models/                 # pydantic 数据模型
  └─ storyboard.py
pipelines/
  └─ video_pipeline.py  # 业务流水线（只调 service，不关心底层厂商）
providers/              # 各厂商适配器（新建）
  ├─ base.py            # 统一接口定义（抽象类）
  ├─ ali_dashscope.py   # 阿里万相(图片) / 阿里TTS(可选)
  └─ mock.py            # 本地占位，便于离线开发
services/               # 领域服务（纯业务）
  ├─ text_service.py    # 文案/分镜
  ├─ image_service.py   # 生图（调用 providers）
  ├─ audio_service.py   # TTS（调用 providers）
  └─ video_service.py   # 合成视频（moviepy）
utils/
  ├─ logger.py
  └─ file_manager.py


## 2、框架说明
(1)providers/base.py 定义能力接口（generate_image、synthesize_speech），任何厂商只要实现它们，就能被 services/* 调用。
(2)services/* 只管“要一张图/一段音频”，不关心“怎么要”。
(3)pipelines/* 串起来：拿分镜→对每个镜头要图→可选要旁白→把所有素材合成视频。