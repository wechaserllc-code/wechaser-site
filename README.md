# wechaser-site

Source for [wechaser.ai](https://wechaser.ai) — WeChaser, enterprise AI middleware.

## Stack
- Static HTML + CSS + vanilla JS
- **Bilingual sources in `src/`** → `scripts/build.py` generates Chinese pages at `/` and English pages at `/en/` (separate URLs, hreflang, per-language meta + JSON-LD)
- Self-hosted fonts in `fonts/` (no Google Fonts — it is blocked in mainland China); Chinese body text uses system fonts
- Cloudflare Pages auto-deploy from `main`; `functions/api/contact.js` handles the booking form

## Editing workflow

```bash
# 1. edit the bilingual source (keep <span data-zh>…</span><span data-en>…</span> pairs)
vim src/index.html
# 2. titles / descriptions / JSON-LD live in the PAGES table
vim scripts/build.py
# 3. regenerate (needs: pip install beautifulsoup4)
python3 scripts/build.py
```

Never edit the generated `*.html` at the root or under `en/` — they are overwritten.
The build warns about any untranslated Chinese left on English pages.

## Site map

```
/                              home                    /en/
/products/shiguangmailuo       时光脉络 product page    /en/products/shiguangmailuo
/compare                       方案对比                 /en/compare
/cases/                        匿名化案例 + 6 行业场景   /en/cases/
/services/consulting           咨询服务                 /en/services/consulting
/services/integration          飞书 / 钉钉接入           /en/services/integration
/services/document-ops         文档整理伴生服务          /en/services/document-ops
/pricing                       报价模型                 /en/pricing
/tech                          架构深度                 /en/tech
/about                         公司 / 交付保障 / 团队    /en/about
/404                           错误页（中英双语）
```

Cloudflare Pages serves `about.html` at `/about` and 308-redirects `/about.html` → `/about`; all canonicals and internal links use the pretty URLs.

## Other files

- `styles.css` · shared design tokens + components
- `js/site.js` · nav scroll, reveal, count-up, booking form submit
- `functions/api/contact.js` · POST `/api/contact` → Feishu bot webhook. **Set `FEISHU_WEBHOOK_URL`** in Cloudflare Pages → Settings → Environment variables; without it the form falls back to opening the visitor's email client
- `robots.txt` · open to search engines and AI crawlers (GEO)
- `llms.txt` · plain-text summary of the company for AI assistants
- `sitemap.xml` · generated, with hreflang alternates
- `_redirects` / `_headers` · Cloudflare Pages redirects and response headers
- `og-image.*`, `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png`, `icon-512.png`
- `DEPLOY.md` · runbook used during initial Cloudflare wiring (kept for history)

## Local preview

```bash
python3 scripts/build.py
python3 -m http.server 8765   # pretty URLs need the .html suffix locally, e.g. /about.html
```

## Deploy

Push to `main`. Cloudflare Pages picks up the webhook and republishes within ~30s.

- **CF Pages project**: `wechaser-site`
- **Custom domain**: [wechaser.ai](https://wechaser.ai)
- **DNS**: Cloudflare nameservers (`tony/joyce.ns.cloudflare.com`)

## Design history

v1 (东方留白 / 朱砂) and v2 (off-white + lime) were removed from the live site; they remain in git history.
The current design is v3 (硬核暗色 + lime + cyan). `brand-spec.md` / `visual-system.md` describe the v1 direction and are kept for reference.

---

Proprietary. © 2026 WeChaser LLC.
