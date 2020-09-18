import math


class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Asteroid({self.x!r}, {self.y!r})"

    def __str__(self):
        return f"Asteroid Instance Object, (x, y) => ({self.x!r}, {self.y!r})"

    # return distance between itself and another asteroid
    def distance(self, asteroid):
        return math.sqrt((self.x - asteroid.x) ** 2 + (self.y - asteroid.y) ** 2)

    # return angle between itself and another asteroid
    def angle(self, asteroid):
        if self.x == asteroid.x:
            if self.y > asteroid.y:
                value = -math.pi
            else:
                value = 0.0
        else:
            value = -math.atan2((asteroid.x - self.x), (asteroid.y - self.y))
        return value

    # return number of visible asteroids, brutally inefficient, kept as a monument to progress
    def count_asteroids(self, locations):
        # remove self from list
        locations.remove(self)

        i = 0
        while i < len(locations):
            ast = locations[i]
            i = i + 1

            # check if same column
            if ast.x != self.x:
                # check if same row
                if ast.y != self.y:
                    # calculate slope
                    slope = (self.y - ast.y) / (self.x - ast.x)

                    j = 0
                    # go through list of asteroids
                    while j < len(locations):
                        ast2 = locations[j]
                        j = j + 1

                        # if its the same object
                        if self == ast2 or ast == ast2:
                            continue

                        # if on the same line
                        if (ast2.y - self.y) == slope * (ast2.x - self.x):
                            # if same direction
                            if (ast2.y - self.y < 0 and ast.y - self.y < 0) \
                                    or (ast2.y - self.y > 0 and ast.y - self.y > 0):
                                locations.remove(ast2)
                                i = i - 1
                                j = j - 1

                else:
                    j = 0
                    # go through list of asteroids
                    while j < len(locations):
                        ast2 = locations[j]
                        j = j + 1

                        # continue if not same row or it is the same object
                        if ast.y != ast2.y or self == ast2 or ast == ast2:
                            continue

                        # remove the asteroid that is behind
                        if self.x > ast.x > ast2.x or ast2.x > ast.x > self.x:
                            locations.remove(ast2)
                            i = i - 1
                            j = j - 1
            else:
                j = 0
                # go through list of asteroids
                while j < len(locations):
                    ast2 = locations[j]
                    j = j + 1

                    # continue if not same column or it is the same object
                    if ast.x != ast2.x or self == ast2 or ast == ast2:
                        continue

                    # remove the asteroid that is behind
                    if self.y > ast.y > ast2.y or ast2.y > ast.y > self.y:
                        locations.remove(ast2)
                        i = i - 1
                        j = j - 1
        return len(locations)


def main():
    # Open Day 10 puzzle input
    file_path = "day10.txt"

    asteroid_locations = get_asteroid_locations(file_path)

    monitoring_station_angles, monitoring_station = puzzle1(asteroid_locations)

    puzzle2(monitoring_station_angles, monitoring_station)


# print puzzle 1 solution
def puzzle1(asteroid_locations):
    max_asteroids = 0
    most_visible_angle = {}
    most_visible = Asteroid(0, 0)

    for i in range(len(asteroid_locations)):
        angle = get_angles(asteroid_locations, asteroid_locations[i])
        value = len(angle)
        if value > max_asteroids:
            max_asteroids = value
            most_visible_angle = angle
            most_visible = asteroid_locations[i]

    print("Puzzle 1: ", max_asteroids)

    return most_visible_angle, most_visible


def puzzle2(monitoring_station_angles, monitoring_station):
    count_destroyed = 0
    destroyed = []
    lucky_number_200 = 0

    # until it destroys at least 200
    while lucky_number_200 == 0:
        # one spin
        for j in sorted(monitoring_station_angles):
            closest_asteroid = Asteroid(-1, -1)
            min_dist = -1

            # for each asteroid at an angle
            for i in monitoring_station_angles[j]:
                if i not in destroyed:
                    value = monitoring_station.distance(i)

                    if min_dist == -1 or value < min_dist:
                        min_dist = value
                        closest_asteroid = i

            if closest_asteroid.x != -1 and closest_asteroid.y != -1:
                destroyed.append(closest_asteroid)
                count_destroyed = count_destroyed + 1
                # print(count_destroyed, closest_asteroid)

                if count_destroyed == 200:
                    lucky_number_200 = closest_asteroid
                    break

    print("Puzzle 2: ", lucky_number_200.x * 100 + lucky_number_200.y)


def get_angles(asteroid_list, asteroid):
    angles = {}

    for ast in asteroid_list:

        if asteroid != ast:

            angle = asteroid.angle(ast)

            if angle in angles:
                angles[angle].append(ast)
            else:
                angles[angle] = [ast]

    return angles


def get_asteroid_locations(file_path):
    # open file
    file = open(file_path, "r")
    x = 0
    y = 0

    asteroid_locations = []

    for line in file:
        for position in line:
            if position == '#':
                asteroid_locations.append(Asteroid(x, y))
            x = x + 1
        y = y + 1
        x = 0

    # close file
    file.close()

    return asteroid_locations


if __name__ == '__main__':
    main()
