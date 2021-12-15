# IMPORT GAME AND CLASSES
import pygame
import sys
import math
from pygame.constants import MOUSEBUTTONDOWN
from board import *
from GUI import *
from AIOpponent import *
import asyncio
from time import sleep

# GESTURES IMPORT
import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model


async def main_game():
    # command line arguments
    arg = sys.argv[1]
    if arg == "--easy":
        level = "easy"
    elif arg == "--medium":
        level = "medium"
    elif arg == "--hard":
        level = "hard"

    # initialize board and game
    board = Board()
    game_state = False
    switch_players = 1
    size = ((board.get_col_board() * 100), (board.get_row_board() + 1) * 100)
    screen = pygame.display.set_mode(size)

    pygame.init()

    # initialize color for game board
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (124, 252, 0)

    connect = Connect4GUI(100, board.get_col_board() * 100,
                          (board.get_row_board() + 1) * 100, WHITE, BLUE, RED, GREEN, board)
    connect.draw_game()

    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 125)
    pygame.display.update()

    # initialize mediapipe
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mpDraw = mp.solutions.drawing_utils

    # Load the gesture recognizer model
    model = load_model('mp_hand_gesture')

    # Load class names
    f = open('gesture.names', 'r')
    classNames = f.read().split('\n')
    f.close()
    # print(classNames)

    # Initializing Disc
    posx = (board.get_col_board() * 100) / 2
    pygame.draw.rect(screen, WHITE, (0, 0, (board.get_col_board() * 100), 100))
    pygame.draw.circle(screen, RED, (posx, int(100 / 2)), (int(100 / 2 - 5)))

    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    while not game_state:
        # Read each frame from the webcam
        _, frame = cap.read()
        x, y, c = frame.shape

        # Flip the frame vertically
        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get hand landmark prediction
        result = hands.process(framergb)
        className = ''
        # post process the result
        if result.multi_hand_landmarks:
            landmarks = []
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    # print(id, lm)
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)

                    landmarks.append([lmx, lmy])

                # Drawing landmarks on frames
                mpDraw.draw_landmarks(
                    frame, handslms, mpHands.HAND_CONNECTIONS)

                # Predict gesture
                prediction = model.predict([landmarks])
                # print(prediction)
                classID = np.argmax(prediction)
                className = classNames[classID]

        # show the prediction on the frame
        cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 2, cv2.LINE_AA)

        # Coin goes right
        if className == "peace":
            pygame.draw.rect(
                screen, WHITE, (0, 0, (board.get_col_board() * 100), 100))
            if(posx < (board.get_col_board() * 100)-(100/2)):
                posx += 10
            if switch_players == 0:
                pygame.draw.circle(
                    screen, RED, (posx, int(100 / 2)), (int(100 / 2 - 5)))

        # Coin goes left
        if className == "okay":
            pygame.draw.rect(
                screen, WHITE, (0, 0, (board.get_col_board() * 100), 100))
            if(posx > 100/2):
                posx -= 10
            if switch_players == 0:
                pygame.draw.circle(
                    screen, RED, (posx, int(100 / 2)), (int(100 / 2 - 5)))

        # Coin Drops
        if className == "thumbs down":
            await asyncio.sleep(1)
            pygame.draw.rect(
                screen, WHITE, (0, 0, (board.get_col_board() * 100), 100))
            if switch_players == 0:
                col = int(math.floor(posx / 100))
                if board.valid_move(col):
                    row = board.open_row(col)
                    board.drop_piece(row, col, 1)
                    if board.winning_move(1):
                        label = myfont.render("Red wins!!", 1, RED)
                        screen.blit(label, (130, 20))
                        game_state = True
                connect = Connect4GUI(100, board.get_col_board() * 100,
                                      (board.get_row_board() + 1) * 100, WHITE, BLUE, RED, GREEN, board)
                connect.draw_game()

                switch_players = 1
                await asyncio.sleep(1)

        pygame.display.update()
        #  Ask for Player 2 Input
        if switch_players == 1 and not game_state:

            # difficulty levels
            if level == "easy":
                col = easy()
            elif level == "medium":
                col = medium(board)
            elif level == "hard":
                col, score = hard(board, 4, True)

            if board.valid_move(col):
                row = board.open_row(col)
                board.drop_piece(row, col, 2)
                if board.winning_move(2):
                    label = myfont.render("Green wins!!", 1, GREEN)
                    screen.blit(label, (130, 20))
                    game_state = True
                    connect = Connect4GUI(100, board.get_col_board() * 100,
                                          (board.get_row_board() + 1) * 100, WHITE, BLUE, RED, GREEN, board)
                    connect.draw_game()

                # Showing disc for the user to play
                pygame.draw.circle(
                    screen, RED, (posx, int(100 / 2)), (int(100 / 2 - 5)))

                switch_players = 0

        if game_state:
            pygame.time.wait(5000)

        # Show the final output
        cv2.imshow("Output", frame)

        if cv2.waitKey(1) == ord('q'):
            break

    # release the webcam and destroy all active windows
    cap.release()

    cv2.destroyAllWindows()

asyncio.run(main_game())
