# Reading - Foundational (K-2) Scope & Gap Analysis

Inventory of the existing `reading_foundational_content.py` nodes (`rf-01`-`rf-25`) against a complete, prerequisite-ordered **K-2 Traditional, explicit systematic-synthetic phonics** reading scope (Saxon Phonics / Orton-Gillingham sequence: direct, mastery-based decoding, NOT whole-language or balanced literacy). Read-only analysis. **No nodes authored here.**

## How this maps to the pipeline

- **Namespace.** Content nodes are `rf-NN` (`reading_foundational_content.py`). The resolver (`node_resolver.py`) maps the scope-sequence ref `read_f_NN` <-> the content id `rf-NN` mechanically (the academic rule `{subject}_{level}_{NN}` <-> `{initial}{level}-{NN}`, with the subject token `read` <-> initial `r`; level letter `f` and the ordinal are carried through unchanged). So `read_f_05` <-> `rf-05`. Every gap id below is a real, resolvable `rf-NN` in that namespace, and its scope ref is `read_f_NN`. NOTE: the ref form is `read_f_NN` (not `reading_f_NN`); the subject key in `scope_sequences` is `phonics_reading`.
- **Generatability.** The native generator (`native_curriculum_generator.py`) reads `scope_sequences["phonics_reading"]["foundational"]` in authored order and resolves each ref to a UUID. Until a gap node is authored in all three files (a `scope_sequences` entry `read_f_NN`, a `reading_foundational_content.py` entry `rf-NN`, and a template node), the generator emits the gap ref as a `needs_content` placeholder (acceptable per the materialize guard); it does not crash.
- **Gap ids** are assigned `rf-26`, `rf-27`, ... sequentially in the prerequisite-ordered traversal below, continuing from the existing 25. Every gap's `prereq_ids` reference nodes that appear earlier in the master order (an existing `rf-01..25` or an earlier gap).

## Namespace confirmation (reported before the scope, per the task)

| | Value |
|---|---|
| Existing content nodes | 25 (`rf-01` .. `rf-25`) |
| Content id format | `rf-NN`, two-digit zero-padded |
| Scope ref format | `read_f_NN` (subject key `phonics_reading`, level `foundational`) |
| Resolver mapping | mechanical academic rule: `read_f_NN` <-> `rf-NN` (subject `read` <-> initial `r`) |
| Mapping exceptions | none for reading; it follows the mechanical rule exactly (unlike `lit`, which is a documented non-mechanical exception) |

## Summary

| | Count |
|---|---|
| Existing nodes covered (`rf-01`-`rf-25`) | 25 |
| Gap nodes to author (`rf-26`-`rf-155`) | 130 |
| **Total ordered scope** | **155** |
| Discrete fluency / automaticity nodes `[F]` (see appendix) | 13 |

Explicit-phonics posture: **phonemic awareness (section 3) is sequenced before and held distinct from letter-sound phonics (section 5)** - a common scope error is collapsing them. Fluency and automaticity targets are **discrete, separately-assessed line items** (`[F]`), not folded into decoding nodes. Sight/irregular words are taught **explicitly** (heart-word method), never by mere exposure. Decoding and its inverse, **encoding/spelling**, are sequenced coherently alongside each other. The tier terminates in genuine **cumulative assessments** (end-of-K / end-of-Grade-1 / end-of-Grade-2 reading readiness).

---

## Master ordered scope

Legend: **status** = `COVERED` (existing `rf-NN`) or `GAP` (to author). `[F]` marks a fluency/automaticity node (a discrete, assessable rate or automaticity checkpoint).


### S1 - Print Concepts & Book Handling

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 1 | rf-26 | GAP | Book orientation and handling (front/back cover, hold upright, turn pages one at a time) | - |
| 2 | rf-20 | COVERED | Print Concepts (print carries meaning; locate title and author; parts of a book) | rf-26 |
| 3 | rf-27 | GAP | Directionality of print: left-to-right, return sweep, top-to-bottom | rf-20 |
| 4 | rf-28 | GAP | Concept of word: spaces separate words; one-to-one voice-to-print matching | rf-27 |
| 5 | rf-29 | GAP | Distinguish letter vs word vs sentence; locate the first and last letter of a word | rf-28 |
| 6 | rf-30 | GAP | Recognize end punctuation in print (period, question mark, exclamation point) | rf-29 |

### S2 - Phonological Awareness (the ear: rhyme, syllables, onset-rime; NO letters)

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 7 | rf-21 | COVERED | Listening Comprehension (attend to and understand spoken language) | - |
| 8 | rf-31 | GAP | Recognize rhyming words (which two words rhyme) | rf-21 |
| 9 | rf-32 | GAP | Produce a rhyming word for a given word | rf-31 |
| 10 | rf-18 | COVERED | Nursery Rhymes and Memorization (rhyme and rhythm through recitation) | rf-32 |
| 11 | rf-33 | GAP | Segment a spoken sentence into words; count the words | rf-21 |
| 12 | rf-34 | GAP | Blend spoken syllables into a word; clap and count syllables | rf-33 |
| 13 | rf-35 | GAP | Segment and delete syllables (say the compound word without one part) | rf-34 |
| 14 | rf-36 | GAP | Onset-rime blending (blend /c/ + at into cat) | rf-34 |
| 15 | rf-37 | GAP | Onset-rime segmenting (break cat into /c/ + at) | rf-36 |
| 16 | rf-38 | GAP | Alliteration: identify spoken words that share the same beginning sound | rf-31 |

### S3 - Phonemic Awareness (DISTINCT from phonics, sequenced before letter-sounds)

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 17 | rf-02 | COVERED | Phonemic Awareness (foundational phoneme-level work) | rf-37 |
| 18 | rf-39 | GAP | Isolate the initial phoneme in a spoken word | rf-02 |
| 19 | rf-40 | GAP | Isolate the final phoneme in a spoken word | rf-39 |
| 20 | rf-41 | GAP | Isolate the medial (vowel) phoneme in a spoken word | rf-40 |
| 21 | rf-42 | GAP | Phoneme categorization: which spoken word has a different beginning/ending sound | rf-40 |
| 22 | rf-43 | GAP | Blend 2-3 spoken phonemes into a word (oral, no letters) | rf-39 |
| 23 | rf-44 | GAP | Segment a spoken word into its 2-3 phonemes (oral, no letters) | rf-43 |
| 24 | rf-45 | GAP | Blend and segment 4-phoneme words including consonant clusters (oral) | rf-44 |
| 25 | rf-46 | GAP | Phoneme deletion (say cat without the /k/) | rf-44 |
| 26 | rf-47 | GAP | Phoneme substitution (change the /k/ in cat to /h/) | rf-46 |
| 27 | rf-48 | GAP | Phoneme addition (add /s/ to the start of top) | rf-47 |
| 28 | rf-49 | GAP | Phonemic-awareness fluency: rapid oral blending and segmenting to automaticity `[F]` | rf-47 |

### S4 - Letter Naming & Formation

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 29 | rf-01 | COVERED | Letter Recognition (recognize and name letters of the alphabet) | rf-30 |
| 30 | rf-50 | GAP | Name all uppercase letters | rf-01 |
| 31 | rf-51 | GAP | Name all lowercase letters | rf-50 |
| 32 | rf-52 | GAP | Match uppercase to lowercase letters | rf-51 |
| 33 | rf-53 | GAP | Form uppercase letters with correct handwriting strokes | rf-50 |
| 34 | rf-54 | GAP | Form lowercase letters with correct handwriting strokes | rf-51 |
| 35 | rf-55 | GAP | Letter-naming automaticity (rapid, accurate letter naming) `[F]` | rf-52 |

### S5 - Letter-Sound Correspondence (the core of explicit phonics)

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 36 | rf-03 | COVERED | Consonant Sounds (consonant letter-sound correspondences) | rf-51, rf-39 |
| 37 | rf-56 | GAP | Consonant sounds set A (m, s, t, p, n) | rf-03 |
| 38 | rf-57 | GAP | Consonant sounds set B (c, k, b, d, g) | rf-56 |
| 39 | rf-58 | GAP | Consonant sounds set C (f, h, l, r, w, j) | rf-57 |
| 40 | rf-59 | GAP | Consonant sounds set D (v, y, z, qu, x) | rf-58 |
| 41 | rf-60 | GAP | Consonant sound review and rapid sound drill | rf-59 |
| 42 | rf-04 | COVERED | Short Vowels (short vowel letter-sound correspondences) | rf-41, rf-56 |
| 43 | rf-61 | GAP | Short a and short i (most contrastive short vowels) | rf-04 |
| 44 | rf-62 | GAP | Short o, short u, and short e | rf-61 |
| 45 | rf-63 | GAP | Short vowel review and contrast drill | rf-62 |
| 46 | rf-64 | GAP | Letter-sound automaticity (consonants and short vowels said instantly) `[F]` | rf-60, rf-63 |

### S6 - Blending CVC (decoding) & Segmenting (encoding)

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 47 | rf-65 | GAP | Blend VC and CVC with continuous sounds (am, Sam) using sound-by-sound blending | rf-64, rf-43 |
| 48 | rf-05 | COVERED | CVC Words (decode consonant-vowel-consonant words) | rf-65 |
| 49 | rf-66 | GAP | Decode CVC words by vowel family: short a | rf-05 |
| 50 | rf-67 | GAP | Decode CVC words: short i and short o | rf-66 |
| 51 | rf-68 | GAP | Decode CVC words: short u and short e | rf-67 |
| 52 | rf-69 | GAP | Segment CVC words to spell them (encoding CVC, the inverse of decoding) | rf-68, rf-44 |
| 53 | rf-70 | GAP | Word families and rimes (-at, -an, -ig, -op): build and read by analogy | rf-66 |
| 54 | rf-71 | GAP | CVC decoding automaticity (read CVC words accurately and automatically) `[F]` | rf-68 |

### S7 - Consonant Digraphs & Blends

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 55 | rf-06 | COVERED | Consonant Blends (consonant clusters in words) | rf-71 |
| 56 | rf-72 | GAP | Decode initial consonant blends (l-blends, r-blends, s-blends) | rf-06 |
| 57 | rf-73 | GAP | Decode final consonant blends (-st, -nd, -mp, -nt, -lk) | rf-72 |
| 58 | rf-74 | GAP | Spell words with initial and final blends (encoding) | rf-73, rf-69 |
| 59 | rf-09 | COVERED | Digraphs (consonant digraphs) | rf-71 |
| 60 | rf-75 | GAP | Digraphs sh and ch (initial and final) | rf-09 |
| 61 | rf-76 | GAP | Digraph th (voiced and unvoiced) and wh | rf-75 |
| 62 | rf-77 | GAP | Final ck and ng; trigraphs -tch and -dge | rf-76 |
| 63 | rf-78 | GAP | Decode words combining blends and digraphs | rf-77, rf-73 |
| 64 | rf-79 | GAP | Spell words with digraphs (encoding) | rf-77, rf-74 |
| 65 | rf-80 | GAP | Blends-and-digraphs decoding automaticity `[F]` | rf-78 |

### S8 - Long Vowels, Silent-e, Vowel Teams (open syllables)

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 66 | rf-07 | COVERED | Long Vowels and Silent E (VCe pattern) | rf-80 |
| 67 | rf-81 | GAP | Silent-e words: a_e and i_e | rf-07 |
| 68 | rf-82 | GAP | Silent-e words: o_e, u_e, e_e | rf-81 |
| 69 | rf-83 | GAP | Contrast short vs long vowels via silent-e (cap/cape, kit/kite) | rf-82 |
| 70 | rf-84 | GAP | Spell silent-e words (encoding) | rf-83, rf-79 |
| 71 | rf-08 | COVERED | Vowel Teams | rf-82 |
| 72 | rf-85 | GAP | Long a vowel teams: ai and ay | rf-08 |
| 73 | rf-86 | GAP | Long e vowel teams: ee and ea | rf-85 |
| 74 | rf-87 | GAP | Long o teams (oa, ow) and long i teams (igh, ie) | rf-86 |
| 75 | rf-88 | GAP | Long u and oo teams: oo (long and short), ew, ue | rf-87 |
| 76 | rf-89 | GAP | Y as a vowel: long i (my, fly) and long e (happy, baby) | rf-88 |
| 77 | rf-90 | GAP | Open-syllable long vowels (go, hi, me, she) | rf-89 |
| 78 | rf-91 | GAP | Spell vowel-team words (encoding) | rf-88, rf-84 |
| 79 | rf-92 | GAP | Vowel-team decoding automaticity `[F]` | rf-90 |

### S9 - R-controlled Vowels, Diphthongs, Advanced Patterns

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 80 | rf-93 | GAP | R-controlled vowels ar and or | rf-92 |
| 81 | rf-94 | GAP | R-controlled vowels er, ir, ur (one shared sound) | rf-93 |
| 82 | rf-95 | GAP | Diphthongs oi and oy | rf-94 |
| 83 | rf-96 | GAP | Diphthongs ou and ow (out, cow) | rf-95 |
| 84 | rf-97 | GAP | Vowel patterns aw and au | rf-96 |
| 85 | rf-98 | GAP | Soft c and soft g (ce/ci/cy, ge/gi/gy) | rf-97 |
| 86 | rf-99 | GAP | Silent-letter patterns (kn, wr, mb, gn) | rf-98 |
| 87 | rf-100 | GAP | Spell r-controlled and diphthong words (encoding) | rf-97, rf-91 |
| 88 | rf-101 | GAP | Advanced-pattern decoding automaticity `[F]` | rf-99 |

### S10 - Syllable Types, Multisyllabic Decoding & Affixes

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 89 | rf-102 | GAP | Closed and open syllable types | rf-90 |
| 90 | rf-103 | GAP | VCe, vowel-team, and r-controlled syllable types | rf-102, rf-93 |
| 91 | rf-104 | GAP | Consonant-le syllable (table, little, apple) | rf-103 |
| 92 | rf-105 | GAP | Syllable division patterns (VC/CV, V/CV) | rf-104 |
| 93 | rf-106 | GAP | Decode two-syllable words by syllable type | rf-105 |
| 94 | rf-107 | GAP | Schwa in unstressed syllables (about, zebra) | rf-106 |
| 95 | rf-108 | GAP | Decode three-syllable words | rf-107 |
| 96 | rf-109 | GAP | Inflectional endings -s and -es (plurals and verbs) | rf-106 |
| 97 | rf-110 | GAP | Inflectional endings -ing and -ed (with and without doubling) | rf-109 |
| 98 | rf-111 | GAP | Common prefixes (un-, re-, dis-, pre-) | rf-106 |
| 99 | rf-112 | GAP | Common suffixes (-ful, -less, -ly, -er, -est) | rf-111 |
| 100 | rf-113 | GAP | Spell two-syllable and affixed words (encoding) | rf-110, rf-100 |
| 101 | rf-114 | GAP | Multisyllabic decoding automaticity `[F]` | rf-108, rf-112 |

### S11 - High-Frequency / Irregular Sight Words (explicit instruction)

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 102 | rf-115 | GAP | Irregular high-frequency words taught explicitly (heart-word method: map the sounds, mark the irregular part) | rf-71 |
| 103 | rf-10 | COVERED | Sight Words First 100 | rf-115 |
| 104 | rf-116 | GAP | High-frequency word set 1 (the, a, I, is, to, of) | rf-10 |
| 105 | rf-117 | GAP | High-frequency word set 2 (was, said, you, are, they, have) | rf-116 |
| 106 | rf-118 | GAP | High-frequency word set 3 (does, where, come, some, one, two) | rf-117 |
| 107 | rf-119 | GAP | High-frequency word set 4 (their, there, would, could, should, people) | rf-118 |
| 108 | rf-120 | GAP | Spell high-frequency words (encoding the regular parts, memorizing the irregular) | rf-119, rf-113 |
| 109 | rf-121 | GAP | Sight-word reading automaticity (read high-frequency words instantly on sight) `[F]` | rf-119 |

### S12 - Decodable Connected-Text Reading

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 110 | rf-122 | GAP | Read decodable phrases and sentences (CVC plus earliest high-frequency words) | rf-71, rf-116 |
| 111 | rf-123 | GAP | Read decodable sentences with blends and digraphs | rf-80, rf-122 |
| 112 | rf-124 | GAP | Read decodable passages with long vowels and vowel teams | rf-92, rf-123 |
| 113 | rf-11 | COVERED | Fluency with Decodable Texts | rf-124 |
| 114 | rf-125 | GAP | Read decodable passages with r-controlled, diphthongs, and multisyllabic words | rf-114, rf-11 |
| 115 | rf-126 | GAP | Self-monitor and self-correct while reading decodable text (does it look right, sound right, make sense) | rf-125 |

### S13 - Fluency: Accuracy, Rate, Prosody (discrete automaticity/rate targets)

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 116 | rf-127 | GAP | Read decodable text with high accuracy (95 percent or better) | rf-126 |
| 117 | rf-128 | GAP | Read in meaningful phrases rather than word-by-word | rf-127 |
| 118 | rf-129 | GAP | Read with expression and attention to punctuation (prosody) | rf-128 |
| 119 | rf-130 | GAP | Repeated-reading routine to build rate on a decodable passage | rf-127 |
| 120 | rf-131 | GAP | End-of-Kindergarten reading-rate target (CVC and simple decodable words, correct words per minute) `[F]` | rf-127 |
| 121 | rf-132 | GAP | End-of-Grade-1 connected-text fluency-rate target (correct words per minute) `[F]` | rf-129, rf-131, rf-130 |
| 122 | rf-133 | GAP | End-of-Grade-2 connected-text fluency-rate target (accuracy plus rate plus prosody) `[F]` | rf-132 |

### S14 - Spelling / Encoding strand checkpoints (the inverse of decoding)

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 123 | rf-134 | GAP | Dictation routine: write sounds, words, and sentences from dictation | rf-69 |
| 124 | rf-135 | GAP | Spell from dictation with blends, digraphs, and silent-e | rf-134, rf-84 |
| 125 | rf-136 | GAP | Spell from dictation with vowel teams and r-controlled vowels | rf-135, rf-100 |
| 126 | rf-137 | GAP | Apply spelling rules (FLOSS, doubling, drop-e, change y to i) | rf-136, rf-113 |
| 127 | rf-138 | GAP | Encoding automaticity: spell grade-level words accurately and quickly `[F]` | rf-137, rf-120 |

### S15 - Foundational Comprehension (from decodable and read-aloud text)

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 128 | rf-22 | COVERED | Story Retelling | rf-21 |
| 129 | rf-139 | GAP | Retell a decodable story in order (beginning, middle, end) | rf-22, rf-122 |
| 130 | rf-13 | COVERED | Comprehension Sequence (order of events) | rf-139 |
| 131 | rf-14 | COVERED | Comprehension Character (who is in the story) | rf-139 |
| 132 | rf-140 | GAP | Identify the setting of a story (where and when) | rf-14 |
| 133 | rf-141 | GAP | Story elements review: character, setting, and plot together | rf-140, rf-13 |
| 134 | rf-12 | COVERED | Comprehension Main Idea | rf-139 |
| 135 | rf-142 | GAP | Identify key details that support the main idea | rf-12 |
| 136 | rf-23 | COVERED | Making Predictions | rf-12 |
| 137 | rf-143 | GAP | Make basic inferences from decodable text (what the text implies) | rf-23, rf-142 |
| 138 | rf-144 | GAP | Ask and answer who, what, where, when, why, and how about a text | rf-143 |
| 139 | rf-24 | COVERED | Text to Self Connections | rf-12 |
| 140 | rf-19 | COVERED | Vocabulary Building | rf-11 |
| 141 | rf-145 | GAP | Use context and word parts to infer the meaning of a new word | rf-19, rf-111 |
| 142 | rf-146 | GAP | Distinguish fiction from informational text | rf-141 |
| 143 | rf-147 | GAP | Compare two texts on the same topic or two versions of a story | rf-146, rf-142 |
| 144 | rf-15 | COVERED | Oral Narration | rf-21, rf-22 |
| 145 | rf-16 | COVERED | Read Aloud Response | rf-11 |
| 146 | rf-17 | COVERED | Poetry Recitation | rf-11 |

### S16 - Daily Spiral-Review Structure (explicit-phonics routines)

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 147 | rf-148 | GAP | Daily phonics review routine (sound drill, blending drill, word reading) | rf-64, rf-71 |
| 148 | rf-149 | GAP | Blending and word-ladder drill routine (change one sound at a time to make a new word) | rf-148, rf-47 |
| 149 | rf-150 | GAP | Daily dictation review routine (encode the reviewed patterns) | rf-134, rf-148 |
| 150 | rf-151 | GAP | Cumulative review checkpoints (about every five lessons, mixed decoding and encoding patterns) | rf-149, rf-126 |
| 151 | rf-152 | GAP | Error-analysis and corrections routine (diagnose why a decoding or encoding error occurred) | rf-151, rf-138 |

### S17 - Cumulative Assessments (terminal)

| # | id | status | topic | prereq_ids |
|---|----|--------|-------|-----------|
| 152 | rf-153 | GAP | End-of-Kindergarten reading readiness assessment (phonemic awareness, letter-sounds, CVC decoding, early high-frequency words, retell) | rf-49, rf-64, rf-71, rf-131, rf-22 |
| 153 | rf-154 | GAP | End-of-Grade-1 reading readiness assessment (blends and digraphs, silent-e and vowel teams, high-frequency words, decodable fluency, retell and sequence) | rf-92, rf-121, rf-132, rf-139, rf-135 |
| 154 | rf-155 | GAP | End-of-Grade-2 reading readiness assessment (multisyllabic decoding, advanced vowel patterns, fluency rate and prosody, comprehension with inference, grade-level encoding) | rf-114, rf-133, rf-143, rf-138, rf-125 |
| 155 | rf-25 | COVERED | Phonics and Reading Assessment (overall foundational reading mastery review) | rf-155 |

---

## Appendix A - Discrete fluency / automaticity targets `[F]`

The single most-omitted piece of an explicit-phonics spine (the reading analogue of math fact fluency). Each is its **own** node with an explicit automaticity or rate target (rapid, criterion-based: e.g. letters/sounds per minute, words read automatically, or correct words per minute on connected text), **not** folded into a decoding or comprehension node.

| id | fluency target | depends on |
|----|----------------|------------|
| rf-49 | Phonemic-awareness fluency: rapid oral blending and segmenting to automaticity | rf-47 |
| rf-55 | Letter-naming automaticity (rapid, accurate letter naming) | rf-52 |
| rf-64 | Letter-sound automaticity (consonants and short vowels said instantly) | rf-60, rf-63 |
| rf-71 | CVC decoding automaticity (read CVC words accurately and automatically) | rf-68 |
| rf-80 | Blends-and-digraphs decoding automaticity | rf-78 |
| rf-92 | Vowel-team decoding automaticity | rf-90 |
| rf-101 | Advanced-pattern decoding automaticity | rf-99 |
| rf-114 | Multisyllabic decoding automaticity | rf-108, rf-112 |
| rf-121 | Sight-word reading automaticity (read high-frequency words instantly on sight) | rf-119 |
| rf-131 | End-of-Kindergarten reading-rate target (CVC and simple decodable words, correct words per minute) | rf-127 |
| rf-132 | End-of-Grade-1 connected-text fluency-rate target (correct words per minute) | rf-129, rf-131, rf-130 |
| rf-133 | End-of-Grade-2 connected-text fluency-rate target (accuracy plus rate plus prosody) | rf-132 |
| rf-138 | Encoding automaticity: spell grade-level words accurately and quickly | rf-137, rf-120 |

---

## Appendix B - Strand notes (explicit-phonics rationale)

- **PA before phonics, kept distinct.** Section 2 (phonological awareness: rhyme, syllables, onset-rime) and section 3 (phonemic awareness: isolate/blend/segment/manipulate phonemes) are entirely oral, no letters. They precede and underlie section 5 (letter-sound correspondence). The existing `rf-02` Phonemic Awareness is placed at the head of section 3; early phonics (`rf-03` Consonant Sounds) depends on `isolate_initial` (a PA skill) as well as letter naming, encoding the PA-before-phonics dependency explicitly.
- **Decoding and encoding interleaved.** Every decoding band has a matching spelling/encoding node (segment-to-spell CVC, spell blends/digraphs, spell silent-e, spell vowel teams, spell advanced vowels, spell multisyllable, spell HFW), and section 14 gathers the encoding checkpoints (dictation routines, spelling rules, encoding automaticity).
- **Explicit sight words.** `heart_word_method` introduces the explicit routine (map the regular sounds, mark only the irregular part) BEFORE the high-frequency word sets, so irregular words are decoded as far as possible and only the irregular grapheme is memorized - the explicit-phonics posture, not whole-word memorization.
- **Terminal cumulative assessments.** Section 17 closes the tier with end-of-K, end-of-Grade-1, and end-of-Grade-2 reading-readiness assessments, each sampling across several prior strands (phonemic awareness, decoding, fluency rate, comprehension, encoding), mirroring the math foundational tier's cumulative-assessment capstones.
- **Legacy note (existing nodes, not re-derived here).** A few existing `rf` nodes carry prerequisites authored before this scope (e.g. `rf-15` Oral Narration -> `rf-21`, `rf-22`). They are reported COVERED with their conceptual placement; any id-ordering cleanup of the original 25 is a separate decision, exactly as the math tier left its legacy `mf-07/08 -> mf-09` ordering documented rather than silently renumbered.

---

## Authoring order note

Gaps are numbered in prerequisite-traversal order, so authoring `rf-26 -> rf-155` sequentially never references an unwritten prerequisite. Each realized node needs, in lockstep: (1) a `scope_sequences["phonics_reading"]["foundational"]` entry `read_f_NN` with `prerequisites` matching the `prereq_ids` column, (2) a `rf-NN` content entry, (3) a template node so the resolver yields a UUID. No nodes are authored in this document.

---

## Parser-style self-check

| check | result | detail |
|-------|--------|--------|
| total >= 150 | PASS | total = 155 |
| covered ids == existing rf-01..rf-25 set | PASS | covered = 25 ids; missing from covered: []; extra: [] |
| gap ids contiguous from rf-26 | PASS | gaps rf-26..rf-155 (130 ids) |
| no duplicate ids | PASS | 155 ids, 155 distinct |
| zero prerequisite-order violations (all prereqs appear earlier) | PASS | 0 violations |
| phonemic awareness (S3) entirely precedes letter-sound phonics (S5) | PASS | last PA node at master pos 28, first phonics node at master pos 36 |
| discrete fluency [F] nodes counted | PASS | 13 fluency nodes: rf-49, rf-55, rf-64, rf-71, rf-80, rf-92, rf-101, rf-114, rf-121, rf-131, rf-132, rf-133, rf-138 |

**All self-checks: PASS.**

