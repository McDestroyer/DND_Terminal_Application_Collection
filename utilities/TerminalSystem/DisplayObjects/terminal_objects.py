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
    # Display objects.
    TERMINAL_OBJECT = PrintableObject
    BORDERED_BOX = BorderedBox
    TEXT_BOX = TextBox
    IMAGE_BOX = ImageBox

    # Buttons.
    BASIC_BUTTON = None
    TOGGLE_BUTTON = None
    RADIO_BUTTON = None

    # Sliders.
    HORIZONTAL_SLIDER = None
    VERTICAL_SLIDER = None

    # Text-based inputs.
    TEXT_INPUT = None
    NUMBER_INPUT = None
    PASSWORD_INPUT = None

    # Popup specialized inputs.
    FILE_INPUT = None
    COLOR_INPUT = None
    DATE_INPUT = None
    TIME_INPUT = None
    DATETIME_INPUT = None

    DROPDOWN_MENU = None

    COLLECTION = None
    # Collection types (?):
        # TABLE = None
        # TREE = None
        # LIST = None
        # GRID = None
        # GRAPH = None
        # CHART = None

    TOOLTIP = None  # A small box that appears when hovering over an object.
    ALERT = None  # A centered, screen-filling message box.
    CONTEXT_MENU = None  # A menu that appears when right-clicking on an object.



