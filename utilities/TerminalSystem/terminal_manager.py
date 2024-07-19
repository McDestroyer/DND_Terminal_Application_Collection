import os
import sys
import time

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


from time import sleep

import color
import cursor as cursor_manager

from input_handler import InputHandler
import window_manager
from units import Units

# For the loading screen.
from terminal_objects import TerminalObjects as TObj
from coordinates import Coordinate


class TerminalManager:
    """Manage a terminal interface."""

    def __init__(self, window_name: str = "Jason's Terminal System", minimum_screen_size: tuple[int, int] = (5, 10),
                 desired_fps: int = 20) -> None:
        """Initialize the TerminalManager object.

        Args:
            window_name (str, optional):
                The name of the window.
                Defaults to "Jason's Terminal System".
            minimum_screen_size (tuple[int, int], optional):
                The minimum screen size (y, x).
                Defaults to (5, 10).
            desired_fps (int, optional):
                The desired frames per second.
                Defaults to 20.
        """
        # Set up the FPS.
        self._desired_fps = 0
        self._frame_time = 0
        self.desired_fps = desired_fps
        self.start_time = time.time_ns()
        self.loop_time = 0
        self.utilities_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

        # Set up the window.
        os.system("title " + window_name)

        # Set up the input.
        self.input = InputHandler(window_name)
        print("Input initialized.")

        # Set up the display cursor.
        self.cursor = cursor_manager.Cursor()
        self.cursor.hide()
        self.cursor.clear_screen()
        print("Cursor initialized.")

        # Calibrate the screen size.
        self.screen_size = self.get_screen_size(minimum_screen_size)

        self.default_color_scheme = {
            "base": {
                "highlight": [color.BACKGROUND_BRIGHT_BLACK],
                "text": [color.BRIGHT_GREEN, color.BACKGROUND_DEFAULT_COLOR],
            },
            "bordered_box": {
                "title": [color.BLACK, color.UNDERLINE, color.RED],
                "border": [color.RED, color.BACKGROUND_BLACK],
            },
            "menu_box": {
                "title": [color.BLACK, color.UNDERLINE, color.RED],
                "border": [color.RED, color.BACKGROUND_BLACK],
                "text": [color.BRIGHT_WHITE, color.BACKGROUND_BLACK],
                "option": [color.BRIGHT_GREEN, color.BACKGROUND_BLACK],
                "selected_option": [color.INVERSE],
            },
            "image_box": {
                "title": [color.BLACK, color.UNDERLINE, color.RED],
                "border": [color.RED, color.BACKGROUND_BLACK],
            },
            "text_box": {
                "title": [color.BLACK, color.UNDERLINE, color.RED],
                "border": [color.RED, color.BACKGROUND_BLACK],
                "text": [color.BRIGHT_WHITE, color.BACKGROUND_BLACK],
            },
            "menu_text_input": {
                "title": [color.BLACK, color.UNDERLINE, color.RED],
                "border": [color.RED, color.BACKGROUND_BLACK],
                "text": [color.BRIGHT_WHITE, color.BACKGROUND_BLACK],
                "cursor": [color.BRIGHT_WHITE, color.BACKGROUND_BLACK],
                "empty": [color.BRIGHT_WHITE, color.BACKGROUND_BLACK],
            },
            "menu_button": {
                "title": [color.BLACK, color.UNDERLINE, color.RED],
                "border": [color.RED, color.BACKGROUND_BLACK],
                "text": [color.BRIGHT_WHITE, color.BACKGROUND_BLACK],
            },
            "menu_slider": {
                "title": [color.BLACK, color.UNDERLINE, color.RED],
                "border": [color.RED, color.BACKGROUND_BLACK],
                "text": [color.BRIGHT_WHITE, color.BACKGROUND_BLACK],
                "slider": [color.BRIGHT_WHITE, color.BACKGROUND_BLACK],
            },
            "menu_option": {
                "text": [color.BRIGHT_WHITE, color.BACKGROUND_BLACK],
                "highlight": [color.BRIGHT_GREEN, color.BACKGROUND_BLACK],
            },
        }

        # Set up the display.
        self.window_manager = window_manager.WindowManager(self.screen_size)
        print("Window manager initialized.")

        # Set up the mouse.
        self._mouse_enabled = False
        self._highlighted_object = None

        self.units = Units()

        self.run_loading_animation()

    def run_loading_animation(self) -> None:
        """Run the loading logo animation."""
        resources_path = os.path.join(self.utilities_directory, "TerminalSystem", "Resources")
        path = os.path.join(resources_path, "SavedScreens", "loading_screen.pkl")
        try:
            raise FileNotFoundError
            # TODO When done modifying base principles, let it load the animation rather than generating it every time.
            loading_screen = self.window_manager.load_screen_from_file("loading", path)
            logo_box = self.window_manager.set_current_screen(loading_screen).get_object_by_name("Logo Box")
        except FileNotFoundError:
            # Set up the loading screen if the file got deleted.
            load_screen = self.window_manager.add_screen("loading")
            animation_path = os.path.join(resources_path, "Images", "flashing_logo.AAI")
            logo_box = TObj.IMAGE_BOX(
                "Logo Box",
                coordinates=Coordinate(self.screen_size, -265, 0, unit_y=Units.PERCENT, unit_x=Units.PERCENT),
                size=Coordinate(self.screen_size, 500, 100, unit_y=Units.PERCENT, unit_x=Units.PERCENT),
                image=animation_path,
                title="Logo Box", border_material=None,
                border_color=[color.BACKGROUND_BLACK+color.BLACK],
                title_mods=[color.UNDERLINE, color.RED, color.BACKGROUND_BLACK],
                shrink_to_fit=False
            )
            load_screen.add_object(logo_box)
            self.window_manager.save_screen_to_file("loading", path)
            self.window_manager.set_current_screen(load_screen)
            pass

        # sleep(1)
        for i in range(45):
            self.loop()

            # Quit if the escape key is pressed.
            # if self.input.kb.is_newly_pressed("space") or self.input.kb.is_newly_pressed("enter") \
            #         or self.input.kb.is_newly_pressed("esc"):
            if self.input.keyboard_states["space"]["newly_pressed"] or \
                    self.input.keyboard_states["enter"]["newly_pressed"] or \
                    self.input.keyboard_states["esc"]["newly_pressed"]:
                self.refresh_screen()
                break

            logo_box.coordinates = Coordinate(
                self.screen_size,
                logo_box.coordinates.values["PERCENT"][0] + 3,
                logo_box.coordinates.values["PERCENT"][1],
                unit_x=Units.PERCENT,
                unit_y=Units.PERCENT
            )

            self.refresh_screen()
            sleep(.02)

    def loop(self) -> None:
        """Run the main loop."""
        self.start_time = time.time_ns()

        # Update the inputs.
        self.input.update()
        if self.input.keyboard_states["esc"]["newly_pressed"]:
            self.quit()
        self.input.check_keybinds(self.window_manager.current_screen)

        # Handle the mouse, applying hovered and dragged effects.
        self.handle_mouse()
        # Handle text highlighting.
        self.handle_highlighting()

        # Update the objects with the new input data and any other data I decide to add later.
        # This is called after handling the mouse so that the objects have up-to-date mouse_over values.
        object_data = {
            "mouse_pos": self.input.mouse.get_screen_char_position(self.screen_size),
            "mouse_inputs": self.input.mouse_states,
            "keyboard_inputs": self.input.keyboard_states,
            "gamepad_inputs": self.input.gamepad_states,
        }
        self.window_manager.current_screen.update_objects(object_data)

    def handle_mouse(self) -> None:
        """Handle the mouse."""
        if self.mouse_enabled:
            # Move the cursor to the mouse position.
            cursor_pos = self.input.mouse.get_screen_char_position(self.screen_size)

            if cursor_pos is not None:
                self.window_manager.mouse.visible = True
                new_coords = Coordinate(
                    self.screen_size,
                    cursor_pos[0],
                    cursor_pos[1]
                )
            # If the mouse is off the screen, hide it.
            else:
                new_coords = None
                self.window_manager.mouse.visible = False
            # Only update the mouse if the position has changed for efficiency.
            if new_coords is not None and new_coords != self.window_manager.mouse.coordinates:
                self.window_manager.mouse.coordinates = new_coords

                # Check if the mouse is over any objects. Start from the back to prioritize the top-most objects.
                hovered = False
                for i in range(len(self.window_manager.current_screen.objects)):
                    obj = self.window_manager.current_screen.objects[-1-i]
                    if obj.coordinates[0] <= cursor_pos[0] < obj.coordinates[0] + obj.size[0] and \
                            obj.coordinates[1] <= cursor_pos[1] < obj.coordinates[1] + obj.size[1] and \
                            obj.visible and obj.name != "Mouse" and not hovered:
                        obj.mouse_over = cursor_pos[0] - obj.coordinates[0], cursor_pos[1] - obj.coordinates[1]
                    else:
                        obj.mouse_over = False

    def handle_highlighting(self) -> None:
        """Handle highlighting."""
        # TODO This changes the hovered object but not the highlighted one properly and may interfere with highlighting.
        for obj in self.window_manager.current_screen.objects:
            if obj.mouse_over:
                if self.highlighted_object is not None and obj != self.highlighted_object:
                    self.highlighted_object.mouse_over = False
                    self.highlighted_object = obj
                    break
            elif self.highlighted_object is not None and obj == self.highlighted_object:
                self.highlighted_object = None

    def quit(self) -> None:
        """Quit the program. Shuts down various things to avoid bugs and weirdness after quitting."""
        self.cursor.show()
        self.cursor.set_pos()
        self.input.clear_input_buffer()
        self.input.kb.release("ctrl")
        os.system("cls")
        print(color.ERROR + "\n\nCTRL + C?! You're killing me!!! Aww, fine... Bye!" + color.END)
        raise KeyboardInterrupt

    def refresh_screen(self) -> None:
        """Refresh the screen and sleep any remaining time needed for maintenance of the desired FPS."""
        self.window_manager.refresh_screen()

        self.loop_time = (time.time_ns() - self.start_time) / 1_000_000_000
        if self.loop_time < self._frame_time:
            sleep((self._frame_time - self.loop_time))

    def get_screen_size(self, min_screen_size: tuple[int, int]) -> tuple[int, int]:
        """Get the screen size.

        Args:
            min_screen_size (tuple[int, int]):
                The minimum screen size (y, x).

        Returns:
            tuple[int, int]: The screen size (y, x).
        """
        # Clear the screen.
        os.system("cls")

        x = 156
        y = 39

        first = True
        while True:

            # Get input
            up = self.input.kb.is_held("up")
            down = self.input.kb.is_held("down")
            left = self.input.kb.is_held("left")
            right = self.input.kb.is_held("right")
            finish = self.input.kb.is_newly_pressed("enter") or self.input.kb.is_newly_pressed("esc")

            if finish:
                os.system("cls")
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
            if up or down or left or right or first:
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

            first = False
            # Sleep to avoid excessive speed
            sleep(0.025)

        return y+1, x

    @property
    def mouse_enabled(self) -> bool:
        """Return whether the mouse is enabled.

        Returns:
            bool: Whether the mouse is enabled.
        """
        return self._mouse_enabled

    @property
    def desired_fps(self) -> int:
        """Return the desired frames per second.

        Returns:
            int: The desired frames per second.
        """
        return self._desired_fps

    @property
    def highlighted_object(self) -> TObj.TERMINAL_OBJECT | None:
        """Return the object containing highlighted text.

        Returns:
            TObj.TERMINAL_OBJECT | None: The object containing highlighted text.
        """
        return self._highlighted_object

    @mouse_enabled.setter
    def mouse_enabled(self, enabled: bool) -> None:
        """Set whether the mouse is enabled.

        Args:
            enabled (bool): Whether the mouse is enabled.
        """
        self._mouse_enabled = enabled
        if enabled:
            self.window_manager.setup_mouse()
        else:
            self.window_manager.remove_mouse()

    @desired_fps.setter
    def desired_fps(self, fps: int) -> None:
        """Set the desired frames per second.

        Args:
            fps (int): The desired frames per second.
        """
        self._desired_fps = fps
        self._frame_time = 1 / fps

    @highlighted_object.setter
    def highlighted_object(self, obj: TObj.TERMINAL_OBJECT | None) -> None:
        """Set the object containing highlighted text.

        Args:
            obj (TObj.TERMINAL_OBJECT | None): The object containing highlighted text.
        """
        for obj in self.window_manager.current_screen.objects:
            if obj != self._highlighted_object:
                obj.highlighting = False
        self._highlighted_object = obj


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
