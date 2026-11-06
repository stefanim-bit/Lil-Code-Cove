/* SCORM 1.2 wrapper for Care Dojo call sims.
   Loaded only in the LMS (SCORM) build. The sim calls CDScorm.setVar() from
   pushRiseVar(), so the same variables it sends to Rise land in the LMS:
     activity_score    → cmi.core.score.raw (0–100)
     activity_complete → cmi.core.lesson_status = "completed"
   The call tab (opened when the LMS frame blocks the mic) never talks to the
   LMS itself; it relays to this page, which reports. */
(function(){
  var api = null, started = false, finished = false;

  function findAPI(win){
    for(var i = 0; win && i < 10; i++){
      try{ if(win.API) return win.API; }catch(e){}
      if(win.parent === win) break;
      win = win.parent;
    }
    return null;
  }
  function getAPI(){
    if(api) return api;
    api = findAPI(window);
    if(!api){ try{ if(window.opener) api = findAPI(window.opener); }catch(e){} }
    return api;
  }
  function init(){
    if(started || new URLSearchParams(location.search).get('cdCallTab') === '1') return;
    var a = getAPI();
    if(!a){ console.warn('[CDScorm] No SCORM 1.2 API found; running without LMS reporting.'); return; }
    started = String(a.LMSInitialize('')) === 'true';
    if(!started) return;
    var status = a.LMSGetValue('cmi.core.lesson_status');
    if(status === 'not attempted' || status === '') a.LMSSetValue('cmi.core.lesson_status', 'incomplete');
    a.LMSCommit('');
  }
  function finish(){
    if(!started || finished) return;
    finished = true;
    try{ api.LMSCommit(''); api.LMSFinish(''); }catch(e){}
  }

  window.CDScorm = {
    setVar: function(name, value){
      if(!started) return;
      if(name === 'activity_score'){
        var n = Math.max(0, Math.min(100, parseInt(value, 10) || 0));
        api.LMSSetValue('cmi.core.score.min', '0');
        api.LMSSetValue('cmi.core.score.max', '100');
        api.LMSSetValue('cmi.core.score.raw', String(n));
        api.LMSCommit('');
      } else if(name === 'activity_complete' && String(value) === 'true'){
        api.LMSSetValue('cmi.core.lesson_status', 'completed');
        api.LMSCommit('');
      }
    }
  };

  init();
  window.addEventListener('pagehide', finish);
  window.addEventListener('beforeunload', finish);
})();
