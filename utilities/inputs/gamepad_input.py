from time import sleep, time_ns

# For testing purposes:

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


# Disables annoying and usually incorrect warnings.
# pylint: disable=wrong-import-position
# pylint: disable=import-error

# Make sure the dependency is installed.
import dependency_installer
dependency_installer.install_dependency("pygamepad")

from pygamepad.gamepads import Gamepad


class _XboxController:
    def __init__(self, gamepad: Gamepad | None, gamepad_input: 'GamepadInput'):
        self.gamepad = gamepad
        self.gamepad_input = gamepad_input

        self.deadzone = 0.15
        self.axes = {}
        self.buttons = {}

        inputs = self.update_inputs()

        self.past_inputs = {}
        self.toggle_buttons = {}

        for button in inputs.keys():
            self.past_inputs[button] = [inputs[button], 0]
            self.toggle_buttons[button] = False

    def update_inputs(self, update_gamepad: bool = False) -> dict[str, float]:
        """Update the inputs from the gamepad and return them as a dictionary.

        Args:
            update_gamepad (bool, optional):
                Whether to update the gamepad if it was disconnected. False by default because of memory leak issues and
                the fact that if it were run without a controller it prints out a lot of errors I can't stop.
                Defaults to False.

        Returns:
            dict[str, float]: A dictionary containing the inputs from the gamepad.
        """
        if update_gamepad:
            self.gamepad = self.gamepad_input.get_gamepad()

        btns = self.gamepad.buttons

        self.axes = {
            'LeftX': btns.ABS_X.value if abs(btns.ABS_X.value) >= self.deadzone else 0.0,
            'LeftY': btns.ABS_Y.value if abs(btns.ABS_Y.value) >= self.deadzone else 0.0,
            'RightX': btns.ABS_RX.value if abs(btns.ABS_RX.value) >= self.deadzone else 0.0,
            'RightY': btns.ABS_RY.value if abs(btns.ABS_RY.value) >= self.deadzone else 0.0,
            'LeftTrigger': btns.ABS_Z.value if abs(btns.ABS_Z.value) >= self.deadzone else 0.0,
            'RightTrigger': btns.ABS_RZ.value if abs(btns.ABS_RZ.value) >= self.deadzone else 0.0,
        }
        self.buttons = {
            'A': 1.0 if btns.BTN_SOUTH.value else 0.0,
            'B': 1.0 if btns.BTN_EAST.value else 0.0,
            'Y': 1.0 if btns.BTN_NORTH.value else 0.0,
            'X': 1.0 if btns.BTN_WEST.value else 0.0,
            'LeftBumper': 1.0 if btns.BTN_TL.value else 0.0,
            'RightBumper': 1.0 if btns.BTN_TR.value else 0.0,
            'Back': 1.0 if btns.BTN_START.value else 0.0,
            'Start': 1.0 if btns.BTN_SELECT.value else 0.0,
            'LeftStick': 1.0 if btns.BTN_THUMBL.value else 0.0,
            'RightStick': 1.0 if btns.BTN_THUMBR.value else 0.0,
            'DPadUp': 1.0 if btns.ABS_HAT0Y.value == -1 else 0.0,
            'DPadDown': 1.0 if btns.ABS_HAT0Y.value == 1 else 0.0,
            'DPadLeft': 1.0 if btns.ABS_HAT0X.value == -1 else 0.0,
            'DPadRight': 1.0 if btns.ABS_HAT0X.value == 1 else 0.0,
        }

        return self.axes | self.buttons


class GamepadInput:
    def __init__(self):
        self.gamepad = None
        self.get_gamepad()

        self.controller = _XboxController(self.gamepad, self)
        self.controller.deadzone = 0.15
        self.hold_delay = .25

    def get_gamepad(self) -> Gamepad | None:
        """Get the gamepad object.

        Returns:
            Gamepad | None: The gamepad object if it exists. If not it tries to get it.
        """
        try:
            # if self.gamepad:
            #     print("Stopping Gamepad!")
            #     self.gamepad.stop_listening()
            #     # self.gamepad = None
            self.gamepad = Gamepad()
            self.gamepad.listen()
            # print("Gamepad Connected!")
        except IndexError:
            # print("Gamepad Not Found!")
            self.gamepad = None
        return self.gamepad

    def read_inputs(self) -> dict[str, float]:
        """Read the inputs from the gamepad and return them as a dictionary.

        Returns:
            dict[str, float]: A dictionary containing the inputs from the gamepad.
        """
        return self.controller.update_inputs()

    def list_axes(self) -> list[str]:
        """List the available axes.

        Returns:
            list[str]: The available axes.
        """
        return list(self.controller.axes.keys())

    def list_buttons(self) -> list[str]:
        """List the available buttons.

        Returns:
            list[str]: The available buttons.
        """
        return list(self.controller.buttons.keys())

    def set_deadzone(self, deadzone: float) -> None:
        """Set the deadzone of the controller.

        Args:
            deadzone (float):
                The deadzone to set.
        """
        self.controller.deadzone = deadzone

    def get_deadzone(self) -> float:
        """Get the deadzone of the controller.

        Returns:
            float: The deadzone of the controller.
        """
        return self.controller.deadzone

    def is_newly_pressed(self, input: str) -> float:
        """Check to see if an input is newly pressed.

        Args:
            input (str):
                The input to check.

        Returns:
            float: the value of the input if it is newly pressed.
        """
        input_list = self.controller.update_inputs()
        past_values = self.controller.past_inputs

        # If the input is pressed and wasn't pressed before, return the value.
        if input_list[input]:
            if not past_values[input][0]:
                self.controller.past_inputs[input] = [input_list[input], time_ns()]
                # Toggle the button toggle variable.
                self.controller.toggle_buttons[input] = not self.controller.toggle_buttons[input]
                return input_list[input]
            else:
                # If the input was pressed before, update the past value.
                self.controller.past_inputs[input][0] = input_list[input]
                return 0.0

        # If the input is not pressed return 0.0.
        self.controller.past_inputs[input] = [0.0, 0]
        return 0.0

    def is_currently_pressed(self, input: str) -> float:
        """Check to see if an input is currently pressed.

        Args:
            input (str):
                The input to check.

        Returns:
            float: the value of the input if it is currently pressed.
        """
        input_list = self.controller.update_inputs()

        # If the input is newly pressed, return True. Used to actuate the toggle and update the past values.
        if self.is_newly_pressed(input):
            return input_list[input]

        # If the input is pressed, return True.
        if input_list[input]:
            return input_list[input]

        # If the input is not pressed, return False.
        return 0.0

    def is_held(self, input: str, hold_time: float = .25) -> float:
        """Check to see if an input is held.

        Args:
            input (str):
                The input to check.
            hold_time (float, optional):
                The time in seconds the input must be held to return True after the first loop.
                Defaults to 0.25.

        Returns:
            float: the value of the input if it is held.
        """
        input_list = self.controller.update_inputs()
        past_values = self.controller.past_inputs

        if self.is_newly_pressed(input):
            return input_list[input]

        # If the input is pressed and was pressed before, return True.
        if input_list[input] and past_values[input][1] > hold_time * 1_000_000_000:
            return input_list[input]

        # If the input is not pressed, return False.
        return 0.0

    # def is_newly_released(self, input: str) -> bool:
    #     """Check to see if an input is newly released.
    #
    #     Args:
    #         input (str):
    #             The input to check.
    #
    #     Returns:
    #         float: the value of the input if it is newly released.
    #     """
    #     input_list = self.controller.update_inputs()
    #     past_values = self.controller.past_inputs
    #
    #     # If the input is not pressed and was pressed before, return True.
    #     if not input_list[input] and past_values[input][0]:
    #         self.controller.past_inputs[input] = [input_list[input], 0]
    #         return True
    #
    #     # If the input is not pressed, and it's nothing new, return False.
    #     self.controller.past_inputs[input] = [0.0, 0]
    #     return False

    def is_newly_released(self, input: str, function: callable or None = None) -> bool:
        """Detect if an input is released and return True if
        it was pressed the last time this function was called.
        Designed to be run every frame, and the inverse of is_newly_pressed.

        Args:
            input (str):
                 key to check the newness of the released compression thereof.
            function (str, optional):
                 The function to execute if the key is newly released.

        Returns:
            bool: True if the key is not pressed but was pressed during the previous call.
            False otherwise.
        """
        result = False
        input_list = self.controller.update_inputs()

        # If the key hasn't been pressed previously, check it's previous value.
        # If it says it wasn't pressed, but it is now, change to fit and set the result accordingly
        # and vise-versa.
        # If the current and previous values are the same, set the result to False.
        if input in self.controller.past_inputs.keys():
            if not input_list[input]:
                if self.controller.past_inputs[input][0]:
                    self.controller.past_inputs[input] = [0.0, 0]
                    result = True
            elif input_list[input] and not self.controller.past_inputs[input][0]:
                self.controller.past_inputs[input] = [input_list[input], time_ns()]

        # If it isn't in the list, set the result and the value
        # to whether or not it's currently pressed.
        else:
            if input_list[input]:
                self.controller.past_inputs[input] = [input_list[input], time_ns()]
            else:
                result = True
                self.controller.past_inputs[input] = [0.0, 0]

        if result and function is not None:
            function()

        return result

    def get_status(self, input: str) -> dict[str, float] | None:
        """Get the status of an input.

        Args:
            input (str):
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

        input_list = self.controller.update_inputs()
        past_values = self.controller.past_inputs

        # If the input is not in the list, return the empty status.
        if input not in input_list.keys():
            return None

        # Get the value of the input.
        val = input_list[input]
        if type(val) is bool:
            if val:
                val = 1.0
            else:
                val = 0.0

        # If this input hasn't been checked before, set the values accordingly.
        if input not in past_values.keys():
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
            if past_values[input][0]:
                status["newly_pressed"] = 0.0
                if time_ns() - past_values[input][1] > self.hold_delay * 1_000_000_000:
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
            if past_values[input][0]:
                status["newly_released"] = 1.0
            else:
                status["newly_released"] = 0.0

        # Update the past values.
        if status["released"] != 0.0:
            self.controller.past_inputs[input] = [0.0, 0]
        elif status["newly_pressed"] != 0.0:
            self.controller.past_inputs[input] = [val, time_ns()]
        elif status["pressed"] != 0.0:
            self.controller.past_inputs[input][0] = val

        return status


if __name__ == "__main__":
    controller = GamepadInput()
    c = cursor.Cursor()
    c.clear_screen()
    while 1:
        start = time_ns()
        c.clear_screen()
        c.set_pos()

        # controller.controller.update_inputs(True)

        # print("A Newly Released:", controller.is_newly_released("A"))
        # print("Inputs:", controller.read_inputs())
        # print("A Newly Pressed:", controller.is_newly_pressed("A"))
        # print("A Pressed:", controller.is_currently_pressed("A"))
        # print("A Held:", controller.is_held("A"))
        # print("A Toggled:", controller.controller.toggle_buttons["A"])
        # print()
        # print("LX Newly Pressed:", controller.is_newly_pressed("LeftX"))
        # print("LX Newly Released:", controller.is_newly_released("LeftX"))
        # print("LX Pressed:", controller.is_currently_pressed("LeftX"))
        # print("LX Held:", controller.is_held("LeftX"))
        # print("LX Toggled:", controller.controller.toggle_buttons["LeftX"])
        # print()
        # print("Deadzone:", controller.get_deadzone())

        print(controller.get_status("A"))

        time_spent = (time_ns() - start) / 1_000_000
        print("Time:", time_spent, time_ns())

        sleep(0.5)
