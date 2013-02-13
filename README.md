Linear Tic-Tac-Toe
==================

A framework for experimenting with different linear function approximators with gradient-descent Sarsa(lambda)
following an epsilon-greedy policy in Tic-Tac-Toe. Each experiment is learning the optimal move vs. a random
agent, where afterstates are used instead of Q values. This is an undiscounted (gamma = 1) episodic task.

The methods covered are as follows:

- Naive coding
    - 3 binary features per cell, one feature for each possible value of (opp, empty, self)

- Tile coding: Maximum of [X, O, Empty] in a tile
    - Horizontal (3 tiles, 9 features)
    - Vertical (3 tiles, 9 features)
    - diagonal (10 tiles, 30 features)
    - All 3 (16 tiles, 48 features)
    - NxM overlapping tiles
        - Each tile is parameterized by (min_x, min_y, width, height)
        - Tile counts explored: 5, 10, 16, 20, 25, 30, 50
        - Randomly generated
    
- Kanerva coding [Each base feature is a board state with 9 ternary features]
    - Hamming distance is the number of base features matched exactly
    - Distance thresholds explore: 0, 1, 2, 3
    - Feature  counts explored: 15, 30, 45, 60, 75, 100
    - Randomly generated

Created by Wesley Tansey
2/10/2013
Released under the MIT license.
