from kivy.uix.screenmanager import Screen
from app.user_profile import get_user_data

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
                text += f"{movie['title']} ({movie['year']})\n"
                text += f"Genre: {movie['genre']}\n"
                text += f"Rating: {rating}\n"
                text += f"{movie['overview'][:150]}...\n"
                text += "-" * 40 + "\n"
        self.ids.library_list.text = text