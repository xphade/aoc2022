#!/usr/bin/env python3
#
# Copyright (c) 2022, xphade <github.com/xphade>
# SPDX-License-Identifier: MIT

import time

from aoc_utils import get_input_path, print_elapsed_time


def find_unique_sequence(datastream: str, distinct_characters: int) -> int:
    i, j = 0, distinct_characters
    while j < len(datastream):
        char_count = {ch: datastream[i:j].count(ch) for ch in datastream[i:j]}
        if all([count == 1 for count in char_count.values()]):
            return j
        i += 1
        j += 1
    assert False  # If we get here, we did not find a unique sequence (invalid input).


def main():
    data_path = get_input_path("Day 06: Tuning Trouble")
    with open(data_path, "r") as file:
        datastream = file.read().strip("\n")

    start = time.monotonic()
    processed_chars_start = find_unique_sequence(datastream, 4)
    processed_chars_message = find_unique_sequence(datastream, 14)
    stop = time.monotonic()

    print(f"Characters processed to find start marker: {processed_chars_start}")
    print(f"Characters processed to find message: {processed_chars_message}")
    print_elapsed_time(start, stop)


if __name__ == "__main__":
    main()
