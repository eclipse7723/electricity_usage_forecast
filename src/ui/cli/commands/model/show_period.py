from src.ui.cli.commands.base_command import BaseCommand
from src.ui.cli.components.colors import Colors


class CommandPeriodShow(BaseCommand):

    def _activate(self, *args, **kwargs):
        period = self._interface.controller.get_period()
        print(f"Current period (days): {Colors.wrap('yellow', period)}")

    def _setup_params(self):
        self.alias = "show period"
        self.description = "shows current period in days"
