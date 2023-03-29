import numpy as np
import random

class AI:
    def __init__(self, epsilon, player, learning_rate):
        self.q_table = [[],[]]
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.player = player

    def q_table_update(self, board_state):
        if len(self.q_table[0]) == 0:
            self.q_table[0].append(board_state)
            self.q_table[1].append(self.possible_moves(board_state))
            return 0

        for i in range(len(self.q_table[0])):
            if np.array_equal(self.q_table[0][i], board_state):
                return i
            else:
                self.q_table[0].append(board_state)
                self.q_table[1].append(self.possible_moves(board_state))
                return i+1

    def possible_moves(self, board_state):
        moves = []
        for i in range(3):
            for j in range(3):
                if board_state[i][j] == 0:
                    moves.append(0)
                else:
                    moves.append(-10)#'NaN')
        possible_moves = np.array([[moves[0],moves[1],moves[2]],[moves[3],moves[4],moves[5]],[moves[6],moves[7],moves[8]]], dtype = float)
        return possible_moves

    def possible_random_moves(self, board_state):
        moves = []
        for i in range(3):
            for j in range(3):
                if board_state[i][j] != -10:
                    moves.append(3*i + j)
        return moves

    def move(self, board_state, state):
        if random.random() < self.epsilon: 
            return np.argmax(self.q_table[1][state])
        else:
            return random.choice(self.possible_random_moves(self.q_table[1][state]))

    def update_reward(self, old_state, new_board_state, move, game_over, result):

        if game_over:
            delta = self.q_table[1][old_state].flatten()[move] + self.learning_rate * (np.max(self.q_table[1][old_state].flatten()[move]) + result - np.max(self.q_table[1][old_state].flatten()[move]))

        for i in range(len(self.q_table[0])):
            if np.array_equal(self.q_table[0][i], new_board_state):
                delta = self.q_table[1][old_state].flatten()[move] + self.learning_rate * (np.max(self.q_table[1][old_state].flatten()[move]) + np.max(self.q_table[1][i].flatten()[move]) - np.max(self.q_table[1][old_state].flatten()[move]))
            else:
                delta = self.q_table[1][old_state].flatten()[move] + self.learning_rate * (np.max(self.q_table[1][old_state].flatten()[move]) + 0 - np.max(self.q_table[1][old_state].flatten()[move]))
              

        temp = self.q_table[1][old_state].flatten()
        temp[move] = delta
        self.q_table[1][old_state] = temp.reshape((3,3))