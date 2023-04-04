import pygame
from pygame.locals import *
import sys

pygame.init()
size = width, height = 320, 240
speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)  # define o tamanho da tela
ball = pygame.image.load("ball.bmp")    # carrega a imagem da bola
ballrect = ball.get_rect()
while 1:                                # cria um loop infinito
    for event in pygame.event.get():    # se houver algum evento do usuário,
        if event.type == pygame.QUIT:   # o programa termina
           sys.exit()

# movimentação da bola e atualização da tela
    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
       speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
       speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ballrect)
    pygame.display.flip()

'''
pygame.init()

#define the window size
win_width = 800
win_height = 800

#create the window
win = pygame.display.set_mode((win_width, win_height))

#set the window title
pygame.display.set_caption("my game")

#vars for the game loop
run = True
clock = pygame.time.Clock()

pygame.draw.rect(win,(255,0,0),(110,100,200,100,))

#loop
while run:
    #set the window refresh rate
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    #window update
    pygame.display.update()
    
#exit the game
pygame.quit()
'''