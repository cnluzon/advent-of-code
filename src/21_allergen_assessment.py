from dataclasses import dataclass, field
from typing import Set, List


@dataclass
class Food:
    ingredients: Set[str]
    allergens: Set[str]

    @classmethod
    def from_str(cls, line):
        ingredients_str, allergens_str = line.strip().split("(contains ")
        ingredients = ingredients_str.split()
        allergens_str = allergens_str.replace(")", "")
        allergens_str = allergens_str.replace(",", "")
        allergens = allergens_str.split()
        return cls(set(ingredients), set(allergens))


@dataclass
class Menu:
    dishes: List[Food]
    ingredients: Set[str] = field(default_factory=set)
    allergens: Set[str] = field(default_factory=set)

    def __post_init__(self):
        for d in self.dishes:
            self.ingredients = self.ingredients.union(d.ingredients)
            self.allergens = self.allergens.union(d.allergens)

    def remove_ingredient(self, name):
        for d in self.dishes:
            if name in d.ingredients:
                d.ingredients.remove(name)

        self.ingredients.remove(name)

    def remove_allergen(self, name):
        for d in self.dishes:
            if name in d.allergens:
                d.allergens.remove(name)

        self.allergens.remove(name)

    def get_dishes_by_allergen(self, name):
        result = []
        for d in self.dishes:
            if name in d.allergens:
                result.append(d)
        return result


@dataclass
class MenuSolver:
    menu: Menu

    def solve(self):
        # Solution is a dict ingredient - allergen
        solution = {}

        next_allergen = self.next_possible_allergen()
        while len(self.menu.allergens) > 0 and next_allergen:
            solution[next_allergen[1]] = next_allergen[0]
            # Update menu
            self.menu.remove_ingredient(next_allergen[0])
            self.menu.remove_allergen(next_allergen[1])

            # Find next allergen
            next_allergen = self.next_possible_allergen()

        return solution

    def count_non_allergen_ingredients(self):
        assigned = self.solve()
        count = 0
        for dish in self.menu.dishes:
            count += len(dish.ingredients)

        return count

    def next_possible_allergen(self):
        for allergen in self.menu.allergens:
            # Find all the dishes that have this marked and intersect them all
            dish_list = self.menu.get_dishes_by_allergen(allergen)
            inter = dish_list[0].ingredients
            for d in dish_list:
                inter = inter.intersection(d.ingredients)
            if len(inter) == 1:
                return list(inter)[0], allergen


def read_data_input(filename):
    with open(filename) as fi:
        menu = []
        lines = fi.readlines()
        for line in lines:
            menu.append(Food.from_str(line))
        return Menu(menu)


if __name__ == "__main__":
    menu = read_data_input("../data/21_full.txt")
    menu_solver = MenuSolver(menu)
    result = menu_solver.count_non_allergen_ingredients()
    print(result)

    menu = read_data_input("../data/21_full.txt")
    result = menu_solver.solve()
    dangerous_list = [result[k] for k in sorted(result.keys())]
    print(",".join(dangerous_list))
