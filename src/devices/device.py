from src.model.period import Period
from src.settings import DEFAULT_DEVICE_ICON_PATH, _DEBUG
from src.event import Event


class Device:

    EVENT_ICON_CHANGE = Event("onDeviceIconChange")
    EVENT_USAGE_DAYS_UPDATE = Event("onDeviceUsageDaysUpdate")
    EVENT_USAGE_HOURS_UPDATE = Event("onDeviceUsageHoursUpdate")
    EVENT_POWER_UPDATE = Event("onDevicePowerUpdate")
    EVENT_AMOUNT_UPDATE = Event("onDeviceAmountUpdate")

    if _DEBUG:
        def __repr__(self):
            return f"<Device [{self.identity}] {self.name!r}>"

    def __init__(self, params):
        self.identity = params["identity"]
        self.name = params["name"]
        self.icon_path = params.get("icon_path", DEFAULT_DEVICE_ICON_PATH)

        self.__amount = 1
        self.__power = 0    # watt
        self.__usage_days = 0
        self.__usage_day_hours = 0

        self.set_usage_day_hours(params.get("usage_day_hours", 0))
        self.set_usage_days(params.get("usage_days", "period"))
        if "watt" in params:
            self.set_watt(params["watt"])
        elif "kWh" in params:
            self.set_kWh(params["kWh"])
        self.set_amount(params.get("amount", 1))

        self._add_observer()

    @property
    def usage_days(self):
        if self.__usage_days == "period":
            return Period.get_days()
        return self.__usage_days

    def set_usage_days(self, days):
        if days == "period":
            self._set_usage_days_as_period()
        else:
            self._set_usage_days(days)

    def _set_usage_days_as_period(self):
        self.__usage_days = "period"
        Device.EVENT_USAGE_DAYS_UPDATE(self, Period.get_days())

    def _set_usage_days(self, days):
        if days > Period.get_days():
            raise ValueError(f"days ({days}) can't be above period ({Period.get_days()})")
        if days < 0:
            raise ValueError(f"days ({days}) can't be negative")
        self.__usage_days = int(days)
        Device.EVENT_USAGE_DAYS_UPDATE(self, days)

    @property
    def usage_day_hours(self):
        return self.__usage_day_hours

    def set_usage_day_hours(self, hours):
        if hours < 0 or hours > 24:
            raise ValueError(f"hours must be in range [0, 24], not {hours}")
        self.__usage_day_hours = hours
        Device.EVENT_USAGE_HOURS_UPDATE(self, hours)

    @property
    def power(self):
        return self.__power

    def set_kWh(self, kwh):
        power = kwh * 100.0
        self._set_power(power)

    def set_watt(self, watt):
        self._set_power(watt)

    def _set_power(self, power):
        if power < 0:
            raise ValueError(f"power ({power}) must be positive value")
        self.__power = power
        Device.EVENT_POWER_UPDATE(self, power)

    @property
    def amount(self):
        return self.__amount

    def set_amount(self, amount):
        if amount < 1:
            raise ValueError(f"amount should be >= 1, not {amount}")
        self.__amount = amount
        Device.EVENT_AMOUNT_UPDATE(self, amount)

    def set_icon_path(self, path):
        self.icon_path = path
        Device.EVENT_ICON_CHANGE(self, path)

    def set_name(self, name):
        self.name = name

    # save\restore

    def get_save(self):
        """ returns dict with device params """
        save = {
            self.identity: {
                "identity": self.identity,
                "name": self.name,
                "icon_path": self.icon_path,
                "usage_days": self.__usage_days,
                "usage_day_hours": self.usage_day_hours,
                "watt": self.power,
                "amount": self.amount,
            }
        }
        return save

    def update_params(self, params):
        for param, value in params.items():
            setter_name = f"set_{param}"
            if setter_name not in dir(self):
                continue
            setter = self.__getattribute__(setter_name)
            setter(value)

    # callbacks

    def _add_observer(self):
        Period.EVENT_UPDATE.addObserver(self._cb_period_update)

    def _cb_period_update(self, days):
        if self.usage_days > days:
            self.__usage_days = days
        return False
