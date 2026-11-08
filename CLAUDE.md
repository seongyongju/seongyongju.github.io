# CLAUDE.md

Personal site for Seongyong Ju, served by GitHub Pages at https://seongyongju.github.io from the `master` branch (Pages' built-in Jekyll, no theme). The previous academicpages version is archived in the private repo `seongyongju/seongyongju.github.io-legacy`.

## Layout

- `index.html` — the whole home page: bio, links, experience, misc. Edit text here directly.
- `_data/publications.yml` — publication list rendered on the home page (newest first; wrap own name in `**...**`).
- `_posts/` — Korean paper-review notes; listed under "Paper Notes" on the home page. Keep existing `permalink:` values so old URLs keep working. `2013-08-14-blog-post-2.md` is an unpublished authoring template.
- `_layouts/default.html`, `_layouts/post.html`, `assets/style.css` — all of the styling. MathJax loads only on posts.
- `files/` — PDFs (CV, papers, slides). Use ASCII filenames; Korean names break across NFC/NFD.
- `images/profile.png` — profile photo.
- `cv.html` and `redirect_from:` in `index.html` keep old academicpages URLs (`/cv/`, `/publications/`, …) alive via `jekyll-redirect-from`.

## Local preview

```bash
bundle install && bundle exec jekyll serve   # needs Ruby ≤ 3.3 for the github-pages gem
```

Plugins must stay on the GitHub Pages whitelist.
