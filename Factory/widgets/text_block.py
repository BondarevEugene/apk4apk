from kivy.uix.label import Label


class TextBlock(Label):

    def __init__(self, text):

        super().__init__(
            text=text,
            size_hint_y=None,
            height=40
        )