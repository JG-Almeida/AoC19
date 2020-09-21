# This is the computer that runs the Intcode programs
def run_program(program, inputs=None, outputs=None, pointer=0, relative_base=None):
    if outputs is None:
        outputs = []
    if inputs is None:
        inputs = []
    if relative_base is None:
        relative_base = [0]
    i = pointer

    # program runs until it finds opcode 99 or finds an error
    while 1:
        instruction = str(program[i])
        opcode = int(instruction[-2:])
        mode = []
        param = []
        size = 0
        write_position = 0

        # get parameter modes
        for n in range(len(instruction) - 2, 0, -1):
            mode.append(int(instruction[n - 1]))

        # select instruction size
        if opcode in (1, 2, 7, 8):
            size = 3

        if opcode in (5, 6):
            size = 2

        if opcode in (3, 4, 9):
            size = 1

        if opcode == 99:
            size = 0

        # omitted modes are 0
        for n in range(len(mode), size):
            mode.append(0)

        if opcode != 99:
            # destination
            if mode[-1] == 0:
                write_position = program[i + size]
            elif mode[-1] == 2:
                write_position = program[i + size] + relative_base[0]

        # increase size of memory
        if len(program) <= write_position:
            for k in range(write_position + 1 - len(program)):
                program.append(0)

        # get parameters according to mode
        for n in range(1, size + 1):
            if mode[n - 1] == 1:
                param.append(program[i + n])
            elif mode[n - 1] == 2:
                pos = program[i + n] + relative_base[0]
                # increase size of memory
                if len(program) <= pos:
                    for k in range(pos + 1 - len(program)):
                        program.append(0)
                param.append(program[pos])
            else:
                pos = program[i + n]
                # increase size of memory
                if len(program) <= pos:
                    for k in range(pos + 1 - len(program)):
                        program.append(0)
                param.append(program[pos])

        # debug print
        # print("Instruction: ", instruction, "Mode: ", mode, "Param: ", param, "RBase: ", relative_base[0], "WritePos: ", write_position)
        # print(program)

        # Opcode 1: add:
        #   - Add together numbers read from two positions and store the result in a third position
        # 3 params:
        #   - The first two parameters indicate the positions from which to read the input values
        #   - The third parameter indicates the position at which the output should be stored
        if opcode == 1:
            program[write_position] = param[0] + param[1]
            i = i + 4
            continue

        # Opcode 2: multiply:
        #   - Multiply together numbers read from two positions and store the result in a third position
        # 3 params:
        #   - The first two parameters indicate the positions from which to read the input values
        #   - The third parameter indicates the position at which the output should be stored
        if opcode == 2:
            program[write_position] = param[0] * param[1]
            i = i + 4
            continue

        # Opcode 3: input
        #   - Takes a single integer as input and saves it to the position given by its only parameter
        # 1 param:
        #   - Position to save input
        if opcode == 3:
            if not inputs:
                return i
            program[write_position] = inputs[0]
            inputs.pop(0)
            i = i + 2
            continue

        # Opcode 4: output:
        #   - Outputs the value of its only parameter
        # 1 param:
        #   - Position to output
        if opcode == 4:
            # print(param[0])
            outputs.append(param[0])
            i = i + 2
            continue

        # Opcode 5: jump-if-true:
        #   - If the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter
        #   - Otherwise, it does nothing
        # 2 param:
        #   - Value to check
        #   - Jump position
        if opcode == 5:
            if param[0] != 0:
                i = param[1]
            else:
                i = i + 3
            continue

        # Opcode 6: jump-if-false:
        #   - If the first parameter is zero, it sets the instruction pointer to the value from the second parameter
        #   - Otherwise, it does nothing
        # 2 param:
        #   - Value to check
        #   - Jump position
        if opcode == 6:
            if param[0] == 0:
                i = param[1]
            else:
                i = i + 3
            continue

        # Opcode 7: less than:
        #   - If the first parameter is less than the second parameter,
        #       it stores 1 in the position given by the third parameter.
        #   - Otherwise, it stores 0
        # 3 param:
        #   - first two parameters are for comparison
        #   - third parameter is position to store
        if opcode == 7:
            if param[0] < param[1]:
                program[write_position] = 1
            else:
                program[write_position] = 0
            i = i + 4
            continue

        # Opcode 8: equals:
        #   - If the first parameter is equal to the second parameter,
        #       it stores 1 in the position given by the third parameter.
        #   - Otherwise, it stores 0
        # 3 param:
        #   - first two parameters are for comparison
        #   - third parameter is position to store
        if opcode == 8:
            if param[0] == param[1]:
                program[write_position] = 1
            else:
                program[write_position] = 0
            i = i + 4
            continue

        # Opcode 9: adjusts the relative base:
        #   - Adjusts the relative base by the value of its only parameter
        #   - The relative base increases (or decreases, if the value is negative) by the value of the parameter
        # 1 param:
        #   - Value to increase/decrease relative base by
        if opcode == 9:
            relative_base[0] = relative_base[0] + param[0]
            i = i + 2
            continue

        # Opcode 99: halt:
        #   - The program is finished and should immediately halt
        if opcode == 99:
            return -1

        return "ERROR - Incorrect Opcode !!!"
