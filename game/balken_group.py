from typing import List

import pygame.sprite

from game.balken import Balken


class BalkenGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

    def move_all_balken(self):
        for balken in self.sprites():
            out_of_window = balken.move_single_balken()
            if out_of_window:
                self.remove(balken)
