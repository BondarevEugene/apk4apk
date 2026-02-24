import os
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
os.environ['KIVY_GL_DEBUG'] = '1'
from kivy.core.window import Window
Window.backend = 'sdl2'

import os
import sys

# Примусове використання програмного рендерингу або Angle (DirectX)
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
os.environ['KIVY_GRAPHICS'] = 'gles'
# Вимикаємо мультисемплінг, який часто ламає рендеринг на AMD
from kivy.config import Config
Config.set('graphics', 'multisamples', '0')
Config.set('graphics', 'resizable', '1')

import os
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
os.environ['KIVY_GRAPHICS'] = 'gles'
import os
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
os.environ['KIVY_NO_ARGS'] = '1'
import configparser
import threading
import subprocess
import json
import os
import shutil
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivy.properties import StringProperty, ListProperty
from plyer import filechooser

ASSETS_DIR = "app_assets"
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)


# Функція конфігурації (тепер поза класом або як static)
def update_buildozer_spec(project_path, app_title):
    config = configparser.ConfigParser(interpolation=None)
    config.optionxform = str
    spec_path = "template.spec"
    if not os.path.exists(spec_path):
        return False
    config.read(spec_path, encoding='utf-8')
    package_name = "".join(filter(str.isalnum, app_title.lower()))
    config.set('app', 'title', app_title)
    config.set('app', 'package.name', package_name)
    config.set('app', 'source.include_exts', 'py,png,jpg,kv,atlas,json')
    with open(os.path.join(project_path, 'buildozer.spec'), 'w', encoding='utf-8') as f:
        config.write(f)
    return True


KV = '''
ScreenManager:
    MainScreen:
    EditorScreen:

<MainScreen>:
    name: "main"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: root.current_path_name if root.current_path_name else "Конструктор"
            left_action_items: [["arrow-left", lambda x: root.go_back()]] if root.navigation_stack else []

        ScrollView:
            MDList:
                id: container
        # Окремий контейнер для плаваючих кнопок
        MDFloatLayout:
            size_hint_y: None
            height: 0
            
        # Кнопка Створити розділ
        MDFloatingActionButton:
            icon: "plus"
            on_release: root.show_add_dialog()
            pos_hint: {"center_x": .85, "y": 1.5} # підняли над нижнім краєм

        # Кнопка Зібрати APK
        MDFloatingActionButton:
            icon: "hammer" 
            on_release: app.generate_apk()
            pos_hint: {"center_x": .15, "y": 1.5}
            md_bg_color: app.theme_cls.primary_color

<EditorScreen>:
    name: "editor"
    MDBoxLayout:
        orientation: "vertical"
        padding: "10dp"
        spacing: "10dp"
        
        MDTopAppBar:
            title: "Редактор вмісту"
            left_action_items: [["check", lambda x: root.save_and_exit()]]
            
        MDTextField:
            id: text_content
            hint_text: "Введіть текст"
            multiline: True
            mode: "rectangle"  # Або "fill", або "line"
            
        MDBoxLayout:
            adaptive_height: True
            spacing: "20dp"
            MDRaisedButton:
                text: "Фото"
                on_release: root.pick_media("image")
            MDRaisedButton:
                text: "Відео"
                on_release: root.pick_media("video")
                
        MDLabel:
            id: media_info
            text: "Медіа не вибрано"
            halign: "center"
'''


class MainScreen(Screen):
    navigation_stack = ListProperty([])
    current_path_name = StringProperty("")

    def refresh_list(self):
        # Перевіряємо, чи ідентифікатори (ids) вже завантажені
        if 'container' not in self.ids:
            return

        self.ids.container.clear_widgets()
        current_node = self.get_current_node()
        for key in current_node:
            item = OneLineIconListItem(
                text=key,
                on_release=lambda x, k=key: self.enter_section(k)
            )
            item.add_widget(IconLeftWidget(icon="pencil", on_release=lambda x, k=key: self.open_editor(k)))
            self.ids.container.add_widget(item)

    def get_current_node(self):
        data = MDApp.get_running_app().app_data
        curr = data
        for step in self.navigation_stack:
            curr = curr[step]["subsections"]
        return curr

    def refresh_list(self):
        self.ids.container.clear_widgets()
        current_node = self.get_current_node()
        for key in current_node:
            item = OneLineIconListItem(text=key, on_release=lambda x, k=key: self.enter_section(k))
            item.add_widget(IconLeftWidget(icon="pencil", on_release=lambda x, k=key: self.open_editor(k)))
            self.ids.container.add_widget(item)

    def show_add_dialog(self):
        self.dialog = MDDialog(
            title="Назва розділу",
            type="custom",
            content_cls=Builder.load_string('MDTextField: {hint_text: "Наприклад: Урок 1"}'),
            buttons=[MDFlatButton(text="Скасувати", on_release=lambda x: self.dialog.dismiss()),
                     MDRaisedButton(text="Створити", on_release=self.add_section)],
        )
        self.dialog.open()

    def add_section(self, *args):
        name = self.dialog.content_cls.text
        if name:
            node = self.get_current_node()
            node[name] = {"content": "", "media_path": "", "media_type": "", "subsections": {}}
            self.refresh_list()
            MDApp.get_running_app().save_data()
        self.dialog.dismiss()

    def enter_section(self, key):
        self.navigation_stack.append(key)
        self.current_path_name = key
        self.refresh_list()

    def go_back(self):
        if self.navigation_stack:
            self.navigation_stack.pop()
            self.current_path_name = self.navigation_stack[-1] if self.navigation_stack else ""
            self.refresh_list()

    def open_editor(self, key):
        app = MDApp.get_running_app()
        app.editing_node = self.get_current_node()[key]
        app.root.current = "editor"


class EditorScreen(Screen):
    def on_enter(self):
        node = MDApp.get_running_app().editing_node
        self.ids.text_content.text = node["content"]
        self.ids.media_info.text = f"Файл: {os.path.basename(node.get('media_path', '')) or 'немає'}"

    def pick_media(self, m_type):
        ext = ["*.jpg", "*.png", "*.jpeg"] if m_type == "image" else ["*.mp4", "*.mkv"]
        file_path = filechooser.open_file(title="Виберіть файл", filters=[(m_type, ext)])
        if file_path:
            filename = os.path.basename(file_path[0])
            dest = os.path.join(ASSETS_DIR, filename)
            shutil.copy(file_path[0], dest)
            node = MDApp.get_running_app().editing_node
            node["media_path"] = dest
            node["media_type"] = m_type
            self.ids.media_info.text = f"Завантажено: {filename}"

    def save_and_exit(self):
        MDApp.get_running_app().editing_node["content"] = self.ids.text_content.text
        MDApp.get_running_app().save_data()
        MDApp.get_running_app().root.current = "main"


class BuilderApp(MDApp):
    app_data = {}
    editing_node = None

    def on_start(self):
        # Як тільки додаток запуститься (навіть якщо вікно чорне),
        # він сам через 2 секунди спробує згенерувати проект.
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.generate_apk(), 2)

    def build(self):
        from kivymd.uix.screen import MDScreen
        from kivymd.uix.button import MDRaisedButton

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "DeepPurple"

        screen = MDScreen()
        screen.add_widget(
            MDRaisedButton(
                text="ЦЕ ПЕРЕВІРКА",
                pos_hint={"center_x": 0.5, "center_y": 0.5},
                on_release=lambda x: print("Кнопка працює!")
            )
        )
        return screen

    # def build(self):
    #     self.theme_cls.primary_palette = "DeepPurple"
    #     self.theme_cls.theme_style = "Light"  # Примусово світла тема
    #     self.load_data()
    #
    #     try:
    #         # Спроба завантажити інтерфейс
    #         ui = Builder.load_string(KV)
    #         return ui
    #     except Exception as e:
    #         # Якщо в KV помилка — вона виведеться червоним у консоль
    #         print("\n" + "!" * 30)
    #         print(f"КРИТИЧНА ПОМИЛКА В KV: \n{e}")
    #         print("!" * 30 + "\n")
    #         # Створюємо заглушку, щоб не було просто чорного екрана
    #         from kivymd.uix.label import MDLabel
    #         return MDLabel(text=f"Помилка завантаження KV:\n{e}", halign="center")

    def load_data(self):
        if os.path.exists("data.json"):
            with open("data.json", "r", encoding="utf-8") as f:
                self.app_data = json.load(f)

    def save_data(self):
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(self.app_data, f, indent=4, ensure_ascii=False)

    def generate_apk(self):
        build_dir = "export_project"
        os.makedirs(build_dir, exist_ok=True)
        self.save_data()
        shutil.copy("data.json", os.path.join(build_dir, "data.json"))

        if os.path.exists(ASSETS_DIR):
            dest_assets = os.path.join(build_dir, ASSETS_DIR)
            if os.path.exists(dest_assets): shutil.rmtree(dest_assets)
            shutil.copytree(ASSETS_DIR, dest_assets)

            # КОД ДВИГУНА (що буде всередині APK)
            engine_code = """
        import json
        import os
        from kivymd.app import MDApp
        from kivy.lang import Builder
        from kivy.uix.screenmanager import Screen, ScreenManager
        from kivymd.uix.list import OneLineListItem
        from kivymd.uix.boxlayout import MDBoxLayout
        from kivy.uix.image import AsyncImage

        KV = '''
        <MenuScreen>:
            MDBoxLayout:
                orientation: 'vertical'
                MDTopAppBar:
                    title: "Зміст"
                    elevation: 4
                ScrollView:
                    MDList:
                        id: container

        <ContentScreen>:
            MDBoxLayout:
                orientation: 'vertical'
                MDTopAppBar:
                    title: root.section_title
                    left_action_items: [["arrow-left", lambda x: root.go_back()]]
                ScrollView:
                    MDBoxLayout:
                        orientation: 'vertical'
                        padding: "16dp"
                        spacing: "16dp"
                        adaptive_height: True
                        id: content_box
        '''

        class MenuScreen(Screen):
            def on_enter(self):
                self.ids.container.clear_widgets()
                app = MDApp.get_running_app()
                for title in app.app_data.keys():
                    item = OneLineListItem(
                        text=title,
                        on_release=lambda x, t=title: self.open_content(t)
                    )
                    self.ids.container.add_widget(item)

            def open_content(self, title):
                app = MDApp.get_running_app()
                app.current_section = title
                self.manager.current = 'content'

        class ContentScreen(Screen):
            section_title = "Вміст"

            def on_enter(self):
                app = MDApp.get_running_app()
                self.section_title = app.current_section
                node = app.app_data[app.current_section]

                container = self.ids.content_box
                container.clear_widgets()

                # Текст
                if node.get("content"):
                    container.add_widget(MDApp.get_running_app().get_label(node["content"]))

                # Картинка
                if node.get("media_path") and node.get("media_type") == "image":
                    if os.path.exists(node["media_path"]):
                        container.add_widget(AsyncImage(source=node["media_path"], size_hint_y=None, height="250dp"))

            def go_back(self):
                self.manager.current = 'menu'

        class GeneratedApp(MDApp):
            app_data = {}
            current_section = ""

            def build(self):
                self.theme_cls.primary_palette = "DeepPurple"
                Builder.load_string(KV)

                # Завантажуємо дані, які конструктор поклав поруч
                if os.path.exists("data.json"):
                    with open("data.json", "r", encoding="utf-8") as f:
                        self.app_data = json.load(f)

                sm = ScreenManager()
                sm.add_widget(MenuScreen(name='menu'))
                sm.add_widget(ContentScreen(name='content'))
                return sm

            def get_label(self, text):
                from kivymd.uix.label import MDLabel
                return MDLabel(text=text, adaptive_height=True)

        if __name__ == "__main__":
            GeneratedApp().run()
        """
        with open(os.path.join(build_dir, "main.py"), "w", encoding="utf-8") as f:
            f.write(engine_code)

        if update_buildozer_spec(build_dir, "My App Factory"):
            threading.Thread(target=self.run_buildozer_command, args=(build_dir,)).start()

    def run_buildozer_command(self, path):
        print("--- СТАРТ BUILD ---")
        process = subprocess.Popen("buildozer android debug", cwd=path, shell=True, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            print(line, end="")


if __name__ == "__main__":
    BuilderApp().run()
