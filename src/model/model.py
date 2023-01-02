from src.model.tariff import Tariff
from src.model.period import Period
from src.devices.device_controller import DeviceController


class Model:

    def __init__(self):
        self.tariff = Tariff()
        self.period = Period()
        self.devices = DeviceController()

    def change_days_period(self, days):
        self.period.update_days(days)

    def get_days_period(self):
        return self.period.get_days()

    def calculate_total_price(self, total_energy):
        price = self.tariff.calculate_price(total_energy)
        return price

    def calculate_energy_consumption(self):
        total_energy = 0
        for device in self.devices.get_devices():
            total_energy += device.usage_day_hours * device.usage_day_hours
        return total_energy
