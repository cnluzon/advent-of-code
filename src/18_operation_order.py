from dataclasses import dataclass
from typing import List

@dataclass
class Operation:
    formula: List[str]
    accepted_operators: List[str]

    def result(self, i):
        index = i
        current = None
        operator = None

        while index < len(self.formula):
            item = self.formula[index]
            if item in self.accepted_operators:
                operator = item
            elif item == "(":
                inner_value, index = self.result(index+1)
                if operator:
                    current = self.calculate(current, inner_value, operator)
                else:
                    current = inner_value
            elif item == ")":
                return current, index
            else:
                if operator:
                    current = self.calculate(current, item, operator)
                else:
                    current = item

            index += 1
        return current

    @staticmethod
    def calculate(a, b, op):
        return eval(f"{a}{op}{b}")


def read_input_data(filename) -> List[Operation]:
    with open(filename) as fi:
        for line in fi.readlines():
            values = list(line.strip())
            values = [item for item in values if item != " "]
            yield Operation(values, ["*", "+"])

if __name__ == "__main__":
    operation_list = list(read_input_data("../data/18_full.txt"))

    print(sum(op.result(0) for op in operation_list))
