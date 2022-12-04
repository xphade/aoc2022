#!/usr/bin/env python3
#
# Copyright (c) 2022, xphade <github.com/xphade>
# SPDX-License-Identifier: MIT

import time
from typing import List, Tuple

from aoc_utils import get_input_path, print_elapsed_time


def preprocess_input(contents: List[str]) -> List[Tuple[int]]:
    assignment_pairs = []
    for line in contents:
        range_pair = [tuple(map(int, rng.split("-"))) for rng in line.split(",")]
        assignment_pairs.append(range_pair)
    return assignment_pairs


def count_fully_contained_ranges(pairs: List[Tuple[int]]) -> int:
    # Sort pairs by length.
    sorted_pairs = [sorted(pair, key=lambda x: x[1] - x[0]) for pair in pairs]
    return sum(x[0] >= y[0] and x[1] <= y[1] for x, y in sorted_pairs)


def count_overlapping_ranges(pairs: List[Tuple[int]]) -> int:
    # Sort pairs by first index (small before big).
    sorted_pairs = [sorted(pair, key=lambda x: x[0]) for pair in pairs]
    return sum((x[1] - y[0]) >= 0 for x, y in sorted_pairs)


def main():
    data_path = get_input_path("Day 04: Camp Cleanup")
    with open(data_path, "r") as file:
        contents = file.read().splitlines()

    start = time.monotonic()
    assignment_pairs = preprocess_input(contents)
    count_fully_contained = count_fully_contained_ranges(assignment_pairs)
    count_overlapping = count_overlapping_ranges(assignment_pairs)
    stop = time.monotonic()

    print(f"Number of fully contained ranges: {count_fully_contained}")
    print(f"Number of overlapping ranges: {count_overlapping}")
    print_elapsed_time(start, stop)


if __name__ == "__main__":
    main()
