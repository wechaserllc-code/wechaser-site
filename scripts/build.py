#!/usr/bin/env python3
"""
Build wechaser.ai from bilingual sources.

    python3 scripts/build.py

Sources live in src/ and keep the original bilingual markup
(<span data-zh>…</span><span data-en>…</span>). This script writes:

  /<page>       Chinese-only pages (zh-CN, the default)
  /en/<page>    English-only pages
  /sitemap.xml  with hreflang alternates

and injects a consistent <head> into every page: title, description,
canonical, hreflang, Open Graph, icons, self-hosted fonts and JSON-LD
(Organization / WebSite / BreadcrumbList / FAQPage / Product / Service).

Edit src/ and the PAGES table below, then re-run. Never edit the generated
files directly — they are overwritten. Requires: beautifulsoup4.
"""
from __future__ import annotations

import datetime as dt
import html
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
SITE = "https://wechaser.ai"
EMAIL = "hello@wechaser.ai"
TODAY = dt.date.today().isoformat()

ORG_NAME = "WeChaser"
ORG_LEGAL = "WeChaser LLC"
PRODUCT_ZH, PRODUCT_EN = "时光脉络", "Shiguangmailuo"

# ---------------------------------------------------------------------------
# Per-page metadata. `crumb` = breadcrumb label; `kind` drives JSON-LD.
# ---------------------------------------------------------------------------
PAGES: dict[str, dict] = {
    "index.html": dict(
        kind="home", priority="1.0",
        zh=dict(title="WeChaser · 面向制造企业的 AI 知识中间件 · 让飞书、钉钉、Claude 懂你的企业",
                desc="WeChaser 为制造企业部署 AI 知识中间件「时光脉络」：把图纸、SOP、客户档案、邮件变成带出处的知识层，飞书 AI、钉钉 AI、ChatGPT、Claude 通过 MCP / REST 直接调用。支持私有化部署，第一阶段调研免费，典型 12 周上线。",
                crumb="首页"),
        en=dict(title="WeChaser · AI knowledge middleware for manufacturers · Make Lark, DingTalk and Claude know your company",
                desc="WeChaser deploys Shiguangmailuo, an AI knowledge middleware for manufacturers: drawings, SOPs, customer records and email become a cited knowledge layer that Lark AI, DingTalk AI, ChatGPT and Claude call via MCP / REST. On-prem ready, free discovery phase, typically live in 12 weeks.",
                crumb="Home"),
    ),
    "products/shiguangmailuo.html": dict(
        kind="product", priority="0.9",
        zh=dict(title="时光脉络 · 企业 AI 知识中间件（MCP / REST / CLI）· WeChaser",
                desc="时光脉络是 WeChaser 的旗舰产品：企业 AI 知识中间件。向量库 + 知识图谱 + 全文三路混合检索，段落级溯源、证据不足即拒答；飞书 AI、钉钉 AI、Claude 等通过 MCP / CLI / REST 调用，文件原件留在本地。",
                crumb="时光脉络"),
        en=dict(title="Shiguangmailuo · Enterprise AI knowledge middleware (MCP / REST / CLI) · WeChaser",
                desc="Shiguangmailuo is WeChaser's flagship enterprise AI knowledge middleware: hybrid vector + knowledge-graph + full-text retrieval, paragraph-level citations, refusal when evidence is thin. Lark AI, DingTalk AI and Claude call it via MCP / CLI / REST; file originals stay on-prem.",
                crumb="Shiguangmailuo"),
    ),
    "cases/index.html": dict(
        kind="page", priority="0.9",
        zh=dict(title="案例与行业场景 · 制造 / 电商 / 法律等 · WeChaser",
                desc="WeChaser 在制造、电商、法律、医疗、教育、投资 6 个行业的使用场景，以及 3 个真实落地项目的实测数据。客户信息已匿名化处理。",
                crumb="案例"),
        en=dict(title="Cases & industry scenarios · Manufacturing, e-commerce, legal · WeChaser",
                desc="How WeChaser is used across manufacturing, e-commerce, legal, medical, education and investment — plus measured results from 3 live, anonymised engagements.",
                crumb="Cases"),
    ),
    "compare.html": dict(
        kind="page", priority="0.8",
        zh=dict(title="企业 AI 知识库怎么选：时光脉络 vs 飞书知识问答 / Dify / FastGPT / 自研 · WeChaser",
                desc="对比平台自带知识问答（飞书 / 钉钉）、开源 RAG 平台（Dify / FastGPT）、内部自研与 WeChaser 时光脉络在数据覆盖、私有化、溯源、权限、上线周期上的差异，附选型四问。",
                crumb="方案对比"),
        en=dict(title="Choosing an enterprise AI knowledge base: Shiguangmailuo vs Lark Q&A / Dify / FastGPT / in-house · WeChaser",
                desc="Built-in Lark/DingTalk Q&A, open-source RAG platforms (Dify / FastGPT), building in-house and WeChaser Shiguangmailuo compared on data coverage, on-prem, citations, permissions and time to value — plus four questions to decide.",
                crumb="Compare"),
    ),
    "tech.html": dict(
        kind="page", priority="0.8",
        zh=dict(title="技术架构 · grounded RAG / 知识图谱 / MCP · WeChaser",
                desc="WeChaser 技术架构：FastAPI + LangGraph + Neo4j + Qdrant + BGE Reranker，三路混合检索与段落级溯源；生成模型可用国内合规 API 或本地开源模型，可完全断网；通过 MCP Bridge 与飞书 Gateway 接入。",
                crumb="技术架构"),
        en=dict(title="Architecture · grounded RAG / knowledge graph / MCP · WeChaser",
                desc="WeChaser architecture: FastAPI + LangGraph + Neo4j + Qdrant + BGE Reranker, hybrid retrieval with paragraph-level citations; generation via approved API or local open-weight models, fully air-gappable; exposed through an MCP bridge and a Lark gateway.",
                crumb="Architecture"),
    ),
    "services/consulting.html": dict(
        kind="service", priority="0.8",
        zh=dict(title="AI 咨询服务 · 业务流程梳理与 AI 转型路线图 · WeChaser",
                desc="陪跑式 AI 咨询：业务流程梳理、AI 转型路线图、最小可落地试点设计。第一阶段调研免费，同期只服务 3–5 家深度客户。",
                crumb="咨询服务"),
        en=dict(title="AI consulting · Workflow audit and AI roadmap · WeChaser",
                desc="Hands-on AI consulting: workflow audit, AI transformation roadmap and smallest-viable pilot design. Discovery is free; we take only 3–5 deep engagements at a time.",
                crumb="Consulting"),
    ),
    "services/integration.html": dict(
        kind="service", priority="0.8",
        zh=dict(title="飞书 / 钉钉 / 企业微信 AI 知识库接入 · WeChaser",
                desc="把时光脉络知识中枢接到企业每天用的协作工具——飞书、钉钉、企业微信、Slack。原生 Bot SDK + Hermes Gateway，员工不换工具，AI 进入现有流程。",
                crumb="飞书 / 钉钉接入"),
        en=dict(title="Lark / DingTalk / WeCom AI knowledge integration · WeChaser",
                desc="Plug the Shiguangmailuo knowledge hub into the tools your team already uses — Lark, DingTalk, WeCom and Slack. Native Bot SDK + Hermes Gateway; nobody switches tools.",
                crumb="Lark / DingTalk integration"),
    ),
    "services/document-ops.html": dict(
        kind="service", priority="0.8",
        zh=dict(title="企业文档整理服务 · OCR / 结构化 / 入库 · WeChaser",
                desc="AI 协助把 PDF、Word、扫描件、Excel、PPT 整理成标准格式，并做内容质检与入库。OCR + 结构化解析 + 段落级元数据，为知识库打好底座。",
                crumb="文档整理服务"),
        en=dict(title="Enterprise document ops · OCR, structuring, ingestion · WeChaser",
                desc="AI-assisted conversion of PDFs, Word, scans, Excel and PPT into clean structured formats, with content QA and ingestion. OCR + structured parsing + paragraph-level metadata — the foundation for a usable knowledge base.",
                crumb="Document ops"),
    ),
    "pricing.html": dict(
        kind="page", priority="0.7",
        zh=dict(title="报价 · 第一阶段免费 · 按里程碑付款 · WeChaser",
                desc="WeChaser 报价模型：三阶段、按里程碑付款、第一阶段调研免费、任意阶段可终止。咨询 / 集成 / 文档运营三类服务的典型区间 ¥30K–¥350K，不收 SaaS 订阅费。",
                crumb="报价"),
        en=dict(title="Pricing · Free discovery · Milestone billing · WeChaser",
                desc="WeChaser pricing: three phases, milestone billing, free discovery, stop at any phase. Typical ranges for consulting, integration and document ops are ¥30K–¥350K. No SaaS subscription.",
                crumb="Pricing"),
    ),
    "about.html": dict(
        kind="about", priority="0.7",
        zh=dict(title="关于 WeChaser · 创始人与交付保障",
                desc="WeChaser 是一家以“创始人 + AI 协同”模式运作的企业 AI 中间件公司。公开商业模型与技术决策；系统部署在客户服务器，驻场直到客户内部接管。",
                crumb="关于"),
        en=dict(title="About WeChaser · Founder and delivery guarantees",
                desc="WeChaser is an enterprise AI middleware company run as founder + AI co-workers. Business model and technical decisions are public; systems run on the client's servers, with on-site support until the client's team takes over.",
                crumb="About"),
    ),
    "404.html": dict(
        kind="404", priority=None,
        zh=dict(title="404 · 页面不存在 · WeChaser", desc="找不到这个页面 · WeChaser", crumb="404"),
        en=None,  # Cloudflare Pages serves the root 404.html for every miss
    ),
}

LANGS = {
    "zh": dict(html_lang="zh-CN", og_locale="zh_CN", hreflang="zh-CN", prefix=""),
    "en": dict(html_lang="en", og_locale="en_US", hreflang="en", prefix="/en"),
}
OTHER = {"zh": "en", "en": "zh"}

# ---------------------------------------------------------------------------
# URL helpers
# ---------------------------------------------------------------------------

def clean_path(rel: str) -> str:
    """src-relative file -> pretty URL path (Cloudflare Pages strips .html)."""
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel[: -len(".html")]


def page_url(rel: str, lang: str) -> str:
    return LANGS[lang]["prefix"] + clean_path(rel)


def out_file(rel: str, lang: str) -> Path:
    return ROOT / rel if lang == "zh" else ROOT / "en" / rel


NON_PAGE_PREFIXES = ("/api/", "/fonts/", "/js/", "/og-image", "/favicon", "/apple-touch", "/icon-", "/llms", "/robots", "/sitemap", "/styles.css")


def rewrite_href(href: str, lang: str) -> str:
    if not href.startswith("/") or href.startswith("//") or href.startswith(NON_PAGE_PREFIXES):
        return href
    path, sep, frag = href.partition("#")
    if path.endswith("/index.html"):
        path = path[: -len("index.html")]
    elif path.endswith(".html"):
        path = path[: -len(".html")]
    if lang == "en":
        path = "/en" + path
    return path + sep + frag


# ---------------------------------------------------------------------------
# JSON-LD
# ---------------------------------------------------------------------------

def org_ld(lang: str) -> dict:
    return {
        "@type": "Organization",
        "@id": f"{SITE}/#org",
        "name": ORG_NAME,
        "legalName": ORG_LEGAL,
        "url": f"{SITE}/",
        "logo": f"{SITE}/icon-512.png",
        "email": EMAIL,
        "foundingDate": "2025",
        "description": (
            "WeChaser 为制造企业部署 AI 知识中间件，让飞书、钉钉、ChatGPT、Claude 等 AI 工具调用企业真实知识，回答带出处，支持私有化部署。"
            if lang == "zh" else
            "WeChaser deploys AI knowledge middleware for manufacturers so Lark, DingTalk, ChatGPT and Claude can use real company knowledge — cited answers, on-prem ready."
        ),
        "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "email": EMAIL,
                          "availableLanguage": ["zh-CN", "en"]},
        "knowsAbout": ["Retrieval-augmented generation", "Knowledge graph", "Model Context Protocol",
                       "Enterprise knowledge management", "Lark / Feishu integration", "DingTalk integration"],
    }


def website_ld(lang: str) -> dict:
    return {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": ORG_NAME,
            "publisher": {"@id": f"{SITE}/#org"}, "inLanguage": LANGS[lang]["html_lang"]}


def breadcrumb_ld(rel: str, lang: str) -> dict | None:
    if rel in ("index.html", "404.html"):
        return None
    items = [("index.html", PAGES["index.html"][lang]["crumb"])]
    if rel.startswith("services/"):
        items.append((None, "服务" if lang == "zh" else "Services"))
    items.append((rel, PAGES[rel][lang]["crumb"]))
    out = []
    for i, (r, name) in enumerate(items, 1):
        el = {"@type": "ListItem", "position": i, "name": name}
        if r:
            el["item"] = SITE + page_url(r, lang)
        out.append(el)
    return {"@type": "BreadcrumbList", "itemListElement": out}


def faq_ld(soup: BeautifulSoup) -> dict | None:
    qas = []
    for d in soup.select("#faq details"):
        q, a = d.find("summary"), d.find("p")
        if q and a:
            qas.append({"@type": "Question", "name": q.get_text(" ", strip=True),
                        "acceptedAnswer": {"@type": "Answer", "text": a.get_text(" ", strip=True)}})
    return {"@type": "FAQPage", "mainEntity": qas} if qas else None


def kind_ld(rel: str, lang: str, meta: dict) -> dict | None:
    kind = PAGES[rel]["kind"]
    url = SITE + page_url(rel, lang)
    if kind == "product":
        return {
            "@type": "SoftwareApplication",
            "name": PRODUCT_ZH if lang == "zh" else PRODUCT_EN,
            "alternateName": PRODUCT_EN if lang == "zh" else PRODUCT_ZH,
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Linux (docker-compose, on-prem)",
            "description": meta["desc"], "url": url,
            "publisher": {"@id": f"{SITE}/#org"},
            "featureList": (["向量 + 知识图谱 + 全文混合检索", "段落级溯源，证据不足即拒答", "MCP / CLI / REST 调用",
                             "飞书 / 钉钉 / 企业微信接入", "私有化部署，可断网运行"] if lang == "zh" else
                            ["Hybrid vector + knowledge-graph + full-text retrieval", "Paragraph-level citations; refuses when evidence is thin",
                             "MCP / CLI / REST access", "Lark / DingTalk / WeCom integration", "On-prem, air-gappable deployment"]),
        }
    if kind == "service":
        return {"@type": "Service", "name": meta["crumb"], "description": meta["desc"], "url": url,
                "provider": {"@id": f"{SITE}/#org"},
                "areaServed": [{"@type": "Country", "name": "China"}, {"@type": "Place", "name": "Worldwide (remote)"}]}
    if kind == "about":
        return {"@type": "AboutPage", "url": url, "about": {"@id": f"{SITE}/#org"}}
    return None


# ---------------------------------------------------------------------------
# Page transform
# ---------------------------------------------------------------------------

def head_html(rel: str, lang: str, meta: dict, ld: list[dict], has_en: bool) -> str:
    L = LANGS[lang]
    url = SITE + page_url(rel, lang)
    e = lambda s: html.escape(s, quote=True)
    lines = [
        '<meta charset="utf-8" />',
        '<meta name="viewport" content="width=device-width,initial-scale=1" />',
        f"<title>{e(meta['title'])}</title>",
        f'<meta name="description" content="{e(meta["desc"])}" />',
    ]
    if rel == "404.html":
        lines.append('<meta name="robots" content="noindex" />')
    else:
        lines.append(f'<link rel="canonical" href="{url}" />')
        if has_en:
            lines += [
                f'<link rel="alternate" hreflang="zh-CN" href="{SITE + page_url(rel, "zh")}" />',
                f'<link rel="alternate" hreflang="en" href="{SITE + page_url(rel, "en")}" />',
                f'<link rel="alternate" hreflang="x-default" href="{SITE + page_url(rel, "zh")}" />',
            ]
    lines += [
        '<meta property="og:type" content="website" />',
        f'<meta property="og:site_name" content="{ORG_NAME}" />',
        f'<meta property="og:url" content="{url}" />',
        f'<meta property="og:title" content="{e(meta["title"])}" />',
        f'<meta property="og:description" content="{e(meta["desc"])}" />',
        f'<meta property="og:image" content="{SITE}/og-image.png" />',
        '<meta property="og:image:width" content="1200" />',
        '<meta property="og:image:height" content="630" />',
        f'<meta property="og:locale" content="{L["og_locale"]}" />',
        f'<meta property="og:locale:alternate" content="{LANGS[OTHER[lang]]["og_locale"]}" />',
        '<meta name="twitter:card" content="summary_large_image" />',
        f'<meta name="twitter:title" content="{e(meta["title"])}" />',
        f'<meta name="twitter:description" content="{e(meta["desc"])}" />',
        f'<meta name="twitter:image" content="{SITE}/og-image.png" />',
        '<meta name="theme-color" content="#060608" />',
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml" />',
        '<link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32" />',
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png" />',
        '<link rel="preload" href="/fonts/inter-tight-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin />',
        '<link rel="stylesheet" href="/fonts/fonts.css" />',
        '<link rel="stylesheet" href="/styles.css" />',
    ]
    if ld:
        graph = {"@context": "https://schema.org", "@graph": ld}
        lines.append('<script type="application/ld+json">' + json.dumps(graph, ensure_ascii=False, separators=(",", ":")) + "</script>")
    return "\n".join(lines) + "\n"


HEAD_DROP = re.compile(r"^(title|meta|link)$")


def build_page(rel: str, lang: str) -> str:
    src = (SRC / rel).read_text(encoding="utf-8")
    soup = BeautifulSoup(src, "html.parser")
    meta = PAGES[rel][lang]
    has_en = PAGES[rel]["en"] is not None

    # 1. keep only this language's content
    drop, keep = f"data-{OTHER[lang]}", f"data-{lang}"
    if rel == "404.html":
        drop = None  # 404 stays bilingual (single page for both)
    if drop:
        for el in soup.find_all(attrs={drop: True}):
            el.decompose()
    for el in soup.find_all(attrs={keep: True}):
        del el[keep]
    if rel == "404.html":
        for el in soup.find_all(attrs={"data-en": True}):
            del el["data-en"]

    soup.html["lang"] = LANGS[lang]["html_lang"]

    # 2. rebuild <head>: drop old meta/links, keep page <style>
    head = soup.head
    for el in list(head.find_all(HEAD_DROP, recursive=False)):
        el.decompose()
    ld = [org_ld(lang), website_ld(lang)]
    for extra in (breadcrumb_ld(rel, lang), kind_ld(rel, lang, meta), faq_ld(soup)):
        if extra:
            ld.append(extra)
    head.insert(0, BeautifulSoup(head_html(rel, lang, meta, ld, has_en), "html.parser"))

    # 3. links → pretty, language-prefixed URLs
    for a in soup.find_all("a", href=True):
        a["href"] = rewrite_href(a["href"], lang)
    for s in soup.find_all("script", src=True):
        if not s["src"].startswith(("http", "/")):
            s["src"] = "/" + s["src"].lstrip("./")

    # 4. language switch: a real link to the other language's URL
    tog = soup.find(id="langToggle")
    if tog:
        if has_en:
            other = OTHER[lang]
            new = soup.new_tag("a", attrs={
                "class": "lang-toggle", "id": "langToggle", "href": page_url(rel, other),
                "hreflang": LANGS[other]["hreflang"], "lang": LANGS[other]["html_lang"],
                "aria-label": "English version" if lang == "zh" else "中文版",
            })
            zh = soup.new_tag("span", attrs={"class": "zh" + (" on" if lang == "zh" else "")}); zh.string = "中"
            en = soup.new_tag("span", attrs={"class": "en" + (" on" if lang == "en" else "")}); en.string = "EN"
            new.append(zh); new.append(en)
            tog.replace_with(new)
        else:
            tog.decompose()

    # 5. counters: real numbers in HTML (crawlers / no-JS see the true value)
    for el in soup.find_all(attrs={"data-count": True}):
        raw = el["data-count"]
        val = float(raw)
        el.string = f"{int(val):,}" if "." not in raw else raw

    # 6. EN pages: the English footer copyright line, etc. — report leftover CJK
    out = "<!doctype html>\n" + str(soup).replace("<!DOCTYPE html>", "").replace("<!doctype html>", "").lstrip()
    out = f"<!-- GENERATED by scripts/build.py from src/{rel} — edit the source, not this file -->\n" + out
    if lang == "en":
        text = BeautifulSoup(out, "html.parser").body.get_text(" ")
        cjk = re.findall(r"[一-鿿][一-鿿·，。、：“”（）\s]*", text)
        allowed = {PRODUCT_ZH, "中", "微"}
        leftovers = sorted({c.strip() for c in cjk if c.strip() and c.strip() not in allowed})
        if leftovers:
            print(f"  ! {rel} [en] untranslated CJK: {leftovers[:12]}")
    return out


def sitemap() -> str:
    parts = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for rel, p in PAGES.items():
        if p["priority"] is None:
            continue
        for lang in ("zh", "en"):
            if p[lang] is None:
                continue
            parts.append("  <url>")
            parts.append(f"    <loc>{SITE + page_url(rel, lang)}</loc>")
            parts.append(f"    <lastmod>{TODAY}</lastmod>")
            parts.append(f'    <xhtml:link rel="alternate" hreflang="zh-CN" href="{SITE + page_url(rel, "zh")}" />')
            parts.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE + page_url(rel, "en")}" />')
            parts.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE + page_url(rel, "zh")}" />')
            parts.append(f"    <priority>{p['priority'] if lang == 'zh' else f'{float(p['priority']) - 0.1:.1f}'}</priority>")
            parts.append("  </url>")
    parts.append("</urlset>")
    return "\n".join(parts) + "\n"


def main() -> None:
    srcs = sorted(str(p.relative_to(SRC)) for p in SRC.rglob("*.html"))
    missing = set(srcs) - set(PAGES)
    if missing:
        raise SystemExit(f"Add metadata for: {sorted(missing)}")
    for rel in srcs:
        for lang in ("zh", "en"):
            if PAGES[rel][lang] is None:
                continue
            dst = out_file(rel, lang)
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(build_page(rel, lang), encoding="utf-8")
            print(f"  {dst.relative_to(ROOT)}  →  {page_url(rel, lang)}")
    (ROOT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    print("  sitemap.xml")


if __name__ == "__main__":
    main()
