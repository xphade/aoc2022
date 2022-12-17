#!/usr/bin/env python3
#
# Copyright (c) 2022, xphade <github.com/xphade>
# SPDX-License-Identifier: MIT

import json
import time
from enum import Enum
from typing import Any, List, Tuple

from aoc_utils import get_input_path, print_elapsed_time

Packet = List[Any]
PacketPair = Tuple[Packet, Packet]


class Result(Enum):
    VALID = 0
    INVALID = 1
    UNDECIDED = 2


def preprocess_input(contents: str) -> List[PacketPair]:
    packet_pairs: List[PacketPair] = []
    for pair in contents.split("\n\n"):
        a, b = pair.splitlines()
        packet_pairs.append((json.loads(a), json.loads(b)))
    return packet_pairs


def compare_integers(lhs: int, rhs: int) -> Result:
    if lhs == rhs:
        return Result.UNDECIDED
    return Result.VALID if lhs < rhs else Result.INVALID


def compare_lists(lhs: Packet, rhs: Packet) -> Result:
    for left, right in zip(lhs, rhs):
        if type(left) != type(right):
            if type(left) is int:
                left = [left]
            else:
                right = [right]

        if type(left) is int and type(right) is int:
            result = compare_integers(left, right)
            if result == Result.UNDECIDED:
                continue
            return result

        result = compare_lists(left, right)
        if result == Result.UNDECIDED:
            continue
        return result

    if len(lhs) == len(rhs):
        return Result.UNDECIDED
    return Result.VALID if len(lhs) < len(rhs) else Result.INVALID


def calculate_sum_of_valid_indices(packet_pairs: List[PacketPair]) -> int:
    sum_of_indices = 0
    for idx, (lhs, rhs) in enumerate(packet_pairs):
        result = compare_lists(lhs, rhs)
        if result == Result.VALID:
            sum_of_indices += idx + 1
    return sum_of_indices


def sort_packets(packets: List[Packet]):
    """Sorts the `packets` using an optimized bubble sort algorithm."""
    n = len(packets)
    while n > 1:
        new_n = 0
        for i in range(1, n):
            if compare_lists(packets[i - 1], packets[i]) == Result.INVALID:
                packets[i - 1], packets[i] = packets[i], packets[i - 1]
                new_n = i
        n = new_n


def find_decoder_key(sorted_packets: List[Packet]) -> int:
    key = 1
    for idx, packet in enumerate(sorted_packets):
        if packet in [[[2]], [[6]]]:
            key *= idx + 1
    return key


def main():
    data_path = get_input_path("Day 13: Distress Signal")
    with open(data_path, "r") as file:
        contents = file.read()

    start = time.monotonic()
    packet_pairs = preprocess_input(contents)
    sum_of_valid_indices = calculate_sum_of_valid_indices(packet_pairs)

    all_packets = [p for pair in packet_pairs for p in pair]
    all_packets.extend([[[2]], [[6]]])
    sort_packets(all_packets)
    decoder_key = find_decoder_key(all_packets)
    stop = time.monotonic()

    print(f"Sum of valid indices: {sum_of_valid_indices}")
    print(f"Decoder key: {decoder_key}")
    print_elapsed_time(start, stop)


if __name__ == "__main__":
    main()
