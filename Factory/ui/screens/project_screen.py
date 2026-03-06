from kivy.uix.screenmanager import Screen
from core.project_manager import build_project


class ProjectScreen(Screen):

    def generate(self):

        build_project()