import numpy as np

def game_over(game_board):
    if np.max(np.sum(game_board, axis=1)) == 3:
        return True, 10

    if np.max(np.sum(game_board, axis=0)) == 3:
        return True, 10
    
    if np.trace(game_board) == 3:
        return True, 10

    if np.min(np.sum(game_board, axis=1)) == -3:
        return True, -10

    if np.min(np.sum(game_board, axis=0)) == -3:
        return True, -10

    if np.trace(game_board) == -3:
        return True, -10
    
    if np.count_nonzero(game_board) == 9:
        return True, 0

    return False , 0