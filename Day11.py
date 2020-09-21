import intcode_computer


def main():
    # Open Day 11 puzzle input
    f = open("day11.txt", "r")

    # Read line and construct a list of integers
    line = f.readline()
    pz_input = line.split(',')
    pz_input = list(map(int, pz_input))

    # puzzle 1
    robot(pz_input.copy(), 0)

    # puzzle 2
    robot(pz_input.copy(), 1)

    # close file
    f.close()


# give the current direction and turn (1 for right and 0 for left)
# receive new direction
# direction is given by a number from 1 to 4, 1 is up and it rotates clockwise
def turn_robot(direction, turn):
    # if right
    if turn == 1:
        if direction == 4:
            direction = 1
        else:
            direction = direction + 1
    # if left
    else:
        if direction == 1:
            direction = 4
        else:
            direction = direction - 1
    return direction


# give position and direction
# receive new position
# robot always moves one
def move_robot(pos, direction):
    if direction == 1:
        pos = (pos[0], pos[1] + 1)
    elif direction == 2:
        pos = (pos[0] + 1, pos[1])
    elif direction == 3:
        pos = (pos[0], pos[1] - 1)
    elif direction == 4:
        pos = (pos[0] - 1, pos[1])
    else:
        print("whoops")

    return pos


# print hull drawing
def draw(hull, min_x, max_x, min_y, max_y):
    # go over the hull positions
    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x):

            # paint
            if (x, y) in hull:
                if hull[(x, y)] == 1:
                    print('▓', end='')

                elif hull[(x, y)] == 0:
                    print(' ', end='')
            else:
                print(' ', end='')
        print(" ")


# run painting robot
def robot(painting_robot, paint):
    # initialize variables
    pointer = 0
    inputs = [paint]
    outputs = []
    relative_base = [0]
    current_position = (0, 0)
    hull = {current_position: 0}
    direction = 1
    max_x = max_y = 0
    min_x = min_y = 0

    # run until halted
    while True:
        # run robot code Beep Bop
        pointer = intcode_computer.run_program(painting_robot, inputs, outputs, pointer, relative_base)

        # halted and should stop
        if pointer == -1:
            break

        # paint on current position
        hull[current_position] = outputs.pop(0)

        # calculate new direction
        direction = turn_robot(direction, outputs.pop(0))

        # calculate new position
        current_position = move_robot(current_position, direction)

        # paint sensor
        if current_position not in hull:
            inputs.append(0)
        else:
            inputs.append(hull[current_position])

        # receive max and min, x and y values, there is probably a better way to do this
        if current_position[0] < min_x:
            min_x = current_position[0]
        elif current_position[0] > max_x:
            max_x = current_position[0]

        if current_position[1] < min_y:
            min_y = current_position[1]
        elif current_position[1] > max_y:
            max_y = current_position[1]

    # paint input determines puzzle 1 or 2
    # should return values instead to make the code flexible but meh
    if paint == 0:
        print("Puzzle 1: ", len(hull))
    else:
        print("Puzzle 2: ")
        draw(hull, min_x, max_x, min_y, max_y)


if __name__ == '__main__':
    main()
