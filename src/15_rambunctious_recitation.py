from collections import defaultdict

numbers = [18, 11, 9, 0, 5, 1]

seen = defaultdict(list)
for i, n in enumerate(numbers, 1):
    seen[n] = [i]

last_number_spoken = numbers[-1]
recite_until = 30000000
for turn in range(len(numbers) + 1, recite_until+1):
    last_seen = seen.get(last_number_spoken, None)
    if len(last_seen) == 1:
        last_number_spoken = 0
    else:
        # has ben seen before
        last_number_spoken = last_seen[-1] - last_seen[-2]

    seen[last_number_spoken].append(turn)

    if turn == recite_until:
        print(f"Turn {turn}: {last_number_spoken}")

