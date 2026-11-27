"""iPhone16 size reference, not a fit/charging qualification.
Apple: https://support.apple.com/en-gb/121029
Body dimensions published; corners/camera details below are illustrative.
"""
import build123d as bd
from cad import model
import hangul_card as c

PHONE_W, PHONE_L, PHONE_T = 71.6, 147.6, 7.8
PHONE_R = 11.0  # illustrative, not from Apple's dimensional drawing
SIDE_BY_SIDE_GAP = 14.0
ATTACHED_CARD_Y = -12.0  # display offset avoids illustrative camera, NOT coil alignment
CAMERA_X, CAMERA_Y = -23.0, 51.0
CAMERA_W, CAMERA_L, CAMERA_R, CAMERA_H = 19.0, 34.0, 9.0, 2.5


@model
def iphone16_reference():
    # Back faces +Z; camera is an illustrative envelope only.
    body = c.rounded(PHONE_W, PHONE_L, PHONE_T, PHONE_R, -PHONE_T)
    body.label, body.color = "iphone16_body_71p6x147p6x7p8_reference", "#919191"
    camera = c.rounded(CAMERA_W,CAMERA_L,CAMERA_H,CAMERA_R,0,CAMERA_X,CAMERA_Y)
    camera.label,camera.color="camera_island_illustrative_not_fit_geometry", "#505050"
    lenses=[]
    for i,y in enumerate((44.0,58.0)):
        lens=c.cyl(11.0,0.3,CAMERA_X,y,CAMERA_H)
        lens.label,lens.color=f"illustrative_lens_{i+1}","#151515"
        lenses.append(lens)
    assert abs(body.bounding_box().size.X-PHONE_W)<1e-6
    assert abs(body.bounding_box().size.Y-PHONE_L)<1e-6
    assert abs(body.bounding_box().size.Z-PHONE_T)<1e-6
    return bd.Compound(children=[body,camera,*lenses],label="iphone16_size_reference")


@model
def beside_iphone():
    phone=iphone16_reference().shape
    card=c.assembly().shape
    x=PHONE_W/2+SIDE_BY_SIDE_GAP+c.WIDTH/2
    card=card.moved(bd.Location((x,0,0)))
    card.label="keyboard_card_60x90x5p8"
    return bd.Compound(children=[phone,card],label="iphone16_keyboard_size_comparison")


@model
def on_iphone():
    phone=iphone16_reference().shape
    card=c.assembly().shape.moved(bd.Location((0,ATTACHED_CARD_Y,0)))
    card.label="keyboard_card_offset_minus12mm_for_scale_only"
    return bd.Compound(children=[phone,card],label="iphone16_keyboard_on_back_reference")


if __name__=="__main__":
    beside_iphone()
    on_iphone()
