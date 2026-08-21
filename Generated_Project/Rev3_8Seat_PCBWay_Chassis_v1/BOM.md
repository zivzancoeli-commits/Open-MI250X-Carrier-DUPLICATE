# BOM — Rev3 8-seat PCBWay chassis PCB

**DO NOT FABRICATE.** This is the PCB bill only. It is not a system shopping list and not a SuperMicro tray.

**Verified connector MPN on this board: Molex 218910-1115 × 16.**  
**Host SuperMicro X11DPH-T is NOT on this PCB** (system BOM / chassis, if bought at all).

| Qty | Ref | MPN / value | Description | Status | Notes |
|---:|---|---|---|---|---|
| 16 | J0_Conn0, J0_Conn1 … J7_Conn0, J7_Conn1 | **Molex 218910-1115** (2189101115) | Mirror Mezz Pro, 688 contact, hermaphroditic, 5.00 mm mated height | **Verified** OCP v1.5 §5/§6.2 + Farnell “Mates With 2189101115” | Only connector MPN on this board. Do not buy 218916 unless a non-5 mm stack is documented. Voltage vs P48V **OPEN** (catalog 30 V vs OCP 44–59.5 V, ticket **167157**). Factory pack is typically reel; BGA/mezz attach is not a default PCBWay process. |
| 32 | H01–H74 (H{seat}{1–4}) | NPTH φ 3.9 mm, 8 mm MIN land | OAM Fig 2 M3.5 holes, one set per seat | **Verified** geometry (OCP v1.5 Fig 2) | Screw **length** / bolster stack **Unknown**. Not a buyable fastener SKU here. |
| 1 | PCB | 4-layer, **492 × 372 mm**, 1.6 mm planning (1.6–2.4 mm range) | FR4 stub, eight 103×166 mm KOZ + host-stub strip | **Inferred** outline (20 mm service margin + 40 mm host region, planning) | **Not a fab gerber.** No P48V pour. No signal tracks. Fits PCBWay advanced finished multilayer 508×600 mm. |

## Explicitly not on this PCB

| Item | Why it is absent |
|---|---|
| SuperMicro **X11DPH-T** | Host motherboard. System BOM only. Not a carrier part. |
| SuperMicro **AS-4124GQ-TNMI** tray / AOM-MCM-Q-P UBB | The thing this PCB is trying to avoid buying. Not a part on this board. |
| CEM x16 edge / SlimSAS / MCIO “GPU cable” | **Not invented.** v1.0 names `PCIE_TXn`/`PCIE_RXn` only, seats 0–1, aimed at a silk REGION. |
| On-board PCIe switch | **MPN Unknown.** Required before seats 2–7 have host I/O. Do not guess Broadcom/Microchip. |
| Clock generator for `PE_REFCLK` | Stub labels on seats 0–1 only. |
| VRMs, 12 V→48 V converter | Forbidden. |
| BMC / SMBus address programming | Overlay Unknown. |
| MODULE_ID / LINK_CONFIG 1k pulldowns | OCP rule exists; population deferred until AMD overlay. |
| 48 V PSU / harness / fuse | Not a PCB part. Do not energize P48V. Dell D3000E-S1 is **12 V CRPS** — do not mix. |
| MI250X OAM modules | Seats only. Modules carry the mating 218910-1115 already. |

## System items (not this board)

If a host is purchased later it is **not** stuffed onto this carrier. Pointers live under `20_System_BOM/` in the repo. Buying a host does not close ticket 167157 and does not make this KiCad PCBWay-ready.
