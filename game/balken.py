import pygame.sprite

from config import BALKEN_WIDTH, BLACK


class Balken(pygame.sprite.Sprite):

    def __init__(self, start_pos_x: float, start_pos_y: float, height: float):
        super().__init__()
        self.image = pygame.Surface((BALKEN_WIDTH, height))
        self.image.fill(BLACK)
        self.rect = pygame.Rect(start_pos_x, start_pos_y, BALKEN_WIDTH, height)
