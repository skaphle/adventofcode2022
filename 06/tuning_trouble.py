#!/usr/bin/python
"""Python solution for Advent of Code 2022, Day 6: Tuning Trouble"""


def find_marker(signal: str, length: int) -> int:
    for pos in range(length, len(signal)+1):
        if len(set(signal[pos-length:pos])) == length:
            return pos


if __name__ == '__main__':
    # program outline:
    # - read input string
    # - go through string
    # - if 4 unique characters, stop; unique: use set

    # test cases
    EXAMPLE_1 = """mjqjpqmgbljsphdztnvjfqwrcgsmlb
bvwbjplbgvbhsrlpgdmjqwftvncz
nppdvjthqldpwncqszvftbrmjlhg
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"""
    EXPECTED_1 = [7, 5, 6, 10, 11]

    for num, line in enumerate(EXAMPLE_1.splitlines()):
        assert find_marker(line,4) == EXPECTED_1[num], f'Expected {EXPECTED_1[num]}'

    # puzzle input:
    with open('input.txt', encoding='utf-8') as f_in:
        input_string = f_in.read()
    print(f'Characters until marker, part 1: {find_marker(input_string,4)}')

    # part 2: same as part 1, but 14 instead of 4
    EXPECTED_2 = [19, 23, 23, 29, 26]
    for num, line in enumerate(EXAMPLE_1.splitlines()):
        assert find_marker(line,14) == EXPECTED_2[num], f'Expected {EXPECTED_2[num]}'
    print(f'Characters until marker, part 2: {find_marker(input_string,14)}')
