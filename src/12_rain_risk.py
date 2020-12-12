from dataclasses import dataclass
from common import Point
from typing import List


@dataclass
class Ship:
    orientation: str

    def rotate(self, direction, degrees):
        direction_order = "NESW"
        steps = degrees // 90
        if direction == "L":
            steps = -steps

        new_index = (direction_order.index(self.orientation) + steps) % 4
        self.orientation = direction_order[new_index]


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
            self.move(instruction)
        elif instruction.type == "rotate":
            self.ship.rotate(instruction.code, instruction.value)

    def move(self, instruction):
        direction = instruction.code
        if instruction.code == "F":
            direction = self.ship.orientation

        x_incr = 0
        y_incr = 0
        if direction == "N":
            y_incr = instruction.value
        elif direction == "S":
            y_incr = -instruction.value
        elif direction == "E":
            x_incr = instruction.value
        elif direction == "W":
            x_incr = -instruction.value
        else:
            raise ValueError(f"Unknown direction: {direction}")

        self.current += Point(x_incr, y_incr)

    def distance_to_start(self):
        return self.current.manhattan(self.start)


@dataclass
class WaypointShip:
    anchor: Point
    waypoint: Point

    def normalize_direction(self, direction, degrees):
        if direction == "R":
            degrees = -degrees
        return degrees % 360

    def rotate(self, direction, degrees):
        diff = self.waypoint - self.anchor
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

        self.waypoint = self.anchor + Point(x, y)

    def move(self, times):
        for i in range(times):
            diff = self.waypoint - self.anchor
            self.anchor = self.waypoint
            self.waypoint += diff

    def move_waypoint(self, direction, value):
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
class WaypointNavigationSystem:
    ship: WaypointShip
    start: Point = Point(0, 0)

    def __post_init__(self):
        self.start = self.ship.anchor

    def update(self, instruction):
        if instruction.type == "move":
            if instruction.code in "NEWS":
                self.ship.move_waypoint(instruction.code, instruction.value)
            elif instruction.code == "F":
                self.ship.move(instruction.value)

        elif instruction.type == "rotate":
            self.ship.rotate(instruction.code, instruction.value)

    def distance_to_start(self):
        return self.ship.anchor.manhattan(self.start)


def read_instructions(filename) -> List[NavigationInstruction]:
    with open(filename) as fi:
        return [NavigationInstruction.from_str(line.strip()) for line in fi.readlines()]


if __name__ == "__main__":
    instructions = read_instructions("../data/12_full.txt")
    ferry_navigation = NavigationSystem(Ship("E"))

    print(ferry_navigation)
    for i in instructions:
        ferry_navigation.update(i)

    manhattan_distance = ferry_navigation.distance_to_start()
    print(manhattan_distance)

    wp_navigation = WaypointNavigationSystem(
        WaypointShip(anchor=Point(0, 0), waypoint=Point(10, 1))
    )

    print(wp_navigation)
    for i in instructions:
        wp_navigation.update(i)

    manhattan_distance = wp_navigation.distance_to_start()
    print(manhattan_distance)
