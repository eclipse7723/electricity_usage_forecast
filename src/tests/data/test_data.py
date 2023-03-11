DAYS_PERIOD = 31

TARIFF_THRESHOLD = 250.0
TARIFF_BELOW_PRICE = 1.44
TARIFF_ABOVE_PRICE = 1.68

TEST_DEVICE_ID = "__test_device"
TEST_DEVICE_PARAMS = dict(
    name="test_device",
    identity=TEST_DEVICE_ID,
    usage_day_hours=12,
    usage_days="period",
    kWh=1.06,   # 1060 watt
    amount=155
)


TEST_DEVICE_PERIOD_USAGE = (DAYS_PERIOD * TEST_DEVICE_PARAMS["usage_day_hours"]) * \
                           TEST_DEVICE_PARAMS["amount"] * TEST_DEVICE_PARAMS["kWh"]
if TEST_DEVICE_PERIOD_USAGE > TARIFF_THRESHOLD:
    TEST_DEVICE_PERIOD_PRICE = (TARIFF_THRESHOLD * TARIFF_BELOW_PRICE) + \
                               (TEST_DEVICE_PERIOD_USAGE - TARIFF_THRESHOLD) * TARIFF_ABOVE_PRICE
else:
    TEST_DEVICE_PERIOD_PRICE = TEST_DEVICE_PERIOD_USAGE * TARIFF_BELOW_PRICE


def setup_test_device(device_controller):
    device_controller.create_device(TEST_DEVICE_PARAMS)
    device_controller.add_device(TEST_DEVICE_ID)


def setup_test_specific_device(device_controller, suffix):
    updated_params = TEST_DEVICE_PARAMS.copy()
    updated_params["name"] += suffix
    updated_params["identity"] += suffix

    device_controller.create_device(updated_params)
    device_controller.add_device(updated_params["identity"])


def setup_test_tariff_to_model(model):
    model.tariff.change_threshold(TARIFF_THRESHOLD)
    model.tariff.set_price(TARIFF_BELOW_PRICE, TARIFF_ABOVE_PRICE)


def setup_test_period_to_model(model):
    model.period.update_days(DAYS_PERIOD)


def setup_test_model(model):
    setup_test_device(model.devices)
    setup_test_tariff_to_model(model)
    setup_test_period_to_model(model)


class RandomDeviceGenerator:
    name_template = "random device #{num}"
    identity_template = "__random_device_{num}"
    generated = 0

    def __init__(self, device_controller):
        self.controller = device_controller
        self.generated_params = {}

    def __call__(self, allow_problem_params=True):
        params = self.create_params(self.generated+1, allow_problem_params)

        device = self.controller.create_device(params)

        self.generated += 1
        self.generated_params[self.generated] = params

        return params, device

    def get(self, key):
        return self.generated_params[key]

    def has(self, key):
        return key in self.generated_params

    def create_params(self, num, allow_problem_params):
        if allow_problem_params is True:
            device_params = self._generate_problem_params(num)
        else:
            device_params = self._generate_normal_params(num)

        if device_params["usage_days"] == DAYS_PERIOD:
            device_params["usage_days"] = "period"

        return device_params

    def _generate_normal_params(self, num):
        import random

        device_params = dict(
            name=self.name_template.format(num=num),
            identity=self.identity_template.format(num=num),
            usage_day_hours=random.randint(0, 24),
            usage_days=random.randint(0, DAYS_PERIOD),
            amount=random.randint(1, 100),
        )

        if self.generated % 2 == 0:
            device_params["watt"] = random.randint(0, 100000)
        else:
            device_params["kWh"] = round(random.random() * random.randint(1, 100), 3)

        return device_params

    def _generate_problem_params(self, num):
        import random

        device_params = dict(
            name=self.name_template.format(num=num),
            identity=self.identity_template.format(num=num),
            usage_day_hours=random.randint(-1, 25),
            usage_days=random.randint(-1, DAYS_PERIOD+5),
            amount=random.randint(-1, 100),
        )

        if self.generated % 2 == 0:
            device_params["watt"] = random.randint(-100, 100000)
        else:
            device_params["kWh"] = round((random.random()-0.5) * random.randint(1, 100), 3)

        return device_params

    def extract_random_device_number(self, identity):
        template = self.identity_template.replace("{num}", "")
        if template not in identity:
            raise ValueError(f"Identity {identity} do not match template {self.identity_template!r}")

        number = int(identity.replace(template, ""))
        return number
