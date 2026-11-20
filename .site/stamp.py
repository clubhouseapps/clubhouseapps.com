#!/usr/bin/env python3
"""Stamp the shared head, header, footer links and scripts into every page.

Every page carries marker pairs such as
    <!-- site:header current=apps --> ... <!-- /site:header -->
and this script rewrites what sits between them, so the eight copies of the header and footer
stay identical. Edit the blocks below, then run from the Website folder:

    python3 .site/stamp.py

Run it after every change to assets/site.css too: it stamps the file's fingerprint into the link (?v=...),
so browsers fetch the new version instead of a cached one.

The site has no build step: the stamped HTML is what gets committed and served.
Asset paths are relative (../ per folder level); page links are root-absolute (/studio/).
"""
import hashlib
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = [
    "index.html",
    "dinnerpilot/index.html",
    "dinnerpilot/privacy/index.html",
    "dinnerpilot/terms/index.html",
    "dinnerpilot/data-deletion/index.html",
    "dinnerpilot/account/index.html",
    "studio/index.html",
    "samples/index.html",
]

def ver(rel):
    """A short fingerprint of a file, added to its link as ?v=... The host lets browsers cache CSS for
    4 hours, so without it a returning visitor gets new pages with the old stylesheet. Re-stamp after
    every change to site.css."""
    return hashlib.md5((ROOT / rel).read_bytes()).hexdigest()[:8]


CHEV = ('<svg class="chev" viewBox="0 0 12 12" aria-hidden="true"><path d="M3 4.5l3 3 3-3" fill="none" '
        'stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def head(p, scene="", **_):
    """The shared head: favicon, the Night shift palette (blue-black, cornflower accent) and type (Reddit Sans,
    JetBrains Mono), the kit's stylesheets, then site.css. A page with a scroll scene marks it in its marker:
    <!-- site:head scene=letter-physics --> adds the scene's early line and both of its stylesheets."""
    scene_lines = ""
    if scene:
        scene_lines = f"""
<script>document.documentElement.classList.add('sc-js');setTimeout(()=>document.documentElement.classList.add('sc-safe'),2500)</script>
<link rel="stylesheet" href="{p}assets/scenes/scenes.css">
<link rel="stylesheet" href="{p}assets/scenes/{scene}/scene.css">"""
    return f"""<link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#0a0d14">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Reddit+Sans:wght@400..700&family=JetBrains+Mono:wght@400..500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}assets/system.css">
<link rel="stylesheet" href="{p}assets/ui/cards.css">
<link rel="stylesheet" href="{p}assets/motion/motion.css">
<link rel="stylesheet" href="{p}assets/backgrounds/backgrounds.css">
<link rel="stylesheet" href="{p}assets/layout/layout.css">
<link rel="stylesheet" href="{p}assets/icons/icon.css">
<style>
:root {{
  --p-bg: #0a0d14; --p-surface: #131824; --p-ink: #e9edf3; --p-muted: #8891a1;
  --p-accent: #5ab9fc; --p-accent-ink: #0a0d14; --p-action: #5ab9fc; --p-action-ink: #0a0d14;
  --p-inv-bg: #e9edf3; --p-inv-surface: #d7dbe1; --p-inv-ink: #0a0d14; --p-inv-muted: #54575f;
  --p-inv-accent: #0a0d14; --p-inv-accent-ink: #e9edf3; --p-inv-action: #0a0d14; --p-inv-action-ink: #e9edf3;
  --font-display: "Reddit Sans", system-ui, sans-serif;
  --font-text: "Reddit Sans", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;
  --display-weight: 500;
  --display-tracking: -0.03em;
  --display-tracking-xl: -0.04em;
}}
</style>
<link rel="stylesheet" href="{p}assets/ui/base.css">
<link rel="stylesheet" href="{p}assets/site.css?v={ver("assets/site.css")}">
<script>document.documentElement.classList.add('m-enter');setTimeout(()=>document.documentElement.classList.add('m-enter-done'),700)</script>
<script src="{p}assets/backgrounds/backgrounds.js"></script>
<script>document.documentElement.classList.add('mo-js');setTimeout(()=>document.documentElement.classList.add('mo-safe'),2500)</script>{scene_lines}"""


MARK_C = '<span class="mark mark--initial" aria-hidden="true">C</span>'


def header(p, current="", **_):
    def cur(name):
        return ' aria-current="page"' if current == name else ""
    return f"""<header class="nav">
  <div class="wrap nav__bar">
    <a class="skip-link" href="#top">Skip to content</a>
    <a class="nav__logo" href="/"{cur("home")}>{MARK_C}Clubhouse Apps</a>
    <nav class="nav__links" aria-label="Main">
      <div class="nav__item">
        <a class="nav__link" href="/#apps"{cur("apps")}>Apps {CHEV}</a>
        <div class="nav__menu">
          <div class="wrap grid">
            <div class="menu-col span-3">
              <p class="t-label">DinnerPilot</p>
              <a href="/dinnerpilot/">Meal plans<span>A family&rsquo;s week inside its budget</span></a>
              <a href="/dinnerpilot/#features">Grocery list<span>Every item, an estimated total</span></a>
              <a href="/dinnerpilot/#pantry">Pantry Chef<span>Dinner from your fridge</span></a>
            </div>
            <div class="menu-col span-3">
              <p class="t-label">DinnerPilot help</p>
              <a href="/dinnerpilot/account/">Account help<span>Password resets and email links</span></a>
              <a href="/dinnerpilot/data-deletion/">Delete your data<span>How to remove your account</span></a>
              <a href="/dinnerpilot/privacy/">Privacy policy<span>What the app stores</span></a>
            </div>
            <a class="menu-card span-3 start-10" href="/dinnerpilot/">
              <div class="panel"><img class="frame__img" src="{p}assets/dp/budget.webp" alt="DinnerPilot showing a week on track at $224 of a $250 budget" loading="lazy"></div>
              <span class="t-card">DinnerPilot</span>
              <span class="t-small muted">In TestFlight for iPhone now</span>
            </a>
          </div>
        </div>
      </div>
      <div class="nav__item"><a class="nav__link" href="/studio/"{cur("studio")}>Studio</a></div>
      <div class="nav__item"><a class="nav__link" href="/#about"{cur("about")}>About</a></div>
    </nav>
    <div class="nav__actions">
      <a class="btn btn--primary" href="/#contact">Get in touch</a>
    </div>
    <button class="nav__toggle" type="button" aria-expanded="false" aria-label="Menu">
      <svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><path d="M2 5h14M2 13h14" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
    </button>
  </div>
</header>"""


def footer_links(p, **_):
    return f"""<div class="grid">
        <div class="span-4 stack-4">
          <a class="nav__logo" href="/">{MARK_C}Clubhouse Apps</a>
          <p class="footer__lede">iPhone apps for families. Websites for local business.</p>
        </div>
        <div class="span-2 start-5 footer__col"><h3>Apps</h3><ul><li><a href="/dinnerpilot/">DinnerPilot</a></li><li><a href="/dinnerpilot/#pantry">Pantry Chef</a></li><li><a href="/dinnerpilot/account/">Account help</a></li></ul></div>
        <div class="span-2 footer__col"><h3>Studio</h3><ul><li><a href="/studio/">Websites</a></li><li><a href="/studio/#pricing">Pricing</a></li><li><a href="/studio/#contact">Get a quote</a></li></ul></div>
        <div class="span-2 footer__col"><h3>Company</h3><ul><li><a href="/#about">About</a></li><li><a href="/#contact">Contact</a></li></ul></div>
        <div class="span-2 footer__col"><h3>Legal</h3><ul><li><a href="/dinnerpilot/privacy/">Privacy policy</a></li><li><a href="/dinnerpilot/terms/">Terms of service</a></li><li><a href="/dinnerpilot/data-deletion/">Delete your data</a></li></ul></div>
      </div>
      <div class="footer__legal">
        <span>&copy; 2026 Clubhouse Apps LLC</span>
        <div class="socials"></div>
      </div>"""


def scripts(p, scene="", **_):
    """The kit's runtimes and site.js. <!-- site:scripts scene=1 --> adds the scroll scenes' runtime."""
    extra = f'\n<script type="module" src="{p}assets/scenes/scenes.js"></script>' if scene else ""
    return f"""<script type="module" src="{p}assets/system.js"></script>
<script type="module" src="{p}assets/motion/motion.js"></script>
<script type="module" src="{p}assets/layout/layout.js"></script>{extra}
<script type="module" src="{p}assets/site.js?v={ver("assets/site.js")}"></script>"""


BLOCKS = {"head": head, "header": header, "footer-links": footer_links, "scripts": scripts}
MARK = re.compile(r"(?P<open><!-- site:(?P<name>[\w-]+)(?P<args>[^>]*?)-->)(?P<body>.*?)(?P<close><!-- /site:(?P=name) -->)", re.S)


def stamp(path):
    rel = path.relative_to(ROOT)
    prefix = "../" * (len(rel.parts) - 1)
    text = path.read_text()

    def sub(m):
        args = dict(a.split("=", 1) for a in m["args"].split())
        body = BLOCKS[m["name"]](prefix, **args)
        return f"{m['open']}\n{body}\n{m['close']}"

    out, n = MARK.subn(sub, text)
    if out != text:
        path.write_text(out)
    print(f"{rel}: {n} blocks")


if __name__ == "__main__":
    for page in PAGES:
        stamp(ROOT / page)
