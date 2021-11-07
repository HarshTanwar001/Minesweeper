import os
import pygame


class Game:

    def __init__(self, board, screen_size):
        self.board = board
        self.screen_size = screen_size
        self.piece_size = self.screen_size[0] / self.board.getSize()[1], self.screen_size[1] / self.board.getSize()[0]
        self.load_images()

    def run(self):
        pygame.init()
        pygame.display.set_caption("Minesweeper")
        self.screen = pygame.display.set_mode(self.screen_size)
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    right_click = pygame.mouse.get_pressed()[2]
                    self.handle_click(position, right_click)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for row in range(self.board.size[0]):
                            for col in range(self.board.size[1]):
                                piece = self.board.get_piece([row, col])
                                piece.click()
            self.draw()
            pygame.display.flip()

            if self.board.get_won():
                print("\nYou Won!")
                running = False

        pygame.quit()

    def draw(self):
        top_left = [0, 0]

        for row in range(self.board.getSize()[0]):
            for col in range(self.board.getSize()[1]):
                piece = self.board.get_piece([row, col])
                image = self.get_image(piece)
                self.screen.blit(image, top_left)
                top_left = top_left[0] + self.piece_size[0], top_left[1]

            top_left = 0, top_left[1] + self.piece_size[1]

    def load_images(self):
        self.images = {}

        for file in os.listdir("Images"):
            if not file.endswith(".png"):
                continue

            image = pygame.image.load("images/" + file)
            image = pygame.transform.scale(image, self.piece_size)
            self.images[file.split(".")[0]] = image

    def get_image(self, piece):
        name = None

        if piece.get_clicked():
            name = "bomb-at-clicked-block" if piece.get_has_bomb() else str(piece.get_num_around())
        else:
            name = "flag" if piece.get_flagged() else "empty-block"

        return self.images[name]

    def handle_click(self, position, right_click):
        if self.board.get_lost():
            return

        pos = position[1] // self.piece_size[1], position[0] // self.piece_size[0]
        piece = self.board.get_piece(pos)
        self.board.handle_click(piece, right_click)
