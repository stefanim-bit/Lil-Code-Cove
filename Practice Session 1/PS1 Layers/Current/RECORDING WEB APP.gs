/**
 * PS1 Layers V3 — Call-recording sink (Google Apps Script Web App)
 * ---------------------------------------------------------------------------
 * Receives the learner's call audio from the sim, saves it to a Drive folder,
 * and appends one row to a "Recordings" tab keyed by attempt_id — the SAME id
 * the sim sends to the telemetry Google Form, so a recording links back to that
 * learner's telemetry rows.
 *
 * The per-action telemetry keeps going to the existing Google Form, untouched.
 * This Web App handles ONLY the audio file, because a Google Form cannot accept
 * a file from an anonymous cross-origin POST.
 *
 * ── ONE-TIME SETUP ──────────────────────────────────────────────────────────
 * 1. Open the results Google Sheet → Extensions → Apps Script.
 * 2. Paste this whole file in. Set SHEET_ID and (optionally) FOLDER_NAME below.
 * 3. Deploy → New deployment → type "Web app".
 *      • Execute as:      Me
 *      • Who has access:  Anyone            <-- IMPORTANT (see note)
 * 4. Copy the Web app URL (ends in /exec) and paste it into RECORDING_ENDPOINT
 *    in the sim HTML (PS1 Layers V3 Call POC.html).
 *
 * TWO SEPARATE COPIES (deploy this script once per copy):
 *   • INTERNAL copy  — its Sheet + Drive folder shared with the L&D group only.
 *   • BPO copy       — its Sheet + Drive folder shared with the Trainers group
 *                      AND the L&D group.
 *   Keep them fully separate: each copy is its own sim HTML with its own
 *   RECORDING_ENDPOINT → its own Web App deployment → its own SHEET_ID and
 *   FOLDER_NAME. That way internal and BPO recordings never mix, and each
 *   audience's results are visible only to the groups you share that copy with.
 *   Playback for the learner is local/in-activity and identical in both copies —
 *   it needs no Drive access, so nothing changes there.
 *
 * WHY "Anyone" AND NOT "Anyone within Wix":
 *   Internal learners use @wix.com, but external BPO learners use @wixcs.com — a
 *   different domain. A domain-scoped Web App rejects the other domain with 401
 *   (the error the earlier build hit). "Anyone" + "Execute as: Me" means every
 *   learner can POST with no sign-in, and the files land in YOUR Drive; learners
 *   never need Drive access. Identity still travels in the payload (name/email).
 *
 * SECURITY NOTE: "Anyone" means the URL accepts anonymous POSTs. It's an
 *   unlisted URL, not a secret. For a POC this matches the anonymous telemetry
 *   Form already in use. If you later want to lock it down, add a shared SECRET
 *   check (see the commented block in doPost) and send it from the sim too.
 */

var SHEET_ID    = 'PASTE_THE_SHEET_ID_HERE';   // the id in the Sheet's URL: /d/<THIS>/edit
var TAB_NAME    = 'Recordings';                 // created automatically if missing
var FOLDER_NAME = 'PS1 Call Recordings';        // Drive folder for the audio files
// var SECRET   = '';                           // optional: require a matching token

function doPost(e) {
  try {
    var p = (e && e.parameter) || {};

    // Optional shared-secret gate (uncomment here and send `secret` from the sim):
    // if (SECRET && p.secret !== SECRET) return _text('forbidden');

    var b64 = p.audio_b64 || '';
    if (!b64) return _text('no audio');

    var mime = p.mime || 'audio/webm';
    var ext  = mime.indexOf('mp4') > -1 ? 'm4a'
             : mime.indexOf('ogg') > -1 ? 'ogg'
             : 'webm';

    var attempt = _clean(p.attempt_id || 'unknown');
    var email   = _clean(p.learner_email || '');
    var name    = _clean(p.learner_name || '');
    var course  = p.course || '';

    // Build a readable, traceable filename: email__attempt.ext
    var safeEmail = email.replace(/[^a-zA-Z0-9._@-]/g, '_') || 'anon';
    var fileName  = safeEmail + '__' + attempt + '.' + ext;

    // Decode and save to Drive.
    var bytes = Utilities.base64Decode(b64);
    var blob  = Utilities.newBlob(bytes, mime, fileName);
    var file  = _folder().createFile(blob);
    file.setDescription('PS1 Call recording · ' + name + ' <' + email + '> · attempt ' + attempt);

    var url = file.getUrl();

    // Append the row to the Recordings tab.
    _sheet().appendRow([ new Date(), attempt, email, name, course, url ]);

    return _text('ok');
  } catch (err) {
    return _text('error: ' + err);
  }
}

// A GET is handy to confirm the deployment is live (visit the /exec URL).
function doGet() { return _text('PS1 recording sink is running.'); }

function _sheet() {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sh = ss.getSheetByName(TAB_NAME);
  if (!sh) {
    sh = ss.insertSheet(TAB_NAME);
    sh.appendRow(['timestamp', 'attempt_id', 'learner_email', 'learner_name', 'course', 'recording_url']);
  }
  return sh;
}

function _folder() {
  var it = DriveApp.getFoldersByName(FOLDER_NAME);
  return it.hasNext() ? it.next() : DriveApp.createFolder(FOLDER_NAME);
}

function _clean(s) { return String(s == null ? '' : s).trim(); }
function _text(s)  { return ContentService.createTextOutput(s).setMimeType(ContentService.MimeType.TEXT); }
