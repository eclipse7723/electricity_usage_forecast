class InterfaceNotFoundError(Exception):
    def __init__(self, name):
        exception_message = f"Interface with name {name!r} not found"
        super(InterfaceNotFoundError, self).__init__(exception_message)
