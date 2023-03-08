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


def setup_test_device_to_model(model):
    model.devices.create_device(TEST_DEVICE_PARAMS)
    model.devices.add_device(TEST_DEVICE_ID)


def setup_test_tariff_to_model(model):
    model.tariff.change_threshold(TARIFF_THRESHOLD)
    model.tariff.set_price(TARIFF_BELOW_PRICE, TARIFF_ABOVE_PRICE)


def setup_test_period_to_model(model):
    model.period.update_days(DAYS_PERIOD)


def setup_test_model(model):
    setup_test_device_to_model(model)
    setup_test_tariff_to_model(model)
    setup_test_period_to_model(model)