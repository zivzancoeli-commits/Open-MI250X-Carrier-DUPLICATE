# Layer stack — planning only (not a PCBWay-signed stackup)

**Generated KiCad:** **12 layer, 2.0 mm** stuffed-switch **target** (8× electrically designed seats + two DNP PM8536B-FEI).  
**Documented cheaper option:** **8 layer, 2.0 mm** DNP-switch / mezz+power-only — **not** the 8×-running target.  
**Do not fabricate. Do not upload.**

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

Why 12 not 4 or 8 for the 8×-running board: two **1311-ball 1.0 mm** PM8536 plus **16× 688-contact** mezz BGAs need more than two signal inners. Guest **8L 2.0 mm $832.74** is the **DNP-switch** coupon if Eli never stuffs the switches; stuffing them is a **12L** (or 16L) job.

**Hypothesis discarded:** a board-wide inner/outer **P48V plane** carrying ~100 A. Replaced by SB175 star + per-seat fuse keepouts + **local** 2 oz F.Cu pours on the 16 verified Conn0 P48V pads.

Inner GND planes do **not** yet via-stitch to SMD GND pads (no via farm on this stub).

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

Use only if both PM8536 stay DNP forever and PE is not fanned out. **Not** the 8×-running target.

## Rules of thumb used

- P48V zone clearance **0.64 mm** (OCP UBB v1.5 >40 V internal 25 mil). Mezz 0.9 mm pitch will still DRC against that — expected, not a sign-off.
- GND zone clearance **0.25 mm**.
- Min trace in project **0.1 mm / 4 mil**. Guest quote was **6/6 mil** — a 1.0 mm BGA escape may need finer and will requote.
