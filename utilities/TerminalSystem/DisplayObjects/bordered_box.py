from copy import deepcopy

import color
from base_terminal_object import PrintableObject
from coordinates import Coordinate


class BorderedBox(PrintableObject):
    """A generic box object. Used primarily to build other types of objects rather than being used directly."""

    def __init__(self,
                 # BaseTerminalObject arguments.
                 name: str, coordinates: Coordinate, size: Coordinate, minimum_size: Coordinate | None = None,
                 description: str | None = None, contents: list[list[list[str, list[str]]]] | None = None,
                 z_index: int = 0,
                 # BorderedBox arguments.
                 title: str | None = None, title_mods: list[str] = None, border_color: list[str] | None = None,
                 border_material: str | None = "██", padding: tuple[int, int] | None = None, draggable: bool = False,
                 resizable: bool = False, highlightable: bool = False) -> None:
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
                Defaults to (1, 1) plus the padding and border if applicable.
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
            draggable (bool, optional):
                Whether the box is draggable by its border.
                Defaults to False.
            resizable (bool, optional):
                Whether the box is resizable by its border (replaces draggable on the bottom, left, and right sides).
                Requires draggable to be True.
                Defaults to False.
            highlightable (bool, optional):
                Whether the contents of the box can be highlighted.
                Defaults to False.
        """

        if padding is None:
            self._padding = (1, 2)
        else:
            self._padding = deepcopy(padding)

        minimum = minimum_size
        if minimum is None:
            minimum = Coordinate(
                coordinates.screen_size,
                1 + (2 + 2 * self._padding[0] if border_material is not None else 0),
                1 + (2 * (len(border_material) + self._padding[1]) if border_material is not None else 0)
            )
        super().__init__(name, coordinates, size, minimum, description, contents, z_index)
        # super().__init__(**kwargs)  # Possible alternative to reduce input complexity.
        self._title = title
        self._border_material = border_material

        # Mouse moving/resizing variables.
        self._draggable = draggable
        self._resizable = resizable

        self._start_drag_mouse_pos = None
        self._start_drag_box_pos = None
        self._start_resize_size = None
        self._dragging = False
        self._resizing = False

        # Text highlighting variables.
        self._highlighting = False
        self._highlighting_start = None
        self._highlighting_end = None
        self._highlighted_text = None

        # Set the defaults.

        if border_color is None:
            self._border_color = []
        else:
            self._border_color = deepcopy(border_color)

        if title_mods is None:
            self._title_mods = deepcopy(self._border_color)
        else:
            self._title_mods = deepcopy(title_mods)

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

    def update_object(self, data: dict[str, any]) -> None:
        """Update the object with new controller inputs.

        Args:
            data (dict[str, any]):
                The data to update the object with.
        """
        super().update_object(data)

        # Drag or resize the box.
        if data["mouse_inputs"] is not None:
            if self._draggable and not (self._resizing or self._dragging):
                if data["mouse_inputs"]["left"]["newly_pressed"] and self.mouse_over:
                    border = ""
                    if self.mouse_over[0] == 0:
                        border += "top"
                    if self.mouse_over[0] == self.size[0] - 1:
                        border += "bottom"
                    if 0 <= self.mouse_over[1] <= len(self._border_material) - 1:
                        border += "left"
                    # if self.mouse_over[1] == self.size[1] - 1:
                    if self.size[1] - len(self._border_material) <= self.mouse_over[1] <= self.size[1] - 1:
                        border += "right"

                    if border:
                        if border != "top" and self.resizable:
                            self._resizing = border[:]
                            self._start_resize_size = self.size[:]
                        else:
                            self._dragging = True
                        self._start_drag_mouse_pos = self.mouse_over[:]  # data["mouse_pos"][:]
                        self._start_drag_box_pos = self._coordinates.char_value_y, self._coordinates.char_value_x
            # Drag the box if the mouse is held.
            elif self._dragging:
                if data["mouse_inputs"]["left"]["pressed"]:
                    self.coordinates = Coordinate(
                        self._coordinates.screen_size,
                        data["mouse_pos"][0] - self._start_drag_mouse_pos[0],
                        data["mouse_pos"][1] - self._start_drag_mouse_pos[1]
                    )
                else:
                    self._dragging = False
            # Resize the box if the mouse is held.
            elif self._resizing:
                if data["mouse_inputs"]["left"]["pressed"]:
                    if data["mouse_pos"] is not None:
                        if "left" in self._resizing:

                            old_x = self.coordinates.char_value_x
                            new_x = data["mouse_pos"][1] - self._start_drag_mouse_pos[1]
                            new_x = min(
                                new_x,
                                self._start_drag_box_pos[1] + self._start_resize_size[1] - self.minimum_size[1]
                            )
                            self.coordinates = Coordinate(
                                self._coordinates.screen_size,
                                self._coordinates.char_value_y,
                                new_x
                            )

                            self.size = Coordinate(
                                self._size.screen_size,
                                self._size.char_value_y,
                                old_x-new_x + self._size.char_value_x
                            )

                        if "right" in self._resizing:
                            delta = data["mouse_pos"][1] - (self.coordinates[1] + self._start_drag_mouse_pos[1])
                            self.size = Coordinate(
                                self._size.screen_size,
                                self._size.char_value_y,
                                delta + self._start_resize_size[1]
                            )
                        if "top" in self._resizing:
                            coordinate_delta = self.coordinates.char_value_y
                            self.coordinates = Coordinate(
                                self._coordinates.screen_size,
                                data["mouse_pos"][0] - self._start_drag_mouse_pos[0],
                                self._coordinates.char_value_x
                            )
                            coordinate_delta -= self.coordinates.char_value_y
                            self.size = Coordinate(
                                self._size.screen_size,
                                coordinate_delta + self._size.char_value_y,
                                self._size.char_value_x
                            )
                        if "bottom" in self._resizing:
                            delta = data["mouse_pos"][0] - (self.coordinates[0] + self._start_drag_mouse_pos[0])
                            self.size = Coordinate(
                                self._size.screen_size,
                                delta + self._start_resize_size[0],
                                self._size.char_value_x
                            )
                else:
                    self._resizing = False

            # HIGHLIGHTING

            # Start text highlighting. (Handle the initial click)
            if data["mouse_inputs"]["left"]["newly_pressed"]:
                y_offset = 0
                x_offset = 0
                if self._border_material is not None:
                    # y_offset = 1 + self._padding[0]
                    # x_offset = len(self._border_material) + self._padding[1]
                    # Allow clicks to start in the padding.
                    y_offset = 1
                    x_offset = len(self._border_material)

                # If the mouse is over the box but not the border, start highlighting and reset the highlighted text.
                if self.mouse_over and y_offset < self.mouse_over[0] < self.size[0] - 1 - y_offset and \
                        x_offset < self.mouse_over[1] < self.size[1] - 1 - x_offset:
                    self._highlighting_start = self.mouse_over[:]
                    self._highlighting = True
                    self._highlighting_end = None
                    self._highlighted_text = None
                # If the mouse is over the border or outside the box, stop highlighting.
                else:
                    self._highlighting_start = None
                    self._highlighting_end = None
                    self._highlighting = False
                    self._highlighted_text = None

            # Continue text highlighting. (Handle the dragging)
            elif self._highlighting_start:
                if data["mouse_inputs"]["left"]["pressed"]:
                    # If it's still in the box.
                    if self.mouse_over:
                        y_offset = 0
                        x_offset = 0
                        if self._border_material is not None:
                            y_offset = 1 + self._padding[0]
                            x_offset = len(self._border_material) + self._padding[1]

                        self._highlighting_end = (
                            min(max(self.mouse_over[0], y_offset), self.size[0] - 1 - y_offset),
                            min(max(self.mouse_over[1], x_offset), self.size[1] - 1 - x_offset)
                        )
                        # Extract the text.
                        if self._highlighting_start == self._highlighting_end:
                            self._highlighted_text = None
                        else:
                            start = self._highlighting_start
                            end = self._highlighting_end
                            # Flip if dragged backwards or upwards.
                            if start[0] > end[0] or (start[0] == end[0] and start[1] > end[1]):
                                start, end = end, start

                            text = []
                            for y in range(start[0], end[0] + 1):
                                line = ""
                                # First line (and last if they're the same).
                                if y == start[0]:
                                    for x in range(start[1], self.size[1] - 1 - x_offset - self._padding[1]
                                                   if y != end[0] else end[1] + 1):
                                        line += self.contents[y][x][0]
                                # Subsequent lines.
                                elif y != end[0]:
                                    for x in range(x_offset + self._padding[1],
                                                   self.size[1] - 1 - x_offset - self._padding[1]):
                                        line += self.contents[y][x][0]
                                # Last line.
                                else:
                                    for x in range(x_offset, end[1] + 1):
                                        line += self.contents[y][x][0]
                                if line.strip() == "":
                                    line = "\n"
                                else:
                                    line = line.strip()
                                text.append(line)
                            self._highlighted_text = " ".join(text)

                    # If it's moved outside the box.
                    else:
                        y_offset = self.coordinates.char_value_y
                        x_offset = self.coordinates.char_value_x
                        y_length = self.size[0]
                        x_length = self.size[1]
                        if self._border_material is not None:
                            y_offset += 1 + self._padding[0]
                            x_offset += len(self._border_material) + self._padding[1]
                            y_length -= 2 + 2 * self._padding[0]
                            x_length -= 2 * (len(self._border_material) + self._padding[1])

                        self._highlighting_end = (
                            min(max(data["mouse_pos"][0] - y_offset, 0), y_length - 1),
                            min(max(data["mouse_pos"][1] - x_offset, 0), x_length - 1)
                        )

                else:
                    self._highlighting = False
                    self._highlighted_text = None
                    if self._highlighting_start and self._highlighting_end:
                        start = self._highlighting_start
                        end = self._highlighting_end
                        if start[0] > end[0] or (start[0] == end[0] and start[1] > end[1]):
                            start, end = end, start
                        self._highlighted_text = []
                        for y in range(start[0], end[0] + 1):
                            line = ""
                            for x in range(start[1], end[1] + 1):
                                line += self.contents[y][x][0]
                            self._highlighted_text.append(line)

            # End text highlighting.

            # Reset text highlighting.

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
    def draggable(self) -> bool:
        return self._draggable

    @property
    def resizable(self) -> bool:
        return self._resizable

    @property
    def size(self) -> Coordinate:
        return self._size

    @property
    def highlighted_text(self) -> str | None:
        return self._highlighted_text

    @property
    def highlighting(self) -> bool:
        return self._highlighting

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

    @draggable.setter
    def draggable(self, new_draggable: bool) -> None:
        self._draggable = new_draggable

    @resizable.setter
    def resizable(self, new_resizable: bool) -> None:
        self._resizable = new_resizable

    @size.setter
    def size(self, new_size: Coordinate) -> None:
        super().resize(new_size)

        self._contents = [[[" ", []] for _ in range(self._size[1])] for _ in range(self._size[0])]

        self.apply_border()
