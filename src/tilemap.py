import json
import math
import random
import time

import pygame

SURROUND_POS = [
    [-1, 0],
    [0, 0],
    [1, 0],
    [-1, -1],
    [0, -1],
    [1, -1],
    [-1, 1],
    [0, 1],
    [1, 1],
]

SURROUND_POS = []
for p in [[[x - 2, y - 2] for x in range(5)] for y in range(5)]:
    SURROUND_POS += p

add_index = 0

def tuple_to_str(tp):
    return ';'.join([str(v) for v in tp])

def str_to_tuple(s):
    return tuple([int(v) for v in s.split(';')])
