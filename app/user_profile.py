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

    return user


def save_user(user):
    os.makedirs("data", exist_ok=True)

    with open(USER_FILE, "w") as f:
        json.dump(user, f, indent=2)


def add_to_library(movie):
    user = load_user()

    if movie["title"] not in user["library"]:
        user["library"].append(movie["title"])

    save_user(user)


def add_rating(movie_title, rating):
    user = load_user()

    user["ratings"][movie_title] = float(rating)

    save_user(user)


def get_user_data():
    return load_user()