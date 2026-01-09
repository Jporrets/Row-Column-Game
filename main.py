from models import Board, Player
import agent
from view import GameGUI
import tkinter as tk
from tkinter import ttk
from launcher import GameSetup

def start_game():
    root = tk.Tk()
    
    setup = GameSetup(root)
    settings = setup.result
    
    if not settings:
        return 

    mode = settings["mode"]
    agent_name = settings["agent"]
    size = settings.get("size", 4)

    # 1. Map strings to CLASSES (no parentheses here)
    agent_classes = {
        "Minimax": agent.MinimaxAgent,
        "Random": agent.RandomAgent,
        "Best Points Move": agent.BestPointsMoveAgent,
        "BPM Depth": agent.BpmDepthAgent
    }
    
    # Initialize variables to None
    agent1 = None
    agent2 = None

    # 2. Handle Logic based on Mode
    if mode == "PvP":
        p1 = Player('Player 1', False)
        p2 = Player('Player 2', False)
        
    elif mode == "PvE":
        p1 = Player('Human', False)
        p2 = Player(f'{agent_name} Agent', True)
        # Initialize the agent class with the player object
        AgentClass = agent_classes.get(agent_name)
        agent2 = AgentClass(p2) 
        
    elif mode == "EvE":
        p1 = Player('Random Agent', True)
        p2 = Player(f'{agent_name} Agent', True)
        # Player 1 gets Random Agent
        agent1 = agent.RandomAgent(p1)
        # Player 2 gets the selected Agent
        AgentClass = agent_classes.get(agent_name)
        agent2 = AgentClass(p2)

    # 3. Create Board and Launch GUI
    board = Board(size, p1, p2)
    root.deiconify()
    
    # Pass the agents to the GUI
    g = GameGUI(root, board, agent1=agent1, agent2=agent2)
    root.mainloop()

if __name__ == "__main__":
    start_game()
