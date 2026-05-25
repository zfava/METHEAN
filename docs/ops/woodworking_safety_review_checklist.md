# Woodworking safety review checklist

Generated from `backend/app/content/woodworking_content.py`. The checklist below renders the actual hazards, PPE, and demonstration criteria for every authored node. Do not edit the node content from this checklist; edit `woodworking_content.py` and regenerate this file. No node may be surfaced to a learner until its `safety_review.reviewed` is set to True by a qualified human reviewer, with `reviewer` and `reviewed_on` recorded; this is the contract this checklist exists to support.

## Reviewer identification

- Reviewer name: ____________________________________________
- Relevant shop / trade experience (years, type, credentials): ____________________________________________
- Date of this review: ____________________________________________

## Completion contract

On completion of this review, for each node confirmed correct:

1. In `backend/app/content/woodworking_content.py`, set the node's `safety_review.reviewed` to `True`, `safety_review.reviewer` to the reviewer's name and credentials, and `safety_review.reviewed_on` to the date in ISO 8601 (`YYYY-MM-DD`).
2. If any item below requires correction, the correction is made in `woodworking_content.py` and this checklist is regenerated, and the review is repeated on the corrected node.
3. No node where `safety_review.reviewed` is `False` may be surfaced to a learner. The integration gate is the responsibility of `learning_context` (see the TODO in `backend/app/services/node_content.py::requires_human_safety_review`).

---

## Per-node review

### woodworking-root: Woodworking (hand-tool first)

- Node type: `root`
- Supervision required: `None`
- Current review state: reviewed = `False`, reviewer = `None`, reviewed_on = `None`

**Reviewer's verdict on this node:**  `[ ] Pass`  `[ ] Pass with corrections (corrections noted in woodworking_content.py)`  `[ ] Fail (do not surface; corrections required and re-review needed)`

Corrections / notes:

```

```

---

### ws-001: Woodworking shop safety: hand tools and the workbench

- Node type: `safety`
- Progression band: `helper`
- Supervision required: `True`
- Current review state: reviewed = `False`, reviewer = `None`, reviewed_on = `None`

#### Hazards (confirm each is named correctly; check or correct)

- [ ] Sharp edges: chisels, plane irons, marking knives, and saws are sharper than they look; a sharp tool dropped point-down can pierce a shoe.
- [ ] Workpiece motion: a board that is not held still becomes a hazard the moment a tool engages it.
- [ ] Sawdust and shavings on the floor: shavings underfoot are slippery and tools dropped into shavings can be hard to see.
- [ ] Oily rags: rags soaked in linseed oil, boiled linseed oil, tung oil, or danish oil can self-heat and ignite if balled up; they must be laid flat outdoors to dry or stored in a sealed metal can with water.
- [ ] Eye injury from chips, sawdust, or sharpening swarf, especially in overhead work, in dry or pitchy stock, and at the grinder or stones.
- [ ] Allergic or toxic reactions to specific woods (cocobolo, padauk, rosewoods, yew, some other tropical hardwoods); an unfamiliar wood is identified before it is cut.
- [ ] Wrist-line cuts: putting a hand or any body part in the path the cutting edge will travel through if it slips.

#### PPE required (confirm each item is correctly named, including what is forbidden; check or correct)

- [ ] Closed-toe shoes (leather work shoes or boots preferred; no sandals or open footwear; cloth sneakers offer little protection from a dropped chisel)
- [ ] Safety glasses for any sharpening, any overhead work, any work with dry or pitchy stock, and any unfamiliar operation; default is to wear them
- [ ] Hair tied back if it would fall forward over the bench
- [ ] No loose sleeves, no scarves, and no jewelry near the cut path
- [ ] No gloves when using saws, chisels, planes, or marking knives; gloves reduce tactile feedback and control

#### Supervision basis (confirm the basis is honest and the threshold is correct)

- [ ] The safety competency is itself supervised: an adult mentor walks the learner through every hazard and every piece of safety equipment in their actual shop and signs off only when the learner can name and locate each. There is no self-attestation on safety.

#### Demonstration criteria (confirm each is measurable on the work itself and correctly states the bar; check or correct)

- [ ] Names every PPE item on the list and explains when each is required and when each is forbidden
- [ ] Locates the fire extinguisher within reach of the bench, names its rating, and confirms the rating is appropriate for what is actually in the shop per the household's confirmation with a local fire-safety authority
- [ ] Locates the first aid kit and confirms it meets a recognized standard (ANSI/ISEA Z308.1 or current American Red Cross guidance)
- [ ] Demonstrates the safe carry of a chisel: held by the handle, the cutting edge controlled, the edge angled away from the carrier's body and away from anyone else in the shop
- [ ] Demonstrates the safe pass of a chisel to another person: handle first, the receiver taking the handle before the giver lets go
- [ ] Demonstrates securing a board to the bench so it does not move when pushed by hand from any direction
- [ ] Names and demonstrates the oily-rag rule: rags from linseed, boiled linseed, tung, or danish oil are laid flat outdoors to dry, or are stored in a sealed metal can; they are never balled up in a trash can
- [ ] Names the wrist-line rule (no body part in the path the cutting edge will travel through if it slips) and shows it on a chisel held over a board
- [ ] Identifies an unfamiliar wood by stopping and asking before any cut
- [ ] Demonstrates safe tool storage at the end of a session: chisels in their rack with edges protected, saws on their hanger or in a till, planes on their sides
- [ ] Names the sharp-tool-is-safer-than-dull rule and explains why

#### Standard references (confirm each is current and the household has confirmed locally)

- [ ] ANSI/ISEA Z308.1 (Minimum Requirements for Workplace First Aid Kits and Supplies). The standard itself supplies the authoritative contents list; this node defers to it.
- [ ] American Red Cross home/shop first-aid kit guidance as an alternate recognized standard; the household chooses one and follows it.
- [ ] Local fire-safety authority confirmation of the appropriate extinguisher rating for the actual shop (the household contacts the local fire marshal or equivalent; A:B:C is the conservative default in the absence of a specific local recommendation).

**Reviewer's verdict on this node:**  `[ ] Pass`  `[ ] Pass with corrections (corrections noted in woodworking_content.py)`  `[ ] Fail (do not surface; corrections required and re-review needed)`

Corrections / notes:

```

```

---

### wc-001: Measure to a marked dimension with a tape measure and a pencil

- Node type: `technique`
- Progression band: `helper`
- Supervision required: `False`
- Current review state: reviewed = `False`, reviewer = `None`, reviewed_on = `None`

#### Hazards (confirm each is named correctly; check or correct)

- [ ] The tape's spring return can snap the metal blade back into a finger if the learner lets it run loose; a minor pinch, not a serious injury
- [ ] The end hook of a tape measure has intentional play (about 1/16 inch) to compensate for the hook's thickness for inside vs outside measurements; a learner who does not know this will get measurements that disagree between pulled and pushed readings

#### PPE required (confirm each item is correctly named, including what is forbidden; check or correct)

- [ ] Shop PPE per ws-001 (closed-toe shoes, the shop's general rules); no additional PPE for measuring

#### Supervision basis (confirm the basis is honest and the threshold is correct)

- [ ] Measuring with tape and pencil involves no cutting tool. Trade-level supervision from woodworking-root still applies through the helper band, but the work itself is low-hazard and can be performed alongside a working mentor rather than under constant watch.

#### Safety-signoff freshness window

- [ ] `fresh_safety_signoff_within_days` = `365` is appropriate for this node

#### Demonstration criteria (confirm each is measurable on the work itself and correctly states the bar; check or correct)

- [ ] Reads a marked dimension from a tape measure to the nearest 1/16 inch, agreeing with a verified second rule across five consecutive measurements
- [ ] Pencil tick falls within 1/32 inch of the intended dimension, verified against the second rule across five consecutive marks
- [ ] Tape is held tight against the work (no slack in the blade between the hook and the read point) for every measurement demonstrated
- [ ] Hook end is engaged correctly for outside measurements (pulled tight against the edge) and the play is named when the mentor asks about it
- [ ] The learner can transfer the same dimension to three points along a board and have all three marks fall within 1/32 inch of each other

**Reviewer's verdict on this node:**  `[ ] Pass`  `[ ] Pass with corrections (corrections noted in woodworking_content.py)`  `[ ] Fail (do not surface; corrections required and re-review needed)`

Corrections / notes:

```

```

---

### wc-002: Mark a line square to a reference edge with a try square and a marking knife

- Node type: `technique`
- Progression band: `helper`
- Supervision required: `True`
- Current review state: reviewed = `False`, reviewer = `None`, reviewed_on = `None`

#### Hazards (confirm each is named correctly; check or correct)

- [ ] The marking knife is sharp and short: a slip cuts the off-hand or the hand holding the square if it is in the knife's path
- [ ] The square's stock against the board: the off-hand pressing the square hard can drag across the knife edge if the knife is lifted off the line
- [ ] The keep-side / waste-side convention: a line marked on the wrong side of the intended cut wastes stock; not a hazard but a real error that compounds in downstream work

#### PPE required (confirm each item is correctly named, including what is forbidden; check or correct)

- [ ] Shop PPE per ws-001
- [ ] Safety glasses optional but recommended for dry or pitchy stock at close range
- [ ] No gloves: the marking knife is a fine tool that requires tactile feedback

#### Supervision basis (confirm the basis is honest and the threshold is correct)

- [ ] The marking knife is the learner's first edged tool in the trade. Mentor on premises with sight of the off-hand throughout helper-band practice. Mentor steps back to apprentice-level supervision (on premises, attention divided) once the learner has demonstrated the technique on at least ten boards across at least two sessions without an off-hand-in-path moment.

#### Safety-signoff freshness window

- [ ] `fresh_safety_signoff_within_days` = `365` is appropriate for this node

#### Demonstration criteria (confirm each is measurable on the work itself and correctly states the bar; check or correct)

- [ ] The marked line is square to the reference edge within 1 degree, verified by a second known-square reference across the full width of the board
- [ ] The line goes fully across the board's face from edge to edge with no gaps or skips
- [ ] The knife wall is a single continuous cut, not a series of misaligned short strokes; the pencil line follows it cleanly
- [ ] The line is on the keep side when the mentor specifies keep-side; on the waste side when the mentor specifies waste-side
- [ ] The off-hand was clear of the knife path throughout the demonstration; mentor confirms
- [ ] The learner can produce three square lines across three boards from the same reference edge with all three lines passing the squareness check

**Reviewer's verdict on this node:**  `[ ] Pass`  `[ ] Pass with corrections (corrections noted in woodworking_content.py)`  `[ ] Fail (do not surface; corrections required and re-review needed)`

Corrections / notes:

```

```

---

### wc-021: Cross-cut to a line with a panel saw

- Node type: `technique`
- Progression band: `apprentice`
- Supervision required: `True`
- Current review state: reviewed = `False`, reviewer = `None`, reviewed_on = `None`

#### Hazards (confirm each is named correctly; check or correct)

- [ ] Sharp teeth: the saw's teeth are sharper than they look, especially a recently filed crosscut blade
- [ ] Slip-into-the-finger: the saw can skip out of the kerf at the start of the cut
- [ ] Workpiece movement: a board not held still moves under the saw and walks the cut
- [ ] Eye injury from kerf dust on a dry, dusty board

#### PPE required (confirm each item is correctly named, including what is forbidden; check or correct)

- [ ] Eyes: safety glasses if the board is dry or pitchy, otherwise optional
- [ ] No loose sleeves or cuffs near the saw path
- [ ] Hair tied back if long enough to fall forward over the work
- [ ] No jewelry on the sawing hand
- [ ] No gloves: gloves reduce control of the saw and are forbidden for this technique

#### Supervision basis (confirm the basis is honest and the threshold is correct)

- [ ] Mentor on premises with sight of the cut; the mentor's role is to watch the off-hand position and the start of the kerf, the two places where a learner can hurt themselves. Mentor steps back once the learner has demonstrated start-and-finish on three boards.

#### Safety-signoff freshness window

- [ ] `fresh_safety_signoff_within_days` = `365` is appropriate for this node

#### Demonstration criteria (confirm each is measurable on the work itself and correctly states the bar; check or correct)

- [ ] The kerf falls on the waste side of the marked line, no further than 1/32 inch from the line, across the full length of the cut
- [ ] The cut face is square to the reference face of the board within roughly 1 degree, checked with a try square against the reference face
- [ ] The cut face is square to the edge of the board within roughly 1 degree, checked from the edge
- [ ] No tear-out at the exit corner: the offcut releases cleanly, not by snapping or splintering
- [ ] The learner can complete a crosscut on softwood in under 90 seconds for a 1x4, with relaxed shoulders
- [ ] The learner can complete a crosscut on hardwood in under 3 minutes for a 1x4, with the same demonstration criteria as softwood

**Reviewer's verdict on this node:**  `[ ] Pass`  `[ ] Pass with corrections (corrections noted in woodworking_content.py)`  `[ ] Fail (do not surface; corrections required and re-review needed)`

Corrections / notes:

```

```

---

## Author-flagged uncertainties (named at the time of authoring)

The author of these nodes named the following points as places where they leaned conservative but could not claim independent verification. Reviewer confirms or corrects each.

### U1. Fire-extinguisher rating

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  The node specifies A:B:C as the conservative default with a Class A exception when no flammables and no electrical are present, and defers final determination to a local fire-safety authority. Reviewer confirms this framing is correct for the household's actual shop.

  Reviewer's correction:

  ```

  ```

### U2. First-aid kit standard

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  The node defers kit contents to ANSI/ISEA Z308.1 or current American Red Cross guidance. Reviewer confirms the named standards are current and the household's chosen standard is met by the actual kit.

  Reviewer's correction:

  ```

  ```

### U3. Tropical-hardwood sensitization list

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  ws-001 names cocobolo, padauk, rosewoods, yew, and 'some other tropical hardwoods' as illustrative sensitizers. The intent is that the learner stops at any unfamiliar wood and asks before cutting. Reviewer confirms the illustrative list is accurate (not exhaustive) and the stop-and-ask rule is the load-bearing safety habit.

  Reviewer's correction:

  ```

  ```

### U4. Oily-rag remedy

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  ws-001 names two acceptable remedies: laid flat outdoors to dry, or sealed in a metal can (with water as one option). Reviewer confirms both forms of the remedy are acceptable and the local waste service's disposal rules are honored.

  Reviewer's correction:

  ```

  ```

### U5. Saw cut-time tolerances

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  wc-021 specifies 'under 90 seconds for a 1x4 in softwood' and 'under 3 minutes for a 1x4 in hardwood' as time-to-cut criteria. These are teaching-band tolerances, not published standards. Reviewer confirms these are reasonable for a learner producing a clean cut and may tune per learner.

  Reviewer's correction:

  ```

  ```

### U6. Squareness tolerance 'within 1 degree'

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  wc-002 and wc-021 use a 1-degree tolerance, checked by a verified second square. This is a teaching-band tolerance, not a furniture-maker's tolerance (arc minutes). Reviewer confirms 1 degree is appropriate for the helper-to-apprentice band.

  Reviewer's correction:

  ```

  ```

### U7. Workbench-height rule

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  ws-001 describes bench height as 'roughly level with the learner's relaxed wrist when standing'. Different traditions give different heights; this is one common teaching rule. Reviewer confirms this rule is appropriate for the work being taught at the helper-to-apprentice band.

  Reviewer's correction:

  ```

  ```

### U8. Sharp-tool-is-safer-than-dull claim

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  ws-001 names this rule and ws-001's demonstration criteria require the learner to explain it. This is universally repeated shop wisdom (a dull tool needs more force; more force means more chance of slip) but is not a measured study. Reviewer confirms the rule and the explanation expected of the learner.

  Reviewer's correction:

  ```

  ```

---

## After this review

Once every node above is set to `safety_review.reviewed = True` in `woodworking_content.py` (with `reviewer` and `reviewed_on` recorded), the woodworking trade is cleared for surfacing through the integration gate. Until then, the gate (per the `requires_human_safety_review` helper) refuses every node where the helper returns True and `safety_review.reviewed` is False.
