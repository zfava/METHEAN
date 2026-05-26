"""Pre-enriched content for Mathematics Developing template nodes."""

MATH_DEVELOPING_CONTENT = {
    "md-01": {
        "enriched": True,
        "learning_objectives": [
            "Add three-digit numbers with and without regrouping",
            "Subtract three-digit numbers including across one regrouping",
            "Use expanded-form and decomposition strategies before reaching for the standard algorithm",
            "Estimate the answer first and judge whether the computed result is reasonable",
        ],
        "teaching_guidance": {
            "introduction": "The child already adds and subtracts within 20 and works with two-digit numbers. The task now is to extend the same place-value thinking to the hundreds, where regrouping can happen at the tens column, the hundreds column, or both. Begin with base-ten blocks so the regrouping is something the child does with their hands before it is something they write down. Names the trade out loud every time: ten ones is one ten, ten tens is one hundred.",
            "scaffolding_sequence": [
                "Build three-digit numbers with base-ten blocks (hundreds flats, tens rods, ones cubes) and read the number aloud in place-value language",
                "Add two three-digit numbers with no regrouping by combining like blocks: hundreds with hundreds, tens with tens, ones with ones",
                "Add two three-digit numbers that regroup at the ones column, physically trading ten ones for a ten before counting the tens",
                "Add two three-digit numbers that regroup at the tens column, trading ten tens for a hundred",
                "Subtract three-digit numbers without regrouping, then with regrouping at the ones column, then at the tens column",
                "Record what the blocks are doing using expanded form (300 + 40 + 7) before introducing column notation",
                "Always estimate first by rounding to the nearest hundred, solve, then compare to the estimate",
            ],
            "socratic_questions": [
                "What do you notice about the ones column? Is there enough to keep as ones, or do we need to trade?",
                "If we trade ten ones for one ten, has the total changed?",
                "Your estimate was 500 and you got 487. Does that seem reasonable, and how do you know?",
                "When we subtract and the top digit is smaller, what can we borrow from, and why does it become ten?",
            ],
            "practice_activities": [
                "Play 'race to 1000': roll three dice, build the number with blocks, add to a running total, race a partner",
                "Solve grocery-receipt problems: add three priced items mentally, then verify on paper",
                "Subtraction story: a savings jar starts at 524 cents, child spends 178 cents, how much remains?",
            ],
            "real_world_connections": [
                "Tracking page numbers read across a chapter book",
                "Counting steps on a long walk or hike",
                "Calculating change from a hundred-dollar bill in a pretend shop",
                "Adding daily step counts across a week",
            ],
            "common_misconceptions": [
                "Adding across columns without regrouping (writing 14 in the ones column instead of carrying the ten)",
                "Subtracting the smaller digit from the larger regardless of position (e.g., treating 43 - 28 as 8 - 3 = 5 in the ones)",
                "Forgetting to update the tens column after borrowing from it",
                "Thinking that 'borrowing' actually removes value from the number, instead of just renaming it",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Adds and subtracts three-digit numbers with one regrouping correctly on 8 of 10 problems",
                "Explains regrouping in place-value language: ten ones is one ten, ten tens is one hundred",
                "Catches an unreasonable answer by comparing it to an estimate before declaring the work done",
            ],
            "assessment_methods": ["mixed paper computation", "oral place-value explanation", "block-based demonstration"],
            "sample_assessment_prompts": [
                "Solve 247 + 365 and show your work in place-value language",
                "Solve 503 - 178 and explain what you traded and why",
                "Estimate 489 + 312 to the nearest hundred. Then solve exactly. Was your estimate close?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is 234 + 152?",
                "expected_type": "number",
                "correct_answer": "386",
                "hints": ["Add the ones, then the tens, then the hundreds, no regrouping needed"],
                "explanation": "234 + 152. Ones: 4 + 2 = 6. Tens: 3 + 5 = 8. Hundreds: 2 + 1 = 3. Answer: 386.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is 247 + 365?",
                "expected_type": "number",
                "correct_answer": "612",
                "hints": ["Ones: 7 + 5 = 12, write 2 carry 1", "Tens: 4 + 6 + 1 carried = 11, write 1 carry 1"],
                "explanation": "247 + 365. Ones: 12, write 2 carry 1. Tens: 4+6+1 = 11, write 1 carry 1. Hundreds: 2+3+1 = 6. Answer: 612.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is 503 - 178?",
                "expected_type": "number",
                "correct_answer": "325",
                "hints": ["The ones place needs to borrow", "You will need to borrow from the hundreds to make the tens column usable"],
                "explanation": "503 - 178. Cannot do 3 - 8 in ones, borrow from tens, but tens is 0, so borrow from hundreds first. 503 becomes 4 hundreds, 9 tens, 13 ones. 13-8 = 5, 9-7 = 2, 4-1 = 3. Answer: 325.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Estimate 489 + 312 by rounding each number to the nearest hundred. What is your estimate?",
                "expected_type": "number",
                "correct_answer": "800",
                "hints": ["489 rounds to 500", "312 rounds to 300"],
                "explanation": "489 rounds to 500, 312 rounds to 300, so the estimate is 800. (The exact answer is 801, so the estimate is very close.)",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "A library has 624 books. They donate 167 to another school. How many books remain?",
                "expected_type": "number",
                "correct_answer": "457",
                "hints": ["This is subtraction: 624 - 167", "You will need to regroup more than once"],
                "explanation": "624 - 167. Ones: borrow, 14 - 7 = 7. Tens: 1 (after lending) - 6, borrow, 11 - 6 = 5. Hundreds: 5 - 1 = 4. Answer: 457 books remain.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Solve 358 + 274 and write each step in place-value language.",
                "type": "number",
                "correct_answer": "632",
                "target_concept": "three_digit_addition_with_regrouping",
            },
            {
                "prompt": "Solve 700 - 246.",
                "type": "number",
                "correct_answer": "454",
                "target_concept": "three_digit_subtraction_across_zeros",
            },
            {
                "prompt": "Estimate 678 + 219 to the nearest hundred. Then solve exactly. Is your estimate reasonable?",
                "type": "open_response",
                "rubric": "Mastery: rounds correctly (700+200=900), computes correctly (897), and compares meaningfully. Proficient: rounds and computes correctly but does not compare. Developing: errors in rounding or computation.",
                "target_concept": "estimation_and_verification",
            },
        ],
        "resource_guidance": {
            "required": ["base-ten blocks (hundreds, tens, ones)", "place-value mat", "pencil and paper for column work"],
            "recommended": ["hundred chart", "three-digit number cards", "play money in $1, $10, $100 denominations"],
        },
        "time_estimates": {"first_exposure": 30, "practice_session": 20, "assessment": 20},
        "accommodations": {
            "dyslexia": "Use color-coded place-value columns (hundreds red, tens blue, ones green) and grid paper to keep digits in their columns.",
            "adhd": "Limit to 3 to 5 problems per session. Use blocks for at least half of every session so the child is moving and touching, not only writing.",
            "gifted": "Push toward four-digit problems and have the child explain why the standard algorithm works using place-value reasoning.",
            "visual_learner": "Always model with base-ten blocks alongside the written work, and use expanded-form notation as a bridge.",
            "kinesthetic_learner": "Physically trade ten ones for a tens rod on a place-value mat for every regroup.",
            "auditory_learner": "Speak each step aloud: 'seven plus five is twelve, write two and carry one ten.'",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "We extend addition and subtraction into the hundreds. The same place-value rules apply, only there are more columns. Today we add and subtract three-digit numbers, regrouping when a column overflows or falls short.",
                "gradual_release": {
                    "i_do": "Model 247 + 365 aloud, naming each step in place-value language: 'seven plus five is twelve ones, write the two and carry the ten.' Show the same work with base-ten blocks on a place-value mat so the carry is visible.",
                    "we_do": "Work three problems together, child speaking the steps while the parent writes, then swap roles. Include one with regrouping at the ones column, one at the tens, and one with no regrouping at all so the child must judge.",
                    "you_do": "Child solves five mixed problems independently, estimates first on each, then checks their answer against the estimate.",
                },
                "guided_practice": [
                    "Solve five three-digit addition problems with the parent watching and prompting on regrouping only",
                    "Solve five three-digit subtraction problems including one that requires borrowing across two columns",
                    "Estimate each answer first by rounding to the nearest hundred",
                ],
                "independent_practice": [
                    "Worksheet of ten mixed three-digit addition and subtraction problems with answers checked against estimates",
                    "Story-problem set: five short word problems involving sums and differences in the hundreds",
                ],
                "mastery_check": [
                    "Solve eight of ten three-digit problems correctly, including at least three with regrouping",
                    "Explain in place-value language what 'carrying' and 'borrowing' actually do to the number",
                    "Catch at least one unreasonable answer in a set by comparing to the estimate",
                ],
                "spiral_review": [
                    "Re-do two-digit addition and subtraction problems at the start of each session for a week to keep the algorithm sharp",
                    "Mix in place-value warm-ups: 'how many tens are in 470?' before each lesson",
                ],
            },
            "classical": {
                "narrative_introduction": "The Romans, the Greeks, and the merchants of every old town reckoned in coins and weights running into the hundreds, and they did it with the same place-value thinking we use now. To take up addition and subtraction in the hundreds is to take up a craft very old and very useful, and to do it well is to stand in a long line of careful reckoners.",
                "memory_work": {
                    "chants": [
                        "Recite the trade rule: ten ones is one ten, ten tens is one hundred",
                        "Recite the columns in order: ones, tens, hundreds, every problem worked from right to left",
                        "Recite the estimate-then-solve rule: round first, reckon second, compare third",
                    ],
                    "recitations": [
                        "A worked example said aloud in place-value language until the steps run without hesitation",
                    ],
                },
                "copywork": [
                    "Copy a small set of clean three-digit problems and their fully worked solutions into the math copybook, neat and exact, so the form of the algorithm is in the hand as well as the head",
                ],
                "recitation_routine": "Begin each lesson by reciting yesterday's worked example, then add today's. The standard form of the algorithm is reviewed cumulatively until it is automatic.",
                "history_integration": "Tell briefly of the old way of reckoning with the abacus or counting board, where a trade in the ones row really did mean moving a bead to the tens row, and the written algorithm is simply the same trade put down on paper.",
                "read_aloud_suggestions": [
                    "A short story or chapter about a shopkeeper, a treasurer, or a counter of stores, where sums in the hundreds are part of the daily work",
                    "A well-written biography passage about an early merchant or mathematician who reckoned by hand",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 18,
                "living_book_suggestions": [
                    "A real, beautifully illustrated arithmetic book that walks a child through three-digit problems using meaningful contexts, never a busy workbook",
                    "A short biography of a merchant, scribe, or treasurer in which sums and differences in the hundreds appear in real life",
                ],
                "short_lesson_flow": "Begin with a few minutes of mental warm-up: doubles and place-value questions. Lay out base-ten blocks and a place-value mat. Pose one real problem: the family's grocery total, the books in the home library, the steps taken yesterday and today. Work the problem with the blocks first, then on paper. Stop while the child is still interested.",
                "narration_prompt": "Tell me, in your own words, what you did to find the answer. Where did the regrouping happen, and why?",
                "real_world_objects": [
                    "Base-ten blocks (hundreds, tens, ones) and a place-value mat",
                    "Real coins or play money, including hundred-dollar bills",
                    "A small notebook in which real sums from the household are kept and added across a week",
                ],
                "nature_connection": "Count and record a real outdoor quantity that runs to the hundreds: pinecones gathered across several walks, steps from the house to the mailbox and back over a week, leaves collected for a nature project.",
                "habit_focus": "The habit of accuracy: work the problem once, carefully, with full attention, rather than scratching out and starting over. Estimate first, so an unreasonable answer is noticed at once.",
            },
            "montessori": {
                "prepared_materials": [
                    "Golden bead material (units, ten-bars, hundred-squares) for concrete place value",
                    "Stamp game (colored tiles standing for units, tens, hundreds) as the first level of abstraction",
                    "Small numeral cards 1 through 9000 for building and reading three-digit and four-digit numbers",
                    "Addition and subtraction strip boards held in reserve for review of basic facts",
                ],
                "presentation": {
                    "three_period_lesson": "No new naming is required; this is the application of the place-value names long since given. The presentation is the operation itself, shown silently and slowly with the materials, then named: 'this is dynamic addition, with exchange.'",
                    "steps": [
                        "Lay out the first addend in golden beads on a tray (or stamps on the board), naming each category aloud",
                        "Lay out the second addend on a second tray (or below the first on the stamp game)",
                        "Combine the units; if there are ten or more, count out ten and exchange them for one ten-bar, then place the ten-bar with the tens",
                        "Combine the tens; if there are ten or more, exchange ten ten-bars for one hundred-square",
                        "Combine the hundreds and read the total aloud",
                        "Record the operation on paper only after the material has been used several times",
                    ],
                },
                "control_of_error": "The materials are the control: ten units physically cannot remain as units once gathered, they must be exchanged for a ten-bar, so the child sees and corrects errors of regrouping without being told. The total formed by the materials and the total written on paper must agree.",
                "abstraction_pathway": "From golden beads (quantity felt in the hand) to the stamp game (color stands for category, weight is gone) to the small bead frame to the written algorithm with no material at all. The child moves to the next level only when the current one is effortless.",
                "extensions": [
                    "Carry the operation into four-digit numbers using the same materials and exchanges",
                    "Introduce static subtraction (no exchange), then dynamic subtraction (with exchange)",
                    "Build a small bank of problems the child writes for themselves and works at the shelf over several days",
                ],
                "observation_focus": "Watch whether the child reaches for the material on hard problems and works on paper on easy ones; this is the natural movement toward abstraction. Watch also for the silent exchange done correctly without prompting.",
            },
            "unschooling": {
                "invitations": [
                    "Leave a small play cash register with hundred-dollar bills and a price tag set on the shelf, alongside real items to buy and sell",
                    "Put a long paper receipt from the family shop on the kitchen table and wonder aloud whether the total really adds up",
                    "Set out a set of dice and a notebook with a casual challenge: build a number in the hundreds, add another, see how high you can go",
                ],
                "real_world_contexts": [
                    "Tallying the family grocery bill or a restaurant check",
                    "Tracking points across a long board game or video game session",
                    "Counting savings in a jar, adding each week's contribution",
                    "Calculating distance traveled across a multi-day trip from the car's odometer",
                ],
                "conversation_starters": [
                    "How much do you think all of these together cost?",
                    "I have $500 saved and the bike costs $327. Do I have enough? How much would I have left?",
                    "Want to guess our total before I add it up, and see how close you get?",
                ],
                "resource_bank": [
                    "A real cash register or shop-set with bills and coins available, not required",
                    "Open-ended board games with running scores: Monopoly, Yahtzee, Phase 10",
                    "A simple notebook for keeping the family's running scores, totals, and reckonings",
                    "Online videos that walk through real sums (with the child's permission), if and when interest arrives",
                ],
                "parent_role": "Add aloud in front of the child often. Welcome rough estimates. When a real number question comes up, work it together on paper or with mental math, not as a lesson but as a real thing being figured out. Never grade or correct mid-attempt; ask, instead, whether the answer seems about right.",
                "observation_documentation": "Note across weeks where three-digit sums and differences arose in real life, what strategies the child used (counting up, place-value reasoning, estimation), and whether they grew more comfortable comparing their answer to a quick estimate.",
            },
        },
        "connections": {
            "reading": "Reading three-digit and four-digit numerals fluently in chapter-book page numbers and real-world signage",
            "science": "Recording counts and measurements that run into the hundreds in nature observation logs",
            "history": "Reading dates in the hundreds and reasoning about how many years separate two events",
        },
    },
}
