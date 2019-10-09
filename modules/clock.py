from datetime import datetime
import pytz
from util import set_position, parse_color


class Clock:
    def __init__(self, config, screen):
        self.config = config
        self.screen = screen
        self.expected_tz = pytz.timezone(config.get("timezone"))
        self.id = self.config.get("id", "clock")
        font_size = self.config.get("font_size", "large").lower()
        font_type = self.config.get("font_size", "sans").lower()
        self.font = self.screen.theme.get_font(font_size, font_type)
        self.color = parse_color(
            self.config.get("color", self.screen.theme.get_primary_color())
        )
        self.time_format = self.config.get("format", "%I:%M %p")

    def prepare(self):
        pass

    def draw(self):
        now = (
            datetime.utcnow()
            .replace(tzinfo=pytz.utc)
            .astimezone(self.expected_tz)
            .strftime(self.time_format)
        )

        text_surf = self.font.render(now, True, self.color)
        text_rect = text_surf.get_rect()

        text_rect = set_position(text_rect, self.screen.rects, self.config)

        self.screen.rects[self.id] = text_rect
        self.screen.blit(text_surf, text_rect)
