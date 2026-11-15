#!/usr/bin/env python3
"""Make the web copies of the DinnerPilot screenshots the site shows.

Source: ../Brand Assets/DinnerPilot Screenshots/ (the current set, TestFlight build 58).
Output: assets/dp/*.webp, sized for 2x screens. Run from the Website folder after the
screenshots are retaken:

    python3 .site/shots.py

Rules from the screenshot guide that this script follows:
- Only the current set is used, never _archive/.
- The small "AI" tags on Pantry Chef's results (shot 30) are painted over with the card colour;
  marketing does not say "AI".
- No fish dishes: the shots chosen here have none.
"""
import pathlib
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT.parent / "Brand Assets" / "DinnerPilot Screenshots"
LOGO = ROOT.parent / "Brand Assets" / "DinnerPilot Logo" / "DinnerPilot app icon 1024.png"
OUT = ROOT / "assets" / "dp"

# Whole screens, shown inside a phone bezel about 312px wide, so 660px covers 2x.
PHONES = {
    "home-week": "08_home-week-on-track",
    "week-mon-wed": "09_home-week-monday-to-wednesday",
    "week-fri-sun": "10_home-week-friday-to-sunday",
    "grocery-list": "18_grocery-list-summary",
    "swap-dinner": "14_swap-a-meal",
    "pantry-chef": "30_pantry-chef-recipe-ideas",
}

# Strips of one screen (left, top, right, bottom in the 1320 x 2868 original), shown as floating cards.
SLICES = {
    "budget": ("08_home-week-on-track", (0, 190, 1320, 1290)),
    "grocery-total": ("18_grocery-list-summary", (0, 1010, 1320, 1790)),
    "dinner-time": ("42_profile-shopping-dinner-time-saved", (0, 1205, 1320, 1890)),
    "dietary": ("37_profile-family-and-diet", (0, 700, 1320, 1720)),
    "traditions": ("39_profile-family-traditions", (0, 975, 1320, 1910)),
}

# Shot 30's "AI" tags, one per recipe row.
AI_TAGS = [(1108, 888, 1216, 948), (1108, 1248, 1216, 1308), (1108, 1606, 1216, 1666)]


def load(name):
    im = Image.open(SRC / f"{name}.png").convert("RGB")
    if name.startswith("30_"):
        d = ImageDraw.Draw(im)
        for box in AI_TAGS:
            d.rectangle(box, fill=im.getpixel((box[0] - 14, (box[1] + box[3]) // 2)))
    return im


def save(im, name, width):
    h = round(im.height * width / im.width)
    im.resize((width, h), Image.LANCZOS).save(OUT / f"{name}.webp", "WEBP", quality=82, method=6)
    print(f"{name}.webp  {width}x{h}  {(OUT / f'{name}.webp').stat().st_size // 1024} KB")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for out, src in PHONES.items():
        save(load(src), out, 660)
    for out, (src, box) in SLICES.items():
        save(load(src).crop(box), out, 820)
    icon = Image.open(LOGO).convert("RGB").resize((128, 128), Image.LANCZOS)
    icon.save(ROOT / "assets" / "dp-icon.png", optimize=True)
    print("dp-icon.png  128x128")
