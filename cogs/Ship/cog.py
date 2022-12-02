from io import BytesIO

import discord
from PIL import Image
from discord.ext import commands

from utils.aircraft import Aircraft, TransformRB, Vector
from utils.canvas import Canvas


class Ship(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roll", aliases=["r"])
    async def roll(self, ctx):
        print("test")
        await ctx.send(embed=discord.Embed().set_image(url="https://cdn.discordapp.com/attachments/262399680284065802/1032771208460128316/airship_bg.png"))
        # a = Aircraft(100, Image.open("airship_top.png"), Image.open("airship_side.png"),
        #              TransformRB(mass=5000, drag_profiles=Vector((50, 50, 50)), position=Vector((100, 100, 100)),
        #                          rotation=Vector((0, 45, 0))))
        # c1 = Canvas(Image.open("airship_side.png").resize((150, 150)), True)
        # c2 = Canvas(Image.open("airship_bg.png").resize((150, 150)), False)
        # a.draw_on(c1)
        # a.draw_on(c2)
        # with BytesIO() as image_binary:
        #     c1.image.save(image_binary, 'PNG')
        #     image_binary.seek(0)
        #     await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
