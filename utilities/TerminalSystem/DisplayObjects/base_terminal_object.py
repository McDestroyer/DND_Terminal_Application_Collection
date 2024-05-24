from copy import deepcopy
from coordinates import Coordinate


class PrintableObject:
    """A generic printable object for the terminal manager."""
    def __init__(self, name: str, coordinates: Coordinate, size: Coordinate, minimum_size: Coordinate | None = None,
                 description: str | None = None, contents: list[list[list[str | list[str]]]] | None = None,
                 z_index: int = 0, visible: bool = True) -> None:
        """Initialize the PrintableObject object.

        Args:
            name (str):
                The name of the object.
            coordinates (Coordinate):
                The coordinates of the upper-left corner of the object.
            size (Coordinate):
                The size of the object.
            minimum_size (Coordinate, optional):
                The minimum size of the object.
            description (str, optional):
                The description of the object.
                Defaults to None.
            contents (list[list[list[str | list[str]]], optional):
                The contents of the object in terminal display format.
                Defaults to a list of empty characters.
            z_index (int, optional):
                The z-index of the object.
                Defaults to 0.
            visible (bool, optional):
                Whether the object is visible.
                Defaults to True.
            """
        self._name = name
        self._coordinates = coordinates
        self._size = size
        self._description = description
        self._contents = deepcopy(contents)
        self._z_index = z_index
        self._visible = visible
        self._should_refresh = True

        # Ensure the size is at least the minimum size.
        if minimum_size is None:
            self._minimum_size = (1, 1)
        else:
            self._minimum_size = minimum_size
        if self._size._char_value_y < self._minimum_size[0] or self._size._char_value_x < self._minimum_size[1]:
            self._size = deepcopy(self._minimum_size)

        # Ensure the contents are not None.
        if self._contents is None:
            self._contents = [[[" ", []] for _ in range(self._size[1])] for _ in range(self._size[0])]

    @property
    def name(self) -> str:
        """Return the name of the object.

        Returns:
            The name of the object.
        """
        return self._name

    @property
    def coordinates(self) -> Coordinate:
        """Return the coordinates of the object.

        Returns:
            Coordinate: The coordinates of the upper left corner of the object.
        """
        return self._coordinates

    @property
    def size(self) -> Coordinate:
        """Return the size of the object.

        Returns:
            Coordinate: The size of the object.
        """
        return self._size

    @property
    def minimum_size(self) -> Coordinate:
        """Return the minimum size of the object.

        Returns:
            Coordinate: The minimum size of the object.
        """
        return self._minimum_size

    @property
    def description(self) -> str | None:
        """Return the description of the object.

        Returns:
            str | None: The description of the object.
        """
        return self._description

    @property
    def contents(self) -> list[list[list[str | list[str]]]]:
        """Return the contents of the object.

        Returns:
            list[list[list[str | list[str]]]]: The contents of the object.
        """
        return self._contents

    @property
    def z_index(self) -> int:
        """Return the z-index of the object.

        Returns:
            int: The z-index of the object.
        """
        return self._z_index

    @property
    def visible(self) -> bool:
        """Return whether the object is visible.

        Returns:
            bool: Whether the object is visible.
        """
        return self._visible

    @property
    def should_refresh(self) -> bool:
        """Return whether the object should be refreshed.

        Returns:
            bool: True if the object should be refreshed.
        """
        return self._should_refresh

    @name.setter
    def name(self, name: str) -> None:
        """Set the name of the object.

        Args:
            name (str):
                The new name of the object.
        """
        self._name = name

    @coordinates.setter
    def coordinates(self, coordinates: Coordinate) -> None:
        """Set the coordinates of the object.

        Args:
            coordinates (Coordinate):
                The new coordinates of the object.
        """
        self._coordinates = coordinates
        self._should_refresh = True

    @size.setter
    def size(self, size: Coordinate) -> None:
        """Set the size of the object.

        Args:
            size (Coordinate):
                The new size of the object.
        """
        self._size = Coordinate(
            self._coordinates.screen_size,
            max(size.values["CHAR"][0], self._minimum_size.values["CHAR"][0]),
            max(size.values["CHAR"][1], self._minimum_size.values["CHAR"][1])
        )

    @minimum_size.setter
    def minimum_size(self, minimum_size: Coordinate) -> None:
        """Set the minimum size of the object.

        Args:
            minimum_size (Coordinate):
                The new minimum size of the object.
        """
        self._minimum_size = minimum_size
        if self._size.char_value_y < self._minimum_size[0] or self._size.char_value_x < self._minimum_size[1]:
            self._size = deepcopy(self._minimum_size)
            self._should_refresh = True

    @description.setter
    def description(self, description: str | None) -> None:
        """Set the description of the object.

        Args:
            description (str | None):
                The new description of the object.
        """
        self._description = description

    @contents.setter
    def contents(self, contents: list[list[list[str | list[str]]]]) -> None:
        """Set the contents of the object.

        Args:
            contents (list[list[list[str | list[str]]]]):
                The new contents of the object.
        """
        self._contents = contents
        self._should_refresh = True

    @z_index.setter
    def z_index(self, z_index: int) -> None:
        """Set the z-index of the object.

        Args:
            z_index (int):
                The new z-index of the object.
        """
        self._z_index = z_index
        self._should_refresh = True

    @visible.setter
    def visible(self, visible: bool) -> None:
        """Set whether the object is visible.

        Args:
            visible (bool):
                Whether the object is visible.
        """
        self._visible = visible
        self._should_refresh = True

    @should_refresh.setter
    def should_refresh(self, value) -> None:
        """Set the object to not need refreshing.

        Args:
            value (bool):
                Whether the object should be refreshed.
        """
        self._should_refresh = value

    def __str__(self) -> str:
        return f"{self._name} at {self._coordinates} with _size {self._size} and z-index {self._z_index}."

    def __repr__(self) -> str:
        return f"{self._name} at {self._coordinates} with _size {self._size} and z-index {self._z_index}."

    def __eq__(self, other) -> bool:
        return self._coordinates == other.coordinates and self._contents == other.contents

    def __ne__(self, other) -> bool:
        return not self == other

    def __lt__(self, other) -> bool:
        return self._z_index < other.z_index

    def __le__(self, other) -> bool:
        return self._z_index <= other.z_index

    def __gt__(self, other) -> bool:
        return self._z_index > other.z_index

    def __ge__(self, other) -> bool:
        return self._z_index >= other.z_index
