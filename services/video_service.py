"""
    视频合成
"""
class VideoService:
    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager


    def compose_video(self, task_id: int, shots: List[Shot], audio_path: Optional[Path], fps: int = 1) -> Path:
        image_paths = [str(s.image_path) for s in shots if s.image_path]
        out = self.file_manager.task_dir(task_id) / 'result.mp4'
        logger.info('VideoService.compose_video -> %s, images=%d', out, len(image_paths))
        try:
            clip = ImageSequenceClip(image_paths, fps=fps)
            if audio_path and audio_path.exists() and audio_path.stat().st_size > 0:
                audio = AudioFileClip(str(audio_path))
                clip = clip.set_audio(audio)
            clip.write_videofile(str(out), codec='libx264', audio_codec='aac')
            clip.close()
            if audio_path and audio_path.exists():
                audio.close()
        except Exception as e:
            logger.exception('Video composition failed: %s', e)
            raise
        return out