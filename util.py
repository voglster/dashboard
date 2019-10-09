import os
import platform


def running_on_rpi():
    if platform.system() != "Linux":
        return False
    return os.uname()[4].startswith("arm")


def set_position(rect, existing_rects, config):
    position = config.get("position", {})
    parent_rect_id = position.get("anchor_to", {}).get("id", "screen")
    parent_rect = existing_rects[parent_rect_id]
    parent_anchor_point = position.get("anchor_to", {}).get("point", "topleft").lower()
    anchor_point = position.get("anchor_point", "topleft")

    # Clever but concise, uses the virtual attributes on PyGame's rect object to align
    setattr(rect, anchor_point, getattr(parent_rect, parent_anchor_point))

    offset_str = position.get("offset", "0, 0")
    x_str, y_str = offset_str.split(",")
    x = int(x_str)
    y = int(y_str)

    if x or y:
        rect = rect.move(x, y)
    return rect


color_lookup = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
}


def parse_color(value):
    if isinstance(value, str):
        # its a string lets see if its in lookup
        color = color_lookup.get(value.casefold())
        if color:
            return color
        if value.startswith("#"):
            # web based color
            return tuple(int(value.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4))
        # expecting a comma separated list
        return tuple((int(x) for x in value.split(",")))
    # not a string? should be a tuple or list.. just return it
    return value
