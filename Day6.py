import numpy as np


def main():
    # Open Day 6 puzzle input
    f = open("day6.txt", "r")

    orbits = get_orbits(f)
    puzzle1(orbits)
    puzzle2(orbits)

    # close file
    f.close()


# get the data from the file into an array
def get_orbits(file):
    # get first element of the array
    line = file.readline().split(')')
    line[1] = line[1][:-1]
    orbits = np.array(line).reshape(1, 2)

    # build the array by adding the remaining elements
    for row in file:
        line = row.split(')')
        line[1] = line[1][:-1]
        orbits = np.vstack([orbits, line])

    return orbits


# get all space objects in a list
def get_objects(orbits):
    objects = ['COM']

    for obj in orbits:
        objects.append(obj[1])

    return objects


# count total orbits
def count_orbits(objects, orbits):
    total = 0

    # for each object add to total its direct and indirect orbits
    for obj in objects:
        total = total + count_path_to_obj(obj, orbits, 0, "COM")

    return total


# find if the object is orbiting another
# if it is add one to the chain and call itself giving the object it orbits as the next object
def count_path_to_obj(obj, orbits, chain_number, end_obj):
    if obj != end_obj:
        for orb in orbits:
            if orb[1] == obj:
                return count_path_to_obj(orb[0], orbits, chain_number + 1, end_obj)
    return chain_number


# build list with orbits between first object and COM
def build_path_to_com(obj, orbits, path):
    for orb in orbits:
        if orb[1] == obj:
            path.append(orb[0])
            return build_path_to_com(orb[0], orbits, path)
    return path


# find the first common element in two lists
def find_common_obj(path1, path2):
    for obj_1 in path1:
        for obj_2 in path2:
            if obj_1 == obj_2:
                return obj_1


# get solution for the first puzzle
def puzzle1(orbits):
    objects = get_objects(orbits)
    print("Puzzle 1: ", count_orbits(objects, orbits))


# get solution for the first puzzle
def puzzle2(orbits):
    # path from you to com
    path_you = []
    path_you = build_path_to_com("YOU", orbits, path_you)

    # path from san to com
    path_san = []
    path_san = build_path_to_com("SAN", orbits, path_san)

    # object where the paths meet
    end_obj = find_common_obj(path_you, path_san)

    # sum paths
    total = count_path_to_obj("YOU", orbits, 0, end_obj)
    total = total + count_path_to_obj("SAN", orbits, 0, end_obj)

    print("Puzzle 2: ", total - 2)


if __name__ == '__main__':
    main()
