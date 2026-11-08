"""Render cv/cv.md to files/CV_SeongyongJu.pdf with headless Chrome.

Usage: python3 cv/build.py [--html]   (--html also keeps cv/cv.html for previewing)
The markup rules are documented at the top of cv.md.
"""
import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "cv" / "cv.md"
OUT_HTML = ROOT / "cv" / "cv.html"
OUT_PDF = ROOT / "files" / "CV_SeongyongJu.pdf"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
WORD_FONTS = "/Applications/Microsoft Word.app/Contents/Resources/DFonts"

CSS = f"""
@font-face {{ font-family: CV; src: local("Cambria"), url("file://{WORD_FONTS}/Cambria.ttc"); }}
@font-face {{ font-family: CV; font-weight: bold; src: local("Cambria Bold"), url("file://{WORD_FONTS}/Cambriab.ttf"); }}
@font-face {{ font-family: CV; font-style: italic; src: local("Cambria Italic"), url("file://{WORD_FONTS}/Cambriai.ttf"); }}
@font-face {{ font-family: CV; font-weight: bold; font-style: italic; src: local("Cambria Bold Italic"), url("file://{WORD_FONTS}/Cambriaz.ttf"); }}
@page {{ size: A4; margin: 18mm 15mm 16mm; }}
body {{ font-family: CV, Cambria, Georgia, serif; font-size: 10pt; line-height: 1.32; color: #000; margin: 0; }}
.name {{ text-align: center; font-size: 15pt; font-weight: bold; margin: 0; }}
.contact {{ text-align: center; margin: 1pt 0 0; }}
h2 {{ font-size: 10.5pt; font-weight: bold; margin: 18pt 0 6pt; padding-bottom: 2pt; border-bottom: .8pt solid #000; break-after: avoid; }}
h3 {{ font-size: 11pt; font-weight: bold; margin: 0; break-after: avoid; }}
h4 {{ font-size: 10pt; font-weight: bold; margin: 0; break-after: avoid; }}
.row {{ display: flex; justify-content: space-between; gap: 12pt; }}
.row > .date {{ white-space: nowrap; font-weight: normal; }}
p {{ margin: 0; }}
ul {{ margin: 0; padding-left: 22pt; }}
li {{ text-align: justify; }}
.gap {{ height: 11pt; }}
.block {{ break-inside: avoid; }}
"""


def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    return re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)


def with_date(text):
    if " || " not in text:
        return inline(text)
    left, date = text.rsplit(" || ", 1)
    return f'<span class="row"><span>{inline(left)}</span><span class="date">{inline(date)}</span></span>'


def render(md):
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S).strip("\n")
    out, bullets, block = [], None, []

    def flush_bullets():
        nonlocal bullets
        if bullets is not None:
            block.append("<ul>" + "".join(f"<li>{b}</li>" for b in bullets) + "</ul>")
            bullets = None

    def flush_block():
        flush_bullets()
        if block:
            out.append('<div class="block">' + "".join(block) + "</div>")
            block.clear()

    lines = md.split("\n")
    out.append(f'<p class="name">{inline(lines[0].lstrip("# "))}</p>')
    out.append(f'<p class="contact">{inline(lines[1])}</p>')
    for line in lines[2:]:
        if line.startswith("  ") and bullets:
            bullets[-1] += "<br>" + inline(line.strip())
            continue
        if line.startswith("- "):
            bullets = bullets or []
            bullets.append(inline(line[2:]))
            continue
        flush_bullets()
        if not line.strip():
            if block:
                flush_block()
                out.append('<div class="gap"></div>')
        elif line.startswith("## "):
            flush_block()
            if out and out[-1] == '<div class="gap"></div>':
                out.pop()
            out.append(f"<h2>{inline(line[3:])}</h2>")
        elif line.startswith("### "):
            block.append(f"<h3>{with_date(line[4:])}</h3>")
        elif line.startswith("#### "):
            block.append(f"<h4>{with_date(line[5:])}</h4>")
        else:
            block.append(f"<p>{with_date(line)}</p>")
    flush_block()
    return f'<!doctype html><meta charset="utf-8"><style>{CSS}</style>\n' + "\n".join(out)


def main():
    OUT_HTML.write_text(render(SRC.read_text(encoding="utf-8")), encoding="utf-8")
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
         "--allow-file-access-from-files", f"--print-to-pdf={OUT_PDF}", OUT_HTML.as_uri()],
        check=True, stderr=subprocess.DEVNULL,
    )
    if "--html" not in sys.argv:
        OUT_HTML.unlink()
    print(f"wrote {OUT_PDF.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
