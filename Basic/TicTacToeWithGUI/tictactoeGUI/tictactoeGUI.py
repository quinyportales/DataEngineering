"""TicTacToe implementing minimax and a GUI"""
import tkinter as tk

class Windows:
        def __init__(self, root, title, battlefield, control_panel, status_panel):
            self.window = root  
            self.window.title(title)
            self.window.resizable(False, False)

            self.window.rowconfigure([0, 1, 2], weight=1)  # Tres filas
            self.window.columnconfigure([0, 1, 2], weight=1)  # Tres columnas

            # Status Panel
            status_panel.label.grid(row=0, column=0, columnspan=3, sticky="nsew")

            #  Battlefield 
            battlefield.frame.grid(row=1, column=0, columnspan=3, sticky="nsew")

            #  Control Panel
            control_panel.frame.grid(row=2, column=0, columnspan=3, sticky="nsew")

class Battlefield:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="white", width=300, height=300)
        self.frame.grid_propagate(False)

        self.marked_positions = []
        self.buttons = {}  

        for row in range(3):
            self.frame.rowconfigure(row, weight=1)
            for col in range(3):
                self.frame.columnconfigure(col, weight=1)

                btn = tk.Button(
                    self.frame,
                    text="",
                    font=("Consolas", 20, "bold"),
                    bg="#343434",
                    foreground="#4584b6",
                )
                btn.grid(row=row, column=col, sticky="nsew")
                self.buttons[(row, col)] = btn  
                btn.bind("<Button-1>", lambda event, r=row, c=col, b=btn: self.get_click(event, r, c, b))

    def get_click(self, event, row, col, button):
        if button["text"] == "":
            button["text"] = "X"
            self.marked_positions.append((row, col))
            self.on_player_move() 

    def on_player_move(self):
        """PC time to play"""
        from minimax import Minimax 
        minimax = Minimax(self) 
    
        board = minimax.get_current_board()
        if minimax.evaluate(board) != 0 or not minimax.is_moves_left(board):
            return  #game over no more move

        best_move = minimax.get_best_move()
        if best_move:  
            row, col = best_move
            self.make_move(row, col, "O") 


    def make_move(self, row, col, symbol):
        if (row, col) in self.buttons and self.buttons[(row, col)]["text"] == "":
            self.buttons[(row, col)]["text"] = symbol
            self.marked_positions.append((row, col))

    def reset_board(self):
        """Resets the board for a new game."""
        self.marked_positions = []
        for button in self.buttons.values():
            button["text"] = ""



class ControlPanel:
    def __init__(self, parent, battlefield):
        self.frame = tk.Frame(parent, bg="#343434", width=150, height=150)  # Control panel frame
        self.frame.grid_propagate(False)

        # control buttons
        restart_button = tk.Button(
            self.frame, 
            text="Restart",
            font=("Consolas", 12), 
            bg="#4584b6", 
            fg="white", 
            command = battlefield.reset_board
            )
        restart_button.pack(pady=10)
         

class StatusPanel:
    """To display messages"""
    def __init__(self, parent):
        self.label = tk.Label(
            parent,
            text="Choose a position",
            font=("Consolas", 20),
            background="#343434",
            foreground="white",
            anchor="center",
            width=20
        )
