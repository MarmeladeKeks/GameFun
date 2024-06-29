import pygame


BLUE = (0, 0, 220)


class GameRendering:
    def __init__(self):
        self.render()
        self.screen = None
        self.clock = None

    def render(self):
        pygame.init()
        pygame.display.set_caption("Flappy Nemo")
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()

        game_active = True

        # Main Execution Loop
        while game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_active = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_key_events(event)

            # Here Game Logic

            # Spielfeld/figur(en) zeichnen (davor Spielfeld löschen)
            self.screen.fill(BLUE)  # clear screen

            # Fenster aktualisieren
            pygame.display.flip()

            # Refresh-Zeiten festlegen
            self.clock.tick(60)

        pygame.quit()

    def handle_key_events(self, event: pygame.event.Event):
        print("Player pressed a key")
        if event.key == pygame.K_SPACE:
            print("Spieler hat Leertaste gedrückt")
