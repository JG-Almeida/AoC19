import intcode_computer


class Tile:
    def __init__(self, x, y, tile_id):
        self.x = x
        self.y = y
        self.tile_id = tile_id

    def __repr__(self):
        return f"Tile({self.x!r}, {self.y!r}, {self.tile_id!r})"

    def __str__(self):
        return f"Tile Instance Object, (x, y) => ({self.x!r}, {self.y!r}, {self.tile_id!r})"


def main():
    file_name = "day13.txt"

    pz_input = parse_puzzle_input(file_name)
    tiles = puzzle1(pz_input.copy())
    print(tiles)


def parse_puzzle_input(file):
    # Open Day 13 puzzle input
    f = open(file, "r")

    # Read line and construct a list of integers
    line = f.readline()
    pz_input = line.split(',')
    pz_input = list(map(int, pz_input))

    # close file
    f.close()

    return pz_input


def puzzle1(pz_input):
    pointer = 0
    inputs = []
    outputs = []
    relative_base = [0]
    tiles = []
    count_block = 0

    intcode_computer.run_program(pz_input, inputs, outputs, pointer, relative_base)

    while outputs:
        tile_id = outputs.pop(2)
        tiles.append(Tile(outputs.pop(0), outputs.pop(0), tile_id))

        if tile_id == 2:
            count_block = count_block + 1

    print("Puzzle1:", count_block)

    return tiles


if __name__ == '__main__':
    main()
