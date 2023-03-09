class InterfaceNotFoundError(Exception):
    def __init__(self, name):
        exception_message = f"Interface with name {name!r} not found"
        super(InterfaceNotFoundError, self).__init__(exception_message)


class InterfaceException(Exception):
    pass


# ------- Command Line Interface ---------------------------------------------------------------------------------------


class CLICommandNotInitialized(InterfaceException):
    def __init__(self, cls):
        exception_message = f"Command {cls.__name__!r} not initialized"
        super().__init__(exception_message)


class CLICommandAlreadyExist(InterfaceException):
    def __init__(self, name):
        exception_message = f"Command with name {name} already exists"
        super().__init__(exception_message)
