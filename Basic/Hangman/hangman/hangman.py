import random

class HangmanGame:
    def __init__(self):
        word_list = ['hangman', 'hello', 'python', 'weekend', 'coding', 'task', 'apple', 'food', 'coffee', 'spanish', 'venezuela']
        self.word = random.choice(word_list).upper()
        self.hidden_word = ['_'] * len(self.word)  #
        
        # Initializing
        self.wrong_guesses = 0
        self.guessed_letters = set()  # Unique letters
        self.attempts_left = 6

    def guess_letter(self, letter):
        letter = letter.upper()
        if letter in self.guessed_letters:
            return "That letter was guessed already"

        if letter in self.word:
            for i, char in enumerate(self.word):
                if char == letter:
                    self.hidden_word[i] = letter
            self.guessed_letters.add(letter)
            return f"You guessed '{letter}'"
        else:
            self.guessed_letters.add(letter)
            self.wrong_guesses += 1
            self.attempts_left -= 1
            return f"Wrong, letter '{letter}' is not in the word"

    def check_win(self):
        return '_' not in self.hidden_word

class Display:
    """To print out the stages on console"""
    def __init__(self):
        self.stages = [
            ''' 
              +---+
              |   |
              O   |
             /|\  |
             / \  |
                  |
            =========
            ''', '''
              +---+
              |   |
              O   |
             /|\  |
             /    |
                  |
            =========
            ''', '''
              +---+
              |   |
              O   |
             /|\  |
                  |
                  |
            =========
            ''', '''
              +---+
              |   |
              O   |
             /|   |
                  |
                  |
            =========''', '''
              +---+
              |   |
              O   |
              |   |
                  |
                  |
            =========
            ''', '''
              +---+
              |   |
              O   |
                  |
                  |
                  |
            =========
            ''', '''
              +---+
              |   |
                  |
                  |
                  |
                  |
            =========
            '''
        ]

    def display_man(self, wrong_guesses, attempts_left):
        print(f"You have {attempts_left} attempts left\n")
        print(self.stages[attempts_left])

    def display_hidden_word(self, hidden_word):
        print(" ".join(hidden_word))

    def display_answer(self, word):
        print(f"The word was {word}")