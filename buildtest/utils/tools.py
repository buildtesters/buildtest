from functools import reduce

from rich.color import Color, ColorParseError


def deep_get(dictionary, *keys):
    return reduce(
        lambda d, key: d.get(key, None) if isinstance(d, dict) else None,
        keys,
        dictionary,
    )


def checkColor(colorArg):
    """Checks the provided colorArg against the compatible colors from Rich.Color"""
    if not colorArg:
        return Color.default().name

    if isinstance(colorArg, Color):
        return colorArg.name

    if colorArg and isinstance(colorArg, list):
        colorArg = colorArg[0]
        return colorArg
    if isinstance(colorArg, str):
        try:
            checkedColor = Color.parse(colorArg).name
        except ColorParseError:
            checkedColor = Color.default().name
        return checkedColor
