import pickle

import color
import input_handler

from base_terminal_object import PrintableObject
from image_box import ImageBox
from input_handler import KeyboardInput, MouseInput, GamepadInput


class Screen:

    def __init__(self, screen_name: str, screen_size: tuple[int, int]) -> None:
        self._name = screen_name
        self._objects = []
        self._screen_size = screen_size
        self._display_array = [
            [
                [
                    " ", [color.BACKGROUND_BLACK]
                ] for _ in range(self._screen_size[1])
            ] for _ in range(self._screen_size[0])
        ]
        self._should_refresh = True

        self._key_bindings = dict()
        self._disabled_key_bindings = dict()

        self.default_keybinds = {

            # MenuBox

            # UP
            "selection_up (KB_UP) [default: MenuBox]": ["up", input_handler.KeyboardInput, "held", self.run_object_keybinds,
                                                        "selection_up", "MenuBox"],
            "selection_up (GP_DPAD_UP) [default: MenuBox]": ["DPadUp", input_handler.GamepadInput, "held", self.run_object_keybinds,
                                                             "selection_up", "MenuBox"],
            # DOWN
            "selection_down (KB_DOWN) [default: MenuBox]": ["down", input_handler.KeyboardInput, "held", self.run_object_keybinds,
                                                            "selection_down", "MenuBox"],
            "selection_down (GP_DPAD_DOWN) [default: MenuBox]": ["DPadDown", input_handler.GamepadInput, "held", self.run_object_keybinds,
                                                                 "selection_down", "MenuBox"],
            # LEFT
            "selection_left (KB_LEFT) [default: MenuBox]": ["left", input_handler.KeyboardInput, "held", self.run_object_keybinds,
                                                            "selection_left", "MenuBox"],
            "selection_left (GP_DPAD_LEFT) [default: MenuBox]": ["DPadLeft", input_handler.GamepadInput, "held", self.run_object_keybinds,
                                                                 "selection_left", "MenuBox"],
            # RIGHT
            "selection_right (KB_RIGHT) [default: MenuBox]": ["right", input_handler.KeyboardInput, "held", self.run_object_keybinds,
                                                              "selection_right", "MenuBox"],
            "selection_right (GP_DPAD_RIGHT) [default: MenuBox]": ["DPadRight", input_handler.GamepadInput, "held", self.run_object_keybinds,
                                                                   "selection_right", "MenuBox"],
            # # Cycle
            # "selection_cycle (KB_TAB) [default: MenuBox]": ["right", input_handler.KeyboardInput, "held", self.run_object_keybinds,
            #                                                   "cycle_selection", "MenuBox"],
            # "selection_cycle (GP_DPAD_RIGHT) [default: MenuBox]": ["DPadRight", input_handler.GamepadInput, "held", self.run_object_keybinds,
            #                                                        "selection_right", "MenuBox"],

        }

    def run_object_keybinds(self, value, key: str, key_type: KeyboardInput | MouseInput | GamepadInput,
                            action_type: str, *args, **kwargs) -> None:
        """Run the keybinds of an object.

        Args:
            value:
                The value to check against.
            key (str):
                The key to check.
            key_type (KeyboardInput | MouseInput | GamepadInput):
                The type of key.
            action_type (str):
                The action type.
            *args:
                The arguments to give the function.
            **kwargs:
                The keyword arguments to give the function.
        """
        pass

    def add_object(self, screen_object: PrintableObject) -> None:
        """Add an object to this screen.

        Args:
            screen_object (PrintableObject):
                The object to add.
        """
        self._objects.append(screen_object)
        self._objects.sort(key=lambda x: x.z_index)
        if screen_object.visible:
            self.update_display()
            self._should_refresh = True

    def remove_object(self, object_name: str) -> None:
        """Remove an object from this screen.

        Args:
            object_name (str):
                The name of the object to remove.
        """
        screen_object = self.get_object_by_name(object_name)
        if screen_object is not None:
            self._objects.remove(screen_object)

            if screen_object.visible:
                self.update_display()
                self._should_refresh = True

    def get_object_by_name(self, object_name: str) -> PrintableObject | None:
        """Return an object on this screen by grabbing the first object by whatever name is given.

        Args:
            object_name (str):
                The name of the object to return.

        Returns:
            PrintableObject | None: The object with the given name, or None if no object has that name.
        """
        for screen_object in self._objects:
            if screen_object.name == object_name:
                return screen_object
        return None

    def load_object_from_file(self, object_name: str, file_path: str) -> None:
        """Load an object from a file and add it to this screen.

        Args:
            object_name (str):
                The new name of the object to load.
            file_path (str):
                The path to the file.
        """
        with open(file_path, "rb") as file:
            obj = pickle.load(file)
        obj.set_name(object_name)
        obj.should_refresh = True
        self.add_object(obj)

    def save_object_to_file(self, object_name: str, file_path: str) -> None:
        """Save an object to a file.

        Args:
            object_name (str):
                The name of the object to save.
            file_path (str):
                The path to the file.
        """
        for screen_object in self._objects:
            if screen_object.get_name() == object_name:
                with open(file_path, "wb") as file:
                    pickle.dump(screen_object, file)

    def update_display(self) -> list[list[list[str | list[str]]]]:
        """Update the screen display array with the contents of the screen objects and return it.

        Returns:
            list[list[list[str | list[str]]]]: The updated display array.
        """
        self.clear_display()

        for screen_object in self._objects:
            if screen_object.visible:
                self.add_to_display(screen_object.contents, screen_object.coordinates)
                screen_object.should_refresh = False

        self._should_refresh = False

        return self._display_array

    def clear_display(self) -> None:
        """Clear the display array of all symbols."""
        self._display_array = [
            [
                [
                    " ", [color.BACKGROUND_DEFAULT_COLOR]
                ] for _ in range(self._screen_size[1])
            ] for _ in range(self._screen_size[0])
        ]

    def add_to_display(self, grid_to_add: list[list[list[str | list[str]]]],
                       coordinates: list[int] | tuple[int, int]) -> None:
        """Add a grid to the display.

        Args:
            grid_to_add (list[list[list[str | list[str]]]]):
                The grid of characters to add to the display.
            coordinates (list[int] | tuple[int, int]):
                The coordinates of the top-left slot to add the grid from.
        """
        # Go through the grid and add the characters to the display in a position offset by the coordinates given.
        for y, row in enumerate(grid_to_add):
            if y + coordinates[0] > len(self._display_array) - 1:
                break
            elif y + coordinates[0] < 0:
                continue
            for x, column in enumerate(row):
                if x + coordinates[1] > len(self._display_array[0]) - 1:
                    break
                elif x + coordinates[1] < 0:
                    continue
                if column[0] != "":
                    self._display_array[y + coordinates[0]][x + coordinates[1]] = column

    def run_animations(self) -> None:
        """Run the animations of the screen objects."""
        for screen_object in self._objects:
            if screen_object.visible and type(screen_object) is ImageBox:
                screen_object.update_image()


    def __str__(self):
        return self._name

    def __repr__(self):
        return self._name

    def __eq__(self, other):
        return self._objects == other.objects

    def __ne__(self, other):
        return not self == other

    @property
    def name(self) -> str:
        """Return the name of the screen.

        Returns:
            The name of the screen.
        """
        return self._name

    @property
    def objects(self) -> list[PrintableObject]:
        """Return the objects on the screen.

        Returns:
            list[PrintableObject]: The objects on the screen.
        """
        return self._objects

    @property
    def screen_size(self) -> tuple[int, int]:
        """Return the size of the screen.

        Returns:
            tuple[int, int]: The size of the screen.
        """
        return self._screen_size

    @property
    def display_array(self) -> list[list[list[str | list[str]]]]:
        """Return the _display array.

        Returns:
            list[list[list[str | list[str]]]]: The _display array.
        """
        return self._display_array

    @property
    def should_refresh(self) -> bool:
        """Return whether the screen should be refreshed.

        Returns:
            bool: True if an object on the screen or the screen itself says it should be refreshed, False otherwise.
        """
        if self._should_refresh:
            return True
        for screen_object in self._objects:
            if screen_object.should_refresh:
                return True
        return False

    @property
    def key_bindings(self) -> dict[str, list[str, KeyboardInput | MouseInput | GamepadInput,
                                             str, callable, tuple, dict]]:
        """Return the key bindings of the screen.

        Returns:
            dict[str, list[str, KeyboardInput | MouseInput | GamepadInput, str, callable, tuple, dict]]:
                The key bindings of the screen.
        """
        return self._key_bindings

    @property
    def disabled_key_bindings(self) -> dict[str, list[str, KeyboardInput | MouseInput | GamepadInput,
                                                      str, callable, tuple, dict]]:
        """Return the disabled key bindings of the screen.

        Returns:
            dict[str, list[str, KeyboardInput | MouseInput | GamepadInput, str, callable, tuple, dict]]:
                The disabled key bindings of the screen.
        """
        return self._disabled_key_bindings

    @name.setter
    def name(self, new_name: str) -> None:
        """Set the name of the screen.

        Args:
            new_name (str):
                The new name of the screen.
        """
        self._name = new_name

    @objects.setter
    def objects(self, new_objects: list[PrintableObject]) -> None:
        """Set the objects on the screen.

        Args:
            new_objects (list[PrintableObject]):
                The new objects on the screen.
        """
        self._objects = new_objects

    @screen_size.setter
    def screen_size(self, new_screen_size: tuple[int, int]) -> None:
        """Set the size of the screen.

        Args:
            new_screen_size (tuple[int, int]):
                The new size of the screen.
        """
        self._screen_size = new_screen_size
        self.clear_display()
        self._should_refresh = True
        for screen_object in self._objects:
            screen_object.coordinates = screen_object.coordinates.screen_size = new_screen_size
            screen_object.size = screen_object.size.screen_size = new_screen_size

    @display_array.setter
    def display_array(self, new_display_array: list[list[list[str | list[str]]]]) -> None:
        """Set the display array. Kinda pointless bc it'd never be used (I hope)

        Args:
            new_display_array (list[list[list[str | list[str]]]]):
                The new display array.
        """
        self._display_array = new_display_array

    @should_refresh.setter
    def should_refresh(self, new_should_refresh: bool) -> None:
        """Set whether the screen should be refreshed.

        Args:
            new_should_refresh (bool):
                True if the screen should be refreshed, False otherwise.
        """
        self._should_refresh = new_should_refresh

    @key_bindings.setter
    def key_bindings(self, new_key_bindings: dict[str, list[str, KeyboardInput | MouseInput | GamepadInput,
                                                            str, callable, tuple, dict]]) -> None:
        """Set the key bindings of the screen.

        Args:
            new_key_bindings (dict[str, list[str, KeyboardInput | MouseInput | GamepadInput,
                                             str, callable, tuple, dict]]):
                The new key bindings of the screen.
        """
        self._key_bindings = new_key_bindings

    @disabled_key_bindings.setter
    def disabled_key_bindings(self, new_disabled_key_bindings: dict[str, list[str,
                              KeyboardInput | MouseInput | GamepadInput, str, callable, tuple, dict]]) -> None:
        """Set the disabled key bindings of the screen.

        Args:
            new_disabled_key_bindings (dict[str, list[str, KeyboardInput | MouseInput | GamepadInput,
                                                      str, callable, tuple, dict]]):
                The new disabled key bindings of the screen.
        """
        self._disabled_key_bindings = new_disabled_key_bindings
