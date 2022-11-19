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
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, RED1, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


    def draw_lives(surf, x, y, lives, img):
        for i in range(lives):
            img_rect= img.get_rect()
            img_rect.x = x + 30 * i
            img_rect.y = y
            surf.blit(img, img_rect)


def newmob():
    mob_element = Mob()
    all_sprites.add(mob_element)
    mobs.add(mob_element)

class Explosion(pygame.sprites.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = nowself.frame += 1
            if self.fram == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get+rect()
                self.rect.center = center


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprites.__init__(self)
        ## dimensionar o jogador img para baixo
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rectcenterx = WIDTH / 2
        self.ect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.det_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()

    def update(self):
        ## tempo limite dos poderes
        if self.power >=2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
           self.power -= 1
           self.power_time = pygame.time.get_ticks()

        ## reexibir
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 30

        self.speedx = 0     ## torna o player estático na tela por padrão.
        # temos que verificar se há um tratamento de evento sendo feito para as teclas de seta
        ## pressionadas

        ## irá devolver uma lista das teclas que foram pressionadas nesse momento
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 5

        # Armas de fogo segurando a barra de espaço
        if keystate[pygame.K_SPACE]:
            self.shoot()

        ## verifica as bordas à esquerda e à direita
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        self.rect.x += self.speedx

    