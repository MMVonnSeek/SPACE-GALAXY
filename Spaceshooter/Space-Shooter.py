## Space Shooter
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
EMERALDGREEN = (0,201,87)
DODGERBLUE3 = (24,116,205)
GOLD1= (255,215,0)
TURQUOISE = (64, 244, 208)
AQUA = (0, 255, 255)
#########################################################

#########################################################
## colocar em "__init__.py" mais tarde
## inicialize o pygame e crie a janela
pygame.init()
pygame.mixer.init()  ## Para o som
screen = pygame.display.set_mode((WIDHT, HEIGHT))
pygame.display.set_caption("Space Shooter - Feito por Max Muller")
clock = pygame.time.Clock()   ##  Para sincronizar o FPS
#########################################################

font_name = pygame.font.match_font('arial')

def main_menu():
    global screen

    menu_song = pygame.mixer.music.load(path.join(sound_folder, "manu.ogg"))
    pygame.mixer.music.play(-1)

    title = pygame.image.load(path.join(img_dir "main.png")).convert()
    title = pygame.transform.scale(title, (WIDHT, HEIGHT), screen)

    screen.blit(title, (0,0))
    pygame.display.update()

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                break
            elif ev.key == pygame.K_q:
                pygame.quit()
                quit()
            elif ev,type == pygame.QUIT:
                pygame.quit()
                quit()
            else:
                draw_text(screen, "Aperte [ENTER] para Começar", 30, WIDTH/2, HEIGHT/2)
                draw_text(screen, )        