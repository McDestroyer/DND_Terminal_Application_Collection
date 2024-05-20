
# Uncomment the following for direct testing

# # These get rid of annoying errors that usually mean nothing.
# # Remove non-import related ones if seriously struggling
#
# # pylint: disable=unused-import
# # pylint: disable=unused-wildcard-import
# # pylint: disable=wildcard-import
# # pylint: disable=unexpected-keyword-arg
# # pylint: disable=no-member
# # pylint: disable=ungrouped-imports
# # pylint: disable=undefined-variable
# # pylint: disable=wrong-import-position
# # pylint: disable=import-error
#
#
# # This is an importer I made for all of my programs going forward, so I wouldn't have to deal with
# # creating and renaming the utilities files for every program or have to deal with learning the "correct" methods.
# import sys
# import os
#
# import_directory = os.path.dirname(os.path.realpath(__file__))
#
# while "utilities" not in os.listdir(import_directory):
#     import_directory = os.path.dirname(import_directory)
#
# import_directory = os.path.join(import_directory, "utilities")
# sys.path.append(import_directory)
#
# # Optionally add if you want to use the terminal system.
# import_directory = os.path.join(import_directory, "TerminalSystem")
# sys.path.append(import_directory)


import time

import color
import cursor
from terminal_tools import assemble_display_string, to_char_array


class Display:

    def __init__(self, display_size: tuple[int, int], anti_flash: bool = False) -> None:
        self.anti_flash = anti_flash

        self.cursor = cursor.Cursor()
        self.cursor.clear_screen()

        self.display_size = (40, 156)  # (rows, columns)
        self.previous_display_array = [
            [
                [
                    " ",
                    [color.BACKGROUND_BLUE]
                ] for _ in range(self.display_size[1])
            ] for _ in range(self.display_size[0])
        ]
        self.display_array = [
            [
                [
                    ".",
                    [color.BACKGROUND_BLUE]
                ] for _ in range(self.display_size[1])
            ] for _ in range(self.display_size[0])
        ]  # display_array[y][x][0 | 1], [row][column]["char", [mods]]
        self.display_string = ""

    def set_display_size(self, size: tuple[int, int]) -> None:
        self.display_size = size
        self.cursor.set_screen(size)
        self.display_array = [[[".", [color.BACKGROUND_BLACK]] for _ in range(size[1])] for _ in range(size[0])]

        # self.previous_display_array = []
        # for item in self.display_array:
        #     self.previous_display_array.append(item[:])

    # Getters and setters.

    def get_display_size(self) -> tuple[int, int]:
        return self.display_size

    def get_display(self) -> list[list[list[str | list[str]]]]:
        return self.display_array

    # Display functions.

    def add_to_display(self, grid_to_add: list[list[list[str | list[str]]]],
                       coordinates: list[int] | tuple[int, int]) -> None:
        """Add stuff to the display.

        Args:
            grid_to_add (list[list[list[str | list[str]]]):
                The grid of characters to add to the display.
            coordinates (list[int] | tuple[int, int]):
                The coordinates of the top-left slot to add the grid from.
        """
        if coordinates[0] > len(self.display_array)-1 or coordinates[1] > len(self.display_array[0])-1:
            raise IndexError("Coordinates out of bounds.")

        # Go through the grid and add the characters to the display in a position offset by the coordinates given.
        for y, row in enumerate(grid_to_add):
            for x, column in enumerate(row):
                if column[0] != "":
                    self.display_array[y + coordinates[0]][x + coordinates[1]] = column

    def clear_display(self) -> None:
        """Clear the display array and refresh. NOT the same as cursor.clear_screen()!!!"""
        self.display_array = [[[".", [color.BACKGROUND_BLACK]] for _ in range(self.display_size[1])] for _ in range(self.display_size[0])]

        if self.anti_flash:
            self.antiflash_refresh_display()
            return
        self.refresh_display()

    def refresh_display(self) -> None:
        """Refresh the display with the most recent display string."""
        self.cursor.clear_screen()

        self.display_string = assemble_display_string(self.display_array)
        print(self.display_string, end="", flush=True)

        self.previous_display_array = []
        for item in self.display_array:
            self.previous_display_array.append(item[:])

    def antiflash_refresh_display(self) -> None:
        """Refresh the display with the most recent display string."""
        if self.display_array == self.previous_display_array:
            print("No change.")
            return
        for row in range(len(self.display_array)):
            for column in range(len(self.display_array[0])):
                if self.display_array[row][column] != self.previous_display_array[row][column]:
                    self.cursor.set_pos(column, row)
                    print("".join(self.display_array[row][column][1]) + self.display_array[row][column][0] + color.END, end="", flush=True)

        self.previous_display_array = []
        for item in self.display_array:
            self.previous_display_array.append(item[:])


if __name__ == "__main__":
    display = Display()
    display.set_display_size((10, 140))
    # display.clear_display()
    hi_msg = to_char_array("Hello, world!", mods=[color.BRIGHT_GREEN, color.BACKGROUND_BLACK]), (0, 0)
    display.add_to_display(to_char_array("Hello, world!", mods=[color.BRIGHT_GREEN, color.BACKGROUND_BLACK]), (0, 0))
    display.antiflash_refresh_display()
    time.sleep(.5)
    display.add_to_display(to_char_array("Hello, world!", mods=[color.BRIGHT_GREEN, color.BACKGROUND_BLACK]), (1, 1))
    display.antiflash_refresh_display()
    time.sleep(.5)
    display.add_to_display(to_char_array("Hello, world!", mods=[color.BRIGHT_GREEN, color.BACKGROUND_BLACK]), (2, 0))
    display.antiflash_refresh_display()
    time.sleep(.5)
    display.add_to_display(to_char_array("Hello, world!", mods=[color.BRIGHT_GREEN, color.BACKGROUND_BLACK]), (3, 1))
    display.antiflash_refresh_display()
    time.sleep(.5)
    display.add_to_display(to_char_array("Hello, world!", mods=[color.BRIGHT_GREEN, color.BACKGROUND_BLACK]), (4, 2))
    display.antiflash_refresh_display()
    time.sleep(.5)
