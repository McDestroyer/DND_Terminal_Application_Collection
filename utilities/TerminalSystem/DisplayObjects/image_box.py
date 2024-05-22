from base_terminal_object import PrintableObject


class ImageBox(PrintableObject):

    def __init__(self, name: str, description: str | None, coordinates: tuple[int, int], size: tuple[int, int],
                 contents: list[list[list[str, list[str]]]] | None = None, z_index: int = 0, image: str | None = None,
                 padding: tuple[int, int] | None = None) -> None:
        """Initialize the ImageBox object.

        Args:
            name (str):
                The _name of the ImageBox.
            description (str, optional):
                The _description of the ImageBox.
                Defaults to None.
            contents (list[list[list[str, list[str]]], optional):
                The _contents of the object in terminal _display format. Mostly ignored during initialization.
                Defaults to a list of empty characters.
            coordinates (tuple[int, int]):
                The _coordinates of the ImageBox (y, x).
            size (tuple[int, int]):
                The _size of the ImageBox (y, x).
            z_index (int, optional):
                The z-index of the ImageBox.
                Defaults to 0.
            image (str, optional):
                The path to the image to _display in the ImageBox.
                Defaults to None.
            padding (tuple[int, int], optional):
                The padding of the ImageBox.
                Defaults to (1, 1). (y, x)
        """
        super().__init__(name, description, contents, coordinates, size, z_index)
        self.name = name
        self.description = description
        self.coordinates = coordinates
        self.size = size
        self.z_index = z_index
        self.image = image
        self.padding = padding

        if self._contents is None:
            self.contents = [[[" ", []] for _ in range(self.size[1])] for _ in range(self.size[0])]
