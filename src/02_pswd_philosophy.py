from dataclasses import dataclass
import re


@dataclass
class Policy:
  min_count: int
  max_count: int
  letter: str


class SledPolicy(Policy):
  def validate(self, password):
    counts = password.count(self.letter)
    return (counts >= self.min_count and counts <= self.max_count)


class TobogganPolicy(Policy):
  def validate(self, password):
    return (password[self.min_count-1] == self.letter) ^ \
           (password[self.max_count-1] == self.letter)


@dataclass
class Password:
  policy: Policy
  value: str
  
  @property
  def is_valid(self):
    return self.policy.validate(self.value)


def parse_password(s, policy_type):
  """Parse a password from a given string"""
  match = re.match(r"(\d+)-(\d+)\s(\w):\s+(\w+)", s)

  if match:
    min_count = int(match.group(1))
    max_count = int(match.group(2))
    letter = match.group(3)
    passwd = match.group(4)
  
    policy = policy_type(min_count, max_count, letter)
    return(Password(policy, passwd))

  return None


def read_passwords(file, policy_type=SledPolicy):
  passwds = []
  with open(file) as fi:
    passwds = [parse_password(s, policy_type=policy_type) for s in fi.readlines()]
  return passwds


if __name__ == "__main__":
  passwds = read_passwords("../data/02.txt", policy_type=SledPolicy)
  valid_pass_count = sum(p.is_valid for p in passwds if p)
  print(f"Valid passwords: {valid_pass_count}")
  
  passwds = read_passwords("../data/02.txt", policy_type=TobogganPolicy)
  valid_pass_count = sum(p.is_valid for p in passwds if p)
  print(f"New valid passwords: {valid_pass_count}")
