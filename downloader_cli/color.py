"""
Handle color related util functions
"""

from typing import Dict


class ShellColor:
    def __init__(self):
        pass

    def __get_color_map(self) -> Dict:
        return {
            'reset': 0,
            'black': 30,
            'red': 31,
            'green': 32,
            'yellow': 33,
            'blue': 34,
            'magenta': 35,
            'cyan': 36,
            'white': 37
        }

    def __is_raw_color(self, color: str) -> bool:
        return color.startswith("\e[") or color.startswith("\033[")

    def __get_reset_color(self) -> str:
        return "\033[0m"

    @property
    def reset(self) -> str:
        return self.__get_reset_color()

    def __build_color_str(self, color_number: int) -> str:
        return f"\033[1;{color_number}m" if color_number != 0 else self.reset

    def is_valid_color(self, color: str) -> bool:
        """
        Check if the passed color is a valid color.

        This method will always return `true` if a raw color string is passed.

        `reset` will not be considered a valid color
        """
        return bool(self.__get_color_map().get(color, 0)) if not self.__is_raw_color(color) else True

    def wrap_in_color(self, to_wrap: str, color: str, skip_reset: bool = False) -> str:
        """
        Wrap the passed string in the provided color and accordingly
        set reset if `skip_reset` is not `False`

        If an empty string is passed for the `color` value, then the `to_wrap` string will
        be returned as is, without any modifications.
        """
        if color == "":
            return to_wrap

        if not self.__is_raw_color(color):
            color_number = self.__get_color_map().get(color, 0)
            if not bool(color_number):
                raise ValueError(
                    'invalid value passed for `color`. Please use `is_valid_color()` to validate the color before using.')

            color = self.__build_color_str(color_number)

        reset_to_add = self.reset
        if skip_reset:
            reset_to_add = ""

        return f"{color}{to_wrap}{reset_to_add}"
