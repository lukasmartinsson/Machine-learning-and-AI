import numpy as np
from matplotlib import pyplot as plt
from tictactoe import Tictactoe
from training import training_round
from AI import AI

np.set_printoptions(suppress=True)

epsilon = 0.9
learning_rate = 0.1
board = Tictactoe()

player1 = AI(epsilon = epsilon, player = 1, learning_rate = learning_rate)
player2 = AI(epsilon = epsilon, player = -1, learning_rate = learning_rate)

win_1 = []
win_2 = []
draws = []

n_games = 500
for i in range(n_games):
    if i % 100 == 0:
        print(i)
    win1, win2, draw = training_round(player1, player2)
    win_1.append(win1)
    win_2.append(win2)
    draws.append(draw)

print(np.sum(win_1), np.sum(win_2), np.sum(draws))

win_rate_1 = np.mean(np.array(win_1).reshape(-1, int(n_games/5)), axis = 1)
win_rate_2 = np.mean(np.array(win_2).reshape(-1, int(n_games/5)), axis = 1)
win_rate_draw = np.mean(np.array(draws).reshape(-1, int(n_games/5)), axis = 1)

plt.plot(win_rate_1, label = 'First Player')
plt.plot(win_rate_2, label = 'Second Player')
plt.plot(win_rate_draw, label = 'Draw')
plt.legend()
plt.show()