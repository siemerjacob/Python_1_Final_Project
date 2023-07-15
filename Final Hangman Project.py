import tkinter as tk
from datetime import datetime
import random
import os

class HangmanGame:
    def __init__(self):
        # Set up the tkinter window
        self.window = tk.Tk()
        self.window.title("Hangman")

        # Set up the game state
        self.word = self.get_random_word()
        self.guesses = set()
        self.max_incorrect_guesses = 6
        self.num_incorrect_guesses = 0
        self.game_over = False

        # Set up the GUI
        #set resolution
        self.window.geometry("1280x720")
        #set background color
        self.window.configure(background='black')
        #set font
        #display number of guesses left
        self.guesses_left = tk.Label(self.window, text="Guesses Left: " + str(self.max_incorrect_guesses - self.num_incorrect_guesses), font=("Arial", 20), bg="black", fg="white")
        self.guesses_left.pack()


        self.window.option_add("*Font", "Arial 24")
        self.label = tk.Label(self.window, text=" ".join(self.get_display_word()), font=("", 24))
        self.label.pack()
        self.entry = tk.Entry(self.window)
        self.entry.pack()
        self.button = tk.Button(self.window, text="Guess", command=self.guess)
        self.button.pack()

        self.new_game_button = tk.Button(self.window, text="New Game", command=self.new_game)
        self.new_game_button.pack()
        self.exit_button = tk.Button(self.window, text="Exit", command=self.exit)
        self.exit_button.pack()

        self.status_text = tk.StringVar()
        self.status = tk.Label(self.window, textvariable=self.status_text)
        self.status.pack()

        #show the gui and start the main loop
        self.window.mainloop()
        #clean up after the game is over
        if self.game_over:
            self.end()

    def new_game(self):
        self.word = self.get_random_word()
        self.guesses = set()
        self.num_incorrect_guesses = 0
        self.game_over = False
        self.label.config(text=" ".join(self.get_display_word()))
        self.entry.delete(0, tk.END)
        self.guesses_left.config(text="Guesses Left: " + str(self.max_incorrect_guesses - self.num_incorrect_guesses))
        self.status_text.set("")

    def exit(self):
        self.window.destroy()

    def get_random_word(self):
        words = ["apple", "orange", "banana", "grape", "strawberry", "blueberry", "pineapple", "watermelon", "kiwi", "mango", "cherry", "peach", "pear", "apricot", "lemon", "lime", "coconut", "avocado", "tomato", "potato", "carrot", "broccoli", "cauliflower", "spinach", "lettuce", "cucumber", "asparagus", "garlic", "onion", "celery", "pepper", "mushroom", "eggplant", "zucchini", "squash", "cabbage", "corn", "sweet potato", "pumpkin", "peanut", "almond", "walnut", "cashew", "pecan", "hazelnut", "macadamia", "pistachio", "sunflower", "pumpkin", "oat", "barley", "quinoa", "rice", "buckwheat", "sugar", "salt", "pepper", "flour", "butter", "milk", "cheese", "yogurt", "cream", "egg", "bread", "pasta", "pizza", "ice cream", "cake", "cookie", "chocolate", "candy", "honey", "jam", "soda", "juice", "coffee", "tea", "beer", "wine", "whiskey", "vodka", "gin", "rum", "chicken", "beef", "pork", "fish", "lobster", "crab", "shrimp", "salmon", "tuna", "duck", "turkey", "rabbit", "goat", "sheep", "horse", "cow", "pig", "elephant", "lion", "tiger", "bear", "wolf", "dog", "cat", "mouse", "rabbit", "bird", "fish", "whale", "dolphin", "shark", "octopus", "crab", "lobster", "ant", "bee", "butterfly", "dragonfly", "ladybug", "mosquito", "spider", "snail", "snake", "frog", "turtle", "rabbit", "deer", "fox", "monkey", "panda", "penguin", "squirrel", "wolf"]

        return random.choice(words)

    # This function returns the word with underscores for unguessed letters
    def get_display_word(self):
        display_word = ""
        for letter in self.word:
            if letter in self.guesses:
                display_word += letter
            else:
                display_word += "_"
        return display_word
    # This function is called when the user clicks the "Guess" button
    def guess(self):
        if self.game_over:
            return

        guess = self.entry.get().lower()
        if len(guess) != 1:
            self.status_text.set("Please enter a single letter.")
            return

        if guess in self.guesses:
            self.status_text.set("You already guessed that letter.")
            return

        self.guesses.add(guess)
        if guess in self.word:
            self.status_text.set("Good guess!")
            self.label.config(text=" ".join(self.get_display_word()))
        else:
            # Increment the number of incorrect guesses
            self.num_incorrect_guesses += 1
            self.status_text.set("Sorry, that's not in the word.")
        # Update the number of guesses left
        self.guesses_left.config(text="Guesses Left: " + str(self.max_incorrect_guesses - self.num_incorrect_guesses))

        # Check if the game is over
        try:
            if self.num_incorrect_guesses >= self.max_incorrect_guesses:
                self.status_text.set("Game over! The word was " + self.word)
                self.game_over = True
            elif self.get_display_word() == self.word:
                self.status_text.set("You win! The word was " + self.word)
                self.game_over = True
        except Exception as e:
            self.status_text.set("An error occurred: " + str(e))
            self.game_over = True


    def save_game_time(self):
                # Get the current time
        now = datetime.now()

                # Format the time as a string
        time_str = now.strftime("%Y-%m-%d %H:%M:%S")

                # Open the file for writing
        with open("game_times.txt", "a") as file:
                    # Write the time string to the file
            file.write(time_str + "\n")

            # This function is called to start the game
        def run(self):
            # Start the game
            self.start()
            # Clean up after the game is over
            if self.game_over:
                self.end()

        def start(self):
            # Show the GUI and start the main loop
            self.window.mainloop()

        # This function is called to clean up after the game is over
        def end(self):
            # Destroy the GUI window
            self.window.destroy()
            # Save the game time
            self.save_game_time()


game = HangmanGame()
game.run()



