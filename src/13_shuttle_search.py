import math


def calculate_next_bus(buses, t):
    next_times = {}
    for v in buses:
        time = ((t // v) + 1) * v
        next_times[v] = time

    best_pick = sorted(next_times.items(), key=lambda x: x[1])[0]
    return best_pick[0] * (best_pick[1] - t)


def lcm(values):
    result = values[0]
    for i in values[1:]:
        result = result * i // math.gcd(result, i)
    return result


def validate_offsets(offset_list, t):
    for o in offset_list:
        if not ((t + o[1]) % o[0] == 0):
            return False

    return True


def calculate_periodicity(offset_list, step, offset):
    found = False
    i = offset
    found = validate_offsets(offset_list, i)
    while not found:
        i += step
        found = validate_offsets(offset_list, i)

    # Returns an offset over the period
    return i


def read_input_data(filename):
    with open(filename) as fi:
        lines = fi.readlines()
        timestamp = int(lines[0].strip())
        return (timestamp, lines[1])


if __name__ == "__main__":
    timestamp, values_str = read_input_data("../data/13.txt")

    buses_numbers = [int(v) for v in values_str.split(',') if v != 'x']

    print(calculate_next_bus(buses_numbers, timestamp))

    offsets = []
    for i, v in enumerate(values_str.split(',')):
        if v != 'x':
            offsets.append((int(v), i))

    # Fist step is one
    offset = 0
    global_period = offsets[0][0]

    for i in range(1, len(offsets)):
        offset = calculate_periodicity(offsets[0:i + 1], global_period, offset)
        global_period = lcm([o[0] for o in offsets[0:i + 1]])

    print("===")
    print(offset)
