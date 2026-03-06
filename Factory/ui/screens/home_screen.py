from kivy.uix.screenmanager import Screen


class HomeScreen(Screen):

    def open_project(self):

        self.manager.current = "project"