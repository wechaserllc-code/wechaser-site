# wechaser-site

Source for [wechaser.ai](https://wechaser.ai) — WeChaser, enterprise AI middleware.

## Stack
- Static HTML + CSS + vanilla JS
- Shared design system (`styles.css`, ~365 lines)
- Bilingual ZH/EN (toggle + localStorage persist)
- No build step — drop into any static host

## Pages
- `/` · home
- `/products/shiguangmailuo.html` · 时光脉络 product page
- `/cases/chaoxian.html` · Chaostring Tech case study
- `/tech.html` · architecture deep-dive
- `/about.html` · company / values / team

## Local preview
```bash
cd ~/wechaser-site
python3 -m http.server 8765
open http://localhost:8765/
```

## Deploy
See [`DEPLOY.md`](./DEPLOY.md). Target is Cloudflare Pages with custom domain on `wechaser.ai`.

## Archived versions
- `v1-eastern-minimalism.html` — first iteration (warm paper + 朱砂 seal)
- `v2-vibrant-minimal.html` — second iteration (off-white + lime, kinetic)
- `index.html` is currently v3 (hardcore dark + lime + cyan)

---

© 2026 WeChaser LLC
