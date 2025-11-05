import numpy as np
from models import Board, Player
import copy
import tabulate as tb

def monte_carlo_eval(board: Board, n_sim:int):
    """
    The function provides evaluation of a position. It should be used after the inteded move to evaluate has been played.
    """

    total_score = 0

    for tries in range(n_sim):
        total_score = total_score + random_game(copy.deepcopy(board)) ### NOT ANOTHER DEEPCOPY
    
    eval = total_score / n_sim
    print(f'Evaluation of current position is:', eval)
        

def random_game(board: Board):
    player1 = board.turn
    player2 = board.player2 if player1 != board.player2 else board.player1

    while True:

        if not board.is_there_move_possible():
            winner = board.is_winner(player1=player1, player2=player2)
            return winner
        
        # Logic to make moves
        try:
            move_choices = board.available_moves_array()
            rng = np.random.default_rng()
            move = tuple(move_choices[rng.integers(len(move_choices))])
            board.make_move(move[0], move[1])
        except:
            raise TabError('Couldnt make move!')