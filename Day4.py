def main():
    solutions = []

    # puzzle solutions
    get_passwords(solutions, 245318, 765747)
    print("Puzzle 1: ", len(solutions))

    eliminate_large_groups(solutions)
    print("Puzzle 2: ", len(solutions))


# Find all numbers within range that obey the following criteria:
#   -Two adjacent digits are the same (like 22 in 122345)
#   -Going from left to right, the digits never decrease;
#       they only ever increase or stay the same (like 111123 or 135679)
# params:
#   -solution, list for possible solutions
#   -start & end, range of possible solutions
def get_passwords(solutions, start, end):
    # iterate over range
    for i in range(start, end):
        flag = 1

        # get number into an int list
        number = list(map(int, str(i)))

        # Going from left to right, the digits never decrease
        for n in range(len(number) - 1):
            if number[n] > number[n + 1]:
                flag = 0

        if flag:
            # Two adjacent digits are the same
            for n in range(len(number) - 1):
                if number[n] == number[n + 1]:
                    solutions.append(i)
                    break

    return solutions


# Receive possible solutions from first puzzle and eliminate those where
# the two adjacent matching digits are not part of a larger group of matching digits
def eliminate_large_groups(solutions):
    # control variables for cycle
    k = len(solutions)
    i = 0

    while i < k:
        aux = str(solutions[i])
        flag = 1

        # if at least one number is repeated twice and only twice
        for n in aux:
            if aux.count(n) == 2:
                flag = 0
                break

        # remove if number is invalid
        if flag:
            solutions.pop(i)
            # decrement control variables to adjust to list remove
            i = i - 1
            k = k - 1

        i = i + 1


if __name__ == '__main__':
    main()
