from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Passport:
  info: Dict[str, str]
  required: List[str]
  optional: List[str]

  def is_valid(self):
    return all([field in self.info.keys() for field in self.required])


def split(sequence, sep):
  chunk = []
  for val in sequence:
    if val == sep:
      yield chunk
      chunk = []
    else:
      chunk.append(val)
  yield chunk


def parse_passport(pass_info):
  # This takes care of blank lines inconsistencies
  # str split is robust to any blanks
  pairs = " ".join(pass_info).split()
  return {pair.split(":")[0]: pair.split(":")[1] for pair in pairs}


def read_passports(filename, required, optional):
  with open(filename) as fi:
    passport_list = []
    lines = fi.readlines()
    for passport_info in split(lines, "\n"):
      if passport_info:
        passport_fields = parse_passport(passport_info)
        passport_list.append(Passport(passport_fields, required, optional))
    
    return passport_list


if __name__ == "__main__":

  required = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
  optional = ["cid"]

  passwords = read_passports("../data/04_full.txt", required, optional)

  print(sum(p.is_valid() for p in passwords))