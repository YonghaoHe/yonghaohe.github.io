#!/usr/bin/env python3
"""
从 content.json 生成 index.html。
用法: python build.py
修改内容请编辑 content.json，然后运行本脚本再 git push。
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT_FILE = ROOT / "content.json"
OUTPUT_FILE = ROOT / "index.html"

# 社交图标 SVG（与原先页面一致）
SOCIAL_SVGS = {
    "wechat": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="28" height="28" fill="currentColor"><path d="M8.691 2.188C3.891 2.188 0 5.476 0 9.53c0 2.212 1.17 4.203 3.002 5.55a.59.59 0 0 1 .213.665l-.39 1.48c-.019.07-.048.141-.048.213 0 .163.13.295.29.295a.326.326 0 0 0 .167-.054l1.903-1.114a.864.864 0 0 1 .717-.098 10.16 10.16 0 0 0 2.837.403c.276 0 .543-.027.811-.05a6.127 6.127 0 0 1-.253-1.738c0-3.56 3.143-6.452 7.029-6.452.39 0 .77.034 1.143.084C16.318 4.59 12.835 2.188 8.691 2.188zm-2.6 4.17a1.128 1.128 0 1 1 0 2.256 1.128 1.128 0 0 1 0-2.256zm5.12 0a1.128 1.128 0 1 1 0 2.256 1.128 1.128 0 0 1 0-2.256zM24 15.088c0-3.381-3.404-6.13-7.604-6.13-4.202 0-7.604 2.749-7.604 6.13 0 3.382 3.402 6.13 7.604 6.13a9.583 9.583 0 0 0 2.422-.312.768.768 0 0 1 .63.083l1.602.938a.27.27 0 0 0 .14.047c.134 0 .244-.11.244-.245 0-.06-.024-.12-.04-.18l-.328-1.245a.498.498 0 0 1 .18-.56C23.004 18.858 24 17.09 24 15.088zm-9.986-1.105a.942.942 0 1 1 0-1.884.942.942 0 0 1 0 1.884zm4.762 0a.942.942 0 1 1 0-1.884.942.942 0 0 1 0 1.884z"/></svg>""",
    "xiaohongshu": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="28" height="28" fill="currentColor"><path d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm4.08 11.31h-1.64l.25 3.56h-1.46l-.25-3.56H11.4l-.18 3.56H9.76l.18-3.56H8.08v-1.29h2.02l.12-2.17H8.24V8.56h2.12l.16-2.39h1.46l-.16 2.39h1.58l.16-2.39h1.46l-.16 2.39h1.48v1.29h-1.62l-.12 2.17h1.78v1.29zm-3.14-1.29l.12-2.17h-1.58l-.12 2.17h1.58z"/></svg>""",
    "x": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="28" height="28" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>""",
}


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def attr_esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def render_subtitle(hero: dict) -> str:
    prefix = esc(hero.get("subtitle_prefix") or "")
    link = hero.get("subtitle_link")
    if link and link.get("text") and link.get("url"):
        a = f'<a href="{attr_esc(link["url"])}">{esc(link["text"])}</a>'
        return f'<p class="subtitle">{prefix}{a}</p>'
    return f'<p class="subtitle">{prefix}</p>'


def render_nav(nav: list) -> str:
    items = []
    for item in nav:
        items.append(
            f'                <li><a href="{attr_esc(item.get("href", "#"))}">{esc(item.get("label", ""))}</a></li>'
        )
    return "\n".join(items)


def render_social(social: list) -> str:
    out = []
    for s in social:
        icon = s.get("icon", "wechat")
        svg = SOCIAL_SVGS.get(icon, SOCIAL_SVGS["wechat"])
        href = s.get("href", "#")
        title = esc(s.get("title", ""))
        extra = ""
        if href.startswith("http"):
            extra = ' target="_blank" rel="noopener"'
        out.append(
            f"""                    <a href="{attr_esc(href)}" class="social-icon" title="{title}"{extra}>
                        {svg}
                    </a>"""
        )
    return "\n".join(out)


def render_timeline_education(items: list) -> str:
    blocks = []
    for it in items:
        blocks.append(
            f"""                <div class="timeline-item">
                    <div class="timeline-date">{esc(it.get("date", ""))}</div>
                    <div class="timeline-content">
                        <h3>{esc(it.get("degree", ""))}</h3>
                        <p class="institution">{esc(it.get("institution", ""))}</p>
                        <p>{esc(it.get("description", ""))}</p>
                    </div>
                </div>"""
        )
    return "\n".join(blocks)


def render_timeline_experience(items: list) -> str:
    blocks = []
    for it in items:
        bullets = it.get("bullets") or []
        li_html = "\n".join(f"                            <li>{esc(b)}</li>" for b in bullets)
        ul = f"\n                        <ul>\n{li_html}\n                        </ul>\n" if li_html else ""
        blocks.append(
            f"""                <div class="timeline-item">
                    <div class="timeline-date">{esc(it.get("date", ""))}</div>
                    <div class="timeline-content">
                        <h3>{esc(it.get("title", ""))}</h3>
                        <p class="institution">{esc(it.get("institution", ""))}</p>{ul}                    </div>
                </div>"""
        )
    return "\n".join(blocks)


def render_authors(authors: list) -> str:
    if not authors:
        return ""
    parts = [f"<strong>{esc(authors[0])}</strong>"]
    for name in authors[1:]:
        parts.append(esc(name))
    return ", ".join(parts)


def render_publication_item(item: dict) -> str:
    thumb_img = (item.get("thumbnail_image") or "").strip()
    if thumb_img:
        thumb = f"""                    <div class="pub-thumbnail">
                        <img src="{attr_esc(thumb_img)}" alt="{esc(item.get("thumbnail_alt") or item.get("title", ""))}">
                    </div>"""
    else:
        ph = esc(item.get("thumbnail_placeholder") or "Paper Image")
        thumb = f"""                    <div class="pub-thumbnail">
                        <div class="pub-thumbnail-placeholder">{ph}</div>
                    </div>"""

    links_html = []
    for link in item.get("links") or []:
        links_html.append(
            f'                            <a href="{attr_esc(link.get("href", "#"))}" class="pub-link">{esc(link.get("label", ""))}</a>'
        )
    links_block = "\n".join(links_html)

    tags_html = "\n".join(
        f'                            <span class="pub-tag">{esc(t)}</span>' for t in (item.get("tags") or [])
    )

    return f"""                <div class="publication-item">
{thumb}
                    <div class="pub-info">
                        <h3>{esc(item.get("title", ""))}</h3>
                        <p class="authors">{render_authors(item.get("authors") or [])}</p>
                        <p class="venue">{esc(item.get("venue", ""))}</p>
                        <div class="publication-links">
{links_block}
                        </div>
                        <div class="pub-tags">
{tags_html}
                        </div>
                    </div>
                </div>"""


def render_publications(items: list) -> str:
    return "\n".join(render_publication_item(it) for it in items)


def build_html(data: dict) -> str:
    site = data.get("site") or {}
    nav = data.get("nav") or []
    hero = data.get("hero") or {}
    edu = data.get("education") or {}
    exp = data.get("experience") or {}
    pubs = data.get("publications") or {}
    footer = data.get("footer") or {}

    logo_name = esc(hero.get("name", ""))
    photo = hero.get("photo") or {}
    about_ps = hero.get("about_paragraphs") or []
    about_p_html = "\n".join(f"                <p>{esc(p)}</p>" for p in about_ps)

    insights = hero.get("core_insights") or []
    li_insights = "\n".join(f"                        <li>{esc(x)}</li>" for x in insights)

    copyright_text = esc(footer.get("copyright", ""))

    return f"""<!DOCTYPE html>
<html lang="{attr_esc(site.get("lang", "zh-CN"))}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{esc(site.get("page_title", "Homepage"))}</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="container">
            <a href="#" class="logo">{logo_name}</a>
            <ul class="nav-links">
{render_nav(nav)}
            </ul>
        </div>
    </nav>

    <!-- Hero / About Section -->
    <header class="hero" id="about">
        <div class="container">
            <div class="hero-content">
                <div class="hero-avatar">
                    <img class="avatar-photo" src="{attr_esc(photo.get("src", ""))}" alt="{esc(photo.get("alt", ""))}">
                </div>
                <div class="hero-text">
                    <h1>{logo_name}</h1>
{render_subtitle(hero)}
                    <p class="tagline">{esc(hero.get("tagline", ""))}</p>
                </div>
            </div>
            <div class="about-content">
{about_p_html}
                <div class="core-insights">
                    <h3>{esc(hero.get("core_insights_title", "Core Insights"))}</h3>
                    <ul>
{li_insights}
                    </ul>
                </div>
                <div class="social-links">
{render_social(hero.get("social") or [])}
                </div>
            </div>
        </div>
    </header>

    <!-- Education Section -->
    <section class="section section-alt" id="education">
        <div class="container">
            <h2 class="section-title">{esc(edu.get("section_title", "Education"))}</h2>
            <div class="timeline education-cards">
{render_timeline_education(edu.get("items") or [])}
            </div>
        </div>
    </section>

    <!-- Experience Section -->
    <section class="section" id="experience">
        <div class="container">
            <h2 class="section-title">{esc(exp.get("section_title", "Experience"))}</h2>
            <div class="timeline">
{render_timeline_experience(exp.get("items") or [])}
            </div>
        </div>
    </section>

    <!-- Publications Section -->
    <section class="section" id="publications">
        <div class="container">
            <h2 class="section-title">{esc(pubs.get("section_title", "Publications"))}</h2>
            <div class="publications-list">
{render_publications(pubs.get("items") or [])}
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>{copyright_text}</p>
        </div>
    </footer>

    <script src="js/main.js"></script>
</body>
</html>
"""


def main() -> int:
    if not CONTENT_FILE.is_file():
        print(f"找不到 {CONTENT_FILE}", file=sys.stderr)
        return 1
    try:
        data = json.loads(CONTENT_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"content.json 解析失败: {e}", file=sys.stderr)
        return 1
    html_out = build_html(data)
    OUTPUT_FILE.write_text(html_out, encoding="utf-8", newline="\n")
    print(f"已生成 {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
