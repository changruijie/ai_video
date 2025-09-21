from utils.ai_client import AIClient
from models.storyboard import Storyboard, Shot

def make_storyboard(topic: str, n_shots: int = 4) -> Storyboard:
    client = AIClient()
    shots = [Shot(idx=i+1, description=f"{topic} - 场景 {i+1}") for i in range(n_shots)]
    return Storyboard(title=topic, shots=shots)
