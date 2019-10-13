from dateutil.parser import parse
from datetime import datetime
import todoist
import pytz
import pygame
from util import set_position

tz = pytz.timezone("US/Central")

fields = ["content", "priority", "child_order"]


def remove_links(task_string):
    """
    Removes any links in a task text
    :param task_string: the task you want to alter
    :return: the altered string
    """
    if "://" in task_string:
        colon_idx = task_string.index("://")
        before_part = task_string[0:colon_idx]
        for idx, char in enumerate(reversed(before_part)):
            if char == " ":
                url_start_idx = colon_idx - idx
                break
        else:
            url_start_idx = 0

        url_end = task_string.find(" ", colon_idx)
        paren_start = task_string.find("(", url_end)
        paren_end = task_string.find(")", paren_start)

        if paren_start != -1 and paren_end != -1:
            task_string = (
                task_string[0:url_start_idx]
                + task_string[paren_start + 1 : paren_end]
                + task_string[paren_end + 1 :]
            )

    return task_string


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
        self.v_spacing = config.get("vertical_spacing", 0)
        self.prepare()

    def prepare(self):
        self.tasks = get_next_tasks(5, self.config["api_key"])

    def draw(self):
        if self.tasks:
            self.draw_tasks()
        else:
            self.draw_all_done()

    def task_text(self):
        for t in self.tasks:
            if len(t["content"]) > 35:
                yield t["content"][:30] + "..."
            else:
                yield t["content"]

    def draw_tasks(self):
        drawing_items = []
        y = 0
        for text in self.task_text():
            text_surf, text_rect = text_objects(
                text,
                self.screen.theme.get_font("small", "sans"),
                self.screen.theme.font_color,
            )
            text_rect.top = y
            y = text_rect.bottom + self.v_spacing
            drawing_items.append((text_rect, text_surf))
        if drawing_items:
            q = [x[0] for x in drawing_items]
            entire_rect = q[0].unionall(q[1:])
            self.screen.rects[self.config["id"]] = entire_rect

            entire_rect = set_position(entire_rect, self.screen.rects, self.config)
            x = entire_rect.left
            y = entire_rect.top

            for rect, surface in drawing_items:
                rect.topleft = (x, y)
                y = rect.bottom + self.v_spacing
                self.screen.blit(surface, rect)

    def draw_all_done(self):
        done_image_rect = self.done_img.get_rect()

        all_done_surface, all_done_rect = text_objects(
            "All done!",
            self.screen.theme.get_font("small", "sans"),
            self.screen.theme.font_color,
        )
        all_done_rect.topleft = done_image_rect.topright

        relax_surf, relax_rect = text_objects(
            "Relax",
            self.screen.theme.get_font("small", "sans"),
            self.screen.theme.font_color,
        )
        relax_rect.topleft = all_done_rect.bottomleft

        q = [relax_rect, done_image_rect, all_done_rect]

        entire_rect = q[0].unionall(q[1:])
        self.screen.rects[self.config["id"]] = entire_rect

        entire_rect = set_position(entire_rect, self.screen.rects, self.config)
        x = entire_rect.left
        y = entire_rect.top

        done_image_rect.topleft = (x, y)
        all_done_rect.topleft = done_image_rect.topright
        relax_rect.left = all_done_rect.left
        relax_rect.top = all_done_rect.bottom + self.v_spacing

        self.screen.blit(self.done_img, done_image_rect)
        self.screen.blit(relax_surf, relax_rect)
        self.screen.blit(all_done_surface, all_done_rect)


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
        todays_items, key=lambda x: x["child_order"] + (4 - x["priority"] * 1000)
    )[:count]

    todays_items = [{field: x[field] for field in fields} for x in todays_items]

    for item in todays_items:
        item["content"] = remove_links(item["content"])

    return todays_items
