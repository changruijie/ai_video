"""
    输入文本 -> 分镜 -> 音频/图片 -> 视频
"""
class VideoPipeline:
    def __init__(self, text_service: TextService, image_service: ImageService, audio_service: AudioService, video_service: VideoService):
        self.text_service = text_service
        self.image_service = image_service
        self.audio_service = audio_service
        self.video_service = video_service


    def run(self, task_id: int, text: str) -> Dict[str, Any]:
        logger.info('Pipeline started for task %s', task_id)
        shots = self.text_service.split_into_shots(text)
        storyboard = Storyboard(task_id, shots)


        # Render images
        for shot in storyboard.shots:
            self.image_service.render_shot(task_id, shot)


        # Synthesize narration
        audio_path = self.audio_service.synthesize_narration(task_id, storyboard.shots)


        # Compose final video
        try:
            video_path = self.video_service.compose_video(task_id, storyboard.shots, audio_path, fps=1)
            result_url = video_path.resolve().as_uri()
            logger.info('Pipeline finished for task %s, result=%s', task_id, result_url)
            return {'status': 'DONE', 'resultUrl': result_url, 'errorMsg': None}
        except Exception as e:
            logger.exception('Pipeline failed for task %s', task_id)
            return {'status': 'FAILED', 'resultUrl': None, 'errorMsg': str(e)}

class RabbitWorker:
    def __init__(self, pipeline: VideoPipeline, config: Config):
        self.pipeline = pipeline
        self.config = config
        self.params = pika.URLParameters(self.config.RABBIT_URL)
        self._stopped = False


    def _on_message(self, ch, method, properties, body):
        logger.info('Worker received message: %s', body)
        try:
            payload = json.loads(body.decode('utf-8'))
        except Exception as e:
            logger.exception('Invalid JSON payload: %s', e)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return


        task_id = payload.get('taskId') or int(time.time())
        text = payload.get('text') or self._fetch_text_from_backend(task_id) or ''


        try:
            result = self.pipeline.run(task_id, text)
            # 回调 Java 后端
            callback_url = f"{self.config.CALLBACK_BASE}/api/task/callback/{task_id}"
            try:
                headers = {'Content-Type': 'application/json'}n