# ClubhouseApps.com — Complete Site Guide

Everything an AI (or human) needs to understand, maintain, and update this website.

---

## Overview

**clubhouseapps.com** is the public website for Clubhouse Apps, the parent company. Everything sits under
it in one site with one look:

1. **Apps**: DinnerPilot (the first app), with its product page and its help and legal pages
2. **Studio**: Clubhouse Apps Studio, which builds websites for local businesses

The site is pure static HTML and CSS plus the Taste Skill kit's own scripts. No framework, no build step,
no package manager. Every file you see is exactly what gets served to the browser.

### Site map

| URL | Page | Notes |
|-----|------|-------|
| `/` | Clubhouse Apps home | Apps, Studio, About, contact |
| `/dinnerpilot/` | DinnerPilot product page | Launch sign-up form (Formspree `maeezoew`) |
| `/dinnerpilot/privacy/` | Privacy policy | Text page |
| `/dinnerpilot/terms/` | Terms of service | Text page |
| `/dinnerpilot/data-deletion/` | Data deletion policy | Text page; Apple requires it |
| `/dinnerpilot/account/` | Account help | Where DinnerPilot account emails lead (password reset, email confirmed); `noindex` |
| `/studio/` | Studio: websites for local businesses | Quote form (Formspree `mlgvvbay`) |
| `/samples/` | Internal sample library | `noindex, nofollow`; **never link it from a public page** |

### Navigation (identical on every page)

- **Header:** Clubhouse Apps logo (home) · **Apps** (menu: DinnerPilot; DinnerPilot help) · **Studio** · **About** · button **Get in touch** (to the home page's contact close).
- **Footer:** the company line, then four columns: **Apps** (DinnerPilot, Pantry Chef, Account help) · **Studio** (Websites, Pricing, Get a quote) · **Company** (About, Contact) · **Legal** (Privacy policy, Terms of service, Delete your data). Legal row: © 2026 Clubhouse Apps LLC.

Every label appears once. Don't add a second link with the same words, and don't link `/samples/`.

---

## Hosting

### GitHub Pages

The site is hosted on **GitHub Pages** — GitHub's free static site hosting service.

- **Repository:** `https://github.com/clubhouseapps/clubhouseapps.com`
- **Branch:** `main` (GitHub Pages serves directly from this branch)
- **Local path:** `~/Desktop/ClubhouseApps/Website/`

### How deployment works

There is no build step and no CI pipeline. Deployment is:

1. Edit files locally
2. `git add` the changed files
3. `git commit -m "description"`
4. `git push origin main`

GitHub Pages picks up the push automatically and the live site updates within ~60 seconds. No dashboard to open, no deploy button to click.

### Custom domain

The file `CNAME` in the repo root contains `clubhouseapps.com`. This is how GitHub Pages knows to serve the site at that domain instead of the default `clubhouseapps.github.io` URL.

**DNS is configured separately** (in the domain registrar's DNS settings, not in this repo). The DNS A records point to GitHub Pages' servers. If you need to change the domain, update both the `CNAME` file and the DNS records.

### Email

Contact email referenced throughout the site: `dave@clubhouseapps.com`

---

## Repository

```
clubhouseapps.com/          ← repo root
├── CNAME                   ← custom domain declaration
├── index.html              ← Clubhouse Apps home (/)
├── .site/stamp.py          ← stamps the shared head, header, footer and scripts into every page
├── .site/shots.py          ← makes assets/dp/ and assets/studio/ from the real screenshots and captures
├── .site/capture.mjs       ← captures a live web page as a phone or desktop browser shows it
├── .site/captures/         ← the raw Sparky's Electric captures shots.py frames
├── assets/
│   ├── site.css            ← the site's own CSS: phone frame, Studio mocks, pricing, text-page layout
│   ├── dp/                 ← DinnerPilot screenshots, web-sized (made by .site/shots.py; don't edit by hand)
│   ├── studio/             ← Sparky's Electric captures, web-sized (made by .site/shots.py)
│   ├── system.css/js, ui/, motion/, layout/, backgrounds/, moments/, effects/, icons/
│   │                       ← the Taste Skill kit (never edit these; only requested files are committed)
│   ├── dp-icon.png, favicon.svg
│   └── shared.css          ← the OLD stylesheet; no page uses it any more (safe to delete with Dave's OK)
├── dinnerpilot/
│   ├── index.html          ← DinnerPilot product page
│   ├── privacy/ terms/ data-deletion/ account/   ← text pages
├── studio/index.html       ← Studio service page
└── samples/index.html      ← internal, unlinked, noindex
```

URL structure mirrors folder structure exactly. `index.html` files serve as the default for each folder.

---

## Commit History

| Date | Hash | Description |
|------|------|-------------|
| 2026-05-16 | `5bedc1a` | Initial site — ClubhouseApps.com + DinnerPilot landing page |
| 2026-05-16 | `12f6686` | Create CNAME (added custom domain) |
| 2026-05-17 | `34288cf` | Add Privacy Policy, Terms of Service, Data Deletion pages; update footers |
| 2026-05-17 | `3403e0d` | Move legal pages under /dinnerpilot/ to reflect org structure |
| 2026-05-17 | `9599ff0` | Full visual redesign — modern, premium look |
| 2026-11-13 | `ab5e7e6` | Homepage rebuilt with the Taste Skill kit |
| 2026-11-14 | `4d9ebbf` | Whole site rebuilt as one: parent-company home, every page on the same kit, shared header and footer |
| 2026-11-14 | `f9d8015` | Every DinnerPilot picture is now a real app screenshot (build 58) instead of a drawn mock |
| 2026-11-14 | `a1482ae` | DinnerPilot hero: grocery card hidden below 1024px |
| 2026-11-14 | `607b0d4` | Home hero: two labelled real phones; Sparky's captured from the live preview; stylesheet fingerprint |
| 2026-11-19 | `1f81d4a` | Impeccable's three real findings fixed |
| 2026-11-19 | `c64ef8e` | Five animations from the web-animations gallery (three didn't run live: their files weren't committed) |
| 2026-11-19 | `2c6f335` | The three missing animation files committed; DinnerPilot gradient sped up |
| 2026-11-19 | `586984b` | DinnerPilot gradient made faster and deeper so the drift shows beside the phone |
| 2026-11-20 | 15fc34a | Whole site redone in the "Night shift" look (Dave chose it from three home-page previews): new colours, type, header, footer, every page rebuilt |

The major work happened on **2026-05-17**: legal pages were added, then immediately reorganized under `/dinnerpilot/` (they had initially been at the root), then the entire site got a full visual redesign in one large commit that touched all three primary files.

---

## Design System

Every page uses the **Taste Skill** kit (`github.com/Leonxlnx/taste-skill`) with one look, **"Night shift"**
(Dave chose it on 2026-11-20 from three home-page previews; the earlier clay-pine look's favicon and share image
are in `../_archive/2026-11-20 site overhaul/`): blue-black ground `#0a0d14`, surface `#131824`, cornflower accent
`#5ab9fc` (palette blue-black-cornflower), Reddit Sans + JetBrains Mono, tonal buttons, the "C" initial mark, soft
corners (`data-radius="soft"`), and the sky lit ground (`data-ground="sky"`: the light blue-grey panels the phones
stand on). Header: nav-mega (the Apps menu opens a panel with a DinnerPilot card). Footer: footer-dark with the
company name set huge across the close (`close--word`). The tokens live in the `site:head` block that `stamp.py`
writes into every page; change them there, then re-stamp. A page with a scroll scene marks it in its markers:
`<!-- site:head scene=letter-physics -->` and `<!-- site:scripts scene=1 -->`.
- **One effect a page** (the kit's rule): a live shader ground, or a big scroll scene, never both on one page.

- **Kit files** (`assets/system.css`, `assets/ui/…`, etc.) are never edited. Override in `assets/site.css` or a page's own `<style>`.
- **`assets/site.css`** holds what the kit doesn't: the phone frame (`.ph`; `.ph--shot` holds a real screenshot), the screenshot strip card (`.shot`), the Studio's step card (`.dpn`), the browser window with the Sparky's Electric sample (`.bw`, `.sp__*`), the pricing halves (`.pricing`), and the text-page layout (`.doc`, `.prose`, `.doc__side`).
- **Page `<style>` blocks** only position each hero's pieces and set panel heights per breakpoint (the kit sizes every section to whole screens).
- **Real screenshots only** for DinnerPilot. Every app screen on the site comes from
  `../Brand Assets/DinnerPilot Screenshots/` (TestFlight build 58). Never draw the app in HTML: drawn mocks
  don't look like the real app. `.site/shots.py` picks the shots, crops the strips used in #features, paints
  over Pantry Chef's small "AI" tags (marketing doesn't say "AI"), and writes `assets/dp/*.webp` at 2x. After
  the app's look changes and the screenshots are retaken, run `python3 .site/shots.py`. Follow the
  screenshot guide's rules: prices are "estimated", Pantry Chef is "with Pro" (not in the free trial), no fish
  dishes.
- **Sparky's Electric is real too**: the Studio sample is captured from its live preview
  (`node .site/capture.mjs <url> .site/captures/sparkys-mobile.png 440 902 3`, and `... sparkys-desktop.png 1280 800 2`),
  then `python3 .site/shots.py` frames it. Recapture after the sample site changes.
- **The home hero** is a collage of real screens on a moving aurora: every few seconds it turns between
  DinnerPilot's screens and Sparky's Electric (desktop and phone), four sets in all (the kit's `ly-collage` sets).
- **Motion** follows design-motion-principles: one entrance per hero, at most one timed loop per page, hover
  answers on every link; all of it stops under reduced motion and on touch screens where it follows the pointer.
- **Animations** (Night shift, 2026-11-20; each page has one effect, as the kit allows):
  | Where | What | How |
  |---|---|---|
  | Home hero | Curtains of blue light sway behind a collage that turns between DinnerPilot's screens and Sparky's Electric | effect `aurora-curtains` on `.ly-collage` (`data-fx`) + the kit's collage sets |
  | Home `#how` | The section holds while you scroll; its three steps (grocery list, meal swap, Pantry Chef) change the phone | kit moment `pinned-chapters` (dealt by `moments.mjs pick`) |
  | DinnerPilot `#claim` | "One app, one job." flies apart letter by letter; "DinnerPilot fits a week of meals to your grocery budget." lands | kit scene `letter-physics` (the page's one effect, so no shader ground on that page; card panels use the lit ground) |
  | Studio hero | A soft dark grain gradient drifts behind the browser window; the project card ticks off its three steps | effect `grain-gradient` (dealt by `effects.mjs pick`) + `data-ly-steps` |
  | Studio `#services` | A slow row of the trades we build for (pause button beside its label; hidden on phones) | kit moment `marquee-row` |
  | Pricing on home, DinnerPilot and Studio | One soft cornflower glow follows the pointer across the plans | `[data-spot]` + `assets/site.js` + `site.css` |
  Retired with the clay-pine look: cursor-spotlight, liquid-type, word-highlight (letter-physics avoids it) and the
  DinnerPilot gradient-mesh. Their files stay in git, unused. No client logos in the marquee until real clients approve them.
- **Most of the kit is not committed.** `assets/moments/`, `assets/effects/` and `assets/components/` sit in this folder
  in full, but only the pieces a page uses are in git. When a page starts using a moment or effect, `git add` its
  `moment.js` + `moment.css` (or `effect.js`) too, or it works on this computer and is missing on the live site.
  Before a push, test from a copy of exactly what git holds (`git checkout-index -a --prefix=<empty folder>/`, then
  serve that folder); after a push, open each changed live page and confirm nothing it loads comes back 404.

### Shared header and footer: `.site/stamp.py`

The header, footer links, `<head>` assets and scripts are written into every page between marker comments
(`<!-- site:header current=apps -->` … `<!-- /site:header -->`). To change the nav or footer, edit the
blocks in `.site/stamp.py` and run:

```bash
python3 .site/stamp.py
```

**Run it after every change to `assets/site.css` too.** The host lets browsers keep CSS for 4 hours, so
`stamp.py` adds a fingerprint of the file to its link (`site.css?v=…`). Without a re-stamp, returning visitors
get the new pages with the old stylesheet (this happened on 2026-11-14: screenshot corners poked out of
their phone frames until the cache ran out).

It rewrites all eight pages. `current=` sets which nav item is underlined (home, apps, studio, about).
Asset paths are relative (`../` per folder level); page links are root-absolute (`/studio/`).

---

## Pages

### `/` Home (parent company)
Hero (iPhone apps for families, websites for local businesses; two labelled phones: DinnerPilot's real home
screen and the real Sparky's Electric site) · **#apps** DinnerPilot with three real screens (Friday to Sunday, grocery list, Pantry Chef) · **#studio** the Studio with both plans and a
project checklist · **#about** "Made with care, not by committee." (ripples under the pointer) with three
principles · **#contact** close: "Get in touch" emails dave@.

### `/dinnerpilot/`
Hero: the real home screen plus the grocery-total strip (hidden on phones) · **#week** three screens · **#features** budget, reminders,
diets, traditions · **#pantry** Pantry Chef · **#pricing** Free plan and Pro plan ($5.99/mo or $39.99/yr,
7-day trial) · **#questions** · **#notify** the launch sign-up (Formspree `maeezoew`, sends with fetch and
shows its confirmation only after Formspree answers).

### `/studio/`
Hero (the real Sparky's site in a browser window + project card) · **#services** six kinds of work beside "Your website includes" ·
**#pricing** The Handoff ($2,000) and The Care Plan ($500 + $100/mo) · **#sample** Sparky's Electric on a
phone · **#questions** · **#contact** the quote form (Formspree `mlgvvbay`, honeypot `_gotcha`).

### Text pages: privacy, terms, data-deletion, account
Same header and footer; a side list of the four DinnerPilot help pages; the wording itself is unchanged
from the legal versions (Nov 2026). **Don't rewrite Privacy or Terms content without being asked.** The
Account page keeps its Supabase password-reset script exactly as it was (Supabase Auth's Site URL must
point to `/dinnerpilot/account/`).

### Checks
The kit's checkers live in `~/Desktop/ClubhouseApps/Claude Tools/taste-skill/skills/taste-skill/scripts/`.
**Impeccable** (a second design skill) is installed for this folder only, in `.claude/` (git-ignored). When Claude
Code is opened in `Website/`, it runs a design check after every file edit and again at the end of each turn.
Run it by hand with `.claude/skills/impeccable/scripts/impeccable detect index.html dinnerpilot/index.html studio/index.html`.
First run (2026-11-19): 29 findings, mostly false alarms ("cramped padding" on the kit's ruled list rows, the
heroes' soft background read as a "radial halo"). The three real ones were fixed the same day: the Studio hero
card's title is no longer an `h5` that skips heading levels, the kit's pulsing "live" dot is held still in
`site.css`, and the browser bar's address grey went from #77786e (4.47:1) to #6b6c62 (5.32:1). 25 findings remain,
all of those two false-alarm kinds.
The trades marquee adds three known false alarms in `consistency.mjs` (the kit's own marquee demo fails the same
way when checked in full): `cut-text` for words entering and leaving its faded edges, and `row-lines` "a clipped
carousel". `site.js` is fingerprinted by `stamp.py` like `site.css`; re-stamp after changing either.
The three main pages were checked with the kit's `consistency.mjs` at 1440, 1024, 820, 768 and 390 and
`copy-lint.mjs` (0 FAIL). Known checker false positives: the phone action bar crossing text mid-scroll
(contrast), its twin-hiding of pricing buttons (scroll-reveal), plan cards not lifting on hover (the kit's
own motion.css excludes `.card--plan`), and the pricing titles' edge on phones (the plans are split into two
phone screens, so the checker no longer sees them as one card row).

---

## Adding a new app

1. Copy `dinnerpilot/` to `newapp/` and rewrite its product page; give it its own legal pages.
2. In `.site/stamp.py`, add it to the **Apps** menu ("Our apps") and the footer's **Apps** column, add its pages to `PAGES`, then run the script.
3. Add a section for it on the home page under **#apps**.

---

## What to update when DinnerPilot launches

- [ ] `index.html` hero proof line and #apps line ("in TestFlight") → App Store
- [ ] `dinnerpilot/index.html` hero proof, FAQ "When can I get DinnerPilot?", pricing buttons and the #notify close → App Store link/badge
- [ ] Footer and menus need no change

---

## Making changes — workflow

```bash
# Navigate to the site folder
cd ~/Desktop/ClubhouseApps/Website

# Make your edits to HTML/CSS files

# Stage and commit
git add index.html dinnerpilot/index.html   # list changed files explicitly
git commit -m "Brief description of what changed"

# Push to deploy
git push origin main
```

The site goes live at clubhouseapps.com within about 60 seconds of the push.

**Never use `git add .` or `git add -A`** — it can accidentally commit `.DS_Store` files or other junk. Always stage named files.

---

## Third-party services referenced

| Service | Purpose | Where referenced |
|---------|---------|-----------------|
| **GitHub Pages** | Hosting | CNAME file + GitHub repo settings |
| **Formspree** | Launch sign-up and Studio quote forms | `dinnerpilot/index.html` (`maeezoew`), `studio/index.html` (`mlgvvbay`) |
| **Google Fonts** | Mona Sans, Geist Mono | the `site:head` block on every page |
| **Supabase** | App backend (mentioned in Privacy Policy only) | `dinnerpilot/privacy/index.html` |
| **AdMob** | App advertising (mentioned in Privacy Policy only) | `dinnerpilot/privacy/index.html` |
| **Anthropic Claude** | App AI features (mentioned in Privacy Policy only) | `dinnerpilot/privacy/index.html` |

---

## Notes for AI agents updating this site

- **No build step.** Edit `.html` and `.css` files directly. What you write is what ships.
- **site.css is global.** A change there affects every page. Check every page before committing.
- **Page styles exist.** Each main page has a short `<style>` block for its hero pieces and panel heights. Only move something to `site.css` if it's reused across pages.
- **The phone and browser mocks are HTML/CSS.** Don't replace them with images unless asked.
- **Legal page content is deliberate.** Don't rewrite Privacy Policy or Terms content without being asked — those have specific legal obligations.
- **Copyright year is 2026.** Update annually.
