# Disables annoying and usually incorrect warnings.
# pylint: disable=wrong-import-position
# pylint: disable=import-error


if __name__ == "__main__":
    # This is an importer I made for all of my programs going forward, so I wouldn't have to deal with
    # creating and renaming the utilities files for every program or have to deal with learning the "correct" methods.
    import sys
    import os


    import_directory = os.path.dirname(os.path.realpath(__file__))

    while "utilities" not in os.listdir(import_directory):
        import_directory = os.path.dirname(import_directory)

    utilities_directory = os.path.join(import_directory, "utilities")
    sys.path.append(utilities_directory)
    import cursor


# Make sure the dependency is installed.
import dependency_installer
dependency_installer.install_dependency("mouse")
dependency_installer.install_dependency("pywin32")
# dependency_installer.install_dependency("windows-curses")
import time
import mouse
import win32gui


class MouseInput:
    """Work with mouse inputs."""

    def __init__(self, window_name: str) -> None:
        """Initialize the MouseInput object.

        Args:
            window_name (str):
                The name of the window to get mouse input from. Used for tracking mouse position.
        """
        self.window_name = window_name

        # The keys previously pressed
        self.past_key_values: dict[str | list[bool | int]] = {}

        self.available_keys = ["left", "right", "middle", "double"]
        self.last_mouse_position = mouse.get_position()
        self.hold_delay = 0.25

        self.last_mouse_movement = [mouse.get_position(), time.time_ns()]
        self.mouse_visibility_delay = 5

        self._past_wheel_delta = 0
        self._wheel_delta = 0
        self.wheel_position = 0
        mouse.hook(self.update_wheel)

    def is_newly_pressed(self, key: str, function: callable or None = None) -> bool:
        """Detect if a key is pressed and return True if
        it wasn't pressed the last time this function was called.
        Designed to be run every frame.

        Args:
            key (str):
                 key to check the newness of the compression thereof.
            function (str, optional):
                 The function to execute if the key is newly pressed.

        Returns:
            bool: True if the key is pressed but was not pressed during the previous call.
            False otherwise.
        """
        result = False

        # If the key has been pressed previously, check it's previous value.
        # If it says it wasn't pressed, but it is now, change to fit and set the result accordingly
        # and vise-versa.
        # If the current and previous values are the same, set the result to False.
        if key in self.past_key_values:
            if mouse.is_pressed(key):
                if self.past_key_values[key][0] is False:
                    self.past_key_values[key][0] = True
                    self.past_key_values[key][1] = time.time_ns()
                    result = True
                elif self.past_key_values[key][0] is True:
                    pass
            elif mouse.is_pressed(key) and self.past_key_values[key][0] is True:
                pass
            else:
                self.past_key_values[key][0] = False
                self.past_key_values[key][1] = 0

        # If it isn't in the list, set the result and the value
        # to whether or not it's currently pressed.
        else:
            if mouse.is_pressed(key):
                result = True
                self.past_key_values[key] = [True, time.time_ns()]
            else:
                self.past_key_values[key] = [False, 0]

        if result and function is not None:
            function()

        return result

    def is_newly_released(self, key: str, function: callable or None = None) -> bool:
        """Detect if a key is released and return True if
        it was pressed the last time this function was called.
        Designed to be run every frame, and the inverse of is_newly_pressed.

        Args:
            key (str):
                 key to check the newness of the released compression thereof.
            function (str, optional):
                 The function to execute if the key is newly released.

        Returns:
            bool: True if the key is not pressed but was pressed during the previous call.
            False otherwise.
        """
        result = False

        # If the key hasn't been pressed previously, check it's previous value.
        # If it says it wasn't pressed, but it is now, change to fit and set the result accordingly
        # and vise-versa.
        # If the current and previous values are the same, set the result to False.
        if key in self.past_key_values:
            if not mouse.is_pressed(key):
                if self.past_key_values[key][0]:
                    self.past_key_values[key] = [False, 0]
                    result = True
            elif mouse.is_pressed(key) and self.past_key_values[key][0] is False:
                self.past_key_values[key] = [True, time.time_ns()]

        # If it isn't in the list, set the result and the value
        # to whether or not it's currently pressed.
        else:
            if mouse.is_pressed(key):
                self.past_key_values[key] = [True, time.time_ns()]
            else:
                result = True
                self.past_key_values[key] = [False, 0]

        if result and function is not None:
            function()

        return result

    def get_relative_position(self) -> tuple[int, int]:
        """Get the relative position of the mouse.

        Returns:
            tuple[int, int]: The relative position of the mouse.
        """
        # TODO: Maybe use a delta time
        position = mouse.get_position()
        relative_position = (position[0] - self.last_mouse_position[0], position[1] - self.last_mouse_position[1])
        self.last_mouse_position = position
        return relative_position

    # def get_position(self) -> tuple[int, int]:
    #     """Get the position of the mouse.
    #
    #     Returns:
    #         tuple[int, int]: The position of the mouse.
    #     """
    #     return mouse.get_position()

    def get_screen_char_position(self, screen_char_size: tuple[int, int]) -> tuple[int, int] | None:
        """Get the CHAR coordinates of the mouse on the screen.

        Returns:
            tuple[int, int] | None: The CHAR coordinates of the mouse on the screen or None if the mouse should be
            hidden.
        """
        window_rect = self.get_window_rect()
        mouse_coords = mouse.get_position()

        terminal_coords = (mouse_coords[1] - window_rect["top"], mouse_coords[0] - window_rect["left"])
        window_size = (window_rect["bottom"] - window_rect["top"], window_rect["right"] - window_rect["left"])

        screen_char_coords = (int(terminal_coords[0] / window_size[0] * screen_char_size[0]),
                              int(terminal_coords[1] / window_size[1] * screen_char_size[1]))

        if (not (window_rect["left"] <= mouse_coords[0] <= window_rect["right"]) or
                not (window_rect["top"] <= mouse_coords[1] <= window_rect["bottom"])):
            return None

        if mouse_coords == self.last_mouse_movement[0]:
            if time.time_ns() - self.last_mouse_movement[1] > self.mouse_visibility_delay * 1_000_000_000:
                return None
        else:
            self.last_mouse_movement = [mouse_coords, time.time_ns()]

        return screen_char_coords

    def get_window_rect(self) -> dict[str, int]:
        """Get the size and position of the window.

        Returns:
            dict[str, int]: The window rectangle.
        """
        try:
            # Find the window handle by title
            hwnd = win32gui.FindWindow(None, self.window_name)
            if hwnd:
                # Get the window position and size
                left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                # +40 on the top to account for the title bar.
                return {"left": left+10, "top": top+40, "right": right-35, "bottom": bottom-30}
                # print(f"Window position: ({left}, {top}), Size: {right - left} x {bottom - top}")
            else:
                print(f"Window '{self.window_name}' not found.")
        except Exception as e:
            print(f"Error: {e}")

    def is_currently_pressed(self, key: str, function: callable or None = None) -> bool:
        """Check to see if a key is currently pressed.

        Args:
            key (str):
                The key to check.
            function (callable | None, optional):
                The function to call if the key is pressed.
                Defaults to None.

        Returns:
            bool: True if the key is pressed. False otherwise.
        """
        # Update the list and time if it's newly pressed.
        if self.is_newly_pressed(key):
            if function is not None:
                function()
            return True

        # If it's not newly pressed, but still pressed, return True anyway.
        if mouse.is_pressed(key):
            if function is not None:
                function()
            return True
        return False

    def is_held(self, key: str, hold_delay: float = .25) -> bool:
        """Check to see if a key is held.

        Args:
            key (str):
                The key to check.
            hold_delay (float, optional):
                The time in seconds the key must be held to return True after the first press.
                Defaults to 0.25.

        Returns:
            bool: True if the key is held. False otherwise.
        """
        if self.is_newly_pressed(key):
            return True
        if mouse.is_pressed(key):
            if time.time_ns() - self.past_key_values[key][1] > hold_delay * 1_000_000_000:
                return True
        return False

    def update_wheel(self, event) -> None:
        """Update the wheel delta.

        Args:
            event (mouse.WheelEvent):
                The wheel event.
        """
        if type(event) is mouse.WheelEvent:
            self._wheel_delta += event.delta
            self.wheel_position += event.delta

    def update_inputs(self) -> dict[str, dict[str, float]]:
        inputs = {}
        for button in self.available_keys:
            inputs[button] = self.get_status(button)

        wheel_delta = self.wheel_delta
        inputs["wheel_delta"] = {
            "pressed": wheel_delta,
            "held": 0.0,
            "released": 1.0 if not wheel_delta else 0.0,
            "newly_pressed": wheel_delta if not self._past_wheel_delta else 0.0,
            "newly_released": 1.0 if not wheel_delta and self._past_wheel_delta else 0.0,
        }
        inputs["wheel_pos"] = {
            "pressed": self.wheel_position
        }

        self._past_wheel_delta = wheel_delta
        return inputs

    def get_status(self, user_input: str) -> dict[str, float] | None:
        """Get the status of an input.

        Args:
            user_input (str):
                The input to check.

        Returns:
            dict[str, float] | None: The status of the input.
                Keys are "pressed", "held", "released", "newly_pressed", and newly_released".
                If the key is invalid, returns None.
        """
        status = {
            "pressed": 0.0,
            "held": 0.0,
            "released": 0.0,
            "newly_pressed": 0.0,
            "newly_released": 0.0,
        }

        past_values = self.past_key_values

        # If the input is not in the list, return the empty status.
        try:
            val = mouse.is_pressed(user_input)
            if type(val) is bool:
                if val:
                    val = 1.0
                else:
                    val = 0.0

        except ValueError:
            return None

        # If this input hasn't been checked before, set the values accordingly.
        if user_input not in past_values.keys():
            status["pressed"] = val
            status["newly_released"] = 0.0
            if val:
                status["released"] = 0.0
                status["newly_pressed"] = val
                status["held"] = val
            else:
                status["released"] = 1.0
                status["newly_pressed"] = 0.0
                status["held"] = 0.0

        # If the input has been checked before and is pressed, set the values accordingly.
        elif val:
            status["pressed"] = val
            status["released"] = not val
            status["newly_released"] = 0.0
            if past_values[user_input][0]:
                status["newly_pressed"] = 0.0
                if time.time_ns() - past_values[user_input][1] > self.hold_delay * 1_000_000_000:
                    status["held"] = val
                else:
                    status["held"] = 0.0
            else:
                status["newly_pressed"] = val
                status["held"] = val

        # If the input has been checked before and is not pressed, set the values accordingly.
        else:
            status["pressed"] = val
            status["released"] = not val
            status["newly_pressed"] = 0.0
            status["held"] = 0.0
            if past_values[user_input][0]:
                status["newly_released"] = 1.0
            else:
                status["newly_released"] = 0.0

        # Update the past values.
        if status["released"] != 0.0:
            self.past_key_values[user_input] = [0.0, 0]
        elif status["newly_pressed"] != 0.0:
            self.past_key_values[user_input] = [val, time.time_ns()]
        elif status["pressed"] != 0.0:
            self.past_key_values[user_input][0] = val

        return status

    @property
    def wheel_delta(self):
        data = self._wheel_delta + 0
        self._wheel_delta = 0
        return data


if __name__ == "__main__":
    title = "Mouse Input Test"
    os.system("title " + title)

    mouse_input = MouseInput(title)
    c = cursor.Cursor()
    while True:
        # print(mouse_input.get_position())
        # c.clear_screen()

        c.set_pos(0, 0)
        print(" " * 100, end="\r", flush=True)
        print(mouse_input.update_inputs()["wheel_scroll"])
        # print(mouse_input.get_screen_char_position((40, 150)))

        # char = mouse_input.get_screen_char_position((40, 156))
        # c.set_pos(char[0], char[1])
        # print(char, end="", flush=True)

        # print(mouse_input.last_mouse_position)
        # print(mouse_input.get_relative_position())
        # if mouse_input.is_newly_pressed("left"):
        #     print("Left mouse button is newly pressed.")
        # if mouse_input.is_newly_pressed("right"):
        #     print("Right mouse button is newly pressed.")
        # if mouse_input.is_newly_pressed("middle"):
        #     print("Middle mouse button is newly pressed.")
        # if mouse_input.is_currently_pressed("left"):
        #     print("Left mouse button is pressed.")
        # if mouse_input.is_currently_pressed("right"):
        #     print("Right mouse button is pressed.")
        # if mouse_input.is_currently_pressed("middle"):
        #     print("Middle mouse button is pressed.")
        # if mouse_input.is_held("left"):
        #     print("Left mouse button is held.")
        # if mouse_input.is_held("right"):
        #     print("Right mouse button is held.")
        # if mouse_input.is_held("middle"):
        #     print("Middle mouse button is held.")
        time.sleep(0.05)


