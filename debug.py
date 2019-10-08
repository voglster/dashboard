from datetime import datetime
import pytz


class Debug:
    def __init__(self, config, screen):
        self.config = config
        self.screen = screen
        import os

        self.git_rev = os.popen("git rev-parse --short HEAD").read().strip()

    def prepare(self):
        pass

    def draw(self):
        font = self.screen.theme.get_font("tiny", "mono")
        color = self.screen.theme.get_primary_color()

        text_surf = font.render(self.git_rev, True, color)
        text_rect = text_surf.get_rect()

        parent_rect = self.screen.rects["screen"]
        parent_anchor_point = "bottomleft"
        anchor_point = "bottomleft"

        # Clever but concise, uses the virtual attributes on PyGame's rect object to align
        setattr(text_rect, anchor_point, getattr(parent_rect, parent_anchor_point))

        self.screen.blit(text_surf, text_rect)
