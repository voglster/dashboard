from datetime import datetime
import pytz


class Clock:
    def __init__(self, config, screen):
        self.config = config
        self.screen = screen
        self.expected_tz = pytz.timezone(config.get("timezone"))

    def prepare(self):
        pass

    def draw(self):
        now = (
            datetime.utcnow()
            .replace(tzinfo=pytz.utc)
            .astimezone(self.expected_tz)
            .strftime(self.config.get("format", "%I:%M %p"))
        )
        font = self.screen.theme.get_font("large", "mono")
        color = self.screen.theme.get_primary_color()

        text_surf = font.render(now, True, color)
        text_rect = text_surf.get_rect()

        parent_rect = self.screen.rects[self.config["anchor_to"]["id"]]
        parent_anchor_point = self.config["anchor_to"]["point"].lower()
        anchor_point = self.config["anchor_point"]

        # Clever but concise, uses the virtual attributes on PyGame's rect object to align
        setattr(text_rect, anchor_point, getattr(parent_rect, parent_anchor_point))

        offset_str = self.config.get("offset", "0, 0")
        x_str, y_str = offset_str.split(",")
        x = int(x_str)
        y = int(y_str)

        if x or y:
            text_rect = text_rect.move(x, y)

        self.screen.rects[self.config["id"]] = text_rect

        self.screen.blit(text_surf, text_rect)
