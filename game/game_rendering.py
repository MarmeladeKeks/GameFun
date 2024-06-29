import math

import pygame
import numpy as np


BLUE = (0, 0, 220)
ROT = (200, 0, 0)
TIME_FACTOR = 1
WORLD_GRAV = 0.0005  # (m / s^2)


class GameRendering:
    def __init__(self):
        self.screen = None
        self.clock: pygame.time.Clock = None
        self.rect: np.ndarray = np.array([0, 0, 100, 100, 1], dtype=float)
        self.player: np.ndarray = np.array([0, 320, 20, 20], dtype=float)
        self.time: float = 0
        self.vel: np.ndarray = np.array([0, 0], dtype=float)
        self.acceleration: float = WORLD_GRAV
        self.jump_cooldown_timer: float = 0

        self.render()

    def render(self):
        pygame.init()
        pygame.display.set_caption("Flappy Nemo")
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()

        game_active = True

        # Main Execution Loop
        while game_active:
            self.time = self.clock.get_time() * TIME_FACTOR
            print(self.time)
            self.acceleration = WORLD_GRAV

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_active = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_events(event)

            # Spielfeld/figur(en) zeichnen (davor Spielfeld löschen) and Game Logic
            self.screen.fill(BLUE)  # clear screen
            self.player_motion()

            # Fenster aktualisieren
            pygame.display.flip()

            # Refresh-Zeiten festlegen
            self.clock.tick(60)

        pygame.quit()

    def handle_key_events(self, event: pygame.event.Event):
        if event.key == pygame.K_SPACE:
            self.acceleration = -0.025 / TIME_FACTOR  # setze Beschleunigung nach oben
            self.vel[1] = 0
            self.jump_cooldown_timer = self.time
            print("Space pressed")

    def draw_rectangle(self):
        pos_rect = self.rect[:2]
        if pos_rect[0] + self.rect[2] > pygame.display.get_window_size()[0]:
            self.rect[4] = -1
        elif pos_rect[0] <= 0:
            self.rect[4] = 1

        self.rect[:2] = self.rect[:2] + (([80, 0] * self.time) * self.rect[4])
        pygame.draw.rect(self.screen, ROT, rect=self.rect[:4])

    def player_motion(self):
        self.vel[1] += self.acceleration * self.time
        player_y = self.player[1] + (self.vel[1]) * self.time
        player_y = self.keep_player_in_bounds(player_y)
        self.player[1] = player_y  # set actual player y Coordinate

        pygame.draw.rect(self.screen, ROT, rect=self.player)

    def keep_player_in_bounds(self, player_y) -> float:
        if player_y <= 0:  # case Fish on Roof
            player_y = 0
            self.vel[1] = 0  # collide with top resets velocity
        elif (
            player_y + self.player[3] >= pygame.display.get_window_size()[1]
        ):  # case Fish on bottom
            player_y = pygame.display.get_window_size()[1] - self.player[3]
            # velocity stays because world grav is still impacting the player
            self.vel[1] = 0
        return player_y
