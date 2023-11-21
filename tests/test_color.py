"""
Handle testing the color related functionality from the
ShellColor class
"""

import pytest

from downloader_cli.color import ShellColor


class TestShellColor:
    def test_is_valid_color(self):
        """
        Test the is_valid_color method of the ShellColor class.
        """
        shell_color = ShellColor()

        assert shell_color.is_valid_color("green") == True
        assert shell_color.is_valid_color("test") == False
        assert shell_color.is_valid_color("reset") == False
        assert shell_color.is_valid_color("\033[0;32m") == True
        assert shell_color.is_valid_color("\e[0;32m") == True
        assert shell_color.is_valid_color("\e_test") == False

    def test_wrap_in_color(self):
        """
        Test the wrap_in_color method of ShellColor class
        """
        shell_color = ShellColor()

        assert shell_color.wrap_in_color(
            "test", "green") == "\033[1;32mtest\033[0m"
        assert shell_color.wrap_in_color(
            "test", "\033[1;31m") == "\033[1;31mtest\033[0m"
        assert shell_color.wrap_in_color(
            "test", "green", True) == "\033[1;32mtest"

        with pytest.raises(ValueError):
            assert shell_color.wrap_in_color(
                "test", "test_color") == "\033[1;32mtest"
