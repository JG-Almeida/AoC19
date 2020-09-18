def main():
    # Open Day 8 puzzle input
    file_path = "day8.txt"

    image = get_layers(file_path)
    check_corruption(image.copy())
    processed_image = stack_layers(image.copy())

    print("Puzzle 2: ")
    for xs in processed_image:
        print(" ".join(map(str, xs)))


def get_layers(file_path):
    file = open(file_path, "r")

    puzzle_input = file.readline()
    puzzle_input = list(map(int, puzzle_input))
    image = []
    wide = 0
    tall = 0
    layer = []
    line = []

    # go through all values
    for i in puzzle_input:

        line.append(i)

        if tall == 24:
            layer.append(line)
            line = []
            tall = 0

            if wide == 5:
                image.append(layer)
                layer = []
                wide = 0
            else:
                wide = wide + 1
        else:
            tall = tall + 1

    # close file
    file.close()
    return image


def check_corruption(image):
    min_zeros = 25 * 6 + 1
    ones = 0
    twos = 0

    for i in range(len(image)):

        count_zeros = sum(x.count(0) for x in image[i])
        count_ones = sum(x.count(1) for x in image[i])
        count_twos = sum(x.count(2) for x in image[i])

        if count_zeros < min_zeros:
            min_zeros = count_zeros
            ones = count_ones
            twos = count_twos

    print("Puzzle 1: ", ones * twos)


def stack_layers(image):
    final_layer = []
    line = []

    for x in range(6):
        for y in range(25):
            for z in image:

                if z[x][y] == 0:
                    line.append(' ')
                    break
                elif z[x][y] == 1:
                    line.append('▓')
                    break

        final_layer.append(line)
        line = []

    return final_layer


if __name__ == '__main__':
    main()
