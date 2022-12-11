#!/usr/bin/env python3
#
# Copyright (c) 2022, xphade <github.com/xphade>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import re
import time
from typing import List, Optional

from aoc_utils import get_input_path, print_elapsed_time


class Monkey:
    ITEM_RGX = re.compile(r"Starting items:.*?\n")
    NUM_RGX = re.compile(r"\d+")
    OPERATION_RGX = re.compile(r"Operation:.*?(\*|\+) (\d+|old)")
    TEST_RGX = re.compile(r"Test:.*?(\d+)")
    TRUE_RGX = re.compile(r"If true:.*?(\d+)")
    FALSE_RGX = re.compile(r"If false:.*?(\d+)")

    def __init__(self, raw_input: str) -> None:
        item_string = self.ITEM_RGX.search(raw_input).group()  # type: ignore
        self._items = list(map(int, self.NUM_RGX.findall(item_string)))

        operation_match = self.OPERATION_RGX.search(raw_input)
        self._operation = operation_match.group(1)  # type: ignore
        self._operation_argument = operation_match.group(2)  # type: ignore

        self.divisor = int(self.TEST_RGX.search(raw_input).group(1))  # type: ignore

        self._true_monkey = int(self.TRUE_RGX.search(raw_input).group(1))  # type: ignore
        self._false_monkey = int(self.FALSE_RGX.search(raw_input).group(1))  # type: ignore

        self.inspected_items = 0

    def _apply_operation(self, number: int) -> int:
        other_number = (
            number
            if self._operation_argument == "old"
            else int(self._operation_argument)
        )
        if self._operation == "*":
            return number * other_number
        elif self._operation == "+":
            return number + other_number
        else:
            assert False  # Should never happen.

    def _throw_item(
        self, item: int, monkeys: List[Monkey], divisor_product: Optional[int]
    ):
        self.inspected_items += 1
        worry_level = self._apply_operation(item)

        if divisor_product:
            worry_level %= divisor_product
        else:
            worry_level //= 3

        idx = (
            self._true_monkey if worry_level % self.divisor == 0 else self._false_monkey
        )

        monkeys[idx].receive(worry_level)

    def throw_items(self, monkeys: List[Monkey], divisor_product: Optional[int]):
        while len(self._items) > 0:
            self._throw_item(self._items.pop(0), monkeys, divisor_product)

    def receive(self, item: int):
        self._items.append(item)


def calculate_monkey_business_level(
    monkeys: List[Monkey], rounds: int, manage_worry_levels: bool
) -> int:
    divisor_product = None
    if manage_worry_levels:
        divisor_product = 1
        for monkey in monkeys:
            divisor_product *= monkey.divisor

    for _ in range(rounds):
        for monkey in monkeys:
            monkey.throw_items(monkeys, divisor_product)

    monkeys.sort(key=lambda monkey: monkey.inspected_items, reverse=True)
    return monkeys[0].inspected_items * monkeys[1].inspected_items


def main():
    data_path = get_input_path("Day 11: Monkey in the Middle")
    with open(data_path, "r") as file:
        raw_inputs = file.read().split("\n\n")

    start = time.monotonic()
    monkeys = [Monkey(raw_input) for raw_input in raw_inputs]
    monkey_business_pt1 = calculate_monkey_business_level(
        monkeys, 20, manage_worry_levels=False
    )
    monkeys = [Monkey(raw_input) for raw_input in raw_inputs]  # Reset monkeys.
    monkey_business_pt2 = calculate_monkey_business_level(
        monkeys, 10000, manage_worry_levels=True
    )
    stop = time.monotonic()

    print(f"Monkey business level (part 1): {monkey_business_pt1}")
    print(f"Monkey business level (part 2): {monkey_business_pt2}")
    print_elapsed_time(start, stop)


if __name__ == "__main__":
    main()
