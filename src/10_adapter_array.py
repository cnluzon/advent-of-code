from dataclasses import dataclass, field
from typing import List
import numpy as np
import math
from itertools import chain, combinations

@dataclass
class AdapterSet:
    values: List[int]
    used: List[int] = field(default_factory=list)
    allowed_difference = 3

    def __post_init__(self):
        self.values = sorted(self.values)
        self.max_jolts = max(self.values) + 3
        self.values = [0] + self.values + [self.max_jolts]

    def find_valid_adapters(self, jolts):
        return filter(lambda x: jolts < x <= jolts + self.allowed_difference, self.values)

    def used_all(self):
        return len(self.values) == len(self.used)

    def find_valid_permutation(self, jolts):
        if jolts == (self.max_jolts - 3):
            return [self.max_jolts]

        for n in self.find_valid_adapters(jolts):
            return [n] + self.find_valid_permutation(n)

    def compute_differences(self, jolts):
        order = self.find_valid_permutation(jolts)
        diffs = {i: 0 for i in range(1, 4)}
        diffs[order[0]] = 1
        for i in range(len(order) - 1):
            diffs[order[i + 1] - order[i]] += 1
        return diffs

    # When you made an elegant recursive solution and then realise
    # that the properties of the problem guarantee that the sorted
    # list IS always the arrangement that uses ALL adapters :D
    def compute_differences_silly(self):
        order = sorted(self.values)
        diffs = {i: 0 for i in range(1, 4)}
        for i in range(len(order) - 1):
            diffs[order[i + 1] - order[i]] += 1

        return diffs

    def count_possible_arrangements(self):
        # Fix elements that are always going to be in all the solutions
        fixed_elements = np.zeros(len(self.values))
        for i in range(1, len(self.values) - 1):
            if self.values[i + 1] - self.values[i] == 3:
                fixed_elements[i] = 1
                fixed_elements[i + 1] = 1

        possibilities = []
        i = 1
        while i < (len(fixed_elements) - 1):
            if fixed_elements[i] == 0:
                p = self.count_ahead(fixed_elements, i, 0)
                # Only go powerset in sets of consecutive removable elements, where it's more difficult
                # to make assumptions
                possibilities.append(self.all_possible_arrangements(self.values[i-1:i+p+1]))
                i += p
            elif fixed_elements[i] == 1:
                i += 1

        # These arrangements are independent of each other, possibilities are a product
        return math.prod(possibilities)

    def all_possible_arrangements(self, values):
        # assume 0 and end are fixed
        arrangements = powerset(values[1:-1])
        count = 0
        for a in arrangements:
            if self.is_valid([values[0]] + list(a) + [values[-1]]):
                count += 1
        return count

    def is_valid(self, values):
        for i in range(len(values)-1):
            if values[i+1] - values[i] > 3:
                return False
        return True

    def count_ahead(self, iter, index, value):
        count = 0
        while iter[index] == value and index < len(iter):
            count += 1
            index += 1
        return count


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def read_values(filename):
    with open(filename) as fi:
        return [int(v) for v in fi.readlines()]


if __name__ == "__main__":
    values = read_values("../data/10_full.txt")

    my_bag = AdapterSet(values)

    differences = my_bag.compute_differences(0)
    print(differences)
    print(differences[1] * differences[3])

    differences = my_bag.compute_differences_silly()
    print(differences)
    print(differences[1] * differences[3])

    print(my_bag.count_possible_arrangements())
