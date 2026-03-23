import os

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button

from app.omdb_api import search_movies, get_movie_details
from app.user_profile import add_to_library, add_rating, get_user_data


class SearchScreen(Screen):
    def search(self):
        query = self.ids.search_input.text
        results = search_movies(query)

        self.ids.results_list.clear_widgets()

        for movie in results[:10]:
            btn = Button(
                text=f"{movie['Title']} ({movie['Year']})",
                size_hint_y=None,
                height=40
            )
            btn.bind(on_press=lambda x, m=movie: self.open_movie(m))
            self.ids.results_list.add_widget(btn)

    def open_movie(self, movie):
        details = get_movie_details(movie["imdbID"])
        details_screen = self.manager.get_screen("details")

        details_screen.movie = details
        details_screen.ids.title.text = f"{details['title']} ({details['year']})"
        details_screen.ids.genre.text = details["genre"]
        details_screen.ids.overview.text = details["overview"]

        self.manager.current = "details"

    def open_library(self):
        self.manager.current = "library"


def open_library(self):
    self.manager.current = "library"


class DetailsScreen(Screen):
    def add_movie(self):
        add_to_library(self.movie)

        try:
            rating = float(self.ids.rating_input.text)
            add_rating(self.movie["title"], rating)
        except:
            pass

        self.manager.current = "search"


class LibraryScreen(Screen):
    def on_enter(self):
        user = get_user_data()

        library = user.get("library", [])
        ratings = user.get("ratings", {})

        text = ""

        if not library:
            text = "Library is empty"
        else:
            for movie in library:
                rating = ratings.get(movie["title"], "—")

                text += f"\n{movie['title']} ({movie['year']})\n"
                text += f"Genre: {movie['genre']}\n"
                text += f"Rating: {rating}\n"
                text += f"{movie['overview'][:150]}...\n"
                text += "-" * 40 + "\n"

        self.ids.library_list.text = text


class RootWidget(ScreenManager):
    pass


class MovieApp(App):
    def build(self):
        kv_path = os.path.join(os.path.dirname(__file__), "ui.kv")
        return Builder.load_file(kv_path)


if __name__ == "__main__":
    MovieApp().run()