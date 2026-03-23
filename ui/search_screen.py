# ui/search_screen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button

from app.recommender import Recommender
from random import sample

from .details_screen import open_movie_screen
from app.omdb_api import search_movies, get_movie_details
from app.user_profile import get_user_data
from app.cache import add_movie

class SearchScreen(Screen):

    def on_enter(self, *args):
        self.load_recommendations()

    def refresh_recommendations(self):
        self.load_recommendations()

    def load_recommendations(self):
        if not hasattr(self.ids, "results_list"):
            return

        self.ids.results_list.clear_widgets()
        user_data = get_user_data()
        library_titles = {m["title"] for m in user_data.get("library", [])}

        recommender = Recommender()
        all_recs = recommender.recommend_for_user(top_n=20)

        new_recs = [m for m in all_recs if m["title"] not in library_titles]
        display_recs = sample(new_recs, min(10, len(new_recs))) if new_recs else []

        if not display_recs:
            btn = Button(text="No recommendations", size_hint_y=None, height=40)
            self.ids.results_list.add_widget(btn)
            return

        for movie in display_recs:
            btn = Button(text=f"{movie['title']} ({movie['year']})", size_hint_y=None, height=40)
            btn.bind(on_press=lambda x, m=movie: open_movie_screen(self.manager, m))
            self.ids.results_list.add_widget(btn)

    def search_movie(self):
        query = self.ids.search_input.text
        results = search_movies(query)
        self.ids.results_list.clear_widgets()

        for movie in results[:10]:
            movie_details = get_movie_details(movie["imdbID"])
            if movie_details:
                add_movie(movie_details)

                btn = Button(
                    text=f"{movie_details['title']} ({movie_details['year']})",
                    size_hint_y=None,
                    height=40
                )

                btn.bind(on_press=lambda x, m=movie_details: open_movie_screen(self.manager, m))
                self.ids.results_list.add_widget(btn)

    def open_movie_detail(self, movie):
        details = get_movie_details(movie["imdbID"])
        if details:
            open_movie_screen(self.manager, details)

    def open_library(self):
        self.manager.current = "library"