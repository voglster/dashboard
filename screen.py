import os
import sys
from itertools import product
import pygame
import time
from loguru import logger
from collections import namedtuple
import schedule
from util import running_on_rpi

from clock import Clock
from weather import Weather
from images import UnSplashImage
from todo import Todoist

ScreenDim = namedtuple("ScreenDim", "width, height")


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


class Theme:
    def __init__(self):
        self.fonts = {}

        sizes = [(115, "large"), (80, "medium"), (60, "small"), (18, "tiny")]

        types = [
            ("./media/fonts/LiberationMono-Regular.ttf", "mono"),
            ("./media/fonts/LiberationSerif-Regular.ttf", "serif"),
            ("./media/fonts/LiberationSans-Regular.ttf", "sans"),
        ]
        for (font_weight, size), (path, font_type) in product(sizes, types):
            self.fonts[(size, font_type)] = pygame.font.Font(path, font_weight)

        for font_weight, size in sizes:
            self.fonts[(size, None)] = pygame.font.Font(
                "./media/fonts/LiberationMono-Regular.ttf", font_weight
            )

        self.font_color = (255, 255, 255)
        self.bg_color = (0, 0, 0)
        pygame.font.init()

    def get_font(self, size, font_type=None):
        return self.fonts.get((size, font_type))

    def get_primary_color(self):
        return self.font_color


modules = {
    "clock": Clock,
    "weather": Weather,
    "unsplash": UnSplashImage,
    "todoist": Todoist,
}


class Dashboard:
    screen = None

    def __init__(self, config):
        if running_on_rpi():
            self.screen, self.screen_dimensions = setup_frame_buffer()
        else:
            self.screen, self.screen_dimensions = setup_dev_screen()

        pygame.mouse.set_visible(False)

        self.theme = Theme()
        self.bg_img = None
        self.clear_screen()
        self.price_graph = None
        self.weather_ico = None
        self.temperature_text = None
        self.temperature_text2 = None
        self.tasks = []
        self.modules = {}
        self.rects = {
            "screen": pygame.Rect(
                0, 0, self.screen_dimensions.width, self.screen_dimensions.height
            )
        }

        for module_config in config["modules"]:
            cls = modules[module_config["name"]]
            c = cls(module_config, self)
            self.modules[module_config["id"]] = c
            if module_config.get("run_every"):
                count, time_scale = module_config["run_every"].split(" ")
                count = int(count)
                getattr(schedule.every(count), time_scale).do(c.prepare)

        self.blit = self.screen.blit

        if config["qboard"].get("debug"):
            from debug import Debug

            d = Debug(config["qboard"], self)
            self.modules["debug"] = d

    def clear_screen(self):
        self.screen.fill(self.theme.bg_color)

    def refresh_screen(self):
        for module in self.modules.values():
            module.draw()
        pygame.display.update()


if __name__ == "__main__":
    from settings import config

    db = Dashboard(config)
    schedule.every(1).second.do(db.refresh_screen)

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
