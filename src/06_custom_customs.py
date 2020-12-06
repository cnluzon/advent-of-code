import numpy as np
from typing import List
from common import split


class CustomForm:
    def __init__(self, answers):
        self.answers = answers

    def __len__(self):
        return len(self.answers)

    def to_binary(self):
        binary_rep = np.zeros(26, dtype=bool)
        for c in self.answers:
            index = ord(c) - ord('a')
            binary_rep[index] = True
        return binary_rep

    @classmethod
    def from_binary(cls, binary_rep):
        answers = ''
        for i, b in enumerate(binary_rep):
            if b:
                answers += chr(i + ord('a'))
        return cls(answers)


class CustomFormGroup:
    def __init__(self, forms: List[CustomForm]):
        self.forms = forms

    def common_answers(self):
        acum = self.forms[0].to_binary()
        for form in self.forms[1:]:
            acum = np.logical_or(acum, form.to_binary())

        return CustomForm.from_binary(acum)


def parse_custom_forms(filename) -> List[CustomFormGroup]:
    with open(filename) as fi:
        group_list = []
        for group_info in split(fi.readlines(), "\n"):
            forms = [CustomForm(v.strip()) for v in group_info]
            group_list.append(CustomFormGroup(forms))
        return group_list


if __name__ == "__main__":
    groups = parse_custom_forms("../data/06_full.txt")

    solution = sum(len(g.common_answers()) for g in groups)
    print(solution)
