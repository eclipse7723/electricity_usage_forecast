from src.model.model import Model
from src.devices.device_manager import DeviceManager
from src.event import EventCollection


class Controller:

    def __init__(self):
        self._model = Model()
        self._add_observers()

    # public - getters

    def get_connected_devices(self):
        devices = self._model.devices.get_devices()
        return devices

    def get_all_devices(self):
        devices = DeviceManager.get_devices()
        return devices

    def get_not_connected_devices(self):
        connected_devices = self.get_connected_devices()
        all_devices = self.get_all_devices()
        not_connected_devices = list(set(all_devices) - set(connected_devices))
        return not_connected_devices

    def get_period_energy_consumption(self):
        """ returns consumed energy (in kWh) in current period """
        total_watt = self._model.calculate_energy_consumption()
        return total_watt

    def get_period_price(self):
        """ returns price of consumed energy in current period """
        total_watt = self.get_period_energy_consumption()
        price = self._model.calculate_total_price(total_watt)
        return price

    def get_period(self):
        """ returns period days """
        return self._model.period.get_days()

    def get_tariff_threshold(self):
        """ returns tariff threshold """
        return self._model.tariff.threshold

    def get_tariff_price(self):
        """ returns price below tariff threshold and above """
        return self._model.tariff.get_price()

    # public - actions

    def connect_device(self, identity):
        self._model.devices.add_device(identity)

    def disconnect_device(self, identity):
        self._model.devices.remove_device(identity)

    def change_period(self, days):
        self._model.period.update_days(days)

    def change_tariff_threshold(self, threshold):
        self._model.tariff.change_threshold(threshold)

    def change_tariff_price(self, below_price, above_price):
        self._model.tariff.set_price(below_price, above_price)

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
