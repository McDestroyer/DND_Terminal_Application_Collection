from copy import deepcopy

from base_terminal_object import PrintableObject
from coordinates import Coordinate


class BorderedBox(PrintableObject):
    """A generic box object."""

    def __init__(self, name: str, coordinates: Coordinate, size: Coordinate, minimum_size: Coordinate | None = None,
                 description: str | None = None, contents: list[list[list[str, list[str]]]] | None = None,
                 z_index: int = 0, title: str | None = None, title_mods: list[str] = None,
                 border_color: list[str] | None = None, border_material: str | None = "██",
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
                The contents of the object in terminal display format. Mostly ignored during initialization.
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
            border_color (list[str], optional):
                The color_scheme of the border.
                Defaults to None.
            border_material (str, optional):
                The material of the border.
                Defaults to "██".
            padding (tuple[int, int], optional):
                The padding of the box.
                Defaults to (1, 2). (y, x)
        """
        super().__init__(name, coordinates, size, minimum_size, description, contents, z_index)
        self._title = title
        self._border_material = border_material

        # Set the defaults.

        if border_color is None:
            self._border_color = []
        else:
            self._border_color = deepcopy(border_color)

        if title_mods is None:
            self._title_mods = deepcopy(self._border_color)
        else:
            self._title_mods = deepcopy(title_mods)

        if padding is None:
            self._padding = (1, 2)
        else:
            self._padding = deepcopy(padding)

        # Apply the border.
        self.apply_border()

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
    def border_color(self) -> list[str]:
        return self._border_color

    @property
    def title_mods(self) -> list[str]:
        return self._title_mods

    @property
    def padding(self) -> tuple[int, int]:
        return self._padding

    @property
    def size(self) -> Coordinate:
        return self._size

    @title.setter
    def title(self, new_title: str) -> None:
        self._title = new_title
        self.apply_border()

    @border_material.setter
    def border_material(self, new_border_material: str) -> None:
        self._border_material = new_border_material
        self.apply_border()

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

    @size.setter
    def size(self, new_size: Coordinate) -> None:
        self._size = new_size

        self._contents = [[[" ", []] for _ in range(self._size[1])] for _ in range(self._size[0])]

        self.apply_border()
