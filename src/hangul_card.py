"""Phase 1 feasibility CAD, mm, +Z up. Not a wireless-charging qualification.

Check each printable part independently, FDM and SLA, before delivery.
Injection molding: bottom_shell and top_frame, pull +Z, material PC.
Dimensions at top. Electronics, fasteners and spring domes are envelopes.
"""
import math
import build123d as bd
from cad import model

WIDTH = model.param("width", 60.0, unit="mm")
LENGTH = model.param("length", 90.0, unit="mm")
HEIGHT = model.param("height", 5.8, unit="mm")
CORNER_R = model.param("corner_radius", 2.0, unit="mm")
EDGE_BREAK = model.param("edge_break", 0.2, unit="mm")
PITCH = model.param("key_pitch", 18.0, unit="mm")
WALL = model.param("wall", 1.0, unit="mm")
RING_OD = model.param("magnet_od", 57.0, unit="mm")
RING_ID = model.param("magnet_id", 46.0, unit="mm")
RING_T = model.param("magnet_thickness", 0.8, unit="mm")
DOME_D = model.param("dome_diameter", 5.0, unit="mm")
DOME_H = model.param("dome_free_height", 0.3, unit="mm")
DOME_METAL_T = 0.05
TRAVEL = model.param("dome_travel", 0.2, unit="mm")
FILM_T = model.param("clear_film", 0.5, unit="mm")
PAD_T, FLOOR_T = 0.2, 0.6
FLOOR_TOP = PAD_T + FLOOR_T
PCB_Z, PCB_T = 3.7, 0.6
DOME_Z = PCB_Z + PCB_T
SENSOR_Z, SENSOR_T = 5.0, 0.2
FILM_Z = SENSOR_Z + SENSOR_T
FRAME_Z = 5.1
FILM_W, FILM_L = 56.0, 64.0
SENSOR_W, SENSOR_L = 54.0, 60.0
ASSEMBLY_GAP = 0.15
ACTUATOR_D = 1.5
BATTERY_W, BATTERY_L, BATTERY_T = 24.0, 10.0, 2.5
BATTERY_Y, BATTERY_Z = 35.0, 1.0
BLE_W, BLE_L, BLE_T = 10.0, 12.0, 1.5
BLE_X, BLE_Y, BLE_Z = -13.0, -34.0, 1.0
IC_W, IC_L, IC_T = 6.0, 6.0, 1.0
IC_X, IC_Y, IC_Z = 13.0, -34.0, 1.0
USB_W, USB_L, USB_H = 8.4, 7.0, 2.6  # generic envelope, NOT a selected connector
USB_Y, USB_Z = -41.0, 1.0
USB_PORT_W, USB_PORT_H = 9.0, 3.0  # explicit provisional opening
SCREW_X, SCREW_Y = 24.0, 39.0
SCREW_D, SCREW_CLEAR_D = 1.4, 1.6
HEAD_D, HEAD_CLEAR_D, HEAD_T = 2.5, 2.7, 0.5
BOSS_D, BOSS_TOP = 3.5, 5.1
GLYPH_DOT_D, GLYPH_DOT_PITCH = 0.35, 0.55
GLYPH_Z, GLYPH_T = 5.78, 0.02
PCB_W, PCB_L, PCB_RAIL_W = 54.0, 76.0, 6.0
RING_Z = 1.0
SUPPORT_TOP, ADHESIVE_T = 5.0, 0.2
FRAME_OPEN_W = FILM_W + 2 * ASSEMBLY_GAP
FRAME_OPEN_L = FILM_L + 2 * ASSEMBLY_GAP

# Each pattern is a distinct editable object; all black/white. Numeric mode is
# abbreviated to a dot-matrix '123' as the source screenshot's small mode mark.
PATTERNS = {
    "arrow_left": ["00100", "01000", "11111", "01000", "00100"],
    "triangle": ["000010000", "000101000", "001000100", "010000010", "111111111"],
    "arrow_right": ["00100", "00010", "11111", "00010", "00100"],
    "chevron_left": ["00001", "00010", "00100", "01000", "10000", "01000", "00100", "00010", "00001"],
    "ring": ["001111100", "010000010", "100000001", "100000001", "100000001", "100000001", "100000001", "010000010", "001111100"],
    "chevron_right": ["10000", "01000", "00100", "00010", "00001", "00010", "00100", "01000", "10000"],
    "numeric_123": ["01001110111", "11000010001", "01001110111", "01001000001", "11101110111"],
    "diamond": ["000010000", "000101000", "001000100", "010000010", "100000001", "010000010", "001000100", "000101000", "000010000"],
    "return": ["0000001", "0010001", "0100001", "1111111", "0100000", "0010000"],
}
NAMES = ("arrow_left", "triangle", "arrow_right", "chevron_left", "ring", "chevron_right", "numeric_123", "diamond", "return")


def zones():
    return [(name, (col - 1) * PITCH, (1 - row) * PITCH)
            for (row, col), name in zip(((r, c) for r in range(3) for c in range(3)), NAMES)]


def screws():
    return [(x, y) for x in (-SCREW_X, SCREW_X) for y in (-SCREW_Y, SCREW_Y)]


def box(w, l, h, x=0, y=0, z=0):
    return bd.Pos(x, y, z) * bd.Box(w, l, h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def rounded(w, l, h, r, z=0, x=0, y=0):
    return bd.Pos(x, y, z) * bd.extrude(bd.RectangleRounded(w, l, r), amount=h)


def cyl(d, h, x=0, y=0, z=0):
    return bd.Pos(x, y, z) * bd.Cylinder(d / 2, h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def named(shape, name, color):
    shape.label, shape.color = name, color
    return shape


def clear(shape, name):
    from bd_materials import plastics
    material = plastics.pc()
    material.pbr = material.pbr.override(transmission=1.0, roughness=0.12, ior=1.58)
    shape.material = material
    return named(shape, name, "#ededed")


def make_shell():
    # Bottom face is at .2: phone pad adds the first .2 mm.
    outer = rounded(WIDTH, LENGTH, FRAME_Z - PAD_T, CORNER_R, PAD_T)
    # Preserve the approved 0.2 perimeter edge break on the contact-side face.
    outer = bd.chamfer(outer.edges().group_by(bd.Axis.Z)[0], length=EDGE_BREAK)
    cavity = rounded(WIDTH - 2 * WALL, LENGTH - 2 * WALL, HEIGHT,
                     CORNER_R - WALL, FLOOR_TOP)
    shell = outer - cavity
    # Shelf below film perimeter; inner opening leaves all nine zones clear.
    shelf = rounded(58.2, 66.0, 0.2, 1.1, 4.8) - rounded(SENSOR_W, SENSOR_L, 0.4, 1.0, 4.7)
    shell = shell + shelf
    for x, y in screws():
        boss = cyl(BOSS_D, BOSS_TOP - FLOOR_TOP, x, y, FLOOR_TOP)
        shell = shell + boss
    for x, y in screws():
        shell = shell - cyl(SCREW_CLEAR_D, HEIGHT, x, y, FLOOR_TOP)
    # Connector through-opening; no connector-model-specific fit claimed.
    shell = shell - box(USB_PORT_W, 4.0, USB_PORT_H, y=-44.0, z=USB_Z-0.2)
    return named(shell, "bottom_shell", "#252525")


@model
def bottom_shell():
    return make_shell()


@model
def top_frame():
    frame = rounded(WIDTH, LENGTH, HEIGHT - FRAME_Z, CORNER_R, FRAME_Z)
    frame = bd.chamfer(frame.edges().group_by(bd.Axis.Z)[-1], length=EDGE_BREAK)
    frame = frame - rounded(FRAME_OPEN_W, FRAME_OPEN_L, 2.0, 1.15, 4.5)
    for x, y in screws():
        frame = frame - cyl(SCREW_CLEAR_D, 2, x, y, FRAME_Z-0.1)
        frame = frame - cyl(HEAD_CLEAR_D, HEAD_T+0.1, x, y, HEIGHT-HEAD_T)
    return named(frame, "top_frame", "#303030")


@model
def top_cover():
    return clear(rounded(FILM_W, FILM_L, FILM_T, 1.0, FILM_Z), "top_cover_flexible_pc")


@model
def finish_layer():
    # Glyph islands are inserted into the finish, not intersecting it.
    finish = rounded(FILM_W, FILM_L, HEIGHT-FILM_Z-FILM_T, 1.0, FILM_Z+FILM_T)
    for name, x, y in zones():
        for px, py in dot_positions(name, x, y):
            finish = finish - cyl(GLYPH_DOT_D, GLYPH_T, px, py, GLYPH_Z)
    return clear(finish, "finish_with_legend_inlays")


@model
def touch_sensor():
    return clear(rounded(SENSOR_W, SENSOR_L, SENSOR_T, 1.0, SENSOR_Z), "touch_sensor_flex_placeholder")


@model
def perimeter_adhesive():
    band = rounded(FILM_W, FILM_L, ADHESIVE_T, 1.0, SUPPORT_TOP)
    band = band - rounded(SENSOR_W, SENSOR_L, 0.4, 1.0, SUPPORT_TOP-0.1)
    return named(band, "perimeter_bond", "#737373")


@model
def pcb():
    # Sparse rigid substrate with three supporting row rails. Copper and
    # electrodes are not represented as a certified wireless-charge keepout.
    board = rounded(PCB_W, PCB_L, PCB_T, 1.0, PCB_Z)
    board = board - rounded(48.0, 60.0, 1.0, 1.0, PCB_Z-0.2)
    for yy in (-PITCH, 0.0, PITCH):
        board = board + box(49.0, PCB_RAIL_W, PCB_T, y=yy, z=PCB_Z)
    for x, y in screws():
        board = board - cyl(BOSS_D+0.4, 1.0, x, y, PCB_Z-0.2)
    return named(board, "pcb_sparse_placeholder", "#4e4e4e")


@model
def dome_sheet():
    sheet = rounded(SENSOR_W, SENSOR_L, 0.10, 1.0, DOME_Z)
    for _, x, y in zones():
        sheet = sheet - cyl(DOME_D+0.2, 0.3, x, y, DOME_Z-0.1)
    return named(sheet, "dome_carrier_pet", "#a5a5a533")


def dome_cap(x, y, height=DOME_H):
    radius = ((DOME_D/2)**2 + height**2) / (2*height)
    center_z = DOME_Z + height - radius
    outer = bd.Pos(x, y, center_z) * bd.Sphere(radius)
    inner = bd.Pos(x, y, center_z) * bd.Sphere(radius-DOME_METAL_T)
    cap = (outer - inner) & cyl(DOME_D, height+0.02, x, y, DOME_Z)
    return cap


@model
def domes():
    return bd.Compound(children=[named(dome_cap(x, y), f"dome_{name}", "#c1c1c1") for name, x, y in zones()], label="nine_tactile_domes")


@model
def actuators():
    return bd.Compound(children=[named(cyl(ACTUATOR_D, SENSOR_Z-DOME_Z-DOME_H, x, y, DOME_Z+DOME_H), f"actuator_{name}", "#d0d0d0") for name, x, y in zones()], label="nine_actuators")


@model
def battery():
    return named(rounded(BATTERY_W, BATTERY_L, BATTERY_T, 0.6, BATTERY_Z, y=BATTERY_Y), "lipo_envelope_no_capacity_claim", "#909090")


@model
def magnet_ring():
    ring = cyl(RING_OD, RING_T, z=RING_Z) - cyl(RING_ID, RING_T+0.2, z=RING_Z-0.1)
    return named(ring, "magnet_ring_envelope_no_polarization", "#777777")


@model
def electronics():
    parts = [named(box(BLE_W, BLE_L, BLE_T, BLE_X, BLE_Y, BLE_Z), "ble_module_and_rf_reserved_volume", "#656565"),
             named(box(IC_W, IC_L, IC_T, IC_X, IC_Y, IC_Z), "touch_ic_reserved_volume", "#454545"),
             named(rounded(USB_W, USB_L, USB_H, 0.5, USB_Z, y=USB_Y), "usb_c_generic_envelope", "#999999")]
    return bd.Compound(children=parts, label="electronics_placeholders")


@model
def fasteners():
    parts = []
    for n, (x, y) in enumerate(screws()):
        shaft = cyl(SCREW_D, HEIGHT-HEAD_T-0.9, x, y, 0.9)
        head = cyl(HEAD_D, HEAD_T, x, y, HEIGHT-HEAD_T)
        screw = shaft + head
        screw = screw - box(1.7, 0.3, 0.15, x, y, HEIGHT-0.15)
        parts.append(named(screw, f"screw_{n+1}_m1p4_unthreaded_envelope", "#b8b8b8"))
    return bd.Compound(children=parts, label="four_fasteners")


@model
def phone_pad():
    return named(rounded(59.6, 89.6, PAD_T, 1.8), "phone_contact_pad", "#444444")


@model
def mounting_bonds():
    h = RING_Z-FLOOR_TOP
    ring = cyl(RING_OD, h, z=FLOOR_TOP) - cyl(RING_ID, h+0.2, z=FLOOR_TOP-0.1)
    parts = [named(ring, "magnet_mount_bond", "#555555"),
             named(rounded(BATTERY_W, BATTERY_L, BATTERY_Z-FLOOR_TOP, 0.6, FLOOR_TOP, y=BATTERY_Y), "battery_mount_bond", "#555555"),
             named(box(BLE_W, BLE_L, BLE_Z-FLOOR_TOP, BLE_X, BLE_Y, FLOOR_TOP), "ble_mount_bond", "#555555"),
             named(box(IC_W, IC_L, IC_Z-FLOOR_TOP, IC_X, IC_Y, FLOOR_TOP), "ic_mount_bond", "#555555")]
    return bd.Compound(children=parts, label="component_mount_adhesives")


def dot_positions(name, x, y):
    pattern = PATTERNS[name]
    # Smaller peripheral symbols preserve the screenshot's optical hierarchy.
    scale = 0.65 if name in ("arrow_left", "arrow_right", "numeric_123", "return") else 1.0
    pitch = GLYPH_DOT_PITCH * scale
    return [(x+(col-(len(row)-1)/2)*pitch, y+((len(pattern)-1)/2-r)*pitch)
            for r, row in enumerate(pattern) for col, val in enumerate(row) if val == "1"]


@model
def legends():
    glyphs = []
    for name, x, y in zones():
        dots = [cyl(GLYPH_DOT_D, GLYPH_T, px, py, GLYPH_Z) for px, py in dot_positions(name, x, y)]
        glyphs.append(named(bd.Compound(dots), f"legend_{name}", "#101010"))
    return bd.Compound(children=glyphs, label="editable_monochrome_legends")


@model
def assembly():
    children = [f().shape for f in (bottom_shell, top_frame, top_cover, finish_layer, touch_sensor,
                perimeter_adhesive, pcb, dome_sheet, domes, actuators, battery, magnet_ring,
                electronics, fasteners, phone_pad, mounting_bonds, legends)]
    result = bd.Compound(children=children, label="nine_key_card_v01")
    bb = result.bounding_box()
    assert abs(bb.size.X-WIDTH) < 1e-5
    assert abs(bb.size.Y-LENGTH) < 1e-5
    assert abs(bb.size.Z-HEIGHT) < 1e-5
    assert abs((WIDTH-RING_OD)/2-1.5) < 1e-6
    assert len(zones()) == 9
    return result


@model
def assembly_open():
    """Same CAD with top optical stack hidden for direct internal inspection."""
    return bd.Compound(children=[f().shape for f in (bottom_shell, pcb, dome_sheet, domes, actuators, battery, magnet_ring, electronics, fasteners, phone_pad, mounting_bonds)], label="internal_inspection")


if __name__ == "__main__":
    assembly()
    assembly_open()
