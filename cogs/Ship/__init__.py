from .cog import Ship


def setup(bot):
    bot.add_cog(Ship(bot))
