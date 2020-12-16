from dataclasses import dataclass
from typing import List
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
    print(ticket_info)

    print(ticket_info.scanning_error_rate)
