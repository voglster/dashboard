from util import parse_color
import pygame


class ColorBG:
    def __init__(self, config, screen):
        self.config = config
        self.screen = screen
        self.color = parse_color(self.config.get("color", "black"))

    def prepare(self):
        pass

    def draw(self):
        pygame.draw.rect(
            self.screen.screen,
            self.color,
            pygame.Rect(0, 0, *self.screen.screen_dimensions),
        )
