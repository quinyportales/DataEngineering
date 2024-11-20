"""
TicTacToe game implementing minimax algorithm and MVC: View
"""
class Board:
    """View for the board game"""
    def __init__(self):
        self.grid = [" "] * 9  # Empty board

    def display(self):
        """Prints out the board"""
        grid = self.grid
        print(f"""
         {grid[0]} | {grid[1]} | {grid[2]}
        ---------
         {grid[3]} | {grid[4]} | {grid[5]}
        ---------
         {grid[6]} | {grid[7]} | {grid[8]}
        ---------
        """)

    def is_cell_empty(self, position):
        """Checks position availability"""
        return self.grid[position] == " " #True if it's empty

    def make_move(self, position, symbol):
        """Fills an available position"""
        if self.is_cell_empty(position):
            self.grid[position] = symbol
            return True
        return False

    def check_winner(self):
        """Checking if there's a winner"""
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
            (0, 4, 8), (2, 4, 6)             # diagonal
        ]
        for combo in winning_combinations:
            #if they're all equals and diferent of " " (empty)
            if self.grid[combo[0]] == self.grid[combo[1]] == self.grid[combo[2]] != " ":
                return self.grid[combo[0]]
        return None

    def evaluate(self):
        """This evaluates the terminal state"""
        winner = self.check_winner()
        if winner == 'X':  # PC wins
            return 10
        if winner == 'O':  # Player wins
            return -10
        return 0  # Tie or still ongoing

    def is_full(self):
        """Check is the boar is full"""
        return " " not in self.grid

    def get_possible_moves(self):
        """Returns a list of index for the avialable spots"""
        #value: X, O, empty
        return [i for (i, value) in enumerate(self.grid) if value == " "]
