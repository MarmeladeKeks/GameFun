import math

import pygame.display

from game.balken import Balken
from game.balken_group import BalkenGroup
import time

from config import MIN_GAP, MIN_BALKEN_HEIGHT, MAX_DIFFICULTY
import random


class BalkenCreator:

    def __init__(self, balken_group: BalkenGroup, game):
        self.balken_group = balken_group
        self.game = game
        self.start_time = time.time_ns() // 1_000_000
        self.difficulty = 0

    def set_difficulty(self, difficulty: float) -> None:
        self.difficulty = difficulty if difficulty <= MAX_DIFFICULTY else MAX_DIFFICULTY

    def random_balken_creation(self, current_time: float) -> bool:
        combined = (current_time - self.start_time) - self.game.time_to_reach_bottom
        if combined < 0:
            return False
        current_random = random.randint(0, 1000)

        # Wahrscheinlichkeit das ein BaLken kommt soll quadratisch mit der zeit in der kein Balken kam ansteigen
        current_random += self.difficulty
        if current_random >= 995:
            (
                self.create_random_balken_oben()
                if random.randint(0, 1) == 1
                else self.create_random_balken_unten()
            )
            self.start_time = time.time_ns() // 1_000_000
            return True
        return False

    def create_random_balken_oben(self) -> None:
        start_pos_x = pygame.display.get_window_size()[0]
        start_pos_y = 0
        height = random.randint(
            MIN_BALKEN_HEIGHT, pygame.display.get_window_size()[1] - MIN_GAP
        )
        self.balken_group.add(Balken(start_pos_x, start_pos_y, height, self.game))

    def create_random_balken_unten(self) -> None:
        start_pos_x = pygame.display.get_window_size()[0]
        start_pos_y = random.randint(
            MIN_GAP, pygame.display.get_window_size()[1] - MIN_BALKEN_HEIGHT
        )
        height = pygame.display.get_window_size()[1] - start_pos_y
        self.balken_group.add(Balken(start_pos_x, start_pos_y, height, self.game))
