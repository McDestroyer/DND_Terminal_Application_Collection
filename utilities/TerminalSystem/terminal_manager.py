import os
import sys
from time import sleep
import color
import cursor as cursor_manager
from input_handler import InputHandler
import window_manager
from units import Units

if __name__ == "__main__":
    # This is an importer I made for all of my programs going forward, so I wouldn't have to deal with
    # creating and renaming the utilities files for every program or have to deal with learning the "correct" methods.

    utilities_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    sys.path.append(utilities_directory)

    # Optionally add if you want to use the input system.
    inputs_directory = os.path.join(utilities_directory, "inputs")
    sys.path.append(inputs_directory)
    # Optionally add if you want to use the terminal system.
    terminal_directory = os.path.join(utilities_directory, "TerminalSystem")
    sys.path.append(terminal_directory)
    display_objects_directory = os.path.join(terminal_directory, "DisplayObjects")
    sys.path.append(display_objects_directory)
    helper_directory = os.path.join(terminal_directory, "HelperObjects")
    sys.path.append(helper_directory)


class TerminalManager:
    """Manage a terminal interface."""

    default_color_scheme = {
        "header": [color.YELLOW],
        "options": [color.BLUE],
        "footer": [color.YELLOW],
        "keybinds": [color.BRIGHT_BLACK, color.ITALIC],
        "selected_option": [color.BOLD, color.GREEN],
    }

    color_scheme = {}

    def __init__(self, window_name: str = "Jason's Terminal System",
                 minimum_screen_size: tuple[int, int] = (5, 10)) -> None:
        """Initialize the TerminalManager object.

        Args:
            minimum_screen_size (tuple[int, int]):
                The minimum screen size (y, x).
        """
        # Set up the window.
        os.system("title " + window_name)

        # Set up the input.
        self.input = InputHandler(window_name)
        print("Input initialized.")

        # Set up the cursor.
        self.cursor = cursor_manager.Cursor()
        self.cursor.hide()
        self.cursor.clear_screen()
        print("Cursor initialized.")

        # Calibrate the screen size.
        self.screen_size = self.get_screen_size(minimum_screen_size)
        print("Screen size set to:", self.screen_size)
        # input()

        # Set up the display.
        self.window_manager = window_manager.WindowManager(self.screen_size)
        print("Window manager initialized.")

        # Set up the color scheme.
        self.color_scheme = self.default_color_scheme

        # Set up the keybinds.
        self.keybinds = {
            "esc": [self.quit],
        }

        # Set up the mouse.
        self.mouse_enabled = False

        self.units = Units()

    def loop(self) -> None:
        """Run the main loop."""
        self.input.check_keybinds()


    def quit(self) -> None:
        """Quit the program."""
        self.cursor.show()
        self.cursor.set_pos()
        self.input.clear_input_buffer()
        print(color.ERROR + "\n\nCTRL + C?! You're killing me!!! Aww, fine... Bye!" + color.END)
        sys.exit()

    def refresh_screen(self) -> None:
        """Refresh the screen."""
        self.window_manager.refresh_screen()

    def get_screen_size(self, min_screen_size: tuple[int, int]) -> tuple[int, int]:
        """Get the screen size.

        Args:
            min_screen_size (tuple[int, int]):
                The minimum screen size (y, x).

        Returns:
            tuple[int, int]: The screen size (y, x).
        """
        x = 156
        y = 39

        while True:

            # Get input
            up = self.input.kb.is_held("up")
            down = self.input.kb.is_held("down")
            left = self.input.kb.is_held("left")
            right = self.input.kb.is_held("right")
            finish = self.input.kb.is_newly_pressed("enter") or self.input.kb.is_newly_pressed("esc")

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
