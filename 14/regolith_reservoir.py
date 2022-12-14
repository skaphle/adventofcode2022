#!/usr/bin/python
"""Python solution for Advent of Code 2022, Day 14: Regolith Reservoir"""

import numpy as np


def read_map_from_string(in_str: str, floor=False) -> tuple:
    all_paths = [[[int(x) for x in c.split(',')]
                  for c in line.split(' -> ')]
                 for line in in_str.splitlines()]
    # determine min/max X, max Y
    y_min = 0
    y_max = max(c[1] for p in all_paths for c in p)
    if floor:
        y_max = y_max + 2
        x_min = 500-y_max
        x_max = 500+y_max
        all_paths.append([[x_min, y_max], [x_max, y_max]])
    else:
        all_x = [c[0] for p in all_paths for c in p]
        x_min = min(all_x)
        x_max = max(all_x)
    # create map
    map_ = np.zeros((y_max-y_min+1, x_max-x_min+1), dtype=int)
    # starting position
    start_pos = (500, 0)
    map_start_pos = (start_pos[1]-y_min, start_pos[0]-x_min)
    map_[map_start_pos] = 3
    # fill map with rock paths
    # - split input into coordinates in a list
    # - draw into map
    for path in all_paths:
        for i in range(len(path)-1):
            start = path[i]
            end = path[i+1]
            if start[0] == end[0]:
                # line along y
                sy = min(start[1], end[1])
                ey = max(start[1], end[1])+1
                map_[sy:ey, start[0]-x_min] = 1
            else:
                # line along x
                sx = min(start[0], end[0]) - x_min
                ex = max(start[0], end[0]) - x_min+1
                map_[start[1], sx:ex] = 1
    return map_, (0, 500-x_min)


def produce_sand(map_: np.array, start_pos: tuple):
    possible = True
    while possible:
        # create new unit of sand to fall
        sand_pos = np.array(start_pos)
        rest = False
        while possible and not rest:
            # try to fall down, left-down, right-down
            rest = True
            for move in ([1, 0], [1, -1], [1, 1]):
                new = sand_pos + np.array(move)
                try:
                    if map_[tuple(new)] == 0:
                        # found suitable next position, move sand
                        sand_pos = new
                        rest = False
                        break
                except IndexError:
                    # outside of map: sand falls out, no suitable
                    # position to rest in possible, end loops
                    possible = False
                    rest = False
                    break
            # no move - either at rest or impossible
            if rest:
                map_[tuple(sand_pos)] = 2
                if tuple(sand_pos) == start_pos:
                    possible = False


if __name__ == '__main__':
    # goal: count units of sand that can rest on rock structures
    #
    # strategy:
    # - read input
    # -- determine max Y, min/max X, create numpy array map
    # -- fill map with rock paths
    # - simulate sand pouring
    # -- while loop sand particles
    # --- while loop until it comes to rest
    # ---- add to map
    # --- if below the lowest rock (higher Y), break loops
    # - count sand units

    # test with example
    EXAMPLE_1 = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""
    ex1_rock_map, ex1_map_start = read_map_from_string(EXAMPLE_1)
    produce_sand(ex1_rock_map, ex1_map_start)
    ex1_num_sand = np.sum(np.where(ex1_rock_map == 2, 1, 0))
    assert ex1_num_sand == 24, 'Expected 24 units of sand in example for part 1'

    # actual puzzle input
    with open('input.txt', encoding='utf-8') as f_in:
        in_txt = f_in.read()
    rock_map, map_start = read_map_from_string(in_txt)
    produce_sand(rock_map, map_start)
    num_sand = np.sum(np.where(rock_map == 2, 1, 0))
    print(f'Sand units to rest on rocks: {num_sand}')

    # Part two: floor instead of abyss
    # - modify read function to increase map size
    # - modify sand function for different endpoint

    # test
    ex2_rock_map, ex2_map_start = read_map_from_string(EXAMPLE_1, floor=True)
    produce_sand(ex2_rock_map, ex2_map_start)
    ex2_num_sand = np.sum(np.where(ex2_rock_map == 2, 1, 0))
    assert ex2_num_sand == 93, 'Expected 93 units of sand in example for part 2'

    # actual puzzle
    rock_map_floor, map_start_floor = read_map_from_string(in_txt, floor=True)
    produce_sand(rock_map_floor, map_start_floor)
    num_sand_floor = np.sum(np.where(rock_map_floor == 2, 1, 0))
    print(f'Sand units to rest on rocks: {num_sand_floor}')
