from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional


WEIGHT_MAP = {
    "thin": ("Thin", 100),
    "extralight": ("ExtraLight", 200),
    "ultralight": ("ExtraLight", 200),
    "light": ("Light", 300),
    "regular": ("Regular", 400),
    "book": ("Regular", 400),
    "normal": ("Regular", 400),
    "medium": ("Medium", 500),
    "semibold": ("SemiBold", 600),
    "demibold": ("SemiBold", 600),
    "bold": ("Bold", 700),
    "extrabold": ("ExtraBold", 800),
    "ultrabold": ("ExtraBold", 800),
    "heavy": ("ExtraBold", 800),
    "black": ("Black", 900),
    "extrablack": ("Black", 900),
    "ultrablack": ("Black", 900),
}


@dataclass(frozen=True)
class FontFile:
    filename: str
    family: str
    weight_text: str
    weight_num: int
    italic: bool
    suffix: Optional[str]


def split_suffix(stem: str) -> tuple[str, Optional[str]]:
    # Split on the first underscore, if present.
    if "_" in stem:
        main, suffix = stem.split("_", 1)
        return main, suffix
    return stem, None


def parse_style(style: str) -> tuple[str, int, bool]:
    # Detect Italic and map weight as numeric or textual.
    italic = False
    base = style
    if style.lower().endswith("italic"):
        italic = True
        base = style[:-6]  # remove 'Italic'

    base = base or "Regular"
    base_lower = base.lower()

    weight_num = 400
    weight_text = "Regular"

    if base_lower.isdigit():
        weight_num = int(base_lower)
        weight_text = canonical_weight(weight_num)
    else:
        weight_text, weight_num = WEIGHT_MAP.get(base_lower, ("Regular", 400))

    return weight_text, weight_num, italic


def canonical_weight(num: int) -> str:
    if num <= 100:
        return "Thin"
    if num <= 200:
        return "ExtraLight"
    if num <= 300:
        return "Light"
    if num <= 400:
        return "Regular"
    if num <= 500:
        return "Medium"
    if num <= 600:
        return "SemiBold"
    if num <= 700:
        return "Bold"
    if num <= 800:
        return "ExtraBold"
    return "Black"


def parse_google_stem(stem: str, original_filename: str) -> FontFile:
    # Expected format: Family[_suffix]-Style (Style may include Italic).
    family = stem
    suffix: Optional[str] = None
    style = "Regular"

    # First split style after the first '-'.
    if "-" in stem:
        before_dash, style = stem.split("-", 1)
    else:
        before_dash = stem

    # before_dash may contain a suffix separated by '_'.
    family, suffix = split_suffix(before_dash)

    weight_text, weight_num, italic = parse_style(style)

    return FontFile(
        filename=original_filename,
        family=family,
        weight_text=weight_text,
        weight_num=weight_num,
        italic=italic,
        suffix=suffix,
    )


def suggest_from_filename(filename: str) -> FontFile:
    stem = filename.rsplit(".", 1)[0]
    return parse_google_stem(stem, filename)


def parse_all(ttf_files: Iterable[str]) -> list[FontFile]:
    return [suggest_from_filename(name) for name in ttf_files]


def family_suffixes(fonts: Iterable[FontFile]) -> dict[str, set[str]]:
    suffixes: dict[str, set[str]] = {}
    for f in fonts:
        fam_set = suffixes.setdefault(f.family, set())
        if f.suffix:
            fam_set.add(f.suffix)
    return suffixes


def build_output_name(font: FontFile, use_numeric: bool, drop_suffix: bool) -> str:
    weight_label = str(font.weight_num) if use_numeric else font.weight_text
    if font.italic:
        weight_label = f"{weight_label}Italic"

    name = f"{font.family}-{weight_label}"
    if font.suffix and not drop_suffix:
        name = f"{name}_{font.suffix}"
    return name
