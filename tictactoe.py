import pygame
from random import randint

pygame.init()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
# End colors

size = [600, 600]

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tic Tac Toe")

done = False
playerTurn = True


class Board():

    def __init__(self, screen):
        self.screen = screen
        self.reset()
        self.winCombination = lambda: (self.grid[0:3],
                                       self.grid[3:6],
                                       self.grid[6:9],
                                       self.grid[0:7:3],
                                       self.grid[1:8:3],
                                       self.grid[2:9:3],
                                       self.grid[0:9:4],
                                       self.grid[2:7:2])
        self.victoryFont = pygame.font.Font(None, 50)

    def reset(self):
        self.grid = [''] * 9
        self.squares = [self.screen.fill(white, (x, y, 200, 200)).inflate(-25, -25)
                        for x in 0, 201, 402 for y in 0, 201, 402]
        pygame.display.flip()

    def _index(self, row, column):
        return row * 3 + column

    def checkEmpty(self, index):
        return self.grid[index] == ''

    def draw_x(self, row, column, color):
        index = self._index(row, column)
        if self.checkEmpty(index):
            pygame.draw.line(screen,
                             color,
                             self.squares[index].topright,
                             self.squares[index].bottomleft,
                             10)
            pygame.display.update(pygame.draw.line(screen, color,
                                  self.squares[index].topleft,
                                  self.squares[index].bottomright,
                                  10))
            self.grid[self._index(row, column)] = 'X'
            return True
        return False

    def draw_o(self, row, column, color):
        index = self._index(row, column)
        if self.checkEmpty(index):
            pygame.display.update(pygame.draw.ellipse(screen,
                                  color,
                                  self.squares[index],
                                  10))
            self.grid[self._index(row, column)] = 'O'
            return True
        return False

    def checkWin(self, char):
        for c in self.winCombination():
            if [char] * 3 == c:
                return True
        return False

    def showVictory(self, message):
        text = self.victoryFont.render(message,
                                       1,
                                       (0, 0, 0),
                                       (240, 240, 255))
        rect = text.get_rect()
        rect.center = 300, 300
        pygame.display.update(self.screen.blit(text, rect))


class Player():

    def __init__(self, board, color):
        self.board = board
        self.color = color
        self.char = 'X'

    def move(self, mouse):
        row = int(mouse[0] / 200)
        column = int(mouse[1] / 200)
        return self.board.draw_x(row, column, self.color)

    def checkWon(self):
        return self.board.checkWin(self.char)

    def victory(self):
        self.board.showVictory("Player won!")


class Computer():
    def __init__(self, board, color):
        self.board = board
        self.color = color
        self.char = 'O'

    def move(self):
        while not self.board.draw_o(randint(0, 2),
                                    randint(0, 2),
                                    self.color):
            pass
        return

    def checkWon(self):
        return self.board.checkWin(self.char)

    def victory(self):
        self.board.showVictory("Computer won!")


screen = pygame.display.set_mode(size)
pygame.font.init()
board = Board(screen)
p = Player(board, blue)
ai = Computer(board, red)
won = False
while not done:
    # input
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        done = True
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if won:
            won = False
            board.reset()
        else:
            mouse = pygame.mouse.get_pos()
            if p.move(mouse):
                if p.checkWon():
                    p.victory()
                    won = True
                else:
                    ai.move()
                    if ai.checkWon():
                        ai.victory()
                        won = True
            else:
                print "invalid move"
    # logic

pygame.quit()
