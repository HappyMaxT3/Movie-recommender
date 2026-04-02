from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from random import sample

from app.recommender import Recommender
from app.omdb_api import search_movies, get_movie_details
from app.user_profile import get_user_data
from app.cache import add_movie
from .details_screen import open_movie_screen


class SearchScreen(Screen):

    def on_enter(self, *args):
        self.load_recommendations()

    def refresh_recommendations(self):
        if hasattr(self.ids, "recommendations_list"):
            self.ids.recommendations_list.clear_widgets()
            self.load_recommendations()

    def create_movie_card(self, movie):
        layout = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=130,
            spacing=10
        )

        poster = movie.get("poster")
        if not isinstance(poster, str) or poster == "N/A":
            poster = ""

        if poster:
            layout.add_widget(
                AsyncImage(
                    source=poster,
                    size_hint_x=None,
                    width=90
                )
            )

        text = f"{movie.get('title', '')} ({movie.get('year', '')})\n{movie.get('genre', '')}"

        btn = Button(text=text)
        btn.bind(on_press=lambda x: open_movie_screen(self.manager, movie))

        layout.add_widget(btn)
        return layout

    def load_recommendations(self):
        if not hasattr(self.ids, "recommendations_list"):
            return

        self.ids.recommendations_list.clear_widgets()

        user_data = get_user_data()
        library_titles = {m["title"] for m in user_data.get("library", [])}

        recommender = Recommender()
        all_recs = recommender.recommend_for_user(top_n=20)

        new_recs = [m for m in all_recs if m["title"] not in library_titles]
        display_recs = sample(new_recs, min(10, len(new_recs))) if new_recs else []

        if not display_recs:
            self.ids.recommendations_list.add_widget(
                Button(text="No recommendations", size_hint_y=None, height=40)
            )
            return

        for movie in display_recs:
            self.ids.recommendations_list.add_widget(self.create_movie_card(movie))

    def search_movie(self):
        if not hasattr(self.ids, "search_results_list"):
            return

        query = self.ids.search_input.text.strip()
        if not query:
            return

        results = search_movies(query)
        self.ids.search_results_list.clear_widgets()

        for movie in results[:10]:
            movie_details = get_movie_details(movie["imdbID"])
            if movie_details:
                add_movie(movie_details)
                self.ids.search_results_list.add_widget(
                    self.create_movie_card(movie_details)
                )

    def search_by_description(self):
        if not hasattr(self.ids, "search_results_list"):
            return

        query = self.ids.search_input.text.strip()
        if not query:
            return

        recommender = Recommender()
        results = recommender.search_by_description(query)

        self.ids.search_results_list.clear_widgets()

        for movie in results:
            self.ids.search_results_list.add_widget(
                self.create_movie_card(movie)
            )

    def open_library(self):
        self.manager.current = "library"