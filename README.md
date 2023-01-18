## Electricity usage forecast

### Requirements
Run `install_requirements.bat` to install all requirements.

### Settings
Open `src/settings.py` and edit the settings as you like.

### How to create new devices?
Open `res/devices.json` and add new section, where key is device identity (should be lowercase word with underscore as spaces) and body is a dict with possible key-values:
* `name` (required) - full name of this device,
* `watt` or `kWh` (required) - how many energy does device use per hour,
* `usage_days` (default: as period) - how many days does this device work,
* `usage_day_hours` (default: 24) - how many hours does this device work per day,
* `icon_path` (only for GUI, default from `settings.py`) - full or relative path to image with icon.

---

### How it works?
Add your devices, set their power (in Watt or kWh) and how often do you use them.
Then use the `calculate` command.
You will receive something like that:

<img src="https://i.imgur.com/1Hpkcsi.png" alt="calculate results">