"""
文本/分镜服务：
当前给出一个最简实现：根据主题生成固定数量的镜头。
后续可以替换为 LLM 生成（例如 DashScope 的 Qwen 模型）。
"""
from models.storyboard import Storyboard, Shot

def make_storyboard(topic: str, n_shots: int = 4) -> Storyboard:
    shots = [Shot(idx=i+1, description=f"{topic} - 场景 {i+1}") for i in range(n_shots)]
    return Storyboard(title=topic, shots=shots)
