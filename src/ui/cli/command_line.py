from src.ui.base_interface import BaseInterface
from src.ui.cli.components.device_card import DeviceCard
from src.ui.cli.components.colors import Colors
import os


def with_accept_message(func):
    def _wrapper():
        func()
        Colors.print("green", "Your changes has been accepted!")
    return _wrapper


class CommandLineInterface(BaseInterface):

    def _set_params(self):
        self.commands = {
            "my devices": [self.show_my_devices, "shows your devices"],
            "commands": [self.show_commands, "shows all available commands"],
            "stop": [self.stop, "stop the program"],
            "add device": [self.add_device, "connect a new device"],
            "remove device": [self.remove_device, "disconnect device"],
            "edit device": [self.edit_my_device, "edit my device (type 'my devices' to view their identities)"],
            "calculate": [self.calculate, "calculate your expected energy consumption and price at this period"],
            "current period": [self.show_current_period, "shows current period in days"],
            "change period": [self.change_current_period, "change period"],
            "show tariff": [self.show_tariff, "shows current tariff for kWh with threshold"],
            "change tariff": [self.change_tariff, "change tariff and threshold"]
        }
        self.my_devices = {device.identity: DeviceCard(device)
                           for device in self.controller.get_connected_devices()}

    def _show_error(self, exception):
        """ notify user about error """
        Colors.print("red", f"[!!!] {exception}")

    def _show_tip(self, text):
        Colors.print("yellow", f"[*]{text}")

    # command's base

    def show_commands(self):
        print("All available commands:")
        for command, (func, descr) in self.commands.items():
            print(f"  {Colors.wrap('green', command)} - {descr}")
        print()

    def __get_command_func(self, alias):
        func, descr = self.commands[alias]
        return func

    def _enter_command(self):
        command = input("> ").lower()

        if self.is_running() is False:
            return

        if command not in self.commands:
            self._show_error(f"Command {command!r} not found")
            self.show_commands()
            return

        func = self.__get_command_func(command)
        try:
            func()
        except Exception as e:
            self._show_error(str(e))

    # commands

    def show_my_devices(self):
        if len(self.my_devices) == 0:
            print("empty list")
            return
        for card in self.my_devices.values():
            print(str(card))

    @with_accept_message
    def edit_my_device(self):
        if len(self.my_devices) == 0:
            self._show_error("Connect at least one device. Type 'add device'")
            return

        identity = input("Device identity: ").lower()
        if identity not in self.my_devices:
            self._show_error(f"Device with identity {identity!r} not found")
            return

        card = self.my_devices[identity]
        card.edit()

    @with_accept_message
    def add_device(self):
        not_connected_devices = self.controller.get_not_connected_devices()
        print("List of not connected devices:")
        for device in not_connected_devices:
            print(f" [{Colors.wrap('yellow', device.identity)}] {device.name!r} ({device.power} Watt)")
        print("Type identity from square brackets to add device")

        identity = input("Identity: ").lower()

        if identity not in not_connected_devices:
            self._show_error(f"Device with id '{identity}' not found")
            return

        self.controller.connect_device(identity)

    @with_accept_message
    def remove_device(self):
        identity = input("Identity: ").lower()

        if identity not in self.controller.get_connected_devices():
            self._show_error(f"Device with id {identity!r} not found in connected devices - type 'my devices' to check")
            return

        self.controller.disconnect_device(identity)

    def calculate(self):
        energy = self.controller.get_energy_consumption()
        price = self.controller.get_period_price()
        period = self.controller.get_period()
        print(f"Your energy consumption for period of {Colors.wrap('yellow', period)} days"
              f" is {Colors.wrap('yellow', energy)} kWh, so price is {Colors.wrap('yellow', price)}")

    def show_current_period(self):
        period = self.controller.get_period()
        print(f"Current period (days): {Colors.wrap('yellow', period)}")

    @with_accept_message
    def change_current_period(self):
        days = int(input("days: "))
        self.controller.change_period(days)

    def show_tariff(self):
        threshold = self.controller.get_tariff_threshold()
        below_price, above_price = self.controller.get_tariff_price()
        print(f"Tariff threshold is {Colors.wrap('yellow', threshold)}. "
              f"Price for 1 kWh below threshold = {Colors.wrap('yellow', below_price)}, "
              f"and above = {Colors.wrap('yellow', above_price)}")

    @with_accept_message
    def change_tariff(self):
        threshold = float(input("New threshold: "))
        below_price = float(input("New price below threshold: "))
        above_price = float(input("New price above threshold: "))
        self.controller.change_tariff_threshold(threshold)
        self.controller.change_tariff_price(below_price, above_price)

    # interface flow

    def _prepare(self):
        os.system("title Electricity usage forecast")
        os.system("cls")
        self.show_commands()

    def _start(self):
        while self.is_running():
            self._enter_command()

    def _stop(self):
        pass