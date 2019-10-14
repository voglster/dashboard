from util import set_position, parse_color


class StaticText:
    def __init__(self, config, screen):
        self.config = config
        self.screen = screen
        self.font = self.screen.theme.get_font(
            self.config.get("font_size", "small"), self.config.get("font_type", "sans")
        )
        if self.config.get("color"):
            color = parse_color(self.config.get("color"))
        else:
            color = self.screen.theme.get_primary_color()
        self.surface = self.font.render(
            self.config.get("text", "No Text Specified"), True, color
        )

    def prepare(self):
        pass

    def draw(self):
        rect = self.surface.get_rect()
        rect = set_position(rect, self.screen.rects, self.config)

        self.screen.rects[self.config["id"]] = rect

        self.screen.blit(self.surface, rect)
