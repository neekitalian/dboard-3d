# Keyboard studio

Four Nothing-inspired product shots, rendered from the exported keyboard GLB in headless Blender 5.3 / Cycles. The references guide lighting, palette and finish; their text and logos are not reproduced.

## Files

- `01-hero-v04.png`: 3000 × 2400, 85 mm perspective, f/11 depth of field.
- `02-top-v04.png`: 2400 × 3000, sharp overhead view.
- `03-exploded-v04.png`: 3000 × 3000, components separated along Z for illustration.
- `04-attached-v04.png`: 2400 × 3000, keyboard on the iPhone 16 reference.
- `keyboard-studio-v04.blend`: four named scenes, editable source meshes and separate Hangul dot objects.
- `render-settings-v04.json`: material intent, cameras, layout and render-only additions.
- `validation-v04.json`: scene configuration and separate glyph checks.
- `previews/`: lower-resolution Cycles proofs used before final rendering.

## Finish

Opaque smooth black touch face: IOR 1.49, transmission 0, roughness 0.09. Black edge finish roughness 0.22. Off-white matte body, white printed Hangul dots and thin zone lines, one red status dot. The assembled face hides the PCB, domes and magnet; these remain visible only when the layers are separated. The intended screen-like appearance is a passive touch surface, not an active LCD/OLED display. No ribs or PLAUD branding are added. Engineering geometry, thickness and layer positions are unchanged.

Lighting uses four large area sources, a neutral world, and a light-grey ground with a soft reflection. Cycles uses 256 maximum samples, adaptive sampling (32 minimum, threshold 0.012), denoising and AgX. The four stills are the requested deliverable; the optional turntable is not included.

Bonded finish, sensor and carrier interfaces share an optical stack in the assembled shots to avoid coincident-surface refraction artifacts. Their original meshes remain editable; the sensor and carrier are shown separately in the exploded view.

## Editable legends

Top row: `ㅅ ㅜ ㄱ`; middle: `ㅏ ㅇ ㅓ`; bottom: `ㄴ ㅗ ㅁ`.

Each printed dot is its own named object. Original graphic-symbol meshes are retained but hidden in the Blender file. The Hangul, grid, indicator and PCB artwork are render-only additions; the engineering STEP and source CAD are unchanged. PCB traces and markings are illustrative surface artwork, not electrical routing.

The attached shot looks toward the phone back and the opaque keyboard face. The ring is concealed. The phone remains a schematic size reference with a 12 mm card offset. Exploded spacing illustrates components and is not an assembly-path simulation.

## Reproduce

From the repository root, with Blender available at your local executable path:

```sh
Blender --background --python render/render_keyboard_opaque.py -- --preview
Blender --background outputs/renders-opaque/keyboard-studio-v04.blend --python render/render_keyboard_opaque.py -- --final
```

This script currently selects the Metal GPU backend for the tested Apple M1 Pro. Choose a suitable Cycles device when running on another platform. It uses the `blender-product-polish` skill from `kevinbadi/blender-skills` as a workflow reference, with a custom headless Cycles implementation in place of its default MCP/EEVEE uniform-gloss recipe.

Rendering does not establish printability, key force, battery performance, phone compatibility or wireless-charging behavior. Existing engineering findings remain in the Phase 1 report.
