from src.model.tariff import Tariff
from src.model.period import Period
from src.devices.device_controller import DeviceController


class Model:

    def __init__(self):
        self.tariff = Tariff()
        self.period = Period()
        self.devices = DeviceController()

    def calculate_total_price(self, total_kWh):
        price = self.tariff.calculate_price(total_kWh)
        return price

    def calculate_energy_consumption(self):
        """ returns energy in Watt """
        total_energy = 0
        for device in self.devices.get_devices():
            total_energy += device.power * (device.usage_days * device.usage_day_hours) * device.amount
        return total_energy
