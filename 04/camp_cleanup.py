#!/usr/bin/python
"""Python solution for Advent of Code 2022, Day 4: Camp Cleanup"""


def string2sets(pair_string: str) -> (set, set):
    str_a, str_b = pair_string.split(',')
    a_start, a_end = map(int, str_a.split('-'))
    b_start, b_end = map(int, str_b.split('-'))
    set_a = set(range(a_start, a_end+1))
    set_b = set(range(b_start, b_end+1))
    return set_a, set_b


def is_fully_contained(pair_string: str) -> bool:
    set_a, set_b = string2sets(pair_string)
    return set_a.issubset(set_b) or set_b.issubset(set_a)


def have_overlap(pair_string: str) -> bool:
    set_a, set_b = string2sets(pair_string)
    return not set_a.isdisjoint(set_b)


if __name__ == '__main__':

    # test cases part one
    EXAMPLE = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""
    EXPECTED = [False, False, False, True, True, False]
    for num, line in enumerate(EXAMPLE.splitlines()):
        assert is_fully_contained(line) == EXPECTED[num], f'Expected {EXPECTED[num]}'

    # test cases part two
    EXPECTED_2 = [False, False, True, True, True, True]
    for num, line in enumerate(EXAMPLE.splitlines()):
        assert have_overlap(line) == EXPECTED_2[num], f'Expected {EXPECTED_2[num]}'

    # actual puzzle
    COUNT_FULLY_CONTAINED = 0
    COUNT_HAVE_OVERLAP = 0
    with open('input.txt', encoding='utf-8') as f_in:
        for line in f_in:
            line = line.strip()
            if is_fully_contained(line):
                COUNT_FULLY_CONTAINED += 1
            if have_overlap(line):
                COUNT_HAVE_OVERLAP += 1
    print(f'One pair contains the other in a total of {COUNT_FULLY_CONTAINED} pairs')
    print(f'There is overlap in a total of {COUNT_HAVE_OVERLAP} pairs')
