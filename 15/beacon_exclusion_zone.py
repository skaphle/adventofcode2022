#!/usr/bin/python
"""Python solution for Advent of Code 2022, Day 15: Beacon Exclusion Zone"""

import re


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

    #test_sensors = []
    test_beacons = []
    #test_radii = []
    test_excluded = []
    for line in EXAMPLE.splitlines():
        match = pattern.match(line)
        Sx, Sy, Bx, By = (int(x) for x in match.groups())
        #test_sensors.append((Sx, Sy))
        test_beacons.append((Bx, By))
        radius = abs(Sx - Bx) + abs(Sy - By)
        #test_radii.append(radius)
        radius_on_y = radius - abs(Sy - TEST_Y_INTEREST)
        test_excluded.extend(range(Sx - radius_on_y, Sx+radius_on_y+1))
    test_excluded_set = set(test_excluded)
    test_beacons_set = set(test_beacons)
    # check that none are coords of B
    for c in list(test_beacons_set):
        if c[1] == TEST_Y_INTEREST and c[0] in test_excluded_set:
            test_excluded_set.remove(c[0])
    assert len(test_excluded_set) == 26, 'Expected 26 excluded positions in example'

    # actual task
    with open('input.txt', encoding='utf-8') as f_in:
        in_txt = f_in.read()
    Y_INTEREST = 2000000
    #sensors = []
    beacons = []
    #radii = []
    excluded = []
    for line in in_txt.splitlines():
        match = pattern.match(line)
        Sx, Sy, Bx, By = (int(x) for x in match.groups())
        #sensors.append((Sx, Sy))
        beacons.append((Bx, By))
        radius = abs(Sx - Bx) + abs(Sy - By)
        #radii.append(radius)
        radius_on_y = radius - abs(Sy - Y_INTEREST)
        excluded.extend(range(Sx - radius_on_y, Sx+radius_on_y+1))
    excluded_set = set(excluded)
    beacons_set = set(beacons)
    # check that none are coords of B
    for c in list(beacons_set):
        if c[1] == Y_INTEREST and c[0] in excluded_set:
            excluded_set.remove(c[0])
    print(len(excluded_set))
