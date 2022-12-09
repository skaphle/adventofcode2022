#!/usr/bin/python
"""Python solution for Advent of Code 2022, Day 9: Rope Bridge"""


import numpy as np


def get_tail_path(instr: str) -> list:
    H = np.array((0, 0))
    T = np.array((0, 0))
    path = [H]
    for motion in instr.splitlines():
        direction = motion.split()[0]
        steps = int(motion.split()[1])
        if direction == 'R':
            T_move = np.array((0, 1))
        elif direction == 'L':
            T_move = np.array((0, -1))
        elif direction == 'U':
            T_move = np.array((1, 0))
        else:
            T_move = np.array((-1, 0))
        for i in range(steps):
            T = T + T_move
            if max(abs(T-H)) > 1:
                H = H + np.sign(T-H)*(T != H)
                path.append(H)
    return path


if __name__ == '__main__':
    # goal: count unique positions of a tail's path following a head
    #
    # strategy:
    # - read input as series of instructions
    # - apply instruction, save positions
    # - count unique
    #
    # read input: simple lines of <direction> <number of steps>
    #
    # apply instruction:
    # - make list of positions
    # - coordinates start at s=(0,0)
    # - change head's position
    # - if distant, change tail and append to list

    # test cases:
    EXAMPLE_1 = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

    test_path = get_tail_path(EXAMPLE_1)
    # now how to test this?
    # print(f'path: {path}')
    test_unique_positions = len(set(tuple(p) for p in test_path))
    assert test_unique_positions == 13, 'Expected 13 positions in test'

    # actual puzzle
    with open('input.txt', encoding='utf-8') as f_in:
        instructions = f_in.read()
    path_1 = get_tail_path(instructions)
    unique_positions_1 = len(set(tuple(p) for p in path_1))
    print(f'Positions visited at least once: {unique_positions_1}')
