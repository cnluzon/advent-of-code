from dataclasses import dataclass, field
from typing import List


@dataclass
class Operation:
    code: str
    value: int
    executed: bool = False


@dataclass
class GameBoy:
    accumulator: int = 0
    inst_pointer: int = 0
    boot_code: List[Operation] = field(default_factory=list)

    def step(self):
        try:
            op = self.boot_code[self.inst_pointer]
        except IndexError:
            raise IndexError(f"Out of memory bounds: {self.inst_pointer}")

        if not op.executed:
            method = getattr(self, f"_execute_{op.code}")
            method(op)
            op.executed = True
            return True
        else:
            return False

    def find_loop(self):
        while self.step():
            pass
        return self.accumulator

    def _execute_nop(self, op):
        self.inst_pointer += 1

    def _execute_acc(self, op):
        self.accumulator += op.value
        self.inst_pointer += 1

    def _execute_jmp(self, op):
        self.inst_pointer += op.value


def read_boot_code(filename):
    op_list = []
    with open(filename) as fi:
        for line in fi.readlines():
            op_list.append(parse_operation(line.strip()))

    return GameBoy(boot_code=op_list)


def parse_operation(line):
    code, value = line.split()
    value = int(value)
    return Operation(code=code, value=value)


if __name__ == "__main__":
    game_boy = read_boot_code("../data/08_full.txt")

    print(game_boy.find_loop())