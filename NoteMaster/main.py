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

import_directory = os.path.join(import_directory, "utilities")
sys.path.append(import_directory)

# Optionally add if you want to use the terminal system.
import_directory = os.path.join(import_directory, "TerminalSystem")
sys.path.append(import_directory)


import audio
from terminal_manager import TerminalManager as terminal
from personal_functions import *


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

    data = {}

    options = [
        ["1. View Notes", view_notes],
        ["2. Add Note", add_note],
        ["3. Edit Note", edit_note],
        ["4. Delete Note", delete_note],
        ["5. Exit", shut_down],
    ]

    def __init__(self) -> None:
        """Initialize the NoteMaster object."""
        text("Greetings! Welcome to NoteMaster!", mods=[color.BOLD, color.GREEN])

    def main_loop(self) -> None:
        """Main"""
        text("What would you like to do?", mods=[color.BOLD, color.BLUE])
        text(self.options, mods=[color.BOLD, color.GREEN])

    def print_options(self) -> None:
        """Print the options."""
        for option in self.options:
            text(option[0], mods=[color.BOLD, color.GREEN])


if __name__ == "__main__":
    try:
        # Clears the screen to allow for a cleaner experience before running the program.
        cursor.clear_screen()
        cursor.set_pos()

        system = NoteMaster()
        system.main_loop()
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
