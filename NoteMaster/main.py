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
terminal_directory = os.path.join(utilities_directory, "TerminalSystem")
sys.path.append(terminal_directory)
display_objects_directory = os.path.join(terminal_directory, "DisplayObjects")
sys.path.append(display_objects_directory)
helper_directory = os.path.join(terminal_directory, "HelperObjects")
sys.path.append(helper_directory)


import audio
from personal_functions import *
from time import sleep, time, time_ns
import color
from cursor import Cursor

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
        self.cursor = Cursor()
        self.cursor.clear_screen()
        self.cursor.set_pos()

        # Initialize the terminal.
        self.terminal = TerminalManager((20, 50))

        # Set up the screen.
        self.terminal.window_manager.add_screen("home")
        self.terminal.window_manager.set_current_screen("home")

        self.screen_size = self.terminal.screen_size

        self.screen = self.terminal.window_manager.current_screen

        self.frame_rate = 20
        self.frame_time = 1 / self.frame_rate

        # Set up the objects.
        box = TObj.TEXT_BOX(
            "Bob Box", coordinates=Coordinate(self.screen_size, 5, 30),
            size=Coordinate(self.screen_size, 10, 20),
            text="This is a box. I am happy!", title="Bob Box", border_color=color.RED,
            # text="This is a box. I am happy! Unfortunately, as a test my master has filled me with far too much text for me to possibly contain. What do you think will happen? Will the word-wrapping succeed and put an ellipsis somewhere at the end?", title="Bob Box", border_color=color.RED,
            title_mods=[color.BOLD, color.UNDERLINE, color.BLUE, color.BACKGROUND_RED],
            color_scheme=[color.BACKGROUND_BLACK, color.BRIGHT_GREEN])
        box2 = TObj.TEXT_BOX(
            "Bob Box 2", coordinates=Coordinate(self.screen_size, 11, 50),
            size=Coordinate(self.screen_size, 10, 50, unit_x=Units.PERCENT),
            text="This is another box. I am happy!", title="Bob Box 2", border_color=color.RED,
            title_mods=[color.BOLD, color.UNDERLINE, color.BLUE, color.BACKGROUND_RED],
            color_scheme=[color.BACKGROUND_BLACK, color.BRIGHT_GREEN])

        # Add the objects to the screen.
        self.screen.add_object(box)
        self.screen.add_object(box2)

        # Update the _display.
        self.screen.update_display()
        self.terminal.window_manager.refresh_screen()

        # _text("Greetings! Welcome to NoteMaster!", mods=[color.BOLD, color.GREEN])

    def main_loop(self) -> None:
        """Main"""

        box = self.screen.get_object_by_name("Bob Box")
        past_times = []

        while True:
            start_time = time_ns()
            # Quit if the escape key is pressed.
            if self.terminal.kb.is_newly_pressed("esc"):
                break

            # Move the box around.
            if self.terminal.kb.is_held("up"):
                box.coordinates = Coordinate(
                    self.terminal.screen_size,
                    box.coordinates.values["CHAR"][0] - 1,
                    box.coordinates.values["CHAR"][1]
                )
            if self.terminal.kb.is_held("down"):
                box.coordinates = Coordinate(
                    self.terminal.screen_size,
                    box.coordinates.values["CHAR"][0] + 1,
                    box.coordinates.values["CHAR"][1]
                )
            if self.terminal.kb.is_held("left"):
                box.coordinates = Coordinate(
                    self.terminal.screen_size,
                    box.coordinates.values["CHAR"][0],
                    box.coordinates.values["CHAR"][1] - 2
                )
            if self.terminal.kb.is_held("right"):
                box.coordinates = Coordinate(
                    self.terminal.screen_size,
                    box.coordinates.values["CHAR"][0],
                    box.coordinates.values["CHAR"][1] + 2
                )

            # Make the box flash.
            if time() % .75 < 0.05:
                if box.visible:
                    box.visible = False
            elif not box.visible:
                box.visible = True

            # Update the display.
            self.screen.update_display()
            self.terminal.window_manager.refresh_screen()

            loop_time = (time_ns() - start_time) / 1_000_000
            # if len(past_times) > 100:
            #     past_times.pop(0)
            # past_times.append(loop_time)
            # past_sum = 0
            # for past_time in past_times:
            #     past_sum += past_time

            # self.cursor.set_pos(0, self.screen_size[1] + 1)
            # print(" " * self.screen_size[1], end="\r", flush=False)
            # print(loop_time, end=" ms ", flush=False)
            # print(past_sum / len(past_times), end=" average ms\r", flush=True)

            # Sleep to avoid letting the display fall behind.
            if loop_time < self.frame_time:
                sleep(self.frame_time - loop_time)


if __name__ == "__main__":
    try:
        note_master = NoteMaster()
        note_master.main_loop()
    # :P
    except KeyboardInterrupt:
        # The 2nd try/except clears all formatting without wasting time,
        # so you don't have to wait for it to scroll out.
        audio.stop_music()
        try:
            text("\n\nCTRL + C?! You're killing me!!! Aww, fine... Bye!",
                 letter_time=0.0025, mods=[color.ERROR])
            sys.exit()
        except KeyboardInterrupt:
            text()
            sys.exit()
