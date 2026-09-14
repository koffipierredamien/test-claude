#!/usr/bin/env bash
# Exporte les fonds SVG en PNG 2x (2560x1440) pour Power BI.
# Power BI n'accepte pas le SVG en arriere-plan de page : PNG obligatoire.
set -euo pipefail
CHROME="${CHROME:-/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell}"
SRC="${1:-fonds/svg_propres}"
DST="${2:-fonds/png}"
mkdir -p "$DST" "$(dirname "$0")/../.tmp_html"
TMP="$(mktemp -d)"
for f in "$SRC"/P*.svg; do
  nom="$(basename "$f" .svg)"
  { printf '<style>html,body{margin:0;padding:0;overflow:hidden}svg{display:block}</style>'
    cat "$f"
  } > "$TMP/$nom.html"
  "$CHROME" --headless --no-sandbox --disable-gpu --hide-scrollbars \
    --force-device-scale-factor=2 --window-size=1280,720 \
    --default-background-color=FFFFFFFF --virtual-time-budget=2000 \
    --screenshot="$DST/$nom.png" "file://$TMP/$nom.html" 2>/dev/null
  echo "$nom.png"
done
rm -rf "$TMP"
