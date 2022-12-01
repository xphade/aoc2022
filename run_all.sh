#!/bin/bash
#
# Copyright (c) 2021, xphade <github.com/xphade>
# SPDX-License-Identifier: MIT
#
# Run all (currently implemented) days.

cd $(dirname "$0")
echo

for i in {01..25}; do
    file=(./${i}_*.py)
    if [[ ! -f ${file[0]} ]]; then
        continue  # file does not exist (yet)
    fi

    echo "Day ${i}:"
    eval "./${i}_*.py inputs/${i}_*.txt"
    echo
done
