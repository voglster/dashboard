from util import parse_xy, parse_color
import pytest


def test_parse_xy_null():
    assert parse_xy() == (0, 0)


def test_parse_xy_float_error():
    with pytest.raises(ValueError):
        parse_xy("0.1, 0.1")


def test_parse_xy_value_error():
    with pytest.raises(ValueError):
        parse_xy("1")


@pytest.mark.parametrize(
    "color,expected",
    [
        ("red", (255, 0, 0)),
        ("#FFFFFF", (255, 255, 255)),
        ("255,255,128", (255, 255, 128)),
    ],
)
def test_parse_color(color, expected):
    assert parse_color(color) == expected


def test_parse_color_bad_name():
    with pytest.raises(ValueError) as excinfo:
        parse_color("foo")
    assert "unknown color" in str(excinfo.value)
