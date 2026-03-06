from engine.layout_engine import build_layout
from engine.block_engine import build_block
from core.project_loader import load_project


def build_page(screen, page_id):

    data = load_project()

    page_data = None

    for p in data["pages"]:

        if p["id"] == page_id:

            page_data = p

            break

    layout = build_layout(page_data["layout"])

    for block in page_data["blocks"]:

        widget = build_block(block)

        layout.add_widget(widget)

    screen.add_widget(layout)