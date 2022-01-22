import pygame
import random

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

s_width = 800
s_height = 700
play_width = 300
play_height = 600
block_size = 20

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height - 50


shape = [
    [[".....",
      ".....",
      ".000.",
      ".000.",
      "....."],

     [".....",
      "..00.",
      "..00.",
      "..00.",
      "....."]],

    [[".....",
      ".....",
      ".00..",
      "..0..",
      "....."],

     [".....",
      ".....",
      "..0..",
      ".00..",
      "....."],

     [".....",
      ".....",
      ".0...",
      ".00..",
      "....."],

     [".....",
      ".....",
      ".00..",
      ".0...",
      "....."]],

    [[".....",
      ".....",
      "..00.",
      "..0..",
      "....."],

     [".....",
      ".....",
      "..00.",
      "...0.",
      "....."],

     [".....",
      ".....",
      "...0.",
      "..00.",
      "....."],

     [".....",
      ".....",
      "..0..",
      "..00.",
      "....."],

     ],

    [	["..0..",
           "..0..",
           "..0..",
           "..0..",
           "....."],
          [".....",
           "0000.",
           ".....",
           ".....",
           "....."]],

    [	 [".....",
           "..0..",
           "..0..",
           "..0..",
           "....."],
          [".....",
           ".000.",
           ".....",
           ".....",
           "....."]],

    [	 [".....",
           ".00..",
           ".00..",
           "....."]],

    [	 [".....",
           ".....",
           "..00.",
           ".....",
           "....."],
          [".....",
           "...0.",
           "...0.",
           ".....",
           "....."],
          ],
    [[".....",
      ".0...",
      ".000.",
      ".....",
      "....."],
     [".....",
      "..00.",
      "..0..",
      "..0..",
      "....."],
     [".....",
      ".....",
      ".000.",
      "...0.",
      "....."],
     [".....",
      "..0..",
      "..0..",
      ".00..",
      "....."]],

    [[".....",
      "...0.",
      ".000.",
      ".....",
      "....."],
     [".....",
      "..0..",
      "..0..",
      "..00.",
      "....."],
     [".....",
      ".....",
      ".000.",
      ".0...",
      "....."],
     [".....",
      ".00..",
      "..0..",
      "..0..",
      "....."]],

    [[".....",
      "..0..",
      ".000.",
      "..0..",
      "....."]],

    [[".....",
      "..0..",
      ".000.",
      ".....",
      "....."],
     [".....",
      "..0..",
      "..00.",
      "..0..",
      "....."],
     [".....",
      ".....",
      ".000.",
      "..0..",
      "....."],
     [".....",
      "..0..",
      ".00..",
      "..0..",
      "....."]]
]

shapes = [x for x in shape]

class Piece(object):
    rows = 20
    columns = 10
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = (129 ,200 ,128)
        self.rotation = 0


def create_grid(locked_positions={}):
    grid = [[(0 ,0 ,0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j ,i) in locked_positions:
                c = locked_positions[(j ,i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0 ,0 ,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():
    global shapes, shape_colors

    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label,
    (top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))


def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * 30),
                         (sx + play_width, sy + i * 30))
        for j in range(col):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * 30, sy),
                             (sx + j * 30, sy + play_height))


def clear_rows(grid, locked):

    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
