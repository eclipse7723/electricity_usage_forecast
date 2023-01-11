from src.exceptions.ui import CLICommandTestFailed


class BaseCommand:

    def __init__(self):
        self.alias = self.__class__.__name__
        self.description = f"{self.__class__.__name__} - default description"
        self._on_params()

        is_test_failed, test_fail_message = self.test()
        if is_test_failed is False:
            raise CLICommandTestFailed(self.__class__.__name__, test_fail_message)

    def _on_params(self):
        pass

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def test(self):
        return True
