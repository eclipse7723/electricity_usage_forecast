from src.ui.cli.commands.base_command import BaseCommand, with_accept_message


class CommandTariffChange(BaseCommand):

    @with_accept_message
    def _activate(self, *args, **kwargs):
        threshold = float(input("New threshold: "))
        below_price = float(input("New price below threshold: "))
        above_price = float(input("New price above threshold: "))
        self._interface.controller.change_tariff_threshold(threshold)
        self._interface.controller.change_tariff_price(below_price, above_price)
        return True

    def _setup_params(self):
        self.alias = "change tariff"
        self.description = "change tariff and threshold"
