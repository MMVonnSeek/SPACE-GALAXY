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
                draw_text(screen, "ou [Q] para Sair", 30, WIDTH/2, (HEIGHT/2)+40)
                pygame.display.update()

    #pygame.mixer.muisc.stop()
    ready = pygame.mixer.Sound(path.join(sound_folder,'getready.ogg'))
    ready.play()
    screen.fill(BACK)
    draw_text(screen, "PREPARE-SE", 60, WIDTH/2, HEIGHT/2)
    pygame.display.update()


def draw_text(surf, text, size, x, y):
    ## selecionando uma fonte de plataforma cruzada para exibir a pontuação
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)   ## True denota a fonte a ser suavizada
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield_bar(surf, x, y, pct):
    # if pct < 0:
    #     pct = 0
    pct = max(pct, 0)
    ## moving them to top
    # BAR_LENGTH = 100
    # BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
       