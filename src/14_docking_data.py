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
    binary_value = list('0' * (len(mask) - len(bin_str)) + bin_str)
    # cut_mask = mask[-len(binary_value):]
    for i, b in enumerate(mask):
        if b != 'X':
            binary_value[i] = b

    return int(''.join(binary_value), 2)


def binary_generator(n):
    for i in range(0, 2 ** n):
        bin_val = bin(i)[2:]
        yield "0" * (n - len(bin_val)) + bin_val


def all_binary_values(masked_value):
    gen = binary_generator(masked_value.count('X'))
    result = []
    for g in gen:
        g_index = 0
        new_masked_value = masked_value[:]
        for b_index, b in enumerate(new_masked_value):
            if b == 'X':
                new_masked_value[b_index] = g[g_index]
                g_index += 1

        yield int(''.join(new_masked_value), 2)


def compute_all_addresses(int_value, mask):
    # 1. Fix the corresponding 1s and 0s in the mask
    bin_str = bin(int_value)[2:]
    binary_value = list('0' * (len(mask) - len(bin_str)) + bin_str)
    for i, b in enumerate(mask):
        if b != '0':
            binary_value[i] = b

    # 2. Combinatorially fill in all possible values
    return all_binary_values(binary_value)


def read_input_data(filename) -> List[Instruction]:
    with open(filename) as fi:
        return [parse_instruction(line) for line in fi.readlines()]


if __name__ == "__main__":
    instructions = read_input_data("../data/14.txt")

    # Version 1 decoder
    memory = {}
    current_mask = instructions[0].value
    for index, instr in enumerate(instructions[1:], 1):
        if instr.type == "mask":
            current_mask = instr.value
        else:
            masked_value = mask_value(instr.value, current_mask)
            memory[instr.position] = masked_value

    print(sum(memory.values()))

    # Version 2 decoder
    memory = {}
    current_mask = instructions[0].value
    for index, instr in enumerate(instructions[1:], 1):
        if instr.type == "mask":
            current_mask = instr.value
        else:
            all_addresses = compute_all_addresses(instr.position, current_mask)
            for p in all_addresses:
                memory[p] = instr.value

    print(sum(memory.values()))
