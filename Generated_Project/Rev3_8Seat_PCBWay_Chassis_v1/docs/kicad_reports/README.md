# KiCad 9.0.9 CLI reports (not a fab sign-off)

Run 2026-08-22 on the **12-layer 2.0 mm** POWER+MECH first article after zone fill.

- `drc.rpt` / `drc.json` — **0 errors**, **39** warnings, **269** unconnected items:
  - `lib_footprint_mismatch` **28** (warning): 16× 218910-1115 + SB175 + fuses/bucks (placed pads carry nets the library footprint does not).
  - `silk_overlap` / `silk_over_copper` / `silk_edge_clearance` / `text_height` (warning).
  - `isolated_copper` **4** (warning): leftover pour islands, not a submit blocker.
  - Unconnected **269**: PE / REFCLK / PERST# have names but no tracks (DNP PM8536). Count may be truncated by the CLI.
- Layer SVG: Edge.Cuts, F.SilkS, F.Cu (filled), F.CrtYd, Dwgs.User, Cmts.User, In1/In4/In7/In10 (GND planes).
- PCB top preview: `../previews/MI250X_8OAM_PCBWay_Chassis_Stub-top.{svg,png}`.

Do not “Update PCB from Schematic”. **DO NOT ENERGIZE P48V.** Do not stuff the DNP switches.
