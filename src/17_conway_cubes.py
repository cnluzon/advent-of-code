from typing import Tuple, Set


class PocketDimension:
    ACTIVE = "#"
    INACTIVE = "."

    def __init__(self, initial_slice):
        # Active cubes are sparse. Save coordinates
        self.active = self.init_slice(initial_slice, z=0)

        # The ones that can get activated must be neighbors of at least one. So I keep
        # A list of the near_active cubes
        self.nearby_active = self.get_active_neighbors()

    def init_slice(self, s, z=0) -> Set[Tuple[int, int, int]]:
        cubes = []
        for y in range(len(s)):
            for x in range(len(s[0])):
                if s[x][y] == self.ACTIVE:
                    cubes.append((x, y, z))
        return set(cubes)

    def get_active_neighbors(self):
        neighbors_list = []
        for cube in self.active:
            neighbors_list.extend(list(self.get_neighbors(cube)))
        return set(neighbors_list)

    @staticmethod
    def get_neighbors(c):
        for x in [c[0] - 1, c[0], c[0] + 1]:
            for y in [c[1] - 1, c[1], c[1] + 1]:
                for z in [c[2] - 1, c[2], c[2] + 1]:
                    if not (x == c[0] and y == c[1] and z == c[2]):
                        yield x, y, z

    def count(self, cube_list):
        result = {self.ACTIVE: 0, self.INACTIVE: 0}
        for c in cube_list:
            result[self.get(c[0], c[1], c[2])] += 1
        return result

    def get(self, x, y, z):
        if (x, y, z) in self.active:
            return self.ACTIVE
        else:
            return self.INACTIVE

    def set(self, x, y, z, value):
        current_value = self.get(x, y, z)
        if current_value == self.ACTIVE:
            if value == self.INACTIVE:
                self.active.remove((x, y, z))
        elif value == self.ACTIVE:
            self.active.add((x, y, z))

        # Nearby needs to be updated
        self.nearby_active = self.get_active_neighbors()

    def step(self):
        # Check elements that can be deactivated:
        to_deactivate = []
        to_activate = []

        for active_cube in self.active:
            neighbors = self.get_neighbors(active_cube)
            counts = self.count(neighbors)
            if not counts[self.ACTIVE] in [2, 3]:
                to_deactivate.append(active_cube)

        for nearby_cube in self.nearby_active:
            neighbors = self.get_neighbors(nearby_cube)
            counts = self.count(neighbors)
            if counts[self.ACTIVE] == 3:
                to_activate.append(nearby_cube)

        for c in to_activate:
            self.set(c[0], c[1], c[2], self.ACTIVE)

        for c in to_deactivate:
            self.set(c[0], c[1], c[2], self.INACTIVE)


class PocketDimension4D:
    ACTIVE = "#"
    INACTIVE = "."

    def __init__(self, initial_slice):
        # Active cubes are sparse. Save coordinates
        self.active = self.init_slice(initial_slice, z=0, w=0)

        # The ones that can get activated must be neighbors of at least one. So I keep
        # A list of the near_active cubes
        self.nearby_active = self.get_active_neighbors()

    def init_slice(self, s, z=0, w=0) -> Set[Tuple[int, int, int, int]]:
        cubes = []
        for y in range(len(s)):
            for x in range(len(s[0])):
                if s[x][y] == self.ACTIVE:
                    cubes.append((x, y, z, w))
        return set(cubes)

    def get_active_neighbors(self):
        neighbors_list = []
        for cube in self.active:
            neighbors_list.extend(list(self.get_neighbors(cube)))
        return set(neighbors_list)

    @staticmethod
    def get_neighbors(c):
        for x in [c[0] - 1, c[0], c[0] + 1]:
            for y in [c[1] - 1, c[1], c[1] + 1]:
                for z in [c[2] - 1, c[2], c[2] + 1]:
                    for w in [c[3] - 1, c[3], c[3] + 1]:
                        if not (x == c[0] and y == c[1] and z == c[2] and w == c[3]):
                            yield x, y, z, w

    def count(self, cube_list):
        result = {self.ACTIVE: 0, self.INACTIVE: 0}
        for c in cube_list:
            result[self.get(c[0], c[1], c[2], c[3])] += 1
        return result

    def get(self, x, y, z, w):
        if (x, y, z, w) in self.active:
            return self.ACTIVE
        else:
            return self.INACTIVE

    def set(self, x, y, z, w, value):
        current_value = self.get(x, y, z, w)
        if current_value == self.ACTIVE:
            if value == self.INACTIVE:
                self.active.remove((x, y, z, w))
        elif value == self.ACTIVE:
            self.active.add((x, y, z, w))

        # Nearby needs to be updated
        self.nearby_active = self.get_active_neighbors()

    def step(self):
        # Check elements that can be deactivated:
        to_deactivate = []
        to_activate = []

        for active_cube in self.active:
            neighbors = self.get_neighbors(active_cube)
            counts = self.count(neighbors)
            if not counts[self.ACTIVE] in [2, 3]:
                to_deactivate.append(active_cube)

        for nearby_cube in self.nearby_active:
            neighbors = self.get_neighbors(nearby_cube)
            counts = self.count(neighbors)
            if counts[self.ACTIVE] == 3:
                to_activate.append(nearby_cube)

        for c in to_activate:
            self.active.add((c[0], c[1], c[2], c[3]))

        for c in to_deactivate:
            self.active.remove((c[0], c[1], c[2], c[3]))

        # Nearby needs to be updated
        self.nearby_active = self.get_active_neighbors()


def read_input_data(filename):
    data = []
    with open(filename) as fi:
        for line in fi.readlines():
            data.append(list(line.strip()))
    return data


if __name__ == "__main__":
    my_pocket = PocketDimension4D(read_input_data("../data/17_full.txt"))

    for i in range(6):
        my_pocket.step()

    print(len(my_pocket.active))