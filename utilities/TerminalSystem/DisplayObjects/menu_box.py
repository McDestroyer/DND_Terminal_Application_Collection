from copy import deepcopy

import color

from terminal_tools import to_char_array, apply_color_scheme
from bordered_box import BorderedBox
from base_menu_option import BaseMenuOption
from coordinates import Coordinate


class MenuBox(BorderedBox):
    """A menu box object."""

    def __init__(self, name: str, coordinates: Coordinate, size: Coordinate, minimum_size: Coordinate | None = None,
                 description: str | None = None, contents: list[list[list[str, list[str]]]] | None = None,
                 z_index: int = 0, title: str | None = None, title_mods: list[str] = None,
                 color_scheme: dict[str, list[str]] | None = None, border_color: list[str] | None = None,
                 border_material: str | None = "██", menu_options: list[BaseMenuOption] | None = None,
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
            color_scheme (dict[str, list[str]], optional):
                The color_scheme of the internals of the box.
                Defaults to None.
            border_color (list[str], optional):
                The color_scheme of the border.
                Defaults to None.
            border_material (str, optional):
                The material of the border.
                Defaults to "██".
            menu_options (list[BaseMenuOption], optional):
                The options to display in the menu box.
                Defaults to None.
            padding (tuple[int, int], optional):
                The padding of the box.
                Defaults to (1, 2). (y, x)
        """
        super().__init__(name, coordinates, size, minimum_size, description, contents, z_index, title, title_mods,
                         border_color, border_material, padding)

        # Set the defaults.

        if menu_options is None:
            self._menu_options = []
        else:
            self._menu_options = deepcopy(menu_options)

        if color_scheme is None:
            self._color_scheme = [color.BACKGROUND_DEFAULT_COLOR]
        else:
            self._color_scheme = deepcopy(color_scheme)

    def add_menu_option(self, new_menu_option: BaseMenuOption) -> None:
        """Add a menu option to the box.

        Args:
            new_menu_option (BaseMenuOption):
                The menu option to add to the box.
        """
        self._menu_options.append(new_menu_option)

    def remove_menu_option(self, menu_option_name: str) -> None:
        """Remove a menu option from the box.

        Args:
            menu_option_name (str):
                The name of the menu option to remove.
        """
        for menu_option in self._menu_options:
            if menu_option.name == menu_option_name:
                self._menu_options.remove(menu_option)
                break

    def clear_menu_options(self) -> None:
        """Clear all menu options from the box."""
        self._menu_options = []

    def display_menu_options(self) -> None:
        """Display the menu options in the box."""
        for menu_option in self._menu_options:
            menu_option.display()

    @property
    def menu_options(self) -> list[BaseMenuOption] | None:
        return self._menu_options

    @property
    def color_scheme(self) -> dict[str, list[str]]:
        """Return the color scheme of the box.

        Returns:
            dict[str, list[str]]: The color scheme of the box.
        """
        return self._color_scheme

    @menu_options.setter
    def menu_options(self, new_menu_options: list[BaseMenuOption]) -> None:
        """Set the menu options of the box.

        Args:
            new_menu_options (list[BaseMenuOption):
                The new menu options to display in the box.
        """
        self._menu_options = new_menu_options

        # Calculate the offset needed to place the text so that it doesn't overlap with the borders.
        y_offset = 0
        x_offset = 0

        if self._border_material is not None:
            y_offset = 1 + self._padding[0]
            x_offset = len(self._border_material) + self._padding[1]

        # Set the text area to be blank.
        for y in range(y_offset, self._size[0] - y_offset):
            for x in range(x_offset, self._size[1] - x_offset):
                self.contents[y][x] = [" ", [color.BACKGROUND_DEFAULT_COLOR]]

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

    @property
    def mouse_over(self) -> bool | tuple[int, int]:
        """Return whether the mouse is over the box.

        Returns:
            bool | tuple[int, int]: Whether the mouse is over the box and where relative to the box.
        """
        return self._mouse_over

    @mouse_over.setter
    def mouse_over(self, new_mouse_over: bool | tuple[int, int]) -> None:
        self._mouse_over = new_mouse_over
        self._should_refresh = True

