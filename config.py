"""
    配置管理
"""
import os
import json
import time
import threading
import logging
import wave
import struct
import re
from pathlib import Path
from typing import Dict, Any, List, Optional


import pika
import requests
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip, AudioFileClip


# -------------------- 配置类 --------------------
class Config:
    RABBIT_URL: str = os.getenv('RABBIT_URL', 'amqp://guest:guest@localhost:5672/')
    RABBIT_QUEUE: str = os.getenv('RABBIT_QUEUE', 'aivideo.task.queue')
    CALLBACK_BASE: str = os.getenv('CALLBACK_BASE', 'http://localhost:8080')
    OUTPUT_DIR: Path = Path(os.getenv('OUTPUT_DIR', './outputs'))
    START_RABBIT_WORKER: bool = os.getenv('START_RABBIT_WORKER', 'true').lower() in ('1', 'true', 'yes')
    DEFAULT_SHOT_DURATION: float = float(os.getenv('DEFAULT_SHOT_DURATION', '2.0'))

# -------------------- 日志配置 --------------------
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')
logger = logging.getLogger('ai_video_oop')


# 确保输出目录存在
Config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------- 数据模型 --------------------
class Shot:
    def __init__(self, index: int, text: str, duration: float):
    self.index = index
    self.text = text
    self.duration = duration
    self.image_path: Optional[Path] = None


def to_dict(self):
    return {'index': self.index, 'text': self.text, 'duration': self.duration, 'image': str(self.image_path) if self.image_path else None}




class Storyboard:
    def __init__(self, task_id: int, shots: List[Shot]):
    self.task_id = task_id
    self.shots = shots


def to_dict(self):
    return {'task_id': self.task_id, 'shots': [s.to_dict() for s in self.shots]}




# -------------------- 工具：文件管理 --------------------
class FileManager:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)


def task_dir(self, task_id: int) -> Path:
    p = self.base_dir / str(task_id)
    p.mkdir(parents=True, exist_ok=True)
    return p