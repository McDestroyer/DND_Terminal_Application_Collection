from copy import deepcopy
from time import time_ns

import color

from bordered_box import BorderedBox
from coordinates import Coordinate


class ImageBox(BorderedBox):
    """A generic box object."""

    def __init__(self, name: str, coordinates: Coordinate, size: Coordinate,
                 image: str | list[list[list[list[str | list[str]]]]], minimum_size: Coordinate | None = None,
                 description: str | None = None, contents: list[list[list[str | list[str]]]] | None = None,
                 z_index: int = 0, title: str | None = None, title_mods: list[str] = None,
                 border_color: list[str] | None = None, border_material: str | None = "██",
                 padding: tuple[int, int] | None = None, centered: bool = True, shrink_to_fit: bool = True) -> None:
        """Initialize the Image Box object.

        Args:
            name (str):
                The name of the box.
            coordinates (Coordinate):
                The coordinates of the box.
            size (Coordinate):
                The size of the box.
            image (str | list[list[list[list[str | list[str]]]]]):
                The image to display in the box. Can be a path to an image file or an image in terminal display format.
            minimum_size (Coordinate, optional):
                The minimum size of the box. Intended for use when one or both of the axes use percentages.
                Overridden when the image size is larger than the minimum size.
                Defaults to None.
            description (str, optional):
                The description of the box. Only used by the person implementing the box.
                Defaults to None.
            contents (list[list[list[str | list[str]]], optional):
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
            centered (bool, optional):
                Whether the contents of the box should be centered.
                Defaults to True.
            shrink_to_fit (bool, optional):
                Whether the box should shrink to fit the image.
                Defaults to True.
        """
        super().__init__(name, coordinates, size, minimum_size, description, contents, z_index, title, title_mods,
                         border_color, border_material, padding)
        self._centered = centered
        self._shrink_to_fit = shrink_to_fit

        self._image_size = Coordinate(self.coordinates.screen_size, 0, 0)
        self._image_frames = 0
        self._frame_time = 0.0
        self._base_colors = ""

        self._current_frame = 0
        self._last_update = time_ns()

        self.image = self.get_image(image)
        self.update_image()

    def get_image(self, image: str | list[list[list[list[str | list[str]]]]]) -> (
            list)[list[list[list[str | list[str]]]]]:
        """Get the image to display in the box.

        Args:
            image (str | list[list[list[list[str | list[str]]]]]):
                The list of frames to display in the box. Can be a path to an image file or a list of frames in
                terminal display format.
                Defaults to None.

        Returns:
            list[list[list[list[str | list[str]]]]]:
                The list of frames to display in the box.
        """
        if isinstance(image, str):
            return self.get_image_from_file(image)
        else:
            return deepcopy(image)

    def get_image_from_file(self, file_path: str) -> list[list[list[list[str | list[str]]]]]:
        """Get the image from a file.

        Args:
            file_path (str):
                The path to the file.

        Returns:
            list[list[list[list[str | list[str]]]]]:
                The list of frames to display in the box.
        """
        # Try to open the file and read the image data.
        try:
            # Check if the file is a valid image file.
            if file_path.upper().split(".")[-1] not in ["AI", "AAI"]:
                raise FileNotFoundError
            # Read the file.
            with open(file_path, "r", encoding="UTF-16") as file:
                file_image = file.readlines()[:]
        # If a valid file is not found, return a blank image.
        except FileNotFoundError:
            return [
                [
                    [" ", [color.BACKGROUND_DEFAULT_COLOR]] * self._minimum_size[1]
                ] * self._minimum_size[0]
            ]

        # Get the metadata.
        # .AI (ASCII Image) files have the format: "width:height:base_colors"
        # .AAI (Animated ASCII Image) files have the format: "width:height:frames:time:base_colors"
        details = file_image.pop(0).strip().split(":")
        self._image_size = Coordinate(self.coordinates.screen_size, int(details[0]), int(details[1]))
        self._base_colors = details[-1].replace("\\033", "\033")
        if file_path.upper().endswith(".AAI"):
            self._image_frames = int(details[2])
            self._frame_time = float(details[3])
        else:
            self._image_frames = 1
            self._frame_time = 0.0

        animation = []

        for i in range(self._image_frames):
            # Step past the blank line.
            file_image.pop(0)

            # Extract color information.
            code_indices = [{} for _ in range(self._image_size[0])]
            for j in range(self._image_size[0]):
                file_image[j] = line = file_image[j].replace("\\033", "\033").rstrip()
                while "\033" in line:
                    start_index = line.find("\033")
                    end_index = line.find("m", start_index)
                    code = line[start_index:end_index + 1]
                    code_indices[j][start_index] = code
                    file_image[j] = line = line[:start_index] + line[end_index + 1:]

            img = [[[" ", [self._base_colors]] for _ in range(self._image_size[1])] for _ in range(self._image_size[0])]

            # Convert the image to the correct format.
            code_str = ""
            for r in range(self._image_size[0]):
                for c, char in enumerate(file_image.pop(0)):
                    # Break this row's loop if the image is too large for the box.
                    if c >= self._image_size[1]:
                        break
                    # Check for color codes at this spot. If there is one, add it to the code string unless it is the
                    # end code, in which case the code string is reset.
                    if c in code_indices[r]:
                        if code_indices[r][c] == color.END:
                            code_str = ""
                        else:
                            code_str += code_indices[r][c]
                    # Set the character and color for the current spot.
                    img[r][c] = [char, [self._base_colors + code_str if code_str else self._base_colors]]

            animation.append(img)

        return animation

    def update_image(self) -> None:
        """Update the image to the next frame."""
        if self._image_frames > 1 and time_ns() - self._last_update >= self._frame_time * 1_000_000_000:
            self._current_frame = (self._current_frame + 1) % self._image_frames
            self._last_update = time_ns()
        self.display_image(self._image[self._current_frame])

    def display_image(self, image: list[list[list[str | list[str]]]]) -> None:
        """Display the image in the box.

        Args:
            image (list[list[list[str | list[str]]]]):
                The image to display.
        """
        # Calculate the offset needed to place the image so that it doesn't overlap with the borders.
        y_offset = 0
        x_offset = 0

        if self._border_material is not None:
            y_offset = 1 + self._padding[0]
            x_offset = len(self._border_material) + self._padding[1]

            # Set the image area to be blank.
            for y in range(1, self._size[0] - 1):
                for x in range(len(self._border_material), self._size[1] - len(self._border_material)):
                    self.contents[y][x] = [" ", [self._base_colors]]
        else:
            for y in range(y_offset, self._size[0] - y_offset):
                for x in range(x_offset, self._size[1] - x_offset):
                    self.contents[y][x] = [" ", [self._base_colors]]

        available_space_y = self._size[0] - 2 * y_offset
        available_space_x = self._size[1] - 2 * x_offset

        if self._centered:
            y_offset = (available_space_y - self._image_size[0]) // 2 + y_offset
            x_offset = (available_space_x - self._image_size[1]) // 2 + x_offset

        # Add the image to the box.
        for y in range(self._image_size[0]):
            for x in range(self._image_size[1]):
                self.contents[y + y_offset][x + x_offset] = deepcopy(image[y][x])

        # if old_contents != self.contents:
        self._should_refresh = True
        # self.apply_border()

    @property
    def image(self) -> list[list[list[str | list[str]]]] | None:
        return self._image

    @image.setter
    def image(self, image: str | list[list[list[str | list[str]]]]) -> None:
        self._image = self.get_image(image)
        min_size = deepcopy(self._image_size)
        if self._border_material is not None:
            y_size = self._image_size[0] + 2 + 2 * self._padding[0]
            x_size = self._image_size[1] + 2 * len(self._border_material) + 2 * self._padding[1]
            if self._shrink_to_fit:
                min_size = Coordinate(
                    self.coordinates.screen_size,
                    max(y_size, self._minimum_size[0]),
                    max(x_size, self._minimum_size[1])
                )
            else:
                min_size = Coordinate(self.coordinates.screen_size, y_size, x_size)
        self.minimum_size = min_size
        self._current_frame = 0
        self._last_update = time_ns()
        self.update_image()

    @property
    def current_frame(self) -> int:
        return self._current_frame

    @property
    def image_frames(self) -> int:
        return self._image_frames

    @property
    def frame_time(self) -> float:
        return self._frame_time

    @property
    def base_colors(self) -> str:
        return self._base_colors

    @property
    def image_size(self) -> Coordinate:
        return self._image_size

    @property
    def last_update(self) -> int:
        return self._last_update

    @property
    def minimum_size(self) -> Coordinate:
        return self._minimum_size

    @minimum_size.setter
    def minimum_size(self, minimum_size: Coordinate) -> None:
        self._minimum_size = minimum_size
        if self._shrink_to_fit:
            self.size = Coordinate(
                self.coordinates.screen_size,
                self._minimum_size[0],
                self._minimum_size[1]
            )
        else:
            self.size = Coordinate(
                self.coordinates.screen_size,
                max(self._size[0], self._minimum_size[0]),
                max(self._size[1], self._minimum_size[1])
            )
        self.update_image()

    @property
    def centered(self) -> bool:
        return self._centered

    @centered.setter
    def centered(self, centered: bool) -> None:
        self._centered = centered
        self.update_image()

    @property
    def shrink_to_fit(self) -> bool:
        return self._shrink_to_fit

    @shrink_to_fit.setter
    def shrink_to_fit(self, shrink_to_fit: bool) -> None:
        self._shrink_to_fit = shrink_to_fit
        self.update_image()

