from board import *
import pygame

'''
Connect4GUI Class: Connect4GUI object is created to store all components needed to render 
                   a connect 4 board game using pygame. The board is created mainly using
                   rectangles and circles. The background and board structure is created first
                   and the pieces are created afterwards. This class contains all the methods
                   needed to create a connect 4 board using pygame.
'''


class Connect4GUI:

    '''
    Method: Connec4GUI constructor. Used to create a Connect4GUI object.
    Parameters:
        pixel_square_size: the pixel size. 
        width: width of the GUI board.
        height: height of the GUI board.
        background_color: background color of the game.
        board_color: color of the connect 4 board.
        P1_color: color of player 1.
        P2_color: color of player 2.
        board: board object.
    Return: none
    '''

    def __init__(self, pixel_square_size, width, height, background_color, board_color, P1_color, P2_color, board):
        self.pixel_square_size = pixel_square_size
        self.width = width
        self.height = height
        self.size = (width, height)
        self.radius = int(self.pixel_square_size / 2 - 5)
        self.board = board
        self.background_color = background_color
        self.board_color = board_color
        self.P1_color = P1_color
        self.P2_color = P2_color

    '''
    Method: get_size. Getter for size attribute.
    Parameters: none.
    Return: size attribute.
    '''

    def get_size(self):
        return self.size

    '''
    Method: get_radius. Getter for radius attribute.
    Parameters: none.
    Return: radius attribute.
    '''

    def get_radius(self):
        return self.radius

    '''
    Method: draw_pieces. Helper method that draws the circular connect 4 pieces.
    Parameters: none.
    Return: none.
    '''

    def draw_pieces(self):
        screen = pygame.display.set_mode(self.size)
        for col in range(self.board.get_col_board()):
            for row in range(self.board.get_row_board()):
                if (self.board.get_board())[row][col] == 1:
                    pygame.draw.circle(screen, self.P1_color, (
                        int(col * self.pixel_square_size + self.pixel_square_size / 2), self.height - int(row * self.pixel_square_size + self.pixel_square_size / 2)), self.radius)
                elif (self.board.get_board())[row][col] == 2:
                    pygame.draw.circle(screen, self.P2_color, (
                        int(col * self.pixel_square_size + self.pixel_square_size / 2), self.height - int(row * self.pixel_square_size + self.pixel_square_size / 2)), self.radius)

    '''
    Method: draw_background_board. Helper method that draws the background and board of the game.
    Parameters: none.
    Return: none.
    '''

    def draw_background_board(self):
        screen = pygame.display.set_mode(self.size)
        for col in range(self.board.get_col_board()):
            for row in range(self.board.get_row_board()):
                pygame.draw.rect(screen, self.board_color, (col * self.pixel_square_size, row *
                                                            self.pixel_square_size + self.pixel_square_size, self.pixel_square_size, self.pixel_square_size))
                pygame.draw.circle(screen, self.background_color, (
                    int(col * self.pixel_square_size + self.pixel_square_size / 2), int(row * self.pixel_square_size + self.pixel_square_size + self.pixel_square_size / 2)), self.radius)

    '''
    Method: draw_game. Draws all components of the connect 4 game.
    Parameters: none.
    Return: none.
    '''

    def draw_game(self):
        screen = pygame.display.set_mode(self.size)
        self.draw_background_board()
        self.draw_pieces()
        pygame.display.update()
