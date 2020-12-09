import itertools
from dataclasses import dataclass
from typing import List


@dataclass
class XMASValidator:
    values: List[int]

    def add_number(self, n):
        if self.is_valid(n):
            self.values = self.values[1:] + [n]
            return True
        else:
            return False

    def is_valid(self, n):
        for pick in itertools.combinations(self.values, 2):
            if len(set(pick)) == len(pick) and sum(pick) == n:
                return True
        return False


def read_input_data(filename):
    with open(filename) as fi:
        values = [int(i.strip()) for i in fi.readlines() if i]
        return values


if __name__ == "__main__":
    values = read_input_data("../data/09_full.txt")

    preamble_length = 25
    preamble = values[0:preamble_length]

    xmas_validator = XMASValidator(preamble)
    for v in values[preamble_length:]:
        if not xmas_validator.add_number(v):
            print(v)
            exit()
