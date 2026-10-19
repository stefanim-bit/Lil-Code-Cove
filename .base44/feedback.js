/* Preview-only review tools. Injected by nginx into .html pages; scenario files are not modified.
   - Inspect: hover any element to see its specs (font, size, colors, spacing); click to lock, Esc to exit.
   - Give feedback: click an element, then post a shared comment and/or copy a note for the Base44 chat.
   - Comments: shared list, grouped by person; the design team can resolve or delete. */
(function () {
  if (window.__b44fb) return;
  window.__b44fb = true;
  var API = '/_b44_api/comments';
  var FILE = decodeURIComponent(location.pathname.replace(/^\//, ''));

  var host = document.createElement('div');
  host.setAttribute('data-b44-feedback', '');
  host.style.cssText = 'all:initial;position:fixed;z-index:2147483647;top:0;left:0;width:0;height:0;';
  var root = host.attachShadow({ mode: 'open' });
  root.innerHTML =
    '<style>' +
    '*{box-sizing:border-box;font-family:-apple-system,"Segoe UI",Roboto,Arial,sans-serif}' +
    '.bar{position:fixed;right:16px;bottom:16px;display:flex;gap:8px}' +
    '.bar button{background:#1355d6;color:#fff;border:0;border-radius:999px;padding:11px 16px;font-size:14px;font-weight:600;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,.25)}' +
    '.bar button.alt{background:#1c1f26}' +
    '.bar button.on{background:#d64545}' +
    '.hl{position:fixed;pointer-events:none;border:2px solid #1355d6;background:rgba(19,85,214,.12);border-radius:3px;display:none}' +
    '.hl.sel{border-color:#d64545;background:rgba(214,69,69,.12)}' +
    '.hl.flash{border-color:#e6a100;background:rgba(230,161,0,.2)}' +
    '.tag{position:fixed;pointer-events:none;background:#1c1f26;color:#fff;font:11px/1 ui-monospace,Menlo,monospace;padding:4px 6px;border-radius:4px;display:none;white-space:nowrap}' +
    '.tip{position:fixed;left:50%;top:12px;transform:translateX(-50%);background:#1c1f26;color:#fff;padding:8px 14px;border-radius:8px;font-size:13px;display:none}' +
    '.spec{position:fixed;width:250px;background:#1c1f26;color:#e9ecf2;border-radius:8px;padding:10px 12px;font-size:12px;box-shadow:0 8px 24px rgba(0,0,0,.35);display:none;pointer-events:none}' +
    '.spec b{display:block;font:600 12px ui-monospace,Menlo,monospace;color:#fff;margin-bottom:6px;word-break:break-all}' +
    '.spec .r{display:flex;justify-content:space-between;gap:10px;padding:2px 0}' +
    '.spec .r span:first-child{color:#9aa3b5}.spec .r span:last-child{text-align:right;word-break:break-all}' +
    '.sw{display:inline-block;width:11px;height:11px;border:1px solid #fff6;border-radius:2px;vertical-align:-1px;margin-right:5px}' +
    '.spec .foot{margin-top:6px;padding-top:6px;border-top:1px solid #3a4150;color:#9aa3b5;font-size:11px}' +
    '.panel{position:fixed;right:16px;bottom:70px;width:350px;max-width:calc(100vw - 32px);background:#fff;color:#1c1f26;border:1px solid #dfe2e8;border-radius:12px;padding:14px;box-shadow:0 8px 28px rgba(0,0,0,.28);display:none;font-size:13px}' +
    '.panel h4{margin:0 0 6px;font-size:14px}' +
    '.sel-info{background:#eef3ff;border-left:4px solid #1355d6;padding:6px 8px;border-radius:5px;margin-bottom:8px;word-break:break-word;max-height:70px;overflow:auto}' +
    'textarea{width:100%;border:1px solid #c9ceda;border-radius:8px;padding:8px;font-size:13px;resize:vertical}' +
    '.row{display:flex;gap:8px;margin-top:8px}' +
    'button.b{flex:1;border-radius:8px;padding:9px;font-size:13px;font-weight:600;cursor:pointer;border:1px solid #c9ceda;background:#fff;color:#1c1f26}' +
    'button.b.p{background:#1355d6;color:#fff;border-color:#1355d6}' +
    'button.b.sm{flex:none;padding:4px 8px;font-size:12px}' +
    'button.b.danger{color:#c62828;border-color:#e3b0b0}' +
    '.msg{margin-top:6px;font-weight:600;color:#1b7a3a}.msg.err{color:#c62828}' +
    '.out{margin-top:8px;display:none}.out .full{margin-top:6px}' +
    '.list{width:380px;max-height:72vh;overflow:auto}' +
    '.ctl{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0 8px;align-items:center}' +
    '.ctl select{font-size:12px;padding:4px;border:1px solid #c9ceda;border-radius:6px}' +
    '.ctl label{font-size:12px;color:#5b6270}' +
    '.who{margin:10px 0 4px;font-weight:700;border-bottom:1px solid #e5e8ee;padding-bottom:3px}' +
    '.c{border:1px solid #e5e8ee;border-radius:8px;padding:8px;margin-bottom:6px}.c.done{opacity:.6}' +
    '.c .meta{color:#5b6270;font-size:11px;margin-bottom:3px;word-break:break-word}' +
    '.c .txt{white-space:pre-wrap;word-break:break-word}' +
    '.c .acts{display:flex;gap:6px;margin-top:6px}' +
    '.empty{color:#5b6270;padding:8px 0}' +
    '</style>' +
    '<div class="hl"></div><div class="tag"></div><div class="tip"></div><div class="spec"></div>' +
    '<div class="panel pick"><h4>Your feedback</h4><div class="sel-info"></div>' +
    '<textarea rows="3" placeholder="What should change? e.g. make this text bigger"></textarea>' +
    '<div class="row"><button class="b p post">Post comment</button><button class="b copy">Copy note for Base44</button></div>' +
    '<div class="row"><button class="b cancel">Cancel</button></div>' +
    '<div class="msg"></div>' +
    '<div class="out"><div style="color:#5b6270">If copying was blocked, select this text and copy it:</div><textarea class="full" rows="5" readonly></textarea></div></div>' +
    '<div class="panel list cm"><h4>Comments <span class="who-am" style="font-weight:400;color:#5b6270"></span></h4>' +
    '<div class="ctl">' +
    '<select class="grp"><option value="person">Group by person</option><option value="new">Newest first</option></select>' +
    '<select class="stat"><option value="open">Open</option><option value="resolved">Resolved</option><option value="all">All</option></select>' +
    '<select class="scope"><option value="page">This page</option><option value="all">All pages</option></select>' +
    '<label><input type="checkbox" class="dt"> Design team</label>' +
    '<button class="b sm name">Change name</button></div>' +
    '<div class="items"></div></div>' +
    '<div class="bar"><button class="alt insp">Inspect</button><button class="fb">Give feedback</button><button class="alt cmb">Comments</button></div>';
  document.documentElement.appendChild(host);

  var $ = function (s) { return root.querySelector(s); };
  var hl = $('.hl'), tag = $('.tag'), tip = $('.tip'), spec = $('.spec');
  var pick = $('.pick'), cm = $('.cm');
  var info = $('.sel-info'), comment = pick.querySelector('textarea'), out = $('.out'), full = $('.full'), msg = $('.msg');
  var bInsp = $('.insp'), bFb = $('.fb'), bCm = $('.cmb');
  var mode = 'off', picked = null, locked = false, comments = [], timer = null;

  function inUI(e) { return e.composedPath().indexOf(host) !== -1; }
  function box(el, cls) {
    var r = el.getBoundingClientRect();
    hl.style.display = 'block';
    hl.className = 'hl' + (cls ? ' ' + cls : '');
    hl.style.left = r.left + 'px'; hl.style.top = r.top + 'px';
    hl.style.width = r.width + 'px'; hl.style.height = r.height + 'px';
    return r;
  }
  function text(el, n) { return (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, n || 120); }
  function selector(el) {
    var parts = [];
    while (el && el.nodeType === 1 && el !== document.body && parts.length < 5) {
      var p = el.tagName.toLowerCase();
      if (el.id) { parts.unshift(p + '#' + el.id); break; }
      var cls = (el.className && typeof el.className === 'string') ? el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
      if (cls) p += '.' + cls;
      var sib = el.parentElement && Array.prototype.filter.call(el.parentElement.children, function (c) { return c.tagName === el.tagName; });
      if (sib && sib.length > 1) p += ':nth-of-type(' + (sib.indexOf(el) + 1) + ')';
      parts.unshift(p);
      el = el.parentElement;
    }
    return parts.join(' > ');
  }
  function label(el) { return el.tagName.toLowerCase() + (text(el) ? ' with text "' + text(el, 80) + '"' : ''); }
  function screenInfo() {
    var bits = [];
    var pr = document.querySelector('.prompt, .screen-title, h1, h2');
    if (pr) bits.push('"' + text(pr, 140) + '"');
    var prog = document.querySelector('#progress');
    if (prog && text(prog)) bits.push('progress: ' + text(prog, 60));
    return bits.join(' | ') || 'not detected';
  }
  function toHex(c) {
    var m = c.match(/[\d.]+/g); if (!m) return c;
    if (m.length > 3 && +m[3] === 0) return 'transparent';
    return '#' + m.slice(0, 3).map(function (n) { return ('0' + (+n).toString(16)).slice(-2); }).join('');
  }
  function bgOf(el) {
    while (el && el.nodeType === 1) {
      var b = getComputedStyle(el).backgroundColor, m = b.match(/[\d.]+/g);
      if (m && !(m.length > 3 && +m[3] === 0)) return b;
      el = el.parentElement;
    }
    return 'rgb(255,255,255)';
  }
  function lum(c) {
    var m = c.match(/[\d.]+/g).slice(0, 3).map(function (n) { n = n / 255; return n <= 0.03928 ? n / 12.92 : Math.pow((n + 0.055) / 1.055, 2.4); });
    return 0.2126 * m[0] + 0.7152 * m[1] + 0.0722 * m[2];
  }
  function contrast(a, b) { var x = lum(a), y = lum(b); return ((Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05)).toFixed(2); }
  function clear(node) { while (node.firstChild) node.removeChild(node.firstChild); }
  function el(tagName, cls, txt) { var n = document.createElement(tagName); if (cls) n.className = cls; if (txt != null) n.textContent = txt; return n; }

  /* ---------- Inspect ---------- */
  function showSpec(t, r) {
    var cs = getComputedStyle(t);
    var cls = (t.className && typeof t.className === 'string') ? '.' + t.className.trim().split(/\s+/).join('.') : '';
    var c = cs.color, bg = bgOf(t);
    var rows = [
      ['Font', cs.fontFamily.split(',')[0].replace(/["']/g, '')],
      ['Weight', cs.fontWeight],
      ['Size', cs.fontSize],
      ['Line height', cs.lineHeight],
      ['Letter spacing', cs.letterSpacing],
      ['Color', c, toHex(c)],
      ['Background', cs.backgroundColor, toHex(cs.backgroundColor)],
      ['Padding', cs.padding],
      ['Margin', cs.margin],
      ['Radius', cs.borderRadius],
      ['Border', cs.borderTopWidth === '0px' ? 'none' : cs.borderTopWidth + ' ' + toHex(cs.borderTopColor)]
    ];
    clear(spec);
    spec.appendChild(el('b', '', t.tagName.toLowerCase() + (t.id ? '#' + t.id : '') + cls + '  ' + Math.round(r.width) + '×' + Math.round(r.height)));
    rows.forEach(function (row) {
      var d = el('div', 'r'); d.appendChild(el('span', '', row[0]));
      var v = el('span', '');
      if (row[2]) { var sw = el('i', 'sw'); sw.style.background = row[1]; v.appendChild(sw); v.appendChild(document.createTextNode(row[2])); }
      else v.textContent = row[1];
      d.appendChild(v); spec.appendChild(d);
    });
    spec.appendChild(el('div', 'foot', 'Text contrast ' + contrast(c, bg) + ':1 · ' + (locked ? 'Click to unlock · Esc to exit' : 'Click to lock · Esc to exit')));
    spec.style.display = 'block';
    var w = 250, h = spec.offsetHeight;
    var x = r.right + 10; if (x + w > window.innerWidth - 8) x = Math.max(8, r.left - w - 10);
    if (x < 8) x = 8;
    var y = Math.min(Math.max(8, r.top), window.innerHeight - h - 8);
    spec.style.left = x + 'px'; spec.style.top = y + 'px';
  }

  /* ---------- Modes ---------- */
  function setMode(m) {
    mode = m; locked = false; picked = null;
    hl.style.display = 'none'; tag.style.display = 'none'; spec.style.display = 'none'; tip.style.display = 'none'; pick.style.display = 'none';
    out.style.display = 'none'; comment.value = ''; msg.textContent = '';
    bInsp.classList.toggle('on', m === 'inspect'); bInsp.textContent = m === 'inspect' ? 'Exit inspect' : 'Inspect';
    bFb.classList.toggle('on', m === 'pick'); bFb.textContent = m === 'pick' ? 'Cancel' : 'Give feedback';
    if (m === 'inspect') { tip.textContent = 'Hover to see specs · click to lock · Esc to exit'; tip.style.display = 'block'; }
    if (m === 'pick') { tip.textContent = 'Click the thing you want to change (Esc to cancel)'; tip.style.display = 'block'; }
  }
  bInsp.addEventListener('click', function () { setMode(mode === 'inspect' ? 'off' : 'inspect'); });
  bFb.addEventListener('click', function () { setMode(mode === 'off' ? 'pick' : 'off'); });
  pick.querySelector('.cancel').addEventListener('click', function () { setMode('off'); });

  document.addEventListener('mousemove', function (e) {
    if ((mode !== 'inspect' && mode !== 'pick') || locked || inUI(e)) return;
    var t = document.elementFromPoint(e.clientX, e.clientY);
    if (!t || t === document.documentElement || t === document.body) return;
    var r = box(t);
    if (mode === 'inspect') {
      tag.textContent = t.tagName.toLowerCase() + ' ' + Math.round(r.width) + '×' + Math.round(r.height);
      tag.style.display = 'block'; tag.style.left = r.left + 'px'; tag.style.top = Math.max(0, r.top - 22) + 'px';
      showSpec(t, r); picked = t;
    }
  }, true);

  function swallow(e) { if (mode !== 'off' && !inUI(e)) { e.preventDefault(); e.stopPropagation(); e.stopImmediatePropagation(); } }
  ['mousedown', 'mouseup', 'pointerdown', 'pointerup', 'touchstart', 'touchend'].forEach(function (t) { document.addEventListener(t, swallow, true); });
  document.addEventListener('click', function (e) {
    if (mode === 'off' || inUI(e)) return;
    swallow(e);
    var t = document.elementFromPoint(e.clientX, e.clientY);
    if (!t) return;
    if (mode === 'inspect') {
      locked = !locked;
      if (locked) { picked = t; var r = box(t, 'sel'); showSpec(t, r); } else { box(t); }
      return;
    }
    picked = t; mode = 'picked'; tip.style.display = 'none'; bFb.classList.remove('on'); bFb.textContent = 'Give feedback';
    box(t, 'sel');
    info.textContent = label(t);
    pick.style.display = 'block'; cm.style.display = 'none'; out.style.display = 'none'; msg.textContent = ''; comment.value = ''; comment.focus();
  }, true);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && mode !== 'off') setMode('off'); }, true);

  /* ---------- Copy note for Base44 chat ---------- */
  pick.querySelector('.copy').addEventListener('click', function () {
    if (!picked) return;
    var cs = getComputedStyle(picked), r = picked.getBoundingClientRect();
    var note =
      'DESIGN FEEDBACK\n' +
      'Scenario file: ' + FILE + '\n' +
      'Screen: ' + screenInfo() + '\n' +
      'Element: ' + info.textContent + '\n' +
      'Location in page: ' + selector(picked) + '\n' +
      'Current look: font ' + cs.fontFamily.split(',')[0] + ', size ' + cs.fontSize + ', weight ' + cs.fontWeight + ', text color ' + cs.color + ', background ' + cs.backgroundColor + ', size ' + Math.round(r.width) + 'x' + Math.round(r.height) + ' (page width ' + window.innerWidth + ')\n' +
      'What I want: ' + (comment.value.trim() || '(not written yet)') + '\n' +
      'Please make this change, then I will preview and confirm or ask for adjustments.';
    full.value = note; out.style.display = 'block';
    msg.className = 'msg'; msg.textContent = 'Copying...';
    function manual() { msg.className = 'msg err'; msg.textContent = 'Copy was blocked. Select the text below, copy it, and paste it into the Base44 chat.'; full.focus(); full.select(); }
    try { navigator.clipboard.writeText(note).then(function () { msg.textContent = 'Copied. Paste it into the Base44 chat.'; }, manual); } catch (err) { manual(); }
  });

  /* ---------- Shared comments ---------- */
  function who() {
    var n = localStorage.getItem('b44name');
    if (!n) { n = (window.prompt('Your name (so the design team knows who commented):') || '').trim(); if (n) localStorage.setItem('b44name', n); }
    return n;
  }
  function api(method, path, body) {
    return fetch(API + (path || ''), { method: method, headers: { 'Content-Type': 'application/json' }, body: body ? JSON.stringify(body) : undefined })
      .then(function (r) { if (!r.ok) throw new Error('http ' + r.status); return r.json(); });
  }
  pick.querySelector('.post').addEventListener('click', function () {
    var t = comment.value.trim();
    msg.className = 'msg err';
    if (!picked) return;
    if (!t) { msg.textContent = 'Write a comment first.'; return; }
    var name = who(); if (!name) { msg.textContent = 'A name is needed to post.'; return; }
    api('POST', '', { author: name, file: FILE, element: label(picked), selector: selector(picked), text: t })
      .then(function () { setMode('off'); refresh(); cm.style.display = 'block'; })
      .catch(function () { msg.textContent = 'Could not post. Try again, or use "Copy note for Base44".'; });
  });

  function ago(s) { var d = (Date.now() - new Date(s)) / 1000; return d < 60 ? 'just now' : d < 3600 ? Math.floor(d / 60) + ' min ago' : d < 86400 ? Math.floor(d / 3600) + ' h ago' : new Date(s).toLocaleDateString(); }
  function flash(c) {
    try { var t = document.querySelector(c.selector); if (t) { t.scrollIntoView({ block: 'center' }); box(t, 'flash'); setTimeout(function () { if (mode === 'off') hl.style.display = 'none'; }, 2500); return; } } catch (e) {}
    alert('That element is not on screen right now (it may be on a different screen of the scenario).');
  }
  var dt = $('.dt'), grp = $('.grp'), stat = $('.stat'), scope = $('.scope'), items = $('.items');
  dt.checked = localStorage.getItem('b44dt') === '1';
  dt.addEventListener('change', function () { localStorage.setItem('b44dt', dt.checked ? '1' : '0'); render(); });
  [grp, stat, scope].forEach(function (s) { s.addEventListener('change', render); });
  $('.name').addEventListener('click', function () { localStorage.removeItem('b44name'); who(); render(); });

  function card(c) {
    var d = el('div', 'c' + (c.resolved ? ' done' : ''));
    d.appendChild(el('div', 'meta', (grp.value === 'person' ? '' : c.author + ' · ') + ago(c.createdAt) + (scope.value === 'all' ? ' · ' + c.file.split('/').pop() : '') + ' · ' + c.element));
    d.appendChild(el('div', 'txt', c.text));
    var a = el('div', 'acts');
    var show = el('button', 'b sm', 'Show'); show.onclick = function () { flash(c); }; a.appendChild(show);
    if (dt.checked) {
      var rs = el('button', 'b sm', c.resolved ? 'Reopen' : 'Resolve');
      rs.onclick = function () { api('PATCH', '/' + c.id, { resolved: !c.resolved }).then(refresh); };
      var del = el('button', 'b sm danger', 'Delete');
      del.onclick = function () { if (confirm('Delete this comment for everyone?')) api('DELETE', '/' + c.id).then(refresh); };
      a.appendChild(rs); a.appendChild(del);
    }
    d.appendChild(a); return d;
  }
  function render() {
    $('.who-am').textContent = localStorage.getItem('b44name') ? '(as ' + localStorage.getItem('b44name') + ')' : '';
    var open = comments.filter(function (c) { return !c.resolved; }).length;
    bCm.textContent = 'Comments (' + open + ')';
    var list = comments.filter(function (c) {
      return (scope.value === 'all' || c.file === FILE) && (stat.value === 'all' || (stat.value === 'open') === !c.resolved);
    });
    clear(items);
    if (!list.length) { items.appendChild(el('div', 'empty', 'No comments here yet.')); return; }
    if (grp.value === 'person') {
      var by = {};
      list.forEach(function (c) { (by[c.author] = by[c.author] || []).push(c); });
      Object.keys(by).sort(function (a, b) { return a.toLowerCase() < b.toLowerCase() ? -1 : 1; }).forEach(function (n) {
        items.appendChild(el('div', 'who', n + ' (' + by[n].length + ')'));
        by[n].forEach(function (c) { items.appendChild(card(c)); });
      });
    } else {
      list.slice().sort(function (a, b) { return a.createdAt < b.createdAt ? 1 : -1; }).forEach(function (c) { items.appendChild(card(c)); });
    }
  }
  function refresh() { return api('GET').then(function (d) { comments = d; render(); }).catch(function () {}); }
  bCm.addEventListener('click', function () {
    var show = cm.style.display !== 'block';
    setMode('off'); cm.style.display = show ? 'block' : 'none';
    if (show) refresh();
  });
  refresh();
  setInterval(function () { if (cm.style.display === 'block') refresh(); }, 15000);
})();
