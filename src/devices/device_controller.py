from src.devices.device_manager import DeviceManager
from src.exceptions.device import *
from src.settings import DEFAULT_DEVICES_SAVE_PATH
from src.event import Event

import json
import os
import warnings


class DeviceController:

    EVENT_CONNECT_DEVICE = Event("onDeviceConnect")
    EVENT_DISCONNECT_DEVICE = Event("onDeviceDisconnect")

    def __init__(self):
        self.connected_devices = {}
        self.saves_path = DEFAULT_DEVICES_SAVE_PATH

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
        if identity in self.connected_devices:
            raise DeviceAlreadyConnected(identity)
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

    def remove_all(self):
        for device in self.get_devices():
            self.remove_device(device.identity)

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

    def save_devices(self):
        """ saves connected devices with their characteristics """
        saves = {}

        for device in self.connected_devices.values():
            save = device.get_save()
            saves.update(save)

        with open(self.saves_path, "w") as f:
            json.dump(saves, f, indent=4)

    def load_devices(self):
        """ load saved connected devices from save """
        if os.path.exists(self.saves_path) is False:
            raise NoSavedDevicesError(self.saves_path)

        with open(self.saves_path, "r") as f:
            try:
                saves = json.load(f)
            except json.decoder.JSONDecodeError as e:
                warnings.warn(f"saves from {self.saves_path!r} is empty")
                saves = {}

        for identity, params in saves.items():
            if self.has_device(identity) is False:
                # that device is not connected - connect it first

                if DeviceManager.has_device(identity) is False:
                    # device is not exists - create
                    params["identity"] = identity
                    self.create_device(params)

                # try to connect this device
                if self.add_device(identity) is False:
                    warnings.warn(f"can't connect device {identity!r}")
                    continue

            device = self.get_device(identity)
            device.update_params(params)

    def set_saves_path(self, path):
        if path.endswith(".json") is False:
            raise TypeError(f"save file must be .json, not {path!r}")
        self.saves_path = path
