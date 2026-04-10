"""Pre-written content for common foundational topics.

These entries provide instant day-one content without requiring
an AI call. The format matches the content engine's output structure.
"""

SEED_CONTENT = {
    "Counting to 20": {
        "enriched": True,
        "learning_objectives": [
            "Count objects to 20 with one-to-one correspondence",
            "Recognize and write numerals 0 through 20",
            "Count forward and backward from any number within 20",
            "Answer 'how many' questions after counting a set",
        ],
        "teaching_guidance": {
            "introduction": "Begin with physical objects the child can touch and move: blocks, buttons, coins, or natural objects like acorns. Counting is a physical activity before it is an abstract one. Have the child touch each object as they say the number aloud.",
            "scaffolding_sequence": [
                "Count collections of 5 objects, touching each one",
                "Count collections of 10 objects, grouping into fives",
                "Count collections of 15 objects, grouping into fives and tens",
                "Count to 20 objects, then count backward from 20",
                "Match numeral cards to collections of objects",
                "Write numerals 0-20 from memory",
            ],
            "socratic_questions": [
                "How do you know you counted every one?",
                "If I add one more, how many will there be?",
                "What number comes just before 15?",
                "Can you show me 12 with your blocks?",
            ],
            "practice_activities": [
                "Count items during a nature walk and record the total",
                "Play counting games: hide objects and count to find them all",
                "Sort a collection and count each group separately",
            ],
            "real_world_connections": [
                "Counting items at the grocery store",
                "Counting steps on a staircase",
                "Setting the table: one plate for each person",
            ],
            "common_misconceptions": [
                "Skipping objects or counting the same object twice (solved by touching each item)",
                "Confusing the last number said with a label for that object rather than the total",
                "Believing that rearranging objects changes the count",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Counts 20 objects accurately with 1:1 correspondence every time",
                "Writes numerals 0-20 without a model",
                "Counts backward from any number within 20",
            ],
            "proficiency_indicators": [
                "Counts to 20 with occasional self-correction",
                "Writes most numerals correctly",
            ],
            "developing_indicators": [
                "Counts to 10 reliably but loses track beyond 10",
                "Recognizes numerals but may not write them all",
            ],
            "assessment_methods": ["oral counting", "object counting", "numeral writing", "counting games"],
            "sample_assessment_prompts": [
                "Count these 18 buttons for me, touching each one",
                "Write the numbers from 0 to 20",
                "Start at 14 and count backward to 1",
            ],
        },
        "resource_guidance": {
            "required": ["counting objects (blocks, buttons, coins)", "numeral cards 0-20", "lined paper"],
            "recommended": ["number line to 20", "ten-frame boards", "dot cards"],
            "philosophy_specific": {
                "classical": "Chanting number sequences, memorization through repetition",
                "charlotte_mason": "Count real objects in nature: acorns, leaves, birds at the feeder",
                "montessori": "Sandpaper numerals, golden bead material, spindle boxes",
            },
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Focus on oral counting before numeral writing. Use large numerals with directional arrows.",
            "adhd": "Keep counting sessions to 5-10 minutes. Use movement: count while jumping, clapping, or walking.",
            "gifted": "Extend to counting to 100 by 1s, 2s, 5s, and 10s. Introduce skip counting patterns.",
        },
    },
    "Addition Facts to 10": {
        "enriched": True,
        "learning_objectives": [
            "Recall all addition combinations that sum to 10 or less",
            "Demonstrate addition with manipulatives",
            "Write addition number sentences",
            "Solve missing addend problems within 10",
        ],
        "teaching_guidance": {
            "introduction": "Addition means putting groups together to find how many in all. Start with physical objects: 'I have 3 blocks and you have 4 blocks. If we put them together, how many do we have?' Let the child discover the answer by counting the combined group.",
            "scaffolding_sequence": [
                "Combine two groups of objects and count the total",
                "Introduce the + and = symbols with manipulatives alongside",
                "Practice doubles facts (1+1, 2+2, 3+3, 4+4, 5+5) as anchors",
                "Practice near-doubles (3+4 is one more than 3+3)",
                "Practice make-a-ten strategy for facts near 10",
                "Build speed with fact recall through games, not timed tests",
            ],
            "socratic_questions": [
                "If you have 5 and I give you 3 more, how could you figure out the total?",
                "You know 4+4 is 8. What would 4+5 be? How do you know?",
                "Is 3+5 the same as 5+3? How could you check?",
            ],
            "practice_activities": [
                "Roll two dice and add the numbers",
                "Use a number line to hop forward for addition",
                "Play 'war' with cards: flip two, add them, highest sum wins",
            ],
            "real_world_connections": [
                "Adding coins to find how much money you have",
                "Combining groups of snacks: 4 crackers plus 3 crackers",
                "Scoring in games: you got 5 points then 4 more points",
            ],
            "common_misconceptions": [
                "Counting from 1 instead of counting on from the larger number",
                "Not understanding that addition is commutative (3+5 = 5+3)",
                "Confusing addition with counting: thinking 5+3 means start at 5 and count 5,6,7 (getting 7 instead of 8)",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Recalls any addition fact to 10 within 3 seconds",
                "Writes correct number sentences for word problems",
                "Solves missing addend problems (__ + 4 = 7)",
            ],
            "proficiency_indicators": [
                "Recalls most facts to 10, uses counting-on for harder ones",
                "Writes number sentences with support",
            ],
            "developing_indicators": [
                "Uses manipulatives to solve addition problems",
                "Knows doubles facts but struggles with others",
            ],
            "assessment_methods": ["oral fact recall", "manipulative demonstration", "written number sentences"],
            "sample_assessment_prompts": [
                "What is 6 + 3? Show me with blocks, then tell me.",
                "Write a number sentence for: Emma has 4 apples and picks 5 more.",
                "What number goes in the blank: __ + 3 = 8?",
            ],
        },
        "resource_guidance": {
            "required": ["counting manipulatives", "number line to 20", "pencil and paper"],
            "recommended": ["dice", "playing cards", "ten-frame boards", "dominos"],
            "philosophy_specific": {
                "classical": "Chanting addition facts, oral drill with immediate correction",
                "charlotte_mason": "Living math: addition discovered through real objects and real situations",
                "montessori": "Addition strip board, golden bead material for concrete understanding",
            },
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Use color-coded manipulatives. Oral fact practice before written.",
            "adhd": "Short bursts of practice (5 minutes). Use games and movement-based activities.",
            "gifted": "Extend to addition facts to 20. Introduce simple missing addend equations.",
        },
    },
    "Letter Recognition": {
        "enriched": True,
        "learning_objectives": [
            "Identify all 26 uppercase letters by name",
            "Identify all 26 lowercase letters by name",
            "Match uppercase to lowercase letters",
            "Distinguish letters from numbers and symbols",
        ],
        "teaching_guidance": {
            "introduction": "Letters are the building blocks of reading and writing. Each letter has a name, a shape (actually two shapes: uppercase and lowercase), and one or more sounds. Start with the letters in the child's name, which makes learning personal and meaningful.",
            "scaffolding_sequence": [
                "Learn the letters in the child's first name",
                "Learn uppercase letters in groups of 3-4, using multisensory methods",
                "Practice identifying learned letters in real books and environmental print",
                "Introduce lowercase letters alongside their uppercase partners",
                "Match uppercase and lowercase pairs through games and sorting",
                "Identify all 26 letters in random order, both cases",
            ],
            "socratic_questions": [
                "What letter does your name start with? Can you find it on this page?",
                "This letter looks a lot like that one. How are they different?",
                "Can you find the letter M hiding somewhere in this room?",
            ],
            "practice_activities": [
                "Letter hunt: find specific letters in books, signs, and packaging",
                "Form letters with playdough, sand, or finger paint",
                "Sort magnetic letters into uppercase and lowercase groups",
            ],
            "real_world_connections": [
                "Reading stop signs, store names, and food packaging",
                "Finding letters on a computer keyboard",
                "Identifying letters on license plates during car rides",
            ],
            "common_misconceptions": [
                "Confusing similar-looking letters: b/d, p/q, m/w (normal and developmental, not dyslexia at this age)",
                "Thinking uppercase and lowercase are different letters rather than two forms of the same letter",
                "Confusing letter names with letter sounds",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Names all 26 uppercase letters in random order",
                "Names all 26 lowercase letters in random order",
                "Matches all uppercase-lowercase pairs",
            ],
            "proficiency_indicators": [
                "Names most letters with occasional hesitation on less common ones (Q, X, Z)",
                "Matches most uppercase-lowercase pairs",
            ],
            "developing_indicators": [
                "Names 15+ letters consistently",
                "Still confuses some similar-looking letters",
            ],
            "assessment_methods": ["letter card identification", "letter sorting", "environmental print reading"],
            "sample_assessment_prompts": [
                "Show me the letter that makes the /s/ sound",
                "What letter is this? (show random letter cards)",
                "Match these uppercase letters with their lowercase partners",
            ],
        },
        "resource_guidance": {
            "required": ["alphabet cards (upper and lowercase)", "alphabet books", "writing surface"],
            "recommended": ["magnetic letters", "sandpaper letters", "alphabet puzzles", "letter stamps"],
            "philosophy_specific": {
                "classical": "Systematic letter instruction with daily review and recitation",
                "charlotte_mason": "Letters discovered in living books and the natural environment",
                "montessori": "Sandpaper letters for tactile learning, movable alphabet",
            },
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 5},
        "accommodations": {
            "dyslexia": "Multisensory approach essential: see it, say it, trace it, build it. Extra time on b/d/p/q.",
            "adhd": "Letter hunts with movement. Learn 2-3 letters per session maximum. Use games.",
            "gifted": "Move quickly to letter sounds once names are solid. Begin CVC blending early.",
        },
    },
}
