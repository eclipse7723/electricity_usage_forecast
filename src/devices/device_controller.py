from src.devices.device_manager import DeviceManager
from src.exceptions.device import DeviceNotFound, WrongDeviceParams


class DeviceController:

    def __init__(self):
        self.connected_devices = {}

    def get_devices(self):
        return self.connected_devices.values()

    def has_device(self, identity):
        return identity in self.connected_devices

    def get_device(self, identity):
        if self.has_device(identity) is False:
            raise DeviceNotFound(identity)
        device = self.connected_devices[identity]
        return device

    def add_device(self, identity):
        try:
            device = DeviceManager.get_device(identity)
            self.connected_devices[identity] = device
            return True
        except DeviceNotFound:
            return False

    def remove_device(self, identity):
        try:
            del self.connected_devices[identity]
            return True
        except KeyError:
            return False

    def create_device(self, params):    # todo
        try:
            device = DeviceController.create_device(..., params)
        except WrongDeviceParams:
            return None
