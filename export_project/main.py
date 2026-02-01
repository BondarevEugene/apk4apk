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

