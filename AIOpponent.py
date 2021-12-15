import random
import pygame
from board import *

'''
File: AIOpponent.py. Contains all the functions relating to the AI component of the connect 4 game
                     such as, the level of game difficulties and the scorig mechanism of the game.
'''

'''
Function: player_score_eval. Evaluates the score of the player in the current game state.
          The for loop will check the array to see the number of positions that are 
          numerically equally to the player and the number of empty spots. Each array
          represents either a center, row, column or diagonal componnents of the board. If
          any of the those components have 4 player pieces, then it means that a victory
          has occured and a score of +100 is given. A similar logic applies for 3 player pieces
          and 2 player pieces. 
Parameters:
    array: an array consisting of center, row, column or diagonal board positions. 
    player: numerical representation of the player in the game.
Return:
    total_points: total number of points scored by player from the current game state.
'''


def player_score_eval(array, player):
    total_points = 0
    count_player = 0
    count_empty = 0

    for position in range(len(array)):
        if array[position] == player:
            count_player += 1
        if array[position] == 0:
            count_empty += 1

    if count_player == 4:
        total_points += 100
    elif count_player == 3 and count_empty == 1:
        total_points += 10
    elif count_player == 2 and count_empty == 2:
        total_points += 5

    return total_points


'''
Function: opponent_score_eval. Evaluates the score of the opponent in the current game state.
          The for loop will check the array to see the number of positions that are 
          numerically equally to the opponent and the number of empty spots. Each array
          represents either a center, row, column or diagonal componnents of the board. If
          any of the those components have 3 opponent pieces and an empty spot, then the 
          player is in a bad game state b/c the opponent is close to winning. Thus, the
          current game state is bad for the player so the total_points scored by the opponent
          will represent a bad game state.
Parameters:
    array: an array consisting of center, row, column or diagonal board positions. 
    opponent: numerical representation of the opponent in the game.
Return:
    total_points: total number of points scored by opponent from the current game state.
'''


def opponent_score_eval(array, opponent):
    total_points = 0
    count_opponent = 0
    count_empty = 0

    for position in range(len(array)):
        if array[position] == opponent:
            count_opponent += 1
        if array[position] == 0:
            count_empty += 1

    if count_opponent == 3 and count_empty == 1:
        total_points += 90
    elif count_opponent == 2 and count_empty == 2:
        total_points += 10

    return total_points


'''
Function: score_evaluation. Helper function that evaluates the total score 
          gained from the player and opponent for a current game state. 
Parameters:
    array: an array consisting of center, row, column or diagonal board positions. 
    opponent: numerical representation of agents in the game.
Return:
    score: total points scored from the current game state based on the player and opponent positions.
'''


def score_evaluation(array, player):
    score = 0
    opponent = 2

    if player == 2:
        opponent = 1

    score += player_score_eval(array, player)
    score -= opponent_score_eval(array, opponent)

    return score


'''
Function: center_scoring. Helper function that evaluates the scoring for 
          center position in the board.
Parameters:
    board: the board state.
    player: numerical representation of agents in the game.
Return:
    result: points accumulated from examining the center positions of the board.
'''


def center_scoring(board, player):
    mboard = board.get_board()
    center_array = []
    for row in range(board.get_row_board()):
        center_array.append(mboard[row][(board.get_col_board() // 2)])

    result = (center_array.count(player) * 3)
    return result


'''
Function: row_scoring. Helper function that evaluates the number of points 
          accumulated from each row in the board.
Parameters:
    board: the board state.
    player: numerical representation of agents in the game.
Return:
    points: points accumulated from examining row positions of the board.
'''


def row_scoring(board, player):
    points = 0
    mboard = board.get_board()
    for row in range(board.get_row_board()):
        row_array = []
        for col in range(board.get_col_board()):
            row_array.append(mboard[row][col])
        for col in range(board.get_col_board() - 3):
            temp_array = []
            for col2 in range(col, col + 4):
                temp_array.append(row_array[col2])
            points += score_evaluation(temp_array, player)
    return points


'''
Function: diagonal_scoring. Helper function that evaluates the number of points 
          accumulated from each diagonal in the board.
Parameters:
    board: the board state.
    player: numerical representation of agents in the game.
Return:
    points: points accumulated from examining diagonal positions of the board.
'''


def diagonal_scoring(board, player):
    points = 0
    mboard = board.get_board()
    for row in range(board.get_row_board() - 3):
        for col in range(board.get_col_board() - 3):
            window = [mboard[row + i][col + i] for i in range(4)]
            points += score_evaluation(window, player)

    for row in range(board.get_row_board() - 3):
        for col in range(board.get_col_board() - 3):
            window = [mboard[row + 3 - i][col + i] for i in range(4)]
            points += score_evaluation(window, player)

    return points


'''
Function: column_scoring. Helper function that evaluates the number of points 
          accumulated from each column in the board.
Parameters:
    board: the board state.
    player: numerical representation of agents in the game.
Return:
    points: points accumulated from examining column positions of the board.
'''


def column_scoring(board, player):
    points = 0
    mboard = board.get_board()
    for col in range(board.get_col_board()):
        col_array = []
        for row in range(board.get_row_board()):
            col_array.append(mboard[row][col])
        for row in range(board.get_row_board() - 3):
            temp_array = []
            for row2 in range(row, row + 4):
                temp_array.append(col_array[row2])
            points += score_evaluation(temp_array, player)
    return points


'''
Function: scoring. Complete scoring in all directions for game state.
Parameters:
    board: the board state.
    player: numerical representation of agents in the game.
Return:
    total_points: points accumulated from examining all positions of the board.
'''


def scoring(board, player):
    total_points = 0
    total_points += column_scoring(board, player)
    total_points += row_scoring(board, player)
    total_points += center_scoring(board, player)
    total_points += diagonal_scoring(board, player)

    return total_points


'''
Function: easy. Easy level of the game. Trivial implementation of AI
          where a random column number (depending on the column size)
          is chosen as the spot where a connect 4 will be placed for 
          the AI agent.
Parameters: none.
Return:
    random_column: randomly selected column number.
'''


def easy():
    pygame.time.wait(700)
    random_column = random.randint(0, 6)
    return random_column


'''
Function: medium. Medium level of the game. Trivial implementation of AI
          where a single depth of the game is examined (a single piece is dropped 
          in every available column in the board state and the column that yields
          the best board state (state with the best points) will be returned)
Parameters: 
    board: board object.
Return:
    empty_col[index]: column that will yield the highest scoring board state.
'''


def medium(board):
    score = float('-inf')
    index = 0
    empty_col = board.empty_col()
    for i in range(len(empty_col)):
        copy = copy_board(board)
        copy.drop_piece(copy.open_row(
            empty_col[i]), empty_col[i], 2)
        points = scoring(copy, 2)
        if score < points:
            score = points
            index = i

    return empty_col[index]


'''
Function: hard. Hard level of the game. Minimax implementation of the game.
Parameters: 
    board: board object.
    ply: depth of tree exploration.
    max: boolean representation of the maximizer. (True = Maximizer)
Return:
    column: column position that will yield the next best step.
    score: score obtained from minimax traversal.
'''


def hard(board, ply, maximizer):
    valid_locations = board.empty_col()
    is_terminal = board.terminal_node()

    if ply == 0 or is_terminal:
        if is_terminal:
            if board.winning_move(1):
                return (None, float('-inf'))
            elif board.winning_move(2):
                return (None, float('inf'))
            else:
                return (None, 0)
        else:
            return (None, scoring(board, 2))

    if maximizer:
        score = float('-inf')
        column = 0
        for col in valid_locations:
            row = board.open_row(col)
            copy = copy_board(board)
            copy.drop_piece(row, col, 2)
            value = hard(copy, ply - 1, False)[1]
            if value > score:
                score = value
                column = col

        return column, score

    else:
        score = float('inf')
        column = 0
        for col in valid_locations:
            row = board.open_row(col)
            copy = copy_board(board)
            copy.drop_piece(row, col, 1)
            value = hard(copy, ply - 1, True)[1]
            if value < score:
                score = value
                column = col

        return column, score
