class Colors:
    reset = "\u001b[0m"

    palette = {
        "red": "\u001b[31m",
        "green": "\u001b[32m",
        "yellow": "\u001b[33m",
        "blue": "\u001b[34m",
        "magenta": "\u001b[35m",
        "white": "\u001b[37m",
    }

    @staticmethod
    def print(color, text):
        colored = Colors.wrap(color, text)
        print(colored)

    @staticmethod
    def wrap(color, text):
        color_code = Colors.palette.get(color, Colors.default())
        return color_code + str(text) + Colors.reset

    @staticmethod
    def default():
        return Colors.palette["white"]
