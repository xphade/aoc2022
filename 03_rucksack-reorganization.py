#!/usr/bin/env python3
#
# Copyright (c) 2021, xphade <github.com/xphade>
# SPDX-License-Identifier: MIT

from typing import List
import time
import string

from aoc_utils import get_input_path, print_elapsed_time


def get_priority(character: str) -> int:
    return string.ascii_letters.index(character) + 1


def calculate_sum_of_item_type_priorities(item_lists: List[str]) -> int:
    sum_of_priorities = 0
    for item_list in item_lists:
        split_index = len(item_list) // 2
        common_items = set(item_list[:split_index]).intersection(
            item_list[split_index:]
        )

        assert len(common_items) == 1
        sum_of_priorities += get_priority(common_items.pop())
    return sum_of_priorities


def calculate_sum_of_badge_priorities(item_lists: List[str]) -> int:
    sum_of_priorities = 0
    for idx in range(0, len(item_lists), 3):
        common_items = (
            set(item_lists[idx])
            .intersection(item_lists[idx + 1])
            .intersection(item_lists[idx + 2])
        )

        assert len(common_items) == 1
        sum_of_priorities += get_priority(common_items.pop())
    return sum_of_priorities


def main():
    data_path = get_input_path("Day 03: Rucksack Reorganization")
    with open(data_path, "r") as file:
        item_lists = file.read().splitlines()

    start = time.monotonic()
    sum_of_type_priorities = calculate_sum_of_item_type_priorities(item_lists)
    sum_of_badge_priorities = calculate_sum_of_badge_priorities(item_lists)
    stop = time.monotonic()

    print(f"Sum of common item type priorities: {sum_of_type_priorities}")
    print(f"Sum of badge priorities: {sum_of_badge_priorities}")
    print_elapsed_time(start, stop)


if __name__ == "__main__":
    main()
