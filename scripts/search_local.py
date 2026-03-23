import json
import re

from app.user_profile import add_rating, get_user_ratings
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


def shorten(text, max_len=200):
    return text[:max_len] + "..." if len(text) > max_len else text


def print_movie(movie):
    print("\n" + "=" * 50)
    print(f"Title: {movie['title']}")
    print(f"Year: {movie['year']}")
    print(f"Genre: {movie['genre']}")
    print(f"Overview: {shorten(movie['overview'])}")


def main():
    movies = load_movies()
    recommender = Recommender()

    ratings = get_user_ratings()
    print(f"=== Local Movie Search ===")
    print(f"Loaded {len(ratings)} rated movies")

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

        # оценка
        rate = input("\nRate this movie (1-5) or press Enter to skip: ")

        if rate.isdigit():
            rate = int(rate)
            if 1 <= rate <= 5:
                add_rating(selected["title"], rate)
                print("Rating saved!")
            else:
                print("Invalid rating")

        print("\n=== Recommendations ===")
        recs = recommender.recommend(selected["title"])

        if not recs:
            print("No recommendations found")
            continue

        for r in recs:
            print("\n" + "-" * 40)
            print(f"Title: {r['title']} ({r['year']})")
            print(f"Genre: {r['genre']}")
            print(f"Overview: {shorten(r['overview'])}")

if __name__ == "__main__":
    main()