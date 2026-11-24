#!/usr/bin/env python3
"""Make the web copies of the DinnerPilot screenshots the site shows.

Source: ../../DinnerPilot/Brand Assets/Screenshots - build 58 (full set)/ (the current set, TestFlight build 58), and the Studio's
Sparky's Electric sample captured from its live preview by .site/capture.mjs (.site/captures/).
Output: assets/dp/*.webp and assets/studio/*.webp, sized for 2x screens. Run from the Website folder after the
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
SRC = ROOT.parent.parent / "DinnerPilot" / "Brand Assets" / "Screenshots - build 58 (full set)"
LOGO = ROOT.parent.parent / "DinnerPilot" / "Brand Assets" / "Logo" / "DinnerPilot app icon 1024.png"
OUT = ROOT / "assets" / "dp"
STUDIO = ROOT / "assets" / "studio"
SPARKYS = ROOT / ".site" / "captures" / "sparkys-mobile.png"  # 440 x 902 at 3x, from capture.mjs
SPARKYS_DESK = ROOT / ".site" / "captures" / "sparkys-desktop.png"  # 1280 x 800 at 2x

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


def save(im, name, width, out=OUT):
    h = round(im.height * width / im.width)
    im.resize((width, h), Image.LANCZOS).save(out / f"{name}.webp", "WEBP", quality=82, method=6)
    print(f"{name}.webp  {width}x{h}  {(out / f'{name}.webp').stat().st_size // 1024} KB")


def phone_frame(page):
    """A web page as a phone screen: a dark status bar with the Dynamic Island above it, the same
    1320 x 2868 proportions as the app screenshots, so it sits in the same .ph--shot frame."""
    page = page.convert("RGB").resize((1320, 2706), Image.LANCZOS)
    screen = Image.new("RGB", (1320, 2868), (17, 17, 16))
    screen.paste(page, (0, 162))
    ImageDraw.Draw(screen).rounded_rectangle((472, 33, 848, 144), radius=56, fill=(0, 0, 0))
    return screen


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for out, src in PHONES.items():
        save(load(src), out, 660)
    for out, (src, box) in SLICES.items():
        save(load(src).crop(box), out, 820)
    if SPARKYS.exists():
        STUDIO.mkdir(parents=True, exist_ok=True)
        save(phone_frame(Image.open(SPARKYS)), "sparkys-phone", 660, STUDIO)
    if SPARKYS_DESK.exists():
        STUDIO.mkdir(parents=True, exist_ok=True)
        save(Image.open(SPARKYS_DESK).convert("RGB"), "sparkys-desktop", 1280, STUDIO)
    icon = Image.open(LOGO).convert("RGB").resize((128, 128), Image.LANCZOS)
    icon.save(ROOT / "assets" / "dp-icon.png", optimize=True)
    print("dp-icon.png  128x128")
