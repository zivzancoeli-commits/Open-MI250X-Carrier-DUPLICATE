# STATUS — Rev3 8-seat PCBWay chassis PCB

**Tree:** `Generated_Project/Rev3_8Seat_PCBWay_Chassis_v1/`  
**Date:** 2026-08-21  
**Pin map:** `22_Pinmap_Research/extracted/OAM_v1.0_OCP_Generic_Pin_Map.csv` (1376 named pads). xlsx in `22_Pinmap_Research/downloads/` wins on mismatch; this generator consumes the CSV (P3V3 = Conn0 C1/C2 checked). **v1.x only.** r2.0 is UNUSABLE.

**DO NOT FABRICATE. DO NOT ENERGIZE P48V** until AMD overlay + Molex 1.2 A/contact follow-up are written. Not a PCBWay upload.

Labels: **Verified** / **Inferred** / **Unknown**. Do not treat Inferred as a pin assignment.

This tree is the **Chamber B OAM chassis PCB only**. It must stay compatible with Eli’s 2026-08-21 sheet. It does **not** shop GPUs, 48 V shelves, cooling loops, or a whole-system cart.

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
| 8× MI250X when modules exist | 8 electrically designed seats | **Fits the chassis intent** at **x8 per GCD** through two DNP **PM8536B-FEI PRIMARY**. **Does not fit** 8× full-width GCD **x16** (256 DS vs 80 host Gen3). |
| SuperMicro **X11DPH-T** (3× Gen3 x16 + 4× Gen3 x8) | **Not on this PCB** | **Fits as the host.** Host-stub silk + cable keepout sized for two CPU **x16 uplinks** to SW0/SW1 + leftover 1× x16 + 4× x8. **No CEM MPN invented.** |
| 2× Xeon Gold **6230** | **Not on this PCB** | Host CPUs. Compatible as the locked host SKU. |
| **NH-D9 DX-3647** (NOT U14S) | **Not on this PCB** | **Fits the sheet.** U14S collides on dual 3647 — do not use U14S. Coolers live on the host, not here. |
| 1000 W ATX/EPS | **Not on this PCB** | **Host only.** Do not treat it as OAM P48V. |
| First stuffing **2×** MI250X (**P41933-001**) | Seats only; GPUs **do-not-order** | **Fits electrically.** Seats 0–1 are first-stuff candidates. All **8** seats already have named PE/power/clock nets so lighting 3–8 does **not** need a respin. Modules DNP until they exist. |
| Chamber A desk **mATX B550M 244×244** | **Not on this PCB** | Chamber A. Do not put it on the chassis. |
| Dell **D3000E-S1** | **Not on this PCB** | **Does not fit as GPU P48V.** It is **12 V CRPS**. Do not tie OAM P48V to it. |
| Molex **218910-1115** ×16 | **Yes** | **Fits** the OCP 5.00 mm stack. Street ~$50–$96 ea. **Do not order** from this tree. |
| **PM8536B-FEI** ×2 | Courtyard **DNP PRIMARY** | **Fits as the stuffed-switch plan.** 96-lane Gen3, 37.5 mm 1311-FCBGA, 1.0 mm pitch, ~$460–475, ~18 wk. x8 per GCD. Not stuffed. **PEX8780-AB80BI G** is a cheaper 80-lane alt in **docs only**. PM8533B-F3EI is a 2-seat alt in docs only. |
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
| P48V | Anderson **SB175** on the long edge → star + Kelvin sense → per-seat **~15 A fuse keepouts** → **local F.Cu pours** on the 16 verified Conn0 P48V pads. **Not** a 100 A flood plane. |
| Switches | **U_SW0** / **U_SW1** **PM8536B-FEI DNP PRIMARY** keepouts (x8 per GCD; SW0 seats 0–3, SW1 seats 4–7) |
| Host region | X=452–492 mm strip. Silk + cable keepout. **No CEM invented.** |

First stuffing: **2 populated modules / 6 DNP modules** is allowed. The copper/netlist already covers all eight.

---

## Verified (this stub)

| Item | Evidence |
|---|---|
| 1376 named pads, Conn0+Conn1 688 each | v1.0 CSV row count |
| P3V3 = Conn0 C1, C2 (2 pads) | v1.0 map; matches v1.5 Table 4. r2.0 (P3V3=6) UNUSABLE |
| Shared OCP rails `P48V` `P12V1` `P12V2` `P3V3` `GND` | v1.0 names on all 8. **No VRM.** P12V2 **Unknown / may be NC**. |
| P48V: 16 Conn0 pads/seat | H59 K59 H60 K60 H61 J61 K61 L61 H62 J62 K62 L62 H63 J63 H64 J64 |
| Molex 218910-1115 CSA **60 V** at OCP P48V | Written **2026-08-18** Molex engineering via Brian Park / ticket **167157**, COFC **80170713**. Eli ack **2026-08-19**. Published OCP P48V map **already satisfies Skip Pins** — do **not** add extra NC pads. |
| Connector MPN 218910-1115, hermaphroditic, 5.00 mm | Farnell 2189101115; OCP v1.5 §5/§6.2 |
| Module PCB 102×165; KOZ 103×166; M3.5 φ3.9 | OCP v1.5 Fig 2 / Fig 14 |
| PM8536B-FEI package | Microchip PFX: 96-lane Gen3, **1311-ball 37.5×37.5 mm FCBGA, 1.0 mm pitch**. PCBWay can assemble 1.0 mm without HDI. ~$460–475, ~18 wk. PRIMARY DNP. |
| X11DPH-T lane budget | SuperMicro: 3× Gen3 x16 + 4× Gen3 x8 = 80 Gen3 lanes |
| HOST_PWRGD | OCP: Power Enable when rails in spec. ≥100 ms after MODULE_PWRGD (v1.5). |
| PCBWay guest quotes 2026-08-21, 492×372, qty 5, ENIG, 2 oz outer / 1 oz inner (12L/16L) | See `PCBWAY.md`. **Prefer 12L 2.0 mm stuffed-switch: PCB $2237.90 + DHL $68.43 = $2306.33**, 14–15 days (two PM8536 DNP). **Prefer 8L 2.0 mm DNP-switch: $832.74 + $68.43**. Caveat: quotes are **6/6 mil + 0.3 mm hole**; 1.0 mm 1311-ball escape will cost more. SMT 16× 688-ball Unknown ($88 floor). **Do not upload.** |

### Pad accounting (one 688+688 map; PCB instantiates it eight times)

| Class | Pads / map | All 8 seats |
|---|---:|---|
| `power_shared` | 728 | named `P48V`/`P12V1`/`P12V2`/`P3V3`/`GND` |
| `pcie_stub` | 64 | hierarchical labels toward DNP PM8536 PRIMARY (x8/GCD). **No CEM.** |
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
| x8 per GCD on the v1.0 16-lane PE bus | 8× running plan vs 80 host Gen3. Each GCD has its own Gen4 x16 (AMD + Hot Chips 34); host trains Gen3. Do not attempt x16-per-GCD (256 DS). | AMD overlay / PE_BIF default |
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

## KiCad CLI — not a fab sign-off

See `docs/kicad_reports/` (KiCad **9.0.9**, 2026-08-21). Hierarchical labels on a named-net stub produce expected ERC dangling/mismatch. DRC footprint-mismatch and unconnected items (no PE tracks; fused P48V islands; DNP PRIMARY switches) are expected. Do not “Update PCB from Schematic”.

---

## Blockers before an order (still open)

1. **Molex 1.2 A/contact at 48–59.5 V (2 oz)** — ticket **167157** current follow-up not in hand. Silk stays DO NOT ENERGIZE.
2. **AMD overlay** (TEST*, dual-GCD PE, xGMI S1–S7, SMBus) still Unknown.
3. **No PE / SerDes / clock tracks** yet — nets and keepouts only.
4. **PM8536B-FEI not purchased / not stuffed** (two DNP PRIMARY courtyards). 8× running needs them. PEX8780 is docs-only cheaper 80-lane alt.
5. **No CEM / host-connector MPN** in the host region (deliberate).
6. **218910-1115 BGA/mezz attach** is a factory process, not a default PCBWay stack. SMT of 16× 688-ball is Unknown.
7. **PIN A3 orientation** still Inferred (180°).
8. **No 48 V harness** on this BOM, no HOST_PWRGD sequencer, no REFCLK generator.
9. Do **not** reuse the old **220 × 120 mm** qty-5 MFC quote.
10. Guest quotes used **6/6 mil + 0.3 mm hole**; a 1.0 mm-pitch 1311-ball escape likely needs finer rules and will cost more.

**Do not upload to PCBWay. Do not energize OAMs.**
