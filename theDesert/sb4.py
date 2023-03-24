
# import sys
from random import randint
import pygame
from pygame.locals import *
pygame.init()


clock = pygame.time.Clock()

fps = 60
up = False
down = False
player_location = [250 ,200]
friction = 0.9
force = 0
misy = randint(0, 400)
missile_loc = [590,misy]

player = pygame.image.load("ship.png")
missile = pygame.image.load("missile.png")

Window_size = (600,400)
pygame.display.set_caption("The Game")
screen = pygame.display.set_mode(Window_size, 0, 0)

player_rect = pygame.Rect(player_location[0], player_location[1], player.get_width(), player.get_height())
missile_rect = pygame.Rect(missile_loc[0], missile_loc[1], missile.get_width(), missile.get_height())

go = True
while go:

    screen.fill((146, 244, 255))
    pygame.draw.rect(screen, (0,0,0), player_rect)
    pygame.draw.rect(screen, (255,0,0), missile_rect)

    screen.blit(player, player_location)
    screen.blit(missile, missile_loc)

    player_rect.x = player_location[0]
    player_rect.y = player_location[1]

    player_location[1] += force

    force *= friction

    if up == True:
        force -= 1
    if down == True:
        force += 1

    for event in pygame.event.get():
        if event.type == QUIT:
            go = False
        if event.type == KEYDOWN:
            if event.key == K_UP:
                up = True
            if event.key == K_DOWN:
                down = True
        if event.type == KEYUP:
            if event.key == K_UP:
                up = False
            if event.key == K_DOWN:
                down = False

    pygame.display.update()
    clock.tick(fps)

pygame.quit()