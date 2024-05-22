from copy import deepcopy

import color

from terminal_tools import to_char_array, apply_color_scheme
from base_terminal_object import PrintableObject
from coordinates import Coordinate


class TextBox(PrintableObject):
    """A generic box object."""

    def __init__(self, name: str, coordinates: Coordinate, size: Coordinate, minimum_size: Coordinate | None = None,
                 description: str | None = None, contents: list[list[list[str, list[str]]]] | None = None,
                 z_index: int = 0, title: str | None = None, title_mods: list[str] = None,
                 color_scheme: list[str] | None = None, border_color: list[str] | None = None,
                 border_material: str | None = "██", text: str | None = None,
                 padding: tuple[int, int] | None = None) -> None:
        """Initialize the Box object.

        Args:
            name (str):
                The name of the box.
            coordinates (Coordinate):
                The coordinates of the box.
            size (Coordinate):
                The size of the box.
            minimum_size (Coordinate, optional):
                The minimum size of the box. Intended for use when one or both of the axes use percentages.
                Defaults to None.
            description (str, optional):
                The description of the box.
                Defaults to None.
            contents (list[list[list[str, list[str]]], optional):
                The contents of the object in terminal _display format. Mostly ignored during initialization.
                Defaults to a list of empty characters.
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
                The _color_scheme of the box.
                Defaults to None.
            border_color (list[str], optional):
                The _color_scheme of the border.
                Defaults to None.
            border_material (str, optional):
                The material of the border.
                Defaults to "██".
            text (str, optional):
                The text to _display in the box.
                Defaults to None.
            padding (tuple[int, int], optional):
                The padding of the box.
                Defaults to (1, 2). (y, x)
        """
        super().__init__(name, coordinates, size, minimum_size, description, contents, z_index)
        self._title = title
        self._border_material = border_material
        self._text = text

        # Set the defaults.
        if minimum_size is None:
            self._minimum_size = (1, 1)
        else:
            self._minimum_size = minimum_size

        if color_scheme is None:
            self._color_scheme = [color.BACKGROUND_BLACK]
        else:
            self._color_scheme = deepcopy(color_scheme)

        if border_color is None:
            self._border_color = []
        else:
            self._border_color = deepcopy(border_color)

        if title_mods is None:
            self._title_mods = deepcopy(self._border_color)
        else:
            self._title_mods = deepcopy(title_mods)

        if padding is None:
            self._padding = (1, 1)
        else:
            self._padding = deepcopy(padding)

        # Apply the border.
        self.apply_border()

        # Fill in the rest of the box.
        # If there is no text, make it blank.
        if text is None:
            text = ""
        self.text = text

    def apply_border(self) -> None:
        """Apply the border to the box."""
        if self._border_material is not None:
            # Top and bottom borders.
            self.contents[0] = deepcopy([[self._border_material[0], self._border_color] for _ in range(self._size[1])])
            self.contents[-1] = deepcopy(self.contents[0])
            # Left and right borders.
            for i in range(1, self._size[0] - 1):
                for j in range(len(self._border_material)):
                    self.contents[i][0+j] = deepcopy([self._border_material[0 + j], self._border_color])
                    self.contents[i][-1-j] = deepcopy([self._border_material[-1 - j], self._border_color])

            if self._title is not None:
                if len(self._title) > self._size[1] - 2:
                    self._title = self._title[:self._size[1] - 5] + "..."

                # Calculate the offset needed to center the title.
                offset = (self._size[1] - len(self._title)) // 2

                for i, letter in enumerate(self._title):
                    self.contents[0][i + offset] = [letter, deepcopy(self._title_mods)]

            self._should_refresh = True

    @property
    def title(self) -> str | None:
        return self._title

    @property
    def border_material(self) -> str | None:
        return self._border_material

    @property
    def text(self) -> str | None:
        return self._text

    @property
    def color_scheme(self) -> list[str]:
        return self._color_scheme

    @property
    def border_color(self) -> list[str]:
        return self._border_color

    @property
    def title_mods(self) -> list[str]:
        return self._title_mods

    @property
    def padding(self) -> tuple[int, int]:
        return self._padding

    @title.setter
    def title(self, new_title: str) -> None:
        self._title = new_title
        self.apply_border()

    @border_material.setter
    def border_material(self, new_border_material: str) -> None:
        self._border_material = new_border_material
        self.apply_border()

    @text.setter
    def text(self, new_text: str) -> None:
        """Set the text of the box.

        Args:
            new_text (str):
                The text to display in the box.
        """
        self._text = new_text

        # Calculate the offset needed to place the text so that it doesn't overlap with the borders.
        y_offset = 0
        x_offset = 0

        if self._border_material is not None:
            y_offset = 1 + self._padding[0]
            x_offset = len(self._border_material) + self._padding[1]

        # Set the text area to be blank.
        for y in range(y_offset, self._size[0] - y_offset):
            for x in range(x_offset, self._size[1] - x_offset):
                self.contents[y][x] = [" ", [color.BACKGROUND_BLACK]]

        # Format the text.
        grid_text = to_char_array(self._text, (self._size[0] - 2 * y_offset, self._size[1] - 2 * x_offset))
        grid_text = apply_color_scheme(self._color_scheme, grid_text)

        # Apply the text to the box.
        for y in range(len(grid_text)):
            for x in range(len(grid_text[y])):
                self.contents[y + y_offset][x + x_offset] = deepcopy(grid_text[y][x])

        self._should_refresh = True

    @color_scheme.setter
    def color_scheme(self, new_color_scheme: list[str]) -> None:
        self._color_scheme = new_color_scheme
        self.apply_border()
        self.text = self._text

    @border_color.setter
    def border_color(self, new_border_color: list[str]) -> None:
        self._border_color = new_border_color
        self.apply_border()

    @title_mods.setter
    def title_mods(self, new_title_mods: list[str]) -> None:
        self._title_mods = new_title_mods
        self.apply_border()

    @padding.setter
    def padding(self, new_padding: tuple[int, int]) -> None:
        self._padding = new_padding
        self.text = self._text
