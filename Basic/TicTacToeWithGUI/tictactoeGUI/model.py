import tkinter as tk
from tictactoeGUI import Windows, Battlefield, StatusPanel, ControlPanel
from minimax import Minimax


if __name__ == "__main__":
    root = tk.Tk()

    battlefield = Battlefield(root)
    control_panel = ControlPanel(root, battlefield)
    status_panel = StatusPanel(root)

    windows = Windows(root, "Tic Tac Toe using Minimax", battlefield, control_panel, status_panel)

    root.mainloop()
