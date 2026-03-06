import os
import zipfile
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup


class FactoryLayout(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        # Назва додатку
        self.add_widget(Label(text="Назва додатку:", size_hint_y=None, height=40))

        self.app_name = TextInput(
            text="MyBookApp",
            multiline=False,
            size_hint_y=None,
            height=40
        )
        self.add_widget(self.app_name)

        # HTML редактор
        self.add_widget(Label(text="HTML контент:", size_hint_y=None, height=40))

        self.html_editor = TextInput(
            text="<h1>Моя книга</h1>\n<p>Тут текст...</p>",
            multiline=True
        )
        self.add_widget(self.html_editor)

        # Кнопка вибору картинки
        self.image_path = ""

        image_button = Button(
            text="Вибрати картинку",
            size_hint_y=None,
            height=50
        )
        image_button.bind(on_press=self.open_file_chooser)

        self.add_widget(image_button)

        # Кнопка створення проекту
        build_button = Button(
            text="Створити Android проект",
            size_hint_y=None,
            height=60
        )
        build_button.bind(on_press=self.create_project)

        self.add_widget(build_button)

        # Статус
        self.status = Label(text="Готово")
        self.add_widget(self.status)

    # -------------------------

    def open_file_chooser(self, instance):

        chooser = FileChooserIconView()

        popup = Popup(
            title="Виберіть картинку",
            content=chooser,
            size_hint=(0.9, 0.9)
        )

        def select_file(instance, selection):

            if selection:
                self.image_path = selection[0]
                self.status.text = f"Обрана картинка: {self.image_path}"

            popup.dismiss()

        chooser.bind(on_submit=select_file)

        popup.open()

    # -------------------------

    def create_project(self, instance):

        app_name = self.app_name.text.strip()
        html = self.html_editor.text

        if not app_name:
            self.status.text = "Введіть назву!"
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        project_name = f"{app_name}_{timestamp}"

        base_dir = os.path.join("projects", project_name)

        os.makedirs(base_dir, exist_ok=True)

        # створюємо main.py додатку
        main_code = f'''
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class BookApp(App):

    def build(self):

        layout = BoxLayout(orientation="vertical")

        label = Label(
            text="""{html}""",
            markup=True
        )

        layout.add_widget(label)

        return layout

if __name__ == "__main__":
    BookApp().run()
'''

        with open(os.path.join(base_dir, "main.py"), "w", encoding="utf-8") as f:
            f.write(main_code)

        # копіюємо buildozer.spec
        if os.path.exists("buildozer.spec"):

            import shutil

            shutil.copy(
                "buildozer.spec",
                os.path.join(base_dir, "buildozer.spec")
            )

        # створюємо ZIP
        zip_path = os.path.join("projects", f"{project_name}.zip")

        with zipfile.ZipFile(zip_path, "w") as zipf:

            for root, dirs, files in os.walk(base_dir):

                for file in files:

                    full = os.path.join(root, file)

                    zipf.write(
                        full,
                        os.path.relpath(full, base_dir)
                    )

        self.status.text = f"Проект створено: {project_name}"


class FactoryApp(App):

    def build(self):
        return FactoryLayout()


if __name__ == "__main__":
    FactoryApp().run()