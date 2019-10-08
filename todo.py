from dateutil.parser import parse
from datetime import datetime
import todoist
import pytz
import pygame

tz = pytz.timezone("US/Central")

fields = ["content", "priority", "day_order"]


def text_objects(text, font, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


class Todoist:
    def __init__(self, config, screen):
        self.config = config
        self.screen = screen
        self.prepare()
        self.tasks = None
        self.done_img = pygame.image.load("./media/relax.png")
        self.prepare()

    def prepare(self):
        self.tasks = get_next_tasks(5, self.config["api_key"])

    def draw(self):
        if self.tasks:
            y = 350
            for t in self.tasks:
                if len(t["content"]) > 35:
                    text = t["content"][:30] + "..."
                else:
                    text = t["content"]
                text_surf, text_rect = text_objects(
                    text,
                    self.screen.theme.get_font("small", "serif"),
                    self.screen.theme.font_color,
                )
                text_rect.left = 20
                text_rect.top = y
                y = text_rect.bottom + 20
                self.screen.blit(text_surf, text_rect)
        else:
            self.screen.blit(self.done_img, (100, 400))
            text_surf, text_rect = text_objects(
                "All done!",
                self.screen.theme.get_font("small", "serif"),
                self.screen.theme.font_color,
            )
            text_rect.left = 650
            text_rect.top = 450
            self.screen.blit(text_surf, text_rect)
            text_surf, text_rect = text_objects(
                "Relax",
                self.screen.theme.get_font("small", "serif"),
                self.screen.theme.font_color,
            )
            text_rect.left = 650
            text_rect.top = 550
            self.screen.blit(text_surf, text_rect)


def get_next_tasks(count=3, api_key=None):
    assert api_key, "You must pass an api key"
    api = todoist.TodoistAPI(api_key)
    api.sync()

    today = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(tz).date()

    todays_items = [
        x
        for x in api.state["items"]
        if x["due"] and parse(x["due"]["date"]).date() <= today and x["checked"] == 0
    ]

    todays_items = sorted(
        todays_items, key=lambda x: x["day_order"] + (4 - x["priority"] * 1000)
    )[:count]

    todays_items = [{field: x[field] for field in fields} for x in todays_items]
    return todays_items
