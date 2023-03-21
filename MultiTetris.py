from random import randrange as rand
import pygame, sys
import atexit
import subprocess

config = {
    'cell_size':    40,
    'cols':         8,
    'rows':         16,
    'delay':        750,
    'maxfps':       30
}

colors = [
    (0,   0,   0  ),
    (255, 0,   0  ),
    (0,   150, 0  ),
    (0,   0,   255),
    (255, 120, 0  ),
    (255, 255, 0  ),
    (180, 0,   255),
    (0,   220, 220)
]

tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],
    
    [[0, 2, 2],
     [2, 2, 0]],
    
    [[3, 3, 0],
     [0, 3, 3]],
    
    [[4, 0, 0],
     [4, 4, 4]],
    
    [[0, 0, 5],
     [5, 5, 5]],
    
    [[6, 6, 6, 6]],
    
    [[7, 7],
     [7, 7]]
]

def rotate_clockwise(shape):
    return [ [ shape[y][x]
            for y in range(len(shape)) ]
        for x in range(len(shape[0]) - 1, -1, -1) ]

def check_collision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[ cy + off_y ][ cx + off_x ]:
                    return True
            except IndexError:
                return True
    return False

def remove_row(board, row):
    del board[row]
    return [[0 for i in range(config['cols'])]] + board
    
def join_matrixes(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat1[cy+off_y-1   ][cx+off_x] += val
    return mat1

def new_board():
    board = [ [ 0 for x in range(config['cols']) ]
            for y in range(config['rows']) ]
    board += [[ 1 for x in range(config['cols'])]]
    return board

class TetrisGame(object):
    def __init__(self, player):
        self.player = player
        self.board = new_board()
        self.new_stone()
        self.gameover = False
        self.paused = False
        self.score = 0
        self.lines = 0
        self.level = 1
        self.total_lines_cleared = 0
        self.fall_speed = config['delay']
        self.drop_bonus = False
        self.quit_game = False
    
    def new_stone(self):
        self.stone = tetris_shapes[rand(len(tetris_shapes))]
        self.stone_x = int(config['cols'] / 2 - len(self.stone[0])/2)
        self.stone_y = 0

        if check_collision(self.board,
                            self.stone,
                            (self.stone_x, self.stone_y)):
            self.gameover = True