import math


# TODO: rename product to chemical
# Reaction object, with outcome, outcome quantity, products necessary and quantity of products necessary
class Reaction:
    def __init__(self, outcome, quantity, products, quantity_products):
        self.outcome = outcome
        self.quantity = quantity
        self.products = products
        self.quantity_products = quantity_products

    def __repr__(self):
        return f"Reaction({self.outcome!r}, {self.quantity!r}, {self.products!r}, {self.quantity_products!r})"

    def __str__(self):
        return f"Reaction Instance Object, (outcome, quantity, input chemicals, quantity of input chemicals) => " \
               f"({self.outcome!r}, {self.quantity!r}, {self.products!r}, {self.quantity_products!r})"

    def get_quantity(self, product):
        for x in range(len(self.products)):
            if self.products[x] == product:
                return self.quantity_products[x]
        return 0


def main():
    # Day 14 puzzle input
    file_name = "day14_example.txt"

    reactions = parse_puzzle_input(file_name)
    puzzle1(reactions)


# parse puzzle input, return reaction list
def parse_puzzle_input(file):
    # Open file
    f = open(file, "r")

    reactions = {}

    # Read line and reaction list
    for line in f:
        products = []
        quantity_products = []

        line = line.split(" ")

        # go through the line, and build two lists, one for the product and another for its quantity
        for x in range(0, len(line), 2):
            # stop at arrow
            if line[x] == "=>":
                break

            quantity_products.append(int(line[x]))
            products.append(line[x + 1].strip(","))

        reactions[line[-1].strip("\n")] = Reaction(line[-1].strip("\n"), int(line[-2]), products, quantity_products)

    reactions['ORE'] = Reaction('ORE', 1, [], [])

    # close file
    f.close()

    return reactions


def puzzle1(reactions):
    level = {'FUEL': 0}
    get_level_of_product(reactions, 'FUEL', level)

    max_level = 0

    for x in level.values():
        if x > max_level:
            max_level = x

    needs = {'FUEL': 1}
    leftovers = {}

    for x in range(0, max_level):
        for y in level:
            if x == level[y]:
                if y in needs:
                    needs[y] = math.ceil(needs[y] / reactions[y].quantity)
                    leftovers[y] = needs[y] % reactions[y].quantity

                for z in reactions[y].products:
                    if z in needs:
                        needs[z] = needs[z] + reactions[y].get_quantity(z) * needs[y]
                    else:
                        needs[z] = reactions[y].get_quantity(z) * needs[y]
    print("Puzzle 1: ", needs['ORE'])

    puzzle2(reactions, leftovers, needs['ORE'], level, max_level)


def get_level_of_product(reactions, root, level):
    if root == 'ORE':
        return None
    for x in reactions[root].products:
        if x in level:
            if level[x] <= level[root]:
                level[x] = level[root] + 1
        else:
            level[x] = level[root] + 1

        get_level_of_product(reactions, x, level)


def puzzle2(reactions, leftovers_one_fuel, ore_needed, level, max_level):
    total_ore = 1000000000000
    total_fuel = 0
    leftovers = {}

    while total_ore > ore_needed:
        total_fuel = total_fuel + math.ceil(total_ore / ore_needed)

        for x in leftovers_one_fuel:
            if x not in leftovers:
                leftovers[x] = leftovers_one_fuel[x] * math.ceil(total_ore / ore_needed)
            else:
                leftovers[x] = leftovers[x] + leftovers_one_fuel[x] * math.ceil(total_ore / ore_needed)

        leftovers['ORE'] = total_ore % ore_needed

        leftovers_to_ore(reactions, leftovers, level, max_level)

        total_ore = leftovers['ORE']
        print(leftovers)

    print("Puzzle 2: ", total_fuel)


def leftovers_to_ore(reactions, leftovers, level, max_level):
    for z in range(0, max_level):
        for x in leftovers:
            if level[x] == z:
                if leftovers[x] == 0:
                    continue
                else:
                    for y in reactions[x].products:
                        if y in leftovers:
                            leftovers[y] = leftovers[y] + math.floor(leftovers[x] / reactions[x].quantity) \
                                           * reactions[x].get_quantity(y)
                        else:
                            leftovers[y] = math.floor(leftovers[x] / reactions[x].quantity) \
                                           * reactions[x].get_quantity(y)
                            leftovers[x] = math.ceil(leftovers[x] % reactions[x].quantity)
                    leftovers[x] = math.ceil(leftovers[x] % reactions[x].quantity)


if __name__ == '__main__':
    main()
