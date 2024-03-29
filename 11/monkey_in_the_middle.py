#!/usr/bin/python
"""Python solution for Advent of Code 2022, Day 11: Monkey in the Middle"""

from math import prod


class Monkey:
    def __init__(self, block: str):
        for line in block.splitlines():
            line = line.strip()
            if line.startswith('Monkey '):
                self.name = line[:-1]
            elif line.startswith('Starting items: '):
                line = line.replace(',', '')
                self.inventory = [int(x) for x in line.split()[2:]]
            elif line.startswith('Operation: '):
                self._operator = line.split()[4]
                self._operand = line.split()[5]
            elif line.startswith('Test: '):
                self._test = int(line.split()[-1])
            elif line.startswith('If true: '):
                self._target_true = int(line.split()[-1])
            elif line.startswith('If false: '):
                self._target_false = int(line.split()[-1])
            else:
                ValueError(f'Unable to read configuration block {block}')
        self.inspected_items = 0

    def throw_items(self, monkey_list, relief=lambda x: x // 3):
        for item in self.inventory:
            self.inspected_items += 1
            if self._operator == '+':
                item = item + int(self._operand)
            elif self._operator == '*':
                item = item * (item if self._operand == 'old' else int(self._operand))
            else:
                ValueError(f'Unable to carry out Operation {self._operator} {self._operand}')
            if relief is not None:
                item = relief(item)
            if item % self._test == 0:
                monkey_list[self._target_true].inventory.append(item)
            else:
                monkey_list[self._target_false].inventory.append(item)
        self.inventory = []


if __name__ == '__main__':
    # goal: find monkeys who inspected items most often
    #
    # strategy:
    # - read input, save monkey state and behaviour
    # - run 20 rounds of turn-based actions
    # - keep track of how often monkeys did stuff
    # - compare, take top two, multiply
    #
    # read input into monkeys:
    # - create monkey class: name, inventory, operation, test; action count
    # - items: just an int
    #
    # process rounds:
    # - loop through inventory
    # - take item, do operation, do test, add to other monkey
    # - can be a class function
    DEBUG = False

    # test
    # read input
    test_monkeys = []
    with open('example_1.txt', encoding='utf-8') as f_in:
        for monkey_block in f_in.read().split('\n\n'):
            test_monkeys.append(Monkey(monkey_block))
    # process rounds
    rounds = 20
    for i in range(rounds):
        for monkey in test_monkeys:
            monkey.throw_items(test_monkeys)
        if DEBUG:
            print(f'After round {i+1}, the monkeys are holding items with these worry levels:')
            for monkey in test_monkeys:
                print(f'{monkey.name}: {monkey.inventory}')
    if DEBUG:
        for monkey in test_monkeys:
            print(f'{monkey.name} inspected items {monkey.inspected_items} times')
    test_most = sorted([m.inspected_items for m in test_monkeys], reverse=True)[:2]
    # print(f'Example: Monkey business after 20 rounds: {test_most[0]*test_most[1]}')
    assert test_most[0]*test_most[1] == 10605

    # actual puzzle
    monkeys = []
    with open('input.txt', encoding='utf-8') as f_in:
        for monkey_block in f_in.read().split('\n\n'):
            monkeys.append(Monkey(monkey_block))
    for i in range(rounds):
        for monkey in monkeys:
            monkey.throw_items(monkeys)
    most = sorted([m.inspected_items for m in monkeys], reverse=True)[:2]
    print(f'Monkey business after 20 rounds: {most[0]*most[1]}')

    # part 2: no divide by 3, 10000 rounds
    #
    # problem: "worry levels" get large so fast that numbers become impossible to store
    #
    # options to "find another way to keep your worry levels manageable":
    # - larger int type?
    # -- breaks down at some other point then
    # - store numbers predivided by the possible divs of all monkeys
    # -- difficult to find a pattern
    # - find a pattern of repetition and use a shortcut
    # - try random relief strategies, maybe one still works
    #
    # on a hunch try this:
    # - multiply all the "divisible by" numbers, take rest when dividing by this
    # - this seems to work in example_1, but why?
    #
    # why does it work though?:
    # - the numbers are all prime numbers
    # - suppose a number A is divisible/not divisible by a prime X
    # - suppose number B is A mod X, B is 0 if divisible and nonzero otherwise
    # - for any operation of +Y, *Y or ()^2 it doesn't matter whether it is applied to A or B
    DEBUG = False
    rounds = 10000

    # need to reinitialize to get same start as previously
    # example_1
    test_monkeys = []
    with open('example_1.txt', encoding='utf-8') as f_in:
        for monkey_block in f_in.read().split('\n\n'):
            test_monkeys.append(Monkey(monkey_block))
    # relief_function = lambda x: x % (23*19*13*17)
    def test_relief_function(x): return x % prod(m._test for m in test_monkeys)
    for i in range(rounds):
        for monkey in test_monkeys:
            monkey.throw_items(test_monkeys, relief=test_relief_function)
        if DEBUG and (i+1 == 1 or i+1 == 20 or (i+1) % 1000 == 0):
            print(f'== After round {i+1} ==')
            for monkey in test_monkeys:
                print(f'{monkey.name} inspected items {monkey.inspected_items} times.')
    test_most = sorted([m.inspected_items for m in test_monkeys], reverse=True)[:2]
    # print(f'Example: Monkey business after 10000 rounds: {test_most[0]*test_most[1]}')
    assert test_most[0]*test_most[1] == 2713310158

    # do same for input
    monkeys = []
    with open('input.txt', encoding='utf-8') as f_in:
        for monkey_block in f_in.read().split('\n\n'):
            monkeys.append(Monkey(monkey_block))
    # relief_function = lambda x: x % (23*19*13*17)
    def relief_function(x): return x % prod(m._test for m in monkeys)
    for i in range(rounds):
        for monkey in monkeys:
            monkey.throw_items(monkeys, relief=relief_function)
        if DEBUG and (i+1 == 1 or i+1 == 20 or (i+1) % 1000 == 0):
            print(f'== After round {i+1} ==')
            for monkey in monkeys:
                print(f'{monkey.name} inspected items {monkey.inspected_items} times.')
    most = sorted([m.inspected_items for m in monkeys], reverse=True)[:2]
    print(f'Monkey business after 10000 rounds: {most[0]*most[1]}')
