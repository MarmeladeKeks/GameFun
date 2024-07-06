import math

import pygame
import numpy as np
import config
from game.balken import Balken
from game.balken_group import BalkenGroup
from game.player import Player
from config import TIME_FACTOR, ROT, BLUE, GREEN, WORLD_GRAV


class GameRendering:
    def __init__(self):
        self.screen = None
        self.clock: pygame.time.Clock = None
        self.rect: np.ndarray = np.array([0, 0, 100, 100, 1], dtype=float)
        self.groups = pygame.sprite.Group()
        self.balken_group = BalkenGroup()
        self.time: float = 0

        self.player = Player(width=20, height=20, game=self)
        self.groups.add(self.player)

        self.render()

    def render(self):
        pygame.init()
        pygame.display.set_caption("Flappy Nemo")
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        config.TIME_TO_REACH_BOTTOM = math.sqrt(
            (pygame.display.get_window_size()[1] - self.player.rect[2]) / WORLD_GRAV
        )
        print(config.TIME_TO_REACH_BOTTOM)

        # add one balken here for now
        self.balken_group.add(Balken(pygame.display.get_window_size()[0], 0, 200, self))

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
            self.balken_group.move_all_balken()

            # Colosion Detection here
            collision_list: list = pygame.sprite.spritecollide(
                self.player, self.balken_group, dokill=False
            )
            if collision_list:
                print("Collision detected")
                self.player.change_player_colour(GREEN)

            # draw all here
            self.groups.draw(self.screen)
            self.balken_group.draw(self.screen)

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
