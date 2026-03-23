import json
import re
from app.recommender import Recommender

from app.config import CACHE_FILE

def clean_title(title):
    return re.sub(r"\(\d{4}\)", "", title).strip()


def normalize(text):
    text = clean_title(text)
    return re.sub(r"[^a-zA-Z0-9 ]", "", text).lower().strip()


def load_movies():
    with open(CACHE_FILE, "r") as f:
        return json.load(f)


def search_movies(query, movies):
    query = normalize(query)

    results = []

    for movie in movies:
        title = normalize(movie["title"])

        if query in title:
            results.append(movie)

    return results


def print_movie(movie):
    print("\n" + "=" * 50)
    print(f"Title: {movie['title']}")
    print(f"Year: {movie['year']}")
    print(f"Genre: {movie['genre']}")
    print(f"Overview: {movie['overview']}")


def main():
    movies = load_movies()
    recommender = Recommender()

    print("=== Local Movie Search ===")

    while True:
        query = input("\nEnter movie name (or '0' to exit): ")

        if query == "0":
            break

        results = search_movies(query, movies)

        if not results:
            print("No movies found")
            continue

        print(f"\nFound {len(results)} movies:")

        for i, movie in enumerate(results):
            print(f"{i+1}. {movie['title']} ({movie['year']})")

        try:
            choice = int(input("Select movie number: ")) - 1
            selected = results[choice]
        except:
            print("Invalid choice")
            continue

        print_movie(selected)

        print("\n=== Recommendations ===")
        recs = recommender.recommend(selected["title"])

        if not recs:
            print("No recommendations found")
            continue

        for r in recs:
            print(f"- {r['title']} ({r['year']}) | {r['genre']} \n--- {r['overview']}")


if __name__ == "__main__":
    main()