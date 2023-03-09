from src.ui.cli.commands.base_command import BaseCommand, with_accept_message


class CommandDeviceSave(BaseCommand):

    def _setup_params(self):
        self.alias = "save devices"
        self.description = "saves all of your connected devices with their settings"

    @with_accept_message
    def _activate(self, *args, **kwargs):
        saves_path = self._interface.controller.get_saves_path()
        self._interface.show_tip(f"Devices will be saved in {saves_path!r}")
        self._interface.controller.save_devices()
