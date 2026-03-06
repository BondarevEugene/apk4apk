from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from ui.screens.home_screen import HomeScreen
from ui.screens.project_screen import ProjectScreen


class FactoryApp(App):

    def build(self):

        sm = ScreenManager()

        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(ProjectScreen(name="project"))

        return sm