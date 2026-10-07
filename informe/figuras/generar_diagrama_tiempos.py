"""Generate the timing diagram (SVG) for the typical entry and exit of a vehicle.

The state sequence is not drawn by hand: it is simulated from the next-state
equations of the design (informe/01-diseno-fsm.md), so the figure always
matches the logic.

Usage: python3 generar_diagrama_tiempos.py  (writes diagrama-tiempos.svg next to it)
"""
from pathlib import Path

CYCLES = 13          # clock periods drawn
STEPS_PER_CYCLE = 20 # time resolution
STATE_NAMES = {0b000: "q0", 0b001: "q1", 0b011: "q2", 0b010: "q3", 0b100: "q4"}

# Asynchronous input events: (time in clock periods, signal, value).
# Sensor edges fall between clock edges, as in the class notes.
EVENTS = [
    (1.4, "S1", 1),
    (3.4, "S2", 1),
    (5.4, "S1", 0),
    (7.4, "S2", 0),
    (10.4, "S3", 1),
    (11.3, "S3", 0),
]


def next_state(q, s1, s2):
    q2, q1, q0 = (q >> 2) & 1, (q >> 1) & 1, q & 1
    d2 = q2 | (q1 & (1 - q0) & (1 - s2))
    d1 = (1 - q2) & s2
    d0 = (1 - q2) & s1
    return (d2 << 2) | (d1 << 1) | d0


def simulate():
    """Return a list of samples: dict of signal values per time step."""
    inputs = {"S1": 0, "S2": 0, "S3": 0}
    q = 0
    samples = []
    total = CYCLES * STEPS_PER_CYCLE
    for step in range(total + 1):
        t = step / STEPS_PER_CYCLE
        phase = step % STEPS_PER_CYCLE
        # Rising clock edge at integer t >= 1, sampling inputs just before the edge.
        if phase == 0 and step > 0 and not inputs["S3"]:
            q = next_state(q, inputs["S1"], inputs["S2"])
        for ev_t, name, value in EVENTS:
            if abs(ev_t - t) < 1e-9:
                inputs[name] = value
        if inputs["S3"]:
            q = 0  # asynchronous reset
        clk = 1 if phase < STEPS_PER_CYCLE // 2 else 0
        samples.append({
            "CLK": clk, **inputs,
            "Q2": (q >> 2) & 1, "Q1": (q >> 1) & 1, "Q0": q & 1,
            "STATE": STATE_NAMES.get(q, format(q, "03b")),
            "E": (q >> 2) & 1,
        })
    return samples


# Layout
LEFT, TOP, ROW_H, WAVE_H = 120, 40, 46, 26
UNIT = 64  # px per clock period
ROWS = ["CLK", "S1", "S2", "S3", "Q2", "Q1", "Q0", "STATE", "E"]
LABELS = {"STATE": "Estado", "E": "E (ENABLE)"}


def x_at(step):
    return LEFT + step * UNIT / STEPS_PER_CYCLE


def digital_path(values, y_base):
    hi, lo = y_base, y_base + WAVE_H
    pts = [(x_at(0), lo if values[0] == 0 else hi)]
    for i in range(1, len(values)):
        if values[i] != values[i - 1]:
            x = x_at(i)
            pts.append((x, pts[-1][1]))
            pts.append((x, hi if values[i] else lo))
    pts.append((x_at(len(values) - 1), pts[-1][1]))
    return "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def bus_shapes(values, y_base):
    """Hexagon-style bus segments with a label per constant region."""
    out = []
    start = 0
    mid = y_base + WAVE_H / 2
    for i in range(1, len(values) + 1):
        if i == len(values) or values[i] != values[start]:
            x0, x1 = x_at(start), x_at(i - 1 if i == len(values) else i)
            s = 4 if x1 - x0 > 10 else 0
            out.append(
                f'<path d="M {x0:.1f},{mid:.1f} L {x0 + s:.1f},{y_base} L {x1 - s:.1f},{y_base} '
                f'L {x1:.1f},{mid:.1f} L {x1 - s:.1f},{y_base + WAVE_H} L {x0 + s:.1f},{y_base + WAVE_H} Z" '
                f'class="bus{" active" if values[start] == "q4" else ""}"/>'
            )
            out.append(
                f'<text x="{(x0 + x1) / 2:.1f}" y="{mid + 5:.1f}" class="buslabel">{values[start]}</text>'
            )
            start = i
    return "\n".join(out)


def render(samples):
    width = int(x_at(len(samples) - 1) + 30)
    height = TOP + ROW_H * len(ROWS) + 40
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="Helvetica, Arial, sans-serif">',
        "<style>"
        ".wave{fill:none;stroke:#1f3a93;stroke-width:2}"
        ".clk{fill:none;stroke:#555;stroke-width:1.5}"
        ".out{fill:none;stroke:#c0392b;stroke-width:2.5}"
        ".bus{fill:#eef2fb;stroke:#1f3a93;stroke-width:1.5}"
        ".bus.active{fill:#fdecea;stroke:#c0392b}"
        ".buslabel{font-size:13px;text-anchor:middle;fill:#111}"
        ".label{font-size:14px;font-weight:bold;fill:#111;text-anchor:end}"
        ".edge{stroke:#bbb;stroke-width:1;stroke-dasharray:3,4}"
        ".note{font-size:12px;fill:#444}"
        "</style>",
        f'<rect width="{width}" height="{height}" fill="#fff"/>',
    ]
    bottom = TOP + ROW_H * len(ROWS)
    for c in range(1, CYCLES + 1):
        x = x_at(c * STEPS_PER_CYCLE)
        parts.append(f'<line x1="{x:.1f}" y1="{TOP - 10}" x2="{x:.1f}" y2="{bottom}" class="edge"/>')
    for r, name in enumerate(ROWS):
        y = TOP + r * ROW_H
        parts.append(f'<text x="{LEFT - 12}" y="{y + WAVE_H / 2 + 5:.1f}" class="label">{LABELS.get(name, name)}</text>')
        values = [s[name] for s in samples]
        if name == "STATE":
            parts.append(bus_shapes(values, y))
        else:
            cls = "clk" if name == "CLK" else "out" if name == "E" else "wave"
            parts.append(f'<path d="{digital_path(values, y)}" class="{cls}"/>')
    parts.append(
        f'<text x="{LEFT}" y="{bottom + 28}" class="note">Líneas punteadas: flancos ascendentes de CLK. '
        "S1, S2 y S3 cambian entre flancos (asincrónicas). S3 resetea los flip-flops de forma asincrónica.</text>"
    )
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    out = Path(__file__).with_name("diagrama-tiempos.svg")
    out.write_text(render(simulate()), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
