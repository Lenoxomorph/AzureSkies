import discord
from discord.ext import commands

from utils.functions import try_delete
from .maps import Maps
from .menus import MainMenu


class Ship(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="maps")
    async def maps(self, ctx):
        await try_delete(ctx.message)

        embeds = (discord.Embed().set_image(url="attachment://map0.png"),
                  discord.Embed().set_image(url="attachment://map1.png"))

        message = await ctx.send(embeds=embeds)
        maps = Maps(message.id)

        await message.add_files(*maps.render_files())
        maps.save()

        await message.edit(view=MainMenu())

    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        await interaction.message.edit(view=MainMenu())
        await interaction.response.send_message(content="Reloaded Menu", ephemeral=True, delete_after=5)
