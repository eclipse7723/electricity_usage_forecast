def import_command(module, name):
    pass


def init_commands():
    module = "src.ui.cli.commands"
    commands = [
        "add_device"
    ]

    for command in commands:
        import_command(module, command)
