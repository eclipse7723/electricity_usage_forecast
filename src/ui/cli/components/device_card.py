from src.model.period import Period


class DeviceCard:

    def __init__(self, device):
        self.device = device
        self._editable = {
            "amount": device.set_amount,
            "power": device.set_watt,
            "name": device.set_name,
            "hours": device.set_usage_day_hours,
            "days": device.set_usage_days,
        }

    def __repr__(self):
        return f"<DeviceCard {self.device.identity!r}>"

    def __str__(self):
        device = self.device
        descr = f" * Device {device.name!r}\n"
        descr += f"    identity: {device.identity}\n" \
                 f"      amount: {device.amount}\n" \
                 f"power (Watt): {device.power}\n" \
                 f" daily usage: {device.usage_day_hours} hours\n" \
                 f"  days usage: {device.usage_days}/{Period.get_days()} days\n" \
                 f"   icon path: {device.icon_path}\n"
        descr += "".center(30, "-")
        return descr

    def _edit_instructions(self):
        print("To edit device type 'param' and new value. Example: 'amount 2'")
        print("Type 'done' to stop edit process. List of editable params:")
        for param in self._editable.keys():
            print(f" - {param}")

    def _edit_error(self, msg):
        print(f"Edit error [!!!] {msg}")

    def edit(self):
        self._edit_instructions()

        while True:
            _command = input("Edit -> ").lower()
            commands = _command.split(" ")

            if len(commands) == 1 and commands[0] == "done":
                break
            elif len(commands) != 2:
                self._edit_error(f"Type param and new value!!! Not {commands}")
                continue

            command, value = commands
            try:
                value = float(value)
            except ValueError:
                pass

            if command not in self._editable:
                self._edit_error(f"Wrong command {command!r}")
                self._edit_instructions()
                continue

            func = self._editable[command]
            try:
                func(value)
            except Exception as e:
                self._edit_error(str(e))


