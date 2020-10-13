import math


# Reaction object, with outcome, outcome quantity, chemicals necessary and quantity of chemicals necessary
class Reaction:
    def __init__(self, outcome, quantity, chemicals, quantity_chemicals):
        self.outcome = outcome
        self.quantity = quantity
        self.chemicals = chemicals
        self.quantity_chemicals = quantity_chemicals

    def __repr__(self):
        return f"Reaction({self.outcome!r}, {self.quantity!r}, {self.chemicals!r}, {self.quantity_chemicals!r})"

    def __str__(self):
        return f"Reaction Instance Object, (outcome, quantity, input chemicals, quantity of input chemicals) => " \
               f"({self.outcome!r}, {self.quantity!r}, {self.chemicals!r}, {self.quantity_chemicals!r})"

    # return the quantity of given chemical necessary
    def get_quantity(self, chemical):
        for x in range(len(self.chemicals)):
            if self.chemicals[x] == chemical:
                return self.quantity_chemicals[x]
        return 0


def main():
    # Day 14 puzzle input
    file_name = "day14.txt"

    reactions = parse_puzzle_input(file_name)

    level, max_level = puzzle1(reactions)

    puzzle2(reactions, level, max_level)


# parse puzzle input, return reaction list
def parse_puzzle_input(file):
    # Open file
    f = open(file, "r")

    reactions = {}

    # Read line and reaction list
    for line in f:
        chemicals = []
        quantity_chemicals = []

        line = line.split(" ")

        # go through the line, and build two lists, one for the chemical and another for its quantity
        for x in range(0, len(line), 2):
            # stop at arrow
            if line[x] == "=>":
                break

            quantity_chemicals.append(int(line[x]))
            chemicals.append(line[x + 1].strip(","))

        # build dictionary with reactions were the key is the outcome
        reactions[line[-1].strip("\n")] = Reaction(line[-1].strip("\n"), int(line[-2]), chemicals, quantity_chemicals)

    reactions['ORE'] = Reaction('ORE', 1, [], [])

    # close file
    f.close()

    return reactions


# print solution to puzzle 1
def puzzle1(reactions):
    level = {'FUEL': 0}
    max_level = 0

    # get level depth for each chemical
    get_level_of_chemical(reactions, 'FUEL', level)

    # calculate max level depth
    for x in level.values():
        if x > max_level:
            max_level = x

    ore_for_one_fuel = get_ore_for_one_fuel(reactions, level, max_level, 1)

    print("Puzzle 1: ", ore_for_one_fuel)

    return level, max_level


# get ore needed to create one fuel, get also leftover chemicals
def get_ore_for_one_fuel(reactions, level, max_level, fuel_needed):
    needs = {'FUEL': fuel_needed}

    # go through every level
    for x in range(0, max_level):
        # go through every chemical
        for y in level:
            # if chemical has level equivalent to the current being analyzed
            if x == level[y]:

                # if chemical being analysed will no longer be user for another's reactions due to level order
                if y in needs:
                    # needs value will me amount of reactions caused
                    needs[y] = math.ceil(needs[y] / reactions[y].quantity)

                # for each chemical needed for the reaction add its necessary quantity to needs
                for z in reactions[y].chemicals:
                    if z in needs:
                        needs[z] = needs[z] + reactions[y].get_quantity(z) * needs[y]
                    else:
                        needs[z] = reactions[y].get_quantity(z) * needs[y]

    return needs['ORE']


# calculate level depth of each chemical based on dependencies to other chemicals
def get_level_of_chemical(reactions, root, level):
    # ORE will always be the end point
    if root == 'ORE':
        return None

    # for each chemical follow its required chemicals until ORE adding checking the level along the way
    for x in reactions[root].chemicals:
        if x in level:
            if level[x] <= level[root]:
                level[x] = level[root] + 1
        else:
            level[x] = level[root] + 1

        get_level_of_chemical(reactions, x, level)


# print solution for puzzle 2
def puzzle2(reactions, level, max_level):
    total_ore = 1000000000000
    left = 0
    right = 1000000000000
    middle = 0

    # search for solution using a binary search
    while left <= right:

        middle = math.floor((left + right) / 2)

        ore_needed = get_ore_for_one_fuel(reactions, level, max_level, middle)

        if ore_needed < total_ore:
            left = middle + 1
        elif ore_needed > total_ore:
            right = middle - 1
        else:
            break

    print("Puzzle 2: ", middle - 1)


if __name__ == '__main__':
    main()
