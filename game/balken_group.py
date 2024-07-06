from typing import List

import pygame.sprite

from game.balken import Balken


class BalkenGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()
        # can i push?
