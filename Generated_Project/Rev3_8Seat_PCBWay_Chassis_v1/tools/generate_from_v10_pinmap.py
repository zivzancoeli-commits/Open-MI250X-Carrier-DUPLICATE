#!/usr/bin/env python3
"""Generate the Rev3 8-seat PCBWay named-net chassis KiCad project.

Writes ONLY into Generated_Project/Rev3_8Seat_PCBWay_Chassis_v1/.
Never overwrites Rev1/Rev2/Rev3_2Seat. Writes only this DUPLICATE checkout.

Pin names: 22_Pinmap_Research/extracted/OAM_v1.0_OCP_Generic_Pin_Map.csv
(xlsx in downloads/ wins on mismatch).

Architecture:
- 8 electrically designed OAM seats (2→4→8 populate: seats 0-1, then 0-3, then all 8).
  16x Molex 218910-1115. Board 492 x 372 mm. 12-layer 2.0 mm stuffed-switch TARGET
  (plan 12-16L, not 4). 8-layer 2.0 mm is a documented cheaper DNP-switch option only.
- 4x2 tiling of 103x166 mm KOZ = 412x332 mm (INFERRED) + 20 mm margin + 40 mm host strip.
- Full-width-capable chassis: 16 named x16 PE buses (8x GCD0 Conn0 + 8x GCD1 named-only)
  toward four DNP PM8536B-FEI courtyards (SW0-SW3). Lane math: 8x2x16 = 256 DS;
  two 96-lane switches are enough for 8x x8/GCD, not 8x x16/GCD. Four 96-lane
  courtyards is the public-MPN answer. PEX8780 / PM8533 stay docs-only.
- Host stub: silk + connector keepout toward X11DPH-T (3x Gen3 x16 + 4x Gen3 x8 ~80 lanes).
  Chassis can SIT and be WIRED for 8 full-width; this host CANNOT LIGHT 8 full-width.
  Four named US x16 keepouts. Do NOT invent a CEM/MCIO MPN. Do not swap the host board.
- Do not route S1-S7 (no xGMI). TEST*/RFU/DO_NOT_USE unmapped. Never drive PVREF.
- HOST_PWRGD is ENABLE. No GPU multiphase VRM on this PCB.
- P48V: Anderson 6325G1 + 2x 1382 (SB175) + per-seat Littelfuse 0476015.MR 15 A
  + LOCAL pours on the 16 verified Conn0 P48V pads. NOT a board-wide 100 A plane.
- P12V1: TRACO THL 40-4812WI from 48 V (40 W first-article; OCP allows <=50 W).
  P3V3: Murata OKI-78SR-3.3/1.5-W36-C from P12V1. No GPU multiphase VRM.
- PM8536B-FEI ball map is not public — DNP courtyards. POWER+MECH first article.
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

from fab_copper import MEZZ_ZONE_CLEAR_MM, build as build_fab_copper, p48_net

ROOT = Path(__file__).resolve().parents[1]
if ROOT.name != "Rev3_8Seat_PCBWay_Chassis_v1":
    raise SystemExit(f"refusing to write outside Rev3 8-seat tree: {ROOT}")
if "Rev1_" in str(ROOT) or "Rev2_" in str(ROOT) or "Rev3_2Seat" in str(ROOT):
    raise SystemExit(f"refusing to overwrite Rev1/Rev2/2-seat trees: {ROOT}")

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
P12V1_PADS = {"A59", "A60", "A61", "A62", "B62"}
P3V3_PADS = {"C1", "C2"}

N_SEATS = 8
N_COLS = 4
N_ROWS = 2
KOZ_W, KOZ_H = 103.0, 166.0
MOD_W, MOD_H = 102.0, 165.0
MARGIN = 20.0
HOST_STRIP = 40.0
BOARD_W = MARGIN + N_COLS * KOZ_W + MARGIN + HOST_STRIP  # 492
BOARD_H = MARGIN + N_ROWS * KOZ_H + MARGIN              # 372
HOST_PCIE_SEATS = {0, 1, 2, 3, 4, 5, 6, 7}  # all 8 electrically named
FIRST_STUFF_SEATS = {0, 1}          # populate path step 1 (stuff SW0 later)
SECOND_STUFF_SEATS = {0, 1, 2, 3}   # populate path step 2 (stuff SW0+SW1)
# One 96-lane switch per two seats: 2 seats × 2 GCD × x16 = 64 DS + 16 US.
N_SWITCHES = 4
SWITCH_SEATS = {
    0: {0, 1},
    1: {2, 3},
    2: {4, 5},
    3: {6, 7},
}
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
N_LAYERS = 12  # stuffed-switch TARGET (four 1311-ball 1.0 mm PM8536 DNP). 8L 2.0 mm is docs-only DNP-switch.
BOARD_THICK_MM = 2.0
OZ2_UM = 0.070
OZ1_UM = 0.035
P48V_CLEAR_MM = 0.64  # OCP UBB v1.5 >40 V internal 25 mil
GND_CLEAR_MM = 0.25
# SB175 on-board in the south margin (NPTH copper inside Edge.Cuts). Housing 6325G1.
SB175_AT = (70.0, 354.0)
# PRIMARY: four Microchip PM8536B-FEI DNP courtyards. Switchtec PFX 96-lane Gen3,
# 1311-ball 37.5 mm FCBGA, 1.0 mm pitch. ~$460-475, ~18 wk.
# Lane math (verified; not a ball map / not a locked pinout):
#   8 × 2 GCD × x16 = 256 downstream. 2×96 = 192 — enough for 8× x8/GCD
#   (128 DS + uplinks), NOT 256 DS. 4×96 = 384. Example partition: each SW
#   16 US + 64 DS (two seats × two GCD × x16) = 80 of 96, 16 spare.
#   4 × 16 US = 64 host-facing vs X11DPH-T ~80. Chassis WIRED for 4× US x16;
#   this host CANNOT LIGHT 256 DS. x8/GCD remains a stuffing option if only
#   SW0+SW1 are populated.
# PCBWay can assemble 1.0 mm without HDI; plan 12-16 layers (not 4).
# Host strip is 40 mm; 37.5 mm body + 1.25 mm per side. Four 40 mm courtyards
# stacked in Y; 12 V brick cluster sits south of SW3 (y>=332).
# PEX8780-AB80BI G is a cheaper 80-lane alt in docs only — not placed
# (80 lanes is exactly 16 US+64 DS with no spare; still too small to replace
# four 96-lane courtyards with two chips).
# PM8533B-F3EI (48-lane, 27 mm) is a 2-seat alt in docs only — not placed.
PM8536_MPN = "PM8536B-FEI"
PM8536_BODY_MM = 37.5
PM8536_CRTYD_MM = 40.0
SW_KEEPOUTS = {
    0: (452.0, 16.0, 492.0, 56.0),     # seats 0-1 first stuff
    1: (452.0, 62.0, 492.0, 102.0),    # seats 2-3
    2: (452.0, 248.0, 492.0, 288.0),   # seats 4-5
    3: (452.0, 292.0, 492.0, 332.0),   # seats 6-7
}
SW_SILK_Y = {0: 36.0, 1: 82.0, 2: 268.0, 3: 312.0}
# X11DPH-T cable keepout (four named US x16 toward host). MPN Unknown — no CEM invented.
HOST_CABLE_KEEPOUT = (452.0, 110.0, 492.0, 244.0)
HOST_SILK_Y = 177.0


def switch_for_seat(oam: int) -> int:
    """SW0=seats 0-1, SW1=2-3, SW2=4-5, SW3=6-7."""
    return oam // 2


def pe_named_buses() -> list[str]:
    """Architectural PE names. GCD0 pads stay OAM{n}_PCIE_* (OCP Conn0).
    GCD1 is named-only (overlay Unknown; not assigned to S1-S7)."""
    names = []
    for oam in range(N_SEATS):
        names.append(f"PE_S{oam}_GCD0_x16")
        names.append(f"PE_S{oam}_GCD1_x16")
    for sw in range(N_SWITCHES):
        names.append(f"PE_SW{sw}_US_x16")
    return names


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
        if signal == "P48V":
            return p48_net(oam)
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
                    "Conn0 16-lane PCIE bus = PE_S{n}_GCD0_x16 (OCP-named pads) toward "
                    "four DNP PM8536B-FEI (SW0-SW3, 2 seats each). PE_S{n}_GCD1_x16 is "
                    "named-only (overlay Unknown; not S1-S7). Full-width capable chassis; "
                    "X11DPH-T cannot light 256 DS. Not a CEM mapping."
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
        f'  (property "ki_description" "OCP generic v1.0 {conn} 688-contact map. NOT AMD MI250X overlay. DO NOT ENERGIZE P48V." (at 0 0 0) (effects (font (size 1.27 1.27)) hide))',
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
		(date "2026-08-22")
		(rev "Rev3_8Seat_PCBWay_v1")
        (comment 1 "DO NOT ENERGIZE P48V. Molex 60V written 2026-08-18; 1.2A/contact OPEN. Skip-pin NC.")
        (comment 2 "{kicad_escape(comment)}")
        (comment 3 "Pin names: OAM Pin map rev 1.0.xlsx — OCP generic, NOT AMD overlay")
        (comment 4 "r2.0 UNUSABLE. P3V3=Conn0 C1/C2. 12L 2.0mm stuffed-switch TARGET. 4x PM8536 DNP. Star-fed P48V.")
	)
'''


SHEETS = [
    ("00_DO_NOT_FABRICATE", "sheets/00_do_not_fabricate.kicad_sch"),
    ("01_Power_Clock_Reset", "sheets/01_power_clock_reset.kicad_sch"),
    ("02_Host_PCIe_Named_8Seat", "sheets/02_host_pcie_stub.kicad_sch"),
    ("03_OAM0_Connectors", "sheets/03_oam0_connectors.kicad_sch"),
    ("04_OAM1_Connectors", "sheets/04_oam1_connectors.kicad_sch"),
    ("05_OAM2_Connectors", "sheets/05_oam2_connectors.kicad_sch"),
    ("06_OAM3_Connectors", "sheets/06_oam3_connectors.kicad_sch"),
    ("07_OAM4_Connectors", "sheets/07_oam4_connectors.kicad_sch"),
    ("08_OAM5_Connectors", "sheets/08_oam5_connectors.kicad_sch"),
    ("09_OAM6_Connectors", "sheets/09_oam6_connectors.kicad_sch"),
    ("10_OAM7_Connectors", "sheets/10_oam7_connectors.kicad_sch"),
    ("11_PM8536_DNP_x4", "sheets/11_pcie_switch_unknown.kicad_sch"),
    ("12_Unmapped_AMD", "sheets/12_unmapped_amd.kicad_sch"),
]


def write_root_sch() -> None:
    p = ROOT / f"{PROJ}.kicad_sch"
    body = sch_header(
        "Rev3 8-seat PCBWay POWER+MECH first article (DO NOT ENERGIZE P48V)",
        "8 OAM seats. Host X11DPH-T is NOT on this PCB. Chassis full-width capable; host cannot light 256 DS. No CEM cable.",
    )
    note = (
        "DO NOT ENERGIZE P48V — POWER+MECH first article (4x PM8536 DNP)\\n"
        "8 electrically designed OAM seats. Populate 2 (0-1) then 4 (0-3) then 8 — no respin.\\n"
        "16x Molex 218910-1115, 5.00 mm stack. 12-layer 2.0 mm stuffed-switch TARGET. Outline 492 x 372 mm.\\n"
        "4x2 of 103x166 mm KOZ = 412x332 mm INFERRED tiling (not a UBB drawing).\\n"
        "FULL-WIDTH CAPABLE: 16x x16 PE names (PE_Sn_GCD0_x16 + PE_Sn_GCD1_x16) toward 4x PM8536B-FEI DNP.\\n"
        "Chassis can SIT/WIRE 8 full-width. Host X11DPH-T ~80 lanes CANNOT LIGHT 256 DS. No CEM invented.\\n"
        "X11DPH-T / NH-D9 DX-3647 / B550M are NOT on this PCB. Do not swap or design the host board.\\n"
        "S1-S7 NOT routed (no xGMI). TEST*/RFU/DO_NOT_USE unmapped. PVREF never driven.\\n"
        "P48V: SB175 (6325G1+2x1382) + 0476015.MR 15A/seat + LOCAL pours. NOT a 100A flood.\\n"
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
    text = """GATE LIST — energize / stuffing. POWER+MECH Gerbers are in fab/. Eli uploads; this agent does not.

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
6. PCIe: chassis is full-width capable (16 named x16 PE buses, 4x PM8536B-FEI DNP).
   SW0=seats 0-1, SW1=2-3, SW2=4-5, SW3=6-7. Each 16 US + 64 DS (hypothesis, not a ball map).
   Two 96-lane switches are enough for 8x x8/GCD, not 8x x16/GCD. Host X11DPH-T ~80 lanes
   cannot light 256 DS. Four named US x16 keepouts. PEX8780 is docs-only cheaper 80-lane alt.
   No CEM cable invented. Host MPN Unknown. Do not stuff PM8536 this article. Do not swap the host.
7. HOST_PWRGD is ENABLE. Sequencing vs P48V/P12V1/P3V3 — OCP + AMD overlay only.
8. Do not reuse the old MFC qty-5 cart for 220x120 mm. That quote is UNRELATED.
9. Per-seat fuse Littelfuse 0476015.MR 15 A. P12V1 = THL 40-4812WI (40 W first article).
   P3V3 = OKI-78SR-3.3/1.5-W36-C from P12V1. No GPU multiphase VRM on this PCB.
10. Do not upload to PCBWay from this agent. 12L 2.0 mm stuffed-switch TARGET (plan 12-16L, not 4);
    8L 2.0 mm is a cheaper DNP-switch option only.

Fab zip is POWER+MECH. Do not stuff the DNP switches. DO NOT ENERGIZE P48V.
"""
    write_text_sheet("sheets/00_do_not_fabricate.kicad_sch", "ENERGIZE / STUFFING GATES (fab zip in fab/)", text)


def write_power_clock_sheet() -> None:
    text = """PURPOSE: Named power / clock / reset stubs from OAM v1.0 pin map.

STAR-FED P48V (NOT a board-wide 100 A plane):
- Board entry: Anderson SB175 (175 A / 600 V) on the long edge, 2 AWG landing.
  Net P48V_STAR. Kelvin+ / Kelvin- pads at the star. Off-board 48 V is NOT a PCB BOM item.
- Dell D3000E-S1 is 12 V CRPS — do not tie OAM P48V to it. 1000 W ATX/EPS is HOST only.
- Per seat: Littelfuse 0476015.MR (15 A, 125 VDC Nano2), then the 16 verified OCP v1.0 Conn0
  P48V pads. Local 2 oz F.Cu pour around those 16 pads only. No extra NC/skip pads.
  Seat nets are P48V / P48V_S1..S7 so the fuses actually isolate.
- Molex 2026-08-18 written yes: CSA 60 V (COFC 80170713) at OCP P48V.
  OPEN: 1.2 A/contact at 48-59.5 V (2 oz). DO NOT ENERGIZE.

SHARED RAILS (OCP names, pads on every seat):
- P48V  Conn0 16 pads  44-59.5 V  up to 700 W class (pin list). MI250X 500/560 W.
        LOCAL pours only. Module has the 48 V core VRMs — no GPU multiphase here.
- P12V1 Conn0 5 pads   12 V infrastructure up to 50 W. Carrier supplies THL 40-4812WI (40 W first article).
        No GPU VRM.
- P12V2 Conn0 27 pads  12 V main for 12V-based OAM. MI250X is 48 V class.
        Unknown / may be NC. Do NOT short to P12V1. Do not invent a P12V2 supply.
- P3V3  Conn0 C1,C2    3.3 V up to 5 W. Carrier supplies OKI-78SR-3.3/1.5-W36-C from P12V1.
- GND   Conn0 majority. Inner GND planes (In1, In4), 2 oz planning.
- PVREF Conn0 G1,G2    MODULE OUTPUT. NEVER drive from carrier. Per-OAM nets.

CLOCK / RESET named on ALL 8 seats (no respin to light 2-7):
- PE_REFCLKP/N, PERST#, HOST_PWRGD (ENABLE), plus WARMRST# / MODULE_PWRGD / PWRBRK# / PRSNT*
- HOST_PWRGD is ENABLE (OCP: Power Enable when P48V/P12V1/P12V2/P3V3 are in spec).

First stuffing may populate 2 modules / 6 DNP (seats 0-1), then 0-3, then all 8. Same nets.

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
    text = """PURPOSE: Named v1.0 PCIE_TXnP/N and PCIE_RXnP/N (n=0..15) on ALL 8 seats
plus 16 architectural x16 PE names (full-width capable chassis).

8 electrically designed seats. Populate 2 (seats 0-1) then 4 (0-3) then 8 —
the PCB does not require a respin.

OCP pin list (module POV):
- PETp/n = module TX, host RX. AC caps on motherboard/carrier — not placed.
- PERp/n = module RX, host TX. AC caps on motherboard/carrier — not placed.

This sheet does NOT map those pairs onto a CEM x16 connector pinout.
Do NOT invent a CEM cable, SlimSAS, MCIO, or retimer BOM.
Do NOT invent PE pin numbers or assign GCD1 onto S1-S7.

Architectural names (hierarchical labels; not a fake BGA pinout):
- PE_S{n}_GCD0_x16 = Conn0 16-lane PCIE bus (OCP-named pads OAM{n}_PCIE_*).
- PE_S{n}_GCD1_x16 = named only. Overlay Unknown. SERDES_7 as GCD1 PE is Inferred.
  Pins not assigned. Not S1-S7.
- PE_SW{k}_US_x16 = four host-facing x16 keepouts toward X11DPH-T.

Lane math (verified; not a locked root cause / not a ball map):
- Full width = 8 modules x 2 GCD x x16 = 256 downstream lanes on the carrier.
- PM8536B-FEI = 96-lane Gen3, 1311-ball 37.5 mm FCBGA 1.0 mm. Ball map not public.
- 2x96 = 192. Even with 16 US/switch: 160 DS — enough for 8x x8/GCD (128 DS), NOT 256 DS.
- 4x96 = 384. Hypothesis partition: each SW 16 US + 64 DS (2 seats x 2 GCD x x16)
  = 80 of 96, 16 spare. 4 x 16 US = 64 host-facing vs X11DPH-T ~80.
- Chassis can SIT and be WIRED for 8 full-width. This host CANNOT LIGHT 256 DS.
  Memory/CPU mix (2x Gold 6230, 64 GB DRAM + 1 TB PMem) does NOT add PCIe lanes.
- x8/GCD remains a stuffing option if only SW0+SW1 are populated.

SW0 = seats 0-1 (first stuff). SW1 = 2-3. SW2 = 4-5. SW3 = 6-7.
PEX8780-AB80BI G (80-lane 35 mm) is a cheaper alt in docs only — not placed.
PM8533B-F3EI (48-lane 27 mm) is a 2-seat alt in docs only — not placed.

X11DPH-T is NOT a part on this PCB. Do not swap or design a host board.
Chamber A B550M is NOT this PCB.
"""
    write_text_sheet("sheets/02_host_pcie_stub.kicad_sch", "Host PE stub (16x x16 names, 4x PM8536 DNP)", text)
    labels = []
    for oam in range(N_SEATS):
        for n in range(16):
            for pn in ("P", "N"):
                for txrx in ("TX", "RX"):
                    labels.append(f"OAM{oam}_PCIE_{txrx}{n}{pn}")
    append_hier_labels("sheets/02_host_pcie_stub.kicad_sch", labels, y0=130, dy=3.81)
    append_hier_labels("sheets/02_host_pcie_stub.kicad_sch", pe_named_buses(), x=200, y0=130, dy=6.0)


def write_oam_connector_sheet(oam: int, rel: str) -> None:
    sw = switch_for_seat(oam)
    seats = ",".join(str(s) for s in sorted(SWITCH_SEATS[sw]))
    if oam in FIRST_STUFF_SEATS:
        stuff = "FIRST STUFF (populate path 2: seats 0-1; stuff SW0 later)"
    elif oam in SECOND_STUFF_SEATS:
        stuff = "SECOND STUFF (populate path 4: seats 0-3; stuff SW0+SW1 later)"
    else:
        stuff = "EIGHT-SEAT STUFF (populate path 8; stuff SW2/SW3 later; no respin)"
    text = f"""OAM{oam} connector instances — {stuff}.

Footprint: Molex 218910-1115 candidate (geometry). Hermaphroditic — mates with itself
(Farnell 2189101115: Mates With 2189101115; mated height 5.00 mm).

Pad nets assigned on the PCB from the v1.0 CSV for this seat:
P48V/P12V1/P3V3/GND, Conn0 PE 16 lanes (PE_S{oam}_GCD0_x16) toward SW{sw} PM8536B-FEI DNP
(seats {seats}, 16 US + 64 DS hypothesis — not a ball map),
PE_S{oam}_GCD1_x16 named-only (pins Unknown; not S1-S7),
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
        f"PE_S{oam}_GCD0_x16", f"PE_S{oam}_GCD1_x16",
    ]
    write_text_sheet(rel, f"OAM{oam} connectors", text)
    append_hier_labels(rel, ports, y0=150)


def write_switch_unknown_sheet() -> None:
    text = """FOUR PM8536B-FEI KEEPOUTS — PRIMARY, DNP. No fake schematic pins. No invented ball map.

U_SW0  PM8536B-FEI  DNP  seats 0-1   16 US + 64 DS   first-stuff pair
U_SW1  PM8536B-FEI  DNP  seats 2-3   16 US + 64 DS   second-stuff pair
U_SW2  PM8536B-FEI  DNP  seats 4-5   16 US + 64 DS
U_SW3  PM8536B-FEI  DNP  seats 6-7   16 US + 64 DS

Package (Verified Microchip PFX table): 96-lane Gen3, 1311-ball 37.5 x 37.5 mm FCBGA,
1.0 mm pitch. Street ~$460-475, ~18 wk. PCBWay can assemble 1.0 mm without HDI;
plan 12-16 layers (not 4). 12L 2.0 mm is the stuffed-switch TARGET.
8L 2.0 mm is a cheaper DNP-switch / mezz+power option only.

Do NOT populate until Eli buys the parts. Courtyard/keepout only — a DNP box, no fake pins.

Lane math (verified; partition is a hypothesis, not a pinout):
- 8 x 2 x x16 = 256 DS. 2x96 = 192 — enough for 8x x8/GCD, NOT 8x x16/GCD.
- 4x96 = 384. Each SW: 16 US + 64 DS (2 seats x 2 GCD x x16) = 80 of 96.
- 4 x 16 US = 64 host-facing. X11DPH-T has ~80 lanes (3x x16 + 4x x8).
  Chassis can SIT/WIRE 8 full-width. This host CANNOT LIGHT 256 DS.

Named PE buses (no routing; ball map not public):
- PE_S0_GCD0_x16 .. PE_S7_GCD0_x16  (Conn0 OCP PCIE pads)
- PE_S0_GCD1_x16 .. PE_S7_GCD1_x16  (named only; pins Unknown; not S1-S7)
- PE_SW0_US_x16 .. PE_SW3_US_x16    (host-facing keepouts; no CEM MPN)

Cheaper 80-lane alt in docs only (not placed): PEX8780-AB80BI G, 35 mm 1156-FCBGA.
2-seat alt in docs only (not placed): PM8533B-F3EI (48-lane, 27 mm, 1.0 mm).

Each MI250X GCD has its own PCIe Gen4 x16 (AMD + Hot Chips 34). Host trains Gen3.
OAM v1.5: one PE x16 on Conn0; a second host x16 may be SERDES_7 on Conn1.
GCD1 = SERDES_7 is Inferred — NO public AMD overlay proving it. Do NOT route S1-S7.

Host X11DPH-T (NOT on this PCB): 3x Gen3 x16 + 4x Gen3 x8 = 80 Gen3 lanes.
Do not invent CEM / SlimSAS / MCIO / retimer / xGMI. Do not swap the host board.

Refclk / PERST# / HOST_PWRGD per seat per OAM v1.5
(HOST_PWRGD >= 100 ms after MODULE_PWRGD). AMD delays still Unknown.

Populate path: seats 0-1 + SW0, then seats 0-3 + SW1, then all 8 + SW2/SW3. Same PCB.
"""
    write_text_sheet("sheets/11_pcie_switch_unknown.kicad_sch", "PM8536B-FEI DNP x4 PRIMARY (keepout only)", text)
    append_hier_labels("sheets/11_pcie_switch_unknown.kicad_sch", pe_named_buses(), y0=150, dy=4.5)


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
    """12-layer stuffed-switch target: local P48V pours, GND planes, SB175, 4x PM8536 DNP keepouts."""
    pads = parse_footprint_pads()
    if len(pads) != 688:
        raise SystemExit(f"expected 688 footprint pads, got {len(pads)}")

    p48_local: list[tuple[float, float]] = []
    p12_local: list[tuple[float, float]] = []
    p3_local: list[tuple[float, float]] = []
    for pad, at, _size, _layers in pads:
        xs = at.split()
        xy = (float(xs[0]), float(xs[1]))
        if pad in P48V_PADS:
            p48_local.append(xy)
        if pad in P12V1_PADS:
            p12_local.append(xy)
        if pad in P3V3_PADS:
            p3_local.append(xy)
    if len(p48_local) != 16:
        raise SystemExit(f"expected 16 Conn0 P48V pads in footprint, got {len(p48_local)}")
    if len(p12_local) != 5:
        raise SystemExit(f"expected 5 Conn0 P12V1 pads in footprint, got {len(p12_local)}")
    if len(p3_local) != 2:
        raise SystemExit(f"expected 2 Conn0 P3V3 pads in footprint, got {len(p3_local)}")

    pad_sig = {(r["connector"], r["pin"]): r["signal"] for r in rows}
    p48_csv = [r["pin"] for r in rows if r["connector"] == "Conn0" and r["signal"] == "P48V"]
    if set(p48_csv) != P48V_PADS:
        raise SystemExit(f"CSV P48V pads {sorted(p48_csv)} != verified set {sorted(P48V_PADS)}")

    nets: dict[str, int] = {}

    def nid(name: str) -> int:
        if name not in nets:
            nets[name] = len(nets) + 1
        return nets[name]

    for n in ["GND", "P48V", "P12V1", "P12V2", "P3V3", "P48V_STAR", "P48V_BRICK"] + [
        p48_net(s) for s in range(1, N_SEATS)
    ]:
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
    (descr "v1.0 mapped Molex 218910-1115. Skip-pin NC. DO NOT ENERGIZE P48V.")
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
    (descr "Anderson 6325G1 + 2x 1382 SB175 175A/600V on-board landing. DO NOT ENERGIZE. Not D3000E-S1.")
    (property "Reference" "J_SB175" (at -40 0) (layer "F.SilkS") (effects (font (size 1.2 1.2) (thickness 0.15))))
    (property "Value" "6325G1_SB175" (at 0 24) (layer "F.Fab") (effects (font (size 1 1) (thickness 0.15))))
    (fp_text user "6325G1 + 2x 1382 — Kelvin sense — DO NOT ENERGIZE P48V" (at -40 6) (layer "F.SilkS")
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

    net_decls = ""  # rebuilt after fab copper assigns P48V_BRICK etc.
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
        f'  (gr_text "DO NOT ENERGIZE P48V  /  Rev3 8-seat PCBWay POWER+MECH first article"',
        f'    (at {BOARD_W/2:.3f} 6) (layer "F.SilkS")',
        '    (effects (font (size 2.4 2.4) (thickness 0.3))))',
        f'  (gr_text "Molex 218910-1115 x16  |  12L 2.0mm TARGET  |  LOCAL P48V pours  |  4x PM8536B-FEI DNP  |  SB175 star  |  NOT a UBB"',
        f'    (at {BOARD_W/2:.3f} 12) (layer "F.SilkS")',
        '    (effects (font (size 1.5 1.5) (thickness 0.18))))',
        f'  (gr_text "4x2 of 103x166 mm KOZ = 412x332 mm INFERRED tiling. Outline {BOARD_W:.0f}x{BOARD_H:.0f} mm < PCBWay adv ML 508x600."',
        f'    (at {BOARD_W/2:.3f} {BOARD_H-6:.3f}) (layer "F.SilkS")',
        '    (effects (font (size 1.4 1.4) (thickness 0.18))))',
    ]

    fuse_centers: list[tuple[int, float, float]] = []
    p48_bboxes: list[tuple[int, float, float, float, float]] = []
    p12_bboxes: list[tuple[int, float, float, float, float]] = []
    p3_bboxes: list[tuple[int, float, float, float, float]] = []
    gnd_via_pts: list[tuple[float, float]] = []
    margin_p = 1.4
    for oam in range(N_SEATS):
        fx, fy = conn0_xy[oam]
        def _bbox(locals_xy):
            world = [fp_to_world(fx, fy, ROT, px, py) for px, py in locals_xy]
            xs = [p[0] for p in world]
            ys = [p[1] for p in world]
            return (min(xs) - margin_p, min(ys) - margin_p, max(xs) + margin_p, max(ys) + margin_p)
        x0, y0, x1, y1 = _bbox(p48_local)
        p48_bboxes.append((oam, x0, y0, x1, y1))
        p12_bboxes.append((oam, *_bbox(p12_local)))
        p3_bboxes.append((oam, *_bbox(p3_local)))
        row = oam // 4
        fuse_cx = x1 + 5.5
        fuse_cy = 169.5 if row == 0 else 336.0
        fuse_centers.append((oam, fuse_cx, fuse_cy))
    # Unique GND stitch vias in KOZ interior (not the south channel / P12 spines).
    seen = set()
    for oam in range(N_SEATS):
        kx, ky = koz_origin(oam)
        for a, b in ((10, 10), (KOZ_W - 10, 10), (10, 70), (KOZ_W - 10, 70)):
            pt = (round(kx + a, 3), round(ky + b, 3))
            if pt not in seen:
                seen.add(pt)
                gnd_via_pts.append(pt)

    for oam in range(N_SEATS):
        kx, ky = koz_origin(oam)
        mx, my = mod_origin(oam)
        cx = kx + KOZ_W / 2
        cy = ky + 8
        sw = switch_for_seat(oam)
        if oam in FIRST_STUFF_SEATS:
            role = f"SEAT {oam}  first-stuff  PE_S{oam}_GCD0+GCD1_x16 -> SW{sw}"
        elif oam in SECOND_STUFF_SEATS:
            role = f"SEAT {oam}  2nd-stuff (0-3)  PE_S{oam}_GCD0+GCD1_x16 -> SW{sw}"
        else:
            role = f"SEAT {oam}  8-seat  PE_S{oam}_GCD0+GCD1_x16 -> SW{sw}  no respin"
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
    h0, h1, h2, h3 = HOST_CABLE_KEEPOUT
    graphics += [
        f'  (gr_rect (start {hx0:.3f} {MARGIN:.3f}) (end {BOARD_W:.3f} {BOARD_H-MARGIN:.3f})',
        '    (stroke (width 0.25) (type solid)) (fill none) (layer "Dwgs.User"))',
        f'  (gr_text "FULL-WIDTH CAPABLE 16x x16 PE NAMES — HOST X11DPH-T CANNOT LIGHT 256 DS (~80 lanes)"',
        f'    (at {BOARD_W/2:.3f} 9.5) (layer "F.SilkS")',
        '    (effects (font (size 1.4 1.4) (thickness 0.16))))',
    ]
    for sw, (a0, a1, a2, a3) in SW_KEEPOUTS.items():
        seats = ",".join(str(s) for s in sorted(SWITCH_SEATS[sw]))
        silk_y = SW_SILK_Y[sw]
        graphics += [
            f'  (gr_rect (start {a0:.3f} {a1:.3f}) (end {a2:.3f} {a3:.3f})',
            '    (stroke (width 0.25) (type dash)) (fill none) (layer "F.CrtYd"))',
            f'  (gr_rect (start {a0:.3f} {a1:.3f}) (end {a2:.3f} {a3:.3f})',
            '    (stroke (width 0.2) (type dash)) (fill none) (layer "Dwgs.User"))',
            f'  (gr_text "U_SW{sw} DNP PRIMARY"',
            f'    (at {hx0+HOST_STRIP/2:.3f} {silk_y:.3f} 90) (layer "F.SilkS")',
            '    (effects (font (size 1.2 1.2) (thickness 0.14))))',
            f'  (gr_text "PM8536B-FEI 37.5mm 1311-FCBGA"',
            f'    (at {hx0+HOST_STRIP/2+7:.3f} {silk_y:.3f} 90) (layer "F.SilkS")',
            '    (effects (font (size 0.9 0.9) (thickness 0.1))))',
            f'  (gr_text "seats {seats}  64DS+16US  x16/GCD"',
            f'    (at {hx0+HOST_STRIP/2+14:.3f} {silk_y:.3f} 90) (layer "F.SilkS")',
            '    (effects (font (size 0.8 0.8) (thickness 0.1))))',
        ]
    graphics += [
        f'  (gr_rect (start {h0:.3f} {h1:.3f}) (end {h2:.3f} {h3:.3f})',
        '    (stroke (width 0.2) (type dash)) (fill none) (layer "F.CrtYd"))',
        f'  (gr_rect (start {h0:.3f} {h1:.3f}) (end {h2:.3f} {h3:.3f})',
        '    (stroke (width 0.15) (type dash)) (fill none) (layer "Dwgs.User"))',
        f'  (gr_text "HOST CABLE KEEPOUT"',
        f'    (at {hx0+HOST_STRIP/2:.3f} {HOST_SILK_Y:.3f} 90) (layer "F.SilkS")',
        '    (effects (font (size 1.4 1.4) (thickness 0.16))))',
        f'  (gr_text "4x named US x16 toward X11DPH-T"',
        f'    (at {hx0+HOST_STRIP/2-8:.3f} {HOST_SILK_Y:.3f} 90) (layer "F.SilkS")',
        '    (effects (font (size 1.0 1.0) (thickness 0.12))))',
        f'  (gr_text "3x x16 + 4x x8 Gen3 ~80 lanes  MPN Unknown"',
        f'    (at {hx0+HOST_STRIP/2+0:.3f} {HOST_SILK_Y:.3f} 90) (layer "F.SilkS")',
        '    (effects (font (size 0.9 0.9) (thickness 0.1))))',
        f'  (gr_text "NO CEM / SlimSAS / MCIO invented"',
        f'    (at {hx0+HOST_STRIP/2+8:.3f} {HOST_SILK_Y:.3f} 90) (layer "F.SilkS")',
        '    (effects (font (size 0.9 0.9) (thickness 0.1))))',
        f'  (gr_text "HOST CANNOT LIGHT 256 DS"',
        f'    (at {hx0+HOST_STRIP/2+16:.3f} {HOST_SILK_Y:.3f} 90) (layer "F.SilkS")',
        '    (effects (font (size 1.0 1.0) (thickness 0.12))))',
        f'  (gr_text "STAR-FED P48V — LOCAL POURS ONLY — DO NOT ENERGIZE"',
        f'    (at {BOARD_W/2:.3f} {BOARD_H-12:.3f}) (layer "F.SilkS")',
        '    (effects (font (size 1.8 1.8) (thickness 0.22))))',
        f'  (gr_text "12L 2.0mm stuffed-switch TARGET. 4x PM8536 DNP. 8L 2.0mm cheaper DNP option. PEX8780 docs-only. No signal tracks."',
        f'    (at {BOARD_W/2:.3f} {BOARD_H-22:.3f}) (layer "Cmts.User")',
        '    (effects (font (size 1.1 1.1) (thickness 0.12))))',
        f'  (gr_text "Populate 2 (0-1+SW0) then 4 (0-3+SW1) then 8 (+SW2/SW3). Same PCB. Conn rotation 180 Inferred."',
        f'    (at {BOARD_W/2:.3f} {BOARD_H-18:.3f}) (layer "Cmts.User")',
        '    (effects (font (size 1.2 1.2) (thickness 0.14))))',
        f'  (gr_text "P48V STAR / Kelvin sense"',
        f'    (at {sx - 40:.3f} {sy:.3f}) (layer "F.SilkS")',
        '    (effects (font (size 1.4 1.4) (thickness 0.16))))',
        f'  (gr_text "off-board 48V via 2 AWG  |  NOT D3000E-S1 12V"',
        f'    (at {sx+55:.3f} {sy:.3f}) (layer "F.SilkS")',
        '    (effects (font (size 1.1 1.1) (thickness 0.14))))',
        f'  (gr_text "P12V2 pads named v1.0 — Unknown / may be NC — do not short to P12V1"',
        f'    (at 280 {BOARD_H-12:.3f}) (layer "Cmts.User")',
        '    (effects (font (size 1.0 1.0) (thickness 0.12))))',
    ]

    for oam, fcx, fcy in fuse_centers:
        graphics += [
            f'  (gr_line (start {sx:.3f} {sy-8:.3f}) (end {fcx:.3f} {fcy:.3f})',
            '    (stroke (width 0.12) (type dash)) (layer "Dwgs.User"))',
        ]

    zones = []
    # Local P48V pours — F.Cu only, one island per seat. Mezz clearance is vendor 0.9 mm pitch.
    # Star copper lives in fab_copper (0.64 mm / 25 mil). Not a 100 A flood.
    for oam, x0, y0, x1, y1 in p48_bboxes:
        nname = p48_net(oam)
        zones.append(zone(
            nid(nname), nname, "F.Cu", MEZZ_ZONE_CLEAR_MM,
            [(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
            priority=20,
        ))
        graphics += [
            f'  (gr_rect (start {x0:.3f} {y0:.3f}) (end {x1:.3f} {y1:.3f})',
            '    (stroke (width 0.12) (type solid)) (fill none) (layer "Dwgs.User"))',
        ]
    # Inner GND planes — board-wide return. Not a P48V flood.
    gnd_poly = [(2.0, 2.0), (BOARD_W - 2.0, 2.0), (BOARD_W - 2.0, BOARD_H - 2.0), (2.0, BOARD_H - 2.0)]
    zones.append(zone(gnd_id, "GND", "In1.Cu", GND_CLEAR_MM, gnd_poly, priority=0))
    zones.append(zone(gnd_id, "GND", "In4.Cu", GND_CLEAR_MM, gnd_poly, priority=0))
    zones.append(zone(gnd_id, "GND", "In7.Cu", GND_CLEAR_MM, gnd_poly, priority=0))
    zones.append(zone(gnd_id, "GND", "In10.Cu", GND_CLEAR_MM, gnd_poly, priority=0))

    fab_fps, fab_tracks, fab_vias, fab_zones, fab_gfx = build_fab_copper(
        nid, p48_bboxes, fuse_centers, conn0_xy, p12_bboxes, p3_bboxes, gnd_via_pts,
    )
    fp_blocks.extend(fab_fps)
    zones.extend(fab_zones)
    graphics.extend(fab_gfx)

    keepouts = [keepout_rect(*SW_KEEPOUTS[i]) for i in range(N_SWITCHES)]
    keepouts.append(keepout_rect(*HOST_CABLE_KEEPOUT))

    net_decls = "\n".join(f'  (net {i} "{name}")' for name, i in sorted(nets.items(), key=lambda kv: kv[1]))

    pcb = f'''(kicad_pcb (version {PCB_VER}) (generator "{GEN}") (generator_version "9.0")
  (general (thickness {BOARD_THICK_MM}))
  (paper "A1")
  (title_block
    (title "DO NOT ENERGIZE P48V — Rev3 8-seat PCBWay POWER+MECH first article")
    (date "2026-08-22")
    (rev "Rev3_8Seat_PCBWay_v1")
    (comment 1 "DO NOT ENERGIZE P48V. Molex 60V written; 1.2A/contact OPEN. Skip-pin NC. Not D3000E-S1.")
    (comment 2 "492 x 372 mm 12-layer 2.0 mm. Local P48V. 4x PM8536 DNP. Full-width capable; host cannot light 256 DS.")
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
    (32 "B.Paste" user)
    (33 "F.Paste" user)
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
{chr(10).join(fab_tracks)}
{chr(10).join(fab_vias)}
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
        w.writerow(["P48V_BRICK", "", "U_P12V1", "1"])


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
                "rules": {"min_clearance": 0.15, "min_track_width": 0.15, "min_via_diameter": 0.6, "min_through_hole_diameter": 0.3},
                "track_widths": [0.15, 0.2, 0.5, 1.0, 2.0],
                "via_dimensions": [{"diameter": 0.6, "drill": 0.3}],
                "custom_rules": (
                    "(version 1)\n"
                    "(rule \"mezz Molex 0.9mm vendor pitch\"\n"
                    "  (constraint clearance (min 0.20mm))\n"
                    "  (condition \"A.Type == 'Pad' && B.Type == 'Pad' && "
                    "A.Parent.Reference =~ 'J[0-7]_Conn.*' && "
                    "B.Parent.Reference =~ 'J[0-7]_Conn.*'\"))\n"
                ),
            }
        },
        "boards": [],
        "cvpcb": {"equivalence_files": []},
        "libraries": {"pinned_footprint_libs": [], "pinned_symbol_libs": []},
        "meta": {"filename": f"{PROJ}.kicad_pro", "version": 3},
        "net_settings": {
            "classes": [
                {"name": "Default", "clearance": 0.2, "track_width": 0.25},
                {"name": "P48V", "clearance": 0.20, "track_width": 1.0,
                 "nets": ["P48V"] + [f"P48V_S{i}" for i in range(1, 8)]},
                {"name": "P48V_STAR", "clearance": 0.64, "track_width": 2.0, "nets": ["P48V_STAR", "P48V_BRICK"]},
                {"name": "GND", "clearance": 0.25, "track_width": 0.5, "nets": ["GND"]},
                {"name": "P12V1", "clearance": 0.20, "track_width": 0.5, "nets": ["P12V1"]},
                {"name": "P3V3", "clearance": 0.20, "track_width": 0.5, "nets": ["P3V3"]},
            ],
            "meta": {"version": 2},
        },
        "pcbnew": {"last_paths": {"netlist": "", "plot": ""}, "page_layout_descr_file": ""},
        "schematic": {"annotate_start_num": 0},
        "sheets": [[f"{PROJ}.kicad_sch", "Root"]] + [[rel, name] for name, rel in SHEETS],
        "text_variables": {
            "DO_NOT_FABRICATE": "false",
            "DO_NOT_ENERGIZE": "true",
            "PINMAP": "OAM Pin map rev 1.0.xlsx OCP Generic Pin Map",
        },
    }
    (ROOT / f"{PROJ}.kicad_pro").write_text(json.dumps(pro, indent=2) + "\n")


def write_ipc_netlist(rows: list[dict]) -> None:
    lines = [
        "# Rev3 8-seat PCBWay named-net chassis (v1.0 map)",
        "# NOT a fabrication netlist. Unmapped pads omitted.",
        "# All 8 seats electrically named. S1-S7 / TEST* omitted. SB175 = P48V_STAR.",
        "# PE_Sn_GCD0_x16 = Conn0 OCP PCIE pads. PE_Sn_GCD1_x16 named-only (not on pads).",
        "# Four PM8536 DNP. Full-width capable chassis; host cannot light 256 DS.",
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
    for s in range(N_SEATS):
        lines.append(f"F{s}.1\tP48V_STAR")
        lines.append(f"F{s}.2\t{p48_net(s)}")
    lines.append("F_P12.1\tP48V_STAR")
    lines.append("F_P12.2\tP48V_BRICK")
    lines.append("U_P12V1.1\tP48V_BRICK")
    lines.append("U_P12V1.2\tGND")
    lines.append("U_P12V1.3\tP12V1")
    lines.append("U_P12V1.5\tGND")
    lines.append("U_P3V3.1\tP12V1")
    lines.append("U_P3V3.2\tGND")
    lines.append("U_P3V3.3\tP3V3")
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
        "do_not_fabricate": False,
        "do_not_energize_p48v": True,
        "rev": "Rev3_8Seat_PCBWay_Chassis_v1",
        "molex_voltage_ticket": "167157",
        "molex_csa_60v": "COFC 80170713 written 2026-08-18 via Brian Park / ticket 167157",
        "molex_skip_pins": "published OCP P48V map satisfies Skip Pins; no extra NC pads",
        "molex_current_followup_open": "1.2 A per used power contact at 48-59.5 V (2 oz); skip/void NC on same MPN",
        "eli_ack": "2026-08-19",
        "layers": N_LAYERS,
        "layer_stack_target": "12L 2.0 mm stuffed-switch (four PM8536B-FEI DNP)",
        "layer_stack_dnp_option": "8L 2.0 mm cheaper DNP-switch / mezz+power option only",
        "board_thickness_mm_planning": BOARD_THICK_MM,
        "copper_oz": {"F.Cu": 2, "inners": 1, "B.Cu": 2},
        "oam_seats": N_SEATS,
        "electrically_named_seats": list(range(N_SEATS)),
        "first_stuff_seats": sorted(FIRST_STUFF_SEATS),
        "second_stuff_seats": sorted(SECOND_STUFF_SEATS),
        "populate_path": "seats 0-1 + SW0, then 0-3 + SW1, then all 8 + SW2/SW3; same PCB",
        "sw0_seats": sorted(SWITCH_SEATS[0]),
        "sw1_seats": sorted(SWITCH_SEATS[1]),
        "sw2_seats": sorted(SWITCH_SEATS[2]),
        "sw3_seats": sorted(SWITCH_SEATS[3]),
        "pe_named_buses": pe_named_buses(),
        "full_width_ds_lanes": 256,
        "host_gen3_lanes": 80,
        "chassis_can_wire_8_full_width": True,
        "host_can_light_8_full_width": False,
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
        "board_entry": "Anderson 6325G1 housing + 2x 1382 1/0 AWG contacts (SB175 175A/600V)",
        "p48v_not_tied_to": "Dell D3000E-S1 12V CRPS",
        "no_psu_shopping_on_pcb_bom": True,
        "fuse_per_seat_A": 15,
        "fuse_mpn": "0476015.MR",
        "fuse_brick_mpn": "0476002.MR",
        "p12v1_mpn": "THL 40-4812WI",
        "p12v1_watts_first_article": 40,
        "p3v3_mpn": "OKI-78SR-3.3/1.5-W36-C",
        "pm8536_pinout": "not_public_DNP_courtyard",
        "pcie_switch_mpn": "PM8536B-FEI",
        "pcie_switch_status": "PRIMARY_DNP",
        "pcie_switch_qty_dnp": 4,
        "pcie_switch_package": "1311-ball 37.5 mm FCBGA 1.0 mm pitch",
        "pcie_switch_lanes": 96,
        "pcie_switch_topology": "full-width capable: 4x PM8536 DNP; each 16US+64DS (2 seats x 2 GCD x x16, hypothesis not a ball map); 16 named x16 PE buses; 2x96 enough for 8x x8/GCD not 8x x16/GCD",
        "pcie_switch_street_usd": [460, 475],
        "pcie_switch_lead_wk": 18,
        "pcie_switch_alt_docs_only": "PEX8780-AB80BI G 80-lane 35 mm cheaper alt, not placed",
        "pcie_switch_2seat_alt_docs_only": "PM8533B-F3EI 48-lane 27 mm, not placed",
        "host_connector_mpn": "Unknown",
        "host_uplinks": "four named US x16 keepouts toward X11DPH-T; host ~80 lanes cannot light 256 DS",
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
