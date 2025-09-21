from utils.ai_client import AIClient

def tts_line(text: str) -> str:
    client = AIClient()
    return client.tts(text)
