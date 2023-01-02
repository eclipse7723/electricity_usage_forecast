from src.settings import DEFAULT_DAYS_PERIOD


class Period:

    days = DEFAULT_DAYS_PERIOD

    @staticmethod
    def get_days():
        return Period.days

    @staticmethod
    def update_days(days):
        if days <= 0 or isinstance(days, int) is False:
            raise ValueError(f"Period ({days}) can't be 0 or negative integer")
        Period.days = days
