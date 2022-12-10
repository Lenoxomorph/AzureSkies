import discord
from PIL import Image


class Canvas:
    def __init__(self, image: Image.Image, is_top=True, ppf=5):
        self.image = image
        self.is_top = is_top
        self.ppf = ppf

    def paste(self, **kwargs):
        kwargs["box"][1] = self.image.height - kwargs["box"][1]
        self.image.paste(**kwargs)
