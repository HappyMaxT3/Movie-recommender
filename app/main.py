from app.omdb_api import search_movies, get_movie_details
from app.cache import add_movie
import time

def main():
    print("=== Movie Search CLI (API) ===")

    while True:
        query = input("\nEnter movie name (or '0' to exit): ")

        if query == "0":
            break

        results = search_movies(query)

        if not results:
            print("No movies found")
            continue

        print("\nSaving movies to cache...")

        for movie in results:
            movie_details = get_movie_details(movie["imdbID"])

            if (
                movie_details
                and movie_details.get("overview") != "N/A"
                and movie_details.get("title")
                and movie_details.get("year")
            ):
                add_movie(movie_details)

            time.sleep(0.2)  # от лимитов API

        print("All movies saved!\n")

        for i, movie in enumerate(results):
            print(f"{i+1}. {movie['Title']} ({movie['Year']})")

        try:
            choice = int(input("Select movie number: ")) - 1
            selected = results[choice]
        except:
            print("Invalid choice")
            continue

        movie_details = get_movie_details(selected["imdbID"])

        print("\n=== Movie Details ===")
        print(f"Title: {movie_details['title']}")
        print(f"Year: {movie_details['year']}")
        print(f"Genre: {movie_details['genre']}")
        print(f"Plot: {movie_details['overview']}")


if __name__ == "__main__":
    main()