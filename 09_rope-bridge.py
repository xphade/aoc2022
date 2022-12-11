#!/usr/bin/env python3
#
# Copyright (c) 2022, xphade <github.com/xphade>
# SPDX-License-Identifier: MIT

import time
from enum import Enum
from typing import List, NamedTuple, Optional, Set, Tuple

from aoc_utils import get_input_path, print_elapsed_time


class Direction(Enum):
    R = RIGHT = 1
    L = LEFT = 2
    U = UP = 3
    D = DOWN = 4


class Move(NamedTuple):
    direction: Direction
    steps: int


Coordinate = Tuple[int, int]


def are_touching(head: Coordinate, tail: Coordinate) -> bool:
    return abs(head[0] - tail[0]) < 2 and abs(head[1] - tail[1]) < 2


def move_head(head: Coordinate, direction: Direction) -> Coordinate:
    if direction == Direction.RIGHT:
        return (head[0] + 1, head[1])
    elif direction == Direction.LEFT:
        return (head[0] - 1, head[1])
    elif direction == Direction.UP:
        return (head[0], head[1] + 1)
    elif direction == Direction.DOWN:
        return (head[0], head[1] - 1)
    else:
        assert False  # Should never happen


def move_tail(head: Coordinate, tail: Coordinate) -> Optional[Coordinate]:
    if are_touching(head, tail):
        return None

    horizontally = head[0] != tail[0]
    vertically = head[1] != tail[1]

    if horizontally:
        new_x = tail[0] + (1 if head[0] > tail[0] else -1)
        tail = (new_x, tail[1])
    if vertically:
        new_y = tail[1] + (1 if head[1] > tail[1] else -1)
        tail = (tail[0], new_y)

    return tail


def apply_step(rope: List[Coordinate], direction: Direction):
    rope[0] = move_head(rope[0], direction)
    for i in range(0, len(rope) - 1):
        if (tail := move_tail(rope[i], rope[i + 1])) is not None:
            rope[i + 1] = tail


def move_rope(rope: List[Coordinate], moves: List[Move]) -> Set[Coordinate]:
    visited: Set[Coordinate] = {rope[-1]}
    for move in moves:
        for _ in range(move.steps):
            apply_step(rope, move.direction)
            visited.add(rope[-1])
    return visited


def main():
    data_path = get_input_path("Day 09: Rope Bridge")
    with open(data_path, "r") as file:
        lines = [line.split() for line in file.read().splitlines()]
        moves = [Move(Direction[d], int(s)) for d, s in lines]

    start = time.monotonic()
    num_visited_two_knots = len(move_rope([(0, 0) for _ in range(2)], moves))
    num_visited_ten_knots = len(move_rope([(0, 0) for _ in range(10)], moves))
    stop = time.monotonic()

    print(f"Positions visited by tail of two-knot rope: {num_visited_two_knots}")
    print(f"Positions visited by tail of ten-knot rope: {num_visited_ten_knots}")
    print_elapsed_time(start, stop)


if __name__ == "__main__":
    main()
