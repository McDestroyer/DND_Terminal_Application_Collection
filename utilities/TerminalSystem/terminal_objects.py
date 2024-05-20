class TerminalObject:
    def __init__(self, display_object, name: str, description: str | None = None,
                 contents: list[list[list[str | list[str]]]] | None = None, coordinates: tuple[int, int] = (0, 0),
                 size: tuple[int, int] = (5, 10), z_index: int = 0) -> None:
        """Initialize the TerminalObject object.

        Args:
            display_object (Display):
                The display object to add the object to when printing.
            name (str):
                The name of the object.
            description (str, optional):
                The description of the object.
                Defaults to None.
            contents (list[list[list[str | list[str]]], optional):
                The contents of the object in terminal display format.
                Defaults to a list of empty characters.
            coordinates (tuple[int, int]):
                The coordinates of the object (y, x).
                Defaults to (0, 0).
            size (tuple[int, int], optional):
                The size of the object (y, x).
                Defaults to (5, 10).
            z_index (int, optional):
                The z-index of the object.
                Defaults to 0.

            """
        self.name = name
        self.description = description
        self.contents = contents
        self.coordinates = coordinates
        self.size = size
        self.z_index = z_index

        if contents is None:
            self.contents = [ [ ["", []] for _ in range(self.size[1])] for _ in range(self.size[0])]

    def get_name(self) -> str:
        """Return the name of the object.

        Returns:
            str: The name of the object.
        """
        return self.name

    def get_description(self) -> str | None:
        """Return the description of the object.

        Returns:
            str | None: The description of the object.
        """
        return self.description

    def get_contents(self) -> list[list[list[str | list[str]]]]:
        """Return the contents of the object.

        Returns:
            list[list[list[str | list[str]]]]: The contents of the object.
        """
        return self.contents

    def get_coordinates(self) -> tuple[int, int]:
        """Return the coordinates of the object.

        Returns:
            tuple[int, int]: The coordinates of the object.
        """
        return self.coordinates

    def get_size(self) -> tuple[int, int]:
        """Return the size of the object.

        Returns:
            tuple[int, int]: The size of the object.
        """
        return self.size

    def get_z_index(self) -> int:
        """Return the z-index of the object.

        Returns:
            int: The z-index of the object.
        """
        return self.z_index

    def set_name(self, name: str) -> None:
        """Set the name of the object.

        Args:
            name (str):
                The new name of the object.
        """
        self.name = name

    def set_description(self, description: str | None) -> None:
        """Set the description of the object.

        Args:
            description (str | None):
                The new description of the object.
        """
        self.description = description

    def set_contents(self, contents: list[list[list[str | list[str]]]]) -> None:
        """Set the contents of the object.

        Args:
            contents (list[list[list[str | list[str]]]):
                The new contents of the object.
        """
        self.contents = contents

    def set_coordinates(self, coordinates: tuple[int, int]) -> None:
        """Set the coordinates of the object.

        Args:
            coordinates (tuple[int, int]):
                The new coordinates of the object.
        """
        self.coordinates = coordinates

    def set_size(self, size: tuple[int, int]) -> None:
        """Set the size of the object.

        Args:
            size (tuple[int, int]):
                The new size of the object.
        """
        self.size = size

    def set_z_index(self, z_index: int) -> None:
        """Set the z-index of the object.

        Args:
            z_index (int):
                The new z-index of the object.
        """
        self.z_index = z_index

    def add_to_display(self, display: list[list[list[str | list[str]]]]) -> None:
        """Add the object to a display.

        Args:
            display (list[list[list[str | list[str]]]):
                The display to add the object to.
        """
        for y in range(self.size[0]):
            for x in range(self.size[1]):
                display[self.coordinates[0] + y][self.coordinates[1] + x] = self.contents[y][x]

    def __str__(self) -> str:
        return f"{self.name} at {self.coordinates} with size {self.size} and z-index {self.z_index}."

    def __repr__(self) -> str:
        return f"{self.name} at {self.coordinates} with size {self.size} and z-index {self.z_index}."

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.coordinates == other.coordinates and self.size == other.size and self.z_index == other.z_index

    def __ne__(self, other) -> bool:
        return not self == other

    def __lt__(self, other) -> bool:
        return self.z_index < other.z_index

    def __le__(self, other) -> bool:
        return self.z_index <= other.z_index

    def __gt__(self, other) -> bool:
        return self.z_index > other.z_index

    def __ge__(self, other) -> bool:
        return self.z_index >= other.z_index


class Box(TerminalObject):
    """A generic box object."""

    def __init__(self, name: str, description: str | None, contents: list[list[list[str, list[str]]]] | None,
                 coordinates: tuple[int, int], size: tuple[int, int], z_index: int = 0, color: list[str] | None = None,
                 border_color: list[str] | None = None, border_material: str | None = "██") -> None:
        """Initialize the Box object.

        Args:
            name (str):
                The name of the box.
            description (str, optional):
                The description of the box.
                Defaults to None.
            contents (list[list[list[str, list[str]]], optional):
                The contents of the object in terminal display format.
                Defaults to a list of empty characters.
            coordinates (tuple[int, int]):
                The coordinates of the box (y, x).
            size (tuple[int, int]):
                The size of the box (y, x).
            z_index (int, optional):
                The z-index of the box.
                Defaults to 0.
            color (list[str], optional):
                The color of the box.
                Defaults to None.
            border_color (list[str], optional):
                The color of the border.
                Defaults to None.
            border_material (str, optional):
                The material of the border.
                Defaults to "██".
        """
        super().__init__(name, description, contents, coordinates, size, z_index)
        self.name = name
        self.description = description
        self.coordinates = coordinates
        self.size = size
        self.z_index = z_index
        self.color = color
        self.border_color = border_color
        self.border_material = border_material