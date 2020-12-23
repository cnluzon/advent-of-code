from dataclasses import dataclass, field
from collections import deque
from common import split
from typing import List


@dataclass
class CombatGame:
    deck_1: deque
    deck_2: deque

    def play(self):
        while self._winner() == 0:
            card_1 = self.deck_1.popleft()
            card_2 = self.deck_2.popleft()

            if card_1 > card_2:
                self.deck_1.append(card_1)
                self.deck_1.append(card_2)
            elif card_2 > card_1:
                self.deck_2.append(card_2)
                self.deck_2.append(card_1)

        return self._winner()

    def _winner(self):
        if len(self.deck_1) == 0:
            return 2
        if len(self.deck_2) == 0:
            return 1

        return 0

    def calculate_score(self, player):
        score = 0
        deck = self.deck_1
        if player == 2:
            deck = self.deck_2

        for i in range(1, len(deck)+1):
            score += i * deck.pop()
        return score


@dataclass
class GameStatus:
    deck_1: deque
    deck_2: deque


@dataclass
class RecursiveCombatGame(CombatGame):
    previous_rounds: List[GameStatus] = field(default_factory=list)

    def play(self):
        while self._winner() == 0:
            round_winner = 0
            seen_it_before = self.check_previous_rounds(self.deck_1, self.deck_2)

            if seen_it_before:
                # Player 1 automatically wins
                return 1

            else:
                # Save this round status
                self.previous_rounds.append(GameStatus(self.deck_1.copy(), self.deck_2.copy()))

                card_1 = self.deck_1.popleft()
                card_2 = self.deck_2.popleft()

                if len(self.deck_1) >= card_1 and len(self.deck_2) >= card_2:
                    sub_deck_1 = self.deck_1.copy()
                    sub_deck_1 = deque([sub_deck_1.popleft() for i in range(card_1)])
                    sub_deck_2 = self.deck_2.copy()
                    sub_deck_2 = deque([sub_deck_2.popleft() for i in range(card_2)])
                    sub_game = RecursiveCombatGame(sub_deck_1, sub_deck_2)
                    round_winner = sub_game.play()
                elif card_1 > card_2:
                    round_winner = 1
                elif card_2 > card_1:
                    round_winner = 2

                if round_winner == 1:
                    self.deck_1.append(card_1)
                    self.deck_1.append(card_2)
                elif round_winner == 2:
                    self.deck_2.append(card_2)
                    self.deck_2.append(card_1)

        return self._winner()

    def check_previous_rounds(self, d1, d2):
        for round in self.previous_rounds:
            if d1 == round.deck_1 and d2 == round.deck_2:
                return True
        return False


def read_input_data(filename):
    with open(filename) as fi:
        lines = fi.readlines()
        decks = []
        for chunk in split(lines, "\n"):
            deck = []
            header = chunk[0]
            assert header[0:6] == "Player"

            for value in chunk[1:]:
                deck.append(int(value.strip()))

            decks.append(deck)

        return RecursiveCombatGame(deque(decks[0]), deque(decks[1]))


if __name__ == "__main__":
    game = read_input_data("../data/22_loop.txt")

    winner = game.play()
    print(game.calculate_score(winner))