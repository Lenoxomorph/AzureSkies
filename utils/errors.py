import traceback

from discord.ext import commands
from discord.ext.commands import CommandInvokeError


def make_error(message, error: bool = False):
    return f"```{'css' if error else 'fix'}\n[ERROR: {message}]\n```"


def make_success(message):
    return f'```diff\n+ {message}\n```'


async def on_error(send_function, error, ctx=None):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, AzureSkiesException):
        return await send_function(make_error(error))
    elif isinstance(error, (commands.UserInputError, commands.NoPrivateMessage, ValueError)):
        return await send_function(make_error(f"COMMAND ERROR: {str(error)}\n"
                                              f"Use \"{ctx.prefix}help " + ctx.command.qualified_name + "\" for help."))
    elif isinstance(error, CommandInvokeError):
        original = error.original
        if isinstance(original, AzureSkiesException):
            return await send_function(make_error(original))
    await send_function(
        make_error(f"UNEXPECTED ERROR!", True)  # TODO Add unexpected error text
    )
    print(traceback.print_exception(type(error), error, error.__traceback__))


class AzureSkiesException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class PermissionsError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class ImpossibleShotError(Exception):
    def __init__(self, msg):
        super().__init__(msg)
