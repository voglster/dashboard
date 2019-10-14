import os
import sys
import pygame
import time
import json
from loguru import logger
from collections import namedtuple
import schedule

from util import running_on_rpi
from datetime import datetime
import pytz

from theme import Theme

from modules.clock import Clock
from modules.weather import Weather
from modules.images import UnSplashImage
from modules.todo import Todoist
from modules.crypto import Crypto
from modules.colorbg import ColorBG
from modules.static_text import StaticText

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


modules = {
    "clock": Clock,
    "weather": Weather,
    "unsplash": UnSplashImage,
    "todoist": Todoist,
    "crypto": Crypto,
    "color_bg": ColorBG,
    "static_text": StaticText,
}


def get_preferred_resolution(config):
    resolution_string = config.get("preferred_resolution", "1280x1024")
    x, y = [int(x) for x in resolution_string.split("x")]
    return x, y


def load_remote_config(config, width, height):
    from registration import get_config

    try:
        return get_config(width, height)
    except:
        return config


class Dashboard:
    screen = None

    def __init__(self):

        if running_on_rpi():
            self.screen, self.screen_dimensions = setup_frame_buffer()
        else:
            from settings import config

            x, y = get_preferred_resolution(config.get("qboard", {}))
            self.screen, self.screen_dimensions = setup_dev_screen(x, y)
        self.rects = {
            "screen": pygame.Rect(
                0, 0, self.screen_dimensions.width, self.screen_dimensions.height
            )
        }

        self.blit = self.screen.blit
        pygame.mouse.set_visible(False)
        self.screen.fill((0, 0, 0))
        self.show_loading()
        pygame.display.update()
        self.tasks = []
        self.modules = {}
        self.theme = None
        self.config = {}
        self.load_config()

    def load_config(self):
        old_config_string = json.dumps(self.config)

        from settings import config

        self.config = self.config or config

        if "modules" not in config or config.get("qboard", {}).get("load_remote"):
            config = load_remote_config(self.config, *self.screen_dimensions)

        new_config_string = json.dumps(config)

        if old_config_string == new_config_string:
            logger.info("Config did not change, skipping reload")
            return
        logger.info("New config found")
        self.config = config

        schedule.clear("module_tasks")
        self.theme = Theme(config.get("qboard").get("theme"))

        self.modules = {}

        self.clear_screen()

        for module_config in config.get("modules", {}):
            module_name = module_config["name"]
            module_id = module_config["id"]
            logger.info(f"Loading module {module_name} for id {module_id}")
            module_class = modules[module_config["name"]]
            module_instance = module_class(module_config, self)
            self.modules[module_config["id"]] = module_instance
            if module_config.get("run_every"):
                count, time_scale = module_config["run_every"].split(" ")
                count = int(count)
                getattr(schedule.every(count), time_scale).do(
                    module_instance.prepare
                ).tag("module_tasks")

        if self.debug:
            from debug import Debug

            self.modules["debug"] = Debug(self.config, self)

    @property
    def timezone(self):
        return pytz.timezone(self.config.get("timezone", "US/Central"))

    @property
    def debug(self):
        return self.config.get("debug", False)

    @property
    def utc_time(self):
        return datetime.utcnow().replace(tzinfo=pytz.utc)

    @property
    def local_time(self):
        return self.utc_time.astimezone(self.timezone)

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
        for key, module in self.modules.items():
            module.draw()
        pygame.display.update()

    def run_forever(self):
        schedule.every(1).second.do(self.refresh_screen)
        schedule.every(30).seconds.do(self.load_config)
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


if __name__ == "__main__":
    db = Dashboard()
    db.run_forever()
