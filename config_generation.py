from math import floor
from itertools import count
from typing import List, Union, Iterable


def single_text(
    text_id,
    text,
    anchor_point="center",
    parent="screen",
    point="center",
    color=None,
    font_size=None,
):
    ret = {
        "name": "static_text",
        "id": text_id,
        "text": text,
        "position": {
            "anchor_point": anchor_point,
            "anchor_to": {"id": parent, "point": point},
        },
    }
    if color:
        ret["color"] = color
    if font_size:
        ret["font_size"] = font_size
    return ret


def split_text(text):
    if not text:
        return (), None, ()
    if isinstance(text, str):
        return (), text, ()
    middle_index = floor(len(text) / 2)
    top_half = tuple(text[i] for i in reversed(range(0, middle_index)))

    if len(text) % 2 == 0:
        # when even bottom includes middle index, and middle is none
        bottom_half = tuple(text[i] for i in range(middle_index, len(text)))
        middle = None
    else:
        # when odd there is a middle entity and bottom skips it
        bottom_half = tuple(text[i] for i in range(middle_index + 1, len(text)))
        middle = text[middle_index]
    return top_half, middle, bottom_half


class StackedTextBuilder:
    def __init__(self, id_prefix, parent, point, color, font_size):
        self.id_prefix = id_prefix
        self.parent = parent
        self.point = point
        self.color = color
        self.font_size = font_size
        self.top_parent = None
        self.top_point = None
        self.bot_parent = None
        self.bot_point = None
        self.prefix_index = None

    def reset(self):
        self.top_parent = self.parent
        self.top_point = self.point
        self.bot_parent = self.parent
        self.bot_point = self.point
        self.prefix_index = count()

    def next_rect_id(self):
        return f"{self.id_prefix}_{next(self.prefix_index)}"

    def centered(self, text):
        rect_id = self.next_rect_id()
        ret = single_text(
            text_id=rect_id,
            text=text,
            anchor_point="center",
            parent=self.parent,
            point=self.point,
            color=self.color,
            font_size=self.font_size,
        )
        self.top_parent, self.top_point = rect_id, "midtop"
        self.bot_parent, self.bot_point = rect_id, "midbottom"
        return ret

    def stack_top(self, text):
        rect_id = self.next_rect_id()
        ret = single_text(
            text_id=rect_id,
            text=text,
            anchor_point="midbottom",
            parent=self.top_parent,
            point=self.top_point,
            color=self.color,
            font_size=self.font_size,
        )
        self.top_parent = rect_id
        return ret

    def stack_bottom(self, text):
        rect_id = self.next_rect_id()
        ret = single_text(
            text_id=rect_id,
            text=text,
            anchor_point="midtop",
            parent=self.bot_parent,
            point=self.bot_point,
            color=self.color,
            font_size=self.font_size,
        )
        self.bot_parent = rect_id
        return ret

    def process(self, text) -> List[dict]:
        self.reset()
        top, middle, bottom = split_text(text)
        ret = []
        if middle:
            ret.append(self.centered(middle))
        for line in top:
            ret.append(self.stack_top(line))
        for line in bottom:
            ret.append(self.stack_bottom(line))
        return ret


def build_stacked_text_config(
    text: Union[str, List[str]],
    parent: str = "screen",
    point: str = "center",
    id_prefix: str = "config_text",
    color: str = None,
    font_size: str = None,
) -> Iterable[dict]:
    if isinstance(text, str):
        text = [text]

    stacked_text_builder = StackedTextBuilder(
        id_prefix, parent, point, color, font_size
    )
    return stacked_text_builder.process(text)


black_background = {"name": "color_bg", "id": "bg1"}
not_connected_top = {
    "name": "static_text",
    "id": "noconn_0",
    "color": "dark_grey",
    "font_size": "extra_small",
    "text": "Not connected",
    "position": {
        "anchor_point": "midtop",
        "anchor_to": {"id": "screen", "point": "midtop"},
    },
}
not_connected_bot = {
    "name": "static_text",
    "id": "noconn_1",
    "color": "dark_grey",
    "font_size": "extra_small",
    "text": "Not connected",
    "position": {
        "anchor_point": "midbottom",
        "anchor_to": {"id": "screen", "point": "midbottom"},
    },
}
offline_and_missing_config = {
    "qboard": {"load_remote": True},
    "modules": [
        black_background,
        not_connected_top,
        not_connected_bot,
        *build_stacked_text_config(
            [
                "error: no config found",
                "cannot connect to server",
                "or missing settings.yml",
            ],
            color="red",
            font_size="small",
        ),
    ],
}
