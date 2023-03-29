from node import MCTSNode


class MonteCarloTreeSearch:

    def __init__(self, node: MCTSNode):
        self.root = node

    def get_best_move(self, iterations=1):
        # MCTS
        for i in range(0, iterations):
            selected_child_node = self.traverse()
            game_result = selected_child_node.rollout()
            selected_child_node.backprop(game_result)
        # Given the best child (exploitation only), get the corresponding move and return it
        best_child = self.root.get_best_child(trade_off_param=0)
        best_move = best_child.corresponding_move
        return best_move, best_child

    def traverse(self):
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                # Expand to new child node and return it
                return current_node.expand()
            else:
                current_node = current_node.get_best_child()
        return current_node
