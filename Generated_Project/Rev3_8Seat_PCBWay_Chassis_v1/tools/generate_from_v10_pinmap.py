#!/usr/bin/env python3
"""Generate the Rev3 8-seat PCBWay chassis stub KiCad project.

Writes ONLY into Generated_Project/Rev3_8Seat_PCBWay_Chassis_v1/.
Never overwrites Rev1/Rev2/Rev3_2Seat. Never writes the original Open-MI250X-Carrier tree.

Pin names: 22_Pinmap_Research/extracted/OAM_v1.0_OCP_Generic_Pin_Map.csv
(xlsx in downloads/ wins on mismatch).

Architecture:
- 8 identical OAM seats, 16x Molex 218910-1115, 4-layer FR-4 stub.
- 4x2 tiling of 103x166 mm KOZ = 412x332 mm (INFERRED, not a UBB drawing) + 20 mm
  service margin + 40 mm host-stub strip = 492 x 372 mm outline (< PCBWay 508x600).
- Seats 0-1: named host PCIe nets toward a documented host-connector REGION.
  Do NOT invent a CEM cable / retimer BOM.
- Seats 2-7: mechanical + power pads only. PCIe/xGMI unrouted / no net.
  Silk: "needs on-board PCIe switch — MPN Unknown".
- Do not route S1-S7 between OAMs. TEST*/RFU/DO_NOT_USE unmapped.
- Do not drive PVREF. P48V pads exist, NO POUR, DO NOT ENERGIZE (ticket 167157).
- P3V3 = Conn0 C1/C2 only (never r2.0).
- M3.5 NPTH φ3.9 mm per OAM Fig 2 at each seat.
- DO NOT FABRICATE until Molex 60V/skip-pin and AMD overlay are closed.
"""
from __future__ import annotations

import csv
import json
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

N_SEATS = 8
N_COLS = 4
N_ROWS = 2
KOZ_W, KOZ_H = 103.0, 166.0
MOD_W, MOD_H = 102.0, 165.0
MARGIN = 20.0
HOST_STRIP = 40.0
BOARD_W = MARGIN + N_COLS * KOZ_W + MARGIN + HOST_STRIP  # 492
BOARD_H = MARGIN + N_ROWS * KOZ_H + MARGIN              # 372
HOST_PCIE_SEATS = {0, 1}
CONN0_MOD = (51.0, 31.5)
CONN1_MOD = (51.0, 133.5)
HOLES_MOD = [(6.0, 31.5), (96.0, 31.5), (6.0, 133.5), (96.0, 133.5)]
ROT = 180  # Inferred PIN A3 vs candidate land (same as Rev2 2-seat)

PCBWAY_ADV_ML = (508.0, 600.0)
PCBWAY_STD_ML = (560.0, 1150.0)


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
    """KiCad net for a v1.0 signal, or None if unmapped on this seat."""
    if is_unmapped(signal):
        return None
    sig = signal.replace(" ", "")
    if signal in SHARED_RAILS:
        return sig
    if oam not in HOST_PCIE_SEATS:
        # seats 2-7: mechanical + power pads only. PVREF named, never driven.
        if signal == "PVREF":
            return f"OAM{oam}_{sig}"
        return None
    return f"OAM{oam}_{sig}"


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
        header += ["wired_on_oam0_1", "notes"]
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
                note = "Named SerDes (xGMI/IF candidate). Named on seats 0-1 only; never routed between OAMs"
            elif cls == "module_output_do_not_drive":
                note = "Module output. Never drive from carrier. Per-OAM nets. Do not short seats together."
            elif cls == "power_shared":
                note = "OCP-named power/ground on all 8 seats. P48V NO POUR. DO NOT ENERGIZE."
            elif cls == "pcie_stub":
                note = "Named on seats 0-1 toward host region. Seats 2-7: no net (need on-board PCIe switch, MPN Unknown)."
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
		(comment 1 "DO NOT FABRICATE. DO NOT ENERGIZE P48V. Ticket 167157 open.")
		(comment 2 "{kicad_escape(comment)}")
		(comment 3 "Pin names: OAM Pin map rev 1.0.xlsx — OCP generic, NOT AMD overlay")
		(comment 4 "r2.0 maps UNUSABLE. P3V3=2 Conn0 C1/C2. 8-seat PCBWay chassis stub.")
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
    ("11_PCIe_Switch_Unknown", "sheets/11_pcie_switch_unknown.kicad_sch"),
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
        "8 identical OAM seats (populate 0-1 now, 2-7 later). Same board.\\n"
        "16x Molex 218910-1115, 5.00 mm stack. 4-layer FR-4. Outline 492 x 372 mm.\\n"
        "4x2 of 103x166 mm KOZ = 412x332 mm INFERRED tiling (not a UBB drawing).\\n"
        "Seats 0-1: named host PCIe nets toward HOST CONNECTOR REGION. No CEM invented.\\n"
        "Seats 2-7: mechanical+power only. needs on-board PCIe switch — MPN Unknown.\\n"
        "X11DPH-T: 3x Gen3 x16 + 4x Gen3 x8. NOT enough lanes for 8x MI250X (2 GCD, typically 2x x16).\\n"
        "S1-S7 NOT routed between OAMs. TEST*/RFU/DO_NOT_USE unmapped. PVREF never driven.\\n"
        "P48V pads exist, NO POUR. Molex catalog 30 V vs OCP 44-59.5 V, ticket 167157.\\n"
        "Dell D3000E-S1 is 12 V CRPS — do not mix. P3V3 = Conn0 C1/C2 only. Never r2.0."
    )
    body += f'''
	(lib_symbols
{power_symbol("P48V")}
{power_symbol("P12V1")}
{power_symbol("P12V2")}
{power_symbol("+3V3")}
{power_symbol("GND")}
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

1. 48V source identified AND harnessed to P48V pads (not Dell D3000E-S1 12V CRPS).
2. Molex 218910-1115 voltage vs P48V OPEN: catalog 30 V max vs OCP 44-59.5 V.
   Pending ticket 167157 / product spec 2189100001-PS-000.
3. Connector gender/stack: hermaphroditic 2189101115 mates with itself, 5 mm stack.
   Confirm PIN A3 orientation on a plot before tape-out (rotation 180 Inferred).
4. Cooling exists (OEM air HS or documented liquid). Do not clamp a custom cold plate on bare die.
5. AMD overlay unknowns (TEST*, dual-GCD PCIe, SMBus map, P12V2 need, xGMI S1-S7).
6. Host X11DPH-T is NOT on this PCB. Dual NH-U14S DX-3647 vs socket pitch: Unknown.
7. PCIe path: seats 0-1 named only, no CEM cable invented. Seats 2-7 need on-board
   PCIe switch — MPN Unknown. X11DPH-T Gen3 lane count cannot feed 8x MI250X.
8. HOST_PWRGD sequencing vs P48V/P12V1/P3V3 — implement only from OCP + AMD overlay.
9. Do not reuse the old MFC qty-5 cart for 220x120 mm. That quote is UNRELATED.

Until then this KiCad tree is a mapping artifact. Do not send to PCBWay. DO NOT ENERGIZE P48V.
"""
    write_text_sheet("sheets/00_do_not_fabricate.kicad_sch", "DO NOT FABRICATE", text)


def write_power_clock_sheet() -> None:
    text = """PURPOSE: Named power / clock / reset stubs from OAM v1.0 pin map.

SHARED RAILS (OCP names, all 8 OAMs — pads exist on every seat):
- P48V  Conn0 16 pads  44-59.5 V  up to 700 W class (pin list). MI250X 500/560 W.
        NO POUR. DO NOT ENERGIZE. Molex catalog 30 V vs OCP, ticket 167157.
- P12V1 Conn0 5 pads   12 V infrastructure up to 50 W. Required.
- P12V2 Conn0 27 pads  12 V main for 12V-based OAM. MI250X is 48 V class. AMD-unknown.
        Do NOT short to P12V1 unless documented.
- P3V3  Conn0 C1,C2    3.3 V up to 5 W. Required. 2 pins — matches v1.5 Table 4; r2.0 has 6.
- GND   Conn0 majority
- PVREF Conn0 G1,G2    MODULE OUTPUT. NEVER drive from carrier. Per-OAM nets on all 8 seats.

CLOCK / RESET named on seats 0-1 only (host-facing stub):
- PE_REFCLKP/N, PERST#, WARMRST#, HOST_PWRGD, MODULE_PWRGD, PWRBRK#, PRSNT0#/1#

Seats 2-7: mechanical+power pads only. Clock/PCIe/SerDes have no net on those seats.

DO NOT: invent VRMs, mix 12 V CRPS into P48V, drive PVREF, pour P48V copper,
or attach a guessed clock chip.
"""
    write_text_sheet("sheets/01_power_clock_reset.kicad_sch", "Power / clock / reset stub", text)
    path = ROOT / "sheets/01_power_clock_reset.kicad_sch"
    existing = path.read_text().rstrip()
    if existing.endswith(")"):
        existing = existing[:-1]
    flags = []
    x = 30.48
    for name, net in [("P48V", "P48V"), ("P12V1", "P12V1"), ("P12V2", "P12V2"),
                      ("+3V3", "P3V3"), ("GND", "GND")]:
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
    for oam in (0, 1):
        labs += [
            f"OAM{oam}_PE_REFCLKP", f"OAM{oam}_PE_REFCLKN", f"OAM{oam}_PERST#",
            f"OAM{oam}_HOST_PWRGD", f"OAM{oam}_MODULE_PWRGD", f"OAM{oam}_PVREF",
        ]
    for oam in range(2, 8):
        labs.append(f"OAM{oam}_PVREF")
    append_hier_labels("sheets/01_power_clock_reset.kicad_sch", labs, y0=170, dy=4.5)


def write_pcie_sheet() -> None:
    text = """PURPOSE: Host PCIe stub using ONLY v1.0 names PCIE_TXnP/N and PCIE_RXnP/N (n=0..15).

THIS SHEET IS SEATS 0 AND 1 ONLY.

OCP pin list (module POV):
- PETp/n = module TX, host RX. AC caps on motherboard/carrier — not placed.
- PERp/n = module RX, host TX. AC caps on motherboard/carrier — not placed.

This sheet does NOT map those pairs onto a CEM x16 connector pinout.
Do NOT invent a CEM cable, SlimSAS, MCIO, or retimer BOM.

Host: SuperMicro X11DPH-T is PCIe Gen3 (3x x16 + 4x x8).
Each MI250X module is 2 GCD, typically 2x x16. 8 modules need far more
host lanes than X11DPH-T provides. Seats 0-1 are the only named host-facing
PCIe nets, aimed at a documented HOST CONNECTOR REGION on the PCB (silk/courtyard,
no connector MPN).

Seats 2-7: see sheet 11. needs on-board PCIe switch — MPN Unknown.
X11DPH-T is NOT a part on this PCB.

Lane order, polarity invert, and dual-GCD (1x16 vs 2x8) need the AMD overlay.
PE_BIF[1:0] on Conn1 report bifurcation; AMD default Unknown.
"""
    write_text_sheet("sheets/02_host_pcie_stub.kicad_sch", "Host PCIe stub (OAM0-OAM1 only)", text)
    labels = []
    for oam in (0, 1):
        for n in range(16):
            for pn in ("P", "N"):
                for txrx in ("TX", "RX"):
                    labels.append(f"OAM{oam}_PCIE_{txrx}{n}{pn}")
    append_hier_labels("sheets/02_host_pcie_stub.kicad_sch", labels, y0=130, dy=3.81)


def write_oam_connector_sheet(oam: int, rel: str) -> None:
    if oam in HOST_PCIE_SEATS:
        text = f"""OAM{oam} connector instances — HOST-FACING SEAT (populate now).

Footprint: Molex 218910-1115 candidate (geometry). Hermaphroditic — mates with itself
(Farnell 2189101115: Mates With 2189101115; mated height 5.00 mm).

Pad nets assigned on the PCB from the v1.0 CSV. Schematic shows hierarchical
ports for power / clock / reset / mgmt. Host PCIe names live on sheet 02.
SerDes S1-S7 named on the PCB for this seat and left unrouted (AMD xGMI unknown).

MODULE_ID / LINK_CONFIG 1k pulldowns NOT placed (AMD overlay unknown).
"""
        ports = [
            "P48V", "P12V1", "P12V2", "P3V3", "GND",
            f"OAM{oam}_PVREF", f"OAM{oam}_PE_REFCLKP", f"OAM{oam}_PE_REFCLKN",
            f"OAM{oam}_PERST#", f"OAM{oam}_HOST_PWRGD", f"OAM{oam}_MODULE_PWRGD",
            f"OAM{oam}_WARMRST#", f"OAM{oam}_PWRBRK#", f"OAM{oam}_PRSNT0#",
            f"OAM{oam}_SMBus_SLV_D", f"OAM{oam}_SMBus_SLV_CLK",
        ]
    else:
        text = f"""OAM{oam} connector instances — MECHANICAL + POWER ONLY (populate later).

Same 2x Molex 218910-1115 land pattern and Fig 2 M3.5 holes as seats 0-1.
PCIe / xGMI / clock / mgmt pads have NO NET on this seat.

needs on-board PCIe switch — MPN Unknown.

Power pads share P48V / P12V1 / P12V2 / P3V3 / GND with the rest of the board.
P48V still NO POUR, DO NOT ENERGIZE. PVREF is a module output — never drive.
"""
        ports = ["P48V", "P12V1", "P12V2", "P3V3", "GND", f"OAM{oam}_PVREF"]
    write_text_sheet(rel, f"OAM{oam} connectors", text)
    append_hier_labels(rel, ports, y0=150)


def write_switch_unknown_sheet() -> None:
    text = """SEATS 2-7 HOST I/O — NOT CLOSED.

X11DPH-T (system host, NOT on this PCB):
  3x PCIe Gen3 x16 + 4x Gen3 x8.
Each MI250X OAM is 2 GCD and typically presents 2x x16 of host PCIe.
8 seats therefore need far more host lanes than the locked motherboard has.

This stub:
- Seats 0-1: named PCIE_* nets aimed at the HOST CONNECTOR REGION on the PCB.
  No CEM / SlimSAS / MCIO / retimer MPN is invented.
- Seats 2-7: mechanical + power pads only. PCIe and S1-S7 have no net.

To light seats 2-7 later, this carrier would need an on-board PCIe switch
(and likely a refclk / PERST distribution tree).

needs on-board PCIe switch — MPN Unknown.

Do not buy a random Broadcom/Microchip switch to "finish" this board.
SI, bifurcation, dual-GCD mapping, and the AMD overlay are all still Unknown.
Do not route S1-S7 as a pretend xGMI mesh.
"""
    write_text_sheet("sheets/11_pcie_switch_unknown.kicad_sch", "PCIe switch MPN Unknown", text)


def write_unmapped_sheet(rows: list[dict]) -> None:
    unmapped = sorted({(r["connector"], r["pin"], r["signal"]) for r in rows if is_unmapped(r["signal"])})
    lines = [
        "Pads explicitly UNMAPPED on every seat (no net, no copper).",
        "Named in the v1.0 generic map but reserved, do-not-use, or TEST pins",
        "whose AMD MI250X function is Unknown. Do not invent pullups or straps.",
        "On seats 2-7, PCIe/SerDes/clock/mgmt are ALSO unnetted (mech+power only).",
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


def write_pcb(rows: list[dict]) -> None:
    """4-layer mechanical+mapped board. No signal tracks. No P48V plane pour."""
    pads = parse_footprint_pads()
    if len(pads) != 688:
        raise SystemExit(f"expected 688 footprint pads, got {len(pads)}")

    pad_sig = {(r["connector"], r["pin"]): r["signal"] for r in rows}
    nets: dict[str, int] = {}

    def nid(name: str) -> int:
        if name not in nets:
            nets[name] = len(nets) + 1
        return nets[name]

    for n in ["GND", "P48V", "P12V1", "P12V2", "P3V3"]:
        nid(n)

    seats_meta = []
    holes = []
    for oam in range(N_SEATS):
        c0 = pcb_from_mod(oam, *CONN0_MOD)
        c1 = pcb_from_mod(oam, *CONN1_MOD)
        seats_meta.append((oam, "Conn0", f"J{oam}_Conn0", c0[0], c0[1], ROT))
        seats_meta.append((oam, "Conn1", f"J{oam}_Conn1", c1[0], c1[1], ROT))
        for i, (hx, hy) in enumerate(HOLES_MOD, start=1):
            px, py = pcb_from_mod(oam, hx, hy)
            holes.append((f"H{oam}{i}", px, py))

    fp_blocks = []
    for oam, conn, ref, x, y, rot in seats_meta:
        role = "HOST_PCIE_NAMED" if oam in HOST_PCIE_SEATS else "MECH_POWER_ONLY"
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
        f'  (gr_text "Molex 218910-1115 x16  |  4-layer  |  no P48V pour  |  ticket 167157  |  NOT a UBB"',
        f'    (at {BOARD_W/2:.3f} 12) (layer "F.SilkS")',
        '    (effects (font (size 1.6 1.6) (thickness 0.2))))',
        f'  (gr_text "4x2 of 103x166 mm KOZ = 412x332 mm INFERRED tiling. Outline {BOARD_W:.0f}x{BOARD_H:.0f} mm < PCBWay adv ML 508x600."',
        f'    (at {BOARD_W/2:.3f} {BOARD_H-6:.3f}) (layer "F.SilkS")',
        '    (effects (font (size 1.4 1.4) (thickness 0.18))))',
    ]

    for oam in range(N_SEATS):
        kx, ky = koz_origin(oam)
        mx, my = mod_origin(oam)
        cx = kx + KOZ_W / 2
        cy = ky + 8
        if oam in HOST_PCIE_SEATS:
            role = f"SEAT {oam}  HOST PCIe NAMED (stub)  populate now"
        else:
            role = f"SEAT {oam}  MECH+POWER ONLY  needs on-board PCIe switch — MPN Unknown"
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
        ]

    hx0 = MARGIN + N_COLS * KOZ_W + MARGIN  # 452
    graphics += [
        f'  (gr_rect (start {hx0:.3f} {MARGIN:.3f}) (end {BOARD_W:.3f} {BOARD_H-MARGIN:.3f})',
        '    (stroke (width 0.25) (type solid)) (fill none) (layer "Dwgs.User"))',
        f'  (gr_rect (start {hx0:.3f} {MARGIN:.3f}) (end {BOARD_W:.3f} {BOARD_H-MARGIN:.3f})',
        '    (stroke (width 0.12) (type dash)) (fill none) (layer "F.CrtYd"))',
        f'  (gr_text "HOST CONNECTOR REGION"',
        f'    (at {hx0+HOST_STRIP/2:.3f} {MARGIN+20:.3f} 90) (layer "F.SilkS")',
        '    (effects (font (size 2.0 2.0) (thickness 0.25))))',
        f'  (gr_text "OAM0+OAM1 PCIE_* named nets point here"',
        f'    (at {hx0+HOST_STRIP/2-8:.3f} {MARGIN+80:.3f} 90) (layer "F.SilkS")',
        '    (effects (font (size 1.2 1.2) (thickness 0.15))))',
        f'  (gr_text "NO CEM / SlimSAS / MCIO invented"',
        f'    (at {hx0+HOST_STRIP/2+0:.3f} {MARGIN+80:.3f} 90) (layer "F.SilkS")',
        '    (effects (font (size 1.2 1.2) (thickness 0.15))))',
        f'  (gr_text "X11DPH-T NOT ON THIS PCB"',
        f'    (at {hx0+HOST_STRIP/2+8:.3f} {MARGIN+80:.3f} 90) (layer "F.SilkS")',
        '    (effects (font (size 1.2 1.2) (thickness 0.15))))',
        f'  (gr_text "seats 2-7: needs on-board PCIe switch — MPN Unknown"',
        f'    (at {hx0+HOST_STRIP/2+16:.3f} {MARGIN+90:.3f} 90) (layer "F.SilkS")',
        '    (effects (font (size 1.1 1.1) (thickness 0.14))))',
        f'  (gr_text "P48V PADS EXIST — NO POUR — DO NOT ENERGIZE"',
        f'    (at {BOARD_W/2:.3f} {BOARD_H-12:.3f}) (layer "F.SilkS")',
        '    (effects (font (size 1.8 1.8) (thickness 0.22))))',
        f'  (gr_text "Inners In1.Cu / In2.Cu reserved. No signal tracks. Seats 2-7 have power nets only."',
        f'    (at {BOARD_W/2:.3f} 16.5) (layer "Cmts.User")',
        '    (effects (font (size 1.3 1.3) (thickness 0.15))))',
        f'  (gr_text "Seat grid: row0 (Y={MARGIN:.0f}) seats 0-3; row1 (Y={MARGIN+KOZ_H:.0f}) seats 4-7; col pitch {KOZ_W:.0f} mm. Conn rotation 180 Inferred."',
        f'    (at {BOARD_W/2:.3f} {BOARD_H-18:.3f}) (layer "Cmts.User")',
        '    (effects (font (size 1.2 1.2) (thickness 0.14))))',
    ]

    pcb = f'''(kicad_pcb (version {PCB_VER}) (generator "{GEN}") (generator_version "9.0")
  (general (thickness 1.6))
  (paper "A1")
  (title_block
    (title "DO NOT FABRICATE — Rev3 8-seat PCBWay chassis stub")
    (date "2026-08-21")
    (rev "Rev3_8Seat_PCBWay_v1")
    (comment 1 "DO NOT FABRICATE. DO NOT ENERGIZE P48V. Ticket 167157.")
    (comment 2 "492 x 372 mm 4-layer FR-4. 16x 218910-1115. Not a UBB.")
  )
  (layers
    (0 "F.Cu" signal)
    (1 "In1.Cu" power)
    (2 "In2.Cu" power)
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
      (layer "F.Cu" (type "copper") (thickness 0.035))
      (layer "dielectric 1" (type "core") (thickness 0.2) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "In1.Cu" (type "copper") (thickness 0.035))
      (layer "dielectric 2" (type "core") (thickness 1.065) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "In2.Cu" (type "copper") (thickness 0.035))
      (layer "dielectric 3" (type "core") (thickness 0.2) (material "FR4") (epsilon_r 4.5) (loss_tangent 0.02))
      (layer "B.Cu" (type "copper") (thickness 0.035))
    )
  )
{net_decls}
{chr(10).join(graphics)}
{chr(10).join(hole_blocks)}
{chr(10).join(fp_blocks)}
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


def write_project() -> None:
    (ROOT / "fp-lib-table").write_text(
        '(fp_lib_table\n  (lib (name "footprints")(type "KiCad")(uri "${KIPRJMOD}/footprints")(options "")(descr "Molex 218910-1115 geometry candidate"))\n)\n'
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
                "track_widths": [0.1, 0.2, 0.5, 1.0],
                "via_dimensions": [{"diameter": 0.6, "drill": 0.3}],
            }
        },
        "boards": [],
        "cvpcb": {"equivalence_files": []},
        "libraries": {"pinned_footprint_libs": [], "pinned_symbol_libs": []},
        "meta": {"filename": f"{PROJ}.kicad_pro", "version": 3},
        "net_settings": {"classes": [], "meta": {"version": 0}},
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
        "# Seats 2-7: power + PVREF only.",
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
    (ROOT / f"netlist/{PROJ}.net").write_text("\n".join(lines) + "\n")


def main() -> None:
    rows = load_pinmap()
    if not FOOTPRINT_SRC.exists():
        raise SystemExit(f"missing footprint {FOOTPRINT_SRC}")
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
        "layers": 4,
        "oam_seats": N_SEATS,
        "connectors_per_seat": 2,
        "molex_mpn": "218910-1115",
        "molex_qty": 16,
        "molex_mates_with": "2189101115 (hermaphroditic, self-mating)",
        "board_outline_mm": [BOARD_W, BOARD_H],
        "koz_reserve_mm": [N_COLS * KOZ_W, N_ROWS * KOZ_H],
        "koz_tiling": "4x2 of 103x166 INFERRED not a UBB drawing",
        "pcbway_adv_finished_ml_mm": list(PCBWAY_ADV_ML),
        "fits_pcbway_508x600": BOARD_W <= PCBWAY_ADV_ML[0] and BOARD_H <= PCBWAY_ADV_ML[1],
        "host_pcie_seats": sorted(HOST_PCIE_SEATS),
        "mech_power_only_seats": [i for i in range(N_SEATS) if i not in HOST_PCIE_SEATS],
        "p3v3_count_conn0": sum(1 for r in rows if r["connector"] == "Conn0" and r["signal"] == "P3V3"),
        "npth_m35_count": N_SEATS * 4,
        "p48v_pour": False,
        "signal_tracks": False,
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
