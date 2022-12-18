#!/usr/bin/env python3
#
# Copyright (c) 2022, xphade <github.com/xphade>
# SPDX-License-Identifier: MIT

import re
import time
from typing import List, Set, Tuple

from aoc_utils import get_input_path, print_elapsed_time

Coordinate = Tuple[int, int]
Map = Set[Coordinate]

COORDINATE_RGX = re.compile(r"(\d+),(\d+)")
SAND_START_LOCATION: Coordinate = (500, 0)


def generate_line(lhs: Coordinate, rhs: Coordinate) -> List[Coordinate]:
    def generate_1d_line(lhs: int, rhs: int) -> List[int]:
        if lhs < rhs:
            return list(range(lhs, rhs + 1))
        else:
            return list(range(rhs, lhs + 1))

    x_coords = generate_1d_line(lhs[0], rhs[0])
    y_coords = generate_1d_line(lhs[1], rhs[1])

    if len(x_coords) == 1:
        x_coords = x_coords * len(y_coords)
    elif len(y_coords) == 1:
        y_coords = y_coords * len(x_coords)

    return list(zip(x_coords, y_coords))


def generate_map(scans: List[str]) -> Map:
    rock_structures: Map = set()
    for scan in scans:
        coordinates = [(int(x), int(y)) for x, y in COORDINATE_RGX.findall(scan)]
        for i in range(1, len(coordinates)):
            rock_structures.update(generate_line(coordinates[i - 1], coordinates[i]))
    return rock_structures


def simulate_one_step(
    position: Coordinate, rock_structures: Map, sand_at_rest: Map
) -> Coordinate:
    below = (position[0], position[1] + 1)
    lower_left = (position[0] - 1, position[1] + 1)
    lower_right = (position[0] + 1, position[1] + 1)

    if below not in rock_structures and below not in sand_at_rest:
        return below
    elif lower_left not in rock_structures and lower_left not in sand_at_rest:
        return lower_left
    elif lower_right not in rock_structures and lower_right not in sand_at_rest:
        return lower_right

    return position


def simulate(rock_structures: Map) -> int:
    sand_at_rest: Map = set()
    sand_position = SAND_START_LOCATION
    max_y = max([coord[1] for coord in rock_structures])

    while True:
        if sand_position[1] == max_y:
            break

        new_position = simulate_one_step(sand_position, rock_structures, sand_at_rest)
        if new_position == sand_position:
            sand_at_rest.add(sand_position)
            sand_position = SAND_START_LOCATION
            continue

        sand_position = new_position

    return len(sand_at_rest)


def simulate_with_floor(rock_structures: Map) -> int:
    sand_at_rest: Map = set()
    sand_position = SAND_START_LOCATION
    max_y = max([coord[1] for coord in rock_structures])

    while True:
        if SAND_START_LOCATION in sand_at_rest:
            break

        new_position = simulate_one_step(sand_position, rock_structures, sand_at_rest)
        if new_position == sand_position or new_position[1] == (max_y + 1):
            sand_at_rest.add(new_position)
            sand_position = SAND_START_LOCATION
            continue

        sand_position = new_position

    return len(sand_at_rest)


def main():
    data_path = get_input_path("Day 14: Regolith Reservoir")
    with open(data_path, "r") as file:
        scans = file.read().splitlines()

    start = time.monotonic()
    rock_structures = generate_map(scans)
    units_at_rest = simulate(rock_structures)
    units_at_rest_after_blocked = simulate_with_floor(rock_structures)
    stop = time.monotonic()

    print(f"Sand units at rest until free-falling: {units_at_rest}")
    print(f"Sand units at rest until source is blocked: {units_at_rest_after_blocked}")
    print_elapsed_time(start, stop)


if __name__ == "__main__":
    main()
