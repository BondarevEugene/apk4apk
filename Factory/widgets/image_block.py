from kivy.uix.image import Image


class ImageBlock(Image):

    def __init__(self, src):

        super().__init__(
            source=src,
            size_hint_y=None,
            height=300
        )