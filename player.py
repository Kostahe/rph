class Player:
    OBSERVATION_ROUNDS = 5
    SHORT_GAME_THRESHOLD = 5

    def __init__(
        self,
        payoff_matrix: list,
        number_of_iterations: int | None = None
    ):
        self.payoff_matrix = payoff_matrix
        self.number_of_iterations = number_of_iterations

        self.my_history = []
        self.opponent_history = []

        self.my_last_move = False
        self.opponent_last_move = False

    def select_move(self) -> bool:
        round_counter = len(self.my_history)
        analyze_opponent = round_counter >= self.OBSERVATION_ROUNDS

        cc = self.payoff_matrix[False][False][0]
        cd = self.payoff_matrix[False][True][0]
        dc = self.payoff_matrix[True][False][0]
        dd = self.payoff_matrix[True][True][0]

        if not analyze_opponent:
            return self.opponent_last_move

        if self.is_tit_for_tat():
            cooperate_value = cc
            alternate_value = (cd + dc) / 2

            if cooperate_value >= alternate_value:
                return False
            else:
                return not self.my_last_move

        if self.is_always_cooperative():
            cooperate_value = cc
            defect_value = dc
            if defect_value > cooperate_value:
                return True
            return False

        if self.is_always_defecting():
            cooperate_value = cd
            defect_value = dd
            if cooperate_value > defect_value:
                return False
            return True

        return self.opponent_last_move

    def is_tit_for_tat(self) -> bool:
        for i in range(1, len(self.my_history)):
            if self.opponent_history[i] != self.my_history[i - 1]:
                return False
        return True

    def is_always_cooperative(self) -> bool:
        return not any(self.opponent_history)

    def is_always_defecting(self) -> bool:
        return all(self.opponent_history)
        
    def record_last_moves(
        self,
        my_last_move: bool,
        opponent_last_move: bool
    ) -> None:
        self.my_last_move = my_last_move
        self.opponent_last_move = opponent_last_move
        self.my_history.append(my_last_move)
        self.opponent_history.append(opponent_last_move)