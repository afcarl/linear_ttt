from functools import partial
import random

def binary_naive_features():
    features = []
    for player in range(3):
        for row in range(3):
            for column in range(3):
                features.append(partial(binary_naive_feature, player, row, column))
    return features

def binary_naive_feature(player, row, column, state):
    return state[row][column] == player

def binary_horizontal_tiles():
    features = []
    for player in range(3):
        for row in range(3):
            features.append(partial(binary_horizontal_tile, player, row))
    return features

def binary_horizontal_tile(player, row, state):
    counts = [0,0,0]
    for column in range(3):
        counts[state[row][column]] += 1
    for i in range(3):
        if counts[player] < counts[i]:
            return False
    return True

def binary_verticle_tiles():
    features = []
    for player in range(3):
        for column in range(3):
            features.append(partial(binary_verticle_tile, player, column))
    return features

def binary_verticle_tile(player, column, state):
    counts = [0,0,0]
    for row in range(3):
        counts[state[row][column]] += 1
    for i in range(3):
        if counts[player] < counts[i]:
            return False
    return True

def binary_diagonal_tiles():
    features = []
    for player in range(3):
        features.append(partial(binary_generic_tile, player, [(0,0)]))
        features.append(partial(binary_generic_tile, player, [(1,0), (0,1)]))
        features.append(partial(binary_generic_tile, player, [(2,0), (1,1), (0,2)]))
        features.append(partial(binary_generic_tile, player, [(2,1), (1,2)]))
        features.append(partial(binary_generic_tile, player, [(2,2)]))
        features.append(partial(binary_generic_tile, player, [(0,2)]))
        features.append(partial(binary_generic_tile, player, [(0,1), (1,2)]))
        features.append(partial(binary_generic_tile, player, [(0,0), (1,1), (2,2)]))
        features.append(partial(binary_generic_tile, player, [(1,0), (2,1)]))
        features.append(partial(binary_generic_tile, player, [(2,0)]))
    return features
        
def binary_generic_tile(player, cells, state):
    counts = [0,0,0]
    for cell in cells:
        counts[state[cell[0]][cell[1]]] += 1
    for i in range(3):
        if counts[player] < counts[i]:
            return False
    return True

def binary_line_tiles():
    features = binary_diagonal_tiles()
    for f in binary_horizontal_tiles():
        features.append(f)
    for f in binary_verticle_tiles():
        features.append(f)
    return features

def binary_random_tiles(num_tiles):
    features = []
    for tile in range(num_tiles):
        height = random.randrange(1,4)
        width = random.randrange(1,4)
        x = random.randrange(3)
        y = random.randrange(3)
        cells = []
        for w in range(width):
            curx = x + w
            if curx > 2:
                break
            for h in range(height):
                cury = y + h
                if cury > 2:
                    break
                cells.append((curx, cury))
        for player in range(3):
            features.append(partial(binary_generic_tile, player, cells))
    return features

def binary_random_kanerva_features(num_features, threshold):
    features = []
    for f in range(num_features):
        points = random.randrange(threshold, 10)
        cells = random.sample([(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)], points)
        matches = zip(cells,[random.randrange(3) for _ in range(points)])
        features.append(partial(binary_kanerva_feature, matches, threshold))
    return features

def binary_kanerva_feature(matches, threshold, state):
    misses = 0
    for match in matches:
        if state[match[0][0]][match[0][1]] != match[1]:
            misses += 1
    return misses <= threshold


























