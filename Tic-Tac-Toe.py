class TicTacToe:
    state = []
    n = 3
    x_round = True
    X_cell = 'X'
    O_cell = 'O'
    empty_cell = ' '
    # or empty_cell = '_'
    result = 'Game not finished'

    def __init__(self):
        for i in range(self.n):
            row = []
            for j in range(self.n):
                row.append(self.empty_cell)
            self.state.append(row)

    def print_state(self):
        print('---------')
        print('|', *[c for c in self.state[0]], '|', sep=' ')
        print('|', *[c for c in self.state[1]], '|', sep=' ')
        print('|', *[c for c in self.state[2]], '|', sep=' ')
        print('---------')

    def count_cells(self, character):
        result = 0
        for row in self.state:
            result += row.count(character)
        return result

    def is_game_finished(self):
        x_count = self.count_cells(self.X_cell)
        o_count = self.count_cells(self.O_cell)
        if abs(x_count - o_count) > 1:
            self.result = 'Impossible'
            return -1
        # check win
        state = [cell for row in self.state for cell in row]
        wins = []
        for win_seq in [[self.X_cell] * self.n, [self.O_cell] * self.n]:
            if win_seq == self.state[:3] or \
                    win_seq == state[3:6] or \
                    win_seq == state[6:] or \
                    win_seq == state[::3] or \
                    win_seq == state[1::3] or \
                    win_seq == state[2::3] or \
                    win_seq == state[::4] or \
                    win_seq == state[2:7:2]:
                wins.append(win_seq[0])
        if len(wins) == 1:
            self.result = wins[0] + ' wins'
            return 2
        if len(wins) == 2:
            self.result = 'Impossible'
            return -1
        if self.count_cells(self.empty_cell) == 0:
            self.result = 'Draw'
            return 1
        self.result = 'Game not finished'
        return 0

    def play(self):
        self.print_state()
        while self.is_game_finished() == 0:
            self.get_move()
            self.print_state()
        print(self.result, end='')

    def get_move(self):
        while True:
            try:
                a, b = [int(i) for i in input('Enter the coordinates: ').split()]
            except ValueError:
                print("You should enter numbers!")
            else:
                if a not in [1, 2, 3] or b not in [1, 2, 3]:
                    print('Coordinates should be from 1 to 3!')
                else:
                    # This cell is occupied! Choose another one!
                    a -= 1
                    b = 3 - b
                    # print('A, b: ', b * 3 + a)
                    if self.state[b][a] in [self.X_cell, self.O_cell]:
                        print('This cell is occupied! Choose another one!')
                    else:
                        if self.x_round:
                            self.state[b][a] = self.X_cell
                        else:
                            self.state[b][a] = self.O_cell
                        self.x_round = not self.x_round
                        break


if __name__ == '__main__':
    my_game = TicTacToe()
    my_game.play()

'''
(1, 3) (2, 3) (3, 3)
(1, 2) (2, 2) (3, 2)
(1, 1) (2, 1) (3, 1)
'''
