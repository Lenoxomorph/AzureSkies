from discord.ext import commands


class Roller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roll", aliases=["r"])
    async def roll(self, ctx, *, dice: str = "1d20"):
        pass
