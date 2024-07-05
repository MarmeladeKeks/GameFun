import pygame.sprite

from config import BALKEN_WIDTH, BLACK


class Balken(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        # TODO: Add Context here
        self.image = None
        self.rect = None

    def create_balken(self, start_pos_x: float, start_pos_y: float, height: int):
        pass
