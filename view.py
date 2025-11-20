import numpy as np
import tkinter as tk
from models import Board, Player
import agent

class GameGUI:
    def __init__(self, board: 'Board', agent1: agent.Agent = None, agent2: agent.Agent = None):
        self.board = board
        self.agent1 = agent1
        self.agent2 = agent2
        self.root = tk.Tk()
        self.root.title("Game")

        # Player names
        self.players_info = tk.Label(self.root, font=("Arial", 14, "bold"))
        self.players_info.pack(pady=5)

        # Board turn
        self.game_info = tk.Label(self.root, font=("Arial", 14))
        self.game_info.pack(pady=5)

        # Container for the board buttons
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        # Buttons stored so you can update them if needed
        self.buttons = [[None for _ in range(board.cols)]
                        for _ in range(board.rows)]

        # Scores frame
        self.score_info = tk.Label(self.root, font=("Arial", 14))
        self.score_info.pack(pady=5)
        
        self.draw_board()
        self.update_info()
        self.highlight_buttons()
        self.get_agent_move()

    
    def draw_board(self):
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
        """
        Ask the board which moves are legal (list of (r,c)),
        then highlight them in light blue.
        """
        # Reset all button colors
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                btn = self.buttons[r][c]
                if btn["state"] != "disabled":
                    btn.config(bg="SystemButtonFace")
        
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                btn = self.buttons[r][c]
                if btn["state"] == "disabled":
                    btn.config(bg="lightgrey")

        

        available_moves = self.board.available_moves_array()
        last_move = self.board.last_move

        # Highlight them
        for (r, c) in available_moves:
            btn = self.buttons[r][c]
            if btn["state"] != "disabled":
                btn.config(bg="lightblue")
        
        if last_move:
            btn = self.buttons[last_move[0]][last_move[1]]
            btn.config(bg="palegreen")

    def update_info(self):
        self.players_info.config(
            text=f"{self.board.player1.name} vs {self.board.player2.name}"
        )
        self.game_info.config(
            text=f'Turn of: {self.board.turn.name}'
        )
        self.score_info.config(
            text=f'****SCORES****\n{self.board.player1.name} : {self.board.player1.get_score()} || {self.board.player2.name} : {self.board.player2.get_score()}'
        )

    def on_click(self, r, c):
        # Validation
        if not self.board.is_move_valid(r,c):
            return

        self.board.make_move(r, c)

        # UI update: disable clicked button
        self.buttons[r][c].config(state="disabled")

        self.update_info()
        self.highlight_buttons()
        self.get_agent_move()

    def get_agent_move(self):
        turn = self.board.turn

        if not turn.is_computer:
            print('Player not an agent, skipping...')
            return
        else: 
            if self.agent1 and turn == self.agent1.player:
                agent_to_use = self.agent1
            elif self.agent2 and turn == self.agent2.player:
                agent_to_use = self.agent2
            else:
                print('No agent assigned for this player, skipping...')
                return

            move = agent_to_use.select_move(self.board)

            if move[0] and move[1] is not None:
                self.board.make_move(move[0], move[1])

                # UI update: disable clicked button
                self.buttons[move[0]][move[1]].config(state="disabled")

                self.update_info()
                self.highlight_buttons()

    def run(self):
        self.root.mainloop()


#
p1 = Player('Human', False)
p2 = Player('Minimax Agent', True)
bb = Board(3, p1, p2, 8)
agent2 = agent.BestPointsMoveAgent(p2)

g = GameGUI(bb, agent2=agent2)
g.run()