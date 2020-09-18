import intcode_computer


def main():
    # Open Day 5 puzzle input
    f = open("day5.txt", "r")

    # Read line and construct a list of integers
    line = f.readline()
    pz_input = line.split(',')
    pz_input = list(map(int, pz_input))

    inputs = [1, 5]
    outputs = []

    # Run program twice, once for each puzzle
    # input for puzzle 1 is 1
    intcode_computer.run_program(pz_input.copy(), inputs, outputs)
    # input for puzzle 2 is 5
    intcode_computer.run_program(pz_input.copy(), inputs, outputs)

    print("Puzzle 1: ", outputs[-2])
    print("Puzzle 2: ", outputs[-1])

    # close file
    f.close()


if __name__ == '__main__':
    main()
