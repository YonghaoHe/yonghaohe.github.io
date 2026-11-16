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
    "wechat": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M8.691 2.188C3.891 2.188 0 5.476 0 9.53c0 2.212 1.17 4.203 3.002 5.55a.59.59 0 0 1 .213.665l-.39 1.48c-.019.07-.048.141-.048.213 0 .163.13.295.29.295a.326.326 0 0 0 .167-.054l1.903-1.114a.864.864 0 0 1 .717-.098 10.16 10.16 0 0 0 2.837.403c.276 0 .543-.027.811-.05a6.127 6.127 0 0 1-.253-1.738c0-3.56 3.143-6.452 7.029-6.452.39 0 .77.034 1.143.084C16.318 4.59 12.835 2.188 8.691 2.188zm-2.6 4.17a1.128 1.128 0 1 1 0 2.256 1.128 1.128 0 0 1 0-2.256zm5.12 0a1.128 1.128 0 1 1 0 2.256 1.128 1.128 0 0 1 0-2.256zM24 15.088c0-3.381-3.404-6.13-7.604-6.13-4.202 0-7.604 2.749-7.604 6.13 0 3.382 3.402 6.13 7.604 6.13a9.583 9.583 0 0 0 2.422-.312.768.768 0 0 1 .63.083l1.602.938a.27.27 0 0 0 .14.047c.134 0 .244-.11.244-.245 0-.06-.024-.12-.04-.18l-.328-1.245a.498.498 0 0 1 .18-.56C23.004 18.858 24 17.09 24 15.088zm-9.986-1.105a.942.942 0 1 1 0-1.884.942.942 0 0 1 0 1.884zm4.762 0a.942.942 0 1 1 0-1.884.942.942 0 0 1 0 1.884z"/></svg>""",
    "xiaohongshu": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" fill="currentColor" role="img" aria-label="Xiaohongshu"><path d="M22.405 9.879c.002.016.01.02.07.019h.725a.797.797 0 0 0 .78-.972.794.794 0 0 0-.884-.618.795.795 0 0 0-.692.794c0 .101-.002.666.001.777zm-11.509 4.808c-.203.001-1.353.004-1.685.003a2.528 2.528 0 0 1-.766-.126.025.025 0 0 0-.03.014L7.7 16.127a.025.025 0 0 0 .01.032c.111.06.336.124.495.124.66.01 1.32.002 1.981 0 .01 0 .02-.006.023-.015l.712-1.545a.025.025 0 0 0-.024-.036zM.477 9.91c-.071 0-.076.002-.076.01a.834.834 0 0 0-.01.08c-.027.397-.038.495-.234 3.06-.012.24-.034.389-.135.607-.026.057-.033.042.003.112.046.092.681 1.523.787 1.74.008.015.011.02.017.02.008 0 .033-.026.047-.044.147-.187.268-.391.371-.606.306-.635.44-1.325.486-1.706.014-.11.021-.22.03-.33l.204-2.616.022-.293c.003-.029 0-.033-.03-.034zm7.203 3.757a1.427 1.427 0 0 1-.135-.607c-.004-.084-.031-.39-.235-3.06a.443.443 0 0 0-.01-.082c-.004-.011-.052-.008-.076-.008h-1.48c-.03.001-.034.005-.03.034l.021.293c.076.982.153 1.964.233 2.946.05.4.186 1.085.487 1.706.103.215.223.419.37.606.015.018.037.051.048.049.02-.003.742-1.642.804-1.765.036-.07.03-.055.003-.112zm3.861-.913h-.872a.126.126 0 0 1-.116-.178l1.178-2.625a.025.025 0 0 0-.023-.035l-1.318-.003a.148.148 0 0 1-.135-.21l.876-1.954a.025.025 0 0 0-.023-.035h-1.56c-.01 0-.02.006-.024.015l-.926 2.068c-.085.169-.314.634-.399.938a.534.534 0 0 0-.02.191.46.46 0 0 0 .23.378.981.981 0 0 0 .46.119h.59c.041 0-.688 1.482-.834 1.972a.53.53 0 0 0-.023.172.465.465 0 0 0 .23.398c.15.092.342.12.475.12l1.66-.001c.01 0 .02-.006.023-.015l.575-1.28a.025.025 0 0 0-.024-.035zm-6.93-4.937H3.1a.032.032 0 0 0-.034.033c0 1.048-.01 2.795-.01 6.829 0 .288-.269.262-.28.262h-.74c-.04.001-.044.004-.04.047.001.037.465 1.064.555 1.263.01.02.03.033.051.033.157.003.767.009.938-.014.153-.02.3-.06.438-.132.3-.156.49-.419.595-.765.052-.172.075-.353.075-.533.002-2.33 0-4.66-.007-6.991a.032.032 0 0 0-.032-.032zm11.784 6.896c0-.014-.01-.021-.024-.022h-1.465c-.048-.001-.049-.002-.05-.049v-4.66c0-.072-.005-.07.07-.07h.863c.08 0 .075.004.075-.074V8.393c0-.082.006-.076-.08-.076h-3.5c-.064 0-.075-.006-.075.073v1.445c0 .083-.006.077.08.077h.854c.075 0 .07-.004.07.07v4.624c0 .095.008.084-.085.084-.37 0-1.11-.002-1.304 0-.048.001-.06.03-.06.03l-.697 1.519s-.014.025-.008.036c.006.01.013.008.058.008 1.748.003 3.495.002 5.243.002.03-.001.034-.006.035-.033v-1.539zm4.177-3.43c0 .013-.007.023-.02.024-.346.006-.692.004-1.037.004-.014-.002-.022-.01-.022-.024-.005-.434-.007-.869-.01-1.303 0-.072-.006-.071.07-.07l.733-.003c.041 0 .081.002.12.015.093.025.16.107.165.204.006.431.002 1.153.001 1.153zm2.67.244a1.953 1.953 0 0 0-.883-.222h-.18c-.04-.001-.04-.003-.042-.04V10.21c0-.132-.007-.263-.025-.394a1.823 1.823 0 0 0-.153-.53 1.533 1.533 0 0 0-.677-.71 2.167 2.167 0 0 0-1-.258c-.153-.003-.567 0-.72 0-.07 0-.068.004-.068-.065V7.76c0-.031-.01-.041-.046-.039H17.93s-.016 0-.023.007c-.006.006-.008.012-.008.023v.546c-.008.036-.057.015-.082.022h-.95c-.022.002-.028.008-.03.032v1.481c0 .09-.004.082.082.082h.913c.082 0 .072.128.072.128V11.19s.003.117-.06.117h-1.482c-.068 0-.06.082-.06.082v1.445s-.01.068.064.068h1.457c.082 0 .076-.006.076.079v3.225c0 .088-.007.081.082.081h1.43c.09 0 .082.007.082-.08v-3.27c0-.029.006-.035.033-.035l2.323-.003c.098 0 .191.02.28.061a.46.46 0 0 1 .274.407c.008.395.003.79.003 1.185 0 .259-.107.367-.33.367h-1.218c-.023.002-.029.008-.028.033.184.437.374.871.57 1.303a.045.045 0 0 0 .04.026c.17.005.34.002.51.003.15-.002.517.004.666-.01a2.03 2.03 0 0 0 .408-.075c.59-.18.975-.698.976-1.313v-1.981c0-.128-.01-.254-.034-.38 0 .078-.029-.641-.724-.998z"/></svg>""",
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
        title = esc(s.get("title", ""))
        extra = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
        anchor = f'<a class="social-icon" href="{esc(href)}" title="{title}" aria-label="{title}"{extra}>{svg}</a>'
        qr = (s.get("qr_src") or "").strip()
        if qr:
            anchor = (
                f'<span class="social-wrap">{anchor}<span class="qr-tip" role="tooltip">'
                f'<img src="{esc(qr)}" alt="{title} QR code" width="128" height="128" loading="lazy"></span></span>'
            )
        out.append(f"                    {anchor}")
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
