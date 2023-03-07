from src.ui.cli.commands.base_command import BaseCommand
from src.ui.cli.components.colors import Colors


class CommandCalculate(BaseCommand):

    def _activate(self, *args, **kwargs):
        energy = self._interface.controller.get_period_energy_consumption_kwh()
        price = self._interface.controller.get_period_price()
        period = self._interface.controller.get_period()
        print(f"Your energy consumption for period of {Colors.wrap('yellow', period)} days"
              f" is {Colors.wrap('yellow', energy)} kWh, so price is {Colors.wrap('yellow', price)}")

    def _setup_params(self):
        self.alias = "calculate"
        self.description = "calculate your expected energy consumption and price at this period"
