import pygame.sprite

from config import BALKEN_WIDTH, BLACK, WORLD_VEL


class Balken(pygame.sprite.Sprite):

    def __init__(self, start_pos_x: float, start_pos_y: float, height: float, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((BALKEN_WIDTH, height))
        self.image.fill(BLACK)
        self.rect = pygame.Rect(
            start_pos_x - BALKEN_WIDTH, start_pos_y, BALKEN_WIDTH, height
        )

    def move_single_balken(self) -> bool:
        self.rect[0] += WORLD_VEL * self.game.time * -1

        # Return if the Balken is outside the windom and shit be removed
        return self.rect[0] + self.rect[2] <= 0
