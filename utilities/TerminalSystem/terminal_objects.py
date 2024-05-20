from enum import Enum
from copy import deepcopy
import color
from terminal_tools import to_char_array, apply_color_scheme


class TerminalObject:
    """A generic terminal object."""
    def __init__(self, name: str, description: str | None = None,
                 contents: list[list[list[str | list[str]]]] | None = None, coordinates: tuple[int, int] = (0, 0),
                 size: tuple[int, int] = (5, 10), z_index: int = 0, visible: bool = True) -> None:
        """Initialize the TerminalObject object.

        Args:
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
            visible (bool, optional):
                Whether the object is visible.
                Defaults to True.
            """
        self.name = name
        self.description = description
        self.contents = deepcopy(contents)
        self.coordinates = deepcopy(coordinates)
        self.size = deepcopy(size)
        self.z_index = z_index
        self.visible = visible
        self.should_refresh = True

        if self.contents is None:
            self.contents = [[["#", []] for _ in range(self.size[1])] for _ in range(self.size[0])]

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

    def get_visible(self) -> bool:
        """Return whether the object is visible.

        Returns:
            bool: Whether the object is visible.
        """
        return self.visible

    def should_refresh(self) -> bool:
        """Return whether the object should be refreshed.

        Returns:
            bool: True if the object should be refreshed.
        """
        return self.should_refresh

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
        self.should_refresh = True

    def set_coordinates(self, coordinates: tuple[int, int]) -> None:
        """Set the coordinates of the object.

        Args:
            coordinates (tuple[int, int]):
                The new coordinates of the object.
        """
        self.coordinates = coordinates
        self.should_refresh = True

    def set_size(self, size: tuple[int, int]) -> None:
        """Set the size of the object.

        Args:
            size (tuple[int, int]):
                The new size of the object.
        """
        self.size = size
        self.should_refresh = True

    def set_z_index(self, z_index: int) -> None:
        """Set the z-index of the object.

        Args:
            z_index (int):
                The new z-index of the object.
        """
        self.z_index = z_index
        self.should_refresh = True

    def set_visible(self, visible: bool) -> None:
        """Set whether the object is visible.

        Args:
            visible (bool):
                Whether the object is visible.
        """
        self.visible = visible
        self.should_refresh = True

    def refreshed(self) -> None:
        """Set the object to not need refreshing."""
        self.should_refresh = False

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
                 coordinates: tuple[int, int], size: tuple[int, int], z_index: int = 0, title: str | None = None,
                 title_mods: list[str] = None, color_scheme: list[str] | None = None,
                 border_color: list[str] | None = None, border_material: str | None = "██", text: str | None = None,
                 padding: tuple[int, int] | None = None) -> None:
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
            title (str, optional):
                The title of the box. If not None, the box will have a title in the top side of the border (if it fits).
                Defaults to None.
            title_mods (list[str], optional):
                The color scheme of the title.
                Defaults to [].
            color_scheme (list[str], optional):
                The color_scheme of the box.
                Defaults to None.
            border_color (list[str], optional):
                The color_scheme of the border.
                Defaults to None.
            border_material (str, optional):
                The material of the border.
                Defaults to "██".
            text (str, optional):
                The text to display in the box.
                Defaults to None.
            padding (tuple[int, int], optional):
                The padding of the box.
                Defaults to (1, 1). (y, x)
        """
        super().__init__(name, description, contents, coordinates, size, z_index)
        self.name = name
        self.description = description
        self.coordinates = deepcopy(coordinates)
        self.size = deepcopy(size)
        self.z_index = z_index
        self.title = title
        self.border_material = border_material
        self.text = text
        self.should_refresh = True

        # Set the defaults.
        if color_scheme is None:
            self.color_scheme = [color.BACKGROUND_BLACK]
        else:
            self.color_scheme = deepcopy(color_scheme)

        if border_color is None:
            self.border_color = []
        else:
            self.border_color = deepcopy(border_color)

        if title_mods is None:
            self.title_mods = deepcopy(self.border_color)
        else:
            self.title_mods = deepcopy(title_mods)

        if padding is None:
            self.padding = (1, 1)
        else:
            self.padding = deepcopy(padding)

        if contents is None:
            self.contents = [[[" ", [color.BACKGROUND_BLACK]] for _ in range(self.size[1])] for _ in range(self.size[0])]
        else:
            self.contents = deepcopy(contents)

        # Apply the border.
        # if border_material is not None:
        #     self.contents[0], self.contents[-1] = [[border_material[0], border_color] for _ in range(self.size[1])]
        #     for i in range(1, self.size[0] - 1):
        #         self.contents[i][0] = [border_material[1], border_color]
        #         self.contents[i][-1] = [border_material[1], border_color]
        self.apply_border()

        # Fill in the rest of the box.
        # If there is no text, make it blank.
        if text is None:
            text = ""
        self.set_text(text)

    def set_text(self, text: str) -> None:
        """Set the text of the box.

        Args:
            text (str):
                The text to display in the box.
        """
        self.text = text

        # Calculate the offset needed to place the text so that it doesn't overlap with the borders.
        row_offset = 0
        col_offset = 0

        if self.border_material is not None:
            row_offset = 1 + self.padding[0]
            col_offset = len(self.border_material) + self.padding[1]

        # Set the text area to be blank.
        # self.contents = [[
        #     ["#", []] for _ in range(col_offset, self.size[1] - col_offset)
        # ] for _ in range(row_offset, self.size[0] - row_offset)]
        for y in range(row_offset-1, self.size[0] - row_offset):
            for x in range(col_offset, self.size[1] - col_offset):
                self.contents[y][x] = [" ", [color.BACKGROUND_BLACK]]

        # Format the text.
        grid_text = to_char_array(self.text, (self.size[0] - 2*row_offset, self.size[1] - 2*col_offset))
        grid_text = apply_color_scheme(self.color_scheme, grid_text)

        # Apply the text to the box.
        for y in range(len(grid_text)):
            for x in range(len(grid_text[y])):
                self.contents[y + row_offset][x + col_offset] = deepcopy(grid_text[y][x])

        self.should_refresh = True

    def get_text(self) -> str:
        """Return the text of the box.

        Returns:
            str: The text of the box.
        """
        return self.text

    def apply_border(self) -> None:
        """Apply the border to the box."""
        if self.border_material is not None:
            # Top and bottom borders.
            self.contents[0] = deepcopy([[self.border_material[0], self.border_color] for _ in range(self.size[1])])
            self.contents[-1] = deepcopy(self.contents[0])
            # Left and right borders.
            for i in range(1, self.size[0] - 1):
                for j in range(len(self.border_material)):
                    self.contents[i][0+j] = deepcopy([self.border_material[0+j], self.border_color])
                    self.contents[i][-1-j] = deepcopy([self.border_material[-1-j], self.border_color])

            if self.title is not None:
                if len(self.title) > self.size[1] - 2:
                    self.title = self.title[:self.size[1] - 5] + "..."

                # Calculate the offset needed to center the title.
                offset = (self.size[1] - len(self.title)) // 2

                for i, letter in enumerate(self.title):
                    self.contents[0][i + offset] = [letter, deepcopy(self.title_mods)]


class Objects(Enum):
    TERMINAL_OBJECT = TerminalObject
    BOX = Box
