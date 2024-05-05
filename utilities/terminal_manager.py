import shutil

import color
import audio
import cursor as cursor_manager
import animations
import keyboard_input as kb
from personal_functions import *


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

    def __init__(self) -> None:
        """Initialize the TerminalManager object."""

        self.kb = kb.KeyboardInput()
        print("Keyboard input initialized.")
        self.cursor = cursor_manager.Cursor()

        # Set up the cursor.
        self.cursor.hide()
        self.cursor.clear_screen()

        # Calibrate the screen size.
        screen = self.get_screen_size()
        print(screen)
        input()
        self.cursor.set_screen(screen)

        # Set up the color scheme.
        self.color_scheme = self.default_color_scheme

    def main_loop(self) -> None:
        """Main loop."""
        # text("What would you like to do?", mods=[color.BOLD, color.BLUE])
        self.print_options()

    def print_options(self) -> None:
        """Print the options."""
        for option in self.options:
            text(option[0], mods=[color.BOLD, color.GREEN])

    def get_screen_size(self) -> tuple[int, int]:
        """Get the screen size.

        Returns:
            tuple[int, int]: The screen size (x, y).
            """
        x = 208
        y = 26

        # self.cursor.set_pos()
        # self.cursor.cursor_print()
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
                y = max(y - 1, 0)
            if down:
                y += 1
            if left:
                x = max(x - 1, 0)
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
            print("x: " + str(x) + "y: " + str(y), end="", flush=True)

            # Sleep to avoid excessive speed
            sleep(0.025)

        return x, y


if __name__ == "__main__":
    fail_screen = (1, 1)
    try:
        terminal = TerminalManager()
        # terminal.main_loop()
    except KeyboardInterrupt:
        cursor_manager.Cursor().show()
        cursor_manager.Cursor().set_pos()
        print("Program terminated.")
    except Exception as e:
        cursor_manager.Cursor().show()
        cursor_manager.Cursor().set_pos()
        print(f"An error occurred: {e}")
        raise e
