import intcode_computer


def main():
    file_name = "day15.txt"

    pz_input = intcode_computer.parse_puzzle_input(file_name)

    puzzle1(pz_input)


def puzzle1(pz_input):
    pointer = 0
    inputs = []
    outputs = []
    relative_base = [0]
    layout = {}
    current_position = [0, 0]
    next_position = [0, 0]
    layout[str(current_position)] = 1
    count = 0

    while layout[str(current_position)] != 2:

        if str([current_position[0] + 1, current_position[1]]) not in layout:
            inputs.append(1)
            next_position = [current_position[0] + 1, current_position[1]]

        elif str([current_position[0] - 1, current_position[1]]) not in layout:
            inputs.append(2)
            next_position = [current_position[0] - 1, current_position[1]]

        elif str([current_position[0], current_position[1] + 1]) not in layout:
            inputs.append(3)
            next_position = [current_position[0], current_position[1] + 1]

        elif str([current_position[0], current_position[1] - 1]) not in layout:
            inputs.append(4)
            next_position = [current_position[0], current_position[1] - 1]

        else:
            if layout[str([current_position[0] + 1, current_position[1]])] != 0:
                inputs.append(1)
                next_position = [current_position[0] + 1, current_position[1]]

            elif layout[str([current_position[0] - 1, current_position[1]])] != 0:
                inputs.append(2)
                next_position = [current_position[0] - 1, current_position[1]]

            elif layout[str([current_position[0], current_position[1] + 1])] != 0:
                inputs.append(3)
                next_position = [current_position[0], current_position[1] + 1]

            elif layout[str([current_position[0], current_position[1] - 1])] != 0:
                inputs.append(4)
                next_position = [current_position[0], current_position[1] - 1]

        intcode_computer.run_program(pz_input, inputs, outputs, pointer, relative_base)

        if outputs[0] == 0:
            layout[str(next_position)] = 0
        elif outputs[0] == 1:
            layout[str(next_position)] = 1
            current_position = next_position

        outputs.pop(0)

        if count == 250:
            print(current_position)
            break
        else:
            count = count + 1

    draw_layout(layout)


# draw screen from tile list
def draw_layout(layout):
    max_x = max_y = 0
    min_x = min_y = 0

    layout_positions = list(map(eval, layout))

    for position in layout_positions:
        # position = eval(position)
        if position[0] > max_x:
            max_x = position[0]

        if position[1] > max_y:
            max_y = position[1]

        if position[0] < min_x:
            min_x = position[0]

        if position[1] < min_y:
            min_y = position[1]

    print(min_x, max_x, min_y, max_y)

    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            position = "[{}, {}]".format(x, y)

            if position in layout:
                if layout[position] == 0:
                    print('█', end='')

                elif layout[position] == 1:
                    print('.', end='')

                elif layout[position] == 2:
                    print('E', end='')

            else:
                print('?', end='')
        print()


if __name__ == '__main__':
    main()
