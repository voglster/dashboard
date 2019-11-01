import pytest
from config_generation import build_stacked_text_config, split_text


def test_draw_text_config_one_line():
    value = build_stacked_text_config("text")
    expected = [
        {
            "name": "static_text",
            "id": "config_text_0",
            "text": "text",
            "position": {
                "anchor_point": "center",
                "anchor_to": {"id": "screen", "point": "center"},
            },
        }
    ]
    assert value == expected


def test_draw_text_config_color():
    value = build_stacked_text_config("text", color="blue")
    expected = [
        {
            "name": "static_text",
            "id": "config_text_0",
            "text": "text",
            "color": "blue",
            "position": {
                "anchor_point": "center",
                "anchor_to": {"id": "screen", "point": "center"},
            },
        }
    ]
    assert value == expected


def test_draw_text_config_font_size():
    value = build_stacked_text_config("text", font_size="humongor")
    expected = [
        {
            "name": "static_text",
            "id": "config_text_0",
            "text": "text",
            "font_size": "humongor",
            "position": {
                "anchor_point": "center",
                "anchor_to": {"id": "screen", "point": "center"},
            },
        }
    ]
    assert value == expected


def test_draw_text_config_two_lines():
    value = build_stacked_text_config(["text", "text2"])
    expected = [
        {
            "name": "static_text",
            "id": "config_text_0",
            "text": "text",
            "position": {
                "anchor_point": "midbottom",
                "anchor_to": {"id": "screen", "point": "center"},
            },
        },
        {
            "name": "static_text",
            "id": "config_text_1",
            "text": "text2",
            "position": {
                "anchor_point": "midtop",
                "anchor_to": {"id": "screen", "point": "center"},
            },
        },
    ]
    assert value == expected


@pytest.mark.parametrize(
    "text,expected",
    [
        (["foo"], ((), "foo", ())),
        (["bar"], ((), "bar", ())),
        ("foo", ((), "foo", ())),
        (["foo", "bar"], (("foo",), None, ("bar",))),
        (["foo", "bar", "baz"], (("foo",), "bar", ("baz",))),
    ],
)
def test_split_text(text, expected):
    assert split_text(text) == expected
