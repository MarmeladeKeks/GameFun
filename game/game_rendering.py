import math

import pygame
import numpy as np
import config
from game.balken import Balken
from game.balken_creation import BalkenCreator
from game.balken_group import BalkenGroup
from game.player import Player
import time
from config import TIME_FACTOR, ROT, BLUE, GREEN, WORLD_GRAV


class GameRendering:
    def __init__(self):
        self.time_to_reach_bottom = None
        self.screen = None
        self.clock: pygame.time.Clock = None
        self.rect: np.ndarray = np.array([0, 0, 100, 100, 1], dtype=float)
        self.groups = pygame.sprite.Group()
        self.balken_group = BalkenGroup()
        self.time: float = 0
        self.time_factor = TIME_FACTOR

        self.player = Player(width=20, height=20, game=self)
        self.groups.add(self.player)
        self.balken_creator = None
        self.input_processed = False

        self.render()

    def render(self):
        pygame.init()
        pygame.joystick.init()
        pygame.display.set_caption("Flappy Nemo")
        self.screen = pygame.display.set_mode((1280, 720), vsync=1)
        self.clock = pygame.time.Clock()

        # Berechnung wie schnell man von ganz oben nach ganz unten fallen kann (Zeit in ms)
        self.time_to_reach_bottom = (
            math.sqrt(
                (pygame.display.get_window_size()[1] - self.player.rect[2]) / WORLD_GRAV
            )
            + 1500
        ) * self.time_factor

        # Controller Support
        joysticks = []

        # Zufälliger Balken Creator
        self.balken_creator = BalkenCreator(self.balken_group, self)

        print(self.time_to_reach_bottom)

        # add one balken here for now
        # self.balken_group.add(Balken(pygame.display.get_window_size()[0], 0, 200, self))

        game_active = True

        # Main Execution Loop
        while game_active:
            self.time = self.clock.get_time() * self.time_factor
            self.player.setup()
            for event in pygame.event.get():
                if event.type == pygame.JOYDEVICEADDED:
                    joy = pygame.joystick.Joystick(event.device_index)
                    joysticks.append(joy)
                if event.type == pygame.QUIT:
                    game_active = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_events(event)

            # Controller Input
            if not self.input_processed:
                for joystick in joysticks:
                    if joystick.get_button(0):
                        self.player.handle_spacebar_pressed()

            # Spielfeld/figur(en) zeichnen (davor Spielfeld löschen) and Game Logic

            # Random Balken Creation
            balken_creation_timer = time.time_ns() // 1_000_000
            self.balken_creator.random_balken_creation(balken_creation_timer)

            self.screen.fill(BLUE)  # clear screen
            self.player.player_motion()
            self.balken_group.move_all_balken()

            # Colosion Detection here
            collision_list: list = pygame.sprite.spritecollide(
                self.player, self.balken_group, dokill=False
            )
            if collision_list:
                self.player.change_player_colour(GREEN)
            # draw all here
            self.groups.draw(self.screen)
            self.balken_group.draw(self.screen)

            # Debug Bee Collision Hitbox
            pygame.draw.rect(self.screen, ROT, self.player.rect, 1)

            # Fenster aktualisieren
            pygame.display.flip()

            self.input_processed = False

            # Refresh-Zeiten festlegen
            self.clock.tick(120)

        pygame.quit()

    def handle_key_events(self, event: pygame.event.Event):
        if event.key == pygame.K_SPACE:
            self.player.handle_spacebar_pressed()
            self.input_processed = True

    def draw_rectangle(self):
        pos_rect = self.rect[:2]
        if pos_rect[0] + self.rect[2] > pygame.display.get_window_size()[0]:
            self.rect[4] = -1
        elif pos_rect[0] <= 0:
            self.rect[4] = 1

        self.rect[:2] = self.rect[:2] + (([80, 0] * self.time) * self.rect[4])
        pygame.draw.rect(self.screen, ROT, rect=self.rect[:4])
