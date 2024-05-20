"""handles screens, makes sure only one is visible at a time, swapping screens, screens, window-wide keybinds and color_scheme schemes, and more."""
import pickle

import color
from display import Display
from screen_class import Screen


class WindowManager:

    def __init__(self, screen_size: tuple[int, int]) -> None:
        """Initialize the WindowManager object.

        Args:
            screen_size (tuple[int, int]):
                The minimum screen size (y, x).
        """
        self.screen_size: tuple[int, int] = screen_size
        self.screens: list[Screen] = []
        self.current_screen: Screen | None = None

        # Set up the display.
        self.display: Display = Display(screen_size)

        self.default_color_scheme = {
            "status": [color.WHITE, color.BACKGROUND_BLACK],
            "header": [color.RED, color.BOLD, color.UNDERLINE, color.BACKGROUND_BLACK],
            "text":   [color.BRIGHT_WHITE, color.BACKGROUND_BLACK],
            "option": [color.BRIGHT_GREEN, color.UNDERLINE, color.BACKGROUND_BRIGHT_BLACK],
            "selected_option": [color.BOLD, color.BRIGHT_BLACK, color.BACKGROUND_BRIGHT_GREEN],
            "footer": [color.RED, color.BACKGROUND_BLACK],
            "keybinds": [color.BRIGHT_BLACK, color.BACKGROUND_BLACK],
        }

        self.color_scheme = self.default_color_scheme

        self.keybinds: dict[str, callable] = {}

    def add_screen(self, screen_name: str) -> None:
        """Add a screen to the WindowManager.

        Args:
            screen_name (str):
                The name of the screen.
        """
        self.screens.append(Screen(screen_name, self.screen_size))

    def remove_screen(self, screen_name: str) -> None:
        """Remove a screen from the WindowManager.

        Args:
            screen_name (str):
                The name of the screen.
        """
        self.screens = [screen for screen in self.screens if screen.get_name() != screen_name]

    def load_screen_from_file(self, screen_name: str, file_path: str) -> None:
        """Load a screen from a file and add it to the WindowManager.

        Args:
            screen_name (str):
                The name of the screen.
            file_path (str):
                The path to the file.
        """
        with open(file_path, "rb") as file:
            screen = pickle.load(file)
        screen.set_name(screen_name)
        self.screens.append(screen)

    def list_screens(self) -> list[Screen]:
        """Return the screens in the WindowManager.

        Returns:
            list[Screen]: The screens in the WindowManager.
        """
        return self.screens

    def get_screen(self, screen_name: str) -> Screen | None:
        """Return a screen from the WindowManager.

        Args:
            screen_name (str):
                The name of the screen.

        Returns:
            Screen: The screen, or None if the screen does not exist.
        """
        for screen in self.screens:
            if screen.get_name() == screen_name:
                return screen
        return None

    def set_current_screen(self, screen_name: str) -> None:
        """Set the current screen to the screen with the given name and update the display.

        Args:
            screen_name (str):
                The name of the screen.
        """
        self.current_screen = self.get_screen(screen_name)
        self.refresh_screen()

    def get_current_screen(self) -> Screen | None:
        """Return the current screen.

        Returns:
            Screen | None: The current screen.
        """
        return self.current_screen

    def refresh_screen(self) -> None:
        """Refresh the screen array and display it."""
        self.display.set_display(self.current_screen.update_display())
        self.display.antiflash_refresh_display()
