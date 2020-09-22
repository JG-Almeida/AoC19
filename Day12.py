class Moon:
    def __init__(self, px, py, pz, vx, vy, vz):
        self.px = px
        self.py = py
        self.pz = pz
        self.vx = vx
        self.vy = vy
        self.vz = vz

    def __repr__(self):
        return f'Moon({self.px!r}, {self.py!r}, {self.pz!r}, {self.vx!r}, {self.vy!r}, {self.vz!r})'

    def __str__(self):
        return f'Moon Instance Object, (x, y) => ({self.px!r}, {self.py!r}, ' \
               f'{self.pz!r}, {self.vx!r}, {self.vy!r}, {self.vz!r})'

    def update_velocity(self, moon):
        if moon.px > self.px:
            self.vx = self.vx + 1
        elif moon.px < self.px:
            self.vx = self.vx - 1

        if moon.py > self.py:
            self.vy = self.vy + 1
        elif moon.py < self.py:
            self.vy = self.vy - 1

        if moon.pz > self.pz:
            self.vz = self.vz + 1
        elif moon.pz < self.pz:
            self.vz = self.vz - 1

    def update_position(self):
        self.px = self.px + self.vx
        self.py = self.py + self.vy
        self.pz = self.pz + self.vz

    def get_potential_energy(self):
        return abs(self.px) + abs(self.py) + abs(self.pz)

    def get_kinetic_energy(self):
        return abs(self.vx) + abs(self.vy) + abs(self.vz)

    def get_energy(self):
        return self.get_kinetic_energy() * self.get_potential_energy()


def main():
    # Open Day 12 puzzle input
    file_path = "day12_example.txt"

    moons = parse_file(file_path)

    puzzle1(moons.copy())
    puzzle2(moons.copy())


def puzzle1(moons):

    for steps in range(1000):
        space_step(moons)

    total_energy = 0

    for moon in moons:
        total_energy = total_energy + moon.get_energy()

    print("Puzzle 1:", total_energy)


def puzzle2(moons):
    steps = {}
    counter = 0

    while True:
        space_step(moons)

        key = get_key(moons)

        if key in steps:
            print("Puzzle 2:", counter)
            break
        else:
            steps[key] = counter

        counter = counter + 1


def get_key(moons):
    key = ""

    for moon in moons:
        key = key + str(moon.px) + str(moon.py) + str(moon.pz) + str(moon.vx) + str(moon.vy) + str(moon.vz)

    return key


def space_step(moons):
    for main_moon in moons:
        for secondary_moon in moons:
            if main_moon != secondary_moon:
                main_moon.update_velocity(secondary_moon)

    for main_moon in moons:
        main_moon.update_position()


def parse_file(file_path):
    # open file
    f = open(file_path, "r")
    moons = []
    x = y = z = 0

    for position in f:
        x = int(position[position.find('=') + 1: position.find(',')])
        position = position[position.find(',') + 1:]
        y = int(position[position.find('=') + 1: position.find(',')])
        position = position[position.find(',') + 1:]
        z = int(position[position.find('=') + 1: position.find('>')])

        moons.append(Moon(x, y, z, 0, 0, 0))

    # close file
    f.close()
    return moons


if __name__ == '__main__':
    main()
