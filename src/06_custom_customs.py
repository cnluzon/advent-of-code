from typing import List
from common import split


class CustomForm:
    def __init__(self, answers):
        self.answers = set(answers)


class CustomFormGroup:
    def __init__(self, forms: List[CustomForm]):
        self.forms = forms

    def union_answers(self):
        acum = self.forms[0].answers
        for form in self.forms[1:]:
            acum = acum.union(form.answers)

        return acum

    def intersection_answers(self):
        acum = self.forms[0].answers
        for form in self.forms[1:]:
            acum = acum.intersection(form.answers)

        return acum


def parse_custom_forms(filename) -> List[CustomFormGroup]:
    with open(filename) as fi:
        group_list = []
        for group_info in split(fi.readlines(), "\n"):
            forms = [CustomForm(v.strip()) for v in group_info]
            group_list.append(CustomFormGroup(forms))
        return group_list


if __name__ == "__main__":
    groups = parse_custom_forms("../data/06_full.txt")

    solution = sum(len(g.union_answers()) for g in groups)
    print(solution)

    solution_all = sum(len(g.intersection_answers()) for g in groups)
    print(solution_all)
