from src.manager import Manager
from src.settings import DEFAULT_DEVICES_PATH
from src.exceptions.device import DeviceNotFound, WrongDeviceParams
from src.devices.device import Device
from src.event import Event
import json
import time
import os


class DeviceManager(Manager):

    EVENT_CREATE_DEVICE = Event("onDeviceCreate")

    devices = {}

    @classmethod
    def _initialize(cls):
        cls.create_devices()

    @classmethod
    def _finalize(cls):
        cls.devices = {}

    @staticmethod
    def has_device(identity):
        return identity in DeviceManager.devices

    @staticmethod
    def get_device(identity):
        if DeviceManager.has_device(identity) is False:
            raise DeviceNotFound(identity)
        return DeviceManager.devices[identity]

    @staticmethod
    def get_devices():
        return DeviceManager.devices.values()

    @staticmethod
    def _generate_identity(name):
        identity = f"{name}_{int(time.time())}"
        return identity

    @staticmethod
    def create_device(params):
        """
            @param params: dict where required key is 'name'
            @return: Device
        """
        if "name" not in params:
            raise WrongDeviceParams(params.get("identity", "undefined"), params, "Device should has name!!!")

        if "identity" not in params:
            name = params["name"]
            identity = DeviceManager._generate_identity(name)
            params["identity"] = identity

        if "icon_path" in params and params["icon_path"] is not None:
            if os.path.exists(params["icon_path"]) is False:
                raise FileNotFoundError(f"Device [{params['identity']}] icon not found: {params['icon_path']}")

        try:
            device = Device(params)
        except Exception as e:
            raise WrongDeviceParams(params["identity"], params, str(e))

        DeviceManager.devices[device.identity] = device
        DeviceManager.EVENT_CREATE_DEVICE(device)

        return device

    @staticmethod
    def create_devices():
        if os.path.exists(DEFAULT_DEVICES_PATH) is False:
            return

        with open(DEFAULT_DEVICES_PATH, "r") as f:
            create_params = json.load(f)

        for device_id, params in create_params.items():
            params["identity"] = device_id
            DeviceManager.create_device(params)

    @staticmethod
    def remove_device(identity):
        if DeviceManager.has_device(identity) is False:
            return
        del DeviceManager.devices[identity]
