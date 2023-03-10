from src.model.model import Model
from src.devices.device_manager import DeviceManager


class Controller:

    def __init__(self):
        self._model = Model()

    # public - getters

    def get_connected_devices(self):
        """ :returns: list of connected devices """
        devices = self._model.devices.get_devices()
        return devices

    def get_all_devices(self):
        """ :returns: list of all existing devices """
        devices = DeviceManager.get_devices()
        return devices

    def get_not_connected_devices(self):
        """ :returns: list of not connected devices"""
        connected_devices = self.get_connected_devices()
        all_devices = self.get_all_devices()
        not_connected_devices = list(set(all_devices) - set(connected_devices))
        return not_connected_devices

    def get_period_energy_consumption_watt(self):
        """ :returns: consumed energy (in watt) of current period """
        total_watt = self._model.calculate_energy_consumption()
        return total_watt

    def get_period_energy_consumption_kwh(self):
        """ :returns: consumed energy (in kWh) in current period """
        total_kWh = self._model.calculate_energy_consumption() / 1000.0
        return total_kWh

    def get_period_price(self):
        """ :returns: price of consumed energy in current period """
        total_kWh = self.get_period_energy_consumption_kwh()
        price = self._model.calculate_total_price(total_kWh)
        return price

    def get_period(self):
        """ :returns: period days """
        return self._model.period.get_days()

    def get_tariff_threshold(self):
        """ :returns: tariff threshold """
        return self._model.tariff.threshold

    def get_tariff_price(self):
        """ :returns: price below tariff threshold and above """
        return self._model.tariff.get_price()

    def get_saves_path(self):
        return self._model.devices.saves_path

    # public - actions

    def connect_device(self, identity: str) -> bool:
        """ :raises: DeviceAlreadyConnected """
        return self._model.devices.add_device(identity)

    def disconnect_device(self, identity: str) -> bool:
        return self._model.devices.remove_device(identity)

    def disconnect_all_devices(self):
        self._model.devices.remove_all()

    def change_period(self, days: int):
        """ raises ValueError if something went wrong """
        self._model.period.update_days(days)

    def change_tariff_threshold(self, threshold: float):
        self._model.tariff.change_threshold(threshold)

    def change_tariff_price(self, below_price: float, above_price: float):
        self._model.tariff.set_price(below_price, above_price)

    def increase_device_amount(self, identity: str) -> bool:
        return self._model.devices.increase_device_amount(identity)

    def decrease_device_amount(self, identity: str) -> bool:
        return self._model.devices.decrease_device_amount(identity)

    def set_save_devices_path(self, path):
        self._model.devices.set_saves_path(path)

    def get_save_devices_path(self):
        return self._model.devices.saves_path

    def save_devices(self):
        self._model.devices.save_devices()

    def load_devices(self):
        """ Raises NoSavedDevicesError if no saves found """
        self._model.devices.load_devices()
