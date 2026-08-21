# Rev3 — 8-seat MI250X PCBWay chassis stub (NOT fab-ready)

**DO NOT FABRICATE. DO NOT ENERGIZE P48V.** Not an order. Not a UBB. Title block on every sheet says the same.

Carrier / UBB-like **PCB** (this tree), not the SendCutSend metal case. 8 identical OAM seats on one board; populate seats 0–1 now, 2–7 later.

- Pin names: OCP generic **v1.0** (`22_Pinmap_Research/extracted/OAM_v1.0_OCP_Generic_Pin_Map.csv`). xlsx in `downloads/` wins on mismatch. **v1.x only.** r2.0 is UNUSABLE.
- 16× **Molex 218910-1115**. 4-layer FR-4. Outline **492 × 372 mm**.
- 4×2 of **103 × 166 mm** KOZ = **412 × 332 mm** (INFERRED tiling, not a UBB drawing) + 20 mm margin + 40 mm host-stub strip.
- Seats 0–1: named host PCIe nets toward a documented HOST CONNECTOR REGION. **No CEM cable invented.**
- Seats 2–7: mechanical + power pads only. Silk: `needs on-board PCIe switch — MPN Unknown`.
- TEST*/RFU/DO_NOT_USE **unmapped**. PVREF **not driven**. S1–S7 **not routed** between OAMs.
- Host SuperMicro **X11DPH-T is NOT on this PCB**.

| File | What |
|---|---|
| `docs/STATUS.md` | Verified / Inferred / Unknown. PCBWay size vs 508×600. Why 8-seat PCB vs AS-4124GQ-TNMI. |
| `docs/PCBWAY.md` | Target size, layers, thickness, finish TBD. Old MFC qty-5 220×120 cart is UNRELATED. |
| `BOM.md` | 16× 218910-1115 is the only verified connector MPN. |
| `MI250X_8OAM_PCBWay_Chassis_Stub.kicad_pro` | KiCad 9.0.2 project |
| `docs/kicad_reports/` | ERC + DRC + layer SVG |
| `docs/previews/` | PCB top PNG/SVG/PDF |

```
python3 Generated_Project/Rev3_8Seat_PCBWay_Chassis_v1/tools/generate_from_v10_pinmap.py
```

Do not “Update PCB from Schematic”. Do not upload to PCBWay.
