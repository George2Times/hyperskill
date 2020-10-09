import random
import copy
import math


class TicTacToe:
    def __init__(self, player1, player2):
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.options = ['X', 'O']
        self.players = {'hard':     self.get_hard_computer_move,
                        'medium':   self.get_medium_computer_move,
                        'easy':     self.get_easy_computer_move,
                        'user':     self.get_player_move}
        self.move_functions = [self.players[player1],
                               self.players[player2]]
        self.turn: 0 or 1 = 0  # 0: player1 1: player2
        self.display()
        self.play()

    def display(self) -> None:
        print('---------')
        for i in range(3):
            print('|', *self.board[i], '|')
        print('---------')

    @staticmethod
    def get_cell(board, x, y) -> str:
        return board[3 - y][x - 1]

    def set_cell(self, value, x, y) -> None:
        self.board[3 - y][x - 1] = value

    def is_valid_move(self, board, x, y) -> bool:
        return self.get_cell(board, x, y) == ' '

    def get_player_move(self) -> (int, int):
        while True:
            coordinates = input('Enter the coordinates: ').split()
            if len(coordinates) != 2:
                print('You should enter numbers!')
            elif any([not i.isnumeric() for i in coordinates]):
                print('You should enter numbers!')
            elif any([not 1 <= int(i) <= 3 for i in coordinates]):
                print('Coordinates should be from 1 to 3!')
            else:
                x, y = map(int, coordinates)
                if not self.is_valid_move(self.board, x, y):
                    print('This cell is occupied! Choose another one!')
                else:
                    return x, y

    def get_valid_moves(self, board) -> [(int, int), ]:
        return [(i, j) for i in range(1, 4) for j in range(1, 4)
                if self.is_valid_move(board, i, j)]

    def get_random_move(self) -> (int, int):
        return random.choice(self.get_valid_moves(self.board))

    def get_easy_computer_move(self) -> (int, int):
        print('Making move level "easy"')
        return self.get_random_move()
    
    def get_medium_computer_move(self) -> (int, int):
        print('Making move level "medium"')
        i_and_enemy = self.options[self.turn], self.options[int(not self.turn)]
        # 1. If it can win in one move (if it has two in a row), it places a third to get three in a row and win
        # 2. If the opponent can win in one move, it plays the third itself to block the opponent to win.
        for player in i_and_enemy:
            for move in self.get_valid_moves(self.board):
                future_board = copy.deepcopy(self.board)
                future_board[3 - move[1]][move[0] - 1] = player
                if self.check_board(future_board) == player + ' wins':
                    return move
        # 3. Otherwise, it makes a random move.
        return self.get_random_move()

    def make_best_move(self) -> (int, int):
        best_score = -math.inf
        best_move = None
        for move in self.get_valid_moves(self.board):
            future_board = copy.deepcopy(self.board)
            future_board[3 - move[1]][move[0] - 1] = self.options[self.turn]
            score = self.minimax(False, self.options[int(not self.turn)], board=future_board)
            future_board[3 - move[1]][move[0] - 1] = ' '
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def minimax(self, isMaxTurn: bool, maximizerMark, board: [[], ]) -> int:
        state = self.check_board(board) == maximizerMark + ' wins'
        if state == 'Draw':
            return 0
        elif state == maximizerMark + ' wins':
            return 1
        elif state in ('X wins', 'O wins'):
            return -1

        scores = []
        for move in self.get_valid_moves(board):
            board = copy.deepcopy(self.board)
            board[3 - move[1]][move[0] - 1] = self.options[self.turn]
            scores.append(self.minimax(not isMaxTurn, maximizerMark, board))
            board[3 - move[1]][move[0] - 1] = ' '

        return max(scores) if isMaxTurn else min(scores)

    def get_hard_computer_move(self) -> (int, int):
        """
        Minimax
        """
        print('Making move level "hard"')
        return self.get_random_move()

    @staticmethod
    def check_board(board: [[], ]) -> str or False:
        """
        return False if game is not finished
        """
        if board[0][0] == board[1][1] == board[2][2] != ' ':
            return board[1][1] + ' wins'
        if board[0][2] == board[1][1] == board[2][0] != ' ':
            return board[1][1] + ' wins'
        for i in range(3):
            if board[i].count('X') == 3:
                return 'X wins'
            if board[i].count('O') == 3:
                return 'O wins'
            col = [j[i] for j in board]
            if col.count('X') == 3:
                return 'X wins'
            if col.count('O') == 3:
                return 'O wins'
        if any([i.count(' ') for i in board]):
            return False
        return 'Draw'

    def play(self) -> None:
        while True:
            move_getter = self.move_functions[self.turn]
            x, y = move_getter()
            self.set_cell(self.options[self.turn], x, y)
            self.display()
            result = self.check_board(self.board)
            if result:
                print(result)
                break
            self.turn = 1 - self.turn


players = ('hard', 'medium', 'easy',
           'user')


def menu():
    """
    command "start" , take two parameters: who will play X and who will play O.
        "user" to play as a human and "easy" to play as an easy level AI.
    command "exit" simply terminate the program.
    """
    command = list(input().split(' '))
    if command[0] == 'exit':
        exit()
    elif command[0] == 'start':
        if len(command) != 3 or \
                command[1] not in players or \
                command[2] not in players:
            print('Bad parameters!')
        else:
            TicTacToe(command[1], command[2])
    else:
        print('Bad command')


def main():
    while True:
        menu()


if __name__ == '__main__':
    main()
