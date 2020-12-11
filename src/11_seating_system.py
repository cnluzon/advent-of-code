import numpy as np


class SeatLayout:
    OCCUPIED = "#"
    EMPTY = "L"
    FLOOR = "."

    def __init__(self, layout):
        self.layout = np.array(layout, dtype=str)

    def __str__(self):
        s = ""
        for row in self.layout:
            s += ''.join(row) + "\n"
        return s

    def get(self, row, col):
        if 0 <= row < self.layout.shape[0] and 0 <= col < self.layout.shape[1]:
            return self.layout[row, col]

    def get_neighborhood(self, row, col):
        neighborhood = []
        for r in [row-1, row, row+1]:
            for c in [col-1, col, col+1]:
                if r != row or c != col:
                    v = self.get(r, c)
                    if v:
                        neighborhood.append(v)
        return neighborhood

    def get_seats_in_sight(self, row, col):
        neighborhood = []
        for r in [-1, 0, 1]:
            for c in [-1, 0, 1]:
                if r != 0 or c != 0:
                    v = self.first_seat_in_direction(row, col, r, c)
                    if v:
                        neighborhood.append(v)
        return neighborhood

    def first_seat_in_direction(self, row, col, row_increment, col_increment):
        r = row + row_increment
        c = col + col_increment
        seat = self.get(r, c)
        found = seat != self.FLOOR
        while not found and seat:
            r += row_increment
            c += col_increment
            seat = self.get(r, c)
            found = seat != self.FLOOR

        return seat

    def update(self, mode="neighbors"):
        new_layout = np.zeros_like(self.layout, dtype=str)

        for row, row_values in enumerate(self.layout):
            for col, value in enumerate(row_values):
                if mode == "neighbors":
                    new_layout[row, col] = self.next_value(value, self.get_neighborhood(row, col))
                elif mode == "sight":
                    new_layout[row, col] = self.next_value(value, self.get_seats_in_sight(row, col), occupied_threshold=5)

        comparison = self.layout == new_layout
        if comparison.all():
            return False
        else:
            self.layout = new_layout
            return True

    def next_value(self, value, neighbors, occupied_threshold=4):
        if value == self.EMPTY:
            if (neighbors.count(self.EMPTY) + neighbors.count(self.FLOOR)) == len(neighbors):
                return self.OCCUPIED

        if value == self.OCCUPIED:
            if neighbors.count(self.OCCUPIED) >= occupied_threshold:
                return self.EMPTY

        return value

    def empty_seats(self):
        return str(self).count(self.EMPTY)

    def occupied_seats(self):
        return str(self).count(self.OCCUPIED)


def read_seat_layout(filename):
    with open(filename) as fi:
        mat = [list(line.strip()) for line in fi.readlines()]
        return SeatLayout(mat)


if __name__ == "__main__":
    seats = read_seat_layout("../data/11_full.txt")

    while seats.update(mode="sight"):
        pass

    # print(seats)

    print(seats.occupied_seats())

