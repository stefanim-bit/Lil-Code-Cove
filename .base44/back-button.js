/* Preview-only "Back to Home" button. Injected by nginx into .html pages; scenario files are not modified.
   Clicking returns the viewer to the repo home (root directory listing). */
(function () {
  // Home page: find every scenario .html under the Practice Session folders and list them by topic,
  // so reviewers open a scenario in one click instead of browsing folders.
  function buildScenarioList() {
    var pre = document.querySelector('pre');
    if (!pre) return;
    var box = document.createElement('div');
    box.id = 'b44-scenarios';
    box.innerHTML = '<h2>Scenarios</h2><p class="b44-note">Loading scenarios\u2026</p>';
    var guide = document.querySelector('.start');
    (guide || pre).parentNode.insertBefore(box, guide || pre);
    // Keep the raw folder list available, but tucked away.
    var d = document.createElement('details');
    d.innerHTML = '<summary>Browse all folders</summary>';
    pre.parentNode.insertBefore(d, pre);
    d.appendChild(pre);

    function list(path) {
      return fetch('/_b44_tree/' + path.map(encodeURIComponent).join('/') + '/')
        .then(function (r) { return r.ok ? r.json() : []; })
        .catch(function () { return []; });
    }
    var skip = /previous versions|build & (check|review)/i;
    var found = []; // {session, topic, name, path}
    function walk(path, session, topic) {
      return list(path).then(function (items) {
        return Promise.all(items.map(function (it) {
          if (skip.test(it.name)) return null;
          var p = path.concat(it.name);
          if (it.type === 'directory') return walk(p, session, topic || it.name);
          if (/\.html$/i.test(it.name)) found.push({ session: session, topic: topic || '', name: it.name, path: p, old: /previous versions/i.test(p.join('/')) });
          return null;
        }));
      });
    }
    // Fetch the admin's document selection. When configured, only listed documents display;
    // until the admin saves a selection, the home page shows everything (out-of-the-box behaviour).
    var selectionP = fetch('/_b44_api/documents').then(function (r) { return r.ok ? r.json() : {}; }).catch(function () { return {}; });
    fetch('/_b44_tree/').then(function (r) { return r.json(); }).then(function (root) {
      var sessions = root.filter(function (x) { return x.type === 'directory' && /^Practice Session/.test(x.name); })
        .sort(function (a, b) { return a.name.localeCompare(b.name, undefined, { numeric: true }); });
      return Promise.all(sessions.map(function (s) { return walk([s.name], s.name, ''); }));
    }).then(function () { return selectionP; }).then(function (sel) {
      sel = sel || {};
      var configured = !!sel.configured;
      var allowed = {};
      if (configured && Array.isArray(sel.published)) sel.published.forEach(function (p) { allowed[p] = true; });
      var visible = configured ? found.filter(function (f) { return allowed[f.path.join('/')]; }) : found;
      var bySession = {};
      visible.forEach(function (f) { (bySession[f.session] = bySession[f.session] || []).push(f); });
      var html = '<h2>Scenarios <a class="b44-admin" href="/_b44_admin" title="Choose which documents display">Manage</a></h2>';
      function card(f) {
        var href = '/' + f.path.map(encodeURIComponent).join('/');
        var label = f.name.replace(/\.html$/i, '');
        return '<a class="b44-card" href="' + href + '"><b>' + label + '</b>' +
          (f.topic ? '<span>' + f.topic + '</span>' : '') + '</a>';
      }
      function sorter(a, b) { return (a.topic + a.name).localeCompare(b.topic + b.name); }
      Object.keys(bySession).sort(function (a, b) { return a.localeCompare(b, undefined, { numeric: true }); }).forEach(function (s) {
        var cur = bySession[s].filter(function (f) { return !f.old; }).sort(sorter);
        html += '<h3>' + s + '</h3><div class="b44-grid">' + cur.map(card).join('') + '</div>';
      });
      if (!visible.length) html += configured
        ? '<p class="b44-note">No documents are published yet. Use <a href="/_b44_admin">Manage</a> to choose which to display.</p>'
        : '<p class="b44-note">No scenarios found.</p>';
      box.innerHTML = html;
    });
  }

  if (window.__b44back) return;
  window.__b44back = true;
  if (location.pathname === '/') {
    // Front page: show only Assets and Practice Session entries. Everything else (code, docs, config)
    // is hidden here; the code/reference folder stays reachable at /Code%20and%20Reference/.
    document.querySelectorAll('pre a').forEach(function (a) {
      var h = a.getAttribute('href') || '';
      if (h === 'Assets/' || h.indexOf('Practice%20Session') === 0) return;
      var n = a.nextSibling;
      if (n && n.nodeType === 3) n.remove();
      a.remove();
    });
    buildScenarioList();
    return;
  }

  // Reserve a strip at the top for the preview buttons so they never cover the scenario.
  var st = document.createElement('style');
  st.textContent = 'html{padding-top:60px!important;box-sizing:border-box}' +
    '#b44-topbar{position:fixed;z-index:2147483645;top:0;left:0;right:0;height:60px;background:#e1f8ff;border-bottom:1px solid #b6aff7}';
  document.head.appendChild(st);
  var bar = document.createElement('div');
  bar.id = 'b44-topbar';
  document.documentElement.appendChild(bar);

  var btn = document.createElement('a');
  btn.href = '/';
  btn.title = 'Back to home';
  btn.setAttribute('aria-label', 'Back to home');
  btn.style.cssText =
    'position:fixed;z-index:2147483646;left:16px;top:16px;' +
    'display:inline-flex;align-items:center;gap:6px;' +
    'background:#8fa3ff;color:#1e1b4b;text-decoration:none;' +
    'border:0;border-radius:999px;padding:11px 18px;' +
    'font:600 14px/1 -apple-system,"Segoe UI",Roboto,Arial,sans-serif;' +
    'box-shadow:0 4px 14px rgba(0,0,0,.25);cursor:pointer;user-select:none;';
  btn.innerHTML = '\u2190 Back to Home';
  document.documentElement.appendChild(btn);
})();
