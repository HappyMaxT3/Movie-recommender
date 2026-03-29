import json
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.config import CACHE_FILE
from app.user_profile import get_user_data

class Recommender:
    def __init__(self):
        with open(CACHE_FILE, "r") as f:
            movies = json.load(f)

        self.df = pd.DataFrame(movies)

        # Комбинируем текст
        self.df["combined"] = (
            self.df["overview"].fillna("") + " " + self.df["genre"].fillna("")
        )

        # TF-IDF
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["combined"])

        # Индекс по названию
        self.indices = pd.Series(self.df.index, index=self.df["title"]).drop_duplicates()

    # рекомендации от фильма
    def recommend_from_movie(self, title, top_n=5):
        if title not in self.indices:
            return []

        idx = self.indices[title]

        sim_scores = cosine_similarity(
            self.tfidf_matrix[idx], self.tfidf_matrix
        ).flatten()

        sim_df = pd.DataFrame({"index": self.df.index, "score": sim_scores})

        # убираем сам фильм
        sim_df = sim_df[sim_df["index"] != idx]
        sim_df = sim_df.sort_values("score", ascending=False).head(top_n)

        return self.df.iloc[sim_df["index"]][["title", "year", "genre", "overview"]].to_dict("records")

    # персональные рекомендации
    def recommend_for_user(self, top_n=5):
        user_data = get_user_data()
        ratings = user_data.get("ratings", {})
        library = user_data.get("library", [])

        library_titles = {movie["title"] for movie in library}

        # фильмы с оценкой >= 4.0
        liked_titles = [title for title, r in ratings.items() if r >= 4.0]
        if not liked_titles:
            return []

        liked_indices = [self.indices[title] for title in liked_titles if title in self.indices]
        if not liked_indices:
            return []

        # создаём user-вектор
        liked_matrix = self.tfidf_matrix[liked_indices]
        user_vector = liked_matrix.mean(axis=0)
        user_vector = np.asarray(user_vector)

        # cosine similarity
        sim_scores = cosine_similarity(user_vector, self.tfidf_matrix).flatten()

        sim_df = pd.DataFrame({"index": self.df.index, "score": sim_scores})

        sim_df = sim_df[~self.df["title"].isin(library_titles)]
        sim_df = sim_df.sort_values("score", ascending=False).head(top_n)

        movie_indices = sim_df["index"].tolist()
        return self.df.iloc[movie_indices][["title", "year", "genre", "overview"]].to_dict("records")