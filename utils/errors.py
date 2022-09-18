def make_error(message, error: bool = False):
    return f"```{'css' if error else 'fix'}\n[ERROR: {message}]\n```"


def make_success(message):
    return f'```diff\n+ {message}\n```'


class AzureSkiesException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
