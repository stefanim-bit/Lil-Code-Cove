#!/bin/zsh
# Builds the SCORM 1.2 zip for the Layers call from the current Tony build.
# Usage: ./build-scorm.sh   (run from anywhere; output lands next to this script)
set -e
HERE="${0:A:h}"
SRC="$HERE/../Current/Tony Test Layers Call"
OUT="$HERE/PS1 Layers Call SCORM.zip"
TMP="$(mktemp -d)"

cp -R "$SRC/." "$TMP/"
cp "$HERE/scorm.js" "$HERE/imsmanifest.xml" "$TMP/"
# Load scorm.js first so CDScorm exists before the sim runs.
python3 -I - "$TMP/index.html" <<'EOF'
import sys
p = sys.argv[1]
s = open(p).read()
tag = '<script src="scorm.js"></script>'
if tag not in s:
    s = s.replace('<head>', '<head>\n' + tag, 1)
open(p, 'w').write(s)
EOF

rm -f "$OUT"
(cd "$TMP" && zip -qr -X "$OUT" . -x '.*')
rm -rf "$TMP"
echo "Built $OUT"
