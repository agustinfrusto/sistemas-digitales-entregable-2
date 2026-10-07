#!/usr/bin/env bash
# Build the deliverable PDF: Markdown -> HTML (pandoc) -> PDF (headless Chrome).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$HERE/Entregable2-SistemasDigitales.pdf"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

command -v pandoc >/dev/null || { echo "pandoc not found (brew install pandoc)" >&2; exit 1; }
[ -x "$CHROME" ] || { echo "Google Chrome not found at: $CHROME" >&2; exit 1; }

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

# Regenerate the figures from their scripts.
python3 -I "$HERE/figuras/generar_diagrama_tiempos.py"
python3 -I "$HERE/figuras/generar_diagrama_estados.py"

# The schematic screenshot may not exist yet: use a visible placeholder instead.
SCHEMATIC="$TMP/04-esquematico.md"
if [ -f "$HERE/figuras/esquematico.png" ]; then
  cp "$HERE/04-esquematico.md" "$SCHEMATIC"
else
  echo "figuras/esquematico.png not found: using placeholder" >&2
  cat > "$TMP/esquematico-pendiente.svg" <<'SVG'
<svg xmlns="http://www.w3.org/2000/svg" width="700" height="320" viewBox="0 0 700 320" font-family="Helvetica, Arial, sans-serif">
<rect x="2" y="2" width="696" height="316" fill="#fff" stroke="#999" stroke-width="2" stroke-dasharray="10,6"/>
<text x="350" y="166" font-size="22" fill="#666" text-anchor="middle">Captura del esquemático pendiente</text>
</svg>
SVG
  while IFS= read -r line; do
    printf '%s\n' "${line//figuras\/esquematico.png/esquematico-pendiente.svg}"
  done < "$HERE/04-esquematico.md" > "$SCHEMATIC"
fi

pandoc "$HERE/portada.md" "$HERE/02-diagrama-tiempos.md" "$HERE/01-diseno-fsm.md" "$SCHEMATIC" \
  --from markdown --to html5 --standalone --embed-resources \
  --number-sections --toc --toc-depth=2 \
  --css "$HERE/estilo.css" -V document-css=false \
  --resource-path "$HERE:$TMP" \
  --output "$TMP/informe.html"

"$CHROME" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$OUT" "file://$TMP/informe.html" >/dev/null 2>&1

echo "wrote $OUT"
