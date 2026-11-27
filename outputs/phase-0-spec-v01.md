# 9-key Hangul phone accessory — Phase 0 review draft v01

Status: awaiting user decisions and approval. No geometry has been built. All proposed values below are unapproved; none is a measured component specification.

## User steering received after initial draft — takes precedence below

- The screenshot IS the physical key visual design, not merely an interaction reference. The earlier Hangul legend table is historical input and no longer the selected visible legend treatment. Nine-zone count remains; exact icon-to-zone mapping is pending confirmation. Candidate mapping: top row left arrow / triangle / right arrow; middle red left chevron / black ring / blue right chevron; bottom numeric-mode mark / yellow diamond / return mark. Yellow flower may be decoration or another control: unresolved, do not silently add a tenth dome.
- Flexible transparent continuous face with nine locally pressed domes is confirmed.
- Magnetic attachment AND wireless charging are required. Whether charging the phone through the accessory, charging the accessory itself, or both is unresolved. A receiver coil, ferrite/shield, routing and changed stack-up may be required. The earlier proposed battery/ring/PCB layout and 5.80 mm budget are NOT approved feasibility evidence for wireless charging. Do not simply insert a nominal coil into the existing assembly or claim compatibility. Component datasheets and charging architecture must precede a revised layer budget.
- Battery placeholder with no capacity claim is accepted.
- Both resin and FDM print-test routes are requested. Review the same nominal design separately; if either route needs geometry changes, show a named variant for approval, never silently thicken it.
- Target phone/case remains unspecified.
- Screenshot red/blue/yellow versus single-red brief remains a pending explicit choice.

The rest of this file is the initial proposal for review, not an approved specification. Where it conflicts with this steering block, this block wins. Phase 0 remains open.

## Fixed brief

- Envelope: 60 mm X × 90 mm Y, 5–6 mm total thickness, mm, +Z up.
- Origin proposed at card XY center, phone-contact plane Z=0. Top of drawing is +Y; front means the touch face.
- Nine tactile zones under one uninterrupted touch-capable surface; no full-height mechanical switches.
- Viewed from the touch face:

| | Left | Center | Right |
|---|---|---|---|
| Top | ㅅ | ㅜ | ㄱ |
| Middle | ㅏ | ㅇ | ㅓ |
| Bottom | ㄴ | ㅗ | ㅁ |

- Layout follows the user's transcription of KR 10-1426655. Patent text, gesture mapping, and legal scope have not been independently verified.
- Transparent/frosted cover, exposed internal structure, editable dot-matrix glyph objects, black/white and one red accent.
- Separate cover, sensor/PCB, dome sheet, battery, magnets, shell, fasteners; BLE, touch IC and USB-C volumes retained.
- Four 3000 px PNG renders, including phone silhouette and exploded assembly; GLB imported into Blender. Long edge 3000 px is proposed; aspect ratios await approval.
- Review stop after each numbered phase; git commit for each phase. No CAD before Phase 0 approval.

## Attachment interpretation — not a new requirement

The supplied phone screenshot shows a central ring and four directional symbols, plus peripheral UI controls. It supplies no physical dimensions, materials, electronics or manufacturing requirements. Its yellow/blue/red palette conflicts with the specified monochrome/single-red treatment if copied literally. Pending decision: interaction reference only, replacement symbols, or combined glyphs. Do not add its microphone/globe/incognito controls to the hardware without instruction.

## Proposed geometry parameters — approval requested

| Parameter | Proposal | Consequence / unresolved detail |
|---|---|---|
| Total thickness | 5.80 | Includes phone pad, coatings and adhesive allowances; no protruding screw heads |
| Key pitch X/Y | 18.0 / 18.0 | Touch-zone pitch, not mechanical keyboard pitch |
| Zone centers | X = -18,0,18; Y = -18,0,18 | Centered on card; 54 × 54 active region, no grooves interrupting drags |
| Touch zones | 18 × 18 nominal virtual cells | Edge cell boundaries at ±27; electrode pattern not yet designed |
| Dome | Ø5.0, 0.30 free height, 0.20 travel target | Nine positions; force/preload/material require vendor data and prototype |
| Continuous top | 0.50 transparent flexible PC film | Candidate, not rigid acrylic; local deflection and nine-zone selectivity unproven |
| Outer XY radius | R2.0 | Mechanical card edges |
| Edge break | 0.20 | Finish target; no automatic reduction if geometry fails |
| Shell sidewall | 1.0 nominal | Magnet pocket limits require exact section review |
| Magnet envelope | OD58 / ID46 / 0.80 thick | Placeholder, centered X=Y=0, close to phone face; no polarization or holding-force certification |
| Magnet edge margin | (60−58)/2 = 1.0 | Total edge-to-magnet space, not extra room beyond a 1.0 wall. Pocket clearance reduces remaining web; unresolved |
| Alternative within requested range | OD57 | 1.5 margin, pending explicit approval; never silently substitute |
| Battery envelope | 24 × 30 × 2.5, centered | Occupies central opening of ring at same height; corner radius from center 19.21 < ID/2=23 before leads/clearance; no capacity promised |
| PCB | 54 × 76 × 0.60 | Shape and cutouts depend on screw and RF keepouts |
| BLE reserved volume | 10 × 12 × 1.5 | Outside central battery, above/below ring where feasible; antenna keepout reserved, not simulated |
| Touch IC reserved volume | 6 × 6 × 1.0 | Under PCB, away from battery and connector; position awaits routing concept |
| USB-C | Center of -Y short edge | Connector SKU and exact shell/cable opening unresolved; no invented port certification |
| Fasteners | Four M1.4 target, corner strips near Y=±39 | Head, insert, engagement and boss sizes await selection; flange clamps frame, not active film |
| General non-contact clearance | ≥0.20 | Measured exact closest distances; contacting supports and adhesives named separately |
| Cover/frame assembly gap | 0.15 per side production proposal | Printer-dependent test coupon needed; not a claimed machining tolerance |
| Print fit gap | 0.30 per side FDM / 0.20 resin candidate | Choose process before use; no global dimensional rescaling |
| Nominal size tolerance | ±0.10 shell features, ±0.20 print target | Provisional targets, not demonstrated capabilities |
| Bottom material | Matte black PC proposed | Better matches injection molding review than anodized aluminium; aluminium would need a separate machining route |
| Red accent | One small status/light-pipe object in +Y strip | Position outside touch region; not nine colored legends |
| Legend size/dots | 4.0 high, Ø0.35 dots, 0.55 dot pitch | Separate named objects, optical decal geometry; not holes through cover |

## Proposed Z budget (bottom to top)

These are allocated bands, not ten fully solid overlapping slabs. Internals sharing a band occupy distinct XY footprints. Exact mounts, actuator geometry and interlayer contacts await CAD.

| Band | Thickness | Z interval |
|---|---:|---:|
| Phone-contact non-slip pad | 0.20 | 0.00–0.20 |
| Bottom shell floor | 0.60 | 0.20–0.80 |
| Lower adhesive allowance | 0.10 | 0.80–0.90 |
| Component bay incl. battery/expansion space, ring, BLE, IC, connector | 2.80 | 0.90–3.70 |
| PCB | 0.60 | 3.70–4.30 |
| Dome sheet / rest height / actuator envelope | 0.50 | 4.30–4.80 |
| Sensor flex and adhesive allocation | 0.20 | 4.80–5.00 |
| Deflection/actuator allocation | 0.20 | 5.00–5.20 |
| Continuous clear film | 0.50 | 5.20–5.70 |
| Hardcoat/finish/assembly allocation | 0.10 | 5.70–5.80 |

The electrical touch sensor must flex and tolerate dome actuation; a solid full-area sensor slab must not block travel. The deflection band must be reconciled with actuator tips and mechanical stops, not treated as unexplained empty air. Battery has only 0.30 vertical budget beyond nominal thickness within the bay, before detailed restraint design. Swelling clearance must be confirmed with a cell supplier. A 0.60 PC floor is a manufacturing concern; production DFM may reject it. No automatic thickening or feature deletion is allowed to force a pass.

## Decisions required before CAD

1. Screenshot use and whether the specified Hangul layout stays unchanged.
2. Flexible continuous face with locally actuated domes, or rigid cover requiring another actuation structure. Smooth drag surface versus stiffness/tactile feel is a prototype question.
3. Confirm/revise all proposed dimensions above, especially 18 pitch, 5.8 total, OD58 ring and its narrow wall. OD57 is an offered alternative, not selected.
4. Target phone/case and intended use orientation: attached while operating on the back, or detach to type? Centered ring must stay at card center. Camera clearance cannot be claimed without device geometry.
5. Magnetic attachment only, or a wireless charging requirement? No charging coil is specified. A centered battery/PCB and conductive components cannot be assumed compatible with charging through the accessory.
6. May battery and electronics remain nonfunctional placeholders with no capacity/endurance promise? Should schematic PCB graphics be shown under the top even though a real PCB may obscure the battery/ring? Exploded view can expose all volumes honestly.
7. FDM or resin print test; printer/material if known. Printed shells test enclosure fit, not transparent film, sensor or spring-steel dome function.
8. PC bottom or anodized aluminium? Suggested production split: molded frame/shell + formed/laminated clear film; the film is not an injection-molded cover.

## Acceptance evidence planned

- Phase 1: single parameterized build123d source, named separate parts/assembly, measured 60×90×approved-Z bounds, nine dome count/locations, ring center and edge margins, feature preservation assertions, snapshots from six directions. Show every successful revision.
- Interference: exact part-pair intersections, zero unintended shared volume. Document intended contacts/adhesives; no blanket overlap exemptions. Dome rest/pressed envelopes included, but rigid snapshots cannot prove film mechanics.
- Clearance: pair-specific intended gaps, exact minimum distances and displacement-based locator checks written independently; demonstrate checks fail on an injected bad placement. Finite sampling alone does not certify all geometry.
- Printing DFM: run on shell/frame in print orientation and chosen process, not pretend electronics/film/magnets are printed. Report pass/fail/not-checked and every remaining finding.
- Production molding DFM: PC shell/frame with declared pull; report floor thickness, bosses, draft, USB-C side-action needs. No claim this validates film forming, electronics, tooling, sink/warpage or life-cycle reliability.
- AgentCAD second opinion: validate exported candidate STEP and any-angle PNGs; compare subsequent iterations with Diff. Temporary validation STEP is internal Phase 1 evidence; final exports remain Phase 2.
- Phase 2: versioned engineering STEP, separate printable STL parts plus assembly reference, GLB at 0.02 mm tolerance; verify units, names and round-trip bounds. Mesh-specific validity does not follow automatically from STEP validity.
- Phase 3: imported approved GLB; editable legend objects; four 3000 px PNGs plus .blend and reproducible render script, PBR/soft studio lighting. Visual appearance does not prove physical manufacturability.

## Tool preparation record

- Installed text-to-cad skill and agentcad skill using skill-installer git fallback (Python HTTPS download had a local certificate-chain error).
- Read both skills. flowful skill and design-review checklist read as reference only; its repository remains in ignored work/references, no source copied into product files.
- Community Blender README inspected: current package calls itself mcp-for-blender; no need to switch to official fallback merely because the older repository redirects.
- Runtime update: cad 0.11.18 and agentcad 0.8.1 installed; cad server started and status verified, zero documents. Homebrew uv 0.13.10 installed. Community mcp-for-blender 2.3.3 installed, Codex MCP entry registered using absolute /opt/homebrew/bin/uvx, addon installed into Blender/5.1/scripts/addons/blender_mcp.py. Blender application installation is still running via Homebrew (terminal session 77994); do not report application or MCP connection as verified. No rendering run. Check installation outcome before Phase 1 tool use; newly registered MCP tools may require a new client session.
- Newly installed skills become discoverable on the next turn; their files are readable in this turn.
- Reference commits: agentcad c6d6e7f23f92b08c8037fa99c27f64494ecb8ef5; flowful ebc80490a67b566b30c4a22407acd9f569650958; community Blender 7f31a4623cafac7441ba9b97e67a8787b9069ee2.

## Checks performed in Phase 0 / limits

Reviewed the supplied brief and image, skill contracts, and arithmetic for ring margin, battery radial envelope, and 5.80 mm layer budget. No CAD build, interference, clearance, DFM, material simulation, RF test, battery qualification, magnetic-force measurement, phone fit test, touch test or patent verification has run. This is a reviewable design proposal, not production release.

## Deliverable paths

Product source at src/; temporary work at ignored work/. Final exports will live at outputs/exports/ with version suffixes (the requested /exports folder is interpreted as a deliverable subfolder, not filesystem-root /exports). Renders at outputs/renders/. All user-facing deliverables stay under outputs/.
