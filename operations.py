from models import VideoGame, Review
from typing import List

def get_active_games(games: List[VideoGame]) -> List[VideoGame]:
    return [g for g in games if not g.is_deleted]

def find_game_by_title(games: List[VideoGame], title: str) -> List[VideoGame]:
    return [g for g in games if title.lower() in g.title.lower() and not g.is_deleted]

def filter_by_genre(games: List[VideoGame], genre: str) -> List[VideoGame]:
    return [g for g in games if g.genre.lower() == genre.lower() and not g.is_deleted]

def soft_delete_game(games: List[VideoGame], game_id: int) -> bool:
    for g in games:
        if g.id == game_id:
            g.is_deleted = True
            return True
    return False
