#!/usr/bin/env python3
#
# Copyright (c) 2022, xphade <github.com/xphade>
# SPDX-License-Identifier: MIT

import string
import time
from typing import List, NamedTuple, Optional, Tuple

from aoc_utils import get_input_path, print_elapsed_time

Map = List[List[str]]


class Coordinate(NamedTuple):
    row: int
    col: int


class Node(NamedTuple):
    position: Coordinate
    steps: int


def find_start_and_end(height_map: Map) -> Tuple[Coordinate, Coordinate]:
    start_pos = end_pos = None
    for r in range(len(height_map)):
        for c in range(len(height_map[r])):
            if height_map[r][c] == "S":
                start_pos = Coordinate(row=r, col=c)
            elif height_map[r][c] == "E":
                end_pos = Coordinate(row=r, col=c)
    assert start_pos is not None and end_pos is not None
    return start_pos, end_pos


def get_height_step(current_height: str, next_height: str) -> int:
    current_height = "a" if current_height == "S" else current_height
    current_height = "z" if current_height == "E" else current_height
    next_height = "a" if next_height == "S" else next_height
    next_height = "z" if next_height == "E" else next_height

    cur_val = string.ascii_letters.index(current_height)
    next_val = string.ascii_letters.index(next_height)
    return next_val - cur_val


def get_adjacent_coordinates(height_map: Map, cur_pos: Coordinate) -> List[Coordinate]:
    adjacent_coords: List[Coordinate] = []
    steps = [Coordinate(-1, 0), Coordinate(0, 1), Coordinate(1, 0), Coordinate(0, -1)]

    for step in steps:
        r = cur_pos.row + step.row
        c = cur_pos.col + step.col
        if r < 0 or c < 0 or r >= len(height_map) or c >= len(height_map[0]):
            continue
        if get_height_step(height_map[cur_pos.row][cur_pos.col], height_map[r][c]) <= 1:
            adjacent_coords.append(Coordinate(row=r, col=c))

    return adjacent_coords


def bfs(height_map: Map, start_pos: Coordinate, end_pos: Coordinate) -> Optional[int]:
    queue = [Node(start_pos, 0)]
    visited = {start_pos}

    while len(queue) > 0:
        current_node = queue.pop(0)
        if current_node.position == end_pos:
            return current_node.steps

        for coordinate in get_adjacent_coordinates(height_map, current_node.position):
            if coordinate in visited:
                continue
            visited.add(coordinate)
            queue.append(Node(coordinate, current_node.steps + 1))

    return None


def generate_possible_starting_points(height_map: Map) -> List[Coordinate]:
    starting_points: List[Coordinate] = []
    for r in range(len(height_map)):
        for c in range(len(height_map[r])):
            if height_map[r][c] == "a":
                starting_points.append(Coordinate(r, c))
    return starting_points


def find_best_starting_point(
    height_map: Map, start_pos: Coordinate, end_pos: Coordinate
) -> Optional[int]:
    starting_points = generate_possible_starting_points(height_map)
    current_best = bfs(height_map, start_pos, end_pos)

    for start in starting_points:
        steps = bfs(height_map, start, end_pos)
        if current_best is None or (steps is not None and steps < current_best):
            current_best = steps

    return current_best


def main():
    data_path = get_input_path("Day 12: Hill Climbing Algorithm")
    with open(data_path, "r") as file:
        height_map: Map = [[c for c in line] for line in file.read().splitlines()]

    start = time.monotonic()
    start_point, end_point = find_start_and_end(height_map)
    steps = bfs(height_map, start_point, end_point)
    best_steps = find_best_starting_point(height_map, start_point, end_point)
    assert steps is not None and best_steps is not None
    stop = time.monotonic()

    print(f"Steps to goal from original starting point: {steps}")
    print(f"Steps to goal from best possible starting point: {best_steps}")
    print_elapsed_time(start, stop)


if __name__ == "__main__":
    main()
