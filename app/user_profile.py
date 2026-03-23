import json
import os

from app.config import USER_FILE


def load_user():
    if not os.path.exists(USER_FILE):
        return {"user_id": 1, "library": [], "ratings": {}}

    with open(USER_FILE, "r") as f:
        user = json.load(f)

    if "library" not in user:
        user["library"] = []
    if "ratings" not in user:
        user["ratings"] = {}

    fixed_library = []
    for item in user["library"]:
        if isinstance(item, dict):
            fixed_library.append(item)

    user["library"] = fixed_library

    return user


def save_user(user):
    os.makedirs("data", exist_ok=True)

    with open(USER_FILE, "w") as f:
        json.dump(user, f, indent=2)


def add_to_library(movie):
    user = load_user()
    library = user.get("library", [])

    # защита от дублей
    if any(m["title"] == movie["title"] for m in library):
        print("Already in library")
        return

    library.append({
        "id": movie.get("id"),
        "title": movie.get("title"),
        "year": movie.get("year"),
        "overview": movie.get("overview"),
        "genre": movie.get("genre")
    })

    user["library"] = library
    save_user(user)


def add_rating(movie_title, rating):
    user = load_user()

    try:
        rating = float(rating)
    except ValueError:
        print("Invalid rating")
        return

    user["ratings"][movie_title] = rating

    save_user(user)


def get_user_data():
    return load_user()