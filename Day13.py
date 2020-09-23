import intcode_computer


def main():
    # Open Day 11 puzzle input
    f = open("day11.txt", "r")

    # Read line and construct a list of integers
    line = f.readline()
    pz_input = line.split(',')
    pz_input = list(map(int, pz_input))

    # puzzle 1

    # puzzle 2

    # close file
    f.close()


if __name__ == '__main__':
    main()