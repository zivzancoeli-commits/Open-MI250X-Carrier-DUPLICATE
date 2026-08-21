# STATUS — Rev3 8-seat PCBWay chassis stub

**Tree:** `Generated_Project/Rev3_8Seat_PCBWay_Chassis_v1/`  
**Date:** 2026-08-21 15:41 PT  
**Pin map:** `22_Pinmap_Research/extracted/OAM_v1.0_OCP_Generic_Pin_Map.csv` (1376 named pads). xlsx in `22_Pinmap_Research/downloads/` wins on mismatch; this generator consumes the CSV (P3V3 = Conn0 C1/C2 checked). **v1.x only.** r2.0 is UNUSABLE.

**DO NOT FABRICATE. DO NOT ENERGIZE P48V.** Named-net + mechanical mapping artifact, not a fab package, not a PCBWay order.

Labels: **Verified** / **Inferred** / **Unknown**. Do not treat Inferred as a pin assignment or a UBB drawing.

---

## What this tree is

8 OAM seats on one 4-layer FR-4 coupon:

| | |
|---|---|
| Outline | **492 × 372 mm** |
| 8-KOZ floor | **412 × 332 mm** = 4×2 of 103×166 mm |
| Seat grid | col pitch 103 mm, row pitch 166 mm. Row 0 (Y=20): seats **0 1 2 3**. Row 1 (Y=186): seats **4 5 6 7**. |
| Connectors | **16×** Molex **218910-1115** (2 per seat), rot 180 **Inferred** |
| Holes | **32×** M3.5 NPTH φ3.9 mm (Fig 2), 8 mm MIN land |
| Layers | 4. Inners reserved. **No signal tracks.** **No P48V pour.** |
| Host region | X=452–492 mm strip. Silk only. **No CEM invented.** |

Seats **0–1** (populate now): v1.0 named nets including host PCIe, aimed at the host region.  
Seats **2–7** (same lands, later): **mechanical + power pads only**; PCIe/xGMI/clock/mgmt **no net**.

Regenerate (do not hand-edit pad nets):

```
python3 Generated_Project/Rev3_8Seat_PCBWay_Chassis_v1/tools/generate_from_v10_pinmap.py
```

---

## PCBWay size vs 508 × 600

| Limit | Value | This board |
|---|---|---|
| PCBWay standard multilayer max | 560 × 1150 mm | 492 × 372 **fits** |
| PCBWay advanced finished multilayer (normal process) | **508 × 600 mm** | 492 < 508 and 372 < 600 → **fits** (16 mm / 228 mm slack) |
| 8-KOZ + 20 mm margin only | 452 × 372 mm | also fits; we added a 40 mm host-stub strip |

It should quote as standard-ish, not an oversize special. **Still do not upload.** Finish TBD. Thickness 1.6 mm in KiCad, planning 1.6–2.4 mm. Old MFC qty-5 **220 × 120 mm** cart is **UNRELATED** (`docs/PCBWAY.md`).

---

## Why 8-seat PCB vs buying AS-4124GQ-TNMI

AS-4124GQ-TNMI is SuperMicro’s 4U MI250 OAM system (AOM-MCM-Q-P UBB, 54 V UBB cable CBL-PWEX-1280, Infinity Fabric GPU–GPU, EPYC 7003 host, 3 kW PSUs). Public integrator pages this run listed barebone starting about **$10.5k–$18k** (Wiredzone $10,502; Broadberry “configuring from $18,287”; Computerlink “starting at $17,088.99”) and several vendors will only sell a **full** system (CPUs + RAM + 4 GPUs), not the tray alone.

This PCB exists because Eli wants a **carrier/UBB-like coupon** that:

1. Holds **8 identical seats** on one FR-4 board (2 populated now).
2. Is **PCBWay-size** (492 × 372 < 508 × 600) instead of a server SKU.
3. Reuses the locked **X11DPH-T** host rather than buying dual EPYC 7003.

It is **not** a replacement for the SuperMicro UBB: xGMI is not routed, seats 2–7 have no host PCIe, P48V is not a closed 54 V harness, and Molex 30 V vs OCP 44–59.5 V is still open. The cost argument is “bare FR-4 + 16 mezz connectors vs a 4U OAM server,” **not** “this stub enumerates 8× MI250X.”

---

## Verified (this stub)

| Item | Evidence |
|---|---|
| 1376 named pads, Conn0+Conn1 688 each | v1.0 CSV row count |
| P3V3 = Conn0 C1, C2 (2 pads) | v1.0 map; matches v1.5 Table 4. r2.0 (P3V3=6) UNUSABLE |
| Shared OCP rails `P48V` `P12V1` `P12V2` `P3V3` `GND` | v1.0 names. Same net on all 8 OAMs. **No VRM. No P48V pour.** |
| P48V: 16 Conn0 pads/seat, OCP 44–59.5 V class | v1.0 pin list / OCP Table 5 family |
| Connector MPN 218910-1115, hermaphroditic, 5.00 mm stack | Farnell 2189101115; OCP v1.5 §5/§6.2. Buy **16× for the carrier** |
| Module PCB 102×165 mm; KOZ 103×166 mm; M3.5 holes φ3.9 mm | OCP v1.5 Fig 2 / Fig 14 |
| 4 copper layers | This generator. Inners reserved. |
| TEST0–TEST14, TEST_MODE#, RFU, DO_NOT_USE | Named in v1.0; **unmapped** (no net, no copper) |
| PVREF Conn0 G1/G2 | Module **output**. Never drive. Per-seat nets `OAM0_PVREF` … `OAM7_PVREF`. |
| X11DPH-T lane budget | SuperMicro: 3× Gen3 x16 + 4× Gen3 x8. Not enough for 8× MI250X. |
| PCBWay 4-layer coupon 492×372 vs 508×600 | capabilities.html advanced finished ML 508×600 |

### Pad accounting (one 688+688 map; PCB instantiates it eight times)

| Class | Pads / map | Seats 0–1 | Seats 2–7 |
|---|---:|---|---|
| `power_shared` | 728 | named `P48V`/`P12V1`/`P12V2`/`P3V3`/`GND` | **same** (mechanical+power) |
| `pcie_stub` | 64 | hierarchical labels toward host region; **no CEM** | **no net** |
| `clock_reset` | 16 | labels only | **no net** |
| `mgmt_stub` | 17 | named | **no net** |
| `ocp_sideband` | 19 | named; ID/CONFIG resistors **not placed** | **no net** |
| `module_output_do_not_drive` | 2 | PVREF | PVREF (still named, never driven) |
| `serdes_named_not_routed` | 448 | named on pads, **not routed between OAMs** | **no net** |
| `qsfp_sideband_named_not_routed` | 14 | named, not routed | **no net** |
| `mgmt_link_named_not_routed` | 8 | named, not routed | **no net** |
| `named_other` | 1 | `SCALE_DEBUG_EN` | **no net** |
| `unmapped_nc` | **59** | TEST*/RFU/DO_NOT_USE. **No net.** | **No net.** |

Netted pads: seats 0–1 = **1317 / 1376** each; seats 2–7 = **730 / 1376** each (728 power + 2 PVREF).  
Unique named nets on the 8-seat PCB: **1187**. Empty pad instances: **3994 / 11008**.

Seat 0 connector centres (match Rev2 2-seat): Conn0 **(71.5, 154.0)**, Conn1 **(71.5, 52.0)** mm.

---

## Inferred

| Item | Basis | Do not treat as |
|---|---|---|
| 8-GPU floor **412 × 332 mm** | 4×2 tiling of 103×166 mm KOZ | A Universal Baseboard drawing |
| 20 mm service margin + 40 mm host strip → **492 × 372 mm** | Copied 20 mm idea from 2-seat envelope; host strip is silk REGION | A fab panel drawing or CEM connector |
| Footprint rotation **180°** | Fig 2 PIN A3 on +X vs candidate land A3 at x=−29.45 | Proven module↔baseboard silk until overlay-checked |
| AS-4124GQ-TNMI street **~$10.5k–$18k** barebone | Integrator pages 2026-08-21 | A quote, a UBB DXF, or permission to copy their xGMI |

---

## Unknown (blocking energize / overlay / order)

| Item | Status |
|---|---|
| AMD MI250X 688-pad overlay | **Unknown** (NDA) |
| Which S1–S7 are xGMI / Infinity Fabric | **Unknown**. Not routed. |
| Dual-GCD host PCIe 1×16 vs 2×8 / `PE_BIF[1:0]` | **Unknown** |
| On-board PCIe switch for seats 2–7 | **MPN Unknown** |
| Host connector in the silk REGION | **Unknown**. Not invented. |
| P12V2 required on 48 V MI250X | **Unknown**. Do not short to P12V1. |
| SMBus slave / FRU / PMBus map | **Unknown**. Do not invent 0x50. |
| HOST_PWRGD delays vs rail windows | AMD timing **Unknown** |
| LINK_CONFIG[4:0] MI250X coding | **Unknown** |
| OEM air-heatsink height / bolster HS MPN | **Unknown** |
| PIN A3 footprint rotation 180° | **Inferred** |

---

## P48V — DO NOT ENERGIZE

| Item | Status |
|---|---|
| Dell D3000E-S1 | **Verified 12 V CRPS**. Not GPU P48V. Never mix. |
| OCP P48V window | **Verified** 44–59.5 V |
| Molex 218910-1115 catalog rating | **Verified 30 V** AC(RMS)/DC max |
| OCP 44–59.5 V into those pads | **OPEN.** Ticket **167157** / `2189100001-PS-000` |
| SuperMicro UBB cable CBL-PWEX-1280 | **Verified as a UBB 54 V cable**, not this mezz, not a closed path here |
| P48V copper pour on this PCB | **Not poured** (deliberate) |

Until ticket **167157** closes with a citable Molex rating for the 16 P48V contacts, do not apply 48 V through 218910-1115 on this board.

---

## KiCad CLI (9.0.2) — not a fab sign-off

| Check | Result | Meaning |
|---|---|---|
| Schematic ERC | **392** violations: 196 `label_dangling` + 196 `hier_label_mismatch` | Expected: hierarchical labels on a named-net stub, not a wired schematic. |
| PCB DRC | **16** `lib_footprint_mismatch` (one per 218910-1115; pads carry nets the library does not) + **499** unconnected items | Expected: no tracks. Do not “Update PCB from Schematic”. |
| Previews | `docs/previews/*-top.png` `*.svg` `*.pdf`; 3D `*-top-render.png`; layer SVG in `docs/kicad_reports/` | Visual only. |


---

## Blockers before an order (all still open)

1. **Molex 30 V catalog vs OCP 44–59.5 V** — ticket **167157** / `2189100001-PS-000` not in hand.
2. **AMD overlay** (TEST*, dual-GCD PE, xGMI S1–S7, SMBus) still Unknown.
3. **No copper**: no PCIe / SerDes / clock routing; no P48V pour.
4. **Seats 2–7** need an on-board PCIe switch — **MPN Unknown**. X11DPH-T has too few lanes for 8× MI250X.
5. **No CEM / host-connector MPN** in the host region (deliberate).
6. **218910-1115 BGA/mezz attach** is a factory process, not a default PCBWay stack.
7. **PIN A3 orientation** still Inferred (180°).
8. **No 48 V harness**, no HOST_PWRGD sequencer, no REFCLK generator.
9. Cooling HS that mates the OAM bolster is Unknown. Do not clamp a custom cold plate on bare die.
10. Do **not** reuse the old **220 × 120 mm** qty-5 MFC quote.

**Cannot PCBWay. Cannot energize OAMs. Cannot replace AS-4124GQ-TNMI with this stub today.**
