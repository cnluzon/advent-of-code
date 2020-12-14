from dataclasses import dataclass
from typing import List


@dataclass
class Instruction:
    type: str


@dataclass
class MaskInstruction(Instruction):
    value: str


@dataclass
class MemoryInstruction(Instruction):
    value: int
    position: int


def parse_instruction(s) -> Instruction:
    typ, val = s.split(" = ")
    if typ == "mask":
        return MaskInstruction(typ, val.strip())
    elif typ[0:3] == "mem":
        pos = int(typ.split("[")[1][:-1])
        return MemoryInstruction("mem", int(val), pos)


def mask_value(int_value, mask):
    bin_str = bin(int_value)[2:]
    binary_value = list('0'*(len(mask)-len(bin_str)) + bin_str)
    # cut_mask = mask[-len(binary_value):]
    for i, b in enumerate(mask):
        if b != 'X':
            binary_value[i] = b

    return int(''.join(binary_value), 2)


def read_input_data(filename) -> List[Instruction]:
    with open(filename) as fi:
        return [parse_instruction(line) for line in fi.readlines()]


if __name__ == "__main__":
    instructions = read_input_data("../data/14.txt")
    print(instructions)

    memory = {}
    current_mask = instructions[0].value
    for index, instr in enumerate(instructions[1:], 1):
        if instr.type == "mask":
            current_mask = instr.value
        else:
            masked_value = mask_value(instr.value, current_mask)
            memory[instr.position] = masked_value

    print(sum(memory.values()))
