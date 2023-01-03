from src.model.tariff import Tariff
from src.model.period import Period
from src.devices.device_controller import DeviceController


class Model:

    def __init__(self):
        self.tariff = Tariff()
        self.period = Period()
        self.devices = DeviceController()

    def calculate_total_price(self, total_watt):
        total_kWh = total_watt / 1000.0
        price = self.tariff.calculate_price(total_kWh)
        return price

    def calculate_energy_consumption(self):
        total_energy = 0
        for device in self.devices.get_devices():
            total_energy += device.usage_days * device.usage_day_hours
        return total_energy
