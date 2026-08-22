# BOM — Rev3 8-seat PCBWay chassis PCB

**DO NOT FABRICATE.** This is the **PCB bill only**. It is not a system shopping list, not a GPU order, not a 48 V shelf, and not a cooling loop.

**Verified connector MPN on this board: Molex 218910-1115 × 16.**  
**Host SuperMicro X11DPH-T is NOT on this PCB.**  
**GPUs (P41933-001) are do-not-order on the sheet and are NOT on this BOM.**  
**Do not add Mean Well / cold-plate / GPU line items here.**

| Qty | Ref | MPN / value | Description | Status | Notes |
|---:|---|---|---|---|---|
| 16 | J0_Conn0, J0_Conn1 … J7_Conn0, J7_Conn1 | **Molex 218910-1115** (2189101115) | Mirror Mezz Pro, 688 contact, hermaphroditic, 5.00 mm mated height | **Verified** OCP v1.5 §5/§6.2 + Farnell | Only stuffed connector MPN. Street **~$50–$96 ea**. **Do not order** from this tree. Voltage: CSA 60 V written 2026-08-18 at OCP P48V (COFC 80170713); **1.2 A/contact at 48–59.5 V still OPEN**. No extra skip/void NC pads. Factory pack typically reel; BGA/mezz attach is not a default PCBWay process. |
| 1 | J_SB175 | Anderson **SB175** 2-pole | 175 A / 600 V board-entry landing, 2 AWG, Kelvin pads | **Verified** family rating (DS-SB175). Geometry planning from 2-pole envelope **53.1×35.4 mm**, holes **Ø6.6 / 28.6 mm** | Housing+contacts are the chassis inlet, not a 48 V PSU. **Do not tie to D3000E-S1 (12 V).** |
| 8 | F0–F7 | **~15 A fuse keepout** | Per-seat P48V fuse | **Keepout only** | **MPN Unknown.** Not a buy line. |
| 0 | U_SW | **PEX8780-AB80BI G** | 80-lane / 20-port Gen3, 35×35 mm 1156-FCBGA | **CANDIDATE DNP** | Qty 1 courtyard. Street **~$309–$359** (OMO/Digi-Key tray). Topology **8× x8 + one x16 uplink**, not 8× x16. **Do not stuff.** PCBWay 1156 assembly **Unknown**. Do not invent a second MPN (PEX8796 / PEX88096 / PM40100 not placed). |
| 32 | H01–H74 (H{seat}{1–4}) | NPTH φ 3.9 mm, 8 mm MIN land | OAM Fig 2 M3.5 holes | **Verified** geometry | Screw length / bolster **Unknown**. Not a fastener SKU here. |
| 1 | PCB | **12-layer generated**, 492 × 372 mm, 2.0 mm, 2 oz outer / 1 oz inner planning | FR4 chassis, eight 103×166 mm KOZ + host-stub strip | **Inferred** outline | **Not a fab gerber.** **8L 2.0 mm is likely if PEX8780 stuffed** (guest qty-5 **$832.74 + $68.43 DHL**). **Do not upload.** |

## Explicitly not on this PCB (sheet-compatible, do not buy onto the carrier)

| Item | Why it is absent |
|---|---|
| SuperMicro **X11DPH-T**, 2× Gold **6230**, **NH-D9 DX-3647** | Host Chamber B. **Not** this PCB. U14S is the wrong cooler (collides). |
| 1000 W ATX/EPS | **Host only.** Not OAM P48V. |
| Chamber A **B550M 244×244** | Desk. Not this PCB. |
| HPE **P41933-001** / any MI250X | Do-not-order on the sheet. Seats exist; modules are not a chassis line. |
| Dell **D3000E-S1** | **12 V CRPS.** Must not feed OAM P48V. |
| Mean Well RCP-2000 / RKP-1UT / any 48 V shelf | **No PSU shopping** on this BOM. SB175 is the inlet only. |
| SuperMicro **CBL-PWEX-1280** / **PWS-3K06G-2R** | Existence proof elsewhere, not a buy here. |
| CEM x16 / SlimSAS / MCIO / retimer | **Not invented.** |
| GPU multiphase VRM / cold plate | Forbidden on this PCB. Module has 48 V core VRMs. |
| MODULE_ID / LINK_CONFIG 1k pulldowns | OCP rule exists; deferred until AMD overlay. |
