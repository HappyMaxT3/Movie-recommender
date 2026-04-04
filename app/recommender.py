import json
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from app.config import CACHE_FILE
from app.user_profile import get_user_data

from app.embedding_model import get_model
from app.embeddings_store import load_or_create_embeddings


class Recommender:
    def __init__(self):
        with open(CACHE_FILE, "r") as f:
            movies = json.load(f)

        self.df = pd.DataFrame(movies)

        if self.df.empty:
            self.embeddings = np.array([])
            self.indices = {}
            return

        # текст
        self.df["combined"] = (
            self.df["overview"].fillna("") + " " + self.df["genre"].fillna("")
        )

        # модель
        self.model = get_model()

        # embeddings
        self.embeddings = load_or_create_embeddings(
            self.df["combined"].tolist()
        )

        # индекс
        self.indices = pd.Series(
            self.df.index, index=self.df["title"]
        ).drop_duplicates()

    # ======================
    # FROM MOVIE
    # ======================
    def recommend_from_movie(self, title, top_n=5):
        if title not in self.indices:
            return []

        idx = self.indices[title]

        sim_scores = cosine_similarity(
            [self.embeddings[idx]], self.embeddings
        ).flatten()

        return self._top_results(sim_scores, exclude_idx=idx, top_n=top_n)

    # ======================
    # PERSONAL
    # ======================
    def recommend_for_user(self, top_n=5):
        user_data = get_user_data()
        ratings = user_data.get("ratings", {})
        library = user_data.get("library", [])

        library_titles = {m["title"] for m in library}

        liked_titles = [t for t, r in ratings.items() if r >= 3.0]
        if not liked_titles:
            return []

        liked_indices = [
            self.indices[t] for t in liked_titles if t in self.indices
        ]
        if not liked_indices:
            return []

        user_vector = np.mean(self.embeddings[liked_indices], axis=0)

        sim_scores = cosine_similarity(
            [user_vector], self.embeddings
        ).flatten()

        return self._top_results(
            sim_scores,
            exclude_titles=library_titles,
            top_n=top_n
        )

    # ======================
    # SEARCH
    # ======================
    def search_by_description(self, query, top_n=10):
        if not query:
            return []

        query_vec = self.model.encode([query])

        sim_scores = cosine_similarity(
            query_vec, self.embeddings
        ).flatten()

        return self._top_results(sim_scores, top_n=top_n)

    # ======================
    # CORE
    # ======================
    def _top_results(self, sim_scores, top_n=5, exclude_idx=None, exclude_titles=None):
        sim_scores = np.array(sim_scores)

        df = self.df.copy()
        df["score"] = sim_scores

        if exclude_idx is not None:
            df = df[df.index != exclude_idx]

        if exclude_titles:
            df = df[~df["title"].isin(exclude_titles)]

        df = df.sort_values("score", ascending=False).head(top_n)

        return self._safe_movies(
            df[["title", "year", "genre", "overview", "poster"]]
        )

    # ======================
    # SAFE OUTPUT
    # ======================
    def _safe_movies(self, df_slice):
        movies = df_slice.to_dict("records")

        for m in movies:
            if not isinstance(m.get("poster", ""), str):
                m["poster"] = ""

        return movies