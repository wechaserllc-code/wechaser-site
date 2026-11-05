// Cloudflare Pages Function: POST /api/contact
// Forwards the booking form to a Feishu (Lark) custom-bot webhook.
// Configure in Cloudflare Pages → Settings → Environment variables:
//   FEISHU_WEBHOOK_URL  (required)  https://open.feishu.cn/open-apis/bot/v2/hook/xxxx
// If it is not set, the endpoint returns 503 and the browser falls back to mailto.

const json = (obj, status = 200) =>
  new Response(JSON.stringify(obj), { status, headers: { 'Content-Type': 'application/json' } });

const clip = (v, n) => String(v ?? '').trim().slice(0, n);

export async function onRequestPost({ request, env }) {
  let data;
  try {
    const ct = request.headers.get('Content-Type') || '';
    data = ct.includes('application/json')
      ? await request.json()
      : Object.fromEntries((await request.formData()).entries());
  } catch {
    return json({ ok: false, error: 'bad_request' }, 400);
  }

  // honeypot: bots fill the hidden "website" field
  if (clip(data.website, 200)) return json({ ok: true });

  const email = clip(data.email, 200);
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json({ ok: false, error: 'invalid_email' }, 400);

  if (!env.FEISHU_WEBHOOK_URL) return json({ ok: false, error: 'not_configured' }, 503);

  const text = [
    '📩 wechaser.ai 新的预约请求',
    `邮箱: ${email}`,
    `公司/职位: ${clip(data.company, 200) || '-'}`,
    `需求: ${clip(data.need, 2000) || '-'}`,
    `语言: ${clip(data.lang, 5)} · 页面: ${clip(data.page, 200)}`,
    `时间: ${new Date().toISOString()}`,
  ].join('\n');

  const r = await fetch(env.FEISHU_WEBHOOK_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ msg_type: 'text', content: { text } }),
  });
  // Feishu replies HTTP 200 with a non-zero `code` on errors (bad token, keyword filter…)
  const res = await r.json().catch(() => ({}));
  if (!r.ok || (res.code ?? res.StatusCode ?? 0) !== 0) return json({ ok: false, error: 'upstream' }, 502);
  return json({ ok: true });
}

export const onRequest = () => json({ ok: false, error: 'method_not_allowed' }, 405);
