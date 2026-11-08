# CLAUDE.md

Personal site for Seongyong Ju, served by GitHub Pages at https://seongyongju.github.io from the `master` branch (Pages' built-in Jekyll, no theme). The previous academicpages version is archived in the private repo `seongyongju/seongyongju.github.io-legacy`.

## Layout

Content lives in small files; `index.html` only arranges them.

- `_data/profile.yml` — name, photo, affiliation line, and the links under the photo.
- `_includes/bio.md` — intro paragraphs (Markdown).
- `_data/publications.yml` — publication list (newest first; wrap own name in `**...**`).
- `_data/experience.yml` — experience list (newest first).
- `_posts/` — Korean paper-review notes, listed at `/notes/` (`notes/index.html`); the home page only links there. Keep existing `permalink:` values so old URLs keep working. `2013-08-14-blog-post-2.md` is an unpublished authoring template.
- `_layouts/default.html`, `_layouts/post.html`, `assets/style.css` — all of the styling. MathJax loads only on posts.
- `files/` — PDFs (CV, papers, slides). Use ASCII filenames; Korean names break across NFC/NFD.
- `images/profile.jpg` — profile photo (600px, metadata stripped).
- `cv.html` and `redirect_from:` in `index.html` keep old academicpages URLs (`/cv/`, `/publications/`, …) alive via `jekyll-redirect-from`.

## Local preview

```bash
bundle install && bundle exec jekyll serve   # needs Ruby ≤ 3.3 for the github-pages gem
```

Plugins must stay on the GitHub Pages whitelist.
