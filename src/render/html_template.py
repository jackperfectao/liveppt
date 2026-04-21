"""HTML template and rendering for LivePPT deck generation."""

import html
import json
from typing import Dict

from src.core.themes import resolve_theme


HTML_TEMPLATE = """<!doctype html>
<html lang=\"zh-CN\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>{page_title}</title>
    <style>
      :root {{
        color-scheme: {color_scheme};
        --bg: {bg};
        --bg-strong: {bg_strong};
        --surface: {surface};
        --surface-strong: {surface_strong};
        --line: {line};
        --text: {text};
        --text-soft: {text_soft};
        --accent: {accent};
        --accent-deep: {accent_deep};
        --success: {success};
        --shadow: {shadow};
        --display: \"Bodoni MT\", \"Didot\", \"Songti SC\", serif;
        --body: \"Inter\", \"PingFang SC\", \"Microsoft YaHei\", sans-serif;
      }}
      * {{ box-sizing: border-box; }}
      html, body {{ margin: 0; min-height: 100%; }}
      body {{
        font-family: var(--body);
        color: var(--text);
        background:
          radial-gradient(circle at top left, color-mix(in srgb, var(--accent) 24%, transparent), transparent 28%),
          radial-gradient(circle at bottom right, color-mix(in srgb, var(--accent-deep) 18%, transparent), transparent 32%),
          linear-gradient(180deg, var(--bg-strong) 0%, var(--bg) 100%);
      }}
      .deck {{ min-height: 100vh; padding: 24px 24px 116px; }}
      .progress {{ position: fixed; top: 0; left: 0; width: 100%; height: 4px; background: color-mix(in srgb, var(--accent) 12%, transparent); z-index: 50; }}
      .progress-bar {{ height: 100%; width: 0; background: linear-gradient(90deg, var(--accent-deep), var(--accent)); transition: width 240ms ease; }}
      .shell {{
        width: min(1120px, 100%);
        min-height: calc(100vh - 140px);
        margin: 28px auto 0;
        border-radius: 36px;
        border: 1px solid var(--line);
        background: linear-gradient(180deg, var(--surface-strong) 0%, var(--surface) 100%);
        box-shadow: var(--shadow);
        padding: 40px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        position: relative;
        overflow: hidden;
      }}
      .shell::after {{
        content: \"\";
        position: absolute;
        right: -120px;
        top: -120px;
        width: 320px;
        height: 320px;
        border-radius: 999px;
        background: radial-gradient(circle, color-mix(in srgb, var(--accent) 16%, transparent) 0%, transparent 72%);
        pointer-events: none;
      }}
      .eyebrow {{
        display: inline-flex; align-items: center; gap: 8px; padding: 8px 14px; border-radius: 999px;
        background: color-mix(in srgb, var(--accent) 10%, transparent); border: 1px solid var(--line); color: var(--accent-deep);
        font-size: 12px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase;
      }}
      h1, h2 {{ margin: 0; font-family: var(--display); letter-spacing: -0.02em; line-height: 1.05; }}
      h1 {{ font-size: clamp(2.4rem, 5vw, 4.6rem); max-width: 11ch; }}
      h2 {{ font-size: clamp(2rem, 4vw, 3.4rem); }}
      .subtitle {{ margin-top: 18px; color: var(--text-soft); font-size: 1.05rem; line-height: 1.8; max-width: 58ch; }}
      .meta {{ display: flex; gap: 10px; flex-wrap: wrap; margin-top: 18px; }}
      .chip {{
        padding: 10px 14px; border-radius: 16px; border: 1px solid var(--line);
        background: color-mix(in srgb, var(--surface-strong) 82%, transparent); color: var(--text-soft); font-size: 13px; line-height: 1.5;
      }}
      .chip strong {{ color: var(--text); }}
      .content {{ display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 24px; margin-top: 28px; }}
      .card {{ border: 1px solid var(--line); border-radius: 24px; padding: 22px; background: color-mix(in srgb, var(--surface-strong) 88%, transparent); }}
      .card h3 {{ margin: 0 0 14px; font-size: 13px; letter-spacing: 0.10em; text-transform: uppercase; color: var(--accent-deep); }}
      .paragraphs p {{ margin: 0 0 14px; line-height: 1.8; color: var(--text-soft); font-size: 1rem; }}
      .bullets {{ margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 12px; color: var(--text-soft); line-height: 1.7; }}
      .bullets li::marker {{ color: var(--accent); }}
      .empty {{ color: var(--text-soft); font-style: italic; }}
      .cover-grid {{ display: grid; grid-template-columns: 1.05fr 0.95fr; gap: 24px; align-items: stretch; margin-top: 28px; }}
      .hero-panel {{ display: flex; flex-direction: column; justify-content: space-between; gap: 20px; }}
      .hero-panel .subtitle {{ max-width: 100%; }}
      .brand-card {{ display: grid; place-items: center; min-height: 320px; text-align: center; }}
      .brand-mark {{
        width: 128px; height: 128px; border-radius: 32px; display: grid; place-items: center; font-size: 42px; font-weight: 900;
        background: linear-gradient(135deg, var(--accent), var(--accent-deep)); color: var(--bg-strong); box-shadow: var(--shadow);
      }}
      .brand-name {{ margin-top: 20px; font-size: 1.2rem; font-weight: 800; color: var(--text); letter-spacing: 0.04em; }}
      .brand-caption {{ margin-top: 8px; color: var(--text-soft); line-height: 1.7; font-size: 0.95rem; }}
      .section-split {{ display: grid; gap: 24px; grid-template-columns: 1.1fr 0.9fr; margin-top: 28px; }}
      .summary-grid {{ display: grid; gap: 14px; margin-top: 28px; }}
      .summary-item {{ border: 1px solid var(--line); border-radius: 20px; padding: 16px; background: color-mix(in srgb, var(--surface-strong) 88%, transparent); color: var(--text-soft); line-height: 1.7; }}
      .summary-item strong {{ color: var(--success); }}
      .footer {{ position: fixed; left: 18px; right: 18px; bottom: 18px; z-index: 40; }}
      .toolbar {{
        width: min(1120px, calc(100% - 36px)); margin: 0 auto; border-radius: 18px; border: 1px solid var(--line);
        background: color-mix(in srgb, var(--surface-strong) 94%, transparent); backdrop-filter: blur(10px); box-shadow: 0 14px 28px rgba(96,65,31,0.10);
        padding: 12px; display: grid; grid-template-columns: 1fr auto auto; gap: 12px; align-items: center;
      }}
      .hint {{ font-size: 13px; color: var(--text-soft); font-weight: 600; }}
      .dots {{ display: inline-flex; gap: 8px; }}
      .dots button {{ width: 10px; height: 10px; border-radius: 999px; border: none; background: color-mix(in srgb, var(--accent) 30%, transparent); cursor: pointer; }}
      .dots button.active {{ width: 36px; background: linear-gradient(90deg, var(--accent-deep), var(--accent)); }}
      .controls {{ display: inline-flex; gap: 8px; }}
      button.ctrl {{ border: 1px solid var(--line); background: color-mix(in srgb, var(--surface-strong) 92%, transparent); color: var(--text); border-radius: 10px; padding: 10px 14px; font-weight: 700; cursor: pointer; }}
      button.ctrl:disabled {{ opacity: 0.45; cursor: not-allowed; }}
      .footer-brand {{ position: fixed; top: 20px; right: 22px; font-size: 12px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-soft); opacity: 0.74; z-index: 60; }}
      @media (max-width: 900px) {{
        .deck {{ padding: 14px 14px 136px; }}
        .shell {{ padding: 24px; border-radius: 24px; min-height: calc(100vh - 168px); }}
        .content, .cover-grid, .section-split {{ grid-template-columns: 1fr; }}
        .toolbar {{ grid-template-columns: 1fr; }}
        .dots {{ justify-content: center; }}
        .controls {{ width: 100%; }}
        button.ctrl {{ flex: 1; }}
        .footer-brand {{ right: 16px; top: 14px; }}
      }}
    </style>
  </head>
  <body>
    <div class=\"footer-brand\">{brand_label}</div>
    <div class=\"progress\"><div id=\"progressBar\" class=\"progress-bar\"></div></div>
    <div class=\"deck\">
      <main id=\"app\"></main>
    </div>
    <footer class=\"footer\">
      <div class=\"toolbar\">
        <div id=\"hint\" class=\"hint\"></div>
        <div id=\"dots\" class=\"dots\"></div>
        <div class=\"controls\">
          <button id=\"prevBtn\" class=\"ctrl\">上一页</button>
          <button id=\"nextBtn\" class=\"ctrl\">下一页</button>
        </div>
      </div>
    </footer>
    <script>
      const deck = {deck_json};
      const app = document.getElementById('app');
      const progressBar = document.getElementById('progressBar');
      const hint = document.getElementById('hint');
      const dots = document.getElementById('dots');
      const prevBtn = document.getElementById('prevBtn');
      const nextBtn = document.getElementById('nextBtn');
      let current = 0;

      function escapeHtml(value) {{
        return String(value)
          .replaceAll('&', '&amp;')
          .replaceAll('<', '&lt;')
          .replaceAll('>', '&gt;')
          .replaceAll('"', '&quot;')
          .replaceAll("'", '&#39;');
      }}

      function initials(value) {{
        const text = String(value || '').trim();
        if (!text) return 'LP';
        return text.replace(/[^A-Za-z0-9一-鿿]/g, '').slice(0, 2).toUpperCase() || 'LP';
      }}

      function renderChips(tags) {{
        if (!tags || !tags.length) return '';
        return `<div class=\"meta\">${{tags.map((item) => `<div class=\"chip\"><strong>${{escapeHtml(item.key)}}：</strong>${{escapeHtml(item.value)}}</div>`).join('')}}</div>`;
      }}

      function renderParagraphs(paragraphs) {{
        if (!paragraphs || !paragraphs.length) return `<div class=\"empty\">这个页面当前没有补充正文，建议在 plan.md 对应章节下补一两段说明。</div>`;
        return `<div class=\"paragraphs\">${{paragraphs.map((text) => `<p>${{escapeHtml(text)}}</p>`).join('')}}</div>`;
      }}

      function renderBullets(bullets) {{
        if (!bullets || !bullets.length) return `<div class=\"empty\">这个页面当前没有要点列表。</div>`;
        return `<ul class=\"bullets\">${{bullets.map((text) => `<li>${{escapeHtml(text)}}</li>`).join('')}}</ul>`;
      }}

      function renderCover(slide) {{
        return `
          <section class=\"shell\">
            <div class=\"cover-grid\">
              <div class=\"hero-panel\">
                <div>
                  <span class=\"eyebrow\">${{escapeHtml(deck.brand)}} · HTML Deck</span>
                  <h1>${{escapeHtml(slide.title)}}</h1>
                  <div class=\"subtitle\">${{escapeHtml(deck.subtitle)}}</div>
                  ${{renderChips(slide.tags)}}
                </div>
                <div class=\"card\">
                  <h3>封面说明</h3>
                  <div class=\"paragraphs\">
                    <p>这是由 LivePPT 自动生成的演示页。</p>
                    <p>你可以继续改 Markdown 内容，也可以切换主题风格，让输出更接近真实发布页面。</p>
                  </div>
                </div>
              </div>
              <div class=\"card brand-card\">
                <div>
                  <div class=\"brand-mark\">${{escapeHtml(initials(deck.brand))}}</div>
                  <div class=\"brand-name\">${{escapeHtml(deck.brand)}}</div>
                  <div class=\"brand-caption\">${{slide.paragraphs?.length ? escapeHtml(slide.paragraphs.join(' ')) : '把 plan.md 变成可以直接打开和分享的 HTML deck。'}}</div>
                </div>
              </div>
            </div>
          </section>
        `;
      }}

      function renderSummary(slide) {{
        return `
          <section class=\"shell\">
            <div>
              <span class=\"eyebrow\">Summary</span>
              <h2>${{escapeHtml(slide.title)}}</h2>
              ${{renderChips(slide.tags)}}
            </div>
            <div class=\"summary-grid\">
              ${{(slide.bullets || []).map((item) => `<div class=\"summary-item\"><strong>✓</strong> ${{escapeHtml(item)}}</div>`).join('')}}
            </div>
          </section>
        `;
      }}

      function renderContent(slide) {{
        return `
          <section class=\"shell\">
            <div>
              <span class=\"eyebrow\">${{escapeHtml(slide.nav || '内容')}}</span>
              <h2>${{escapeHtml(slide.title)}}</h2>
              ${{renderChips(slide.tags)}}
            </div>
            <div class=\"section-split\">
              <div class=\"card\">
                <h3>正文</h3>
                ${{renderParagraphs(slide.paragraphs)}}
              </div>
              <div class=\"card\">
                <h3>要点</h3>
                ${{renderBullets(slide.bullets)}}
              </div>
            </div>
          </section>
        `;
      }}

      function renderSlide(slide) {{
        if (slide.type === 'cover') return renderCover(slide);
        if (slide.type === 'summary') return renderSummary(slide);
        return renderContent(slide);
      }}

      function renderDots() {{
        dots.innerHTML = deck.slides.map((slide, index) => `<button data-index=\"${{index}}\" class=\"${{index === current ? 'active' : ''}}\" aria-label=\"${{escapeHtml(slide.nav || slide.title)}}\"></button>`).join('');
      }}

      function render() {{
        const slide = deck.slides[current];
        app.innerHTML = renderSlide(slide);
        hint.textContent = `${{String(current + 1).padStart(2, '0')}} / ${{String(deck.slides.length).padStart(2, '0')}} · ${{slide.nav || slide.title}}`;
        progressBar.style.width = `${{((current + 1) / deck.slides.length) * 100}}%`;
        prevBtn.disabled = current === 0;
        nextBtn.disabled = current === deck.slides.length - 1;
        renderDots();
      }}

      prevBtn.addEventListener('click', () => {{ if (current > 0) {{ current -= 1; render(); }} }});
      nextBtn.addEventListener('click', () => {{ if (current < deck.slides.length - 1) {{ current += 1; render(); }} }});
      dots.addEventListener('click', (event) => {{
        const button = event.target.closest('button[data-index]');
        if (!button) return;
        current = Number(button.dataset.index) || 0;
        render();
      }});
      document.addEventListener('keydown', (event) => {{
        if (event.key === 'ArrowRight' || event.key === ' ') {{ event.preventDefault(); if (current < deck.slides.length - 1) {{ current += 1; render(); }} }}
        if (event.key === 'ArrowLeft') {{ event.preventDefault(); if (current > 0) {{ current -= 1; render(); }} }}
        if (event.key === 'Home') {{ current = 0; render(); }}
        if (event.key === 'End') {{ current = deck.slides.length - 1; render(); }}
      }});
      render();
    </script>
  </body>
</html>
"""


def render_html(deck: dict, theme_tokens: Dict[str, str]) -> str:
    return HTML_TEMPLATE.format(
        page_title=html.escape(deck["title"]),
        deck_json=json.dumps(deck, ensure_ascii=False),
        brand_label=html.escape(deck["brand"]),
        color_scheme="dark" if theme_tokens["bg"].startswith("#0") else "light",
        bg=theme_tokens["bg"],
        bg_strong=theme_tokens["bg_strong"],
        surface=theme_tokens["surface"],
        surface_strong=theme_tokens["surface_strong"],
        line=theme_tokens["line"],
        text=theme_tokens["text"],
        text_soft=theme_tokens["text_soft"],
        accent=theme_tokens["accent"],
        accent_deep=theme_tokens["accent_deep"],
        success=theme_tokens["success"],
        shadow=theme_tokens["shadow"],
    )
