from src.ui.cli.commands.base_command import BaseCommand
from src.ui.cli.components.colors import Colors


class CommandTariffShow(BaseCommand):

    def _activate(self, *args, **kwargs):
        threshold = self._interface.controller.get_tariff_threshold()
        below_price, above_price = self._interface.controller.get_tariff_price()

        print(f"Tariff threshold is {Colors.wrap('yellow', threshold)}. "
              f"Price for 1 kWh below threshold = {Colors.wrap('yellow', below_price)}, "
              f"and above = {Colors.wrap('yellow', above_price)}")

    def _setup_params(self):
        self.alias = "show tariff"
        self.description = "shows current tariff for kWh with threshold"
