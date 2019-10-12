import cryptocompare
from datetime import datetime
from tempfile import TemporaryDirectory
import pygame
from util import set_position
from loguru import logger

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


class Crypto:
    def __init__(self, config, screen):
        self.config = config
        self.screen = screen
        self.coin = self.config.get("coin", "BTC")
        self.img = None
        self.current = None
        self.low = None
        self.high = None
        self.prepare()

    def prepare(self):
        with TemporaryDirectory() as td:
            filename = td + "/pricing.png"
            logger.debug(f"Preparing crypto and saving to {filename}")
            fig_conf = self.config.get("fig", {})
            width = fig_conf.get("width", 500)
            height = fig_conf.get("height", 500)
            fig_alpha = float(fig_conf.get("alpha", 1))
            ax_alpha = float(fig_conf.get("ax_alpha", 1))
            self.current, self.low, self.high = plot_coin(
                self.coin,
                filename=filename,
                x=width,
                y=height,
                fig_alpha=fig_alpha,
                ax_alpha=ax_alpha,
            )
            self.img = pygame.image.load(filename)

    def draw(self):
        if self.img:
            font = self.screen.theme.get_font("extra_small", "sans")
            text = f"{self.coin}: ${round(self.current, 2):,.2f}"
            surface = font.render(text, True, self.screen.theme.get_primary_color())
            text_rect = surface.get_rect()
            img_rect = self.img.get_rect()
            img_rect.topright = text_rect.bottomright

            entire_rect = text_rect.union(img_rect)
            set_position(entire_rect, self.screen.rects, self.config)

            self.screen.rects[self.config.get("id")] = entire_rect

            text_rect.topright = entire_rect.topright
            img_rect.topright = text_rect.bottomright

            self.screen.blit(surface, text_rect)
            self.screen.blit(self.img, img_rect)


def get_btc_prices(coin="BTC"):
    raw = cryptocompare.get_historical_price_minute(coin, "USD", 60)
    for row in raw["Data"]:
        row["time"] = datetime.fromtimestamp(row["time"])
    return raw["Data"]


def get_range(data, accessor):
    minimum_value = min((x[accessor] for x in data))
    maximum_value = max((x[accessor] for x in data))
    return minimum_value, maximum_value


def plot_coin(
    coin="BTC",
    filename="pricing.png",
    show=False,
    x=500,
    y=500,
    fig_alpha=1.0,
    ax_alpha=1.0,
):
    fig = plt.figure()
    dpi = fig.get_dpi()
    fig.set_size_inches(x / float(dpi), y / float(dpi))
    fig.patch.set_alpha(fig_alpha)
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().tick_left()
    ax.get_yaxis().set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
    ax.patch.set_alpha(ax_alpha)

    data = get_btc_prices(coin)

    price_range = get_range(data, "open")
    low, high = price_range
    current = data[-1]["close"]
    plt.ylim(*price_range)
    plt.xlim(*get_range(data, "time"))

    plt.plot([x["time"] for x in data], [x["open"] for x in data], lw=2.5)
    if show:
        plt.show()
    else:
        plt.savefig(filename, transparent=False)
    plt.close(fig)
    return current, low, high


if __name__ == "__main__":
    plot_coin(show=False)
