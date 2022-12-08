#!/usr/bin/python
"""Python solution for Advent of Code 2022, Day 8: Treetop Tree House"""

import numpy as np


def get_visible_trees(trees: np.array) -> np.array:
    visible = np.zeros(trees.shape, dtype=bool)
    largest_m = np.zeros(trees.shape[0], dtype=int)
    largest_n = np.zeros(trees.shape[1], dtype=int)
    largest_o = np.zeros(trees.shape[0], dtype=int)
    largest_p = np.zeros(trees.shape[1], dtype=int)
    for m, _ in enumerate(largest_m):
        for n, _ in enumerate(largest_n):
            if trees[m, n] > largest_m[m] or n == 0 and trees[m, n] == 0:
                largest_m[m] = trees[m, n]
                visible[m, n] = True
            if trees[m, n] > largest_n[n] or m == 0 and trees[m, n] == 0:
                largest_n[n] = trees[m, n]
                visible[m, n] = True
            o = -m-1
            p = -n-1
            if trees[o, p] > largest_o[o] or n == 0 and trees[o, p] == 0:
                largest_o[o] = trees[o, p]
                visible[o, p] = True
            if trees[o, p] > largest_p[p] or m == 0 and trees[o, p] == 0:
                largest_p[p] = trees[o, p]
                visible[o, p] = True
    return visible


if __name__ == '__main__':
    # goal: count trees larger than outer trees
    #
    # structure:
    # - read in input, convert into array
    # - mark visible trees
    # - count
    #
    # read input:
    # - there is probably already a smart way to read into a np.array
    #
    # visible trees:
    # - start array of false/invisible
    # - for each direction - O(4)
    # -- for each entry in row/column - O(N^2)
    # --- check if there was a larger tree before - O(1), save largest
    #
    # count:
    # - simple sum(array)

    # test cases:
    EXAMPLE_1 = """30373
25512
65332
33549
35390"""
    TEST_EXPECTED = np.array([[1, 1, 1, 1, 1],
                              [1, 1, 1, 0, 1],
                              [1, 1, 0, 1, 1],
                              [1, 0, 1, 0, 1],
                              [1, 1, 1, 1, 1]], dtype=bool)
    test_trees = np.array([[int(c) for c in l] for l in EXAMPLE_1.splitlines()])
    test_visible = get_visible_trees(test_trees)

    assert (test_visible == TEST_EXPECTED).all(), f'vis:\n{test_visible}\nexp:\n{TEST_EXPECTED}'
    assert test_visible.sum() == 21, 'Expected 21 visible'

    # puzzle part 1
    with open('input.txt', encoding='utf-8') as f_in:
        trees = np.array([[int(c) for c in l.strip()] for l in f_in])
    visible_trees = get_visible_trees(trees)
    print(f'Number of visible trees: {visible_trees.sum()}')
