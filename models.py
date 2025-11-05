import numpy as np

class Board:
    def __init__(self, size: int, player1: 'Player', player2: 'Player', seed: int=None):
        self.rows = size
        self.cols = size
        self.seed = seed
        self.player1 = player1
        self.player2 = player2
        self.turn: Player = player1 # player1 is first mover

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
    
    def change_turn(self):
        """
        This function changes the player playing: from the player that has moved to the player that will make the next move.

        Parameters:
            None

        Returns:
            None
        """
        try:
            self.turn = self.player2 if self.turn == self.player1 else self.player1
        except:
            raise TypeError (f'Turn not recognized:', self.turn)

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
        
        return False ##CHECK

    def make_move(self, row: int, col: int) -> None:
        """
        Records a player's move. If the move is valid, it adds the points from the cell to the player's score. It sets the cell to 0. Automatically switches player's turn.

        Parameters:
            row (int): Row index of the move
            col (int): Column index of the move

        Returns: 
            None

        Raises:
            ValueError: If the move is invalid

        """
        if self.is_move_valid(row, col):
            points = self.table[row, col]
            self.table[row, col] = 0
            self.turn.add_to_score(points)
            self.last_move = (row, col)
            self.change_turn()
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
    
    def available_moves_array(self):
        """
        This function computes a matrix with available moves. It then finds indexes of squares where moves are available.
        The lenght of the return array is equal to the number of available moves.

        Parameters:
            None

        Returns:
            NDArray: array of the original matrix indexes with possible moves.
        """
        table = self.table

        if self.last_move is None: 
            moves_array = np.argwhere(table != 0)
            return moves_array

        last_row_index, last_col_index = self.last_move
        last_row = table[last_row_index, :]
        last_column = table[:, last_col_index]

        new_table = np.full_like(table, -1)
        new_table[last_row_index, :] = last_row
        new_table[:, last_col_index] = last_column

        moves_array = np.argwhere((new_table != -1) & (new_table != 0))

        return moves_array
    
    def is_winner(self, player1: 'Player', player2: 'Player'):
        """
        This function checks if there is a winner.

        Params:
            None

        Returns:
            int: 1 if given player1 wins, -1 if given player1 loses, 0 if draw
        """

        if self.is_there_move_possible(): raise TabError('There are still moves available! Keep playing')
        score_p1 = player1.get_score()
        score_p2 = player2.get_score()

        if score_p1 > score_p2: return 1
        if score_p2 > score_p1: return -1
        if score_p1 == score_p2: return 0
        else : raise TabError('Error in is_winner')



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
    