import intcode_computer


def main():
    file_name = "day15.txt"

    pz_input = intcode_computer.parse_puzzle_input(file_name)

    repair_droid(pz_input)


# repair droid stumbles around until it maps the whole maze
def repair_droid(pz_input):
    pointer = 0
    inputs = []
    outputs = []
    relative_base = [0]
    layout = {}
    current_position = [0, 0]
    next_position = [0, 0]
    layout[str(current_position)] = 1
    memory = []
    oxygen = ""

    # robot movement
    while True:

        # chose direction to move, prioritizing unknown locations
        if str([current_position[0] + 1, current_position[1]]) not in layout:
            inputs.append(1)
            next_position = [current_position[0] + 1, current_position[1]]
            memory.append(2)

        elif str([current_position[0] - 1, current_position[1]]) not in layout:
            inputs.append(2)
            next_position = [current_position[0] - 1, current_position[1]]
            memory.append(1)

        elif str([current_position[0], current_position[1] + 1]) not in layout:
            inputs.append(3)
            next_position = [current_position[0], current_position[1] + 1]
            memory.append(4)

        elif str([current_position[0], current_position[1] - 1]) not in layout:
            inputs.append(4)
            next_position = [current_position[0], current_position[1] - 1]
            memory.append(3)

        # if all locations are known, backtrack
        else:
            # the memory keeps a list os steps to backtrack
            inputs.append(memory.pop())

            # adjust next position according to backtracking
            if inputs[0] == 1:
                next_position = [current_position[0] + 1, current_position[1]]

            elif inputs[0] == 2:
                next_position = [current_position[0] - 1, current_position[1]]

            elif inputs[0] == 3:
                next_position = [current_position[0], current_position[1] + 1]

            elif inputs[0] == 4:
                next_position = [current_position[0], current_position[1] - 1]

        # run robot computer with direction input
        intcode_computer.run_program(pz_input, inputs, outputs, pointer, relative_base)

        # the output informs us of whether the robot found a wall, an empty space or the oxygen machine
        if outputs[0] == 0:
            layout[str(next_position)] = 0
            memory.pop()

        elif outputs[0] == 1:
            layout[str(next_position)] = 1
            current_position = next_position

        elif outputs[0] == 2:
            oxygen = str(next_position)
            layout[str(next_position)] = 2
            current_position = next_position

        outputs.pop(0)

        # stop once all of the maze as been searched
        # if memory is empty, there are no more steps to backtrack meaning everything was explored
        # layout length check garantees that the robot doesn't stop immediately
        if len(memory) == 0 and len(layout) > 4:
            break

    # Puzzle 1 solution, get graph from layout and see distance from start to oxygen
    draw_layout(layout)
    graph = graph_from_layout(layout)
    level = get_level_dfs(graph, str([0, 0]))
    print("Puzzle 1: ", level[oxygen])

    # Puzzle 2 solution, level between oxygen and every room, then check maximum level depth
    level = get_level_dfs(graph, oxygen)
    max_oxi = 0

    for oxi in level:
        if level[oxi] > max_oxi:
            max_oxi = level[oxi]

    print("Puzzle 2: ", max_oxi-1)


# draw screen from layout
def draw_layout(layout):
    max_x = max_y = 0
    min_x = min_y = 0

    layout_positions = list(map(eval, layout))

    # check room dimensions
    for position in layout_positions:

        if position[0] > max_x:
            max_x = position[0]

        if position[1] > max_y:
            max_y = position[1]

        if position[0] < min_x:
            min_x = position[0]

        if position[1] < min_y:
            min_y = position[1]

    # go through every position and fill in corresponding character
    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x + 1):
            position = "[{}, {}]".format(x, y)

            if x == 0 and y == 0:
                # Robot starting point
                print('S', end='')

            else:
                if position in layout:

                    # wall
                    if layout[position] == 0:
                        print('█', end='')

                    # hallway
                    elif layout[position] == 1:
                        print('.', end='')

                    # Oxygen
                    elif layout[position] == 2:
                        print('O', end='')

                else:
                    # unknown, probably out of bounds
                    print('?', end='')
        print()


# convert layout to graph so we can do a graph search
def graph_from_layout(layout):
    graph = {}

    for position in layout:
        if layout[position] == 1 or layout[position] == 2:
            if position not in graph:
                graph[position] = []

            position = eval(position)

            # check if adjacent positions are not walls
            if layout[str([position[0], position[1] + 1])] == 1 or layout[str([position[0], position[1] + 1])] == 2:
                graph[str(position)].append(str([position[0], position[1] + 1]))

            if layout[str([position[0], position[1] - 1])] == 1 or layout[str([position[0], position[1] - 1])] == 2:
                graph[str(position)].append(str([position[0], position[1] - 1]))

            if layout[str([position[0] + 1, position[1]])] == 1 or layout[str([position[0] + 1, position[1]])] == 2:
                graph[str(position)].append(str([position[0] + 1, position[1]]))

            if layout[str([position[0] - 1, position[1]])] == 1 or layout[str([position[0] - 1, position[1]])] == 2:
                graph[str(position)].append(str([position[0] - 1, position[1]]))

    return graph


# get level of each object through a Depth-first search
def get_level_dfs(maze, root):
    discovered = []
    stack = [root]
    level = {root: 0}

    while stack:
        v = stack.pop(0)

        if v not in discovered:
            discovered.append(v)
            for edge in maze[v]:
                level[edge] = level[v] + 1
                stack.insert(0, edge)

    return level


if __name__ == '__main__':
    main()
