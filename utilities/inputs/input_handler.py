import sys

from keyboard_input import KeyboardInput
from mouse_input import MouseInput
from gamepad_input import GamepadInput
from screen_class import Screen


class InputHandler:
    """Handle mouse, keyboard, and gamepad inputs."""
    def __init__(self, window_name: str) -> None:
        self.kb = KeyboardInput()
        """The keyboard class."""
        self.mouse = MouseInput(window_name)
        """The mouse class."""
        self.gp = GamepadInput()
        """The gamepad class."""

        # self.keybinds: dict[str, list[str, KeyboardInput | MouseInput | GamepadInput, str, callable, tuple, dict]] = {}
        """The keybinds are in the form of\n
        {"name": ["key", device, "action type key", function, *args, **kwargs]}\n
        where:\n
        name is the name of the keybind,\n
        key is the key to press,\n
        device is one of the following: KeyboardInput, MouseInput, or GamepadInput,\n
        action type key is one of the following: "pressed", "held", "released", "newly_pressed", or "newly_released",\n
        function is the function to run,\n
        and *args and **kwargs are the arguments and keyword arguments."""

        # self.disabled_keybinds: dict[str, dict[
        #     str, list[str, KeyboardInput | MouseInput | GamepadInput, str, callable, tuple, dict]
        # ]] = []

    def update(self) -> None:
        """Update the inputs and store the values."""
        self.keyboard_states = self.kb.update_inputs()
        self.mouse_states = self.mouse.update_inputs()
        try:
            self.gamepad_states = self.gp.update_inputs()
        except:
            self.gamepad_states = None

    def check_keybinds(self, screen: Screen) -> None:
        """Check the keybinds. If a keybind is pressed, run the function.

        Args:
            screen (Screen):
                The screen to check the keybinds for.
        """
        try:
            for binding in screen.key_bindings:
                # Check the device given in the keybind.
                key = screen.key_bindings[binding][0]
                device = screen.key_bindings[binding][1]
                action_type = screen.key_bindings[binding][2]
                function = screen.key_bindings[binding][3]
                args = screen.key_bindings[binding][4]
                kwargs = screen.key_bindings[binding][5]

                # value = device.get_status(key)[action_type]

                if device == self.kb:
                    value = self.keyboard_states[key][action_type]
                elif device == self.mouse:
                    value = self.mouse_states[key][action_type]
                elif device == self.gp and self.gamepad_states is not None:
                    value = self.gamepad_states[key][action_type]
                else:
                    value = None

                # If the value is not None, run the function, giving it the value.
                if value:
                    function(value, *args, **kwargs)
        except KeyError:
            return None

    def add_keybind(self, screen: Screen, binding_name: str, key: str, device: KeyboardInput | MouseInput | GamepadInput,
                    action_type: str, function: callable, *args, **kwargs) -> None:
        """Add a keybind.

        Args:
            screen (Screen):
                The screen to add the keybind to.
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
        screen.key_bindings[binding_name] = [key, device, action_type, function, args, kwargs]

    def remove_keybind(self, screen: Screen, binding_name: str) -> None:
        """Remove a keybind.

        Args:
            screen (Screen):
                The screen to remove the keybind from.
            binding_name (str):
                The name of the keybind.
        """
        screen.key_bindings.pop(binding_name)

    def disable_keybind(self, screen: Screen, binding_name: str) -> None:
        """Disable a keybind.

        Args:
            screen (Screen):
                The screen to disable the keybind for.
            binding_name (str):
                The name of the keybind.
        """
        screen.disabled_key_bindings.update(screen.key_bindings.pop(binding_name))

    def enable_keybind(self, screen: Screen, binding_name: str) -> None:
        """Enable a keybind.

        Args:
            screen (Screen):
                The screen to enable the keybind for.
            binding_name (str):
                The name of the keybind.
        """
        screen.key_bindings.update(screen.disabled_key_bindings.pop(binding_name))

    def disable_all_keybinds(self, screen: Screen) -> None:
        """Disable all keybinds.

        Args:
            screen (Screen):
                The screen to disable all keybinds for.
        """
        screen.disabled_key_bindings.update(screen.key_bindings)
        screen.key_bindings.clear()

    def enable_all_keybinds(self, screen: Screen) -> None:
        """Enable all keybinds.

        Args:
            screen (Screen):
                The screen to enable all keybinds for.
        """
        screen.key_bindings.update(screen.disabled_key_bindings)
        screen.disabled_key_bindings.clear()

    def clear_keybinds(self, screen: Screen) -> None:
        """Clear all keybinds.

        Args:
            screen (Screen):
                The screen to clear the keybinds for.
        """
        screen.key_bindings.clear()
        screen.disabled_key_bindings.clear()

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
