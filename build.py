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
    "xiaohongshu": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="28" height="28" fill="currentColor" role="img" aria-label="Xiaohongshu"><path d="M22.405 9.879c.002.016.01.02.07.019h.725a.797.797 0 0 0 .78-.972.794.794 0 0 0-.884-.618.795.795 0 0 0-.692.794c0 .101-.002.666.001.777zm-11.509 4.808c-.203.001-1.353.004-1.685.003a2.528 2.528 0 0 1-.766-.126.025.025 0 0 0-.03.014L7.7 16.127a.025.025 0 0 0 .01.032c.111.06.336.124.495.124.66.01 1.32.002 1.981 0 .01 0 .02-.006.023-.015l.712-1.545a.025.025 0 0 0-.024-.036zM.477 9.91c-.071 0-.076.002-.076.01a.834.834 0 0 0-.01.08c-.027.397-.038.495-.234 3.06-.012.24-.034.389-.135.607-.026.057-.033.042.003.112.046.092.681 1.523.787 1.74.008.015.011.02.017.02.008 0 .033-.026.047-.044.147-.187.268-.391.371-.606.306-.635.44-1.325.486-1.706.014-.11.021-.22.03-.33l.204-2.616.022-.293c.003-.029 0-.033-.03-.034zm7.203 3.757a1.427 1.427 0 0 1-.135-.607c-.004-.084-.031-.39-.235-3.06a.443.443 0 0 0-.01-.082c-.004-.011-.052-.008-.076-.008h-1.48c-.03.001-.034.005-.03.034l.021.293c.076.982.153 1.964.233 2.946.05.4.186 1.085.487 1.706.103.215.223.419.37.606.015.018.037.051.048.049.02-.003.742-1.642.804-1.765.036-.07.03-.055.003-.112zm3.861-.913h-.872a.126.126 0 0 1-.116-.178l1.178-2.625a.025.025 0 0 0-.023-.035l-1.318-.003a.148.148 0 0 1-.135-.21l.876-1.954a.025.025 0 0 0-.023-.035h-1.56c-.01 0-.02.006-.024.015l-.926 2.068c-.085.169-.314.634-.399.938a.534.534 0 0 0-.02.191.46.46 0 0 0 .23.378.981.981 0 0 0 .46.119h.59c.041 0-.688 1.482-.834 1.972a.53.53 0 0 0-.023.172.465.465 0 0 0 .23.398c.15.092.342.12.475.12l1.66-.001c.01 0 .02-.006.023-.015l.575-1.28a.025.025 0 0 0-.024-.035zm-6.93-4.937H3.1a.032.032 0 0 0-.034.033c0 1.048-.01 2.795-.01 6.829 0 .288-.269.262-.28.262h-.74c-.04.001-.044.004-.04.047.001.037.465 1.064.555 1.263.01.02.03.033.051.033.157.003.767.009.938-.014.153-.02.3-.06.438-.132.3-.156.49-.419.595-.765.052-.172.075-.353.075-.533.002-2.33 0-4.66-.007-6.991a.032.032 0 0 0-.032-.032zm11.784 6.896c0-.014-.01-.021-.024-.022h-1.465c-.048-.001-.049-.002-.05-.049v-4.66c0-.072-.005-.07.07-.07h.863c.08 0 .075.004.075-.074V8.393c0-.082.006-.076-.08-.076h-3.5c-.064 0-.075-.006-.075.073v1.445c0 .083-.006.077.08.077h.854c.075 0 .07-.004.07.07v4.624c0 .095.008.084-.085.084-.37 0-1.11-.002-1.304 0-.048.001-.06.03-.06.03l-.697 1.519s-.014.025-.008.036c.006.01.013.008.058.008 1.748.003 3.495.002 5.243.002.03-.001.034-.006.035-.033v-1.539zm4.177-3.43c0 .013-.007.023-.02.024-.346.006-.692.004-1.037.004-.014-.002-.022-.01-.022-.024-.005-.434-.007-.869-.01-1.303 0-.072-.006-.071.07-.07l.733-.003c.041 0 .081.002.12.015.093.025.16.107.165.204.006.431.002 1.153.001 1.153zm2.67.244a1.953 1.953 0 0 0-.883-.222h-.18c-.04-.001-.04-.003-.042-.04V10.21c0-.132-.007-.263-.025-.394a1.823 1.823 0 0 0-.153-.53 1.533 1.533 0 0 0-.677-.71 2.167 2.167 0 0 0-1-.258c-.153-.003-.567 0-.72 0-.07 0-.068.004-.068-.065V7.76c0-.031-.01-.041-.046-.039H17.93s-.016 0-.023.007c-.006.006-.008.012-.008.023v.546c-.008.036-.057.015-.082.022h-.95c-.022.002-.028.008-.03.032v1.481c0 .09-.004.082.082.082h.913c.082 0 .072.128.072.128V11.19s.003.117-.06.117h-1.482c-.068 0-.06.082-.06.082v1.445s-.01.068.064.068h1.457c.082 0 .076-.006.076.079v3.225c0 .088-.007.081.082.081h1.43c.09 0 .082.007.082-.08v-3.27c0-.029.006-.035.033-.035l2.323-.003c.098 0 .191.02.28.061a.46.46 0 0 1 .274.407c.008.395.003.79.003 1.185 0 .259-.107.367-.33.367h-1.218c-.023.002-.029.008-.028.033.184.437.374.871.57 1.303a.045.045 0 0 0 .04.026c.17.005.34.002.51.003.15-.002.517.004.666-.01a2.03 2.03 0 0 0 .408-.075c.59-.18.975-.698.976-1.313v-1.981c0-.128-.01-.254-.034-.38 0 .078-.029-.641-.724-.998z"/></svg>""",
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
        qr_src = (s.get("qr_src") or "").strip()
        extra = ""
        if href.startswith("http"):
            extra = ' target="_blank" rel="noopener"'
        anchor = f"""                    <a href="{attr_esc(href)}" class="social-icon" title="{title}"{extra}>
                        {svg}
                    </a>"""
        if qr_src:
            alt_raw = s.get("qr_alt") or f"{s.get('title', '')} QR code"
            alt = esc(alt_raw)
            out.append(
                f"""                <span class="social-icon-wrap">
{anchor}
                    <span class="social-qr-tooltip" role="tooltip">
                        <img src="{attr_esc(qr_src)}" alt="{alt}" width="128" height="128" loading="lazy">
                    </span>
                </span>"""
            )
        else:
            out.append(anchor)
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
