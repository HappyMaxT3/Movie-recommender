import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.config import CACHE_FILE

class Recommender:
    def __init__(self, path=CACHE_FILE):
        with open(path, "r") as f:
            movies = json.load(f)

        self.df = pd.DataFrame(movies)

        # комбинация текста
        self.df["combined"] = (
            self.df["overview"].fillna("") + " " + self.df["genre"].fillna("")
        )

        # TF-IDF
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["combined"])

        # cosine similarity
        self.similarity = cosine_similarity(self.tfidf_matrix)

        # индекс по названию
        self.indices = pd.Series(self.df.index, index=self.df["title"]).drop_duplicates()

    def recommend(self, title, top_n=5):
        if title not in self.indices:
            return []

        idx = self.indices[title]

        sim_scores = list(enumerate(self.similarity[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        sim_scores = sim_scores[1: top_n + 1]

        movie_indices = [i[0] for i in sim_scores]

        return self.df.iloc[movie_indices][
            ["title", "year", "genre", "overview"]
        ].to_dict("records")