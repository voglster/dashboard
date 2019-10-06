import os
import sys
import pygame
import time
from datetime import datetime
import pytz
from loguru import logger
from collections import namedtuple
import schedule
from todo import get_next_tasks
from util import running_on_rpi

ScreenDim = namedtuple("ScreenDim", "width, height")
tz = pytz.timezone("US/Central")


def text_objects(text, font, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def setup_frame_buffer():
    drivers = ["fbcon", "directfb", "svgalib"]
    for driver in drivers:
        if not os.getenv("SDL_VIDEODRIVER"):
            os.putenv("SDL_VIDEODRIVER", driver)
        try:
            pygame.display.init()
            break
        except pygame.error:
            logger.info(f"Driver: {driver} failed.")
    else:
        raise Exception("No suitable video driver found!")

    screen_dim = ScreenDim(
        pygame.display.Info().current_w, pygame.display.Info().current_h
    )
    logger.info(f"Framebuffer size: {screen_dim.width} x {screen_dim.height}")

    pygame.init()
    screen = pygame.display.set_mode(screen_dim, pygame.FULLSCREEN)

    return screen, screen_dim


def setup_dev_screen():
    dims = ScreenDim(1280, 1024)
    pygame.init()
    screen = pygame.display.set_mode(dims)
    return screen, dims


class Dashboard:
    screen = None

    def __init__(self):
        if running_on_rpi():
            self.screen, self.screen_dimensions = setup_frame_buffer()
        else:
            self.screen, self.screen_dimensions = setup_dev_screen()
        self.bg_img = None
        self.done_img = pygame.image.load("./media/relax.png")
        pygame.mouse.set_visible(False)
        self.clear_screen()
        self.price_graph = None
        self.weather_ico = None
        self.temperature_text = None
        self.temperature_text2 = None
        self.large_text = pygame.font.Font(
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 115
        )
        self.medium_text = pygame.font.Font(
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 80
        )
        self.small_text = pygame.font.Font(
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 60
        )
        self.font_color = (255, 255, 255)
        pygame.font.init()
        pygame.display.update()
        self.tasks = []

    def clear_screen(self):
        self.screen.fill((0, 0, 0))

    def render_bg(self):
        if self.bg_img:
            self.screen.blit(self.bg_img, (0, 0))

    def show_time(self):
        now = (
            datetime.utcnow()
            .replace(tzinfo=pytz.utc)
            .astimezone(tz)
            .strftime("%I:%M %p")
        )
        text_surf, text_rect = text_objects(now, self.large_text, self.font_color)
        text_rect.center = (
            (self.screen_dimensions.width - text_rect.width / 2 - 5),
            (text_rect.height / 2 + 5),
        )

        self.screen.blit(text_surf, text_rect)

    def show_weather(self):
        if self.weather_ico and self.temperature_text:
            self.screen.blit(self.weather_ico, (10, 10))
            ico_w, ico_h = self.weather_ico.get_size()

            text_surf, text_rect = text_objects(
                self.temperature_text, self.small_text, self.font_color
            )
            text_rect.top = 10
            text_rect.left = 10 + 10 + ico_w
            self.screen.blit(text_surf, text_rect)
            text_surf, text_rect2 = text_objects(
                self.temperature_text2, self.small_text, self.font_color
            )
            text_rect2.top = ico_h + 10
            text_rect2.left = 10

            self.screen.blit(text_surf, text_rect2)

    def load_tasks(self):
        self.tasks = get_next_tasks(5)

    def show_tasks(self):
        if self.tasks:
            y = 450
            for t in self.tasks:
                if len(t["content"]) > 35:
                    text = t["content"][:30] + "..."
                else:
                    text = t["content"]
                text_surf, text_rect = text_objects(
                    text, self.small_text, self.font_color
                )
                text_rect.left = 20
                text_rect.top = y
                y = text_rect.bottom + 20
                self.screen.blit(text_surf, text_rect)
        else:
            self.screen.blit(self.done_img, (100, 400))
            text_surf, text_rect = text_objects(
                "All done!", self.small_text, self.font_color
            )
            text_rect.left = 650
            text_rect.top = 450
            self.screen.blit(text_surf, text_rect)
            text_surf, text_rect = text_objects(
                "Relax", self.small_text, self.font_color
            )
            text_rect.left = 650
            text_rect.top = 550
            self.screen.blit(text_surf, text_rect)

    def refresh_screen(self):
        self.render_bg()
        self.show_time()
        self.show_tasks()
        self.show_weather()
        pygame.display.update()

    def get_bg(self):
        from images import background_file

        with background_file() as (filename, font_color):
            self.bg_img = pygame.image.load(filename)
            self.font_color = font_color

    def get_weather(self):
        from weather import get, downloaded_weather_icon

        self.temperature_text, self.temperature_text2, icon_code = get()
        with downloaded_weather_icon(icon_code) as icon_path:
            self.weather_ico = pygame.image.load(icon_path)


if __name__ == "__main__":
    db = Dashboard()
    db.load_tasks()
    db.get_bg()
    db.get_weather()

    schedule.every(1).minute.do(db.load_tasks)
    schedule.every(1).second.do(db.refresh_screen)
    schedule.every(3).minutes.do(db.get_bg)
    schedule.every(10).minutes.do(db.get_weather)

    while True:
        schedule.run_pending()
        time.sleep(0.05)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                    sys.exit(0)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
