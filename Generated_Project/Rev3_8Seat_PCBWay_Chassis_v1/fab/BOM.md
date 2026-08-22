# BOM — Rev3 8-seat PCBWay chassis PCB (POWER+MECH first article)

**PCB bill only.** Not a GPU order, not a 48 V shelf, not a cooling loop.  
**DO NOT ENERGIZE P48V** until Molex 1.2 A/contact at 48–59.5 V is written (ticket 167157).  
**Do not upload from this tree** — Eli uploads the `fab/` zip if he accepts it.

Host SuperMicro X11DPH-T is **not** on this PCB. GPUs (P41933-001) are **do-not-order**.

| Qty | Ref | MPN | Description | Status | Notes |
|---:|---|---|---|---|---|
| 16 | J0_Conn0 … J7_Conn1 | **Molex 218910-1115** | Mirror Mezz Pro, 688 contact, 5.00 mm | **Buy** | CSA 60 V at OCP P48V (COFC 80170713). 1.2 A/contact OPEN. Skip-pin = published map. SMT of 16× 688-ball is a factory process. |
| 1 | J_SB175 | Anderson **6325G1** | SB175 2-pole gray housing | **Buy** | 175 A / 600 V. Cable-side housing. |
| 2 | — | Anderson **1382** | SB175 1/0 AWG silver contact | **Buy** | Pair with 6325G1. Not D3000E-S1. |
| 8 | F0–F7 | Littelfuse **0476015.MR** | Nano2 15 A 125 VDC | **Buy** | Per-seat P48V. Land = KiCad `Fuse_Littelfuse-NANO2-451_453`. |
| 1 | F_P12 | Littelfuse **0476002.MR** | Nano2 2 A 125 VDC | **Buy** | THL40 input. Same land. |
| 1 | U_P12V1 | TRACO **THL 40-4812WI** | 18–75 Vin, 12 V / 3.35 A / 40 W isolated 1×1 | **Buy** | OCP P12V1 ≤50 W; this MPN is the 40 W first-article cap. Returns bonded to board GND. |
| 1 | U_P3V3 | Murata **OKI-78SR-3.3/1.5-W36-C** | 7–36 Vin, 3.3 V / 1.5 A / 4.95 W SIP | **Buy** | From P12V1. No GPU VRM. |
| 0 | U_SW0, U_SW1 | **PM8536B-FEI** | 96-lane Gen3 1311-FCBGA 1.0 mm | **DNP** | Courtyard only. Ball map not public. Do not stuff this article. |
| 32 | H0{1–4}…H7{1–4} | (NPTH φ3.9 mm) | OAM Fig 2 M3.5 | **Fab** | Not a fastener SKU. |
| 1 | PCB | 12L 492×372 mm 2.0 mm ENIG 2 oz/1 oz green/white | FR-4 chassis | **Fab zip** | Guest qty-5 **$2237.90 + $68.43 DHL**. See `fab/`. |

## Explicitly not on this PCB

| Item | Why it is absent |
|---|---|
| SuperMicro **X11DPH-T**, 2× Gold **6230**, **NH-D9 DX-3647** | Host Chamber B. Not this PCB. |
| 1000 W ATX/EPS | Host only. Not OAM P48V. |
| HPE **P41933-001** / any MI250X | Do-not-order. Seats exist; modules are not a chassis line. |
| Dell **D3000E-S1** | 12 V CRPS. Must not feed OAM P48V. |
| Mean Well / any 48 V shelf | No PSU shopping. SB175 is the inlet. |
| CEM x16 / SlimSAS / MCIO / retimer | Not invented (no public footprint chosen). |
| GPU multiphase VRM / cold plate | Forbidden. |
