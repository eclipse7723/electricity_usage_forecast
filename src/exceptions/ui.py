class InterfaceNotFoundError(Exception):
    def __init__(self, name):
        exception_message = f"Interface with name {name!r} not found"
        super(InterfaceNotFoundError, self).__init__(exception_message)


# ------- Command Line Interface ---------------------------------------------------------------------------------------


class CLICommandTestFailed(Exception):
    def __init__(self, name, fail_description):
        exception_message = f"Command {name!r} failed its test: {fail_description}"
        super().__init__(exception_message)
