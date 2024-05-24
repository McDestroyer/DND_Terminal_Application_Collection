class Unit:
    """A unit of measurement for the terminal _display. Used to convert between different units of measurement
    internally. This exists to allow for the use of different units of measurement in the same program and to allow for
    easy addition of new units of measurement.

    Attributes:
        name (str):
            The name of the unit.
        to_char_func (callable):
            A function that converts a value to a number of characters.
        from_char_func (callable):
            A function that converts a number of characters to a value.
    """
    def __init__(self, name: str, to_char: callable, from_char: callable) -> None:
        self.name = name
        self.to_char_func = to_char
        self.from_char_func = from_char

    def to_char(self, value: float, screen_size: tuple[int, int], axis: int) -> int:
        """Convert a value to char format from whatever it was before.

        Args:
            value:
                The value to convert.
            screen_size (tuple[int, int]):
                The size of the screen.
            axis (int):
                The axis to convert.
        """
        return int(self.to_char_func(value, screen_size, axis))

    def from_char(self, value: float, screen_size: tuple[int, int], axis: int) -> int:
        """Convert a value from char format to whatever it was before.

        Args:
            value:
                The value to convert.
            screen_size (tuple[int, int]):
                The size of the screen.
            axis (int):
                The axis to convert.
        """
        return self.from_char_func(value, screen_size, axis)


# Put all unit functions here.


# CHAR


def char_to_char(value: float, screen_size: tuple[int, int], axis: int) -> float:
    """Convert a value to char format from whatever it was before.

    Args:
        value:
            The value to convert.
        screen_size (tuple[int, int]):
            The size of the screen.
        axis (int):
            The axis to convert.
    """
    return value


def char_from_char(value: float, screen_size: tuple[int, int], axis: int) -> float:
    """Convert a value from char format to whatever it was before.

    Args:
        value:
            The value to convert.
        screen_size (tuple[int, int]):
            The size of the screen.
        axis (int):
            The axis to convert.

    Returns:
        float: The value in characters.
    """
    return value


# PERCENT


def percent_to_char(value: float, screen_size: tuple[int, int], axis: int) -> int:
    """Convert a value to char format from whatever it was before.

    Args:
        value:
            The value to convert.
        screen_size (tuple[int, int]):
            The size of the screen.
        axis (int):
            The axis to convert.

    Returns:
        int: The value in characters.
    """
    return int(value / 100 * screen_size[axis])


def percent_from_char(value: float, screen_size: tuple[int, int], axis: int) -> float:
    """Convert a value from char format to whatever it was before.

    Args:
        value:
            The value to convert.
        screen_size (tuple[int, int]):
            The size of the screen.
        axis (int):
            The axis to convert.
    """
    return 100 * value / screen_size[axis]




class Units:
    """The units of the terminal display.

    Attributes:
        CHAR (callable):
            The numbers given with this refer to distance as a number of characters. Note that a characters dimensions
            are roughly 2:1.
        PERCENT (callable):
            The numbers given with this refer to distance as a percentage of the screen's size.
            Whether horizontal or vertical is determined by context.
    """
    # DOUBLED_CHAR (callable):
    #     The numbers given with this refer to distance as a number of pairs of characters. Note that a doubled
    #     characters dimensions are roughly 1:1. Similar to CHAR, but with a different aspect ratio.
    # HORIZONTAL_PERCENT (callable):
    #     The numbers given with this refer to distance as a percentage of the screen's width. Similar to PERCENT,
    #     but specifically for horizontal distance regardless of context.
    # VERTICAL_PERCENT (callable):
    #     The numbers given with this refer to distance as a percentage of the screen's height. Similar to PERCENT,
    #     but specifically for vertical distance regardless of context.

    CHAR: Unit = Unit(
        name="CHAR",
        to_char=char_to_char,
        from_char=char_from_char,
    )
    PERCENT: Unit = Unit(
        name="PERCENT",
        to_char=percent_to_char,
        from_char=percent_from_char,
    )
