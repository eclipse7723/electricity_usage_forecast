class DeviceNotFound(Exception):
    def __init__(self, identity):
        exception_message = f"Device with id {identity!r} not found"
        super(DeviceNotFound, self).__init__(exception_message)


class WrongDeviceParams(Exception):
    def __init__(self, identity, params, details=None):
        exception_message = f"Device with id {identity!r} has wrong params:\n{params}"
        if details is not None:
            exception_message += f"\nDetails: {details}"
        super(WrongDeviceParams, self).__init__(exception_message)


class DeviceAlreadyConnected(Exception):
    def __init__(self, identity):
        exception_message = f"Device with id {identity!r} alrady connected"
        super(DeviceAlreadyConnected, self).__init__(exception_message)

