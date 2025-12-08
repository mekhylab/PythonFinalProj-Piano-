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

clock = pygame.time.Clock()
FPS = 30

WHITE = (255, 255, 255)

running= True
while running:
    win.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    win.fill((255, 255, 255))

    tile_width = WIDTH // 4
    tile_height = HEIGHT // 4

    for i in range(4):
        for j in range(4):
            rect = pygame.Rect(i * tile_width, j * tile_height, tile_width, tile_height)
            pygame.draw.rect(win, (0, 0, 0), rect, 1)

clock.tick(FPS)
pygame.display.update()
pygame.quit()
