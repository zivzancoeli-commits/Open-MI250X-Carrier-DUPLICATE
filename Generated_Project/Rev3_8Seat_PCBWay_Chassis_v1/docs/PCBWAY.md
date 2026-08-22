# PCBWay target (planning only — DO NOT UPLOAD / DO NOT ORDER)

**Date:** 2026-08-21  
**Source of limits:** https://www.pcbway.com/capabilities.html (Standard PCB + Advanced PCB tables).  
**Guest quotes:** live PCBWay guest cart 2026-08-21, outline **492 × 372 mm**, **qty 5 minimum** (**qty 1 rejected**), **2 oz outer OK**, **ENIG**.  
**Prefer 2.0 mm thickness.**  
**This tree is not a gerber package.** Every schematic/PCB title block: **DO NOT FABRICATE**. **Do not upload. Do not order.**

## Target coupon

| Item | This stub | PCBWay capability used | Status |
|---|---|---|---|
| Outline | **492 × 372 mm** | Standard multilayer max **560 × 1150 mm**; advanced finished multilayer **508 × 600 mm** (normal process) | **Fits both.** |
| 8-KOZ reserve | **412 × 332 mm** | n/a (mechanical) | **Inferred** 4×2 tiling of verified 103×166 mm KOZ. |
| Margin | 20 mm service + 40 mm host-stub strip | n/a | Host strip holds 2× 37.5 mm PM8536 courtyards + cable keepout. |
| Layers (**no-switch / DNP-switch**) | **8L 2.0 mm** preferred 8L stack | Standard | Live guest quote below. Mezz + local P48V only. |
| Layers (**stuffed-switch**) | **12–16L 2.0 mm** (two PM8536B-FEI) | Standard 1–14; 16L is Advanced | Generated KiCad is **12L 2.0 mm**. 12–16L quotes are a **separate fetch**. |
| Copper | **2 oz outer** (quotes); 1 oz inner on 12L/16L | Outer 1–8 oz; inner 1–4 oz (4–10 L) | Local P48V pours live on **F.Cu 2 oz**. |
| Finish | ENIG **in the guest quote**; still **TBD** for attach | HASL / ENIG / OSP | Do not pick until Molex attach process is known. |
| Qty | Guest form **qty 5 min** (qty 1 rejected). **Not ordered.** | — | |

## Live 4L / 8L guest quotes 2026-08-21 (do not upload / do not order)

All: **492 × 372 mm**, **qty 5**, **ENIG**, **2 oz outer**. Prefer **2.0 mm**.

| Stack | PCB | DHL | Total | Days | Use |
|---|---:|---:|---:|---|---|
| 4L 1.6 mm | $528.88 | $57.23 | $586.11 | 4–5 | Too thin for 8 mezz + future switch. |
| 4L 2.0 mm | $501.50 | $68.43 | $569.93 | — | Cheaper than 4L 1.6. Form reset track/space to **8/8 mil**. Still not the switch stack. |
| **8L 2.0 mm** | **$832.74** | **$68.43** | **$901.17** | **7–8** | **Preferred 8L stack. No-switch / DNP-switch / mezz+power.** |
| 8L 1.6 mm | $1498.93 | — | — | 12–13 | **Avoid.** |

SMT for **16× 688-ball Molex** is **Unknown** (form only showed an **$88 floor**). Mezz attach is not a default PCBWay stack.

## Stuffed-switch stack (12–16L) — separate fetch

**8L 2.0 mm** above is the **no-switch / DNP-switch** coupon. **12–16L** is the **stuffed-switch** stack for two **PM8536B-FEI** (1.0 mm 1311-FCBGA). Those quotes are fetched separately; numbers already on this page:

| Stack | PCB | DHL | Total | Days | Use |
|---|---:|---:|---:|---|---|
| **12L 2.0 mm Standard** | **$2237.90** | **$68.43** | **$2306.33** | 14–15 | **Stuffed-switch TARGET (generated KiCad).** Prefer 2.0 mm. |
| 12L 1.6 mm Standard | $2194.09 | $57.23 | $2251.32 | — | Prefer 2.0 mm. |
| 16L 2.0 mm Advanced | $2937.84 | $68.43 | $3006.27 | 20–21 | Standard form max 14L; 16L is Advanced. |
| 16L 1.6 mm Advanced | $2937.84 | $57.23 | $2995.07 | — | Prefer 2.0 mm if 16L ever needed. |

12L/16L quotes used **2 oz outer / 1 oz inner**. **Caveat:** guest forms used **6/6 mil + 0.3 mm hole**. A **1.0 mm-pitch 1311-ball** PM8536 escape likely needs finer rules and will cost more.

## Old MFC cart is UNRELATED

A previous qty-**5** MFC/PCBWay-style cart for a **220 × 120 mm** board is **not this coupon**.

- Do **not** reuse that quote, that qty, or that outline.
- This board is **492 × 372 mm**, 16× 218910-1115, 8 electrically designed seats.
- Do **not** upload gerbers. Do **not** click order.

## Layer stack

See `docs/LAYER_STACK.md`.

- **8L 2.0 mm** = no-switch / DNP-switch (preferred 8L).
- **12–16L 2.0 mm** = stuffed-switch (generated KiCad is 12L).

**Do not upload. Do not order.**
