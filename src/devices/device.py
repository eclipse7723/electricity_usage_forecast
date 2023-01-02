from src.model.period import Period
from src.settings import DEFAULT_DEVICE_ICON_PATH


class Device:
    def __init__(self, params):
        self._id = params["id"]
        self.name = params["name"]
        self.icon_path = params.get("icon_path", DEFAULT_DEVICE_ICON_PATH)

        self.__power = 0    # watt
        self.__usage_days = 0
        self.__usage_day_hours = 0

        self.set_usage_day_hours(params.get("usage_day_hours", 0))
        self.set_usage_days(params.get("usage_days", Period.days))
        if "watt" in params:
            self.set_watt(params["watt"])
        elif "kWh" in params:
            self.set_kWh(params["kWh"])

    @property
    def usage_days(self):
        return self.__usage_days

    def set_usage_days(self, days):
        if days >= Period.days:
            raise ValueError(f"days ({days}) can't be above period ({Period.days})")
        if days < 0:
            raise ValueError(f"days ({days}) can't be negative")
        self.__usage_days = days

    @property
    def usage_day_hours(self):
        return self.__usage_day_hours

    def set_usage_day_hours(self, hours):
        if hours < 0 or hours > 24:
            raise ValueError(f"hours must be in range [0, 24], not {hours}")
        self.__usage_day_hours = hours

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
