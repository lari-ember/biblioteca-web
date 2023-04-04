import pygame

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
