#!/usr/bin/python
"""Python solution for Advent of Code 2022, Day 9: Rope Bridge"""


import numpy as np


def get_tail_path(instr: str, knots: int = 2) -> list:
    rope = [np.array((0,0)) for i in range(knots)]
    path = [np.array((0,0))]
    for motion in instr.splitlines():
        direction = motion.split()[0]
        steps = int(motion.split()[1])
        if direction == 'R':
            head_move = np.array((0, 1))
        elif direction == 'L':
            head_move = np.array((0, -1))
        elif direction == 'U':
            head_move = np.array((1, 0))
        else:
            head_move = np.array((-1, 0))
        for i in range(steps):
            rope[0] = rope[0] + head_move
            for j in range(1, knots):
                knot = rope[j]
                prev_knot = rope[j-1]
                if max(abs(prev_knot-knot)) > 1:
                    knot = knot + np.sign(prev_knot-knot)*(prev_knot != knot)
                    rope[j] = knot
            path.append(rope[-1])
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

    # tests
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

    # part two: rope is 10 knots instead of 2
    #
    # strategy:
    # - add intermediate positions, 1 extra loop

    # tests
    test_path_2 = get_tail_path(EXAMPLE_1, 10)
    test_unique_positions_2 = len(set(tuple(p) for p in test_path_2))
    assert test_unique_positions_2 == 1, 'Expected 1 position in test 2'
    EXAMPLE_2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""
    test_path_3 = get_tail_path(EXAMPLE_2, 10)
    test_unique_positions_3 = len(set(tuple(p) for p in test_path_3))
    assert test_unique_positions_3 == 36, 'Expected 36 positions in test 3'

    # apply to actual input
    path_2 = get_tail_path(instructions, 10)
    unique_positions_2 = len(set(tuple(p) for p in path_2))
    print(f'Positions visited at least once: {unique_positions_2}')
