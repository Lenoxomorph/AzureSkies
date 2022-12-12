from .cog import Ship


async def setup(bot):
    await bot.add_cog(Ship(bot))
