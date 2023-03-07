from src.ui.cli.commands.base_command import BaseCommand


class CommandMyDevices(BaseCommand):

    def _activate(self, *args, **kwargs):
        my_devices = self._interface.my_devices

        if len(my_devices) == 0:
            print("empty list")
            return

        for card in my_devices.values():
            print(str(card))

    def _setup_params(self):
        self.alias = "my devices"
        self.description = "shows all of your connected devices"
