# WeChaser — Deploy Runbook

Target: **wechaser.ai** → Cloudflare Pages (free, fast, edge SSL)

Code lives at: `https://github.com/xuansir321/wechaser-site`

---

## Status snapshot

- ✅ Repo created (public): `xuansir321/wechaser-site`
- ✅ All v3 pages pushed (`main` branch)
- ✅ GitHub Pages enabled at `https://xuansir321.github.io/wechaser-site/` (preview only — internal links break under sub-path)
- ⏳ Cloudflare account: needs creation
- ⏳ DNS: currently at GoDaddy (NS `ns23/24.domaincontrol.com`), pointed at Lovable's IPs
- ⏳ Custom domain on Pages: not connected

---

## Strategy

Move DNS authority to Cloudflare (full delegation). This gives:
- Free SSL on apex + `www`
- One-click custom-domain on Pages (CF auto-creates the CNAME)
- Free CDN, analytics, bot protection
- Clean kill of the current Lovable site (DNS no longer points there)

There is a non-NS-migration alternative (CNAME flattening at GoDaddy), included at bottom for reference. Skip unless you have a specific reason not to use Cloudflare for DNS.

---

## Step-by-step (you do steps 1-3, 5-7; I prepped 0, 4)

### 0. (already done) GitHub repo + push

```
$ gh repo view xuansir321/wechaser-site --web
```

---

### 1. Sign up Cloudflare (5 min)

1. Open https://dash.cloudflare.com/sign-up
2. Use email `wechaserllc@gmail.com` (per your global config)
3. Verify email
4. Skip the upsell — go straight to **Add a Site**

---

### 2. Add `wechaser.ai` as a zone (5 min)

1. Cloudflare dashboard → **Add a Site** → enter `wechaser.ai`
2. Pick **Free** plan
3. Cloudflare scans existing DNS at GoDaddy — review the records it finds.
   - You'll see existing A records (Lovable's `15.197.225.128`, `3.33.251.168`)
   - **Delete the A records** that point to Lovable (we want clean state). Or leave them — they'll be overridden in step 6 anyway.
4. Cloudflare gives you **2 nameservers** like:
   ```
   abigail.ns.cloudflare.com
   davis.ns.cloudflare.com
   ```
   (yours will be different — write yours down)

---

### 3. Change nameservers at GoDaddy (5 min, propagation ~10 min)

1. Open https://account.godaddy.com → My Products → `wechaser.ai` → **DNS**
2. Scroll to **Nameservers** section → click **Change Nameservers**
3. Switch from "I'll use my own nameservers" or "Default" to **Custom**
4. Replace with the 2 Cloudflare NS from step 2
5. Save
6. Back in Cloudflare → click **Done, check nameservers** → CF will email you when active (usually 5-10 min, sometimes up to 24h)

> ⚠️ Once NS changes, GoDaddy DNS is no longer authoritative. The existing Lovable site at `wechaser.ai` will go offline within ~10 min. (You confirmed this is desired.)

---

### 4. (already done by me) Verify code on GitHub

```
$ open https://github.com/xuansir321/wechaser-site
```

---

### 5. Create Cloudflare Pages project (5 min)

Wait until step 3's email confirms the zone is active before doing this.

1. CF dashboard → left sidebar → **Workers & Pages** → **Create**
2. Tab: **Pages** → **Connect to Git**
3. Click **GitHub** → authorize Cloudflare (one-time GitHub OAuth)
4. Pick the repo: `xuansir321/wechaser-site`
5. **Begin setup**
6. Settings:
   | Field | Value |
   |---|---|
   | Project name | `wechaser-site` (auto-fills) |
   | Production branch | `main` |
   | Framework preset | **None** |
   | Build command | _(leave empty)_ |
   | Build output directory | `/` |
7. **Save and Deploy**
8. Wait ~30 seconds. You'll get a URL like `wechaser-site.pages.dev`. Test it loads.

---

### 6. Add custom domain (2 min)

1. In the Pages project → **Custom domains** tab → **Set up a custom domain**
2. Enter `wechaser.ai` → **Continue**
3. Cloudflare auto-detects the zone is on the same account → **Activate domain**
4. Repeat for `www.wechaser.ai` (optional but recommended; CF will set a redirect to apex)
5. SSL cert provisions in ~30s. Status flips to **Active**.

---

### 7. Verify (1 min)

```bash
# from your terminal
curl -sI https://wechaser.ai | head -5
# should return HTTP/2 200 with `cf-ray:` and `server: cloudflare`
```

Open https://wechaser.ai in browser. Check:
- [ ] Home renders v3 design (dark + lime)
- [ ] Nav links work (Product / Cases / Tech / About)
- [ ] Lang toggle ZH/EN works
- [ ] Counters animate
- [ ] Mobile responsive
- [ ] All 5 pages serve at HTTPS

---

## What happens to the old Lovable site

Once GoDaddy nameservers flip in step 3, GoDaddy DNS stops being authoritative for `wechaser.ai`. The Lovable A records become dead. Lovable still hosts your `wechaser-doorway.lovable.app` page — that subdomain is unaffected. You can keep it or delete it from Lovable's dashboard later.

---

## Future updates

Every push to `main` auto-deploys to wechaser.ai. Workflow:

```bash
cd /Users/xuansmacbook/wechaser-site
# edit files
git add -A
git commit -m "describe change"
git push
# CF Pages picks it up, deploys in ~30 seconds
```

Preview deploys: any push to a non-main branch gets a `<branch>.<project>.pages.dev` URL.

---

## Alternative path (skip the NS migration)

If you don't want to move DNS to Cloudflare:

1. Stay on GoDaddy DNS
2. After step 5 (you have `wechaser-site.pages.dev` live), in Pages → Custom domains → enter `wechaser.ai`
3. CF will say "DNS not on Cloudflare" and ask you to add a CNAME externally
4. Go to GoDaddy DNS → add CNAME: `@` → `wechaser-site.pages.dev` (apex CNAME via "ANAME" / CNAME flattening; GoDaddy supports this through "Forwarding" in some cases — may need workaround)

This is messier. Apex CNAME at GoDaddy is poorly supported. Recommended only if you can't change NS for other reasons.

---

## Rollback

If anything breaks and you want the Lovable site back:
1. GoDaddy → DNS → revert nameservers to GoDaddy defaults
2. Restore the Lovable A records in GoDaddy DNS
3. Wait 10 min for propagation

---

_Maintained from `~/wechaser-site/DEPLOY.md`. Update when deploy steps change._
