#!/usr/bin/env python3
"""
Generate index.html from content.json.
Usage: python build.py
Edit content.json, run this script, then commit index.html together with it.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT_FILE = ROOT / "content.json"
OUTPUT_FILE = ROOT / "index.html"

OWNER_AUTHOR = "Yonghao He"
PUBLICATION_VISIBLE_FROM_YEAR = 2025

ICON_ATTRS = 'width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
SOCIAL_SVGS = {
    "scholar": f'<svg {ICON_ATTRS}><path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11.5V16c3 2.5 9 2.5 12 0v-4.5"/></svg>',
    "github": f'<svg {ICON_ATTRS}><path d="M9 19c-4 1.2-4-2-6-2.5M15 21v-3.2c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1-.3-3.4 1.3a11.6 11.6 0 0 0-6.2 0C6.6 2.8 5.6 3.1 5.6 3.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4.2 9.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V21"/></svg>',
    "email": f'<svg {ICON_ATTRS}><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
}
THUMB_SVG = '<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="1.5"/><path d="M3 17l5-4 4 3 3-2 6 4"/></svg>'


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def render_social(social: list) -> str:
    out = []
    for s in social:
        svg = SOCIAL_SVGS.get(s.get("icon", ""), "")
        href = (s.get("href") or "#").strip()
        extra = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
        out.append(
            f'                    <a class="social-icon" href="{esc(href)}" title="{esc(s.get("title", ""))}" aria-label="{esc(s.get("title", ""))}"{extra}>{svg}</a>'
        )
    return "\n".join(out)


def render_rows(items: list, primary: str, secondary: str) -> str:
    rows = []
    for it in items:
        rows.append(
            f"""                    <li><span class="row-date">{esc(it.get("date", ""))}</span><span class="row-main">{esc(it.get(primary, ""))}<small>{esc(it.get(secondary, ""))}</small></span></li>"""
        )
    return "\n".join(rows)


def render_authors(authors: list) -> str:
    parts = []
    for name in authors:
        text = esc(name)
        if (name or "").strip() == OWNER_AUTHOR:
            text = f"<strong>{text}</strong>"
        parts.append(text)
    return ", ".join(parts)


def publication_year(item: dict) -> int | None:
    year = item.get("year")
    if isinstance(year, int):
        return year
    if isinstance(year, str) and year.strip().isdigit():
        return int(year.strip())
    match = re.search(r"\b((?:19|20)\d{2})\b", item.get("venue") or "")
    return int(match.group(1)) if match else None


def render_publication_item(item: dict, *, earlier: bool) -> str:
    thumb_img = (item.get("thumbnail_image") or "").strip()
    if thumb_img:
        thumb = f'<img src="{esc(thumb_img)}" alt="{esc(item.get("title", ""))}">'
    else:
        thumb = THUMB_SVG
    links = []
    for link in item.get("links") or []:
        href = (link.get("href") or "").strip()
        if not href:
            continue
        extra = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
        links.append(f'<a href="{esc(href)}"{extra}>{esc(link.get("label", ""))}</a>')
    links_html = f'\n                    <div class="pub-links">{"".join(links)}</div>' if links else ""
    cls = "pub-card pub-card--earlier" if earlier else "pub-card"
    return f"""                <article class="{cls}">
                    <div class="pub-main">
                        <div class="pub-thumb">{thumb}</div>
                        <div class="pub-info">
                            <span class="pub-venue">{esc(item.get("venue", ""))}</span>
                            <h3>{esc(item.get("title", ""))}</h3>
                            <p class="pub-authors">{render_authors(item.get("authors") or [])}</p>
                        </div>
                    </div>{links_html}
                </article>"""


def render_publications(items: list) -> tuple[str, int]:
    blocks, n_earlier = [], 0
    for item in items:
        year = publication_year(item)
        earlier = year is not None and year < PUBLICATION_VISIBLE_FROM_YEAR
        n_earlier += earlier
        blocks.append(render_publication_item(item, earlier=earlier))
    return "\n".join(blocks), n_earlier


def render_hiring(wip: dict) -> str:
    hiring = wip.get("hiring") or {}
    roles = "\n".join(
        f"""                <span class="role" tabindex="0">{esc(r.get("title", ""))}<em role="tooltip">{esc(r.get("jd", ""))}</em></span>"""
        for r in hiring.get("roles") or []
    )
    return f"""            <div class="hiring">
                <strong>{esc(hiring.get("label", "We are hiring"))}</strong>
{roles}
            </div>"""


def build_html(data: dict) -> str:
    site = data.get("site") or {}
    hero = data.get("hero") or {}
    edu = data.get("education") or {}
    exp = data.get("experience") or {}
    news = data.get("news") or {}
    wip = data.get("work_in_progress") or {}
    pubs = data.get("publications") or {}
    footer = data.get("footer") or {}

    photo = hero.get("photo") or {}
    if (photo.get("src") or "").strip():
        avatar = f'<img src="{esc(photo["src"])}" alt="{esc(photo.get("alt", ""))}">'
    else:
        avatar = esc(photo.get("initials") or "".join(w[0] for w in hero.get("name", "").split()[:2]))

    news_html = "\n".join(
        f'                    <li><time>{esc(n.get("date", ""))}</time><span>{esc(n.get("text", ""))}</span></li>'
        for n in news.get("items") or []
    )
    wip_html = "\n".join(
        f'                <div class="wip-card"><h3>{esc(w.get("title", ""))}</h3><p>{esc(w.get("text", ""))}</p></div>'
        for w in wip.get("items") or []
    )
    legend = " &middot; ".join(
        f'<sup>{esc(l["mark"])}</sup> {esc(l["label"])}' for l in pubs.get("legend") or []
    )
    legend_html = f'<span class="legend">({legend})</span>' if legend else ""
    pubs_html, n_earlier = render_publications(pubs.get("items") or [])
    more = ""
    if n_earlier:
        more = f"""
            <button type="button" class="pub-more" id="pub-more" aria-expanded="false" data-count="{n_earlier}">View more ({n_earlier} earlier papers)</button>"""

    return f"""<!DOCTYPE html>
<html lang="{esc(site.get("lang", "en"))}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{esc(site.get("page_title", "Homepage"))}</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <main class="page">
        <header class="card hero" id="about">
            <div class="hero-id">
                <div class="avatar">{avatar}</div>
                <h1>{esc(hero.get("name", ""))}</h1>
                <p class="role-line">{esc(hero.get("subtitle_prefix", ""))}</p>
                <div class="social">
{render_social(hero.get("social") or [])}
                </div>
            </div>
            <p class="intro">{esc(hero.get("tagline", ""))}</p>
            <section class="hero-col" id="education">
                <h2 class="eyebrow">{esc(edu.get("section_title", "Education"))}</h2>
                <ul class="rows">
{render_rows(edu.get("items") or [], "degree", "institution")}
                </ul>
            </section>
            <section class="hero-col" id="experience">
                <h2 class="eyebrow">{esc(exp.get("section_title", "Experiences"))}</h2>
                <ul class="rows">
{render_rows(exp.get("items") or [], "title", "institution")}
                </ul>
            </section>
        </header>

        <section class="card news" id="news">
            <h2 class="eyebrow">{esc(news.get("section_title", "Latest News"))}</h2>
            <ul class="news-list">
{news_html}
            </ul>
        </section>

        <section id="wip">
            <h2 class="section-title">{esc(wip.get("section_title", "Work in progress"))}</h2>
            <div class="wip-grid">
{wip_html}
            </div>
{render_hiring(wip)}
        </section>

        <section id="publications">
            <h2 class="section-title">{esc(pubs.get("section_title", "Publications"))} {legend_html}</h2>
            <div class="pub-grid" id="pub-grid">
{pubs_html}
            </div>{more}
        </section>
    </main>

    <footer class="footer"><p>{esc(footer.get("copyright", ""))}</p></footer>
    <script src="js/main.js"></script>
</body>
</html>
"""


def main() -> int:
    if not CONTENT_FILE.is_file():
        print(f"Missing {CONTENT_FILE}", file=sys.stderr)
        return 1
    try:
        data = json.loads(CONTENT_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"content.json parse error: {e}", file=sys.stderr)
        return 1
    OUTPUT_FILE.write_text(build_html(data), encoding="utf-8", newline="\n")
    print(f"Generated {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
