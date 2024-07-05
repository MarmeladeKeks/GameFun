import math

import pygame
import numpy as np

from game.player import Player

BLUE = (0, 0, 220)
ROT = (200, 0, 0)
TIME_FACTOR = 1
WORLD_GRAV = 0.0005  # (m / s^2)


class GameRendering:
    def __init__(self):
        self.screen = None
        self.clock: pygame.time.Clock = None
        self.rect: np.ndarray = np.array([0, 0, 100, 100, 1], dtype=float)
        self.groups = pygame.sprite.Group()
        self.time: float = 0

        self.player = Player(width=20, height=20, game=self)
        self.groups.add(self.player)
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
            self.player.setup()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_active = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_events(event)

            # Spielfeld/figur(en) zeichnen (davor Spielfeld löschen) and Game Logic
            self.screen.fill(BLUE)  # clear screen
            self.player.player_motion()

            # draw all here
            self.groups.draw(self.screen)

            # Fenster aktualisieren
            pygame.display.flip()

            # Refresh-Zeiten festlegen
            self.clock.tick(60)

        pygame.quit()

    def handle_key_events(self, event: pygame.event.Event):
        if event.key == pygame.K_SPACE:
            self.player.handle_spacebar_pressed()

    def draw_rectangle(self):
        pos_rect = self.rect[:2]
        if pos_rect[0] + self.rect[2] > pygame.display.get_window_size()[0]:
            self.rect[4] = -1
        elif pos_rect[0] <= 0:
            self.rect[4] = 1

        self.rect[:2] = self.rect[:2] + (([80, 0] * self.time) * self.rect[4])
        pygame.draw.rect(self.screen, ROT, rect=self.rect[:4])
