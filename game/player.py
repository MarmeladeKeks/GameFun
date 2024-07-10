import math

import pygame.sprite
import numpy as np

from config import WORLD_GRAV, BEE_VEL, BEE_ROTATION_UP_VEL, BEE_ROTATION_DOWN_VEL


class Player(pygame.sprite.Sprite):

    def __init__(self, width: float, height: float, game):
        super().__init__()
        self.biene_images = [
            pygame.transform.smoothscale(
                pygame.image.load(f"resources/biene-r-00{x}.png"), size=(60, 60)
            )
            for x in range(1, 7)
        ]
        self.animation_frame: float = 0
        self.game = game
        self.image = self.biene_images[self.animation_frame]
        self.rect = self.image.get_rect(center=(90, 320))
        self.rect.h = 50
        self.vel: np.ndarray = np.array([0, 0], dtype=float)
        self.acceleration: float = WORLD_GRAV
        self.jump_cooldown_timer: float = 0
        self.rotation_angle = 0

    def setup(self):
        self.acceleration = WORLD_GRAV

    def handle_spacebar_pressed(self):
        # self.acceleration = (
        #     -0.05 / self.game.time_factor
        # )  # setze Beschleunigung nach oben
        self.acceleration = 0
        self.vel[1] = BEE_VEL
        self.jump_cooldown_timer = self.game.time

    def handle_bee_animation(self):
        self.animation_frame = round(self.animation_frame + 0.5, 1)
        if self.animation_frame > 5.1:
            self.animation_frame = 0
        # self.image = self.biene_images[math.floor(self.animation_frame)]

    def handle_rotation(self):
        # case Biene fliegt nach oben
        if self.vel[1] < 0:
            self.rotation_angle += self.game.time * BEE_ROTATION_UP_VEL
            if self.rotation_angle >= 30:
                self.rotation_angle = 30
        # Biene fällt nach unten
        elif self.vel[1] > 0:
            self.rotation_angle += self.game.time * BEE_ROTATION_DOWN_VEL
            if self.rotation_angle <= -70:
                self.rotation_angle = -70

    def player_motion(self):
        self.vel[1] += self.acceleration * self.game.time
        player_y = self.rect.y + (self.vel[1]) * self.game.time
        player_y = self.keep_player_in_bounds(player_y)
        self.rect.y = player_y  # set actual player y Coordinate

        # Handle Bee Animation
        if self.vel[1] <= 0 or self.animation_frame < 5:
            self.handle_bee_animation()

        self.handle_rotation()

        self.image = pygame.transform.rotozoom(
            self.biene_images[math.floor(self.animation_frame)],
            angle=self.rotation_angle,
            scale=1,
        )
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
        self.rect[2] = min(self.rect[2], 70)
        self.rect[3] = min(self.rect[3], 70)

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
