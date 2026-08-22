# STATUS — Rev3 8-seat PCBWay chassis PCB

**Tree:** `Generated_Project/Rev3_8Seat_PCBWay_Chassis_v1/`  
**Date:** 2026-08-22  
**Pin map:** `22_Pinmap_Research/extracted/OAM_v1.0_OCP_Generic_Pin_Map.csv` (1376 named pads). xlsx in `22_Pinmap_Research/downloads/` wins on mismatch; this generator consumes the CSV (P3V3 = Conn0 C1/C2 checked). **v1.x only.** r2.0 is UNUSABLE.

**DO NOT ENERGIZE P48V.** POWER+MECH first-article Gerbers are in `fab/`. **Do not upload from this agent.** Eli uploads if he accepts the zip.

Labels: **Verified** / **Inferred** / **Unknown**. Do not treat Inferred as a pin assignment.

This tree is the **Chamber B OAM chassis PCB only** (8-seat OAM carrier). It is **not** a motherboard. Do **not** swap or design an X11/Xeon host board. It must stay compatible with Eli’s 2026-08-21 sheet. It does **not** shop GPUs, 48 V shelves, cooling loops, or a whole-system cart.

**Architecture target:** 8-seat **full-width capable** (16× x16 PE names, four DNP switch courtyards). **First article remains POWER+MECH:** this zip still cannot run 8 live GPUs without AMD overlay + PM8536 ball maps. Host **X11DPH-T** stays; it cannot light 256 downstream lanes.

Regenerate (do not hand-edit pad nets):

```
python3 Generated_Project/Rev3_8Seat_PCBWay_Chassis_v1/tools/generate_from_v10_pinmap.py
```

---

## Compatibility vs the sheet

| Sheet item | On this PCB? | Fits / does not |
|---|---|---|
| 8× OAM KOZ 103×166 mm, 16× Molex **218910-1115**, 32× M3.5 NPTH φ3.9 mm | **Yes** (this board) | **Fits.** 4×2 tiling **412×332 mm** (Inferred) on outline **492×372 mm**. |
| Board in Chamber B next to E-ATX **304.8×330.2 mm** | Mechanical neighbour, not a part | **Fits as a neighbour.** Chassis PCB 492×372 can sit in Chamber B beside the host. Coolers are **not** on this PCB. |
| 8× MI250X when modules exist | 8 electrically designed seats | **Chassis can SIT and be WIRED** for 8× full-width (16 named x16 PE buses, 4× **PM8536B-FEI DNP**). **This host cannot LIGHT** 8× full-width: X11DPH-T has **~80** Gen3 lanes vs **256** downstream. |
| SuperMicro **X11DPH-T** (3× Gen3 x16 + 4× Gen3 x8) | **Not on this PCB** | **Fits as the host.** Host-stub silk + cable keepout: four named **US x16** toward SW0–SW3. Host has 3× x16 + 4× x8 (**~80** lanes). **No CEM MPN invented.** Do not swap or design an X11/Xeon host board. |
| 2× Xeon Gold **6230** | **Not on this PCB** | Host CPUs. Compatible as the locked host SKU. |
| **NH-D9 DX-3647** (NOT U14S) | **Not on this PCB** | **Fits the sheet.** U14S collides on dual 3647 — do not use U14S. Coolers live on the host, not here. |
| 1000 W ATX/EPS | **Not on this PCB** | **Host only.** Do not treat it as OAM P48V. |
| First stuffing **2×** MI250X (**P41933-001**) | Seats only; GPUs **do-not-order** | **Fits electrically.** Populate path **2→4→8**: seats **0–1** first, then **0–3**, then all **8**. Same PCB; stuff seats/switches later. All **8** seats already have named PE/power/clock nets. Modules DNP until they exist. |
| Chamber A desk **mATX B550M 244×244** | **Not on this PCB** | Chamber A. Do not put it on the chassis. |
| Dell **D3000E-S1** | **Not on this PCB** | **Does not fit as GPU P48V.** It is **12 V CRPS**. Do not tie OAM P48V to it. |
| Molex **218910-1115** ×16 | **Yes** | **Fits** the OCP 5.00 mm stack. Street ~$50–$96 ea. **Do not order** from this tree. |
| **PM8536B-FEI** ×4 | Courtyard **DNP PRIMARY** | **Fits as the stuffed-switch plan for a full-width-capable chassis.** 96-lane Gen3, 37.5 mm 1311-FCBGA, 1.0 mm pitch, ~$460–475, ~18 wk. Four courtyards (SW0–SW3). Not stuffed. **PEX8780-AB80BI G** is a cheaper 80-lane alt in **docs only**. PM8533B-F3EI is a 2-seat alt in docs only. |
| xGMI / Infinity Fabric S1–S7 | No net | **Does not fit** (overlay Unknown). Not routed. |
| Custom cold plate / GPU HS | **Not on this PCB** | **Do not shop** onto this BOM. |

---

## What this tree is

8 electrically designed OAM seats on one **12-layer, 2.0 mm** FR-4 chassis (stuffed-switch **target**; plan 12–16L, not 4). **8L 2.0 mm is a cheaper DNP-switch option only.**

| | |
|---|---|
| Outline | **492 × 372 mm** (fits PCBWay advanced finished ML **508 × 600**) |
| 8-KOZ floor | **412 × 332 mm** = 4×2 of 103×166 mm |
| Seat grid | col pitch 103 mm, row pitch 166 mm. Row 0 (Y=20): seats **0 1 2 3**. Row 1 (Y=186): seats **4 5 6 7**. |
| Connectors | **16×** Molex **218910-1115** (2 per seat), rot 180 **Inferred** |
| Holes | **32×** M3.5 NPTH φ3.9 mm (Fig 2), 8 mm MIN land |
| Layers | **12L 2.0 mm** stuffed-switch **prefer** (guest **$2237.90 + $68.43 DHL = $2306.33**, 14–15 days). **8L 2.0 mm $832.74** is the DNP-switch / mezz+power prefer. 16L Advanced **$2937.84**. |
| P48V | Anderson **6325G1** + 2× **1382** → star + Kelvin → per-seat **0476015.MR** 15 A → **local F.Cu pours**. **Not** a 100 A flood. |
| P12V1 / P3V3 | **THL 40-4812WI** (40 W from 48 V) + **OKI-78SR-3.3/1.5-W36-C** (4.95 W from P12V1). No GPU VRM. |
| Switches | **U_SW0–U_SW3** **PM8536B-FEI DNP** courtyards (ball map not public). SW0=seats 0–1, SW1=2–3, SW2=4–5, SW3=6–7. |
| Host region | X=452–492 mm strip. Four 40 mm switch courtyards stacked in Y + cable keepout. **No CEM invented.** |
| PE names | 16 architectural x16 buses: `PE_S0_GCD0_x16`…`PE_S7_GCD1_x16`. GCD0 = Conn0 OCP PCIE pads. GCD1 = **named only** (overlay Unknown; not S1–S7). Four `PE_SWk_US_x16` keepouts. |

Populate path: **2** (seats 0–1 + SW0) → **4** (seats 0–3 + SW1) → **8** (all seats + SW2/SW3). Same copper.

---

## Verified (this named-net chassis)

| Item | Evidence |
|---|---|
| 1376 named pads, Conn0+Conn1 688 each | v1.0 CSV row count |
| P3V3 = Conn0 C1, C2 (2 pads) | v1.0 map; matches v1.5 Table 4. r2.0 (P3V3=6) UNUSABLE |
| Shared OCP rails `P48V` `P12V1` `P12V2` `P3V3` `GND` | v1.0 names on all 8. **No VRM.** P12V2 **Unknown / may be NC**. |
| P48V: 16 Conn0 pads/seat | H59 K59 H60 K60 H61 J61 K61 L61 H62 J62 K62 L62 H63 J63 H64 J64 |
| Molex 218910-1115 CSA **60 V** at OCP P48V | Written **2026-08-18** Molex engineering via Brian Park / ticket **167157**, COFC **80170713**. Eli ack **2026-08-19**. Published OCP P48V map **already satisfies Skip Pins** — do **not** add extra NC pads. |
| Connector MPN 218910-1115, hermaphroditic, 5.00 mm | Farnell 2189101115; OCP v1.5 §5/§6.2 |
| Module PCB 102×165; KOZ 103×166; M3.5 φ3.9 | OCP v1.5 Fig 2 / Fig 14 |
| PM8536B-FEI package | Microchip PFX: 96-lane Gen3, **1311-ball 37.5×37.5 mm FCBGA, 1.0 mm pitch**. PCBWay can assemble 1.0 mm without HDI. ~$460–475, ~18 wk. PRIMARY DNP ×4. |
| Lane math (not a ball map) | 8×2×x16 = **256 DS**. 2×96 = 192 — enough for 8× **x8/GCD** (128 DS + uplinks), **not** 256 DS. 4×96 = 384. Hypothesis partition: each SW 16 US + 64 DS (2 seats × 2 GCD × x16) = 80 of 96. 4×16 US = 64 host-facing vs X11DPH-T **~80**. |
| X11DPH-T lane budget | SuperMicro: 3× Gen3 x16 + 4× Gen3 x8 = **80** Gen3 lanes. 2× Gold 6230 + 64 GB DRAM + 1 TB PMem does **not** add PCIe lanes. Chassis **wired** for 8 full-width; this host **cannot light** 8 full-width. |
| HOST_PWRGD | OCP: Power Enable when rails in spec. ≥100 ms after MODULE_PWRGD (v1.5). |
| PCBWay guest quotes 2026-08-21, 492×372, qty 5, ENIG, 2 oz outer / 1 oz inner (12L/16L) | See `PCBWAY.md`. **Prefer 12L 2.0 mm stuffed-switch: PCB $2237.90 + DHL $68.43 = $2306.33**, 14–15 days (four PM8536 DNP courtyards; this article does not stuff them). **Prefer 8L 2.0 mm DNP-switch: $832.74 + $68.43**. Caveat: quotes are **6/6 mil + 0.3 mm hole**; 1.0 mm 1311-ball escape will cost more. SMT 16× 688-ball Unknown ($88 floor). **Do not upload.** |

### Pad accounting (one 688+688 map; PCB instantiates it eight times)

| Class | Pads / map | All 8 seats |
|---|---:|---|
| `power_shared` | 728 | named `P48V`/`P12V1`/`P12V2`/`P3V3`/`GND` |
| `pcie_stub` | 64 | Conn0 16-lane PCIE = `PE_Sn_GCD0_x16` toward DNP PM8536. `PE_Sn_GCD1_x16` named-only (not on these pads). **No CEM.** |
| `clock_reset` | 16 | per-seat REFCLK / PERST# / HOST_PWRGD (+ other OCP clock/reset names) |
| `mgmt_stub` | 17 | named (SMBus etc.). Overlay still Unknown. |
| `ocp_sideband` | 19 | named; ID/CONFIG resistors **not placed** |
| `module_output_do_not_drive` | 2 | PVREF. **Never drive.** |
| `serdes_named_not_routed` | 448 | **No net.** No xGMI. SERDES_7 as GCD1 PE is **Inferred**, not routed. |
| `unmapped_nc` | **59** | TEST*/RFU/DO_NOT_USE. **No net.** |

Seat 0 connector centres (match Rev2 2-seat): Conn0 **(71.5, 154.0)**, Conn1 **(71.5, 52.0)** mm.

---

## Inferred

| Item | Basis | Do not treat as |
|---|---|---|
| 8-GPU floor **412 × 332 mm** | 4×2 tiling of 103×166 mm KOZ | A Universal Baseboard drawing |
| 20 mm service margin + 40 mm host strip → **492 × 372 mm** | Planning envelope | A fab panel drawing or CEM connector |
| Footprint rotation **180°** | Fig 2 PIN A3 on +X vs candidate land A3 at x=−29.45 | Proven module↔baseboard silk until overlay-checked |
| Four 40 mm PM8536 courtyards in the 40 mm host strip | SW0–SW3 stacked in Y; 12 V brick moved south of SW3 | A stuffed BGA pinout |
| 16 named x16 PE buses (`PE_Sn_GCD0_x16` / `PE_Sn_GCD1_x16`) | Full-width chassis architecture. GCD0 = Conn0 OCP PCIE pads. GCD1 named-only. | AMD overlay / PE pin numbers / S1–S7 assignment |
| Each SW 16 US + 64 DS | Lane-count partition of a 96-lane PFX (80 of 96). **Not** a public ball map | A legal route |
| x8/GCD if only SW0+SW1 stuffed | Stuffing option on the same PCB (2×96 = 192 ≥ 128 DS + uplinks) | The architecture target (architecture is full-width capable) |
| GCD1 = Conn1 SERDES_7 | OAM v1.5 “second PE x16 may be SERDES_7” | Proven MI250X mapping |

---

## Unknown (blocking energize / overlay / order)

| Item | Status |
|---|---|
| AMD MI250X 688-pad overlay | **Unknown** (NDA) |
| Which S1–S7 are xGMI / Infinity Fabric | **Unknown**. **No net.** |
| Dual-GCD host PCIe 1×16 vs 2×8 / `PE_BIF[1:0]` | **Unknown** |
| Host connector in the silk REGION | **Unknown**. Not invented. |
| P12V2 required on 48 V MI250X | **Unknown**. Do not short to P12V1. |
| SMBus slave / FRU / PMBus map | **Unknown**. Do not invent 0x50. |
| HOST_PWRGD delays vs rail windows | AMD timing **Unknown** (OCP ≥100 ms note only) |
| LINK_CONFIG[4:0] MI250X coding | **Unknown** |
| PIN A3 footprint rotation 180° | **Inferred** |
| 1.2 A per used 218910-1115 power contact at 48–59.5 V (2 oz) | **OPEN** (ticket 167157 follow-up) |
| skip/void is NC on the same MPN | **OPEN** (same follow-up) |

---

## P48V — DO NOT ENERGIZE

| Item | Status |
|---|---|
| Dell D3000E-S1 | **Verified 12 V CRPS**. Not GPU P48V. Never mix. |
| OCP P48V window | **Verified** 44–59.5 V |
| Molex 218910-1115 catalog line | Still prints 30 V; **written CSA 60 V** at OCP P48V 2026-08-18 (COFC 80170713) |
| Skip Pins | Published OCP P48V assignment **already satisfies**; no extra NC pads |
| 1.2 A/contact at 48–59.5 V, 2 oz | **OPEN** |
| P48V copper | **Local per-seat F.Cu pours** + SB175 star. **Not** a board-wide 100 A plane |
| Off-board 48 V PSU / shelf | **Not a PCB BOM item.** Do not shop it here. |

Voltage/skip-pin is no longer a 30 V catalog brick wall. **Current-rating follow-up still blocks energize.** Keep silk **DO NOT ENERGIZE P48V**.

---

## What Eli can upload vs what stays DNP

| Eli can upload / buy onto this PCB | Stays DNP / not this zip |
|---|---|
| `fab/Rev3_8Seat_PCBWay_12L_492x372_qty5_gerbers.zip` (Gerbers, drill, IPC-356, PnP, FAB_NOTES, BOM, top preview) | **Do not upload from this agent.** Eli uploads if he accepts. |
| 12L 2.0 mm 492×372 ENIG 2 oz/1 oz green/white qty 5 — guest **$2237.90 + $68.43 DHL** | 8L DNP-switch coupon is cheaper if he never stuffs switches |
| 16× **218910-1115**, 32× M3.5 NPTH, Anderson **6325G1** + **2× 1382**, **0476015.MR** ×8, **0476002.MR**, **THL 40-4812WI**, **OKI-78SR-3.3/1.5-W36-C** | **PM8536B-FEI** ×4 (courtyard only; ball map not public) |
| Local P48V / P12V1 / P3V3 copper + GND planes + star/fuses | PE / REFCLK / PERST# **tracks** (named, not routed) |
| Silk **DO NOT ENERGIZE P48V** | Host CEM connector (keepout only; no MPN invented) |
| Skip-pin NC (TEST*/RFU/DO_NOT_USE have no net) | AMD overlay, xGMI S1–S7, PVREF drive, D3000E-S1 |

**Energize is still blocked** on Molex 1.2 A/contact (ticket 167157). First article is POWER+MECH.

---

## KiCad CLI

See `docs/kicad_reports/` (KiCad **9.0.9**). ERC dangling hierarchical labels are expected. DRC on fabricated copper: **0 errors**. Remaining warnings are `lib_footprint_mismatch` (placed pads carry nets the library copy does not), silk, and a few isolated-copper islands. Unconnected PE / REFCLK / PERST# nets are expected (four DNP switches). Do not “Update PCB from Schematic”.

---

## Still open (not a reason to withhold the zip)

1. **Molex 1.2 A/contact at 48–59.5 V (2 oz)** — silk stays DO NOT ENERGIZE.
2. **AMD overlay** still Unknown. Do not invent it.
3. **PM8536B-FEI** ×4 DNP until a public/legal ball map exists. 1.0 mm escape will need finer than **6/6 mil** and a requote.
4. **No CEM host MPN** (deliberate). X11DPH-T **~80** lanes cannot light **256** DS — do not swap the host board in this tree.
5. **218910-1115 mezz attach** is a factory process.
6. **PIN A3** rotation 180° still Inferred.
7. P12V1 first-article module is **40 W** (THL 40-4812WI) vs OCP ≤50 W.
8. GCD1 x16 pins remain **Unknown**. `PE_Sn_GCD1_x16` is a name, not a pad map. POWER+MECH still cannot run 8 live GPUs without maps.

**Do not energize OAMs. Do not stuff the DNP switches on this article.**
