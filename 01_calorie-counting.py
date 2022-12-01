#!/usr/bin/env python3

import time
from typing import List

from aoc_utils import get_input_path, print_elapsed_time


def count_calories(content: List[str]) -> List[int]:
    elves_calories: List[int] = [0]
    for line in content:
        if len(line) == 0:
            elves_calories.append(0)
            continue
        elves_calories[-1] += int(line)
    return elves_calories


def main():
    data_path = get_input_path("Day 01: Calorie Counting")
    with open(data_path, "r") as file:
        content = file.read().splitlines()

    start = time.monotonic()
    calories = count_calories(content)
    max_calories = max(calories)

    assert len(calories) >= 3
    sum_of_top_three = sum(sorted(calories, reverse=True)[:3])
    stop = time.monotonic()

    print(f"Most Calories carried by any Elf: {max_calories}")
    print(f"Sum of Calories carried by top three Elves: {sum_of_top_three}")
    print_elapsed_time(start, stop)


if __name__ == "__main__":
    main()
