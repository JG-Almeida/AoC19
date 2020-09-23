import math
import copy


# moon object, with position and velocity
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

    # calculate new velocity given another moon
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

    # update position with the current velocity
    def update_position(self):
        self.px = self.px + self.vx
        self.py = self.py + self.vy
        self.pz = self.pz + self.vz

    # calculate potential energy for the moon
    def get_potential_energy(self):
        return abs(self.px) + abs(self.py) + abs(self.pz)

    # calculate kinetic energy for the moon
    def get_kinetic_energy(self):
        return abs(self.vx) + abs(self.vy) + abs(self.vz)

    # calculate total energy for the moon
    def get_energy(self):
        return self.get_kinetic_energy() * self.get_potential_energy()


def main():
    # Open Day 12 puzzle input
    file_path = "day12.txt"

    moons = parse_file(file_path)
    puzzle1(copy.deepcopy(moons))
    puzzle2(moons)


# puzzle one solution
# find total energy after 1000 steps
def puzzle1(moons):
    # run 1000 steps
    for steps in range(1000):
        space_step(moons)

    total_energy = 0

    # calculate total energy in the system
    for moon in moons:
        total_energy = total_energy + moon.get_energy()

    print("Puzzle 1:", total_energy)


# puzzle two solution
# find the first step that is the same as a previous step
def puzzle2(moons):
    counter = 1
    x = y = z = 0

    # keep initial state in a list
    initial_state = []
    for moon in moons:
        initial_state.append(moon.px)
        initial_state.append(moon.py)
        initial_state.append(moon.pz)

    while True:
        current_state = []
        counter = counter + 1

        # update one step of the moons
        space_step(moons)

        # current state in a list
        for moon in moons:
            current_state.append(moon.px)
            current_state.append(moon.py)
            current_state.append(moon.pz)
            if not (moon.vx == moon.vy == moon.vz == 0):
                continue

        # first x cycle
        if current_state[0] == initial_state[0] and current_state[3] == initial_state[3] \
                and current_state[6] == initial_state[6] and current_state[9] == initial_state[9] and not x:
            x = counter

        # first y cycle
        if current_state[1] == initial_state[1] and current_state[4] == initial_state[4] \
                and current_state[7] == initial_state[7] and current_state[10] == initial_state[10] and not y:
            y = counter

        # first z cycle
        if current_state[2] == initial_state[2] and current_state[5] == initial_state[5] \
                and current_state[8] == initial_state[8] and current_state[11] == initial_state[11] and not z:
            z = counter

        # calculate the first time all cycles align through least common multiple
        if x and y and z:
            answer = lcm(x, lcm(y, z))
            print("Puzzle 2:", answer)
            break


# one step for all the moons
def space_step(moons):
    for main_moon in moons:
        for secondary_moon in moons:
            if main_moon != secondary_moon:
                main_moon.update_velocity(secondary_moon)

    for main_moon in moons:
        main_moon.update_position()


# parse puzzle input and return a list with the moons
def parse_file(file_path):
    # open file
    f = open(file_path, "r")
    moons = []

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


# least common multiple
def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)


if __name__ == '__main__':
    main()
