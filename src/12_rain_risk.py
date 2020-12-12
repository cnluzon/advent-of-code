from dataclasses import dataclass
from common import Point
from typing import List


@dataclass
class Ship:
    position: Point
    orientation: str

    def rotate(self, direction, degrees):
        direction_order = "NESW"
        steps = degrees // 90
        if direction == "L":
            steps = -steps

        new_index = (direction_order.index(self.orientation) + steps) % 4
        self.orientation = direction_order[new_index]

    def move(self, code, value):
        direction = code
        if code == "F":
            direction = self.orientation

        x_incr = 0
        y_incr = 0
        if direction == "N":
            y_incr = value
        elif direction == "S":
            y_incr = -value
        elif direction == "E":
            x_incr = value
        elif direction == "W":
            x_incr = -value
        else:
            raise ValueError(f"Unknown direction: {direction}")

        self.position += Point(x_incr, y_incr)


@dataclass
class WaypointShip(Ship):
    waypoint: Point

    def normalize_direction(self, direction, degrees):
        if direction == "R":
            degrees = -degrees
        return degrees % 360

    def rotate(self, direction, degrees):
        diff = self.waypoint - self.position
        degrees = self.normalize_direction(direction, degrees)

        x = 0
        y = 0
        if degrees == 90:
            x = -diff.y
            y = diff.x
        elif degrees == 180:
            x = -diff.x
            y = -diff.y
        elif degrees == 270:
            x = diff.y
            y = -diff.x
        else:
            x = diff.x
            y = diff.y

        self.waypoint = self.position + Point(x, y)

    def move(self, direction, value):
        if direction == "F":
            self._move_forward(value)
        else:
            self._move_waypoint(direction, value)

    def _move_forward(self, times):
        for i in range(times):
            diff = self.waypoint - self.position
            self.position = self.waypoint
            self.waypoint += diff

    def _move_waypoint(self, direction, value):
        x_incr = 0
        y_incr = 0
        if direction == "N":
            y_incr = value
        elif direction == "S":
            y_incr = -value
        elif direction == "E":
            x_incr = value
        elif direction == "W":
            x_incr = -value
        else:
            raise ValueError(f"Unknown direction: {direction}")

        self.waypoint += Point(x_incr, y_incr)

@dataclass
class NavigationInstruction:
    code: str
    value: int
    type: str

    @classmethod
    def from_str(cls, s):
        code = s[0]
        value = int(s[1:])
        if code in "NSWEF":
            inst_type = "move"
        else:
            inst_type = "rotate"

        return cls(code, value, inst_type)


@dataclass
class NavigationSystem:
    ship: Ship
    start: Point = Point(0, 0)
    current: Point = Point(0, 0)

    def __post_init__(self):
        self.current = self.start

    def update(self, instruction):
        if instruction.type == "move":
            self.ship.move(instruction.code, instruction.value)
        elif instruction.type == "rotate":
            self.ship.rotate(instruction.code, instruction.value)

    def distance_to_start(self):
        return self.ship.position.manhattan(self.start)


def read_instructions(filename) -> List[NavigationInstruction]:
    with open(filename) as fi:
        return [NavigationInstruction.from_str(line.strip()) for line in fi.readlines()]


if __name__ == "__main__":
    instructions = read_instructions("../data/12.txt")
    ferry_navigation = NavigationSystem(Ship(position=Point(0, 0), orientation="E"))

    for i in instructions:
        ferry_navigation.update(i)

    manhattan_distance = ferry_navigation.distance_to_start()
    print(manhattan_distance)

    # Change ship type
    wp_navigation = NavigationSystem(
        WaypointShip(position=Point(0, 0), waypoint=Point(10, 1), orientation="E")
    )

    for i in instructions:
        wp_navigation.update(i)

    manhattan_distance = wp_navigation.distance_to_start()
    print(manhattan_distance)
