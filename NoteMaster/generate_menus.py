import color
from terminal_objects import TerminalObjects as TObj
from units import Units
from coordinates import Coordinate


def generate_main_menu(self):
    """Generate the main menu."""
    main_menu = TObj.MENU_BOX(
        "Main Menu",
        coordinates=Coordinate(self.screen_size, 0, 0, unit_y=Units.PERCENT, unit_x=Units.PERCENT),
        size=Coordinate(self.screen_size, 100, 100, unit_y=Units.PERCENT, unit_x=Units.PERCENT),
        title="Main Menu",
        title_mods=[color.UNDERLINE, color.BRIGHT_RED, color.BACKGROUND_BLUE],
        color_scheme=[color.BACKGROUND_DEFAULT_COLOR, color.BRIGHT_GREEN],
        menu_options=[
            TObj.BASE_MENU_OPTION(
                "View Notes",
                "View Notes",
                boundaries=Coordinate(self.screen_size, 10, 10, unit_y=Units.PERCENT, unit_x=Units.PERCENT),
                color_scheme=[color.BRIGHT_WHITE, color.BACKGROUND_DEFAULT_COLOR],
                function=self.view_notes,
            ),
            TObj.BASE_MENU_OPTION(
                "Add Note",
                "Add Note",
                boundaries=Coordinate(self.screen_size, 10, 30, unit_y=Units.PERCENT, unit_x=Units.PERCENT),
                color_scheme=[color.BRIGHT_WHITE, color.BACKGROUND_DEFAULT_COLOR],
                function=self.add_note,
            ),
            TObj.BASE_MENU_OPTION(
                "Edit Note",
                "Edit Note",
                boundaries=Coordinate(self.screen_size, 10, 50, unit_y=Units.PERCENT, unit_x=Units.PERCENT),
                color_scheme=[color.BRIGHT_WHITE, color.BACKGROUND_DEFAULT_COLOR],
                function=self.edit_note,
            ),
            TObj.BASE_MENU_OPTION(
                "Delete Note",
                "Delete Note",
                boundaries=Coordinate(self.screen_size, 10, 70, unit_y=Units.PERCENT, unit_x=Units.PERCENT),
                color_scheme=[color.BRIGHT_WHITE, color.BACKGROUND_DEFAULT_COLOR],
                function=self.delete_note,
            ),
            TObj.BASE_MENU_OPTION(
                "Exit",
                "Exit",
                boundaries=Coordinate(self.screen_size, 10, 90, unit_y=Units.PERCENT, unit_x=Units.PERCENT),
                color_scheme=[color.BRIGHT_WHITE, color.BACKGROUND_DEFAULT_COLOR],
                function=self.shut_down,
            ),
        ],
    )
    return main_menu


def generate_test_objects(self):

    box3 = TObj.TEXT_BOX(
        "Bob Box 3",
        coordinates=Coordinate(self.screen_size, 50, 50, unit_y=Units.PERCENT, unit_x=Units.PERCENT),
        size=Coordinate(self.screen_size, 50, 50, unit_y=Units.PERCENT, unit_x=Units.PERCENT),
        text="I'm the hidden 3rd box! Somehow, my existence works!", title="Bob Box 3", border_color=[color.BLUE],
        title_mods=[color.UNDERLINE, color.BRIGHT_RED, color.BACKGROUND_BLUE],
        color_scheme=[color.BACKGROUND_DEFAULT_COLOR, color.BRIGHT_GREEN]
    )
    box4 = TObj.TEXT_BOX(
        "Bob Box 4",
        coordinates=Coordinate(self.screen_size, 0, 0, unit_y=Units.PERCENT, unit_x=Units.PERCENT),
        size=Coordinate(self.screen_size, 50, 50, unit_y=Units.PERCENT, unit_x=Units.PERCENT),
        text="I'm the hidden 4th box! Somehow, my existence works!", title="Bob Box 4", border_color=[color.BLUE],
        title_mods=[color.UNDERLINE, color.BRIGHT_RED, color.BACKGROUND_BLUE],
        color_scheme=[color.BACKGROUND_DEFAULT_COLOR, color.BRIGHT_GREEN]
    )
    box5 = TObj.TEXT_BOX(
        "Bob Box 5",
        coordinates=Coordinate(self.screen_size, 0, 50, unit_y=Units.PERCENT, unit_x=Units.PERCENT),
        size=Coordinate(self.screen_size, 50, 50, unit_y=Units.PERCENT, unit_x=Units.PERCENT),
        text="I'm the hidden 5th box! Somehow, my existence works!", title="Bob Box 5", border_color=[color.BLUE],
        title_mods=[color.UNDERLINE, color.BRIGHT_RED, color.BACKGROUND_BLUE],
        color_scheme=[color.BACKGROUND_DEFAULT_COLOR, color.BRIGHT_GREEN]
    )
    box6 = TObj.TEXT_BOX(
        "Bob Box 6",
        coordinates=Coordinate(self.screen_size, 50, 0, unit_y=Units.PERCENT, unit_x=Units.PERCENT),
        size=Coordinate(self.screen_size, 50, 50, unit_y=Units.PERCENT, unit_x=Units.PERCENT),
        text="I'm the hidden 6th box! Somehow, my existence works!", title="Bob Box 6", border_color=[color.BLUE],
        title_mods=[color.UNDERLINE, color.BRIGHT_RED, color.BACKGROUND_BLUE],
        color_scheme=[color.BACKGROUND_DEFAULT_COLOR, color.BRIGHT_GREEN]
    )
    return box3, box4, box5, box6