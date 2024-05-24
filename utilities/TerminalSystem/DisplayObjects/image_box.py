from copy import deepcopy

import color

from bordered_box import BorderedBox
from coordinates import Coordinate


class TextBox(BorderedBox):
    """A generic box object."""

    def __init__(self, name: str, coordinates: Coordinate, size: Coordinate, minimum_size: Coordinate | None = None,
                 description: str | None = None, contents: list[list[list[str | list[str]]]] | None = None,
                 z_index: int = 0, title: str | None = None, title_mods: list[str] = None,
                 border_color: list[str] | None = None, border_material: str | None = None,
                 image: str | list[list[list[str | list[str]]]] | None = None,
                 padding: tuple[int, int] | None = None) -> None:
        """Initialize the Image Box object.

        Args:
            name (str):
                The name of the box.
            coordinates (Coordinate):
                The coordinates of the box.
            size (Coordinate):
                The size of the box.
            minimum_size (Coordinate, optional):
                The minimum size of the box. Intended for use when one or both of the axes use percentages.
                Overridden when the image size is larger than the minimum size.
                Defaults to None.
            description (str, optional):
                The description of the box.
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
            image (str | list[list[list[str | list[str]]]], optional):
                The image to display in the box. Can be a path to an image file or an image in terminal display format.
                Defaults to None.
            padding (tuple[int, int], optional):
                The padding of the box.
                Defaults to (1, 2). (y, x)
        """
        super().__init__(name, coordinates, size, minimum_size, description, contents, z_index, title, title_mods,
                         border_color, border_material, padding)
        self._image = self.get_image(image)

    def get_image(self, image: str | list[list[list[str | list[str]]]] | None) -> list[list[list[str | list[str]]]]:
        """Get the image to display in the box.

        Args:
            image (str | list[list[list[str, list[str]]]] | None):
                The image to display in the box. Can be a path to an image file or an image in terminal display format.
                Defaults to None.

        Returns:
            list[list[list[str, list[str]]]]:
                The image to display in the box.
        """
        if image is None:
            return [[[" ", [color.BACKGROUND_DEFAULT_COLOR]]]]
        elif isinstance(image, str):
            return self.get_image_from_file(image)
        else:
            return image

    def get_image_from_file(self, file_path: str) -> list[list[list[str | list[str]]]]:
        """Get the image from a file.

        Args:
            file_path (str):
                The path to the file.

        Returns:
            list[list[list[str | list[str]]]]:
                The image to display in the box.
        """
        # Try to open the file and read the image data.
        try:
            # Check if the file is a valid image file.
            if file_path.upper().split(".")[-1] not in ["AI", "AAI"]:
                raise FileNotFoundError
            # Read the file.
            with open(file_path, "r") as file:
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
        details = file_image.pop(0).split(":")
        self._image_size = (int(details[0]), int(details[1]))
        self._base_colors = details[-1]
        if file_path.upper().endswith(".AAI"):
            self._image_frames = int(details[2])
            self._frame_time = float(details[3])
        else:
            self._image_frames = 1
            self._frame_time = 0.0

        # Step past the blank line.
        file_image.pop(0)

        # Convert the image to the correct format.
        reading_code = None
        for r in range(self._image_size[0]):
            for c in enumerate(file_image.pop(0)):
                if c == "\033":
                    c = [c, [self._base_colors]]
                else:
                    c = [c, []]
                # file_image[0][c] = [file_image[0][c], [self._base_colors]]

        # for r, row in enumerate(image):
        #     for c, char in enumerate(row):
        #         if char == "\033":
        #             row[i] = [char, [self._base_colors]]
        #     row = [row]

        return None

    @property
    def image(self) -> list[list[list[str | list[str]]]] | None:
        return self._image

    @image.setter
    def image(self, image: str | list[list[list[str | list[str]]]]) -> None:
        self._image = self.get_image(image)
