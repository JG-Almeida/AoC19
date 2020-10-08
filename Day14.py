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

    reactions = []

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

        reactions.append(Reaction(line[-1].strip("\n"), int(line[-2]), products, quantity_products))

    # close file
    f.close()

    return reactions


def puzzle1(reactions):
    reactions_index = {}

    for x in reactions:
        reactions_index[x.outcome] = x.products

    reactions_index['ORE'] = []

    level = get_level_of_product(reactions_index, 'FUEL')
    needs = {}
    max_level = list(level.values())[-1]

    for x in range(0, max_level):
        for y in level:
            if x < level[y]:
                break

            for z in reactions:
                if z.outcome == y:
                    if y not in needs:
                        for k in z.products:
                            needs[k] = z.get_quantity(k)
    print(needs)

def get_level_of_product(reactions, root):
    discovered = [root]
    queue = [root]
    level = {root: 0}

    while queue:
        v = queue.pop(0)

        for edge in reactions[v]:
            if edge not in discovered:
                level[edge] = level[v] + 1
                queue.append(edge)
                discovered.append(edge)
            else:
                level[edge] = level[v] + 1

    return level


if __name__ == '__main__':
    main()
