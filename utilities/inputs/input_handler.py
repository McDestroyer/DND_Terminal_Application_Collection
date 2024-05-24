import sys

from keyboard_input import KeyboardInput
from mouse_input import MouseInput
from gamepad_input import GamepadInput


class InputHandler:
    """Handle mouse, keyboard, and gamepad inputs."""
    def __init__(self, window_name: str) -> None:
        self.kb = KeyboardInput()
        """The keyboard class."""
        self.mouse = MouseInput(window_name)
        """The mouse class."""
        self.gp = GamepadInput()
        """The gamepad class."""

        self.keybinds: dict[str, list[str, KeyboardInput | MouseInput | GamepadInput, str, callable, tuple, dict]] = {}
        """The keybinds, in the form of {"name": ["key", device, "action type key", function, *args, **kwargs]} where:\n
        name is the name of the keybind,\n
        key is the key to press,\n
        device is one of the following: KeyboardInput, MouseInput, or GamepadInput,\n
        action type key is one of the following: "pressed", "held", "released", "newly_pressed", or "newly_released",\n
        function is the function to run,\n
        and *args and **kwargs are the arguments and keyword arguments."""

        self.disabled_keybinds: dict[
            str, list[str, KeyboardInput | MouseInput | GamepadInput, str, callable, tuple, dict]
        ] = []

    def check_keybinds(self) -> None:
        """Check the keybinds. If a keybind is pressed, run the function."""
        for binding in self.keybinds:
            # Check the device given in the keybind.
            key = self.keybinds[binding][0]
            device = self.keybinds[binding][1]
            action_type = self.keybinds[binding][2]
            function = self.keybinds[binding][3]
            args = self.keybinds[binding][4]
            kwargs = self.keybinds[binding][5]

            value = device.get_status(key)[action_type]

            # If the value is not None, run the function, giving it the value.
            if value:
                function(value, *args, **kwargs)
                return

    def add_keybind(self, binding_name: str, key: str, device: KeyboardInput | MouseInput | GamepadInput,
                    action_type: str, function: callable, *args, **kwargs) -> None:
        """Add a keybind.

        Args:
            binding_name (str):
                The name of the keybind.
            key (str):
                The key to press.
            device (KeyboardInput | MouseInput | GamepadInput):
                The device to use.
            action_type (str):
                The action type key.
            function (callable):
                The function to run.
            *args:
                The arguments to give the function.
            **kwargs:
                The keyword arguments to give the function.
        """
        self.keybinds[binding_name] = [key, device, action_type, function, args, kwargs]

    def remove_keybind(self, binding_name: str) -> None:
        """Remove a keybind.

        Args:
            binding_name (str):
                The name of the keybind.
        """
        self.keybinds.pop(binding_name)

    def disable_keybind(self, binding_name: str) -> None:
        """Disable a keybind.

        Args:
            binding_name (str):
                The name of the keybind.
        """
        self.disabled_keybinds.update(self.keybinds.pop(binding_name))

    def enable_keybind(self, binding_name: str) -> None:
        """Enable a keybind.

        Args:
            binding_name (str):
                The name of the keybind.
        """
        self.keybinds.update(self.disabled_keybinds.pop(binding_name))

    def disable_all_keybinds(self) -> None:
        """Disable all keybinds."""
        self.disabled_keybinds.update(self.keybinds)
        self.keybinds.clear()

    def enable_all_keybinds(self) -> None:
        """Enable all keybinds."""
        self.keybinds.update(self.disabled_keybinds)
        self.disabled_keybinds.clear()

    def clear_keybinds(self) -> None:
        """Clear all keybinds."""
        self.keybinds.clear()
        self.disabled_keybinds.clear()

    def clear_input_buffer(self) -> None:
        try:
            print("Clearing...")
            # For Windows platform
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
            print("Successfully cleared the input buffer.")
        except ImportError:
            # For Linux/Unix
            print("Clear failed.")
            print("Are you on Linux/Unix? Trying again...")
            import termios
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            print("Successfully cleared the input buffer.")
