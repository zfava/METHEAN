# Gardening / horticulture safety review checklist

Generated from `backend/app/content/gardening_content.py`. The checklist below renders the actual hazards, PPE, and demonstration criteria for every authored node. Do not edit the node content from this checklist; edit `gardening_content.py` and regenerate this file. No node may be surfaced to a learner until its `safety_review.reviewed` is set to True by a qualified human reviewer, with `reviewer` and `reviewed_on` recorded; this is the contract this checklist exists to support.

## Reviewer identification

- Reviewer name: ____________________________________________
- Relevant garden / horticulture experience (years, type, credentials; market grower, master gardener, cooperative-extension agent, working farmer, certified horticulturist, etc.): ____________________________________________
- Date of this review: ____________________________________________

## Completion contract

On completion of this review, for each node confirmed correct:

1. In `backend/app/content/gardening_content.py`, set the node's `safety_review.reviewed` to `True`, `safety_review.reviewer` to the reviewer's name and credentials, and `safety_review.reviewed_on` to the date in ISO 8601 (`YYYY-MM-DD`).
2. If any item below requires correction, the correction is made in `gardening_content.py` and this checklist is regenerated, and the review is repeated on the corrected node.
3. No node where `safety_review.reviewed` is `False` may be surfaced to a learner. The integration gate is the responsibility of `learning_context` (see the TODO in `backend/app/services/node_content.py::requires_human_safety_review`).

---

## Per-node review

### gardening-root: Gardening and horticulture (food-garden first)

- Node type: `root`
- Supervision required: see `default_supervision_policy` (hand-tool: helper-band supervised, apprentice-band mentor on premises, journeyman optional with current safety; power-tool: supervised through journeyman; ladder: supervised through journeyman; chemical application: supervised, not authored in helper or apprentice bands)
- Current review state: reviewed = `False`, reviewer = `None`, reviewed_on = `None`

**Reviewer's verdict on this node:**  `[ ] Pass`  `[ ] Pass with corrections (corrections noted in gardening_content.py)`  `[ ] Fail (do not surface; corrections required and re-review needed)`

Corrections / notes:

```

```

---

### gs-001: Garden safety: sun and heat, soil-borne hazards, hand-tool injuries, allergens and toxic plants, water hazards, and lifting

- Node type: `safety`
- Progression band: `helper`
- Supervision required: `True`
- Current review state: reviewed = `False`, reviewer = `None`, reviewed_on = `None`

#### Hazards (confirm each is named correctly; check or correct)

- [ ] Sun and heat exposure: outdoor garden work in warm months carries real risk of sunburn, dehydration, heat exhaustion, and heat stroke. The household follows current CDC / NIOSH outdoor-worker heat-illness guidance for hydration, rest in shade, and watching for early symptoms.
- [ ] Soil-borne wounds and tetanus risk: a puncture or laceration in soil can introduce tetanus and other soil bacteria. The household ensures every member's tetanus immunization status is current per their healthcare provider's recommendation; the node does not name a specific interval.
- [ ] Sharp hand-tool injuries: pruners, hori-hori knives, sharpened trowels, scissors, and harvest knives are all sharp enough to cut a hand. A hori-hori in particular has both a serrated and a straight edge; both can injure.
- [ ] Allergens and toxic plants: poison ivy, poison oak, and poison sumac cause contact dermatitis from urushiol; other regional plants (depending on the household's location) can also cause contact or systemic reactions. The household uses the state cooperative extension service to learn the specific toxic plants in their region; the node does not enumerate.
- [ ] Stinging insects: bees, wasps, hornets, and yellow jackets nest in and around gardens, especially in summer. For any household member with a known sting allergy, the household's anaphylaxis-management plan governs and the mentor knows where the epinephrine is.
- [ ] Tick exposure (region-dependent): in many regions ticks carry Lyme disease, Rocky Mountain spotted fever, or other vector-borne illnesses. The household follows current CDC tick-prevention and tick-check guidance for their region.
- [ ] Lifting strain: full bags of soil, compost, mulch, and harvest crates can exceed a learner's safe carry weight. Bend at the knees not the back; carry loads close to the body; ask for help with anything that does not feel light.
- [ ] Water-borne hazards: standing water in barrels, ponds, and large containers is a drowning hazard for young children. Rain barrels and water features are covered or fenced per the household's safety arrangement.
- [ ] Slips and falls: wet soil, hoses laid across paths, and uneven ground are tripping hazards. Hoses are coiled or laid against an edge when not in use; tools are not left on the ground in path lines.

#### PPE required (confirm each item is correctly named, including what is allowed; check or correct)

- [ ] Closed-toe shoes or boots: leather garden boots preferred; no sandals or bare feet in the garden. A sharp tool dropped point-down is the easiest soil-borne injury in the trade.
- [ ] Sun-rated clothing or sunscreen: a brimmed sun hat, long sleeves rated for sun protection, OR a broad-spectrum sunscreen at the SPF and reapplication interval recommended by the household's healthcare provider or current CDC / Skin Cancer Foundation public guidance. The node does not specify an SPF number; the household chooses per their skin and the day's UV index.
- [ ] Garden gloves: leather or coated cloth gloves are allowed AND recommended for most garden work to reduce thorn punctures, hand abrasions, and soil contact with broken skin. This is the opposite of the woodworking shop's no-gloves-on-edged-tools rule because the dominant hazards differ: in the garden the puncture and the allergen win, in the shop the loss of feel wins. Gloves come off for fine tasks where touch is needed (handling small seed, transplanting fragile seedlings) and the mentor names when each is correct.
- [ ] Long pants and long sleeves for tick-active regions and seasons, per current CDC tick-prevention guidance for the household's region.
- [ ] Eye protection (safety glasses): required for any cutting work overhead (small-tree pruning at apprentice band and above), for any string-trimmer or mower work (gated separately, not in this batch), and for any work where soil or compost is being moved in wind. Optional for low-risk ground tasks.
- [ ] Hair tied back if long enough to fall forward when bending over a planting row or when working with stinging or thorny plants.

#### Supervision basis (confirm the basis is honest and the threshold is correct)

- [ ] The safety competency is itself supervised: an adult mentor walks the learner through every hazard in the actual garden and the actual tool shed and signs off only when the learner can name and locate each. There is no self-attestation on safety. The mentor also confirms the household's plans for tetanus status, anaphylaxis (if applicable), water-feature safety, and chemical storage in their particular situation.

#### Demonstration criteria (confirm each is measurable on the work itself and correctly states the bar; check or correct)

- [ ] Names every PPE item on the list and explains when each is required and when each is optional
- [ ] Locates the first aid kit and confirms it meets a recognized standard (ANSI/ISEA Z308.1 or current American Red Cross guidance), and points to the tweezers specifically if the household is in a tick-active region
- [ ] Locates the drinking water and shade area and names the household's rule for hot-day breaks (or names that the household defers to current CDC / NIOSH outdoor-worker heat-illness guidance for the day's conditions)
- [ ] Names the household's tetanus immunization status arrangement and confirms with the mentor that every working household member is current per their healthcare provider's recommendation
- [ ] Demonstrates the safe carry of a hori-hori or pruners: blade closed or sheathed, edge controlled, the carrier walking with the tool angled away from their body and away from anyone else in the garden
- [ ] Demonstrates the safe pass of a sharp garden tool to another person: handle first, the receiver taking the handle before the giver lets go
- [ ] Names the wrist-line rule (no body part in the path the cutting edge will travel through if it slips) and shows it on a hori-hori or trowel held over a planting hole
- [ ] Names the regional toxic plants the household has identified using the state cooperative extension service, and demonstrates the stop-and-ask rule on any unfamiliar plant before bare-armed contact
- [ ] Names the household's anaphylaxis plan if applicable (where the epinephrine is, when to use it, when to call emergency services) per the household's healthcare provider's instructions; if no household member has a known sting allergy, names the general first-response rule for an apparent severe reaction (call emergency services)
- [ ] Names the tick rule for the region per current CDC tick-prevention guidance (cover skin in tick season, perform a tick check after the session, use the tweezers from the first aid kit to remove a tick with steady straight pull and save the tick if illness develops); in regions where ticks are not a concern, names that no tick rule applies and the mentor confirms
- [ ] Demonstrates safe lifting form on a real bag of soil or compost (or refuses to lift it because it is too heavy and asks for help; both are correct answers)
- [ ] Demonstrates safe tool storage at the end of a session: sharp tools returned to their shed or rack, hoses coiled, no tools left in path lines
- [ ] Names the sharp-tool-is-safer-than-dull rule and explains why
- [ ] Demonstrates washing any scratch or cut at the spigot before the end of the session, and names when a wound exceeds first-aid-kit scope and the mentor or household healthcare contact must be called

#### Standard references (confirm each is current and the household has confirmed locally)

- [ ] ANSI/ISEA Z308.1 (Minimum Requirements for Workplace First Aid Kits and Supplies). The standard itself supplies the authoritative contents list; this node defers to it.
- [ ] American Red Cross home/garden first-aid kit guidance as an alternate recognized standard; the household chooses one and follows it.
- [ ] Current CDC / NIOSH outdoor-worker heat-illness prevention guidance, including hydration, rest in shade, and recognition of early heat-illness symptoms. The household reads the current guidance for their conditions; this node does not name a specific water volume or break interval.
- [ ] Current CDC tick-prevention and tick-removal guidance for tick-active regions. The household identifies whether their region is tick-active per the CDC's regional information.
- [ ] Tetanus immunization status per each household member's healthcare provider's recommendation. This node does not write a tetanus booster interval; the household's healthcare provider sets it per current ACIP / CDC guidance.
- [ ] Each state's cooperative extension service for the regional list of toxic plants (poison ivy / oak / sumac, regional toxics) and for regional pest, disease, and soil information. The household identifies their state's extension service and uses it as the regional safety reference.
- [ ] Each household member with a known sting or other anaphylaxis allergy has an individual anaphylaxis-management plan from their healthcare provider; this node defers to that plan and to current emergency-medical guidance for severe allergic reactions.
- [ ] Sun-exposure protection (broad-spectrum SPF, brimmed hat, UV-rated clothing) per current public-health guidance (CDC / Skin Cancer Foundation). The household chooses the SPF and reapplication interval per their conditions; this node does not specify a number.

**Reviewer's verdict on this node:**  `[ ] Pass`  `[ ] Pass with corrections (corrections noted in gardening_content.py)`  `[ ] Fail (do not surface; corrections required and re-review needed)`

Corrections / notes:

```

```

---

### gc-001: Read a seed packet for spacing, depth, sun, water, days-to-maturity, and direct-sow vs. transplant

- Node type: `technique`
- Progression band: `helper`
- Supervision required: `False`
- Current review state: reviewed = `False`, reviewer = `None`, reviewed_on = `None`

#### Hazards (confirm each is named correctly; check or correct)

- [ ] Misreading the depth instruction can lead to a learner planting seed too deep (it does not germinate) or too shallow (it dries out before germination); not a safety hazard but a real wasted-work error that compounds across a season
- [ ] Misreading direct-sow vs. start-indoors-and-transplant can have a learner sowing a tomato seed outdoors in cold soil where it will rot, or starting indoors a carrot whose taproot dislikes transplanting; not a safety hazard but a real wasted-season error
- [ ] Seed treatment warnings on the packet (some commercial seed is treated with fungicide or insecticide and is labeled with handling and disposal cautions): the learner reads the warning and applies it. The node does not enumerate the chemicals; the packet's label and the EPA-registered information govern.
- [ ] Seed storage: opened seed packets stored damp or warm lose viability. Not a safety hazard but the practice is part of the doing.

#### PPE required (confirm each item is correctly named; check or correct)

- [ ] Garden PPE per gs-001 (closed-toe shoes, garden gloves if handling treated seed); no additional PPE for reading the packet itself

#### Supervision basis (confirm the basis is honest and the threshold is correct)

- [ ] Reading a packet involves no cutting tool, no body load, and no exposure. Trade-level supervision from gardening-root still applies through the helper band, but the reading itself is low-hazard and can be performed alongside a working mentor rather than under constant watch. The mentor confirms the learner's extracted numbers before any sowing happens.

#### Safety-signoff freshness window

- [ ] `fresh_safety_signoff_within_days` = `365` is appropriate for this node

#### Demonstration criteria (confirm each is measurable on the work itself and correctly states the bar; check or correct)

- [ ] Extracts every operative field from a real packet onto a planting card: crop and variety, direct-sow vs. start-indoors, weeks-before-last-frost (if indoors) or soil condition (if direct-sow), depth, in-row spacing, between-row spacing, thinning, sun, water, days-to-maturity
- [ ] Names which DTM counting convention applies to the crop (from sowing for direct-sown crops, from transplant for transplanted crops) and points to where the packet says so, or names that the packet did not say and the household defers to the seed company's website or the cooperative extension service
- [ ] Names the household's last frost and first frost dates from a local source and explains how the packet's calendar instructions anchor to them
- [ ] Names any seed treatment warning on the packet and the handling rule that follows (gloves on, no eating, packet stored away from food); if the packet has no treatment warning, names that and confirms with the mentor
- [ ] Names the storage rule for any leftover seed: cool, dry, dark, in a labeled envelope or jar, with the open date written on the label
- [ ] Reads three different packets for three different crops onto three planting cards correctly, with the mentor verifying each card before any sowing

**Reviewer's verdict on this node:**  `[ ] Pass`  `[ ] Pass with corrections (corrections noted in gardening_content.py)`  `[ ] Fail (do not surface; corrections required and re-review needed)`

Corrections / notes:

```

```

---

### gc-002: Use a trowel or hori-hori knife to dig a planting hole at correct depth and width

- Node type: `technique`
- Progression band: `helper`
- Supervision required: `True`
- Current review state: reviewed = `False`, reviewer = `None`, reviewed_on = `None`

#### Hazards (confirm each is named correctly; check or correct)

- [ ] Sharp tool: a hori-hori has both a serrated edge and a straight edge; a sharpened trowel has a sharpened front edge. A slip can cut the off-hand or the leg if the tool path is not controlled.
- [ ] Off-hand-in-path: the off-hand steadies the soil or the plant, and a learner can put a finger directly under the trowel's tip on a downward stroke if the wrist-line rule is not held
- [ ] Kneeling strain and knee injury on hard or stony ground: the learner is typically kneeling for ten to thirty minutes per session; without a kneeling pad on hard ground the knee bursa can become inflamed
- [ ] Back strain from bending repeatedly at the waist: leaning over to dig from a standing position rather than kneeling can strain the lower back over a long session
- [ ] Soil contact: a hand cut while digging makes immediate contact with soil bacteria; the wound-wash and tetanus-status habits from gs-001 govern
- [ ] Buried hazards (root, rock, glass, or wire in old garden soil): the trowel can strike or be deflected by a buried object; the learner stops on any unexpected resistance and looks before pushing

#### PPE required (confirm each item is correctly named; check or correct)

- [ ] Garden PPE per gs-001 (closed-toe shoes, hat, water, sun protection)
- [ ] Garden gloves on for general digging; off for the moment of fine placement
- [ ] A kneeling pad on any ground harder than soft loam, or a low garden stool
- [ ] Eye protection optional but recommended when working in dry, windy conditions where soil or compost might blow into the face

#### Supervision basis (confirm the basis is honest and the threshold is correct)

- [ ] The hori-hori (or sharpened trowel) is the learner's first sharp garden tool in the trade. Mentor on premises with sight of the off-hand and the tool path throughout helper-band practice. Mentor steps back to apprentice-level supervision (on premises, attention divided) once the learner has demonstrated the technique on at least ten holes across at least two sessions without an off-hand-in-path moment and with correct kneeling form.

#### Safety-signoff freshness window

- [ ] `fresh_safety_signoff_within_days` = `365` is appropriate for this node

#### Demonstration criteria (confirm each is measurable on the work itself and correctly states the bar; check or correct)

- [ ] The finished hole reaches the depth specified by the planting card or the mentor, within roughly 1/2 inch, verified by holding the trowel or the plant beside the hole
- [ ] The finished hole is at least the width of the intended root ball plus roughly 1 inch all around at the bottom; the bottom is roughly flat, not pointed
- [ ] The displaced soil is in the bucket or on the tarp, not scattered across the bed where the next plant will go
- [ ] The off-hand was clear of the trowel path throughout the demonstration; the mentor confirms
- [ ] The learner is kneeling on a pad (or seated on a stool) with the back roughly straight, not bent over from a standing position
- [ ] The trowel was set down on a known surface (the bucket, the tarp, beside the hole on the soil-tarp side) between strokes, never in the path the learner moves through
- [ ] On any buried hazard struck during the dig (root, rock, glass, wire), the learner stopped, named the object, and asked the mentor before continuing
- [ ] The learner can dig three holes for three different specifications (seed depth, small transplant, larger transplant) on softer ground in a single session

**Reviewer's verdict on this node:**  `[ ] Pass`  `[ ] Pass with corrections (corrections noted in gardening_content.py)`  `[ ] Fail (do not surface; corrections required and re-review needed)`

Corrections / notes:

```

```

---

### gc-021: Transplant a tray of started seedlings to a prepared garden bed at correct spacing

- Node type: `technique`
- Progression band: `apprentice`
- Supervision required: `True`
- Current review state: reviewed = `False`, reviewer = `None`, reviewed_on = `None`

#### Hazards (confirm each is named correctly; check or correct)

- [ ] Sharp tool: a trowel or hori-hori is in use for every hole; the hazards from gc-002 carry forward (off-hand-in-path, slip into the leg or hand)
- [ ] Sun and heat exposure: transplanting is typically done at the season's warmest moments and the learner is outdoors for an hour or more; the sun-and-water habit from gs-001 governs
- [ ] Stooping and kneeling for an extended session: a tray of twelve to fifty seedlings transplanted in one session compounds back and knee strain
- [ ] Damage to the seedling: rough handling of the root ball, planting at the wrong depth for the crop, or planting on a hot afternoon when the seedling wilts before recovering can kill a young plant. Not a safety hazard for the learner but a real wasted-work error if the work is not done correctly.
- [ ] Transplant shock: even correct transplanting causes some shock; the learner learns to recognize normal shock (wilting on day one, recovering by day three) from abnormal shock (collapse, root rot, sun scald)
- [ ] Soil contact in cuts: any small hand cut during the session is in immediate contact with soil; the wound-wash and tetanus-status habits from gs-001 govern

#### PPE required (confirm each item is correctly named; check or correct)

- [ ] Garden PPE per gs-001 (closed-toe shoes, hat, water, sun protection)
- [ ] Garden gloves on for soil handling; OFF for the moment of root-ball release and seedling placement, where touch matters
- [ ] Kneeling pad or low stool
- [ ] Eye protection optional; recommended in dry, windy conditions

#### Supervision basis (confirm the basis is honest and the threshold is correct)

- [ ] Transplanting is the apprentice band's first multi-step technique that combines a sharp tool, a living organism, and a real bed. Mentor on premises with sight of the work for the first three transplants of each new crop. Mentor steps back to apprentice-level supervision (on premises, attention divided) once the learner has demonstrated correct depth, spacing, root-ball handling, and watering-in on three transplants of the crop. Mentor returns to direct watch for any new crop the learner has not transplanted before, because the planting depth and root-ball handling rules differ across crop families.

#### Safety-signoff freshness window

- [ ] `fresh_safety_signoff_within_days` = `365` is appropriate for this node

#### Demonstration criteria (confirm each is measurable on the work itself and correctly states the bar; check or correct)

- [ ] Every transplant in the row is at the in-row spacing the planting card specifies, within roughly 1 inch, measured by tape or marked stick
- [ ] Every row is at the between-row spacing the planting card specifies, within roughly 1 inch
- [ ] Every transplant is at the correct planting depth for its crop: tomato-family deeper than the cell soil line; brassicas, lettuces, and most herbs at the cell soil line; alliums shallow with the tip just at or above the soil line; the learner names which rule applies to each crop and the mentor confirms
- [ ] Every root ball is intact at the moment of placement: the plug came out of the cell without fracturing, the roots are pale and branching, no major root mass left in the cell
- [ ] Every transplant is held by the leaves and the root ball, never by the stem, during transfer from the cell to the hole; the mentor confirms by watching the hand position
- [ ] Every transplant is firmed gently by fingertip, not compacted by palm; the soil around the root ball is in full contact with the root ball, no visible air gaps
- [ ] Every transplant is watered in immediately after planting, with a gentle flow at the base, until water visibly pools and drains; the learner does not blast the seedling with a jet of water
- [ ] The off-hand was clear of the trowel path throughout each hole; the mentor confirms
- [ ] The learner completes a row of six to twelve transplants in a single session without leaving any plant out of the soil for more than the time it takes to dig its hole (roots exposed to sun and air for prolonged periods dry out)
- [ ] On the next session (24 to 72 hours later), the learner observes the transplants and names which look healthy (perked up, leaves firm), which are in normal transplant shock (slight wilt, recovering), and any that need attention (severe wilt, collapse, sun scald, signs of pest damage)

**Reviewer's verdict on this node:**  `[ ] Pass`  `[ ] Pass with corrections (corrections noted in gardening_content.py)`  `[ ] Fail (do not surface; corrections required and re-review needed)`

Corrections / notes:

```

```

---

## Author-flagged uncertainties (named at the time of authoring)

The author of these nodes named the following points as places where they leaned conservative but could not claim independent verification. Reviewer confirms or corrects each.

### U1. Tetanus booster interval

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  gs-001 does not name a specific tetanus booster interval. It defers to each household member's healthcare provider for current tetanus immunization status per current ACIP / CDC guidance. Reviewer confirms this deferral is correct and that no specific interval should be written into the node.

  Reviewer's correction:

  ```

  ```

### U2. Sunscreen SPF level and reapplication interval

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  gs-001 does not name a specific SPF number or reapplication interval. It defers to current CDC / Skin Cancer Foundation public guidance and to the household's healthcare provider per the household's skin and the day's UV index. Reviewer confirms this deferral is correct.

  Reviewer's correction:

  ```

  ```

### U3. Hardening-off duration

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  gc-021 names "7 to 10 days of progressive outdoor exposure" as the common teaching rule for hardening-off, flagged in the node as a teaching tolerance, not a published standard. The mentor confirms readiness per the crop and the household's setup. Reviewer confirms this teaching tolerance is appropriate and that the mentor's final-call rule is the correct safeguard.

  Reviewer's correction:

  ```

  ```

### U4. Planting-depth rules per crop family

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  gc-021 names three crop-family planting-depth rules: tomato-family deeper than the cell soil line; brassicas, lettuces, and most herbs at the cell soil line; alliums shallow with the tip just at or above the soil line. These are commonly taught rules but vary by tradition and by crop-within-family. Reviewer confirms the three rules are accurate for the bands authored here and that the planting card / mentor / cooperative extension is the load-bearing reference for crops outside these three families.

  Reviewer's correction:

  ```

  ```

### U5. Watering-in volume rule

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  gc-021 specifies watering-in "with a gentle flow at the base of the plant until water visibly pools and drains." The volume is unstated by design (a 4-inch plug receives roughly 1 to 2 quarts in practice, but the visible-pool-and-drain rule is the criterion). Reviewer confirms the visible-pool-and-drain rule is the right criterion for the helper-to-apprentice band rather than a fluid-ounce target.

  Reviewer's correction:

  ```

  ```

### U6. Spacing distances per crop

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  gc-021 defers all spacing distances entirely to the planting card produced from gc-001, which in turn defers to the seed packet for the specific crop. No invented spacing numbers are in the nodes. Reviewer confirms this deferral is correct and the seed packet is the load-bearing reference.

  Reviewer's correction:

  ```

  ```

### U7. Days-to-maturity counting convention

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  gc-001 names that DTM is counted from sowing for direct-sown crops and from transplant out for transplanted crops, and points the learner to the packet for the per-crop statement. Reviewer confirms this convention is correct and that the packet (or the seed company's instructions / state cooperative extension) governs in cases where the packet does not state explicitly.

  Reviewer's correction:

  ```

  ```

### U8. Sharp-garden-tool-is-safer-than-dull rule

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  gs-001 carries the sharp-tool-is-safer rule, mirroring the woodworking shop's rule for the same reason (a sharp tool takes less force and gives more control), specifically applied to hori-hori, pruners, and harvest knives. This is universally repeated horticulture-and-shop wisdom but is not a measured study. Reviewer confirms the rule and the explanation expected of the learner.

  Reviewer's correction:

  ```

  ```

### U9. Tick-active region designation

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  gs-001 defers the determination of whether the household's region is tick-active to current CDC regional tick information. The node does not enumerate which states or counties are tick-active; the household identifies their region per the CDC. Reviewer confirms this deferral is correct.

  Reviewer's correction:

  ```

  ```

### U10. Regional toxic-plant list

- [ ] **Confirmed as authored.** Notes: 

- [ ] **Correction required.** Authored framing: 

  gs-001 names poison ivy / oak / sumac as the universally identified toxic plants for contact (urushiol) and defers the regional list of other toxic plants entirely to the state cooperative extension service. The node does not enumerate. Reviewer confirms this deferral is correct and the state cooperative extension is the load-bearing regional reference.

  Reviewer's correction:

  ```

  ```

---

## After this review

Once every node above is set to `safety_review.reviewed = True` in `gardening_content.py` (with `reviewer` and `reviewed_on` recorded), the gardening trade is cleared for surfacing through the integration gate. Until then, the gate (per the `requires_human_safety_review` helper) refuses every node where the helper returns True and `safety_review.reviewed` is False.
