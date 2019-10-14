import pyowm
import pygame
from util import set_position


def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


weather_code_lookup = {
    (200, None): 60200,
    (200, "day"): 60200,
    (200, "night"): 60200,
    (201, None): 60201,
    (201, "day"): 60201,
    (201, "night"): 60201,
    (202, None): 60202,
    (202, "day"): 60202,
    (202, "night"): 60202,
    (210, "day"): 60210,
    (210, "night"): 60210,
    (210, None): 60210,
    (211, "day"): 60211,
    (211, "night"): 60211,
    (211, None): 60211,
    (212, "day"): 60212,
    (212, None): 60212,
    (212, "night"): 60212,
    (221, None): 60221,
    (221, "day"): 60221,
    (221, "night"): 60221,
    (230, "day"): 60230,
    (230, "night"): 60230,
    (230, None): 60230,
    (231, None): 60231,
    (231, "day"): 60231,
    (231, "night"): 60231,
    (232, "day"): 60232,
    (232, "night"): 60232,
    (232, None): 60232,
    (300, None): 60300,
    (300, "day"): 60300,
    (300, "night"): 60300,
    (301, None): 60301,
    (301, "day"): 60301,
    (301, "night"): 60301,
    (302, "day"): 60302,
    (302, "night"): 60302,
    (302, None): 60302,
    (310, None): 60310,
    (310, "day"): 60310,
    (310, "night"): 60310,
    (311, None): 60311,
    (311, "day"): 60311,
    (311, "night"): 60311,
    (312, None): 60312,
    (312, "day"): 60312,
    (312, "night"): 60312,
    (313, None): 60313,
    (313, "day"): 60313,
    (313, "night"): 60313,
    (314, None): 60314,
    (314, "day"): 60314,
    (314, "night"): 60314,
    (321, "day"): 60321,
    (321, "night"): 60321,
    (321, None): 60321,
    (500, "day"): 60500,
    (500, "night"): 60500,
    (500, None): 60500,
    (501, "day"): 60501,
    (501, "night"): 60501,
    (501, None): 60501,
    (502, "day"): 60502,
    (502, "night"): 60502,
    (502, None): 60502,
    (503, "day"): 60503,
    (503, "night"): 60503,
    (503, None): 60503,
    (504, "day"): 60504,
    (504, "night"): 60504,
    (504, None): 60504,
    (511, "day"): 60511,
    (511, "night"): 60511,
    (511, None): 60511,
    (520, "day"): 60520,
    (520, "night"): 60520,
    (520, None): 60520,
    (521, "day"): 60521,
    (521, "night"): 60521,
    (521, None): 60521,
    (522, "day"): 60522,
    (522, "night"): 60522,
    (522, None): 60522,
    (531, "day"): 60531,
    (531, "night"): 60531,
    (531, None): 60531,
    (600, "day"): 60600,
    (600, "night"): 60600,
    (600, None): 60600,
    (601, "day"): 60601,
    (601, "night"): 60601,
    (601, None): 60601,
    (602, "day"): 60602,
    (602, "night"): 60602,
    (602, None): 60602,
    (611, "day"): 60611,
    (611, "night"): 60611,
    (611, None): 60611,
    (612, "day"): 60612,
    (612, "night"): 60612,
    (612, None): 60612,
    (615, "day"): 60615,
    (615, "night"): 60615,
    (615, None): 60615,
    (616, "day"): 60616,
    (616, "night"): 60616,
    (616, None): 60616,
    (620, "day"): 60620,
    (620, "night"): 60620,
    (620, None): 60620,
    (621, "day"): 60621,
    (621, "night"): 60621,
    (621, None): 60621,
    (622, "day"): 60622,
    (622, "night"): 60622,
    (622, None): 60622,
    (701, "day"): 60701,
    (701, "night"): 60701,
    (701, None): 60701,
    (711, "day"): 60711,
    (711, "night"): 60711,
    (711, None): 60711,
    (721, "day"): 60721,
    (721, "night"): 60721,
    (721, None): 60721,
    (731, "day"): 60731,
    (731, "night"): 60731,
    (731, None): 60731,
    (741, "day"): 60741,
    (741, "night"): 60741,
    (741, None): 60741,
    (751, "day"): 60751,
    (751, "night"): 60751,
    (751, None): 60751,
    (761, "day"): 60761,
    (761, "night"): 60761,
    (761, None): 60761,
    (762, "day"): 60762,
    (762, "night"): 60762,
    (762, None): 60762,
    (771, "day"): 60771,
    (771, "night"): 60771,
    (771, None): 60771,
    (781, "day"): 60781,
    (781, "night"): 60781,
    (781, None): 60781,
    (800, "day"): 60800,
    (800, None): 60800,
    (800, "night"): 61800,
    (801, "day"): 60801,
    (801, None): 60801,
    (801, "night"): 61801,
    (802, "day"): 60802,
    (802, None): 60802,
    (802, "night"): 61802,
    (803, "day"): 60803,
    (803, "night"): 60803,
    (803, None): 60803,
    (804, "day"): 60804,
    (804, "night"): 60804,
    (804, None): 60804,
    (900, "day"): 60900,
    (900, "night"): 60900,
    (900, None): 60900,
    (901, "day"): 60901,
    (901, "night"): 60901,
    (901, None): 60901,
    (902, "day"): 60902,
    (902, "night"): 60902,
    (902, None): 60902,
    (903, None): 60903,
    (903, "day"): 60903,
    (903, "night"): 60903,
    (904, "day"): 60904,
    (904, "night"): 60904,
    (904, None): 60904,
    (905, "day"): 60905,
    (905, "night"): 60905,
    (905, None): 60905,
    (906, "day"): 60906,
    (906, None): 60906,
    (906, "night"): 60906,
    (950, "day"): 60950,
    (950, None): 60950,
    (950, "night"): 60950,
    (951, "day"): 60800,
    (951, None): 60800,
    (951, "night"): 61800,
    (952, "day"): 60952,
    (952, "night"): 60952,
    (952, None): 60952,
    (953, "day"): 60953,
    (953, "night"): 60953,
    (953, None): 60953,
    (954, "day"): 60954,
    (954, None): 60954,
    (954, "night"): 60954,
    (955, "day"): 60955,
    (955, "night"): 60955,
    (955, None): 60955,
    (956, None): 60956,
    (956, "day"): 60956,
    (956, "night"): 60956,
    (957, "day"): 60957,
    (957, "night"): 60957,
    (957, None): 60957,
    (958, "day"): 60958,
    (958, "night"): 60958,
    (958, None): 60958,
    (959, "day"): 60959,
    (959, None): 60959,
    (959, "night"): 60959,
    (960, "day"): 60960,
    (960, "night"): 60960,
    (960, None): 60960,
    (961, None): 60961,
    (961, "day"): 60961,
    (961, "night"): 60961,
    (962, "day"): 60962,
    (962, "night"): 60962,
    (962, None): 60962,
}


def arrange_rects(point, icon_rect, temp_rect, description_rect):
    icon_rect.topleft = point
    temp_rect.midleft = icon_rect.midright
    temp_rect.move_ip(10, 0)
    description_rect.topleft = icon_rect.bottomleft
    description_rect.move_ip(0, 10)


class Weather:
    def __init__(self, config, screen):
        self.config = config
        self.screen = screen
        self.weather_icon = None
        self.temperature_text = None
        self.temperature_text2 = None
        self.weather_ico = None
        self.weather_code = None
        self.owm = pyowm.OWM(config["api_key"])
        self.weather_font = pygame.font.Font(
            "./media/fonts/owfont-regular.ttf", config.get("icon_size", 112)
        )
        lat, long = config["gps"].split(",")
        lat = float(lat)
        long = float(long)

        self.coords = (lat, long)

        self.prepare()

    def day_night(self):
        return "day" if 6 < self.screen.local_time.hour < 18 else "night"

    def prepare(self):
        w = self.owm.weather_at_coords(*self.coords).get_weather()
        self.temperature_text = (
            str(int(round(w.get_temperature("fahrenheit")["temp"], 0)))
            + "\N{DEGREE SIGN}F"
        )
        self.temperature_text2 = w.get_detailed_status()
        self.weather_code = weather_code_lookup[
            (w.get_weather_code(), self.day_night())
        ]

    def draw(self):
        theme = self.screen.theme
        font = self.screen.theme.get_font("small", "sans")

        if self.temperature_text and self.weather_code is not None:
            s = self.weather_font.render(chr(self.weather_code), True, (255, 255, 255))
            icon_rect = s.get_rect()

            temperature_text_surface, temperature_rect = text_objects(
                self.temperature_text, font, theme.font_color
            )

            description_surf, description_rect = text_objects(
                self.temperature_text2, font, theme.font_color
            )
            arrange_rects((0, 0), icon_rect, temperature_rect, description_rect)

            entire_rect = icon_rect.unionall((temperature_rect, description_rect))

            entire_rect = set_position(entire_rect, self.screen.rects, self.config)
            self.screen.rects[self.config["id"]] = entire_rect

            arrange_rects(
                entire_rect.topleft, icon_rect, temperature_rect, description_rect
            )

            self.screen.blit(s, icon_rect)
            self.screen.blit(temperature_text_surface, temperature_rect)
            self.screen.blit(description_surf, description_rect)
