"""
TicTacToe game implementing minimax algorithm and MVC: Model
"""
class Player:
    """Human player"""
    def __init__(self, symbol):
        self.symbol = symbol

    def make_move(self, board):
        """Choose a position on the board"""
        while True:
            position = int(input(f"Player ({self.symbol}), choose a place (0-8): "))
            if 0 <= position < 9 and board.is_cell_empty(position):
                board.make_move(position, self.symbol)
                break
            print("Invalid position")

class Computer:
    """Computer player using Minimax algorithm"""
    def __init__(self, symbol, minimax_function):
        self.symbol = symbol
        self.opponent_symbol = 'O' if symbol == 'X' else 'X'
        self.minimax = minimax_function 

    def make_move(self, board):
        """Computer chooses the best move using Minimax"""
        best_move = self.minimax(board, self.symbol)
        board.make_move(best_move['index'], self.symbol)
