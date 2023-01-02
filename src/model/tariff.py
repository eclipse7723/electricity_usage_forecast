from src.settings import DEFAULT_TARIFF_THRESHOLD, DEFAULT_TARIFF_BELOW_PRICE, DEFAULT_TARIFF_ABOVE_PRICE
from src.event import Event


class Tariff:

    EVENT_THRESHOLD_UPDATE = Event("onTariffThresholdUpdate")
    EVENT_PRICE_UPDATE = Event("onTariffPriceUpdate")

    def __init__(self):
        self.threshold = DEFAULT_TARIFF_THRESHOLD
        self.price_below_threshold = DEFAULT_TARIFF_BELOW_PRICE
        self.price_above_threshold = DEFAULT_TARIFF_ABOVE_PRICE

    def change_threshold(self, threshold: float):
        self.threshold = threshold
        Tariff.EVENT_THRESHOLD_UPDATE(threshold)

    def set_price(self, price_below_threshold: float, price_above_threshold: float):
        self.price_below_threshold = price_below_threshold
        self.price_above_threshold = price_above_threshold
        Tariff.EVENT_PRICE_UPDATE(price_below_threshold, price_above_threshold)

    def calculate_price(self, energy):
        if energy > self.threshold:
            energy_below_threshold = self.threshold
            energy_above_threshold = energy - self.threshold
        else:
            energy_below_threshold = energy
            energy_above_threshold = 0

        price_below_threshold = energy_below_threshold * self.price_below_threshold
        price_above_threshold = energy_above_threshold * self.price_above_threshold

        price = price_below_threshold + price_above_threshold

        return price
