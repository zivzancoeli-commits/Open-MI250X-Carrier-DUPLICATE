# Rev3 — 8-seat chassis, 2-module first article (POWER+MECH)

**DO NOT ENERGIZE P48V** until Molex 1.2 A/contact at 48–59.5 V (2 oz) is written (ticket 167157).  
**Do not upload from this agent.** Eli uploads `fab/Rev3_8Seat_PCBWay_12L_492x372_qty5_gerbers.zip` if he accepts it.

Chamber B **OAM chassis PCB** only. Not a motherboard. Do not swap X11DPH-T.

- **First-article target: seats 0–1.** Without overlay, 2× MI250X = two modules **sit** and at most **GCD0** on each can be targeted (**2 GCDs**). **Not** 2× full-width (**4 GCDs**).
- Legal host PE today: Conn0 OCP `PCIE_*` = `PE_S0_GCD0_x16` + `PE_S1_GCD0_x16` toward the host keepout. GCD1 named-only. Not S1–S7. Conn1 has **0** `PCIE_*`.
- Host X11DPH-T: two GCD0 x16 **fit**; two full-width modules **do not**. **No CEM/MCIO MPN invented.**
- Same PCB populate **2 → 4 → 8**. Later-seat x16 names + SW0–SW3 DNP kept. Do not stuff switches this article.
- Pin names: OCP generic **v1.0**. **v1.x only.** r2.0 is UNUSABLE. P3V3 = Conn0 C1/C2.
- **P48V:** Anderson **6325G1** + 2× **1382** → star spines (not a 100 A flood) → per-seat **0476015.MR** 15 A. First populate F0/F1. Off-board 48 V: 240 V / 50 A single-phase class — **not** RST-5000-48 (3-phase).
- **P12V1 / P3V3:** **THL 40-4812WI** (40 W from 48 V) + **OKI-78SR-3.3/1.5-W36-C** (4.95 W from P12V1). No GPU VRM.
- TEST*/RFU/DO_NOT_USE **unmapped**. PVREF **not driven**. S1–S7 **no net**.
- Silk keeps **DO NOT ENERGIZE P48V**. PE stays unrouted (DNP switches).

| File | What |
|---|---|
| `fab/Rev3_8Seat_PCBWay_12L_492x372_qty5_gerbers.zip` | Gerbers, drill, IPC-356, PnP, FAB_NOTES, BOM |
| `docs/STATUS.md` | What Eli can upload vs what stays DNP |
| `docs/HUNT_MOLEX_PLUG_COOL.md` | Research: Molex 1.2 A @ 48–59.5 V, 218910→CEM path, MI250X cooler FRU — all **not found** |
| `docs/CONCEPT_8x_FULL_WIDTH.md` | Pointer to 8× full-width **CONCEPT** (ideas only) |
| `docs/LATE_BIND.md` | Pointer: reserved vs later-spin (**respin**, not silk ECO) |
| [`../Rev3_8Seat_FULLWIDTH_CONCEPT/LATE_BIND.md`](../Rev3_8Seat_FULLWIDTH_CONCEPT/LATE_BIND.md) | Late-bind table. **DO NOT FABRICATE** live PE. |
| [`../Rev3_8Seat_FULLWIDTH_CONCEPT/CONCEPT.md`](../Rev3_8Seat_FULLWIDTH_CONCEPT/CONCEPT.md) | 8× full-width fabric sketch. **DO NOT FABRICATE.** X11DPH-T cannot light 256 DS. |
| `docs/FAB_NOTES.md` | Stackup, skip-pin NC, do-not-energize |
| `docs/PCBWAY.md` | Guest quotes 2026-08-21. Agent does not upload. |
| `BOM.md` | PCB bill with buyable MPNs |
| `docs/previews/` | Top SVG/PNG |

```
python3 Generated_Project/Rev3_8Seat_PCBWay_Chassis_v1/tools/generate_from_v10_pinmap.py
python3 Generated_Project/Rev3_8Seat_PCBWay_Chassis_v1/tools/export_fab.py
```

Do not “Update PCB from Schematic”. Do not stuff PM8536 on this article. Do not upload to PCBWay from this tree. First article still cannot run 2 live GPUs without maps. **This zip will not work as a live GPU chassis if sent to PCBWay.**

**8× full-width CONCEPT** (sibling folder): ideas only. **DO NOT FABRICATE** as live PE. **DO NOT ENERGIZE.** Host stays X11DPH-T and **cannot light 8× full-width**. Routing 16× x16 + four 1311-ball escapes is a **respin** (`LATE_BIND.md`).
