from base_terminal_object import PrintableObject
from text_box import TextBox


class TerminalObjects:
    """The terminal _display objects.

    Attributes:
        TERMINAL_OBJECT (PrintableObject):
            The basic terminal object.
        TEXT_BOX (TextBox):
            The _text box.
    """
    TERMINAL_OBJECT = PrintableObject
    TEXT_BOX = TextBox
