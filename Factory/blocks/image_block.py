from kivy.uix.image import Image


class ImageBlock(Image):

    def __init__(self, data, **kwargs):

        super().__init__(**kwargs)

        self.source = data["src"]