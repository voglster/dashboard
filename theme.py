import pygame
from itertools import product

default_font_weights = {
    "large": 115,
    "medium": 80,
    "small": 60,
    "extra_small": 35,
    "tiny": 18,
}


class Theme:
    def __init__(self, theme):
        self.fonts = {}
        theme = theme or {}

        sizes = theme.get("font_weights", default_font_weights)

        types = [
            ("./media/fonts/LiberationMono-Regular.ttf", "mono"),
            ("./media/fonts/LiberationSerif-Regular.ttf", "serif"),
            ("./media/fonts/LiberationSans-Regular.ttf", "sans"),
        ]
        for (size, font_weight), (path, font_type) in product(sizes.items(), types):
            self.fonts[(size, font_type)] = pygame.font.Font(path, font_weight)

        for size, font_weight in sizes.items():
            self.fonts[(size, None)] = pygame.font.Font(
                "./media/fonts/LiberationMono-Regular.ttf", font_weight
            )

        from util import parse_color

        self.font_color = parse_color(theme.get("primary_color", "white"))
        self.bg_color = (0, 0, 0)
        pygame.font.init()

    def get_font(self, size, font_type=None):
        return self.fonts.get((size, font_type))

    def get_primary_color(self):
        return self.font_color
