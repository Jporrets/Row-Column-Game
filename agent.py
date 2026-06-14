import numpy as np
from models import Board, Player
import copy
import mcts_implementation
from numba import njit

class Agent:
    def __init__(self, player: Player = None, name: str = None):
        self.player = player # Keep track of which player the agent is assigned to. Used for view handling.
        self.name = name or self.__class__.__name__
        
    def select_move(self, board: Board) :
        """Return a move given the current board state."""
        raise TypeError('Parent class agent has no method for selecting a move. Use subclasses')

class RandomAgent(Agent):
    def select_move(self, board: Board):
        moves = board.available_moves_array()
        rng = np.random.default_rng()
        return tuple(moves[rng.integers(len(moves))])

class BestPointsMoveAgent(Agent):

    def select_move(self, board: Board):
        moves = board.available_moves_array()
        max_points = float('-inf')
        max_index = None


        for index, move in enumerate(moves):
            points = board.get_board()[move[0], move[1]]
            if points > max_points: 
                max_points = points
                max_index = index
        return moves[max_index]

class BpmDepthAgent(Agent):

    def select_move(self, board: Board):
        depth = 6 # Tournaments show it to be optimal

        available_moves = board.available_moves_array()

        max_diff = -100000
        max_diff_index = None

        hpm_agent = BestPointsMoveAgent()

        for index, move in enumerate(available_moves) :
            working_board = copy.deepcopy(board)
            player1 = working_board.turn
            player2 = working_board.player2 if player1 != working_board.player2 else working_board.player1

            working_board.make_move(move[0], move[1])


            for _ in range(depth) :
                if not working_board.is_there_move_possible(): break

                simulated_move = hpm_agent.select_move(working_board)
                working_board.make_move(simulated_move[0], simulated_move[1])
            
            p1_score = player1.get_score() 
            p2_score = player2.get_score()
            diff = p1_score - p2_score

            if diff > max_diff :
                max_diff_index = index
                max_diff = diff
        
        return available_moves[max_diff_index]

class MinimaxAgent(Agent):

    def select_move(self, board: Board, depth: int = 12):
        best_score = float('-inf')
        best_move_found = None

        alpha = float('-inf')
        beta = float('inf')

        isMax = True if board.player1 == self.player else False

        for move in board.available_moves_array():
            board.make_move(move[0], move[1]) #

            score = self.minimax(board, isMax, depth - 1, alpha, beta) #

            board.undo_last_move() #
            if score > best_score:
                best_score = score
                best_move_found = move

            alpha = max(alpha, best_score)

        return best_move_found

    def minimax(self, board: Board, isMax: bool, depth: int, alpha: float = float('-inf'), beta: float = float('inf')):

        # Transposition table lookup
        h = board.hash_board_state()
        entry = board.transposition_table.get(h)

        if entry is not None and entry['depth'] >= depth:
            if entry['flag'] == 'EXACT':
                return entry['value']
            elif entry['flag'] == 'LOWERBOUND':
                alpha = max(alpha, entry['value'])
            elif entry['flag'] == 'UPPERBOUND':
                beta = min(beta, entry['value'])
            
            if alpha >= beta:
                return entry['value']
            
        
        # Terminal node or depth limit reached
        if depth == 0 or not board.is_there_move_possible():
            val = self.quick_evaluation(board, isMax)
            board.transposition_table[h] = {'value': val, 'depth': depth, 'flag': 'EXACT'}
            return val
        
        # Move generation and ordering
        moves = board.available_moves_array()
        values = board.table[moves[:, 0], moves[:, 1]]
        moves = moves[np.argsort(-values)] # Sort moves by their point value in descending order for better pruning

        original_alpha = alpha
        original_beta = beta

        if isMax :
            value = float('-inf')
            for move in moves:
                board.make_move(move[0], move[1])
                eval = self.minimax(board, False, depth - 1, alpha, beta)
                board.undo_last_move()

                value = max(value, eval)
                alpha = max(alpha, value)
                if beta <= alpha: break
            
        else :
            value = float('inf')
            for move in moves:
                board.make_move(move[0], move[1])
                eval = self.minimax(board, True, depth - 1, alpha, beta)
                board.undo_last_move()

                value = min(value, eval)
                beta = min(beta, value)
                if beta <= alpha: break
            
        
        if value <= original_alpha:
            flag = 'UPPERBOUND'
        elif value >= original_beta:
            flag = 'LOWERBOUND'
        else:
            flag = 'EXACT'

        board.transposition_table[h] = {
            'value': value,
            'depth': depth,
            'flag': flag
        }
        return value

    def quick_evaluation(self, board: Board, isMax: bool):
        """
        A quick evaluation function that considers only the score difference.
        The function evaluates the board for the current player.
        """

        # Players
        player1 = board.turn
        player2 = board.player2 if player1 != board.player2 else board.player1

        # 1. Score difference
        score_diff = player1.get_score() - player2.get_score()

        # Weights
        w_score = 1.0

        final_eval = (w_score * score_diff)

        return final_eval if isMax else -final_eval

# MCTS proper

class MCTSAgent(Agent):
    def select_move(self, board: Board):
        root_state = board.get_board()

        if board.last_move is None:
            last_row, last_col = -1, -1
        else:
            last_row, last_col = board.last_move

        best_r, best_c = mcts_implementation.mcts_search(
            root_state,
            iterations     = 1000000,
            root_player    = 100,
            max_moves      = board.rows * board.cols,
            root_last_row  = last_row,
            root_last_col  = last_col,
        )

        if best_r == -1:
            raise RuntimeError('MCTS failed to find a move!')
        
        return (best_r, best_c)
