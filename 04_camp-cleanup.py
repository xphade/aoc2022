#!/usr/bin/env python3
#
# Copyright (c) 2022, xphade <github.com/xphade>
# SPDX-License-Identifier: MIT

import time
from typing import List, Tuple

from aoc_utils import get_input_path, print_elapsed_time

Range = Tuple[int, int]
Pair = List[Range]


def preprocess_input(contents: List[str]) -> List[Pair]:
    assignment_pairs: List[Pair] = []
    for line in contents:
        range_pair: Pair = [tuple(map(int, rng.split("-"))) for rng in line.split(",")]
        assignment_pairs.append(range_pair)
    return assignment_pairs


def count_fully_contained_ranges(pairs: List[Pair]) -> int:
    def lhs_in_rhs(lhs: Range, rhs: Range) -> bool:
        return lhs[0] >= rhs[0] and lhs[1] <= rhs[1]

    def rhs_in_lhs(lhs: Range, rhs: Range) -> bool:
        return rhs[0] >= lhs[0] and rhs[1] <= lhs[1]

    return sum(lhs_in_rhs(x, y) or rhs_in_lhs(x, y) for x, y in pairs)


def count_overlapping_ranges(pairs: List[Pair]) -> int:
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
