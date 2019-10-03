import cryptocompare
from datetime import datetime

import matplotlib.pyplot as plt

low, high, current = 0, 0, 0


def get_btc_prices():
    raw = cryptocompare.get_historical_price_minute("BTC", "USD", 60)
    for row in raw["Data"]:
        row["time"] = datetime.fromtimestamp(row["time"])
    return raw["Data"]


def get_range(data, accessor):
    minimum_value = min((x[accessor] for x in data))
    maximum_value = max((x[accessor] for x in data))
    return minimum_value, maximum_value


def plot_btc(filename="pricing.png", show=False):
    fig = plt.figure(figsize=(6.7, 5))
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)

    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    data = get_btc_prices()

    price_range = get_range(data, "open")
    global low
    global high
    global current
    low, high = price_range
    current = data[-1]["close"]
    plt.ylim(*price_range)
    plt.xlim(*get_range(data, "time"))

    plt.plot([x["time"] for x in data], [x["open"] for x in data], lw=2.5)
    if show:
        plt.show()
    else:
        plt.savefig(filename)
    plt.close(fig)


if __name__ == "__main__":
    plot_btc(show=False)
