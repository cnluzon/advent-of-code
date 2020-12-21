from dataclasses import dataclass
from typing import List

@dataclass
class Operation:
    formula: List[str]
    accepted_operators: List[str]

    def result(self, formula, i):
        index = i
        current = None
        operator = None

        while index < len(formula):
            item = formula[index]
            if item in self.accepted_operators:
                operator = item
            elif item == "(":
                inner_value, index = self.result(formula, index+1)
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
        return current, index

    def result_precedence(self, formula, start, end, op="+"):
        # formula = self.formula
        sub_formula = formula[start:end]
        while op in sub_formula:
            sub_result, i, j = self.evaluate_around(sub_formula, sub_formula.index(op), sub_formula.index(op))
            sub_formula = sub_formula[:i] + [str(sub_result)] + sub_formula[j:]

        return int(self.result(sub_formula, 0)[0])

    def evaluate_around(self, formula, start, end):
        # formula[i] == operator.
        i = start-1
        j = end+1
        left = None
        right = None

        if formula[i] == ")":
            last_parenthesis = self.get_parenthesis_left(formula, i)
            left = self.result_precedence(formula, last_parenthesis, i+1)
            i = last_parenthesis
        else:
            left = int(formula[i])

        if formula[j] == "(":
            last_parenthesis = self.get_parenthesis_right(formula, j)
            right = self.result_precedence(formula, end+1, last_parenthesis+1)
            j = last_parenthesis + 1
        else:
            right = int(formula[j])
            j += 1

        return (left + right), i, j


    def get_parenthesis_left(self, formula, start):
        stack = []
        while start >= 0:
            if formula[start] == ")":
                stack.append(start)
            elif formula[start] == "(":
                stack.pop()
                if len(stack) == 0:
                    return start

            start -= 1

        return 0

    def get_parenthesis_right(self, formula, start):
        stack = []
        while start < len(formula):
            if formula[start] == "(":
                stack.append(start)
            elif formula[start] == ")":
                stack.pop()
                if len(stack) == 0:
                    return start
            start += 1

        return len(formula)

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
    operation_list = list(read_input_data("../data/18.txt"))

    i = 0
    results = []
    for i in range(len(operation_list)):
        form = ' '.join(operation_list[i].formula)
        value = int(operation_list[i].result_precedence(operation_list[i].formula, 0, len(operation_list[i].formula)))
        print(f"{form} = {value}")
        results.append(value)

    print(sum(results))


