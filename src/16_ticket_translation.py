from dataclasses import dataclass
from typing import List
import math
import re


@dataclass
class Field:
    value: int

    def is_rule_compliant(self, rule):
        for r in rule.valid_ranges:
            if self.value in r:
                return True
        return False


@dataclass
class ClosedInterval:
    start: int
    end: int

    def __contains__(self, value):
        return self.start <= value <= self.end


@dataclass
class FieldRule:
    name: str
    valid_ranges: List[ClosedInterval]

    @classmethod
    def from_string(cls, s):
        expr = re.compile("(.+): (\d+)-(\d+) or (\d+)-(\d+)")
        match = expr.match(s)
        ranges = [ClosedInterval(int(match.group(2)), int(match.group(3))),
                  ClosedInterval(int(match.group(4)), int(match.group(5)))]
        return cls(match.group(1), ranges)


@dataclass
class Ticket:
    values: List[Field]

    def __getitem__(self, i) -> Field:
        return self.values[i]

    @classmethod
    def from_string(cls, s):
        return cls([Field(int(v)) for v in s.split(",")])

    def validate(self, rules):
        invalid_fields = []
        for v in self.values:
            validations = [v.is_rule_compliant(r) for r in rules]
            if not any(validations):
                invalid_fields.append(v)
        return invalid_fields


@dataclass
class TicketKnowledge:
    rules: List[FieldRule]
    my_ticket: Ticket
    nearby_tickets: List[Ticket]

    @property
    def scanning_error_rate(self):
        ser = 0
        for ticket in self.nearby_tickets:
            ser += sum([t.value for t in ticket.validate(self.rules)])
        return ser

    def discard_invalid(self):
        new_ticket_list = []
        for ticket in self.nearby_tickets:
            if len(ticket.validate(self.rules)) == 0:
                new_ticket_list.append(ticket)

        self.nearby_tickets = new_ticket_list

    def assign_fields(self):
        # For a given column in the nearby tickets, it can only be
        # for a field where all the values are valid. So I go value
        # by value and find the set of rules it matches.
        # Get the common ones. If there are more than one, continue
        # to the next column.

        # Unassigned: column, rule
        unassigned = list(enumerate(self.rules))  # set([r.name for r in self.rules])
        possible_fields = {}
        assigned_fields = {}

        c = 0
        while len(unassigned) > 0:
            if c not in [assigned_fields.keys()]:
                column_values = [t[c] for t in self.nearby_tickets]
                matching_fields = self.find_matching_fields(column_values, [u[1] for u in unassigned])
                if len(matching_fields) == 1:
                    # Assign this one
                    assigned_fields[c] = matching_fields[0]

                    # Remove this possibility from the rest
                    unassigned = [u for u in unassigned if u[1].name != matching_fields[0]]
                    # Remove from the possibles, also
                    possible_fields = self.remove_value(possible_fields, matching_fields[0])

                    # While a possible field is left with length 1, assign it and try again.
                    assignable_field = self.get_assignable_field(possible_fields)
                    while not assignable_field is None:
                        assigned_fields[assignable_field] = possible_fields[assignable_field][0]
                        unassigned = [u for u in unassigned if u[1].name != possible_fields[assignable_field][0]]
                        possible_fields = self.remove_value(possible_fields, possible_fields[assignable_field][0])
                        assignable_field = self.get_assignable_field(possible_fields)

                else:
                    possible_fields[c] = matching_fields

            c = (c+1) % len(column_values)

        return assigned_fields


    def remove_value(self, possible, value):
        for k in possible:
            possible[k] = [item for item in possible[k] if item != value]

        return {k: possible[k] for k in possible if len(possible[k]) > 0}


    def get_assignable_field(self, possible):
        for k in possible:
            if len(possible[k]) == 1:
                return k
        return None


    def find_matching_fields(self, field_list, possible_rules):
        matching_fields = []
        for r in possible_rules:
            validations = [f.is_rule_compliant(r) for f in field_list]
            if all(validations):
                matching_fields.append(r.name)
        return matching_fields


def read_data_info(filename):
    with open(filename) as fi:
        rules = parse_rules(fi)
        header = fi.readline().strip()
        if header != "your ticket:":
            raise ValueError(f"Format error. Expected header found {header}")

        ticket = parse_tickets(fi)[0]
        header = fi.readline().strip()
        if header != "nearby tickets:":
            raise ValueError(f"Format error. Expected header found {header}")

        nearby = parse_tickets(fi)

        return TicketKnowledge(rules, ticket, nearby)


def parse_rules(fi):
    line = fi.readline().strip()
    rule_list = []
    while line:
        rule_list.append(FieldRule.from_string(line))
        line = fi.readline().strip()
    return rule_list


def parse_tickets(fi):
    line = fi.readline().strip()
    ticket_list = []
    while line:
        ticket_list.append(Ticket.from_string(line))
        line = fi.readline().strip()
    return ticket_list


if __name__ == "__main__":
    ticket_info = read_data_info("../data/16_full.txt")

    print(ticket_info.scanning_error_rate)

    print("===")
    ticket_info.discard_invalid()
    fields_assignment = ticket_info.assign_fields()

    departure_indexes = [k for k in fields_assignment.keys() if fields_assignment[k][0:9] == "departure"]

    values = []
    for i in departure_indexes:
        values.append(ticket_info.my_ticket[i].value)

    print(math.prod(values))
