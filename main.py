import pygame
from pygame import mixer
from sys import exit
from random import randrange
import sys,os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path,relative_path)


pygame.init()
mixer.init()
screen_width,screen_height = 500,700
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
gravity = 4
game_over = False

#score
score = 0
font = pygame.font.SysFont('dubai.ttf',40)
score_text = font.render(f'score : {score}',False,(255,255,255))
score_text_width = score_text.get_width()
score_text_height = score_text.get_height()

#sound
egg_collect = pygame.mixer.Sound('assets/egg_collect.wav')
pygame.mixer.Sound.set_volume(egg_collect,0.5)
defeat_sound = pygame.mixer.Sound('assets/defeat.wav')
pygame.mixer.Sound.set_volume(defeat_sound,0.5)

sky_bg_url = resource_path('assets/sky.png')
sky_bg = pygame.transform.scale(pygame.image.load(sky_bg_url),(screen_width,screen_height))

ground_url = resource_path('assets/ground.png')
ground = pygame.transform.scale(pygame.image.load(ground_url),(100*5,24*5))
ground_rect = ground.get_rect()
ground_rect.x , ground_rect.y = 0,580

class Egg(pygame.sprite.Sprite):
    def __init__(self,x,y,img,ground,bucket):
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ground = ground
        self.bucket = bucket

    def draw(self):
        screen.blit(self.img,self.rect)

    def update(self):
        global score
        global game_over
        global egg_collect
        global defeat_sound
        self.rect.y += gravity

        if self.rect.colliderect(self.ground):
            # self.rect.x = randrange(0,440)
            # self.rect.y = -200
            game_over = True
            pygame.mixer.Sound.play(defeat_sound)

        if self.rect.colliderect(self.bucket):
            self.rect.x = randrange(0,440)
            self.rect.y = -200
            score += 1
            pygame.mixer.Sound.play(egg_collect)


        self.draw()


class Bucket(pygame.sprite.Sprite):
    def __init__(self,x,y,img,speed):
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def movement(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_d or pygame.K_RIGHT] and self.rect.x <= 416:
            self.rect.x += self.speed
        if keys_pressed[pygame.K_a or pygame.K_LEFT] and self.rect.x >= 0:
            self.rect.x -= self.speed


    def draw(self):
        screen.blit(self.img,self.rect)

    def update(self):
        self.movement()
        self.draw()

bucket_img_url = resource_path('assets/bucket.png')
bucket_img = pygame.transform.scale(pygame.image.load(bucket_img_url), (24*3.5, 24*3.5))
bucket = Bucket(250,496,bucket_img,4.5)

egg_img_url = resource_path('assets/egg.png')
egg_img = pygame.transform.scale(pygame.image.load(egg_img_url),(20*3,24*3))
egg = Egg(300,-50,egg_img,ground_rect,bucket)



while game_over == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if gravity <= 7:
        gravity += 0.0005

    #load bg
    screen.blit(sky_bg,(0,0))
    screen.blit(ground,(ground_rect.x , ground_rect.y))

    #score
    score_text = font.render(f'score : {score}',False,(255,255,255))
    screen.blit(score_text,(0,0))

    egg.update()
    bucket.update()

    pygame.display.update()
    clock.tick(60)

# game over text
game_over_text = font.render('Game over',False,(255,255,255))
game_over_text_width = game_over_text.get_width()
game_over_text_height = game_over_text.get_height()
game_over_text_x = (screen_width - game_over_text_width) // 2
game_over_text_y = (screen_height - game_over_text_height) // 2

#game over score_text (go = game over)
go_score_text_x = (screen_width - score_text_width) // 2
go_score_text_y= ((screen_height - score_text_height) // 2) + 50

# game over
while game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((0,0,0))
    screen.blit(game_over_text,(game_over_text_x,game_over_text_y))
    screen.blit(score_text,(go_score_text_x,go_score_text_y))

    pygame.display.update()
    clock.tick(60)