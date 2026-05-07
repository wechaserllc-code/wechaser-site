# wechaser-site

Source for [wechaser.ai](https://wechaser.ai) — WeChaser, enterprise AI middleware.

## Stack
- Static HTML + CSS + vanilla JS — no build step
- Shared design system (`styles.css`)
- Bilingual ZH/EN (toggle + localStorage persist)
- Cloudflare Pages auto-deploy from `main`

## Site map

```
/                              home
/products/shiguangmailuo       时光脉络 product page
/services/consulting           咨询服务详情
/services/integration          飞书 / 钉钉接入
/services/document-ops         文档整理伴生服务
/cases/                        匿名化案例 + 6 行业场景
/pricing                       报价模型
/tech                          架构深度
/about                         公司 / 价值观 / 团队
/404                           错误页
```

## Other files

- `styles.css` · shared design tokens + components
- `js/site.js` · nav scroll, language toggle, reveal-on-scroll
- `robots.txt` · allow search · block AI training crawlers (GPTBot / ClaudeBot / Google-Extended / CCBot)
- `sitemap.xml` · for search engines
- `_redirects` · Cloudflare Pages redirects (legacy URLs → new)
- `og-image.svg` / `og-image.png` · social share card (1200×630)
- `DEPLOY.md` · runbook used during initial Cloudflare wiring (kept for history)

## Local preview

```bash
cd ~/wechaser-site
python3 -m http.server 8765
# open http://localhost:8765
```

## Deploy

Push to `main`. Cloudflare Pages picks up the webhook and republishes within ~30s.

- **CF Pages project**: `wechaser-site`
- **Custom domain**: [wechaser.ai](https://wechaser.ai)
- **DNS**: Cloudflare nameservers (`tony/joyce.ns.cloudflare.com`)

## Archived design iterations

- `v1-eastern-minimalism.html` — first iteration (warm paper + 朱砂 seal)
- `v2-vibrant-minimal.html` — second iteration (off-white + lime, kinetic hero)
- `index.html` is currently v3 (硬核暗色 + lime + cyan)

---

Proprietary. © 2026 WeChaser LLC.
