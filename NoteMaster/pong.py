"""
File: pong.py
Name: Jason Fanger
ID: X00504571
Desc: Pong game.
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
from random import random

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


class System:
    def __init__(self) -> None:

        # Initialize the terminal.
        self.terminal = TerminalManager("NoteMaster", (20, 50), 20)
        self.terminal.mouse_enabled = False

        # Set up the screen.
        self.screen_dict = dict()
        # self.screen_dict["menu"] = self.terminal.window_manager.add_screen("menu")
        self.screen_dict["game"] = self.terminal.window_manager.add_screen("game")
        self.terminal.window_manager.set_current_screen("game")

        self.screen_size = self.terminal.screen_size

        self.screen = self.terminal.window_manager.current_screen

        paddle_height = 15

        # Set up the objects.
        left_paddle = TObj.TERMINAL_OBJECT(
            "Left Paddle", coordinates=Coordinate(self.screen_size, 50, 2,
                                                  unit_y=Units.PERCENT),
            size=Coordinate(self.screen_size, int(self.screen_size[0]*paddle_height / 100), 1),
            contents=[[["█", [color.RED]]] for _ in range(int(self.screen_size[0]*paddle_height / 100))],
        )
        right_paddle = TObj.TERMINAL_OBJECT(
            "Right Paddle", coordinates=Coordinate(self.screen_size, 50, self.screen_size[1] - 3,
                                                   unit_y=Units.PERCENT),
            size=Coordinate(self.screen_size, int(self.screen_size[0]*paddle_height / 100), 1),
            contents=[[["█", [color.BRIGHT_GREEN]]] for _ in range(int(self.screen_size[0]*paddle_height / 100))],
        )
        ball = TObj.TERMINAL_OBJECT(
            "Bob Box 2", coordinates=Coordinate(self.screen_size, 50, 50,
                                                unit_y=Units.PERCENT, unit_x=Units.PERCENT),
            size=Coordinate(self.screen_size, 1, 2, unit_x=Units.PERCENT),
            contents=[[["█", [color.BRIGHT_WHITE]] for _ in range(2)]],
        )
        score = TObj.TEXT_BOX(
            "Score", coordinates=Coordinate(self.screen_size, 1, 50, unit_x=Units.PERCENT),
            size=Coordinate(self.screen_size, 1, 7),
            text="0 | 0", border_material=None, center_text=True,
            color_scheme=[color.BACKGROUND_BLACK, color.BRIGHT_YELLOW])

        # Add the objects to the screens.
        self.screen_dict["game"].add_object(left_paddle)
        self.screen_dict["game"].add_object(right_paddle)
        self.screen_dict["game"].add_object(ball)
        self.screen_dict["game"].add_object(score)

        # Update the display.
        self.terminal.loop()
        self.terminal.refresh_screen()

    def main_loop(self) -> None:
        self.screen = self.terminal.window_manager.current_screen

        left_paddle = self.screen.get_object_by_name("Left Paddle")
        right_paddle = self.screen.get_object_by_name("Right Paddle")
        ball = self.screen.get_object_by_name("Bob Box 2")
        score = self.screen.get_object_by_name("Score")

        ball_velocity = [0, 1]
        ball_position = [ball.coordinates.char_value_y, ball.coordinates.char_value_x]
        paddle_speed = 1
        score_values = [0, 0]
        score.text = f"{score_values[0]} | {score_values[1]}"

        while True:
            self.terminal.loop()

            # Move the paddles.
            left_paddle_speed = 0
            right_paddle_speed = 0
            if self.terminal.input.keyboard_states["w"]["pressed"]:
                left_paddle_speed -= paddle_speed
                left_paddle.coordinates = Coordinate(
                    self.screen_size,
                    max(left_paddle.coordinates.char_value_y - paddle_speed, 0),
                    left_paddle.coordinates.char_value_x
                )
            if self.terminal.input.keyboard_states["s"]["pressed"]:
                left_paddle_speed += paddle_speed
                left_paddle.coordinates = Coordinate(
                    self.screen_size,
                    min(left_paddle.coordinates.char_value_y + paddle_speed, self.screen_size[0] - left_paddle.size.char_value_y),
                    left_paddle.coordinates.char_value_x
                )
            if self.terminal.input.keyboard_states["up"]["pressed"]:
                right_paddle_speed -= paddle_speed
                right_paddle.coordinates = Coordinate(
                    self.screen_size,
                    max(right_paddle.coordinates.char_value_y - paddle_speed, 0),
                    right_paddle.coordinates.char_value_x
                )
            if self.terminal.input.keyboard_states["down"]["pressed"]:
                right_paddle_speed += paddle_speed
                right_paddle.coordinates = Coordinate(
                    self.screen_size,
                    min(right_paddle.coordinates.char_value_y + paddle_speed, self.screen_size[0] - right_paddle.size.char_value_y),
                    right_paddle.coordinates.char_value_x
                )

            # Move the ball.
            ball_position[0] += ball_velocity[0]
            ball_position[1] += ball_velocity[1]

            # Vertical
            if ball_position[0] <= 0 or ball_position[0] >= self.screen_size[0] - 1:
                ball_velocity[0] *= -1 + (random() - .5) * 0.5  # Add some randomness (+- 0.25)
                ball_position[0] = 0 if ball_position[0] <= 0 else self.screen_size[0] - 1

            # Left paddle
            if int(ball_position[1]) <= 2:
                if left_paddle.coordinates.char_value_y <= int(ball_position[0]) and \
                        int(ball_position[0]) + 1 <= left_paddle.coordinates.char_value_y + left_paddle.size.char_value_y:
                    ball_velocity[1] *= -1
                    # Add some randomness (+ 0-0.25)
                    ball_velocity[1] += random() * 0.25 * (ball_velocity[1] / abs(ball_velocity[1]))
                    ball_velocity[0] += left_paddle_speed / 2
                    ball_position[1] = left_paddle.coordinates.char_value_x + 1
                else:
                    score_values[1] += 1
                    score.text = f"{score_values[0]} | {score_values[1]}"
                    ball_position = [self.screen_size[0] / 2, self.screen_size[1] / 2]
                    ball_velocity = [.5, -1]
            # Right paddle
            if int(ball_position[1]) >= self.screen_size[1] - 4:
                if right_paddle.coordinates.char_value_y <= int(ball_position[0]) and \
                        int(ball_position[0]) + 1 <= right_paddle.coordinates.char_value_y + right_paddle.size.char_value_y:
                    ball_velocity[1] *= -1
                    # Add some randomness (+ 0-0.25)
                    ball_velocity[1] += random() * 0.25 * (ball_velocity[1] / abs(ball_velocity[1]))
                    ball_velocity[0] += right_paddle_speed / 2
                    ball_position[1] = right_paddle.coordinates.char_value_x - 2
                else:
                    score_values[0] += 1
                    score.text = f"{score_values[0]} | {score_values[1]}"
                    ball_position = [self.screen_size[0] / 2, self.screen_size[1] / 2]
                    ball_velocity = [.5, 1]

            ball.coordinates = Coordinate(
                self.screen_size,
                int(ball_position[0]),
                int(ball_position[1]),
            )

            self.terminal.refresh_screen()

            self.terminal.cursor.set_pos(self.screen_size[1] + 1, 0)
            print(" " * self.screen_size[1], end="\r", flush=False)
            print(f"Ball: {ball_position} | {ball_velocity}", end="", flush=False)
            print(f"Right Paddle: {right_paddle.coordinates.char_value_y}", end="", flush=True)


if __name__ == "__main__":
    system = None
    try:
        system = System()
        system.main_loop()
    # :P
    except KeyboardInterrupt:
        system.terminal.quit()
