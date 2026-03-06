import os


def generate_app(data):

    name = data["app"]["name"]

    output = f"generated/{name}"

    os.makedirs(output, exist_ok=True)

    generate_main(data, output)
    generate_pages(data, output)
    generate_navigation(data, output)
    generate_spec(data, output)


def generate_main(data, path):

    code = """
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from navigation import build_navigation

class GeneratedApp(App):

    def build(self):

        sm = ScreenManager()

        build_navigation(sm)

        return sm


GeneratedApp().run()
"""

    with open(f"{path}/main.py", "w") as f:
        f.write(code)

def generate_pages(data, path):

    pages_path = f"{path}/pages"

    os.makedirs(pages_path, exist_ok=True)

    for page in data["pages"]:

        code = f"""
from kivy.uix.screenmanager import Screen
from engine.page_engine import build_page


class {page['id'].capitalize()}(Screen):

    def on_enter(self):

        build_page(self, "{page['id']}")
"""

        with open(f"{pages_path}/{page['id']}.py", "w") as f:
            f.write(code)