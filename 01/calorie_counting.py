#!/usr/bin/python
"""Python solution for Advent of Code 2022, Day 1: Calorie Counting"""

if __name__ == '__main__':

    # part 1: calories of the most loaded elf
    elves = []
    calories = []
    with open('input.txt', encoding='utf-8') as f_in:
        for line in f_in:
            line = line.strip()
            if len(line) > 0:
                cal = int(line)
                calories.append(cal)
            else:
                elves.append(calories)
                calories = []
    if len(calories) > 0:
        elves.append(calories)

    sum_calories = [sum(elf) for elf in elves]

    print(max(sum_calories))

    # part 2: calories of the top 3 most carrying elves
    sum_calories.sort(reverse=True)
    print(sum(sum_calories[:3]))
