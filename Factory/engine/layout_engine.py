from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout


def build_layout(layout_type):

    if layout_type == "column":

        return BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

    if layout_type == "row":

        return BoxLayout(
            orientation="horizontal",
            spacing=10,
            padding=10
        )

    if layout_type == "grid":

        return GridLayout(
            cols=2,
            spacing=10,
            padding=10,
            size_hint_y=None
        )

    return BoxLayout(orientation="vertical")