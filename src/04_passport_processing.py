import re
from dataclasses import dataclass, field
from typing import Dict, List
from datetime import datetime
from typing import Any


@dataclass
class Field:
  key: str
  value: Any
  parsed_value: str


@dataclass
class YearField(Field):
  min_value: int = 0
  max_value: int = 0

  def __post_init__(self):
    self.value = int(self.value)

  def is_valid(self):
    return (self.value >= self.min_value) \
      and (self.value <= self.max_value) \
      and (len(str(self.value)) == 4)


@dataclass
class BirthYearField(YearField):
  min_value: int = 1920
  max_value: int = 2002


@dataclass
class IssueYearField(YearField):
  min_value: int = 2010
  max_value: int = datetime.now().year


@dataclass
class ExpirationYearField(YearField):
  min_value: int = datetime.now().year
  max_value: int = 2030


@dataclass
class HeightField(Field):
  unit: str = "None"

  def __post_init__(self):
    self.valid_units = ["cm", "in"]

    if (len(self.value) >= 3):
      self.unit = self.value[-2:]
      self.value = int(self.value[:-2])
    
    if self.unit == "cm":
      self.min_value = 150
      self.max_value = 193
    elif self.unit == "in":
      self.min_value = 59
      self.max_value = 76


  def is_valid(self):
    return ((self.unit in self.valid_units) \
      and self.value <= self.max_value and self.value >= self.min_value)


@dataclass
class HexColorField(Field):
  def is_valid(self):
    hex_expression = re.compile("#[0-9a-f]{6}")
    return bool(hex_expression.match(self.value))


@dataclass
class CategoricalField(Field):
  allowed_values: List[str] = field(default_factory=list)

  def is_valid(self):
    return self.value in self.allowed_values


@dataclass
class EyeColorField(CategoricalField):
  def __post_init__(self):
    self.allowed_values = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


@dataclass
class FixedLengthNumericalField(Field):
  def is_valid(self):
    field_expr = re.compile("[0-9]{9}")
    return bool(field_expr.match(self.value)) and len(self.value) == 9


@dataclass
class Passport:
  info: Dict[str, Field]
  required: List[str]


  def __str__(self):
    result = []
    for k in sorted(self.required):
      try:
        result.append(f"{self.info[k].parsed_value}")
      except KeyError:
        result.append("-")

    result.append(f"{self.is_valid()}")
    result.append(",".join(self.invalid_fields()))
    result.append(",".join(self.missing_fields()))
    return "\t".join(result)


  def is_valid(self):
    if len(self.missing_fields()) > 0:
      return False
    else:
      if len(self.invalid_fields()) > 0:
        return False

    return True


  def invalid_fields(self):
    keys = []
    for field in self.info.keys():
      if not self.info[field].is_valid():
        keys.append(field)

    return keys


  def missing_fields(self):
    keys = []
    for field in required:
      if not field in self.info.keys():
        keys.append(field)

    return keys


def split(sequence, sep):
  chunk = []
  for val in sequence:
    if val == sep:
      yield chunk
      chunk = []
    else:
      chunk.append(val)
  yield chunk


def parse_fields(pass_info, required):
  # Field types
  field_types = {
    "byr": BirthYearField,
    "iyr": IssueYearField,
    "eyr": ExpirationYearField,
    "hgt": HeightField,
    "hcl": HexColorField,
    "ecl": EyeColorField,
    "pid": FixedLengthNumericalField,
  }

  # This takes care of blank lines inconsistencies
  # str split is robust to any blanks
  pairs = " ".join(pass_info).split()
  field_dict = {}

  for p in pairs:
    (key, value) = p.split(":")
    if key in required:
      field = field_types[key](key, value, value)
      field_dict[key] = field
      
  return field_dict


def read_passports(filename, required):
  with open(filename) as fi:
    passport_list = []
    lines = fi.readlines()
    for passport_info in split(lines, "\n"):
      if passport_info:
        passport_fields = parse_fields(passport_info, required)
        passport_list.append(Passport(passport_fields, required))
      
    return passport_list


if __name__ == "__main__":
  required = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
  passports = read_passports("../data/04.txt", required)

  # First half
  print(sum((len(p.missing_fields()) == 0) for p in passports))

  # Second half
  print(sum(p.is_valid() for p in passports))

