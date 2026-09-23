/* ============================================================================
 * scorm12.js — minimal SCORM 1.2 runtime wrapper  (TEST PACKAGE)
 * ----------------------------------------------------------------------------
 * Finds the LMS "API" object per the SCORM 1.2 spec (walk up window.parent,
 * then window.opener), and exposes tiny helpers. Every call is defensive: if
 * no LMS API is found (e.g. opened straight from disk), the helpers no-op so
 * the scenario still runs for local testing.
 * ==========================================================================*/
(function (global) {
  var api = null;
  var initialized = false;

  function findAPI(win) {
    var tries = 0;
    while (win && win.API == null && win.parent && win.parent !== win && tries < 20) {
      tries++;
      win = win.parent;
    }
    return win ? win.API : null;
  }

  function getAPI() {
    if (api) return api;
    var found = findAPI(global);
    if (!found && global.opener) found = findAPI(global.opener);
    api = found || null;
    return api;
  }

  var SCORM = {
    available: function () { return !!getAPI(); },

    init: function () {
      var a = getAPI();
      if (!a) { console.log("[SCORM] No LMS API found — running standalone."); return false; }
      var ok = a.LMSInitialize("") === "true";
      initialized = ok;
      if (ok) {
        // Only set to incomplete if the LMS hasn't already stored a status.
        var status = a.LMSGetValue("cmi.core.lesson_status");
        if (!status || status === "not attempted" || status === "unknown") {
          a.LMSSetValue("cmi.core.lesson_status", "incomplete");
        }
        a.LMSCommit("");
      }
      console.log("[SCORM] LMSInitialize -> " + ok);
      return ok;
    },

    set: function (key, value) {
      var a = getAPI();
      if (!a || !initialized) return false;
      var ok = a.LMSSetValue(key, String(value)) === "true";
      a.LMSCommit("");
      return ok;
    },

    /* score 0..100 (optional) */
    setScore: function (raw, min, max) {
      var a = getAPI();
      if (!a || !initialized) return false;
      a.LMSSetValue("cmi.core.score.raw", String(raw));
      if (min != null) a.LMSSetValue("cmi.core.score.min", String(min));
      if (max != null) a.LMSSetValue("cmi.core.score.max", String(max));
      a.LMSCommit("");
      return true;
    },

    complete: function () {
      return this.set("cmi.core.lesson_status", "completed");
    },

    finish: function () {
      var a = getAPI();
      if (!a || !initialized) return false;
      a.LMSCommit("");
      var ok = a.LMSFinish("") === "true";
      initialized = false;
      console.log("[SCORM] LMSFinish -> " + ok);
      return ok;
    }
  };

  global.SCORM12 = SCORM;
})(window);
