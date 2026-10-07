# Beacon control FSM — Entregable #2

## Objective

Design and implement the clocked sequential controller that enables the road
beacons (`ENABLE = 1`) after detecting the entry sequence S1S2 = 00 → 10 → 11 →
01 → 00, and resets on exit (S3).

## Problem / why

Course deliverable (Sistemas Digitales, Universidad de Montevideo). Every
deliverable item in the brief must be produced and consistent with the others.

## Scope

- In: synthesis documents (state diagram → equations), timing diagram,
  SimulIDE 0.4.14-SR4 schematic + `.simu`, report assembly, video script.
- Out: recording the video, uploading to Moodle (user-owned).

## Constraints

- Moore machine, D flip-flops, S3 drives asynchronous RST (per class notes).
- Reversals allowed during entry detection (Hip #2); one vehicle at a time (Hip #1).
- Report artifacts written in Spanish (academic deliverable).
- Work sequentially: at most one agent at a time.

## Checklist

- [x] T1 — State diagram, state/output table, encoding, encoded table,
  next-state and output logic (`informe/01-diseno-fsm.md`).
  Route: inline (single file). Evidence: equations verified by exhaustive
  simulation of every specified transition (script, all OK).
- [ ] T2 — Timing diagram, typical entry + exit without reversals.
- [ ] T3 — SimulIDE schematic and `.simu` file (0.4.14-SR4).
- [ ] T4 — Report assembly and video script (< 3 min).

## Acceptance criteria

- Every transition in the state table is reproduced by the derived equations.
- Schematic in SimulIDE reproduces the timing diagram.

## Checks

- TDD: off (not a software project; no configured runner). Functional check:
  exhaustive simulation of the derived equations against the state table.

## Progress

- T1 done. Chosen encoding q0=000, q1=001, q2=011, q3=010, q4=100 (minimum
  cost out of all 840 encodings with q0=000).

## Next step

T2 — timing diagram.
