from pathlib import Path
from os import environ

import pygame
from snake import *

# UI colors
BUTTON_CLR = (70, 70, 70)
BUTTON_HOVER_CLR = (100, 100, 100)
TEXT_CLR = (255, 255, 255)

BASE_DIR = Path(__file__).resolve().parent.parent
BADGE_PATH = BASE_DIR / "assets" / "images" / "project_badge.png"


def draw_screen(surface):
    surface.fill(SURFACE_CLR)


def draw_grid(surface):
    x = 0
    y = 0
    for _ in range(ROWS):
        x += SQUARE_SIZE
        y += SQUARE_SIZE
        pygame.draw.line(surface, GRID_CLR, (x, 0), (x, HEIGHT))
        pygame.draw.line(surface, GRID_CLR, (0, y), (WIDTH, y))


def draw_button(surface, rect, text, font):
    mouse_pos = pygame.mouse.get_pos()
    color = BUTTON_HOVER_CLR if rect.collidepoint(mouse_pos) else BUTTON_CLR
    pygame.draw.rect(surface, color, rect, border_radius=6)
    text_surface = font.render(text, True, TEXT_CLR)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)


def load_project_badge():
    if BADGE_PATH.exists():
        badge = pygame.image.load(str(BADGE_PATH)).convert_alpha()
        return pygame.transform.smoothscale(badge, (120, 120))
    return None


def play_game():
    pygame.init()
    environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption("AI Snake Game - BFS Pathfinding")
    game_surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    snake = Snake(game_surface)

    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 25)
    buttons = {
        'x1': pygame.Rect(10, HEIGHT - 40, 50, 30),
        'x2': pygame.Rect(70, HEIGHT - 40, 50, 30),
        'x6': pygame.Rect(130, HEIGHT - 40, 50, 30),
        'x10': pygame.Rect(190, HEIGHT - 40, 50, 30),
        'reset': pygame.Rect(250, HEIGHT - 40, 80, 30),
        'pause': pygame.Rect(340, HEIGHT - 40, 80, 30)
    }
    speed = 1
    paused = False
    project_badge = load_project_badge()

    mainloop = True
    while mainloop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for key, button in buttons.items():
                    if button.collidepoint(event.pos):
                        if key == 'x1':
                            speed = 1
                        elif key == 'x2':
                            speed = 2
                        elif key == 'x6':
                            speed = 6
                        elif key == 'x10':
                            speed = 10
                        elif key == 'reset':
                            snake = Snake(game_surface)
                        elif key == 'pause':
                            paused = not paused

        if not paused:
            draw_screen(game_surface)
            draw_grid(game_surface)
            snake.update()

        for key, button in buttons.items():
            draw_button(game_surface, button, key, font)

        credit_text = "Designed by: Hassan Abdulsalam Mohammed"
        text_surface = small_font.render(credit_text, True, TEXT_CLR)
        game_surface.blit(text_surface, (10, HEIGHT - 70))

        if project_badge:
            game_surface.blit(project_badge, (WIDTH - project_badge.get_width() - 10, 10))

        clock.tick(FPS * speed)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    play_game()
