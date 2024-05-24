from units import Units, Unit


class Coordinate:

    def __init__(self, screen_size: tuple[int, int], value_y: float, value_x: float,
                 unit_y: Unit = Units.CHAR, unit_x: Unit = Units.CHAR) -> None:
        """Initialize the Coordinate object.

        Args:
            screen_size (tuple[int, int]):
                The _size of the screen.
            value_y (float):
                The value of the y-coordinate.
            value_x (float):
                The value of the x-coordinate.
            unit_y (Unit, optional):
                The unit of the y-coordinate.
                Defaults to Units.CHAR.
            unit_x (Unit, optional):
                The unit of the x-coordinate.
                Defaults to Units.CHAR.
        """
        self._screen_size = screen_size

        # Get the values in character form.
        self._given_value_y = value_y
        self._given_value_x = value_x
        self._char_value_y = unit_y.to_char(value_y, screen_size, 0)
        self._char_value_x = unit_x.to_char(value_x, screen_size, 1)
        self._unit_y = unit_y
        self._unit_x = unit_x

        # Convert the values to all units and store them.
        self._values = {
            unit_y.name: [value_y, unit_y.from_char(self._char_value_x, screen_size, 0)],
        }
        if unit_x != unit_y:
            self._values[unit_x.name] = [unit_x.from_char(self._char_value_y, screen_size, 1), value_x]

        self._update_values()

    def _update_values(self) -> None:
        """Update the values of the coordinate."""
        for unit in Units.__dict__.keys():
            if unit.startswith("__"):
                continue
            if unit not in self._values:
                self._values[unit] = [
                    Units.__dict__[unit].from_char(self._char_value_y, self._screen_size, 0),
                    Units.__dict__[unit].from_char(self._char_value_x, self._screen_size, 1)
                ]

    def add_with_unit(self, coord: 'Coordinate', unit: Unit) -> 'Coordinate':
        """Add coordinate and this one together using the given coordinate type and returns the new value.

        Args:
            coord (Coordinate):
                The coordinate to add to this one.
            unit (Unit):
                The unit to add.
        """
        y_vals = self._values[unit.name][0] + coord._values[unit.name][0]
        x_vals = self._values[unit.name][1] + coord._values[unit.name][1]

        return Coordinate(
            self._screen_size,
            y_vals,
            x_vals,
            unit,
            unit
        )

    @property
    def values(self) -> dict[str, list[float]]:
        """Return the values of the coordinate.

        Returns:
            dict[str, list[float]]: The values of the coordinate.
        """
        return self._values

    @property
    def char_value_y(self) -> float:
        """Return the y-coordinate in characters.

        Returns:
            float: The y-coordinate in characters.
        """
        return self._char_value_y

    @char_value_y.setter
    def char_value_y(self, value: float) -> None:
        """Set the y-coordinate in characters.

        Args:
            value (float):
                The y-coordinate in characters.
        """
        self._char_value_y = value
        self._update_values()

    @property
    def char_value_x(self) -> float:
        """Return the x-coordinate in characters.

        Returns:
            float: The x-coordinate in characters.
        """
        return self._char_value_x

    @char_value_x.setter
    def char_value_x(self, value: float) -> None:
        """Set the x-coordinate in characters.

        Args:
            value (float):
                The x-coordinate in characters.
        """
        self._char_value_x = value
        self._update_values()

    @property
    def unit_y(self) -> Unit:
        """Return the y-coordinate unit.

        Returns:
            Unit: The y-coordinate unit.
        """
        return self._unit_y

    @unit_y.setter
    def unit_y(self, unit: Unit) -> None:
        """Set the y-coordinate unit.

        Args:
            unit (Unit):
                The y-coordinate unit.
        """
        self._unit_y = unit

    @property
    def unit_x(self) -> Unit:
        """Return the x-coordinate unit.

        Returns:
            Unit: The x-coordinate unit.
        """
        return self._unit_x

    @unit_x.setter
    def unit_x(self, unit: Unit) -> None:
        """Set the x-coordinate unit.

        Args:
            unit (Unit):
                The x-coordinate unit.
        """
        self._unit_x = unit

    @property
    def screen_size(self) -> tuple[int, int]:
        """Return the size of the screen.

        Returns:
            tuple[int, int]: The size of the screen.
        """
        return self._screen_size

    @screen_size.setter
    def screen_size(self, size: tuple[int, int]) -> None:
        """Set the size of the screen.

        Args:
            size (tuple[int, int]):
                The size of the screen.
        """
        self._screen_size = size
        self._char_value_y = self._unit_y.to_char(self._given_value_y, self._screen_size, 0)
        self._char_value_x = self._unit_x.to_char(self._given_value_x, self._screen_size, 1)
        self._update_values()

    def __str__(self):
        return f"Coordinates: ({self.values['CHAR'][0]}, {self.values['CHAR'][1]})"

    def __repr__(self):
        return f"Coordinates: ({self.values['CHAR'][0]}, {self.values['CHAR'][1]})"

    def __getitem__(self, item):
        return self.values["CHAR"][item]

    def __setitem__(self, key, value):
        # self.values["CHAR"][key] = value
        if key == 0:
            self._char_value_y = value[0]
        elif key == 1:
            self._char_value_x = value[1]
        else:
            raise (IndexError("Index out of range."))
        self._update_values()

    # def __delitem__(self, key):
    #     # del self.values["CHAR"][key]
    #     if key == 0:
    #         self.char_value_y = value[0]
    #     elif key == 1:
    #         self.char_value_x = value[1]
    #     else:
    #         raise (IndexError("Index out of range."))
    #     self._update_values()

    def __len__(self):
        return len(self.values)

    def __iter__(self):
        return iter(self.values)

    def __contains__(self, item):
        return item in self.values

    def __eq__(self, other):
        return self.values["CHAR"] == other.values["CHAR"]

    def __ne__(self, other):
        return not self == other

    # def __lt__(self, other):
    #     return self.values["CHAR"] < other.values["CHAR"]
    #
    # def __le__(self, other):
    #     return self.values["CHAR"] <= other.values["CHAR"]
    #
    # def __gt__(self, other):
    #     return self.values["CHAR"] > other.values["CHAR"]
    #
    # def __ge__(self, other):
    #     return self.values["CHAR"] >= other.values["CHAR"]

    def __add__(self, other):
        return Coordinate(
            self._screen_size,
            self._unit_y.from_char(self._char_value_y + other._char_value_y, self._screen_size, 0),
            self._unit_x.from_char(self._char_value_x + other._char_value_x, self._screen_size, 1),
            self._unit_y,
            self._unit_x
        )

    def __sub__(self, other):
        return Coordinate(
            self._screen_size,
            self._unit_y.from_char(self._char_value_y - other._char_value_y, self._screen_size, 0),
            self._unit_x.from_char(self._char_value_x - other._char_value_x, self._screen_size, 1),
            self._unit_y,
            self._unit_x
        )

    def __mul__(self, other):
        return Coordinate(
            self._screen_size,
            self._unit_y.from_char(self._char_value_y * other.char_value_y, self._screen_size, 0),
            self._unit_x.from_char(self._char_value_x * other.char_value_x, self._screen_size, 1),
            self._unit_y,
            self._unit_x
        )

    def __truediv__(self, other):
        return Coordinate(
            self._screen_size,
            self._unit_y.from_char(self._char_value_y / other.char_value_y, self._screen_size, 0),
            self._unit_x.from_char(self._char_value_x / other.char_value_x, self._screen_size, 1),
            self._unit_y,
            self._unit_x
        )

    def __floordiv__(self, other):
        raise NotImplementedError("Floor division of _coordinates is not supported.")

    def __mod__(self, other):
        raise NotImplementedError("Modulo of _coordinates is not supported.")

    def __divmod__(self, other):
        raise NotImplementedError("Division and modulo of _coordinates is not supported.")

    def __pow__(self, other):
        raise NotImplementedError("Exponentiation of _coordinates is not supported.")

    def __lshift__(self, other):
        raise NotImplementedError("Left shift of _coordinates is not supported.")

    def __rshift__(self, other):
        raise NotImplementedError("Right shift of _coordinates is not supported.")

    def __and__(self, other):
        raise NotImplementedError("Bitwise AND of _coordinates is not supported.")

    def __xor__(self, other):
        raise NotImplementedError("Bitwise XOR of _coordinates is not supported.")

    def __or__(self, other):
        raise NotImplementedError("Bitwise OR of _coordinates is not supported.")

    def __neg__(self):
        return Coordinate(
            self._screen_size,
            -self._unit_y.from_char(self._char_value_y, self._screen_size, 0),
            -self._unit_x.from_char(self._char_value_x, self._screen_size, 1),
            self._unit_y,
            self._unit_x
        )

    def __pos__(self):
        return Coordinate(
            self._screen_size,
            self._unit_y.from_char(self._char_value_y, self._screen_size, 0),
            self._unit_x.from_char(self._char_value_x, self._screen_size, 1),
            self._unit_y,
            self._unit_x
        )

    def __abs__(self):
        return Coordinate(
            self._screen_size,
            abs(self._unit_y.from_char(self._char_value_y, self._screen_size, 0)),
            abs(self._unit_x.from_char(self._char_value_x, self._screen_size, 1)),
            self._unit_y,
            self._unit_x
        )

    def __invert__(self):
        raise NotImplementedError("Bitwise NOT of _coordinates is not supported.")

    def __complex__(self):
        raise NotImplementedError("Complex conversion of _coordinates is not supported.")

    def __int__(self):
        raise NotImplementedError("Integer conversion of _coordinates is not supported.")

    def __float__(self):
        raise NotImplementedError("Float conversion of _coordinates is not supported.")

    def __round__(self, n=None):
        raise NotImplementedError("Rounding of _coordinates is not supported.")

    def __floor__(self):
        raise NotImplementedError("Floor of _coordinates is not supported.")

    def __ceil__(self):
        raise NotImplementedError("Ceiling of _coordinates is not supported.")

    def __trunc__(self):
        raise NotImplementedError("Truncation of _coordinates is not supported.")

    def __iadd__(self, other):
        self._char_value_y += other._char_value_y
        self._char_value_x += other._char_value_x
        self._update_values()
        return self

    def __isub__(self, other):
        self._char_value_y -= other._char_value_y
        self._char_value_x -= other._char_value_x
        self._update_values()
        return self

    def __imul__(self, other):
        raise NotImplementedError("Multiplication of _coordinates is not supported.")

    def __itruediv__(self, other):
        raise NotImplementedError("Division of _coordinates is not supported.")

    def __ifloordiv__(self, other):
        raise NotImplementedError("Floor division of _coordinates is not supported.")

    def __imod__(self, other):
        raise NotImplementedError("Modulo of _coordinates is not supported.")

    def __ipow__(self, other):
        raise NotImplementedError("Exponentiation of _coordinates is not supported.")

    def __ilshift__(self, other):
        raise NotImplementedError("Left shift of _coordinates is not supported.")

    def __irshift__(self, other):
        raise NotImplementedError("Right shift of _coordinates is not supported.")

    def __iand__(self, other):
        raise NotImplementedError("Bitwise AND of _coordinates is not supported.")

    def __ixor__(self, other):
        raise NotImplementedError("Bitwise XOR of _coordinates is not supported.")

    def __ior__(self, other):
        raise NotImplementedError("Bitwise OR of _coordinates is not supported.")

    def __index__(self):
        raise NotImplementedError("Index conversion of _coordinates is not supported.")

    # @property
    # def char_x(self):
    #     """I'm the 'x' property."""
    #     return self._char_value_x
    #
    # @char_x.setter
    # def char_x(self, value):
    #     self._char_value_x = value
    #
    # @char_x.deleter
    # def char_x(self):
    #     del self._char_value_x


# if __name__ == "__main__":
#     print(Units.__dict__.keys())
#     # quit()
#     for unit in Units.__dict__.keys():
#         if unit.startswith("__"):
#             continue
#         print(
#             unit, "\n"*5,
#             type(unit), "\n"*5,
#             Units.__dict__[unit], "\n"*5,
#             type(Units.__dict__[unit]))
#         print(f"Type Conversion ({unit}):", Units.__dict__[unit].from_char(50, (75, 75), 0))
#         # Units.__dict__[unit].from_char(50, (100, 100), 1)
#     coord1 = Coordinate((10, 10), 1, 1)
#     coord2 = Coordinate((10, 10), 2, 2)
#
#     print(coord1 + coord2)
#     assert coord1 + coord2 == Coordinate((10, 10), 3, 3)
#     print(coord1 - coord2)
#     assert coord1 - coord2 == Coordinate((10, 10), -1, -1)
#     print(coord1 == coord2)
#     assert not (coord1 == coord2)
#     print(coord1 != coord2)
#     assert coord1 != coord2
#     print(coord1.values)
#     print(coord2.values)
#     print(coord1)
#     print(coord2)
