import math

import pygame.display

from game.balken import Balken
from game.balken_group import BalkenGroup
import time

from config import (
    MIN_GAP,
    MIN_BALKEN_HEIGHT,
    MAX_DIFFICULTY,
    MIN_GAP_START,
    MAX_GAP_END,
)
import random
import opensimplex


class BalkenCreator:

    def __init__(self, balken_group: BalkenGroup, game):
        self.balken_group = balken_group
        self.game = game
        self.start_time = time.time_ns() // 1_000_000
        self.difficulty = 0
        self.noise_scaling_factor = (
            -MIN_GAP_START - MIN_GAP + pygame.display.get_window_size()[1] - MAX_GAP_END
        ) / 2
        self.noice_t = (
            pygame.display.get_window_size()[1] + MIN_GAP_START - MAX_GAP_END
        ) / 2
        self.perlin_noise_x: int = 0

    def set_difficulty(self, difficulty: float) -> None:
        self.difficulty = difficulty if difficulty <= MAX_DIFFICULTY else MAX_DIFFICULTY

    def random_balken_creation(self, current_time: float) -> bool:
        combined = (current_time - self.start_time) - self.game.time_to_reach_bottom
        if combined < 0:
            return False

        # Use Open Simplex Noice Function to generate gap point for the next Balken

        noice = opensimplex.noise2(self.perlin_noise_x, 1)
        current_noise = noice * self.noise_scaling_factor + self.noice_t
        end_y = current_noise - MIN_GAP / 2
        start_y = current_noise + MIN_GAP / 2

        # Create the two Balken oben und unten
        self.create_random_balken_oben(end_y)
        self.create_random_balken_unten(start_y)

        # Reset Balken Creation Timer
        self.start_time = time.time_ns() // 1_000_000

        # Increment noise x
        self.perlin_noise_x += 1.5
        return True

    def create_random_balken_oben(self, end_y: int) -> None:
        start_pos_x = pygame.display.get_window_size()[0]
        start_pos_y = 0
        self.balken_group.add(Balken(start_pos_x, start_pos_y, end_y, self.game))

    def create_random_balken_unten(self, start_y: int) -> None:
        start_pos_x = pygame.display.get_window_size()[0]
        height = pygame.display.get_window_size()[1] - start_y
        self.balken_group.add(Balken(start_pos_x, start_y, height, self.game))
