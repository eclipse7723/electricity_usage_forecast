class DeviceException(Exception):
    pass


class DeviceNotFound(DeviceException):
    def __init__(self, identity):
        exception_message = f"Device with id {identity!r} not found"
        super(DeviceNotFound, self).__init__(exception_message)


class WrongDeviceParams(DeviceException):
    def __init__(self, identity, params, details=None):
        exception_message = f"Device with id {identity!r} has wrong params:\n{params}"
        if details is not None:
            exception_message += f"\nDetails: {details}"
        super(WrongDeviceParams, self).__init__(exception_message)


class DeviceAlreadyConnected(DeviceException):
    def __init__(self, identity):
        exception_message = f"Device with id {identity!r} already connected"
        super(DeviceAlreadyConnected, self).__init__(exception_message)


class NoSavedDevicesError(DeviceException):
    def __init__(self, path):
        exception_message = f"Saved devices were not found in {path!r}"
        super(NoSavedDevicesError, self).__init__(exception_message)


