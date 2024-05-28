import pickle

import color
import input_handler
from coordinates import Coordinate
from display import Display
from screen_class import Screen
from terminal_objects import TerminalObjects as TObj


class WindowManager:

    def __init__(self, screen_size: tuple[int, int]) -> None:
        """Initialize the WindowManager object.

        Args:
            screen_size (tuple[int, int]):
                The screen size (y, x).
        """
        self._screen_size: tuple[int, int] = screen_size
        self._screens: list[Screen] = []
        self._current_screen: Screen | None = None

        # Set up the display.
        self._display: Display = Display(screen_size)

        self._default_color_scheme = {
            "status": [color.WHITE, color.BACKGROUND_BLACK],
            "header": [color.RED, color.BOLD, color.UNDERLINE, color.BACKGROUND_BLACK],
            "text":   [color.BRIGHT_WHITE, color.BACKGROUND_BLACK],
            "option": [color.BRIGHT_GREEN, color.UNDERLINE, color.BACKGROUND_BRIGHT_BLACK],
            "selected_option": [color.BOLD, color.BRIGHT_BLACK, color.BACKGROUND_BRIGHT_GREEN],
            "footer": [color.RED, color.BACKGROUND_BLACK],
            "keybinds": [color.BRIGHT_BLACK, color.BACKGROUND_BLACK],
        }

        self._color_scheme = self._default_color_scheme

        self.mouse = None

    def setup_mouse(self) -> None:
        """Set up the mouse."""
        self.mouse = TObj.TERMINAL_OBJECT(
            "Mouse", coordinates=Coordinate(self.screen_size, 1, 1),
            size=Coordinate(self.screen_size, 2, 2),
            contents=[
                [
                    ["|", [color.BRIGHT_WHITE, color.UNDERLINE]],
                    ["\\", [color.BRIGHT_WHITE, color.UNDERLINE]],
                ],
                [
                    ["", [color.BRIGHT_WHITE]],
                    ["`", [color.BRIGHT_WHITE]],
                ],
            ],
            z_index=10000,
        )
        self.current_screen.add_object(self.mouse)

    def remove_mouse(self) -> None:
        """Remove the mouse."""
        self.current_screen.remove_object("Mouse")
        self.mouse = None

    def add_screen(self, screen_name: str) -> Screen:
        """Add a screen to the WindowManager.

        Args:
            screen_name (str):
                The name of the screen.

        Returns:
            Screen: The screen.
        """
        screen = Screen(screen_name, self._screen_size)
        self._screens.append(screen)
        return screen

    def remove_screen(self, screen_name: str) -> Screen:
        """Remove a screen from the WindowManager.

        Args:
            screen_name (str):
                The name of the screen.

        Returns:
            Screen: The screen.
        """
        screen = self.get_screen_by_name(screen_name)
        self._screens.remove(screen)
        return screen

    def save_screen_to_file(self, screen_name: str, file_path: str) -> None:
        """Save a screen to a file.

        Args:
            screen_name (str):
                The name of the screen.
            file_path (str):
                The path to the file.
        """
        screen = self.get_screen_by_name(screen_name)
        with open(file_path, "wb") as file:
            pickle.dump(screen, file)

    def load_screen_from_file(self, screen_name: str, file_path: str) -> Screen:
        """Load a screen from a file and add it to the WindowManager.

        Args:
            screen_name (str):
                The name of the screen.
            file_path (str):
                The path to the file.

        Returns:
            Screen: The screen.
        """
        with open(file_path, "rb") as file:
            screen = pickle.load(file)

        screen.name = screen_name
        self._screens.append(screen)
        return screen

    def get_screen_by_name(self, screen_name: str) -> Screen | None:
        """Return a screen from the WindowManager.

        Args:
            screen_name (str):
                The name of the screen.

        Returns:
            Screen: The screen, or None if the screen does not exist.
        """
        for screen in self._screens:
            if screen.name == screen_name:
                return screen
        return None

    def set_current_screen(self, screen: str | Screen) -> Screen:
        """Set the current screen to the given screen or the screen with the given name and update the display.

        Args:
            screen (str | Screen):
                The name of the screen or the screen itself.

        Returns:
            Screen: The screen.
        """
        if isinstance(screen, Screen):
            self._current_screen = screen
        else:
            self._current_screen = self.get_screen_by_name(screen)
        if self.mouse is not None:
            self._current_screen.add_object(self.mouse)
        else:
            self._current_screen.remove_object("Mouse")
        return self._current_screen

    def refresh_screen(self) -> None:
        """Refresh the screen array and display it."""
        self._display.display_array = self._current_screen.update_display()

    @property
    def display(self) -> Display:
        """Return the display.

        Returns:
            Display: The display.
        """
        return self._display

    @property
    def color_scheme(self) -> dict[str, list[str]]:
        """Return the color scheme.

        Returns:
            dict[str, list[str]]: The color scheme.
        """
        return self._color_scheme

    @property
    def default_color_scheme(self) -> dict[str, list[str]]:
        """Return the default color scheme.

        Returns:
            dict[str, list[str]]: The default color scheme.
        """
        return self._default_color_scheme

    @property
    def screens(self) -> list[Screen]:
        """Return the screens.

        Returns:
            list[Screen]: The screens.
        """
        return self._screens

    @property
    def screen_size(self) -> tuple[int, int]:
        """Return the screen size.

        Returns:
            tuple[int, int]: The screen size.
        """
        return self._screen_size

    @property
    def current_screen(self) -> Screen | None:
        """Return the current screen.

        Returns:
            Screen | None: The current screen.
        """
        return self._current_screen

    @property
    def display_array(self) -> list[list[list[str | list[str]]]]:
        """Return the display array.

        Returns:
            list[list[list[str | list[str]]]]: The display array.
        """
        return self._display.display_array

    @property
    def display_size(self) -> tuple[int, int]:
        """Return the display size.

        Returns:
            tuple[int, int]: The display size.
        """
        return self._display.display_size

    @screen_size.setter
    def screen_size(self, new_screen_size: tuple[int, int]) -> None:
        """Set the screen size.

        Args:
            new_screen_size (tuple[int, int]):
                The new screen size.
        """
        self._screen_size = new_screen_size
        self._display.display_size = new_screen_size
        for screen in self._screens:
            screen.screen_size = new_screen_size
        self.refresh_screen()

    @color_scheme.setter
    def color_scheme(self, new_color_scheme: dict[str, list[str]]) -> None:
        """Set the color scheme.

        Args:
            new_color_scheme (dict[str, list[str]]):
                The new color scheme.
        """
        self._color_scheme = new_color_scheme
        self.refresh_screen()

    # @keybinds.setter
    # def keybinds(self, new_keybinds: dict[str, callable]) -> None:
    #     """Set the keybinds.
    #
    #     Args:
    #         new_keybinds (dict[str, callable]):
    #             The new keybinds.
    #     """
    #     self._keybinds = new_keybinds
    #     self.refresh_screen()

    @screens.setter
    def screens(self, new_screens: list[Screen]) -> None:
        """Set the screens.

        Args:
            new_screens (list[Screen]):
                The new screens.
        """
        self._screens = new_screens

    @current_screen.setter
    def current_screen(self, new_current_screen: Screen) -> None:
        """Set the current screen.

        Args:
            new_current_screen (Screen):
                The new current screen.
        """
        self._current_screen = new_current_screen
        self.refresh_screen()

    @display_array.setter
    def display_array(self, new_display_array: list[list[list[str | list[str]]]]) -> None:
        """Set the display array.

        Args:
            new_display_array (list[list[list[str | list[str]]]]):
                The new display array.
        """
        self._display.display_array = new_display_array
        self._display.antiflash_refresh_display()

    @display_size.setter
    def display_size(self, new_display_size: tuple[int, int]) -> None:
        """Set the display size.

        Args:
            new_display_size (tuple[int, int]):
                The new display size.
        """
        self._display.display_size = new_display_size
        self.refresh_screen()

    @default_color_scheme.setter
    def default_color_scheme(self, new_default_color_scheme: dict[str, list[str]]) -> None:
        """Set the default color scheme.

        Args:
            new_default_color_scheme (dict[str, list[str]]):
                The new default color scheme.
        """
        self._default_color_scheme = new_default_color_scheme
        self.refresh_screen()

    @display.setter
    def display(self, new_display: Display) -> None:
        """Set the display.

        Args:
            new_display (Display):
                The new display.
        """
        self._display = new_display
        self.refresh_screen()
