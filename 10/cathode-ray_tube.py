#!/usr/bin/python
"""Python solution for Advent of Code 2022, Day 10: Cathode-Ray Tube"""

import numpy as np


def poll_cpu(instructions: str, poll_fcn) -> list:
    # run the instructions and return a list made of (cycle, value)
    instr = instructions.splitlines()
    current_instruction = ''
    end = 0
    cycle = 1
    V = 0
    X = 1
    ret = []
    while instr or current_instruction:
        # read in a new instruction
        if not current_instruction:
            current_instruction = instr.pop(0)
            if current_instruction == 'noop':
                current_instruction = ''
            else:
                V = int(current_instruction.split()[1])
                end = cycle + 1
        # report
        if poll_fcn(cycle):
            if DEBUG:
                print(f'Cycle {cycle:3}: X = {X}, signal strength = {cycle*X}')
            ret.append((cycle, X))
        # delayed increment for addx; this may seem weird but this way
        # it can be easily extended for longer operations
        if cycle == end:
            X += V
            current_instruction = ''
        cycle += 1
    return ret


def get_screen(instructions: str) -> np.array:
    # run the instructions and return a list made of (cycle, value)
    instr = instructions.splitlines()
    current_instruction = ''
    end = 0  # signal end of current instruction
    cycle = 1
    V = 0  # addx argument
    X = 1  # current central position of sprite
    m, n = 0, 0  # current position on CRT (down, right)
    width = 40
    screen = np.zeros((6, 40), dtype=bool)
    ret = []
    while instr or current_instruction:
        # read in a new instruction
        if not current_instruction:
            current_instruction = instr.pop(0)
            if current_instruction == 'noop':
                current_instruction = ''
            else:
                V = int(current_instruction.split()[1])
                end = cycle + 1
        # draw
        m = (cycle-1) // width
        n = (cycle-1) % width
        if n in [X-1, X, X+1]:
            screen[m, n] = True
        if cycle % 40 == 0 or cycle % 40 == 1:
            if DEBUG:
                print(f'Cycle {cycle:3}: X = {X}, m = {m}, n = {n}')
        # delayed increment for addx
        if cycle == end:
            X += V
            current_instruction = ''
        cycle += 1
    return screen


def draw_screen(screen: np.array):
    print('\n'.join(''.join('#' if x else '.' for x in y) for y in screen.tolist()))


if __name__ == '__main__':
    # goal: report the state of a register with cycles and instructions
    #
    # strategy:
    # - get instructions, follow line by line
    # - track current cycle and register state
    # - report after X cycles
    #
    # cycle: integer number
    # register: integer
    # report cycle X: if cycle in list(report), or function?
    #
    # confusing language "during" vs "at start of" cycle
    # - cycle starts at 1: before/at start of/during first cycle
    # - treat "during Xth cycle" as "cycle == X" before applying addx
    #
    # main loop:
    # - option 1: loop over instructions
    # --- increment cycle by 1 or 2
    # --- check if new cycle meets report criteria
    # --- if by 2, check if 1 would meet report criteria
    # --- execute the instruction
    # - option 2: loop over cycle
    # --- if no instruction, begin next, set end of instruction
    # --- check if need to report
    # --- check if instruction ends, execute, mark done
    # --- increment cycle by 1
    #
    # choose option 2

    # tests
    DEBUG = False
    EXAMPLE_1 = """noop
addx 3
addx -5"""
    poll_cpu(EXAMPLE_1, lambda x: True)
    with open('example_2.txt', encoding='utf-8') as f_in:
        EXAMPLE_2 = f_in.read()
    test_poll = poll_cpu(EXAMPLE_2, lambda x: (x-20) % 40 == 0)
    # (compare debug print statements with puzzle.txt)
    assert sum(x[0]*x[1] for x in test_poll) == 13140, 'Expected 13140 as sum'

    # actual puzzle
    with open('input.txt', encoding='utf-8') as f_in:
        in_str = f_in.read()
    poll = poll_cpu(in_str, lambda x: (x-20) % 40 == 0)
    signal_strength_sum = sum(x[0]*x[1] for x in poll)
    print(f'Sum of signal strengths: {signal_strength_sum}')

    # part two: draw a sprite on a screen
    #
    # strategy:
    # - add a CRT screen position
    # - compare that to current X register
    # - return a list of lists of char (easier: np.array)
    #
    # create new function copied from the previous
    print()

    # test
    DEBUG = False
    test_drawing = get_screen(EXAMPLE_2)
    # draw_screen(test_drawing)
    # (visual comparison)

    # actual puzzle
    drawing = get_screen(in_str)
    draw_screen(drawing)
