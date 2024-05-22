from copy import deepcopy

import color
from cursor import Cursor
from terminal_tools import assemble_display_string


class Display:

    def __init__(self, display_size: tuple[int, int]) -> None:

        self._cursor = Cursor()
        self._cursor.clear_screen()

        self._display_size = display_size  # (rows, columns)
        self._previous_display_array = [
            [
                [
                    " ",
                    [color.BACKGROUND_BLUE]
                ] for _ in range(self._display_size[1])
            ] for _ in range(self._display_size[0])
        ]
        self._display_array = [
            [
                [
                    " ",
                    [color.BACKGROUND_BLUE]
                ] for _ in range(self._display_size[1])
            ] for _ in range(self._display_size[0])
        ]  # _display_array[y][x][0 | 1], [row][column]["char", [mods]]
        self._display_string = ""

    # Display functions.

    def clear_display(self) -> None:
        """Clear the display array and refresh. NOT the same as cursor.clear_screen()!!!"""
        self._display_array = [
            [
                [
                    " ", [color.BACKGROUND_BLACK]
                ] for _ in range(self._display_size[1])
            ] for _ in range(self._display_size[0])
        ]

        self.refresh_display()

    def refresh_display(self) -> None:
        """Refresh the display with the most recent display string."""
        self._cursor.clear_screen()

        self._display_string = assemble_display_string(self._display_array)
        print(self._display_string, end="", flush=True)

        self._previous_display_array = deepcopy(self._display_array)

    def antiflash_refresh_display(self) -> None:
        """Refresh the display with the most recent display string, only updating the parts that are different."""
        # Skip if there have been no changes.
        if self._display_array == self._previous_display_array:
            return
        # If the previous display array is shorter than the current one, print the whole thing.
        # Usually should only occur when changing display sizes.
        elif len(self._previous_display_array) < len(self._display_array):
            self.refresh_display()
            return

        # Cycle through the display array and print the characters that have changed.
        for row in range(len(self._display_array)):
            for column in range(len(self._display_array[0])):
                if self._display_array[row][column] != self._previous_display_array[row][column]:
                    # Possibly inefficient, printing separately to jump each time, but it works.
                    self._cursor.set_pos(column, row)
                    print("".join(self._display_array[row][column][1]) + self._display_array[row][column][0] +
                          color.END, end="", flush=False)
        self._cursor.set_pos(0, 0)
        print("", end="", flush=True)

        self._previous_display_array = deepcopy(self._display_array)

    @property
    def display_array(self) -> list[list[list[str | list[str]]]]:
        """Return the display array.

        Returns:
            list[list[list[str | list[str]]]]: The display array.
        """
        return self._display_array

    @property
    def display_string(self) -> str:
        """Return the display string.

        Returns:
            str: The display string.
        """
        return self._display_string

    @property
    def display_size(self) -> tuple[int, int]:
        """Return the display size.

        Returns:
            tuple[int, int]: The display size.
        """
        return self._display_size

    @property
    def cursor(self) -> Cursor:
        """Return the cursor.

        Returns:
            Cursor: The cursor.
        """
        return self._cursor

    @property
    def previous_display_array(self) -> list[list[list[str | list[str]]]]:
        """Return the previous display array.

        Returns:
            list[list[list[str | list[str]]]]: The previous display array.
        """
        return self._previous_display_array

    @previous_display_array.setter
    def previous_display_array(self, new_previous_display_array: list[list[list[str | list[str]]]]) -> None:
        """Set the previous display array.

        Args:
            new_previous_display_array (list[list[list[str | list[str]]]]):
                The new previous display array.
        """
        self._previous_display_array = deepcopy(new_previous_display_array)

    @display_array.setter
    def display_array(self, new_display_array: list[list[list[str | list[str]]]]) -> None:
        """Set the display array.

        Args:
            new_display_array (list[list[list[str | list[str]]]]):
                The new display array.
        """
        self._display_array = deepcopy(new_display_array)
        self.antiflash_refresh_display()

    @display_string.setter
    def display_string(self, new_display_string: str) -> None:
        """Set the display string.

        Args:
            new_display_string (str):
                The new display string.
        """
        self._display_string = deepcopy(new_display_string)
        self.refresh_display()

    @display_size.setter
    def display_size(self, new_display_size: tuple[int, int]) -> None:
        """Set the display size.

        Args:
            new_display_size (tuple[int, int]):
                The new display size.
        """
        self._display_size = deepcopy(new_display_size)
        self._display_array = [
            [
                [
                    " ", [color.BACKGROUND_BLACK]
                ] for _ in range(new_display_size[1])
            ] for _ in range(new_display_size[0])
        ]

        self.refresh_display()

    @cursor.setter
    def cursor(self, new_cursor: Cursor) -> None:
        """Set the cursor.

        Args:
            new_cursor (Cursor):
                The new cursor.
        """
        self._cursor = new_cursor


if __name__ == "__main__":
    display = Display((10, 140))
