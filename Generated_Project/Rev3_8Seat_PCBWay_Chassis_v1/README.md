# Rev3 — 8-seat MI250X PCBWay chassis (NOT fab-ready)

**DO NOT FABRICATE. DO NOT ENERGIZE P48V** until AMD overlay + Molex 1.2 A/contact follow-up are written. Not an order. Not a UBB.

Chamber B **OAM chassis PCB** only. Compatible with Eli’s 2026-08-21 sheet; does **not** shop GPUs, 48 V shelves, or cooling.

- Pin names: OCP generic **v1.0**. **v1.x only.** r2.0 is UNUSABLE. P3V3 = Conn0 C1/C2.
- **8 electrically designed seats** (first stuffing may be 2 modules / 6 DNP — **no respin** for the other six).
- 16× **Molex 218910-1115**. Outline **492 × 372 mm**. Generated **12-layer 2.0 mm**. **8L 2.0 mm is likely if the PEX8780 1156 is stuffed.**
- All 8: named `P48V`/`P12V1`/`P3V3`/`GND`, named PE toward one **PEX8780-AB80BI G CANDIDATE DNP** (8× x8 Gen3 + one x16 uplink). Per-seat REFCLK/PERST#/HOST_PWRGD. **No second switch MPN.**
- Host stub: silk + keepout toward **X11DPH-T** (3× Gen3 x16 + 4× Gen3 x8). **One CPU x16** = switch uplink. **No CEM invented.**
- **SB175** + local P48V pours + ~15 A fuse keepouts. **Not** a 100 A flood. **Not** Dell D3000E-S1 (12 V).
- TEST*/RFU/DO_NOT_USE **unmapped**. PVREF **not driven**. S1–S7 **no net** (no xGMI).
- X11DPH-T, NH-D9 DX-3647, B550M, GPUs, Mean Well: **NOT on this PCB**.

| File | What |
|---|---|
| `docs/STATUS.md` | Compatibility matrix vs the sheet. Verified / Inferred / Unknown. |
| `docs/PCBWAY.md` | Guest quotes 2026-08-21. 8L likely if PEX8780 stuffed. Do not upload. |
| `docs/LAYER_STACK.md` | 8L likely if stuffed; generated 12L. |
| `BOM.md` | PCB bill only. 16× 218910-1115. No GPU/PSU/cooling lines. |
| `MI250X_8OAM_PCBWay_Chassis_Stub.kicad_pro` | KiCad 9 project |
| `docs/kicad_reports/` | ERC + DRC + layer SVG |
| `docs/previews/` | PCB top PNG/SVG |

```
python3 Generated_Project/Rev3_8Seat_PCBWay_Chassis_v1/tools/generate_from_v10_pinmap.py
```

Do not “Update PCB from Schematic”. Do not upload to PCBWay.
