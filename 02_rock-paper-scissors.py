#!/usr/bin/env python3
#
# Copyright (c) 2021, xphade <github.com/xphade>
# SPDX-License-Identifier: MIT

import time
from typing import Dict

from aoc_utils import get_input_path, print_elapsed_time

# Both groups have unique elements and specify their scores.
ROCK = 1
PAPER = 2
SCISSORS = 3

LOSE = 0
DRAW = 3
WIN = 6

STRATEGY_MAP: Dict[str, int] = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSORS,
    "X": ROCK,
    "Y": PAPER,
    "Z": SCISSORS,
}

RESULT_MAP: Dict[str, int] = {"X": LOSE, "Y": DRAW, "Z": WIN}


def calculate_game_score(my_play: int, opponent_play: int) -> int:
    if my_play == opponent_play:
        return DRAW

    if my_play == ROCK:
        return WIN if opponent_play == SCISSORS else LOSE
    elif my_play == PAPER:
        return WIN if opponent_play == ROCK else LOSE
    else:  # SCISSORS
        return WIN if opponent_play == PAPER else LOSE


def calculate_total_score(my_play: int, opponent_play: int) -> int:
    return my_play + calculate_game_score(my_play, opponent_play)


def get_actual_play(opponent_play: int, required_result: int) -> int:
    if required_result == DRAW:
        return opponent_play

    if opponent_play == ROCK:
        return PAPER if required_result == WIN else SCISSORS
    elif opponent_play == PAPER:
        return SCISSORS if required_result == WIN else ROCK
    else:  # SCISSORS
        return ROCK if required_result == WIN else PAPER


def main():
    data_path = get_input_path("Day 02: Rock Paper Scissors")
    with open(data_path, "r") as file:
        games = [line.split(" ") for line in file.read().splitlines()]

    start = time.monotonic()
    assumed_total_score = actual_total_score = 0
    for game in games:
        opponent_play = STRATEGY_MAP[game[0]]
        assumed_play = STRATEGY_MAP[game[1]]
        assumed_total_score += calculate_total_score(assumed_play, opponent_play)

        required_result = RESULT_MAP[game[1]]
        actual_play = get_actual_play(opponent_play, required_result)
        actual_total_score += calculate_total_score(actual_play, opponent_play)
    stop = time.monotonic()

    print(f"Total score according to assumed strategy: {assumed_total_score}")
    print(f"Total score according to actual strategy: {actual_total_score}")
    print_elapsed_time(start, stop)


if __name__ == "__main__":
    main()
