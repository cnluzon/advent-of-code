from dataclasses import dataclass
import math
import numpy as np
from common import Point


class CircularMap:
  def __init__(self, mapfile, start):
    self.grid = self._read_map(mapfile)
    self.position = start
    

  def _read_map(self, mapfile):
    with open(mapfile) as fi:
      lines = fi.readlines()
      for index, values in enumerate(lines):
        lines[index] = [c for c in values.strip()]

      return np.matrix(lines)


  def move(self, h, v):
    self.position.x = (self.position.x + h) % self.grid.shape[1]

    if (self.position.y + v) < 0 or \
       (self.position.y + v) >= self.grid.shape[0]:
      raise ValueError("Illegal move")

    self.position.y = (self.position.y + v)


  def has_tree(self):
    """Returns true if current position is a tree"""
    return self.grid[self.position.y, self.position.x] == "#"


class Tobogganer:
  def __init__(self, map):
    self.map = map


  def go_to_start(self):
    self.map.position = Point(0, 0)


  def travel_counting_trees(self, h, v):
    ntrees = 0
    while not self.has_arrived():
      self.map.move(h, v)
      if (self.map.has_tree()):
        ntrees += 1
    return ntrees


  def has_arrived(self):
    return self.map.position.y == self.map.grid.shape[0] - 1


if __name__ == "__main__":
  tobogganer = Tobogganer(CircularMap("../data/03.txt", Point(0, 0)))

  ntrees = tobogganer.travel_counting_trees(3, 1)
  print(ntrees)

  ntrees_list = []

  for moves in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
    tobogganer.go_to_start()
    ntrees = tobogganer.travel_counting_trees(moves[0], moves[1])
    ntrees_list.append(ntrees)

  print(math.prod(ntrees_list))