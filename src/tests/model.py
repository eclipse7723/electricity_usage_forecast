import unittest
from src.model.model import Model
from src.tests.data.test_data import *


class ModelTests(unittest.TestCase):

    def setUp(self):
        model = Model()
        setup_test_model(model)

        self.model = model

    def test_device_setup(self):
        connected_devices = self.model.devices.get_devices()

        self.assertEqual(1, len(connected_devices), "Wrong number of connected devices")
        self.assertTrue(self.model.devices.has_device(TEST_DEVICE_ID), "Test device not found")

        test_device = self.model.devices.get_device(TEST_DEVICE_ID)

        self.assertEqual(TEST_DEVICE_PARAMS["name"], test_device.name)
        self.assertEqual(TEST_DEVICE_PARAMS["identity"], test_device.identity)
        self.assertEqual(TEST_DEVICE_PARAMS["usage_day_hours"], test_device.usage_day_hours)
        self.assertEqual(DAYS_PERIOD, test_device.usage_days)
        self.assertAlmostEqual(TEST_DEVICE_PARAMS["kWh"]*1000.0, test_device.power, 1)
        self.assertEqual(TEST_DEVICE_PARAMS["amount"], test_device.amount)

    def test_period_setup(self):
        current_period = self.model.period.get_days()

        self.assertEqual(current_period, DAYS_PERIOD)

    def test_devices_react_on_period_update(self):
        current_period = self.model.period.get_days()
        test_device = self.model.devices.get_device(TEST_DEVICE_ID)

        self.assertEqual(current_period, test_device.usage_days, "Usage days of test device is not same as period")

        new_period = 123
        self.model.period.update_days(new_period)
        self.assertEqual(new_period, test_device.usage_days, "Usage days of test device didn't change (1)")

        self.model.period.update_days(current_period)
        self.assertEqual(current_period, test_device.usage_days, "Usage days of test device didn't change (2)")

    def test_tariff_setup(self):
        current_threshold = self.model.tariff.threshold
        below_price, above_price = self.model.tariff.get_price()

        self.assertEqual(TARIFF_THRESHOLD, current_threshold, "Tariff threshold didn't changed on setup")
        self.assertEqual(TARIFF_BELOW_PRICE, below_price, "Tariff below price didn't changed on setup")
        self.assertEqual(TARIFF_ABOVE_PRICE, above_price, "Tariff above price didn't changed on setup")

    def test_price_calculate(self):
        kWh = self.model.calculate_energy_consumption() / 1000.0
        self.assertGreater(kWh, 0, "Impossible to have <= 0 consumed energy")
        self.assertAlmostEqual(TEST_DEVICE_PERIOD_USAGE, kWh, 1, "Wrong calculated usage for period")

        price = self.model.calculate_total_price(kWh)
        self.assertGreater(price, 0, "Impossible to have <= 0 price")
        self.assertAlmostEqual(TEST_DEVICE_PERIOD_PRICE, price, 1, "Wrong calculated price")
