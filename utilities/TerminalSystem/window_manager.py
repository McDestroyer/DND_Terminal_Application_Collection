"""handles screens, makes sure only one is visible at a time, swapping screens, screens, window-wide keybinds and color schemes, and more."""
import color


class WindowManager:

    def __init__(self, screen_size: tuple[int, int]) -> None:
        """Initialize the WindowManager object.

        Args:
            screen_size (tuple[int, int]):
                The minimum screen size (y, x).
        """
        self.screen_size = screen_size
        self.screens = []
        self.current_screen = None

        self.color_scheme = {}
        self.default_color_scheme = {
            "header": [color.YELLOW],
            "options": [color.BLUE],
            "footer": [color.YELLOW],
            "keybinds": [color.BRIGHT_BLACK, color.ITALIC],
            "selected_option": [color.BOLD, color.GREEN],
        }
