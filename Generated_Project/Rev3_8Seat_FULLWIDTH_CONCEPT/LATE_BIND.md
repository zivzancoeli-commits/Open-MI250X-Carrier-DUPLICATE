# LATE BIND — what is reserved vs what a later spin must add

**DO NOT ENERGIZE P48V. First-article POWER+MECH zip remains sit-only.**  
**CONCEPT 8× full-width: DO NOT FABRICATE as live PE.**  
**Do not claim this board will work as a GPU chassis if sent to PCBWay.**

Routing **16× x16 PE** and escaping **four 1311-ball 1.0 mm BGAs** is a **copper respin**, not a silkscreen ECO. Named nets, courtyards, and comment-layer corridors do **not** become tracks when an overlay arrives.

Do **not** invent: AMD overlay pads, PM8536 balls, CEM/MCIO pinouts, r2.0 maps, S1–S7, TEST\*/RFU/DO_NOT_USE, or a host-cable MPN.

Same PCB **outline** (492×372 mm) for populate **2 → 4 → 8**. That is the only “no-respin” promise. PE / BGA / host plug are not.

Canonical CONCEPT: [CONCEPT.md](CONCEPT.md). Rev3 tree: `Generated_Project/Rev3_8Seat_PCBWay_Chassis_v1/`.

---

## Honesty: small change vs respin

| When maps arrive | Small (same outline / populate) | Respin (new copper / geometry) |
|---|---|---|
| Stuff more OAMs / F2–F7 | **Yes** — seats and fuses already on the board | |
| Assign already-named Conn0 `PCIE_*` nets | Names exist | **Tracks, vias, impedance** still a respin |
| GCD1, 16× x16, four-switch fabric | Names + DNP courtyards exist | **Escape + route 256 DS + 64 US** is a respin |
| Host connector | Keepout rectangle exists | **Footprint + pin map + routes** is a respin |
| PM8536 stuffed | 40 mm courtyards exist | **1311-ball fanout** (finer than guest **6/6 mil**, requote) is a respin |

---

## Missing doc → reserved now → later spin adds

### Overlay (AMD 688-pad)

| | |
|---|---|
| Reserved | **GCD0:** public Conn0 `PCIE_TX/RX0–15` P/N (64 pads/seat) already named `OAM{n}_PCIE_*`. Architectural bus `PE_Sn_GCD0_x16`. Seats **0–1** called out toward the host keepout. **GCD1:** names `PE_Sn_GCD1_x16` only. Conn1 has **0** `PCIE_*`. S1–S7 **no net**. |
| Later spin | Confirm GCD0 against overlay. Assign **GCD1 pads and nets**, then **route**. Do **not** guess tracks now. Do **not** assign S1–S7 / TEST\*/RFU/DO_NOT_USE here. |
| Not small | Any PE pair routing. |

### PM8536B-FEI ×4

| | |
|---|---|
| Reserved | Four **DNP** 40 mm courtyards **SW0–SW3** (already on the Rev3 board). Package table (public): 96-lane Gen3, 1311-ball 37.5 mm, 1.0 mm. Hypothesis load (not a pinout): 64 DS + 16 US per switch. |
| Later spin | Legal/public **ball map** → footprint → **escape**. Requote vs 6/6 mil guest stack. |
| Not small | BGA fanout. Courtyard ≠ footprint. |

### Host plug

| | |
|---|---|
| Reserved | Host-strip **keepout** + names `PE_S0_GCD0_x16`, `PE_S1_GCD0_x16` (first article) and `PE_SW0..3_US_x16` (CONCEPT). **No MPN.** |
| Later spin | Place a **real** connector from a cited datasheet. Still do not invent OAM↔cable maps. |
| Not small | Footprint + PE to that connector. X11DPH-T still **cannot light 256 DS**. |

### Molex 1.2 A / cooling

| | |
|---|---|
| Reserved | Silk **DO NOT ENERGIZE P48V**. Ticket **167157** OPEN. Coolers **not on this PCB**. |
| Later spin | Molex current write-up (off-board decision to energize). Cooling is **off-board** — do not shop onto the chassis BOM. |
| Not a PCB ECO | Neither item is a silkscreen fix. |

### 2 → 4 → 8 populate

| | |
|---|---|
| Reserved | Same **492×372** outline, 8 KOZ, 16× Molex, 32× M3.5 NPTH, SB175 star, per-seat `0476015.MR`. First article: seats **0–1**, F0/F1. |
| Later spin | Stuff more seats/fuses. **Still no live PE** until overlay + routes + host plug + Molex current. |

---

## Comment-layer corridors (no copper, no fake pins)

On the Rev3 PCB, **Dwgs.User / Cmts.User** only (not fab silk, not tracks):

| Corridor | Approx. box (mm) | Meaning |
|---|---|---|
| Seats 0–1 GCD0 → host keepout | (105, 138) – (452, 178) | Planning note for `PE_S0_GCD0_x16` + `PE_S1_GCD0_x16` toward the existing keepout. Conn0 Y-band. |
| Seats 0–1 GCD0 → SW0 courtyard | (105, 22) – (452, 56) | Planning note toward **U_SW0** DNP courtyard. Not a ball map. |

These boxes overlap later KOZs on purpose: they are **intent**, not a route. Inner layers named `signal_reserved` in generation meta are the same class of note — **not** escaped pairs.

---

## PCBWay

The zip in `Rev3_8Seat_PCBWay_Chassis_v1/fab/` is **POWER+MECH sit-only**. Sending it does **not** yield a working 2× or 8× GPU chassis. **Do not upload from this agent.** **DO NOT ENERGIZE.**
