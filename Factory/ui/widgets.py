from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty


class StepWidget(BoxLayout):

    title = StringProperty()

    icon = StringProperty("assets/icons/working.png")

    def set_status(self, status):

        if status == "ok":
            self.icon = "assets/icons/ok.png"

        elif status == "error":
            self.icon = "assets/icons/error.png"

        else:
            self.icon = "assets/icons/working.png"