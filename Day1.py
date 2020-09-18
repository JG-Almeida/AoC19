import math


def main():
    # Open Day 1 puzzle input
    f = open("day1.txt", "r")

    puzzle1(f)
    f.seek(0)   # reset file pointer
    puzzle2(f)

    # close file
    f.close()


def puzzle1(f):
    total = 0

    # calculate fuel for each module of the ship
    for x in f:
        aux = math.floor(int(x) / 3) - 2
        total = total + aux

    print("Puzzle 1:", total)


def puzzle2(f):
    total = 0

    # calculate fuel for each module of the ship
    for x in f:
        aux = int(x)

        # calculate fuel necessary to transport the modules + fuel
        while 1:
            aux = math.floor(aux / 3) - 2

            # check if the fuel necessary to transport the fuel is above 0
            if aux > 0:
                # get total
                total = total + aux
            else:
                # break free from module calculation
                break

    print("Puzzle 2:", total)


if __name__ == '__main__':
    main()
