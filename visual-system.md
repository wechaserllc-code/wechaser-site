# Visual System — Declared Before Build

## Type Scale (rem, base 16px)
- Display 1 (Hero zh): 6rem / 96px / 思源宋体 900 / line 1.05
- Display 2 (Section title): 3rem / 48px / 思源宋体 700 / line 1.15
- H3 (Sub-section): 1.75rem / 28px / 思源宋体 700
- Body L (lead): 1.25rem / 20px / 思源黑体 400 / line 1.7
- Body M: 1rem / 16px / line 1.75
- Caption (mono): 0.75rem / 12px / JetBrains Mono / tracking +.15em uppercase

## Spacing rhythm
- Section padding: 160px top, 160px bottom (desktop), 96px (mobile)
- Sub-section gap: 64px
- Element gap: 24px / 32px

## Layout patterns
1. **Hero**: full viewport, 大字标题居左，小字注脚居右下，朱砂印章右上角
2. **Statement section**: 单列居中，最大文本宽度 720px，气定神闲
3. **Capability triad**: 三段式纵向排版（不是横向卡片），每段标题 + 描述 + 一根细线分隔
4. **Use-case**: 两列对照 — 左侧场景标题，右侧结果数字 + 描述
5. **How it works**: 4 步骤，编号 01-04 用 mono，step 间用细朱砂线连接
6. **Trust block**: 3 行短文 + 印章背书
7. **CTA**: 单行大字 + 输入框（邮箱预约演示）
8. **Footer**: 极简，左 logo + © 信息，右 sitemap

## Color usage rules
- 95% 页面是 paper(#FAF7F2) + ink(#211F1B)
- 朱砂红 (#A8362C) 只用于：印章、关键数字 underline、CTA hover、进度指示
- 严禁渐变填充，背景永远是单色

## Section header pattern
每个 section title 上方有一行 mono 标签：`§ 01 · CAPABILITY`
title 下方紧跟一句小标题（思源黑体 normal）

## Bilingual mechanism
- `<html lang>` 默认 zh-CN
- 全局 toggle 在右上角：「中 / EN」
- 切换通过 body class .lang-en 控制 [data-zh] [data-en] 显隐
- 字体栈在两种语言下自动切换 (Noto Serif SC vs Söhne/Inter Display)

## Page sections (final IA)
1. Nav (logo + 锚点 + 语言切换 + 预约 CTA)
2. Hero (主张 + 副标 + 印章)
3. Why now (一段散文式价值主张)
4. Capabilities (三大能力纵向排布)
5. Use cases (4 个制造业场景)
6. How it works (4 步)
7. Trust & deployment (本地化 / 安全 / 合规)
8. CTA banner (预约演示)
9. Footer
