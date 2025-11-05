from models import Board, Player
import environment
import tabulate as tb



size = environment.read_size('D:\Raccolta\Progetti\Advanced Py\Row Column Game\mod.txt')
board = Board(size= size, seed=8)


print('\n\nInit Board based on txt env. Size:', size)
print('Row Column Game mode:', environment.read_mod('D:\Raccolta\Progetti\Advanced Py\Row Column Game\mod.txt'), '\n\n')
print(tb.tabulate(board.get_board(), tablefmt='fancy_grid'))

human_p1 = str(input('Inserisci il tuo nickname:'))
player = Player(name=human_p1, is_computer=False)
bot = Player(name='CPU1', is_computer=True)

while board.is_there_move_possible():

    pass