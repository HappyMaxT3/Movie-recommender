from kivy.uix.screenmanager import Screen
from app.user_profile import add_to_library, add_rating

def open_movie_screen(manager, movie):
    screen = manager.get_screen("details")
    screen.movie = movie
    screen.ids.title.text = f"{movie['title']} ({movie['year']})"
    screen.ids.genre.text = movie["genre"]
    screen.ids.overview.text = movie["overview"]
    screen.ids.rating_input.text = ""
    if movie.get("poster"):
        screen.ids.poster.source = movie["poster"]
    manager.current = "details"


class DetailsScreen(Screen):
    def add_movie(self):
        add_to_library(self.movie)
        try:
            rating = float(self.ids.rating_input.text)
            add_rating(self.movie["title"], rating)
        except ValueError:
            pass
        self.manager.current = "search"