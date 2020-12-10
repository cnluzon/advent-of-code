from dataclasses import dataclass, field
from typing import List


@dataclass
class AdapterSet:
    values: List[int]
    used: List[int] = field(default_factory=list)
    allowed_difference = 3

   def __post_init__(self):
        self.values = sorted(self.values)
        self.max_jolts = max(self.values) + 3

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
        for i in range(len(order)-1):
            diffs[order[i+1] - order[i]] += 1
        return diffs

    # When you made an elegant recursive solution and then realise
    # that the properties of the problem guarantee that the sorted
    # list IS the arrangement :D
    def compute_differences_silly(self):
        order = sorted(self.values)
        diffs = {i: 0 for i in range(1, 4)}
        diffs[order[0]] = 1
        diffs[3] += 1
        for i in range(len(order) - 1):
            diffs[order[i + 1] - order[i]] += 1

        return diffs


def read_values(filename):
    with open(filename) as fi:
        return [int(v) for v in fi.readlines()]


if __name__ == "__main__":
    values = read_values("../data/10.txt")
    print(list(sorted(values)))
    my_bag = AdapterSet(values)

    differences = my_bag.compute_differences(0)
    print(differences)
    print(differences[1]*differences[3])

    differences = my_bag.compute_differences_silly()
    print(differences)
    print(differences[1]*differences[3])

