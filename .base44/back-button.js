/* Preview-only "Back to Home" button. Injected by nginx into .html pages; scenario files are not modified.
   Clicking returns the viewer to the repo home (root directory listing). */
(function () {
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
    return;
  }

  var btn = document.createElement('a');
  btn.href = '/';
  btn.title = 'Back to home';
  btn.setAttribute('aria-label', 'Back to home');
  btn.style.cssText =
    'position:fixed;z-index:2147483646;left:16px;bottom:16px;' +
    'display:inline-flex;align-items:center;gap:6px;' +
    'background:#1355d6;color:#fff;text-decoration:none;' +
    'border:0;border-radius:999px;padding:11px 18px;' +
    'font:600 14px/1 -apple-system,"Segoe UI",Roboto,Arial,sans-serif;' +
    'box-shadow:0 4px 14px rgba(0,0,0,.25);cursor:pointer;user-select:none;';
  btn.innerHTML = '\u2190 Back to Home';
  document.documentElement.appendChild(btn);
})();
