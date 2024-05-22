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
#
# import_directory = os.path.join(import_directory, "DisplayObjects")
# sys.path.append(import_directory)

from time import sleep
import color
import cursor as cursor_manager
import keyboard_input as kb
import window_manager
# from terminal_objects import TerminalObjects as TObj
from units import Units


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
        "_keybinds": [color.BRIGHT_BLACK, color.ITALIC],
        "selected_option": [color.BOLD, color.GREEN],
    }

    color_scheme = {}

    def __init__(self, screen_size: tuple[int, int]) -> None:
        """Initialize the TerminalManager object.

        Args:
            screen_size (tuple[int, int]):
                The minimum screen _size (y, x).
        """
        self.units = Units()

        self.kb = kb.KeyboardInput()
        print("Keyboard input initialized.")
        self.cursor = cursor_manager.Cursor()

        # Set up the cursor.
        self.cursor.hide()
        self.cursor.clear_screen()

        # Calibrate the screen _size.
        self.screen_size = self.get_screen_size(screen_size)
        print(self.screen_size)
        input()
        # self.cursor.set_screen(screen)

        # Set up the _display.
        self.window_manager = window_manager.WindowManager(self.screen_size)

        # Set up the _color_scheme scheme.
        self.color_scheme = self.default_color_scheme

    def get_screen_size(self, min_screen_size: tuple[int, int]) -> tuple[int, int]:
        """Get the screen _size.

        Args:
            min_screen_size (tuple[int, int]):
                The minimum screen _size (y, x).

        Returns:
            tuple[int, int]: The screen _size (y, x).
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
    # try:
    #     # Initialize the terminal.
    #     terminal = TerminalManager((20, 50))
    #
    #     # Set up the screen.
    #     terminal.window_manager.add_screen("home")
    #     terminal.window_manager.set_current_screen("home")
    #
    #     # Set up the objects.
    #     box = TObj.TEXT_BOX(
    #         "Bob Box", None, coordinates=(5, 30), size=(10, 15),
    #         text="This is a box. I am happy!", title="Bob Box", border_color=color.RED,
    #         title_mods=[color.BOLD, color.UNDERLINE, color.BLUE, color.BACKGROUND_RED],
    #         color_scheme=[color.BACKGROUND_BLACK, color.BRIGHT_GREEN])
    #     box2 = TObj.TEXT_BOX(
    #         "Bob Box 2", None, coordinates=(11, 50), size=(10, 30),
    #         text="This is another box. I am happy!", title="Bob Box 2", border_color=color.RED,
    #         title_mods=[color.BOLD, color.UNDERLINE, color.BLUE, color.BACKGROUND_RED],
    #         color_scheme=[color.BACKGROUND_BLACK, color.BRIGHT_GREEN])
    #
    #     # Add the objects to the screen.
    #     terminal.window_manager.current_screen.add_object(box)
    #     terminal.window_manager.current_screen.add_object(box2)
    #
    #     # Update the _display.
    #     terminal.window_manager.current_screen.update_display()
    #     terminal.window_manager.refresh_screen()
    #
    #     while True:
    #         # Quit if the escape key is pressed.
    #         if terminal.kb.is_newly_pressed("esc"):
    #             break
    #
    #         # Move the box around.
    #         coords = box.coordinates
    #         if terminal.kb.is_held("up"):
    #             box.set_coordinates((coords[0] - 1, coords[1]))
    #         if terminal.kb.is_held("down"):
    #             box.set_coordinates((coords[0] + 1, coords[1]))
    #         if terminal.kb.is_held("left"):
    #             box.set_coordinates((coords[0], coords[1] - 1))
    #         if terminal.kb.is_held("right"):
    #             box.set_coordinates((coords[0], coords[1] + 1))
    #
    #         # Make the box flash.
    #         if time() % .75 < 0.25:
    #             if box.get_visible():
    #                 box.set_visible(False)
    #         elif not box.get_visible():
    #             box.set_visible(True)
    #
    #         # Update the _display.
    #         terminal.window_manager.get_current_screen().update_display()
    #         terminal.window_manager.refresh_screen()
    #
    #         # Sleep to avoid letting the _display fall behind.
    #         sleep(.0125)
    #
    # except KeyboardInterrupt:
    #     cursor_manager.Cursor().show()
    #     cursor_manager.Cursor().set_pos()
    #     print("Program terminated.")
    # except Exception as e:
    #     cursor_manager.Cursor().show()
    #     cursor_manager.Cursor().set_pos()
    #     print(f"An error occurred: {e}")
    #     raise e
