from widgets.text_block import TextBlock
from widgets.image_block import ImageBlock


def build_block(block):

    t = block["type"]

    if t == "text":

        return TextBlock(block["value"])

    if t == "image":

        return ImageBlock(block["src"])

    return TextBlock("Unknown block")