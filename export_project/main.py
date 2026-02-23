from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class MyApp(App):

    def build(self):
        layout = BoxLayout(orientation="vertical")

        label = Label(text="BookApp працює 🚀", font_size="24sp")
        button = Button(text="Натисни мене")

        button.bind(on_press=self.on_button_click)

        layout.add_widget(label)
        layout.add_widget(button)

        return layout

    def on_button_click(self, instance):
        print("Кнопка натиснута")


if __name__ == "__main__":
    MyApp().run()
