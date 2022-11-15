from __future__ import division
import pygame
import random
from os import path

## pasta de ativos 
img_dir = path.join(path.dirname(__file__), 'ativos')
sound_folder = path.join(path.dirname(__file__), 'sons')

########################################################
## para colocar em "constant.py" depois
WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000
BAR_LENGTH = 100
BAR_HEIGHT = 10

# Defina as cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED1 = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
TURQUOISE = (64, 244, 208)
AQUA = (0, 255, 255)
#########################################################

#########################################################
