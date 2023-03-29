import numpy as np

class Tictactoe:
    def __init__(self):
        self.board_state = np.array([[1,-1,1], [0,0,0],[1,-1,1]]) # np.zeros((3,3), dtype=int)

    def get_board_state(self):
        return self.board_state
    
    def update_board_state(self, move, player):
        temp = self.board_state.flatten()
        temp[move] = player
        self.board_state = temp.reshape((3,3))