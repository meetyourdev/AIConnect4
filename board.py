import numpy as np

'''
Board Class: Used to create connect 4 board object. This class contains methods
             that can be used to retrieve certain attributes of the board object
             as well as methods to check the state of the board (i.e. empty column
             or row positions and checks if victories have occured or not in the game).
'''


class Board:

    '''
    Method: Board Constructor. Consists of row and column size,
            2D matrix of board, player and AI numerical representation. 
    Parameters: 
        row_board: number of rows for connect 4 board. Default is a row of size 6.
        col_board: number of columns for connect 4 board. Default is a row of size 7.
    Return: none
    '''

    def __init__(self, row_board=6, col_board=7):
        self.row_board = row_board
        self.col_board = col_board
        self.board = [[0 for i in range(col_board)] for j in range(row_board)]
        self.player_piece = 1
        self.AI_piece = 2

    '''
    Method: get_row_board
    Parameters: none
    Return: row size
    '''

    def get_row_board(self):
        return self.row_board

    '''
    Method: col_row_board
    Parameters: none
    Return: column size
    '''

    def get_col_board(self):
        return self.col_board

    '''
    Method: get_board
    Parameters: none
    Return: board 2D matrix
    '''

    def get_board(self):
        return self.board

    '''
    Method: get_player_piece
    Parameters: none
    Return: numerical representatio of player piece
    '''

    def get_player_piece(self):
        return self.player_piece

    '''
    Method: get_AI_piece
    Parameters: none
    Return: numerical representatio of AI piece
    '''

    def get_AI_piece(self):
        return self.AI_piece

    '''
    Method: print_board. Prints the 2D matrix array board in the 
            correct orientation. 2D matrix needs to be flipped
            vertically in order to properly represent the connect 4 board.
    Parameters: none
    Return: none
    '''

    def print_board(self):
        new_board = []
        for row in range(self.row_board-1, -1, -1):
            print(self.board[row])

    '''
    Method: drop_piece. Drops the player (1) or AI (2) numerical representation
            into the 2D matrix of the board.
    Parameters: none
    Return: none
    '''

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    '''
    Method: open_row. Returns the empty row position for a specific
            column in the 2D matrix board.
    Parameters:
        col: column of the board.
    Return: 
        row: empty row in the specified paramter column.
    '''

    def open_row(self, col):
        for row in range(self.row_board):
            if self.board[row][col] == 0:
                return row

    '''
    Method: valid_move. Checks if a column still contains empty empty rows.
    Parameters:
        col: column of the board.
    Return: 
        True: if the column is not completely empty.
        False: if the column is full.
    '''

    def valid_move(self, col):
        if (self.board[self.row_board - 1][col] == 0):
            return True
        else:
            return False

    '''
    Method: empty_col. Appends all columns that are not completely fill
            into a list.
    Parameters: none
    Return: 
        empty_col: list of empty columns (i.e. [0, 3, 4, 5]).
    '''

    def empty_col(self):
        empty_col = []
        for column in range(self.col_board):
            if self.valid_move(column) == True:
                empty_col.append(column)
        return empty_col

    '''
    Method: horiztonal_win. Only need to check a certain number of columns
            to identify a horizontal victory. Example: checking row 3, we 
            only need to check from col 0 to 3, col 1 to 4, col 2 to 5 and
            col 3 to 6.
    Parameters:
        piece: numerical representation of the player or AI piece.
    Return:
        True: if a horizontal win (4 pieces horizontally) exists on the board.
        None: if a horizontal win does not exist.
    '''

    def horizontal_win(self, piece):
        for col in range(self.col_board - 3):
            for row in range(self.row_board):
                if self.board[row][col] == piece and self.board[row][col + 1] == piece and self.board[row][col + 2] == piece and self.board[row][
                        col + 3] == piece:
                    return True

    '''
    Method: vertical_win. Only need to check a certain number of rows
            to identify a horizontal victory. Example: checking col 3, we 
            only need to check from row 0 to 3, row 1 to 4, and row 2 to 5. 
    Parameters:
        piece: numerical representation of the player or AI piece.
    Return:
        True: if a vertical win (4 pieces vertically) exists on the board.
        None: if a vertical win does not exist.
    '''

    def vertical_win(self, piece):
        for col in range(self.col_board):
            for row in range(self.row_board - 3):
                if self.board[row][col] == piece and self.board[row + 1][col] == piece and self.board[row + 2][col] == piece and self.board[row + 3][
                        col] == piece:
                    return True

    '''
    Method: diagonal_win. Checks both positive and negative sloped diagonals.
    Parameters:
        piece: numerical representation of the player or AI piece.
    Return:
        True: if a diagonal win (4 pieces diagonally) exists on the board.
        None: if a diagonal win does not exist.
    '''

    def diagonal_win(self, piece):
        for col in range(self.col_board - 3):
            for row in range(self.row_board - 3):
                if self.board[row][col] == piece and self.board[row + 1][col + 1] == piece and self.board[row + 2][col + 2] == piece and self.board[row + 3][
                        col + 3] == piece:
                    return True

        for col in range(self.col_board - 3):
            for row in range(3, self.row_board):
                if self.board[row][col] == piece and self.board[row - 1][col + 1] == piece and self.board[row - 2][col + 2] == piece and self.board[row - 3][
                        col + 3] == piece:
                    return True

    '''
    Method: winning_move. The board is checked to see if a horizontal, vertical or diagonal win
            exists for a certain piece. 
    Parameters:
        piece: numerical representation of the player or AI piece.
    Return:
        True: one of the three types of wins exists for a certain piece on the board.
        False: no victory currently exists for a certain piece on the board.
    '''

    def winning_move(self, piece):
        return self.horizontal_win(piece) or self.vertical_win(piece) or self.diagonal_win(piece)

    '''
    Method: terminal_node. 
    Parameters: none
    Return:
        True: if a winning board exists or if the board is tied where the board is completely filled
              with not winners.
        False: if there are not winners or if the board still has positions that are still empty.
    '''

    def terminal_node(self):
        return len(self.empty_col()) == 0 or self.winning_move(1) or self.winning_move(2)


'''
Function: copy_board. Creates a new instance of the board object where the
          board matrix is the same as the board that needs to be copied.
Parameters:
    board: 2D matrix of the board that needs to be copied.
Return:
    new_board: new board object, which is the copied version of the board parameter.
'''


def copy_board(board):
    new_board = Board(board.get_row_board(), board.get_col_board())

    for row in range(board.get_row_board()):
        for col in range(board.get_col_board()):
            (new_board.get_board())[row][col] = (
                board.get_board())[row][col]

    return new_board
