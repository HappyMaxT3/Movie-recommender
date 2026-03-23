from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import os

from app.omdb_api import search_movies, get_movie_details
from app.user_profile import add_to_library, add_rating


class MainLayout(BoxLayout):
    def search(self):
        query = self.ids.search_input.text
        results = search_movies(query)

        if not results:
            self.ids.results_label.text = "No movies found"
            return

        text = ""
        for i, movie in enumerate(results[:5]):
            text += f"{i+1}. {movie['Title']} ({movie['Year']})\n"

        self.results = results
        self.ids.results_label.text = text

    def select_movie(self):
        try:
            index = int(self.ids.choice_input.text) - 1
            selected = self.results[index]
        except:
            self.ids.results_label.text = "Invalid choice"
            return

        details = get_movie_details(selected["imdbID"])
        self.selected_movie = details

        self.ids.results_label.text = f"""
{details['title']} ({details['year']})
{details['genre']}

{details['overview'][:200]}...
"""

    def add_movie(self):
        if hasattr(self, "selected_movie"):
            add_to_library(self.selected_movie)
            self.ids.results_label.text = "Added to library!"

    def rate_movie(self):
        if not hasattr(self, "selected_movie"):
            self.ids.results_label.text = "Select movie first"
            return

        try:
            rating = float(self.ids.rating_input.text)
            add_rating(self.selected_movie["title"], rating)
            self.ids.results_label.text = "Rating saved!"
        except:
            self.ids.results_label.text = "Invalid rating"


class MovieApp(App):
    def build(self):
        kv_path = os.path.join(os.path.dirname(__file__), "ui.kv")
        Builder.load_file(kv_path)
        return MainLayout()


if __name__ == "__main__":
    MovieApp().run()