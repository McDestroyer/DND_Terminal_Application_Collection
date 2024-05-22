"""A series of cursor moving commands with a built-in cursor tracker:

    cursor_up(): Moves the cursor up a given number of lines (Default: 1).
    cursor_down(): Moves the cursor down a given number of lines (Default: 1).
    cursor_left(): Moves the cursor left a given number of lines (Default: 1).
    cursor_right(): Moves the cursor right a given number of lines (Default: 1).

    beginning(): Moves the cursor to the beginning of the current line.

    clear_line_after(): Clear the current line after the cursor.
    clear_line_before(): Clear the current line before the cursor.
    clear_line(): Clear the current line from the beginning.

    clear_screen_after(): Clear the screen after the cursor.
    clear_screen_before(): Clear the screen before the cursor.
    clear_screen(): Clear the entire screen.

    replace_current(): Identical to clear_line() but with a different _name.
    replace_previous(): Move the curser to the previous line and clears it to allow overwriting.

    save(): Save the current position of the cursor. Can be loaded again using load().
    load(): Load the previously saved cursor position. Position can be saved with save().
    get_saved_pos(): Get the saved cursor position.

    set_pos(): Set the position of the cursor to specific _coordinates.
    get_pos(): Get the current position of the cursor.

    cursor_print(): Print _text at the current cursor position.
"""

import color


class Cursor:

    def __init__(self) -> None:
        """Initialize the Cursor object."""
        self.screen_width = 1
        self.screen_height = 1
        self.hidden = False
        self.screen_saved = False
        self.set_pos()
        self.cursor_pos = [1, 1]
        self.cursor_pos_saved = None

    def set_screen(self, screen: tuple[int, int]) -> None:
        """Set the dimensions of the screen.

        Args:
            screen (tuple[int, int]):
                The dimensions of the screen [width, height].
        """
        self.screen_width = screen[0]
        self.screen_height = screen[1]

    # Cursor Movement

    def cursor_up(self, num: int = 1) -> None:
        """Move the cursor a number of spaces up.

        Args:
            num (int, optional):
                The number of spaces to move.
                Defaults to 1.
        """
        print(f"\033[{num}A", end="")
        self.cursor_pos[1] -= num

    def cursor_down(self, num: int = 1) -> None:
        """Move the cursor a number of spaces down.

        Args:
            num (int, optional):
                The number of spaces to move.
                Defaults to 1.
        """
        print(f"\033[{num}B", end="")
        self.cursor_pos[1] += num

    def cursor_right(self, num: int = 1) -> None:
        """Move the cursor a number of spaces right.

        Args:
            num (int, optional):
                The number of spaces to move.
                Defaults to 1.
        """
        print(f"\033[{num}C", end="")
        self.cursor_pos[0] += num

    def cursor_left(self, num: int = 1) -> None:
        """Move the cursor a number of spaces left.

        Args:
            num (int, optional):
                The number of spaces to move.
                Defaults to 1.
        """
        print(f"\033[{num}D", end="")
        self.cursor_pos[0] -= num

    # Go to line position

    def beginning(self) -> None:
        """Move the cursor to the beginning of the current line."""
        print("\r", end="")
        self.cursor_pos[0] = 0

    # def _ending():
    #     """Move the cursor to the end of the current line.
    #     Work In Progress, DOES NOT WORK!!!"""
    #     cursor_down()
    #     beginning()
    #     cursor_left()

    # Clearing single lines

    def clear_line_after(self) -> None:
        """Clear the current line after the cursor."""
        print("\033[K", end="")

    def clear_line_before(self) -> None:
        """Clear the current line before the cursor.
        Effectively replaces the preceding _text with blank spaces."""
        print("\033[1K", end="")

    def clear_line(self) -> None:
        """Clear the current line from the beginning."""
        print("\033[2K", end="")
        self.cursor_pos[0] = 0

    # Clearing _screens

    def clear_screen_after(self) -> None:
        """Clear the screen after the cursor."""
        print("\033[J", end="")

    def clear_screen_before(self) -> None:
        """Clear the screen before the cursor."""
        print("\033[1J", end="")

    def clear_screen(self) -> None:
        """Clear the entire screen."""
        print("\033[2J", end="")
        self.set_pos()

    # Prep to replace previous _text

    def replace_current(self) -> None:
        """Alternative wording to clear_line(). Literally just calls that function.
        Used in preparation to print there again."""
        self.clear_line()

    def replace_previous(self) -> None:
        """Move the cursor back one line and clears it in preparation to print on it again."""
        print("\033[F\033[K", end="")
        self.cursor_pos[1] -= 1
        self.cursor_pos[0] = 0

    # Save and load cursor position

    def save(self) -> None:
        """Save the current position of the cursor. Can be loaded again using load()."""
        print("\033[s", end="")
        self.cursor_pos_saved = self.cursor_pos

    def load(self) -> None:
        """Load the previously saved cursor position. Position can be saved with save()."""
        print("\033[u", end="")
        if self.cursor_pos_saved is None:
            return
        self.cursor_pos = self.cursor_pos_saved
        self.cursor_pos_saved = None

    def get_saved_pos(self) -> list[int]:
        """Get the saved cursor position."""
        return self.cursor_pos_saved

    # Set cursor position

    def set_pos(self, column: int = 0, line: int = 0) -> None:
        """Set the position of the cursor to specific _coordinates.

        Args:
            column (int, optional):
                The column or x-axis to set the position of the cursor to.
                Defaults to 0. (The left side of the screen)
            line (int, optional):
                The line or y-axis to set the position of the cursor to.
                Defaults to 0. (The top of the screen)
        """
        print(f"\033[{line+1};{column+1}H", end="")
        self.cursor_pos = [column, line]

    def get_pos(self) -> list[int]:
        """Get the current position of the cursor."""
        return self.cursor_pos

    # Hide and show cursor

    def hide(self) -> None:
        """Makes the cursor invisible. Can be undone with show()."""
        print("\033[?25l")
        self.hidden = True

    def show(self) -> None:
        """Makes the cursor _visible. Inverse of hide()."""
        print("\033[?25h")
        self.hidden = False

    # Save and load screen

    def load_screen(self) -> None:
        """Restores the screen after it has been wiped by save_screen() and re-saves it.
        This hides anything done between these points.
        """
        if not self.screen_saved:
            return
        print("\033[?47l")
        self.screen_saved = False

    def save_screen(self) -> None:
        """Saves the screen and clears it. Can be undone by load_screen().
        Anything done between the save and the load will be hidden.
        """
        print("\033[?47h")
        self.screen_saved = True

    # Printing

    def cursor_print(self, *message: object, letter_time: float = .0125, line_delay: float = 0, sep: str = " ",
                     end: str = "", mods: list = None, flush: bool = True, boundaries: dict[str, int] = None,
                     move_to_start: bool = False, wrap_words: bool = True, center_lines: bool = False,
                     cutoff_ending: str | None = "...", ) -> None:
        """Print _text at the current cursor position and track it. Please do not include any 0-width characters outside
        escape sequences as this will mess with the cursor tracking, and don't use \\r or \\b as I couldn't be bothered
        to make it work properly.

        Args:
            *message (str, optional):
                A message or prompt to output to the user.
                Defaults to "".
            letter_time (float, optional):
                Time delay between each letter printed.
                Defaults to .0125.
            line_delay (int, optional):
                Additional time delay between each line printed.
                Defaults to 0.
            sep (str, optional):
                String inserted between values.
                Defaults to " ".
            end (str, optional):
                String appended after the last value.
                Defaults to "".
            mods (list, optional):
                List of modifiers from the colorizer class to apply to the message.
                Defaults to [].
            flush (bool, optional):
                Determines if the _text is output immediately or not.
                Defaults to True.
            boundaries (list[int], optional):
                The boundaries of the _text, inclusive. Used to check if the _text will go off the screen,
                and if so, move the cursor to the next line.
                Defaults to {left: 0, right: screen_width, top: cursor_pos[1], bottom: screen_height}.
            move_to_start (bool, optional):
                Determines if the cursor should move to the start of the given or default boundaries before printing.
                Defaults to False.
            wrap_words (bool, optional):
                Determines if words should be wrapped intact if possible or not.
                Defaults to True.
            center_lines (bool, optional):
                Determines if the lines should be centered in the boundaries.
                Defaults to False.
            cutoff_ending (str | None, optional):
                Determines what should be appended to the message if it is cut off. If None, an error is raised upon
                the _text being cut-off.
                Defaults to "...".

        Returns:
            False if the _text cannot fit on the screen, True otherwise.
        """
        # Calculate lines required
        if boundaries is None:
            boundaries = {
                "left": 0,
                "right": self.screen_width,
                "top": self.cursor_pos[1],
                "bottom": self.screen_height
            }
        bound_keys = boundaries.keys()

        # Right
        if "right" in bound_keys and boundaries["right"] is not None:
            right = boundaries["right"]
        else:
            right = self.screen_width
            boundaries["right"] = right
        # Left
        if "left" in bound_keys and boundaries["left"] is not None:
            left = boundaries["left"]
        else:
            left = 0
            boundaries["left"] = left
        # Top
        if "top" in bound_keys and boundaries["top"] is not None:
            top = boundaries["top"]
        else:
            top = self.cursor_pos[1]
            boundaries["top"] = top
        # Bottom
        if "bottom" in bound_keys and boundaries["bottom"] is not None:
            bottom = boundaries["bottom"]
        else:
            bottom = self.screen_height
            boundaries["bottom"] = bottom

        # Move the cursor to the start of the boundaries if requested.
        if move_to_start:
            self.set_pos(top, left)

        # Having a function have a default list is "dangerous" so this serves as an equivalent if None.
        # Otherwise, prints the markup escape codes.
        for i in (mods if mods is not None else []):
            print(i, end="")

    # # Calculate the available space.
    # def line_wrap_formatter(self, message: tuple, boundaries: dict[str, int], sep: str, end: str, wrap_words: bool,
    #                         center_lines: bool, cutoff_ending: str | None) -> list[str]:
    #     """Wrap the message to fit within the boundaries.
    #
    #     Args:
    #         message (tuple):
    #             The message to wrap.
    #         boundaries (dict[str, int]):
    #             The boundaries of the _text, inclusive.
    #         sep (str):
    #             The separator between each item in the message.
    #         end (str):
    #             The ending character to append to the message.
    #         wrap_words (bool):
    #             Determines if words should be wrapped intact if possible or not.
    #         center_lines (bool):
    #             Determines if the lines should be centered in the boundaries.
    #         cutoff_ending (str | None):
    #             The ending to append to the message if it is cut off.
    #
    #     Returns:
    #         list[str]: The wrapped message.
    #     """
    #     right = boundaries["right"]
    #     left = boundaries["left"]
    #     top = boundaries["top"]
    #     bottom = boundaries["bottom"]
    #
    #     first_line_length = right - max(self.cursor_pos[0], left)
    #     following_line_length = right - left
    #     max_following_lines = top - bottom
    #
    #     # maximum_chars = max_following_lines * following_line_length + first_line_length
    #
    #     full_message = sep.join(message) + end
    #
    #     max_line_letters = first_line_length
    #     coloring = False
    #     printing_lines = []
    #     current_printing_line = ""
    #     current_word = ""
    #
    #     for char in full_message:
    #         # Check if the message is too long and kill if so.
    #         if len(current_printing_line) >= max_line_letters and len(printing_lines) >= max_following_lines:
    #             current_printing_line = current_printing_line[:max_line_letters - len(cutoff_ending)] + cutoff_ending
    #             printing_lines.append(current_printing_line)
    #             break
    #         # Checks to see if a _color_scheme code was found.
    #         if not coloring:
    #             # Check for special characters.
    #
    #             # If a newline is found, it creates a new line.
    #             if char == "\n":
    #                 printing_lines.append(current_printing_line.strip())
    #                 max_line_letters = following_line_length
    #                 current_printing_line = ""
    #                 current_word = ""
    #                 continue
    #             # Ignore carriage returns and backspaces.
    #             if char == "\r":
    #                 continue
    #             if char == "\b":
    #                 continue
    #             if char == "\t":
    #                 # If the tab would otherwise go over the line length, ignore it.
    #                 if len(current_printing_line) + 4 > max_line_letters:
    #                     # Create a new line.
    #                     printing_lines.append(current_printing_line.strip())
    #                     max_line_letters = following_line_length
    #                     current_printing_line = ""
    #                     current_word = ""
    #                     continue
    #                 # Add a tab if it fits.
    #                 current_printing_line += " " * 4
    #                 current_word = ""
    #                 continue
    #             # If a _color_scheme code is found, it sets the coloring flag to True.
    #             if char == "\033":
    #                 coloring = True
    #                 continue
    #             # If a space is found, it ends the current word and potentially the current line.
    #             if char == " ":
    #                 # End the current word.
    #                 current_word = ""
    #
    #                 # If the space would otherwise go over the line length,
    #                 # cut it off at the end of the line and ignore it.
    #                 if len(current_printing_line) == max_line_letters:
    #                     # Create a new line.
    #                     printing_lines.append(current_printing_line.strip())
    #                     max_line_letters = following_line_length
    #                     current_printing_line = ""
    #                     continue
    #
    #                 # Add a space if it fits.
    #                 current_printing_line += " "
    #                 continue
    #             # If a regular character is found, it adds it to the current line and word.
    #             else:
    #                 # If the line is full, it creates a new line with the current word or letter.
    #                 if len(current_printing_line) == max_line_letters:
    #                     if not wrap_words or len(current_word) > max_line_letters:
    #                         printing_lines.append(current_printing_line.strip())
    #                         max_line_letters = following_line_length
    #                         current_printing_line = char
    #                         current_word = char
    #                         continue
    #
    #                     # If the word is not too long yet, it adds it to the next line.
    #                     current_printing_line.removesuffix(current_word)
    #
    #                     printing_lines.append(current_printing_line.strip())
    #                     max_line_letters = following_line_length
    #                     current_word += char
    #                     current_printing_line = current_word
    #                     continue
    #                 # Otherwise, just add the letter to the current line and word.
    #                 current_printing_line += char
    #                 current_word += char
    #                 continue
    #         # If a _color_scheme code was found, it checks for the end of the code.
    #         else:
    #             if char == "m":
    #                 coloring = False
    #             continue
    #
    #     # Do a bit of formatting (Centering _text)
    #     if center_lines:
    #         for i, line in enumerate(printing_lines):
    #             if len(line) < following_line_length:
    #                 if i == 0 and first_line_length < following_line_length:
    #                     printing_lines[i] = line.center(first_line_length)
    #                 printing_lines[i] = line.center(following_line_length)
    #
    #     return printing_lines

    # def _text(*message: object, letter_time: float = .025, line_delay: float = 0,
    #          sep: str = " ", end: str = "\n", mods: list = None, flush: bool = True) -> None:
    #     """Mimic print() but with more functionality and a default time delay.
    #
    #     Args:
    #
    #     """
    #     # Having a function have a default list is "dangerous" so this serves as an equivalent if None.
    #     # Otherwise, prints the markup escape codes.
    #     for i in (mods if not mods is None else []):
    #         print(i, end="")
    #
    #     # Due to anything in the message slot being turned into a tuple, this checks to see if the 1st
    #     # item is a tuple as that usually indicates that it was passed on from intext() or one of the
    #     # 'put() functions. It also serves to allow for easy listing of items in a list.
    #     # Does not run if there's more than one argument, so adding a "" and setting sep to "" would
    #     # override this.
    #     if len(message) == 1:
    #         if isinstance(message[0], (tuple, list)):
    #             message = message[0]
    #
    #     # The speed multiplier. Added fow using esc to speed up outputs.
    #     speed = 1
    #
    #     # Cycles through and prints each letter with delay.
    #     for j, i in enumerate(message):
    #
    #         if not j == 0:
    #             for letter in sep:
    #
    #                 if keybd.is_currently_pressed("esc"):
    #                     speed = 0
    #
    #                 print(letter, end='', flush=flush)
    #                 sleep(letter_time * speed)
    #         for letter in str(i):
    #
    #             if keybd.is_currently_pressed("esc"):
    #                 speed = 0
    #
    #             print(letter, end='', flush=flush)
    #             sleep(letter_time * speed)
    #
    #     # Cleans up and optionally waits at the end.
    #     sleep(line_delay * speed)
    #     if not mods is None:
    #         print(_color_scheme.END, end="")
    #     print(end=end)


# Testing
if __name__ == "__main__":
    cursor = Cursor()
    cursor.cursor_print("Hello World, this Is A Test Of The Cursor Print Function",
                        letter_time=.025, line_delay=0, sep=" ", end="\n", mods=[color.BOLD, color.GREEN], flush=True,
                        boundaries={"right": 50, "left": 0, "top": 0, "bottom": 20}, move_to_start=True,
                        wrap_words=True, center_lines=True, cutoff_ending="...")
    print("printed")
    # print("Hello"*5, end="", flush=True)
    # time.sleep(3)
    # cursor.cursor_left(10)
    # print("Hi", end="")
    # # cursor._ending()
    # print("Pizza")
    # print(len(""))
    # print(len(_color_scheme.BLUE))
    # print(_color_scheme.BLUE)
    # print(len(f"{_color_scheme.BLUE}"))
    # print(f"{_color_scheme.RED}red{_color_scheme.BLUE}blue{_color_scheme.BRIGHT_WHITE}bright_white{_color_scheme.END}end")
    # print(f"""
    # {_color_scheme.BLACK}black
    # {_color_scheme.BRIGHT_BLACK}bright_black
    # {_color_scheme.WHITE}white
    # {_color_scheme.DEFAULT_COLOR}default
    # {_color_scheme.BRIGHT_WHITE}bright_white""")
    # print(len("\n"))
    # for letter in _color_scheme.BLUE:
    #     print(letter, end=" ")
    # print()
