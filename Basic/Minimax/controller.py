"""
TicTacToe game implementing minimax algorithm and MVC: Controller
"""
from view import Board

class Game:
    """Controls the flow of the game"""
    def __init__(self, player, computer):
        self.player = player
        self.computer = computer
        self.board = Board()

    # stactic so I don't need an instance to call it
    @staticmethod
    def minimax(board, player):
        """Minimax algorithm to choose the best move"""
        score = board.evaluate()
        if score != 0:
            return {'score': score}
        if board.is_full(): 
            return {'score': 0}

        avail_spots = board.get_possible_moves()
        moves = []

        for spot in avail_spots:
            move = {}
            move['index'] = spot

            board.make_move(spot, player)

            if player == 'X':
                result = Game.minimax(board, 'O')
                move['score'] = result['score']
            else:
                result = Game.minimax(board, 'X')
                move['score'] = result['score']

            #revert the moves
            board.grid[spot] = ' '

            #move is a list of dict with the positions and the scores
            moves.append(move)

        if player == 'X':
            best_move = max(moves, key=lambda x: x['score'])
        else:
            best_move = min(moves, key=lambda x: x['score'])

        return best_move


    def play(self):
        """Controls the game flow"""
        current_player = self.player

        while True:
            # Show the board
            self.board.display()

            # Current player choose
            current_player.make_move(self.board)

            # Checking if there's a winner
            winner = self.board.check_winner()
            if winner:
                self.board.display()
                print(f"{winner} wins!")
                break

            # Check for a tie
            if self.board.is_full():
                self.board.display()
                print("It's a tie :( !")
                break

            # Switching players
            if current_player == self.computer:
                current_player = self.player
            else:
                current_player = self.computer
