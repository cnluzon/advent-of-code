from dataclasses import dataclass
import re

@dataclass
class Policy:
  min_count: int
  max_count: int
  letter: str


@dataclass
class Password:
  policy: Policy
  value: str

  @property
  def is_valid(self):
    counts = self.value.count(self.policy.letter)
    return (counts >= self.policy.min_count and counts <= self.policy.max_count)
  

def parse_password(s):
  """Parse a password from a given string"""
  match = re.match(r"(\d+)-(\d+)\s(\w):\s+(\w+)", s)

  if match:
    min_count = int(match.group(1))
    max_count = int(match.group(2))
    letter = match.group(3)
  
    passwd = match.group(4)
  
    return Password(
      Policy(min_count, max_count, letter),
      passwd
    )

  return None


if __name__ == "__main__":
  passwds = []
  with open("../data/02_full.txt") as fi:
    passwds = [parse_password(s) for s in fi.readlines()]

  valid_pass_count = sum(p.is_valid for p in passwds if p)
  print(f"Valid passwords: {valid_pass_count}")
  
