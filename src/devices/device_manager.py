from src.settings import DEFAULT_DEVICES_PATH
from src.exceptions.device import DeviceNotFound, WrongDeviceParams
from src.devices.device import Device
import json


class DeviceManager:

    devices = {}

    @staticmethod
    def has_device(identity):
        return identity in DeviceManager.devices

    @staticmethod
    def get_device(identity):
        if DeviceManager.has_device(identity) is False:
            raise DeviceNotFound(identity)
        return DeviceManager.devices[identity]

    @staticmethod
    def create_device(params):
        device = Device(params)
        return device

    @staticmethod
    def create_devices():
        pass  # todo: import devices from `DEFAULT_TARIFF_ABOVE_PRICE`
        for device_id, params in ...:
            try:
                device = Device()
            except Exception as e:
                raise WrongDeviceParams(device_id, params, str(e))
