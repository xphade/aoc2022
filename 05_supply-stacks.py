#!/usr/bin/env python3
#
# Copyright (c) 2022, xphade <github.com/xphade>
# SPDX-License-Identifier: MIT

import re
import time
from copy import deepcopy
from typing import List, NamedTuple, Tuple

from aoc_utils import get_input_path, print_elapsed_time

Stack = List[str]
Instruction = NamedTuple("Instruction", count=int, source=int, destination=int)

INSTRUCTION_REGEX = re.compile(r".*?([0-9]+).*?([0-9]+).*?([0-9]+)")


def preprocess_input(contents: str) -> Tuple[List[Stack], List[Instruction]]:
    stacks_raw, instructions_raw = contents.split("\n\n")
    stacks_lines = stacks_raw.splitlines()
    number_of_stacks = int(stacks_lines[-1][-2])

    stacks: List[Stack] = [[] for _ in range(number_of_stacks)]
    for row in stacks_lines[:-1]:
        for i in range(number_of_stacks):
            ch = row[4 * i + 1]
            if ch != " ":
                stacks[i].insert(0, ch)

    instructions: List[Instruction] = []
    for line in instructions_raw.splitlines():
        res = INSTRUCTION_REGEX.search(line)
        assert res is not None and len(res.groups()) == 3

        cnt, src, dst = map(int, res.groups())
        instructions.append(Instruction(count=cnt, source=src, destination=dst))

    return stacks, instructions


def apply_instruction_9000(stacks: List[Stack], instruction: Instruction):
    cnt, src, dst = instruction
    for _ in range(cnt):
        stacks[dst - 1].append(stacks[src - 1].pop())


def apply_instruction_9001(stacks: List[Stack], instruction: Instruction):
    cnt, src, dst = instruction
    stacks[dst - 1].extend(stacks[src - 1][-cnt:])
    del stacks[src - 1][-cnt:]


def main():
    data_path = get_input_path("Day 05: Supply Stacks")
    with open(data_path, "r") as file:
        contents = file.read()

    start = time.monotonic()
    stacks_pt1, instructions = preprocess_input(contents)
    stacks_pt2 = deepcopy(stacks_pt1)

    for instruction in instructions:
        apply_instruction_9000(stacks_pt1, instruction)
        apply_instruction_9001(stacks_pt2, instruction)

    top_crates_pt1 = "".join(map(lambda x: x[-1], stacks_pt1))
    top_crates_pt2 = "".join(map(lambda x: x[-1], stacks_pt2))
    stop = time.monotonic()

    print(f"Top crates when using CrateMover 9000: {top_crates_pt1}")
    print(f"Top crates when using CrateMover 9001: {top_crates_pt2}")
    print_elapsed_time(start, stop)


if __name__ == "__main__":
    main()
