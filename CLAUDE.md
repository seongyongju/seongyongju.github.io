# CLAUDE.md

Personal site for Seongyong Ju, served by GitHub Pages at https://seongyongju.github.io from the `master` branch (Pages' built-in Jekyll, no theme). The previous academicpages version is archived in the private repo `seongyongju/seongyongju.github.io-legacy`.

## Layout

Content lives in small files; `index.html` only arranges them.

- `_data/profile.yml` — name, photo, affiliation line, and the links under the photo.
- `_includes/bio.md` — intro paragraphs (Markdown).
- `_data/publications.yml` — publication list; `year` decides placement: current build year on the home page, older (or `prior: true`) on `/publications/` (`publications.html`). Shared markup in `_includes/pub.html`. Full (newest first; own name is not bolded; co-first authors get `<sup>*</sup>` plus `note:`).
- `_data/experience.yml` — experience list (newest first).
- `_posts/` — Korean paper-review notes, listed at `/notes/` (`notes/index.html`); the home page only links there. Keep existing `permalink:` values so old URLs keep working. `2013-08-14-blog-post-2.md` is an unpublished authoring template.
- `_layouts/default.html`, `_layouts/post.html`, `assets/style.css` — all of the styling. MathJax loads only on posts.
- `cv/cv.md` — CV source (markup rules at the top of the file). `python3 cv/build.py` regenerates `files/CV_SeongyongJu.pdf` via headless Chrome, using Cambria from Microsoft Word if installed. Commit both.
- `files/` — PDFs (CV, papers, slides). Use ASCII filenames; Korean names break across NFC/NFD.
- `images/profile.jpg` — profile photo (600px, metadata stripped).
- `cv.html` and `redirect_from:` in `index.html` keep old academicpages URLs (`/cv/`, `/publications/`, …) alive via `jekyll-redirect-from`.

## Local preview

```bash
bundle install && bundle exec jekyll serve   # needs Ruby ≤ 3.3 for the github-pages gem
```

Plugins must stay on the GitHub Pages whitelist.
