# These get rid of annoying errors that usually mean nothing.
# Remove non-import related ones if seriously struggling

# pylint: disable=unused-import
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=unexpected-keyword-arg
# pylint: disable=no-member
# pylint: disable=ungrouped-imports
# pylint: disable=undefined-variable
# pylint: disable=wrong-import-position
# pylint: disable=import-error


# This is an importer I made for all of my programs going forward, so I wouldn't have to deal with
# creating and renaming the utilities files for every program or have to deal with learning the "correct" methods.
import sys
import os

import_directory = os.path.dirname(os.path.realpath(__file__))

while "utilities" not in os.listdir(import_directory):
    import_directory = os.path.dirname(import_directory)

import_directory = os.path.join(import_directory, "utilities")
sys.path.append(import_directory)

# Optionally add if you want to use the terminal system.
import_directory = os.path.join(import_directory, "TerminalSystem")
sys.path.append(import_directory)

from time import sleep
import color
import cursor as cursor_manager
import keyboard_input as kb
import window_manager
import terminal_objects as TObj


class TerminalManager:
    """Manage a terminal interface."""

    cursor_pos = [0, 0]
    header_text = ""
    options = []
    footer_text = ""
    keybinds = {}

    default_color_scheme = {
        "header": [color.YELLOW],
        "options": [color.BLUE],
        "footer": [color.YELLOW],
        "keybinds": [color.BRIGHT_BLACK, color.ITALIC],
        "selected_option": [color.BOLD, color.GREEN],
    }

    color_scheme = {}

    def __init__(self, screen_size: tuple[int, int]) -> None:
        """Initialize the TerminalManager object.

        Args:
            screen_size (tuple[int, int]):
                The minimum screen size (y, x).
        """

        self.kb = kb.KeyboardInput()
        print("Keyboard input initialized.")
        self.cursor = cursor_manager.Cursor()
        #
        # # Set up the cursor.
        # self.cursor.hide()
        # self.cursor.clear_screen()

        # Calibrate the screen size.
        self.screen_size = self.get_screen_size(screen_size)
        print(self.screen_size)
        input()
        # self.cursor.set_screen(screen)

        # Set up the display.
        self.window_manager = window_manager.WindowManager(self.screen_size)

        # Set up the color_scheme scheme.
        self.color_scheme = self.default_color_scheme

    def get_screen_size(self, min_screen_size: tuple[int, int]) -> tuple[int, int]:
        """Get the screen size.

        Args:
            min_screen_size (tuple[int, int]):
                The minimum screen size (y, x).

        Returns:
            tuple[int, int]: The screen size (y, x).
        """
        x = 156
        y = 41

        while True:

            # Get input
            up = self.kb.is_held("up")
            down = self.kb.is_held("down")
            left = self.kb.is_held("left")
            right = self.kb.is_held("right")
            finish = self.kb.is_newly_pressed("enter") or self.kb.is_newly_pressed("esc")

            if finish:
                break
            if up:
                y = max(y - 1, min_screen_size[0])
            if down:
                y += 1
            if left:
                x = max(x - 1, min_screen_size[1])
            if right:
                x += 1

            # Print
            self.cursor.clear_screen()
            self.cursor.set_pos()
            for i in range(y):
                if i != 0:
                    print()
                if i == y - 1 or i == 0:
                    print(color.YELLOW + "█"*(x-1) + color.BLUE + "█" + color.END, end="", flush=True)
                    continue
                print(color.GREEN + "█"*(x-1) + color.RED + "█" + color.END, end="", flush=True)
            print("x: " + str(x) + " y: " + str(y), end="", flush=True)

            # Sleep to avoid excessive speed
            sleep(0.025)

        return y+1, x


if __name__ == "__main__":
    fail_screen = (1, 1)
    try:
        terminal = TerminalManager((20, 50))
        terminal.window_manager.add_screen("home")
        terminal.window_manager.set_current_screen("home")
        box = TObj.Box(
            "Bob Box", None, None, coordinates=(5, 10), size=(10, 15),
            text="This is a box. I am happy!", title="Bob Box", border_color=color.RED,
            title_mods=[color.BOLD, color.UNDERLINE, color.BLUE, color.BACKGROUND_RED],
            color_scheme=[color.BACKGROUND_BLACK, color.BRIGHT_GREEN])
        terminal.window_manager.get_current_screen().add_object(box)
        terminal.window_manager.get_current_screen().update_display()
        terminal.window_manager.refresh_screen()

    except KeyboardInterrupt:
        cursor_manager.Cursor().show()
        cursor_manager.Cursor().set_pos()
        print("Program terminated.")
    except Exception as e:
        cursor_manager.Cursor().show()
        cursor_manager.Cursor().set_pos()
        print(f"An error occurred: {e}")
        raise e
