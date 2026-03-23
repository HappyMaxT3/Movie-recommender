import json
import os
import re

from app.config import CACHE_FILE


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return []

    with open(CACHE_FILE, "r") as f:
        return json.load(f)


def save_cache(movies):
    with open(CACHE_FILE, "w") as f:
        json.dump(movies, f, indent=2, ensure_ascii=False)


# привести к одному виду
def clean_title(title):
    return re.sub(r"\(\d{4}\)", "", title).strip()

def normalize_title(title):
    return clean_title(title).lower().strip()


def movie_exists(new_movie, movies):
    new_title = normalize_title(new_movie["title"])
    new_year = str(new_movie["year"])

    for m in movies:
        existing_title = normalize_title(m["title"])
        existing_year = str(m["year"])

        if existing_title == new_title and existing_year == new_year:
            return True

    return False


def add_movie(movie):
    movies = load_cache()

    if movie_exists(movie, movies):
        return

    movies.append(movie)
    save_cache(movies)