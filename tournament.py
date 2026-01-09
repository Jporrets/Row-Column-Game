import tabulate as tb
from models import Player, Board
import agent
import matplotlib.pyplot as plt

####################################

# The file contains functions to run tournaments between different agents on the same board configurations.
# Its purpose is to evaluate and compare the performance of various AI agents in a competitive setting.
# Just run the file to see the tournament results.
# If you want to customize the agents or the number of simulations, modify the following parameters.

n_sim = 20 ## Number of games to be played in the tournament
first_agent = agent.BpmDepthAgent()
second_agent = agent.MinimaxAgent()
size = 4 ## Board size


####################################

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
            move = first_agent.select_move(board)
            board.make_move(move[0], move[1])
            moves_played['First Agent'] = moves_played['First Agent'] + 1
        elif board.turn == second_agent_player :
            move = second_agent.select_move(board)
            board.make_move(move[0], move[1])
            moves_played['Second Agent'] = moves_played['Second Agent'] + 1
    
    return board.is_winner(first_agent_player, second_agent_player)

def torunament(n_sim: int, fa: agent.Agent, sa: agent.Agent, b_size:int):
    '''
    Runs a tournament between two agents on random boards of given size. Returns a dictionary with the number of wins for each agent and draws.
    '''
    print(f'\n\nStarting tournament between {fa.name} and {sa.name} on {n_sim} games...')
    print(f'\nDepending on the board size and agent complexity, this may take a while...\n')

    wins_dict = {fa.name : 0, sa.name : 0, 'draw' : 0}

    for _ in range(n_sim) :
        res = a_vs_a_same_board(fa, sa, b_size)

        if res == 1 : wins_dict[fa.name] = wins_dict[fa.name] + 1
        elif res == -1 : wins_dict[sa.name] = wins_dict[sa.name] + 1
        elif res == 0 : wins_dict['draw'] = wins_dict['draw'] + 1

    return wins_dict

def show_tournament_results(results_dict):
    """
    Takes a dictionary like {'first agent': 20, 'second agent': 0, 'draw': 0}
    and displays a bar chart.
    """
    labels = list(results_dict.keys())
    counts = list(results_dict.values())
    total_games = sum(counts)
    
    # Calculate percentages for the text labels
    percentages = [(count / total_games * 100) if total_games > 0 else 0 for count in counts]
    
    # Create the figure
    plt.figure(figsize=(10, 6))
    
    # Colors: Blue for Agent 1, Red for Agent 2, Grey for Draw
    colors = ['#3498db', '#e74c3c', '#95a5a6']
    
    # Create bars
    bars = plt.bar(labels, counts, color=colors, edgecolor='black', alpha=0.8)
    
    # Add titles and styling
    plt.title(f'Tournament Results\nTotal Games: {total_games}', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Wins', fontsize=12)
    
    # Add labels on top of bars
    for bar, pct in zip(bars, percentages):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)} ({pct:.1f}%)',
                ha='center', va='bottom', fontweight='bold', fontsize=11)

    plt.tight_layout()
    plt.show()

show_tournament_results(torunament(n_sim, first_agent, second_agent, size))
