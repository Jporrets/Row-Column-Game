import tabulate as tb
from models import Player, Board
import agent

def a_vs_a_same_board(first_agent: agent.Agent, second_agent: agent.Agent, board_size: int, ):
    """
    Plays a game between two agents. First agent always moves first. Returns winner of the game. Games are played on random boards
    """
    first_agent_player = Player('first agent', True)
    second_agent_player = Player('second agent', True)
    board = Board(board_size, first_agent_player, second_agent_player)

    moves_played = {'First Agent': 0, 'Second Agent': 0}

    while board.is_there_move_possible():
        if board.turn == first_agent_player :
            print('First agent turn')
            move = first_agent.select_move(board)
            board.make_move(move[0], move[1])
            moves_played['First Agent'] = moves_played['First Agent'] + 1
        elif board.turn == second_agent_player :
            print('Second agent turn')
            move = second_agent.select_move(board)
            board.make_move(move[0], move[1])
            moves_played['Second Agent'] = moves_played['Second Agent'] + 1
    
    print('Moves played',moves_played)
    return board.is_winner(first_agent_player, second_agent_player)

def torunament(n_sim: int, fa: agent.Agent, sa: agent.Agent, b_size:int):
    wins_dict = {'first agent' : 0, 'second agent' : 0, 'draw' : 0}

    for _ in range(n_sim) :
        res = a_vs_a_same_board(fa, sa, b_size)

        if res == 1 : wins_dict['first agent'] = wins_dict['first agent'] + 1
        elif res == -1 : wins_dict['second agent'] = wins_dict['second agent'] + 1
        elif res == 0 : wins_dict['draw'] = wins_dict['draw'] + 1

    return wins_dict


table = []
n_sim = 20
first_agent = agent.BpmDepthAgent()
second_agent = agent.MinimaxAgent()
size = 5


wins_dict = torunament(n_sim, first_agent, second_agent, size)
for key, val in wins_dict.items():
    percent = (val / n_sim) * 100
    table.append([key, val, f"{percent:.2f}%"])

# Print results
print(tb.tabulate(table, headers=["Result", "Count", "Percentage"], tablefmt="fancy_grid"))