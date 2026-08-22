# KiCad 9.0.9 CLI reports (not a fab sign-off)

Run 2026-08-22 on the regenerated **12-layer 2.0 mm** 8-seat named-net chassis. Hierarchical named nets, no PE tracks: **do not treat these counts as a tape-out.**

- `erc.rpt` / `erc.json` — **1280** violations, all error: `label_dangling` **640**, `hier_label_mismatch` **640**. Expected (hierarchical labels on named nets, no wires).
- `drc.rpt` / `drc.json` — **54** violations + **499** unconnected items:
  - `clearance` **32** (error): netclass P48V 0.64 mm vs 0.40 mm pad pitch on Conn0 (P48V pads next to unmapped DO_NOT_USE). OCP >40 V rule vs 0.9 mm mezz — expected, not a sign-off.
  - `lib_footprint_mismatch` **17** (warning): 16× 218910-1115 (pads carry nets the library footprint does not) + 1× Anderson SB175 (placed pads vs library copy).
  - `copper_edge_clearance` **2** (error): SB175 NPTH on the long edge (housing hangs off Y=372). Intentional inlet.
  - `silk_overlap` **2**, `silk_edge_clearance` **1** (warning).
  - Unconnected **499** reported: no PE tracks; fused P48V islands (`P48V_STAR` not shorted to seat `P48V`); DNP switches. Count may be truncated by the CLI.
- Layer SVG: Edge.Cuts, F.SilkS, F.Cu, F.CrtYd, Dwgs.User, Cmts.User, In1/In4/In7/In10 (GND plane outlines).
- PCB top previews: `../previews/MI250X_8OAM_PCBWay_Chassis_Stub-top.{svg,pdf,png}` and `-top-render.png`. Schematic: `../previews/MI250X_8OAM_PCBWay_Chassis_Stub-schematic.pdf` (14 sheets).

Do not “Update PCB from Schematic”. **DO NOT FABRICATE. DO NOT ENERGIZE P48V.**
