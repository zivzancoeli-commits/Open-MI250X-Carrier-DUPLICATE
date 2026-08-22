# Fab notes — Rev3 8-seat PCBWay POWER+MECH first article

**Do not upload from this agent.** Eli uploads if he accepts the zip.  
**DO NOT ENERGIZE P48V** until the Molex **1.2 A/contact at 48–59.5 V (2 oz)** write-up is in hand (ticket **167157**).

## What this zip is

Gerbers + drill + IPC-D-356 + pick-and-place for a **12-layer, 2.0 mm, 492 × 372 mm** FR-4 coupon matching the live **2026-08-21** PCBWay guest quote (qty **5**, **ENIG**, **2 oz outer / 1 oz inner**, green soldermask / white silk). Min geometry in the project is **6/6 mil (0.15 mm)** and **0.3 mm** drill — the quoted form.

Silk keeps **DO NOT ENERGIZE P48V**. “DO NOT FABRICATE” is dropped on this first article because POWER+MECH copper is generated for submit. PE / switch balls are **not** routed.

## Stackup (planning, matches the quoted coupon)

| Layer | KiCad | Cu | Use |
|---:|---|---:|---|
| 1 | F.Cu | 2 oz | Mezz, local P48V / P12V1 / P3V3, SB175, fuses, bucks |
| 2 | In1.Cu | 1 oz | GND plane |
| 3–4 | In2/In3 | 1 oz | PE reserved (empty this article) |
| 5 | In4.Cu | 1 oz | GND plane |
| 6–7 | In5/In6 | 1 oz | Reserved |
| 8 | In7.Cu | 1 oz | GND plane |
| 9–10 | In8/In9 | 1 oz | Reserved |
| 11 | In10.Cu | 1 oz | GND plane |
| 12 | B.Cu | 2 oz | Reserved / host-stub |

Dielectric thicknesses in the `.kicad_pcb` are evened to ~2.0 mm. PCBWay will issue the signed stack after engineering review.

## Skip-pin / NC

Published OCP v1.0 P48V map **already satisfies Skip Pins**. TEST* / RFU / DO_NOT_USE pads have **no net and no extra copper**. Do **not** add NC pads. Do **not** short them.

## P48V

- Inlet: Anderson **6325G1** housing + **2× 1382** 1/0 AWG contacts (SB175, 175 A / 600 V). PCB landing is on-board (NPTH copper inside Edge.Cuts). Kelvin pads at the star.
- Star net `P48V_STAR` is **not** a board-wide 100 A flood.
- Per seat: Littelfuse **0476015.MR** (15 A, 125 VDC Nano2) then a **local** F.Cu island on the 16 verified Conn0 P48V pads.
- Brick input: Littelfuse **0476002.MR** (2 A, 125 VDC) into THL 40-4812WI.
- **Dell D3000E-S1 is 12 V — never tie to OAM P48V.**
- Mezz pad-to-pad gap is **0.40 mm** (Molex 0.9 mm pitch). OCP 25 mil (0.64 mm) is held on star/fuse copper. Custom DRC waives vendor pitch on mezz pads only.

## P12V1 / P3V3

- **TRACO THL 40-4812WI**: 18–75 V in, 12 V / 3.35 A / **40 W**. OCP allows P12V1 ≤50 W; this buyable 1×1 module is the first-article cap. Isolated module; primary and secondary returns bonded to board GND.
- **Murata OKI-78SR-3.3/1.5-W36-C**: 3.3 V / 1.5 A / 4.95 W from P12V1 (≤5 W). No GPU multiphase VRM.
- P12V2 is named from v1.0 and is **Unknown / may be NC** — not supplied.

## Switches / host

- Two **PM8536B-FEI** remain **DNP courtyards**. Public Microchip pages do not give a ball map; do not invent an AMD overlay or a fake BGA pinout.
- If those BGAs are stuffed later, 1.0 mm pitch escape likely needs **finer than 6/6 mil** and a requote. This zip stays on the quoted 6/6 + 0.3 mm hole.
- Host: silk + keepout toward **X11DPH-T**. No CEM / SlimSAS / MCIO MPN invented (none chosen with a public footprint for this chassis).

## SMT / mezz attach

16× 688-ball Molex **218910-1115** is **not** a default PCBWay stack. Call it out on the order. Guest form only showed an $88 SMT floor.

## What Eli can upload vs what stays DNP

See `docs/STATUS.md`. Upload the `fab/` zip as a Standard 12L coupon. Do not stuff PM8536. Do not energize P48V.
