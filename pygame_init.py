import pygame
def init():
    pygame.mixer.init()
    pygame.font.init()
    font = pygame.font.Font('Fonts/NotoSansJP-VariableFont_wght.ttf', 32)
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 700
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Gameshow')
    return screen, font
