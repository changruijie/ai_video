## 1、项目框架
ai_video_project/
│── app.py                # 启动入口（FastAPI / Flask）
│── config.py             # 配置管理
│── requirements.txt      # 依赖
│
├── services/             # 业务服务层
│   ├── __init__.py
│   ├── text_service.py   # 文本相关：分镜生成、脚本处理
│   ├── audio_service.py  # TTS、语音合成
│   ├── image_service.py  # 角色/场景图生成
│   ├── video_service.py  # 视频合成
│
├── models/               # 数据模型层（DTO / 数据结构）
│   ├── __init__.py
│   ├── storyboard.py     # 分镜对象
│   ├── character.py      # 人物对象
│   ├── scene.py          # 场景对象
│
├── utils/                # 工具类（日志、文件管理、AI SDK 封装）
│   ├── __init__.py
│   ├── logger.py
│   ├── file_manager.py
│   ├── ai_client.py      # OpenAI / DashScope / ComfyUI 调用封装
│
├── pipelines/            # 工作流编排
│   ├── __init__.py
│   ├── video_pipeline.py # 从输入文本 -> 分镜 -> 音频/图片 -> 视频
│
└── tests/                # 单元测试
    ├── test_services.py
    ├── test_pipeline.py

## 2、框架说明
（1）单一职责：每个 service 负责一个 AI 功能模块（文本/音频/图像/视频）。
（2）模型抽象：models 中定义统一数据结构（比如 Storyboard 对象包含：镜头描述、角色、场景、对白），避免不同 AI 输出杂乱无章。
（3）工具层隔离：utils/ai_client.py 统一封装第三方 API 调用，未来替换供应商（OpenAI → 阿里云）只需改这里。
（4）流水线编排：pipelines/video_pipeline.py 把整个流程（文本→分镜→图片→TTS→视频）打通，作为 MVP 交付核心。
（5）可扩展性：以后要加字幕、背景音乐，只需新增 service 并在 pipeline 里接入