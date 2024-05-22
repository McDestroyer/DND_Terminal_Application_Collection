import pickle

import color

from base_terminal_object import PrintableObject


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
        """Update the screen _display array with the _contents of the screen objects and return it.

        Returns:
            list[list[list[str | list[str]]]]: The updated _display array.
        """
        self.clear_display()

        for screen_object in self._objects:
            if screen_object.visible:
                self.add_to_display(screen_object.contents, screen_object.coordinates)
                screen_object.should_refresh = False

        self._should_refresh = False

        return self._display_array

    def clear_display(self) -> None:
        """Clear the _display array of all symbols."""
        self._display_array = [
            [
                [
                    " ", [color.BACKGROUND_BLACK]
                ] for _ in range(self._screen_size[1])
            ] for _ in range(self._screen_size[0])
        ]

    def add_to_display(self, grid_to_add: list[list[list[str | list[str]]]],
                       coordinates: list[int] | tuple[int, int]) -> None:
        """Add stuff to the _display.

        Args:
            grid_to_add (list[list[list[str | list[str]]]]):
                The grid of characters to add to the _display.
            coordinates (list[int] | tuple[int, int]):
                The coordinates of the top-left slot to add the grid from.
        """
        # if (_coordinates[0] + len(grid_to_add) > len(self._display_array)-1 or
        #         _coordinates[1] + len(grid_to_add[0]) > len(self._display_array[0])-1):
        #     raise IndexError("Coordinates out of bounds.")

        # Go through the grid and add the characters to the _display in a position offset by the _coordinates given.
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

    def __str__(self):
        return self._name

    def __repr__(self):
        return self._name

    def __eq__(self, other):
        return self._objects == other.screen_objects

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

    @display_array.setter
    def display_array(self, new_display_array: list[list[list[str | list[str]]]]) -> None:
        """Set the _display array.

        Args:
            new_display_array (list[list[list[str | list[str]]]]):
                The new _display array.
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
