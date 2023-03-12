import unittest
from src.devices.device_controller import DeviceController
from src.tests.data.test_data import RandomDeviceGenerator, DAYS_PERIOD
from src.model.period import Period


TEST_DEVICES_COUNT = 3
TEST_SAVE_PATH = "test_save_devices.json"


class DeviceControllerTests(unittest.TestCase):

    def setUp(self):
        self.controller = DeviceController()
        self._randomizer = RandomDeviceGenerator(self.controller)

        Period.update_days(DAYS_PERIOD)

        for i in range(1, TEST_DEVICES_COUNT + 1):
            params, device = self._randomizer(allow_problem_params=False)
            self.controller.add_device(device.identity)

            print(f"ADD DEVICE {device.identity} with initial params: {params}")

    def test_setup_devices(self):
        # check actual connected devices
        _connected_devices = self.controller.get_devices()
        self.assertEqual(TEST_DEVICES_COUNT, len(_connected_devices), "Wrong number of connected devices")

    def test_save_load_devices(self):
        # update saves path
        self.controller.set_saves_path(TEST_SAVE_PATH)
        self.assertEqual(TEST_SAVE_PATH, self.controller.saves_path, "Path with saved devices is wrong")

        self.controller.save_devices()

        # check if save has been created
        from os import path
        self.assertTrue(path.exists(TEST_SAVE_PATH), "Save devices not found")

        # disconnect all devices and check size
        self.controller.remove_all()
        _connected_devices = self.controller.get_devices()
        self.assertEqual(0, len(_connected_devices), "Wrong number of connected devices")

        # load and connect previous devices
        self.controller.load_devices()

        # check is devices have been connected
        _connected_devices = self.controller.get_devices()
        self.assertEqual(TEST_DEVICES_COUNT, len(_connected_devices), "Wrong number of loaded devices")

        for device in _connected_devices:
            self._check_loaded_device(device)

    # utils

    def _check_loaded_device(self, device):
        params_number = self._randomizer.extract_random_device_number(device.identity)
        initial_params = self._randomizer.get(params_number)
        actual_params = device.get_save()[device.identity]

        for key, value in initial_params.items():
            if key == "kWh":
                # convert to watt
                key = "watt"
                value *= 1000.0

            actual_value = actual_params[key]
            self.assertEqual(value, actual_value, f"{device.identity}: wrong load {key!r}")

