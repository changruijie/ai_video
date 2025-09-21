"""
    文本相关：分镜生成、脚本处理
"""
class TextService:
    def __init__(self, ai_client: AIClient):
        self.ai_client = ai_client


    def split_into_shots(self, text: str, max_shots: int = 12) -> List[Shot]:
        if not text:
            return [Shot(0, '镜头：空白', Config.DEFAULT_SHOT_DURATION)]
        parts = re.split(r'[。.!?；;\n]+', text)
        shots_texts = [p.strip() for p in parts if p.strip()]
        shots_texts = shots_texts[:max_shots]
        shots = [Shot(i, s, Config.DEFAULT_SHOT_DURATION) for i, s in enumerate(shots_texts)]
        logger.debug('TextService.split_into_shots -> %d shots', len(shots))
        return shots