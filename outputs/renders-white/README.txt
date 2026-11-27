WHITE PRODUCT RENDERS v05

Four product shots from the approved white appearance, rendered in headless Blender 5.3 / Cycles on Metal. 256 maximum samples with adaptive sampling, denoising, AgX and an 85 mm camera. Hero uses f/11 depth of field; other views are sharp. Final PNGs have a 3000 px long edge.

01 Hero: 3000 x 2400.
02 Top: 2400 x 3000.
03 Exploded: 3000 x 3000.
04 Attached: 2400 x 3000.

Solid white opaque touch face and body, neutral-grey visible zone markings, no red accent. Dot legends remain separate editable objects. The surface is a passive touch layer, not an active display. Internal component materials are visible only in the separated view.

The original 49 CAD source meshes remain editable. Bonded finish/sensor/carrier interfaces are omitted in assembled beauty passes; individual sensor/carrier films are revealed in the exploded view. Printed legends, thin grid, illustrative PCB artwork and a 35 micrometer edge bevel are render additions.

Current geometry is 60 x 90 x 5.8 mm. The new target is approximately 3 mm, referenced to the PLAUD Note published 2.99 mm device thickness. No source components have been compressed or removed to imply a solved thin stack-up. See ../spec-white/design-brief-v05.txt.

The attached phone remains a schematic reference; the card offset is illustrative. These renders do not validate charging, phone fit, force, travel, electrical design or manufacturing. Earlier engineering reports apply to the previous 5.8 mm review geometry, not a 3 mm production design.

Reproduce from the repository root:
Blender --background --python render/render_keyboard_white.py -- --preview
Blender --background outputs/renders-white/keyboard-studio-v05.blend --python render/render_keyboard_white.py -- --final

The script selects the tested Apple Metal GPU backend. Use --cpu or adapt the device selection on other platforms.

Glyph correction: ㅏ and ㅓ use the middle (fifth) row of nine for their horizontal arms. Four rows remain above and below; validation checks actual scene mesh positions as well as the source patterns.
