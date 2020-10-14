import math


def main():
    file_name = "day16.txt"

    pz_input = parse_puzzle_input(file_name)

    puzzle1(pz_input)


def parse_puzzle_input(file):
    # Open file with puzzle input
    f = open(file, "r")

    # Read line and construct a list of integers
    line = f.readline()
    pz_input = list(map(int, line))

    # close file
    f.close()

    return pz_input


def puzzle1(pz_input):
    row = pz_input
    pattern = [0, 1, 0, -1]

    for x in range(0, 100):
        row = phase(row, pattern)
    print(row[:8])


def phase(row, pattern):
    new_row = []
    row_pattern = pattern.copy()

    for j in range(len(row)):

        new_row.append(calculate_row(row_pattern, row))

        row_pattern.insert(0, pattern[0])
        row_pattern.insert(math.floor(len(row_pattern) / 2), pattern[1])
        row_pattern.insert(math.floor(len(row_pattern) * 3 / 4), pattern[2])
        row_pattern.append(pattern[-1])

    return new_row


def calculate_row(pattern, row):
    total = 0
    index = 0

    for value in row:
        if len(pattern) - 1 > index:
            index = index + 1
        else:
            index = 0

        total = total + value * pattern[index]

    return int(repr(total)[-1])


if __name__ == '__main__':
    main()
