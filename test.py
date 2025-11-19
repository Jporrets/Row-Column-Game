import tabulate as tb
import agent
from models import Board, Player

p1 = Player('Minimax', True)
p2 = Player('HPM Agent', True)
bb = Board(9, p1, p2, 8)
ai = agent.MinimaxAgent()

test_ai = agent.BpmDepthAgent()

# print(tb.tabulate(bb.get_board(), tablefmt='fancy_grid'))


# EVAL TEST
print(tb.tabulate(bb.get_board(), tablefmt='fancy_grid'))
evaluation = print(ai.depth6Eval(bb, True))


while bb.is_there_move_possible():

    print(tb.tabulate(bb.get_board(), tablefmt='fancy_grid'))

    if bb.turn == p1:
        move = test_ai.select_move(bb)
        bb.make_move(move[0], move[1])
    elif bb.turn  == p2:
        # row = int(input('insert row: '))
        # col = int(input('interst col: '))
        # bb.make_move(row, col)
        move = ai.select_move(bb, 8)
        bb.make_move(move[0], move[1])

# Winner logic
if bb.is_winner(p1, p2) == 1:
    print(f'The winner is {p1.name}')
elif bb.is_winner(p1, p2) == -1:
    print(f'The winner is {p2.name}')
else: print('Draw')

print(f'\n\n****** SCORES ARE ******')
print(f'{p1.name} = {p1.score} ||||| {p2.name} = {p2.score} ')