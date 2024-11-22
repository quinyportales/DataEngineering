from hangman import Display, HangmanGame

if __name__ == "__main__":
    # Initializing the game
    hangman = HangmanGame()
    display = Display()
    is_running = True

    while is_running:
        display.display_man(hangman.wrong_guesses, hangman.attempts_left)
        display.display_hidden_word(hangman.hidden_word)
        letter = input("Enter a letter: ")

        print(hangman.guess_letter(letter))
        
        if hangman.check_win():
            display.display_hidden_word(hangman.hidden_word)
            print("Congratulations, you won!")
            break
        
        if hangman.attempts_left == 0:
            display.display_answer(hangman.word)
            print("Game Over, you lost!")
            display.display_man(hangman.wrong_guesses, hangman.attempts_left)
            break