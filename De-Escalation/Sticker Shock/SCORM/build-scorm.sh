#!/bin/zsh
# Builds the SCORM 1.2 zip (Wix Smart / LMS upload) for the guided Sticker Shock call.
# Usage: ./build-scorm.sh   (run from anywhere; output lands next to this script)
# Copies everything in the build folder, so Daniel's images get included once added there.
set -e
HERE="${0:A:h}"
SRC="$HERE/../Current/Sticker Shock Call - Guided"
OUT="$HERE/Sticker Shock Call - Guided SCORM.zip"
TMP="$(mktemp -d)"

cp -R "$SRC/." "$TMP/"
cp "$HERE/scorm.js" "$HERE/imsmanifest.xml" "$TMP/"
# Load scorm.js first so CDScorm exists before the sim runs.
python3 -I - "$TMP/index.html" <<'PY'
import sys
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
tag = '<script src="scorm.js"></script>'
if tag not in s:
    s = s.replace('<head>', '<head>\n' + tag, 1)
open(p, 'w', encoding='utf-8').write(s)
PY

rm -f "$OUT"
(cd "$TMP" && zip -qr -X "$OUT" . -x '.*')
rm -rf "$TMP"
echo "Built $OUT"
