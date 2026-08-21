# PCBWay target (planning only — DO NOT UPLOAD / DO NOT ORDER)

**Date:** 2026-08-21  
**Source of limits:** https://www.pcbway.com/capabilities.html (Standard PCB + Advanced PCB tables).  
**This tree is not a gerber package.** Every schematic/PCB title block: **DO NOT FABRICATE**.

## Target coupon

| Item | This stub | PCBWay capability used | Status |
|---|---|---|---|
| Outline | **492 × 372 mm** | Standard multilayer max **560 × 1150 mm**; advanced finished multilayer **508 × 600 mm** (normal process) | **Fits both.** 492 < 508 and 372 < 600, so it should quote as standard-ish / advanced-normal, not an oversized special. |
| 8-KOZ reserve | **412 × 332 mm** | n/a (mechanical) | **Inferred** 4×2 tiling of verified 103×166 mm KOZ. Not a UBB drawing. |
| Margin | 20 mm service + 40 mm host-stub strip | n/a | **Planning** (copied 20 mm idea from the 2-seat envelope). |
| Layers | **4** (F.Cu / In1.Cu / In2.Cu / B.Cu) | Standard 1–14 | Inners **reserved**. Do not invent a 20-layer UBB. |
| Thickness | **1.6 mm** in the KiCad stackup; planning range **1.6–2.4 mm** | Standard 0.2–3.2 mm; 1.6 / 2.0 / 2.4 listed | 2.0–2.4 mm may be wanted later for stiffness of a ~0.5 m coupon. **TBD.** |
| Material | FR-4 | Standard FR-4 | |
| Min trace | 0.1 mm in project rules | Standard min 0.1 mm / 4 mil | No signal tracks on this stub, so unused. |
| Finish | **TBD** | HASL / ENIG / OSP / … | Do not pick ENIG vs HASL until Molex attach process is known. |
| Solder mask / silk | Green / white **TBD** | Standard colors | Silk already carries DO NOT FABRICATE / DO NOT ENERGIZE. |
| Qty | **Not ordered.** | — | |

## Old MFC cart is UNRELATED

A previous qty-**5** MFC/PCBWay-style cart for a **220 × 120 mm** board is **not this coupon**.

- Do **not** reuse that quote, that qty, or that outline.
- This board is **492 × 372 mm**, 16× 218910-1115, 8 seats.
- Do **not** upload gerbers. Do **not** click order.

## Why it still cannot be ordered

See `STATUS.md`. Headline blockers: Molex catalog **30 V** vs OCP **44–59.5 V** (ticket **167157**), no AMD overlay, no P48V pour by design, no host connector MPN, seats 2–7 need an on-board PCIe switch (**MPN Unknown**), 218910-1115 mezz attach is not a default PCBWay stack.

**Do not upload. Do not order.**
