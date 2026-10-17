class Player:
    """Analyzes the opponent's moves and chooses the next move"""

    MEMORY_SIZE = 5
    OBSERVATION_ROUNDS = 6
    SHORT_GAME_THRESHOLD = 10
    HIGH_ANALYSIS_THRESHOLD = 0.8

    def __init__(
        self,
        payoff_matrix: list,
        number_of_iterations: int | None = None
    ):
        self.payoff_matrix = payoff_matrix
        self.number_of_iterations = number_of_iterations

        self.my_moves = Memory(self.MEMORY_SIZE)
        self.opponent_moves = Memory(self.MEMORY_SIZE)

        self.my_last_move = False
        self.opponent_last_move = False

        self.round_counter = 0

    def select_move(self) -> bool:
        cc = self.payoff_matrix[False][False][0]
        cd = self.payoff_matrix[False][True][0]
        dc = self.payoff_matrix[True][False][0]
        dd = self.payoff_matrix[True][True][0]

        if self.number_of_iterations and self.number_of_iterations - 1 == self.round_counter:
            return True

        if self.round_counter < self.OBSERVATION_ROUNDS:
            return self.opponent_last_move

        opponent_analyzer = OpponentAnalyzer(
            my_moves=self.my_moves.get(),
            opponent_moves=self.opponent_moves.get()
        )

        cooperation_rate = opponent_analyzer.cooperation_rate()
        defection_rate = opponent_analyzer.defection_rate()
        defection_response_rate = opponent_analyzer.defection_response_rate()
        cooperation_response_rate = opponent_analyzer.cooperation_response_rate()

        if defection_rate >= self.HIGH_ANALYSIS_THRESHOLD:
            cooperate_value = cd
            defect_value = dd

            if cooperate_value > defect_value:
                return False
            return True

        if (
            cooperation_response_rate > self.HIGH_ANALYSIS_THRESHOLD and
            defection_response_rate > self.HIGH_ANALYSIS_THRESHOLD
        ):
            cooperate_value = cc
            alternate_value = (cd + dc) / 2
                    
            if cooperate_value >= alternate_value:
                return False
            return not self.my_last_move

        if cooperation_rate >= self.HIGH_ANALYSIS_THRESHOLD:
            cooperate_value = cc
            defect_value = dc
            if defect_value > cooperate_value:
                return True
            return False
        
        return self.opponent_last_move
    
    def record_last_moves(
        self,
        my_last_move: bool,
        opponent_last_move: bool
    ) -> None:
        self.my_last_move = my_last_move
        self.opponent_last_move = opponent_last_move
        self.my_moves.add(my_last_move)
        self.opponent_moves.add(opponent_last_move)
        self.round_counter += 1

class OpponentAnalyzer:
    """Analyzes the opponent's recent moves and estimates its behavior"""

    ANALYSE_WINDOW = 5

    def __init__(
        self,
        my_moves: list[bool],
        opponent_moves: list[bool]
    ):
        self.my_history = my_moves
        self.opponent_history = opponent_moves  

    def defection_rate(self) -> float:
        recent_moves = self.opponent_history[-self.ANALYSE_WINDOW:]

        return recent_moves.count(True) / len(recent_moves)

    def cooperation_rate(self) -> float:
        recent_moves = self.opponent_history[-self.ANALYSE_WINDOW:]

        return recent_moves.count(False) / len(recent_moves)

    def defection_response_rate(self) -> float:
        defections = 0
        reactions = 0

        for i in range(1, len(self.my_history)):
            if self.my_history[i - 1]:
                defections += 1
                if self.opponent_history[i]:
                    reactions += 1

        if defections == 0:
            return 0.0

        return reactions / defections
    
    def cooperation_response_rate(self) -> float:
        cooperations = 0
        reactions = 0

        for i in range(1, len(self.my_history)):
            if not self.my_history[i - 1]:
                cooperations += 1
                if not self.opponent_history[i]:
                    reactions += 1

        if cooperations == 0:
            return 0.0
            
        return reactions / cooperations

class Memory:
    """Stores the most recent moves using a circular buffer"""

    def __init__(self, size: int):
        self.size = size
        self.data = [None] * size
        self.index = 0
        self.full = False

    def add(self, value: bool) -> None:
        self.data[self.index] = value
        self.index = (self.index + 1) % self.size

        if self.index == 0:
            self.full = True

    def get(self) -> list[bool]:
        if not self.full:
            return self.data[:self.index]

        return self.data[self.index:] + self.data[:self.index]