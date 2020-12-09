import itertools
from dataclasses import dataclass
from typing import List


@dataclass
class XMASValidator:
    values: List[int]
    window: List[int]

    def add_number(self, n):
        if self.is_valid(n):
            self.window = self.window[1:] + [n]
            return True
        else:
            return False

    def is_valid(self, n):
        for pick in itertools.combinations(self.window, 2):
            if len(set(pick)) == len(pick) and sum(pick) == n:
                return True
        return False

    def find_contiguous_sum(self, n):
        for i in range(len(self.values)):
            sum_values = self.contiguous_sum_ahead(i, n)
            if sum_values:
                return sum_values

    def contiguous_sum_ahead(self, start, n):
        accum = 0
        i = start
        while accum < n and i <= len(self.values):
            accum += self.values[i]
            i += 1

        if accum == n:
            return self.values[start: i]
        else:
            return None



def read_input_data(filename):
    with open(filename) as fi:
        values = [int(i.strip()) for i in fi.readlines() if i]
        return values


if __name__ == "__main__":
    values = read_input_data("../data/09_full.txt")

    preamble_length = 25
    preamble = values[0:preamble_length]

    xmas_validator = XMASValidator(values, preamble)
    for v in values[preamble_length:]:
        if not xmas_validator.add_number(v):
            print(v)
            sum_vals = xmas_validator.find_contiguous_sum(v)
            print(min(sum_vals) + max(sum_vals))
            exit()
