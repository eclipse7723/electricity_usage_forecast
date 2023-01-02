from src.devices.device_manager import DeviceManager
from src.exceptions.device import DeviceNotFound
from src.event import Event


class DeviceController:

    EVENT_CONNECT_DEVICE = Event("onDeviceConnect")
    EVENT_DISCONNECT_DEVICE = Event("onDeviceDisconnect")

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
            DeviceController.EVENT_CONNECT_DEVICE(device)
            return True
        except DeviceNotFound:
            return False

    def remove_device(self, identity):
        try:
            device = self.connected_devices.pop(identity)
            DeviceController.EVENT_DISCONNECT_DEVICE(device)
            return True
        except KeyError:
            return False

    def create_device(self, params):
        device = DeviceManager.create_device(params)
        return device

    def increase_device_amount(self, identity):
        if self.has_device(identity) is False:
            return False

        device = self.get_device(identity)
        device.set_amount(device.amount + 1)
        return True

    def decrease_device_amount(self, identity):
        if self.has_device(identity) is False:
            return False

        device = self.get_device(identity)
        if device.amount == 1:
            self.remove_device(identity)
        else:
            device.set_amount(device.amount - 1)

        return True
