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


def validate_split(ruledict, k, message):
    # Poda el diccionario para que solo tenga la rama 42
    pass

if __name__ == "__main__":
    rules_dict, messages = read_data_input("../data/19_loops.txt")

    result = validate(rules_dict, '0', messages[0])

    count = 0
    for m in messages:
        try:
            result = validate(rules_dict, '0', m)
        if result[0] and len(result[1]) == 0:
            count += 1

    print(count)