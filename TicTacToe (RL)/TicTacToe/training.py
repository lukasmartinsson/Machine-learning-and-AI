import numpy as np
import random

from tictactoe import Tictactoe
import game_over

def training_round(player1, player2):

    board = Tictactoe()
    
    # Get the board_state
    board_state = board.get_board_state()

    first = False
    game_status = False
    
    win1, win2 , draw = 0, 0, 0

    while True:

        # Update player1 q_table with the board_state and return the state
        state1 = player1.q_table_update(board_state)

        # Make a epislon move and return the move
        move1 = player1.move(board_state, state1)

        # Update the board_state
        board.update_board_state(move1, player1.player)

        # Get the board_state
        board_state = board.get_board_state()
       
        game_status, result = game_over(board_state)
        
        if first:
            player2.update_reward(state2, board_state, move2, game_status, -result)

        first == True

        if game_status:
            player1.update_reward(state1, board_state, move1, game_status, result)
            if result == 10:
                win1 = 1
                return win1, win2, draw
            if result == -10:
                win2 = 1
                return win1, win2, draw
            if result == 0:
                draw = 1
                return win1, win2, draw


        # Update player2 q_table with the board_state and return the state
        state2 = player2.q_table_update(board_state)
        
        # Make a epislon move and return the move
        move2 = player2.move(board_state, state2)

        # Update the board_state
        board.update_board_state(move2, player2.player)

        # Get the board_state
        board_state = board.get_board_state()

        game_status, result = game_over(board_state)

        player1.update_reward(state1, board_state, move1, game_status, result)

        if game_status:
            player2.update_reward(state2, board_state, move2, game_status, -result)
            if result == 10:
                win1 = 1
                return win1, win2, draw
            if result == -10:
                win2 = 1
                return win1, win2, draw
            if result == 0:
                draw = 1
                return win1, win2, draw