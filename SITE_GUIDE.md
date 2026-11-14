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
├── assets/
│   ├── site.css            ← the site's own CSS: product mocks + the text-page layout
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
| 2026-11-14 | — | Whole site rebuilt as one: parent-company home, every page on the same kit, shared header and footer |

The major work happened on **2026-05-17**: legal pages were added, then immediately reorganized under `/dinnerpilot/` (they had initially been at the root), then the entire site got a full visual redesign in one large commit that touched all three primary files.

---

## Design System

Every page uses the **Taste Skill** kit (`github.com/Leonxlnx/taste-skill`) with one dealt look:
clay-pine palette (warm stone ground `#efe9e0`, pine green accent `#2e5b44`), Mona Sans + Geist Mono,
tonal pill buttons, ring mark, round corners. The tokens live in the `site:head` block that `stamp.py`
writes into every page; change them there, then re-stamp.

- **Kit files** (`assets/system.css`, `assets/ui/…`, etc.) are never edited. Override in `assets/site.css` or a page's own `<style>`.
- **`assets/site.css`** holds what the kit doesn't: the hand-drawn DinnerPilot phone (`.ph`), the small step card (`.dpn`), the browser window with the Sparky's Electric sample (`.bw`, `.sp__*`), the pricing halves (`.pricing`), and the text-page layout (`.doc`, `.prose`, `.doc__side`).
- **Page `<style>` blocks** only position each hero's pieces and set panel heights per breakpoint (the kit sizes every section to whole screens).
- **No screenshots**: every app screen on the site is live HTML drawn from real app data (build 55).
- **Motion** follows design-motion-principles: one entrance per hero, one timed loop per page at most, hover answers on every link; all of it stops under reduced motion.

### Shared header and footer: `.site/stamp.py`

The header, footer links, `<head>` assets and scripts are written into every page between marker comments
(`<!-- site:header current=apps -->` … `<!-- /site:header -->`). To change the nav or footer, edit the
blocks in `.site/stamp.py` and run:

```bash
python3 .site/stamp.py
```

It rewrites all eight pages. `current=` sets which nav item is underlined (home, apps, studio, about).
Asset paths are relative (`../` per folder level); page links are root-absolute (`/studio/`).

---

## Pages

### `/` Home (parent company)
Hero (iPhone apps for families, websites for local businesses; a Studio sample site and DinnerPilot's
home screen) · **#apps** DinnerPilot with three phone screens · **#studio** the Studio with both plans and a
project checklist · **#about** "Made with care, not by committee." (ripples under the pointer) with three
principles · **#contact** close: "Get in touch" emails dave@.

### `/dinnerpilot/`
Hero with the grocery-list card that ticks off · **#week** three screens · **#features** budget, reminders,
diets, traditions · **#pantry** Pantry Chef · **#pricing** Free plan and Pro plan ($5.99/mo or $39.99/yr,
7-day trial) · **#questions** · **#notify** the launch sign-up (Formspree `maeezoew`, sends with fetch and
shows its confirmation only after Formspree answers).

### `/studio/`
Hero (sample site + project card) · **#services** six kinds of work beside "Your website includes" ·
**#pricing** The Handoff ($2,000) and The Care Plan ($500 + $100/mo) · **#sample** Sparky's Electric on a
phone · **#questions** · **#contact** the quote form (Formspree `mlgvvbay`, honeypot `_gotcha`).

### Text pages: privacy, terms, data-deletion, account
Same header and footer; a side list of the four DinnerPilot help pages; the wording itself is unchanged
from the legal versions (Nov 2026). **Don't rewrite Privacy or Terms content without being asked.** The
Account page keeps its Supabase password-reset script exactly as it was (Supabase Auth's Site URL must
point to `/dinnerpilot/account/`).

### Checks
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
