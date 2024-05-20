import pickle

import color
from terminal_objects import *


class Screen:

    def __init__(self, screen_name: str, screen_size: tuple[int, int]) -> None:
        self.screen_name = screen_name
        self.screen_objects = []
        self.screen_size = screen_size
        self.display_array = [[[" ", [color.BACKGROUND_BLACK]] for _ in range(self.screen_size[1])] for _ in range(self.screen_size[0])]
        self.should_refresh = True

    def add_object(self, screen_object: TerminalObject) -> None:
        """Add an object to this screen.

        Args:
            screen_object (TerminalObject):
                The object to add.
        """
        self.screen_objects.append(screen_object)
        self.screen_objects.sort(key=lambda x: x.get_z_index())
        if screen_object.visible:
            self.update_display()
            self.should_refresh = True

    def remove_object(self, object_name: str) -> None:
        """Remove an object from this screen.

        Args:
            object_name (str):
                The name of the object to remove.
        """
        screen_object = [screen_object for screen_object in self.screen_objects if screen_object.get_name() == object_name][0]
        self.screen_objects = [screen_object for screen_object in self.screen_objects if screen_object.get_name() != object_name]
        if screen_object.visible:
            self.update_display()
            self.should_refresh = True

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
        obj.should_refresh()
        self.add_object(obj)

    def save_object_to_file(self, object_name: str, file_path: str) -> None:
        """Save an object to a file.

        Args:
            object_name (str):
                The name of the object to save.
            file_path (str):
                The path to the file.
        """
        for screen_object in self.screen_objects:
            if screen_object.get_name() == object_name:
                with open(file_path, "wb") as file:
                    pickle.dump(screen_object, file)

    def get_objects(self) -> list[TerminalObject]:
        """Return the objects on this screen.

        Returns:
            list[TerminalObject]: A list of the objects on this screen.
        """
        return self.screen_objects

    def get_name(self) -> str:
        return self.screen_name

    def get_display(self) -> list[list[list[str | list[str]]]]:
        return self.display_array

    def should_refresh(self) -> bool:
        """Return whether the screen should be refreshed.

        Returns:
            bool: True if an object on the screen or the screen itself says it should be refreshed, False otherwise.
        """
        if self.should_refresh:
            return True
        for screen_object in self.screen_objects:
            if screen_object.should_refresh():
                return True
        return False

    def update_display(self) -> list[list[list[str | list[str]]]]:
        """Update the screen display array with the contents of the screen objects and return it.

        Returns:
            list[list[list[str | list[str]]]]: The updated display array.
        """
        self.clear_display()

        for screen_object in self.screen_objects:
            if screen_object.visible:
                self.add_to_display(screen_object.get_contents(), screen_object.get_coordinates())
                screen_object.refreshed()

        self.should_refresh = False

        return self.display_array

    def clear_display(self) -> None:
        """Clear the display array of all symbols."""
        self.display_array = [[[" ", [color.BACKGROUND_BLACK]] for _ in range(self.screen_size[1])] for _ in range(self.screen_size[0])]

    def add_to_display(self, grid_to_add: list[list[list[str | list[str]]]],
                       coordinates: list[int] | tuple[int, int]) -> None:
        """Add stuff to the display.

        Args:
            grid_to_add (list[list[list[str | list[str]]]):
                The grid of characters to add to the display.
            coordinates (list[int] | tuple[int, int]):
                The coordinates of the top-left slot to add the grid from.
        """
        if (coordinates[0] + len(grid_to_add) > len(self.display_array)-1 or
                coordinates[1] + len(grid_to_add[0]) > len(self.display_array[0])-1):
            raise IndexError("Coordinates out of bounds.")

        # Go through the grid and add the characters to the display in a position offset by the coordinates given.
        for y, row in enumerate(grid_to_add):
            for x, column in enumerate(row):
                if column[0] != "":
                    self.display_array[y + coordinates[0]][x + coordinates[1]] = column

    def __str__(self):
        return self.screen_name

    def __repr__(self):
        return self.screen_name

    def __eq__(self, other):
        return self.screen_objects == other.screen_objects

    def __ne__(self, other):
        return not self == other

    def refresh_display_objects(self):
        for screen_object in self.screen_objects:
            screen_object.get_contents()

