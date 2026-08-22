# Generated Project — MI250X OAM Prototype Carrier Rev1

Auto-generated KiCad 9 hierarchical schematic for a **single AMD Instinct MI250X OAM** prototype carrier board.

**Status:** `0.1-prototype` — architectural scaffold, not layout-ready or procurement-ready.

## Open in KiCad

```
Generated_Project/Rev1_MI250X_Carrier/MI250X_Carrier_Rev1.kicad_pro
```

Requires **KiCad 9** (schematic format version `20250114`).

## Regenerate

```bash
python3 Generated_Project/tools/generate_kicad_project.py
```

## Hierarchy

| Sheet | File | Function |
|-------|------|----------|
| Root | `MI250X_Carrier_Rev1.kicad_sch` | Top-level sheet instances |
| OAM Interface | `sheets/02_oam_interface.kicad_sch` | Mirror Mezz Conn0/Conn1 placeholders |
| Host PCIe | `sheets/03_host_pcie.kicad_sch` | Gen4 x16 host edge / routing |
| Power System | `sheets/04_power_system.kicad_sch` | 12V input, OAM 12V, 3.3V management |
| Clocking & Reset | `sheets/05_clocking_reset.kicad_sch` | 100 MHz PE_REFCLK, PERST# |
| Management | `sheets/06_management.kicad_sch` | FRU EEPROM, I2C, PMBus, UART, temp sensor |
| Test Points | `sheets/07_test_points.kicad_sch` | Bring-up measurement access |
| Expansion | `sheets/08_expansion.kicad_sch` | Multi-OAM hooks (DNP on Rev1) |

## Documentation

- `Rev1_MI250X_Carrier/docs/sources.md` — verified references
- `Rev1_MI250X_Carrier/docs/assumptions.md` — prototype assumptions
- `Rev1_MI250X_Carrier/docs/open_questions.md` — blocking TODOs
- `Rev1_MI250X_Carrier/docs/oam_signal_map.md` — OCP logical signal names
- `ENGINEERING_REVIEW.md` — post-generation review report
- `BOM_Rev1_Prototype.md` — placeholder BOM

## Design rules

- OCP OAM signal **names** used where verified; physical pin numbers **TODO**.
- AMD-specific behavior marked **TODO** — not routed or assigned.
- Does not modify `16_KiCad_Design/` per `AI_DESIGN_RULES.md`.

## Buyable first system (copied tree, 2026-08-17)

Do not overwrite Rev1 or other Rev2 production folders. The 2-OAM **v1.0-mapped stub** (not fab-ready) is:

```
Generated_Project/Rev2_MI250X_Carrier_BuyableFirstSystem_v1/
```

Shopping list: `20_System_BOM/SHOPPING.md`. Pin map authority: `22_Pinmap_Research/` (OCP generic v1.0, 688 contacts, not r2.0).

## Rev3 8-seat PCBWay chassis (Chamber B PCB only, 2026-08-22)

**DO NOT ENERGIZE P48V.** POWER+MECH first-article zip is in `Rev3_8Seat_PCBWay_Chassis_v1/fab/`. Do not upload from this agent. Does not overwrite Rev1 or Rev2 trees.

```
Generated_Project/Rev3_8Seat_PCBWay_Chassis_v1/
```

Eight electrically designed OAM seats on a **12-layer 2.0 mm** stuffed-switch target (two DNP **PM8536B-FEI PRIMARY**; 8L 2.0 mm is a cheaper DNP-switch option in docs only). Compatible with the Chamber B sheet (X11DPH-T neighbour, not on this PCB). See `Rev3_8Seat_PCBWay_Chassis_v1/docs/STATUS.md`.

## Exhaustive public-source hunt (copied tree, 2026-08-17)

Research only — **not fab-ready**. Findings: `Generated_Project/Rev2_MI250X_Carrier_ExhaustiveSourceHunt_v1/FINDINGS.md`.
