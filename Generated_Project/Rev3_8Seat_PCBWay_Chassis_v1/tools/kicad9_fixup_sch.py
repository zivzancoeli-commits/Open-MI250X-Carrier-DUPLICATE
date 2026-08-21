#!/usr/bin/env python3
"""Rewrite generator sexpr so KiCad 9.0.2 will load it (string-first tokens)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PAGES = {
    "sheets/00_do_not_fabricate.kicad_sch": "2",
    "sheets/01_power_clock_reset.kicad_sch": "3",
    "sheets/02_host_pcie_stub.kicad_sch": "4",
    "sheets/03_oam0_connectors.kicad_sch": "5",
    "sheets/04_oam1_connectors.kicad_sch": "6",
    "sheets/05_oam2_connectors.kicad_sch": "7",
    "sheets/06_oam3_connectors.kicad_sch": "8",
    "sheets/07_oam4_connectors.kicad_sch": "9",
    "sheets/08_oam5_connectors.kicad_sch": "10",
    "sheets/09_oam6_connectors.kicad_sch": "11",
    "sheets/10_oam7_connectors.kicad_sch": "12",
    "sheets/11_pcie_switch_unknown.kicad_sch": "13",
    "sheets/12_unmapped_amd.kicad_sch": "14",
}


def _uuid_of(text: str) -> str:
    m = re.search(r'\(uuid "([^"]+)"\)', text)
    return m.group(1) if m else "00000000-0000-0000-0000-000000000001"


def collapse_quoted_text_newlines(src: str) -> str:
    def repl(m: re.Match) -> str:
        return '(text "' + m.group(1).replace("\n", "\\n") + '"'
    return re.sub(r'\(text "(.*?)"', repl, src, flags=re.S)


def fix_text(src: str) -> str:
    pat = re.compile(
        r'\(text \(at ([^)]+)\)\s*'
        r'\(effects \(font \(size ([^)]+)\)(?: \(thickness [^)]+\))?\)(?: \(justify ([^)]+)\))?\)\s*'
        r'\(uuid "([^"]+)"\)\s*'
        r'"(.*?)"\s*\)',
        re.S,
    )

    def repl(m: re.Match) -> str:
        at, size, just, uu, content = m.groups()
        content = content.replace("\n", "\\n")
        just_s = f" (justify {just})" if just else ""
        return (
            f'(text "{content}"\n'
            f'\t\t(exclude_from_sim no)\n'
            f'\t\t(at {at})\n'
            f'\t\t(effects (font (size {size})){just_s})\n'
            f'\t\t(uuid "{uu}")\n'
            f'\t)'
        )

    src = pat.sub(repl, src)
    return collapse_quoted_text_newlines(src)


def fix_label(src: str) -> str:
    if re.search(r'\(label "', src):
        return src
    pat = re.compile(
        r'\(label \(at ([^)]+)\)\s*'
        r'\(effects \(font \(size ([^)]+)\)\)(?: \(justify ([^)]+)\))?\)\s*'
        r'\(uuid "([^"]+)"\)\s*'
        r'"(.*?)"\s*\)',
        re.S,
    )

    def repl(m: re.Match) -> str:
        at, size, just, uu, content = m.groups()
        just_s = f" (justify {just})" if just else ""
        return (
            f'(label "{content}"\n'
            f'\t\t(at {at})\n'
            f'\t\t(effects (font (size {size})){just_s})\n'
            f'\t\t(uuid "{uu}")\n'
            f'\t)'
        )

    return pat.sub(repl, src)


def fix_hier(src: str) -> str:
    if re.search(r'\(hierarchical_label "', src):
        return src
    pat = re.compile(
        r'\(hierarchical_label \(at ([^)]+)\)\s*'
        r'\(effects \(font \(size ([^)]+)\)\)(?: \(justify ([^)]+)\))?\)\s*'
        r'\(uuid "([^"]+)"\)\s*'
        r'\(shape (\w+)\)\s*'
        r'"(.*?)"\s*\)',
        re.S,
    )

    def repl(m: re.Match) -> str:
        at, size, just, uu, shape, content = m.groups()
        just_s = f" (justify {just})" if just else ""
        return (
            f'(hierarchical_label "{content}"\n'
            f'\t\t(shape {shape})\n'
            f'\t\t(at {at})\n'
            f'\t\t(effects (font (size {size})){just_s})\n'
            f'\t\t(uuid "{uu}")\n'
            f'\t)'
        )

    return pat.sub(repl, src)


def fix_sheet(src: str, root_uuid: str) -> str:
    if re.search(r"\(sheet\n\s*\(at", src):
        src = src.replace("/PLACEHOLDER", f"/{root_uuid}")
        return src
    pat = re.compile(
        r'\(sheet \(at ([0-9.]+) ([0-9.]+)\) \(size ([0-9.]+) ([0-9.]+)\)\s*'
        r'\(stroke \(width ([^)]+)\) \(type (\w+)\)\)\s*'
        r'\(fill \(color ([^)]+)\)\)\s*'
        r'\(uuid "([^"]+)"\)\s*'
        r'\(property "Sheetname" "([^"]+)" \(at ([^)]+)\)\s*'
        r'\(effects \(font \(size ([^)]+)\)\) \(justify ([^)]+)\)\) \(uuid "[^"]+"\)\)\s*'
        r'\(property "Sheetfile" "([^"]+)" \(at ([^)]+)\)\s*'
        r'\(effects \(font \(size ([^)]+)\)\) \(justify ([^)]+)\)\) \(uuid "[^"]+"\)\)\s*'
        r'\)',
        re.S,
    )

    def repl(m: re.Match) -> str:
        (sx, sy, w, h, sw, st, fill, uu, sname, nat, nsz, nj,
         sfile, fat, fsz, fj) = m.groups()
        page = PAGES.get(sfile, "2")
        return (
            f'(sheet\n'
            f'\t\t(at {sx} {sy})\n'
            f'\t\t(size {w} {h})\n'
            f'\t\t(exclude_from_sim no)\n'
            f'\t\t(in_bom yes)\n'
            f'\t\t(on_board yes)\n'
            f'\t\t(dnp no)\n'
            f'\t\t(stroke (width {sw}) (type {st}))\n'
            f'\t\t(fill (color {fill}))\n'
            f'\t\t(uuid "{uu}")\n'
            f'\t\t(property "Sheetname" "{sname}"\n'
            f'\t\t\t(at {nat})\n'
            f'\t\t\t(effects (font (size {nsz})) (justify {nj}))\n'
            f'\t\t)\n'
            f'\t\t(property "Sheetfile" "{sfile}"\n'
            f'\t\t\t(at {fat})\n'
            f'\t\t\t(effects (font (size {fsz})) (justify {fj}))\n'
            f'\t\t)\n'
            f'\t\t(instances\n'
            f'\t\t\t(project "MI250X_8OAM_PCBWay_Chassis_Stub"\n'
            f'\t\t\t\t(path "/{root_uuid}"\n'
            f'\t\t\t\t\t(page "{page}")\n'
            f'\t\t\t\t)\n'
            f'\t\t\t)\n'
            f'\t\t)\n'
            f'\t)'
        )

    return pat.sub(repl, src)


def fix_symbol_instance(src: str, sheet_uuid: str) -> str:
    if "(lib_id" in src and "(exclude_from_sim no)" in src and "(instances" in src:
        return src
    pat = re.compile(
        r'\(symbol \(lib_id "([^"]+)"\) \(at ([^)]+)\) \(unit (\d+)\)\s*'
        r'\(in_bom yes\) \(on_board yes\) \(dnp no\)\s*'
        r'\(uuid "([^"]+)"\)\s*'
        r'\(property "Reference" "([^"]+)" \(at ([^)]+)\)\s*'
        r'\(effects \(font \(size ([^)]+)\)\) hide\) \(uuid "[^"]+"\)\)\s*'
        r'\(property "Value" "([^"]+)" \(at ([^)]+)\)\s*'
        r'\(effects \(font \(size ([^)]+)\)\)\) \(uuid "[^"]+"\)\)\s*'
        r'\(pin "1" \(uuid "([^"]+)"\)\)\s*'
        r'\)',
        re.S,
    )

    def repl(m: re.Match) -> str:
        lib, at, unit, uu, ref, rat, rsz, val, vat, vsz, puu = m.groups()
        return (
            f'(symbol\n'
            f'\t\t(lib_id "{lib}")\n'
            f'\t\t(at {at})\n'
            f'\t\t(unit {unit})\n'
            f'\t\t(exclude_from_sim no)\n'
            f'\t\t(in_bom yes)\n'
            f'\t\t(on_board yes)\n'
            f'\t\t(dnp no)\n'
            f'\t\t(uuid "{uu}")\n'
            f'\t\t(property "Reference" "{ref}"\n'
            f'\t\t\t(at {rat})\n'
            f'\t\t\t(effects (font (size {rsz})) hide)\n'
            f'\t\t)\n'
            f'\t\t(property "Value" "{val}"\n'
            f'\t\t\t(at {vat})\n'
            f'\t\t\t(effects (font (size {vsz})))\n'
            f'\t\t)\n'
            f'\t\t(pin "1"\n'
            f'\t\t\t(uuid "{puu}")\n'
            f'\t\t)\n'
            f'\t\t(instances\n'
            f'\t\t\t(project "MI250X_8OAM_PCBWay_Chassis_Stub"\n'
            f'\t\t\t\t(path "/{sheet_uuid}"\n'
            f'\t\t\t\t\t(reference "{ref}")\n'
            f'\t\t\t\t\t(unit {unit})\n'
            f'\t\t\t\t)\n'
            f'\t\t\t)\n'
            f'\t\t)\n'
            f'\t)'
        )

    return pat.sub(repl, src)


def fix_lib_symbols(src: str) -> str:
    src = src.replace(
        '(pin_names (offset 0)) (in_bom yes) (on_board yes)',
        '(pin_names (offset 0)) (exclude_from_sim no) (in_bom yes) (on_board yes)',
    )
    src = re.sub(
        r'\(name "([^"]+)" \(effects \(font \(size [^)]+\)\)\)\) \(number "([^"]+)" \(effects \(font \(size [^)]+\)\)\)\)',
        r'(name "\1") (number "\2")',
        src,
    )
    return src


def add_header_footer(src: str) -> str:
    if '(generator_version "9.0")' not in src:
        src = src.replace(
            '(generator "rev3_8seat_pcbway_chassis_v1")',
            '(generator "rev3_8seat_pcbway_chassis_v1") (generator_version "9.0")',
            1,
        )
    src = src.replace('(generator_version "9.0") (generator_version "9.0")',
                      '(generator_version "9.0")')
    if "(sheet_instances" in src:
        return src
    src = src.rstrip()
    if src.endswith(")"):
        src = src[:-1]
    src += (
        "\n\t(sheet_instances\n"
        "\t\t(path \"/\"\n"
        "\t\t\t(page \"1\")\n"
        "\t\t)\n"
        "\t)\n"
        "\t(embedded_fonts no)\n"
        ")\n"
    )
    return src


def extract_lib_symbols(src: str) -> str:
    m = re.search(r'\(lib_symbols\n.*?\n\t\)\n', src, re.S)
    return m.group(0) if m else ""


def inject_lib_symbols(src: str, block: str) -> str:
    if "(lib_symbols" in src or not block:
        return src
    # after title_block closing
    return src.replace("\t)\n\n\t(text", f"\t)\n\n{block}\n\t(text", 1)


def fix_file(path: Path, root_uuid: str | None = None, lib_block: str = "") -> str:
    src = path.read_text()
    uu = _uuid_of(src)
    src = fix_text(src)
    src = fix_label(src)
    src = fix_hier(src)
    src = fix_symbol_instance(src, uu)
    src = fix_lib_symbols(src)
    if lib_block:
        src = inject_lib_symbols(src, lib_block)
    if root_uuid:
        src = fix_sheet(src, root_uuid)
    src = add_header_footer(src)
    path.write_text(src)
    return uu


def main() -> None:
    root = ROOT / "MI250X_8OAM_PCBWay_Chassis_Stub.kicad_sch"
    raw = root.read_text()
    root_uuid = _uuid_of(raw)
    lib_block = extract_lib_symbols(raw)
    fix_file(root, root_uuid=root_uuid)
    for rel in PAGES:
        extra = lib_block if rel.endswith("01_power_clock_reset.kicad_sch") else ""
        fix_file(ROOT / rel, lib_block=extra)
    print("kicad9-fixed", ROOT)


if __name__ == "__main__":
    main()
