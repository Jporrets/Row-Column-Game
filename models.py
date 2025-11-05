import numpy as np
import tabulate as tb

class Board:
    def __init__(self, size: int, seed: int=None):
        self.rows = size
        self.cols = size
        self.seed = seed

        # Automatically create a random board upon init
        if self.seed is not None:
            np.random.seed(seed)
        self.table = np.random.randint(1, 10, size=(self.rows, self.cols))

        self.last_move = None

    def get_board(self) -> np.ndarray:
        """
        Returns the current state of the board

        Returns:
            np.ndarray: Current board state
        """
        return self.table
    
    def is_move_valid(self, row: int, col: int) -> bool:
        """
        Checks if the move is valid based on the last move.

        Parameters:
            row (int): Row index of the move
            col (int): Column index of the move

        Returns:
            bool: True if the move is valid, False otherwise

        Raises:
            IndexError: If the move is out of bounds

        Notes:
            A move is valid if:
            - The cell is not already taken (not 0)
            - If it's the first move, any cell is acceptable
            - For subsequent moves, the move must be in the same row or column as the last move
        """
        try:
            cell_value = self.table[row, col]
        except IndexError:
            raise IndexError('Move out of board bounds.')
        
        if cell_value == 0: return False

        if self.last_move is None: 
            return True
        
        if row == self.last_move[0] or col == self.last_move[1]:
            return True

    def make_move(self, row: int, col: int, player: 'Player') -> None:
        """
        Records a player's move. If the move is valid, it adds the points from the cell to the player's score. It sets the cell to 0.

        Parameters:
            row (int): Row index of the move
            col (int): Column index of the move
            player (Player): The player making the move

        Returns: 
            None

        Raises:
            ValueError: If the move is invalid

        """
        if self.is_move_valid(row, col):
            points = self.table[row, col]
            self.table[row, col] = 0
            player.add_to_score(points)
            self.last_move = (row, col)
        else :
            raise ValueError('Invalid move! Cell already taken.')
        
    def is_there_move_possible(self) -> bool:
        """
        Checks if there are any possible moves left based on the last move made.

        Parameters:
            None

        Returns: 
            bool: True if moves are possible, False otherwise 
        """
        if self.last_move is None: return True

        row_index, col_index = self.last_move
        if np.any(self.table[row_index, :] != 0) or np.any(self.table[:, col_index] != 0):
            return True
        
        return False

    
class Player:
    def __init__(self, name: str, is_computer: bool):
        self.name = name
        self.score = 0
        self.is_computer = is_computer

    def add_to_score(self, points: int):
        """
        Adds points to the player's score

        Parameters:
            points (int): Points to add

        Returns: 
            None

        """
        self.score += points

    def get_score(self) -> int:
        """
        Returns the player's current score

        Returns:
            int: Current score

        """
        return self.score
    