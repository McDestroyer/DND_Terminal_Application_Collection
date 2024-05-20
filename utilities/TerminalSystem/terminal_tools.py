import color


def bounded_text_formatter(message: tuple | str | list, boundaries: dict[str, int], sep: str, end: str,
                           wrap_words: bool, center_lines: bool, cutoff_ending: str | None) -> list[str]:
    """Wrap the message to fit within the boundaries and convert it to the grid_to_add format.

    WARNING: Do not use this function to wrap text that contains color codes or some other special characters.

    Args:
        message (tuple | str | list):
            The message to wrap.
        boundaries (list[tuple[int, int]]):
            The boundaries of the text, [(top_left_y, top_left_x), (bottom_right_y, bottom_right_x)] inclusive.
        sep (str):
            The separator between each item in the message.
        end (str):
            The ending character to append to the message.
        wrap_words (bool):
            Determines if words should be wrapped intact if possible or not.
        center_lines (bool):
            Determines if the lines should be centered in the boundaries.
        cutoff_ending (str | None):
            The ending to append to the message if it is cut off.

    Returns:
        list[str]: The wrapped message.
    """
    right = boundaries["right"]
    left = boundaries["left"]
    top = boundaries["top"]
    bottom = boundaries["bottom"]

    first_line_length = right - max(0, left)
    following_line_length = right - left
    max_following_lines = top - bottom

    full_message = sep.join(message) + end

    max_line_letters = first_line_length
    printing_lines = []
    current_printing_line = ""
    current_word = ""

    for char in full_message:
        # Check if the message is too long and kill if so.
        if len(current_printing_line) >= max_line_letters and len(printing_lines) >= max_following_lines:
            current_printing_line = current_printing_line[:max_line_letters - len(cutoff_ending)] + cutoff_ending
            printing_lines.append(current_printing_line)
            break

        # Check for special characters.

        # If a newline is found, it creates a new line.
        if char == "\n":
            printing_lines.append(current_printing_line.strip())
            max_line_letters = following_line_length
            current_printing_line = ""
            current_word = ""
            continue
        # Ignore carriage returns and backspaces.
        if char == "\r":
            continue
        if char == "\b":
            continue
        if char == "\t":
            # If the tab would otherwise go over the line length, ignore it.
            if len(current_printing_line) + 4 > max_line_letters:
                # Create a new line.
                printing_lines.append(current_printing_line.strip())
                max_line_letters = following_line_length
                current_printing_line = ""
                current_word = ""
                continue
            # Add a tab if it fits.
            current_printing_line += " " * 4
            current_word = ""
            continue
        # If a space is found, it ends the current word and potentially the current line.
        if char == " ":
            # End the current word.
            current_word = ""

            # If the space would otherwise go over the line length,
            # cut it off at the end of the line and ignore it.
            if len(current_printing_line) == max_line_letters:
                # Create a new line.
                printing_lines.append(current_printing_line.strip())
                max_line_letters = following_line_length
                current_printing_line = ""
                continue

            # Add a space if it fits.
            current_printing_line += " "
            continue
        # If a regular character is found, it adds it to the current line and word.
        else:
            # If the line is full, it creates a new line with the current word or letter.
            if len(current_printing_line) == max_line_letters:
                if not wrap_words or len(current_word) > max_line_letters:
                    printing_lines.append(current_printing_line.strip())
                    max_line_letters = following_line_length
                    current_printing_line = char
                    current_word = char
                    continue

                # If the word is not too long yet, it adds it to the next line.
                current_printing_line.removesuffix(current_word)

                printing_lines.append(current_printing_line.strip())
                max_line_letters = following_line_length
                current_word += char
                current_printing_line = current_word
                continue
            # Otherwise, just add the letter to the current line and word.
            current_printing_line += char
            current_word += char
            continue

    printing_lines.append(current_printing_line.strip())

    # Do a bit of formatting (Centering text)
    if center_lines:
        for i, line in enumerate(printing_lines):
            if len(line) < following_line_length:
                if i == 0 and first_line_length < following_line_length:
                    printing_lines[i] = line.center(first_line_length)
                printing_lines[i] = line.center(following_line_length)

    return printing_lines


def assemble_display_string(display_array: list[list[list[str | list[str]]]]) -> str:
    """Assemble the display string from the display array.
    Used for printing the final step before printing the display array.

    Args:
        display_array (list[list[list[str | list[str]]]):
            The display array to convert to a string.

    Returns:
        str: The display string ready to be printed.
    """
    string_array = []
    for row in display_array:
        string = ""
        for column in row:
            string += "".join(column[1]) + column[0] + color.END
        string_array.append(string)

    return "\n".join(string_array)


def to_char_array(string: str, mods: list[str] | None = None,
                  boundaries: dict[str, int] | None = None) -> list[list[list[str | list[str]]]]:
    """Convert a string to the format used by the stuff_to_add class.

    Args:
        string (str):
            The string to convert.
        mods (list[str] | None, optional):
            The list of modifications to apply to the string.
            Defaults to [].
        boundaries (dict[str, int] | None, optional):
            The boundaries of the text, inclusive.
            Defaults to {"top": 0, "bottom": 10, "left": 0, "right": 100}.

    Returns:
        list[list[list[str | list[str]]]: The converted fancy char array int the FNGR (Fancy New Generation Rendering) format.
    """
    if mods is None:
        mods = []
    if boundaries is None:
        boundaries = {"top": 0, "bottom": 10, "left": 0, "right": 100}

    string_array = bounded_text_formatter(string, boundaries, "", "", True, False, "")
    char_array = [[[letter, mods] for letter in row] for row in string_array]

    return char_array