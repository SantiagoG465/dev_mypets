
from pydantic import BaseModel
from typing import Optional

class VideoGame(BaseModel):
    id: int
    title: str
    genre: str
    platform: str
    rating: float
    is_deleted: bool = False



#
class Review(BaseModel):
    id: int
    game_id: int
    reviewer: str
    score: float
    comment: str

