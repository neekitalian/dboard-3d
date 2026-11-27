# Phase 0 — revised review specification v02

Status: review pending. Supersedes v01 where inconsistent. No CAD built; no DFM/interference checks performed.

## Confirmed by user

- 60 × 90 mm card; target 5–6 mm total; mm, +Z up.
- Continuous flexible transparent touch surface; nine locally pressable tactile dome zones; no full-height switches.
- Screenshot defines physical key appearance. Remove flower entirely; all glyphs black/white, superseding the initial single-red-accent brief.
- Nine-zone mapping interpreted from the preceding question: top row ← / △ / →; middle row left chevron / ring / right chevron; bottom numeric-mode mark / diamond / return. No additional flower button. Preserve glyphs as separate editable objects. Exact numeric-mode lettering to be visually checked against screenshot.
- Preserve underlying original Hangul input/gesture intent; visible labels follow screenshot. Firmware and patent verification are outside current CAD/render evidence.
- Magnetically attach to phone back, with centered approximately 56–59 mm magnet ring and positive edge margin.
- Phone must remain wirelessly chargeable through the attached accessory. Accessory itself is not specified to receive wireless power.
- Battery/electronic placeholder volumes permitted, no capacity/endurance claim.
- Run both resin and FDM printing reviews. Never silently change geometry to pass one process.
- Stop for review after each phase; commit each phase.

## Proposed mechanical dimensions — not yet approved

| Parameter | Review proposal |
|---|---|
| Thickness | 5.80 mm envelope, feasibility unresolved with charging |
| XY corner radius | R2.0 mm |
| Edge break | 0.20 mm |
| Zone pitch | 18 × 18 mm |
| Zone centers | X,Y each −18,0,+18 mm; +Y is top |
| Active touch area | 54 × 54 mm centered; uninterrupted drag surface |
| Dome | Ø5.0 mm, free height 0.30 mm; target travel 0.20 mm, vendor unselected |
| Flexible transparent face | 0.50 mm PC candidate; film deflection/force unverified |
| Sidewall | 1.0 mm nominal, subject to magnet pocket review |
| Magnet | OD58 / ID46 / thickness0.80 mm placeholder; centered XY |
| Ring-to-outer-edge total space | 1.0 mm per side at X extremes; this includes wall and pocket clearance, not extra margin outside wall |
| Ring alternative | OD57 gives 1.5 mm edge space; explicit approval required before choosing |
| Assembly gaps | 0.15 mm per side nominal production fit; general noncontact gap ≥0.20 mm |
| Print fit candidates | FDM 0.30 mm per side; resin 0.20 mm per side; variants must be named and reviewed |
| Dimensional targets | Shell ±0.10 mm; print ±0.20 mm provisional, process capability unverified |
| Fasteners | Four M1.4 candidates near Y=±39; exact screws/boss/insert dimensions unselected |
| USB-C location | Center of −Y short edge; connector SKU and opening unselected |
| Bottom material | Matte black PC candidate; avoids continuous aluminium over charging path |
| Glyphs | Approximately 4 mm high, dot Ø0.35 / pitch0.55 mm candidate; separate decals/objects, not perforations |

## Wireless charging changes the packaging decision

The initial centered 24×30×2.5 mm LiPo plus full 54×76×0.6 mm PCB proposal is withdrawn as the packaging baseline for charging. Battery foils, PCB copper, conductive sensor electrodes and nine metal domes may occupy the phone's charging field. Merely making the shell transparent or nonmetallic does not establish a charging path. Moving the battery alone is insufficient.

Apple advises that intervening objects and thick/metal/battery cases can reduce charging performance. WPC describes conductive foreign-object heating and coupling loss with increased coil distance. These support treating the current arrangement as unverified; they do not establish a universal clearance diameter or allowable 5.8 mm gap.

Sources:
- https://support.apple.com/en-nz/108377
- https://www.wirelesspowerconsortium.com/media/cd4ljryt/qi-v13-introduction.pdf
- https://www.wirelesspowerconsortium.com/media/klfjiwfh/qi-v13-fod.pdf

Recommended next design study, subject to approval: peripheral battery and electronics, no continuous metal bottom or broad copper plane over the charging region, explicit charger/phone-dependent electromagnetic exclusion area. Nine dome locations and sensor conductors must be assessed, not omitted. Component sizes/positions and exclusion diameter remain unresolved pending target hardware. No arbitrary charging window diameter is frozen here.

A passive through-charging study cannot be certified by CAD interference/DFM. Actual target phone, case and charger, negotiated charging behavior, temperature and efficiency must be tested. An active receive/retransmit assembly would be a different architecture requiring approval and new thickness/thermal budgeting; none is added by default.

## Initial thickness budget — provisional allocation only

| Bottom to top | mm |
|---|---:|
| Contact pad | 0.20 |
| Bottom floor | 0.60 |
| Lower adhesive | 0.10 |
| Component bay | 2.80 |
| PCB/sensor support allocation | 0.60 |
| Dome/actuator envelope | 0.50 |
| Sensor flex and adhesive | 0.20 |
| Deflection allocation | 0.20 |
| Clear flexible face | 0.50 |
| Finish/assembly allocation | 0.10 |
| Total | 5.80 |

These bands are not ten solid full-area slabs. The former full-area PCB and centered battery are not retained as a charging-compatible solution. Electrical layout, actuator contacts, battery expansion allowance and mounts need a revised layout before approval. A 0.60 mm floor also requires process-specific review. Current total is an arithmetic target, not proof of assembly feasibility.

## Review decisions outstanding

1. Phone model, case (or bare phone), charger model and desired minimum charging power. Without these, only a generic concept can be produced; through-charging stays an open requirement.
2. May Phase 1 proceed as a geometry/appearance feasibility prototype while charging remains explicitly unverified, or must charging feasibility gate all CAD? No physical feature will be dropped to create a charging path.
3. Approve/revise proposed pitch, radii, thickness, dome size, material, clearances and OD58 magnet (or explicitly select OD57). These are proposals, not user-specified values.

## Validation and delivery contract

Phase 1: one build123d script with parameters at top, named separate components and assembly; bounds/count/location assertions; exact pairwise interference and clearance checks with deliberate fault test; rest/pressed envelopes; six-view snapshots; AgentCAD independent STEP checks/angle renders and revision Diff. Show each successful run. Report flexible/electrical/RF/charging behavior as untested.

Printing DFM on printable shell/frame parts in declared orientations, separately FDM and resin. Do not evaluate a dome/electronics assembly as though all parts print in place. Production molding check on molded PC parts with stated pull; film forming, electronics and spring metal are distinct processes. Every failed or unjudged item is reported; no silent feature reduction.

Phase 2: versioned outputs/exports/ engineering STEP, per-part printable STL and assembly reference, GLB with tolerance0.02 mm. Confirm exported bounds, units, separate names and mesh validity. Internal validation STEP during Phase 1 is evidence, not the final Phase 2 delivery.

Phase 3: import approved GLB into Blender. Four 3000 px-long-edge PNG candidates: hero, top, exploded, phone-back attachment. Black/white only; clear/frosted PBR and matte/gloss contrast; separate editable glyph objects. Deliver .blend plus reproducible source. Final framing/aspect ratios subject to review.

## Tool status and checks

Installed cad0.11.18, agentcad0.8.1, uv0.13.10, mcp-for-blender2.3.3, both CAD skills. CAD server status verified with zero documents. Community MCP registered in Codex; addon installed. Blender executable now exists at /Applications/Blender.app/Contents/MacOS/Blender; executable version and live addon connection not yet checked. flowful source is restricted to ignored reference workspace; no code copied into product repo.

This phase reviewed requirements/image, reference documents and dimensional arithmetic only. No model run, interference, clearance, DFM, touch/mechanical force, electromagnetic simulation or hardware charging test has passed. Phase 0 remains open for review.
