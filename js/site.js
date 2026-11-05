/* ============================================================
   WeChaser v3 — Shared site behavior
   Lang toggle / nav scroll / reveal / count-up / hero rotator
   ============================================================ */
(function(){
  const body = document.body;

  // language: each language has its own URL (/ and /en/); the toggle is a plain link.
  const isEn = document.documentElement.lang === 'en';

  // contact form → /api/contact (Cloudflare Pages Function), mailto fallback
  const form = document.getElementById('ctaForm');
  if(form){
    const status = document.getElementById('ctaStatus');
    const btn = form.querySelector('button[type=submit]');
    const T = isEn
      ? {sending:'Sending…', ok:'Thanks — we\'ll reply within one business day.', fail:'Couldn\'t send. Opening your email client instead…'}
      : {sending:'提交中…', ok:'已收到，我们会在 1 个工作日内回复。', fail:'提交失败，正在为你打开邮件客户端…'};
    form.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const data = Object.fromEntries(new FormData(form).entries());
      data.lang = isEn ? 'en' : 'zh'; data.page = location.pathname;
      btn.disabled = true; status.className = 'form-status'; status.textContent = T.sending;
      try{
        const r = await fetch('/api/contact', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data)});
        if(!r.ok) throw new Error(r.status);
        status.textContent = T.ok; form.reset();
      }catch(err){
        status.className = 'form-status err'; status.textContent = T.fail;
        const subject = encodeURIComponent('[WeChaser] 30-min call request — ' + (data.email||''));
        const body = encodeURIComponent('Email: '+(data.email||'')+'\nCompany / role: '+(data.company||'')+'\nWhat I want to solve: '+(data.need||'')+'\n');
        setTimeout(()=>{ location.href = 'mailto:hello@wechaser.ai?subject='+subject+'&body='+body; }, 600);
      }finally{ btn.disabled = false; }
    });
  }

  // nav scrolled state
  const nav = document.getElementById('nav');
  if(nav){
    const onScroll = ()=> nav.classList.toggle('scrolled', window.scrollY > 8);
    window.addEventListener('scroll', onScroll, {passive:true});
    onScroll();
  }

  // reveal on scroll with safety fallback
  const reveals = document.querySelectorAll('.reveal');
  if(reveals.length){
    const io = new IntersectionObserver((entries)=>{
      entries.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
    }, {threshold:0.05, rootMargin:'0px 0px 200px 0px'});
    reveals.forEach(el=>io.observe(el));
    setTimeout(()=>{ reveals.forEach(el=>el.classList.add('in')); }, 1600);
  }

  // count-up tickers — real values are in the HTML (for crawlers / no-JS); we only animate visually
  const ticks = document.querySelectorAll('[data-count]');
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function fmt(n, decimals){ if(decimals===0) return Math.round(n).toLocaleString(); return n.toFixed(decimals); }
  function animateCount(el){
    const raw = el.getAttribute('data-count');
    const target = parseFloat(raw);
    const decimals = (raw.split('.')[1]||'').length;
    const dur = 1400, start = performance.now();
    function tick(t){
      const p = Math.min(1, (t-start)/dur);
      el.textContent = fmt(target * (1 - Math.pow(1-p, 3)), decimals);
      if(p<1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }
  if(ticks.length && !reduce && 'IntersectionObserver' in window){
    const tio = new IntersectionObserver((entries)=>{
      entries.forEach(e=>{ if(e.isIntersecting){ animateCount(e.target); tio.unobserve(e.target); } });
    }, {threshold:0.3});
    ticks.forEach(el=>tio.observe(el));
  }

  // hero rotator (only if present)
  const rotators = document.querySelectorAll('.hero-rotator');
  if(rotators.length){
    rotators.forEach(rot => {
      const wordsAttr = rot.getAttribute('data-words');
      if(!wordsAttr) return;
      const words = wordsAttr.split('|');
      const span = rot.querySelector('em');
      let i = 0;
      if(!window.matchMedia('(prefers-reduced-motion: reduce)').matches){
        setInterval(()=>{
          rot.classList.add('flipping');
          setTimeout(()=>{
            i = (i+1) % words.length;
            span.textContent = words[i];
            rot.classList.remove('flipping');
          }, 280);
        }, 2200);
      }
    });
  }
})();
