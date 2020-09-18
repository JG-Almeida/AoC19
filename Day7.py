import intcode_computer
import itertools


def main():
    # Open Day 7 puzzle input
    f = open("day7.txt", "r")

    # Read line and construct a list of integers
    line = f.readline()
    pz_input = line.split(',')
    pz_input = list(map(int, pz_input))

    puzzle1(pz_input.copy())
    puzzle2(pz_input.copy())

    # close file
    f.close()


def puzzle1(pz_input):
    max_val = 0
    phase_settings = list(itertools.permutations([0, 1, 2, 3, 4]))
    outputs = []

    for i in range(len(phase_settings)):
        inputs = list(phase_settings[i])
        inputs.insert(1, 0)

        # Amplifier 1
        intcode_computer.run_program(pz_input.copy(), inputs, outputs)
        inputs.insert(1, outputs.pop())

        # Amplifier 2
        intcode_computer.run_program(pz_input.copy(), inputs, outputs)
        inputs.insert(1, outputs.pop())

        # Amplifier 3
        intcode_computer.run_program(pz_input.copy(), inputs, outputs)
        inputs.insert(1, outputs.pop())

        # Amplifier 4
        intcode_computer.run_program(pz_input.copy(), inputs, outputs)
        inputs.insert(1, outputs.pop())

        # Amplifier 5
        intcode_computer.run_program(pz_input.copy(), inputs, outputs)
        value = outputs.pop()

        if value > max_val:
            max_val = value

    print("Puzzle 1: ", max_val)


def puzzle2(pz_input):
    phase_settings = list(itertools.permutations([5, 6, 7, 8, 9]))
    max_val = 0
    value = 0

    for i in range(len(phase_settings)):
        halt = 1
        pz_i1 = pz_input.copy()
        pz_i2 = pz_input.copy()
        pz_i3 = pz_input.copy()
        pz_i4 = pz_input.copy()
        pz_i5 = pz_input.copy()
        outputs = []
        amplifier_pointer = [0, 0, 0, 0, 0]
        inputs = [phase_settings[i][0], 0]

        # Amplifier 1
        amplifier_pointer[0] = intcode_computer.run_program(pz_i1, inputs, outputs, amplifier_pointer[0])
        inputs.insert(0, phase_settings[i][1])
        inputs.insert(1, outputs.pop())

        # Amplifier 2
        amplifier_pointer[1] = intcode_computer.run_program(pz_i2, inputs, outputs, 0)
        inputs.insert(0, phase_settings[i][2])
        inputs.insert(1, outputs.pop())

        # Amplifier 3
        amplifier_pointer[2] = intcode_computer.run_program(pz_i3, inputs, outputs, amplifier_pointer[2])
        inputs.insert(0, phase_settings[i][3])
        inputs.insert(1, outputs.pop())

        # Amplifier 4
        amplifier_pointer[3] = intcode_computer.run_program(pz_i4, inputs, outputs, amplifier_pointer[3])
        inputs.insert(0, phase_settings[i][4])
        inputs.insert(1, outputs.pop())

        # Amplifier 5
        amplifier_pointer[4] = intcode_computer.run_program(pz_i5, inputs, outputs, amplifier_pointer[4])
        inputs.insert(0, outputs.pop())

        while halt:

            # Amplifier 1
            amplifier_pointer[0] = intcode_computer.run_program(pz_i1, inputs, outputs, amplifier_pointer[0])
            inputs.insert(0, outputs.pop())

            # Amplifier 2
            amplifier_pointer[1] = intcode_computer.run_program(pz_i2, inputs, outputs, amplifier_pointer[1])
            inputs.insert(0, outputs.pop())

            # Amplifier 3
            amplifier_pointer[2] = intcode_computer.run_program(pz_i3, inputs, outputs, amplifier_pointer[2])
            inputs.insert(0, outputs.pop())

            # Amplifier 4
            amplifier_pointer[3] = intcode_computer.run_program(pz_i4, inputs, outputs, amplifier_pointer[3])
            inputs.insert(0, outputs.pop())

            # Amplifier 5
            amplifier_pointer[4] = intcode_computer.run_program(pz_i5, inputs, outputs, amplifier_pointer[4])
            inputs.insert(0, outputs.pop())

            if -1 in amplifier_pointer:
                halt = 0
                value = inputs[0]

        if value > max_val:
            max_val = value

    print("Puzzle 2: ", max_val)


if __name__ == '__main__':
    main()
