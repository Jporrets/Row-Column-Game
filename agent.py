import numpy as np
from models import Board, Player
import copy

class Agent:
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

    def select_move(self, board: Board, depth: int):
        best_score = float('-inf')
        best_move_found = None

        alpha = float('-inf')
        beta = float('inf')

        for move in board.available_moves_array():
            board.make_move(move[0], move[1]) #

            score = self.minimax(board, False, depth - 1, alpha, beta)
            print(f'Score for the move {move} is {score}')

            board.undo_last_move() #
            if score > best_score:
                best_score = score
                best_move_found = move

            alpha = max(alpha, score)

        return best_move_found

    def minimax(self, board: Board, isMax: bool, depth: int, alpha: float = float('-inf'), beta: float = float('inf')):

        if depth == 0 or not board.is_there_move_possible():
            # return self.static_evaluation(board, isMax)
            return self.static_evaluation(board, isMax)
        
        if isMax :
            maxEval = float('-inf')
            for move in board.available_moves_array():
                board.make_move(move[0], move[1]) #
                eval = self.minimax(board, False, depth - 1, alpha, beta)
                board.undo_last_move() #
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha: break
            return maxEval
        else :
            minEval = float('inf')
            for move in board.available_moves_array():
                
                board.make_move(move[0], move[1]) #
                eval = self.minimax(board, True, depth - 1, alpha, beta)
                board.undo_last_move() #
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha: break
            return minEval

    def static_evaluation(self, board: Board, isMax: bool):

        hpm_agent = BestPointsMoveAgent()
        high_move = hpm_agent.select_move(board)
        if high_move.size == 0: return 0

        score = board.get_board()[high_move[0], high_move[1]]
        # print(f'Evaluation for the position is: {score}')

        if isMax:
            return score
        else:
            return (-1 * score)
        
    def depth6Eval(self, board: Board, isMax: bool):
        depth = 6 # Tournaments show it to be optimal

        available_moves = board.available_moves_array()

        max_diff = float('-inf')

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

            max_diff = max(diff, max_diff)
        
        if isMax: 
            return max_diff
        else:
            return (-1*max_diff)



# Monte Carlo Based agent

def monte_carlo_eval(board: Board, n_sim:int):
    """
    The function provides evaluation of a position. It should be used after the inteded move to evaluate has been played.
    """

    total_score = 0
    #b = copy.deepcopy(board) ### NOT ANOTHER DEEPCOPY

    for tries in range(n_sim):
        total_score = total_score + random_game(copy.deepcopy(board)) 
    
    eval = total_score / n_sim
    #print(f'Evaluation of current position is:', eval)
    return eval
        

def random_game(board: Board):
    player1 = board.turn
    player2 = board.player2 if player1 != board.player2 else board.player1

    while True:

        if not board.is_there_move_possible():
            winner = board.is_winner(player1=player1, player2=player2)
            return winner
        
        # Logic to make moves
        try:
            
            move = weighted_choice(board)
            board.make_move(move[0], move[1])
        except:
            raise TabError('Couldnt make move!')

def mc_make_choice(board:Board):

    possible_moves = board.available_moves_array()
    eval_array = []

    for move in possible_moves :
        temp_board = copy.deepcopy(board)
        temp_board.make_move(move[0], move[1])
        eval = monte_carlo_eval(temp_board, 1000)
        eval_array.append(eval * - 1)

    max_index = np.argmin(eval_array)
    # print(possible_moves)
    # print(max_index)
    # print('array:', eval_array)
    # print(f'Best move looks to be: {possible_moves[max_index]}, with eval of: {min(eval_array) * -1}')
    return possible_moves[max_index]

def weighted_choice(board:Board):
    available_m = board.available_moves_array()
    a1 = BestPointsMoveAgent().select_move(board)
    a2 = BpmDepthAgent().select_move(board)

    lenght = len(available_m)
    normal_weight = (1 - 0.7) / lenght

    weights = []
    for move in available_m:

        if move == a1 and move == a2:
            weights.append(0.7)
        elif move == a1 and move != a2:
            weights.append(0.5)
        elif move == a2 and move != a1:
            weights.append(0.2)
        else:
            weights.append(normal_weight)
    
    weights = np.array(weights)

    move = tuple(available_m[np.random.choice(range(len(available_m)), p=weights/weights.sum())])
    return move
    