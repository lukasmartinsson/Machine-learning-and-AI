import numpy as np
from gamestate import GameState
from node import MCTSNode
from search import MonteCarloTreeSearch
from move import Move


def main():
    print("You play as O, computer play as X")
    print("X goes first!")
    print("")

    # Initialize game
    initial_board = np.zeros(shape=(3, 3))
   #initial_board[1,1] = -1

    current_game_state = GameState(initial_board=initial_board, initial_player=GameState.playerX)
    current_node = MCTSNode(game_state=current_game_state)

    # Print initial game board
    current_node.game_state.print_board()
    print("\n")

    # Play game
    while not current_node.game_state.is_game_over():

        mcts = MonteCarloTreeSearch(node=current_node)
        best_move, new_node = mcts.get_best_move(10000)
        current_node = new_node
        current_node.game_state.print_board()
        print("\n")

        if not current_node.game_state.is_game_over():
            player_input = [int(i) for i in input("Select move by typing 'x y' coordinates: ").strip().split(" ")]
            player_move = Move(player=GameState.playerO, x=player_input[0], y=player_input[1])
            current_game_state = current_node.game_state.make_move(move=player_move)
            current_node = MCTSNode(game_state=current_game_state, parent=current_node, move=player_move)
            current_node.game_state.print_board()
            print("\n")

    game_result = current_node.game_state.get_game_result()
    if game_result == GameState.playerX:
        print("X wins!")
    elif game_result == GameState.playerO:
        print("O wins!")
    else:
        print("It is a tie!")


if __name__ == '__main__':
    main()
