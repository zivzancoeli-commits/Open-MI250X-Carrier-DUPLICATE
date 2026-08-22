# STATUS — Rev3 8-seat PCBWay chassis PCB

**Tree:** `Generated_Project/Rev3_8Seat_PCBWay_Chassis_v1/`  
**Date:** 2026-08-22  
**Pin map:** `22_Pinmap_Research/extracted/OAM_v1.0_OCP_Generic_Pin_Map.csv` (1376 named pads). xlsx in `22_Pinmap_Research/downloads/` wins on mismatch; this generator consumes the CSV (P3V3 = Conn0 C1/C2 checked). **v1.x only.** r2.0 is UNUSABLE.

**DO NOT ENERGIZE P48V.** POWER+MECH first-article Gerbers are in `fab/`. **Do not upload from this agent.** Eli uploads if he accepts the zip.

Labels: **Verified** / **Inferred** / **Unknown**. Do not treat Inferred as a pin assignment.

This tree is the **Chamber B OAM chassis PCB only** (8-seat OAM carrier). It is **not** a motherboard. Do **not** swap or design an X11/Xeon host board. It must stay compatible with Eli’s 2026-08-21 sheet. It does **not** shop GPUs, 48 V shelves, cooling loops, or a whole-system cart.

**First-article target:** seats **0–1** (2 modules) on this same 8-seat PCB. **Without an AMD overlay, “2× MI250X” on this zip means two modules can sit and at most GCD0 on each can be targeted (2 GCDs) — not 2 modules at full width (4 GCDs).** Host **X11DPH-T** (3× x16 + 4× x8): two GCD0 x16 **fit**; two full-width modules **do not**. Later-seat 8-wide names stay. POWER+MECH: still cannot run live GPUs without maps + Molex current write-up. **DO NOT ENERGIZE.**

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
| 8× MI250X when modules exist | 8 electrically designed seats | **Later-seat names kept.** Chassis can still sit/wire 8× named x16. **This host cannot LIGHT 8× full-width** (~80 vs 256 DS). Not the first-article target. |
| SuperMicro **X11DPH-T** (3× Gen3 x16 + 4× Gen3 x8) | **Not on this PCB** | **Fits as the host.** First-article keepout: **two** named x16 (`PE_S0_GCD0_x16` + `PE_S1_GCD0_x16`). Two GCD0 x16 **fit**. Two full-width modules (4× x16) **do not**. **No CEM/MCIO MPN invented.** |
| First stuffing **2×** MI250X (**P41933-001**) | Seats **0–1** | **Stated first-article target.** Two modules can **sit**. At most **GCD0** on each can be **named toward the host keepout** (2 GCDs). **Not** 2× full-width (4 GCDs). GPUs **do-not-order**. Same PCB for 4 then 8. |
| 2× Xeon Gold **6230** | **Not on this PCB** | Host CPUs. Compatible as the locked host SKU. |
| **NH-D9 DX-3647** (NOT U14S) | **Not on this PCB** | **Fits the sheet.** U14S collides on dual 3647 — do not use U14S. Coolers live on the host, not here. |
| 1000 W ATX/EPS | **Not on this PCB** | **Host only.** Do not treat it as OAM P48V. |
| Chamber A desk **mATX B550M 244×244** | **Not on this PCB** | Chamber A. Do not put it on the chassis. |
| Dell **D3000E-S1** | **Not on this PCB** | **Does not fit as GPU P48V.** It is **12 V CRPS**. Do not tie OAM P48V to it. |
| Molex **218910-1115** ×16 | **Yes** | **Fits** the OCP 5.00 mm stack. Street ~$50–$96 ea. **Do not order** from this tree. |
| **PM8536B-FEI** ×4 | Courtyard **DNP** | **Not stuffed for 2-module first article.** Kept for later 8-seat path. Ball map not public. |
| xGMI / Infinity Fabric S1–S7 | No net | **Does not fit** (overlay Unknown). Not routed. |
| Custom cold plate / GPU HS | **Not on this PCB** | **Do not shop** onto this BOM. |

---

## What 2× can and cannot do (this zip)

Hypothesis **verified** from `22_Pinmap_Research/extracted/OAM_v1.0_OCP_Generic_Pin_Map.csv` (1376 pads) + `OAM_Pin_list_Rev1.0.csv`:

| Fact | Evidence | Label |
|---|---|---|
| Conn0 `PCIE_TX/RX0–15` P/N = **64 pads**, lanes 0–15 | Generic pin map; pin list `PETp/n` + `PERp/n [15:0]` = “PCIe or equivalent **host link**”, Conn0, Required | **Verified** OCP names. Architectural name: `PE_Sn_GCD0_x16`. |
| Conn1 `PCIE_*` count | **0** | **Verified** |
| Conn1 `S7_*` = SERDES_7 reserved link, 64 pads | Pin list “SerDes Reserved Link”; interconnect “defined by Module and System integrator” | **Named, no net.** Not a legal GCD1 PE map. |
| S1–S7 | 448 SerDes pads, **no net** | **Verified** unmapped on this chassis. |

**Can (first article, seats 0–1):**

- Two OAM modules **sit** (KOZ, Molex, M3.5 NPTH, named P48V after F0/F1, P12V1, P3V3, GND).
- At most **GCD0** on each is a legal named host PE (`PE_S0_GCD0_x16`, `PE_S1_GCD0_x16`) toward the existing host keepout — **2 GCDs**, not 4.
- Those two x16 names **fit** X11DPH-T’s 3× x16 slots **as a lane budget**. No connector MPN is placed.

**Cannot:**

- 2 modules at **full width** (4 GCDs). GCD1 pins **Unknown**; not assigned to S1–S7.
- Light even the 2 GCD0 links: Molex 1.2 A/contact **OPEN**, no host cable MPN, PE **not routed**, switches **DNP**.
- Invent CEM / Molex-to-CEM / MCIO-on-carrier without a cited public footprint **and** without inventing the OAM↔MCIO map. None placed. SuperMicro CBL-MCIO is a UBB cable, not this host.
- Feed P48V from RST-5000-48 (3-phase) on a 240 V / 50 A **single-phase** wall. Off-board 48 V stays DPU-3200-48 class, not a PCB BOM item.
- Use OAM r2.0 (P3V3 = Conn0 C1/C2 only).

---

## 8× full-width CONCEPT (ideas only — DO NOT FABRICATE)

Eli asked for an **8× MI250X full-width chassis CONCEPT** to build ideas on. It is **not** this zip, **not** a new CPU board, and **not** a live PE design.

Canonical doc: [`Generated_Project/Rev3_8Seat_FULLWIDTH_CONCEPT/CONCEPT.md`](../../Rev3_8Seat_FULLWIDTH_CONCEPT/CONCEPT.md) (also `docs/CONCEPT_8x_FULL_WIDTH.md`).

| | |
|---|---|
| What | 8 seats, 16 named x16 PE, four DNP PM8536 courtyards already on this board, xGMI as **boxes + port names** (`XGMI_Sn_P*`) only |
| Host | Still **X11DPH-T** (~80 lanes). **This CONCEPT cannot light 8× full-width on that host** (256 DS). 4× named US x16 = 64 **fit as an uplink budget only**. |
| Do not | Invent overlay pads, PM8536 balls, CEM/MCIO, r2.0, S1–S7, TEST\*/RFU/DO_NOT_USE, or a cable MPN |
| Silk / comments | CONCEPT / DO NOT FABRICATE on **Cmts.User** (not fab silk). **Do not claim DRC-clean live PE.** **DO NOT ENERGIZE.** |

Lane arithmetic (not a pinout): 256 DS + 64 US vs 4×96 = 384. Each SW hypothesis: 2 seats × 2 GCD × x16 DS + one x16 US.

---

## What this tree is

8 electrically designed OAM seats on one **12-layer, 2.0 mm** FR-4 chassis. **First article = seats 0–1.** Later 4- and 8-seat names stay on the same copper.

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
| Switches | **U_SW0–U_SW3** **PM8536B-FEI DNP** (later path; **not** stuffed for 2-module first article). |
| Host region | X=452–492 mm strip. First-article silk: **two** x16 names toward keepout. **No CEM/MCIO invented.** |
| PE names | First article: `PE_S0_GCD0_x16` + `PE_S1_GCD0_x16`. Later seats keep `PE_S2…S7_GCD0/GCD1_x16`. GCD1 = **named only**. |

Populate path: **2** (seats 0–1, no stuffed switch) → **4** (seats 0–3) → **8** (all seats + SW0–SW3). Same copper.

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
| Conn0 host PE | 64 `PCIE_*` pads, lanes 0–15. Pin list: PETp/n + PERp/n “PCIe or equivalent host link”. **Only legal named host PE.** |
| Conn1 PCIE | **0** pads. S7_* = SERDES_7 reserved, **no net**. |
| X11DPH-T lane budget | SuperMicro: 3× Gen3 x16 + 4× Gen3 x8 = **80** Gen3 lanes. Two GCD0 x16 **fit**. Two full-width modules (4× x16) **do not**. DRAM/PMem does **not** add lanes. |
| HOST_PWRGD | OCP: Power Enable when rails in spec. ≥100 ms after MODULE_PWRGD (v1.5). |
| PCBWay guest quotes 2026-08-21, 492×372, qty 5, ENIG, 2 oz outer / 1 oz inner (12L/16L) | See `PCBWAY.md`. **Prefer 12L 2.0 mm stuffed-switch: PCB $2237.90 + DHL $68.43 = $2306.33**, 14–15 days (four PM8536 DNP courtyards; this article does not stuff them). **Prefer 8L 2.0 mm DNP-switch: $832.74 + $68.43**. Caveat: quotes are **6/6 mil + 0.3 mm hole**; 1.0 mm 1311-ball escape will cost more. SMT 16× 688-ball Unknown ($88 floor). **Do not upload.** |

### Pad accounting (one 688+688 map; PCB instantiates it eight times)

| Class | Pads / map | All 8 seats |
|---|---:|---|
| `power_shared` | 728 | named `P48V`/`P12V1`/`P12V2`/`P3V3`/`GND` |
| `pcie_stub` | 64 | Conn0 16-lane PCIE = `PE_Sn_GCD0_x16`. First article: seats 0–1 toward host keepout. GCD1 named-only. **No CEM.** |
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
| Calling Conn0 PCIE “GCD0” | OCP host-link name + dual-GCD public fact; overlay still Unknown | AMD pin assignment |
| First-article host path = two Conn0 x16 toward keepout | Lane budget vs X11DPH-T 3× x16 | A CEM/MCIO cable or PE-to-slot map |
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
| Off-board 48 V PSU / shelf | **Not a PCB BOM item.** 240 V / 50 A **single-phase** wall class (DPU-3200-48 class). **Not** RST-5000-48 (3-phase). First populate: seats 0–1 / F0–F1 only. |

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

See `docs/kicad_reports/` (KiCad **9.0.9**). ERC dangling hierarchical labels are expected. DRC on fabricated copper: **0 errors**, **38** warnings (lib footprint mismatch, leftover silk at SB175, isolated copper). Unconnected PE / REFCLK / PERST# nets are expected (four DNP switches). Do not “Update PCB from Schematic”.

---

## Still open (not a reason to withhold the zip)

1. **Molex 1.2 A/contact at 48–59.5 V (2 oz)** — silk stays DO NOT ENERGIZE.
2. **AMD overlay** still Unknown. Do not invent it.
3. **PM8536B-FEI** ×4 DNP until a public/legal ball map exists. 1.0 mm escape will need finer than **6/6 mil** and a requote.
4. **No CEM / MCIO host MPN** (deliberate). Two GCD0 x16 fit the host; two full-width modules do not.
5. **218910-1115 mezz attach** is a factory process.
6. **PIN A3** rotation 180° still Inferred.
7. P12V1 first-article module is **40 W** (THL 40-4812WI) vs OCP ≤50 W.
8. GCD1 x16 pins remain **Unknown**. `PE_Sn_GCD1_x16` is a name, not a pad map. First article cannot run 2 live GPUs without maps + Molex current.

**Do not energize OAMs. Do not stuff the DNP switches on this article.**
