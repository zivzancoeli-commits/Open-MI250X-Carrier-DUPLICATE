# Layer stack — planning only (not a PCBWay-signed stackup)

**Generated KiCad:** **12 layer, 2.0 mm** stuffed-switch **target** (8× electrically designed seats + four DNP **PM8536B-FEI PRIMARY**, full-width capable). Plan **12–16L, not 4**. PCBWay can assemble 1.0 mm without HDI.  
**Documented cheaper option:** **8 layer, 2.0 mm** DNP-switch / mezz+power-only — **not** the 8×-running target.  
**PEX8780-AB80BI G** is a cheaper 80-lane alt in **docs only** — not placed.  
**DO NOT ENERGIZE P48V.** Fab zip is in `fab/`. Do not upload from this agent.

PCBWay: 12L is inside Standard 1–14. Outline 492×372 < advanced finished ML **508×600**. Guest quotes 2026-08-21 used **2 oz outer / 1 oz inner**, ENIG, qty 5. See `PCBWAY.md`.

Thickness sum below is **planning**. Dielectric thicknesses are evened to hit ~2.0 mm with 2 oz outer (70 µm) and 1 oz inner (35 µm). A real stackup comes from PCBWay after an engineering review (especially for 1.0 mm-pitch 1311-ball escape).

## 12L 2.0 mm — stuffed-switch TARGET (this `.kicad_pcb`)

| Layer | KiCad name | Type | Cu | Assignment |
|---:|---|---|---:|---|
| 1 | F.Cu | signal | 2 oz | Mezz SMD, **local P48V pours**, SB175, silk |
| 2 | In1.Cu | power | 1 oz | **GND** plane |
| 3 | In2.Cu | signal | 1 oz | PE / switch reserved |
| 4 | In3.Cu | signal | 1 oz | PE / switch reserved |
| 5 | In4.Cu | power | 1 oz | **GND** plane |
| 6 | In5.Cu | signal | 1 oz | Reserved |
| 7 | In6.Cu | signal | 1 oz | Reserved |
| 8 | In7.Cu | power | 1 oz | **GND** plane |
| 9 | In8.Cu | signal | 1 oz | Reserved |
| 10 | In9.Cu | signal | 1 oz | Reserved |
| 11 | In10.Cu | power | 1 oz | **GND** plane |
| 12 | B.Cu | signal | 2 oz | Reserved / host-stub |

Guest **8L 2.0 mm $832.74** (qty 5, 7–8 days) is the **preferred 8L / no-switch / DNP-switch** coupon if all four PM8536 stay DNP; stuffing them is a **12–16L** job.

**Hypothesis discarded:** a board-wide inner/outer **P48V plane** carrying ~100 A. Replaced by SB175 star + per-seat fuse keepouts + **local** 2 oz F.Cu pours on the 16 verified Conn0 P48V pads.

Inner GND planes are via-stitched at the inlet, bucks, and around each mezz (not via-in-pad).

## 8L 2.0 mm — cheaper DNP-switch option (not generated)

| Layer | Type | Cu | Assignment |
|---:|---|---:|---|
| 1 | signal | 2 oz | Mezz + local P48V + SB175 |
| 2 | GND | 1 oz | GND |
| 3 | signal | 1 oz | Reserved |
| 4 | GND | 1 oz | GND |
| 5 | signal | 1 oz | Reserved |
| 6 | GND | 1 oz | GND |
| 7 | signal | 1 oz | Reserved |
| 8 | signal | 2 oz | Reserved |

Use only if all four PM8536 stay DNP forever and PE is not fanned out. **Not** the 8×-running target. Do not treat this as the PEX8780 stuffed stack — PEX8780 is docs-only.

## Rules of thumb used

- P48V star/fuse copper clearance **0.64 mm** (OCP UBB v1.5 >40 V internal 25 mil). Mezz pad islands use **0.20 mm** (vendor 0.9 mm pitch). Custom DRC waives vendor pitch on mezz pads only.
- GND zone clearance **0.25 mm**.
- Min geometry in this zip **6/6 mil (0.15 mm)** and **0.3 mm** drill — the quoted form. A 1.0 mm 1311-ball PM8536 escape will need finer than 6/6 and a requote; switches stay DNP on this article.
- Inner GND planes are via-stitched at KOZ interiors, bucks, and the P12V1/P3V3 alley (not via-in-pad).
