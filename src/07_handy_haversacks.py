from dataclasses import dataclass
import networkx as nx


@dataclass
class BagGroup:
    color: str
    modifier: str
    amount: int

    @property
    def id(self):
        return f"{self.modifier}_{self.color}"


class BagRegulations:
    def __init__(self):
        self.dependencies = nx.DiGraph()

    def add_bags(self, bag_list):
        curr_nodes = self.dependencies.nodes
        self.dependencies.add_nodes_from([bag.id for bag in bag_list if bag.id not in curr_nodes])

    def add_rule(self, rule):
        container, contains = parse_rule(rule)

        self.add_bags([container] + contains)

        for bag in contains:
            self.dependencies.add_edge(container.id, bag.id, amount=bag.amount)

    def find_containers(self, bag_type):
        self._add_root_node()

        paths = nx.algorithms.all_simple_paths(self.dependencies, "root", "shiny_gold")
        resulting_bags = set()
        for p in paths:
            for item in p:
                if item not in ["root", bag_type]:
                    resulting_bags.add(item)

        self.dependencies.remove_node("root")
        return resulting_bags

    def _add_root_node(self):
        self.dependencies.add_node("root")
        for node in self.dependencies.nodes:
            predecessors = list(self.dependencies.predecessors(node))
            if not predecessors:
                self.dependencies.add_edge("root", node)

    def count_bags_inside(self, bag_type):
        bags_in = list(self.dependencies.successors(bag_type))
        # Base case: Does not contain anything
        if not bags_in:
            return 0
        # Recursive case: bags= edge * contents_inside(destination) for edge in children(bag_type)
        else:
            value = 0
            for b in bags_in:
                n_bags = self.dependencies.get_edge_data(bag_type, b)["amount"]
                value += self.count_bags_inside(b) * n_bags + n_bags

            return value


def parse_rule(r):
    container_str, contains_str = r.split(" contain ")

    container = parse_container(container_str)
    contains = parse_contains(contains_str)

    return container, contains


def parse_container(c):
    container_values = c.split()

    return BagGroup(color=container_values[1],
                    modifier=container_values[0],
                    amount=1)


def parse_contains(c):
    if c.strip() == "no other bags.":
        return []

    contains_str_list = c.split(",")

    contains = []
    for contains_str in contains_str_list:
        words = contains_str.split()

        new_bag = BagGroup(color=words[2],
                           modifier=words[1],
                           amount=int(words[0]))

        contains.append(new_bag)

    return contains


def read_bag_regulations(filename):
    regulations = BagRegulations()
    with open(filename) as fi:
        for rule in fi.readlines():
            regulations.add_rule(rule)

    return regulations


if __name__ == "__main__":
    current_regulations = read_bag_regulations("../data/07_full.txt")

    possible_bags = current_regulations.find_containers("shiny_gold")
    print(len(possible_bags))

    contained_bags = current_regulations.count_bags_inside("shiny_gold")
    print(contained_bags)
