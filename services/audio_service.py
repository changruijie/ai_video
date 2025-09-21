"""
    音频处理
"""

class AudioService:
    def __init__(self, ai_client: AIClient, file_manager: FileManager):
        self.ai_client = ai_client
        self.file_manager = file_manager


    def synthesize_narration(self, task_id: int, shots: List[Shot]) -> Path:
        total_duration = max(1.0, sum(s.duration for s in shots))
        out = self.file_manager.task_dir(task_id) / 'narration.wav'
        path = self.ai_client.synthesize_audio_placeholder(' '.join(s.text for s in shots), out, total_duration)
        logger.info('AudioService.synthesize_narration -> %s', path)
        return path