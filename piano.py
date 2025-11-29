#make piano tiles
import pygame

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512


info = pygame.display.Info()
width=info.current_w
height=info.current_h

if width >= height:
    win=pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
    win=pygame.display.set_mode(SCREEN,pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

running= True
while running:
    
