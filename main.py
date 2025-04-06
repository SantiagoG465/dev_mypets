from fastapi import FastAPI, HTTPException
from models import VideoGame, Review
from utils import read_csv, write_csv
from typing import List

app = FastAPI()

# Archivos CSV para persistencia
VIDEO_CSV = "database/videogames.csv"
REVIEW_CSV = "database/reviews.csv"

# Cargar videojuegos
games: List[VideoGame] = read_csv(VIDEO_CSV, VideoGame)

#  Precargar 5 videojuegos si el CSV está vacío
if not games:
    games = [
        VideoGame(id=1, title="The Legend of Zelda: Breath of the Wild", genre="Adventure", platform="Switch", rating=9.7, is_deleted=False),
        VideoGame(id=2, title="God of War Ragnarok", genre="Action", platform="PS5", rating=9.5, is_deleted=False),
        VideoGame(id=3, title="Elden Ring", genre="RPG", platform="PC", rating=9.3, is_deleted=False),
        VideoGame(id=4, title="Hades", genre="Roguelike", platform="PC", rating=9.0, is_deleted=False),
        VideoGame(id=5, title="Hollow Knight", genre="Metroidvania", platform="PC", rating=9.2, is_deleted=False),
    ]
    write_csv(VIDEO_CSV, games)

# Cargar reseñas
reviews: List[Review] = read_csv(REVIEW_CSV, Review)

#  Endpoints de videojuegos
@app.post("/videogames", response_model=VideoGame)
def create_game(game: VideoGame):
    games.append(game)
    write_csv(VIDEO_CSV, games)
    return game\

@app.get("/videogames/search")
def search_by_title(title: str):
    results = [g for g in games if title.lower() in g.title.lower()]
    if not results:
        raise HTTPException(status_code=404, detail="No matching games found")
    return results
@app.get("/videogames/filter/genre/{genre}")
def filter_by_genre(genre: str):
    filtered = [g for g in games if g.genre.lower() == genre.lower()]
    if not filtered:
        raise HTTPException(status_code=404, detail="No games found for that genre")
    return filtered

@app.get("/videogames", response_model=List[VideoGame])
def get_all_games():
    return [g for g in games if not g.is_deleted]

@app.get("/videogames/{game_id}", response_model=VideoGame)
def get_game(game_id: int):
    for game in games:
        if game.id == game_id and not game.is_deleted:
            return game
    raise HTTPException(status_code=404, detail="Game not found or deleted")

@app.delete("/videogames/{game_id}")
def soft_delete_game(game_id: int):
    for game in games:
        if game.id == game_id:
            game.is_deleted = True
            write_csv(VIDEO_CSV, games)
            return {"message": f"Game {game.title} marked as deleted"}
    raise HTTPException(status_code=404, detail="Game not found")

# ✍️ Endpoints de reseñas
@app.post("/reviews", response_model=Review)
def create_review(review: Review):
    reviews.append(review)
    write_csv(REVIEW_CSV, reviews)
    return review

@app.get("/reviews", response_model=List[Review])
def get_all_reviews():
    return reviews

@app.get("/reviews/game/{game_id}", response_model=List[Review])
def get_reviews_for_game(game_id: int):
    return [r for r in reviews if r.game_id == game_id]

# 🧪 Endpoint raíz
@app.get("/")
def root():
    return {"message": "API de comparación de videojuegos"}
