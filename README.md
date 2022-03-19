# AIConnect4

Connect Four is a two-player connection board game, in which the players choose a color and then take turns dropping colored tokens
into a seven-column, six-row vertically suspended grid. The pieces fall straight down, occupying the lowest available space within 
the column. The objective of the game is to be the first to form a horizontal, vertical, or diagonal line of four of one's own tokens.

This project allows user to play Connect 4 using hand and finger gestures. 

This project integrates media pipe library provides high-fidelity hand and finger tracking. It employs machine learning (ML) to infer 
21 3D landmarks of a hand from just a single frame. Open CV library is used to capture hand movements and fed to Tensflow's pre-trained 
model to indentify gestures.

