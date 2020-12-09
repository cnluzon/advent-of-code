from dataclasses import dataclass, field
from typing import List
from enum import Enum


class ExecutionCode(Enum):
    SUCCESS = 0
    END_OF_PROGRAM = 1
    OUT_OF_MEMORY = -1
    REPEATED_OPERATION = -2


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

    def __len__(self):
        return len(self.boot_code)

    def reset(self):
        self.accumulator = 0
        self.inst_pointer = 0
        for op in self.boot_code:
            op.executed = False

    def swap(self, index):
        if self.boot_code[index].code == "nop":
            self.boot_code[index].code = "jmp"
        elif self.boot_code[index].code == "jmp":
            self.boot_code[index].code = "nop"

    def step(self) -> ExecutionCode:
        op = self.boot_code[self.inst_pointer]
        if op.executed:
            return ExecutionCode.REPEATED_OPERATION
        else:
            method = getattr(self, f"_execute_{op.code}")
            result_code = method(op)
            op.executed = True
            return result_code

    def run(self) -> ExecutionCode:
        exec_code = self.step()
        while exec_code == ExecutionCode.SUCCESS:
            exec_code = self.step()

        return exec_code

    def _execute_nop(self, op) -> ExecutionCode:
        self.inst_pointer += 1
        if self._code_ended():
            return ExecutionCode.END_OF_PROGRAM
        return ExecutionCode.SUCCESS

    def _execute_acc(self, op) -> ExecutionCode:
        self.accumulator += op.value
        self.inst_pointer += 1
        if self._code_ended():
            return ExecutionCode.END_OF_PROGRAM
        return ExecutionCode.SUCCESS

    def _execute_jmp(self, op) -> ExecutionCode:
        self.inst_pointer += op.value
        # Does a jmp +1 at the end of a program produce a END_OF_PROGRAM or an OUT_OF_MEMORY error?
        # I'm assuming that's success
        if self._code_ended():
            return ExecutionCode.END_OF_PROGRAM
        elif self.inst_pointer < 0 or self.inst_pointer > len(self.boot_code):
            return ExecutionCode.OUT_OF_MEMORY
        return ExecutionCode.SUCCESS

    def _code_ended(self):
        if self.inst_pointer == len(self.boot_code):
            return True
        return False


class GameBoyFactory:
    def __init__(self, a_game_boy):
        self.game_boy = a_game_boy

    def __iter__(self):
        for i in range(len(self.game_boy)):
            self.game_boy.swap(i)
            yield self.game_boy
            self.game_boy.swap(i)
            self.game_boy.reset()


def read_boot_code(filename):
    op_list = []
    with open(filename) as fi:
        for line in fi.readlines():
            op_list.append(parse_operation(line.strip()))

    return GameBoy(boot_code=op_list)


def parse_operation(line):
    code_str, value_str = line.split()
    value = int(value_str)
    return Operation(code=code_str, value=value)


if __name__ == "__main__":
    game_boy = read_boot_code("../data/08_full.txt")

    code = game_boy.run()
    print(game_boy.accumulator)

    game_boy.reset()
    factory = GameBoyFactory(game_boy)
    for gb in factory:
        code = gb.run()
        if code == ExecutionCode.END_OF_PROGRAM:
            print(gb.accumulator)
