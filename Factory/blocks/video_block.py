from kivy.uix.video import Video


class VideoBlock(Video):

    def __init__(self, data, **kwargs):

        super().__init__(**kwargs)

        self.source = data["src"]

        self.state = "play"