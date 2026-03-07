from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock

from core.build_manager import BuildManager

KV = "ui/factory.kv"


class FactoryApp(App):

    def build(self):

        self.manager = BuildManager(self)

        root = Builder.load_file(KV)

        return root

    def start_build(self):

        self.root.ids.progress.value = 0
        self.root.ids.log.text = ""

        self.manager.start()

    def update_progress(self, value):

        self.root.ids.progress.value = value

    def log(self, text):

        log = self.root.ids.log
        log.text += text + "\n"
        log.cursor = (0, len(log.text))

    def set_step(self, index, status):

        steps = self.root.ids.steps.children[::-1]

        step = steps[index]

        step.set_status(status)


def run():
    FactoryApp().run()