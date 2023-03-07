from src.ui.base_interface import BaseInterface
from src.ui.cli.components.device_card import DeviceCard
from src.ui.cli.components.colors import Colors
from src.ui.cli.components.command_tree import CommandTree
from src.settings import _DEBUG

import traceback
import os


class CommandLineInterface(BaseInterface):

    alias = "cli"

    def _set_params(self):
        self.commands = CommandTree(self)
        self.my_devices = {device.identity: DeviceCard(device)
                           for device in self.controller.get_connected_devices()}
        self.__observers = []

    def show_error(self, exception):
        """ notify user about error """
        if _DEBUG is True:
            traceback.print_stack()
        Colors.print("red", f"[!!!] {exception}")

    def show_tip(self, text):
        print(f"{Colors.wrap('yellow', '[*]')} {text}")

    # callbacks

    def _add_observers(self):
        self._add_observer("onDeviceConnect", self._cb_device_connected)
        self._add_observer("onDeviceDisconnect", self._cb_device_disconnected)

    def _cb_device_connected(self, device):
        self.my_devices[device.identity] = DeviceCard(device)
        return False

    def _cb_device_disconnected(self, device):
        del self.my_devices[device.identity]
        return False

    # interface flow

    def _prepare(self):
        os.system("title Electricity usage forecast")
        os.system("cls")
        self._add_observers()
        self.commands.show_commands()

    def _start(self):
        while self.is_running():
            self.commands.enter()

    def _stop(self):
        self.commands = None
        self.my_devices = None
