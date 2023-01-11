from src.ui.cli.components.colors import Colors


class DeviceCard:

    def __init__(self, device):
        self.device = device
        self._editable = {
            "amount": device.set_amount,
            "power": device.set_watt,
            "name": device.set_name,
            "hours": device.set_usage_day_hours,
            "days": device.set_usage_days,
            "icon": device.set_icon_path
        }

    def __repr__(self):
        return f"<DeviceCard {self.device.identity!r}>"

    def __str__(self):
        device = self.device

        descr = f"* {Colors.wrap('yellow', device.name)} [{Colors.wrap('red', device.identity)}]"
        template = "\n{param:>16}: {value}"
        descr += template.format(param="amount", value=Colors.wrap('yellow', device.amount))
        descr += template.format(param="power (Watt)", value=Colors.wrap('yellow', device.power))
        if device.usage_day_hours < 1:
            descr += template.format(param="daily usage",
                                     value=Colors.wrap('yellow', device.usage_day_hours*60) + " minutes")
        else:
            descr += template.format(param="daily usage",
                                     value=Colors.wrap('yellow', device.usage_day_hours) + " hours")
        descr += template.format(param="days usage", value=Colors.wrap('yellow', device.usage_days) + " days")
        descr += template.format(param="icon path", value=Colors.wrap('yellow', device.icon_path))
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


