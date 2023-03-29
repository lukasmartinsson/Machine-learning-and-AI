import numpy as np

class MCTSNode:
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state
        self.parent = parent
        self.children = []

        self._n_visits = 0
        self._score = 0
        self._move = move

        self._untried_moves = None

    @property
    def q(self):
        return self._score

    @property
    def n(self):
        return self._n_visits

    @property
    def corresponding_move(self):
        return self._move

    @property
    def untried_moves(self):
        if self._untried_moves is None:
            self._untried_moves = self.game_state.legal_moves()
        return self._untried_moves

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def is_terminal_node(self):
        return self.game_state.is_game_over()

    def add_child_node(self, child_node):
        self.children.append(child_node)

    def get_best_child(self, trade_off_param=2.0):
        # Upper bound confidence trees
        child_scores = []
        for child in self.children:
            score = (child.q / child.n) + trade_off_param * np.sqrt((2 * np.log(self.n) / child.n))
            child_scores.append(score)
        return self.children[np.argmax(child_scores)]

    def expand(self):
        untried_move = self.untried_moves.pop()
        child_game_state = self.game_state.make_move(untried_move)
        child_node = MCTSNode(game_state=child_game_state, parent=self, move=untried_move)
        self.add_child_node(child_node)
        return child_node

    def rollout(self):
        simulation_state = self.game_state #copy.deepcopy(self.game_state)
        # Simulate game until terminal state
        while not simulation_state.is_game_over():
            legal_moves = simulation_state.legal_moves()
            move = self.rollout_policy_choose_move(legal_moves)
            simulation_state = simulation_state.make_move(move)
        # Return result of match
        return simulation_state.get_game_result()

    def rollout_policy_choose_move(self, possible_moves):
        # Random uniform policy
        return possible_moves[np.random.randint(len(possible_moves))]

    def backprop(self, game_result):
        self._n_visits += 1
        self._score += game_result
        if self.parent:
            self.parent.backprop(game_result)
