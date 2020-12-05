import numpy as np


def binary_lookup(bin_seq, low_token="F", high_token="B"):
    cur_start: int = 0
    cur_end: int = 2 ** len(bin_seq)

    for b in bin_seq:
        if b == low_token:
            cur_end -= (cur_end - cur_start) // 2
        elif b == high_token:
            cur_start += (cur_end - cur_start) // 2

    return cur_start


class BoardingPass:
    def __init__(self, seat):
        self.seat_row = binary_lookup(seat[0:7], low_token="F", high_token="B")
        self.seat_col = binary_lookup(seat[7:], low_token="L", high_token="R")
        self.id = self.seat_row * 8 + self.seat_col


def read_boarding_passes(filename):
    plist = []
    with open(filename) as fi:
        for line in fi.readlines():
            plist.append(BoardingPass(line.strip()))

    return plist


def find_my_seat(plist):
    """
    Finds the only empty seat in the middle of the plane, excluding
    leading and trailing empty seats.
    """
    available_seats = 2 ** 7 * 8
    seats = np.zeros(available_seats, dtype=int)

    for p in plist:
        seats[p.id] = 1

    for i in range(1, len(seats)-1):
        if seats[i] != 0:
            continue
        if seats[i - 1] != 1 or seats[i + 1] != 1:
            continue
        return i


if __name__ == "__main__":
    boarding_passes = read_boarding_passes("../data/05_full.txt")

    # First half
    print(max(p.id for p in boarding_passes))

    # Second half
    my_seat = find_my_seat(boarding_passes)
    print(my_seat)
