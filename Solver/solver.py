import numpy as np

board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]


def print_b(board):
    for i in range(len(board[0])):
        print(board[i][:])

class Solver:
    def __init__(self,board):
        self.board = board

    def solve(self):
        pos = self.empty()
        if pos is True:
            return True
        else:
            i, j = pos
        for value in range(1, 10):
            if self.check( i, j, value):
                self.board[i][j] = value
                if self.solve():
                    return True
                self.board[i][j] = 0
        return False

    def check(self, i, j, value):
        if self.check_row_column( i, j, value) is False or self.check_subfield(i, j, value) is False:
            return False
        else:
            return True

    def empty(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    return i, j
        return True

    def check_row_column(self, i, j, value):
        col = [self.board[i][j] for i in range(len(self.board))]
        if value in self.board[i][:] or value in col:
            return False
        return True

    def check_subfield(self, i, j, value):
        subsize = int(np.sqrt(len(self.board)))
        subfield_number = np.array([i, j]) // subsize
        subfield_index_left = subfield_number * subsize
        subfield = np.random.rand(subsize, subsize).tolist()
        for k in range(subsize):
            for h in range(subsize):
                subfield[k][h] = self.board[subfield_index_left[0] + k][subfield_index_left[1] + h]
        if value in subfield:
            return False
        return True

    def get_board(self):
        return self.board


