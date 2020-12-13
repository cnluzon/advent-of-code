
# 1005526
# 37,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,x,x,x,587,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,13,19,x,x,x,23,x,x,x,x,x,29,x,733,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,17

# 939
# 7,13,x,x,59,x,31,19

values = [int(v) for v in "7,13,x,x,59,x,31,19".split(',') if v != 'x']
timestamp = 939

values = [int(v) for v in "37,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,x,x,x,587,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,13,19,x,x,x,23,x,x,x,x,x,29,x,733,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,17".split(',') if v != 'x']
timestamp = 1005526


next_times = {}
for v in values:
    time = ((timestamp // v) + 1) * v
    next_times[v] = time

print(next_times.items())

best_pick = sorted(next_times.items(), key=lambda x: x[1])[0]
print(best_pick)

result = best_pick[0] * (best_pick[1]-timestamp)
print(result)