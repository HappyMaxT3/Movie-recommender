import os
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from .search_screen import SearchScreen
from .details_screen import DetailsScreen
from .library_screen import LibraryScreen

class RootWidget(ScreenManager):
    pass

class MovieApp(App):
    def build(self):
        kv_path = os.path.join(os.path.dirname(__file__), "ui.kv")
        Builder.load_file(kv_path)

        sm = RootWidget()
        sm.add_widget(SearchScreen(name="search"))
        sm.add_widget(DetailsScreen(name="details"))
        sm.add_widget(LibraryScreen(name="library"))
        return sm

if __name__ == "__main__":
    MovieApp().run()