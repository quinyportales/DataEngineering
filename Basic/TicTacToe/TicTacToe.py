
"""
Tic tac tore game on the terminal 
"""

import os
import datetime
from random import randint
from pathlib import Path

def win_log(name):
    """
    Write/update the file with current player victory log
    """
    current_time = datetime.datetime.now().strftime('%d-%m-%Y %X ')
    filename = 'win_log.txt'
    with open(filename, 'a',  encoding='utf-8') as f:
        f.write(f'{current_time} {name} won \n')
        print(f'{current_time} {name} won \n')

def print_win_log(name):
    """
    Shows the current player victory log on the terminal
    """
    filename = Path('win_log.txt')
    if filename.is_file():
        with open(filename, 'r',  encoding='utf-8') as f:
            print(f.read())
    else:
        print('No win log found\n')
    menu(name)

def clear_win_log():
    """Deletes the win log file"""
    filename = Path('win_log.txt')
    if filename.is_file():
        os.remove(filename)
        print('Win log cleared\n')
    else:
        print('No win log found\n')
    menu(name)

def print_board(board):
    """This print out a 3x3 board"""
    for row in board:
        print(row)

def menu(name):
    """Prints out the menu on the terminal"""
    options = ['Play', 'View win log', 'Clear win log', 'Exit']
    for i,option in enumerate(options):
        print(f'{i+1} {option}')
    choosed = False
    while choosed is False:
        choosed = int(input('Choose an option: '))
        if choosed not in range(1, len(options)+1):
            choosed = False
            print('Invalid option')
            continue
    if choosed == 1:
        play_tic_tac_toe(name)
    elif choosed == 2:
        print_win_log(name)
    elif choosed == 3:
        clear_win_log()
    else:
        print('Bye bye! till the next game')


def eval_board(player):
    """
    This function evaluates the board and returns the winner if there is one
    """
    rows_player = []
    cols_player = []
    for i,j in player:
        rows_player.append(i)
        cols_player.append(j)
    rows_player.sort()
    cols_player.sort()
    if len(set(rows_player)) == 1 or len(set(cols_player)) == 1 or rows_player == cols_player :
        print('Game Over!')
        return 'winner'
    return None


def play_tic_tac_toe(name):
    """
    Takes the position from the user to fill the blank spaces and 
    generates random position for the PC player
    """

    board = [[None for _ in range(0,3)] for _ in range(0,3)]
    player=[]
    pc =[]
    while any(None in row for row in board):
        row, col = ((input("Coose your position row and col separated by a blank space: ")).split())
        print('\n')
        row, col = int(row), int(col)
        if  row not in range(0,3) or col not in range(0,3):
            print('Invalid position, enter row and col in range')
            continue
        if  board[row][col] is not None:
            print('Position already taken')
            continue
        player.append((row,col))
        board[row][col] = 'X'

        #PC time to play
        while any(None in row for row in board):
            pc_row= randint(0, 2)
            pc_col = randint(0,2)
            if board[pc_row][pc_col] is None:
                pc.append((pc_row,pc_col))
                board[pc_row][pc_col] = 'O'
                break
            continue
        print_board(board)

        #time to evaluate
        if len(player)>=3:
            winner = eval_board(player)
            if winner is not None:
                win_log(name)
                break
            if len(pc)>=3:
                winner = eval_board(pc)
            if winner is not None:
                print('PC wins')
                break
            if winner is None:
                print("It's a Draw")
                winner = 'Draw'
    menu(name)
    return player, pc


if __name__=='__main__':
    name = input('Enter your name: ')
    print(f'Hello {name} \n')
    menu(name)
