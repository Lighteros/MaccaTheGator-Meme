(function () {
  'use strict';
  document.documentElement.classList.add('js');
  var CA = '0x8822e660ED5b894E1158533213b1173716cDB522';
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = matchMedia('(pointer: fine)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- loader ---------- */
  var loader = $('#loader');
  if (loader) {
    var tips = ['TIP: Always verify the contract address before you swap.', 'TIP: Buy only on Uniswap · Ethereum mainnet.', 'TIP: Flamingo blood martinis restore full health.', 'TIP: Skip the heist. Hold the bags.'];
    $('#ldtip').textContent = tips[Math.floor(Math.random() * tips.length)];
    var p = 0, bar = $('#ldbar');
    var iv = setInterval(function () { p = Math.min(100, p + 8 + Math.random() * 18); bar.style.width = p + '%'; if (p >= 100) { clearInterval(iv); setTimeout(done, 200); } }, 90);
    var done = function () { if (loader.classList.contains('done')) return; loader.classList.add('done'); document.dispatchEvent(new Event('macca:ready')); };
    setTimeout(done, 2500);
  } else { setTimeout(function () { document.dispatchEvent(new Event('macca:ready')); }, 0); }

  /* ---------- burger ---------- */
  var burger = $('#burger'), nav = $('#nav');
  if (burger) {
    burger.addEventListener('click', function () { var o = nav.classList.toggle('open'); burger.setAttribute('aria-expanded', o); });
    $$('#nav a').forEach(function (a) { a.addEventListener('click', function () { nav.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); }); });
  }

  /* ---------- toast ---------- */
  var toast = $('#toast'), tt;
  function showToast(title, sub) {
    if (!toast) return;
    toast.querySelector('b').textContent = title; toast.querySelector('span').textContent = sub;
    toast.classList.add('show'); clearTimeout(tt); tt = setTimeout(function () { toast.classList.remove('show'); }, 1800);
  }

  /* ---------- copy CA ---------- */
  function copyText(t) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(t);
    return new Promise(function (res, rej) {
      var ta = document.createElement('textarea'); ta.value = t; ta.style.position = 'fixed'; ta.style.opacity = '0'; document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy') ? res() : rej(); } catch (e) { rej(e); } document.body.removeChild(ta);
    });
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-copy]'); if (!b) return;
    var el = $(b.dataset.copy); var text = el ? el.textContent.trim() : CA;
    copyText(text).then(function () {
      var prev = b.textContent; b.textContent = 'Copied ✓'; setTimeout(function () { b.textContent = prev; }, 1400);
      showToast('MISSION PASSED!', 'CA copied · +RESPECT'); burst(e.clientX, e.clientY);
    }).catch(function () { showToast('COPY FAILED', 'Select the CA manually'); });
  });

  /* ---------- reveal ---------- */
  var io = new IntersectionObserver(function (en) {
    en.forEach(function (x) {
      if (!x.isIntersecting) return;
      x.target.classList.add('in');
      if (x.target.classList.contains('step')) setTimeout(function () { x.target.classList.add('done'); }, 700);
      $$('.b i', x.target).forEach(function (i) { i.style.width = i.dataset.w + '%'; });
      io.unobserve(x.target);
    });
  }, { threshold: 0.12 });
  $$('[data-reveal]').forEach(function (el) { io.observe(el); });
  if (reduce) $$('.b i').forEach(function (i) { i.style.width = i.dataset.w + '%'; });

  /* ---------- typer ---------- */
  var typer = $('#typer');
  if (typer && !reduce) {
    var lines = typer.dataset.lines.split('|'), li = 0, ci = lines[0].length, del = false;
    setTimeout(function tick() {
      var L = lines[li];
      if (!del) { ci++; if (ci > L.length) { del = true; return setTimeout(tick, 2200); } }
      else { ci--; if (ci === 0) { del = false; li = (li + 1) % lines.length; } }
      typer.textContent = lines[li].slice(0, ci) + (ci < lines[li].length ? '▌' : '');
      setTimeout(tick, del ? 28 : 55);
    }, 3200);
  }

  /* ---------- scroll HUD: wanted, minimap, nav ---------- */
  var hud = $('#hud'), stars = $$('#wanted i'), prog = $('#progc');
  var secs = $$('main section[id]'), navLinks = $$('#nav a');
  function onScroll() {
    var y = scrollY, h = document.documentElement.scrollHeight - innerHeight, r = h > 0 ? y / h : 0;
    if (hud) hud.classList.toggle('scrolled', y > 40);
    var lvl = Math.round(r * stars.length); stars.forEach(function (s, i) { s.classList.toggle('lit', i < lvl); });
    if (prog) prog.style.strokeDashoffset = 301.6 * (1 - r);
    var cur = ''; secs.forEach(function (s) { if (s.getBoundingClientRect().top < innerHeight * 0.4) cur = s.id; });
    navLinks.forEach(function (a) { var hsh = a.getAttribute('href').split('#')[1]; if (hsh) a.classList.toggle('on', hsh === cur); });
  }
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* ---------- parallax (mouse) + tilt ---------- */
  var layers = $$('[data-depth]'), mx = 0, my = 0;
  if (fine && !reduce) {
    addEventListener('mousemove', function (e) { mx = e.clientX / innerWidth - 0.5; my = e.clientY / innerHeight - 0.5; }, { passive: true });
    (function loop() {
      var sy = Math.min(scrollY, innerHeight);
      layers.forEach(function (l) { var d = parseFloat(l.dataset.depth); var base = l.classList.contains('sun') ? 'translateX(-50%) ' : (l.classList.contains('r') ? '' : ''); l.style.transform = base + 'translate3d(' + (-mx * 60 * d) + 'px,' + (-my * 30 * d + sy * d * 0.5) + 'px,0)' + (l.classList.contains('r') ? ' scaleX(-1)' : ''); });
      requestAnimationFrame(loop);
    })();
    function tiltify(el, amt) {
      el.addEventListener('mousemove', function (e) { var r = el.getBoundingClientRect(); var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5; el.style.transform = 'perspective(900px) rotateY(' + x * amt + 'deg) rotateX(' + -y * amt + 'deg)'; });
      el.addEventListener('mouseleave', function () { el.style.transform = ''; });
    }
    var t = $('#tilt'); if (t) tiltify(t, 18);
    $$('[data-tilt]').forEach(function (el) { tiltify(el, 10); });
    /* magnetic buttons */
    $$('.btn').forEach(function (b) {
      b.addEventListener('mousemove', function (e) { var r = b.getBoundingClientRect(); b.style.transform = 'translate(' + (e.clientX - r.left - r.width / 2) * 0.18 + 'px,' + (e.clientY - r.top - r.height / 2) * 0.25 + 'px)'; });
      b.addEventListener('mouseleave', function () { b.style.transform = ''; });
    });
  }

  /* ---------- neon cursor trail + bursts ---------- */
  var cv = $('#trail'), cx = cv && cv.getContext('2d'), pts = [], parts = [];
  function size() { if (!cv) return; var d = Math.min(devicePixelRatio || 1, 2); cv.width = innerWidth * d; cv.height = innerHeight * d; cx.setTransform(d, 0, 0, d, 0, 0); }
  function burst(x, y) { if (!cx || reduce) return; for (var i = 0; i < 40; i++) { var a = Math.random() * Math.PI * 2, s = 2 + Math.random() * 6; parts.push({ x: x, y: y, vx: Math.cos(a) * s, vy: Math.sin(a) * s, l: 1, c: ['#ff2fa8', '#21f3ff', '#ffb347', '#b6ff3b'][i % 4] }); } }
  if (cx && !reduce) {
    size(); addEventListener('resize', size);
    if (fine) addEventListener('mousemove', function (e) { pts.push({ x: e.clientX, y: e.clientY, l: 1 }); if (pts.length > 26) pts.shift(); }, { passive: true });
    (function draw() {
      cx.clearRect(0, 0, innerWidth, innerHeight);
      for (var i = 1; i < pts.length; i++) {
        var a = pts[i - 1], b = pts[i]; b.l -= 0.035;
        cx.strokeStyle = 'rgba(255,47,168,' + Math.max(0, b.l) + ')'; cx.lineWidth = 6 * b.l; cx.shadowBlur = 16; cx.shadowColor = '#ff2fa8'; cx.lineCap = 'round';
        cx.beginPath(); cx.moveTo(a.x, a.y); cx.lineTo(b.x, b.y); cx.stroke();
      }
      pts = pts.filter(function (p) { return p.l > 0; });
      parts.forEach(function (p) { p.x += p.vx; p.y += p.vy; p.vy += 0.15; p.l -= 0.02; cx.fillStyle = p.c; cx.shadowColor = p.c; cx.shadowBlur = 12; cx.globalAlpha = Math.max(0, p.l); cx.fillRect(p.x, p.y, 4, 4); cx.globalAlpha = 1; });
      parts = parts.filter(function (p) { return p.l > 0; });
      requestAnimationFrame(draw);
    })();
  }

  /* ---------- Lenis + GSAP ---------- */
  document.addEventListener('macca:ready', function () {
    if (reduce) return;
    var lenis;
    if (window.Lenis) {
      lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
      $$('a[href^="#"],a[href^="/#"]').forEach(function (a) {
        a.addEventListener('click', function (e) { var id = a.getAttribute('href').split('#')[1]; var t = id && document.getElementById(id); if (t && location.pathname === '/') { e.preventDefault(); lenis.scrollTo(t, { offset: -70 }); } });
      });
    }
    if (window.gsap) {
      var g = window.gsap;
      if (window.ScrollTrigger) {
        g.registerPlugin(ScrollTrigger);
        if (lenis) { lenis.on('scroll', ScrollTrigger.update); g.ticker.add(function (t) { lenis.raf(t * 1000); }); g.ticker.lagSmoothing(0); }
        $$('.sec-h .num').forEach(function (n) { g.fromTo(n, { xPercent: -40, opacity: 0 }, { xPercent: 0, opacity: 1, ease: 'none', scrollTrigger: { trigger: n, start: 'top 95%', end: 'top 55%', scrub: true } }); });
        $$('.marq').forEach(function (m, i) { g.to(m, { x: i ? 120 : -120, ease: 'none', scrollTrigger: { trigger: m, start: 'top bottom', end: 'bottom top', scrub: true } }); });
        var fh = $('.final h2'); if (fh) g.fromTo(fh, { scale: 0.7 }, { scale: 1.05, ease: 'none', scrollTrigger: { trigger: '.final', start: 'top bottom', end: 'center center', scrub: true } });
        g.to('.hero-in', { yPercent: 18, opacity: 0.2, ease: 'none', scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true } });
      } else if (lenis) { (function raf(t) { lenis.raf(t); requestAnimationFrame(raf); })(); }
      var tl = g.timeline({ defaults: { ease: 'power3.out' } });
      if ($('.title')) tl.from('.kick', { y: 20, opacity: 0, duration: .5 })
        .from('.title', { scale: 1.6, opacity: 0, rotate: -18, duration: .9, ease: 'back.out(1.6)' }, '-=.2')
        .from('.tagline,.lead', { x: -40, opacity: 0, stagger: .1, duration: .6 }, '-=.4')
        .from('.hero .cta .btn', { y: 30, opacity: 0, stagger: .08, duration: .5 }, '-=.3')
        .fromTo('.hero .ca', { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: .4, onComplete: function () { var c = $('.hero .ca'); c.classList.add('in'); } }, '-=.2')
        .from('.hero-card', { x: 120, rotate: 8, opacity: 0, duration: 1, ease: 'expo.out' }, '-=1');
      if ($('.page-top h1')) g.from('.page-top h1', { scale: 1.5, opacity: 0, rotate: -10, duration: .9, ease: 'back.out(1.6)' });
    } else if (lenis) { (function raf(t) { lenis.raf(t); requestAnimationFrame(raf); })(); }
  });

  /* ---------- live DexScreener stats ---------- */
  function fmt(n) { if (n == null || isNaN(n)) return '—'; var a = Math.abs(n); if (a >= 1e9) return '$' + (n / 1e9).toFixed(2) + 'B'; if (a >= 1e6) return '$' + (n / 1e6).toFixed(2) + 'M'; if (a >= 1e3) return '$' + (n / 1e3).toFixed(1) + 'K'; return '$' + n.toFixed(0); }
  function fmtP(n) { n = Number(n); if (!n) return '—'; if (n >= 1) return '$' + n.toFixed(4); var s = n.toPrecision(3); return '$' + (n < 1e-6 ? n.toExponential(2) : Number(s).toString()); }
  function countTo(el, v) { var s = 0, t0 = performance.now(); (function f(t) { var k = Math.min(1, (t - t0) / 1400); el.textContent = fmt(v * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(f); })(t0); }
  fetch('https://api.dexscreener.com/latest/dex/tokens/' + CA).then(function (r) { return r.json(); }).then(function (d) {
    var ps = (d && d.pairs || []).filter(function (p) { return (p.chainId || '').toLowerCase() === 'ethereum'; });
    ps.sort(function (a, b) { return ((b.liquidity || {}).usd || 0) - ((a.liquidity || {}).usd || 0); });
    var p = ps[0]; if (!p) return;
    var mc = Number(p.marketCap || p.fdv || 0), cash = $('#cash'); if (cash && mc) countTo(cash, mc);
    var L = $('#live'); if (!L) return;
    L.querySelector('[data-stat="price"]').textContent = fmtP(p.priceUsd);
    L.querySelector('[data-stat="mcap"]').textContent = fmt(mc);
    var c = p.priceChange && p.priceChange.h24, ce = L.querySelector('[data-stat="chg"]');
    if (c != null) { ce.textContent = (c > 0 ? '+' : '') + Number(c).toFixed(1) + '%'; ce.className = c >= 0 ? 'up' : 'dn'; }
    L.querySelector('[data-stat="liq"]').textContent = fmt(p.liquidity && p.liquidity.usd);
  }).catch(function () {});

  /* ---------- lightbox ---------- */
  var lb = $('#lb');
  if (lb) {
    var img = $('#lbimg'), cap = $('#lbcap'), items = $$('.vm-btn[data-full]'), cur = 0, last;
    var open = function (i) { cur = (i + items.length) % items.length; var b = items[cur]; img.src = b.dataset.full; img.alt = b.dataset.cap; cap.textContent = b.querySelector('.n').textContent + ' · ' + b.dataset.cap; lb.hidden = false; };
    var close = function () { lb.hidden = true; if (last) last.focus(); };
    items.forEach(function (b, i) { b.addEventListener('click', function () { last = b; open(i); $('.lb-x', lb).focus(); }); });
    $('.lb-x', lb).addEventListener('click', close);
    $('.lb-p', lb).addEventListener('click', function () { open(cur - 1); });
    $('.lb-n', lb).addEventListener('click', function () { open(cur + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    addEventListener('keydown', function (e) { if (lb.hidden) return; if (e.key === 'Escape') close(); if (e.key === 'ArrowLeft') open(cur - 1); if (e.key === 'ArrowRight') open(cur + 1); });
  }

  /* ---------- radio (WebAudio synthwave loop) ---------- */
  var radio = $('#radio'), rb = $('#radioBtn'), st = $('#station'), ac, timer, gain;
  var stations = ['FLAMINGO FM', 'GATOR 103.3', 'PINK WAVE RADIO'];
  var si = 0;
  function play() {
    ac = ac || new (window.AudioContext || window.webkitAudioContext)();
    gain = ac.createGain(); gain.gain.value = 0.06; gain.connect(ac.destination);
    var roots = [[57, 60, 64, 67], [53, 57, 60, 64], [55, 59, 62, 67], [52, 55, 59, 64]], step = 0;
    var bpm = 0.16;
    timer = setInterval(function () {
      var ch = roots[Math.floor(step / 8) % 4], n = ch[step % 4] + (step % 8 > 3 ? 12 : 0) + si * 2;
      var o = ac.createOscillator(), g = ac.createGain(); o.type = 'sawtooth'; o.frequency.value = 440 * Math.pow(2, (n - 69) / 12);
      g.gain.setValueAtTime(0.0001, ac.currentTime); g.gain.exponentialRampToValueAtTime(1, ac.currentTime + 0.01); g.gain.exponentialRampToValueAtTime(0.0001, ac.currentTime + bpm * 1.4);
      o.connect(g); g.connect(gain); o.start(); o.stop(ac.currentTime + bpm * 1.5);
      if (step % 4 === 0) { var b = ac.createOscillator(), bg = ac.createGain(); b.type = 'triangle'; b.frequency.value = 440 * Math.pow(2, (ch[0] - 24 - 69 + si * 2) / 12); bg.gain.setValueAtTime(1.6, ac.currentTime); bg.gain.exponentialRampToValueAtTime(0.0001, ac.currentTime + bpm * 3.8); b.connect(bg); bg.connect(gain); b.start(); b.stop(ac.currentTime + bpm * 4); }
      step++;
    }, bpm * 1000);
  }
  function stop() { clearInterval(timer); if (gain) gain.disconnect(); }
  if (rb) rb.addEventListener('click', function () {
    var on = radio.classList.toggle('on'); rb.setAttribute('aria-pressed', on);
    if (on) { si = (si + 1) % stations.length; st.textContent = stations[si]; rb.textContent = 'OFF'; try { play(); } catch (e) {} }
    else { rb.textContent = 'TUNE'; stop(); }
  });

  /* ---------- cheat code: MACCA ---------- */
  var buf = '';
  addEventListener('keydown', function (e) {
    if (e.target.matches && e.target.matches('input,textarea')) return;
    buf = (buf + (e.key || '').toUpperCase()).slice(-5);
    if (buf === 'MACCA') { buf = ''; showToast('CHEAT ACTIVATED', 'PINK GATOR RAIN'); rain(); }
  });
  function rain() {
    for (var i = 0; i < 24; i++) (function (i) {
      setTimeout(function () {
        var im = document.createElement('img'); im.src = '/img/logo-200.webp'; im.alt = ''; im.className = 'gator-rain';
        im.style.left = Math.random() * 96 + 'vw'; document.body.appendChild(im);
        var dur = 2200 + Math.random() * 1800;
        im.animate([{ transform: 'translateY(0) rotate(0)' }, { transform: 'translateY(' + (innerHeight + 160) + 'px) rotate(' + (Math.random() * 720 - 360) + 'deg)' }], { duration: dur, easing: 'cubic-bezier(.4,0,.8,1)' }).onfinish = function () { im.remove(); };
      }, i * 90);
    })(i);
  }
  var title = $('#title'); if (title) title.addEventListener('click', function () { burst(innerWidth / 3, innerHeight / 2); rain(); });
  /* ---------- X drop: photo reel lazy-load ---------- */
  var reel = $('#reel');
  if (reel) {
    var loadReel = function () {
      $$('img[data-src]', reel).forEach(function (im) { im.onload = function () { im.classList.add('ld'); }; im.src = im.dataset.src; im.removeAttribute('data-src'); });
    };
    if ('IntersectionObserver' in window) {
      var rio = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { loadReel(); rio.disconnect(); } }, { rootMargin: '600px 0px' });
      rio.observe(reel);
    } else loadReel();
  }

  /* ---------- X drop: vibe videos play on view ---------- */
  var vids = $$('video[data-vibe]');
  if (vids.length && !reduce && 'IntersectionObserver' in window) {
    var vio = new IntersectionObserver(function (en) {
      en.forEach(function (x) {
        var v = x.target;
        if (x.isIntersecting) { if (v.preload !== 'auto') v.preload = 'auto'; var pr = v.play(); if (pr && pr.catch) pr.catch(function () {}); }
        else v.pause();
      });
    }, { threshold: 0.35 });
    vids.forEach(function (v) { v.muted = true; vio.observe(v); });
  }
})();
