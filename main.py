#!/usr/bin/env python

import random

from player import Player


PAYOFF_MATRIX = [
    [(4, 4), (1, 6)],
    [(6, 1), (2, 2)]
]

ROUNDS = 20

class AlwaysCooperate:
    def select_move(self) -> bool:
        return False

    def record_last_moves(
        self,
        my_last_move: bool,
        opponent_last_move: bool
    ) -> None:
        pass


class AlwaysDefect:
    def select_move(self) -> bool:
        return True

    def record_last_moves(
        self,
        my_last_move: bool,
        opponent_last_move: bool
    ) -> None:
        pass


class TitForTat:
    def __init__(self):
        self.opponent_last_move = False

    def select_move(self) -> bool:
        return self.opponent_last_move

    def record_last_moves(
        self,
        my_last_move: bool,
        opponent_last_move: bool
    ) -> None:
        self.opponent_last_move = opponent_last_move


class SuspiciousTitForTat:
    def __init__(self):
        self.opponent_last_move = True

    def select_move(self) -> bool:
        return self.opponent_last_move

    def record_last_moves(
        self,
        my_last_move: bool,
        opponent_last_move: bool
    ) -> None:
        self.opponent_last_move = opponent_last_move


class TitForTwoTats:
    def __init__(self):
        self.opponent_history = []

    def select_move(self) -> bool:
        if len(self.opponent_history) < 2:
            return False

        return (
            self.opponent_history[-1]
            and self.opponent_history[-2]
        )

    def record_last_moves(
        self,
        my_last_move: bool,
        opponent_last_move: bool
    ) -> None:
        self.opponent_history.append(opponent_last_move)


class GrimTrigger:
    def __init__(self):
        self.triggered = False

    def select_move(self) -> bool:
        return self.triggered

    def record_last_moves(
        self,
        my_last_move: bool,
        opponent_last_move: bool
    ) -> None:
        if opponent_last_move:
            self.triggered = True


class RandomPlayer:
    def select_move(self) -> bool:
        return random.choice([False, True])

    def record_last_moves(
        self,
        my_last_move: bool,
        opponent_last_move: bool
    ) -> None:
        pass


def move_to_string(move: bool) -> str:
    return "D" if move else "C"


def play_game(
    player1,
    player2,
    payoff_matrix: list,
    rounds: int
) -> tuple[int, int]:

    score1 = 0
    score2 = 0

    for round_number in range(1, rounds + 1):
        move1 = player1.select_move()
        move2 = player2.select_move()

        payoff = payoff_matrix[move1][move2]

        score1 += payoff[0]
        score2 += payoff[1]

        player1.record_last_moves(move1, move2)
        player2.record_last_moves(move2, move1)

        print(
            f"{round_number:2}. kolo | "
            f"P1: {move_to_string(move1)} | "
            f"P2: {move_to_string(move2)} | "
            f"Score: {score1}:{score2}"
        )

    return score1, score2


def print_result(
    score1: int,
    score2: int,
    rounds: int
) -> None:

    if score1 > score2:
        result = "WIN"
    elif score1 < score2:
        result = "LOSS"
    else:
        result = "DRAW"

    print()
    print(f"Final score: {score1}:{score2}")
    print(f"Result: {result}")
    print(f"P1 average: {score1 / rounds:.2f}")
    print(f"P2 average: {score2 / rounds:.2f}")


def test(opponent_class, rounds: int = ROUNDS) -> None:
    print()
    print("=" * 60)
    print(f"Souper: {opponent_class.__name__}")
    print("=" * 60)

    player = Player(
        payoff_matrix=PAYOFF_MATRIX,
        number_of_iterations=rounds
    )

    opponent = opponent_class()

    score1, score2 = play_game(
        player,
        opponent,
        PAYOFF_MATRIX,
        rounds
    )

    print_result(score1, score2, rounds)


def test_against_self(rounds: int = ROUNDS) -> None:
    print()
    print("=" * 60)
    print("Player vs Player")
    print("=" * 60)

    player1 = Player(
        payoff_matrix=PAYOFF_MATRIX,
        number_of_iterations=rounds
    )

    player2 = Player(
        payoff_matrix=PAYOFF_MATRIX,
        number_of_iterations=rounds
    )

    score1, score2 = play_game(
        player1,
        player2,
        PAYOFF_MATRIX,
        rounds
    )

    print_result(score1, score2, rounds)


if __name__ == "__main__":
    random.seed(42)

    test(AlwaysCooperate)
    test(AlwaysDefect)
    test(TitForTat)
    test(SuspiciousTitForTat)
    test(TitForTwoTats)
    test(GrimTrigger)
    test(RandomPlayer)

    test_against_self()