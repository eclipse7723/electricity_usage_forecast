from src.model.model import Model
from src.event import EventCollection


class Controller:

    def __init__(self):
        self._model = Model()
        self._add_observers()

    # callbacks

    def _add_observers(self):
        EventCollection.addObserver("onDeviceCardClickedAdd", self._cb_clicked_add)
        EventCollection.addObserver("onDeviceCardClickedRemove", self._cb_clicked_remove)

    def _cb_clicked_add(self, device_card):
        identity = device_card.device.identity
        self._model.devices.increase_device_amount(identity)
        return False

    def _cb_clicked_remove(self, device_card):
        identity = device_card.device.identity
        self._model.devices.decrease_device_amount(identity)
        return False
