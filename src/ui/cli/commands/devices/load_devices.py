from src.ui.cli.commands.base_command import BaseCommand, with_accept_message
from src.exceptions.device import NoSavedDevicesError


class CommandDeviceLoad(BaseCommand):

    def _setup_params(self):
        self.alias = "load devices"
        self.description = "loads connected devices from save"

    @with_accept_message
    def _activate(self, *args, **kwargs):
        try:
            self._interface.controller.load_devices()
        except NoSavedDevicesError as e:
            self._interface.show_error(str(e))
            return False

        return True
