import random
import requests

# List of words for the Hangman game
url = "https://raw.githubusercontent.com/ignis-sec/Pwdb-Public/master/wordlists/ignis-1K.txt"
response = requests.get(url)
WORD_LIST = response.text.split()


class HangmanGame:
    def __init__(self):
        self.word = random.choice(WORD_LIST).lower()
        self.guessed_letters = set()
        self.wrong_attempts = 0
        self.max_attempts = 6

    def guess(self, letter):
        if letter in self.guessed_letters:
            return "You've already guessed that letter."

        self.guessed_letters.add(letter)

        if letter in self.word:
            if all(l in self.guessed_letters for l in self.word):
                return "Congratulations! You've guessed the password: " + self.word
            return "Correct! " + self.get_display_word() + "\n" + self.get_game_status()
        else:
            self.wrong_attempts += 1
            if self.wrong_attempts >= self.max_attempts:
                return "Game over! The password was: " + self.word
            return "Wrong! " + self.get_display_word() + "\n" + self.get_game_status()

    def get_display_word(self):
        return " ".join(l if l in self.guessed_letters else "_" for l in self.word)

    def get_remaining_attempts(self):
        return self.max_attempts - self.wrong_attempts

    def get_guessed_letters(self):
        return ", ".join(sorted(self.guessed_letters))

    def get_game_status(self, prefix_message=""):
        return (
            f"{prefix_message}\n"
            f"Remaining attempts: {self.get_remaining_attempts()}\n"
            f"Guessed characters: {self.get_guessed_letters()}\n"
        )


# Dictionary to store active games
active_games = {}


def start_new_game(chat_id):
    active_games[chat_id] = HangmanGame()
    return active_games[chat_id]
