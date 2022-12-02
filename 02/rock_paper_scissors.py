#!/usr/bin/python
"""Python solution for Advent of Code 2022, Day 2: Rock Paper Scissors"""


def calculate_score(other, own):
    if other not in ['A', 'B', 'C'] or own not in ['X', 'Y', 'Z']:
        raise ValueError
    ord_other = ord(other)  # ord('A')=65, ord('Z')=88
    ord_own = ord(own)
    if ord_other + 23 in (ord_own + 1, ord_own - 2):
        outcome = 0
    elif ord_other + 23 == ord_own:
        outcome = 3
    elif ord_other + 23 in (ord_own - 1, ord_own + 2):
        outcome = 6
    shape = ord_own - 87
    return outcome+shape


if __name__ == '__main__':

    total_score = 0
    with open('input.txt', encoding='utf-8') as f_in:
        for line in f_in:
            words = line.split()
            total_score += calculate_score(*words)
    print(f'total_score: {total_score}')
