Linear Tic-Tac-Toe
==================

A framework for experimenting with different linear function approximators with gradient-descent Sarsa(lambda)
following an epsilon-greedy policy in Tic-Tac-Toe. Each experiment is learning the optimal move vs. a random
agent, where afterstates are used instead of Q values. This is an undiscounted (gamma = 1) episodic task.

The methods covered are as follows:

- Naive coding
    - 1 ternary feature per cell, values (-1, 0, 1) for (opp, empty, self)
    - 3 binary features per cell, one feature for each possible value of (opp, empty, self)

- Tile coding: Maximum of [X, O, Empty] in a tile
    - Horizontal (3 features)
    - Verticle (3 features)
    - diagonal (10 features)
    - All 3 (16 features)
    - NxM overlapping tiles
        - Each tile is parameterized by (min_x, min_y, width, height)
        - Feature counts explored: 5, 10, 16, 20, 25 
        - Discovery methods:
            - Randomly generated
            - Evolved
    
- Kanerva coding [Each base feature is a board state with 9 ternary features]
    - Hamming distance is the number of base features matched exactly
    - Distance thresholds explore: 0, 1, 2, 3
    - Feature  counts explored: 5, 10, 16, 20, 25
    - Kanerva feature discovery:
        - Randomly generated
        - Evolved

Created by Wesley Tansey
2/10/2013
Released under the MIT license.
