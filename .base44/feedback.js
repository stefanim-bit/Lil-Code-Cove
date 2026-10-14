/* Preview-only "Give feedback" tool. Injected by nginx into .html pages; scenario files are not modified.
   Click the button, click any element, type what you want changed, copy the note, paste it into the Base44 chat. */
(function () {
  if (window.top !== window.self && window.__b44fb) return;
  if (window.__b44fb) return;
  window.__b44fb = true;

  var host = document.createElement('div');
  host.setAttribute('data-b44-feedback', '');
  host.style.cssText = 'all:initial;position:fixed;z-index:2147483647;top:0;left:0;width:0;height:0;';
  var root = host.attachShadow({ mode: 'open' });
  root.innerHTML =
    '<style>' +
    '*{box-sizing:border-box;font-family:-apple-system,"Segoe UI",Roboto,Arial,sans-serif}' +
    '.btn{position:fixed;right:16px;bottom:16px;background:#1355d6;color:#fff;border:0;border-radius:999px;padding:11px 18px;font-size:14px;font-weight:600;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,.25)}' +
    '.btn.on{background:#d64545}' +
    '.hl{position:fixed;pointer-events:none;border:2px solid #1355d6;background:rgba(19,85,214,.12);border-radius:3px;display:none}' +
    '.hl.sel{border-color:#d64545;background:rgba(214,69,69,.12)}' +
    '.tip{position:fixed;left:50%;top:12px;transform:translateX(-50%);background:#1c1f26;color:#fff;padding:8px 14px;border-radius:8px;font-size:13px;display:none}' +
    '.panel{position:fixed;right:16px;bottom:70px;width:340px;max-width:calc(100vw - 32px);background:#fff;color:#1c1f26;border:1px solid #dfe2e8;border-radius:12px;padding:14px;box-shadow:0 8px 28px rgba(0,0,0,.28);display:none;font-size:13px}' +
    '.panel h4{margin:0 0 6px;font-size:14px}' +
    '.sel-info{background:#eef3ff;border-left:4px solid #1355d6;padding:6px 8px;border-radius:5px;margin-bottom:8px;word-break:break-word;max-height:70px;overflow:auto}' +
    'textarea{width:100%;border:1px solid #c9ceda;border-radius:8px;padding:8px;font-size:13px;resize:vertical}' +
    '.row{display:flex;gap:8px;margin-top:8px}' +
    '.row button{flex:1;border-radius:8px;padding:9px;font-size:13px;font-weight:600;cursor:pointer;border:1px solid #c9ceda;background:#fff}' +
    '.row button.p{background:#1355d6;color:#fff;border-color:#1355d6}' +
    '.out{margin-top:8px;display:none}' +
    '.ok{color:#1b7a3a;font-weight:600;margin-top:6px}' +
    '</style>' +
    '<div class="hl"></div><div class="tip">Click the thing you want to change (Esc to cancel)</div>' +
    '<div class="panel">' +
    '<h4>Your feedback</h4><div class="sel-info"></div>' +
    '<textarea rows="3" placeholder="What should change? e.g. make this text bigger"></textarea>' +
    '<div class="row"><button class="p copy">Copy note</button><button class="cancel">Cancel</button></div>' +
    '<div class="out"><div class="ok">Copied. Paste it into the Base44 chat.</div>' +
    '<div style="margin-top:6px;color:#5b6270">If copy did not work, select this text and copy it:</div>' +
    '<textarea class="full" rows="5" readonly></textarea></div>' +
    '</div>' +
    '<button class="btn">Give feedback</button>';
  document.documentElement.appendChild(host);

  var $ = function (s) { return root.querySelector(s); };
  var btn = $('.btn'), hl = $('.hl'), tip = $('.tip'), panel = $('.panel');
  var info = $('.sel-info'), comment = panel.querySelector('textarea'), out = $('.out'), full = $('.full');
  var active = false, picked = null;

  function inUI(e) { return e.composedPath().indexOf(host) !== -1; }
  function box(el, cls) {
    var r = el.getBoundingClientRect();
    hl.style.display = 'block';
    hl.className = 'hl' + (cls ? ' ' + cls : '');
    hl.style.left = r.left + 'px'; hl.style.top = r.top + 'px';
    hl.style.width = r.width + 'px'; hl.style.height = r.height + 'px';
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
  function screenInfo() {
    var bits = [];
    var pr = document.querySelector('.prompt, .screen-title, h1, h2');
    if (pr) bits.push('"' + text(pr, 140) + '"');
    var prog = document.querySelector('#progress');
    if (prog && text(prog)) bits.push('progress: ' + text(prog, 60));
    return bits.join(' | ') || 'not detected';
  }

  function start() { active = true; btn.textContent = 'Cancel'; btn.classList.add('on'); tip.style.display = 'block'; panel.style.display = 'none'; }
  function stop() { active = false; picked = null; btn.textContent = 'Give feedback'; btn.classList.remove('on'); tip.style.display = 'none'; hl.style.display = 'none'; panel.style.display = 'none'; out.style.display = 'none'; comment.value = ''; }

  btn.addEventListener('click', function () { active || picked ? stop() : start(); });
  root.querySelector('.cancel').addEventListener('click', stop);

  document.addEventListener('mousemove', function (e) {
    if (!active || inUI(e)) return;
    var el = document.elementFromPoint(e.clientX, e.clientY);
    if (el && el !== document.documentElement && el !== document.body) box(el);
  }, true);

  function swallow(e) { if (active && !inUI(e)) { e.preventDefault(); e.stopPropagation(); e.stopImmediatePropagation(); } }
  ['mousedown', 'mouseup', 'pointerdown', 'pointerup', 'touchstart', 'touchend'].forEach(function (t) { document.addEventListener(t, swallow, true); });
  document.addEventListener('click', function (e) {
    if (!active || inUI(e)) return;
    swallow(e);
    var el = document.elementFromPoint(e.clientX, e.clientY);
    if (!el) return;
    picked = el; active = false; tip.style.display = 'none';
    box(el, 'sel');
    var label = el.tagName.toLowerCase() + (text(el) ? ' with text "' + text(el, 80) + '"' : '');
    info.textContent = label;
    panel.style.display = 'block'; out.style.display = 'none'; comment.value = ''; comment.focus();
  }, true);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && (active || picked)) stop(); }, true);

  root.querySelector('.copy').addEventListener('click', function () {
    if (!picked) return;
    var cs = getComputedStyle(picked);
    var file = decodeURIComponent(location.pathname.replace(/^\//, ''));
    var note =
      'DESIGN FEEDBACK\n' +
      'Scenario file: ' + file + '\n' +
      'Screen: ' + screenInfo() + '\n' +
      'Element: ' + info.textContent + '\n' +
      'Location in page: ' + selector(picked) + '\n' +
      'Current look: font-size ' + cs.fontSize + ', text color ' + cs.color + ', background ' + cs.backgroundColor + ', size ' + Math.round(picked.getBoundingClientRect().width) + 'x' + Math.round(picked.getBoundingClientRect().height) + ' (page width ' + window.innerWidth + ')\n' +
      'What I want: ' + (comment.value.trim() || '(not written yet)') + '\n' +
      'Please make this change, then I will preview and confirm or ask for adjustments.';
    full.value = note; out.style.display = 'block';
    var ok = root.querySelector('.ok');
    function manual() { ok.textContent = 'Copy was blocked. Select the text below, copy it, and paste it into the Base44 chat.'; full.focus(); full.select(); }
    ok.textContent = 'Copying...';
    try {
      navigator.clipboard.writeText(note).then(function () { ok.textContent = 'Copied. Paste it into the Base44 chat.'; }, manual);
    } catch (err) { manual(); }
  });
})();
