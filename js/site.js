/* ============================================================
   WeChaser v3 — Shared site behavior
   Lang toggle / nav scroll / reveal / count-up / hero rotator
   ============================================================ */
(function(){
  const body = document.body;

  // language toggle
  const toggle = document.getElementById('langToggle');
  if(toggle){
    const zhSpan = toggle.querySelector('.zh');
    const enSpan = toggle.querySelector('.en');
    function setLang(lang){
      if(lang==='en'){ body.classList.add('lang-en'); document.documentElement.setAttribute('lang','en'); zhSpan.classList.remove('on'); enSpan.classList.add('on'); }
      else { body.classList.remove('lang-en'); document.documentElement.setAttribute('lang','zh-CN'); enSpan.classList.remove('on'); zhSpan.classList.add('on'); }
      try { localStorage.setItem('wc_lang', lang); } catch(e){}
    }
    toggle.addEventListener('click', ()=>{ setLang(body.classList.contains('lang-en') ? 'zh' : 'en'); });
    try { const saved = localStorage.getItem('wc_lang'); if(saved) setLang(saved); } catch(e){}
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

  // count-up tickers
  const ticks = document.querySelectorAll('[data-count]');
  function fmt(n, decimals){ if(decimals===0) return Math.round(n).toLocaleString(); return n.toFixed(decimals); }
  function animateCount(el){
    const raw = el.getAttribute('data-count');
    const target = parseFloat(raw);
    const decimals = (raw.split('.')[1]||'').length;
    const dur = 1400;
    const start = performance.now();
    function tick(t){
      const p = Math.min(1, (t-start)/dur);
      const eased = 1 - Math.pow(1-p, 3);
      el.textContent = fmt(target * eased, decimals);
      if(p<1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }
  if(ticks.length){
    const tio = new IntersectionObserver((entries)=>{
      entries.forEach(e=>{ if(e.isIntersecting){ animateCount(e.target); tio.unobserve(e.target); } });
    }, {threshold:0.3});
    ticks.forEach(el=>tio.observe(el));
    setTimeout(()=>{
      ticks.forEach(el=>{
        const v = el.textContent.trim();
        if(v === '0' || v === '0.0' || v === '0.00') animateCount(el);
      });
    }, 1800);
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
