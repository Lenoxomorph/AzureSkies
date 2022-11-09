import discord
from PIL import Image
from discord.ext import commands


class Ship(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roll", aliases=["r"])
    async def roll(self, ctx, *, dice: str = "1d20"):
        bg = Image.open("airship_bg.png")
        bg.paste(Image.open("airship_top.png"), (0, 0))
        await ctx.send(file=discord.File(bg))
