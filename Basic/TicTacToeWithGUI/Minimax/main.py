"""
TicTacToe implementation 
"""
from Model import Player, Computer
from Controller import Game

if __name__=="__main__":
    player = Player('X')
    computer = Computer('O', Game.minimax) 
    game = Game(player, computer)
    game.play()