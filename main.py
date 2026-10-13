#!/usr/bin/env python

from player import Player

PAYOFF_MATRIX = [
    [(4, 4), (1, 6)],
    [(6, 1), (2, 2)]
]

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


def move_to_string(move: bool) -> str:
    if move:
        return "D"
    return "C"


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
            f"Player: {move_to_string(move1)} | "
            f"Opponent: {move_to_string(move2)} | "
            f"Score: {score1}:{score2}"
        )

    return score1, score2


def test(opponent_class, rounds: int = 100) -> None:
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

    print()
    print(f"Final score: {score1}:{score2}")


if __name__ == "__main__":
    test(AlwaysCooperate)
    test(AlwaysDefect)
    test(TitForTat)