from io import BytesIO

import discord
from PIL import Image
from discord.ext import commands

from utils.aircraft import Aircraft, TransformRB, Vector
from utils.canvas import Canvas
from utils.functions import try_delete
from utils.menus import ButtonMenu


class Ship(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="maps")
    async def maps(self, ctx):
        file = discord.File(r"C:\Users\micro\PycharmProjects\AzureSkies\db\images\airship_bg (2).png", filename="test.png")
        embed = discord.Embed()
        embed.set_image(url="attachment://test.png")


        file2 = discord.File(r"C:\Users\micro\PycharmProjects\AzureSkies\db\images\airship_bg (1).png", filename="test.png")
        embed2 = discord.Embed()
        embed2.set_image(url="attachment://test2.png")

        message = await ctx.send(content="re", embed=embed)
        await message.add_files(file)

        await message.remove_attachments()

        await message.add_files(file2)


        # await ctx.send("https://cdn.discordapp.com/attachments/262399680284065802/1032771208460128316/airship_bg.png")

        # await try_delete(ctx.message)
        # embed1 = discord.Embed(title="reeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee").set_image(url="https://cdn.discordapp.com/attachments/262399680284065802/1032771208460128316/airship_bg.png")
        # embed2 = discord.Embed(title="reeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee").set_image(url="https://cdn.discordapp.com/attachments/262399680284065802/1032771208460128316/airship_bg.png")
        # await ctx.send(embeds=[embed1, embed2], view=ButtonMenu())
        # await ctx.send(embed=discord.Embed().set_image(url="https://cdn.discordapp.com/attachments/262399680284065802/1032771208460128316/airship_bg.png"))

        # with BytesIO() as image_binary:
        #     create_image().save(image_binary, 'PNG')
        #     image_binary.seek(0)
        #     await message.channel.send(file=discord.File(fp=image_binary, filename='image.png'))

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
