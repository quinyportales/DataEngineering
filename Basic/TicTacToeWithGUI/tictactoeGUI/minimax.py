class Minimax:
    def __init__(self, battlefield):
        self.battlefield = battlefield

    def evaluate(self, board):
        """Board current state evaluation"""

        for row in range(3):
            if board[row][0] == board[row][1] == board[row][2] != "":
                if board[row][0] == "O":
                    return +10
                else:
                    return -10

        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != "":
                if  board[0][col] == "O":
                    return +10
                else:
                    return -10


        if board[0][0] == board[1][1] == board[2][2] != "":
            if board[0][0] == "O": 
                return +10 
            else:
               return -10

        if board[0][2] == board[1][1] == board[2][0] != "":
            if board[0][2] == "O":
                return +10
            else:
                return -10

        return 0  #tie or not finished game

    def is_moves_left(self, board):
        """available positions"""
        for row in board:
            if "" in row:
                return True
        return False

    def minimax(self, board, depth, is_maximizing):
        """implementing Minimax."""
        score = self.evaluate(board)

        #if the game over
        if score == +10 or score == -10: 
            return score
        if not self.is_moves_left(board):
            return 0 

        if is_maximizing:
            best = -float("inf")

            for row in range(3):
                for col in range(3):
                    if board[row][col] == "":
                        board[row][col] = "O"  
                        best = max(best, self.minimax(board, depth + 1, False))
                        board[row][col] = ""  #reverting the move
            return best
        else:
            best = float("inf")

            for row in range(3):
                for col in range(3):
                    if board[row][col] == "":
                        board[row][col] = "X"  
                        best = min(best, self.minimax(board, depth + 1, True))
                        board[row][col] = "" 
            return best

    def get_best_move(self):
        """best PC move"""
        board = self.get_current_board()
        best_val = -100000
        best_move = None

        for row in range(3):
            for col in range(3):
                if board[row][col] == "":
                    board[row][col] = "O"  
                    move_val = self.minimax(board, 0, False)
                    board[row][col] = ""  #revert the move

                    if move_val > best_val:
                        best_val = move_val
                        best_move = (row, col)

        return best_move

    def get_current_board(self):
        board = [["" for _ in range(3)] for _ in range(3)]
        for (row, col), button in self.battlefield.buttons.items():
            board[row][col] = button["text"]
        return board
