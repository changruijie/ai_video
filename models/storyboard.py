from pydantic import BaseModel
from typing import List, Optional

class Shot(BaseModel):
    idx: int
    description: str
    character: Optional[str] = None
    dialogue: Optional[str] = None

class Storyboard(BaseModel):
    title: str
    shots: List[Shot]
