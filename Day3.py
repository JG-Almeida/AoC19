import numpy as np


def main():
    # Open Day 3 puzzle input
    f = open("day3.txt", "r")

    # Read line and construct a list of directions
    line = f.readline()
    pz_input = line.split(',')
    wire_1 = create_wire_path(pz_input)

    # Read line and construct a list of directions
    line = f.readline()
    pz_input = line.split(',')
    wire_2 = create_wire_path(pz_input)

    # find intersections
    intersections = find_intersections(wire_1, wire_2)

    # get puzzle solutions
    print("Puzzle 1: ", find_distance(intersections))
    print("Puzzle 2: ", find_steps(intersections, wire_1, wire_2))

    # close file
    f.close()


# Construct wire path with given puzzle input
def create_wire_path(pz_input):
    # initialize array
    wire = np.array([0, 0]).reshape(1, 2)

    # go through all puzzle instructions
    for x in pz_input:
        line = np.array(wire[len(wire) - 1])

        # get direction and construct new coordinate
        if x[0] == 'R':
            line[0] = line[0] + int(x[1:])

        if x[0] == 'L':
            line[0] = line[0] - int(x[1:])

        if x[0] == 'U':
            line[1] = line[1] + int(x[1:])

        if x[0] == 'D':
            line[1] = line[1] - int(x[1:])

        # add new coordinate to array
        wire = np.vstack([wire, line])

    return wire


# find intersections given two wires
def find_intersections(wire_1, wire_2):
    intersections = np.array([0, 0]).reshape(1, 2)

    # go through both wires
    for w1 in range(1, len(wire_1) - 1):
        for w2 in range(1, len(wire_2) - 1):

            # check for wire intersection
            # wires going in different directions
            if wire_1[w1][0] == wire_1[w1 + 1][0] and wire_2[w2][1] == wire_2[w2 + 1][1]:
                # wire 2's y position is between wire 1's current and future y positions
                if wire_1[w1][1] <= wire_2[w2][1] <= wire_1[w1 + 1][1] or \
                        wire_1[w1][1] >= wire_2[w2][1] >= wire_1[w1 + 1][1]:
                    # wire 1's x position is between wire 2's current and future x positions
                    if wire_2[w2][0] <= wire_1[w1][0] <= wire_2[w2 + 1][0] or \
                            wire_2[w2][0] >= wire_1[w1][0] >= wire_2[w2 + 1][0]:
                        intersections = np.vstack([intersections, [wire_1[w1][0], wire_2[w2][1]]])

            # check for wire intersection
            # wires going in different directions
            if wire_1[w1][1] == wire_1[w1 + 1][1] and wire_2[w2][0] == wire_2[w2 + 1][0]:
                # wire 2's x position is between wire 1's current and future x positions
                if wire_1[w1][0] <= wire_2[w2][0] <= wire_1[w1 + 1][0] or \
                        wire_1[w1][0] >= wire_2[w2][0] >= wire_1[w1 + 1][0]:
                    # wire 1's y position is between wire 2's current and future y positions
                    if wire_2[w2][1] <= wire_1[w1][1] <= wire_2[w2 + 1][1] or \
                            wire_2[w2][1] >= wire_1[w1][1] >= wire_2[w2 + 1][1]:
                        intersections = np.vstack([intersections, [wire_2[w2][0], wire_1[w1][1]]])

    return intersections


# find the minimum distance from start to any of the intersections
def find_distance(intersections):

    # first intersection is the starting minimum
    min_num = (abs(intersections[1][0]) + abs(intersections[1][1]))

    # go through all intersections
    for i in range(2, len(intersections)):

        # calculate manhattan distance
        aux = (abs(intersections[i][0]) + abs(intersections[i][1]))

        # keep if new minimum
        if min_num > aux:
            min_num = aux

    return min_num


# count the steps a wire takes to a certain intersection
def count_steps(intersection, wire):
    total = 0
    break_flag = 1

    # run through each wire until intersection
    for i in range(len(wire)-1):

        # look for intersection
        # if wire's x position is the same as the intersection's x position
        if wire[i][0] == wire[i + 1][0] == intersection[0]:
            # if intersection's y position is between current and future wire's y position
            if wire[i][1] <= intersection[1] <= wire[i + 1][1] or \
                    wire[i][1] >= intersection[1] >= wire[i + 1][1]:
                break_flag = 0

        # look for intersection
        # if wire's y position is the same as the intersection's y position
        if wire[i][1] == wire[i + 1][1] == intersection[1]:
            # if intersection's x position is between current and future wire's x position
            if wire[i][0] <= intersection[0] <= wire[i + 1][0] or \
                    wire[i][0] >= intersection[0] >= wire[i + 1][0]:
                break_flag = 0

        if break_flag:
            # steps to next wire position
            new_stretch = abs(wire[i][0] - wire[i + 1][0]) + abs(wire[i][1] - wire[i + 1][1])
            total = total + new_stretch
        else:
            # steps to intersection
            new_stretch = abs(wire[i][0] - intersection[0]) + abs(wire[i][1] - intersection[1])
            total = total + new_stretch

            # exit cycle
            break

    return total


# find the fewest combined steps the wires must take to reach an intersection
def find_steps(intersections, wire_1, wire_2):

    # first intersection is the starting minimum
    min_num = count_steps(intersections[1], wire_1)  + count_steps(intersections[1], wire_2)

    # run through all intersections
    for i in range(2, len(intersections)):
        # get steps for each wire
        steps = count_steps(intersections[i], wire_1)
        steps = steps + count_steps(intersections[i], wire_2)

        # check if its a new minimum
        if min_num > steps or min_num == -1:
            min_num = steps

    return min_num


if __name__ == '__main__':
    main()
