from src.ui.cli.commands.base_command import BaseCommand


class CommandStopInterface(BaseCommand):

    def _setup_params(self):
        self.alias = "stop"
        self.description = "stop the program"

    def _activate(self, *args, **kwargs):
        self._interface.stop()
