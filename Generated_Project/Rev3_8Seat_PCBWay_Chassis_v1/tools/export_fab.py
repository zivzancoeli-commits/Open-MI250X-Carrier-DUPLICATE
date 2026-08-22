#!/usr/bin/env python3
"""Export PCBWay-submittable fab files. Does not upload."""
from __future__ import annotations

import shutil
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJ = ROOT / "MI250X_8OAM_PCBWay_Chassis_Stub.kicad_pcb"
FAB = ROOT / "fab"
LAYERS = ",".join([
    "F.Cu", "In1.Cu", "In2.Cu", "In3.Cu", "In4.Cu", "In5.Cu",
    "In6.Cu", "In7.Cu", "In8.Cu", "In9.Cu", "In10.Cu", "B.Cu",
    "F.Paste", "B.Paste", "F.SilkS", "B.SilkS", "F.Mask", "B.Mask", "Edge.Cuts",
])


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.check_call(cmd)


def fill_zones(pcb_path: Path) -> None:
    """Fill copper zones and save so Gerbers contain pours, not empty planes."""
    import pcbnew

    board = pcbnew.LoadBoard(str(pcb_path))
    filler = pcbnew.ZONE_FILLER(board)
    filler.Fill(board.Zones())
    board.Save(str(pcb_path))
    print("filled zones", pcb_path)


def main() -> None:
    if FAB.exists():
        shutil.rmtree(FAB)
    FAB.mkdir()
    fill_zones(PROJ)
    gerber_dir = FAB / "gerbers"
    gerber_dir.mkdir()
    run([
        "kicad-cli", "pcb", "export", "gerbers",
        "--output", str(gerber_dir),
        "--layers", LAYERS,
        "--subtract-soldermask",
        "--no-protel-ext",
        str(PROJ),
    ])
    run([
        "kicad-cli", "pcb", "export", "drill",
        "--output", str(gerber_dir),
        "--format", "excellon",
        "--excellon-zeros-format", "decimal",
        "--excellon-units", "mm",
        "--generate-map",
        "--map-format", "gerberx2",
        "--excellon-separate-th",
        str(PROJ),
    ])
    run([
        "kicad-cli", "pcb", "export", "ipcd356",
        "--output", str(FAB / "MI250X_8OAM_PCBWay_Chassis.ipc356"),
        str(PROJ),
    ])
    run([
        "kicad-cli", "pcb", "export", "pos",
        "--output", str(FAB / "MI250X_8OAM_PCBWay_Chassis-top.pos"),
        "--side", "front",
        "--units", "mm",
        "--format", "csv",
        str(PROJ),
    ])
    shutil.copy(ROOT / "docs" / "FAB_NOTES.md", FAB / "FAB_NOTES.md")
    shutil.copy(ROOT / "BOM.md", FAB / "BOM.md")
    preview = ROOT / "docs" / "previews" / "MI250X_8OAM_PCBWay_Chassis_Stub-top.png"
    if preview.exists():
        shutil.copy(preview, FAB / "top-preview.png")
    zpath = FAB / "Rev3_8Seat_PCBWay_12L_492x372_qty5_gerbers.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(FAB.rglob("*")):
            if p == zpath or p.is_dir():
                continue
            z.write(p, p.relative_to(FAB))
    print("wrote", zpath)


if __name__ == "__main__":
    main()
