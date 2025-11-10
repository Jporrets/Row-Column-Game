import tabulate as tb
import agent
from models import Board, Player

p1 = Player('p1', True)
p2 = Player('p2', False)
bb = Board(5, p1, p2, 8)
ai = agent.BestPointsMoveAgent()

# print(tb.tabulate(bb.get_board(), tablefmt='fancy_grid'))

while bb.is_there_move_possible():

    print(tb.tabulate(bb.get_board(), tablefmt='fancy_grid'))

    if bb.turn == p1:
        move = ai.select_move(bb)
        bb.make_move(move[0], move[1])
    elif bb.turn  == p2:
        row = int(input('insert row: '))
        col = int(input('interst col: '))
        bb.make_move(row, col)

print(bb.is_winner(p1, p2))