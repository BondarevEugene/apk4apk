from kivy.uix.label import Label


class TextBlock(Label):

    def __init__(self, data, **kwargs):

        super().__init__(**kwargs)

        self.text = data["content"]