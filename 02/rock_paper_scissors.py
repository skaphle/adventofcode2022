#!/usr/bin/python
"""Python solution for Advent of Code 2022, Day 2: Rock Paper Scissors"""


def calculate_score(other, own):
    if other not in ['A', 'B', 'C'] or own not in ['X', 'Y', 'Z']:
        raise ValueError
    ord_other = ord(other)  # ord('A')=65, ord('X')=88
    ord_own = ord(own)
    if ord_other + 23 in (ord_own + 1, ord_own - 2):
        outcome = 0
    elif ord_other + 23 == ord_own:
        outcome = 3
    elif ord_other + 23 in (ord_own - 1, ord_own + 2):
        outcome = 6
    shape = ord_own - 87
    return outcome + shape


def calculate_score_2(other, end):
    if other not in ['A', 'B', 'C'] or end not in ['X', 'Y', 'Z']:
        raise ValueError
    # note that ord('A')=65, ord('X')=88
    num_end = (ord(end) + 2) % 3  # (X,Y,Z)->(0,1,2)
    outcome = num_end * 3  # (X,Y,Z)->(0,3,6)
    shape = (ord(other) + ord(end) + 2) % 3 + 1  # A+(X,Y,Z)->(S,R,P)->3,1,2
    return outcome + shape


if __name__ == '__main__':

    # test cases
    assert calculate_score('A', 'Y') == 8, "Expected 8"
    assert calculate_score('B', 'X') == 1, "Expected 1"
    assert calculate_score('C', 'Z') == 6, "Expected 6"

    assert calculate_score_2('A', 'Y') == 4, "Expected 4"
    assert calculate_score_2('B', 'X') == 1, "Expected 1"
    assert calculate_score_2('C', 'Z') == 7, "Expected 7"

    total_score = 0
    total_score_2 = 0
    with open('input.txt', encoding='utf-8') as f_in:
        for line in f_in:
            words = line.split()
            total_score += calculate_score(*words)
            total_score_2 += calculate_score_2(*words)
    print(f'total_score: {total_score}')
    print(f'total_score_2: {total_score_2}')
