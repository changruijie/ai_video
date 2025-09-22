from providers.base import ImageProvider, TTSProvider
from PIL import Image, ImageDraw
import os, numpy as np
from moviepy.editor import AudioClip

class MockImageProvider(ImageProvider):
    def generate_image(self, prompt: str, out_path: str, size: str = "1024x1024") -> str:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        w, h = map(int, size.split("x"))
        img = Image.new("RGB", (w, h), (80, 120, 180))
        d = ImageDraw.Draw(img); d.text((20, 20), prompt, fill=(255, 255, 255))
        img.save(out_path)
        return out_path

class MockTTSProvider(TTSProvider):
    def synthesize_speech(self, text: str, out_path: str, voice: str | None = None) -> str:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        duration = 2.5
        def make_frame(t):
            # 简单正弦波作为占位
            freq = 440
            return 0.05*np.sin(2*np.pi*freq*t)
        ac = AudioClip(make_frame, duration=duration, fps=44100)
        ac.write_audiofile(out_path, fps=44100, nbytes=2, bitrate="192k")
        return out_path
