def main():
    # Open Day 6 puzzle input
    file_path = "day6.txt"

    parent = {"COM": "NONE"}
    level = {"COM": 0}
    orbits = get_orbits(file_path)
    print("Puzzle 1: ", count_orbits(orbits, parent, level))

    puzzle2(orbits, parent, level)


# Get file_path as a parameter, return dictionary with orbit objects
def get_orbits(file_path):
    file = open(file_path, "r")
    orbits = {}

    for row in file:
        line = row.split(')')
        line[1] = line[1][:-1]

        if line[1] not in orbits:
            orbits[line[1]] = []

        if line[0] in orbits:
            orbits[line[0]].append(line[1])
        else:
            orbits[line[0]] = [line[1]]

    # close file
    file.close()

    return orbits


# get level an parent of each object through a Breadth-first search
def get_level_and_parent(orbits, root, level, parent):
    discovered = [root]
    queue = [root]

    while queue:
        v = queue.pop(0)

        for edge in orbits[v]:
            if edge not in discovered:
                level[edge] = level[v] + 1
                parent[edge] = v
                queue.append(edge)
                discovered.append(edge)


# get level an parent of each object through a Depth-first search
def get_level_and_parent_dfs(orbits, root, level, parent):
    discovered = []
    stack = [root]

    while stack:
        v = stack.pop(0)

        if v not in discovered:
            discovered.append(v)
            for edge in orbits[v]:
                level[edge] = level[v] + 1
                parent[edge] = v
                stack.insert(0, edge)


# sum level of each object to get total
def count_orbits(orbits, parent, level):
    total = 0

    get_level_and_parent_dfs(orbits, "COM", level, parent)

    for x in level:
        total = total + level[x]

    return total


# builds the path from start to com through the parent
def build_path_to_com(parent, start):
    next_obj = parent[start]
    path = [start, next_obj]

    while next_obj != "COM":
        next_obj = parent[next_obj]
        path.append(next_obj)

    return path


# given two paths, returns the first common object
def find_common_obj(path1, path2):
    for obj_1 in path1:
        for obj_2 in path2:
            if obj_1 == obj_2:
                return obj_1

    return "COM"


# print solution for the second puzzle
def puzzle2(orbits, parent, level):
    # paths from you and san to com
    path_you = build_path_to_com(parent, "YOU")
    path_san = build_path_to_com(parent, "SAN")

    # find common object
    end_obj = find_common_obj(path_you, path_san)

    # sum levels of you and san and subtract common object twice
    total = level["YOU"] + level["SAN"] - level[end_obj]*2

    print("Puzzle 2: ", total - 2)


if __name__ == '__main__':
    main()
