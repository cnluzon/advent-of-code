import itertools
import math


def find_sum_set(values, expected_sum, n_elements):
  """
  Given a list of values, returns the product of the first n_elements found
  that sum expected_sum
  """
  for pick in itertools.combinations(values, n_elements):
    if (sum(pick)) == expected_sum:
      return math.prod(pick)


if __name__ == "__main__":
  values = []
  with open("../data/01.txt") as fi:
    values = [int(v) for v in fi.readlines()]

  result_1 = find_sum_set(values, 2020, 2)
  print(result_1)

  result_2 = find_sum_set(values, 2020, 3)
  print(result_2)
