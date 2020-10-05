import intcode_computer


class Tile:
    def __init__(self, x, y, tile_id):
        self.x = x
        self.y = y
        self.tile_id = tile_id

    def __repr__(self):
        return f"Tile({self.x!r}, {self.y!r}, {self.tile_id!r})"

    def __str__(self):
        return f"Tile Instance Object, (x, y) => ({self.x!r}, {self.y!r}, {self.tile_id!r})"


def main():
    file_name = "day13.txt"

    pz_input = parse_puzzle_input(file_name)
    tiles = puzzle1(pz_input.copy())
    draw_screen(tiles)

    print("Puzzle2:", puzzle2(pz_input.copy()))


def parse_puzzle_input(file):
    # Open Day 13 puzzle input
    f = open(file, "r")

    # Read line and construct a list of integers
    line = f.readline()
    pz_input = line.split(',')
    pz_input = list(map(int, pz_input))

    # close file
    f.close()

    return pz_input


def puzzle1(pz_input):
    pointer = 0
    inputs = []
    outputs = []
    relative_base = [0]

    intcode_computer.run_program(pz_input, inputs, outputs, pointer, relative_base)

    tiles, count_block, x, x, x = output_to_tiles(outputs)

    print("Puzzle1:", count_block)

    return tiles


def draw_screen(tiles):
    prev_y = 0

    for tile in tiles:
        if tile.y != prev_y:
            prev_y = tile.y
            print()

        if tile.tile_id == 0:
            print(' ', end='')
        elif tile.tile_id == 1:
            print('█', end='')
        elif tile.tile_id == 2:
            print('▞', end='')
        elif tile.tile_id == 3:
            print('▲', end='')
        elif tile.tile_id == 4:
            print('○', end='')
    print()


def output_to_tiles(outputs):
    tiles = []
    count_block = 0
    score = 0
    paddle_x = 0
    ball_x = 0

    while outputs:
        if outputs[0] == -1 and outputs[1] == 0:
            outputs.pop(0)
            outputs.pop(0)
            score = outputs.pop(0)
        else:
            tile_id = outputs.pop(2)
            tiles.append(Tile(outputs.pop(0), outputs.pop(0), tile_id))

            if tile_id == 2:
                count_block = count_block + 1
            if tile_id == 3:
                paddle_x = tiles[-1].x
            if tile_id == 4:
                ball_x = tiles[-1].x

    return tiles, count_block, score, paddle_x, ball_x


def puzzle2(pz_input):
    pz_input[0] = 2
    pointer = 0
    inputs = []
    outputs = []
    relative_base = [0]

    while True:
        intcode_computer.run_program(pz_input, inputs, outputs, pointer, relative_base)
        tiles, x, score, paddle_x, ball_x = output_to_tiles(outputs)
        print(score)
        draw_screen(tiles)

        if paddle_x > ball_x:
            joystick = -1
        elif paddle_x < ball_x:
            joystick = 1
        else:
            joystick = 0

        # if joystick == 'f':
        #     break
        # elif joystick == 'a':
        #     joystick = -1
        # elif joystick == 'd':
        #     joystick = 1
        # else:
        #     joystick = 0

        inputs.append(joystick)


if __name__ == '__main__':
    main()
