import requests
from app.config import OMDB_API_KEY, BASE_URL


def search_movies(title):
    params = {
        "apikey": OMDB_API_KEY,
        "s": title
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()
    print(data)

    if data.get("Response") == "False":
        return []

    return data.get("Search", [])


def get_movie_details(imdb_id):
    params = {
        "apikey": OMDB_API_KEY,
        "i": imdb_id,
        "plot": "full"
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get("Response") == "False":
        return None

    return {
        "id": imdb_id,
        "title": data.get("Title"),
        "year": data.get("Year"),
        "overview": data.get("Plot"),
        "genre": data.get("Genre")
    }