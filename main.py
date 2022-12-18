import asyncio
import os

import discord
from discord.ext import commands

from cogs.Map.menus import MainMenu, CanvasMenu, ZoomMenu, PanMenu
from utils import config
from utils import csvUtils
from utils.errors import on_error

# TODO Get Current Position,

# TODO Weather, Altitude, Heading, Travel Speeds,

menus = [MainMenu, CanvasMenu, ZoomMenu, PanMenu]


async def get_prefix(the_bot, message):
    if not message.guild:
        return commands.when_mentioned_or(config.DEFAULT_PREFIX)(the_bot, message)
    gp = await the_bot.get_guild_prefix(message.guild)
    return commands.when_mentioned_or(gp)(the_bot, message)


class AzureSkies(commands.Bot):
    def __init__(self, prefix, description=None, **options):
        super().__init__(
            prefix,
            description=description,
            **options,
        )
        self.prefixes = dict()

    async def setup_hook(self) -> None:
        for menu in menus:
            self.add_view(menu())

    async def get_guild_prefix(self, guild: discord.Guild) -> str:
        guild_id = str(guild.id)
        if guild_id in self.prefixes:
            return self.prefixes.get(guild_id, config.DEFAULT_PREFIX)

        gp = csvUtils.search_csv(guild_id, "db/prefixes.csv")
        if gp:
            gp = ''.join(gp)
        else:
            gp = config.DEFAULT_PREFIX
        self.prefixes[guild_id] = gp
        return gp

    async def close(self):
        print("Close")


desc = (
    "A bot for helping the players and GM of Azuridrian"
)
intents = discord.Intents.all()

bot = AzureSkies(
    prefix=get_prefix,
    description=desc,
    activity=discord.Activity(type=discord.ActivityType.listening, name='eldritch screams'),
    allowed_mentions=discord.AllowedMentions.none(),
    intents=intents,
    chunk_guilds_at_startup=False,
)


@bot.event
async def on_ready():
    print(f"Logged in as - \"{bot.user.name}\" - {bot.user.id}")
    print(f'AzureSkies has risen in {len(bot.guilds)} servers')


@bot.event
async def on_resumed():
    print("Resumed")


@bot.event
async def on_command_error(ctx, error):
    await on_error(ctx, error)


async def main():
    async with bot:
        for dir_name in os.listdir('cogs'):
            if dir_name != "__pycache__":
                await bot.load_extension(f'cogs.{dir_name}')
        await bot.start(config.BOT_TOKEN)


if __name__ == '__main__':
    asyncio.run(main())
