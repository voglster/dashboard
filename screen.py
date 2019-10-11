import os
import sys
from itertools import product
import pygame
import time
from loguru import logger
from collections import namedtuple
import schedule
from util import running_on_rpi

from modules.clock import Clock
from modules.weather import Weather
from modules.images import UnSplashImage
from modules.todo import Todoist

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


def setup_dev_screen(width=1280, height=1024):
    dims = ScreenDim(width, height)
    pygame.init()
    screen = pygame.display.set_mode(dims)
    return screen, dims


default_font_weights = {"large": 115, "medium": 80, "small": 60, "tiny": 18}


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


modules = {
    "clock": Clock,
    "weather": Weather,
    "unsplash": UnSplashImage,
    "todoist": Todoist,
}


def get_preferred_resolution(config):
    resolution_string = config.get("qboard", {}).get(
        "preferred_resolution", "1280x1024"
    )
    x, y = [int(x) for x in resolution_string.split("x")]
    return x, y


class Dashboard:
    screen = None

    def __init__(self, config):
        x, y = get_preferred_resolution(config)

        if running_on_rpi():
            self.screen, self.screen_dimensions = setup_frame_buffer()
        else:
            self.screen, self.screen_dimensions = setup_dev_screen(x, y)
        self.blit = self.screen.blit

        pygame.mouse.set_visible(False)

        self.debug = config["qboard"].get("debug", False)
        self.theme = Theme(config.get("qboard", {}).get("theme"))
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
        self.show_loading()
        pygame.display.update()

        for module_config in config["modules"]:
            cls = modules[module_config["name"]]
            c = cls(module_config, self)
            self.modules[module_config["id"]] = c
            if module_config.get("run_every"):
                count, time_scale = module_config["run_every"].split(" ")
                count = int(count)
                getattr(schedule.every(count), time_scale).do(c.prepare)

        if self.debug:
            from debug import Debug

            d = Debug(config["qboard"], self)
            self.modules["debug"] = d

    def show_loading(self):
        sys_font = pygame.font.SysFont("arial", 25)
        white = (255, 255, 255)
        text_surface = sys_font.render("QBoard is starting.. one moment", True, white)
        r = text_surface.get_rect()
        r.center = self.rects["screen"].center
        self.blit(text_surface, r)

    def clear_screen(self):
        self.screen.fill(self.theme.bg_color)

    def refresh_screen(self):
        for module in self.modules.values():
            module.draw()
        if self.debug:
            self.draw_module_rects()
        pygame.display.update()

    def draw_module_rects(self):
        for module_instance_id, rect in self.rects.items():
            if module_instance_id == "screen":
                pass
            pygame.draw.lines(
                self.screen,
                (255, 255, 255),
                True,
                [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft],
            )


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
