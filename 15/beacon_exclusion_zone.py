#!/usr/bin/python
"""Python solution for Advent of Code 2022, Day 15: Beacon Exclusion Zone"""

import cProfile
from itertools import islice
import re


def find_possible_locations(sensor_list: list, radius_list: list, max_: int) -> list:
    # strategy:
    # - loop over every possible coordinate
    # -- loop over every sensor
    # --- check if coordinate in radius
    # - if not in any sensor's radius, save position
    possible = []
    # sort sensor and radius?
    indices = sorted(list(range(len(sensor_list))), key=sensor_list.__getitem__)
    #indices = sorted(list(range(len(sensor_list))), key=lambda l: sensor_list[l][1])
    #indices = list(range(len(sensor_list)))
    for y in range(0, max_+1):
        #x_skip = 0
        x_count = 0
        x_iter = range(0, max_+1)
        for x in x_iter:
            # if x < x_skip:
            #    continue
            is_possible = True
            for i in indices:
                s = sensor_list[i]
                r = radius_list[i]
                dx = s[0] - x if s[0] > x else x - s[0]
                dy = s[1] - y if s[1] > y else y - s[1]
                if dx + dy <= r:
                    is_possible = False
                    #x_skip = s[0] + r - dy + 1
                    next(islice(x_iter, r - dy, r-dy+2), '')
                    break
            if is_possible:
                possible.append((x, y))
            x_count += 1
    return possible


def find_possible_locations_fast(sensor_list: list, radius_list: list, max_: int) -> list:
    # new faster strategy:
    # instead of all coords, only check the outline of each sensor's area
    possible = []
    #indices = sorted(list(range(len(sensor_list))), key=sensor_list.__getitem__)
    indices = sorted(list(range(len(sensor_list))), key=radius_list.__getitem__, reverse=True)
    for i in indices:
        s = sensor_list[i]
        r = radius_list[i]
        # -- loop over x/y, coordinates for outline+1, add to candidates list
        for j in range(4*(r+1)):
            # go clockwise 12-3-6-9-12
            if j < r+1:
                x = s[0] + j
            elif j < 3*(r+1):
                x = s[0] + 2*(r+1) - j
            else:
                x = s[0] - 4*(r+1) + j
            if j < 2*(r+1):
                y = s[1] - (r+1) + j
            else:
                y = s[1] + 3*(r+1) - j
            if x < 0 or x > max_ or y < 0 or y > max_:
                continue
            # second loop over sensors to eliminate candidates
            # (don't append 50M candidate tuples to a list)
            is_possible = True
            for j in indices:
                s2 = sensor_list[j]
                r2 = radius_list[j]
                dx = s2[0] - x if s2[0] > x else x - s2[0]
                #dx = abs(s[0]-x)
                dy = s2[1] - y if s2[1] > y else y - s2[1]
                #dy = abs(s[1]-y)
                if dx + dy <= r2:
                    is_possible = False
                    break
            if is_possible:
                possible.append((x, y))
    # make unique
    return list(set(possible))


if __name__ == '__main__':
    # goal: positions where beacon is not in a single line
    #
    # strategy:
    # - read input, list of beacons and signals
    # - option a)
    # -- create map array, mark every spot as S/B/excluded/unknown
    # -- simply read line of interest
    # - option b)
    # -- don't craft a whole map_
    # -- for every spot in the line, check if it is excluded by a signal
    #
    # opt a) requires a lot of resources and seems wasteful
    # opt b) should be good enough if it works
    #
    # check excluded?
    # - from a) for every S, use distance to its B, mark every spot in "radius"
    # - from b) still need radius of every S to compute -> do that first

    # detailed strategy:
    # - read input, list of beacons and signals
    # - loop over signals
    # -- calculate radius for all signals
    # -- check which x-values of y-line of interest are in radius, add to list
    # -- make sure none of those are coords of B
    # - count entries

    # to read in coordinates, use regexp
    pattern = re.compile(
        r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')

    # test
    EXAMPLE = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""
    TEST_Y_INTEREST = 10

    test_sensors = []
    test_beacons = []
    test_radii = []
    test_excluded = []
    for line in EXAMPLE.splitlines():
        match = pattern.match(line)
        Sx, Sy, Bx, By = (int(x) for x in match.groups())
        test_sensors.append((Sx, Sy))
        test_beacons.append((Bx, By))
        radius = abs(Sx - Bx) + abs(Sy - By)
        test_radii.append(radius)
        radius_on_y = radius - abs(Sy - TEST_Y_INTEREST)
        test_excluded.extend(range(Sx - radius_on_y, Sx+radius_on_y+1))
    test_excluded_set = set(test_excluded)
    test_beacons_set = set(test_beacons)
    # check that none are coords of B
    for c in list(test_beacons_set):
        if c[1] == TEST_Y_INTEREST and c[0] in test_excluded_set:
            test_excluded_set.remove(c[0])
    assert len(test_excluded_set) == 26, 'Expected 26 excluded positions in example'

    # actual puzzle
    with open('input.txt', encoding='utf-8') as f_in:
        in_txt = f_in.read()
    Y_INTEREST = 2000000
    sensors = []
    beacons = []
    radii = []
    excluded = []
    for line in in_txt.splitlines():
        match = pattern.match(line)
        Sx, Sy, Bx, By = (int(x) for x in match.groups())
        sensors.append((Sx, Sy))
        beacons.append((Bx, By))
        radius = abs(Sx - Bx) + abs(Sy - By)
        radii.append(radius)
        radius_on_y = radius - abs(Sy - Y_INTEREST)
        excluded.extend(range(Sx - radius_on_y, Sx+radius_on_y+1))
    excluded_set = set(excluded)
    beacons_set = set(beacons)
    # check that none are coords of B
    for c in list(beacons_set):
        if c[1] == Y_INTEREST and c[0] in excluded_set:
            excluded_set.remove(c[0])
    print(f'Number of excluded positions: {len(excluded_set)}')

    # part 2: get the only possible position of the beacon
    #
    # now a full map would make it easier
    # - not feasible:
    # - "MemoryError: Unable to allocate 14.6 TiB for an array
    #    with shape (4000000, 4000000) and data type bool"
    # - need to be efficient
    #
    # strategy:
    # - loop over every possible coordinate
    # -- loop over every sensor
    # --- check if coordinate in radius
    # - if not in any sensor's radius, save position
    #
    # this strategy actually takes extremely long, can do better?
    # - turn into function and profile: max_=1000
    # -- takes 12s, built-in abs called a lot (44088049 function calls)
    # -- use _abs=abs: 10 seconds, barely less
    # - improve algorithm
    # -- switch x<->y
    # -- jump to end of current sensor's radius: 0.1s
    # - test with max_=10000, takes 5s, still too much
    # -- sort sensors by x/y-value: 30k instead of 450k function calls, 4.4s
    # --- only works because I test until 10k, no time reduction
    # - test with max_=20000, 18s
    # -- use compile() and exec(): minimal change (<10%)
    # -- don't use abs: no change
    # - test a minimap function, 2 for loops, 1 variable to increment, max=10k,
    #   takes 5s in profile
    # - call from outside emacs elpy ipython buffer: same
    # - really skip with itertools.islice(): minor change
    #
    # expected runtime:
    # - max=10k -> 5s
    # - max=1M -> 5s*100*100=50000s
    # - max=4M -> 50000s*16=400000s, ~5 days
    #
    # need completely new strategy
    # - instead of all coords, only check the outline of each sensor's area
    # - loop over sensors to get candidates
    # -- loop over x/y, coordinates for outline+1, add to candidates list
    # - loop over sensors to eliminate candidates
    # -- loop over candidates
    # --- if candidate in sensor range, remove from list
    #
    # this produces 50M candidate tuples, instead eliminate in inner loop

    # test
    test_possible = []
    TEST_MAX = 20
    MAX = 4000000
    #test_possible = find_possible_locations(test_sensors, test_radii, TEST_MAX)
    test_possible = find_possible_locations_fast(test_sensors, test_radii, TEST_MAX)
    assert len(test_possible) == 1, f'Expected one position, not {len(test_possible)}'
    test_tuning_freq = test_possible[0][0]*MAX+test_possible[0][1]
    assert test_tuning_freq == 56000011, 'Expected tuning frequency 56000011'

    # actual puzzle
    pr = cProfile.Profile()
    pr.enable()
    # solution = find_possible_locations(sensors, radii, 10000)
    solution = find_possible_locations_fast(sensors, radii, MAX)
    pr.disable()
    pr.print_stats(sort='time')
    # takes ~180s
    print(f'Possible position(s): {solution}')
    tuning_freq = solution[0][0]*MAX+solution[0][1]
    print(f'Tuning frequency: {tuning_freq}')
