# Rev3 — 8-seat MI250X PCBWay POWER+MECH first article

**DO NOT ENERGIZE P48V** until Molex 1.2 A/contact at 48–59.5 V (2 oz) is written (ticket 167157).  
**Do not upload from this agent.** Eli uploads `fab/Rev3_8Seat_PCBWay_12L_492x372_qty5_gerbers.zip` if he accepts it.

Chamber B **OAM chassis PCB** only. Compatible with Eli’s 2026-08-21 sheet; does **not** shop GPUs, 48 V shelves, or cooling.

- Pin names: OCP generic **v1.0**. **v1.x only.** r2.0 is UNUSABLE. P3V3 = Conn0 C1/C2.
- **8 electrically designed seats**. Populate **2** (seats 0–1) then **4** (0–3) then **8** — **no respin**.
- 16× **Molex 218910-1115**. Outline **492 × 372 mm**. **12-layer 2.0 mm** stuffed-switch **target**.
- **Full-width capable chassis:** 16 named x16 PE buses (`PE_Sn_GCD0_x16` + `PE_Sn_GCD1_x16`) toward four **PM8536B-FEI DNP** courtyards (SW0–SW3). GCD1 is named-only (not S1–S7). **This host (X11DPH-T, ~80 lanes) cannot light 256 DS.** **No CEM invented. No AMD overlay invented.** Do not swap the host board.
- **P48V:** Anderson **6325G1** + 2× **1382** → star spines (not a 100 A flood) → per-seat **0476015.MR** 15 A → local Conn0 pours.
- **P12V1 / P3V3:** **THL 40-4812WI** (40 W from 48 V) + **OKI-78SR-3.3/1.5-W36-C** (4.95 W from P12V1). No GPU VRM.
- TEST*/RFU/DO_NOT_USE **unmapped**. PVREF **not driven**. S1–S7 **no net** (no xGMI).
- Silk keeps **DO NOT ENERGIZE P48V**. “DO NOT FABRICATE” is dropped: POWER+MECH copper DRC errors are clean enough to submit. PE stays unrouted (DNP switches).

| File | What |
|---|---|
| `fab/Rev3_8Seat_PCBWay_12L_492x372_qty5_gerbers.zip` | Gerbers, drill, IPC-356, PnP, FAB_NOTES, BOM |
| `docs/STATUS.md` | What Eli can upload vs what stays DNP |
| `docs/FAB_NOTES.md` | Stackup, skip-pin NC, do-not-energize |
| `docs/PCBWAY.md` | Guest quotes 2026-08-21. Agent does not upload. |
| `BOM.md` | PCB bill with buyable MPNs |
| `docs/previews/` | Top SVG/PNG |

```
python3 Generated_Project/Rev3_8Seat_PCBWay_Chassis_v1/tools/generate_from_v10_pinmap.py
python3 Generated_Project/Rev3_8Seat_PCBWay_Chassis_v1/tools/export_fab.py
```

Do not “Update PCB from Schematic”. Do not stuff PM8536 on this article. Do not upload to PCBWay from this tree. POWER+MECH still cannot run 8 live GPUs without maps.
