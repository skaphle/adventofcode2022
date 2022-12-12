#!/usr/bin/python
"""Python solution for Advent of Code 2022, Day 12: Hill Climbing Algorithm"""

import numpy as np


def compute_distances(input_map: np.array) -> np.array:
    M, N = input_map.shape
    t_S = divmod(list(input_map.flat).index('S'), N)
    t_E = divmod(list(input_map.flat).index('E'), N)
    S = np.array(t_S)
    E = np.array(t_E)

    # other arrays
    visited = np.zeros(input_map.shape, dtype=bool)
    distance = np.ones(input_map.shape, dtype=int) * M * N
    height = np.vectorize(ord)(input_map)
    height[t_S] = ord('a')
    height[t_E] = ord('z')

    # main loop
    current = S
    t_c = tuple(current)
    distance[t_S] = 0
    for i in range(M*N):
        # check every unvisited, reachable neighbor and note its distance
        for delta in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = current + np.array(delta)
            t_n = tuple(neighbor)
            if 0 <= neighbor[0] < M and 0 <= neighbor[1] < N and height[t_n] <= height[t_c] + 1:
                # technically in our setup, the first value is always the minimum
                distance[t_n] = min(distance[t_n], distance[t_c]+1)
        visited[t_c] = True
        # where to check next?
        if visited[t_E] or min(input_map[~visited]) == M*N:
            print(f'Distance to E: {distance[t_E]}')
            break
        min_dist = min(distance[~visited])
        t_c = divmod(list(np.where(~visited, distance, -1).flat).index(min_dist), N)
        current = np.array(t_c)
    return distance


if __name__ == '__main__':
    # goal: find shortest path
    #
    # strategy:
    # - should be a standard problem
    # - ideas:
    # -- a) try all possible directions, recursively try again, end if visit target or previous node
    # -- b) save shortest distance to each node, iteratively continue until whole field is filled
    # - look online, b) is essentially Dijkstra's algorithm
    #
    # details:
    # - read in the whole mxn map, save as an np.array, maybe converted to int
    # - same-sized np.array of bool to mark visited nodes (start: all unvisited)
    # - same-sized np.array of int to note distance from starting node (start: inf or m*n)
    # - main loop, start with start S as current node
    # -- for every neighbor, check unvisited, check if reachable, assign distance
    # -- mark current as visited
    # -- check if destination is reached or remaining unvisited have distance inf: stop
    # -- else use unvisited with smallest distance for current node
    #
    # practical questions:
    # - do I need to save the actual best path? - only for testing, multiple solutions
    # - smart use of smallest unvisited? make a set? - np.where

    # Example
    EXAMPLE_1 = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
    test_map_ar = np.array([list(line) for line in EXAMPLE_1.splitlines()])
    test_endpoint = divmod(list(test_map_ar.flat).index('E'), test_map_ar.shape[1])
    test_distance = compute_distances(test_map_ar)
    assert test_distance[test_endpoint] == 31, 'Distance in example should be 31'

    # Actual puzzle input
    with open('input.txt', encoding='utf-8') as f_in:
        in_txt = f_in.read()
    map_ar = np.array([list(line) for line in in_txt.splitlines()])
    endpoint = divmod(list(test_map_ar.flat).index('E'), test_map_ar.shape[1])
    distance = compute_distances(map_ar)
    # print(distance[endpoint])
