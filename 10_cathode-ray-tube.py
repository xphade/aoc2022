#!/usr/bin/env python3
#
# Copyright (c) 2022, xphade <github.com/xphade>
# SPDX-License-Identifier: MIT

import re
import time
from typing import List, NamedTuple

from aoc_utils import get_input_path, print_elapsed_time


class Instruction(NamedTuple):
    cmd: str
    arg: int


INSTRUCTION_REGEX = re.compile(r"([a-zA-Z]+) ?(-?\d+)?")


def preprocess_input(contents: List[str]) -> List[Instruction]:
    matches = [INSTRUCTION_REGEX.match(line) for line in contents]
    assert all([match is not None for match in matches])
    return [
        Instruction(
            cmd=match.group(1),  # type: ignore
            arg=(0 if match.group(2) is None else int(match.group(2))),  # type: ignore
        )
        for match in matches
    ]


def get_wait_cycles(instruction: Instruction) -> int:
    assert instruction.cmd in {"noop", "addx"}
    return 1 if instruction.cmd == "noop" else 2


def execute(instruction: Instruction, register_value: int) -> int:
    if instruction.cmd == "noop":
        return register_value
    assert instruction.cmd == "addx"
    return register_value + instruction.arg


def cycle(instructions: List[Instruction]) -> List[int]:
    current_value = 1
    register_values: List[int] = []
    wait_cycles = 0
    while len(instructions) > 0 or wait_cycles > 0:
        wait_cycles = (
            get_wait_cycles(instructions[0]) if wait_cycles == 0 else wait_cycles
        )

        register_values.append(current_value)
        wait_cycles -= 1

        if wait_cycles == 0:
            current_value = execute(instructions.pop(0), current_value)

    return register_values


def evaluate_cycles(cycles: List[int]) -> int:
    result = 0
    for i in range(len(cycles)):
        cycle = i + 1
        if ((cycle - 20) % 40) != 0:
            continue
        result += cycle * cycles[i]
    return result


def draw_crt(cycles: List[int]) -> str:
    crt = ""
    for pixel_pos, sprite_pos in enumerate(cycles):
        if pixel_pos > 0 and pixel_pos % 40 == 0:
            crt += "\n"

        if pixel_pos % 40 in {sprite_pos - 1, sprite_pos, sprite_pos + 1}:
            crt += "🎅"
        else:
            crt += "🎄"
    return crt


def main():
    data_path = get_input_path("Day 10: Cathode-Ray Tube")
    with open(data_path, "r") as file:
        contents = file.read().splitlines()

    start = time.monotonic()
    instructions = preprocess_input(contents)
    cycles = cycle(instructions)
    sum_signal_strengths = evaluate_cycles(cycles)
    crt = draw_crt(cycles)
    stop = time.monotonic()

    print(f"Sum of signal strengths: {sum_signal_strengths}")
    print(f"Image displayed on CRT:\n{crt}")
    print_elapsed_time(start, stop)


if __name__ == "__main__":
    main()
