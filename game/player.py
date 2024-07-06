import pygame.sprite
import numpy as np

from config import TIME_FACTOR, WORLD_GRAV, ROT


class Player(pygame.sprite.Sprite):

    def __init__(self, width: float, height: float, game):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((width, height))
        self.image.fill(ROT)
        self.rect = pygame.Rect(30, 320, 20, 20)
        self.vel: np.ndarray = np.array([0, 0], dtype=float)
        self.acceleration: float = WORLD_GRAV
        self.jump_cooldown_timer: float = 0

    def setup(self):
        self.acceleration = WORLD_GRAV

    def handle_spacebar_pressed(self):
        self.acceleration = -0.025 / TIME_FACTOR  # setze Beschleunigung nach oben
        self.vel[1] = 0
        self.jump_cooldown_timer = self.game.time

    def player_motion(self):
        self.vel[1] += self.acceleration * self.game.time
        player_y = self.rect.y + (self.vel[1]) * self.game.time
        player_y = self.keep_player_in_bounds(player_y)
        self.rect.y = player_y  # set actual player y Coordinate

    def keep_player_in_bounds(self, player_y) -> float:
        if player_y <= 0:  # case Fish on Roof
            player_y = 0
            self.vel[1] = 0  # collide with top resets velocity
        elif (
            player_y + self.rect[3] >= pygame.display.get_window_size()[1]
        ):  # case Fish on bottom
            player_y = pygame.display.get_window_size()[1] - self.rect[3]
            # velocity stays because world grav is still impacting the player
            self.vel[1] = 0
        return player_y

    def change_player_colour(self, color: pygame.Color):
        self.image.fill(color)
