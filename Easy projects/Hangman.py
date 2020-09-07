import random


class HungMan():
    hidden_words = ['python', 'java', 'kotlin', 'javascript']

    def __init__(self, attempts, answers=None):
        if answers is None:
            answers = []
        print('H A N G M A N')
        self.hidden_word = random.choice(self.hidden_words)
        self.hidden_word_characters = set(self.hidden_word)
        self.answers = answers
        self.guessed_characters = self.hidden_word_characters.intersection(self.answers)
        self.attempts = attempts
        self.play()
        
    def play(self):
        while self.attempts > 0 and len(self.hidden_word_characters.difference(self.guessed_characters)):
            self.print()
            self.check_input()
        self.end_game()

    def print(self):
        result = []
        for ch in self.hidden_word:
            if ch in self.guessed_characters:
                result.append(ch)
            else:
                result.append('-')
        print('\n' + ''.join(result))
        # print("Left attempts:", self.attempts)

    def check_input(self):
        user_input = input('Input a letter: ')
        if len(user_input) != 1:
            print('You should input a single letter')
        elif not user_input.isascii() or not user_input.islower():
            print('It is not an ASCII lowercase letter')
        elif user_input in self.answers:
            print('You already typed this letter')
        else:
            self.answers.append(user_input)
            if user_input in self.hidden_word_characters:
                self.guessed_characters.add(user_input)
            else:
                print('No such letter in the word')
                self.attempts -= 1

    def end_game(self):
        if self.attempts > 0:
            print('You guessed the word ' + self.hidden_word + '!\nYou survived!')
        else:
            print('''You are hanged!''')


if __name__ == '__main__':
    while True:
        decision = input('Type "play" to play the game, "exit" to quit: ')
        if decision == "play":
            hungMan = HungMan(8)
        elif decision == "exit":
            break
