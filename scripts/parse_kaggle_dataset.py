import kagglehub
import pandas as pd
import json
import os


def main():
    path = kagglehub.dataset_download(
        "harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows"
    )

    print("Dataset path:", path)

    files = os.listdir(path)
    csv_file = [f for f in files if f.endswith(".csv")][0]
    csv_path = os.path.join(path, csv_file)

    df = pd.read_csv(csv_path)

    movies = []

    for _, row in df.iterrows():
        title = str(row["Series_Title"]).strip()
        year = str(row["Released_Year"]).strip()
        overview = str(row["Overview"]).strip()
        genre = str(row["Genre"]).strip()

        if year == "nan" or overview == "nan":
            continue

        movie = {
            "id": f"kaggle_{_}",  # уникальный id
            "title": f"{title} ({year})",  # 👈 как ты хотел
            "year": year,
            "overview": overview,
            "genre": genre
        }

        movies.append(movie)

    os.makedirs("data", exist_ok=True)

    with open("data/movies.json", "w") as f:
        json.dump(movies, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(movies)} movies to data/movies.json")


if __name__ == "__main__":
    main()