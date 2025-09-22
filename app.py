from fastapi import FastAPI, Query
from pipelines.video_pipeline import run_pipeline

app = FastAPI(title="AI Video (Ali Wanxiang Ready)")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/generate")
def generate(
    topic: str = Query(..., description="视频主题/文案"),
    provider: str = Query("ali", description="生图提供商：ali/mock"),
    with_tts: bool = Query(False, description="是否合成旁白")
):
    """
    通过 provider 参数可以快速切到 mock，不走外网（本地开发时很有用）。
    """
    result = run_pipeline(topic, provider=provider, with_tts=with_tts)
    return result

# 启动： uvicorn app:app --reload --port 8000
