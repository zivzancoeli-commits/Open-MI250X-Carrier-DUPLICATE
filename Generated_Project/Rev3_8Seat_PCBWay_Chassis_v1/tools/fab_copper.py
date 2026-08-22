#!/usr/bin/env python3
"""POWER+MECH copper for the Rev3 first article.

Called by generate_from_v10_pinmap.write_pcb(). Returns KiCad s-expr strings.

Routing policy:
  Do NOT flood P48V as one 100 A pour, and do NOT drag fat traces across the
  688-ball mezzanine. P48V_STAR lives in the left margin + two row spines in
  the copper-free channels south of each Conn0 row. Each seat fuse sits on
  that spine with pad 1 on STAR and pad 2 on a short per-seat P48V tongue
  into the Conn0 island. P12V1 / P3V3 use the same channels. F.Cu GND is
  low-priority and fills leftover (mezz GND pads + inner-plane stitches).

Buyable MPNs: see docs/BOM.md / BOM.md.
"""
from __future__ import annotations

import uuid

MEZZ_ZONE_CLEAR_MM = 0.20  # Molex 0.9 mm pitch, 0.50 mm pads → 0.40 mm gap
STAR_CLEAR_MM = 0.64  # OCP UBB v1.5 >40 V internal 25 mil, star/fuse copper
GND_CLEAR_MM = 0.25

# Row spines in the channels south of Conn0 (not across balls).
# Row 0 Conn0 Y≈154, P48V pads ≈157–162, NPTH ≈163.5, row1 KOZ at 186.
# Row 1 Conn0 Y≈320, P48V pads ≈323–328, NPTH ≈329.5, board south 372.
ROW_SPINE = {
    # STAR bus sits SOUTH of the fuse so pad 2 (seat net) is not in STAR copper.
    0: {"star_y0": 173.0, "star_y1": 178.0, "fuse_y": 169.5, "p12_y0": 179.0, "p12_y1": 183.0,
        "p3_y0": 183.5, "p3_y1": 185.5},
    1: {"star_y0": 343.0, "star_y1": 348.0, "fuse_y": 336.0, "p12_y0": 349.0, "p12_y1": 353.0,
        "p3_y0": 353.5, "p3_y1": 356.0},
}

# 12 V brick cluster: host-strip SOUTH of SW1 keepout (y>=324) and inside
# x=452–492. THL40 courtyard ≈ 26.9 × 26.9 mm.
P12_MOD_XY = (470.0, 330.0)  # pin 1; courtyard south of SW1 (y=324), west of x=492
P3V3_MOD_XY = (454.0, 366.0)
FP12_XY = (448.0, 336.0)

BOARD_W, BOARD_H = 492.0, 372.0


def uid() -> str:
    return str(uuid.uuid4())


def p48_net(oam: int) -> str:
    return "P48V" if oam == 0 else f"P48V_S{oam}"


def zone(net_id: int, name: str, layer: str, clearance: float,
         pts: list[tuple[float, float]], priority: int = 0,
         min_th: float = 0.25) -> str:
    poly = " ".join(f"(xy {x:.3f} {y:.3f})" for x, y in pts)
    return f'''  (zone (net {net_id}) (net_name "{name}") (layer "{layer}") (uuid "{uid()}")
    (hatch edge 0.5)
    (priority {priority})
    (connect_pads yes (clearance {clearance}))
    (min_thickness {min_th})
    (filled_areas_thickness no)
    (fill yes (thermal_gap {clearance}) (thermal_bridge_width 0.5))
    (polygon (pts {poly}))
  )'''


def rect(x0, y0, x1, y1) -> list[tuple[float, float]]:
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def track(a, b, w, layer, net) -> str:
    return (
        f'  (segment (start {a[0]:.3f} {a[1]:.3f}) (end {b[0]:.3f} {b[1]:.3f})'
        f' (width {w}) (layer "{layer}") (net {net}) (uuid "{uid()}"))'
    )


def via(xy, net, layers=("F.Cu", "In1.Cu")) -> str:
    return (
        f'  (via (at {xy[0]:.3f} {xy[1]:.3f}) (size 0.8) (drill 0.4)'
        f' (layers "{layers[0]}" "{layers[1]}") (net {net}) (uuid "{uid()}"))'
    )


def fp_nano(ref: str, xy, rot: float, value: str, net1, net2) -> str:
    x, y = xy
    n1i, n1n = net1
    n2i, n2n = net2
    rot_s = f" {rot:.0f}" if rot else ""
    return f'''  (footprint "footprints:Fuse_Littelfuse-NANO2-451_453" (layer "F.Cu") (uuid "{uid()}")
    (at {x:.3f} {y:.3f}{rot_s})
    (descr "{value} Nano2")
    (property "Reference" "{ref}" (at 0 -2.8) (layer "F.SilkS")
      (effects (font (size 0.8 0.8) (thickness 0.1))))
    (property "Value" "{value}" (at 0 2.8) (layer "F.Fab")
      (effects (font (size 0.7 0.7) (thickness 0.1))))
    (attr smd)
    (fp_rect (start -3.69 -1.83) (end 3.69 1.83)
      (stroke (width 0.05) (type solid)) (fill none) (layer "F.CrtYd"))
    (pad "1" smd rect (at -2.455 0) (size 1.96 3.15)
      (layers "F.Cu" "F.Mask" "F.Paste") (net {n1i} "{n1n}"))
    (pad "2" smd rect (at 2.455 0) (size 1.96 3.15)
      (layers "F.Cu" "F.Mask" "F.Paste") (net {n2i} "{n2n}"))
  )'''


def fp_thl40(ref: str, xy, nets: dict) -> str:
    x, y = xy
    def n(pin):
        i, name = nets[pin]
        return f'(net {i} "{name}")'
    return f'''  (footprint "footprints:Converter_DCDC_TRACO_THL40-xxxxWI_THT" (layer "F.Cu") (uuid "{uid()}")
    (at {x:.3f} {y:.3f})
    (descr "THL 40-4812WI 40W 12V from 48V. Isolated; both returns bonded to GND.")
    (property "Reference" "{ref}" (at 2.5 -4) (layer "F.SilkS")
      (effects (font (size 1 1) (thickness 0.12))))
    (property "Value" "THL 40-4812WI" (at 2.5 25) (layer "F.Fab")
      (effects (font (size 0.8 0.8) (thickness 0.1))))
    (attr through_hole)
    (fp_rect (start -10.95 -3.25) (end 15.95 23.65)
      (stroke (width 0.05) (type solid)) (fill none) (layer "F.CrtYd"))
    (pad "1" thru_hole roundrect (at 0 0) (size 2.4 2.4) (drill 1.4)
      (layers "*.Cu" "*.Mask") {n("1")})
    (pad "2" thru_hole circle (at 5.08 0) (size 2.4 2.4) (drill 1.4)
      (layers "*.Cu" "*.Mask") {n("2")})
    (pad "3" thru_hole circle (at -7.62 20.32) (size 2.4 2.4) (drill 1.4)
      (layers "*.Cu" "*.Mask") {n("3")})
    (pad "4" thru_hole circle (at 2.54 20.32) (size 2.4 2.4) (drill 1.4)
      (layers "*.Cu" "*.Mask"))
    (pad "5" thru_hole circle (at 12.7 20.32) (size 2.4 2.4) (drill 1.4)
      (layers "*.Cu" "*.Mask") {n("5")})
    (pad "6" thru_hole circle (at 12.7 0) (size 2.4 2.4) (drill 1.4)
      (layers "*.Cu" "*.Mask"))
  )'''


def fp_oki(ref: str, xy, rot: float, nets: dict) -> str:
    x, y = xy
    rot_s = f" {rot:.0f}" if rot else ""
    def n(pin):
        i, name = nets[pin]
        return f'(net {i} "{name}")'
    return f'''  (footprint "footprints:Converter_DCDC_Murata_OKI-78SR_Vertical" (layer "F.Cu") (uuid "{uid()}")
    (at {x:.3f} {y:.3f}{rot_s})
    (descr "OKI-78SR-3.3/1.5-W36-C 3.3V 1.5A from P12V1")
    (property "Reference" "{ref}" (at 2.54 3.2) (layer "F.SilkS")
      (effects (font (size 0.8 0.8) (thickness 0.1))))
    (property "Value" "OKI-78SR-3.3/1.5-W36-C" (at 2.54 4.6) (layer "F.Fab")
      (effects (font (size 0.6 0.6) (thickness 0.08))))
    (attr through_hole)
    (fp_rect (start -2.91 -5.44) (end 8 3.41)
      (stroke (width 0.05) (type solid)) (fill none) (layer "F.CrtYd"))
    (pad "1" thru_hole rect (at 0 0) (size 1.8 1.8) (drill 1)
      (layers "*.Cu" "*.Mask") {n("1")})
    (pad "2" thru_hole circle (at 2.54 0) (size 1.8 1.8) (drill 1)
      (layers "*.Cu" "*.Mask") {n("2")})
    (pad "3" thru_hole circle (at 5.08 0) (size 1.8 1.8) (drill 1)
      (layers "*.Cu" "*.Mask") {n("3")})
  )'''


def fuse_xy(oam: int, p48_bbox: tuple[float, float, float, float]) -> tuple[float, float, float]:
    """Nano2, rot 0 (pads along +X). Pad 1 (STAR) west, pad 2 (seat) east."""
    x0, y0, x1, y1 = p48_bbox
    row = oam // 4
    fx = x1 + 5.5
    fy = ROW_SPINE[row]["fuse_y"]
    # Seat 4 (row1 col0) would sit inside the SB175 courtyard at (70, 354).
    if row == 1 and fx < 100:
        fx = 105.0
        fy = 332.0
    return fx, fy, 0.0


def build(nid, p48_bboxes, fuse_centers, conn0_xy, p12_bboxes, p3_bboxes, gnd_via_pts):
    """Return (footprints, tracks, vias, zones, graphics) as lists of s-expr."""
    n_star = nid("P48V_STAR")
    n_brick = nid("P48V_BRICK")
    n_gnd = nid("GND")
    n_p12 = nid("P12V1")
    n_p3 = nid("P3V3")
    n_seat = [nid(p48_net(s)) for s in range(8)]

    fps: list[str] = []
    tracks: list[str] = []
    vias: list[str] = []
    zones: list[str] = []
    gfx: list[str] = []

    fuse_pos = []
    for oam, x0, y0, x1, y1 in p48_bboxes:
        fx, fy, rot = fuse_xy(oam, (x0, y0, x1, y1))
        fuse_pos.append((oam, fx, fy, rot, x0, y0, x1, y1))
        fps.append(fp_nano(
            f"F{oam}", (fx, fy), rot,
            "0476015.MR",
            (n_star, "P48V_STAR"),
            (n_seat[oam], p48_net(oam)),
        ))

    fps.append(fp_nano(
        "F_P12", FP12_XY, 0.0, "0476002.MR",
        (n_star, "P48V_STAR"), (n_brick, "P48V_BRICK"),
    ))
    fps.append(fp_thl40("U_P12V1", P12_MOD_XY, {
        "1": (n_brick, "P48V_BRICK"),
        "2": (n_gnd, "GND"),
        "3": (n_p12, "P12V1"),
        "5": (n_gnd, "GND"),
    }))
    fps.append(fp_oki("U_P3V3", P3V3_MOD_XY, 0.0, {
        "1": (n_p12, "P12V1"),
        "2": (n_gnd, "GND"),
        "3": (n_p3, "P3V3"),
    }))

    star_pri = 10

    def next_star_pri() -> int:
        nonlocal star_pri
        star_pri += 1
        return star_pri

    # ----- STAR: left riser + two row buses + inlet + SE tongue -----
    # Leave x=14.5–16.5 as a 2 mm alley for P12V1 (STAR clearance 0.64).
    zones.append(zone(n_star, "P48V_STAR", "F.Cu", STAR_CLEAR_MM,
                      rect(6, 8, 14.3, 364), priority=next_star_pri(), min_th=0.5))
    zones.append(zone(n_star, "P48V_STAR", "F.Cu", STAR_CLEAR_MM,
                      rect(16.7, ROW_SPINE[0]["star_y0"], 430, ROW_SPINE[0]["star_y1"]),
                      priority=next_star_pri(), min_th=0.5))
    zones.append(zone(n_star, "P48V_STAR", "F.Cu", STAR_CLEAR_MM,
                      rect(16.7, ROW_SPINE[1]["star_y0"], 400, ROW_SPINE[1]["star_y1"]),
                      priority=next_star_pri(), min_th=0.5))
    zones.append(zone(n_star, "P48V_STAR", "F.Cu", STAR_CLEAR_MM,
                      rect(16.7, 338, 90, 352), priority=next_star_pri(), min_th=0.5))
    zones.append(zone(n_star, "P48V_STAR", "F.Cu", STAR_CLEAR_MM,
                      rect(400, 328, FP12_XY[0] - 1.6, 340), priority=next_star_pri(), min_th=0.5))

    # Per-seat P48V tongue (pad 2) + STAR stub (pad 1 → south bus).
    for oam, fx, fy, rot, x0, y0, x1, y1 in fuse_pos:
        row = oam // 4
        bus_y0 = ROW_SPINE[row]["star_y0"]
        # Pad 2 (east) + stub north into the Conn0 island. Stays off pad 1.
        tongue = rect(fx + 0.4, min(y1 - 0.8, fy - 2.5), fx + 5.0, fy + 2.2)
        zones.append(zone(n_seat[oam], p48_net(oam), "F.Cu", MEZZ_ZONE_CLEAR_MM,
                          tongue, priority=21, min_th=0.4))
        # Pad 1 (west) down to the STAR bus.
        stub = rect(fx - 5.0, fy - 2.2, fx - 0.3, bus_y0 + 2.0)
        zones.append(zone(n_star, "P48V_STAR", "F.Cu", STAR_CLEAR_MM,
                          stub, priority=next_star_pri(), min_th=0.4))
        gfx += [
            f'  (gr_text "F{oam} 0476015.MR 15A"',
            f'    (at {fx:.3f} {fy - 4.2:.3f}) (layer "F.SilkS")',
            '    (effects (font (size 0.8 0.8) (thickness 0.1))))',
        ]

    # Brick island: F_P12 pad 2 (+2.455) and THL pin 1 (0,0 at P12_MOD_XY)
    zones.append(zone(n_brick, "P48V_BRICK", "F.Cu", STAR_CLEAR_MM,
                      rect(FP12_XY[0] + 0.8, 326, P12_MOD_XY[0] + 8, 342),
                      priority=12, min_th=0.4))

    # P12V1 alley (x≈15.5) + row spines. Unique priorities where they touch.
    zones.append(zone(n_p12, "P12V1", "F.Cu", 0.25,
                      rect(15.0, 20, 16.05, 360), priority=30, min_th=0.35))
    zones.append(zone(n_p12, "P12V1", "F.Cu", 0.25,
                      rect(16.5, ROW_SPINE[0]["p12_y0"], 430, ROW_SPINE[0]["p12_y1"]),
                      priority=31, min_th=0.35))
    zones.append(zone(n_p12, "P12V1", "F.Cu", 0.25,
                      rect(16.5, ROW_SPINE[1]["p12_y0"], 400, ROW_SPINE[1]["p12_y1"]),
                      priority=32, min_th=0.35))
    zones.append(zone(n_p12, "P12V1", "F.Cu", 0.25,
                      rect(400, 349, 488, 368), priority=33, min_th=0.35))
    alley_vias: set[tuple[float, float]] = set()
    for oam, x0, y0, x1, y1 in p12_bboxes:
        zones.append(zone(n_p12, "P12V1", "F.Cu", MEZZ_ZONE_CLEAR_MM,
                          rect(x0, y0, x1, y1), priority=40 + oam, min_th=0.3))
        iy = (y0 + y1) / 2
        drop_x = x0 - 3.0
        ay = y0 + 1.4  # A-row, north edge of the P12V1 cluster
        zones.append(zone(n_p12, "P12V1", "F.Cu", MEZZ_ZONE_CLEAR_MM,
                          rect(drop_x - 1.2, ay - 1.0, x0 + 0.4, ay + 1.0),
                          priority=48 + oam, min_th=0.3))
        tracks.append(track((x0 + 1.5, ay), (drop_x, ay), 0.5, "F.Cu", n_p12))
        vias.append(via((drop_x, ay), n_p12, ("F.Cu", "B.Cu")))
        tracks.append(track((drop_x, ay), (15.5, ay), 0.5, "B.Cu", n_p12))
        key = (15.5, round(ay, 3))
        if key not in alley_vias:
            alley_vias.add(key)
            vias.append(via((15.5, ay), n_p12, ("F.Cu", "B.Cu")))

    # P3V3: thin spines + local C1/C2 islands
    zones.append(zone(n_p3, "P3V3", "F.Cu", 0.20,
                      rect(2.0, 20, 5.0, 360), priority=50, min_th=0.3))
    zones.append(zone(n_p3, "P3V3", "F.Cu", 0.20,
                      rect(16.5, ROW_SPINE[0]["p3_y0"], 430, ROW_SPINE[0]["p3_y1"]),
                      priority=51, min_th=0.3))
    zones.append(zone(n_p3, "P3V3", "F.Cu", 0.20,
                      rect(16.5, ROW_SPINE[1]["p3_y0"], 400, ROW_SPINE[1]["p3_y1"]),
                      priority=52, min_th=0.3))
    zones.append(zone(n_p3, "P3V3", "F.Cu", 0.20,
                      rect(430, 358, 480, 370), priority=53, min_th=0.3))
    zones.append(zone(n_p3, "P3V3", "B.Cu", 0.20,
                      rect(2.0, 20, 5.0, 360), priority=50, min_th=0.3))
    p3_alley: set[tuple[float, float]] = set()
    for oam, x0, y0, x1, y1 in p3_bboxes:
        zones.append(zone(n_p3, "P3V3", "F.Cu", MEZZ_ZONE_CLEAR_MM,
                          rect(x0, y0, x1, y1), priority=60 + oam, min_th=0.3))
        iy = (y0 + y1) / 2
        drop_x = x1 + 3.0
        zones.append(zone(n_p3, "P3V3", "F.Cu", MEZZ_ZONE_CLEAR_MM,
                          rect(x1 - 0.4, iy - 1.2, drop_x + 1.2, iy + 1.2),
                          priority=68 + oam, min_th=0.3))
        tracks.append(track(((x0 + x1) / 2, iy), (drop_x, iy), 0.5, "F.Cu", n_p3))
        vias.append(via((drop_x, iy), n_p3, ("F.Cu", "B.Cu")))
        tracks.append(track((drop_x, iy), (3.5, iy), 0.4, "B.Cu", n_p3))
        key = (3.5, round(iy, 3))
        if key not in p3_alley:
            p3_alley.add(key)
            vias.append(via((3.5, iy), n_p3, ("F.Cu", "B.Cu")))

    # F.Cu GND leftover fill (priority 0). Keepouts punch SW/host holes.
    zones.append(zone(n_gnd, "GND", "F.Cu", GND_CLEAR_MM,
                      rect(2, 2, BOARD_W - 2, BOARD_H - 2), priority=0, min_th=0.3))

    # Stitch vias: generator KOZ-corner list + left-margin + channel (not via-in-pad)
    seen = set()
    for pt in gnd_via_pts:
        seen.add((round(pt[0], 2), round(pt[1], 2)))
        vias.append(via(pt, n_gnd))
    gfx += [
        f'  (gr_text "U_P12V1 THL 40-4812WI 40W from 48V"',
        f'    (at {P12_MOD_XY[0]:.3f} {P12_MOD_XY[1] - 6:.3f}) (layer "F.SilkS")',
        '    (effects (font (size 0.9 0.9) (thickness 0.1))))',
        f'  (gr_text "U_P3V3 OKI-78SR 3.3V 1.5A from P12V1"',
        f'    (at {P3V3_MOD_XY[0] + 8:.3f} {P3V3_MOD_XY[1] + 6:.3f}) (layer "F.SilkS")',
        '    (effects (font (size 0.8 0.8) (thickness 0.1))))',
        f'  (gr_text "F_P12 0476002.MR 2A"',
        f'    (at {FP12_XY[0]:.3f} {FP12_XY[1] - 4:.3f}) (layer "F.SilkS")',
        '    (effects (font (size 0.7 0.7) (thickness 0.08))))',
        '  (gr_text "STAR spines — not a 100A flood — DO NOT ENERGIZE"',
        '    (at 220 172) (layer "Cmts.User")',
        '    (effects (font (size 1.0 1.0) (thickness 0.12))))',
    ]

    return fps, tracks, vias, zones, gfx
