# Layer stack — planning only (not a PCBWay-signed stackup)

**Switch keepout:** Broadcom **PEX8780-AB80BI G** — **CANDIDATE, not stuffed.** 80-lane / 20-port Gen3, **35×35 mm 1156-FCBGA**.  
**If this BGA is ever stuffed: 8-layer 2.0 mm is likely.** PCBWay assembly of 1156-FCBGA is **Unknown** — keep DNP.  
**Generated KiCad** is still **12 layer, 2.0 mm** (mezz + local P48V + GND planes). That is not a stuffed-1156 sign-off.  
**Do not fabricate. Do not upload. Do not invent a second switch MPN.**

PCBWay: 8L and 12L are inside Standard 1–14. Outline 492×372 < advanced finished ML **508×600**. Guest quotes 2026-08-21 used **2 oz outer / 1 oz inner**, ENIG, qty 5. See `PCBWAY.md`.

Thickness sum below is **planning**. Dielectric thicknesses are evened to hit ~2.0 mm with 2 oz outer (70 µm) and 1 oz inner (35 µm). A real stackup comes from PCBWay after an engineering review (especially for a 1156-FCBGA escape).

## 8L 2.0 mm — likely if PEX8780 1156 is stuffed (not generated)

| Layer | Type | Cu | Assignment |
|---:|---|---:|---|
| 1 | signal | 2 oz | Mezz + local P48V + SB175 |
| 2 | GND | 1 oz | GND |
| 3 | signal | 1 oz | PE / switch reserved |
| 4 | GND | 1 oz | GND |
| 5 | signal | 1 oz | PE / switch reserved |
| 6 | GND | 1 oz | GND |
| 7 | signal | 1 oz | Reserved |
| 8 | signal | 2 oz | Reserved / host-stub |

Guest **8L 2.0 mm $832.74** (qty 5, 2026-08-21). This is the likely stuffed stack for **one** 35 mm 1156-FCBGA, not a second invented switch.

## 12L 2.0 mm — current generated `.kicad_pcb`

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

Generated 12L is leftover copper-plane planning for the 16× 688-contact mezz. Stuffing the PEX8780 CANDIDATE is **8L-likely**, not a 12L requirement. Do not treat 12L as a tape-out.

**Hypothesis discarded:** a board-wide inner/outer **P48V plane** carrying ~100 A. Replaced by SB175 star + per-seat fuse keepouts + **local** 2 oz F.Cu pours on the 16 verified Conn0 P48V pads.

Inner GND planes do **not** yet via-stitch to SMD GND pads (no via farm on this stub).

## Rules of thumb used

- P48V zone clearance **0.64 mm** (OCP UBB v1.5 >40 V internal 25 mil). Mezz 0.9 mm pitch will still DRC against that — expected, not a sign-off.
- GND zone clearance **0.25 mm**.
- Min trace in project **0.1 mm / 4 mil**. Guest quote was **6/6 mil** — a 1156-FCBGA escape may need finer and will requote.
