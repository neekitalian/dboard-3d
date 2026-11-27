# Keyboard viewer

Open index.html. The viewer is white-only; index-light.html is an identical compatibility entry. Each page includes its SVG, styles and scripts and works offline. Keep the anatomy/ and exports/ folders together for the model download links. The complete package is ../anatomy-viewer-v02.zip.

## Views

- Layers: separate the 49 CAD parts into eight groups.
- Inside: hide the cover, sensor and carrier to reveal the PCB, nine domes, magnet and electronics. This changes visibility, not the CAD.
- iPhone: compare the keyboard and iPhone 16 at the same scale.

Select a part for dimensions and details. Zoom in and drag to inspect it. Arrow keys and Home/End adjust separation; Space opens or closes; Escape clears selection. Play starts the demonstration. Animation pauses offscreen and honors reduced motion.

## Source

Uses the user-requested https://github.com/neekitalian/anatomy at commit 1482e8469b0a9e0d8cc18ea2740a01423d29ae80. The MIT-licensed iso-kit supplies projection, cards, page structure and styles; lathe supplies lighting vectors and tonal shading. Source and license are in visual/vendor/anatomy/.

The drawing uses the actual build123d surface meshes, tessellated at 0.08 mm and 0.25 rad. checks/anatomy_data.py creates cad-parts-v02.json; visual/build.mjs builds the pages. Geometry uses millimeters, with a Y-axis reflection and recalculated normals for display. Openings, rails, dome shells and separate legends come from the CAD.

This mesh adapter is not an Anatomy primitive/SDF scene. It does not claim a pass from the primitive A.audit/settle checks. SVG layer separation is explanatory, not a validated assembly path, deformable simulation or continuous collision test. Layer order and visible surfaces were reviewed in screenshots.

## Phone reference

Published iPhone 16 body size: 71.6 x 147.6 x 7.8 mm. Source: https://support.apple.com/en-gb/121029. All other phone details are schematic:

- Body corner radius: 11 mm.
- Camera island: 19 x 34 x 2.5 mm, R9, center X=-23/Y=51.
- Lenses: diameter11 x 0.3 mm, centers Y=44 and58.
- No phone case is modeled.
- Side-by-side CAD gap: 14 mm. The SVG uses a different presentation gap, with the same object scale.
- Attached card offset: 12 mm toward the phone bottom. This avoids the illustrative camera but does not establish MagSafe alignment. The initial centered pose collided with the illustrative camera; the card was repositioned without shrinking either object.
- Phone back Z=0; front Z=-7.8; keyboard top Z=5.8. Attached overall depth: 13.6 mm. The camera bump is schematic and additional to the nominal body thickness.

## Checks

The attached reference passed static interference checks for all 53 parts, threshold 0.000001 mm3, without fit exemptions or unmeasured pairs. See phone-interference-v02.json.

Both GLBs imported into Blender 5.3 with 53 mesh objects each. Overall bounds were within 0.02 mm of 145.6 x147.6 x13.6 mm (beside) and 71.6 x147.6 x13.6 mm (attached). See glb-import-checks.json.

Browser checks cover both themes, all views, selection/reset, keyboard control, zoom/pan/reset, a 390 px viewport and reduced motion. Console checks were clean and the mobile page had no horizontal overflow. Screenshots include four-times close-ups. English-only HTML strings, page language and dynamic control labels were checked.

The Anatomy line checker reported zero floating ends out of zero decorative open strokes. CAD outlines use iso-edge and are outside that test; this is not a full mesh geometry audit.

## Limits

This remains a review prototype. Resin thin-feature checks fail; FDM and molding warnings remain. The visualization does not fix them. Wireless charging, phone fit, magnetic force/polarity, key force, fatigue, local film deflection, electrodes, firmware, fastening and battery swelling are unverified. Battery, BLE, IC and USB-C are placeholder volumes. Opaque SVG shading is used to explain the geometry, not to predict optical transmission.

The four final 3000 px Blender product renders have not started. Review this version before continuing the later phases.
