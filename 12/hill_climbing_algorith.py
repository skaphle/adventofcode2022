#!/usr/bin/python
"""Python solution for Advent of Code 2022, Day 12: Hill Climbing Algorithm"""

import numpy as np


def compute_distances(input_map: np.array, reverse=False) -> np.array:
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
    current = E if reverse else S
    t_c = tuple(current)
    distance[t_c] = 0
    for i in range(M*N):
        # check every unvisited, reachable neighbor and note its distance
        for delta in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = current + np.array(delta)
            t_n = tuple(neighbor)
            if 0 <= neighbor[0] < M and 0 <= neighbor[1] < N:
                if (reverse and height[t_n] + 1 >= height[t_c] or
                        not reverse and height[t_n] <= height[t_c] + 1):
                    # technically in our setup, the first value is always the minimum
                    distance[t_n] = min(distance[t_n], distance[t_c]+1)
        visited[t_c] = True
        # where to check next?
        if not reverse and visited[t_E] or len(distance[~visited]) == 0 or min(distance[~visited]) == M*N:
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
    endpoint = divmod(list(map_ar.flat).index('E'), map_ar.shape[1])
    distance = compute_distances(map_ar)
    print(f'Minimum distance from S to E: {distance[endpoint]}')

    # part 2: fewest steps required from any start at same elevation a
    #
    # strategy:
    # - revert E and S
    # - continue until whole map is calculated
    # - take min of options
    #
    # modify function to work for both tasks
    # - create reverse parameter

    # Example
    test_distance_2 = compute_distances(test_map_ar, reverse=True)
    test_min_dist = min(test_distance_2[np.where(test_map_ar == 'a')])
    assert test_min_dist == 29, 'Shortest path in example should be 29'

    # Actual puzzle input
    distance_2 = compute_distances(map_ar, reverse=True)
    # ignore S because this was computed in part one
    min_dist = min(distance_2[np.where(map_ar == 'a')])
    print(f'Distance in shortest path from any a to E: {min_dist}')
