WHITE KEYBOARD - ADDITIONAL 3D FORMATS v05

keyboard-white-v05.glb: corrected assembled white appearance model, meters in glTF convention.
keyboard-white-v05.gltf + .bin: the same model as separate glTF files; keep both together.
keyboard-white-v05.obj + .mtl: separate named objects and material references; coordinates in millimeters, +Z up. Keep both files together.
keyboard-white-v05.fbx: separate objects/materials, unit-aware. Reimported and checked in Blender.
keyboard-white-v05.stl: assembled triangle mesh, coordinates in millimeters, +Z up; no colors or editable part hierarchy.
keyboard-white-v05.ply: assembled mesh, coordinates in millimeters, +Z up; not a material-preserving appearance format.
keyboard-structure-review-v02.step: original engineering review B-rep assembly. Nominal 60 x 90 x 5.8 mm; original engineering legends/materials, not the later white Hangul appearance additions.

The assembly mesh is for visualization and interchange, not a print-ready fused solid or a mold design. Existing thin-feature/DFM findings remain unresolved. STL/PLY may contain disconnected and intentionally touching/overlapping components. Do not print it as a single functional assembly.

Nominal body: 60 x 90 x 5.8 mm. Printed surface details and the status proxy extend overall mesh thickness to about 5.887 mm. The proposed approximately 3 mm redesign has not been implemented.

The white surface is opaque; Hangul arm positions in ㅏ and ㅓ are centered. Exported model files omit the studio floor, phone and photographic cameras/lights. OBJ/FBX/glTF retain named objects. STL and PLY merge the mesh hierarchy.

Validation: all five new formats were reimported and their three bounds matched the source within 0.02 mm. This checks units and conversion, not force, fit, charging or printability. See conversion-checks.json.
