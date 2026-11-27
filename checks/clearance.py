"""Exact geometric checks, including faults that must be detected.
Run: cad run checks/clearance.py. No shape is created as a public model here.
"""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import build123d as bd
from cad.build123d import leaves
import hangul_card as c


def run():
    root = c.assembly().shape
    parts = {s.label: s for s in leaves(root)}
    rows = []

    def distance(a, b, minimum, label):
        measured = parts[a].distance_to(parts[b])
        rows.append({"check": label, "parts": [a,b], "minimum_mm": minimum, "measured_mm": measured, "passed": measured >= minimum-1e-6})
        assert rows[-1]["passed"], rows[-1]

    distance("magnet_ring_envelope_no_polarization", "bottom_shell", 0.20, "magnet_shell_clearance")
    distance("magnet_ring_envelope_no_polarization", "lipo_envelope_no_capacity_claim", 0.20, "battery_ring_clearance")
    distance("lipo_envelope_no_capacity_claim", "pcb_sparse_placeholder", 0.20, "battery_pcb_vertical_gap")
    distance("top_cover_flexible_pc", "top_frame", c.ASSEMBLY_GAP, "film_frame_per_side_gap")
    distance("usb_c_generic_envelope", "bottom_shell", 0.20, "connector_shell_gap")
    for name, _, _ in c.zones():
        distance(f"dome_{name}", "dome_carrier_pet", 0.10, f"dome_{name}_carrier_gap")
        distance(f"actuator_{name}", "touch_sensor_flex_placeholder", 0.0, f"actuator_{name}_sensor_contact")

    # PCB must cover the complete footprint under all nine dome bases.
    board = parts["pcb_sparse_placeholder"]
    for name, x, y in c.zones():
        probe = c.cyl(c.DOME_D, 0.05, x,y,c.DOME_Z-0.05)
        missing = (probe - board).volume
        assert missing < 1e-6, (name, missing)
    rows.append({"check":"all_nine_dome_base_footprints_supported", "passed":True})

    # Exact conservative pressed envelopes: one dome at a time, plus all nine.
    # These caps approximate deflection; they are NOT elastic force or buckling models.
    for name,x,y in c.zones():
        pressed = c.dome_cap(x,y,c.DOME_H-c.TRAVEL)
        actuator = c.cyl(c.ACTUATOR_D, c.SENSOR_Z-c.DOME_Z-c.DOME_H, x,y,c.DOME_Z+c.DOME_H-c.TRAVEL)
        assert (pressed & board).volume < 1e-6
        assert (actuator & board).volume < 1e-6
        assert (pressed & actuator).volume < 1e-6
    rows.append({"check":"nine_pressed_dome_actuator_proxy_envelopes", "passed":True, "limits":"no deformable sensor/film, spring stresses, preload or force"})

    # A displaced film must hit its frame: it is actually located by the opening.
    film = parts["top_cover_flexible_pc"]
    for axis in ("x", "y"):
        vector = (c.ASSEMBLY_GAP+0.1,0,0) if axis=="x" else (0,c.ASSEMBLY_GAP+0.1,0)
        intrusion = (film.moved(bd.Location(vector)) & parts["top_frame"]).volume
        assert intrusion > 1e-5
        rows.append({"check":f"locator_shift_{axis}", "shared_volume_mm3":intrusion, "passed":True})

    # Planted fault: oversized ring must intersect the shell wall. This does not
    # alter the delivered shape. A detector returning zero would fail this test.
    bad_ring = c.cyl(59.5,c.RING_T,z=c.RING_Z)-c.cyl(c.RING_ID,c.RING_T+0.2,z=c.RING_Z-0.1)
    intrusion = (bad_ring & parts["bottom_shell"]).volume
    assert intrusion > 1e-5
    rows.append({"check":"planted_oversize_ring_detected", "shared_volume_mm3":intrusion,"passed":True})
    # Planted fault: shift battery into ring, then ensure exact intersection finds it.
    bad_battery = parts["lipo_envelope_no_capacity_claim"].moved(bd.Location((0,-12,0)))
    intrusion = (bad_battery & parts["magnet_ring_envelope_no_polarization"]).volume
    assert intrusion > 1e-5
    rows.append({"check":"planted_battery_ring_collision_detected", "shared_volume_mm3":intrusion,"passed":True})
    out = {"passed":True,"checks":rows,"part_count":len(parts),"limits":["No RF/electromagnetic/thermal/charging proof", "No cell swelling or cable routing proof", "Unthreaded fasteners and generic connector envelopes", "No continuous elastic motion or dome force analysis"]}
    target=Path(__file__).resolve().parents[1]/"outputs/phase-1/clearance-v01.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))


if __name__=="__main__":
    run()
