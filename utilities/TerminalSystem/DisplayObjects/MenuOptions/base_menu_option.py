from coordinates import Coordinate
from terminal_tools import to_char_array


class BaseMenuOption:
    """A basic menu option."""

    def __init__(self, name: str, text: str, boundaries: Coordinate,  color_scheme: dict[str, list[str]] | None = None,
                 function: callable | None = None, *args, **kwargs) -> None:
        """Initialize the MenuOption object.

        Args:
            name (str):
                The name of the menu option.
            text (str):
                The text of the menu option.
            boundaries (Coordinate):
                The boundaries of the menu option.
            color_scheme (dict[str, list[str]], optional):
                The color scheme of the menu option.
                Defaults to None.
            function (callable, optional):
                The function called under certain circumstances.
                Defaults to None.
            *args:
                The arguments to hand to the function if and when it's called.
            **kwargs:
                The keyword arguments to hand to the function if and when it's called.
        """
        self._name: str = name
        self._text: str = text
        self._boundaries: Coordinate = boundaries
        self._function: callable = function
        self._color_scheme: dict[str, list[str]] = color_scheme if color_scheme is not None else []
        self._function_args = args
        self._function_kwargs = kwargs
        self._highlighted: bool = False
        self.colors = color_scheme["default"]

        self._display_array = [
            [
                [" ", self._color_scheme["default"]] for _ in range(self._boundaries[1])
            ] for _ in range(self._boundaries[0])
        ]

    def call_function(self) -> None:
        """Call the function of the menu option."""
        if self._function is not None:
            self._function(*self._function_args, **self._function_kwargs)

    # def highlight(self) -> None:
    #     self._color_scheme = self._color_scheme["highlighted"]

    def assemble_display(self) -> None:
        """Assemble the display array."""
        self._display_array = [
            [
                [" ", self._color_scheme["default"]] for _ in range(self._boundaries[1])
            ] for _ in range(self._boundaries[0])
        ]
        for y, row in enumerate(to_char_array(self._text, (self._boundaries[0], self._boundaries[1]))):
            for x, char in enumerate(row):
                self._display_array[y][x] = [char, self._color_scheme["default"]]


    @property
    def name(self) -> str:
        """Return the name of the menu option.

        Returns:
            str: The name of the menu option.
        """
        return self._name

    @property
    def text(self) -> str:
        """Return the text of the menu option.

        Returns:
            str: The text of the menu option.
        """
        return self._text

    @property
    def function(self) -> callable:
        """Return the function of the menu option.

        Returns:
            callable: The function of the menu option.
        """
        return self._function

    @property
    def color_scheme(self) -> dict[str, list[str]]:
        """Return the color scheme of the menu option.

        Returns:
            dict[str, list[str]]: The color scheme of the menu option.
        """
        return self._color_scheme

    @property
    def boundaries(self) -> Coordinate:
        """Return the boundaries of the menu option.

        Returns:
            Coordinate: The boundaries of the menu option.
        """
        return self._boundaries

    @property
    def display_array(self) -> list[list[list[str | list[str]]]]:
        """Return the display array.

        Returns:
            list[list[list[str | list[str]]]]: The display array.
        """
        return self._display_array

    @property
    def highlighted(self) -> bool:
        """Return whether the menu option is highlighted.

        Returns:
            bool: True if the menu option is highlighted, False otherwise.
        """
        return self._highlighted

    @name.setter
    def name(self, new_name: str) -> None:
        """Set the name of the menu option.

        Args:
            new_name (str):
                The new name of the menu option.
        """
        self._name = new_name

    @text.setter
    def text(self, new_text: str) -> None:
        """Set the text of the menu option.

        Args:
            new_text (str):
                The new text of the menu option.
        """
        self._text = new_text

    @function.setter
    def function(self, new_function: callable) -> None:
        """Set the function of the menu option.

        Args:
            new_function (callable):
                The new function of the menu option.
        """
        self._function = new_function

    @color_scheme.setter
    def color_scheme(self, new_color_scheme: dict[str, list[str]]) -> None:
        """Set the color scheme of the menu option.

        Args:
            new_color_scheme (dict[str, list[str]]):
                The new color scheme of the menu option.
        """
        self._color_scheme = new_color_scheme

    @boundaries.setter
    def boundaries(self, new_boundaries: Coordinate) -> None:
        """Set the boundaries of the menu option.

        Args:
            new_boundaries (Coordinate):
                The new boundaries of the menu option.
        """
        self._boundaries = new_boundaries

    @highlighted.setter
    def highlighted(self, new_highlighted: bool) -> None:
        """Set whether the menu option is highlighted.

        Args:
            new_highlighted (bool):
                True if the menu option is highlighted, False otherwise.
        """
        self._highlighted = new_highlighted
