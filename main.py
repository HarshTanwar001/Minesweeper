from board import Board
from game import Game

grid = [8, 8]
bomb_prob = 0.15

board = Board(grid, bomb_prob)
screen_size = [720, 720]

game = Game(board, screen_size)
game.run()
