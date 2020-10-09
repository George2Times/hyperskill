from typing import Callable
from random import choice


class Board:
    """Tic-Tac-Toe board"""
    __board: [str, ...] = ['_', '_', '_',
                           '_', '_', '_',
                           '_', '_', '_']
    wins_combinations: ((int, int, int), ...) = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6),  # diagonals
    )

    # print
    def __repr__(self) -> str:
        return f'''\t\t---------
        | {self.__board[0]} {self.__board[1]} {self.__board[2]} |
        | {self.__board[3]} {self.__board[4]} {self.__board[5]} |
        | {self.__board[6]} {self.__board[7]} {self.__board[8]} |
        ---------'''

    def clear(self) -> None:
        """Reset board state."""
        self.__board = ['_', '_', '_', '_', '_', '_', '_', '_', '_']

    def __len__(self) -> int:
        """Return the number of empty cells."""
        return self.__board.count('_')

    def winner(self) -> str or None:
        """Return winner if exist, else None"""
        # before first 5 moves there is no winner
        if self.__len__() in (9, 8, 7, 6):
            return None
        # after 5 moves check if there is a winner
        for w in self.wins_combinations:
            if all(self.__board[i] == 'X' for i in w):
                return 'X wins'
            if all(self.__board[i] == 'O' for i in w):
                return 'O wins'
        # 0 moves left + no winner = 'Draw'
        if self.__len__() == 0:
            return 'Draw'
        return None

    def __getitem__(self, i: int) -> str:
        return self.__board[i]

    def __setitem__(self, i: int, value: str) -> None:
        self.__board[i] = value

    def is_free(self, i: int) -> bool:
        return self.__board[i] == '_'

    def __iter__(self) -> str:
        for i in self.__board:
            yield i


class User:
    @staticmethod
    def move(_board: Board, current_turn='X') -> int:
        """Gets coordinates from user input"""
        while True:
            try:
                x, y = [int(i) for i in input('Enter the coordinates: ').split()]
            except (NameError, ValueError):
                print('You should enter numbers!')
                continue
            if not 0 < x < 4 or not 0 < y < 4:
                print('Coordinates should be from 1 to 3!')
                continue
            cell: int = ((3 - y) * 3) + (x - 1)
            if not _board.is_free(cell):
                print('This cell is occupied! Choose another one!')
                continue
            return cell


class RandomAI:
    @staticmethod
    def rand_move(_board: Board) -> int:
        """Return random free cell."""
        return choice([i for i, _ in enumerate(_board) if _board.is_free(i)])

    def move(self, _board: Board, current_turn='X') -> int:
        """Returns a random integer from 0 to 8."""
        print('Making move level "easy"')
        return self.rand_move(_board=_board)


class MediumAI(RandomAI):
    def move(self, _board: Board, current_turn='X') -> int:
        """
        if it can win in one move -> do it
        stop the enemy from winning -> do it
        else -> returns a random free cell
        """
        print('Making move level "medium"')
        for win_combination in _board.wins_combinations:
            win_line = [_board[i] for i in win_combination]
            try:
                # order: first check if I can win, next if I can stop enemy
                order = ('X', 'O') if current_turn == 'X' else ('O', 'X')
                for player in order:
                    if win_line.count(player) == 2:
                        cell = win_combination[win_line.index('_')]
                        return cell
            except:
                print('Something is wrong')
                continue
        return self.rand_move(_board=_board)


class HardAI(MediumAI):
    outcomes: {str: (int, int), } = {
        'X wins': (-1, 0),
        'O wins': (1, 0),
        'Draw': (0, 0),
    }

    def move(self, _board: Board, current_turn='X') -> int:
        print('Making move level "hard"')
        if current_turn == 'X':
            _, cell = self.min(_board, -2, 2)
        else:
            _, cell = self.max(_board, -2, 2)
        return cell

    def max(self, _board, alpha, beta) -> (int, int):
        # -1 - loss
        # 0 - draw
        # 1 - win
        maxv: int = -2
        cell: int = -1

        result = _board.winner()
        if result:
            return self.outcomes[result]

        for i, item in enumerate(_board):
            if item == '_':
                _board[i] = 'O'
                m, _ = self.min(_board, alpha, beta)
                if m > maxv:
                    maxv = m
                    cell = i
                _board[i] = '_'

                if maxv >= beta:
                    return maxv, cell
                if maxv > alpha:
                    alpha = maxv
        return maxv, cell

    def min(self, _board, alpha, beta) -> (int, int):
        minv: int = 2
        cell: int = -1

        result = _board.winner()
        if result:
            return self.outcomes[result]

        for i, item in enumerate(_board):
            if item == '_':
                _board[i] = 'X'
                m, _ = self.max(_board, alpha, beta)
                if m < minv:
                    minv = m
                    cell = i
                _board[i] = '_'

            if minv <= alpha:
                return minv, cell
            if minv < beta:
                beta = minv
        return minv, cell


def game(board=Board(),
         player1=User(),  # 'X' player, turn_switcher = True
         player2=RandomAI(),  # 'O' player, turn_switcher = False
         starts_game='X') -> str:
    """Returns result of the game"""
    turn_switcher: bool = True if starts_game == 'X' else 'O'
    board.clear()
    while True:
        current_turn: str = 'X' if turn_switcher else 'O'
        print(board)
        winner = board.winner()
        if winner is not None:
            return winner
        cell = player1.move(board, current_turn=current_turn) if turn_switcher else \
            player2.move(board, current_turn=current_turn)
        board[cell] = current_turn
        turn_switcher = not turn_switcher


def main():
    difficulties: {str: Callable, } = {
        'user': User,
        'easy': RandomAI,
        'medium': MediumAI,
        'hard': HardAI
    }
    while True:
        command: [str, ...] = input('Input command: ').lower().split()
        if 'exit' in command:
            exit('Bye!')
        try:
            p1 = difficulties[command[1]]()
            p2 = difficulties[command[2]]()
            print(game(player1=p1, player2=p2))
        except (KeyError, IndexError, ValueError):
            print("Unknown option")
            continue


if __name__ == "__main__":
    main()
