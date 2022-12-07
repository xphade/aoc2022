#!/usr/bin/env python3
#
# Copyright (c) 2022, xphade <github.com/xphade>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import re
import time
from typing import List, NamedTuple, Optional

from aoc_utils import get_input_path, print_elapsed_time


class File(NamedTuple):
    name: str
    size: int


class TerminalCommand(NamedTuple):
    cmd: str
    arg: Optional[str]
    output: List[str]


class Directory:
    def __init__(self, name: str, parent: Optional[Directory]) -> None:
        self.name: str = name
        self.size = 0
        self.files: List[File] = []
        self.dirs: List[Directory] = []
        self.parent = parent

    def add_file(self, file: File) -> None:
        self.files.append(file)
        self.size += file.size

    def add_directory(self, directory: Directory) -> None:
        self.dirs.append(directory)


COMMAND_REGEX = re.compile(r"^\$ (cd|ls) *(.*)$")
DIRECTORY_REGEX = re.compile(r"^dir (.*)$")
FILE_REGEX = re.compile(r"^(\d+) (.*)$")


def preprocess_terminal_output(terminal_output: List[str]) -> List[TerminalCommand]:
    terminal_commands: List[TerminalCommand] = []
    current_command_idx = -1

    for i in range(len(terminal_output)):
        if match := COMMAND_REGEX.match(terminal_output[i]):
            terminal_commands.append(
                TerminalCommand(cmd=match.group(1), arg=match.group(2), output=[])
            )
            current_command_idx += 1
            continue

        terminal_commands[current_command_idx].output.append(terminal_output[i])

    return terminal_commands


def ls(output: List[str], current_directory: Directory):
    for line in output:
        if match := DIRECTORY_REGEX.match(line):
            current_directory.add_directory(
                Directory(name=match.group(1), parent=current_directory)
            )
        elif match := FILE_REGEX.match(line):
            current_directory.add_file(
                File(name=match.group(2), size=int(match.group(1)))
            )
        else:
            assert False  # Should never happen.


def cd(argument: str, current_directory: Directory) -> Directory:
    new_directory = current_directory
    if argument == "/":
        while new_directory.parent is not None:
            new_directory = new_directory.parent
    elif argument == "..":
        assert new_directory.parent
        new_directory = new_directory.parent
    else:
        assert argument in [dir.name for dir in current_directory.dirs]
        for dir in current_directory.dirs:
            if dir.name == argument:
                new_directory = dir
                break
    return new_directory


def apply_commands(
    terminal_commands: List[TerminalCommand], current_directory: Directory
):
    for command in terminal_commands:
        if command.cmd == "ls":
            ls(command.output, current_directory)
        elif command.cmd == "cd":
            assert command.arg is not None
            current_directory = cd(command.arg, current_directory)
        else:
            assert False  # Should never happen.


def calculate_size(current_directory: Directory) -> int:
    for dir in current_directory.dirs:
        current_directory.size += calculate_size(dir)
    return current_directory.size


def directory_sizes_max_100k(current_directory: Directory) -> List[int]:
    sizes: List[int] = []
    for dir in current_directory.dirs:
        sizes.extend(directory_sizes_max_100k(dir))

    if current_directory.size <= 100000:
        sizes.append(current_directory.size)

    return sizes


def find_directory_size_to_delete(
    current_directory: Directory, size_needed: int, current_best: int
) -> int:
    if current_directory.size >= size_needed and current_directory.size < current_best:
        current_best = current_directory.size

    for dir in current_directory.dirs:
        current_best = find_directory_size_to_delete(dir, size_needed, current_best)

    return current_best


def main():
    data_path = get_input_path("Day 07: No Space Left On Device")
    with open(data_path, "r") as file:
        terminal_output = file.read().splitlines()

    start = time.monotonic()

    commands = preprocess_terminal_output(terminal_output)
    root = Directory(name="/", parent=None)
    apply_commands(commands, root)
    calculate_size(root)
    print(sum(directory_sizes_max_100k(root)))

    size_needed = 30000000 - (70000000 - root.size)
    print(find_directory_size_to_delete(root, size_needed, current_best=70000000))

    stop = time.monotonic()

    print_elapsed_time(start, stop)


if __name__ == "__main__":
    main()
