#!/usr/bin/python
"""Python solution for Advent of Code 2022, Day 13: Distress Signal"""

from ast import literal_eval
from functools import cmp_to_key


def cmp(a: int, b: int) -> 1 | 0 | -1:
    """Basic implementation of python 2 cmp()."""
    return (a > b) - (a < b)


def order(left: int | list, right: int | list) -> 1 | 0 | -1:
    """Extension of cmp(left,right) that accepts lists."""
    if isinstance(left, int) and isinstance(right, int):
        return cmp(left, right)
    if isinstance(left, list) and isinstance(right, list):
        for i in range(min(len(left), len(right))):
            sub = order(left[i], right[i])
            if sub != 0:
                return sub
        return cmp(len(left), len(right))
    if isinstance(left, int) and isinstance(right, list):
        return order([left], right)
    if isinstance(left, list) and isinstance(right, int):
        return order(left, [right])
    return None


if __name__ == '__main__':
    # goal: check if pair of lists/integers is ordered
    #
    # strategy:
    # - read input, convert string to lists
    # - check if ordered
    # - return sum of indices
    #
    # convert string to lists
    # - use ast.literal_eval
    #
    # check if ordered
    # - program literally like instruction text

    # test with example
    EXAMPLE_1 = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""
    EXPECTED_1 = [True, True, False, True, False, True, False, False]
    test_pairs = [[literal_eval(p) for p in pair.splitlines()]
                  for pair in EXAMPLE_1.split('\n\n')]
    test_ordered = [-1 == order(pair[0], pair[1]) for pair in test_pairs]
    assert test_ordered == EXPECTED_1, f'Expected {EXPECTED_1}, not {test_ordered}'
    test_sum = sum(i+1 for i in range(len(test_ordered)) if test_ordered[i])
    assert test_sum == 13, 'Expected 13 as sum of indices in example'

    # actual puzzle input
    with open('input.txt', encoding='utf-8') as f_in:
        in_txt = f_in.read()
    pairs = [[literal_eval(p) for p in pair.splitlines()]
             for pair in in_txt.split('\n\n')]
    ordered = [-1 == order(pair[0], pair[1]) for pair in pairs]
    index_sum = sum(i+1 for i in range(len(ordered)) if ordered[i])
    print(f'Sum of indices of ordered pairs: {index_sum}')

    # part 2: put into right order
    #
    # this requires a sorting algorithm
    # - sort/sorted need key, not order function
    # - use functools.cmp_to_key

    # test with example
    div_pack = [[[2]], [[6]]]
    t_all_p = [literal_eval(p) for p in EXAMPLE_1.splitlines() if p]
    t_all_p.extend(div_pack)
    t_all_s = sorted(t_all_p, key=cmp_to_key(order))
    t_dk = (t_all_s.index(div_pack[0])+1) * (t_all_s.index(div_pack[1])+1)
    assert t_dk == 140, 'Expected 140 as decoder key in example'

    # actual puzzle
    all_packets = [literal_eval(p) for p in in_txt.splitlines() if p]
    all_packets.extend(div_pack)
    all_sorted = sorted(all_packets, key=cmp_to_key(order))
    decoder_key = (all_sorted.index(div_pack[0])+1) * (all_sorted.index(div_pack[1])+1)
    print(f'Decoder key: {decoder_key}')
