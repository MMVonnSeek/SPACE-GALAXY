# SPACE SHOOTER
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
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter - Feito por Max Muller")
clock = pygame.time.Clock()   ##  Para sincronizar o FPS
#########################################################

font_name = pygame.font.match_font('arial')

def main_menu():
    global screen

    menu_song = pygame.mixer.music.load(path.join(sound_folder, "menu.ogg"))
    pygame.mixer.music.play(-1)

    title = pygame.image.load(path.join(img_dir, "main.png")).convert()
    title = pygame.transform.scale(title, (WIDTH, HEIGHT), screen)

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
        elif ev.type == pygame.QUIT:
                pygame.quit()
                quit() 
        else:
            draw_text(screen, "Aperte [ENTER] para Começar", 30, WIDTH/2, HEIGHT/2)
            draw_text(screen, "ou [Q] para Sair", 30, WIDTH/2, (HEIGHT/2)+40)
            pygame.display.update()

    #pygame.mixer.music.stop()
    ready = pygame.mixer.Sound(path.join(sound_folder,'getready.ogg'))
    ready.play()
    screen.fill(BLACK)
    draw_text(screen, "PREPARE-SE!", 60, WIDTH/2, HEIGHT/2)
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

class Explosion(pygame.sprite.Sprite):
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
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        ## dimensionar o jogador img para baixo
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0 
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
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

    def shoot(self):
        ## informar a bala o local de spawn
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shooting_sound.play()
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shooting_sound.play()

            """   POWER   """    
            if self.power >= 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                missile1 = Missile(self.rect.centerx, self.rect.top) # O míssil dispara do centro da nave
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(missile1)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(missile1)
                shooting_sound.play()
                missile_sound.play()

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


# defina os inimigos     
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *.90 / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(5, 20)  ##  para randomizar a velocidade do Mob

        ## randomize os movimentos um pouco mais
        self.speedx = random.randrange(-3, 3)

        ##  adicionando rotação ao elemento mob
        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8) 
        self.last_update = pygame.time.get_ticks()  ##  momento em que a rotação tem que acontecer

    def rotate(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_update > 50: # em milissegundos
            self.last_update = time_now
            self.rotation = (self.rotation + self.rotation_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate() 
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        ##  agora e se o elemento mob sair da tela

        if (self.rect.top > HEIGHT + 10) or (self.rect.left < -25) or (self.rect.right > HEIGHT + 20):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)  ##  para randomizar a velocidade do Mob

##  defina a sprite para Powerups   
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()                             
        ##  coloque a bala de acordo com a posição atual do jogador
        self.rect.center = center 
        self.speedy = 2

    def update(self):   
        """deve aparecer bem na frente do jogador"""
        self.rect.y += self.speedy
        ##  mate o sprite depois que ele passar pela borda superior
        if self.rect.top > HEIGHT:
            self.kill()


##  define o sprite para balas
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        ##  coloque a bala de acordo com a posição atual do jogador
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):      
        """deve aparecer bem na frente do jogador"""
        self.rect.y += self.speedy
        ##  mate o sprite depois que ele passar pela borda superior
        if self.rect.bottom < 0:
            self.kill()

        ##  agora precisamos de uma maneira de atirar
        ##  vamos vinculá-lo à "barra de espaço".
        ##  adicionando um evento para ele no loop do jogo

##  MÍSSEIS DE FOGO    
class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        """deve aparecer bem na frente do jogador"""
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


#########################################################
## Carregar todas as imagens do jogo

background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()
##  desenhe este reto primeiro

player_img = pygame.image.load(path.join(img_dir, 'playerShip1_orange.png')).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, 'laserRed16.png')).convert()
missile_img = pygame.image.load(path.join(img_dir, 'missile.png')).convert_alpha()
# meteor_img = pygame.image.load(path.join(img_dir, 'meteorBrown_med1.png')).convert()
meteor_images = []
meteor_list = [
    'meteorBrown_big1.png',
    'meteorBrown_big2.png',
    'meteorBrown_med1.png',
    'meteorBrown_med3.png',
    'meteorBrown_small1.png',
    'meteorBrown_small2.png',
    'meteorBrown_tiny1.png'
]

for image in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, image)).convert())
    
## Explosão do meteoro
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    ##  redimensionar a explosão
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    
    ## explosão do jogador
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
    
##  carregar power-ups
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()


#########################################################


######################################################### 
### Carregar todos os sons do jogo
shooting_sound = pygame.mixer.Sound(path.join(sound_folder, 'pew.wav'))
missile_sound = pygame.mixer.Sound(path.join(sound_folder, 'rocket.ogg'))
expl_sounds = []
for sound in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(sound_folder, sound)))
##  música de fundo principal    
#pygame.mixer.music.load(path.join(sound_folder, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.2)     ##   diminuiu um pouco o som

player_die_sound = pygame.mixer.Sound(path.join(sound_folder, 'rumble1.ogg'))
######################################################### 

##  TODO:  faça a música do jogo repetir várias vezes. play(loops=-1) não está funcionando
# Error :
# TypeError: play() não aceita argumentos de palavra-chave
#pygame.mixer.music.play()

######################################################### 
## Game loop
running = True
menu_display = True
while running:
    if menu_display:
        main_menu()
        pygame.time.wait(3000)
        
        # Parar a música do menu
        pygame.mixer.music.stop()
        #   Tocar a música do jogo
        pygame.mixer.music.load(path.join(sound_folder, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
        pygame.mixer.music.play(-1)     ##  faz o jogo soar em um loop infinito
        
        menu_display = False
        
        ##  agrupar todos os sprites juntos para facilitar a atualização
        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        
        ##  gerar um grupo de mob
        mobs = pygame.sprite.Group()
        for i in range(8):
            # mob_element = Mob()
            # all_sprites.add(mob_element)
            # mobs.add(mob_element)
            newmob()
            
        ##  grupo para balas
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        
        #### Variável do placar
        score = 0
        
    #1 Process Input/events
    clock.tick(FPS)    ##  fará com que o loop funcione na mesma velocidade o tempo todo
    for event in pygame.event.get():    # obtém todos os eventos que ocorreram até agora e os mantém atualizados.
        ##  ouvindo o botão X no topo
        if event.type == pygame.QUIT:
            running = False
            
        ##  Pressione ESC para sair do jogo
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        # ## event for shooting the bullets
        # elif event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         player.shoot()      ## we have to define the shoot()  function

    #2 Update
    all_sprites.update()
    
    
    ##  verifica se uma bala atingiu um mob
    ##  agora temos um grupo de balas e um grupo de mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    ##  agora, como excluímos o elemento mob quando acertamos um com uma bala, precisamos resgatá-los novamente
    ##  pois não haverá mob_elements deixado de fora
    for hit in hits:
        score += 50 - hit.radius    ##  dê pontuações diferentes para acertar meteoros grandes e pequenos
        random.choice(expl_sounds).play()
        # m = Mob()
        # all_sprites.add(m)
        # mobs.add(m)
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()  ##  gera um novo mob
        
    ##  o loop acima criará a quantidade de objetos mob que foram mortos e aparecerão novamente
    #########################################################

    ##  vefirica se o jogador colide com um mob
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)        ## gives back a list, True makes the mob element disappear
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0: 
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            # running = False     ## GAME OVER 3:D
            player.hide()
            player.lives -= 1
            player.shield = 100
        
    ##  se o jogador acertar um power up
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
        
    ##  se o jogador morrer e a explosão terminar, finalize o jogo
    if player.lives == 0 and not death_explosion.alive():
        running = False
        # menu_display = True
        # pygame.display.update()
    
    #3 Draw/render
    screen.fill(BLACK)
    ##  desenhe a imagem stargaze.png
    screen.blit(background, background_rect)

    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH /2, 10)    ##  10px para baixo da tela
    draw_shield_bar(screen, 5, 5, player.shield)

    # Draw lives
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)

    ##  Feito depois de desenhar tudo na tela
    pygame.display.flip()

pygame.quit()

# By: Max Muller                  