import intcode_computer


def main():
    # Open Day 2 puzzle input
    f = open("day2.txt", "r")

    # Read line and construct a list of integers
    line = f.readline()
    pz_input = line.split(',')
    pz_input = list(map(int, pz_input))

    puzzle1(pz_input.copy())
    puzzle2(pz_input)

    # close file
    f.close()


def puzzle1(pz_input):
    pz_input[1] = 12
    pz_input[2] = 2
    intcode_computer.run_program(pz_input)
    print("Puzzle 1:", pz_input[0])


# Beep Boop computer runs instruction
def run_computer(pz_input):
    intcode_computer.run_program(pz_input)
    return pz_input[0]


def puzzle2(pz_input):
    # iterate noun
    for noun in range(0, 99):
        # iterate verb
        for verb in range(0, 99):
            pz_input[1] = noun
            pz_input[2] = verb

            result = run_computer(pz_input.copy())

            # check for desired output
            if result == 19690720:
                print("Puzzle 2:", 100 * noun + verb)
                # solution found, no need to keep iterating
                return


if __name__ == '__main__':
    main()
