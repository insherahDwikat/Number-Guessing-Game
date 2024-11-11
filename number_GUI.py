import tkinter as tk
from tkinter import messagebox
import random
import time
import os
import pygame  # For sound effects

# Initialize pygame for sound effects
pygame.mixer.init()

# Provide full paths to sound files here
WIN_SOUND = pygame.mixer.Sound("C:/Users/Zaincp/OneDrive/Desktop/sounds/win_sound.wav")
LOSE_SOUND = pygame.mixer.Sound("C:/Users/Zaincp/OneDrive/Desktop/sounds/lose_sound.wav")
CLICK_SOUND = pygame.mixer.Sound("C:/Users/Zaincp/OneDrive/Desktop/sounds/click_sound.wav")

LEADERBOARD_FILE = "leaderboard.txt"

def update_leaderboard(name, difficulty, attempts):
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, 'r') as file:
            leaderboard = file.readlines()
    else:
        leaderboard = []
    
    leaderboard.append(f"{name} - {difficulty} - Attempts: {attempts}\n")
    
    with open(LEADERBOARD_FILE, 'w') as file:
        file.writelines(leaderboard)

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.geometry("500x400")
        self.root.configure(bg="lightyellow")

        self.player_name = ""
        self.secret_number = None
        self.attempts = 0
        self.max_attempts = float("inf")
        self.start_time = 0
        self.difficulty = ""
        self.min_number = 1
        self.max_number = 100
        self.time_left = 60  # Set 60 seconds timer
        self.wrong_guesses = []  # List to store wrong guesses

        self.setup_welcome_screen()

    def play_click_sound(self):
        CLICK_SOUND.play()  # Play the click sound whenever a button is pressed

    def exit_to_welcome(self):
        self.play_click_sound()  # Play click sound before going back to the welcome screen
        self.setup_welcome_screen()  # Go back to the welcome screen

    def setup_welcome_screen(self):
        self.clear_screen()
        self.welcome_frame = tk.Frame(self.root, bg="lightyellow")
        self.welcome_frame.pack(pady=20)

        tk.Label(self.welcome_frame, text="Welcome to the Number Guessing Game", font=("Arial", 16), bg="lightyellow").pack(pady=10)
        tk.Label(self.welcome_frame, text="Enter your name:", font=("Arial", 12), bg="lightyellow").pack(pady=5)
        self.name_entry = tk.Entry(self.welcome_frame, font=("Arial", 12))
        self.name_entry.pack(pady=5)

        tk.Button(self.welcome_frame, text="Start Game", command=self.start_game_setup).pack(pady=10)
        
        # Add an Exit button to close the game
        tk.Button(self.welcome_frame, text="Exit", command=self.root.quit).pack(pady=10)

    def start_game_setup(self):
        self.play_click_sound()  # Play click sound when the "Start Game" button is clicked
        self.player_name = self.name_entry.get().strip()
        if not self.player_name:
            messagebox.showerror("Error", "Please enter your name to start the game.")
            return

        self.setup_difficulty_screen()

    def setup_difficulty_screen(self):
        self.clear_screen()
        self.difficulty_frame = tk.Frame(self.root, bg="lightyellow")
        self.difficulty_frame.pack(pady=20)

        tk.Button(self.difficulty_frame, text="Easy (1-50)", command=lambda: self.start_game("easy", 1, 50, float("inf"))).pack(pady=5)
        tk.Button(self.difficulty_frame, text="Medium (1-100)", command=lambda: self.start_game("medium", 1, 100, 10)).pack(pady=5)
        tk.Button(self.difficulty_frame, text="Hard (1-500)", command=lambda: self.start_game("hard", 1, 500, 5)).pack(pady=5)
        tk.Button(self.difficulty_frame, text="View Leaderboard", command=self.show_leaderboard).pack(pady=10)
        
        # Add an Exit button to go back to the welcome screen
        tk.Button(self.difficulty_frame, text="Exit to Main Menu", command=self.exit_to_welcome).pack(pady=10)

    def start_game(self, difficulty, min_number, max_number, max_attempts):
        self.play_click_sound()  # Play click sound when a difficulty button is clicked
        self.difficulty = difficulty
        self.min_number = min_number
        self.max_number = max_number
        self.max_attempts = max_attempts
        self.secret_number = random.randint(min_number, max_number)
        self.attempts = 0
        self.start_time = time.time()
        self.time_left = 60  # Reset the timer to 60 seconds
        self.wrong_guesses = []  # Reset wrong guesses at the start of a new game

        self.setup_game_screen()

    def setup_game_screen(self):
        self.clear_screen()
        self.game_frame = tk.Frame(self.root, bg="lightyellow")
        self.game_frame.pack(pady=20)

        tk.Label(self.game_frame, text=f"Guess the number between {self.min_number} and {self.max_number}", font=("Arial", 14), bg="lightyellow").pack(pady=10)

        self.attempts_label = tk.Label(self.game_frame, text="Attempts: 0", font=("Arial", 12), bg="lightyellow")
        self.attempts_label.pack()

        self.timer_label = tk.Label(self.game_frame, text="Time left: 60s", font=("Arial", 12), bg="lightyellow")
        self.timer_label.pack()

        self.guess_entry = tk.Entry(self.game_frame, font=("Arial", 14))
        self.guess_entry.pack(pady=10)

        tk.Button(self.game_frame, text="Submit Guess", command=self.check_guess).pack(pady=5)

        self.hint_label = tk.Label(self.game_frame, text="", font=("Arial", 12), fg="blue", bg="lightyellow")
        self.hint_label.pack(pady=5)

        self.wrong_guesses_label = tk.Label(self.game_frame, text="Wrong Guesses: None", font=("Arial", 12), fg="red", bg="lightyellow")
        self.wrong_guesses_label.pack(pady=10)
        
        # Add an Exit button to go back to the welcome screen
        tk.Button(self.game_frame, text="Exit to Main Menu", command=self.exit_to_welcome).pack(pady=10)

        self.update_timer()

    def check_guess(self):
        self.play_click_sound()  # Play click sound when a guess is submitted
        try:
            guess = int(self.guess_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            return

        self.attempts += 1
        self.attempts_label.config(text=f"Attempts: {self.attempts}")

        if guess < self.secret_number:
            self.hint_label.config(text="Too low!")
            self.wrong_guesses.append(guess)
        elif guess > self.secret_number:
            self.hint_label.config(text="Too high!")
            self.wrong_guesses.append(guess)
        else:
            WIN_SOUND.play()  # Play win sound when the guess is correct
            messagebox.showinfo("Congratulations!", f"You've guessed the number {self.secret_number} in {self.attempts} attempts.")
            self.end_game()

        if self.attempts >= self.max_attempts:
            LOSE_SOUND.play()  # Play lose sound if max attempts reached
            messagebox.showinfo("Game Over", f"You've used all {self.max_attempts} attempts! The correct number was {self.secret_number}.")
            self.end_game()

        # Clear the guess entry after each submission
        self.guess_entry.delete(0, tk.END)  # Clear the input field after submitting the guess

        # Update the list of wrong guesses on the screen
        self.wrong_guesses_label.config(text=f"Wrong Guesses: {', '.join(map(str, self.wrong_guesses))}")

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left}s")
            self.root.after(1000, self.update_timer)
        else:
            LOSE_SOUND.play()  # Play lose sound on timeout
            messagebox.showinfo("Time Up", f"Time is up! The correct number was {self.secret_number}.")
            self.end_game()

    def end_game(self):
        update_leaderboard(self.player_name, self.difficulty, self.attempts)
        self.setup_difficulty_screen()

    def show_leaderboard(self):
        self.play_click_sound()  # Play click sound when "View Leaderboard" is clicked
        if os.path.exists(LEADERBOARD_FILE):
            with open(LEADERBOARD_FILE, 'r') as file:
                leaderboard = file.readlines()
        else:
            leaderboard = ["No scores yet!"]

        leaderboard_text = "\n".join([line.strip() for line in leaderboard])
        messagebox.showinfo("Leaderboard", leaderboard_text)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Run the game
root = tk.Tk()
app = NumberGuessingGame(root)
root.mainloop()
