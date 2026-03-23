from app.omdb_api import search_movies, get_movie_details
from app.cache import add_movie
from app.user_profile import add_to_library, add_rating, get_user_data
from app.recommender import Recommender

# import time

def shorten(text, max_len=200):
    return text[:max_len] + "..." if text and len(text) > max_len else text


def print_movie(movie):
    print("\n" + "=" * 50)
    print(f"Title: {movie['title']}")
    print(f"Year: {movie['year']}")
    print(f"Genre: {movie['genre']}")
    print(f"Overview: {shorten(movie['overview'])}")


def print_recommendations(recs):
    print("\n=== Recommendations ===")

    if not recs:
        print("No recommendations found")
        return

    for r in recs:
        print("\n" + "-" * 40)
        print(f"Title: {r['title']} ({r['year']})")
        print(f"Genre: {r['genre']}")
        print(f"Overview: {shorten(r['overview'])}")


def main():
    print("=== Movie Recommender CLI ===")

    while True:
        user_data = get_user_data()
        print(f"\nYour library: {len(user_data['library'])} movies")
        print(f"Rated movies: {len(user_data['ratings'])}")

        query = input("\nEnter movie name (or '0' to exit): ")

        if query == "0":
            break

        results = search_movies(query)

        if not results:
            print("No movies found")
            continue

        print("\nFound movies:")

        for i, movie in enumerate(results[:10]):
            print(f"{i+1}. {movie['Title']} ({movie['Year']})")

        try:
            choice = int(input("Select movie number: ")) - 1
            selected = results[choice]
        except:
            print("Invalid choice")
            continue

        movie_details = get_movie_details(selected["imdbID"])

        if not movie_details:
            print("Error loading movie")
            continue

        print_movie(movie_details)

        # добавление в библиотеку
        add = input("\nAdd to library? (y/n): ").lower()

        if add == "y":
            add_to_library(movie_details)
            add_movie(movie_details)
            print("Added to library!")

        # оценка
        rate = input("Rate this movie (0.5-5.0) or Enter to skip: ")

        try:
            rate_float = float(rate)
            if 0.5 <= rate_float <= 5.0:
                add_rating(movie_details["title"], rate_float)
                print("Rating saved!")
            else:
                print("Invalid rating, must be between 0.5 and 5.0")
        except ValueError:
            if rate.strip() != "":
                print("Invalid input, skipped")

        # обновление модель
        recommender = Recommender()

        # рекомендации
        recs = recommender.recommend(movie_details["title"])
        print_recommendations(recs)

        # time.sleep(0.2)


if __name__ == "__main__":
    main()