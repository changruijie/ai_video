from fastapi import FastAPI, Query
from pipelines.video_pipeline import run_pipeline

app = FastAPI(title="AI Video Demo")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/generate")
def generate(topic: str = Query(..., description="视频主题/文案")):
    result = run_pipeline(topic)
    return result

# 启动：
# uvicorn app:app --reload --port 8000
