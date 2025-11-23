import tabulate as tb
import agent
from models import Board, Player
from copy import deepcopy
import time

p1 = Player('Minimax', True)
p2 = Player('HPM Agent', True)
bb = Board(5, p1, p2, 8)
ai = agent.MinimaxAgent()

test_ai = agent.MinimaxTEST()

# print(tb.tabulate(bb.get_board(), tablefmt='fancy_grid'))


# # EVAL TEST
# bb.make_move(2,2)
# print(tb.tabulate(bb.get_board(), tablefmt='fancy_grid'))

# evaluation = print(ai.handcrafted_evaluation(bb, False))
# move = ai.select_move(bb, 10)
# bb.make_move(move[0], move[1])
# print(tb.tabulate(bb.get_board(), tablefmt='fancy_grid'))
# evaluation = print(ai.handcrafted_evaluation(bb, False))


# while bb.is_there_move_possible():

#     print(tb.tabulate(bb.get_board(), tablefmt='fancy_grid'))

#     if bb.turn == p1:
#         move = test_ai.select_move(deepcopy(bb), 10)
#         bb.make_move(move[0], move[1])
#     elif bb.turn  == p2:
#         # row = int(input('insert row: '))
#         # col = int(input('interst col: '))
#         # bb.make_move(row, col)
#         move = ai.select_move(deepcopy(bb), 10)
#         bb.make_move(move[0], move[1])

# # Winner logic
# if bb.is_winner(p1, p2) == 1:
#     print(f'The winner is {p1.name}')
# elif bb.is_winner(p1, p2) == -1:
#     print(f'The winner is {p2.name}')
# else: print('Draw')

# print(f'\n\n****** SCORES ARE ******')
# print(f'{p1.name} = {p1.score} ||||| {p2.name} = {p2.score} ')

# Time test
def test_agent_performance(board: Board, agent: agent.Agent, depth: int):
    """
    Tests the performance of an agent's algorithm for the given board state and depth.
    """
    print(f"Testing Agent at depth {depth}...")

    # Start measuring time for select_move (which calls minimax)
    start_time = time.time()
    move = agent.select_move(deepcopy(board), depth)
    end_time = time.time()
    select_move_time = end_time - start_time

    print(f"Time taken for select_move at depth {depth}: {select_move_time:.4f} seconds")


    # Optionally print the best move for validation
    print(f"Best move at depth {depth}: {move}")
    print("-" * 50)

# print('Performance Test for Minimax')
# test_agent_performance(deepcopy(bb), ai, 10)
print('\n Performance Test for TESTMINI')
test_agent_performance(deepcopy(bb), test_ai, 10)