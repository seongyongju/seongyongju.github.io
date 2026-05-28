# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal academic website for Seongyong Ju (Chung-Ang University), published to GitHub Pages at https://seongyongju.github.io. It is a fork of the [academicpages](https://academicpages.github.io) template, which itself is a detached fork of the [Minimal Mistakes](https://mmistakes.github.io/minimal-mistakes/) Jekyll theme. Site is built by Jekyll (Ruby) and served statically.

## Common Commands

Local development (from repo root):

```bash
bundle install                    # install Ruby gems (delete Gemfile.lock first if you hit security/version errors)
bundle exec jekyll liveserve      # build + serve at http://localhost:4000 with live reload (hawkins gem)
bundle exec jekyll serve --config _config.yml,_config.dev.yml   # serve with dev overrides applied
bundle exec jekyll build          # one-shot build into _site/ (gitignored)
```

Note: `_config.yml` is **not** auto-reloaded; restart the server after editing it. `_config.dev.yml` overrides `url` to `localhost:4000` and disables analytics for local runs.

JS bundle (only needed when editing `assets/js/_main.js` or `assets/js/plugins/*`):

```bash
npm install
npm run build:js                  # uglifies vendor + plugins + _main.js into assets/js/main.min.js
npm run watch:js                  # rebuild on change
```

Content generators (optional helpers in `markdown_generator/`):

```bash
cd markdown_generator
python publications.py            # reads publications.tsv → writes ../_publications/YYYY-MM-DD-<slug>.md
python talks.py                   # reads talks.tsv       → writes ../_talks/YYYY-MM-DD-<slug>.md
python pubsFromBib.py             # alternative: build publications from BibTeX
```

Talk map (run from `_talks/` after talks exist):

```bash
cd _talks && python ../talkmap.py    # geocodes `location:` front-matter, emits ../talkmap/ HTML/JS cluster map
```

## Architecture

### Jekyll collections drive the content model
Defined in `_config.yml` under `collections:` — `publications`, `teaching`, `portfolio`, `talks`. Each collection has a directory (`_publications/`, `_teaching/`, etc.); every Markdown file in a collection becomes a page at `/<collection>/<slug>/`. Adding new content = drop a Markdown file with the right front matter into the collection directory; no code changes required. Default front-matter values per collection (layout, author_profile, share, comments) are set in `_config.yml` under `defaults:` rather than in each file.

### Pages vs. posts vs. collections
- `_pages/` — top-level pages (about, cv, publications index, etc.). Listed in `include:` in `_config.yml` so Jekyll picks them up despite the underscore.
- `_posts/` — blog posts, conventional Jekyll naming `YYYY-MM-DD-title.md`.
- `_drafts/` — unpublished posts.
- Index/listing pages for each collection live in `_pages/` (e.g. `publications.md`, `presentations.html`) and use Liquid loops over `site.publications`, `site.talks`, etc.

### Layouts and includes
- `_layouts/` — top-level page templates (`single.html`, `archive.html`, `talk.html`, `splash.html`). Front-matter `layout:` in any page selects one.
- `_includes/` — reusable HTML partials (masthead, sidebar, author profile, archive single rows, comments providers under `comments-providers/`, analytics under `analytics-providers/`). `single.html` and `archive.html` compose these.
- `_sass/` — SCSS partials compiled via `assets/css/main.scss`. `_variables.scss` holds theme-wide colors/typography. Output style is `compressed` in prod, `expanded` in dev (set in `_config.dev.yml`).

### Site-wide configuration surfaces
- `_config.yml` — site title, author profile (name, email, social links, avatar), analytics, plugins, collection definitions, defaults.
- `_data/navigation.yml` — top nav links. Edit here, not in templates.
- `_data/authors.yml` — multi-author definitions if posts override the default author.
- `_data/ui-text.yml` — i18n strings used by includes/layouts.

### Asset paths
- `images/` — site images (including `profile.png` referenced by `author.avatar` in `_config.yml`).
- `files/` — downloadable assets (PDFs, CV, etc.); served at `/files/...`.
- `assets/` — CSS, JS, fonts.

### GitHub Pages constraints
`Gemfile` pins `github-pages` gem, so plugins must be on the GitHub Pages whitelist. The `whitelist:` block in `_config.yml` reflects this. Adding a non-whitelisted plugin will work locally but break the deployed build.

## Editing Tips

- When adding a publication or talk, prefer dropping a Markdown file directly into `_publications/` or `_talks/` over running the TSV generators — the generators are useful for bulk import but overwrite-style.
- The `read_more: "disabled"` and `talkmap_link: false` flags in `_config.yml` are intentionally off; flip them only if you also add the corresponding content (talkmap output, post excerpts).
- `repository: "seongyongju/seongyongju.github.io"` and `url: https://seongyongju.github.io` are the deploy targets — don't change unless renaming the GitHub repo.
