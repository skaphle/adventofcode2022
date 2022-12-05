#!/usr/bin/python
"""Python solution for Advent of Code 2022, Day 5: Supply Stacks"""


def read_drawing(draw_string: str) -> list:
    """Read 'drawing' from a string and return a list of lists."""
    # read input:
    # - read lines including whitespace
    # - last line: get position of entries and prepare empty lists
    # - other lines in reverse: insert into lists
    stacks = []
    positions = []
    for _line in draw_string.splitlines()[::-1]:
        if not positions:
            for pos, char in enumerate(_line):
                if not char.isspace():
                    positions.append(pos)
                    stacks.append([])
        else:
            for _num, pos in enumerate(positions):
                if len(_line) >= pos and not _line[pos].isspace():
                    stacks[_num].append(_line[pos])
    return stacks


def apply_instructions(stacks: list, instructions: str, multiple=False):
    """Change the STACKS according to the INSTRUCTIONS given. Use MULTIPLE for part two."""
    for _line in instructions.splitlines():
        words = _line.split()
        amount = int(words[1])
        from_stack = int(words[3])-1
        to_stack = int(words[5])-1
        temp = []
        for _ in range(amount):
            temp.append(stacks[from_stack].pop())
        if multiple:
            stacks[to_stack].extend(temp[::-1])
        else:
            stacks[to_stack].extend(temp)


def print_top(stacks: list) -> str:
    """Return the top element of each list in STACKS together in a single string."""
    out = ''
    for stack in stacks:
        try:
            out += stack[-1]
        except IndexError:
            out += ' '
    return out


if __name__ == '__main__':
    # program outline:
    # - open input
    # - read until newline, process as current stack
    # - read rest, translate into operations
    # - execute operations on stacks
    # - print top of every stack

    # crates:
    # - stacks: list of length 10
    # - stack: list of arbitrary length (no string bc string immutable)
    # - make a class for this? not necessary, list of lists is enough

    # test cases
    EXAMPLE_1 = """    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

    test_drawing, test_instruction = EXAMPLE_1.split('\n\n')
    test_stacks = read_drawing(test_drawing)
    assert print_top(test_stacks) == 'NDP', "Expected 'NDP'"
    EXPECTED_1 = ['DCP', ' CZ', 'M Z', 'CMZ']
    for num, line in enumerate(test_instruction.splitlines()):
        apply_instructions(test_stacks, line)
        # print(print_top(test_stacks))
        assert print_top(test_stacks) == EXPECTED_1[num], f'Expected {EXPECTED_1[num]}'

    # actual puzzle
    with open('input.txt', encoding='utf-8') as f_in:
        input_txt = f_in.read()

    # find empty line: \n\n in linux
    drawing, instruction = input_txt.split('\n\n')
    crate_stacks = read_drawing(drawing)
    apply_instructions(crate_stacks, instruction)
    print(f'Crates on top after rearrangement: {print_top(crate_stacks)}')

    # part 2: modify apply_instructions
    test_stacks_2 = read_drawing(test_drawing)
    EXPECTED_2 = ['DCP', ' CD', 'C D', 'MCD']
    for num, line in enumerate(test_instruction.splitlines()):
        apply_instructions(test_stacks_2, line, True)
        # print(print_top(test_stacks_2))
        assert print_top(test_stacks_2) == EXPECTED_2[num], f'Expected {EXPECTED_2[num]}'

    # actual puzzle
    crate_stacks_2 = read_drawing(drawing)
    apply_instructions(crate_stacks_2, instruction, multiple=True)
    print(f'Crates on top after rearrangement: {print_top(crate_stacks_2)}')
