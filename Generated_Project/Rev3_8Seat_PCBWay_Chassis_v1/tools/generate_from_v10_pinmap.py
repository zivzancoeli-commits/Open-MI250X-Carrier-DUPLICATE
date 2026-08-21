#!/usr/bin/env python3
"""Generate the Rev3 8-seat PCBWay chassis stub KiCad project.

Writes ONLY into Generated_Project/Rev3_8Seat_PCBWay_Chassis_v1/.
Never overwrites Rev1/Rev2/Rev3_2Seat. Never writes the original Open-MI250X-Carrier tree.

Pin names: 22_Pinmap_Research/extracted/OAM_v1.0_OCP_Generic_Pin_Map.csv
(xlsx in downloads/ wins on mismatch).

Architecture:
- 8 electrically designed OAM seats (first stuffing may populate 2 modules / 6 DNP).
  16x Molex 218910-1115. Board 492 x 372 mm. 12-layer 2.0 mm stuffed-switch TARGET.
  8-layer 2.0 mm is a documented cheaper DNP-switch option only — not the 8x-running stack.
- 4x2 tiling of 103x166 mm KOZ = 412x332 mm (INFERRED) + 20 mm margin + 40 mm host strip.
- All 8 seats: named P48V/P12V1/P3V3/GND, named PE toward two DNP PM8536B-FEI
  (x8 per GCD; SW0 seats 0-3, SW1 seats 4-7), per-seat REFCLK/PERST#/HOST_PWRGD.
- Host stub: silk + connector keepout toward X11DPH-T (3x Gen3 x16 + 4x Gen3 x8).
  Two CPU x16 = switch uplinks. Do NOT invent a CEM MPN.
- Do not route S1-S7 (no xGMI). TEST*/RFU/DO_NOT_USE unmapped. Never drive PVREF.
- HOST_PWRGD is ENABLE. No GPU multiphase VRM on this PCB.
- P48V: Anderson SB175 + per-seat ~15 A fuse keepouts + LOCAL pours on the 16
  verified Conn0 P48V pads. NOT a board-wide 100 A plane. Do not tie to D3000E-S1 (12 V).
- Molex 2026-08-18: 2189101115 CSA 60 V (COFC 80170713) at OCP P48V; published
  OCP P48V map already satisfies Skip Pins — do NOT add extra NC pads.
  Residual OPEN: 1.2 A/contact at 48-59.5 V (2 oz). DO NOT ENERGIZE until written.
- P3V3 = Conn0 C1/C2 only (never r2.0). P12V2 named, Unknown / may be NC.
- M3.5 NPTH φ3.9 mm per OAM Fig 2 at each seat.
- Do not shop GPUs / 48 V shelves / cooling onto this PCB BOM.
"""
from __future__ import annotations

import csv
import json
import math
import re
import shutil
import uuid
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if ROOT.name != "Rev3_8Seat_PCBWay_Chassis_v1":
    raise SystemExit(f"refusing to write outside Rev3 8-seat tree: {ROOT}")
if "Open-MI250X-Carrier" in str(ROOT) and "DUPLICATE" not in str(ROOT) and "omi-dup" not in str(ROOT):
    raise SystemExit(f"refusing to write the original repo tree: {ROOT}")

REPO = Path(__file__).resolve().parents[3]
PINMAP = REPO / "22_Pinmap_Research/extracted/OAM_v1.0_OCP_Generic_Pin_Map.csv"
XLSX = REPO / "22_Pinmap_Research/downloads/OAM_Pin_map_rev_1.0.xlsx"
FOOTPRINT_SRC = ROOT / "footprints/218910-1115_candidate.kicad_mod"
PROJ = "MI250X_8OAM_PCBWay_Chassis_Stub"
GEN = "rev3_8seat_pcbway_chassis_v1"

SCH_VER = 20250114
PCB_VER = 20241229
SYM_VER = 20241209

SHARED_RAILS = {"P48V", "P12V1", "P12V2", "P3V3", "GND"}
UNMAPPED_EXACT = {"RFU", "DO_NOT_USE"}
# Verified OCP v1.0 Conn0 P48V pads only. Do not add skip/void NC pads.
P48V_PADS = {
    "H59", "K59", "H60", "K60",
    "H61", "J61", "K61", "L61",
    "H62", "J62", "K62", "L62",
    "H63", "J63", "H64", "J64",
}

N_SEATS = 8
N_COLS = 4
N_ROWS = 2
KOZ_W, KOZ_H = 103.0, 166.0
MOD_W, MOD_H = 102.0, 165.0
MARGIN = 20.0
HOST_STRIP = 40.0
BOARD_W = MARGIN + N_COLS * KOZ_W + MARGIN + HOST_STRIP  # 492
BOARD_H = MARGIN + N_ROWS * KOZ_H + MARGIN              # 372
HOST_PCIE_SEATS = {0, 1, 2, 3, 4, 5, 6, 7}  # all 8 electrically named; first stuffing may populate 0-1
FIRST_STUFF_SEATS = {0, 1}
SW0_SEATS = {0, 1, 2, 3}
SW1_SEATS = {4, 5, 6, 7}
# Classes named on every seat so stuffing 6 more modules needs no respin.
NAMED_ON_ALL = {
    "power_shared", "pcie_stub", "clock_reset", "mgmt_stub",
    "ocp_sideband", "module_output_do_not_drive", "named_other",
}
# No xGMI / QSFP copper. TEST*/RFU already unmapped.
NO_NET_CLASSES = {
    "serdes_named_not_routed", "mgmt_link_named_not_routed",
    "qsfp_sideband_named_not_routed", "unmapped_nc",
}
CONN0_MOD = (51.0, 31.5)
CONN1_MOD = (51.0, 133.5)
HOLES_MOD = [(6.0, 31.5), (96.0, 31.5), (6.0, 133.5), (96.0, 133.5)]
ROT = 180  # Inferred PIN A3 vs candidate land (same as Rev2 2-seat)

PCBWAY_ADV_ML = (508.0, 600.0)
PCBWAY_STD_ML = (560.0, 1150.0)
N_LAYERS = 12  # stuffed-switch TARGET (8x-running). 8L 2.0 mm is docs-only cheaper DNP option.
BOARD_THICK_MM = 2.0
OZ2_UM = 0.070
OZ1_UM = 0.035
P48V_CLEAR_MM = 0.64  # OCP UBB v1.5 >40 V internal 25 mil
GND_CLEAR_MM = 0.25
# Long-edge SB175 (DS-SB175 2-pole envelope 53.1 x 35.4 mm). Body hangs off Y=372.
SB175_AT = (70.0, 362.0)
# PM8536B-FEI: 96-lane Gen3, 1311-ball 37.5 mm FCBGA, 1.0 mm pitch. DNP courtyard only.
# Host strip is 40 mm; 37.5 mm body + 1.25 mm per side.
PM8536_BODY_MM = 37.5
PM8536_CRTYD_MM = 40.0
# (x0, y0, x1, y1) courtyards in the host strip.
SW0_KEEPOUT = (452.0, 28.0, 492.0, 68.0)    # seats 0-3
SW1_KEEPOUT = (452.0, 284.0, 492.0, 324.0)  # seats 4-7
# X11DPH-T cable keepout (two CPU x16 uplinks). MPN Unknown — no CEM invented.
HOST_CABLE_KEEPOUT = (452.0, 90.0, 492.0, 250.0)


def uid() -> str:
    return str(uuid.uuid4())


def load_pinmap() -> list[dict]:
    rows = list(csv.DictReader(PINMAP.open()))
    if len(rows) != 1376:
        raise SystemExit(f"expected 1376 named pads, got {len(rows)}")
    p3 = [(r["connector"], r["pin"]) for r in rows if r["signal"] == "P3V3"]
    if p3 != [("Conn0", "C1"), ("Conn0", "C2")]:
        raise SystemExit(f"P3V3 must be Conn0 C1/C2 only, got {p3}")
    return rows


def is_unmapped(signal: str) -> bool:
    return signal in UNMAPPED_EXACT or signal.startswith("TEST")


def classify(signal: str) -> str:
    if is_unmapped(signal):
        return "unmapped_nc"
    if signal in SHARED_RAILS:
        return "power_shared"
    if signal == "PVREF":
        return "module_output_do_not_drive"
    if signal.startswith("PCIE_"):
        return "pcie_stub"
    if signal in {
        "PE_REFCLKP", "PE_REFCLKN", "PERST#", "WARMRST#", "HOST_PWRGD",
        "MODULE_PWRGD", "PWRBRK#", "PRSNT0#", "PRSNT1#", "AUX_100M_REFCLKP",
        "AUX_100M_REFCLKN", "AUX_156M_REFCLKP", "AUX_156M_REFCLKN",
        "DWN_PERST#", "DWN_REFCLKP", "DWN_REFCLKN",
    }:
        return "clock_reset"
    if signal.startswith("S") and re.match(r"S[1-7]_", signal):
        return "serdes_named_not_routed"
    if signal.startswith("MNGMT_LINK"):
        return "mgmt_link_named_not_routed"
    if signal.startswith(("CONN1_", "CONN2_")):
        return "qsfp_sideband_named_not_routed"
    if signal.startswith(("JTAG", "SMBus", "I2C", "UART", "SLV_ALERT")):
        return "mgmt_stub"
    if signal.startswith((
        "MODULE_ID", "LINK_CONFIG", "PE_BIF", "PLINK", "MANF",
        "FW_RECOVERY", "PWRRDT", "THERMTRIP", "DEBUG_PORT",
    )):
        return "ocp_sideband"
    return "named_other"


def net_name(oam: int, signal: str) -> str | None:
    """KiCad net for a v1.0 signal, or None if unmapped on this seat.

    All 8 seats are electrically designed (no respin to light seats 2-7).
    S1-S7 / QSFP / TEST* stay without nets. P12V2 stays the OCP name (Unknown/may be NC).
    """
    if is_unmapped(signal):
        return None
    sig = signal.replace(" ", "")
    cls = classify(signal)
    if cls in NO_NET_CLASSES:
        return None
    if signal in SHARED_RAILS:
        return sig
    if cls in NAMED_ON_ALL:
        return f"OAM{oam}_{sig}"
    return None


def kicad_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def seat_col_row(oam: int) -> tuple[int, int]:
    return oam % N_COLS, oam // N_COLS


def koz_origin(oam: int) -> tuple[float, float]:
    c, r = seat_col_row(oam)
    return MARGIN + c * KOZ_W, MARGIN + r * KOZ_H


def mod_origin(oam: int) -> tuple[float, float]:
    x, y = koz_origin(oam)
    return x + 0.5, y + 0.5


def pcb_from_mod(oam: int, mx: float, my: float) -> tuple[float, float]:
    """Figure 2 module coords -> PCB. Y-flipped like the Rev2 2-seat placement."""
    ox, oy = mod_origin(oam)
    return ox + mx, oy + (MOD_H - my)


def write_classification_csv(rows: list[dict]) -> None:
    out = ROOT / "netlist/v10_pad_classification.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as f:
        w = csv.writer(f)
        header = ["connector", "pad", "v10_signal", "class"]
        header += [f"oam{i}_net" for i in range(N_SEATS)]
        header += ["wired_on_all_8", "notes"]
        w.writerow(header)
        for r in rows:
            sig = r["signal"]
            cls = classify(sig)
            nets = [net_name(i, sig) or "" for i in range(N_SEATS)]
            wired = cls in {
                "power_shared", "pcie_stub", "clock_reset", "mgmt_stub",
                "ocp_sideband", "module_output_do_not_drive",
            }
            note = ""
            if cls == "unmapped_nc":
                note = "Named in v1.0 but AMD overlay unknown or reserved; no copper"
            elif cls == "serdes_named_not_routed":
                note = "Named SerDes (xGMI/IF candidate). NO NET on any seat. Do not route S1-S7."
            elif cls == "module_output_do_not_drive":
                note = "Module output. Never drive from carrier. Per-OAM nets. Do not short seats together."
            elif cls == "power_shared":
                note = (
                    "OCP-named power/ground on all 8 seats. P48V = local per-seat pour "
                    "on 16 Conn0 pads after fuse keepout; NOT a 100A flood. "
                    "P12V2 Unknown/may be NC. Do not tie P48V to D3000E-S1 (12 V). DO NOT ENERGIZE."
                )
            elif cls == "pcie_stub":
                note = (
                    "Named on all 8 seats toward DNP PM8536B-FEI (x8/GCD). "
                    "SW0=seats 0-3, SW1=seats 4-7. Not a CEM mapping."
                )
            w.writerow([r["connector"], r["pin"], sig, cls, *nets, "yes" if wired else "no", note])


def power_symbol(name: str) -> str:
    pin_rot = 90 if name != "GND" else 270
    y_off = 3.556 if name != "GND" else -3.81
    return f'''(symbol "power:{name}" (power) (pin_names (offset 0)) (in_bom yes) (on_board yes)
	(property "Reference" "#PWR" (at 0 -3.81 0) (effects (font (size 1.27 1.27)) hide))
	(property "Value" "{name}" (at 0 {y_off} 0) (effects (font (size 1.27 1.27))))
	(property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
	(symbol "{name}_0_1"
		(pin power_in line (at 0 0 {pin_rot}) (length 0) (name "{name}" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
	)
)
'''


def build_conn_symbol(conn: str, rows: list[dict]) -> str:
    by_class: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for r in rows:
        if r["connector"] != conn:
            continue
        sig = r["signal"]
        cls = classify(sig)
        if cls == "unmapped_nc":
            continue
        by_class[cls].append((r["pin"], sig.replace(" ", "_")))

    unit_map = {
        1: ["power_shared", "module_output_do_not_drive"],
        2: ["clock_reset", "mgmt_stub", "ocp_sideband", "named_other"],
        3: ["pcie_stub"],
        4: ["serdes_named_not_routed", "mgmt_link_named_not_routed", "qsfp_sideband_named_not_routed"],
    }
    etype_for = {
        "power_shared": "power_in",
        "module_output_do_not_drive": "passive",
        "clock_reset": "passive",
        "mgmt_stub": "passive",
        "ocp_sideband": "passive",
        "named_other": "passive",
        "pcie_stub": "passive",
        "serdes_named_not_routed": "passive",
        "mgmt_link_named_not_routed": "passive",
        "qsfp_sideband_named_not_routed": "passive",
    }
    sym = f"OAM_{conn}_v10"
    lines = [
        f'(symbol "{sym}" (pin_names (offset 1.016)) (pin_numbers hide) (in_bom yes) (on_board yes)',
        f'  (property "Reference" "J" (at 0 -2.54 0) (effects (font (size 1.27 1.27))))',
        f'  (property "Value" "{sym}" (at 0 2.54 0) (effects (font (size 1.27 1.27))))',
        f'  (property "Footprint" "footprints:218910-1115_candidate" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))',
        f'  (property "Datasheet" "OAM Pin map rev 1.0.xlsx OCP Generic Pin Map" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))',
        f'  (property "ki_description" "OCP generic v1.0 {conn} 688-contact map. NOT AMD MI250X overlay. DO NOT FABRICATE." (at 0 0 0) (effects (font (size 1.27 1.27)) hide))',
        f'  (property "ki_fp_filters" "218910-1115*" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))',
    ]
    for unit, classes in unit_map.items():
        pins: list[tuple[str, str, str]] = []
        for cls in classes:
            for pad, sig in by_class.get(cls, []):
                pins.append((pad, sig, etype_for[cls]))
        grouped: dict[str, list[tuple[str, str]]] = defaultdict(list)
        order = []
        for pad, sig, et in pins:
            if sig not in grouped:
                order.append((sig, et))
            grouped[sig].append((pad, et))
        n = max(len(order), 1)
        h = max(n * 2.54 + 10.16, 25.4)
        w = 50.8
        lines.append(f'  (symbol "{sym}_{unit}_1"')
        lines.append(f'    (rectangle (start {-w/2} {-h/2}) (end {w/2} {h/2})')
        lines.append(f'      (stroke (width 0.254) (type solid)) (fill (type background)))')
        y0 = h / 2 - 5.08
        for i, (sig, et) in enumerate(order):
            y = y0 - i * 2.54
            pads = grouped[sig]
            for j, (pad, pet) in enumerate(pads):
                hide = " hide" if j else ""
                lines.append(
                    f'    (pin {pet} line (at {-w/2 - 2.54} {y:.3f} 0) (length 2.54){hide}'
                    f' (name "{kicad_escape(sig)}" (effects (font (size 1.016 1.016))))'
                    f' (number "{pad}" (effects (font (size 1.016 1.016)))))'
                )
        lines.append("  )")
    lines.append(")")
    return "\n".join(lines)


def write_symbol_lib(rows: list[dict]) -> None:
    conn0 = build_conn_symbol("Conn0", rows)
    conn1 = build_conn_symbol("Conn1", rows)
    text = (
        f'(kicad_symbol_lib (version {SYM_VER}) (generator "{GEN}")\n'
        + conn0 + "\n" + conn1 + "\n)\n"
    )
    (ROOT / "symbols/OAM_v10_mapped.kicad_sym").write_text(text)


def sch_header(title: str, comment: str) -> str:
    return f'''(kicad_sch (version {SCH_VER}) (generator "{GEN}")
	(uuid "{uid()}")
	(paper "A3")
	(title_block
		(title "{kicad_escape(title)}")
		(date "2026-08-21")
		(rev "Rev3_8Seat_PCBWay_v1")
        (comment 1 "DO NOT FABRICATE. DO NOT ENERGIZE P48V. Molex 60V written 2026-08-18; 1.2A/contact OPEN.")
        (comment 2 "{kicad_escape(comment)}")
        (comment 3 "Pin names: OAM Pin map rev 1.0.xlsx — OCP generic, NOT AMD overlay")
        (comment 4 "r2.0 UNUSABLE. P3V3=Conn0 C1/C2. 12L 2.0mm stuffed-switch TARGET. Star-fed P48V.")
	)
'''


SHEETS = [
    ("00_DO_NOT_FABRICATE", "sheets/00_do_not_fabricate.kicad_sch"),
    ("01_Power_Clock_Reset", "sheets/01_power_clock_reset.kicad_sch"),
    ("02_Host_PCIe_Stub_OAM0_1", "sheets/02_host_pcie_stub.kicad_sch"),
    ("03_OAM0_Connectors", "sheets/03_oam0_connectors.kicad_sch"),
    ("04_OAM1_Connectors", "sheets/04_oam1_connectors.kicad_sch"),
    ("05_OAM2_MechPower", "sheets/05_oam2_connectors.kicad_sch"),
    ("06_OAM3_MechPower", "sheets/06_oam3_connectors.kicad_sch"),
    ("07_OAM4_MechPower", "sheets/07_oam4_connectors.kicad_sch"),
    ("08_OAM5_MechPower", "sheets/08_oam5_connectors.kicad_sch"),
    ("09_OAM6_MechPower", "sheets/09_oam6_connectors.kicad_sch"),
    ("10_OAM7_MechPower", "sheets/10_oam7_connectors.kicad_sch"),
    ("11_PM8536_DNP", "sheets/11_pcie_switch_unknown.kicad_sch"),
    ("12_Unmapped_AMD", "sheets/12_unmapped_amd.kicad_sch"),
]


def write_root_sch() -> None:
    p = ROOT / f"{PROJ}.kicad_sch"
    body = sch_header(
        "Rev3 8-seat PCBWay chassis stub (NOT fab-ready)",
        "8 OAM seats. Host X11DPH-T is NOT on this PCB. No CEM cable. No 20-layer UBB.",
    )
    note = (
        "DO NOT FABRICATE / DO NOT ENERGIZE P48V\\n"
        "8 electrically designed OAM seats (first stuffing: 2 modules / 6 DNP OK — no respin).\\n"
        "16x Molex 218910-1115, 5.00 mm stack. 12-layer 2.0 mm stuffed-switch TARGET. Outline 492 x 372 mm.\\n"
        "4x2 of 103x166 mm KOZ = 412x332 mm INFERRED tiling (not a UBB drawing).\\n"
        "All 8: named PE toward 2x PM8536B-FEI DNP (x8/GCD; SW0=0-3, SW1=4-7). No CEM invented.\\n"
        "Host stub: X11DPH-T 3x Gen3 x16 + 4x Gen3 x8 keepout. Two CPU x16 = switch uplinks.\\n"
        "X11DPH-T / NH-D9 DX-3647 / B550M are NOT on this PCB. Chamber A mATX is not this PCB.\\n"
        "S1-S7 NOT routed (no xGMI). TEST*/RFU/DO_NOT_USE unmapped. PVREF never driven.\\n"
        "P48V: SB175 long-edge entry + ~15A fuse/seat + LOCAL pours on 16 Conn0 pads. NOT a 100A flood.\\n"
        "Molex 2026-08-18: CSA 60V (COFC 80170713) at OCP P48V; skip pins = published map, no extra NC.\\n"
        "OPEN: 1.2 A/contact at 48-59.5 V (2 oz). HOST_PWRGD is ENABLE. No GPU VRM. P12V2 Unknown/may be NC.\\n"
        "Dell D3000E-S1 is 12 V CRPS — do not mix into P48V. P3V3 = Conn0 C1/C2 only. Never r2.0."
    )
    body += f'''
	(lib_symbols
{power_symbol("P48V")}
{power_symbol("P12V1")}
{power_symbol("P12V2")}
{power_symbol("+3V3")}
{power_symbol("GND")}
{power_symbol("P48V_STAR")}
	)

	(text (at 25.4 15.24 0)
		(effects (font (size 1.8 1.8) (thickness 0.3)) (justify left top))
		(uuid "{uid()}")
		"{note}"
	)
'''
    # 4 columns x 4 rows of 70x32 mm sheets starting y=95
    cols, w, h, x0, y0, dx, dy = 4, 65, 32, 20, 100, 72, 42
    for i, (name, rel) in enumerate(SHEETS):
        c, r = i % cols, i // cols
        x = x0 + c * dx
        y = y0 + r * dy
        body += f'''	(sheet (at {x} {y}) (size {w} {h})
		(stroke (width 0.1524) (type solid))
		(fill (color 0 0 0 0.0000))
		(uuid "{uid()}")
		(property "Sheetname" "{name}" (at {x+2.54} {y-2.54} 0)
			(effects (font (size 1.27 1.27)) (justify left bottom)) (uuid "{uid()}"))
		(property "Sheetfile" "{rel}" (at {x+2.54} {y+h+2.54} 0)
			(effects (font (size 1.016 1.016)) (justify left top)) (uuid "{uid()}"))
	)
'''
    body += ")\n"
    p.write_text(body)


def write_text_sheet(rel: str, title: str, text: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        sch_header(title, "Documentation sheet — no invented nets")
        + f'''
	(text (at 20.32 20.32 0)
		(effects (font (size 1.5 1.5)) (justify left top))
		(uuid "{uid()}")
		"{kicad_escape(text)}"
	)
)
'''
    )


def append_hier_labels(rel: str, labels: list[str], x: float = 25.4, y0: float = 150.0, dy: float = 5.08) -> None:
    path = ROOT / rel
    existing = path.read_text().rstrip()
    if existing.endswith(")"):
        existing = existing[:-1]
    extra = []
    y = y0
    for lab in labels:
        extra.append(f'''
	(hierarchical_label (at {x} {y} 0)
		(effects (font (size 1.27 1.27)) (justify left))
		(uuid "{uid()}")
		(shape bidirectional)
		"{lab}"
	)
''')
        y += dy
        if y > 260:
            y = y0
            x += 70
    path.write_text(existing + "\n" + "".join(extra) + "\n)\n")


def write_do_not_fab_sheet() -> None:
    text = """GATE LIST — all must be closed before fabrication or applying power to an MI250X.

1. 48V source identified AND harnessed to the SB175. Dell D3000E-S1 is 12 V CRPS —
   do not tie OAM P48V to it. No PSU shopping on this PCB BOM.
2. Molex 218910-1115 voltage/skip-pin: WRITTEN YES 2026-08-18 (Brian Park / ticket 167157).
   CSA 60 V (COFC 80170713) at OCP P48V. Published OCP P48V map already satisfies Skip Pins
   — do NOT add extra NC pads. Eli ack 2026-08-19.
   STILL OPEN: 1.2 A per used power contact at 48-59.5 V (2 oz), and skip/void is NC
   on the same MPN. DO NOT ENERGIZE until that current follow-up is written.
3. Connector gender/stack: hermaphroditic 2189101115 mates with itself, 5 mm stack.
   Confirm PIN A3 orientation on a plot before tape-out (rotation 180 Inferred).
4. AMD overlay unknowns (TEST*, dual-GCD PE vs SERDES_7, SMBus map, P12V2 need, xGMI S1-S7).
5. Host X11DPH-T is NOT on this PCB. Cooler on the host is NH-D9 DX-3647 (NOT U14S).
   Chamber A mATX B550M 244x244 is NOT on this PCB.
6. PCIe: all 8 seats named toward 2x PM8536B-FEI DNP (x8 per GCD). Two CPU x16 uplinks.
   No CEM cable invented. Host MPN Unknown (silk keepout only).
7. HOST_PWRGD is ENABLE. Sequencing vs P48V/P12V1/P3V3 — OCP + AMD overlay only.
8. Do not reuse the old MFC qty-5 cart for 220x120 mm. That quote is UNRELATED.
9. Per-seat ~15 A fuse MPN still Unknown (keepout only). P12V1 <=50 W and P3V3 <=5 W
   sources are keepouts — no GPU multiphase VRM on this PCB.
10. Do not upload to PCBWay. 12L 2.0 mm is the stuffed-switch target; 8L 2.0 mm is
    a cheaper DNP-switch option only.

Until then this KiCad tree is a mapping artifact. Do not send to PCBWay. DO NOT ENERGIZE P48V.
"""
    write_text_sheet("sheets/00_do_not_fabricate.kicad_sch", "DO NOT FABRICATE", text)


def write_power_clock_sheet() -> None:
    text = """PURPOSE: Named power / clock / reset stubs from OAM v1.0 pin map.

STAR-FED P48V (NOT a board-wide 100 A plane):
- Board entry: Anderson SB175 (175 A / 600 V) on the long edge, 2 AWG landing.
  Net P48V_STAR. Kelvin+ / Kelvin- pads at the star. Off-board 48 V is NOT a PCB BOM item.
- Dell D3000E-S1 is 12 V CRPS — do not tie OAM P48V to it. 1000 W ATX/EPS is HOST only.
- Per seat: ~15 A fuse keepout (MPN Unknown), then the 16 verified OCP v1.0 Conn0
  P48V pads. Local 2 oz F.Cu pour around those 16 pads only. No extra NC/skip pads.
- Molex 2026-08-18 written yes: CSA 60 V (COFC 80170713) at OCP P48V.
  OPEN: 1.2 A/contact at 48-59.5 V (2 oz). DO NOT ENERGIZE.

SHARED RAILS (OCP names, pads on every seat):
- P48V  Conn0 16 pads  44-59.5 V  up to 700 W class (pin list). MI250X 500/560 W.
        LOCAL pours only. Module has the 48 V core VRMs — no GPU multiphase here.
- P12V1 Conn0 5 pads   12 V infrastructure up to 50 W. Carrier supplies <=50 W.
        Keepout only; no VRM MPN invented.
- P12V2 Conn0 27 pads  12 V main for 12V-based OAM. MI250X is 48 V class.
        Unknown / may be NC. Do NOT short to P12V1. Do not invent a P12V2 supply.
- P3V3  Conn0 C1,C2    3.3 V up to 5 W. Carrier supplies <=5 W. 2 pins — v1.5 Table 4.
- GND   Conn0 majority. Inner GND planes (In1, In4), 2 oz planning.
- PVREF Conn0 G1,G2    MODULE OUTPUT. NEVER drive from carrier. Per-OAM nets.

CLOCK / RESET named on ALL 8 seats (no respin to light 2-7):
- PE_REFCLKP/N, PERST#, HOST_PWRGD (ENABLE), plus WARMRST# / MODULE_PWRGD / PWRBRK# / PRSNT*
- HOST_PWRGD is ENABLE (OCP: Power Enable when P48V/P12V1/P12V2/P3V3 are in spec).

First stuffing may populate 2 modules / 6 DNP. Nets already exist on all 8.

DO NOT: invent VRMs, mix 12 V CRPS into P48V, drive PVREF, pour a 100 A P48V plane,
shop a 48 V shelf onto this BOM, or attach a guessed clock chip.
"""
    write_text_sheet("sheets/01_power_clock_reset.kicad_sch", "Power / clock / reset stub", text)
    path = ROOT / "sheets/01_power_clock_reset.kicad_sch"
    existing = path.read_text().rstrip()
    if existing.endswith(")"):
        existing = existing[:-1]
    flags = []
    x = 30.48
    for name, net in [("P48V_STAR", "P48V_STAR"), ("P48V", "P48V"), ("P12V1", "P12V1"),
                      ("P12V2", "P12V2"), ("+3V3", "P3V3"), ("GND", "GND")]:
        flags.append(f'''
	(symbol (lib_id "power:{name}") (at {x} 140 0) (unit 1)
		(in_bom yes) (on_board yes) (dnp no)
		(uuid "{uid()}")
		(property "Reference" "#PWR{name.replace('+','')}" (at {x} 135 0)
			(effects (font (size 1.27 1.27)) hide) (uuid "{uid()}"))
		(property "Value" "{name}" (at {x} 145 0)
			(effects (font (size 1.27 1.27))) (uuid "{uid()}"))
		(pin "1" (uuid "{uid()}"))
	)
	(label (at {x} 145.1 0)
		(effects (font (size 1.27 1.27)) (justify left bottom))
		(uuid "{uid()}")
		"{net}"
	)
''')
        x += 25.4
    path.write_text(existing + "\n" + "".join(flags) + "\n)\n")
    labs = []
    for oam in range(N_SEATS):
        labs += [
            f"OAM{oam}_PE_REFCLKP", f"OAM{oam}_PE_REFCLKN", f"OAM{oam}_PERST#",
            f"OAM{oam}_HOST_PWRGD", f"OAM{oam}_MODULE_PWRGD", f"OAM{oam}_PVREF",
        ]
    append_hier_labels("sheets/01_power_clock_reset.kicad_sch", labs, y0=170, dy=4.5)


def write_pcie_sheet() -> None:
    text = """PURPOSE: Named v1.0 PCIE_TXnP/N and PCIE_RXnP/N (n=0..15) on ALL 8 seats.

8 electrically designed seats. First stuffing may populate 2 modules / 6 DNP —
the PCB does not require a respin for the other six.

OCP pin list (module POV):
- PETp/n = module TX, host RX. AC caps on motherboard/carrier — not placed.
- PERp/n = module RX, host TX. AC caps on motherboard/carrier — not placed.

This sheet does NOT map those pairs onto a CEM x16 connector pinout.
Do NOT invent a CEM cable, SlimSAS, MCIO, or retimer BOM.

Intended 8x topology (DNP until stuffed):
- Two Microchip PM8536B-FEI (Switchtec PFX 96-lane Gen3, 1311-ball 37.5 mm FCBGA).
  SW0 = seats 0-3 (16 US + 64 DS). SW1 = seats 4-7. x8 per GCD.
- Each seat's 16 named PE lanes = 2x x8 (GCD0/GCD1 split is planning; PE_BIF AMD-unknown).
- Second host x16 as SERDES_7: Inferred, NOT proven. Do not route S1-S7 as GCD1.
- Host X11DPH-T (NOT on this PCB): 3x Gen3 x16 + 4x Gen3 x8.
  Two CPU x16 = switch uplinks (silk + connector keepout, MPN Unknown).
  Remaining 1x x16 + 4x x8 unused on this chassis.

8 x 2 x x16 = 256 downstream vs 80 host Gen3 — do not attempt x16-per-GCD.
PEX8780 80-lane is a cheaper alt in docs only. Do not stuff PM8536 until purchased.

X11DPH-T is NOT a part on this PCB. Chamber A B550M is NOT this PCB.
"""
    write_text_sheet("sheets/02_host_pcie_stub.kicad_sch", "Host PE stub (all 8 seats via DNP PM8536)", text)
    labels = []
    for oam in range(N_SEATS):
        for n in range(16):
            for pn in ("P", "N"):
                for txrx in ("TX", "RX"):
                    labels.append(f"OAM{oam}_PCIE_{txrx}{n}{pn}")
    append_hier_labels("sheets/02_host_pcie_stub.kicad_sch", labels, y0=130, dy=3.81)


def write_oam_connector_sheet(oam: int, rel: str) -> None:
    sw = "SW0 PM8536B-FEI DNP (seats 0-3)" if oam in SW0_SEATS else "SW1 PM8536B-FEI DNP (seats 4-7)"
    stuff = "FIRST STUFF candidate (2 modules / 6 DNP OK)" if oam in FIRST_STUFF_SEATS else "electrically designed; module may be DNP"
    text = f"""OAM{oam} connector instances — {stuff}.

Footprint: Molex 218910-1115 candidate (geometry). Hermaphroditic — mates with itself
(Farnell 2189101115: Mates With 2189101115; mated height 5.00 mm).

Pad nets assigned on the PCB from the v1.0 CSV for this seat:
P48V/P12V1/P3V3/GND, PE (16 lanes) toward {sw},
PE_REFCLK / PERST# / HOST_PWRGD (ENABLE). S1-S7 have NO NET (no xGMI).
TEST*/RFU/DO_NOT_USE unmapped. PVREF is a module output — never drive.
P12V2 named from v1.0 but Unknown / may be NC. P48V is a LOCAL pour after a ~15 A fuse keepout.

MODULE_ID / LINK_CONFIG 1k pulldowns NOT placed (AMD overlay unknown).
"""
    ports = [
        "P48V", "P12V1", "P12V2", "P3V3", "GND",
        f"OAM{oam}_PVREF", f"OAM{oam}_PE_REFCLKP", f"OAM{oam}_PE_REFCLKN",
        f"OAM{oam}_PERST#", f"OAM{oam}_HOST_PWRGD", f"OAM{oam}_MODULE_PWRGD",
        f"OAM{oam}_WARMRST#", f"OAM{oam}_PWRBRK#", f"OAM{oam}_PRSNT0#",
        f"OAM{oam}_SMBus_SLV_D", f"OAM{oam}_SMBus_SLV_CLK",
    ]
    write_text_sheet(rel, f"OAM{oam} connectors", text)
    append_hier_labels(rel, ports, y0=150)


def write_switch_unknown_sheet() -> None:
    text = """TWO PM8536B-FEI KEEPOUTS — DNP. No fake schematic pins.

U_SW0  PM8536B-FEI  DNP  seats 0-3   16 US + 64 DS   x8 per GCD
U_SW1  PM8536B-FEI  DNP  seats 4-7   16 US + 64 DS   x8 per GCD

Package (Verified Microchip PFX table): 96-lane Gen3, 1311-ball 37.5 x 37.5 mm FCBGA, 1.0 mm pitch.
PCBWay can assemble 1.0 mm without HDI; 12L 2.0 mm is the stuffed-switch TARGET.
8L 2.0 mm is a cheaper DNP-switch / mezz+power option only — not the 8x-running stack.
Caveat: guest quotes used 6/6 mil + 0.3 mm hole; 1311-ball escape may need finer rules.

Do NOT populate until Eli buys the parts. Courtyard/keepout only.
PEX8780-AB80BI G (80-lane 35 mm) is a cheaper alt in docs only — not placed.
PM8533B-F3EI (48-lane 27 mm) is a 2-seat alt in docs only — not placed.

Host X11DPH-T (NOT on this PCB): 3x Gen3 x16 + 4x Gen3 x8 = 80 Gen3 lanes.
Two CPU x16 become the two switch uplinks (silk + connector keepout, MPN Unknown).
Do not invent CEM / SlimSAS / MCIO / retimer.

8 x 2 x x16 = 256 DS vs 80 host — x16-per-GCD is impossible. x8 per GCD is the plan.
GCD1 = SERDES_7 is Inferred (OAM v1.5 may put a second PE x16 on Conn1 SERDES_7).
Do NOT route S1-S7 as if that were proven. No xGMI mesh.

Refclk / PERST# / HOST_PWRGD per seat per OAM v1.5
(HOST_PWRGD >= 100 ms after MODULE_PWRGD). AMD delays still Unknown.
"""
    write_text_sheet("sheets/11_pcie_switch_unknown.kicad_sch", "PM8536B-FEI DNP x2 (keepout only)", text)


def write_unmapped_sheet(rows: list[dict]) -> None:
    unmapped = sorted({(r["connector"], r["pin"], r["signal"]) for r in rows if is_unmapped(r["signal"])})
    lines = [
        "Pads explicitly UNMAPPED on every seat (no net, no copper).",
        "Named in the v1.0 generic map but reserved, do-not-use, or TEST pins",
        "whose AMD MI250X function is Unknown. Do not invent pullups or straps.",
        "S1-S7 / QSFP sideband also have no net (no xGMI). All 8 seats are otherwise electrically named.",
        "",
    ]
    for conn, pad, sig in unmapped:
        lines.append(f"{conn} {pad:4s}  {sig}")
    write_text_sheet("sheets/12_unmapped_amd.kicad_sch", "Unmapped / AMD-unknown pads", "\n".join(lines))


def parse_footprint_pads() -> list[tuple[str, str, str, str]]:
    raw = FOOTPRINT_SRC.read_text()
    return re.findall(
        r'\(pad "([A-Z]+\d+)" smd circle \(at ([^)]+)\) \(size ([^)]+)\) \(layers ([^)]+)\)\)',
        raw,
    )


def fp_to_world(fx: float, fy: float, rot: int, px: float, py: float) -> tuple[float, float]:
    """Footprint-local pad -> PCB. ROT 180 is the inferred PIN A3 placement."""
    if rot == 180:
        return fx - px, fy - py
    if rot == 0:
        return fx + px, fy + py
    raise SystemExit(f"unsupported footprint rotation {rot}")


def zone(net_id: int, name: str, layer: str, clearance: float, pts: list[tuple[float, float]],
         priority: int = 0, hatch: str = "0.5") -> str:
    poly = " ".join(f"(xy {x:.3f} {y:.3f})" for x, y in pts)
    return f'''  (zone (net {net_id}) (net_name "{name}") (layer "{layer}") (uuid "{uid()}")
    (hatch edge {hatch})
    (priority {priority})
    (connect_pads yes (clearance {clearance}))
    (min_thickness 0.25)
    (filled_areas_thickness no)
    (fill yes (thermal_gap {clearance}) (thermal_bridge_width 0.5))
    (polygon (pts {poly}))
  )'''


def keepout_rect(x0: float, y0: float, x1: float, y1: float, layers: str = "*.Cu") -> str:
    return f'''  (zone (net 0) (net_name "") (layers "{layers}") (uuid "{uid()}")
    (hatch edge 0.5)
    (priority 0)
    (keepout (tracks not_allowed) (vias not_allowed) (pads allowed) (copperpour not_allowed) (footprints not_allowed))
    (fill yes (thermal_gap 0.5) (thermal_bridge_width 0.5))
    (polygon (pts (xy {x0:.3f} {y0:.3f}) (xy {x1:.3f} {y0:.3f}) (xy {x1:.3f} {y1:.3f}) (xy {x0:.3f} {y1:.3f})))
  )'''


def write_pcb(rows: list[dict]) -> None:
    """12-layer stuffed-switch target: local P48V pours, GND planes, SB175, 2x PM8536 DNP keepouts."""
    pads = parse_footprint_pads()
    if len(pads) != 688:
        raise SystemExit(f"expected 688 footprint pads, got {len(pads)}")

    p48_local: list[tuple[float, float]] = []
    for pad, at, _size, _layers in pads:
        if pad in P48V_PADS:
            xs = at.split()
            p48_local.append((float(xs[0]), float(xs[1])))
    if len(p48_local) != 16:
        raise SystemExit(f"expected 16 Conn0 P48V pads in footprint, got {len(p48_local)}")

    pad_sig = {(r["connector"], r["pin"]): r["signal"] for r in rows}
    p48_csv = [r["pin"] for r in rows if r["connector"] == "Conn0" and r["signal"] == "P48V"]
    if set(p48_csv) != P48V_PADS:
        raise SystemExit(f"CSV P48V pads {sorted(p48_csv)} != verified set {sorted(P48V_PADS)}")

    nets: dict[str, int] = {}

    def nid(name: str) -> int:
        if name not in nets:
            nets[name] = len(nets) + 1
        return nets[name]

    for n in ["GND", "P48V", "P12V1", "P12V2", "P3V3", "P48V_STAR"]:
        nid(n)

    seats_meta = []
    holes = []
    conn0_xy: dict[int, tuple[float, float]] = {}
    for oam in range(N_SEATS):
        c0 = pcb_from_mod(oam, *CONN0_MOD)
        c1 = pcb_from_mod(oam, *CONN1_MOD)
        conn0_xy[oam] = c0
        seats_meta.append((oam, "Conn0", f"J{oam}_Conn0", c0[0], c0[1], ROT))
        seats_meta.append((oam, "Conn1", f"J{oam}_Conn1", c1[0], c1[1], ROT))
        for i, (hx, hy) in enumerate(HOLES_MOD, start=1):
            px, py = pcb_from_mod(oam, hx, hy)
            holes.append((f"H{oam}{i}", px, py))

    fp_blocks = []
    for oam, conn, ref, x, y, rot in seats_meta:
        role = "ELEC_NAMED_8SEAT" if oam in FIRST_STUFF_SEATS else "ELEC_NAMED_DNP_MODULE_OK"
        pad_lines = [
            '    (pad "" np_thru_hole circle (at -31.5000 -9.5000) (size 1.80 1.80) (drill 1.80) (layers "*.Cu" "*.Mask"))',
            '    (pad "" np_thru_hole circle (at 31.5000 -9.5000) (size 1.80 1.80) (drill 1.80) (layers "*.Cu" "*.Mask"))',
        ]
        for pad, at, size, layers in pads:
            sig = pad_sig.get((conn, pad))
            extra = ""
            if sig:
                n = net_name(oam, sig)
                if n:
                    extra = f' (net {nid(n)} "{n}")'
            pad_lines.append(
                f'    (pad "{pad}" smd circle (at {at}) (size {size}) (layers {layers}){extra})'
            )
        fp_blocks.append(f'''  (footprint "footprints:218910-1115_candidate" (layer "F.Cu") (at {x:.3f} {y:.3f} {rot})
    (descr "v1.0 mapped geometry candidate — DO NOT FABRICATE")
    (property "Reference" "{ref}" (at 0 -14) (layer "F.SilkS") (effects (font (size 1.2 1.2) (thickness 0.15))))
    (property "Value" "218910-1115" (at 0 14) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))
    (property "Sheetfile" "{PROJ}.kicad_sch" (at 0 0) (layer "F.Fab") (effects (font (size 1 1)) hide))
    (fp_text user "OAM{oam} {conn} {role}; unmapped pads have no net" (at 0 0) (layer "Cmts.User")
      (effects (font (size 0.8 0.8) (thickness 0.1))))
{chr(10).join(pad_lines)}
  )''')

    star_id = nid("P48V_STAR")
    gnd_id = nid("GND")
    p48_id = nid("P48V")
    sx, sy = SB175_AT
    fp_blocks.append(f'''  (footprint "footprints:Anderson_SB175_2pole" (layer "F.Cu") (at {sx:.3f} {sy:.3f})
    (descr "Anderson SB175 175A/600V long-edge entry. 2 AWG landing. DO NOT ENERGIZE. Not D3000E-S1.")
    (property "Reference" "J_SB175" (at 0 -28) (layer "F.SilkS") (effects (font (size 1.2 1.2) (thickness 0.15))))
    (property "Value" "SB175_175A_600V" (at 0 24) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))
    (fp_text user "2 AWG from shelf — Kelvin sense at star — DO NOT ENERGIZE P48V" (at 0 -22) (layer "F.SilkS")
      (effects (font (size 0.8 0.8) (thickness 0.1))))
    (fp_rect (start -26.55 -17.7) (end 26.55 17.7) (stroke (width 0.15) (type solid)) (fill none) (layer "F.SilkS"))
    (fp_rect (start -27.5 -18.5) (end 27.5 18.5) (stroke (width 0.12) (type dash)) (fill none) (layer "F.CrtYd"))
    (pad "1" smd rect (at -14.3 -8) (size 14 10) (layers "F.Cu" "F.Paste" "F.Mask") (net {star_id} "P48V_STAR"))
    (pad "2" smd rect (at 14.3 -8) (size 14 10) (layers "F.Cu" "F.Paste" "F.Mask") (net {gnd_id} "GND"))
    (pad "K+" smd circle (at -14.3 -16.5) (size 2.2 2.2) (layers "F.Cu" "F.Paste" "F.Mask") (net {star_id} "P48V_STAR"))
    (pad "K-" smd circle (at 14.3 -16.5) (size 2.2 2.2) (layers "F.Cu" "F.Paste" "F.Mask") (net {gnd_id} "GND"))
    (pad "" np_thru_hole circle (at -14.3 8) (size 8.00 8.00) (drill 6.60) (layers "*.Cu" "*.Mask"))
    (pad "" np_thru_hole circle (at 14.3 8) (size 8.00 8.00) (drill 6.60) (layers "*.Cu" "*.Mask"))
  )''')

    net_decls = "\n".join(f'  (net {i} "{name}")' for name, i in sorted(nets.items(), key=lambda kv: kv[1]))
    hole_blocks = []
    for ref, hx, hy in holes:
        hole_blocks.append(
            f'''  (footprint "NPTH_3.9_Fig2" (layer "F.Cu") (at {hx:.3f} {hy:.3f})
    (property "Reference" "{ref}" (at 0 -4) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))
    (property "Value" "NPTH_3.9" (at 0 4) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))
    (pad "" np_thru_hole circle (at 0 0) (size 8.00 8.00) (drill 3.90) (layers "*.Cu" "*.Mask"))
  )'''
        )

    graphics = [
        f'  (gr_rect (start 0 0) (end {BOARD_W:.3f} {BOARD_H:.3f})',
        '    (stroke (width 0.2) (type solid)) (fill none) (layer "Edge.Cuts"))',
        f'  (gr_text "DO NOT FABRICATE  /  DO NOT ENERGIZE P48V  /  Rev3 8-seat PCBWay chassis stub"',
        f'    (at {BOARD_W/2:.3f} 6) (layer "F.SilkS")',
        '    (effects (font (size 2.4 2.4) (thickness 0.3))))',
        f'  (gr_text "Molex 218910-1115 x16  |  12L 2.0mm TARGET  |  LOCAL P48V pours  |  2x PM8536B-FEI DNP  |  SB175 star  |  NOT a UBB"',
        f'    (at {BOARD_W/2:.3f} 12) (layer "F.SilkS")',
        '    (effects (font (size 1.5 1.5) (thickness 0.18))))',
        f'  (gr_text "4x2 of 103x166 mm KOZ = 412x332 mm INFERRED tiling. Outline {BOARD_W:.0f}x{BOARD_H:.0f} mm < PCBWay adv ML 508x600."',
        f'    (at {BOARD_W/2:.3f} {BOARD_H-6:.3f}) (layer "F.SilkS")',
        '    (effects (font (size 1.4 1.4) (thickness 0.18))))',
    ]

    fuse_centers: list[tuple[int, float, float]] = []
    p48_bboxes: list[tuple[int, float, float, float, float]] = []
    margin_p = 1.4
    for oam in range(N_SEATS):
        fx, fy = conn0_xy[oam]
        world = [fp_to_world(fx, fy, ROT, px, py) for px, py in p48_local]
        xs = [p[0] for p in world]
        ys = [p[1] for p in world]
        x0, y0 = min(xs) - margin_p, min(ys) - margin_p
        x1, y1 = max(xs) + margin_p, max(ys) + margin_p
        p48_bboxes.append((oam, x0, y0, x1, y1))
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        dx, dy = cx - fx, cy - fy
        nrm = math.hypot(dx, dy) or 1.0
        fuse_cx = cx + 11.0 * dx / nrm
        fuse_cy = cy + 11.0 * dy / nrm
        fuse_centers.append((oam, fuse_cx, fuse_cy))

    for oam in range(N_SEATS):
        kx, ky = koz_origin(oam)
        mx, my = mod_origin(oam)
        cx = kx + KOZ_W / 2
        cy = ky + 8
        sw = "SW0" if oam in SW0_SEATS else "SW1"
        if oam in FIRST_STUFF_SEATS:
            role = f"SEAT {oam}  ELEC NAMED  first-stuff OK  PE->{sw}  x8/GCD"
        else:
            role = f"SEAT {oam}  ELEC NAMED  module DNP OK  PE->{sw}  no respin"
        graphics += [
            f'  (gr_rect (start {kx:.3f} {ky:.3f}) (end {kx+KOZ_W:.3f} {ky+KOZ_H:.3f})',
            '    (stroke (width 0.15) (type solid)) (fill none) (layer "Dwgs.User"))',
            f'  (gr_rect (start {kx:.3f} {ky:.3f}) (end {kx+KOZ_W:.3f} {ky+KOZ_H:.3f})',
            '    (stroke (width 0.12) (type dash)) (fill none) (layer "F.CrtYd"))',
            f'  (gr_rect (start {mx:.3f} {my:.3f}) (end {mx+MOD_W:.3f} {my+MOD_H:.3f})',
            '    (stroke (width 0.12) (type dash)) (fill none) (layer "Dwgs.User"))',
            f'  (gr_text "{role}"',
            f'    (at {cx:.3f} {cy:.3f}) (layer "F.SilkS")',
            '    (effects (font (size 1.5 1.5) (thickness 0.18))))',
            f'  (gr_text "OAM{oam} KOZ 103x166 (Fig 14)  module 102x165 (Fig 2)  M3.5 NPTH 3.9 mm"',
            f'    (at {cx:.3f} {ky+KOZ_H-6:.3f}) (layer "Dwgs.User")',
            '    (effects (font (size 1.1 1.1) (thickness 0.12))))',
            f'  (gr_text "P48V local pour — 16 Conn0 pads — 2 oz — not a 100A plane"',
            f'    (at {cx:.3f} {ky+14:.3f}) (layer "Cmts.User")',
            '    (effects (font (size 0.9 0.9) (thickness 0.1))))',
        ]

    hx0 = MARGIN + N_COLS * KOZ_W + MARGIN  # 452
    a0, a1, a2, a3 = SW0_KEEPOUT
    b0, b1, b2, b3 = SW1_KEEPOUT
    h0, h1, h2, h3 = HOST_CABLE_KEEPOUT
    graphics += [
        f'  (gr_rect (start {hx0:.3f} {MARGIN:.3f}) (end {BOARD_W:.3f} {BOARD_H-MARGIN:.3f})',
        '    (stroke (width 0.25) (type solid)) (fill none) (layer "Dwgs.User"))',
        f'  (gr_rect (start {a0:.3f} {a1:.3f}) (end {a2:.3f} {a3:.3f})',
        '    (stroke (width 0.25) (type dash)) (fill none) (layer "F.CrtYd"))',
        f'  (gr_rect (start {a0:.3f} {a1:.3f}) (end {a2:.3f} {a3:.3f})',
        '    (stroke (width 0.2) (type dash)) (fill none) (layer "Dwgs.User"))',
        f'  (gr_text "U_SW0 DNP"',
        f'    (at {hx0+HOST_STRIP/2:.3f} {48:.3f} 90) (layer "F.SilkS")',
        '    (effects (font (size 1.4 1.4) (thickness 0.16))))',
        f'  (gr_text "PM8536B-FEI 37.5mm 1311-FCBGA"',
        f'    (at {hx0+HOST_STRIP/2+8:.3f} {48:.3f} 90) (layer "F.SilkS")',
        '    (effects (font (size 1.0 1.0) (thickness 0.12))))',
        f'  (gr_text "seats 0-3  x8/GCD  16US+64DS"',
        f'    (at {hx0+HOST_STRIP/2+16:.3f} {48:.3f} 90) (layer "F.SilkS")',
        '    (effects (font (size 0.9 0.9) (thickness 0.1))))',
        f'  (gr_rect (start {h0:.3f} {h1:.3f}) (end {h2:.3f} {h3:.3f})',
        '    (stroke (width 0.2) (type dash)) (fill none) (layer "F.CrtYd"))',
        f'  (gr_rect (start {h0:.3f} {h1:.3f}) (end {h2:.3f} {h3:.3f})',
        '    (stroke (width 0.15) (type dash)) (fill none) (layer "Dwgs.User"))',
        f'  (gr_text "HOST CABLE KEEPOUT"',
        f'    (at {hx0+HOST_STRIP/2:.3f} {170:.3f} 90) (layer "F.SilkS")',
        '    (effects (font (size 1.5 1.5) (thickness 0.18))))',
        f'  (gr_text "X11DPH-T two CPU x16 uplinks"',
        f'    (at {hx0+HOST_STRIP/2-8:.3f} {170:.3f} 90) (layer "F.SilkS")',
        '    (effects (font (size 1.1 1.1) (thickness 0.14))))',
        f'  (gr_text "3x x16 + 4x x8 Gen3  MPN Unknown"',
        f'    (at {hx0+HOST_STRIP/2+0:.3f} {170:.3f} 90) (layer "F.SilkS")',
        '    (effects (font (size 1.0 1.0) (thickness 0.12))))',
        f'  (gr_text "NO CEM / SlimSAS / MCIO invented"',
        f'    (at {hx0+HOST_STRIP/2+8:.3f} {170:.3f} 90) (layer "F.SilkS")',
        '    (effects (font (size 1.0 1.0) (thickness 0.12))))',
        f'  (gr_text "X11DPH-T NOT ON THIS PCB"',
        f'    (at {hx0+HOST_STRIP/2+16:.3f} {170:.3f} 90) (layer "F.SilkS")',
        '    (effects (font (size 1.1 1.1) (thickness 0.14))))',
        f'  (gr_rect (start {b0:.3f} {b1:.3f}) (end {b2:.3f} {b3:.3f})',
        '    (stroke (width 0.25) (type dash)) (fill none) (layer "F.CrtYd"))',
        f'  (gr_rect (start {b0:.3f} {b1:.3f}) (end {b2:.3f} {b3:.3f})',
        '    (stroke (width 0.2) (type dash)) (fill none) (layer "Dwgs.User"))',
        f'  (gr_text "U_SW1 DNP"',
        f'    (at {hx0+HOST_STRIP/2:.3f} {304:.3f} 90) (layer "F.SilkS")',
        '    (effects (font (size 1.4 1.4) (thickness 0.16))))',
        f'  (gr_text "PM8536B-FEI 37.5mm 1311-FCBGA"',
        f'    (at {hx0+HOST_STRIP/2+8:.3f} {304:.3f} 90) (layer "F.SilkS")',
        '    (effects (font (size 1.0 1.0) (thickness 0.12))))',
        f'  (gr_text "seats 4-7  x8/GCD  16US+64DS"',
        f'    (at {hx0+HOST_STRIP/2+16:.3f} {304:.3f} 90) (layer "F.SilkS")',
        '    (effects (font (size 0.9 0.9) (thickness 0.1))))',
        f'  (gr_text "STAR-FED P48V — LOCAL POURS ONLY — DO NOT ENERGIZE"',
        f'    (at {BOARD_W/2:.3f} {BOARD_H-12:.3f}) (layer "F.SilkS")',
        '    (effects (font (size 1.8 1.8) (thickness 0.22))))',
        f'  (gr_text "12L 2.0mm stuffed-switch TARGET. 8L 2.0mm is cheaper DNP option only. No signal tracks yet."',
        f'    (at {BOARD_W/2:.3f} 16.5) (layer "Cmts.User")',
        '    (effects (font (size 1.2 1.2) (thickness 0.14))))',
        f'  (gr_text "Seat grid: row0 (Y={MARGIN:.0f}) seats 0-3; row1 (Y={MARGIN+KOZ_H:.0f}) seats 4-7; col pitch {KOZ_W:.0f} mm. Conn rotation 180 Inferred."',
        f'    (at {BOARD_W/2:.3f} {BOARD_H-18:.3f}) (layer "Cmts.User")',
        '    (effects (font (size 1.2 1.2) (thickness 0.14))))',
        f'  (gr_text "P48V STAR / Kelvin sense"',
        f'    (at {sx:.3f} {sy-32:.3f}) (layer "F.SilkS")',
        '    (effects (font (size 1.4 1.4) (thickness 0.16))))',
        f'  (gr_text "off-board 48V via 2 AWG  |  NOT D3000E-S1 12V"',
        f'    (at {sx+55:.3f} {sy:.3f}) (layer "F.SilkS")',
        '    (effects (font (size 1.1 1.1) (thickness 0.14))))',
        f'  (gr_rect (start 118 {BOARD_H-18:.3f}) (end 148 {BOARD_H-6:.3f})',
        '    (stroke (width 0.15) (type dash)) (fill none) (layer "F.CrtYd"))',
        f'  (gr_text "P12V1 in <=50W  MPN Unknown  no VRM"',
        f'    (at 133 {BOARD_H-12:.3f}) (layer "F.SilkS")',
        '    (effects (font (size 0.9 0.9) (thickness 0.1))))',
        f'  (gr_rect (start 152 {BOARD_H-18:.3f}) (end 182 {BOARD_H-6:.3f})',
        '    (stroke (width 0.15) (type dash)) (fill none) (layer "F.CrtYd"))',
        f'  (gr_text "P3V3 in <=5W  MPN Unknown  no VRM"',
        f'    (at 167 {BOARD_H-12:.3f}) (layer "F.SilkS")',
        '    (effects (font (size 0.9 0.9) (thickness 0.1))))',
        f'  (gr_text "P12V2 pads named v1.0 — Unknown / may be NC — do not short to P12V1"',
        f'    (at 280 {BOARD_H-12:.3f}) (layer "Cmts.User")',
        '    (effects (font (size 1.0 1.0) (thickness 0.12))))',
    ]

    fw, fh = 20.0, 12.0
    for oam, fcx, fcy in fuse_centers:
        graphics += [
            f'  (gr_rect (start {fcx-fw/2:.3f} {fcy-fh/2:.3f}) (end {fcx+fw/2:.3f} {fcy+fh/2:.3f})',
            '    (stroke (width 0.2) (type dash)) (fill none) (layer "F.CrtYd"))',
            f'  (gr_rect (start {fcx-fw/2:.3f} {fcy-fh/2:.3f}) (end {fcx+fw/2:.3f} {fcy+fh/2:.3f})',
            '    (stroke (width 0.15) (type dash)) (fill none) (layer "Dwgs.User"))',
            f'  (gr_text "~15A FUSE S{oam}  MPN Unknown"',
            f'    (at {fcx:.3f} {fcy:.3f}) (layer "F.SilkS")',
            '    (effects (font (size 0.8 0.8) (thickness 0.1))))',
            f'  (gr_line (start {sx:.3f} {sy-8:.3f}) (end {fcx:.3f} {fcy:.3f})',
            '    (stroke (width 0.12) (type dash)) (layer "Dwgs.User"))',
        ]

    zones = []
    # Local P48V pours — F.Cu only, one island per seat, 16 verified pads. Not a flood.
    for oam, x0, y0, x1, y1 in p48_bboxes:
        zones.append(zone(
            p48_id, "P48V", "F.Cu", P48V_CLEAR_MM,
            [(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
            priority=20,
        ))
        graphics += [
            f'  (gr_rect (start {x0:.3f} {y0:.3f}) (end {x1:.3f} {y1:.3f})',
            '    (stroke (width 0.12) (type solid)) (fill none) (layer "Dwgs.User"))',
        ]
    # Star copper at SB175 only (P48V_STAR), not tied to seat P48V until fuse is placed.
    star_poly = [(sx - 22, sy - 22), (sx + 22, sy - 22), (sx + 22, sy + 6), (sx - 22, sy + 6)]
    zones.append(zone(star_id, "P48V_STAR", "F.Cu", P48V_CLEAR_MM, star_poly, priority=15))
    # Inner GND planes — board-wide return. Not a P48V flood.
    gnd_poly = [(2.0, 2.0), (BOARD_W - 2.0, 2.0), (BOARD_W - 2.0, BOARD_H - 2.0), (2.0, BOARD_H - 2.0)]
    zones.append(zone(gnd_id, "GND", "In1.Cu", GND_CLEAR_MM, gnd_poly, priority=0))
    zones.append(zone(gnd_id, "GND", "In4.Cu", GND_CLEAR_MM, gnd_poly, priority=0))
    zones.append(zone(gnd_id, "GND", "In7.Cu", GND_CLEAR_MM, gnd_poly, priority=0))
    zones.append(zone(gnd_id, "GND", "In10.Cu", GND_CLEAR_MM, gnd_poly, priority=0))

    keepouts = [
        keepout_rect(*SW0_KEEPOUT),
        keepout_rect(*SW1_KEEPOUT),
        keepout_rect(*HOST_CABLE_KEEPOUT),
    ]
    for oam, fcx, fcy in fuse_centers:
        keepouts.append(keepout_rect(fcx - fw / 2, fcy - fh / 2, fcx + fw / 2, fcy + fh / 2))
    keepouts.append(keepout_rect(118.0, BOARD_H - 18.0, 148.0, BOARD_H - 6.0))
    keepouts.append(keepout_rect(152.0, BOARD_H - 18.0, 182.0, BOARD_H - 6.0))

    pcb = f'''(kicad_pcb (version {PCB_VER}) (generator "{GEN}") (generator_version "9.0")
  (general (thickness {BOARD_THICK_MM}))
  (paper "A1")
  (title_block
    (title "DO NOT FABRICATE — Rev3 8-seat PCBWay chassis stub")
    (date "2026-08-21")
    (rev "Rev3_8Seat_PCBWay_v1")
    (comment 1 "DO NOT FABRICATE. DO NOT ENERGIZE P48V. Molex 60V written; 1.2A/contact OPEN.")
    (comment 2 "492 x 372 mm 12-layer 2.0 mm stuffed-switch TARGET. Local P48V. 2x PM8536 DNP. SB175.")
  )
  (layers
    (0 "F.Cu" signal)
    (1 "In1.Cu" power)
    (2 "In2.Cu" signal)
    (3 "In3.Cu" signal)
    (4 "In4.Cu" power)
    (5 "In5.Cu" signal)
    (6 "In6.Cu" signal)
    (7 "In7.Cu" power)
    (8 "In8.Cu" signal)
    (9 "In9.Cu" signal)
    (10 "In10.Cu" power)
    (31 "B.Cu" signal)
    (37 "F.SilkS" user)
    (36 "B.SilkS" user)
    (39 "F.Mask" user)
    (38 "B.Mask" user)
    (41 "Cmts.User" user)
    (40 "Dwgs.User" user)
    (44 "Edge.Cuts" user)
    (45 "F.CrtYd" user)
    (49 "F.Fab" user)
  )
  (setup
    (pad_to_mask_clearance 0)
    (stackup
      (layer "F.Cu" (type "copper") (thickness {OZ2_UM}))
      (layer "dielectric 1" (type "prepreg") (thickness 0.11) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "In1.Cu" (type "copper") (thickness {OZ1_UM}))
      (layer "dielectric 2" (type "core") (thickness 0.15) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "In2.Cu" (type "copper") (thickness {OZ1_UM}))
      (layer "dielectric 3" (type "prepreg") (thickness 0.11) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "In3.Cu" (type "copper") (thickness {OZ1_UM}))
      (layer "dielectric 4" (type "core") (thickness 0.15) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "In4.Cu" (type "copper") (thickness {OZ1_UM}))
      (layer "dielectric 5" (type "prepreg") (thickness 0.11) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "In5.Cu" (type "copper") (thickness {OZ1_UM}))
      (layer "dielectric 6" (type "core") (thickness 0.15) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "In6.Cu" (type "copper") (thickness {OZ1_UM}))
      (layer "dielectric 7" (type "prepreg") (thickness 0.11) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "In7.Cu" (type "copper") (thickness {OZ1_UM}))
      (layer "dielectric 8" (type "core") (thickness 0.15) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "In8.Cu" (type "copper") (thickness {OZ1_UM}))
      (layer "dielectric 9" (type "prepreg") (thickness 0.11) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "In9.Cu" (type "copper") (thickness {OZ1_UM}))
      (layer "dielectric 10" (type "core") (thickness 0.15) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "In10.Cu" (type "copper") (thickness {OZ1_UM}))
      (layer "dielectric 11" (type "prepreg") (thickness 0.11) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "B.Cu" (type "copper") (thickness {OZ2_UM}))
    )
  )
{net_decls}
{chr(10).join(graphics)}
{chr(10).join(hole_blocks)}
{chr(10).join(fp_blocks)}
{chr(10).join(zones)}
{chr(10).join(keepouts)}
)
'''
    (ROOT / f"{PROJ}.kicad_pcb").write_text(pcb)

    nl = ROOT / "netlist/named_nets.csv"
    with nl.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["net", "oam", "connector", "pads"])
        grouped = defaultdict(list)
        for r in rows:
            for oam in range(N_SEATS):
                n = net_name(oam, r["signal"])
                if n:
                    grouped[(n, oam, r["connector"])].append(r["pin"])
        for (n, oam, conn), plist in sorted(grouped.items()):
            w.writerow([n, oam, conn, " ".join(plist)])
        w.writerow(["P48V_STAR", "", "J_SB175", "1 K+"])


def write_project() -> None:
    (ROOT / "fp-lib-table").write_text(
        '(fp_lib_table\n  (lib (name "footprints")(type "KiCad")(uri "${KIPRJMOD}/footprints")(options "")(descr "218910-1115 + Anderson SB175 geometry candidates"))\n)\n'
    )
    (ROOT / "sym-lib-table").write_text(
        '(sym_lib_table\n  (lib (name "OAM_v10_mapped")(type "KiCad")(uri "${KIPRJMOD}/symbols/OAM_v10_mapped.kicad_sym")(options "")(descr "v1.0 OCP generic named pads"))\n)\n'
    )
    pro = {
        "board": {
            "design_settings": {
                "defaults": {
                    "board_outline_line_width": 0.1,
                    "copper_line_width": 0.2,
                    "courtyard_line_width": 0.05,
                    "silk_line_width": 0.12,
                },
                "rules": {"min_clearance": 0.1, "min_track_width": 0.1},
                "track_widths": [0.1, 0.2, 0.5, 1.0, 2.0],
                "via_dimensions": [{"diameter": 0.6, "drill": 0.3}],
            }
        },
        "boards": [],
        "cvpcb": {"equivalence_files": []},
        "libraries": {"pinned_footprint_libs": [], "pinned_symbol_libs": []},
        "meta": {"filename": f"{PROJ}.kicad_pro", "version": 3},
        "net_settings": {
            "classes": [
                {"name": "Default", "clearance": 0.2, "track_width": 0.25},
                {"name": "P48V", "clearance": 0.64, "track_width": 2.0, "nets": ["P48V", "P48V_STAR"]},
                {"name": "GND", "clearance": 0.25, "track_width": 0.5, "nets": ["GND"]},
            ],
            "meta": {"version": 2},
        },
        "pcbnew": {"last_paths": {"netlist": "", "plot": ""}, "page_layout_descr_file": ""},
        "schematic": {"annotate_start_num": 0},
        "sheets": [[f"{PROJ}.kicad_sch", "Root"]] + [[rel, name] for name, rel in SHEETS],
        "text_variables": {
            "DO_NOT_FABRICATE": "true",
            "DO_NOT_ENERGIZE": "true",
            "PINMAP": "OAM Pin map rev 1.0.xlsx OCP Generic Pin Map",
        },
    }
    (ROOT / f"{PROJ}.kicad_pro").write_text(json.dumps(pro, indent=2) + "\n")


def write_ipc_netlist(rows: list[dict]) -> None:
    lines = [
        "# Open-MI250X 8-OAM v1.0 named-net stub (PCBWay chassis)",
        "# NOT a fabrication netlist. Unmapped pads omitted.",
        "# All 8 seats electrically named. S1-S7 / TEST* omitted. SB175 = P48V_STAR.",
        "# Format: ref.pad  net",
    ]
    for oam in range(N_SEATS):
        for conn, ref in (("Conn0", f"J{oam}_Conn0"), ("Conn1", f"J{oam}_Conn1")):
            for r in rows:
                if r["connector"] != conn:
                    continue
                n = net_name(oam, r["signal"])
                if n:
                    lines.append(f"{ref}.{r['pin']}\t{n}")
    lines.append("J_SB175.1\tP48V_STAR")
    lines.append("J_SB175.K+\tP48V_STAR")
    lines.append("J_SB175.2\tGND")
    lines.append("J_SB175.K-\tGND")
    (ROOT / f"netlist/{PROJ}.net").write_text("\n".join(lines) + "\n")


def main() -> None:
    rows = load_pinmap()
    if not FOOTPRINT_SRC.exists():
        raise SystemExit(f"missing footprint {FOOTPRINT_SRC}")
    sb175 = ROOT / "footprints/Anderson_SB175_2pole.kicad_mod"
    if not sb175.exists():
        raise SystemExit(f"missing footprint {sb175}")
    write_classification_csv(rows)
    write_symbol_lib(rows)
    write_project()
    write_root_sch()
    write_do_not_fab_sheet()
    write_power_clock_sheet()
    write_pcie_sheet()
    write_oam_connector_sheet(0, "sheets/03_oam0_connectors.kicad_sch")
    write_oam_connector_sheet(1, "sheets/04_oam1_connectors.kicad_sch")
    write_oam_connector_sheet(2, "sheets/05_oam2_connectors.kicad_sch")
    write_oam_connector_sheet(3, "sheets/06_oam3_connectors.kicad_sch")
    write_oam_connector_sheet(4, "sheets/07_oam4_connectors.kicad_sch")
    write_oam_connector_sheet(5, "sheets/08_oam5_connectors.kicad_sch")
    write_oam_connector_sheet(6, "sheets/09_oam6_connectors.kicad_sch")
    write_oam_connector_sheet(7, "sheets/10_oam7_connectors.kicad_sch")
    write_switch_unknown_sheet()
    write_unmapped_sheet(rows)
    write_pcb(rows)
    write_ipc_netlist(rows)
    meta = {
        "pinmap_csv": str(PINMAP.relative_to(REPO)),
        "xlsx_present": XLSX.exists(),
        "named_pads": len(rows),
        "unmapped_signal_names": sorted({r["signal"] for r in rows if is_unmapped(r["signal"])}),
        "shared_rails": sorted(SHARED_RAILS),
        "do_not_fabricate": True,
        "do_not_energize_p48v": True,
        "rev": "Rev3_8Seat_PCBWay_Chassis_v1",
        "molex_voltage_ticket": "167157",
        "molex_csa_60v": "COFC 80170713 written 2026-08-18 via Brian Park / ticket 167157",
        "molex_skip_pins": "published OCP P48V map satisfies Skip Pins; no extra NC pads",
        "molex_current_followup_open": "1.2 A per used power contact at 48-59.5 V (2 oz); skip/void NC on same MPN",
        "eli_ack": "2026-08-19",
        "layers": N_LAYERS,
        "layer_stack_target": "12L 2.0 mm stuffed-switch (8x-running)",
        "layer_stack_dnp_option": "8L 2.0 mm cheaper DNP-switch option only",
        "board_thickness_mm_planning": BOARD_THICK_MM,
        "copper_oz": {"F.Cu": 2, "inners": 1, "B.Cu": 2},
        "oam_seats": N_SEATS,
        "electrically_named_seats": list(range(N_SEATS)),
        "first_stuff_seats": sorted(FIRST_STUFF_SEATS),
        "sw0_seats": sorted(SW0_SEATS),
        "sw1_seats": sorted(SW1_SEATS),
        "connectors_per_seat": 2,
        "molex_mpn": "218910-1115",
        "molex_qty": 16,
        "molex_street_usd_each": [50, 96],
        "molex_mates_with": "2189101115 (hermaphroditic, self-mating)",
        "board_outline_mm": [BOARD_W, BOARD_H],
        "koz_reserve_mm": [N_COLS * KOZ_W, N_ROWS * KOZ_H],
        "koz_tiling": "4x2 of 103x166 INFERRED not a UBB drawing",
        "pcbway_adv_finished_ml_mm": list(PCBWAY_ADV_ML),
        "fits_pcbway_508x600": BOARD_W <= PCBWAY_ADV_ML[0] and BOARD_H <= PCBWAY_ADV_ML[1],
        "p3v3_count_conn0": sum(1 for r in rows if r["connector"] == "Conn0" and r["signal"] == "P3V3"),
        "p48v_pads_conn0": sorted(P48V_PADS),
        "p48v_pad_count_per_seat": 16,
        "npth_m35_count": N_SEATS * 4,
        "p48v_pour": "local_per_seat_F.Cu_not_board_wide_flood",
        "p48v_star_net": "P48V_STAR",
        "board_entry": "Anderson SB175 175A/600V long edge, 2 AWG",
        "p48v_not_tied_to": "Dell D3000E-S1 12V CRPS",
        "no_psu_shopping_on_pcb_bom": True,
        "fuse_per_seat_A": 15,
        "fuse_mpn": "Unknown",
        "pcie_switch_mpn": "PM8536B-FEI",
        "pcie_switch_qty_dnp": 2,
        "pcie_switch_package": "1311-ball 37.5 mm FCBGA 1.0 mm pitch",
        "pcie_switch_alt_docs_only": "PEX8780-AB80BI G 80-lane 35 mm",
        "host_connector_mpn": "Unknown",
        "host_uplinks": "two X11DPH-T CPU x16 to SW0/SW1",
        "xgmi_routed": False,
        "no_gpu_vrm": True,
        "pvref_driven": False,
        "p12v2_status": "named_v1.0_Unknown_may_be_NC",
        "signal_tracks": False,
        "inner_planes": {
            "In1.Cu": "GND", "In2.Cu": "signal_reserved", "In3.Cu": "signal_reserved",
            "In4.Cu": "GND", "In5.Cu": "signal_reserved", "In6.Cu": "signal_reserved",
            "In7.Cu": "GND", "In8.Cu": "signal_reserved", "In9.Cu": "signal_reserved",
            "In10.Cu": "GND",
        },
    }
    (ROOT / "netlist/generation_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from kicad9_fixup_sch import main as kicad9_fixup
    kicad9_fixup()
    print("generated", ROOT)
    print("outline_mm", BOARD_W, BOARD_H, "fits_508x600", meta["fits_pcbway_508x600"])


if __name__ == "__main__":
    main()
