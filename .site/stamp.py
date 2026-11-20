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


def head(p, **_):
    return f"""<link rel="icon" href="{p}assets/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#efe9e0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Mona+Sans:wdth,wght@75..125,400..600&family=Geist+Mono:wght@400..500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}assets/system.css">
<link rel="stylesheet" href="{p}assets/ui/cards.css">
<link rel="stylesheet" href="{p}assets/motion/motion.css">
<link rel="stylesheet" href="{p}assets/backgrounds/backgrounds.css">
<link rel="stylesheet" href="{p}assets/layout/layout.css">
<link rel="stylesheet" href="{p}assets/icons/icon.css">
<style>
:root {{
  --p-bg: #efe9e0; --p-surface: #e2d9cb; --p-ink: #22261f; --p-muted: #5a5c53;
  --p-accent: #2e5b44; --p-accent-ink: #ffffff; --p-action: #2e5b44; --p-action-ink: #ffffff;
  --p-inv-bg: #22261f; --p-inv-surface: #2e322a; --p-inv-ink: #efe9e0; --p-inv-muted: #a19e96;
  --p-inv-accent: #efe9e0; --p-inv-accent-ink: #22261f; --p-inv-action: #efe9e0; --p-inv-action-ink: #22261f;
  --font-display: "Mona Sans", system-ui, sans-serif;
  --font-text: "Mona Sans", system-ui, sans-serif;
  --font-mono: "Geist Mono", ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;
  --display-weight: 500;
  --display-tracking: -0.03em;
  --display-tracking-xl: -0.04em;
  --display-stretch: 104%;
  --ly-scale: 0.96;
}}
</style>
<link rel="stylesheet" href="{p}assets/ui/base.css">
<link rel="stylesheet" href="{p}assets/site.css?v={ver("assets/site.css")}">
<script>document.documentElement.classList.add('m-enter');setTimeout(()=>document.documentElement.classList.add('m-enter-done'),700)</script>
<script src="{p}assets/backgrounds/backgrounds.js"></script>
<script>document.documentElement.classList.add('mo-js');setTimeout(()=>document.documentElement.classList.add('mo-safe'),2500)</script>"""


def header(p, current="", **_):
    def cur(name):
        return ' aria-current="page"' if current == name else ""
    return f"""<header class="nav nav--centre">
  <div class="wrap nav__bar">
    <a class="skip-link" href="#top">Skip to content</a>
    <a class="nav__logo" href="/"{cur("home")}><span class="mark" data-mark="ring" aria-hidden="true"></span>Clubhouse Apps</a>
    <nav class="nav__links" aria-label="Main">
      <div class="nav__item">
        <a class="nav__link" href="/#apps"{cur("apps")}>Apps {CHEV}</a>
        <div class="nav__menu">
          <div class="wrap grid">
            <div class="menu-col span-3">
              <p class="t-label">Our apps</p>
              <a href="/dinnerpilot/">DinnerPilot<span>Weekly meal plans and grocery lists for families</span></a>
            </div>
            <div class="menu-col span-3">
              <p class="t-label">DinnerPilot help</p>
              <a href="/dinnerpilot/account/">Account help<span>Password resets and email links</span></a>
              <a href="/dinnerpilot/data-deletion/">Delete your data<span>How to remove your account</span></a>
            </div>
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
    return """<div class="grid">
        <div class="span-4 stack-4">
          <a class="nav__logo" href="/"><span class="mark" data-mark="ring" aria-hidden="true"></span>Clubhouse Apps</a>
          <p class="footer__lede">Apps for everyday life. Websites for local business.</p>
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


def scripts(p, **_):
    return f"""<script type="module" src="{p}assets/system.js"></script>
<script type="module" src="{p}assets/motion/motion.js"></script>
<script type="module" src="{p}assets/layout/layout.js"></script>
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
