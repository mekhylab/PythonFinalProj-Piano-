import random
import pygame

print("RUNNING PIANO DASH FILE")


HIGH_SCORE_FILE = "highscore.txt"


def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return 0


def save_high_score(value):
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(value))
    except:
        pass


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()                                              #pygame initialization

WIDTH, HEIGHT = 288, 512
SCREEN = (WIDTH, HEIGHT)
win = pygame.display.set_mode(SCREEN)
pygame.display.set_caption("Piano Dash")

clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
RED = (200, 0, 0)
BLUE = (30, 144, 255)

TILE_WIDTH = WIDTH // 4
TILE_HEIGHT = 130

GAME_BG = pygame.image.load("assets/bg_easy.jpg").convert()
GAME_BG = pygame.transform.scale(GAME_BG, SCREEN)

HOME_BG = pygame.image.load("assets/homescreen.jpg").convert()
HOME_BG = pygame.transform.scale(HOME_BG, SCREEN)

easy_click_sound = pygame.mixer.Sound("assets/random.wav")
die_sound = pygame.mixer.Sound("assets/die_sound.wav")

easy_click_sound.set_volume(0.9)
die_sound.set_volume(0.9)

font = pygame.font.SysFont("arial", 24, bold=True)
big_font = pygame.font.SysFont("arial", 32, bold=True)


class Tile(pygame.sprite.Sprite):
    def __init__(self, col, y, speed):
        super().__init__()
        self.col = col
        self.speed = speed
        self.alive = True

        self.image = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()
        self.rect.topleft = (col * TILE_WIDTH, y)

    def update(self):
        self.rect.y += self.speed


def spawn_tile(group, speed):                          #tile class spawn function
    col = random.randint(0, 3)
    tile = Tile(col, -TILE_HEIGHT, speed)
    group.add(tile)


def draw_grid(surface):     #drawgrid
    for i in range(5):
        pygame.draw.line(surface, GRAY, (0, i * TILE_HEIGHT), (WIDTH, i * TILE_HEIGHT), 1)
    for i in range(5):
        pygame.draw.line(surface, GRAY, (i * TILE_WIDTH, 0), (i * TILE_WIDTH, HEIGHT), 1)


def main():                  #main function
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"

    state = MENU
    running = True

    tiles = pygame.sprite.Group()
    score = 0
    high_score = load_high_score()

    base_speed = 4
    speed = base_speed

    current_bg = None

    def trigger_game_over():
        nonlocal state
        die_sound.play()
        state = GAME_OVER

    def menu_click():
        easy_click_sound.play()

    while running:
        clock.tick(FPS)
        click_pos = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = event.pos

            if event.type == pygame.KEYDOWN:
                if state == GAME_OVER and event.key == pygame.K_r:
                    menu_click()
                    tiles.empty()
                    score = 0
                    speed = base_speed
                    spawn_tile(tiles, speed)
                    state = PLAYING

                if state == GAME_OVER and event.key == pygame.K_m:
                    menu_click()
                    tiles.empty()
                    score = 0
                    speed = base_speed
                    current_bg = None
                    state = MENU

        if state == MENU:                   #menu 
            win.blit(HOME_BG, (0, 0))

            title = big_font.render("Piano Dash", True, WHITE)
            subtitle = font.render("Choose a level", True, WHITE)
            win.blit(title, (WIDTH // 2 - title.get_width() // 2, 70))
            win.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 110))

            easy_rect = pygame.Rect(60, 170, 170, 40)
            med_rect = pygame.Rect(60, 230, 170, 40)
            hard_rect = pygame.Rect(60, 290, 170, 40)

            pygame.draw.rect(win, BLUE, easy_rect, border_radius=8)
            pygame.draw.rect(win, BLUE, med_rect, border_radius=8)
            pygame.draw.rect(win, BLUE, hard_rect, border_radius=8)

            win.blit(font.render("Easy", True, WHITE), (easy_rect.x + 55, easy_rect.y + 7))
            win.blit(font.render("Medium", True, WHITE), (med_rect.x + 40, med_rect.y + 7))
            win.blit(font.render("Hard", True, WHITE), (hard_rect.x + 55, hard_rect.y + 7))

            hs_surf = font.render(f"High Score: {high_score}", True, WHITE)
            win.blit(hs_surf, (WIDTH // 2 - hs_surf.get_width() // 2, 380))

            if click_pos:
                if easy_rect.collidepoint(click_pos):
                    menu_click()
                    base_speed = 3
                    speed = base_speed
                    current_bg = GAME_BG
                    tiles.empty()
                    spawn_tile(tiles, speed)
                    score = 0
                    state = PLAYING

                elif med_rect.collidepoint(click_pos):
                    menu_click()
                    base_speed = 6
                    speed = base_speed
                    current_bg = GAME_BG
                    tiles.empty()
                    spawn_tile(tiles, speed)
                    score = 0
                    state = PLAYING

                elif hard_rect.collidepoint(click_pos):
                    menu_click()
                    base_speed = 10
                    speed = base_speed
                    current_bg = GAME_BG
                    tiles.empty()
                    spawn_tile(tiles, speed)
                    score = 0
                    state = PLAYING

            pygame.display.flip()
            continue

        if state == PLAYING:                 #playing state
            tiles.update()

            if click_pos:
                hit_any = False
                for tile in list(tiles):
                    if tile.rect.collidepoint(click_pos) and tile.alive:
                        hit_any = True
                        tile.alive = False
                        tiles.remove(tile)

                        score += 1
                        speed = base_speed + score // 3

                        easy_click_sound.play()

                        if score > high_score:
                            high_score = score
                            save_high_score(high_score)
                        break

                if not hit_any:
                    trigger_game_over()

            if len(tiles) == 0:
                spawn_tile(tiles, speed)
            else:
                last = list(tiles)[-1]
                if last.rect.top >= 0:
                    spawn_tile(tiles, speed)

            for tile in tiles:
                if tile.rect.y >= HEIGHT and tile.alive:
                    trigger_game_over()
                    break

        if state in (PLAYING, GAME_OVER):
            if current_bg is not None:
                win.blit(current_bg, (0, 0))
            else:
                win.fill(BLACK)
        else:
            win.blit(HOME_BG, (0, 0))

        draw_grid(win)
        tiles.draw(win)

        win.blit(font.render(f"Score: {score}", True, BLACK), (10, 10))
        hs_text = font.render(f"High: {high_score}", True, BLACK)
        win.blit(hs_text, (WIDTH - hs_text.get_width() - 10, 10))

        if state == GAME_OVER:
            overlay = pygame.Surface(SCREEN)
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            win.blit(overlay, (0, 0))

            go_text = big_font.render("Game Over", True, RED)
            score_text = font.render(f"Score: {score}", True, WHITE)
            retry_text = font.render("R = Restart   M = Menu", True, WHITE)

            win.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2 - 50))
            win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 10))
            win.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 30))

        pygame.display.flip()

    pygame.quit()          #quit pygame


if __name__ == "__main__":
    main()
