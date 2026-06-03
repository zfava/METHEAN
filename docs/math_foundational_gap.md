# Mathematics — Foundational (K–2) Scope & Gap Analysis

Inventory of the existing `math_foundational_content.py` nodes (`mf-01`–`mf-30`)
against a complete, prerequisite-ordered **K–2 Traditional** mathematics scope
(Saxon / Singapore spine, explicit instruction, incremental development with
continuous distributed practice). Read-only analysis. **No nodes authored here.**

## How this maps to the pipeline

- **Namespace.** Content nodes are `mf-NN` (`math_foundational_content.py`). The
  resolver (`node_resolver.py`) maps the scope-sequence ref `math_f_NN` ↔ the
  content id `mf-NN` mechanically (e.g. `math_f_31` ↔ `mf-31`). Every gap id
  below is a real, resolvable `mf-NN` in that namespace.
- **Generatability.** The native generator (`native_curriculum_generator.py`)
  reads `scope_sequences["mathematics"]["foundational"]` in authored order and
  resolves each ref to a UUID. To realize a gap node you author three things in
  prerequisite order: a `scope_sequences` entry `math_f_NN`, a
  `math_foundational_content.py` entry `mf-NN`, and a template node so it
  persists to a UUID. **Until authored, the generator emits a gap ref as a
  `needs_content` placeholder** (acceptable per the materialize guard) — it does
  not crash and does not block surrounding weeks.
- **Gap ids** are assigned `mf-31`, `mf-32`, … sequentially in the
  prerequisite-ordered traversal below. Every gap's `prereq_ids` reference nodes
  that appear earlier in the master order (existing `mf-01..30` or an earlier
  gap).

## Summary

| | Count |
|---|---|
| Existing nodes covered (`mf-01`–`mf-30`) | 30 |
| Gap nodes to author (`mf-31`–`mf-157`) | 127 |
| **Total ordered scope** | **157** |
| Discrete fluency / automaticity nodes | 12 (see §17) |

The existing 30 nodes are a thin spine: one node per topic. A Traditional K–2
program is far more incremental, and — most importantly — separates **strategy
introduction** from **fact automaticity** as distinct, separately-assessed
steps. The largest categories of gaps are: (1) early counting/subitizing
granularity, (2) **fact-fluency/automaticity targets** (the most-omitted piece,
called out as discrete nodes in §4, §5, §7, §17), (3) multi-digit computation
with/without regrouping, (4) intro to multiplication, (5) 3-digit place value,
and (6) the daily spiral-review structure (§15).

---

## Master ordered scope

Legend: **status** = `COVERED` (existing `mf-NN`) or `GAP` (to author).
`[F]` marks a fluency/automaticity node.

### §1 — Counting & Number Sense (Kindergarten)

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 1 | mf-31 | GAP | Count to 5 (one-to-one touch count) | — |
| 2 | mf-32 | GAP | Count to 10 with objects | mf-31 |
| 3 | mf-33 | GAP | Subitize quantities 1–5 (instant recognition) | mf-31 |
| 4 | mf-34 | GAP | Ten-frame representation of 0–10 | mf-32, mf-33 |
| 5 | mf-01 | COVERED | Counting to 20 | — |
| 6 | mf-03 | COVERED | One-to-One Correspondence | mf-01 |
| 7 | mf-35 | GAP | Cardinality principle (last count = total) | mf-03 |
| 8 | mf-36 | GAP | Count backward from 10 | mf-32 |
| 9 | mf-37 | GAP | Count backward from 20 | mf-01, mf-36 |
| 10 | mf-38 | GAP | Count on from any number within 20 | mf-01 |
| 11 | mf-39 | GAP | Numeral formation/writing 0–10 | mf-32 |
| 12 | mf-40 | GAP | Numeral formation/writing 11–20 | mf-01, mf-39 |
| 13 | mf-02 | COVERED | Number Recognition 0–100 | mf-01 |
| 14 | mf-04 | COVERED | Counting to 100 (by ones) | mf-01, mf-02 |
| 15 | mf-41 | GAP | Count within 120 | mf-04 |
| 16 | mf-42 | GAP | Hundreds-chart navigation (+1/+10, rows/columns) | mf-04 |
| 17 | mf-43 | GAP | Numeral writing to 100 | mf-02, mf-40 |
| 18 | mf-44 | GAP | Count on from any number within 100 | mf-04 |

### §2 — Comparing, Ordering, Patterns

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 19 | mf-45 | GAP | Compare two groups: more/fewer/same (objects) | mf-35 |
| 20 | mf-11 | COVERED | Comparing Numbers Greater/Less/Equal | mf-04 |
| 21 | mf-46 | GAP | Comparison symbols `>` `<` `=` (notation) | mf-11 |
| 22 | mf-47 | GAP | Order numbers within 100 (least → greatest) | mf-11 |
| 23 | mf-48 | GAP | One more / one less (within 100) | mf-11 |
| 24 | mf-49 | GAP | Ten more / ten less (within 100) | mf-42, mf-11 |
| 25 | mf-12 | COVERED | Ordinal Numbers (1st–10th) | mf-04 |
| 26 | mf-18 | COVERED | Patterns and Sequences | mf-01 |
| 27 | mf-50 | GAP | Growing vs repeating patterns | mf-18 |
| 28 | mf-10 | COVERED | Skip Counting by 2s, 5s, and 10s | mf-04 |
| 29 | mf-51 | GAP `[F]` | Skip-counting fluency (2s/5s/10s to 100) to automaticity | mf-10 |
| 30 | mf-20 | COVERED | Even and Odd Numbers | mf-10 |

### §3 — Place Value

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 31 | mf-09 | COVERED | Place Value Tens and Ones | mf-04 |
| 32 | mf-52 | GAP | Compose/decompose teen numbers as 10 + ones | mf-34, mf-09 |
| 33 | mf-53 | GAP | Bundle tens (groups of ten) with manipulatives | mf-09 |
| 34 | mf-54 | GAP | Two-digit numbers as tens + ones (expanded form) | mf-09 |
| 35 | mf-55 | GAP | Place value to hundreds (intro) | mf-54 |
| 36 | mf-56 | GAP | Three-digit place value: hundreds/tens/ones | mf-55 |
| 37 | mf-57 | GAP | Expanded form of three-digit numbers | mf-56 |
| 38 | mf-58 | GAP | Compare three-digit numbers | mf-56, mf-46 |
| 39 | mf-19 | COVERED | Number Lines | mf-04, mf-11 |
| 40 | mf-59 | GAP | Locate/represent numbers to 100 on a number line | mf-19 |

### §4 — Addition: concept → facts → fluency

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 41 | mf-60 | GAP | Addition concept: part–part–whole / putting together | mf-34, mf-35 |
| 42 | mf-61 | GAP | Addition within 5 (objects, `+` `=` symbols) | mf-60 |
| 43 | mf-62 | GAP `[F]` | Addition facts within 5 **to automaticity** | mf-61 |
| 44 | mf-05 | COVERED | Addition Facts to 10 | mf-01, mf-02, mf-03 |
| 45 | mf-63 | GAP `[F]` | Addition facts within 10 **to automaticity** | mf-05, mf-62 |
| 46 | mf-64 | GAP | Number bonds to 10 (pairs that make 10) | mf-05 |
| 47 | mf-65 | GAP | Doubles facts (1+1 … 5+5) | mf-05 |
| 48 | mf-66 | GAP `[F]` | Doubles facts (to 10+10) **to automaticity** | mf-65 |
| 49 | mf-67 | GAP | Near-doubles strategy | mf-66 |
| 50 | mf-68 | GAP | Make-a-ten strategy | mf-64 |
| 51 | mf-69 | GAP `[F]` | Make-ten facts **to automaticity** | mf-68 |
| 52 | mf-70 | GAP | Commutative property of addition | mf-05 |
| 53 | mf-71 | GAP | Adding zero (additive identity) | mf-61 |
| 54 | mf-72 | GAP | Count-on strategy for +1/+2/+3 | mf-38, mf-61 |
| 55 | mf-07 | COVERED | Addition Facts to 20 | mf-05, mf-09 |
| 56 | mf-73 | GAP `[F]` | Addition facts within 20 **to automaticity** | mf-07, mf-63, mf-69 |
| 57 | mf-28 | COVERED | Number Bonds to 20 | mf-07 |
| 58 | mf-25 | COVERED | Addition of Three Numbers | mf-07 |
| 59 | mf-74 | GAP | Add three numbers using make-ten / doubles | mf-25, mf-69 |

### §5 — Subtraction: concept → facts → fluency

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 60 | mf-75 | GAP | Subtraction concept: take-from / missing part | mf-60 |
| 61 | mf-76 | GAP | Subtraction within 5 | mf-75 |
| 62 | mf-77 | GAP `[F]` | Subtraction facts within 5 **to automaticity** | mf-76 |
| 63 | mf-06 | COVERED | Subtraction Facts to 10 | mf-05 |
| 64 | mf-78 | GAP `[F]` | Subtraction facts within 10 **to automaticity** | mf-06, mf-77 |
| 65 | mf-79 | GAP | Subtraction as unknown-addend (think-addition) | mf-06, mf-64 |
| 66 | mf-80 | GAP | Fact families / addition–subtraction relationship | mf-79 |
| 67 | mf-81 | GAP | Count-back strategy for −1/−2/−3 | mf-36, mf-76 |
| 68 | mf-08 | COVERED | Subtraction Facts to 20 | mf-06, mf-09 |
| 69 | mf-82 | GAP `[F]` | Subtraction facts within 20 **to automaticity** | mf-08, mf-78 |
| 70 | mf-83 | GAP `[F]` | Mixed +/− facts within 20 **to automaticity** | mf-73, mf-82 |
| 71 | mf-26 | COVERED | Mental Math Strategies | mf-07, mf-08 |
| 72 | mf-84 | GAP | Missing addend / missing subtrahend equations | mf-80 |
| 73 | mf-85 | GAP | Meaning of the equal sign (true/false, balance) | mf-61, mf-76 |

### §6 — Multi-digit Addition & Subtraction (Grade 1–2)

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 74 | mf-86 | GAP | Two-digit + one-digit (no regrouping) | mf-54, mf-73 |
| 75 | mf-87 | GAP | Add tens to a two-digit number | mf-49, mf-54 |
| 76 | mf-88 | GAP | Two-digit + two-digit (no regrouping) | mf-86, mf-87 |
| 77 | mf-89 | GAP | Subtract tens from a two-digit number | mf-49, mf-54 |
| 78 | mf-90 | GAP | Two-digit − two-digit (no regrouping) | mf-82, mf-89 |
| 79 | mf-91 | GAP | Two-digit addition **with** regrouping (ones→ten) | mf-88, mf-68 |
| 80 | mf-92 | GAP | Two-digit subtraction **with** regrouping (ten→ones) | mf-90, mf-79 |
| 81 | mf-93 | GAP | Three-digit addition (no regrouping) | mf-56, mf-88 |
| 82 | mf-94 | GAP | Three-digit addition with regrouping | mf-93, mf-91 |
| 83 | mf-95 | GAP | Three-digit subtraction (no regrouping) | mf-56, mf-90 |
| 84 | mf-96 | GAP | Three-digit subtraction with regrouping | mf-95, mf-92 |
| 85 | mf-27 | COVERED | Estimation Introduction | mf-11 |
| 86 | mf-97 | GAP | Estimate sums/differences (round to nearest ten) | mf-27, mf-49 |

### §7 — Intro to Multiplication (Grade 2)

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 87 | mf-98 | GAP | Equal groups concept | mf-51 |
| 88 | mf-99 | GAP | Repeated addition | mf-98, mf-73 |
| 89 | mf-100 | GAP | Arrays (rows × columns) | mf-99 |
| 90 | mf-101 | GAP | Skip-count to total equal groups | mf-51, mf-98 |
| 91 | mf-102 | GAP | Multiplication as repeated addition (`×` intro) | mf-99, mf-100 |
| 92 | mf-103 | GAP | ×2 facts (doubles link) | mf-102, mf-66 |
| 93 | mf-104 | GAP | ×5 facts (skip-count by 5) | mf-102, mf-101 |
| 94 | mf-105 | GAP | ×10 facts (skip-count by 10) | mf-102, mf-101 |
| 95 | mf-106 | GAP `[F]` | ×2 / ×5 / ×10 facts **to automaticity** | mf-103, mf-104, mf-105 |
| 96 | mf-107 | GAP | Doubling and halving (intro) | mf-103 |
| 97 | mf-108 | GAP | Equal sharing / partitioning (division readiness) | mf-98 |

### §8 — Measurement

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 98 | mf-109 | GAP | Compare length directly (longer/shorter) | mf-45 |
| 99 | mf-13 | COVERED | Measurement Length | mf-11 |
| 100 | mf-110 | GAP | Measure length with nonstandard units | mf-13 |
| 101 | mf-111 | GAP | Measure length with inches / centimeters (ruler) | mf-110 |
| 102 | mf-112 | GAP | Estimate & compare lengths in standard units | mf-111, mf-97 |
| 103 | mf-14 | COVERED | Measurement Weight | mf-11 |
| 104 | mf-113 | GAP | Compare capacity/volume (holds more/less) | mf-45 |
| 105 | mf-114 | GAP | Measure weight with nonstandard units | mf-14 |
| 106 | mf-115 | GAP | Temperature (hot/cold; read thermometer to 10s) | mf-42 |
| 107 | mf-116 | GAP | Length word problems (add/subtract lengths) | mf-111, mf-90 |

### §9 — Geometry

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 108 | mf-17 | COVERED | 2D Shapes | mf-01 |
| 109 | mf-117 | GAP | Attributes of 2D shapes (sides, vertices) | mf-17 |
| 110 | mf-29 | COVERED | Sorting and Classifying | mf-11, mf-17 |
| 111 | mf-118 | GAP | 3D shapes (cube, sphere, cone, cylinder) | mf-17 |
| 112 | mf-119 | GAP | Attributes of 3D shapes (faces, edges, vertices) | mf-118, mf-117 |
| 113 | mf-120 | GAP | Compose 2D shapes (combine into new shapes) | mf-117 |
| 114 | mf-121 | GAP | Compose 3D shapes | mf-119 |
| 115 | mf-122 | GAP | Partition shapes into equal parts (halves, fourths) | mf-117 |
| 116 | mf-123 | GAP | Symmetry (line of symmetry intro) | mf-117 |
| 117 | mf-124 | GAP | Position & spatial words (above/below/beside) | mf-17 |

### §10 — Fractions (partitioning)

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 118 | mf-125 | GAP | Equal vs unequal parts | mf-122 |
| 119 | mf-21 | COVERED | Fractions Visual Half and Quarter | mf-11 |
| 120 | mf-126 | GAP | Halves, thirds, fourths of a whole (regions) | mf-21, mf-125 |
| 121 | mf-127 | GAP | Fractions of a set (share equally) | mf-126, mf-108 |
| 122 | mf-128 | GAP | Naming unit fractions (one-half, one-third, one-fourth) | mf-126 |

### §11 — Time

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 123 | mf-129 | GAP | Sequence events / time words (before/after) | mf-12 |
| 124 | mf-130 | GAP | Days of week, months, calendar | mf-129 |
| 125 | mf-15 | COVERED | Time Hours and Half Hours | mf-02 |
| 126 | mf-131 | GAP | Tell time to the quarter hour | mf-15 |
| 127 | mf-132 | GAP | Tell time to five minutes | mf-131, mf-51 |
| 128 | mf-133 | GAP | A.M./P.M. and elapsed time (whole hours) | mf-132 |

### §12 — Money

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 129 | mf-16 | COVERED | Coins Identification | mf-02 |
| 130 | mf-134 | GAP | Value of coins (penny/nickel/dime/quarter) | mf-16 |
| 131 | mf-135 | GAP | Count like coins (skip count) | mf-134, mf-51 |
| 132 | mf-136 | GAP | Count mixed coins | mf-135 |
| 133 | mf-137 | GAP | Dollar bills and `$` / `¢` notation | mf-134 |
| 134 | mf-138 | GAP | Make amounts / make change (within $1) | mf-136, mf-82 |
| 135 | mf-139 | GAP | Money word problems | mf-138 |

### §13 — Data

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 136 | mf-140 | GAP | Sort objects into categories and count | mf-29 |
| 137 | mf-22 | COVERED | Tally Charts and Data | mf-01 |
| 138 | mf-141 | GAP | Picture graphs | mf-22 |
| 139 | mf-142 | GAP | Bar graphs (read and build) | mf-141 |
| 140 | mf-143 | GAP | Interpret data (how many more/less) | mf-142, mf-90 |

### §14 — Word Problems (across operations)

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 141 | mf-23 | COVERED | Word Problems Single Step Addition | mf-07 |
| 142 | mf-24 | COVERED | Word Problems Single Step Subtraction | mf-08 |
| 143 | mf-144 | GAP | Add-to / take-from / put-together problem types | mf-23, mf-24 |
| 144 | mf-145 | GAP | Compare problems (difference unknown) | mf-144 |
| 145 | mf-146 | GAP | Start-unknown / change-unknown problems | mf-144, mf-84 |
| 146 | mf-147 | GAP | Two-step word problems (within 100) | mf-145, mf-91, mf-92 |
| 147 | mf-148 | GAP | Choose the operation (mixed problem sets) | mf-147 |
| 148 | mf-149 | GAP | Equal-group / multiplication word problems | mf-102, mf-144 |

### §15 — Daily Spiral Review Structure (Saxon hallmark)

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 149 | mf-150 | GAP | Daily "Meeting" routine (calendar, counting, pattern) | mf-130, mf-18 |
| 150 | mf-151 | GAP `[F]` | Daily timed fact-practice drill routine | mf-73, mf-82 |
| 151 | mf-152 | GAP | Mixed / cumulative spiral-review problem sets | mf-148 |
| 152 | mf-153 | GAP | Cumulative review checkpoints (~every 5 lessons) | mf-152 |
| 153 | mf-154 | GAP | Error-analysis & corrections routine | mf-153 |

### §16 — Cumulative Assessments

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 154 | mf-30 | COVERED | Foundational Math Review and Assessment | — |
| 155 | mf-155 | GAP | End-of-Kindergarten cumulative assessment | mf-63, mf-78, mf-17, mf-15, mf-16 |
| 156 | mf-156 | GAP | End-of-Grade-1 cumulative assessment | mf-73, mf-82, mf-88, mf-90, mf-126 |
| 157 | mf-157 | GAP | End-of-Grade-2 cumulative assessment | mf-94, mf-96, mf-106, mf-147, mf-132, mf-138 |

---

## §17 — Fluency / Automaticity targets (discrete, assessable)

The single most-omitted piece of a Traditional math spine. Each is its **own**
node with an explicit automaticity target (typically a timed, criterion-based
check — e.g. correct-per-minute or 100% within a time window), **not** folded
into a strategy or concept node.

| id | fluency target | depends on (strategy/concept nodes) |
|----|----------------|--------------------------------------|
| mf-51 | Skip-count 2s/5s/10s to 100, automatic | mf-10 |
| mf-62 | Addition facts within 5, automatic | mf-61 |
| mf-63 | Addition facts within 10, automatic | mf-05, mf-62 |
| mf-66 | Doubles facts to 10+10, automatic | mf-65 |
| mf-69 | Make-ten facts, automatic | mf-68 |
| mf-73 | Addition facts within 20, automatic | mf-07, mf-63, mf-69 |
| mf-77 | Subtraction facts within 5, automatic | mf-76 |
| mf-78 | Subtraction facts within 10, automatic | mf-06, mf-77 |
| mf-82 | Subtraction facts within 20, automatic | mf-08, mf-78 |
| mf-83 | Mixed +/− within 20, automatic | mf-73, mf-82 |
| mf-106 | ×2 / ×5 / ×10 facts, automatic | mf-103, mf-104, mf-105 |
| mf-151 | Daily timed fact-drill routine (delivery structure) | mf-73, mf-82 |

The existing nodes `mf-05`/`mf-06`/`mf-07`/`mf-08` teach the **facts**; the new
`mf-62/63/73` and `mf-77/78/82/83` are the **automaticity checkpoints** layered
on top. This separation is the core gap a Saxon/Singapore spine fills.

---

## Authoring order note

Gaps are numbered in prerequisite traversal order, so authoring `mf-31 → mf-157`
sequentially never references an unwritten prerequisite. Each realized node
needs, in lockstep: (1) a `scope_sequences["mathematics"]["foundational"]` entry
`math_f_NN` with `prerequisites` matching the `prereq_ids` column, (2) a
`mf-NN` content entry, (3) a template node so the resolver yields a UUID. No
nodes are authored in this document.
