from piece import Piece
from random import random


class Board:
    def __init__(self, size, prob):
        self.size = size
        self.prob = prob
        self.lost = False
        self.num_clicked = 0
        self.num_not_bombs = 0
        self.set_board()

    def set_board(self):
        self.board = []

        for row in range(self.size[0]):
            row = []
            for col in range(self.size[1]):
                has_bomb = random() < self.prob

                if not has_bomb:
                    self.num_not_bombs += 1

                piece = Piece(has_bomb)
                row += [piece]

            self.board += [row]
        self.set_neighbors()

    def getSize(self):
        return self.size

    def get_piece(self, position):
        return self.board[position[0]][position[1]]

    def set_neighbors(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                piece = self.get_piece([row, col])
                neighbors = self.get_neighbors([row, col])

                piece.set_neighbors(neighbors)

    def get_neighbors(self, position):
        neighbors = []

        for row in range(position[0] - 1, position[0] + 2):
            for col in range(position[1] - 1, position[1] + 2):
                out_of_bounds = row < 0 or row >= self.size[0] or col < 0 or col >= self.size[1]
                same = row == position[0] and col == position[1]

                if same or out_of_bounds:
                    continue

                neighbors += [self.get_piece([row, col])]

        return neighbors

    def handle_click(self, piece, flag):
        if piece.get_clicked() or (not flag and piece.get_flagged()):
            return
        if flag:
            piece.toggle_flag()
            return

        piece.click()

        if piece.get_has_bomb():
            self.lost = True
            return

        self.num_clicked += 1

        if piece.get_num_around() != 0:
            return

        for neighbor in piece.get_neighbors():
            if not neighbor.get_has_bomb() and not neighbor.get_clicked():
                self.handle_click(neighbor, False)

    def get_won(self):
        return self.num_not_bombs == self.num_clicked

    def get_lost(self):
        return self.lost
