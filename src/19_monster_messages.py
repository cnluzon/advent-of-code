from __future__ import annotations
from common import split


def parse_rule_dict(lines):
    rule_dict = {}
    for rule_str in lines:
        key, children = rule_str.strip().split(":")
        children = str.replace(children, '"', "")
        rule = children.split("|")
        rule_vals = [r.split() for r in rule]
        rule_dict[key] = rule_vals

    return rule_dict


def read_data_input(filename):
    with open(filename) as fi:
        lines = fi.readlines()
        chunks = list(split(lines, "\n"))
        rules = chunks[0]
        values = [c.strip() for c in chunks[1]]

        rule_dict = parse_rule_dict(rules)

        return rule_dict, values


def validate(ruledict, k, message):
    match = []
    for r in ruledict[k]:
        if r == ["a"] or r == ["b"]:
            if r[0] == message[0]:
                return [True, message[1:]]
            else:
                return [False, message]

        matched = True
        remaining = message
        for key in r:
            result = validate(ruledict, key, remaining)
            remaining = result[1]
            matched = matched and result[0]
            if not matched:
                break

        if matched:
            return [True, remaining]

    return [any(match), message[len(match):]]


def validate_split(ruledict, message):
    # The result matches the "expression" 42+ 42{n} 31{n}

    # At least one 42 complying part
    result = validate(rules_dict, '42', message)
    valid = result[0]
    remainder = result[1]

    # Then a number of 42 > = number of 31 after, since the first rule
    # generates an unlimited amount of 42-words
    n_42 = 0
    while valid and remainder != '':
        partial = validate(rules_dict, '42', remainder)
        valid = partial[0]
        if valid:
            n_42 += 1
            remainder = partial[1]

    n_31 = 0
    valid = True
    while valid and remainder != '':
        partial = validate(rules_dict, '31', remainder)
        valid = partial[0]
        if valid:
            n_31 += 1
            remainder = partial[1]

    if n_42 >= n_31 >= 1 and remainder == '':
        return True

    return False


if __name__ == "__main__":
    rules_dict, messages = read_data_input("../data/19.txt")

    result = validate_split(rules_dict, messages[0])

    count = 0
    for m in messages:
        result = validate(rules_dict, '0', m)
        if result[0] and len(result[1]) == 0:
            count += 1

    print(count)

    rules_dict, messages = read_data_input("../data/19_full_loops.txt")

    count = 0
    for m in messages:
        result = validate_split(rules_dict, m)
        if result:
            count += 1

    print(count)