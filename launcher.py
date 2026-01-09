import tkinter as tk
from tkinter import ttk

class GameSetup(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Game Settings")
        self.result = None
        self.geometry("300x250")
        
        # 1. Game Mode Selection
        tk.Label(self, text="Select Game Mode:").pack(pady=5)
        self.mode_var = tk.StringVar(value="PvP")
        ttk.Combobox(self, textvariable=self.mode_var, 
                     values=["PvP", "PvE", "EvE"]).pack()

        # 2. Agent Selection
        tk.Label(self, text="Select AI Agent:").pack(pady=5)
        self.agent_var = tk.StringVar(value="Minimax")
        ttk.Combobox(self, textvariable=self.agent_var, 
                     values=[
                            "Random",
                            "Minimax",
                            "Best Points Move",
                            "BPM Depth",
                        ]).pack()

        # 3. Board Size Selection
        tk.Label(self, text="Board Size (NxN):").pack(pady=5)
        self.size_var = tk.IntVar(value=4) # Default to 4x4
        tk.Spinbox(self, from_=3, to=10, textvariable=self.size_var, width=5).pack()
        
        # Start Button
        tk.Button(self, text="Start Game", command=self.on_submit).pack(pady=20)
        
        # Make this window modal (locks the main window until closed)
        self.transient(parent)
        self.grab_set()
        parent.wait_window(self)

    def on_submit(self):
        self.result = {
            "mode": self.mode_var.get(),
            "agent": self.agent_var.get(),
            "size": self.size_var.get()
        }
        self.destroy()