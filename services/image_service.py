from utils.ai_client import AIClient

def render_scene(prompt: str) -> str:
    client = AIClient()
    return client.gen_image(prompt)
