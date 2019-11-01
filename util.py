import os
import platform
from pygame import Rect
from typing import Dict, Tuple, Union, List, Iterable
from math import floor
from itertools import count


def running_on_rpi():
    if platform.system() != "Linux":
        return False
    return os.uname()[4].startswith("arm")


def parse_xy(value: str = None):
    if value is None:
        return 0, 0
    if "," not in value:
        raise (ValueError(f"expected 2 values comma separated but got {value}"))
    x_str, y_str = value.split(",")
    return int(x_str), int(y_str)


def set_position(target_rect: Rect, existing_rects: Dict[str, Rect], config: dict):
    position = config.get("position", {})
    parent_rect_id = position.get("anchor_to", {}).get("id", "screen")
    parent_rect = existing_rects[parent_rect_id]
    parent_anchor_point = position.get("anchor_to", {}).get("point", "topleft").lower()
    anchor_point = position.get("anchor_point", "topleft")

    # Clever but concise, uses the virtual attributes on PyGame's rect object to align
    setattr(target_rect, anchor_point, getattr(parent_rect, parent_anchor_point))

    x, y = parse_xy(position.get("offset"))

    if x or y:
        target_rect.move_ip(x, y)
    return target_rect


named_colors = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "grey": (128, 128, 128),
    "dark_grey": (64, 64, 64),
}


def parse_web_color(original_value: str) -> Tuple[int, int, int]:
    """
    Parsing a hex string into red green a blue components
    :param original_value: the hex tring to parse "#FFFFFF"
    :return: a tuple of ints representing red green and blue
    """
    value = original_value.lstrip("#")
    if len(value) > 6:
        raise ValueError(f"{original_value} is not a valid web color")
    red = int(value[0:2], 16)
    green = int(value[2:4], 16)
    blue = int(value[4:6], 16)
    return red, green, blue


def parse_color(value: Union[str, Tuple[int, int, int]]) -> Tuple[int, int, int]:
    if isinstance(value, str):
        color = named_colors.get(value.casefold())
        if color:
            return color
        if value.startswith("#"):
            return parse_web_color(value)
        if "," in value:
            r, g, b = value.split(",")
            return int(r), int(g), int(b)

        raise ValueError(f"'{value}' is an unknown color")
    # not a string? should be a tuple or list.. just return it
    return value
