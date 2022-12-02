import discord
from PIL import Image


class TestMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label="Send Message", style=discord.ButtonStyle.grey)
    async def menu1(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Hello, You clicked me")


class Canvas:
    def __init__(self, image: Image.Image, is_top=True, ppf=5):
        self.image = image
        self.is_top = is_top
        self.ppf = ppf

    def paste(self, **kwargs):
        kwargs["box"][1] = self.image.height - kwargs["box"][1]
        self.image.paste(**kwargs)
