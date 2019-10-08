from tempfile import TemporaryDirectory
from contextlib import contextmanager
import urllib.request
import pyowm
import pygame


def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


class Weather:
    def __init__(self, config, screen):
        self.config = config
        self.screen = screen
        self.weather_icon = None
        self.temperature_text = None
        self.temperature_text2 = None
        self.weather_ico = None
        self.owm = pyowm.OWM(config["api_key"])
        lat, long = config["gps"].split(",")
        lat = float(lat)
        long = float(long)

        self.coords = (lat, long)

        self.prepare()

    def prepare(self):
        self.temperature_text, self.temperature_text2, icon_code = self.get()
        with downloaded_weather_icon(icon_code) as icon_path:
            self.weather_ico = pygame.image.load(icon_path)

    def draw(self):
        theme = self.screen.theme
        font = self.screen.theme.get_font("small", "serif")

        if self.weather_ico and self.temperature_text:
            icon_rect = self.weather_ico.get_rect()

            temperature_text_surface, temperature_rect = text_objects(
                self.temperature_text, font, theme.font_color
            )

            temperature_rect.topleft = icon_rect.topright
            temperature_rect.move_ip(10, 0)

            description_surf, description_rect = text_objects(
                self.temperature_text2, font, theme.font_color
            )

            description_rect.topleft = icon_rect.bottomleft
            description_rect.move_ip(0, 10)

            entire_rect = icon_rect.unionall((temperature_rect, description_rect))

            parent_rect = self.screen.rects[self.config["anchor_to"]["id"]]
            parent_anchor_point = self.config["anchor_to"]["point"].lower()
            anchor_point = self.config["anchor_point"]

            setattr(
                entire_rect, anchor_point, getattr(parent_rect, parent_anchor_point)
            )

            icon_rect.topleft = entire_rect.topleft
            temperature_rect.topright = entire_rect.topright
            description_rect.bottomleft = entire_rect.bottomleft

            self.screen.blit(self.weather_ico, icon_rect)
            self.screen.blit(temperature_text_surface, temperature_rect)
            self.screen.blit(description_surf, description_rect)

    def get(self):
        w = self.owm.weather_at_coords(*self.coords).get_weather()
        temp = round(w.get_temperature("fahrenheit")["temp"], 1)
        desc = w.get_detailed_status()
        icon = w.get_weather_icon_name()
        return f"{ temp }f", desc, icon


@contextmanager
def downloaded_weather_icon(code):
    with TemporaryDirectory() as d:
        yield get_weather_icon(code, d)


def get_weather_icon(code, path="./"):
    url = f"http://openweathermap.org/img/wn/{code}@2x.png"
    urllib.request.urlretrieve(url, f"{path}weather_{code}.png")
    return f"{path}weather_{code}.png"
