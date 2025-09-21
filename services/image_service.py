"""
    角色、场景图生成
"""
class ImageService:
    def __init__(self, ai_client: AIClient, file_manager: FileManager):
        self.ai_client = ai_client
        self.file_manager = file_manager


    def render_shot(self, task_id: int, shot: Shot) -> Path:
        out = self.file_manager.task_dir(task_id) / f'shot_{shot.index}.png'
        path = self.ai_client.generate_image_placeholder(shot.text, out)
        shot.image_path = path
        logger.info('ImageService.render_shot -> %s', path)
        return path