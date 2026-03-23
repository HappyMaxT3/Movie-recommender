from app.omdb_api import search_movies, get_movie_details
from app.cache import add_movie
from app.user_profile import add_to_library, add_rating, get_user_data
from app.recommender import Recommender


def shorten(text, max_len=200):
    # return text[:max_len] + "..." if text and len(text) > max_len else text
    return text


def print_movie(movie):
    print("\n" + "=" * 50)
    print(f"Title: {movie['title']}")
    print(f"Year: {movie['year']}")
    print(f"Genre: {movie['genre']}")
    print(f"Overview: {shorten(movie['overview'])}")


def print_user_library(user_data):
    print("\n=== Your Library ===")

    library = user_data.get("library", [])
    ratings = user_data.get("ratings", {})

    if not library:
        print("Library is empty")
        return

    for i, movie in enumerate(library):
        rating = ratings.get(movie["title"], "—")
        print(f"{i+1}. {movie['title']} | Rating: {rating}")


def print_recommendations(title, recs):
    print(f"\n=== {title} ===")

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

        print("\n1. Search movie")
        print("2. View library")
        print("0. Exit")

        choice = input("Choose option: ")

        if choice == "0":
            break

        if choice == "2":
            print_user_library(user_data)
            continue

        if choice != "1":
            print("Invalid choice")
            continue

        query = input("\nEnter movie name: ")

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

        # добавить в библиотеку
        add = input("\nAdd to library? (y/n): ").lower()

        if add == "y":
            add_to_library(movie_details)
            add_movie(movie_details)
            print("Added to library!")

        # рейтинг 
        rate = input("Rate this movie (0.5-5.0) or Enter to skip: ")

        try:
            rate_float = float(rate)
            if 0.5 <= rate_float <= 5.0:
                add_rating(movie_details["title"], rate_float)
                print("Rating saved!")
            else:
                print("Invalid rating")
        except ValueError:
            if rate.strip() != "":
                print("Invalid input, skipped")

        # рекомендации
        recommender = Recommender()

        recs_from_movie = recommender.recommend_from_movie(
            movie_details["title"], top_n=5
        )

        recs_for_user = recommender.recommend_for_user(top_n=5)

        print_recommendations("From this movie", recs_from_movie)
        print_recommendations("For you", recs_for_user)


if __name__ == "__main__":
    main()