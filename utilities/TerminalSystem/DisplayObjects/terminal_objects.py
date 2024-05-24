from base_terminal_object import PrintableObject
from text_box import TextBox
from bordered_box import BorderedBox
from image_box import ImageBox


class TerminalObjects:
    """The terminal _display objects.

    Attributes:
        TERMINAL_OBJECT (PrintableObject):
            The basic terminal object.
        BORDERED_BOX (BorderedBox):
            A basic bordered box. Used primarily to build other types of objects. rather than being used directly.
        TEXT_BOX (TextBox):
            A basic text box.
        IMAGE_BOX (ImageBox):
            A basic image box.
    """
    TERMINAL_OBJECT = PrintableObject
    BORDERED_BOX = BorderedBox
    TEXT_BOX = TextBox
    IMAGE_BOX = ImageBox
