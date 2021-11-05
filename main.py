from board import Board
from game import Game

size = [8, 8]
bomb_prob = 0.15

board = Board(size, bomb_prob)
screen_size = [800, 800]

game = Game(board, screen_size)
game.run()
