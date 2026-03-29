from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage

from app.user_profile import get_user_data


class LibraryScreen(Screen):

    def on_enter(self):
        if not hasattr(self.ids, "library_list"):
            return

        self.ids.library_list.clear_widgets()

        user = get_user_data()
        library = user.get("library", [])
        ratings = user.get("ratings", {})

        if not library:
            self.ids.library_list.add_widget(
                Label(text="Library is empty", size_hint_y=None, height=40)
            )
            return

        for movie in library:
            rating = ratings.get(movie["title"], "—")

            # --- Карточка фильма ---
            card = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=150,
                spacing=10,
                padding=5
            )

            # --- Постер ---
            poster_url = movie.get("poster", "")

            if poster_url and poster_url != "N/A":
                poster = AsyncImage(
                    source=poster_url,
                    size_hint_x=None,
                    width=100
                )
            else:
                poster = Label(
                    text="No Image",
                    size_hint_x=None,
                    width=100
                )

            # --- Текст справа ---
            text = BoxLayout(orientation="vertical")

            text.add_widget(Label(
                text=f"{movie['title']} ({movie['year']})",
                bold=True,
                size_hint_y=None,
                height=30
            ))

            text.add_widget(Label(
                text=f"Genre: {movie['genre']}",
                size_hint_y=None,
                height=25
            ))

            text.add_widget(Label(
                text=f"Rating: {rating}",
                size_hint_y=None,
                height=25
            ))

            text.add_widget(Label(
                text=movie["overview"][:120] + "...",
                size_hint_y=None,
                height=60
            ))

            # --- собираем ---
            card.add_widget(poster)
            card.add_widget(text)

            self.ids.library_list.add_widget(card)