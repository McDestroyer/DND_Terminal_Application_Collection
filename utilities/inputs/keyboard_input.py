"""Work with keyboard inputs."""
import time

# Disables annoying and usually incorrect warnings.
# pylint: disable=wrong-import-position
# pylint: disable=import-error

# Make sure the dependency is installed.
# import dependency_installer
# dependency_installer.install_dependency("keyboard")

import keyboard


class KeyboardInput:
    """Work with keyboard inputs."""

    def __init__(self) -> None:
        """Initialize the KeyboardInput object."""
        # The keys previously pressed
        self.keys = {}
        self.hold_delay = 0.25
        # keyboard.remap_hotkey("ctrl+c", "alt+c")
        # keyboard.remap_hotkey("ctrl+v", "alt+v")
        # keyboard.remap_hotkey("esc", "ctrl+c", trigger_on_release=True)

        self.key_list = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            'space', 'enter', 'esc', 'tab', 'shift', 'ctrl', 'alt',
            'backspace', 'delete', 'insert', 'home', 'end', 'pageup', 'pagedown',
            'up', 'down', 'left', 'right',
            # '+', '-', '*', '/', '=', '<', '>', '!', '@', '#', '$', '%', '^', '&', '|',
            # '(', ')', '[', ']', '{', '}', ':', ';', ',', '.', '?', '_', '`', '~',
            '`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '[', '{', ']', '}', '\\',
            '|', ';', ':', '\'', '"', ',', '<', '.', '>', '/', '?'
        ]

        cannon_names = list(keyboard._canonical_names.canonical_names.values())
        for name in cannon_names:
            if len(name) > 1 and name not in self.key_list:
                self.key_list.append(name)

        # self.update_inputs()

        self.block_all()

    def block_all(self) -> None:
        """Block all keys so they don't do anything in the background by accident."""
        keys = self.update_inputs().keys()
        for key in keys:
            try:
                keyboard.block_key(key)
            except:
                pass

    def unblock_all(self) -> None:
        """Unblock all keys so they do something in the background."""
        keys = self.update_inputs().keys()
        for key in keys:
            try:
                keyboard.unhook_all()
            except:
                pass

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
        if key in self.keys:
            if keyboard.is_pressed(key) and self.keys[key][0] is False:
                self.keys[key][0] = True
                self.keys[key][1] = time.time_ns()
                result = True
            elif keyboard.is_pressed(key) and self.keys[key][0] is True:
                pass
            else:
                self.keys[key][0] = False
                self.keys[key][1] = 0

        # If it isn't in the list, set the result and the value
        # to whether or not it's currently pressed.
        else:
            if keyboard.is_pressed(key):
                self.keys[key] = [True, time.time_ns()]
                result = True
            else:
                self.keys[key] = [False, 0]

        # If a function is provided and the result was True, run the function.
        if result and function is not None:
            function()

        return result

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
        # Update the time
        self.is_newly_pressed(key)

        # Update the list
        if key in self.keys:
            self.keys[key][0] = keyboard.is_pressed(key)
        else:
            self.keys[key] = [keyboard.is_pressed(key), 0]

        # Run if true
        if function is not None and self.keys[key][0]:
            function()

        return self.keys[key][0]

    def is_held(self, key: str, function: callable or None = None) -> bool:
        """Check if a key is being held down. Returns True if just pressed, false for the next

        Args:
            key (str):
                The key to check.
            function (callable | None, optional):
                The function to call if the key is held.
                Defaults to None.

        Returns:
            bool: True if the key is held. False otherwise.
        """
        result = False

        if keyboard.is_pressed(key):
            if key not in self.keys.keys():
                self.keys[key] = [False, 0]
            # If it's the first time the key is pressed, set the time and result.
            if not self.keys[key][0]:
                self.keys[key][1] = time.time_ns()
                result = True
            # If it's pressed and the time is greater than the hold_delay, set the result.
            else:
                if time.time_ns() - self.keys[key][1] > self.hold_delay * 1_000_000_000:
                    result = True
            # If it's not greater than the hold_delay, the result is False by default.

        # If it's not pressed, reset the time.
        else:
            if key not in self.keys.keys():
                self.keys[key] = [False, 0]
            else:
                self.keys[key][1] = 0

        # Update the list
        self.keys[key][0] = keyboard.is_pressed(key)

        # Run the given function if set and pressed.
        if function is not None and result:
            function()

        return result

    def update_inputs(self) -> dict[str, dict[str, float]]:
        """Update the inputs."""
        key_statuses = {}

        for key in self.key_list:
            stat = self.get_status(key)
            if stat is not None:
                key_statuses[key] = stat
        return key_statuses

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

        past_values = self.keys

        # If the input is not in the list, return the empty status.
        try:
            val = keyboard.is_pressed(user_input)
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
            self.keys[user_input] = [0.0, 0]
        elif status["newly_pressed"] != 0.0:
            self.keys[user_input] = [val, time.time_ns()]
        elif status["pressed"] != 0.0:
            self.keys[user_input][0] = val

        return status


if __name__ == "__main__":
    kb = KeyboardInput()

    # kb.update_inputs()
    keys = list(kb.update_inputs().keys())
    keys.sort()
    print(keys)

    while True:
        break
        # if kb.is_newly_pressed("a"):
        #     print("a is newly pressed")
        # if kb.is_currently_pressed("a"):
        #     print("a is currently pressed")
        # if kb.is_held("a"):
        #     print("a is held")
        # if kb.get_status("a")["held"]:
        #     print(kb.get_status("a")["held"])
        # print(kb.get_status("a"))
        #
        # time.sleep(0.1)
