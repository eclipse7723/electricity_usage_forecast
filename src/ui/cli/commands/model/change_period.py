from src.ui.cli.commands.base_command import BaseCommand, with_accept_message


class CommandPeriodChange(BaseCommand):

    @with_accept_message
    def _activate(self, *args, **kwargs):
        days = int(input("days: "))
        self._interface.controller.change_period(days)
        return True

    def _setup_params(self):
        self.alias = "change period"
        self.description = "change period"
