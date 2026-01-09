import numpy as np
import tkinter as tk
from tkinter import messagebox
from models import Board, Player
import agent
from copy import deepcopy
import time

class GameGUI:
    def __init__(self, master: tk.Tk, board: 'Board', agent1: agent.Agent = None, agent2: agent.Agent = None):
        # Initialize game state, players, and agents
        self.board = board
        self.agent1 = agent1
        self.agent2 = agent2
        self.master = master
        self.master.title("Game")

        # UI Components: Labels for player info, game info, and score
        self.players_info = tk.Label(self.master, font=("Arial", 14, "bold"))
        self.players_info.pack(pady=5)

        self.game_info = tk.Label(self.master, font=("Arial", 14))
        self.game_info.pack(pady=5)

        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack()

        self.buttons = [[None for _ in range(board.cols)]
                        for _ in range(board.rows)]

        self.score_info = tk.Label(self.master, font=("Arial", 14))
        self.score_info.pack(pady=5)

        # Initialize the game UI and start the first move
        self.draw_board()
        self.update_info()
        self.highlight_buttons()
        self.get_agent_move()

    ######
    # Helper Methods
    ######

    def draw_board(self):
        """Draw the game board with buttons."""
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                value = self.board.table[r][c]
                btn = tk.Button(
                    self.board_frame,
                    text=str(value),
                    width=4,
                    height=2,
                    command=lambda r=r, c=c: self.on_click(r, c)
                )
                btn.grid(row=r, column=c, padx=2, pady=2)
                self.buttons[r][c] = btn

    def highlight_buttons(self):
        """Highlight legal moves and previous move."""
        # Reset all button colors
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                btn = self.buttons[r][c]
                if btn["state"] != "disabled":
                    btn.config(bg="SystemButtonFace")
        
        available_moves = self.board.available_moves_array()
        last_move = self.board.last_move

        # Highlight legal moves
        for (r, c) in available_moves:
            btn = self.buttons[r][c]
            if btn["state"] != "disabled":
                btn.config(bg="lightblue")

        # Highlight last move
        if last_move:
            btn = self.buttons[last_move[0]][last_move[1]]
            btn.config(bg="palegreen")

    def update_info(self):
        """Update player names, turn, and score info."""
        self.players_info.config(
            text=f"{self.board.player1.name} vs {self.board.player2.name}"
        )
        self.game_info.config(
            text=f'Turn of: {self.board.turn.name}'
        )
        self.score_info.config(
            text=f'****SCORES****\n{self.board.player1.name} : {self.board.player1.get_score()} || {self.board.player2.name} : {self.board.player2.get_score()}'
        )

    ######
    # Event Handlers
    ######

    def on_click(self, r, c):
        """Handle click event on board."""
        # Validate move
        if not self.board.is_move_valid(r, c):
            return

        # Make the move
        self.board.make_move(r, c)
        self.buttons[r][c].config(state="disabled")

        # Update UI
        self.update_info()
        self.highlight_buttons()

        # Check if the move ended the game
        self.winner_handler()

        # Let agent make a move if it's the agent's turn
        self.get_agent_move()

    def get_agent_move(self):
        """Get the agent's move if it's the agent's turn."""
        # Small delay for better UX
        time.sleep(0.5)

        if not self.board.is_there_move_possible():
            print('No moves available, skipping agent turn...')
            return

        turn = self.board.turn

        if not turn.is_computer:
            print('Player not an agent, skipping...')
            return
        
        print('Agent turn')
        if self.agent1 and turn == self.agent1.player:
            agent_to_use = self.agent1
        elif self.agent2 and turn == self.agent2.player:
            agent_to_use = self.agent2
        else:
            print('No agent assigned for this player, skipping...')
            return

        move = agent_to_use.select_move(deepcopy(self.board))
        print(f'Agent selected move: {move}')

        self.board.make_move(move[0], move[1])
        self.buttons[move[0]][move[1]].config(state="disabled")

        # Update UI
        self.update_info()
        self.highlight_buttons()

        # Check if the agent's move ended the game
        self.winner_handler()

    ######
    # Game Logic Handlers
    ######

    def winner_handler(self):
        """Check for a winner and display an alert if there's one."""
        if self.board.is_there_move_possible():
            return
        
        winner = self.board.is_winner(self.board.player1, self.board.player2)

        if winner == 1:
            messagebox.showinfo("Game Over", f"{self.board.player1.name} wins!")
        elif winner == -1:
            messagebox.showinfo("Game Over", f"{self.board.player2.name} wins!")
        elif winner == 0:
            messagebox.showinfo("Game Over", "It's a draw!")
        
        self.master.quit()  # Close the game window after showing the result

    ######
    # Game Loop
    ######

    def run(self):
        """Start the tkinter main loop."""
        self.master.mainloop()