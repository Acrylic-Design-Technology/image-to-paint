from __future__ import print_function
from collections.abc import Sequence
import os
from PIL import Image, ImageFilter, ImageOps, ImageChops
import random, pygame, sys, math, colorsys
import argparse
import os
import numpy as np
from PIL import ImageColor

os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()

# a stroke object contains a color, color number, brush radius, brush number & move list
class Stroke():
    def __init__(self, color, radius):
        self.color = color
        self.radius = radius
        self.move_list = []
        self.color_number = 0
        self.brush_number = 0

    def addPoint(self, point):
        assert(len(point) == 2)
        self.move_list.append(point)

#Image class containing pil image object, image pixel access object and methods.
class MyImage():
    def __init__(self, image):
        self.image = image
        self.array = image.load()
        (self.width, self.height) = image.size

    def save(self, name):
        self.image.save(name)

    def getSize(self):
        return self.image.size

def draw_strokes(strokes, window, width, height):
    """ Take the strokes and write them to the pygame canvas and gcode file.
    """
    f = open('strokes_gcode.txt', 'w+')
    f.write('T1'+'\rF'+'600'+'.\r')

    xScale = 46.0 / width
    yScale = 46.0 / height

    for stroke in strokes:
        f.write('G1 Z.200\n')
        # MOVE TO COLOR COORDINATES
        f.write('G1 X'+ str(stroke.move_list[0][0]*xScale)[:6]+ \
                ' Y'+ str(stroke.move_list[0][1]*yScale)[:6]+'\r')
        f.write('G1 Z.00\n')

        for p in range(1, len(stroke.move_list)):
            f.write('G1 X'+ str(stroke.move_list[p][0]*xScale)[:6]+
                    ' Y'+ str(stroke.move_list[p][1]*yScale)[:6]+'\r')

        pygame.draw.lines(window, stroke.color, False, stroke.move_list, stroke.radius)

    f.close()

# window settings
image = MyImage(Image.open('rsz_image.png').convert('RGB'))
width, height = image.getSize()
canvas = MyImage(Image.new('RGB', image.getSize(), (255,255,255)))
window = pygame.display.set_mode(image.getSize())
window.fill((255, 255, 255))

# dummy strokes sample
strokes_arr = []
r = 16
stroke_color = (255, 160, 85)
move_list = [(105, 217), (99, 232), (98, 247), (98, 262), (98, 277), (101, 292), (108, 306), (105, 321), (104, 336), (106, 351), (109, 366), (96, 375), (93, 390), (94, 405), (87, 419), (95, 432), (103, 445), (113, 456), (124, 466), (136, 476), (151, 477), (161, 488), (175, 480), (185, 468), (182, 452), (193, 441), (208, 444), (223, 440), (229, 425), (217, 413), (201, 407), (186, 414), (173, 404), (157, 406), (153, 421), (160, 435), (149, 446), (134, 438), (119, 431), (103, 425), (87, 428), (78, 441), (73, 456), (57, 455), (42, 462), (29, 452), (13, 456)]
stroke = Stroke(stroke_color, r)
stroke.move_list = move_list
strokes_arr.append(stroke)

r = 16
stroke_color = (25, 128, 212)
move_list = [(219, 105), (203, 105), (187, 100), (174, 110), (158, 106), (150, 119), (134, 117), (125, 130), (136, 141), (141, 156), (126, 163), (122, 178), (115, 192), (102, 202), (96, 217), (85, 228), (69, 228), (54, 235), (40, 225), (25, 219), (26, 203), (24, 187), (36, 176), (31, 160), (32, 144), (30, 128), (25, 112), (28, 96), (43, 94), (45, 78), (36, 64), (20, 60), (4, 56), (0, 71)]
stroke = Stroke(stroke_color, r)
stroke.move_list = move_list
strokes_arr.append(stroke)

# output strokes to gcode in text file
draw_strokes(strokes_arr, window, width, height)