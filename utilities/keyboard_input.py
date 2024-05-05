"""Work with keyboard inputs."""
import time

# Disables annoying and usually incorrect warnings.
# pylint: disable=wrong-import-position
# pylint: disable=import-error

# Make sure the dependency is installed.
import dependency_installer
dependency_installer.install_dependency("keyboard")

import keyboard


class KeyboardInput:
    """Work with keyboard inputs."""

    def __init__(self) -> None:
        """Initialize the KeyboardInput object."""
        # The keys previously pressed
        self.keys = {}
        self.hold_delay = 0.25

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
