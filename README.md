# 🧩 Row-Column Game

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

A strategic logic puzzle game where the objective is to reach the highest possible score by toggling entire rows or columns.

---

## 🎮 Rules
**Row-Column Game** is a simple game. You choose a cell and the opponent can choose a cell from the same row or column. When no more moves are possible, the player with the highest score is the winner.

## 📊 Tournament & Benchmarking
Want to see which AI is superior? Run the tournament script to simulate matches between different agents.

```bash
python tournament.py
```

## 🧠 AI Agents
This project implements several AI strategies to challenge the player:

* **Random Agent:** Selects a valid move entirely at random.
* **Best Points Move (BPM):** An agent that always picks the first iteration of the highest possible value move.
* **BPM Depth:** A smarter version of the BPM agent that looks one step ahead to avoid "traps" (high-value moves that open up even better moves for the opponent). Tournaments show that a depth of 6 is optimal. Highet depths usually lead to allucinations that diminish effectivness.
* **Minimax Agent:** Uses a recursive search tree to simulate future possibilities, playing optimally to maximize its score while minimizing yours. Uses alpha beta pruning.

## 🚀 Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/Jporrets/Row-Column-Game.git](https://github.com/Jporrets/Row-Column-Game.git)
    cd Row-Column-Game
    ```

2.  **Run the Game:**
    Ensure you have Python 3.12+ installed:
    ```bash
    python main.py
    ```

## Tournament
The tournament file is used to test algorithms against one another. 
Outuput of two tournaments on boards with size 5:
<img width="1000" height="600" alt="Figure_1" src="https://github.com/user-attachments/assets/e79e2d10-eaa1-4fdd-aa54-d4075fd38e10" />
<img width="1000" height="600" alt="Figure_2" src="https://github.com/user-attachments/assets/8c82f692-8907-4844-b4f5-c4451ddf5301" />
The small board size makes it so that there is a remarkable advantage for the first mover.
