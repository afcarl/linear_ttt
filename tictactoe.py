"""
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
"""

import random
from copy import copy, deepcopy
import csv
import numpy as np
import matplotlib.pyplot as plt
from features import *
from math import sqrt

EMPTY = 0
PLAYER_X = 1
PLAYER_O = 2
DRAW = 3

BOARD_FORMAT = "----------------------------\n| {0} | {1} | {2} |\n|--------------------------|\n| {3} | {4} | {5} |\n|--------------------------|\n| {6} | {7} | {8} |\n----------------------------"
NAMES = [' ', 'X', 'O']
def printboard(state):
    cells = []
    for i in range(3):
        for j in range(3):
            cells.append(NAMES[state[i][j]].center(6))
    print BOARD_FORMAT.format(*cells)

def emptystate():
    return [[EMPTY,EMPTY,EMPTY],[EMPTY,EMPTY,EMPTY],[EMPTY,EMPTY,EMPTY]]

def gameover(state):
    for i in range(3):
        if state[i][0] != EMPTY and state[i][0] == state[i][1] and state[i][0] == state[i][2]:
            return state[i][0]
        if state[0][i] != EMPTY and state[0][i] == state[1][i] and state[0][i] == state[2][i]:
            return state[0][i]
    if state[0][0] != EMPTY and state[0][0] == state[1][1] and state[0][0] == state[2][2]:
        return state[0][0]
    if state[0][2] != EMPTY and state[0][2] == state[1][1] and state[0][2] == state[2][0]:
        return state[0][2]
    for i in range(3):
        for j in range(3):
            if state[i][j] == EMPTY:
                return EMPTY
    return DRAW

class LinearSarsaLambdaAgent(object):
    def __init__(self, player, features, weights, initial_alpha = 0.1, epsilon = 0.1, tdlambda = 0.9, verbose = False, lossval = -1, learning = True):
        self.player = player
        self.features = features
        self.weights = weights
        self.alpha = initial_alpha
        self.verbose = verbose
        self.lossval = lossval
        self.learning = learning
        self.epsilon = epsilon
        self.tdlambda = tdlambda
        self.prevstate = None
        self.prevscore = 0
        self.count = 0
        self.eligibility_traces = np.zeros(len(weights))

    def episode_over(self, winner):
        self.backup(self.winnerval(winner))
        self.prevstate = None
        self.prevscore = 0
        self.eligibility_traces = np.zeros(len(self.weights))
        self.count += 1.0
        #if self.learning:
        #    self.alpha = 1.0 / sqrt(self.count)

    def observe_reward(self, r):
        self.reward = r

    def action(self, state):
        r = random.random()
        if r < self.epsilon:
            move = self.random(state)
            self.log('>>>>>>> Exploratory action: ' + str(move))
        else:
            move = self.greedy(state)
            self.log('>>>>>>> Best action: ' + str(move))
        state[move[0]][move[1]] = self.player
        nextstate = self.statetuple(state)
        nextscore = self.lookup(state)
        state[move[0]][move[1]] = EMPTY
        if self.prevstate != None:
            self.backup(nextscore)
        self.prevstate = nextstate
        self.prevscore = nextscore
        self.replace_traces(self.prevstate)
        return move

    def random(self, state):
        available = []
        for i in range(3):
            for j in range(3):
                if state[i][j] == EMPTY:
                    available.append((i,j))
        return random.choice(available)

    def greedy(self, state):
        maxval = -50000
        maxmove = None
        if self.verbose:
            cells = []
        for i in range(3):
            for j in range(3):
                if state[i][j] == EMPTY:
                    # Consider playing this move
                    state[i][j] = self.player
                    # Lookup the afterstate's value
                    val = self.lookup(state)
                    # Set the state back to empty so we can consider other states
                    state[i][j] = EMPTY
                    # Is this the best move we've found so far?
                    if val > maxval or maxmove == None:
                        maxval = val
                        maxmove = (i, j)
                    if self.verbose:
                        cells.append('{0:.3f}'.format(val).center(6))
                elif self.verbose:
                    cells.append(NAMES[state[i][j]].center(6))
        if self.verbose:
            print BOARD_FORMAT.format(*cells)
        return maxmove

    def backup(self, nextval):
        if self.prevstate != None and self.learning:
            delta = self.reward - self.prevscore + nextval
            if self.verbose:
                print 'Old weights: {0}'.format(self.weights)
            m = float(sum([f(self.prevstate) for f in self.features]))
            self.weights += self.alpha / m * delta * self.eligibility_traces
            if self.verbose:
                print 'New weights: {0}'.format(self.weights)

    def replace_traces(self, state):
        for (i,f) in enumerate(self.features):
            if f(state):
                self.eligibility_traces[i] = 1
            else:
                self.eligibility_traces[i] *= self.tdlambda

    def lookup(self, state):
        return sum([x*y(state) for (x,y) in zip(self.weights, self.features)])

    def winnerval(self, winner):
        if winner == self.player:
            return 1
        elif winner == EMPTY:
            return 0.5
        elif winner == DRAW:
            return 0
        else:
            return self.lossval

    def statetuple(self, state):
        return (tuple(state[0]),tuple(state[1]),tuple(state[2]))

    def log(self, s):
        if self.verbose:
            print s

class RandomAgent(object):
    def __init__(self, player):
        self.player = player

    def action(self, state):
        available = []
        for i in range(3):
            for j in range(3):
                if state[i][j] == EMPTY:
                    available.append((i,j))
        return random.choice(available)

    def observe_reward(self, r):
        pass

    def episode_over(self, winner):
        pass

class Human(object):
    def __init__(self, player):
        self.player = player

    def action(self, state):
        printboard(state)
        action = raw_input('Your move? ')
        return (int(action.split(',')[0]),int(action.split(',')[1]))

    def episode_over(self, winner):
        if winner == DRAW:
            print 'Game over! It was a draw.'
        else:
            print 'Game over! Winner: Player {0}'.format(winner)

    def observe_reward(self, r):
        pass

def play(agent1, agent2):
    state = emptystate()
    for i in range(9):
        if i % 2 == 0:
            move = agent1.action(state)
        else:
            move = agent2.action(state)
        state[move[0]][move[1]] = (i % 2) + 1
        winner = gameover(state)
        if winner != EMPTY:
            agent1.episode_over(winner)
            agent2.episode_over(winner)
            return winner
        agent1.observe_reward(0)
        agent2.observe_reward(0)
    return winner

def measure_performance_vs_random(agent1, agent2):
    epsilon1 = agent1.epsilon
    epsilon2 = agent2.epsilon
    agent1.epsilon = 0
    agent2.epsilon = 0
    agent1.learning = False
    agent2.learning = False
    r1 = RandomAgent(1)
    r2 = RandomAgent(2)
    r1.epsilon = 1
    r2.epsilon = 1
    probs = [0,0,0,0,0,0]
    games = 100
    for i in range(games):
        winner = play(agent1, r2)
        if winner == PLAYER_X:
            probs[0] += 1.0 / games
        elif winner == PLAYER_O:
            probs[1] += 1.0 / games
        else:
            probs[2] += 1.0 / games
    for i in range(games):
        winner = play(r1, agent2)
        if winner == PLAYER_O:
            probs[3] += 1.0 / games
        elif winner == PLAYER_X:
            probs[4] += 1.0 / games
        else:
            probs[5] += 1.0 / games
    agent1.epsilon = epsilon1
    agent2.epsilon = epsilon2
    agent1.learning = True
    agent2.learning = True
    return probs

FEATURES = {
    'naive': binary_naive_features(),
    'horizontal tiles': binary_horizontal_tiles(),
    'verticle tiles': binary_verticle_tiles(),
    'diagonal tiles': binary_diagonal_tiles(),
    'all line tiles': binary_line_tiles(),
    'random 5 tiles': binary_random_tiles(5),
    'random 10 tiles': binary_random_tiles(10),
    'random 16 tiles': binary_random_tiles(16),
    'random 20 tiles': binary_random_tiles(20),
    'random 25 tiles': binary_random_tiles(25),
    'kanerva 15 features and 0 threshold': binary_random_kanerva_features(15,0),
    'kanerva 30 features and 0 threshold': binary_random_kanerva_features(30,0),
    'kanerva 45 features and 0 threshold': binary_random_kanerva_features(45,0),
    'kanerva 60 features and 0 threshold': binary_random_kanerva_features(60,0),
    'kanerva 75 features and 0 threshold': binary_random_kanerva_features(75,0),
    'kanerva 15 features and 1 threshold': binary_random_kanerva_features(15,1),
    'kanerva 30 features and 1 threshold': binary_random_kanerva_features(30,1),
    'kanerva 45 features and 1 threshold': binary_random_kanerva_features(45,1),
    'kanerva 60 features and 1 threshold': binary_random_kanerva_features(60,1),
    'kanerva 75 features and 1 threshold': binary_random_kanerva_features(75,1),
    'kanerva 15 features and 2 threshold': binary_random_kanerva_features(15,2),
    'kanerva 30 features and 2 threshold': binary_random_kanerva_features(30,2),
    'kanerva 45 features and 2 threshold': binary_random_kanerva_features(45,2),
    'kanerva 60 features and 2 threshold': binary_random_kanerva_features(60,2),
    'kanerva 75 features and 2 threshold': binary_random_kanerva_features(75,2),
    'kanerva 15 features and 3 threshold': binary_random_kanerva_features(15,3),
    'kanerva 30 features and 3 threshold': binary_random_kanerva_features(30,3),
    'kanerva 45 features and 3 threshold': binary_random_kanerva_features(45,3),
    'kanerva 60 features and 3 threshold': binary_random_kanerva_features(60,3),
    'kanerva 75 features and 3 threshold': binary_random_kanerva_features(75,3),
}


if __name__ == "__main__":
    experiment_name = 'all line tiles'
    features1 = FEATURES[experiment_name]
    features2 = FEATURES[experiment_name]
    weights1 = np.zeros(len(features1))
    weights2 = np.zeros(len(features2))
    p1 = LinearSarsaLambdaAgent(1, features1, weights1)
    p2 = LinearSarsaLambdaAgent(2, features2, weights2)
    r1 = RandomAgent(1)
    r2 = RandomAgent(2)
    series = ['P1-Win','P1-Lose','P1-Draw','P2-Win','P2-Lose','P2-Draw']
    #series = ['P1-Win', 'P2-Win', 'Draw']
    colors = ['r','b','g','c','m','b']
    markers = ['+', '.', 'o', '*', '^', 's']
    f = open('{0}_results.csv'.format(experiment_name.replace(' ', '_')), 'wb')
    writer = csv.writer(f)    
    writer.writerow(series)
    perf = [[] for _ in range(len(series) + 1)]
    for i in range(1000):
        if i % 10 == 0:
            print 'Game: {0}'.format(i)
            probs = measure_performance_vs_random(p1, p2)
            writer.writerow(probs)
            f.flush()
            perf[0].append(i)
            for idx,x in enumerate(probs):
                perf[idx+1].append(x)
        winner = play(p1,r2)
        p1.episode_over(winner)
        winner = play(r1,p2)
        p2.episode_over(winner)
    f.close()
    for i in range(1,len(perf)):
        plt.plot(perf[0], perf[i], label=series[i-1], color=colors[i-1])
    plt.xlabel('Episodes')
    plt.ylabel('Probability')
    plt.ylim([0,1])
    plt.title('RL Agent Performance vs. Random Agent\n({0})'.format(experiment_name))
    plt.legend()
    plt.savefig('{0}.png'.format(experiment_name.replace(' ', '_')))