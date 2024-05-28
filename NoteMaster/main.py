"""
File: main.py
Name: Jason Fanger
ID: X00504571
Desc: A general note-taking app designed for DND.
"""

# These get rid of annoying errors that usually mean nothing.
# Remove non-import related ones if seriously struggling

# pylint: disable=unused-import
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=unexpected-keyword-arg
# pylint: disable=no-member
# pylint: disable=ungrouped-imports
# pylint: disable=undefined-variable
# pylint: disable=wrong-import-position
# pylint: disable=import-error
# pylint: disable=

# This is an importer I made for all of my programs going forward, so I wouldn't have to deal with
# creating and renaming the utilities files for every program or have to deal with learning the "correct" methods.
import sys
import os


import_directory = os.path.dirname(os.path.realpath(__file__))

while "utilities" not in os.listdir(import_directory):
    import_directory = os.path.dirname(import_directory)

utilities_directory = os.path.join(import_directory, "utilities")
sys.path.append(utilities_directory)

# Optionally add if you want to use the terminal system.
inputs_directory = os.path.join(utilities_directory, "inputs")
sys.path.append(inputs_directory)
terminal_directory = os.path.join(utilities_directory, "TerminalSystem")
sys.path.append(terminal_directory)
display_objects_directory = os.path.join(terminal_directory, "DisplayObjects")
sys.path.append(display_objects_directory)
menu_directory = os.path.join(display_objects_directory, "MenuObjects")
sys.path.append(menu_directory)
helper_directory = os.path.join(terminal_directory, "HelperObjects")
sys.path.append(helper_directory)


from time import sleep, time_ns

import color

from terminal_manager import TerminalManager
from terminal_objects import TerminalObjects as TObj
from units import Units
from coordinates import Coordinate


class NoteMaster:

    file_path = "notes.txt"

    # Data Format: {
    #     "Characters": {
    #         "Me": [
    #             {
    #                 "Date Met": "01-01-1970",
    #                 "Name/Title": "Me, Emperor of the Multiverse",
    #                 "Last Seen Time": "01-01-1970",
    #                 "Last Seen Location": "Insert town here",
    #                 "Race": "Human",
    #                 "Description": "",
    #                 "Notes": [],

    # data = {}
    #
    # options = [
    #     ["1. View Notes", view_notes],
    #     ["2. Add Note", add_note],
    #     ["3. Edit Note", edit_note],
    #     ["4. Delete Note", delete_note],
    #     ["5. Exit", shut_down],
    # ]

    def __init__(self) -> None:
        """Initialize the NoteMaster object."""

        # Initialize the terminal.
        self.terminal = TerminalManager("NoteMaster", (20, 50))
        self.terminal.mouse_enabled = True

        # Set up the screen.
        self.screen_dict = dict()
        self.screen_dict["home"] = self.terminal.window_manager.add_screen("home")
        self.screen_dict["menu 1"] = self.terminal.window_manager.add_screen("menu 1")
        self.terminal.window_manager.set_current_screen("home")

        self.screen_size = self.terminal.screen_size

        self.screen = self.terminal.window_manager.current_screen

        self.frame_rate = 30
        self.frame_time = (1 / self.frame_rate) * 1_000

        # Set up the objects.
        box = TObj.TEXT_BOX(
            "Bob Box", coordinates=Coordinate(self.screen_size, 5, 30),
            size=Coordinate(self.screen_size, 10, 25),
            text="This is a box.\n I am happy!", title="Bob Box", border_color=[color.RED],
            title_mods=[color.UNDERLINE, color.BLUE, color.BACKGROUND_RED],
            color_scheme=[color.BACKGROUND_DEFAULT_COLOR, color.BRIGHT_GREEN])
        box2 = TObj.TEXT_BOX(
            "Bob Box 2", coordinates=Coordinate(self.screen_size, 11, 50, unit_x=Units.PERCENT),
            size=Coordinate(self.screen_size, 10, 50, unit_x=Units.PERCENT),
            text="This is another box. I am happy!", title="Bob Box 2", border_color=[color.RED],
            title_mods=[color.UNDERLINE, color.RED, color.BACKGROUND_RED],
            color_scheme=[color.BACKGROUND_DEFAULT_COLOR, color.BRIGHT_GREEN])

        # Add the objects to the screens.
        self.screen_dict["home"].add_object(box)
        self.screen_dict["home"].add_object(box2)

        self.terminal.input.add_keybind(self.screen_dict["home"], "move box up", "up", self.terminal.input.kb,
                                        "held", self.move_box, box, (-1, 0))
        self.terminal.input.add_keybind(self.screen_dict["home"], "move box down", "down", self.terminal.input.kb,
                                        "held", self.move_box, box, (1, 0))
        self.terminal.input.add_keybind(self.screen_dict["home"], "move box left", "left", self.terminal.input.kb,
                                        "held", self.move_box, box, (0, -1))
        self.terminal.input.add_keybind(self.screen_dict["home"], "move box right", "right", self.terminal.input.kb,
                                        "held", self.move_box, box, (0, 1))
        self.terminal.input.add_keybind(self.screen_dict["home"], "toggle screen 2", "tab", self.terminal.input.kb,
                                        "newly_pressed", self.toggle_screen_2)
        self.terminal.input.add_keybind(self.screen_dict["menu 1"], "toggle screen 2", "tab", self.terminal.input.kb,
                                        "newly_pressed", self.toggle_screen_2)

        # Update the display.
        self.terminal.refresh_screen()

    def move_box(self, _, box: TObj.TERMINAL_OBJECT, direction_mask: tuple[int, int]) -> None:
        box.coordinates = Coordinate(
            self.screen_size,
            box.coordinates.char_value_y + 1 * direction_mask[0],
            box.coordinates.char_value_x + 2 * direction_mask[1]
        )

    def toggle_screen_2(self, _) -> None:
        if self.terminal.window_manager.current_screen.name == "home":
            self.screen = self.terminal.window_manager.set_current_screen("menu 1")
        else:
            self.screen = self.terminal.window_manager.set_current_screen("home")

    def main_loop(self) -> None:
        """Main"""

        # box = self.screen.get_object_by_name("Bob Box")
        box2 = self.screen.get_object_by_name("Bob Box 2")
        past_times = []  # For debugging and timing purposes.

        self.screen = self.terminal.window_manager.set_current_screen("home")

        while True:
            start_time = time_ns()
            self.terminal.loop()
            loop_time = (time_ns() - start_time) / 1_000_000

            # Quit if the escape key is pressed.
            if self.terminal.input.kb.is_newly_pressed("esc"):
                break

            # Test mouse over.
            if box2.mouse_over:
                box2.text = str(box2.mouse_over)
            else:
                box2.text = "This is another box. I am happy!"

            # Update the display.
            self.terminal.refresh_screen()

            self.terminal.cursor.set_pos(0, self.screen_size[1] + 1)
            print(" " * self.screen_size[1], end="\r", flush=False)
            # print(logo_box.im)

            # loop_time = (time_ns() - start_time) / 1_000_000
            if len(past_times) > 100:
                past_times.pop(0)
            past_times.append(loop_time)
            past_sum = 0
            for past_time in past_times:
                past_sum += past_time

            self.terminal.cursor.set_pos(0, self.screen_size[1] + 1)
            print(" " * self.screen_size[1], end="\r", flush=False)
            print(loop_time, end=" ms ", flush=False)
            print(past_sum / len(past_times), end=" average ms\r", flush=True)

            # Sleep to avoid letting the display fall behind.
            # self.terminal.cursor.set_pos(0, self.screen_size[1] + 1)
            # print(" " * self.screen_size[1], end="\r", flush=False)
            # print(f"Loop: {loop_time}/{self.frame_time} ms", end=" ", flush=False)
            # print(f"Sleeping: {self.frame_time - loop_time} ms", end="", flush=True)
            # if loop_time < self.frame_time:
            #     sleep((self.frame_time - loop_time) / 1_000)


if __name__ == "__main__":
    note_master = None
    try:
        note_master = NoteMaster()
        note_master.main_loop()
    # :P
    except KeyboardInterrupt:
        note_master.terminal.quit()
