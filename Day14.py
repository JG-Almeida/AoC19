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
    file_name = "day14_example.txt"

    reactions = parse_puzzle_input(file_name)

    ore_for_one_fuel, leftovers, level, max_level = puzzle1(reactions)

    puzzle2(reactions, leftovers, ore_for_one_fuel, level, max_level)


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

    ore_for_one_fuel, leftovers = get_ore_for_one_fuel(reactions, level, max_level)

    print("Puzzle 1: ", ore_for_one_fuel)

    return ore_for_one_fuel, leftovers, level, max_level


# get ore needed to create one fuel, get also leftover chemicals
def get_ore_for_one_fuel(reactions, level, max_level):
    needs = {'FUEL': 1}
    leftovers = {}

    # go through every level
    for x in range(0, max_level):
        # go through every chemical
        for y in level:
            # if chemical has level equivalent to the current being analyzed
            if x == level[y]:

                # if chemical being analysed will no longer be user for another's reactions due to level order
                if y in needs:
                    # calculate leftovers
                    if y in leftovers:
                        if needs[y] >= reactions[y].quantity:
                            leftovers[y] = leftovers[y] + (needs[y] % reactions[y].quantity)
                        else:
                            leftovers[y] = (reactions[y].quantity - needs[y])
                    else:
                        if needs[y] >= reactions[y].quantity:
                            leftovers[y] = needs[y] % reactions[y].quantity
                        else:
                            leftovers[y] = (reactions[y].quantity - needs[y])
                    # needs value will me amount of reactions caused
                    needs[y] = math.ceil(needs[y] / reactions[y].quantity)

                # for each chemical needed for the reaction add its necessary quantity to needs
                for z in reactions[y].chemicals:
                    if z in needs:
                        needs[z] = needs[z] + reactions[y].get_quantity(z) * needs[y]
                    else:
                        needs[z] = reactions[y].get_quantity(z) * needs[y]

    return needs['ORE'], leftovers


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


# TODO: there seems to be some miscalculation along the way or perhaps flawed logic
def puzzle2(reactions, leftovers_one_fuel, ore_needed, level, max_level):
    total_ore = 1000000000000
    total_fuel = 0
    leftovers = {}

    while total_ore > ore_needed:

        # total fuel is current fuel plus current ore divided by the amount of ore necessary for for one fuel
        total_fuel = total_fuel + math.floor(total_ore / ore_needed)

        # multiply leftovers for a single fuel by the amount of fuel created
        for x in leftovers_one_fuel:
            if x not in leftovers:
                leftovers[x] = leftovers_one_fuel[x] * math.floor(total_ore / ore_needed)
            else:
                leftovers[x] = leftovers[x] + leftovers_one_fuel[x] * math.floor(total_ore / ore_needed)

        # leftover ore is the remainder of the division
        leftovers['ORE'] = total_ore % ore_needed

        # transform leftovers back to ore as much as possible
        leftovers_to_ore(reactions, leftovers, level, max_level)

        # current ore to create fuel will be the leftover ore plus ore from leftovers
        total_ore = leftovers['ORE']

    print("Puzzle 2: ", total_fuel)


# reverts leftovers into ore
def leftovers_to_ore(reactions, leftovers, level, max_level):
    
    for z in range(0, max_level):
        for x in leftovers:
            if level[x] == z:
                if leftovers[x] == 0:
                    continue
                for y in reactions[x].chemicals:
                    if y in leftovers:
                        leftovers[y] = leftovers[y] + math.floor(leftovers[x] / reactions[x].quantity) \
                                       * reactions[x].get_quantity(y)
                    else:
                        leftovers[y] = math.floor(leftovers[x] / reactions[x].quantity) \
                                       * reactions[x].get_quantity(y)
                leftovers[x] = leftovers[x] % reactions[x].quantity


if __name__ == '__main__':
    main()
