import intcode_computer


def main():
    # Open Day 9 puzzle input
    f = open("day9.txt", "r")

    # Read line and construct a list of integers
    line = f.readline()
    pz_input = line.split(',')
    pz_input = list(map(int, pz_input))

    # Run program twice, once for each puzzle

    # input for puzzle 1 is 1
    inputs = [1]
    outputs = []
    relative_base = [0]
    intcode_computer.run_program(pz_input.copy(), inputs, outputs, 0, relative_base)
    print("Puzzle 1: ", outputs[0])

    # # input for puzzle 2 is 2
    inputs = [2]
    outputs = []
    relative_base = [0]
    intcode_computer.run_program(pz_input.copy(), inputs, outputs, 0, relative_base)
    print("Puzzle 2: ", outputs[0])

    # close file
    f.close()


if __name__ == '__main__':
    main()
