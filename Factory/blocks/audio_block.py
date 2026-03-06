from kivy.core.audio import SoundLoader
from kivy.uix.button import Button


class AudioBlock(Button):

    def __init__(self, data, **kwargs):

        super().__init__(**kwargs)

        self.text = "Play audio"

        self.sound = SoundLoader.load(data["src"])

        self.bind(on_press=self.play)

    def play(self, *args):

        if self.sound:
            self.sound.play()