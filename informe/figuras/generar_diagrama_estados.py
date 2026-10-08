"""Generate the state/output diagram (SVG) of the beacon control Moore FSM.

Labels on the transitions are the S1S2 values. S3 is not drawn as a normal
transition: it drives the asynchronous reset of the flip-flops.

Usage: python3 generar_diagrama_estados.py  (writes diagrama-estados.svg next to it)
"""
import math
from pathlib import Path

STATES = ["q0", "q1", "q2", "q3", "q4"]
OUTPUT = {"q0": 0, "q1": 0, "q2": 0, "q3": 0, "q4": 1}
FORWARD = [("q0", "q1", "10"), ("q1", "q2", "11"), ("q2", "q3", "01"), ("q3", "q4", "00")]
REVERSAL = [("q1", "q0", "00"), ("q2", "q1", "10"), ("q3", "q2", "11")]
SELF_LOOPS = {"q0": "00", "q1": "10", "q2": "11", "q3": "01", "q4": "XX"}

# Layout
R = 42            # state circle radius
X0, DX = 190, 190 # first circle x and spacing
CY = 190          # row y
WIDTH, HEIGHT = X0 + DX * 4 + 90, 350
LEGEND = "Etiquetas de transición: S1S2 (XX = cualquier valor). S3 actúa sobre el reset asíncrono de los flip-flops."


def cx(name):
    return X0 + DX * STATES.index(name)


def on_circle(name, angle_deg):
    a = math.radians(angle_deg)
    return cx(name) + R * math.cos(a), CY + R * math.sin(a)


def state_shape(name):
    active = OUTPUT[name] == 1
    cls = "state active" if active else "state"
    x = cx(name)
    return (
        f'<circle cx="{x}" cy="{CY}" r="{R}" class="{cls}"/>'
        f'<text x="{x}" y="{CY - 3}" class="sname">{name}</text>'
        f'<text x="{x}" y="{CY + 17}" class="sout">E={OUTPUT[name]}</text>'
    )


def forward_arrow(src, dst, label):
    dy = -14  # slightly above the row center line
    half = math.sqrt(R * R - dy * dy)
    x1, x2 = cx(src) + half, cx(dst) - half
    y = CY + dy
    return (
        f'<line x1="{x1:.1f}" y1="{y}" x2="{x2:.1f}" y2="{y}" class="arrow" marker-end="url(#head)"/>'
        f'<text x="{(x1 + x2) / 2:.1f}" y="{y - 8}" class="tlabel">{label}</text>'
    )


def reversal_arrow(src, dst, label):
    # Curved below the row, from the bottom-left of src to the bottom-right of dst.
    x1, y1 = on_circle(src, 125)
    x2, y2 = on_circle(dst, 55)
    mx = (x1 + x2) / 2
    cy_ctrl = CY + R + 70
    apex = (y1 + 2 * cy_ctrl + y2) / 4
    return (
        f'<path d="M {x1:.1f},{y1:.1f} Q {mx:.1f},{cy_ctrl} {x2:.1f},{y2:.1f}" '
        f'class="arrow" marker-end="url(#head)"/>'
        f'<text x="{mx:.1f}" y="{apex + 20:.1f}" class="tlabel">{label}</text>'
    )


def self_loop(name, label):
    # Loop above the circle, between -125 and -55 degrees.
    x1, y1 = on_circle(name, -125)
    x2, y2 = on_circle(name, -55)
    x = cx(name)
    top = CY - R - 62
    return (
        f'<path d="M {x1:.1f},{y1:.1f} C {x - 42:.1f},{top} {x + 42:.1f},{top} {x2:.1f},{y2:.1f}" '
        f'class="arrow" marker-end="url(#head)"/>'
        f'<text x="{x}" y="{CY - R - 56 + 4}" class="tlabel" dy="-10">{label}</text>'
    )


def reset_arrow():
    x2 = cx("q0") - R
    x1 = 20
    return (
        f'<line x1="{x1}" y1="{CY}" x2="{x2}" y2="{CY}" class="arrow reset" marker-end="url(#head-reset)"/>'
        f'<text x="{(x1 + x2) / 2:.1f}" y="{CY - 10}" class="rlabel">RST (S3 = 1)</text>'
    )


def render():
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" font-family="Helvetica, Arial, sans-serif">',
        "<style>"
        ".state{fill:#eef2fb;stroke:#1f3a93;stroke-width:2}"
        ".state.active{fill:#fdecea;stroke:#c0392b;stroke-width:2.5}"
        ".sname{font-size:18px;font-weight:bold;fill:#111;text-anchor:middle}"
        ".sout{font-size:13px;fill:#333;text-anchor:middle}"
        ".arrow{fill:none;stroke:#1f3a93;stroke-width:2}"
        ".arrow.reset{stroke:#555}"
        ".tlabel{font-size:14px;font-weight:bold;fill:#111;text-anchor:middle}"
        ".rlabel{font-size:12px;fill:#444;text-anchor:middle}"
        ".note{font-size:12px;fill:#444}"
        "</style>",
        "<defs>"
        '<marker id="head" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
        'orient="auto" markerUnits="userSpaceOnUse"><path d="M 0,0 L 10,5 L 0,10 z" fill="#1f3a93"/></marker>'
        '<marker id="head-reset" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" '
        'orient="auto" markerUnits="userSpaceOnUse"><path d="M 0,0 L 10,5 L 0,10 z" fill="#555"/></marker>'
        "</defs>",
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="#fff"/>',
    ]
    parts += [forward_arrow(*t) for t in FORWARD]
    parts += [reversal_arrow(*t) for t in REVERSAL]
    parts += [self_loop(n, lbl) for n, lbl in SELF_LOOPS.items()]
    parts.append(reset_arrow())
    parts += [state_shape(n) for n in STATES]
    parts.append(f'<text x="{WIDTH / 2:.0f}" y="{HEIGHT - 20}" class="note" text-anchor="middle">{LEGEND}</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    out = Path(__file__).with_name("diagrama-estados.svg")
    out.write_text(render(), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
