#!/usr/bin/env python3
#
# Copyright (c) 2022, xphade <github.com/xphade>
# SPDX-License-Identifier: MIT

from aoc_utils import get_input_path, print_elapsed_time
from typing import List, Set, Tuple
import time

# We assume that x is in downwards direction, y to the right.
Coordinate = Tuple[int, int]


def find_visisble_trees(tree_line: List[int]) -> List[int]:
    current_max = -1
    visible_trees: List[int] = []
    for idx, tree_height in enumerate(tree_line):
        if tree_height > current_max:
            visible_trees.append(idx)
            current_max = tree_height
    return visible_trees


def look_outside_left_right(tree_map: List[List[int]]) -> Set[Coordinate]:
    visible_tree_coords: Set[Coordinate] = set()
    for idx, tree_line in enumerate(tree_map):
        visible_left = find_visisble_trees(tree_line)
        coords_left: Set[Coordinate] = {(idx, tree) for tree in visible_left}
        trees_right = find_visisble_trees(list(reversed(tree_line)))
        # Account for reversed list
        trees_right = [(len(tree_line) - 1) - t for t in trees_right]
        coords_right: Set[Coordinate] = {(idx, tree) for tree in trees_right}
        visible_tree_coords = visible_tree_coords.union(coords_left).union(coords_right)
    return visible_tree_coords


def look_outside_top_bottom(tree_map: List[List[int]]) -> Set[Coordinate]:
    transposed_map: List[List[int]] = list(map(list, zip(*tree_map)))
    visible_tree_coords: Set[Coordinate] = set()
    for idx, tree_line in enumerate(transposed_map):
        trees_left = find_visisble_trees(tree_line)
        coords_left: Set[Coordinate] = {(tree, idx) for tree in trees_left}
        trees_right = find_visisble_trees(list(reversed(tree_line)))
        # Account for reversed list
        trees_right = [(len(tree_line) - 1) - t for t in trees_right]
        coords_right: Set[Coordinate] = {(tree, idx) for tree in trees_right}
        visible_tree_coords = visible_tree_coords.union(coords_left).union(coords_right)
    return visible_tree_coords


# TODO: A lot of repeated code in here, maybe rather do it similarly to part 1.
def calculate_scenic_score(tree_map: List[List[int]], tree_coord: Coordinate) -> int:
    x, y = tree_coord
    tree_height = tree_map[x][y]
    scenic_score = 1
    # Left:
    i, j = x, y
    blocked_count = 0
    while j > 0:
        blocked_count += 1
        j -= 1
        if tree_height <= tree_map[i][j]:
            break
    scenic_score *= blocked_count
    # Right:
    i, j = x, y
    blocked_count = 0
    while j < (len(tree_map[i]) - 1):
        blocked_count += 1
        j += 1
        if tree_height <= tree_map[i][j]:
            break
    scenic_score *= blocked_count
    # Top:
    i, j = x, y
    blocked_count = 0
    while i > 0:
        blocked_count += 1
        i -= 1
        if tree_height <= tree_map[i][j]:
            break
    scenic_score *= blocked_count
    # Bottom:
    i, j = x, y
    blocked_count = 0
    while i < (len(tree_map) - 1):
        blocked_count += 1
        i += 1
        if tree_height <= tree_map[i][j]:
            break
    scenic_score *= blocked_count
    return scenic_score


def find_best_tree(tree_map: List[List[int]]) -> int:
    best_score = 0
    for row in range(len(tree_map)):
        for col in range(len(tree_map[row])):
            best_score = max(best_score, calculate_scenic_score(tree_map, (row, col)))
    return best_score


def main():
    data_path = get_input_path("Day 08: Treetop Tree House")
    with open(data_path, "r") as file:
        tree_map = file.read().splitlines()

    start = time.monotonic()
    tree_map = [[int(c) for c in line] for line in tree_map]
    visible_tree_coordinates = look_outside_left_right(tree_map).union(
        look_outside_top_bottom(tree_map)
    )
    outside_visible_trees = len(visible_tree_coordinates)
    best_scenic_score = find_best_tree(tree_map)
    stop = time.monotonic()

    print(f"Number of visible trees from outside: {outside_visible_trees}")
    print(f"Best scenic score of any tree: {best_scenic_score}")
    print_elapsed_time(start, stop)


if __name__ == "__main__":
    main()
