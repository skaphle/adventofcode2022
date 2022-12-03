#!/usr/bin/python
"""Python solution for Advent of Code 2022, Day 3: Rucksack Reorganization"""

import string


def find_shared(contents: str) -> str:
    contents = contents.strip()
    if len(contents) == 0 or len(contents) % 2 != 0:
        raise ValueError(f'contents "{contents}" not string of even length')
    compartment_a = contents[:len(contents)//2]
    compartment_b = contents[len(contents)//2:]
    shared = set(compartment_a).intersection(compartment_b)
    if len(shared) != 1:
        raise ValueError('need exactly one shared item')
    return shared.pop()


def priority(item: str) -> int:
    if len(item) != 1:
        raise ValueError('item not single character')
    if item in string.ascii_lowercase:
        return ord(item) - ord('a') + 1
    if item in string.ascii_uppercase:
        return ord(item) - ord('A') + 27
    raise ValueError('item not in [a-zA-Z]')


if __name__ == '__main__':

    # test cases
    assert priority('a') == 1, "Expected 1"
    assert priority('z') == 26, "Expected 26"
    assert priority('A') == 27, "Expected 27"
    assert priority('Z') == 52, "Expected 52"

    EXAMPLE = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""
    EXPECTED = 'pLPvts'
    for num,line in enumerate(EXAMPLE.splitlines()):
        assert find_shared(line) == EXPECTED[num], f'Expected {EXPECTED[num]}'
    assert sum(priority(find_shared(line))
               for line in EXAMPLE.splitlines()) == 157, 'Expected 157'

    # actual puzzle
    SUM_PRIORITIES = 0
    with open('input.txt', encoding='utf-8') as f_in:
        for line in f_in:
            SUM_PRIORITIES += priority(find_shared(line))
    print(f'sum of priorities: {SUM_PRIORITIES}')
