from typing import Tuple, Set
import itertools


class PocketHyperDimension:
    ACTIVE = True
    INACTIVE = False

    def __init__(self, initial_slice, dims=3):
        self.active = self.init_slice(initial_slice, dims=(dims-2))
        self.dimsize = dims

        # The ones that can get activated must be neighbors of at least one
        self.nearby_active = self.get_active_neighbors()

    def init_slice(self, s, dims) -> Set[Tuple]:
        cubes = []
        for y in range(len(s)):
            for x in range(len(s[0])):
                if s[x][y] == self.ACTIVE:
                    cubes.append(tuple([x, y] + [0]*dims))
        return set(cubes)

    def get_active_neighbors(self):
        neighbors_list = []
        for cube in self.active:
            n = self.get_neighbors(cube)
            neighbors_list.extend(n)
        return set(neighbors_list)

    def get_neighbors(self, c):
        values = []
        for dim in range(self.dimsize):
            values.append((c[dim]-1, c[dim], c[dim]+1))

        all_neighbors = set(itertools.product(*values))
        all_neighbors.remove(c)
        return all_neighbors

    def count(self, cube_list):
        result = {self.ACTIVE: 0, self.INACTIVE: 0}
        for c in cube_list:
            result[self.get(c)] += 1
        return result

    def get(self, cube):
        if cube in self.active:
            return self.ACTIVE
        else:
            return self.INACTIVE

    def step(self):
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
            self.active.add(c)

        for c in to_deactivate:
            self.active.remove(c)

        # Nearby needs to be updated
        self.nearby_active = self.get_active_neighbors()


def read_input_data(filename):
    data = []
    with open(filename) as fi:
        for line in fi.readlines():
            chr_values = list(line.strip())
            bool_values = []
            for v in chr_values:
                if v == "#":
                    bool_values.append(True)
                else:
                    bool_values.append(False)
            data.append(bool_values)

    return data


if __name__ == "__main__":
    my_pocket = PocketHyperDimension(read_input_data("../data/17_full.txt"), dims=3)

    for i in range(6):
        my_pocket.step()

    print(len(my_pocket.active))

    my_pocket = PocketHyperDimension(read_input_data("../data/17_full.txt"), dims=4)

    for i in range(6):
        my_pocket.step()

    print(len(my_pocket.active))
