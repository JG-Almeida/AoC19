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
        return f"Reaction Instance Object, (x, y) => ({self.outcome!r}, {self.quantity!r}, " \
               f"{self.products!r}, {self.quantity_products!r})"


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
            products.append(line[x + 1])

        reactions.append(Reaction(line[-1].strip("\n"), int(line[-2]), products, quantity_products))

    # close file
    f.close()

    return reactions


def puzzle1(reactions):
    reactions_index = {}
    index = 0

    for x in reactions:
        reactions_index[x.outcome] = index
        index = index + 1

    print(reactions_index)


if __name__ == '__main__':
    main()
