from copy import deepcopy
from random import randint

class Game:
    def __init__(self, player='X', computer='O'):
        self.player = player
        self.computer = computer
        self.empty = ' '
        self.board = [[self.empty for x in range(3)] for x in range(3)]

    def calculate_move(self):
        if self.is_board_empty():
            move = self.random_corner()
            return {'row': move[0], 'col': move[1]}

        move = self.minimax(self.computer, [-2, None], [2, None])
        if not move[1]:
            return False
        else:
            return {'row': move[1][0], 'col': move[1][1]}

    def minimax(self, mark, alpha, beta):
        if self.has_won(self.player):
            return [1, None]
        elif self.has_won(self.computer):
            return [-1, None]
        elif self.tied():
            return [0, None]

        if mark == self.player:
            for move in self.get_moves():
                new_board = Game(self.player, self.computer)
                new_board.board = deepcopy(self.board)
                alpha_copy = deepcopy(alpha)
                beta_copy = deepcopy(beta)
                value = new_board.move(mark, move[0], move[1]).minimax(self.opponent(mark), alpha_copy, beta_copy)[0]

                if value > alpha[0]:
                    alpha = [value, move]

                if alpha[0] >= beta[0]:
                    return alpha

            return alpha
        else:
            for move in self.get_moves():
                new_board = Game(self.player, self.computer)
                new_board.board = deepcopy(self.board)
                alpha_copy = deepcopy(alpha)
                beta_copy = deepcopy(beta)
                value = new_board.move(mark, move[0], move[1]).minimax(self.opponent(mark), alpha_copy, beta_copy)[0]

                if value < beta[0]:
                    beta = [value, move]

                if beta[0] <= alpha[0]:
                    return beta

            return beta

    def opponent(self, mark):
        return self.computer if mark == self.player else self.player

    def get_moves(self):
        moves = []
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == self.empty:
                    moves.append([r, c])
        return moves

    def tied(self):
        return not self.has_won(self.player) and not self.has_won(self.computer) and self.is_board_full()

    def is_board_full(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == self.empty:
                    return False
        return True

    def is_board_empty(self):
        return all(self.board[row][col] == self.empty for row in range(3) for col in range(3))

    def has_won(self, mark):
        return self.won_horizontal(mark) or self.won_vertical(mark) or self.won_diagonal(mark)

    def won_vertical(self, mark):
        for col in range(3):
            if self.board[0][col] == mark and self.board[0][col] == self.board[1][col] == self.board[2][col]:
                return True
        return False

    def won_horizontal(self, mark):
        for row in range(3):
            if self.board[row][0] == mark and self.board[row][0] == self.board[row][1] == self.board[row][2]:
                return True
        return False

    def won_diagonal(self, mark):
        return (self.board[0][0] == mark and self.board[0][0] == self.board[1][1] == self.board[2][2]) or \
               (self.board[2][0] == mark and self.board[2][0] == self.board[1][1] == self.board[0][2])

    def move(self, mark, row, col):
        if self.board[row][col] == self.empty:
            self.board[row][col] = mark
        return self

    def random_corner(self):
        return [(0, 0), (0, 2), (2, 0), (2, 2)][randint(0, 3)]
