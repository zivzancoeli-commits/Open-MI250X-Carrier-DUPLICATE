# KiCad 9.0.2 CLI reports (not a fab sign-off)

- `erc.rpt` / `erc.json` — **392** violations (`label_dangling` 196, `hier_label_mismatch` 196). Expected named-net stub (hierarchical labels, no wires).
- `drc.rpt` / `drc.json` — **16** `lib_footprint_mismatch` (one per 218910-1115; pads carry nets the library footprint does not) + **499** unconnected items (no tracks).
- Layer SVG: Edge.Cuts, F.SilkS, F.Cu, Dwgs.User, Cmts.User, F.CrtYd.
- PCB top previews: `../previews/MI250X_8OAM_PCBWay_Chassis_Stub-top.{svg,pdf,png}` and `-top-render.png`.

**DO NOT FABRICATE. DO NOT ENERGIZE P48V.**
