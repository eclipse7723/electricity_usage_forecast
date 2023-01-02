from src.settings import DEFAULT_DEVICES_PATH
from src.exceptions.device import DeviceNotFound, WrongDeviceParams
from src.devices.device import Device
import json
import time
import os


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
    def _generate_identity(name):
        identity = f"{name}_{int(time.time())}"
        return identity

    @staticmethod
    def create_device(params):
        if "identity" not in params:
            name = params["name"]
            identity = DeviceManager._generate_identity(name)
            params["identity"] = identity

        if "icon_path" in params and os.path.exists(params["icon_path"]) is False:
            raise FileNotFoundError(f"Device [{params['identity']}] icon not found: {params['icon_path']}")

        device = Device(params)
        DeviceManager.devices[device.identity] = device

        return device

    @staticmethod
    def create_devices():
        if os.path.exists(DEFAULT_DEVICES_PATH) is False:
            return

        with open(DEFAULT_DEVICES_PATH, "r") as f:
            create_params = json.load(f)

        for device_id, params in create_params.items():
            DeviceManager.create_device(params)
