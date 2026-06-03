"""Pre-enriched content for Mathematics Foundational template nodes."""

MATH_FOUNDATIONAL_CONTENT = {
    "mf-01": {
        "enriched": True,
        "learning_objectives": [
            "Count objects to 20 with one-to-one correspondence",
            "Recognize and write numerals 0-20",
            "Count forward and backward from any number within 20",
            "Answer 'how many' questions after counting a set",
        ],
        "teaching_guidance": {
            "introduction": "Begin with physical objects the child can touch and move: blocks, buttons, coins, or natural objects like acorns. Counting is a physical activity before it is an abstract one. Have the child touch each object as they say the number aloud.",
            "scaffolding_sequence": [
                "Count collections of 5 objects, touching each one",
                "Count collections of 10, grouping into fives",
                "Count collections of 15, grouping into fives and tens",
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
                "Skipping objects or counting the same object twice",
                "Confusing the last number with a label rather than the total",
                "Believing that rearranging objects changes the count",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Counts 20 objects accurately with 1:1 correspondence every time",
                "Writes numerals 0-20 without a model",
                "Counts backward from any number within 20",
            ],
            "assessment_methods": ["oral counting", "object counting", "numeral writing"],
            "sample_assessment_prompts": [
                "Count these 18 buttons, touching each one",
                "Write the numbers from 0 to 20",
                "Start at 14 and count backward to 1",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Count the stars: \u2b50\u2b50\u2b50\u2b50\u2b50\u2b50\u2b50 How many are there?",
                "expected_type": "number",
                "correct_answer": "7",
                "hints": ["Touch each star as you count it", "Start from the left and go to the right"],
                "explanation": "There are 7 stars. Counting each one: 1, 2, 3, 4, 5, 6, 7.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What number comes after 9?",
                "expected_type": "number",
                "correct_answer": "10",
                "hints": ["Count: 7, 8, 9, ..."],
                "explanation": "After 9 comes 10.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What number comes before 6?",
                "expected_type": "number",
                "correct_answer": "5",
                "hints": ["Count backward: 8, 7, 6, ..."],
                "explanation": "Before 6 is 5.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Count backward from 12 to 7. What numbers did you say?",
                "expected_type": "text",
                "hints": ["Start at 12 and go down one at a time"],
                "explanation": "12, 11, 10, 9, 8, 7",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "I have 13 blocks. I get 1 more. How many do I have now?",
                "expected_type": "number",
                "correct_answer": "14",
                "hints": ["Start at 13 and count one more"],
                "explanation": "13 + 1 = 14. When you add one more to 13, you get 14.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What number is between 15 and 17?",
                "expected_type": "number",
                "correct_answer": "16",
                "hints": ["Count: 15, ?, 17"],
                "explanation": "16 is between 15 and 17.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Start at 4 and count to 19. How many numbers did you say?",
                "expected_type": "number",
                "correct_answer": "16",
                "hints": [
                    "Count each one: 4, 5, 6, ... all the way to 19",
                    "You can count on your fingers or use tally marks",
                ],
                "explanation": "From 4 to 19 is 16 numbers: 4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Write the even numbers from 2 to 20.",
                "expected_type": "text",
                "hints": ["Even numbers: 2, 4, 6, ..."],
                "explanation": "2, 4, 6, 8, 10, 12, 14, 16, 18, 20",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Count these objects and write the number: \U0001f535\U0001f535\U0001f535\U0001f535\U0001f535\U0001f535\U0001f535\U0001f535\U0001f535\U0001f535\U0001f535\U0001f535\U0001f535\U0001f535\U0001f535",
                "type": "number",
                "correct_answer": "15",
                "target_concept": "counting_to_20",
            },
            {
                "prompt": "Start at 20 and count backward to 10.",
                "type": "text",
                "rubric": "Mastery: counts 20,19,18...10 without errors. Proficient: one self-correction. Developing: needs help beyond 15.",
                "target_concept": "backward_counting",
            },
            {
                "prompt": "Write the numeral for 'seventeen'.",
                "type": "number",
                "correct_answer": "17",
                "target_concept": "numeral_writing",
            },
            {
                "prompt": "What is the number that is one more than 18?",
                "type": "number",
                "correct_answer": "19",
                "target_concept": "one_more",
            },
            {
                "prompt": "How do you know you counted every object without skipping any?",
                "type": "open_response",
                "rubric": "Mastery: explains touching each one and counting in order. Proficient: mentions being careful. Developing: cannot explain strategy.",
                "target_concept": "counting_strategy",
            },
        ],
        "resource_guidance": {
            "required": ["counting objects", "numeral cards 0-20"],
            "recommended": ["number line", "ten-frame boards"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Focus on oral counting before numeral writing. Use large numerals with directional arrows.",
            "adhd": "Keep sessions to 5-10 minutes. Count while jumping, clapping, or walking.",
            "gifted": "Extend to 100 by 1s, 2s, 5s, 10s. Introduce skip counting.",
            "visual_learner": "Color-coded number lines and ten-frames with bright counters.",
            "kinesthetic_learner": "Walk a floor number line. Move objects into counted piles.",
            "auditory_learner": "Chant counting sequences rhythmically. Sing counting songs.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Counting is matching one number word to one object. Today we count to twenty, read and write the numerals, and count backward.",
                "gradual_release": {
                    "i_do": "Model counting twelve counters aloud, touching each once, then say the last number, twelve, tells how many in all. Write 12.",
                    "we_do": "Count sixteen together, child touching while you say the words, then swap. Build sets to a target numeral card together.",
                    "you_do": "Child counts sets of 14, 18, 20 independently and writes the numeral for each.",
                },
                "guided_practice": [
                    "Match numeral cards 0 to 20 to the correct quantity",
                    "Fill in missing numbers on a 1 to 20 track",
                ],
                "independent_practice": [
                    "Worksheet: write numerals 0 to 20",
                    "Count and label five sets of objects",
                ],
                "mastery_check": [
                    "Count 18 objects with one-to-one correspondence",
                    "Write 0 to 20 from memory",
                    "Count backward from 14",
                ],
                "spiral_review": [
                    "Re-count within 10 to confirm retention before extending to 20",
                ],
            },
            "classical": {
                "narrative_introduction": "Numbers march in a fixed and beautiful order. Once we know the order by heart, all of arithmetic stands on it. We will learn the count to twenty so well we could say it in our sleep.",
                "memory_work": {
                    "chants": [
                        "Forward chant 1 to 20, clear and rhythmic, daily",
                        "Backward chant 20 to 1",
                        "Seed skip-counting chants: by twos and by fives to twenty",
                    ],
                    "recitations": [
                        "A short counting rhyme committed to memory, recited at the start of each math time",
                    ],
                },
                "copywork": [
                    "Copy the numerals 0 to 20 in order, neatly, building the hand-eye memory of their forms",
                ],
                "recitation_routine": "Begin each lesson by reciting yesterday's count before adding today's; the sequence is reviewed cumulatively, never assumed.",
                "history_integration": "Count along a simple timeline of the child's own life, one mark per year, tying number order to the chronological spine.",
                "read_aloud_suggestions": [
                    "A rhythmic, well-written counting book read aloud with expression",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 12,
                "living_book_suggestions": [
                    "A single beautiful counting picture book with real, lovely illustrations; never a busy workbook-style book",
                ],
                "short_lesson_flow": "Read the counting book once, attentively, then close it. Bring out a small basket of real objects (acorns, buttons, shells). Count a set together, calmly, stopping while interest is still high.",
                "narration_prompt": "Tell me about the counting we just did. What did you count, and how many were there?",
                "real_world_objects": [
                    "Acorns or leaves gathered on a walk",
                    "Place settings at the family table",
                    "Stairs counted on the way up",
                ],
                "nature_connection": "On the next nature walk, count a set of found things and add the number to the nature notebook with a small drawing.",
                "habit_focus": "The habit of attention: count carefully, once, all the way through, without rushing or losing track.",
            },
            "montessori": {
                "prepared_materials": [
                    "Number rods (length embodies quantity)",
                    "Sandpaper numerals 0 to 9 then teens",
                    "Spindle boxes (quantity, the concept of zero, one-to-one to nine)",
                    "Cards and counters (one-to-one and odd/even to ten, then teen board to twenty)",
                ],
                "presentation": {
                    "three_period_lesson": "Naming: place a numeral and its quantity, this is fourteen. Recognition: show me fourteen. Recall: what is this? Move slowly; never rush to the third period.",
                    "steps": [
                        "Trace the sandpaper numeral while saying its name",
                        "Lay out the matching quantity of counters beneath the numeral",
                        "Self-check by pairing counters; an unpaired or extra counter reveals the error",
                    ],
                },
                "control_of_error": "The counters and spindle box quantities are fixed, so a miscount leaves a leftover or a gap that the child sees and corrects without being told.",
                "abstraction_pathway": "From rods and counters (quantity felt), to sandpaper numerals (symbol), to pairing symbol with quantity, toward writing the numeral from the held idea.",
                "extensions": [
                    "Build the numbers eleven to nineteen on the teen board with bead bars",
                    "Count a long bead chain and lay numeral tickets at each landmark",
                ],
                "observation_focus": "Watch for sustained concentration and free repetition; the child returning to the work by choice is the signal of construction, not a grade.",
            },
            "unschooling": {
                "invitations": [
                    "Leave a bowl of interesting objects (smooth stones, coins, buttons) within reach",
                    "Put an abacus or a set of blocks on a low shelf and say nothing",
                    "Bake together where the recipe needs counted scoops, cups, and cookies",
                ],
                "real_world_contexts": [
                    "Sharing snacks fairly among everyone present",
                    "Counting stairs every time they are climbed",
                    "Counting and trading coins during real or pretend shopping",
                    "Tallying a collection the child already loves: dinosaurs, cars, rocks",
                ],
                "conversation_starters": [
                    "How many do you think are in here? Want to find out?",
                    "If everyone gets the same, how many does each person get?",
                    "I wonder which pile has more.",
                ],
                "resource_bank": [
                    "Counting and number picture books left available, not assigned",
                    "Board games involving counting spaces or collecting",
                    "A real or play cash register and coins",
                ],
                "parent_role": "Notice where counting already lives in the child's actual interests and join it there. Answer real questions, model counting aloud in daily life, and resist turning a moment of curiosity into a lesson.",
                "observation_documentation": "Over days, jot where counting arose naturally, how high the child counts confidently, whether they hold one-to-one correspondence, and whether they self-correct. This replaces any test.",
            },
        },
        "connections": {
            "reading": "Number words as sight words",
            "science": "Counting specimens during nature observation",
            "history": "Counting on a timeline",
        },
    },
    "mf-02": {
        "enriched": True,
        "learning_objectives": [
            "Identify and read numerals from 0 to 100",
            "Understand the difference between a number and a numeral",
            "Begin to understand place value conceptually",
        ],
        "teaching_guidance": {
            "introduction": "Numbers are ideas. Numerals are the symbols we write to represent those ideas. The numeral '5' represents the idea of five things. Now we extend from 20 all the way to 100. Use a hundred chart as a visual anchor.",
            "scaffolding_sequence": [
                "Read numerals 0-50 from a hundred chart",
                "Read numerals 51-100",
                "Point to any named numeral on the chart",
                "Write numerals to 50 from memory",
                "Identify numerals in real-world contexts (addresses, prices, page numbers)",
            ],
            "socratic_questions": [
                "What patterns do you see in the hundred chart?",
                "What changes when we go from 19 to 20?",
                "If I cover up a number, can you figure out what it is from the numbers around it?",
            ],
            "practice_activities": [
                "Hundred chart puzzles: fill in missing numbers",
                "Number scavenger hunt: find numbers in books, signs, and packages",
                "Write numbers from 1 to 50 as fast as you can",
            ],
            "real_world_connections": ["House numbers on your street", "Page numbers in a book", "Prices at a store"],
            "common_misconceptions": [
                "Reversing digits: writing 31 as 13",
                "Not understanding that 40 means 'four tens'",
                "Thinking numbers end at some point",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Reads any numeral 0-100 on sight",
                "Points to correct numeral when given orally",
                "Writes numerals to 50 from memory",
            ],
            "assessment_methods": ["numeral identification", "hundred chart activities", "numeral writing"],
            "sample_assessment_prompts": [
                "Read these numbers: 47, 82, 15, 63, 90",
                "Write the number sixty-three",
                "Point to 78 on the hundred chart",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What number is this: 25?",
                "expected_type": "text",
                "correct_answer": "twenty-five",
                "hints": ["The 2 means two tens, the 5 means five ones"],
                "explanation": "25 is read as twenty-five.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Write the numeral for 'thirty-four'.",
                "expected_type": "number",
                "correct_answer": "34",
                "hints": ["Thirty means 3 tens, four means 4 ones"],
                "explanation": "Thirty-four is written as 34.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What number comes right after 49?",
                "expected_type": "number",
                "correct_answer": "50",
                "hints": ["Count: 47, 48, 49, ..."],
                "explanation": "After 49 comes 50.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What number is 10 more than 35?",
                "expected_type": "number",
                "correct_answer": "45",
                "hints": ["On the hundred chart, go down one row"],
                "explanation": "35 + 10 = 45. Adding 10 changes the tens digit by 1.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Write all the numbers from 88 to 100.",
                "expected_type": "text",
                "hints": ["Start at 88 and keep counting"],
                "explanation": "88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Read this number: 76",
                "type": "text",
                "correct_answer": "seventy-six",
                "target_concept": "numeral_reading",
            },
            {
                "prompt": "Write the numeral for 'ninety-one'.",
                "type": "number",
                "correct_answer": "91",
                "target_concept": "numeral_writing",
            },
            {
                "prompt": "What number is between 59 and 61?",
                "type": "number",
                "correct_answer": "60",
                "target_concept": "number_sequence",
            },
        ],
        "resource_guidance": {"required": ["hundred chart", "numeral cards"], "recommended": ["number line to 100"]},
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Extra-large numerals. One decade at a time. Watch for 12/21 reversals.",
            "adhd": "Hundred chart games with movement. Number scavenger hunts.",
            "gifted": "Extend to 1000. Place value notation. Number patterns on the chart.",
            "visual_learner": "Color-coded hundred chart with decades in different colors.",
            "kinesthetic_learner": "Floor hundred chart to walk on. Magnetic number tiles.",
            "auditory_learner": "Say number names aloud while pointing. Partner quizzing.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "A numeral is the symbol we write for a number. We will read every numeral to one hundred on sight, and learn that a two-digit numeral is built from tens and ones: 63 is six tens and three ones.",
                "gradual_release": {
                    "i_do": "Read numerals across a hundred chart, pointing and naming. Build 63 with base-ten rods: six ten-rods, three unit cubes, saying six tens, three ones, sixty-three.",
                    "we_do": "Read a row of the chart together; cover a numeral and deduce it from neighbors; build two or three numbers with tens-and-ones blocks and read them aloud together.",
                    "you_do": "Child reads a mixed set (47, 82, 15, 63, 90), writes sixty-three, and shows the tens and ones in 40.",
                },
                "guided_practice": [
                    "Hundred chart fill-in puzzles",
                    "Build a given two-digit number with base-ten blocks, then read it",
                ],
                "independent_practice": [
                    "Write numerals to 50 from memory",
                    "Numeral scavenger sheet: record numbers found on signs and packages",
                ],
                "mastery_check": [
                    "Read any numeral 0 to 100 on sight",
                    "Write sixty-three correctly",
                    "State how many tens and ones are in 40",
                ],
                "spiral_review": [
                    "Re-read numerals 0 to 20 to confirm retention before extending",
                ],
            },
            "classical": {
                "narrative_introduction": "The numerals are an alphabet for quantity. There are only ten symbols, yet with place they name every number to a hundred and beyond. We learn to read them all, and the secret of place: where a digit sits tells how much it is worth.",
                "memory_work": {
                    "chants": [
                        "Count by tens to one hundred as a rhythmic chant",
                        "Recite the decade names: twenty, thirty, forty, fifty",
                        "Read the hundred chart aloud, one row a day, then cumulatively",
                    ],
                    "recitations": [
                        "A short place-value verse memorized: two tens and three, that's twenty-three",
                    ],
                },
                "copywork": [
                    "Copy the numerals in rows of ten (0 to 9, 10 to 19, and so on), the neat columns revealing the repeating pattern of the ones place",
                ],
                "recitation_routine": "Open each lesson by reciting the count-by-tens and the prior decades before adding today's, so the sequence is always cumulative.",
                "history_integration": "Number a simple century timeline and read the years aloud in order, binding numeral reading to the chronological spine.",
                "read_aloud_suggestions": [
                    "A well-written read-aloud that plays with hundreds and large numbers, chosen for rich language",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A single beautifully illustrated picture book that explores numbers toward one hundred; real artwork, never a workbook in disguise",
                ],
                "short_lesson_flow": "Read the chosen book once, attentively, then close it. Bring out a jar of one hundred real things (beans, buttons) or a real hundred chart. Read a handful of numerals together, and group a small pile into tens and ones. Stop while interest is still high.",
                "narration_prompt": "Tell me what you noticed about the numbers as they grew. What happened each time we reached a new ten?",
                "real_world_objects": [
                    "House numbers noticed on a walk",
                    "Page numbers in the current family read-aloud",
                    "Prices at the market",
                ],
                "nature_connection": "Gather a nature collection, group it into tens and ones, and record the two-digit total with a small drawing in the nature notebook.",
                "habit_focus": "Accuracy and attention: read each numeral carefully and fully, rather than guessing from the first digit.",
            },
            "montessori": {
                "prepared_materials": [
                    "Golden bead material: unit beads, ten-bars, hundred-square, for felt place value",
                    "The hundred board with its control chart",
                    "Large place-value number cards that overlay to show tens and ones",
                ],
                "presentation": {
                    "three_period_lesson": "With the ten cards and bead quantities: this is forty, four tens; show me sixty; what is this? Always pair the written symbol with the bead quantity.",
                    "steps": [
                        "Build a quantity with ten-bars and unit beads",
                        "Lay the matching large numeral cards beside it",
                        "Compose a two-digit number by sliding the units card over the zero of the tens card, so 60 with 3 overlaid becomes 63, showing place value physically",
                    ],
                },
                "control_of_error": "The hundred board control chart and the fixed bead quantities make a misplacement visible as a gap or mismatch, which the child corrects without an adult verdict.",
                "abstraction_pathway": "From golden beads (quantity felt), to the overlaid place-value cards (structure of tens and ones made visible), toward reading and writing any numeral from the held idea with no chart needed.",
                "extensions": [
                    "Build the hundred board independently against its control",
                    "Skip-count the bead chains and lay numeral tickets at the landmarks",
                    "Choose a two-digit number, build it in beads, and label it",
                ],
                "observation_focus": "Watch for the child grasping that a digit's position carries its value, and for free, repeated work with the hundred board by choice.",
            },
            "unschooling": {
                "invitations": [
                    "Leave a real hundred chart or a jar of one hundred interesting objects within reach",
                    "Set out a calendar at child height, a tape measure, a ruler, and real coins",
                    "Keep a deck of cards and a couple of two-digit-scoring games accessible",
                ],
                "real_world_contexts": [
                    "Reading house numbers and bus numbers",
                    "Finding the page they are on in a loved book",
                    "Reading prices and totals while shopping",
                    "Keeping score in a game",
                    "Reading ages, the calendar, channel and jersey numbers",
                ],
                "conversation_starters": [
                    "What number is our house? What about next door?",
                    "How many pages does this book have, and what page are we on?",
                    "I wonder how they write the prices here.",
                ],
                "resource_bank": [
                    "Number and big-number picture books, available not assigned",
                    "Board games with two-digit scoring",
                    "Real money and a calculator left accessible",
                    "A wall calendar the child can reach",
                ],
                "parent_role": "Read numerals aloud naturally through the day (prices, addresses, page numbers), answer what number is that without turning it into a drill, and follow the child's own number interests.",
                "observation_documentation": "Over time, note which numerals the child reads confidently, whether they read the tens correctly (sixty-three, not six-three), and whether place-value language is emerging. No test; mastery inferred from real reading.",
            },
        },
        "connections": {
            "reading": "Reading number words and matching to numerals",
            "science": "Recording two-digit measurement data",
            "history": "Years and dates on timelines",
        },
    },
    "mf-03": {
        "enriched": True,
        "learning_objectives": [
            "Demonstrate one-to-one correspondence when counting",
            "Understand that each object gets exactly one count",
            "Recognize that the last number said represents the total",
            "Understand that counting order does not change the total",
        ],
        "teaching_guidance": {
            "introduction": "One-to-one correspondence means each object gets exactly one number. The child touches, moves, or points to each object as they say one number. This is the bridge between reciting numbers and actually counting.",
            "scaffolding_sequence": [
                "Line up 5 objects and touch each while counting",
                "Count scattered objects by moving each to a counted pile",
                "Count objects in a circle without losing track",
                "Count the same group arranged differently to prove the total stays the same",
            ],
            "socratic_questions": [
                "How can you make sure you don't count any twice?",
                "What if we move these blocks around, will the number change?",
                "Why did you touch each one as you counted?",
            ],
            "practice_activities": [
                "Count a jar of buttons by moving each to a new pile",
                "Count steps as you walk across the room",
            ],
            "real_world_connections": ["Passing out one napkin per person at dinner", "Giving one treat to each pet"],
            "common_misconceptions": [
                "Saying numbers faster than pointing",
                "Counting an object twice because it wasn't moved aside",
                "Thinking a spread-out group has more than a bunched-up group",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Counts 15 scattered objects without double-counting or skipping",
                "Explains that rearranging objects doesn't change the count",
            ],
            "assessment_methods": ["object counting", "observation", "oral explanation"],
            "sample_assessment_prompts": [
                "Count these 12 scattered buttons",
                "If I spread these out more, will there be more?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Count the dots: * * * * * How many?",
                "expected_type": "number",
                "correct_answer": "5",
                "hints": ["Point to each dot as you count"],
                "explanation": "There are 5 dots.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "You have 8 blocks in a line. You push them into a pile. How many blocks are in the pile?",
                "expected_type": "number",
                "correct_answer": "8",
                "hints": ["Did you add or remove any blocks?"],
                "explanation": "Still 8. Moving objects doesn't change the count.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Sam counted 10 apples. Someone moved them closer together. Sam counted again and got 8. What went wrong?",
                "expected_type": "text",
                "hints": ["Did the number of apples change?"],
                "explanation": "Sam probably skipped some. Moving objects doesn't change the count. Sam should touch each apple.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "You have 14 objects in a circle. How would you count them without counting any twice?",
                "expected_type": "text",
                "hints": ["Think about marking your starting point"],
                "explanation": "Start at one object and mark it. Count around until you get back to the marked one.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Count these 11 scattered objects.",
                "type": "number",
                "correct_answer": "11",
                "target_concept": "one_to_one",
            },
            {
                "prompt": "If I spread 7 blocks far apart, how many are there?",
                "type": "number",
                "correct_answer": "7",
                "target_concept": "conservation",
            },
            {
                "prompt": "Show me your strategy for counting without missing any.",
                "type": "open_response",
                "rubric": "Mastery: describes moving or marking objects. Proficient: demonstrates a strategy. Developing: no clear strategy.",
                "target_concept": "counting_strategy",
            },
        ],
        "resource_guidance": {"required": ["small counting objects"], "recommended": ["sorting trays"]},
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 10},
        "accommodations": {
            "dyslexia": "No reading required. Purely manipulative-based counting.",
            "adhd": "Large satisfying objects. Sets under 15. Frequent switching.",
            "gifted": "Larger sets (30+). Estimation before counting.",
            "visual_learner": "Brightly colored objects. Mark counted items with stickers.",
            "kinesthetic_learner": "Move every object. Sort into containers as counted.",
            "auditory_learner": "Say each number aloud with emphasis. Tap table with each count.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Counting means giving each object exactly one number word. We touch or move each object as we say its number, and the last number we say tells how many there are in all. Today we also see that moving the objects around never changes how many there are.",
                "gradual_release": {
                    "i_do": "Model counting nine counters in a line: touch each one once, saying one number per touch, then say nine, that is how many in all. Slide the nine into a pile and count again to show it is still nine.",
                    "we_do": "Count a scattered set of twelve together: the child slides each object into a counted pile while you both say the numbers, then swap roles. Rearrange the set and count again together to confirm the total holds.",
                    "you_do": "Child counts sets of 8, 13, and 15 independently, moving each object aside as it is counted, and states the total for each.",
                },
                "guided_practice": [
                    "Count a line of objects, touching each exactly once",
                    "Count a scattered set by sliding each object into a counted pile",
                    "Count one set, rearrange it, and count again to check the total stays the same",
                ],
                "independent_practice": [
                    "Counting mat: cross off each printed object as it is counted",
                    "Count five small sets of objects and write the total for each",
                ],
                "mastery_check": [
                    "Count 15 scattered objects with no double-count and no skip",
                    "Explain why moving the objects does not change the count",
                    "State the total without recounting after the last object",
                ],
                "spiral_review": [
                    "Briefly re-count sets within 10 to confirm the careful touch-count habit before working with larger sets",
                ],
            },
            "classical": {
                "narrative_introduction": "Counting has a law: every thing gets one number, and no thing gets two. When each has been given its one number, the last number said is the answer; it tells how many. Learn the law, and the careful habit of it, and counting becomes sure.",
                "memory_work": {
                    "chants": [
                        "Chant the touch-and-count rhythm, one number for each touch, never letting the voice race ahead of the hand",
                        "A short rule chanted daily: one thing, one number; the last number tells how many",
                    ],
                    "recitations": [
                        "Recite the rule of counting from memory before each counting task: each object gets exactly one number, and moving the objects never changes how many there are",
                    ],
                },
                "copywork": [
                    "Copy the numerals 1 to 15 in order, neatly, so the symbol for each count is sure and ready to the hand",
                ],
                "recitation_routine": "Begin each lesson by reciting the rule of counting and counting one familiar set aloud, slowly and exactly, before any new work; the careful habit is rehearsed cumulatively, never assumed.",
                "history_integration": "Count the years along a simple timeline, one careful touch per year mark, so the discipline of one number per thing is practiced on the chronological spine.",
                "read_aloud_suggestions": [
                    "A rhythmic, well-made counting book, read aloud with a finger touching each pictured thing as its number is said",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 12,
                "living_book_suggestions": [
                    "A single beautiful counting picture book with real, lovely illustrations and one clear set of things to a page; never a busy or cartoonish workbook-style book",
                ],
                "short_lesson_flow": "Look together at one or two pages of the counting book, touching each pictured thing as its number is said. Then set the book aside and bring out a small basket of real objects gathered earlier. Count a set together, slowly, the child touching each object once and sliding it aside. Stop while the child is still attentive and content.",
                "narration_prompt": "Tell me how you counted. How did you make sure each thing got one number, and that none was counted twice or missed?",
                "real_world_objects": [
                    "Acorns, shells, or smooth stones gathered on a walk",
                    "One napkin set at each place at the family table",
                    "Eggs settled one to each cup of a carton",
                ],
                "nature_connection": "On the next nature walk, the child counts a small set of found things, touching each one, and records the number with a little drawing in the nature notebook.",
                "habit_focus": "The habit of attention: count once, slowly, touching each thing as its number is said, never letting the voice race ahead of the hand.",
            },
            "montessori": {
                "prepared_materials": [
                    "Cards and counters: numeral cards 1 to 10 with loose counters laid one by one beneath each",
                    "Spindle boxes, where a fixed number of spindles is gathered into each numbered compartment so the hand feels the quantity",
                    "Number rods, where each rod's length embodies its count",
                    "A counting tray with a set of identical objects for free counting work",
                ],
                "presentation": {
                    "three_period_lesson": "With a counted set: this is how many, nine; show me when you have given each one its own number; what is this, how many in all? Move slowly, and let the child do the touching.",
                    "steps": [
                        "Lay the counters beneath a numeral one at a time, one counter to one place, saying one number for each counter",
                        "Place the counters in pairs so the layout itself shows when a set is even or odd, and so a missing or extra counter is plain to see",
                        "Slide a counted set into a new arrangement and count again, letting the child discover for themselves that the total is unchanged",
                    ],
                },
                "control_of_error": "The counters are a fixed set and each has its place, so a counter left over or a space left empty shows the child directly that a number was skipped or doubled. The material corrects, not the adult.",
                "abstraction_pathway": "From the spindles and counters held in the hand (the quantity felt and the one-to-one match made physical), to laying counters beneath the written numeral (quantity joined to symbol), toward counting any set with the eyes and a light touch alone.",
                "extensions": [
                    "Count a longer bead chain, touching each bead, and lay a numeral ticket at its end",
                    "Bring a set of objects from the room, count it freely on the counting tray, then rearrange it and confirm the total",
                ],
                "observation_focus": "Watch whether the hand and the voice move together, one number to one object, and whether the child returns to the cards and counters by choice; the unforced repetition is the sign the idea is being built.",
            },
            "unschooling": {
                "invitations": [
                    "Leave a basket of interesting objects beside a muffin tin or egg carton, so a child can drop one thing into each cup",
                    "Set out a small pitcher and several cups for free pouring and table-setting play",
                    "Keep dot dominoes, dice, and a deck of cards on a low shelf and say nothing",
                ],
                "real_world_contexts": [
                    "Setting the table, one plate, one fork, and one cup to each seat",
                    "Feeding the pets, one scoop into each bowl",
                    "Handing out one snack, sticker, or crayon to each person present",
                    "Loading an egg carton, one egg to each cup",
                    "Watching the elevator buttons light one at a time, one for each floor",
                ],
                "conversation_starters": [
                    "Everyone needs one fork. How will you know you have given each person theirs?",
                    "Did the number of cookies change when we moved them onto the plate?",
                    "How do you keep from counting the same one twice?",
                ],
                "resource_bank": [
                    "Counting picture books left available, not assigned",
                    "Muffin tins, ice cube trays, and egg cartons for matching one thing to one space",
                    "Dominoes, dice, and board games that move one space per count",
                    "A real or play set of dishes for table-setting",
                ],
                "parent_role": "Notice the many daily moments when a child is already matching one thing to one place, setting a table, sharing treats, loading a carton, and simply count aloud alongside them. Answer real questions, model touching each thing as you count, and let an occasional miscount stand as something the child can notice, rather than correcting it into a lesson.",
                "observation_documentation": "Over days, jot where one-to-one counting arose on its own, whether the child's touch keeps pace with the words, whether they can say the total without recounting, and whether they trust that a rearranged set holds its number. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Tracking words while reading one at a time",
            "science": "Counting specimens in a collection",
            "history": "Counting items in historical illustrations",
        },
    },
    "mf-04": {
        "enriched": True,
        "learning_objectives": [
            "Count to 100 by ones fluently",
            "Count by tens to 100",
            "Count forward from any given number within 100",
            "Understand the repeating pattern of tens",
        ],
        "teaching_guidance": {
            "introduction": "Counting to 100 is the child's first encounter with the structure of our base-ten system. The pattern repeats every ten: 21,22,23...29,30. Use a hundred chart so the child can SEE the pattern.",
            "scaffolding_sequence": [
                "Count from 1 to 30, then 1 to 50, building up",
                "Use a hundred chart and point to each number",
                "Practice hard transitions: 29-30, 39-40, 49-50",
                "Count by 10s: 10, 20, 30...100",
                "Count forward from a random starting point",
            ],
            "socratic_questions": [
                "What pattern do you notice after every 9?",
                "If you're at 57, what comes next?",
                "What's the same about 23, 33, 43, 53?",
            ],
            "practice_activities": [
                "Hundred chart coloring: color every 5th number",
                "Count to 100 while doing jumping jacks",
                "Hundred chart puzzles: cut apart and reassemble",
            ],
            "real_world_connections": ["Counting pennies to make a dollar", "Days of school on a hundred chart"],
            "common_misconceptions": [
                "Stalling at decade transitions",
                "Confusing teens and tens (13 vs 30)",
                "Thinking you must start at 1",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Counts to 100 without hesitation at transitions",
                "Counts by tens to 100 fluently",
                "Counts forward from any number to 100",
            ],
            "assessment_methods": ["oral counting", "hundred chart completion"],
            "sample_assessment_prompts": ["Count from 1 to 100", "Count by tens", "Start at 46 and count to 70"],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Count by tens: 10, 20, 30, __, __, __",
                "expected_type": "text",
                "correct_answer": "40, 50, 60",
                "hints": ["Add 10 each time"],
                "explanation": "40, 50, 60.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What number comes after 29?",
                "expected_type": "number",
                "correct_answer": "30",
                "hints": ["After 29, a new group of ten starts"],
                "explanation": "After 29 comes 30.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Start at 55 and count to 65.",
                "expected_type": "text",
                "correct_answer": "55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65",
                "hints": ["Watch the transition from 59 to 60"],
                "explanation": "55 through 65, including the 59-60 transition.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Start at 87 and count to 100. How many numbers did you say?",
                "expected_type": "number",
                "correct_answer": "14",
                "hints": ["Count from 87 through 100 on your fingers"],
                "explanation": "87 through 100 is 14 numbers.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Count from 38 to 52.",
                "type": "text",
                "rubric": "Mastery: fluent. Proficient: one pause. Developing: stumbles at transitions.",
                "target_concept": "counting_to_100",
            },
            {
                "prompt": "What number comes after 99?",
                "type": "number",
                "correct_answer": "100",
                "target_concept": "counting_to_100",
            },
            {
                "prompt": "Count by tens from 10 to 100.",
                "type": "text",
                "correct_answer": "10, 20, 30, 40, 50, 60, 70, 80, 90, 100",
                "target_concept": "skip_counting_tens",
            },
        ],
        "resource_guidance": {"required": ["hundred chart"], "recommended": ["number line to 100"]},
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Oral counting primary. Written sequences as reinforcement.",
            "adhd": "Full-body counting: jump, step, clap. Decade movement breaks.",
            "gifted": "Count to 1000. By 3s, 4s, 6s. Multiple skip-count overlap.",
            "visual_learner": "Hundred chart with color patterns. Wall number line.",
            "kinesthetic_learner": "Walk a giant floor hundred chart. Snap cubes into tens.",
            "auditory_learner": "Counting songs. Rhythmic chanting at decade transitions.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Counting to one hundred follows a pattern that repeats every ten: after 29 comes 30, after 39 comes 40. Today we count to one hundred by ones and by tens, and we learn to start counting from any number, not only from one.",
                "gradual_release": {
                    "i_do": "Model counting on the hundred chart, pointing to each number, and name the pattern aloud at each decade: twenty-eight, twenty-nine, and a new ten begins, thirty. Then model counting by tens down the final column.",
                    "we_do": "Count the chart together, the child pointing while you both say the numbers, rehearsing the hard transitions 29 to 30 and 39 to 40. Count by tens together, then start from a number you name and count on.",
                    "you_do": "Child counts 1 to 100 independently, counts by tens from 10 to 100, and counts forward from a given starting number to a given end.",
                },
                "guided_practice": [
                    "Hundred chart fill-in puzzles with missing numbers",
                    "Rehearse the decade transitions 29 to 30, 39 to 40, 49 to 50",
                    "Count by tens down a column of the hundred chart",
                ],
                "independent_practice": [
                    "Complete a blank hundred chart from memory",
                    "Write the missing numbers along a counting strip",
                ],
                "mastery_check": [
                    "Count 1 to 100 aloud with no stall at the decade transitions",
                    "Count by tens from 10 to 100 fluently",
                    "Count forward from any given number to 100",
                ],
                "spiral_review": [
                    "Re-count within 30 and rehearse the decade transitions before extending the count again",
                ],
            },
            "classical": {
                "narrative_introduction": "The count to one hundred has a hidden order: it is ten tens, and each ten repeats the same pattern of ones. Learn the whole count by heart, and the structure of number stands ready for everything that follows.",
                "memory_work": {
                    "chants": [
                        "Forward chant 1 to 100 daily, clear and rhythmic",
                        "A count-by-tens chant: ten, twenty, thirty, all the way to one hundred",
                        "Chant the decade transitions with a lift of the voice: twenty-eight, twenty-nine, THIRTY",
                    ],
                    "recitations": [
                        "A counting verse or rhyme that carries the count toward one hundred, recited at the start of math time",
                    ],
                },
                "copywork": [
                    "Copy the hundred chart numerals in rows of ten, the neat columns making the repeating pattern of the ones place visible to the eye and the hand",
                ],
                "recitation_routine": "Begin each lesson by reciting the count reached so far, cumulatively, before extending it; the sequence is rehearsed in full, never assumed.",
                "history_integration": "Count the years along a century timeline and read that one hundred years is a century, binding the count to one hundred to the chronological spine.",
                "read_aloud_suggestions": [
                    "A well-made read-aloud that plays with hundreds and large numbers, chosen for rich and rhythmic language",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A single beautifully illustrated picture book that journeys toward one hundred, with real artwork and never a workbook in disguise",
                ],
                "short_lesson_flow": "Read a few pages of the chosen book attentively, then close it. Bring out one hundred real things, pennies or beans or buttons, or a real hundred chart. Count a stretch of them together, calmly, grouping by tens, and pausing at the decade transitions. Stop while the child is still attentive.",
                "narration_prompt": "Tell me what you noticed about the numbers as they climbed toward one hundred. What happened each time you reached a new ten?",
                "real_world_objects": [
                    "One hundred pennies counted into stacks of ten",
                    "The days of school marked one by one toward a hundredth day",
                    "Steps counted on a long walk",
                ],
                "nature_connection": "Gather a large nature collection, count it toward one hundred in groups of ten, and record the total with a small drawing in the nature notebook.",
                "habit_focus": "The habit of steady, accurate attention: holding the count carefully through its whole length, especially at the decade transitions where it is easy to slip.",
            },
            "montessori": {
                "prepared_materials": [
                    "The hundred board with its loose numeral tiles and its control chart",
                    "The hundred chain, ten ten-bars joined, and the shorter bead chains for skip counting",
                    "Large numeral cards for the tens landmarks",
                ],
                "presentation": {
                    "three_period_lesson": "With the tens landmarks on the hundred board: this is forty; show me sixty; what is this? Then let the child build and count freely.",
                    "steps": [
                        "Lay the hundred board tiles in order against the frame, one to one hundred",
                        "Count the hundred chain bead by bead, laying a numeral ticket at each ten so the pattern of tens is seen",
                        "Choose any tile and count on from it, so counting is freed from always starting at one",
                    ],
                },
                "control_of_error": "The hundred board control chart and the fixed length of the bead chain make a misplaced tile or a miscount show as a gap or a mismatch, which the child sees and corrects without an adult's word.",
                "abstraction_pathway": "From the hundred chain held and counted bead by bead (the count felt in its full length), to the hundred board (the pattern of ten tens seen at once), toward counting to one hundred from any starting point with no chart at all.",
                "extensions": [
                    "Skip-count the longer bead chains and lay numeral tickets at the landmarks",
                    "Build the whole hundred board independently and check it against its control chart",
                ],
                "observation_focus": "Watch for the child grasping that each new ten repeats the same run of ones, and for free, repeated work with the hundred board and chains by choice.",
            },
            "unschooling": {
                "invitations": [
                    "Leave a real hundred chart or a jar of one hundred interesting objects within reach",
                    "Keep a coin jar going and count it together when it is full",
                    "Set out board games whose paths run toward one hundred spaces",
                ],
                "real_world_contexts": [
                    "Counting pennies into stacks of ten to make a dollar",
                    "Marking the days of school toward the hundredth day",
                    "Counting steps, stairs, or laps",
                    "Reading the calendar and counting down to an awaited day",
                    "Counting spaces around a long board game",
                ],
                "conversation_starters": [
                    "How high do you think you can count today? Want to find out together?",
                    "We are at thirty-nine. I wonder what comes next.",
                    "Why do you think a new ten always starts right after a nine?",
                ],
                "resource_bank": [
                    "A hundred chart kept available, not assigned",
                    "A coin jar and real money",
                    "A wall calendar the child can reach",
                    "Counting and big-number picture books, and board games with long counted paths",
                ],
                "parent_role": "Count aloud through the day wherever counting naturally reaches toward one hundred, pennies, days, steps, and follow the child's own interest in how high they can go. Answer real questions about the pattern of the tens, and let collections and countdowns do the teaching rather than a drill.",
                "observation_documentation": "Over time, note how high the child counts confidently, whether the decade transitions trip them, whether they can count on from a number rather than only from one, and whether they have noticed the repeating pattern of tens. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Counting syllables in longer words",
            "science": "Counting to 100 for measurement",
            "history": "100 years is a century on the timeline",
        },
    },
    "mf-05": {
        "enriched": True,
        "learning_objectives": [
            "Recall all addition combinations within 10",
            "Demonstrate addition with manipulatives",
            "Write addition number sentences",
            "Solve missing addend problems within 10",
        ],
        "teaching_guidance": {
            "introduction": "Addition means putting groups together. Start with objects: 'I have 3 blocks and you have 4. Put them together, how many?' Let the child discover by counting the combined group.",
            "scaffolding_sequence": [
                "Combine two groups and count the total",
                "Introduce + and = symbols alongside manipulatives",
                "Practice doubles: 1+1, 2+2, 3+3, 4+4, 5+5",
                "Practice near-doubles: 3+4 is one more than 3+3",
                "Practice make-ten for facts near 10",
                "Build recall through games, not timed tests",
            ],
            "socratic_questions": [
                "If you have 5 and get 3 more, how could you find the total?",
                "You know 4+4=8. What would 4+5 be?",
                "Is 3+5 the same as 5+3? How could you check?",
            ],
            "practice_activities": [
                "Roll two dice and add",
                "Number line hopping forward",
                "Card game war: flip two, add, highest sum wins",
            ],
            "real_world_connections": ["Adding coins", "Combining groups of snacks", "Scoring in games"],
            "common_misconceptions": [
                "Counting from 1 instead of counting on",
                "Not understanding commutativity",
                "Counting the starting number in count-on",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Recalls any fact to 10 within 3 seconds",
                "Writes correct number sentences",
                "Solves missing addend: __ + 4 = 7",
            ],
            "assessment_methods": ["oral recall", "manipulative demo", "written sentences"],
            "sample_assessment_prompts": [
                "What is 6+3?",
                "Show 4+5 with blocks",
                "What goes in the blank: __ + 3 = 8?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is 3 + 2?",
                "expected_type": "number",
                "correct_answer": "5",
                "hints": ["Start with 3, count up 2"],
                "explanation": "3 + 2 = 5.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is 5 + 5?",
                "expected_type": "number",
                "correct_answer": "10",
                "hints": ["Doubles fact"],
                "explanation": "5 + 5 = 10.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is 4 + 5?",
                "expected_type": "number",
                "correct_answer": "9",
                "hints": ["4+4=8, so 4+5 is one more"],
                "explanation": "4 + 5 = 9.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Fill in: __ + 4 = 9",
                "expected_type": "number",
                "correct_answer": "5",
                "hints": ["What plus 4 equals 9?"],
                "explanation": "5 + 4 = 9.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "How many ways can you make 8 with two numbers?",
                "expected_type": "text",
                "hints": ["Start with 0+8, then 1+7..."],
                "explanation": "0+8, 1+7, 2+6, 3+5, 4+4, 5+3, 6+2, 7+1, 8+0.",
            },
        ],
        "assessment_items": [
            {"prompt": "What is 7 + 2?", "type": "number", "correct_answer": "9", "target_concept": "addition_facts"},
            {
                "prompt": "Fill in: __ + 6 = 10",
                "type": "number",
                "correct_answer": "4",
                "target_concept": "missing_addend",
            },
            {
                "prompt": "What is 5 + 4? Explain your strategy.",
                "type": "open_response",
                "rubric": "Mastery: correct (9) with strategy. Proficient: correct, vague strategy. Developing: incorrect.",
                "target_concept": "addition_strategy",
            },
        ],
        "resource_guidance": {
            "required": ["counting manipulatives", "number line"],
            "recommended": ["dice", "playing cards", "ten-frames"],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Oral practice before written. Manipulatives longer than typical. No timed tests.",
            "adhd": "Games: dice, cards, dominoes. Never worksheets for drill. 5-minute max.",
            "gifted": "Addition within 20. Missing addend. Commutativity as concept.",
            "visual_learner": "Ten-frames with two-color counters. Number bond diagrams.",
            "kinesthetic_learner": "Snap cubes in different colors, snap together, count.",
            "auditory_learner": "Chant fact families. Partner quizzing. Doubles songs.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Addition is putting groups together; the total tells how many there are in all. Today we combine groups, write the number sentence that records it, find a missing part, and build quick, sure recall of the sums within ten.",
                "gradual_release": {
                    "i_do": "Model with counters: take a group of three and a group of four, slide them together, count the whole, seven. Write the number sentence, 3 + 4 = 7. Model counting on from the larger group rather than counting all.",
                    "we_do": "Combine groups together and write the number sentence together. Practice the doubles and the near-doubles, and find a missing addend by hiding part of a known whole.",
                    "you_do": "Child solves the sums within ten, first with counters and then without, writes the matching number sentences, and solves missing-addend problems such as blank plus 4 equals 9.",
                },
                "guided_practice": [
                    "Combine two groups of counters and count the total, then write the number sentence",
                    "Build the doubles with two-color counters: 3 and 3, 4 and 4",
                    "Find the missing addend when part of a known whole is hidden",
                ],
                "independent_practice": [
                    "Fact practice through dice, dominoes, and card games rather than timed drill",
                    "Write the number sentence for each combined group",
                ],
                "mastery_check": [
                    "Recall any sum within ten quickly and correctly",
                    "Write a correct addition number sentence",
                    "Solve a missing-addend problem within ten",
                ],
                "spiral_review": [
                    "Revisit the doubles and the combinations within five before extending recall toward ten",
                ],
            },
            "classical": {
                "narrative_introduction": "Addition is the joining of numbers, and the small sums within ten are the bricks of all arithmetic. Learned by heart, so they answer at once, every later calculation rests upon them.",
                "memory_work": {
                    "chants": [
                        "Chant the doubles in rhythm: one and one are two, two and two are four, on to five and five",
                        "Chant the pairs that make ten: nine and one, eight and two, seven and three",
                        "Chant a fact family together: three, four, seven; seven, four, three",
                    ],
                    "recitations": [
                        "Recite the addition combinations within ten in order, a few each day, until the whole set is held in memory",
                    ],
                },
                "copywork": [
                    "Copy addition number sentences neatly, such as 3 + 4 = 7, so the written form of each fact is sure and familiar to the hand",
                ],
                "recitation_routine": "Begin each lesson by reciting the sums learned so far before adding new ones; the facts are reviewed cumulatively, never assumed.",
                "history_integration": "Add the years between two dates on a simple timeline to find the span between them, applying the joining of numbers to the chronological spine.",
                "read_aloud_suggestions": [
                    "A well-told story in which groups of things are gathered and combined, read aloud for its language and its quiet arithmetic",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 12,
                "living_book_suggestions": [
                    "A beautifully illustrated picture book in which real things are gathered and combined, chosen for lovely artwork and never a busy workbook",
                ],
                "short_lesson_flow": "Set out two small groups of real objects. Ask the child to put the groups together and find how many there are now, letting them discover the total by counting the combined group. Do two or three such combinings, calmly, and stop while the child is still interested.",
                "narration_prompt": "Tell me how you found the total. What did you do with the two groups, and how did you know how many there were in all?",
                "real_world_objects": [
                    "Acorns or shells brought from two pockets and combined",
                    "Coins from two small piles counted together",
                    "Pieces of fruit or crackers shared into one group at the table",
                ],
                "nature_connection": "On a walk, gather two small handfuls of found things, combine them, and tell the total; record the little sum with a drawing in the nature notebook.",
                "habit_focus": "The habit of careful and honest work: counting the combined group exactly, and trusting a sum only when it has truly been found.",
            },
            "montessori": {
                "prepared_materials": [
                    "The addition strip board with its numbered strips",
                    "Golden bead bars for combining quantities and counting the whole",
                    "The addition charts for the later memorization stage",
                ],
                "presentation": {
                    "three_period_lesson": "With a known sum: this is seven, three and four make seven; show me another way to make seven; what do three and four make? Spoken with the materials in hand.",
                    "steps": [
                        "Combine two golden bead bars and count the whole quantity they make",
                        "Lay two strips on the addition strip board to build a sum and read the total",
                        "Record the number sentence, then check the sum against the addition control chart",
                    ],
                },
                "control_of_error": "The fixed length of the strips on the addition strip board, and the addition control chart, let a wrong sum show itself as a mismatch the child sees and corrects without an adult's verdict.",
                "abstraction_pathway": "From combining golden beads (the sum felt in the hand), to the strip board (the sum built and seen), to the addition charts (the sum committed to memory), toward writing and recalling the fact with no material at all.",
                "extensions": [
                    "Find every way to make a chosen number and lay them out together",
                    "Work the addition snake game, exchanging colored bead bars for golden tens",
                ],
                "observation_focus": "Watch for the child moving from counting all, to counting on, to simply knowing the sum, and for free, repeated return to the addition work by choice.",
            },
            "unschooling": {
                "invitations": [
                    "Leave dice, dominoes, and a deck of cards on a low shelf and say nothing",
                    "Bake or cook together where scoops, cups, and pieces are combined and counted",
                    "Keep a coin jar and a set of board games with scoring within reach",
                ],
                "real_world_contexts": [
                    "Combining snacks or treats and finding how many there are altogether",
                    "Keeping a running score in a game",
                    "Adding coins while saving or shopping",
                    "Putting two groups of toys together and asking how many now",
                    "Setting the table and adding the places for guests",
                ],
                "conversation_starters": [
                    "You have four and I have three. How many do we have if we put them together?",
                    "Is there a way to find the total without counting them all over again?",
                    "We made eight last time with three and five. What other two numbers make eight?",
                ],
                "resource_bank": [
                    "Dice, dominoes, and playing cards kept available, not assigned",
                    "Board games that involve scoring and combining",
                    "A coin jar and real money",
                    "Math picture books left on a low shelf",
                ],
                "parent_role": "Notice the many daily moments of combining, snacks, coins, scores, toys, and count the totals aloud alongside the child. Ask genuine how-many-altogether questions, model counting on from the larger group, and let games and real combining build the facts rather than a drill.",
                "observation_documentation": "Over time, note whether the child counts all or counts on, which sums they simply know, whether they write or say number sentences in play, and whether they see that the order of two groups does not change the total. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Addition word problems need reading comprehension",
            "science": "Adding measurements in experiments",
            "history": "Adding dates to find time spans",
        },
    },
    "mf-06": {
        "enriched": True,
        "learning_objectives": [
            "Recall all subtraction facts within 10",
            "Understand subtraction as taking away or finding difference",
            "Connect subtraction to addition as inverse operations",
            "Write subtraction number sentences",
        ],
        "teaching_guidance": {
            "introduction": "Subtraction means taking some away or finding how many more. Start with objects: 'You have 8 grapes. You eat 3. How many are left?' Let the child physically remove objects and count what remains.",
            "scaffolding_sequence": [
                "Remove objects from a group and count what's left",
                "Introduce - and = symbols alongside manipulatives",
                "Connect to addition: if 3+5=8, then 8-5=3",
                "Practice counting back from the larger number",
                "Practice think-addition: 9-4=? Think 4+?=9",
            ],
            "socratic_questions": [
                "You have 7 and take away 3. How could you figure out what's left?",
                "If 6+2=8, what is 8-2?",
                "Is 7-3 the same as 3-7? Why not?",
            ],
            "practice_activities": [
                "Cover some objects, count what's visible",
                "Number line hopping backward",
                "Fact family triangles: 3, 5, 8",
            ],
            "real_world_connections": [
                "Eating snacks: had 10, ate 4, how many left?",
                "Friends leaving a group",
                "Spending coins",
            ],
            "common_misconceptions": [
                "Thinking subtraction is commutative",
                "Counting the starting number when counting back",
                "Not connecting subtraction to addition",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Recalls any subtraction fact within 10 in under 3 seconds",
                "Uses think-addition to solve subtraction",
                "Writes fact families",
            ],
            "assessment_methods": ["oral recall", "manipulative demo", "fact family writing"],
            "sample_assessment_prompts": ["What is 9-4?", "Show 7-3 with blocks", "Write the fact family for 2, 6, 8"],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is 5 - 2?",
                "expected_type": "number",
                "correct_answer": "3",
                "hints": ["Start with 5, take away 2"],
                "explanation": "5 - 2 = 3.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is 10 - 5?",
                "expected_type": "number",
                "correct_answer": "5",
                "hints": ["10 split in half"],
                "explanation": "10 - 5 = 5.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is 9 - 6?",
                "expected_type": "number",
                "correct_answer": "3",
                "hints": ["Think: 6 + ? = 9"],
                "explanation": "9 - 6 = 3.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Fill in: 10 - __ = 4",
                "expected_type": "number",
                "correct_answer": "6",
                "hints": ["Think: 4 + ? = 10"],
                "explanation": "10 - 6 = 4.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "If 3+5=8, write two subtraction facts using the same numbers.",
                "expected_type": "text",
                "hints": ["Use 3, 5, and 8"],
                "explanation": "8-3=5 and 8-5=3.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "What is 9 - 7?",
                "type": "number",
                "correct_answer": "2",
                "target_concept": "subtraction_facts",
            },
            {
                "prompt": "Write the fact family for 4, 5, 9.",
                "type": "text",
                "rubric": "Mastery: all four facts. Proficient: 3 facts. Developing: 1-2 facts.",
                "target_concept": "fact_families",
            },
            {
                "prompt": "You had 8 crayons. Some broke. Now you have 3. How many broke?",
                "type": "number",
                "correct_answer": "5",
                "target_concept": "subtraction_word_problem",
            },
        ],
        "resource_guidance": {
            "required": ["counting manipulatives", "number line"],
            "recommended": ["fact family triangles"],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Manipulatives extensively. Oral practice before written. Fact family triangles as anchors.",
            "adhd": "Game-based: bowling, cards. Never timed tests.",
            "gifted": "Subtraction within 20. Missing subtrahend. Negative number concepts.",
            "visual_learner": "Number line backward hops in color. Ten-frame removal.",
            "kinesthetic_learner": "Physical removal of objects. Walk backward on floor number line.",
            "auditory_learner": "Chant fact families. Subtraction songs. Partner quizzing.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Subtraction is taking some away and finding how many are left, or finding how many more one group holds than another. Today we take away with objects, write the number sentence that records it, and use the addition facts we know to find differences.",
                "gradual_release": {
                    "i_do": "Model with objects: here are eight grapes, eat three, physically remove them and count the five that remain. Write the number sentence, 8 - 3 = 5, and show its addition partner, 3 + 5 = 8.",
                    "we_do": "Remove objects from a group together and write the number sentence. Practice counting back from the larger number, and practice think-addition together: for 9 - 4, think four and what make nine.",
                    "you_do": "Child solves the subtraction facts within ten, first with objects and then without, writes the matching number sentences, and uses think-addition to find a difference.",
                },
                "guided_practice": [
                    "Take objects away from a group and count what remains",
                    "Fact-family triangles that link an addition and its two subtractions",
                    "Count back from the larger number on a number line",
                ],
                "independent_practice": [
                    "Subtraction fact practice through dice and card games rather than timed drill",
                    "Write the subtraction number sentence for each take-away",
                ],
                "mastery_check": [
                    "Recall any subtraction fact within ten quickly and correctly",
                    "Write a correct subtraction number sentence",
                    "Explain subtraction as the inverse of addition with a fact family",
                ],
                "spiral_review": [
                    "Revisit the addition facts and their fact families before extending subtraction recall",
                ],
            },
            "classical": {
                "narrative_introduction": "Subtraction is the undoing of addition: what has been joined can be parted again. Learn the differences within ten by heart, and see that every subtraction is an addition turned around.",
                "memory_work": {
                    "chants": [
                        "Chant a fact family in full: three and five are eight; eight take five is three; eight take three is five",
                        "Chant counting back from a number: nine, eight, seven, six",
                        "Chant the differences from ten: ten take one is nine, ten take two is eight",
                    ],
                    "recitations": [
                        "Recite the subtraction facts within ten in order, a few each day, until the whole set is held in memory",
                    ],
                },
                "copywork": [
                    "Copy subtraction number sentences neatly, such as 8 - 3 = 5, so the written form of each fact is sure and familiar to the hand",
                ],
                "recitation_routine": "Begin each lesson by reciting the differences learned so far, with their addition partners, before adding new ones; the facts are reviewed cumulatively, never assumed.",
                "history_integration": "Subtract one year from another on a simple timeline to find how long ago an event was, applying the parting of numbers to the chronological spine.",
                "read_aloud_suggestions": [
                    "A well-told story in which things are eaten, given away, or shared out, read aloud for its language and its quiet arithmetic",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 12,
                "living_book_suggestions": [
                    "A beautifully illustrated picture book in which real things are shared, eaten, or given away, chosen for lovely artwork and never a busy workbook",
                ],
                "short_lesson_flow": "Set out a small group of real objects. Ask the child to take some away and find how many are left, letting them discover the difference by counting what remains. Do two or three such takings-away, calmly, and stop while the child is still interested.",
                "narration_prompt": "Tell me what you did to find how many were left. How did you know your answer was right?",
                "real_world_objects": [
                    "Grapes or crackers, some eaten and the rest counted",
                    "Coins, some spent and the rest counted",
                    "A small group of toys, some given away and the rest counted",
                ],
                "nature_connection": "On a walk, gather a small handful of found things, give some away, and tell how many remain; record the little difference with a drawing in the nature notebook.",
                "habit_focus": "The habit of honest and careful work: counting exactly what remains, and trusting a difference only when it has truly been found.",
            },
            "montessori": {
                "prepared_materials": [
                    "The subtraction strip board with its numbered strips",
                    "Golden bead bars for laying out a quantity and taking a part away",
                    "The subtraction charts for the later memorization stage",
                ],
                "presentation": {
                    "three_period_lesson": "With a known difference: this is the difference, eight take three leaves five; show me a take-away that leaves five; what does eight take three leave? Spoken with the materials in hand.",
                    "steps": [
                        "Lay out a quantity in golden beads, take a part away, and count the quantity that remains",
                        "Use the subtraction strip board to build a difference and read it",
                        "Record the number sentence, then check the difference against the subtraction control chart",
                    ],
                },
                "control_of_error": "The fixed length of the strips on the subtraction strip board, and the subtraction control chart, let a wrong difference show itself as a mismatch the child sees and corrects without an adult's verdict.",
                "abstraction_pathway": "From taking beads away (the difference felt in the hand), to the strip board (the difference built and seen), to the charts (the differences committed to memory), toward recalling a difference and seeing subtraction as addition reversed with no material at all.",
                "extensions": [
                    "Find every way to take a part from a chosen whole and lay them out together",
                    "Work the subtraction snake game with the colored bead bars",
                ],
                "observation_focus": "Watch for the child connecting each subtraction to its addition partner, moving from counting back to thinking the addition, and returning to the subtraction work by choice.",
            },
            "unschooling": {
                "invitations": [
                    "Leave dice, dominoes, and a deck of cards on a low shelf and say nothing",
                    "Cook or bake together where pieces are eaten or taken away as you go",
                    "Keep a coin jar and a set of board games within reach",
                ],
                "real_world_contexts": [
                    "Eating some of a snack and counting what is left",
                    "Spending coins and counting the change that remains",
                    "Giving some toys away and counting those still on the shelf",
                    "Asking how many more one pile or one score holds than another",
                ],
                "conversation_starters": [
                    "You had seven and ate two. How many are left now?",
                    "We know three and four make seven. Could that help you take four from seven?",
                    "How many more grapes do I have than you?",
                ],
                "resource_bank": [
                    "Dice, dominoes, and playing cards kept available, not assigned",
                    "Board games that involve scoring and losing points",
                    "A coin jar and real money",
                    "Math picture books left on a low shelf",
                ],
                "parent_role": "Notice the daily moments of taking away, snacks eaten, coins spent, toys given, and count what remains aloud with the child. Ask genuine how-many-are-left and how-many-more questions, show how a known addition fact answers a subtraction, and let games and real life build the facts rather than a drill.",
                "observation_documentation": "Over time, note whether the child counts back or thinks the addition, which differences they simply know, whether they write or say subtraction sentences in play, and whether they see subtraction and addition as two sides of one fact. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Subtraction word problems need comprehension",
            "science": "Measuring differences: taller, heavier",
            "history": "Time spans between historical dates",
        },
    },
    "mf-07": {
        "enriched": True,
        "learning_objectives": [
            "Add any two numbers with sums to 20",
            "Use strategies: counting on, making ten, doubles, doubles plus one",
            "Solve addition word problems within 20",
        ],
        "teaching_guidance": {
            "introduction": "Extending beyond 10. The key strategy is making ten: to solve 8+5, think '8 needs 2 to make 10, then 3 left over, so 13.' Use ten-frames to make this visual.",
            "scaffolding_sequence": [
                "Review facts to 10, then extend with 10+1, 10+2, etc.",
                "Practice doubles to 20: 6+6=12, 7+7=14, 8+8=16, 9+9=18",
                "Practice doubles-plus-one: 6+7=13",
                "Master make-ten using ten-frames",
                "Solve word problems within 20",
            ],
            "socratic_questions": [
                "How could you use 7+7 to solve 7+8?",
                "What's a fast way to add 9 to any number?",
                "If 8+5 is hard, could you rearrange it?",
            ],
            "practice_activities": [
                "Ten-frame addition: fill first frame, overflow to second",
                "Double dice: roll one, double it",
                "Number bond puzzles for teens",
            ],
            "real_world_connections": ["Adding two-digit scores", "Combining groups larger than 10"],
            "common_misconceptions": [
                "Treating teens as two separate digits",
                "Not decomposing to use make-ten",
                "Over-relying on finger counting",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Solves any addition within 20 in under 5 seconds",
                "Explains make-ten strategy",
                "Solves word problems within 20",
            ],
            "assessment_methods": ["oral recall", "strategy explanation", "word problems"],
            "sample_assessment_prompts": ["What is 8+7?", "How would you solve 9+6 using make-ten?"],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is 10 + 6?",
                "expected_type": "number",
                "correct_answer": "16",
                "hints": ["10 plus a number is easy"],
                "explanation": "10 + 6 = 16.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is 7 + 7?",
                "expected_type": "number",
                "correct_answer": "14",
                "hints": ["Doubles fact"],
                "explanation": "7 + 7 = 14.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is 8 + 5?",
                "expected_type": "number",
                "correct_answer": "13",
                "hints": ["Make ten: 8+2=10, then 3 more"],
                "explanation": "8 + 5 = 13. Break 5 into 2+3. 8+2=10, 10+3=13.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is 9 + 7?",
                "expected_type": "number",
                "correct_answer": "16",
                "hints": ["9 is close to 10. 10+7=17, minus 1"],
                "explanation": "9 + 7 = 16.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Sara has 9 red flowers and 8 yellow. How many total? Explain your strategy.",
                "expected_type": "text",
                "hints": ["9+8. Try doubles: 9+9=18, minus 1"],
                "explanation": "9+8=17. Strategy: 9+9=18, minus 1 = 17.",
            },
        ],
        "assessment_items": [
            {"prompt": "What is 8 + 6?", "type": "number", "correct_answer": "14", "target_concept": "addition_to_20"},
            {
                "prompt": "Solve 7+8 and explain your strategy.",
                "type": "open_response",
                "rubric": "Mastery: correct (15) with clear strategy. Proficient: correct, vague. Developing: incorrect.",
                "target_concept": "addition_strategy",
            },
            {
                "prompt": "Jake found 6 shells then 9 more. How many?",
                "type": "number",
                "correct_answer": "15",
                "target_concept": "word_problem",
            },
        ],
        "resource_guidance": {"required": ["ten-frame boards", "counters"], "recommended": ["Rekenrek"]},
        "time_estimates": {"first_exposure": 25, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Ten-frame visuals, not written symbols. Oral strategy names.",
            "adhd": "High-engagement dice and card games. Rotate strategies.",
            "gifted": "Addition within 100. Two-digit plus one-digit mentally.",
            "visual_learner": "Double ten-frames. Arrow diagrams for make-ten.",
            "kinesthetic_learner": "Two ten-frames with counters. Move to fill one frame.",
            "auditory_learner": "Verbalize: 'Eight needs two to make ten. Five is two and three. Thirteen.'",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Now we add beyond ten. The key strategy is making ten: to add 8 + 5, give 8 the 2 it needs to make 10, then add the 3 that are left, 13. Today we use the strategies, counting on, doubles, doubles plus one, and making ten, and solve word problems within 20.",
                "gradual_release": {
                    "i_do": "Model making ten on two ten-frames: for 8 + 5, slide 2 counters across to fill the first frame to ten, then count the 3 that remain, 13. Model a double, 7 + 7, and a doubles-plus-one, 7 + 8.",
                    "we_do": "Build sums on the ten-frames together, naming the strategy aloud each time. Practice the doubles to twenty together, then solve a word problem within twenty together.",
                    "you_do": "Child adds two numbers with sums to twenty, choosing and naming a strategy, and solves addition word problems within twenty.",
                },
                "guided_practice": [
                    "Make ten on two ten-frames to add a single-digit pair past ten",
                    "Practice the doubles and doubles-plus-one to twenty",
                    "Sort facts by the strategy that fits them best",
                ],
                "independent_practice": [
                    "Strategy practice through dice and card games with sums to twenty",
                    "Solve written addition word problems within twenty",
                ],
                "mastery_check": [
                    "Add any two numbers with a sum to twenty",
                    "Name and use a strategy: counting on, doubles, doubles plus one, or making ten",
                    "Solve an addition word problem within twenty",
                ],
                "spiral_review": [
                    "Revisit the facts within ten and the make-ten strategy before practicing the harder sums to twenty",
                ],
            },
            "classical": {
                "narrative_introduction": "Beyond ten, addition rests on a few clear strategies and on the doubles. Learn the doubles to twenty by heart and the way to make a ten, and any sum to twenty comes within easy reach.",
                "memory_work": {
                    "chants": [
                        "Chant the doubles to twenty: six and six are twelve, seven and seven are fourteen, on to nine and nine",
                        "Chant the make-ten pairs: eight needs two, seven needs three, six needs four",
                        "Chant the doubles-plus-one facts: six and seven are thirteen",
                    ],
                    "recitations": [
                        "Recite the names of the strategies and what each one does: counting on, doubles, doubles plus one, making ten",
                    ],
                },
                "copywork": [
                    "Copy number sentences for sums to twenty, neatly, noting beside each the strategy that solved it",
                ],
                "recitation_routine": "Begin each lesson by reciting the doubles and the facts within ten before extending to the sums past ten; the work is cumulative and never assumed.",
                "history_integration": "Add quantities and spans of years larger than ten along a timeline, carrying addition past the ten onto the chronological spine.",
                "read_aloud_suggestions": [
                    "A well-told story in which larger groups of things are gathered and combined, read aloud for its language",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 12,
                "living_book_suggestions": [
                    "A beautifully illustrated picture book in which larger groups of real things are gathered and joined, chosen for lovely artwork",
                ],
                "short_lesson_flow": "Give the child real objects and a sum that reaches past ten. Let them find a way to the total in their own time, often by making a ten, and let them show you the way they found. Do one or two such sums, calmly, and stop while interest is high.",
                "narration_prompt": "Tell me the way you found the total. What did you do to make it easier than counting them all?",
                "real_world_objects": [
                    "Two groups of more than ten objects combined",
                    "Two game scores added together",
                    "Eggs counted across two cartons",
                ],
                "nature_connection": "On a walk, gather two nature collections that together pass ten, combine them, and tell the total; record it with a small drawing in the nature notebook.",
                "habit_focus": "The habit of thinking before counting: pausing to look for a clever way to the answer rather than counting every object from one.",
            },
            "montessori": {
                "prepared_materials": [
                    "The colored bead bars, one through ten, each length its own color",
                    "The addition snake game with its golden ten bars for exchanging",
                    "The teen boards and the addition charts",
                ],
                "presentation": {
                    "three_period_lesson": "With the snake game: this is a ten, made and exchanged; show me where a new ten is made; what have we made here? Spoken with the beads in hand.",
                    "steps": [
                        "Lay a snake of colored bead bars end to end",
                        "Count along the snake, and each time ten is reached, exchange the colored bars for a golden ten bar, so making ten is done by the hand",
                        "Record the sums reached, and check them against the addition control chart",
                    ],
                },
                "control_of_error": "The exchange in the snake game only works when a true ten is gathered, and the addition control chart confirms each sum, so a miscount shows itself to the child without an adult's verdict.",
                "abstraction_pathway": "From the snake game (making ten felt as a real exchange in the hand), to the addition charts (the sums to twenty committed to memory), toward adding to twenty by chosen strategy with no beads at all.",
                "extensions": [
                    "Lay longer snakes and exchange several tens",
                    "Build the teen quantities on the teen board and find the doubles among the bead bars",
                ],
                "observation_focus": "Watch for the child reaching for a ten by choice rather than counting all, and for free, repeated return to the snake game and the bead work.",
            },
            "unschooling": {
                "invitations": [
                    "Leave two or three dice, dominoes, and a deck of cards within reach",
                    "Keep board games with two-digit scoring and an egg carton or ten-frame tray accessible",
                    "Cook or bake together where amounts past ten are gathered and counted",
                ],
                "real_world_contexts": [
                    "Adding game scores that climb past ten",
                    "Combining two groups of more than ten things",
                    "Adding two prices while shopping",
                    "Counting eggs or objects across two cartons or trays",
                ],
                "conversation_starters": [
                    "You have eight and you want five more. Is there a quick way to get there?",
                    "What is seven and seven? So what would seven and eight be?",
                    "We are at fourteen. How many more to reach twenty?",
                ],
                "resource_bank": [
                    "Dice, dominoes, and playing cards kept available, not assigned",
                    "Board games with two-digit scoring",
                    "Egg cartons or ten-frame trays for grouping by ten",
                    "Math picture books left on a low shelf",
                ],
                "parent_role": "Combine and count aloud past ten wherever it arises in real life, scores, prices, collections, and ask genuine how-many-altogether questions. Notice and name the strategies the child invents, and let games and real combining build the strategies rather than a drill.",
                "observation_documentation": "Over time, note whether the child counts on, makes a ten, or uses the doubles, which sums to twenty they simply know, and whether they can solve a real word problem. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Two-step word problems to 20",
            "science": "Adding measurements exceeding 10",
            "history": "Adding groups of people or years",
        },
    },
    "mf-08": {
        "enriched": True,
        "learning_objectives": [
            "Subtract within 20 fluently",
            "Use think-addition strategy for subtraction",
            "Solve subtraction word problems within 20",
            "Understand: if 8+7=15, then 15-7=8",
        ],
        "teaching_guidance": {
            "introduction": "Subtraction within 20 builds on addition within 20. The most powerful strategy is think-addition: to solve 15-8, think '8 + what = 15?' Also use subtract-through-ten: 13-5 = 13-3-2 = 10-2 = 8.",
            "scaffolding_sequence": [
                "Review subtraction within 10",
                "Subtract teen numbers by thinking addition: 12-5, think 5+?=12",
                "Subtract through ten: 14-6 = 14-4-2 = 8",
                "Practice fact families for teen numbers",
                "Solve word problems: take-away, comparison, missing part",
            ],
            "socratic_questions": [
                "If you know 7+6=13, how does that help with 13-6?",
                "How would you solve 15-9?",
                "What's the connection between 8+8=16 and 16-8?",
            ],
            "practice_activities": [
                "Fact family flashcards for teen numbers",
                "Subtraction stories for problems like 17-9",
                "Number line jumps backward",
            ],
            "real_world_connections": [
                "Had 15 grapes, ate some, how many left?",
                "Comparing: 18 vs 11, how much more?",
            ],
            "common_misconceptions": [
                "Trying to count back large amounts instead of thinking addition",
                "Not connecting subtraction to known addition facts",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Solves any subtraction within 20 in under 5 seconds",
                "Explains think-addition strategy",
                "Solves comparison word problems",
            ],
            "assessment_methods": ["oral recall", "strategy explanation", "word problems"],
            "sample_assessment_prompts": ["What is 16-9?", "How does 6+8=14 help with 14-8?"],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is 12 - 2?",
                "expected_type": "number",
                "correct_answer": "10",
                "hints": ["Take 2 from 12"],
                "explanation": "12 - 2 = 10.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is 13 - 7?",
                "expected_type": "number",
                "correct_answer": "6",
                "hints": ["Think: 7 + ? = 13"],
                "explanation": "13 - 7 = 6.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is 16 - 8?",
                "expected_type": "number",
                "correct_answer": "8",
                "hints": ["8+8=16, so 16-8=?"],
                "explanation": "16 - 8 = 8. Doubles in reverse.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Amy has 17 beads. She gives 8 away. How many left?",
                "expected_type": "number",
                "correct_answer": "9",
                "hints": ["17-8. Think: 8+?=17"],
                "explanation": "17 - 8 = 9.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Write the fact family for 7, 9, 16.",
                "expected_type": "text",
                "hints": ["2 addition + 2 subtraction using 7, 9, 16"],
                "explanation": "7+9=16, 9+7=16, 16-7=9, 16-9=7.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "What is 15 - 7?",
                "type": "number",
                "correct_answer": "8",
                "target_concept": "subtraction_within_20",
            },
            {
                "prompt": "Lee has 14 crayons, Sam has 6. How many more does Lee have?",
                "type": "number",
                "correct_answer": "8",
                "target_concept": "comparison",
            },
            {
                "prompt": "Explain how knowing 8+5=13 helps solve 13-5.",
                "type": "open_response",
                "rubric": "Mastery: explains inverse relationship. Proficient: correct answer. Developing: counts back.",
                "target_concept": "inverse_relationship",
            },
        ],
        "resource_guidance": {"required": ["ten-frames", "counters"], "recommended": ["fact family triangles"]},
        "time_estimates": {"first_exposure": 25, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Think-addition: 15-8 becomes 8+?=15. Avoids backward counting.",
            "adhd": "Vary modality every 3-4 problems: oral, written, manipulative, game.",
            "gifted": "Subtraction within 100. Mental strategies. Check with addition.",
            "visual_learner": "Number line jumps color-coded. Fact family triangle cards.",
            "kinesthetic_learner": "Snap cube trains: break 15 into 8 and remainder.",
            "auditory_learner": "Verbalize: 'Nine plus what is sixteen? Seven. So sixteen minus nine is seven.'",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Subtraction within twenty leans on the addition facts we already know. The strongest strategy is think-addition: to solve 15 - 8, think eight and what make fifteen. We also subtract through ten: 13 - 5 is 13 take 3 to reach ten, then take 2 more. Today we subtract teen numbers fluently, write fact families, and solve word problems.",
                "gradual_release": {
                    "i_do": "Model 15 - 8 by think-addition, saying aloud eight and what make fifteen, seven. Model 14 - 6 as subtract-through-ten on a ten-frame: take 4 to reach ten, then take 2 more, eight. Then build the fact family for 7, 9, 16.",
                    "we_do": "Solve teen subtractions together by thinking the addition, subtract through ten together with counters, build and read a teen fact family together, and work a comparison word problem together.",
                    "you_do": "Child solves subtraction within twenty, names the strategy used, writes the fact family, and solves take-away and comparison word problems.",
                },
                "guided_practice": [
                    "Think-addition with fact-family triangles for teen numbers",
                    "Subtract through ten on a ten-frame",
                    "Comparison problems: find how many more one group holds than another",
                ],
                "independent_practice": [
                    "Teen subtraction practice through dice and card games rather than timed drill",
                    "Solve written subtraction word problems within twenty",
                ],
                "mastery_check": [
                    "Solve any subtraction within twenty",
                    "Explain the think-addition strategy",
                    "Solve a comparison word problem within twenty",
                ],
                "spiral_review": [
                    "Revisit subtraction within ten and the addition facts within twenty before harder teen subtraction",
                ],
            },
            "classical": {
                "narrative_introduction": "Every subtraction is an addition turned around, and the teen numbers part exactly as the smaller ones do. Learn the teen fact families by heart, and let the addition you already know answer the subtraction at once.",
                "memory_work": {
                    "chants": [
                        "Chant a teen fact family in full: seven and nine are sixteen; nine and seven are sixteen; sixteen take seven is nine; sixteen take nine is seven",
                        "Chant the doubles in reverse: eight and eight are sixteen, so sixteen take eight is eight",
                        "Chant the think-addition move: to take a number away, ask what adds back to the whole",
                    ],
                    "recitations": [
                        "Recite the teen subtraction facts and their addition partners in order, a few each day, until the set is held",
                    ],
                },
                "copywork": [
                    "Copy teen fact families and subtraction number sentences neatly, such as 16 - 7 = 9, so each written fact is sure to the hand",
                ],
                "recitation_routine": "Begin each lesson by reciting the teen facts and families learned so far, with their addition partners, before adding new ones; the work is cumulative and never assumed.",
                "history_integration": "Subtract one year from another on a simple timeline to find the span between two events, carrying the parting of numbers onto the chronological spine.",
                "read_aloud_suggestions": [
                    "A well-told story in which larger groups of things are given away, lost, or compared, read aloud for its language and its quiet arithmetic",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 12,
                "living_book_suggestions": [
                    "A beautifully illustrated picture book in which real things past ten are shared, eaten, or compared, chosen for lovely artwork and never a busy workbook",
                ],
                "short_lesson_flow": "Set out a real group of more than ten objects. Ask the child to take some away and find how many remain, or to compare two groups and find how many more one holds. Let the child show you the way they found it. Do one or two such problems, calmly, and stop while interest is high.",
                "narration_prompt": "Tell me how you found how many were left, or how many more. What did you do, and how did you know your answer was right?",
                "real_world_objects": [
                    "Strawberries or grapes, some eaten and the rest counted",
                    "Two groups of objects set side by side and compared",
                    "Coins, some spent and the rest counted",
                ],
                "nature_connection": "On a walk, gather two nature collections that pass ten, and tell how many more one holds than the other; record the comparison with a small drawing in the nature notebook.",
                "habit_focus": "The habit of thinking before counting: reaching for an addition fact already known rather than counting back one by one.",
            },
            "montessori": {
                "prepared_materials": [
                    "The subtraction strip board extended through the teen numbers",
                    "The colored bead bars and golden ten bars, for taking a quantity through ten",
                    "The stamp game for recording subtraction",
                ],
                "presentation": {
                    "three_period_lesson": "With a teen difference: this is the difference, fifteen take seven leaves eight; show me the addition hidden inside it; what does fifteen take seven leave? Spoken with the materials in hand.",
                    "steps": [
                        "Lay a teen quantity as a golden ten bar and a colored bar",
                        "Take a part away by first taking from the colored bar to reach ten, then taking from the ten, so subtracting through ten is done by the hand",
                        "Record the subtraction on the stamp game, and check the difference against the control chart",
                    ],
                },
                "control_of_error": "The fixed length of the subtraction strip board, the ten-bar exchange, and the control chart let a wrong difference show itself as a mismatch the child sees and corrects without an adult's verdict.",
                "abstraction_pathway": "From taking through ten with the bead bars (the strategy felt as a real exchange in the hand), to recording on the stamp game, toward solving teen subtraction by think-addition with no material at all.",
                "extensions": [
                    "Work longer subtraction problems on the strip board and the stamp game",
                    "Build the teen fact families with the bead bars and find the doubles among them",
                ],
                "observation_focus": "Watch for the child taking through ten or thinking the addition rather than counting back, and for free, repeated return to the subtraction work.",
            },
            "unschooling": {
                "invitations": [
                    "Leave two dice, dominoes, and a deck of cards within reach for free play with teen numbers",
                    "Keep a coin jar and board games with scoring past ten accessible",
                    "Cook or bake together where pieces past ten are eaten or taken away",
                ],
                "real_world_contexts": [
                    "Eating some of a group of more than ten things and counting what is left",
                    "Comparing two scores or two collections and asking how many more",
                    "Spending coins and counting the change that remains",
                    "Counting the days left until an awaited event",
                ],
                "conversation_starters": [
                    "You had seventeen and ate eight. How many are left now?",
                    "You know eight and eight are sixteen. Could that help you take eight from sixteen?",
                    "You have fourteen and I have six. How many more do you have than me?",
                ],
                "resource_bank": [
                    "Dice, dominoes, and playing cards kept available, not assigned",
                    "Board games with two-digit scoring",
                    "A coin jar and real money",
                    "Math picture books left on a low shelf",
                ],
                "parent_role": "Notice the daily moments of taking away and comparing past ten, snacks, scores, coins, and count what is left or how many more aloud with the child. Show how a known addition fact answers a subtraction, and let games and real life build the facts rather than a drill.",
                "observation_documentation": "Over time, note whether the child thinks the addition or counts back, which teen facts they simply know, whether they handle how-many-more comparisons, and whether they see subtraction and addition as two sides of one fact. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Comparison word problems: who has more?",
            "science": "Differences in measurements",
            "history": "Years between events",
        },
    },
    "mf-09": {
        "enriched": True,
        "learning_objectives": [
            "Understand that two-digit numbers are made of tens and ones",
            "Decompose numbers: 45 = 4 tens + 5 ones",
            "Use base-ten blocks to represent two-digit numbers",
        ],
        "teaching_guidance": {
            "introduction": "Place value is the biggest idea in elementary math. The digit 3 in 35 means something different from 3 in 53. Use base-ten blocks: a ten-rod is ten cubes stuck together. To build 34, grab 3 ten-rods and 4 unit cubes.",
            "scaffolding_sequence": [
                "Build numbers 10-19 with ten-rods and units",
                "Build numbers 20-50",
                "Build numbers 50-99",
                "Say tens and ones: '42 is 4 tens and 2 ones'",
                "Write expanded form: 42 = 40 + 2",
            ],
            "socratic_questions": [
                "In 67, what does the 6 mean? The 7?",
                "Which is worth more: the 3 in 36 or the 3 in 63?",
                "How many tens are in 80?",
            ],
            "practice_activities": [
                "Build numbers with blocks and write the numeral",
                "Place value mat: sort blocks into tens and ones columns",
                "Riddles: I have 5 tens and 3 ones. What number am I?",
            ],
            "real_world_connections": ["Dimes (10 cents) and pennies (1 cent)", "Bundles of 10 sticks vs loose sticks"],
            "common_misconceptions": [
                "Thinking 16 means '1 and 6' not '1 ten and 6 ones'",
                "Reversing digits",
                "Thinking ones digit is worth more",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Decomposes any two-digit number into tens and ones",
                "Builds any two-digit number with blocks",
                "Explains why digit position matters",
            ],
            "assessment_methods": ["block building", "expanded form writing", "oral explanation"],
            "sample_assessment_prompts": [
                "Build 73 with blocks",
                "Write 58 in expanded form",
                "Which digit is worth more in 49?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "How many tens are in 30?",
                "expected_type": "number",
                "correct_answer": "3",
                "hints": ["30 = ? tens and 0 ones"],
                "explanation": "30 has 3 tens.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "I have 5 tens and 2 ones. What number?",
                "expected_type": "number",
                "correct_answer": "52",
                "hints": ["5 tens = 50, plus 2"],
                "explanation": "52.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Write 67 in expanded form.",
                "expected_type": "text",
                "correct_answer": "60 + 7",
                "hints": ["Break into tens and ones"],
                "explanation": "67 = 60 + 7.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Which is greater: 47 or 74? Explain using place value.",
                "expected_type": "text",
                "hints": ["Compare tens digits"],
                "explanation": "74 is greater: 7 tens vs 4 tens.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "What number has 6 tens and 9 ones?",
                "type": "number",
                "correct_answer": "69",
                "target_concept": "place_value",
            },
            {
                "prompt": "Explain why the 5 in 56 is worth more than the 6.",
                "type": "open_response",
                "rubric": "Mastery: 5 means 50, 6 means 6. Proficient: says 5 means 50. Developing: cannot explain.",
                "target_concept": "place_value_understanding",
            },
        ],
        "resource_guidance": {"required": ["base-ten blocks"], "recommended": ["place value mat", "dimes and pennies"]},
        "time_estimates": {"first_exposure": 25, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Physical base-ten blocks before written notation. Say 'four tens and two ones' before 42.",
            "adhd": "Build numbers with blocks. Race to build: call a number, build fast.",
            "gifted": "Hundreds, thousands. Expanded notation: 342 = 300+40+2.",
            "visual_learner": "Place value mat with marked columns. Tens blue, ones green.",
            "kinesthetic_learner": "Bundle craft sticks into tens. Physical grouping essential.",
            "auditory_learner": "Say place value name: 'The five means five TENS which is FIFTY.'",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Place value is the biggest idea in early math: a digit's position tells how much it is worth. The 3 in 35 means three tens; the 3 in 53 means three ones. Today we build two-digit numbers with base-ten blocks, name their tens and ones, and write them in expanded form.",
                "gradual_release": {
                    "i_do": "Model building 34 on a place-value mat: three ten-rods in the tens column, four unit cubes in the ones column. Say three tens and four ones, thirty-four. Write the expanded form, 34 = 30 + 4.",
                    "we_do": "Build two-digit numbers together on the mat, naming the tens and the ones aloud each time. Write the expanded form together, and solve a place-value riddle together.",
                    "you_do": "Child builds any two-digit number with blocks, names its tens and ones, writes it in expanded form, and tells which digit is worth more.",
                },
                "guided_practice": [
                    "Build a number with base-ten blocks and write its numeral",
                    "Sort blocks into the tens and ones columns of a place-value mat",
                    "Place-value riddles: I have 5 tens and 3 ones, what number am I?",
                ],
                "independent_practice": [
                    "Write two-digit numbers in expanded form",
                    "Build a list of numbers with blocks and record each numeral",
                ],
                "mastery_check": [
                    "Decompose any two-digit number into tens and ones",
                    "Build any two-digit number with base-ten blocks",
                    "Explain why a digit's position changes its worth",
                ],
                "spiral_review": [
                    "Revisit the teen numbers as one ten and some ones before larger two-digit work",
                ],
            },
            "classical": {
                "narrative_introduction": "Our numbers hold a hidden cleverness: the same ten digits can write every number, because where a digit sits tells how much it is worth. The place of a digit is its rank, and learning that order is learning the secret of written number.",
                "memory_work": {
                    "chants": [
                        "Chant count-by-tens to one hundred, the spine of the tens place",
                        "Chant the place names from the right: ones, then tens",
                        "Chant the rule: the right-hand place is ones, the next place is tens",
                    ],
                    "recitations": [
                        "Recite the place-value rule, and read two-digit numbers aloud as so many tens and so many ones",
                    ],
                },
                "copywork": [
                    "Copy two-digit numbers in expanded form, neatly, such as 42 = 40 + 2, the writing making the tens and the ones plain",
                ],
                "recitation_routine": "Begin each lesson by reciting the place names and the place-value rule before new work; the idea is rehearsed cumulatively, never assumed.",
                "history_integration": "Tell, simply, that writing numbers by place was a great invention: older ways of writing numbers had no such cleverness, and the place-value system made all of arithmetic far easier.",
                "read_aloud_suggestions": [
                    "A well-made read-aloud about numbers and how large numbers are written, chosen for clear and rich language",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 12,
                "living_book_suggestions": [
                    "A beautifully illustrated picture book about numbers and the grouping of things, with real artwork and never a busy workbook",
                ],
                "short_lesson_flow": "Bring out real things to bundle. Count out ten craft sticks and tie them into a bundle of ten, then make more, and gather some loose ones. Make a two-digit number as bundles and loose sticks, and name its tens and its ones. Do one or two numbers, calmly, and stop while interest is high.",
                "narration_prompt": "Tell me how you made your number. How many bundles of ten did you use, and how many loose ones?",
                "real_world_objects": [
                    "Bundles of ten craft sticks tied with a band, beside loose single sticks",
                    "Dimes worth ten cents beside pennies worth one",
                    "Beans or buttons gathered into cups of ten with some loose",
                ],
                "nature_connection": "Gather a nature collection, bundle it into groups of ten with some loose ones, and write the two-digit total with a small drawing in the nature notebook.",
                "habit_focus": "The habit of orderly, careful work: gathering exactly ten before bundling, and keeping the tens and the ones each in their proper place.",
            },
            "montessori": {
                "prepared_materials": [
                    "The golden bead material: unit beads and ten-bars",
                    "The large place-value number cards that overlay, tens and ones",
                    "A place-value tray for laying out the quantity and its cards",
                ],
                "presentation": {
                    "three_period_lesson": "With the cards and beads: this is forty, four tens; show me forty; what is this? Always pairing the written card with the bead quantity.",
                    "steps": [
                        "Build a two-digit quantity with ten-bars and unit beads",
                        "Lay the matching tens card and units card beside the beads",
                        "Slide the units card over the zero of the tens card, so 40 with 2 becomes 42, showing the tens and the ones joined",
                    ],
                },
                "control_of_error": "The fixed bead quantities and the overlaying number cards make a wrong build show itself as a mismatch the child sees and corrects without an adult's verdict.",
                "abstraction_pathway": "From the golden beads (the tens and ones felt in the hand), to the overlay cards (the structure of place made visible), toward reading and writing any two-digit number from the held idea with no material.",
                "extensions": [
                    "Build numbers all the way to ninety-nine with the beads and cards",
                    "Work place-value riddles with the number cards alone",
                ],
                "observation_focus": "Watch for the child grasping that a digit's position carries its value, and for free, repeated work with the golden beads and cards by choice.",
            },
            "unschooling": {
                "invitations": [
                    "Leave bundling materials within reach: craft sticks and rubber bands, or beads to thread in tens",
                    "Keep a coin jar of dimes and pennies accessible",
                    "Set base-ten blocks out on a low shelf and say nothing",
                ],
                "real_world_contexts": [
                    "Counting and trading dimes and pennies",
                    "Bundling a pile of small things into groups of ten with some loose",
                    "Reading the two-digit numbers on house doors, page corners, and clocks",
                    "Filling an egg carton or ten-frame tray and counting the tens and the loose ones",
                ],
                "conversation_starters": [
                    "In thirty-five, what do you think the three stands for?",
                    "If we bundle these into tens, how many bundles will there be, and how many loose?",
                    "Which is worth more, the four or the nine in forty-nine?",
                ],
                "resource_bank": [
                    "Dimes and pennies and a coin jar",
                    "Craft sticks and rubber bands for bundling",
                    "Base-ten blocks kept available, not assigned",
                    "Number picture books on a low shelf",
                ],
                "parent_role": "Count and bundle things in tens through the day, and talk about what each digit means when a two-digit number comes up in real life. Answer the child's questions about big numbers, and let coins and bundling do the teaching rather than a worksheet.",
                "observation_documentation": "Over time, note whether the child sees a two-digit number as tens and ones, can bundle a pile into tens and decompose a number, and understands that a digit's position carries its worth. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Understanding page and chapter numbers",
            "science": "Recording two-digit measurements",
            "history": "Understanding years and decades",
        },
    },
    "mf-10": {
        "enriched": True,
        "learning_objectives": [
            "Skip count by 2s to 30",
            "Skip count by 5s to 100",
            "Skip count by 10s to 100",
            "Recognize patterns in skip counting",
        ],
        "teaching_guidance": {
            "introduction": "Skip counting is counting by groups. It's faster, reveals patterns, and builds the foundation for multiplication. Start with physical objects grouped in twos, fives, and tens.",
            "scaffolding_sequence": [
                "Group objects in pairs, count by 2s",
                "Use a hundred chart: color every 2nd number",
                "Count by 5s using tally marks",
                "Count by 10s using ten-rods",
                "Identify patterns: 5s end in 0 or 5, 10s end in 0",
            ],
            "socratic_questions": [
                "What pattern do you see counting by 2s?",
                "If counting by 5s and we're at 35, what's next?",
                "Why is counting by 10s so easy?",
            ],
            "practice_activities": [
                "Count pairs of shoes by 2s",
                "Count nickels by 5s",
                "Hundred chart: circle patterns for 2s, 5s, 10s in different colors",
            ],
            "real_world_connections": ["Counting nickels", "Counting dimes", "Counting pairs of socks"],
            "common_misconceptions": ["Starting at 0 instead of the skip number", "Losing the pattern mid-sequence"],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Skip counts by 2s to 30 fluently",
                "By 5s to 100 fluently",
                "By 10s to 100 fluently",
            ],
            "assessment_methods": ["oral skip counting", "pattern completion"],
            "sample_assessment_prompts": ["Count by 2s to 24", "Count by 5s to 60", "Count by 10s to 100"],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Count by 10s: 10, 20, 30, __, __, __",
                "expected_type": "text",
                "correct_answer": "40, 50, 60",
                "hints": ["Add 10 each time"],
                "explanation": "40, 50, 60.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Count by 5s: 5, 10, 15, 20, __, __",
                "expected_type": "text",
                "correct_answer": "25, 30",
                "hints": ["Add 5 each time"],
                "explanation": "25, 30.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Count by 2s: 12, 14, 16, __, __, __",
                "expected_type": "text",
                "correct_answer": "18, 20, 22",
                "hints": ["Add 2 each time"],
                "explanation": "18, 20, 22.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Count by 5s from 35 to 70.",
                "expected_type": "text",
                "correct_answer": "35, 40, 45, 50, 55, 60, 65, 70",
                "hints": ["Start at 35, add 5 each time"],
                "explanation": "35, 40, 45, 50, 55, 60, 65, 70.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Count by 2s from 2 to 20.",
                "type": "text",
                "correct_answer": "2, 4, 6, 8, 10, 12, 14, 16, 18, 20",
                "target_concept": "skip_counting_2s",
            },
            {
                "prompt": "What pattern do you notice counting by 5s?",
                "type": "open_response",
                "rubric": "Mastery: all end in 0 or 5, alternating. Proficient: end in 0 or 5. Developing: no pattern identified.",
                "target_concept": "patterns",
            },
        ],
        "resource_guidance": {"required": ["hundred chart"], "recommended": ["coins", "objects for grouping"]},
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Oral skip counting with rhythm. Highlighted skip-count numbers on chart.",
            "adhd": "Full-body: jump on every count. Bounce ball while skip counting.",
            "gifted": "By 3s, 4s, 6s, 7s, 8s, 9s. Connect to multiplication. Common multiples.",
            "visual_learner": "Color-coded chart: 2s red, 5s blue, 10s green.",
            "kinesthetic_learner": "Walk floor line stepping on every 2nd, 5th, 10th number.",
            "auditory_learner": "Rhythmic chanting. Whisper skipped, shout counted. Songs.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Skip counting is counting by groups instead of by ones. It is faster, it reveals patterns, and it lays the ground for multiplication. Today we count by twos, fives, and tens, and we find the pattern in each.",
                "gradual_release": {
                    "i_do": "Model grouping objects in pairs and counting them by twos. Color every fifth number on a hundred chart and read the count by fives. Count ten-rods by tens, and name the pattern aloud.",
                    "we_do": "Group objects and skip-count them together. Color the hundred-chart patterns for twos, fives, and tens together, and name what each pattern is: fives end in zero or five, tens end in zero.",
                    "you_do": "Child skip-counts by twos to thirty, by fives and tens to one hundred, and describes the pattern of each.",
                },
                "guided_practice": [
                    "Count grouped objects by twos, fives, and tens",
                    "Color the hundred-chart patterns for twos, fives, and tens in different colors",
                    "Fill in the missing numbers of a skip-count sequence",
                ],
                "independent_practice": [
                    "Skip-count practice through movement and counting games",
                    "Complete skip-count strips for twos, fives, and tens",
                ],
                "mastery_check": [
                    "Skip-count by twos to thirty fluently",
                    "Skip-count by fives and by tens to one hundred fluently",
                    "Describe the pattern in a skip-count sequence",
                ],
                "spiral_review": [
                    "Revisit counting by tens and counting to one hundred before extending the skip counts",
                ],
            },
            "classical": {
                "narrative_introduction": "Skip counting is the first music of multiplication. Chanted until they are sure, the twos, the fives, and the tens become a foundation that all later arithmetic stands upon.",
                "memory_work": {
                    "chants": [
                        "Chant by twos to thirty, daily and rhythmic",
                        "Chant by fives to one hundred, and chant by tens to one hundred",
                        "Chant the patterns: the fives end in zero or five, the tens end in zero",
                    ],
                    "recitations": [
                        "Recite the skip-count sequences in order, cumulatively, before each new one is extended",
                    ],
                },
                "copywork": [
                    "Copy the skip-count sequences neatly in rows, the columns making the repeating pattern plain to the eye",
                ],
                "recitation_routine": "Begin each lesson by reciting the skip counts learned so far before extending them; the sequences are rehearsed in full, never assumed.",
                "history_integration": "Count along a timeline by tens, marking the decades, so skip counting is practiced on the chronological spine.",
                "read_aloud_suggestions": [
                    "A rhythmic, well-made counting book that plays with groups of things, read aloud with expression",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A lovely picture book in which real things come in groups, pairs and bunches and stacks, chosen for beautiful artwork",
                ],
                "short_lesson_flow": "Bring out real things that naturally come in groups, pairs of shoes, stacks of pennies, and count them together by twos or by fives. Notice the pattern as it unfolds. Count one such set, calmly, and stop while the child is still interested.",
                "narration_prompt": "Tell me how you counted them. What did you count by, and what did you notice about the numbers?",
                "real_world_objects": [
                    "Pairs of shoes or socks counted by twos",
                    "Nickels counted by fives and dimes counted by tens",
                    "Stacks or bunches of small things",
                ],
                "nature_connection": "On a walk, count found things that come in groups, the petals of flowers, the legs of insects, and add a skip count to the nature notebook with a small drawing.",
                "habit_focus": "The habit of noticing: attending to the pattern as it unfolds and holding the count steady without losing it midway.",
            },
            "montessori": {
                "prepared_materials": [
                    "The colored bead chains, the short chains for skip counting and the long chains for extended work",
                    "Numeral tickets and arrows for marking the landmark numbers",
                    "The hundred board for seeing the skip-count patterns",
                ],
                "presentation": {
                    "three_period_lesson": "With a bead chain: this is counting by fives; show me where twenty falls on the chain; what number is this landmark? Spoken with the beads in hand.",
                    "steps": [
                        "Lay out a bead chain and count along it, touching each bead bar in turn",
                        "Lay a numeral ticket at the end of each bar, five, ten, fifteen, so the skip count is built and labeled",
                        "Read the landmark numbers back, and find the same pattern on the hundred board",
                    ],
                },
                "control_of_error": "The fixed length of each bead bar and the numeral tickets make a miscount show itself as a mismatch the child sees and corrects without an adult's word.",
                "abstraction_pathway": "From counting the bead chain bar by bar (the skip count built and felt in the hand), toward chanting and writing the twos, fives, and tens from memory.",
                "extensions": [
                    "Count the longer bead chains and mark their landmarks",
                    "Color the patterns of twos, fives, and tens on the hundred board",
                ],
                "observation_focus": "Watch for the child counting by the group rather than by ones, and for noticing the landmark patterns by choice.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a coin jar of nickels and dimes within reach",
                    "Leave a hundred chart and pairs of things to count where the child will find them",
                    "Set out board games whose pieces or scores move in groups",
                ],
                "real_world_contexts": [
                    "Counting nickels by fives and dimes by tens",
                    "Counting pairs of shoes, socks, or gloves by twos",
                    "Counting fingers and toes by fives",
                    "Scoring by twos or fives in a game",
                ],
                "conversation_starters": [
                    "These come in twos. Is there a faster way to count them than one at a time?",
                    "We are counting nickels: five, ten, what comes next?",
                    "Why do you think counting dimes is so easy?",
                ],
                "resource_bank": [
                    "A coin jar of nickels and dimes",
                    "A hundred chart kept available, not assigned",
                    "Board games that move or score in groups",
                    "Counting picture books on a low shelf",
                ],
                "parent_role": "Count by groups aloud wherever it arises in real life, coins, pairs, stacks, and follow the child's own noticing of the patterns. Answer real questions, and let counting coins and games do the teaching rather than a worksheet.",
                "observation_documentation": "Over time, note whether the child counts by twos, fives, and tens, whether they see and use the patterns, and whether they begin each count at the skip number rather than at zero. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Rhythm in poetry connects to skip counting rhythm",
            "science": "Counting by groups when tallying observations",
            "history": "Decades (by 10s) and centuries on timelines",
        },
    },
    "mf-11": {
        "enriched": True,
        "learning_objectives": [
            "Compare two numbers using greater than, less than, equal to",
            "Use > < = symbols correctly",
            "Compare two-digit numbers by tens first, then ones",
            "Order numbers from least to greatest",
        ],
        "teaching_guidance": {
            "introduction": "Comparing answers 'which is more?' Use two groups side by side. For two-digit numbers, compare tens first. If equal, compare ones. The alligator mouth faces the bigger number.",
            "scaffolding_sequence": [
                "Compare groups of objects by matching one-to-one",
                "Compare single-digit numbers with > < =",
                "Introduce alligator mouth mnemonic",
                "Compare two-digit numbers: tens first",
                "Order 3-5 numbers least to greatest",
            ],
            "socratic_questions": [
                "Which group has more? How do you know?",
                "Is 34 greater or less than 43? How did you decide?",
                "If tens are the same, how do you compare?",
            ],
            "practice_activities": [
                "Comparison war card game",
                "Number line ordering",
                "Build both numbers with blocks and compare",
            ],
            "real_world_connections": ["Comparing ages", "Comparing prices", "Comparing game scores"],
            "common_misconceptions": ["Comparing ones instead of tens first", "Reversing > and <"],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Correctly compares any two numbers within 100",
                "Explains using place value",
                "Orders 5 numbers least to greatest",
            ],
            "assessment_methods": ["symbol placement", "ordering", "explanation"],
            "sample_assessment_prompts": ["Put > < or = between 45 and 54", "Order: 72, 27, 45, 54, 63"],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which is greater: 7 or 3?",
                "expected_type": "number",
                "correct_answer": "7",
                "hints": ["Which comes later when counting?"],
                "explanation": "7 is greater.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Put > < or = between 5 and 5.",
                "expected_type": "text",
                "correct_answer": "=",
                "hints": ["Are they the same?"],
                "explanation": "5 = 5.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Which is greater: 38 or 83?",
                "expected_type": "number",
                "correct_answer": "83",
                "hints": ["Compare tens: 3 vs 8"],
                "explanation": "83. It has 8 tens vs 3 tens.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Order least to greatest: 45, 54, 39, 93, 41",
                "expected_type": "text",
                "correct_answer": "39, 41, 45, 54, 93",
                "hints": ["Find smallest tens digit first"],
                "explanation": "39, 41, 45, 54, 93.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Write > < or = between 47 and 74.",
                "type": "text",
                "correct_answer": "<",
                "target_concept": "comparison",
            },
            {
                "prompt": "Order least to greatest: 62, 26, 55, 82",
                "type": "text",
                "correct_answer": "26, 55, 62, 82",
                "target_concept": "ordering",
            },
            {
                "prompt": "Explain how you compare two two-digit numbers.",
                "type": "open_response",
                "rubric": "Mastery: compare tens first, then ones. Proficient: gets correct answers. Developing: compares ones first.",
                "target_concept": "comparison_strategy",
            },
        ],
        "resource_guidance": {
            "required": ["comparison symbol cards", "base-ten blocks"],
            "recommended": ["number line"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Base-ten blocks to compare visually. Say comparison aloud, not just symbols.",
            "adhd": "Comparison war card game: flip two, compare, slap bigger. High engagement.",
            "gifted": "Three-digit numbers. Order 5+. Density: always a number between two numbers.",
            "visual_learner": "Number line with both marked. Block towers side by side.",
            "kinesthetic_learner": "Build both numbers with blocks. Compare heights physically.",
            "auditory_learner": "Say: 'Seven tens is more than four tens. Seventy-four is greater.'",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Comparing answers the question, which is more. We set two groups side by side. For two-digit numbers we compare the tens first, and only if the tens are equal do we compare the ones. Today we use the symbols for greater than, less than, and equal to, and we order numbers from least to greatest.",
                "gradual_release": {
                    "i_do": "Model with two groups of objects, matching them one to one to see which has more. Write the comparison with the symbol, its open side facing the larger number. Build 34 and 43 with base-ten blocks and compare the tens first.",
                    "we_do": "Compare numbers together, placing the greater-than, less-than, or equal sign. Build both numbers and compare them, and order three numbers from least to greatest together.",
                    "you_do": "Child compares any two numbers within one hundred, places the correct symbol, explains the comparison using place value, and orders five numbers from least to greatest.",
                },
                "guided_practice": [
                    "Comparison war: each player turns a card, the higher number wins",
                    "Build both numbers with blocks and compare the tens, then the ones",
                    "Place the greater-than, less-than, or equal sign between number pairs",
                ],
                "independent_practice": [
                    "Order sets of numbers from least to greatest",
                    "Comparison practice pages with the three symbols",
                ],
                "mastery_check": [
                    "Correctly compare any two numbers within one hundred",
                    "Explain a comparison using place value",
                    "Order five numbers from least to greatest",
                ],
                "spiral_review": [
                    "Revisit tens and ones place value before harder two-digit comparisons",
                ],
            },
            "classical": {
                "narrative_introduction": "Numbers stand in an unbroken order, each one greater than the one before it. To compare two numbers is to find their places in that order. Learn the rule, compare the tens first and then the ones, and any two numbers can be set rightly side by side.",
                "memory_work": {
                    "chants": [
                        "Chant the rule of comparing: compare the tens first; if the tens are equal, compare the ones",
                        "Chant the count, so the order of the numbers is sure and ready",
                        "Chant the sign rule: the open side of the sign faces the greater number",
                    ],
                    "recitations": [
                        "Recite the rule of comparing, and read comparisons aloud, such as forty-five is less than fifty-four",
                    ],
                },
                "copywork": [
                    "Copy comparisons neatly with their symbols, such as 45 < 54, and copy short lists set in order from least to greatest",
                ],
                "recitation_routine": "Begin each lesson by reciting the rule of comparing and the count before new comparisons; the rule is rehearsed cumulatively, never assumed.",
                "history_integration": "Order the years of events along a timeline from earliest to latest, applying least-to-greatest to the chronological spine.",
                "read_aloud_suggestions": [
                    "A well-told story in which things are measured, weighed, and compared, read aloud for its language",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 12,
                "living_book_suggestions": [
                    "A beautifully illustrated picture book in which amounts of real things are compared, chosen for lovely artwork and never a busy workbook",
                ],
                "short_lesson_flow": "Set out two groups of real things, two bags or two baskets. Ask the child which has more, and let them tell you how they know. Introduce the words greater and less as they are needed. Compare one or two pairs, calmly, and stop while interest is high.",
                "narration_prompt": "Tell me which group had more, and how you knew it was the greater one.",
                "real_world_objects": [
                    "Two bags or baskets of objects set side by side",
                    "Two stacks of coins compared",
                    "Two groups of nature finds gathered on a walk",
                ],
                "nature_connection": "Gather two nature collections, compare them to see which holds more, and set three or four collections in order from least to greatest; record the comparison in the nature notebook.",
                "habit_focus": "The habit of fair and careful judgment: looking truly to see which is the greater rather than guessing at a glance.",
            },
            "montessori": {
                "prepared_materials": [
                    "The golden bead material for building two quantities side by side",
                    "The large numeral cards",
                    "A small set of comparison symbol cards for greater than, less than, and equal to",
                ],
                "presentation": {
                    "three_period_lesson": "With two built quantities: this is the greater; show me the greater; which of these is greater? Always with the quantities in view.",
                    "steps": [
                        "Build two two-digit quantities with golden beads, set side by side",
                        "Compare the tens first and then the ones, and lay the symbol card between them so its open side faces the greater quantity",
                        "Order three or more built quantities from least to greatest",
                    ],
                },
                "control_of_error": "The bead quantities are concrete and fully visible, so a wrong comparison shows itself plainly when the two quantities stand side by side.",
                "abstraction_pathway": "From comparing the bead quantities (which is more, seen and felt), to comparing the numeral cards by their places, toward comparing written numbers with no material at all.",
                "extensions": [
                    "Order longer sets of built numbers from least to greatest",
                    "Compare numbers all the way to ninety-nine",
                ],
                "observation_focus": "Watch for the child comparing the tens first by choice, and for free, repeated work with the comparing material.",
            },
            "unschooling": {
                "invitations": [
                    "Leave a deck of cards within reach for a comparison war game",
                    "Keep two jars or collections side by side, inviting a which-has-more question",
                    "Set out board games whose scores are compared at the end",
                ],
                "real_world_contexts": [
                    "Comparing ages, heights, and shoe sizes in the family",
                    "Comparing prices while shopping",
                    "Comparing game scores to see who is ahead",
                    "Lining up collections and asking which group is the largest",
                ],
                "conversation_starters": [
                    "Which pile do you think has more? How could we be sure?",
                    "Is thirty-four more or less than forty-three? How can you tell?",
                    "Who has the higher score so far?",
                ],
                "resource_bank": [
                    "A deck of cards for comparison games",
                    "Board games with scores to compare",
                    "Number picture books on a low shelf",
                ],
                "parent_role": "Compare and order things aloud wherever it arises in real life, prices, ages, scores, and ask genuine which-is-more questions. Talk about looking at the tens first when two-digit numbers come up, and let games and real comparisons do the teaching.",
                "observation_documentation": "Over time, note whether the child compares two numbers accurately, looks at the tens first for two-digit numbers, uses the comparison symbols, and can put a set of numbers in order. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Comparing word lengths or page counts",
            "science": "Comparing measurements: heavier, taller, longer",
            "history": "Comparing dates: which came first?",
        },
    },
    "mf-12": {
        "enriched": True,
        "learning_objectives": [
            "Understand ordinal numbers first through tenth",
            "Use ordinal numbers to describe position",
            "Distinguish ordinal from cardinal numbers",
        ],
        "teaching_guidance": {
            "introduction": "Cardinal numbers tell how many (three cats). Ordinal numbers tell position (the third cat). Line up objects and practice: first, second, third through tenth.",
            "scaffolding_sequence": [
                "Line up 5 objects, practice first through fifth",
                "Extend to first through tenth",
                "Practice with real sequences: who is first in line?",
                "Match ordinal words to abbreviations: 1st, 2nd, 3rd",
            ],
            "socratic_questions": [
                "What is the difference between 'three' and 'third'?",
                "If 5 people are in line and you are second, how many are ahead?",
            ],
            "practice_activities": [
                "Line up 10 toys and name positions",
                "Calendar: what day is the 3rd?",
                "Story problems: the 5th house has a red door",
            ],
            "real_world_connections": ["Line order at school", "Calendar dates", "Race finishing order"],
            "common_misconceptions": ["Confusing ordinal and cardinal", "Starting ordinal counting from zero"],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Uses ordinal numbers first through tenth correctly",
                "Writes abbreviations 1st-10th",
                "Applies to real situations",
            ],
            "assessment_methods": ["oral identification", "written abbreviations"],
            "sample_assessment_prompts": ["Point to the fourth object", "Write the abbreviation for seventh"],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Write the abbreviation for 'fifth'.",
                "expected_type": "text",
                "correct_answer": "5th",
                "hints": ["Number followed by th"],
                "explanation": "Fifth = 5th.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "8 books on a shelf. You want the 6th. How many are before it?",
                "expected_type": "number",
                "correct_answer": "5",
                "hints": ["6th book has books 1st-5th before it"],
                "explanation": "5 books before the 6th.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Tom is 1st, Sara is 3rd, Lee is between them. What place is Lee?",
                "expected_type": "text",
                "correct_answer": "2nd",
                "hints": ["Between 1st and 3rd"],
                "explanation": "Lee is 2nd.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "10 houses on a street. The 4th is blue, the 7th is red. How many houses between them?",
                "expected_type": "number",
                "correct_answer": "2",
                "hints": ["5th and 6th are between them"],
                "explanation": "2 houses (5th and 6th).",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Point to the 7th object in a line of 10.",
                "type": "number",
                "correct_answer": "7",
                "target_concept": "ordinal",
            },
            {
                "prompt": "What is the difference between 'four' and 'fourth'?",
                "type": "open_response",
                "rubric": "Mastery: four is how many, fourth is position. Proficient: gives example. Developing: cannot distinguish.",
                "target_concept": "cardinal_vs_ordinal",
            },
        ],
        "resource_guidance": {
            "required": ["10 objects for ordering"],
            "recommended": ["calendar", "ordinal number cards"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 10},
        "accommodations": {
            "dyslexia": "Oral practice first. Physical lineup. Written abbreviations after oral is solid.",
            "adhd": "Active games: race to be first, second, third. Line up toys.",
            "gifted": "Extend to 20th, 50th, 100th. Calendar dates. Historical sequences.",
            "visual_learner": "Numbered position cards next to objects in line.",
            "kinesthetic_learner": "Walk the line pointing and naming positions.",
            "auditory_learner": "Chant ordinals. Stories: 'The THIRD little pig.'",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Cardinal numbers tell how many, as in three cats. Ordinal numbers tell position, as in the third cat. Today we name positions first through tenth, write the abbreviations 1st through 10th, and learn to tell an ordinal number from a cardinal one.",
                "gradual_release": {
                    "i_do": "Model with a line of five objects: name first through fifth, touching each in turn. Write the abbreviations 1st, 2nd, 3rd. Explain plainly the difference between three and third.",
                    "we_do": "Line objects up and name positions together through tenth. Match the ordinal words to their abbreviations together, and find positions in a real line of people or things.",
                    "you_do": "Child names positions first through tenth, writes the abbreviations 1st through 10th, and tells ordinal from cardinal in sentences.",
                },
                "guided_practice": [
                    "Line up ten objects and name each position first through tenth",
                    "Match ordinal words to their abbreviations, first to 1st through tenth to 10th",
                    "Find ordinal dates on a calendar",
                ],
                "independent_practice": [
                    "Ordinal position practice pages",
                    "Write the abbreviations for the ordinal words",
                ],
                "mastery_check": [
                    "Use ordinal numbers first through tenth correctly",
                    "Write the abbreviations 1st through 10th",
                    "Apply ordinal numbers to a real situation",
                ],
                "spiral_review": [
                    "Revisit counting to ten and the difference between how-many and which-position",
                ],
            },
            "classical": {
                "narrative_introduction": "Besides the numbers that tell how many, there are numbers that tell which one in an order: first, second, third. Learn the ordinal names in their sequence, and every position has a name ready for it.",
                "memory_work": {
                    "chants": [
                        "Chant the ordinal numbers in order, first through tenth",
                        "Chant the ordinal-and-abbreviation pairs: first, 1st; second, 2nd; third, 3rd",
                    ],
                    "recitations": [
                        "Recite the ordinals first through tenth, and note that words such as primary and secondary come from old roots for first and second",
                    ],
                },
                "copywork": [
                    "Copy the ordinal words and their abbreviations neatly, such as first and 1st, second and 2nd",
                ],
                "recitation_routine": "Begin each lesson by reciting the ordinal sequence before new work; the sequence is rehearsed cumulatively, never assumed.",
                "history_integration": "Name the order of events on a timeline, the first event and the second, and note that kings and queens are numbered by ordinals, a ruler called the Third.",
                "read_aloud_suggestions": [
                    "A well-told story or rhyme that names things in their order, read aloud for its language",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A lovely story with a clear sequence of events, told in worthy language and real illustrations",
                ],
                "short_lesson_flow": "With the child, line up a few real things, or recall together the order of the day's events. Name the positions naturally, first, second, third, as they come. Take one short turn, and stop while the child is still interested.",
                "narration_prompt": "After a story, tell me what happened first, what happened second, and what came after that.",
                "real_world_objects": [
                    "The order of children in a line",
                    "The order of the events of the day",
                    "Dates on the calendar and places in a row",
                ],
                "nature_connection": "On a walk, notice the order of things seen, the first bird, the second tree, and record an ordered list in the nature notebook.",
                "habit_focus": "The habit of orderly attention: keeping events and things in their true order, first things first.",
            },
            "montessori": {
                "prepared_materials": [
                    "A set of identical small objects to line up",
                    "Ordinal label cards, first through tenth, with their abbreviations",
                    "A calendar for ordinal dates",
                ],
                "presentation": {
                    "three_period_lesson": "With a line of objects: this one is the third; show me the third; which position is this? Spoken with the line in view.",
                    "steps": [
                        "Line up ten objects in a row",
                        "Name a position, and the child places the matching ordinal label, then names each position in turn",
                        "Find and name ordinal dates on the calendar",
                    ],
                },
                "control_of_error": "The line of objects is itself the control: the third object is plainly the third, so a mislabel shows against the line and the child corrects it.",
                "abstraction_pathway": "From naming positions in a real line of objects, to matching the ordinal label cards, toward using the ordinal words and abbreviations with no objects at all.",
                "extensions": [
                    "Name ordinal dates across the calendar month",
                    "Name positions in longer lines and in the real routines of the day",
                ],
                "observation_focus": "Watch for the child distinguishing how-many, the cardinal, from which-place, the ordinal.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a calendar at child height where ordinal dates are read each day",
                    "Leave toys and figures out for lining-up and ordering play",
                    "Set out games whose finishing order or turn order matters",
                ],
                "real_world_contexts": [
                    "Who is first in line and who is second",
                    "The order of the events of the day",
                    "Calendar dates and the floors of a building",
                    "Finishing order in a race or game, and whose turn comes first",
                ],
                "conversation_starters": [
                    "You are second in line. How many people are ahead of you?",
                    "What was the third thing we did today?",
                    "Whose turn was first, and whose came next?",
                ],
                "resource_bank": [
                    "A wall calendar the child can reach",
                    "Games with a turn order or a finishing order",
                    "Story books with a clear sequence of events",
                ],
                "parent_role": "Use ordinal words naturally through the day, first, next, the third, and point out finishing order and calendar dates as they come up. Answer the child's questions about position, and let real routines do the teaching.",
                "observation_documentation": "Over time, note whether the child uses the ordinal numbers first through tenth, tells an ordinal from a cardinal number, and applies position words in real life. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Sequence: first, second, third in stories",
            "science": "Experiment steps: first, second, third",
            "history": "Chronological order of events",
        },
    },
    "mf-13": {
        "enriched": True,
        "learning_objectives": [
            "Measure length using nonstandard units",
            "Understand measurement requires consistent units",
            "Compare lengths of two objects",
            "Use rulers to measure in inches",
        ],
        "teaching_guidance": {
            "introduction": "Measurement starts with comparison: which is longer? Then 'how much longer?' using units. Start with nonstandard units (paper clips) so the child understands repeating a unit end-to-end. Then transition to rulers.",
            "scaffolding_sequence": [
                "Compare two objects: which is longer?",
                "Measure with paper clips laid end-to-end",
                "Measure same object with blocks: different number, discuss why",
                "Introduce ruler with standard units",
                "Measure objects to the nearest inch",
            ],
            "socratic_questions": [
                "Why did you get a different number with blocks vs paper clips?",
                "What if everyone used different-sized clips?",
                "Why do we need rulers?",
            ],
            "practice_activities": [
                "Measure 5 objects with paper clips, record in a chart",
                "Estimate then measure with a ruler",
                "Compare two objects: how much longer is one?",
            ],
            "real_world_connections": [
                "Measuring height growth",
                "Measuring for recipes",
                "Checking if furniture fits",
            ],
            "common_misconceptions": [
                "Not starting at the end of the object",
                "Gaps between paper clips",
                "Starting at 1 instead of 0 on ruler",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Measures with nonstandard units accurately",
                "Measures with ruler to nearest inch",
                "Explains why standard units matter",
            ],
            "assessment_methods": ["hands-on measurement", "ruler reading", "oral explanation"],
            "sample_assessment_prompts": ["Measure this pencil with paper clips", "Measure this book with a ruler"],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "A book is 8 paper clips long. A shoe is 10. Which is longer?",
                "expected_type": "text",
                "correct_answer": "the shoe",
                "hints": ["10 > 8"],
                "explanation": "The shoe. 10 > 8.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You measure a table with your hand and get 6. Your friend gets 8. Did the table change? What happened?",
                "expected_type": "text",
                "hints": ["Are your hands the same size?"],
                "explanation": "No change. Your hand is bigger than your friend's. This is why we need standard units.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "A line goes from 0 to 5 on a ruler. How many inches?",
                "expected_type": "number",
                "correct_answer": "5",
                "hints": ["Read where the line ends"],
                "explanation": "5 inches.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Object A is 7 inches. Object B is 4 inches. How much longer is A?",
                "expected_type": "number",
                "correct_answer": "3",
                "hints": ["7 - 4"],
                "explanation": "3 inches longer.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Measure this line with paper clips.",
                "type": "number",
                "correct_answer": "6",
                "target_concept": "nonstandard_measurement",
            },
            {
                "prompt": "Why is a ruler better than paper clips for measuring?",
                "type": "open_response",
                "rubric": "Mastery: rulers give same answer for everyone. Proficient: more accurate. Developing: cannot explain.",
                "target_concept": "standard_units",
            },
        ],
        "resource_guidance": {
            "required": ["paper clips", "ruler", "objects to measure"],
            "recommended": ["blocks", "measuring tape"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Hands-on measuring, not reading rulers. Nonstandard units first.",
            "adhd": "Measure everything. Scavenger hunt: find something 5 clips long.",
            "gifted": "Inches and centimeters. Half-inch. Unit conversion.",
            "visual_learner": "Bright rulers. Mark length with tape or stickers.",
            "kinesthetic_learner": "Body parts as units: hand spans, foot lengths.",
            "auditory_learner": "Narrate: 'The pencil reaches to 6. Six inches.'",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Measurement begins with comparison: which is longer? Then it asks how much longer, by laying a unit end to end. We start with nonstandard units, paper clips, so the child sees that a unit must be repeated with no gaps and no overlaps, and then we move to the ruler and standard inches.",
                "gradual_release": {
                    "i_do": "Model comparing two objects to see which is longer. Lay paper clips end to end along an object, with no gaps, counting the units. Then model the ruler: line the object up at the zero mark and read where it ends.",
                    "we_do": "Measure objects together with paper clips, then with blocks, and discuss why the same object gave two different numbers. Read the ruler together to the nearest inch.",
                    "you_do": "Child measures objects with nonstandard units and with a ruler to the nearest inch, compares two lengths, and tells how much longer one object is.",
                },
                "guided_practice": [
                    "Measure five objects with paper clips and record each length in a chart",
                    "Estimate a length, then measure it with a ruler to check",
                    "Compare two objects and find how much longer one is",
                ],
                "independent_practice": [
                    "Measure objects around the room with a ruler and record the results",
                    "A measuring scavenger hunt: find something about five units long",
                ],
                "mastery_check": [
                    "Measure with nonstandard units accurately, end to end with no gaps",
                    "Measure with a ruler to the nearest inch, starting at zero",
                    "Explain why standard units matter",
                ],
                "spiral_review": [
                    "Revisit direct comparison of two lengths before measuring with units again",
                ],
            },
            "classical": {
                "narrative_introduction": "To measure is to ask how many of a chosen unit fit along a thing. The rule is exact and worth keeping: lay the unit end to end, with no gaps and no overlaps, and count. Once that rule is sure, the ruler and its inches are simply a fixed unit kept ready.",
                "memory_work": {
                    "chants": [
                        "Chant the rule of measuring: lay the unit end to end, no gaps, no overlaps, then count",
                        "Chant the inch facts as they are met: twelve inches make one foot",
                    ],
                    "recitations": [
                        "Recite the rule of measuring, and recite that a unit must be the same each time or the count cannot be trusted",
                    ],
                },
                "copywork": [
                    "Copy a neat measurement record, each object beside its length, and copy the numbered marks of the ruler in order",
                ],
                "recitation_routine": "Begin each lesson by reciting the rule of measuring before any measuring is done; the rule is rehearsed cumulatively, never assumed.",
                "history_integration": "Tell that people once measured with the body, the cubit from elbow to fingertip, the span of a hand, the foot, and that the trouble of bodies differing led to fixed, standard units.",
                "read_aloud_suggestions": [
                    "A well-told story or account in which things are measured, and the old body-based measures appear",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A beautifully illustrated book about how things are measured and built, with real artwork and never a busy workbook",
                ],
                "short_lesson_flow": "Take a real question outdoors or around the home, how tall is the sunflower, how long is the table, and answer it together. Lay a chosen unit end to end, count carefully, and then try a ruler. Measure one or two real things, calmly, and stop while interest is high.",
                "narration_prompt": "Tell me how you measured it. What unit did you use, and how did you keep your measuring honest?",
                "real_world_objects": [
                    "A growing plant measured week by week",
                    "Furniture measured to see whether it will fit a space",
                    "The child's own height marked and measured",
                ],
                "nature_connection": "On a nature walk, measure a found thing, a leaf, a stick, a stone, and record its length with a small drawing in the nature notebook.",
                "habit_focus": "The habit of exactness: starting at the very end, laying each unit truly against the last, and reading the measure honestly.",
            },
            "montessori": {
                "prepared_materials": [
                    "The red rods, graded in length, for direct comparison and ordering",
                    "A child-sized ruler and measuring tape",
                    "Practical-life objects of many lengths to measure and order",
                ],
                "presentation": {
                    "three_period_lesson": "With the red rods: this is the longest; show me the longest; which rod is this? Then, with a ruler, name the units along its edge.",
                    "steps": [
                        "Order the red rods from shortest to longest and compare them directly",
                        "Lay a chosen unit end to end along an object and count the units",
                        "Measure the same object with the ruler and read its length in inches",
                    ],
                },
                "control_of_error": "The graded red rods fit together in only one true order, and a measuring laid with gaps or overlaps gives a count that does not match the ruler, so the error shows itself to the child.",
                "abstraction_pathway": "From comparing the red rods directly (length felt in the hand), to laying units end to end, toward reading a length from the ruler alone.",
                "extensions": [
                    "Measure many objects and order them by length",
                    "Measure with both inches and centimeters and compare the two units",
                ],
                "observation_focus": "Watch for the child laying units truly end to end and starting the ruler at zero, and for free, repeated measuring by choice.",
            },
            "unschooling": {
                "invitations": [
                    "Leave a ruler, a measuring tape, and paper clips within reach",
                    "Keep a height chart on the wall where the child can mark and measure",
                    "Set out building and cooking materials where measuring naturally arises",
                ],
                "real_world_contexts": [
                    "Measuring the child's own growing height",
                    "Measuring ingredients and pans while cooking and baking",
                    "Checking whether a piece of furniture or a toy will fit a space",
                    "Measuring for a building or craft project the child cares about",
                ],
                "conversation_starters": [
                    "How long do you think this is? How could we find out?",
                    "You measured with your hand and I measured with mine and we got different numbers. Why?",
                    "Which of these is longer, and how much longer?",
                ],
                "resource_bank": [
                    "A ruler and a measuring tape kept available",
                    "A wall height chart",
                    "Paper clips, blocks, and other things to measure with",
                ],
                "parent_role": "Measure things aloud as real questions arise, cooking, building, growing, and let the child measure alongside. Answer genuine questions about length and units, and let real projects do the teaching rather than a worksheet.",
                "observation_documentation": "Over time, note whether the child lays units end to end without gaps, reads a ruler from zero, compares two lengths, and understands why a unit must stay the same. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Reading numbers on rulers and tape measures",
            "science": "Measuring plant growth and object sizes",
            "history": "Historical measurements: cubits, spans",
        },
    },
    "mf-14": {
        "enriched": True,
        "learning_objectives": [
            "Compare weights by holding objects",
            "Use a balance scale to compare weights",
            "Measure weight using nonstandard units",
            "Understand: heavier, lighter, about the same",
        ],
        "teaching_guidance": {
            "introduction": "Weight is how heavy something is. Start with the child's hands as a balance: hold one object in each hand. Then use a real balance scale. Then measure: how many blocks balance the apple?",
            "scaffolding_sequence": [
                "Hold two objects, compare: which is heavier?",
                "Predict, then check with balance scale",
                "Order 3 objects lightest to heaviest",
                "Measure weight in nonstandard units",
                "Discover that bigger does not always mean heavier",
            ],
            "socratic_questions": [
                "Which is heavier: a big pillow or a small rock?",
                "If the balance tips left, which side is heavier?",
                "How many blocks balance this orange?",
            ],
            "practice_activities": [
                "Balance scale exploration with classroom objects",
                "Weight sorting: heavy, medium, light",
                "Estimation: predict blocks needed, then check",
            ],
            "real_world_connections": [
                "Weighing produce at the store",
                "Feeling backpack weight",
                "Comparing heavy and light toys",
            ],
            "common_misconceptions": [
                "Bigger always means heavier",
                "Confusing weight and size",
                "Not understanding balanced = equal weight",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Correctly compares weights with balance scale",
                "Uses vocabulary correctly",
                "Measures weight in nonstandard units",
            ],
            "assessment_methods": ["hands-on balance scale", "prediction and verification"],
            "sample_assessment_prompts": ["Which is heavier: apple or ball?", "How many blocks balance this eraser?"],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "A rock and cotton ball are on a balance. It tips toward the rock. Which is heavier?",
                "expected_type": "text",
                "correct_answer": "the rock",
                "hints": ["Heavier side goes down"],
                "explanation": "The rock. Heavier side tips down.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "A pencil balances with 3 blocks. A marker with 5 blocks. Which is heavier?",
                "expected_type": "text",
                "correct_answer": "the marker",
                "hints": ["More blocks = heavier"],
                "explanation": "The marker. 5 blocks > 3 blocks.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "A big balloon and small stone on a scale. Stone side goes down. Why?",
                "expected_type": "text",
                "hints": ["Is bigger always heavier?"],
                "explanation": "The stone is denser. Size doesn't determine weight.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Apple balances with 8 cubes. Orange with 6 cubes. How many more cubes does the apple weigh?",
                "expected_type": "number",
                "correct_answer": "2",
                "hints": ["8 - 6"],
                "explanation": "2 more cubes.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Use the balance to compare two objects. Which is heavier?",
                "type": "text",
                "rubric": "Mastery: uses scale correctly with vocabulary. Proficient: correct result. Developing: needs help.",
                "target_concept": "weight_comparison",
            },
            {
                "prompt": "Can a small object be heavier than a big one? Give an example.",
                "type": "open_response",
                "rubric": "Mastery: clear example and explanation. Proficient: gives example. Developing: says no.",
                "target_concept": "size_vs_weight",
            },
        ],
        "resource_guidance": {
            "required": ["balance scale", "various objects"],
            "recommended": ["uniform cubes for measuring"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Purely hands-on. No reading. Balance scale is naturally accessible.",
            "adhd": "Prediction games: which heavier? Guess then test. Surprise maintains engagement.",
            "gifted": "Grams and kilograms. Estimate before measuring. Calculate differences.",
            "visual_learner": "Clear balance scale showing which side goes down.",
            "kinesthetic_learner": "Hold objects in each hand. Feel the difference first.",
            "auditory_learner": "Narrate: 'Rock side DOWN. Rock is HEAVIER.'",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Weight is how heavy a thing is. We begin with the hands as a balance, holding one object in each, then move to a real balance scale, and then we measure: how many blocks balance the apple?",
                "gradual_release": {
                    "i_do": "Model holding two objects, one in each hand, to feel which is heavier. Model the balance scale, naming that the heavier side sinks. Then model measuring, counting the cubes that balance an object.",
                    "we_do": "Predict which object is heavier, then check it on the balance together. Order three objects from lightest to heaviest, and measure an object's weight in cubes together.",
                    "you_do": "Child compares weights on the balance, orders objects by weight, measures weight in nonstandard units, and uses the words heavier, lighter, and about the same correctly.",
                },
                "guided_practice": [
                    "Explore the balance scale with objects from around the room",
                    "Sort objects into heavy, medium, and light",
                    "Estimate how many cubes will balance an object, then check",
                ],
                "independent_practice": [
                    "Weigh several objects in cubes and record each weight",
                    "Predict-and-test games: guess the heavier object, then balance it",
                ],
                "mastery_check": [
                    "Compare two weights correctly with a balance scale",
                    "Use the words heavier, lighter, and about the same correctly",
                    "Measure an object's weight in nonstandard units",
                ],
                "spiral_review": [
                    "Revisit holding two objects to compare before measuring weight with units again",
                ],
            },
            "classical": {
                "narrative_introduction": "Weight is felt, not seen, and the eye is easily fooled, for a small thing may outweigh a large one. The balance is an old and honest instrument: it tells plainly the truth that the hand can only guess.",
                "memory_work": {
                    "chants": [
                        "Chant the words of weight, used exactly: heavier, lighter, balanced, about the same",
                    ],
                    "recitations": [
                        "Recite the rule of the balance: the heavier side sinks, and when the pans rest level the weights are equal",
                        "Recite that size is not weight: a large thing is not always the heavier one",
                    ],
                },
                "copywork": [
                    "Copy a neat weight record, each object beside the count of units that balanced it",
                ],
                "recitation_routine": "Begin each lesson by reciting the rule of the balance before any weighing is done; the rule is rehearsed cumulatively, never assumed.",
                "history_integration": "Tell that the balance is one of the oldest instruments people made, that they weighed goods against fixed stones and other set weights, and that the balance became an emblem of fair and honest judgment.",
                "read_aloud_suggestions": [
                    "A well-told story or account in which goods are weighed and the balance or its old weights appear",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 12,
                "living_book_suggestions": [
                    "A beautifully illustrated book in which things are weighed and the balance appears, with real artwork and never a busy workbook",
                ],
                "short_lesson_flow": "Bring out two real things. Let the child hold one in each hand and tell which feels heavier, then check the judgment on a balance scale. Weigh one or two pairs, calmly, and stop while interest is high.",
                "narration_prompt": "Tell me which object was heavier, and how the balance showed it to you.",
                "real_world_objects": [
                    "Rocks and pinecones gathered and weighed against each other",
                    "Produce held and compared, a potato against an apple",
                    "Heavy and light toys compared in the hands",
                ],
                "nature_connection": "On a nature walk, gather found things, weigh and order them on a balance, and discover that the largest is not always the heaviest; record the finding in the nature notebook.",
                "habit_focus": "The habit of honest judgment: trusting the balance and the feel of the hand over the eye's quick guess at size.",
            },
            "montessori": {
                "prepared_materials": [
                    "The baric tablets, graded by weight and told apart by the muscular sense, often with eyes closed",
                    "A child-sized balance scale",
                    "Uniform objects, such as cubes, for measuring weight",
                ],
                "presentation": {
                    "three_period_lesson": "With the baric tablets: this is the heaviest; show me the heaviest; which is this? Often judged with the eyes closed, by the feel in the hand.",
                    "steps": [
                        "Sort the baric tablets by weight using the muscular sense, with eyes closed",
                        "Predict which of two objects is heavier, then check the prediction on the balance",
                        "Count the uniform units that balance an object to measure its weight",
                    ],
                },
                "control_of_error": "The baric tablets are a fixed, graded set, and the balance shows equality plainly when its pans rest level, so a wrong judgment of weight reveals itself to the child.",
                "abstraction_pathway": "From feeling weight in the hand with the baric tablets, to the balance scale that shows it, toward measuring and comparing weight by a counted unit.",
                "extensions": [
                    "Weigh many objects and order them from lightest to heaviest",
                    "Measure weight with a uniform unit and compare the counts",
                ],
                "observation_focus": "Watch for the child trusting the balance and the muscular sense rather than the look of an object's size.",
            },
            "unschooling": {
                "invitations": [
                    "Leave a balance scale and an assortment of objects of varied weight within reach",
                    "Keep a kitchen scale accessible where cooking and weighing meet",
                    "Let a seesaw or balance toy be available for free play with weight",
                ],
                "real_world_contexts": [
                    "Weighing fruit and vegetables on the scale at the store",
                    "Feeling how heavy a backpack is when it is full",
                    "Comparing a heavy toy and a light one in the hands",
                    "Noticing how a seesaw tips toward the heavier rider",
                ],
                "conversation_starters": [
                    "Which of these do you think is heavier? How could we find out for sure?",
                    "The balance tipped down on one side. Which side is heavier?",
                    "Can a small thing be heavier than a big thing? Can you think of one?",
                ],
                "resource_bank": [
                    "A balance scale and a kitchen scale kept available",
                    "An assortment of objects of different weights",
                    "Picture books about weighing and balancing",
                ],
                "parent_role": "Notice weighing wherever it arises in real life, groceries, backpacks, cooking, and weigh alongside the child. Ask genuine heavier-and-lighter questions, and let the grocery scale and the seesaw do the teaching rather than a worksheet.",
                "observation_documentation": "Over time, note whether the child compares weights by hand and by balance, measures weight in units, uses the weight vocabulary, and understands that size does not decide weight. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Reading weight labels on packages",
            "science": "Weighing specimens in experiments",
            "history": "Historical weight units: stones, pounds, talents",
        },
    },
    "mf-15": {
        "enriched": True,
        "learning_objectives": [
            "Read analog clocks to the hour and half hour",
            "Read digital clocks",
            "Understand AM and PM",
            "Relate time to daily routines",
        ],
        "teaching_guidance": {
            "introduction": "Time tells us when things happen. Start with the child's daily routine: breakfast at 7, lunch at 12, bed at 8. Use a real analog clock with movable hands. The short hand tells the hour, the long hand tells the minutes.",
            "scaffolding_sequence": [
                "Learn the short hand points to the hour",
                "Practice reading o'clock times on analog clock",
                "Introduce half past: long hand on 6",
                "Connect analog to digital display",
                "Practice with daily schedule: what time do we eat lunch?",
            ],
            "socratic_questions": [
                "Which hand is the hour hand? How do you know?",
                "What does it mean when the long hand points to 12?",
                "What does it mean when the long hand points to 6?",
            ],
            "practice_activities": [
                "Set a play clock to match given times",
                "Draw hands on blank clock faces",
                "Match analog clocks to digital displays",
                "Create a daily schedule with clock drawings",
            ],
            "real_world_connections": [
                "What time do you wake up?",
                "What time is your favorite show?",
                "How long until dinner?",
            ],
            "common_misconceptions": [
                "Reading the minute hand as the hour",
                "Thinking 12:30 means 12 hours and 30 hours",
                "Not understanding that the hour hand moves between numbers",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Reads any o'clock and half-past time on analog clock",
                "Writes times in digital format",
                "Matches analog to digital correctly",
            ],
            "assessment_methods": ["clock reading", "clock setting", "time matching"],
            "sample_assessment_prompts": [
                "What time does this clock show?",
                "Set the clock to 3:30",
                "Write this time in digital form",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "The short hand points to 4 and the long hand points to 12. What time is it?",
                "expected_type": "text",
                "correct_answer": "4:00",
                "hints": ["Long hand on 12 means o'clock"],
                "explanation": "4:00. The hour hand on 4 and minute hand on 12 means 4 o'clock.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Write 'seven o'clock' in digital form.",
                "expected_type": "text",
                "correct_answer": "7:00",
                "hints": ["O'clock means :00"],
                "explanation": "7:00.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "The short hand is between 2 and 3, and the long hand points to 6. What time is it?",
                "expected_type": "text",
                "correct_answer": "2:30",
                "hints": ["Long hand on 6 means half past", "The hour hand is past 2 but not yet at 3"],
                "explanation": "2:30. Half past 2.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "You eat breakfast at 7:00 AM and lunch at 12:00 PM. How many hours between breakfast and lunch?",
                "expected_type": "number",
                "correct_answer": "5",
                "hints": ["Count from 7 to 12"],
                "explanation": "5 hours. Count: 8, 9, 10, 11, 12 = 5 hours.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "What time is shown when the short hand is on 9 and long hand on 12?",
                "type": "text",
                "correct_answer": "9:00",
                "target_concept": "reading_o_clock",
            },
            {
                "prompt": "What time is shown when the short hand is between 5 and 6, and the long hand is on 6?",
                "type": "text",
                "correct_answer": "5:30",
                "target_concept": "reading_half_past",
            },
            {
                "prompt": "Is 8:00 in the morning AM or PM?",
                "type": "text",
                "correct_answer": "AM",
                "target_concept": "am_pm",
            },
        ],
        "resource_guidance": {
            "required": ["analog clock with movable hands"],
            "recommended": ["digital clock for comparison", "daily schedule template"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Geared clock with color-coded hands. One concept at a time.",
            "adhd": "Connect to child's schedule: 'At 3:00 we have snack. Show me 3:00.'",
            "gifted": "Quarter hours, 5-minute intervals. Elapsed time problems.",
            "visual_learner": "Color hour and minute sides differently. Clock face templates.",
            "kinesthetic_learner": "Large play clock with moveable hands. Paper plate clocks.",
            "auditory_learner": "Say: 'Short hand THREE. Long hand TWELVE. THREE O'CLOCK.'",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Time tells us when things happen. On an analog clock the short hand points to the hour and the long hand tells the minutes. Today we read clocks to the hour and the half hour, read a digital clock, learn what AM and PM mean, and tie clock times to the routines of the day.",
                "gradual_release": {
                    "i_do": "Model with a clock that has movable hands: the short hand points to the hour; when the long hand points to twelve it is an o'clock time; when it points to six it is half past. Show the same time on a digital display.",
                    "we_do": "Read o'clock and half-past times together on the analog clock, and set the hands to match a time. Match an analog clock to its digital display together.",
                    "you_do": "Child reads o'clock and half-past times on an analog clock, reads a digital clock, tells AM from PM, and names what the family does at given times.",
                },
                "guided_practice": [
                    "Set a play clock to match a given time",
                    "Draw the hands on blank clock faces for o'clock and half-past times",
                    "Match analog clocks to their digital displays",
                ],
                "independent_practice": [
                    "Make a daily schedule with a small clock drawing beside each event",
                    "Read clocks around the home and name the time",
                ],
                "mastery_check": [
                    "Read any o'clock and half-past time on an analog clock",
                    "Read a digital clock and tell AM from PM",
                    "Relate a given time to a routine of the day",
                ],
                "spiral_review": [
                    "Revisit which hand is the hour hand before reading half-past times again",
                ],
            },
            "classical": {
                "narrative_introduction": "The clock is a small, faithful machine that marks the turning of the day. Its short hand keeps the hours and its long hand the minutes. Learn its few clear rules by heart, and the clock can be read at a glance.",
                "memory_work": {
                    "chants": [
                        "Chant the rule of the hands: the short hand tells the hour, the long hand tells the minutes",
                        "Chant the hours around the clock face in order, one through twelve",
                        "Chant the two marks: long hand on twelve is o'clock, long hand on six is half past",
                    ],
                    "recitations": [
                        "Recite the rules of the clock, and recite that the morning hours are AM and the afternoon and evening hours are PM",
                    ],
                },
                "copywork": [
                    "Copy the hours one through twelve as they sit around the clock face, and copy a few written times such as 7 o'clock and half past 8",
                ],
                "recitation_routine": "Begin each lesson by reciting the rules of the clock before reading any times; the rules are rehearsed cumulatively, never assumed.",
                "history_integration": "Tell that people once kept time by the sun and by water and sand glasses long before clocks with hands, and that the dividing of the day into hours is an old human ordering of time.",
                "read_aloud_suggestions": [
                    "A well-told story shaped by the hours of a day, or an account of how people have kept time",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 12,
                "living_book_suggestions": [
                    "A beautifully illustrated picture book that follows the hours of a day, with real artwork and never a busy workbook",
                ],
                "short_lesson_flow": "Sit with a real clock that has movable hands. Tie it to the rhythm the child already knows, breakfast time, lunch time, bedtime. Set the hands to one or two familiar times together, and read them. Stop while the child is still interested.",
                "narration_prompt": "Tell me what the clock looked like at lunch time today, and where each hand was pointing.",
                "real_world_objects": [
                    "The real clocks in the home, read at the moments of the day",
                    "A clock with movable hands set to familiar times",
                    "The family's daily rhythm of waking, meals, and rest",
                ],
                "nature_connection": "Notice the sun's place in the sky at different hours, and note in the nature notebook what time the morning birds sing or the shadows grow long.",
                "habit_focus": "The habit of punctuality and order: noticing the time and meeting the rhythm of the day faithfully.",
            },
            "montessori": {
                "prepared_materials": [
                    "A clock with movable hands, the hour hand and minute hand clearly different",
                    "Time cards pairing an analog clock face with its digital time",
                    "A picture schedule of the day's events with their times",
                ],
                "presentation": {
                    "three_period_lesson": "With the movable clock: this is three o'clock; show me three o'clock; what time is this? The hands set and read together.",
                    "steps": [
                        "Name the hour hand and the minute hand and what each one tells",
                        "Set the movable hands to o'clock and half-past times and read them",
                        "Match each analog clock card to its digital time, and place the day's events on the schedule",
                    ],
                },
                "control_of_error": "The time cards pair each analog clock with one digital time, so a wrong match is plain to the child, and the movable clock can be checked against a card.",
                "abstraction_pathway": "From setting and reading the movable clock by hand, to matching analog and digital faces, toward reading any clock in the room at a glance.",
                "extensions": [
                    "Follow the picture schedule through a real day",
                    "Read clocks and note the time of each work chosen during the day",
                ],
                "observation_focus": "Watch for the child telling the hour hand from the minute hand reliably, and reading time as part of the real day by choice.",
            },
            "unschooling": {
                "invitations": [
                    "Keep both an analog clock and a digital clock visible at child height",
                    "Leave a clock with movable hands and a play clock within reach",
                    "Let a timer be available for the child to set for things they care about",
                ],
                "real_world_contexts": [
                    "Reading the clock to know when a favorite show or activity begins",
                    "Noticing the time of waking, meals, and bedtime",
                    "Setting a timer for baking or for a turn",
                    "Counting how long until an awaited event",
                ],
                "conversation_starters": [
                    "It is almost time for your show. Can you find what the clock looks like now?",
                    "Which hand do you think tells the hour? How can you tell?",
                    "What time do you think we will have dinner?",
                ],
                "resource_bank": [
                    "An analog clock and a digital clock kept visible",
                    "A clock with movable hands and a play clock",
                    "A timer the child may set, and picture books that follow a day",
                ],
                "parent_role": "Read the time aloud through the day as it matters, before a show, before a meal, and let the child read the clock alongside you. Answer real questions about the hands and the hours, and let the rhythm of the day do the teaching.",
                "observation_documentation": "Over time, note whether the child reads o'clock and half-past times, reads a digital clock, tells AM from PM, and ties clock times to the events of the day. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Time words: morning, afternoon, evening in stories",
            "science": "Timing experiments: how long did it take?",
            "history": "Morning vs afternoon of a famous historical day",
        },
    },
    "mf-16": {
        "enriched": True,
        "learning_objectives": [
            "Identify penny, nickel, dime, and quarter",
            "Know the value of each coin",
            "Count collections of same-type coins",
            "Begin counting mixed coins",
        ],
        "teaching_guidance": {
            "introduction": "Coins are math you can hold. Start with real coins. A penny is 1 cent, a nickel is 5 cents, a dime is 10 cents, a quarter is 25 cents. The tricky part: a dime is smaller than a nickel but worth more. Size does not equal value.",
            "scaffolding_sequence": [
                "Identify each coin by sight and name",
                "Learn the value of each coin",
                "Count groups of same coins: 5 pennies = 5 cents",
                "Count nickels by 5s, dimes by 10s",
                "Begin counting simple mixed collections",
            ],
            "socratic_questions": [
                "Which coin is worth the most? Is it the biggest?",
                "If you have 3 dimes, how much money is that?",
                "Which would you rather have: 5 pennies or 1 nickel? Why?",
            ],
            "practice_activities": [
                "Sort real coins into groups",
                "Count collections of same coins",
                "Play store: price items at 5, 10, 15 cents",
                "Coin rubbings with labels",
            ],
            "real_world_connections": [
                "Paying for items at a store",
                "Saving coins in a piggy bank",
                "Making change at a lemonade stand",
            ],
            "common_misconceptions": [
                "Thinking bigger coins are always worth more",
                "Confusing nickel and dime values",
                "Counting mixed coins by ones instead of by value",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Names all 4 coins on sight",
                "States correct value for each",
                "Counts groups of same coins accurately",
            ],
            "assessment_methods": ["coin identification", "value recall", "counting practice"],
            "sample_assessment_prompts": [
                "Name this coin and tell me its value",
                "How much are 4 dimes worth?",
                "Count these nickels",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "How much is a nickel worth?",
                "expected_type": "number",
                "correct_answer": "5",
                "hints": ["It's the big coin that's worth 5"],
                "explanation": "A nickel is worth 5 cents.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "How much is a dime worth?",
                "expected_type": "number",
                "correct_answer": "10",
                "hints": ["The small silver coin"],
                "explanation": "A dime is worth 10 cents.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You have 3 dimes. How many cents?",
                "expected_type": "number",
                "correct_answer": "30",
                "hints": ["Count by 10s: 10, 20, 30"],
                "explanation": "3 dimes = 30 cents.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You have 6 nickels. How many cents?",
                "expected_type": "number",
                "correct_answer": "30",
                "hints": ["Count by 5s"],
                "explanation": "6 nickels = 30 cents.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Which is worth more: 7 pennies or 1 nickel?",
                "expected_type": "text",
                "correct_answer": "7 pennies",
                "hints": ["7 cents vs 5 cents"],
                "explanation": "7 pennies = 7 cents. 1 nickel = 5 cents. 7 > 5.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Name all 4 coins and their values.",
                "type": "text",
                "rubric": "Mastery: all 4 correct. Proficient: 3 correct. Developing: 1-2 correct.",
                "target_concept": "coin_identification",
            },
            {
                "prompt": "How much are 5 dimes worth?",
                "type": "number",
                "correct_answer": "50",
                "target_concept": "counting_coins",
            },
        ],
        "resource_guidance": {
            "required": ["real or play coins (penny, nickel, dime, quarter)"],
            "recommended": ["play store setup", "coin sorting tray"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Physical coin handling. Size and color as identifiers, not text.",
            "adhd": "Play store: price items, buy and sell. Real coins.",
            "gifted": "Mixed coins. Make change. How many ways to make 50 cents?",
            "visual_learner": "Coin posters with large images and values.",
            "kinesthetic_learner": "Handle real coins. Sort by size and feel. Coin rubbings.",
            "auditory_learner": "Chants: 'Penny one cent! Nickel five cents!'",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Coins are math you can hold. A penny is one cent, a nickel five cents, a dime ten cents, and a quarter twenty-five cents. The tricky part is that a dime is smaller than a nickel yet worth more: size does not equal value. Today we name the coins, learn their values, and count collections of them.",
                "gradual_release": {
                    "i_do": "Model naming each coin by sight and stating its value. Count a group of same coins aloud, nickels by fives and dimes by tens. Show plainly that a dime, though smaller than a nickel, is worth more.",
                    "we_do": "Sort real coins by type together, count a group of same coins, and begin counting a simple mixed collection together by starting with the most valuable coins.",
                    "you_do": "Child names all four coins on sight, states each value, counts collections of same coins, and begins counting simple mixed collections.",
                },
                "guided_practice": [
                    "Sort real coins into groups by type",
                    "Count groups of same coins, nickels by fives and dimes by tens",
                    "Play store: price items at five, ten, and fifteen cents and pay with coins",
                ],
                "independent_practice": [
                    "Count several collections of same coins and write each total",
                    "Begin counting simple mixed collections of two coin types",
                ],
                "mastery_check": [
                    "Name all four coins on sight and state each value",
                    "Count a collection of same coins correctly",
                    "Begin counting a simple mixed collection by value",
                ],
                "spiral_review": [
                    "Revisit skip counting by fives and tens, which underlies counting nickels and dimes",
                ],
            },
            "classical": {
                "narrative_introduction": "Each coin is a small token of an agreed worth. Four coins carry the everyday values, and their worths must simply be known by heart: a penny one, a nickel five, a dime ten, a quarter twenty-five. Once those are sure, money can be counted.",
                "memory_work": {
                    "chants": [
                        "Chant the coins and their values: penny one, nickel five, dime ten, quarter twenty-five",
                        "Chant by fives for the nickels and by tens for the dimes",
                    ],
                    "recitations": [
                        "Recite the four coin values, and recite the rule that the size of a coin does not tell its worth",
                    ],
                },
                "copywork": [
                    "Copy the names of the coins beside their values, neatly, so each coin and its worth are joined in the hand",
                ],
                "recitation_routine": "Begin each lesson by reciting the coins and their values before counting any money; the values are rehearsed cumulatively, never assumed.",
                "history_integration": "Tell that coins are very old, that people once traded goods directly before money was made, and that a coin's worth is a value agreed upon, not a thing of its size.",
                "read_aloud_suggestions": [
                    "A well-told story in which coins are earned, saved, and spent, read aloud for its language",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 12,
                "living_book_suggestions": [
                    "A beautifully illustrated picture book about earning, saving, and spending, with real artwork and never a busy workbook",
                ],
                "short_lesson_flow": "Bring out a handful of real coins. Look at them closely, name each, and learn its value. Count a small group of same coins together, calmly, for a real purpose, perhaps toward a small saving. Stop while interest is high.",
                "narration_prompt": "Tell me about the coins we counted. Which is worth the most, and is it the biggest?",
                "real_world_objects": [
                    "Real coins counted into a piggy bank toward a saving goal",
                    "Coins used to pay for a small item at a shop",
                    "Coins given as a gift or to someone in need",
                ],
                "nature_connection": "Take coins outdoors and make coin rubbings of leaves and bark, or count the coins needed for a small treat after a walk, noting it in the notebook.",
                "habit_focus": "The habit of careful handling and honest counting: knowing the worth of what one holds and counting it truly.",
            },
            "montessori": {
                "prepared_materials": [
                    "Real coins, penny, nickel, dime, and quarter, in a sorting tray",
                    "Coin value cards pairing each coin with its written worth",
                    "A practical-life shop or money box for real exchanges",
                ],
                "presentation": {
                    "three_period_lesson": "With the coins: this is a dime, worth ten cents; show me the dime; what is this coin, and what is it worth?",
                    "steps": [
                        "Name each coin and learn its value, handling the real coin",
                        "Sort the coins by type and count a group of one kind",
                        "Use the coins in a real exchange at the practical-life shop or money box",
                    ],
                },
                "control_of_error": "The coin value cards pair each coin with one worth, and a real exchange that does not balance shows the child plainly that a count was wrong.",
                "abstraction_pathway": "From handling and naming the real coins, to counting groups of one kind, toward counting a mixed collection by value with no cards.",
                "extensions": [
                    "Count mixed collections of coins by starting with the most valuable",
                    "Make change in the practical-life shop",
                ],
                "observation_focus": "Watch for the child counting coins by their value rather than by ones, and grasping that size does not decide worth.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a jar of real coins within reach for free sorting and counting",
                    "Set out a real or play cash register and a small shop of priced items",
                    "Leave a piggy bank or saving jar where the child can add and count coins",
                ],
                "real_world_contexts": [
                    "Paying for a small item at a real store",
                    "Saving coins toward something the child wants",
                    "Making change at a lemonade stand or pretend shop",
                    "Sorting and counting the coins found in pockets and couch cushions",
                ],
                "conversation_starters": [
                    "Which coin do you think is worth the most? Is it the biggest one?",
                    "If you have three dimes, how much money is that?",
                    "Would you rather have five pennies or one nickel? Why?",
                ],
                "resource_bank": [
                    "A jar of real coins kept available",
                    "A real or play cash register and a piggy bank",
                    "Picture books about money, saving, and shops",
                ],
                "parent_role": "Let the child handle real coins and real small purchases, count change aloud together, and follow their interest in saving for something they want. Answer genuine questions about coin values, and let real shopping do the teaching.",
                "observation_documentation": "Over time, note whether the child names the four coins and their values, counts groups of same coins, begins to count mixed collections by value, and understands that size does not decide worth. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Reading price tags and coin names",
            "science": "Coins as metals: properties of different metals",
            "history": "History of money: why coins exist",
        },
    },
    "mf-17": {
        "enriched": True,
        "learning_objectives": [
            "Identify circles, squares, rectangles, triangles, and hexagons",
            "Describe shapes by number of sides and vertices",
            "Find shapes in the real world",
            "Distinguish between 2D shapes and 3D objects",
        ],
        "teaching_guidance": {
            "introduction": "Shapes are everywhere. Start by looking: the clock is a circle, the door is a rectangle, the yield sign is a triangle. Then get precise: count sides and corners (vertices). A triangle has 3 sides and 3 corners.",
            "scaffolding_sequence": [
                "Identify circle, square, triangle in the environment",
                "Add rectangle and hexagon",
                "Count sides and vertices for each shape",
                "Sort shapes by number of sides",
                "Find shapes in nature and architecture",
                "Begin to distinguish flat (2D) from solid (3D)",
            ],
            "socratic_questions": [
                "How is a square different from a rectangle?",
                "How many sides does a triangle have? Can you draw one with different-length sides?",
                "Is a circle a shape with sides? Why or why not?",
            ],
            "practice_activities": [
                "Shape scavenger hunt around the house",
                "Build shapes with toothpicks and marshmallows",
                "Sort shapes by number of sides",
                "Create a shape collage from magazine cutouts",
            ],
            "real_world_connections": [
                "Stop sign is an octagon",
                "Pizza slices are triangles",
                "Wheels are circles",
                "Books are rectangles",
            ],
            "common_misconceptions": [
                "Thinking a shape must be a certain orientation",
                "Confusing square and rectangle (a square IS a rectangle)",
                "Thinking shapes must be regular",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Names 5 basic shapes on sight",
                "Describes each by sides and vertices",
                "Finds real-world examples of each shape",
            ],
            "assessment_methods": ["shape identification", "property description", "real-world scavenger hunt"],
            "sample_assessment_prompts": [
                "Name this shape and count its sides",
                "Find 3 circles in this room",
                "How are squares and rectangles alike and different?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "How many sides does a triangle have?",
                "expected_type": "number",
                "correct_answer": "3",
                "hints": ["Tri means three"],
                "explanation": "A triangle has 3 sides.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What shape has 4 equal sides and 4 corners?",
                "expected_type": "text",
                "correct_answer": "square",
                "hints": ["All sides the same length"],
                "explanation": "A square.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "How many sides does a hexagon have?",
                "expected_type": "number",
                "correct_answer": "6",
                "hints": ["Hex means six"],
                "explanation": "A hexagon has 6 sides.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Is a square a rectangle? Explain.",
                "expected_type": "text",
                "hints": ["A rectangle has 4 sides and 4 right angles. Does a square?"],
                "explanation": "Yes. A square is a special rectangle where all sides are equal.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Name 3 real-world objects shaped like circles.",
                "expected_type": "text",
                "hints": ["Look around: clocks, wheels, plates..."],
                "explanation": "Examples: clock face, wheel, plate, coin, pizza, frisbee.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Name this shape and tell me how many sides and corners.",
                "type": "text",
                "rubric": "Mastery: correct name, sides, and corners. Proficient: correct name and one property. Developing: names shape only.",
                "target_concept": "shape_properties",
            },
            {
                "prompt": "How is a rectangle different from a triangle?",
                "type": "open_response",
                "rubric": "Mastery: compares sides (4 vs 3) and corners. Proficient: notes different sides. Developing: vague.",
                "target_concept": "shape_comparison",
            },
        ],
        "resource_guidance": {
            "required": ["shape flashcards or cutouts"],
            "recommended": ["geoboards", "pattern blocks", "toothpicks and marshmallows"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Shape recognition is a visual strength. Hands-on exploration.",
            "adhd": "Shape scavenger hunt with movement. Build with sticks and clay.",
            "gifted": "3D shapes. Perimeter. Symmetry and tessellation.",
            "visual_learner": "Colorful posters. Pattern blocks. Symmetry with mirrors.",
            "kinesthetic_learner": "Build with toothpicks, pipe cleaners. Geoboard. Tangrams.",
            "auditory_learner": "Shape songs. Verbal property descriptions.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "A flat shape is two-dimensional: it has sides and corners but no thickness. Today we learn five shapes by name (circle, square, rectangle, triangle, hexagon), describe each by counting its sides and vertices (corners), find them in the world around us, and learn that a flat shape drawn on paper is not the same as a solid object you can hold.",
                "gradual_release": {
                    "i_do": "Hold up each shape, name it, and trace its sides and corners aloud: a triangle has three sides and three vertices. Show that a square turned on its corner is still a square, since orientation does not change a shape. Hold a flat paper circle beside a ball and name one flat and one solid.",
                    "we_do": "Sort shape cards by name together, count the sides and vertices of each, and sort a tray of objects into flat shapes and solid objects.",
                    "you_do": "Child names all five shapes on sight, states the sides and vertices of each, finds an example of each in the room, and tells whether an object is a flat shape or a solid.",
                },
                "guided_practice": [
                    "Sort shape cards by number of sides",
                    "Count the sides and vertices of each shape and write the numbers",
                    "Go on a shape scavenger hunt and name the shape of each object found",
                ],
                "independent_practice": [
                    "Draw and label each of the five shapes with its number of sides and vertices",
                    "Sort a set of objects into flat shapes and solid objects",
                ],
                "mastery_check": [
                    "Name all five shapes on sight regardless of their orientation",
                    "State the number of sides and vertices for each shape",
                    "Tell whether a given object is a flat shape or a solid object",
                ],
                "spiral_review": [
                    "Revisit counting to six, which underlies counting the sides and vertices of each shape",
                ],
            },
            "classical": {
                "narrative_introduction": "Long before there were numbers on a page, people saw shapes in the world and gave them names. The circle has no corner at all; the triangle has three; the square and rectangle have four; the hexagon has six. To know a shape is to know its name and to know how many sides and corners it carries.",
                "memory_work": {
                    "chants": [
                        "Chant the shapes and their sides: circle none, triangle three, square four, rectangle four, hexagon six",
                        "Chant the corners: a triangle three corners, a square four corners, a hexagon six corners",
                    ],
                    "recitations": [
                        "Recite the five shape names in order, and recite that a flat shape has sides and corners while a solid object has faces you can hold",
                    ],
                },
                "copywork": [
                    "Copy each shape's name beside its number of sides, neatly, so the name and the count are joined in the hand",
                ],
                "recitation_routine": "Begin each lesson by reciting the five shapes and their side counts before any new work; the shape names are rehearsed cumulatively.",
                "history_integration": "Tell that builders of long ago used these same shapes in arches, towers, and tiled floors, and that the study of shapes, geometry, is one of the oldest studies of all.",
                "read_aloud_suggestions": [
                    "A well-illustrated book that names shapes in the world, read aloud for its language and pictures",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 12,
                "living_book_suggestions": [
                    "A beautifully illustrated picture book that finds shapes in nature and architecture, with real artwork and never a worksheet",
                ],
                "short_lesson_flow": "Step outside or walk through the house with no rush. Look closely at one thing at a time: a round plate, a rectangular window, a triangular roof gable. Name the shape, count its sides and corners together, and notice whether it is flat or solid. Stop while the looking is still a pleasure.",
                "narration_prompt": "Tell me about the shapes you found today. Which one had no corners at all?",
                "real_world_objects": [
                    "A round clock face and a round plate",
                    "A rectangular door and a rectangular book",
                    "A triangular roof gable or sign",
                    "A hexagonal tile or pencil",
                ],
                "nature_connection": "Look for shapes in nature: the round face of a flower, the hexagon of a honeycomb cell, the triangle of a fir tree, and draw one carefully from life in the nature notebook.",
                "habit_focus": "The habit of attention: looking long enough at a real thing to see its true shape, its sides, and its corners.",
            },
            "montessori": {
                "prepared_materials": [
                    "The geometric cabinet with its framed shape insets",
                    "Shape cards in solid, thick-outline, and thin-outline forms for matching",
                    "A basket pairing flat shapes with solid objects, a circle card with a ball and a square card with a cube",
                ],
                "presentation": {
                    "three_period_lesson": "With the geometric cabinet insets: this is a triangle; show me the triangle; what is this shape?",
                    "steps": [
                        "Take an inset from the cabinet, feel its outline with two fingers, and name it",
                        "Trace each side and each corner with a finger while counting them",
                        "Match the inset to its shape card, then sort flat shape cards from solid objects",
                    ],
                },
                "control_of_error": "Each geometric cabinet inset fits only its own frame, so a wrong shape will not seat; the matching cards likewise pair one to one, showing the child any mistake without a word from the adult.",
                "abstraction_pathway": "From feeling the framed insets with the fingers, to matching them to thick-outline and then thin-outline cards, toward naming a flat shape on sight and telling it from a solid object.",
                "extensions": [
                    "Build shapes with the constructive triangles to see how shapes are composed",
                    "Find and name the shapes of objects throughout the room and home",
                    "Sort a collection into flat shapes and solid objects",
                ],
                "observation_focus": "Watch for the child tracing sides and corners with the finger, naming shapes regardless of orientation, and beginning to separate flat shapes from solid objects.",
            },
            "unschooling": {
                "invitations": [
                    "Leave out pattern blocks or shape tiles for free building",
                    "Set out a basket of household objects of varied shapes to handle and sort",
                    "Keep paper and a tray of round, square, and triangular things to trace",
                ],
                "real_world_contexts": [
                    "Naming the shapes of road signs, windows, and tiles while out and about",
                    "Noticing the shapes in a building's bricks, arches, and roof",
                    "Cutting food into shapes, a sandwich into triangles or rectangles",
                    "Spotting hexagons in a honeycomb or on a soccer ball",
                ],
                "conversation_starters": [
                    "What shape is that sign? How many sides does it have?",
                    "Is a circle a shape with corners? Why not?",
                    "This shape is flat on the paper, but this ball is not flat. How are they different?",
                ],
                "resource_bank": [
                    "Pattern blocks and shape tiles kept available",
                    "Picture books that find shapes in the world",
                    "Paper, scissors, and household objects of many shapes for tracing and sorting",
                ],
                "parent_role": "Name shapes as they come up in real life, on signs, in buildings, and in food, and wonder aloud about sides and corners. Follow the child's noticing rather than drilling, and let real objects show the difference between a flat shape and a solid thing.",
                "observation_documentation": "Over time, note whether the child names the five shapes, counts their sides and corners, finds them in the world, and tells a flat shape from a solid object. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Shape words as vocabulary",
            "science": "Shapes in nature: hexagons, circles, triangles",
            "history": "Geometry in ancient architecture: pyramids, arches",
        },
    },
    "mf-18": {
        "enriched": True,
        "learning_objectives": [
            "Identify repeating patterns",
            "Extend patterns by 3+ elements",
            "Create original patterns",
            "Recognize growing patterns",
        ],
        "teaching_guidance": {
            "introduction": "Patterns are the heartbeat of mathematics. Start with simple AB patterns using colors or shapes: red, blue, red, blue. What comes next? Then try ABC, ABB, and growing patterns (1, 2, 3, 4...).",
            "scaffolding_sequence": [
                "Identify AB patterns with objects",
                "Extend AB patterns by 3 elements",
                "Create ABC and ABB patterns",
                "Identify the pattern core (the part that repeats)",
                "Introduce growing number patterns: 2, 4, 6, 8",
            ],
            "socratic_questions": [
                "What is the part that keeps repeating?",
                "What comes next? How do you know?",
                "Can you make a pattern I haven't seen before?",
            ],
            "practice_activities": [
                "Build patterns with colored blocks",
                "Clap-snap patterns with sound",
                "Nature patterns: find patterns in leaves, flowers, pinecones",
            ],
            "real_world_connections": [
                "Patterns in music: verse, chorus, verse",
                "Day-night-day-night",
                "Stripes on clothing",
            ],
            "common_misconceptions": [
                "Thinking a pattern must be only 2 elements",
                "Not identifying the core unit",
                "Confusing random sequences with patterns",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Extends any repeating pattern correctly",
                "Creates original patterns",
                "Identifies the core of a pattern",
            ],
            "assessment_methods": ["pattern extension", "pattern creation", "core identification"],
            "sample_assessment_prompts": [
                "What comes next: circle, square, circle, square, __?",
                "Make your own pattern",
                "What is the repeating part?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What comes next: red, blue, red, blue, __?",
                "expected_type": "text",
                "correct_answer": "red",
                "hints": ["The pattern alternates"],
                "explanation": "Red. The pattern is AB repeating.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What comes next: 1, 2, 1, 2, 1, __?",
                "expected_type": "number",
                "correct_answer": "2",
                "hints": ["1, 2 keeps repeating"],
                "explanation": "2.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What comes next: circle, circle, square, circle, circle, square, __, __, __?",
                "expected_type": "text",
                "correct_answer": "circle, circle, square",
                "hints": ["The core is 3 items long"],
                "explanation": "Circle, circle, square. AAB pattern.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "What comes next: 2, 4, 6, 8, __?",
                "expected_type": "number",
                "correct_answer": "10",
                "hints": ["Each number is 2 more"],
                "explanation": "10. Growing pattern: add 2 each time.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Extend by 3: triangle, circle, triangle, circle, __, __, __",
                "type": "text",
                "correct_answer": "triangle, circle, triangle",
                "target_concept": "pattern_extension",
            },
            {
                "prompt": "Create your own pattern and explain the rule.",
                "type": "open_response",
                "rubric": "Mastery: pattern with stated rule. Proficient: creates pattern. Developing: random sequence.",
                "target_concept": "pattern_creation",
            },
        ],
        "resource_guidance": {"required": ["colored blocks or shapes"], "recommended": ["pattern block templates"]},
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Physical objects, not written symbols. Color and shape patterns.",
            "adhd": "Body patterns: clap-snap-stomp. Musical patterns. Frequent changes.",
            "gifted": "Growing patterns with rules. Function machines. Input-output.",
            "visual_learner": "Color patterns. Bead strings. Pattern block designs.",
            "kinesthetic_learner": "Block patterns. Body movement: jump-clap-jump-clap.",
            "auditory_learner": "Sound patterns: clap-snap. Musical rhythms.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "A pattern is something that repeats in a rule you can name. The part that repeats is the pattern's core: in red, blue, red, blue the core is red, blue. Today we identify a repeating pattern, find its core, extend it by three or more elements, create our own patterns, and meet growing patterns where the change increases each time, like two, four, six, eight.",
                "gradual_release": {
                    "i_do": "Build an AB pattern with colored blocks, name the core aloud, and extend it by three. Then build an ABC and an AAB pattern and name each core. Show a growing pattern, two, four, six, and say the rule: add two each time.",
                    "we_do": "Read a pattern together, point to and name its core, and extend it by three elements. Build a new pattern together and say its rule.",
                    "you_do": "Child identifies a repeating pattern, names its core, extends it by three or more, creates an original pattern with a stated rule, and recognizes a simple growing pattern.",
                },
                "guided_practice": [
                    "Extend AB, ABC, and AAB patterns by three elements",
                    "Point to and name the core of each pattern",
                    "Build a new pattern with blocks and say its rule",
                ],
                "independent_practice": [
                    "Extend several patterns by three elements and check each against its core",
                    "Create original patterns and write or say the rule for each",
                ],
                "mastery_check": [
                    "Extend any repeating pattern correctly by three or more elements",
                    "Name the core, the repeating part, of a pattern",
                    "Create an original pattern and recognize a simple growing pattern",
                ],
                "spiral_review": [
                    "Revisit skip counting by twos and fives, which are themselves growing patterns",
                ],
            },
            "classical": {
                "narrative_introduction": "The world keeps order, and order shows itself in patterns. Day follows night and night follows day; the seasons turn in the same circle every year. A pattern is a rule that repeats, and the part that repeats is its core. To find the core is to find the rule, and once the rule is known the pattern can be carried on.",
                "memory_work": {
                    "chants": [
                        "Chant a clapping pattern, clap clap snap, clap clap snap, until the core is sure",
                        "Chant a growing pattern by twos: two, four, six, eight, ten",
                    ],
                    "recitations": [
                        "Recite the rule of patterns: find the core, the part that repeats, and the pattern can be carried on",
                    ],
                },
                "copywork": [
                    "Copy a short pattern of letters or numbers neatly, then continue it for three more, so the hand follows the rule",
                ],
                "recitation_routine": "Begin each lesson by clapping or chanting a known pattern and naming its core before any new pattern is met.",
                "history_integration": "Tell that people have always read patterns in order to live well: the pattern of the seasons told them when to plant and harvest, and the pattern of the moon marked the months.",
                "read_aloud_suggestions": [
                    "A cumulative or repetitive tale whose words build in a pattern, read aloud so the ear hears the repeating rule",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A beautifully illustrated book whose pictures or words carry a clear repeating pattern, with real artwork and never a worksheet",
                ],
                "short_lesson_flow": "Bring out a basket of natural objects or colored beads. Make one simple pattern together, calmly, and let the child name what repeats. Extend it a little, then invite the child to make one of their own. Stop while the making is still a delight.",
                "narration_prompt": "Tell me about the pattern you made. What is the part that repeats?",
                "real_world_objects": [
                    "Colored beads threaded on a string",
                    "Pinecones, shells, and leaves laid in a pattern",
                    "Stripes and patterns on cloth or pottery",
                ],
                "nature_connection": "Look closely for the patterns nature makes: the spiral of a snail's shell, the rows of seeds in a sunflower, the petals around a flower's center, and draw one in the nature notebook.",
                "habit_focus": "The habit of observation: noticing the order and repetition that is already present in the world.",
            },
            "montessori": {
                "prepared_materials": [
                    "The colored bead bars and bead chains",
                    "Baskets of sortable objects, colored tiles, beads, and small natural items, for laying patterns",
                    "Pattern cards showing a core to copy and continue",
                ],
                "presentation": {
                    "three_period_lesson": "With a laid pattern: this is the core, the part that repeats; show me the core; what is this part of the pattern called?",
                    "steps": [
                        "Lay a simple AB pattern with the materials and read it aloud",
                        "Find and isolate the core, then extend the pattern by repeating the core",
                        "Create an original pattern and let a partner continue it",
                    ],
                },
                "control_of_error": "A pattern card shows the correct continuation, and the child sees plainly when a laid pattern no longer matches its core; the bead chains, repeating the same bar, make a break in the pattern visible at once.",
                "abstraction_pathway": "From laying and reading concrete object patterns, to isolating the core, toward seeing growing number patterns in the bead chains and continuing a pattern with no card.",
                "extensions": [
                    "Skip count along a bead chain to meet growing patterns",
                    "Make ABC and AAB patterns for another child to extend",
                    "Hunt for and record patterns found in the room and outdoors",
                ],
                "observation_focus": "Watch for the child isolating the core rather than copying element by element, and beginning to see the rule of a growing pattern.",
            },
            "unschooling": {
                "invitations": [
                    "Leave out colored beads, blocks, or tiles for free pattern making",
                    "Set out natural objects, stones, leaves, and shells, that invite sorting and arranging",
                    "Keep a drum or a pair of spoons nearby for making sound and rhythm patterns",
                ],
                "real_world_contexts": [
                    "Hearing the pattern in a favorite song, verse and chorus repeating",
                    "Noticing patterns in clothing stripes, tiled floors, and brick walls",
                    "Following the daily pattern of the routine and the weekly pattern of the days",
                    "Spotting patterns in nature on a walk, petals, pinecone spirals, animal stripes",
                ],
                "conversation_starters": [
                    "What part of this keeps repeating?",
                    "Can you guess what comes next? How did you know?",
                    "Can you make a pattern I have never seen before?",
                ],
                "resource_bank": [
                    "Colored beads, blocks, and tiles kept available",
                    "Music and instruments for rhythm patterns",
                    "Picture books and songs rich in repetition",
                ],
                "parent_role": "Notice patterns aloud as they appear in songs, on walks, and in the day's routine, and wonder together about what repeats and what comes next. Let the child make and break and remake patterns freely, following their own designs rather than a set exercise.",
                "observation_documentation": "Over time, note whether the child notices patterns, names the repeating core, extends patterns, invents original ones, and begins to see growing patterns. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Rhyming patterns in poetry",
            "science": "Patterns: seasons, day/night, life cycles",
            "history": "Historical patterns: rise and fall of civilizations",
        },
    },
    "mf-19": {
        "enriched": True,
        "learning_objectives": [
            "Use a number line to count forward and backward",
            "Use a number line to add and subtract",
            "Place numbers on a number line",
            "Compare numbers using a number line",
        ],
        "teaching_guidance": {
            "introduction": "A number line is a picture of numbers in order. Start with a physical number line on the floor: tape numbers 0-20 and have the child walk along it. Jump forward for addition, backward for subtraction.",
            "scaffolding_sequence": [
                "Walk a floor number line counting forward",
                "Walk backward on the number line",
                "Add: start at 5, jump 3 forward, land on 8",
                "Subtract: start at 9, jump 4 back, land on 5",
                "Place missing numbers on a partial line",
                "Compare: which is farther right?",
            ],
            "socratic_questions": [
                "Start at 6 and jump 4. Where do you land?",
                "Which number is farther from 0: 8 or 12?",
                "Are bigger numbers left or right?",
            ],
            "practice_activities": [
                "Floor number line walking",
                "Paper number line with hops drawn",
                "Place numbers on a blank line between two given numbers",
            ],
            "real_world_connections": [
                "Rulers are number lines",
                "Thermometers are vertical number lines",
                "Timelines are number lines",
            ],
            "common_misconceptions": [
                "Counting the starting number as a hop",
                "Thinking the number line ends",
                "Not spacing numbers evenly",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Uses number line to add and subtract within 20",
                "Places numbers correctly",
                "Uses number line to compare",
            ],
            "assessment_methods": ["number line addition", "number placement", "comparison"],
            "sample_assessment_prompts": ["Show 7+5 on a number line", "Where does 13 go between 10 and 20?"],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Start at 3. Jump forward 4. Where do you land?",
                "expected_type": "number",
                "correct_answer": "7",
                "hints": ["3, then count 4 jumps: 4,5,6,7"],
                "explanation": "7.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Start at 10. Jump back 3. Where?",
                "expected_type": "number",
                "correct_answer": "7",
                "hints": ["10, count back: 9,8,7"],
                "explanation": "7.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Where does 15 go between 10 and 20?",
                "expected_type": "text",
                "correct_answer": "exactly in the middle",
                "hints": ["15 is 5 from both 10 and 20"],
                "explanation": "Exactly in the middle.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Show 8 + 6 on a number line. Answer?",
                "expected_type": "number",
                "correct_answer": "14",
                "hints": ["Start at 8, hop 6 forward"],
                "explanation": "14.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Use a number line to solve 9 + 5.",
                "type": "number",
                "correct_answer": "14",
                "target_concept": "number_line_addition",
            },
            {
                "prompt": "Use a number line to solve 15 - 7.",
                "type": "number",
                "correct_answer": "8",
                "target_concept": "number_line_subtraction",
            },
            {
                "prompt": "Place 6, 14, 18 on a number line from 0 to 20.",
                "type": "open_response",
                "rubric": "Mastery: all correct with spacing. Proficient: correct order. Developing: order wrong.",
                "target_concept": "number_placement",
            },
        ],
        "resource_guidance": {"required": ["number line (floor or paper)"], "recommended": ["walk-on number line"]},
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Large clear lines with consistent spacing. Walking before paper.",
            "adhd": "Floor line with full-body hopping. Sidewalk chalk outside.",
            "gifted": "Negative numbers. Open number lines. Fraction placement.",
            "visual_learner": "Color-coded: even one color, odd another. Wall display.",
            "kinesthetic_learner": "Walk-on line. Jump forward add, backward subtract.",
            "auditory_learner": "Count aloud while pointing. Narrate hops.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "A number line is a picture of the numbers in order, evenly spaced, with bigger numbers to the right and smaller to the left. It turns counting, adding, subtracting, and comparing into movement: forward to add, backward to subtract. Today we count forward and backward on it, add and subtract with hops, place numbers in their right spots, and compare numbers by which sits farther right.",
                "gradual_release": {
                    "i_do": "Walk a floor number line, counting forward, then backward. Model addition: start on 5, hop 3 forward, land on 8, and say plainly that the starting number is not counted as a hop. Model subtraction by hopping back. Compare two numbers by naming which is farther right.",
                    "we_do": "Walk and hop the number line together: count forward and back, solve an addition and a subtraction by hopping, place a missing number between two marked ones, and compare two numbers.",
                    "you_do": "Child counts forward and backward on the line, adds and subtracts by hopping, places numbers correctly, and compares two numbers by position.",
                },
                "guided_practice": [
                    "Walk a floor number line counting forward and then backward",
                    "Add and subtract within twenty by hopping forward and back",
                    "Place missing numbers on a partly labeled line and compare two numbers",
                ],
                "independent_practice": [
                    "Solve addition and subtraction problems on a paper number line, drawing the hops",
                    "Place a set of numbers on a blank line from zero to twenty",
                ],
                "mastery_check": [
                    "Add and subtract within twenty using a number line, without counting the start as a hop",
                    "Place numbers in their correct, evenly spaced positions on a line",
                    "Compare two numbers by which is farther right on the line",
                ],
                "spiral_review": [
                    "Revisit counting forward and backward by ones, the movement the number line makes visible",
                ],
            },
            "classical": {
                "narrative_introduction": "Numbers have an order, and that order can be drawn as a straight road: each number a step along it, the small numbers behind, the large ahead. Once the road is drawn, every sum is a journey: to add is to walk forward, to subtract is to walk back. The number line makes the order of numbers something the eye can see and the foot can travel.",
                "memory_work": {
                    "chants": [
                        "Chant the rule of the line: forward to add, backward to subtract, and the bigger number lies to the right",
                        "Chant a count up and back along the line: nought, one, two, three, and back again",
                    ],
                    "recitations": [
                        "Recite that on the number line each step is the same size, and that the number you start on is not counted as a step",
                    ],
                },
                "copywork": [
                    "Draw a number line with evenly spaced marks and copy the numerals in order beneath them",
                ],
                "recitation_routine": "Begin each lesson by counting aloud up and down the line and reciting the rule of forward and backward before any new work.",
                "history_integration": "Tell that picturing numbers as points along a line is an old idea that joined counting to measuring, and that the ruler and the measuring tape are number lines put to work.",
                "read_aloud_suggestions": [
                    "A story of a journey told in steps or stages, read aloud so the child hears distance counted out like a number line",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A picture book that counts a journey or a climb step by step, with real artwork and never a workbook page",
                ],
                "short_lesson_flow": "Lay a number line along the floor or take up a real ruler or measuring tape. Walk it together, counting calmly. Take a few small hops forward to add, a few back to subtract, for a real purpose, perhaps measuring a length. Stop while the walking is still a pleasure.",
                "narration_prompt": "Tell me about the hops we took. When we hopped forward, did the number get bigger or smaller?",
                "real_world_objects": [
                    "A ruler and a measuring tape, which are number lines",
                    "A floor number line marked with tape or sidewalk chalk",
                    "A thermometer, a number line standing upright",
                ],
                "nature_connection": "Outdoors, use a measuring tape to measure the height of a sunflower or the length of a fallen branch, reading the number line that the tape is, and note it in the nature notebook.",
                "habit_focus": "The habit of accuracy: stepping evenly and counting truly, so each hop on the line is the same size.",
            },
            "montessori": {
                "prepared_materials": [
                    "A number line rug or long printed number line marked in even units",
                    "The colored bead chains, laid out straight to form a counted line",
                    "Number tickets to lay beside the line and a small marker the child moves along it",
                ],
                "presentation": {
                    "three_period_lesson": "With the number line: this point is twelve; show me twelve; what number is this point on the line?",
                    "steps": [
                        "Walk the eye and a finger along the number line, counting each evenly spaced point",
                        "Place a marker on a number, hop it forward to add, hop it back to subtract, counting the hops",
                        "Lay number tickets in their places on the line and compare two by their position",
                    ],
                },
                "control_of_error": "The bead chain beneath the line is the control: each hop counted on the line can be checked bead by bead against the chain, and a number ticket laid in the wrong place will not match the bead count there.",
                "abstraction_pathway": "From walking and hopping a concrete bead-chain line, to moving a marker on the printed number line, toward picturing the line in the mind and adding, subtracting, and comparing without it.",
                "extensions": [
                    "Use the longer bead chains to extend the line well past twenty",
                    "Skip count along the line in twos, fives, and tens",
                    "Find the difference between two numbers by counting the hops between them",
                ],
                "observation_focus": "Watch for the child keeping the hops even, not counting the starting number as a hop, and reading bigger numbers as lying to the right.",
            },
            "unschooling": {
                "invitations": [
                    "Mark a number line on the floor or driveway with tape or chalk for hopping games",
                    "Leave out a ruler, a measuring tape, and a tape-marked hopscotch grid",
                    "Keep a thermometer where the child can watch the number rise and fall",
                ],
                "real_world_contexts": [
                    "Hopping forward and back on a sidewalk hopscotch or chalk number line",
                    "Measuring things around the house with a ruler or tape measure",
                    "Watching a thermometer climb and drop with the weather",
                    "Reading the numbers count up on a clock, a stopwatch, or a flight of stairs",
                ],
                "conversation_starters": [
                    "If you stand on seven and hop forward three, where do you land?",
                    "Which number is farther along the line, eight or twelve?",
                    "When you hop backward, does the number get bigger or smaller?",
                ],
                "resource_bank": [
                    "A chalk or tape number line outdoors",
                    "Rulers, measuring tapes, and a thermometer kept available",
                    "Hopscotch and other hopping games",
                ],
                "parent_role": "Point out the number lines already in the child's world, the ruler, the tape measure, the thermometer, the marked stairs, and play hopping and measuring games when the child is keen. Wonder aloud about forward and backward hops, and let real measuring answer the questions.",
                "observation_documentation": "Over time, note whether the child counts forward and backward along a line, hops to add and subtract, places numbers in their right spots, and compares numbers by position. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Timelines as number lines for stories",
            "science": "Thermometers as vertical number lines",
            "history": "Timelines ARE number lines for events",
        },
    },
    "mf-20": {
        "enriched": True,
        "learning_objectives": [
            "Identify even and odd numbers",
            "Understand even numbers make two equal groups",
            "Understand odd numbers have 1 left over",
            "Recognize even/odd patterns",
        ],
        "teaching_guidance": {
            "introduction": "Even numbers split into two equal groups with nothing left. Odd numbers have one left over. Pair up objects: if every one has a partner, it's even. If one is alone, it's odd.",
            "scaffolding_sequence": [
                "Pair up objects: 6 makes 3 pairs (even), 7 has one left (odd)",
                "Sort numbers 1-10 into even and odd",
                "Connect to skip counting by 2s: 2,4,6,8,10 are even",
                "Extend to 1-20",
                "Discover: even numbers end in 0,2,4,6,8",
            ],
            "socratic_questions": [
                "Is 9 even or odd? Check with objects.",
                "What do all even numbers have in common at the ones digit?",
                "Add 1 to an even number. Even or odd?",
            ],
            "practice_activities": [
                "Pair up counters to test even/odd",
                "Color even numbers on hundred chart",
                "Sort number cards into even/odd piles",
            ],
            "real_world_connections": [
                "Pairing for buddy activities",
                "Sharing cookies evenly",
                "House numbers: even one side, odd the other",
            ],
            "common_misconceptions": [
                "Thinking 0 is not even (it is)",
                "Not connecting to ones digit for larger numbers",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Identifies any number 1-20 as even or odd",
                "Explains using pairing or ones digit",
                "Knows the pattern: even ends in 0,2,4,6,8",
            ],
            "assessment_methods": ["identification", "explanation", "pattern recognition"],
            "sample_assessment_prompts": ["Is 13 even or odd? How do you know?", "List all even numbers 1-20"],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Is 6 even or odd?",
                "expected_type": "text",
                "correct_answer": "even",
                "hints": ["Can 6 split into 2 equal groups?"],
                "explanation": "Even. 6 = 3 + 3.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Is 9 even or odd?",
                "expected_type": "text",
                "correct_answer": "odd",
                "hints": ["Pair 9 objects: one is left out"],
                "explanation": "Odd. 4 pairs + 1 left over.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "List all even numbers from 1 to 12.",
                "expected_type": "text",
                "correct_answer": "2, 4, 6, 8, 10, 12",
                "hints": ["Count by 2s"],
                "explanation": "2, 4, 6, 8, 10, 12.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Is 0 even or odd? Explain.",
                "expected_type": "text",
                "hints": ["Can 0 split into 2 equal groups?"],
                "explanation": "Even. 0 splits into two groups of 0. Also, 0 ends in 0, an even digit.",
            },
        ],
        "assessment_items": [
            {"prompt": "Is 14 even or odd?", "type": "text", "correct_answer": "even", "target_concept": "even_odd"},
            {"prompt": "Is 17 even or odd?", "type": "text", "correct_answer": "odd", "target_concept": "even_odd"},
            {
                "prompt": "How can you tell if a number is even by looking at it?",
                "type": "open_response",
                "rubric": "Mastery: check ones digit (0,2,4,6,8). Proficient: try pairing. Developing: no method.",
                "target_concept": "even_odd_rule",
            },
        ],
        "resource_guidance": {"required": ["counters for pairing"], "recommended": ["hundred chart"]},
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 10},
        "accommodations": {
            "dyslexia": "Physical pairing. No reading. Purely manipulative.",
            "adhd": "Grab objects, pair them, shout 'even!' or 'odd!' Quick and active.",
            "gifted": "Even+even=? Odd+odd=? Even+odd=? Discover and prove.",
            "visual_learner": "Two-color counters in pairs. Highlighted on chart.",
            "kinesthetic_learner": "Pair socks, shoes, gloves. Real objects.",
            "auditory_learner": "'2, 4, 6, 8, who do we appreciate? EVEN!'",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "An even number splits into two equal groups with nothing left over; an odd number always has one left over. The surest test is pairing: give each thing a partner, and if every thing has one the number is even, but if one stands alone the number is odd. Today we identify even and odd numbers, show why with pairing, and learn the pattern that even numbers end in zero, two, four, six, or eight.",
                "gradual_release": {
                    "i_do": "Take six counters and pair them: three pairs, none alone, so six is even. Take seven and pair them: one stands alone, so seven is odd. Then point along a count of numbers and show that even numbers end in zero, two, four, six, or eight.",
                    "we_do": "Pair counters together for several numbers, calling out even or odd, and sort number cards into an even pile and an odd pile.",
                    "you_do": "Child identifies a number as even or odd, shows why by pairing or by the ones digit, and names the even-number pattern.",
                },
                "guided_practice": [
                    "Pair counters to test whether numbers are even or odd",
                    "Sort number cards from one to twenty into even and odd piles",
                    "Color the even numbers on a hundred chart and see the pattern",
                ],
                "independent_practice": [
                    "Decide even or odd for a list of numbers and write the reason",
                    "List all the even numbers and all the odd numbers within twenty",
                ],
                "mastery_check": [
                    "Identify any number within twenty as even or odd",
                    "Explain the answer using pairing or the ones digit",
                    "State the pattern: even numbers end in zero, two, four, six, or eight",
                ],
                "spiral_review": [
                    "Revisit skip counting by twos, which lands on every even number in turn",
                ],
            },
            "classical": {
                "narrative_introduction": "Of every number it may be asked: can it be shared fairly between two? The numbers that can, that fall into two equal halves with nothing left over, the ancients called even; the numbers that leave one over they called odd. This is one of the oldest things known about number, and it is learned by the simple act of pairing.",
                "memory_work": {
                    "chants": [
                        "Chant the even numbers by twos: two, four, six, eight, ten, twelve",
                        "Chant the rule: even splits in two with none to spare, odd always leaves one standing there",
                    ],
                    "recitations": [
                        "Recite that an even number ends in zero, two, four, six, or eight, and an odd number ends in one, three, five, seven, or nine",
                    ],
                },
                "copywork": [
                    "Copy the even numbers in one row and the odd numbers in another, neatly, so the two patterns are seen side by side",
                ],
                "recitation_routine": "Begin each lesson by chanting the even numbers and reciting the rule of even and odd before any new work.",
                "history_integration": "Tell that the study of even and odd is among the oldest in arithmetic, that thinkers of old held it a first and important truth about every number, and that it begins the long study of how numbers are built.",
                "read_aloud_suggestions": [
                    "A story of fair sharing between two, read aloud so the child hears when a thing divides evenly and when one is left over",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A simple, beautifully illustrated counting or sharing book, with real artwork and never a workbook",
                ],
                "short_lesson_flow": "Bring out a small handful of real objects, perhaps acorns or buttons. Try to share them fairly between two, calmly, and see whether any is left over. Name the number even or odd. Try another small number. Stop while interest is high.",
                "narration_prompt": "Tell me what happened when we shared the seven acorns. Was there one left over? Even or odd?",
                "real_world_objects": [
                    "Acorns, buttons, or pebbles shared fairly between two",
                    "Pairs of socks, shoes, and gloves, which are even by nature",
                    "House numbers, even on one side of the street and odd on the other",
                ],
                "nature_connection": "Outdoors, notice where nature pairs and where it does not: the two wings of a butterfly, the petals counted around a flower, and ask whether the count is even or odd.",
                "habit_focus": "The habit of attention: noticing whether a thing shares out fairly or leaves one over.",
            },
            "montessori": {
                "prepared_materials": [
                    "The cards and counters material, numeral cards one to ten with loose counters",
                    "Baskets of small objects for free pairing",
                    "A box of number cards to sort into even and odd",
                ],
                "presentation": {
                    "three_period_lesson": "With the cards and counters: this number is even, see how every counter has a partner; show me a number that is even; is this number even or odd?",
                    "steps": [
                        "Lay the numeral cards in order and place counters beneath each, two by two in pairs",
                        "For each number run a finger up between the pairs: if it passes clear through the number is even, if a lone counter blocks it the number is odd",
                        "Sort the numbers into even and odd, and notice the pairs alternate",
                    ],
                },
                "control_of_error": "The counters themselves are the control: laid in pairs, an odd number always shows one counter with no partner, and the finger run between the columns is stopped by it, so the child sees even and odd without being told.",
                "abstraction_pathway": "From laying counters in pairs and feeling whether one is left over, to recognizing even and odd on sight, toward knowing a number by its ones digit alone.",
                "extensions": [
                    "Test numbers past ten by pairing larger collections",
                    "Investigate what happens when two even numbers, or two odd numbers, are joined",
                    "Find even and odd in the world: stairs, windows, house numbers",
                ],
                "observation_focus": "Watch for the child laying the counters truly in pairs and reading even or odd from the lone counter rather than guessing.",
            },
            "unschooling": {
                "invitations": [
                    "Keep baskets of small objects, buttons, beans, pebbles, within reach for free sorting and pairing",
                    "Leave out two small bowls inviting a child to share a handful fairly between them",
                    "Have a hundred chart or number chart on the wall to color and notice",
                ],
                "real_world_contexts": [
                    "Sharing snacks, grapes, or crackers fairly between two people",
                    "Pairing socks and shoes from the laundry",
                    "Noticing house numbers, even on one side of the street and odd on the other",
                    "Choosing teams or partners and finding whether everyone has a buddy",
                ],
                "conversation_starters": [
                    "If we share these grapes between the two of us, will it come out fair, or is one left over?",
                    "Does everyone here have a partner, or is someone left out?",
                    "What do you notice about the numbers on this side of the street?",
                ],
                "resource_bank": [
                    "Baskets of small countable objects kept available",
                    "A hundred chart or number chart",
                    "Everyday sharing moments: snacks, toys, teams",
                ],
                "parent_role": "Let the everyday business of sharing fairly and pairing things up raise the question of even and odd, and wonder aloud about whether a number comes out fair. Follow the child's noticing of patterns rather than drilling, and let real handfuls of objects do the showing.",
                "observation_documentation": "Over time, note whether the child tells even from odd, shows why by pairing or sharing, and notices the pattern of even numbers. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Even/odd page numbers (left vs right)",
            "science": "Symmetry: even numbers of legs, wings",
            "history": "Roman numerals: which even, which odd?",
        },
    },
    "mf-21": {
        "enriched": True,
        "learning_objectives": [
            "Understand halves and quarters as equal parts of a whole",
            "Divide shapes and objects into halves and quarters",
            "Recognize that fractions mean equal parts",
            "Use words: half, quarter, whole, equal parts",
        ],
        "teaching_guidance": {
            "introduction": "Fractions start with sharing. If you have one cookie and two children, how do you share fairly? Cut it in half. Each child gets one half. The key word is EQUAL: the parts must be the same size.",
            "scaffolding_sequence": [
                "Fold paper in half: two equal parts",
                "Fold paper into quarters: four equal parts",
                "Identify halves and quarters in pictures",
                "Divide real objects: cut a sandwich in half, an apple in quarters",
                "Recognize that unequal parts are NOT fractions",
            ],
            "socratic_questions": [
                "If I cut this in two pieces but they're different sizes, is that half?",
                "How many quarters make a whole?",
                "Which is bigger: one half or one quarter?",
            ],
            "practice_activities": [
                "Fold and cut paper into halves and quarters",
                "Color half or a quarter of shapes",
                "Share food fairly: divide crackers, fruit",
            ],
            "real_world_connections": [
                "Half an hour = 30 minutes",
                "A quarter of a dollar = 25 cents",
                "Pizza slices as fractions",
            ],
            "common_misconceptions": [
                "Thinking any two pieces are halves even if unequal",
                "Not realizing a quarter is smaller than a half",
                "Thinking fractions only apply to circles",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Divides shapes into equal halves and quarters",
                "Identifies whether parts are equal",
                "Knows 2 halves = 1 whole, 4 quarters = 1 whole",
            ],
            "assessment_methods": ["folding and cutting", "shape division", "oral explanation"],
            "sample_assessment_prompts": [
                "Fold this paper into quarters",
                "Is this shape divided into equal halves?",
                "How many quarters make a whole?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "How many equal parts are in a half?",
                "expected_type": "number",
                "correct_answer": "2",
                "hints": ["Half means 2 equal pieces"],
                "explanation": "A half means the whole is divided into 2 equal parts.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "How many quarters make a whole?",
                "expected_type": "number",
                "correct_answer": "4",
                "hints": ["Quarter means 4 equal pieces"],
                "explanation": "4 quarters make a whole.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Which is bigger: one half of a pizza or one quarter of the same pizza?",
                "expected_type": "text",
                "correct_answer": "one half",
                "hints": ["Half = 2 pieces, quarter = 4 pieces. Which pieces are bigger?"],
                "explanation": "One half. Cutting into fewer pieces makes bigger pieces.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "A rectangle is cut into 4 pieces. Two pieces are big and two are small. Are these quarters? Why or why not?",
                "expected_type": "text",
                "hints": ["Quarters must be equal"],
                "explanation": "No. Quarters must be 4 EQUAL parts. If they're different sizes, they're not quarters.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Draw a circle divided into equal halves.",
                "type": "open_response",
                "rubric": "Mastery: line through center creating 2 equal parts. Proficient: approximately equal. Developing: clearly unequal.",
                "target_concept": "halves",
            },
            {
                "prompt": "How many halves make a whole?",
                "type": "number",
                "correct_answer": "2",
                "target_concept": "whole_from_halves",
            },
        ],
        "resource_guidance": {
            "required": ["paper for folding", "scissors"],
            "recommended": ["fraction circles", "play food for sharing"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "No fraction notation. Only words (half, quarter) and physical folding/cutting.",
            "adhd": "Cut real food: sandwiches, apples, pizza. Eat the fractions.",
            "gifted": "Thirds, sixths, eighths. Compare: which bigger, 1/2 or 1/4?",
            "visual_learner": "Fraction circles and bars, color coded. Fold and shade.",
            "kinesthetic_learner": "Fold paper. Cut playdough. Break crackers. Physical division.",
            "auditory_learner": "Narrate: 'Folding in HALF. TWO EQUAL parts. Each ONE HALF.'",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "A fraction is an equal part of a whole. When a whole is split into two equal parts, each part is one half; into four equal parts, each is one quarter. The word that matters most is equal: if the parts are not the same size, they are not halves or quarters at all. Today we divide shapes and objects into halves and quarters, use the words half, quarter, whole, and equal parts, and learn that two halves and four quarters each make one whole.",
                "gradual_release": {
                    "i_do": "Fold a sheet of paper exactly in half, matching the edges, and name the two equal parts halves. Fold it again into four equal parts and name them quarters. Show plainly that two pieces of different sizes are not halves: the parts must be equal.",
                    "we_do": "Fold and cut paper into halves and then quarters together, naming the parts, and check by laying the pieces on each other that they are equal.",
                    "you_do": "Child folds or cuts a whole into equal halves and quarters, names the parts with the right words, and tells whether given parts are equal.",
                },
                "guided_practice": [
                    "Fold paper into halves, then into quarters, matching the edges so the parts are equal",
                    "Color one half, then one quarter, of simple shapes",
                    "Sort pictures into shapes split into equal parts and shapes split into unequal parts",
                ],
                "independent_practice": [
                    "Divide real objects into halves and quarters: a sandwich, an apple, a cracker",
                    "Draw a shape and split it into equal halves, and another into equal quarters",
                ],
                "mastery_check": [
                    "Divide a shape or object into equal halves and into equal quarters",
                    "Tell whether parts are truly equal, and so whether they are halves or quarters",
                    "State that two halves make one whole and four quarters make one whole",
                ],
                "spiral_review": [
                    "Revisit fair sharing, splitting a set of objects equally, the same equal-parts idea applied to numbers",
                ],
            },
            "classical": {
                "narrative_introduction": "A whole thing may be broken into parts, but only when the parts are equal does the breaking give a fraction. Cut a loaf in two equal pieces and each is a half; cut it in four equal pieces and each is a quarter. The fraction is the language of fair division: it answers the old question of how to share a whole so that each share is just.",
                "memory_work": {
                    "chants": [
                        "Chant the parts: two equal parts are halves, four equal parts are quarters",
                        "Chant the wholes: two halves make a whole, four quarters make a whole",
                    ],
                    "recitations": [
                        "Recite the rule of fractions: the parts must be equal, or they are no fraction at all",
                    ],
                },
                "copywork": [
                    "Copy the fraction words, whole, half, quarter, and equal parts, neatly, beside a drawing of each",
                ],
                "recitation_routine": "Begin each lesson by reciting the fraction words and the rule of equal parts before any new folding or cutting.",
                "history_integration": "Tell that fractions arose from the everyday need to divide things fairly, land, bread, and grain, and that for as long as people have shared, they have needed the language of halves and quarters.",
                "read_aloud_suggestions": [
                    "A story in which something is shared or divided fairly, read aloud so the child hears the question of equal parts",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 12,
                "living_book_suggestions": [
                    "A beautifully illustrated picture book about sharing or about cooking, with real artwork and never a worksheet",
                ],
                "short_lesson_flow": "At a real moment of sharing, perhaps an apple or a sandwich at snack time, cut it together into two equal parts and name them halves. Another day, cut into quarters. Let the child do the cutting and the naming, calmly, for a real purpose. Stop while interest is high.",
                "narration_prompt": "Tell me how we shared the apple. How many equal parts did we make? What is each part called?",
                "real_world_objects": [
                    "An apple, a sandwich, or an orange cut into halves and quarters at a real meal",
                    "Folded paper or cloth divided into equal parts",
                    "A clock face, whose half hour and quarter hour the child may begin to notice",
                ],
                "nature_connection": "Outdoors, notice the halves nature makes: a leaf with its two matching sides about the midrib, a seed split in two, and wonder whether the halves are truly equal.",
                "habit_focus": "The habit of fair dealing: dividing a whole so that each part is honestly equal.",
            },
            "montessori": {
                "prepared_materials": [
                    "The fraction circles, a whole and its halves and quarters as inset pieces",
                    "The fraction skittles for halving and quartering",
                    "Real objects to fold and cut: paper, and food at snack time",
                ],
                "presentation": {
                    "three_period_lesson": "With the fraction circle pieces: this is one half, two of these fill the whole; show me one half; what is this piece called?",
                    "steps": [
                        "Lift the whole circle, then the two halves, then the four quarters from their frames, naming each",
                        "Fit the halves and then the quarters back into the whole, seeing that they fill it exactly",
                        "Fold and cut paper, or share real food, into equal halves and quarters",
                    ],
                },
                "control_of_error": "The fraction inset is the control: only equal pieces will fit the frame and fill the whole, so a piece cut or chosen unequal will not seat, showing the child plainly that the parts must be equal.",
                "abstraction_pathway": "From handling the equal inset pieces and fitting them into the whole, to folding and cutting real objects into equal parts, toward naming halves and quarters and knowing how many make a whole without the material.",
                "extensions": [
                    "Divide the fraction circles into thirds, sixths, and eighths",
                    "Compare the pieces: see that a half is larger than a quarter",
                    "Find halves and quarters in the day: half an hour, a quarter of a dollar",
                ],
                "observation_focus": "Watch for the child insisting on equal parts, naming halves and quarters with the right words, and noticing that more parts means smaller parts.",
            },
            "unschooling": {
                "invitations": [
                    "Let the child do real cutting and sharing at snack and meal times",
                    "Leave out paper for folding and play dough for dividing",
                    "Keep play food that comes apart into halves and quarters within reach",
                ],
                "real_world_contexts": [
                    "Cutting a sandwich, a pizza, or an apple to share fairly",
                    "Halving a recipe, or measuring half a cup and a quarter cup while cooking",
                    "Sharing a treat equally between friends or siblings",
                    "Noticing the half hour and quarter hour on a clock, and the quarter in a handful of coins",
                ],
                "conversation_starters": [
                    "If we cut this in two so it is fair, what do we call each piece?",
                    "Which would you rather have, half of the cookie or a quarter of it? Why?",
                    "How many quarters do you think it takes to make the whole thing?",
                ],
                "resource_bank": [
                    "Real food and a child-safe knife for sharing",
                    "Paper, play dough, and play food that divides",
                    "A measuring cup set used in real cooking",
                ],
                "parent_role": "Hand the child the real job of cutting and sharing fairly, and use the words half, quarter, and equal parts as it naturally comes up at meals and in cooking. Wonder aloud about whether a cut is fair, and let real sharing, where unfair parts are quickly noticed, do the teaching.",
                "observation_documentation": "Over time, note whether the child divides wholes into equal halves and quarters, uses the fraction words, insists that parts be equal, and knows how many parts make a whole. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Half-hour in time. 'Half' as vocabulary.",
            "science": "Dividing specimens for observation",
            "history": "Dividing land and territories",
        },
    },
    "mf-22": {
        "enriched": True,
        "learning_objectives": [
            "Collect data by counting and tallying",
            "Organize data in tally charts",
            "Read and interpret tally charts",
            "Answer questions about data",
        ],
        "teaching_guidance": {
            "introduction": "Data is information we collect to answer a question. How many of each color are in this bag of candy? Count them, make tally marks, and organize the information so we can see patterns and answer questions.",
            "scaffolding_sequence": [
                "Practice making tally marks: groups of 5 with a diagonal cross",
                "Collect data: count items and record with tallies",
                "Organize tallies into a chart with categories",
                "Read a tally chart and answer questions about it",
                "Compare categories: which has the most? Least? How many more?",
            ],
            "socratic_questions": [
                "Which group has the most? How can you tell from the tallies?",
                "How many more red than blue? How did you figure that out?",
                "What question could you answer with this data?",
            ],
            "practice_activities": [
                "Survey classmates or family: favorite color, animal, or food",
                "Count items in a collection and make a tally chart",
                "Weather tallies: track sunny, cloudy, rainy days for a week",
            ],
            "real_world_connections": [
                "Voting and counting votes",
                "Tracking weather over a month",
                "Counting types of animals seen on a nature walk",
            ],
            "common_misconceptions": [
                "Making 6th tally mark wrong (should start new group after 5)",
                "Counting tallies by ones instead of by fives",
                "Not keeping categories clearly separated",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Makes correct tally marks in groups of 5",
                "Creates a tally chart from collected data",
                "Answers comparison questions from a chart",
            ],
            "assessment_methods": ["tally chart creation", "chart reading", "comparison questions"],
            "sample_assessment_prompts": [
                "Make a tally chart of these items",
                "How many more cats than dogs?",
                "Which has the fewest?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "You see 7 birds. Draw tally marks for 7.",
                "expected_type": "text",
                "correct_answer": "IIII II",
                "hints": ["Group of 5 with cross, then 2 more"],
                "explanation": "7 = one group of 5 plus 2 more lines.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "A tally chart shows: Cats IIII III, Dogs IIII I. How many more cats than dogs?",
                "expected_type": "number",
                "correct_answer": "2",
                "hints": ["Cats = 8, Dogs = 6. Subtract."],
                "explanation": "Cats = 8, Dogs = 6. 8 - 6 = 2 more cats.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You counted 12 red beads. How many tally groups of 5 and how many extras?",
                "expected_type": "text",
                "correct_answer": "2 groups and 2 extras",
                "hints": ["12 divided into groups of 5"],
                "explanation": "2 groups of 5 = 10, plus 2 more = 12.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Make a tally chart: 5 apples, 8 bananas, 3 oranges. Which fruit has the most?",
                "expected_type": "text",
                "correct_answer": "bananas",
                "hints": ["8 is the largest number"],
                "explanation": "Bananas (8) have the most.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Create a tally chart for: 6 red, 9 blue, 4 green.",
                "type": "open_response",
                "rubric": "Mastery: correct tallies with groups of 5, clear categories. Proficient: correct counts, messy format. Developing: incorrect tallies.",
                "target_concept": "tally_chart_creation",
            },
            {
                "prompt": "From the chart, how many more blue than green?",
                "type": "number",
                "correct_answer": "5",
                "target_concept": "data_comparison",
            },
        ],
        "resource_guidance": {
            "required": ["paper and pencil for tallying"],
            "recommended": ["collections to sort and count", "chart paper"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Tally marks are non-reading. Highly accessible. Count by fives.",
            "adhd": "Data about things they care about: snacks, pet behaviors, weather.",
            "gifted": "Bar graphs, pictographs. Own survey questions. Analyze results.",
            "visual_learner": "Color-coded charts. Large chart paper. Sticky note graphs.",
            "kinesthetic_learner": "Craft sticks bundled in fives as physical tallies.",
            "auditory_learner": "Count aloud by fives: 'Five, ten, fifteen, and two is seventeen.'",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Data is information we collect to answer a question. To find out how many of each kind there are, we count and keep a tally, marking each in groups of five, four marks and a fifth struck across. Then we organize the tallies into a chart by category. Today we collect data with tallies, build a tally chart, read it, and answer questions like which has the most and how many more.",
                "gradual_release": {
                    "i_do": "Pose a question, then count a collection, making a tally mark for each, gathering them into groups of five. Show plainly that the sixth mark begins a new group. Organize the tallies into a chart by category, then read it aloud and answer: which has the most, and how many more.",
                    "we_do": "Count and tally a collection together, organize the marks into a chart with clear categories, count the tallies by fives, and answer comparison questions from the chart.",
                    "you_do": "Child collects data by counting and tallying in groups of five, builds a tally chart, reads it, and answers questions about the data.",
                },
                "guided_practice": [
                    "Make tally marks in groups of five for given counts",
                    "Count a collection and record it in a tally chart by category",
                    "Read a tally chart and answer which has the most, the least, and how many more",
                ],
                "independent_practice": [
                    "Survey the family on a question and build a tally chart of the answers",
                    "Read a finished tally chart and write the answers to questions about it",
                ],
                "mastery_check": [
                    "Make correct tally marks, in groups of five, for a count",
                    "Build a tally chart from collected data with clear categories",
                    "Read a tally chart and answer comparison questions about it",
                ],
                "spiral_review": [
                    "Revisit skip counting by fives, used to total the tally groups quickly",
                ],
            },
            "classical": {
                "narrative_introduction": "When a thing must be counted, the mind soon needs help to keep its place. The tally is that help: one mark for each, gathered four together and a fifth struck across, so the eye can read fives at a glance. Set the tallies in order by kind, and a plain chart is made, and from the chart the truth of the count can be read and questioned.",
                "memory_work": {
                    "chants": [
                        "Chant the tally: one, two, three, four, and the fifth strikes across to close the group",
                        "Count a chart of tallies aloud by fives: five, ten, fifteen, and the ones that are left",
                    ],
                    "recitations": [
                        "Recite the rule of the tally: gather the marks in fives, keep each kind apart, and the count is easily read",
                    ],
                },
                "copywork": [
                    "Copy a small tally chart neatly, the categories named and the tally marks ruled in even groups of five",
                ],
                "recitation_routine": "Begin each lesson by chanting the count of a tally group by fives and reciting the rule of the tally before any new collecting.",
                "history_integration": "Tell that the tally is one of the oldest of all records, that people kept counts by scratching marks on bone, wood, and stone long before numerals were written, and that counting heads and goods, the census, is among the oldest uses of number.",
                "read_aloud_suggestions": [
                    "A story or true account in which something is counted up and recorded, read aloud so the child hears a count being kept",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A beautifully illustrated book about birds, weather, or the seasons that invites the child to count and notice, never a workbook",
                ],
                "short_lesson_flow": "Choose a real question worth answering, perhaps the birds at the window or the weather each day. Watch, and keep a tally calmly as things are observed. After some days, look at the tallies together, count them by fives, and see what the gathered marks tell. Stop while interest is fresh.",
                "narration_prompt": "Tell me what our tally chart shows. Which kind did we see the most, and how do you know?",
                "real_world_objects": [
                    "Real coins, buttons, or shells counted and tallied",
                    "A bird feeder or window where birds may be watched and tallied",
                    "A simple weather record kept day by day with tally marks",
                ],
                "nature_connection": "On a nature walk, keep a tally of what is seen, the birds, the kinds of tree, the colors of leaf, and bring the count home to the nature notebook to read together.",
                "habit_focus": "The habit of careful observation: watching truly and recording each thing honestly, one mark at a time.",
            },
            "montessori": {
                "prepared_materials": [
                    "Baskets of sortable objects, beads, counters, small natural items, to count and tally",
                    "Tally cards or strips for recording marks in groups of five",
                    "A simple category chart the child fills and reads",
                    "A daily weather chart the child keeps over time",
                ],
                "presentation": {
                    "three_period_lesson": "With a tally group: this is a group of five, four marks and one struck across; show me a group of five; how many is this group?",
                    "steps": [
                        "Choose a question and sort a collection into its categories",
                        "Count each category, making a tally mark for each and gathering them into groups of five",
                        "Set the tallies into the chart by category, count them by fives, and read the chart to answer questions",
                    ],
                },
                "control_of_error": "The objects themselves are the control: the tally marks for a category can be checked back against the counted objects, and a recount that does not match the chart shows the child plainly where the error lies.",
                "abstraction_pathway": "From counting concrete objects one by one, to recording each as a tally mark gathered in fives, toward reading a finished chart and answering its questions without recounting.",
                "extensions": [
                    "Keep a weather tally over a month and read the gathered result",
                    "Survey the family or friends on a question and chart the answers",
                    "Carry the tally chart on toward a simple bar graph or pictograph",
                ],
                "observation_focus": "Watch for the child closing each group at the fifth mark, keeping the categories apart, and reading the chart by fives rather than recounting by ones.",
            },
            "unschooling": {
                "invitations": [
                    "Keep paper and pencil handy for tallying whatever the child wants to count",
                    "Put up a wall chart for tracking something real, the weather, birds, or daily reading",
                    "Leave out collections, buttons, coins, cards, that invite sorting and counting",
                ],
                "real_world_contexts": [
                    "Tallying the birds, cars, or dogs seen on a walk or a drive",
                    "Keeping a weather chart through a week or a month",
                    "Counting votes when the family decides something together",
                    "Sorting and counting a collection: rocks, cards, toy animals",
                ],
                "conversation_starters": [
                    "How could we keep count of all of these without losing our place?",
                    "Which one did we see the most of? How can you tell from the marks?",
                    "How many more sunny days than rainy days were there?",
                ],
                "resource_bank": [
                    "Paper, pencils, and a wall chart kept available",
                    "Collections of things to sort and count",
                    "Real questions worth answering by counting",
                ],
                "parent_role": "When a real question of how many comes up, reach for paper and tally it together, and show how marks gathered in fives keep the count. Follow the child's own curiosity about what to count, and let the gathered chart answer the question that started it.",
                "observation_documentation": "Over time, note whether the child counts and tallies in groups of five, organizes the marks into a chart, reads it, and answers questions from the data. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Reading chart titles and labels",
            "science": "Recording observation data in journals",
            "history": "Census: counting populations through history",
        },
    },
    "mf-23": {
        "enriched": True,
        "learning_objectives": [
            "Solve single-step addition word problems",
            "Identify key information in a word problem",
            "Draw pictures to represent word problems",
            "Write number sentences for word problems",
        ],
        "teaching_guidance": {
            "introduction": "Word problems are math stories. The child reads the story, figures out what is happening (putting together = addition), draws a picture, and writes a number sentence. Start by acting out problems with real objects.",
            "scaffolding_sequence": [
                "Act out addition stories with real objects",
                "Draw pictures to represent the problem",
                "Identify the key numbers and the action (joining, adding)",
                "Write a number sentence with + and =",
                "Solve and check by counting the picture",
            ],
            "socratic_questions": [
                "What is happening in this story? Are things being added or taken away?",
                "What numbers do you see in the problem?",
                "Can you draw a picture of what's happening?",
            ],
            "practice_activities": [
                "Act out word problems with toys or snacks",
                "Draw and solve: picture first, then number sentence",
                "Write your own addition word problems",
            ],
            "real_world_connections": [
                "How many altogether when combining groups?",
                "Total items in a shopping cart",
                "Combined scores in a game",
            ],
            "common_misconceptions": [
                "Not reading carefully and missing key information",
                "Adding all numbers even when some aren't relevant",
                "Not checking if the answer makes sense",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Solves addition word problems within 20",
                "Draws a matching picture",
                "Writes a correct number sentence",
            ],
            "assessment_methods": ["word problem solving", "picture drawing", "number sentence writing"],
            "sample_assessment_prompts": [
                "Tom has 7 cars. He gets 5 more. How many now?",
                "Draw a picture and write a number sentence.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Sam has 3 apples. He picks 4 more. How many apples does Sam have?",
                "expected_type": "number",
                "correct_answer": "7",
                "hints": ["3 apples + 4 more apples"],
                "explanation": "3 + 4 = 7 apples.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "There are 5 birds in a tree. 3 more land. How many birds now?",
                "expected_type": "number",
                "correct_answer": "8",
                "hints": ["5 + 3"],
                "explanation": "5 + 3 = 8 birds.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Emma has 8 stickers. She gets 6 more at school. How many stickers does Emma have now?",
                "expected_type": "number",
                "correct_answer": "14",
                "hints": ["8 + 6. Use make-ten: 8+2=10, then 4 more"],
                "explanation": "8 + 6 = 14 stickers.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "There are 9 red fish and 7 blue fish in a tank. How many fish altogether? Write the number sentence.",
                "expected_type": "text",
                "hints": ["9 + 7 = ?"],
                "explanation": "9 + 7 = 16 fish.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Jake has 6 toy cars. He gets 8 more for his birthday. How many does he have now?",
                "type": "number",
                "correct_answer": "14",
                "target_concept": "addition_word_problem",
            },
            {
                "prompt": "Write a number sentence for: 5 cats are sleeping. 7 more cats come. How many cats?",
                "type": "text",
                "correct_answer": "5 + 7 = 12",
                "target_concept": "number_sentence",
            },
            {
                "prompt": "Draw a picture and solve: There are 4 red balls and 9 blue balls. How many balls?",
                "type": "open_response",
                "rubric": "Mastery: picture matches, correct answer (13), number sentence written. Proficient: correct answer with picture. Developing: incorrect.",
                "target_concept": "problem_solving",
            },
        ],
        "resource_guidance": {
            "required": ["counters for acting out problems"],
            "recommended": ["drawing paper", "word problem cards"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Read problems aloud. Picture representations. Focus on math, not reading.",
            "adhd": "Act out with real objects. Child is the character. Personal and physical.",
            "gifted": "Two-step problems. Extra information distractors. Write own problems.",
            "visual_learner": "Draw every problem. Bar model diagrams.",
            "kinesthetic_learner": "Act out with objects before writing.",
            "auditory_learner": "Read aloud. Retell in own words. State question before solving.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "A word problem is a math story. To solve it, the child reads the story, finds the numbers and the action, decides whether things are being joined together, draws a picture of what is happening, and writes a number sentence with a plus and an equals sign. When groups are put together, the story calls for addition.",
                "gradual_release": {
                    "i_do": "Read an addition story aloud, then act it out with counters. Think aloud: here are the numbers, here things are being joined, so I add. Draw a picture of the two groups, write the number sentence with plus and equals, and check the answer by counting the picture.",
                    "we_do": "Read a word problem together, find the key numbers and the joining action, draw the picture, write the number sentence, solve it, and check by counting.",
                    "you_do": "Child reads an addition word problem, identifies the key information, draws a picture, writes a number sentence, and solves it.",
                },
                "guided_practice": [
                    "Act out addition stories with counters or toys",
                    "Underline or name the key numbers and the joining action in a problem",
                    "Draw a picture for a word problem and write its number sentence",
                ],
                "independent_practice": [
                    "Solve addition word problems by drawing a picture and writing the number sentence",
                    "Write an addition word problem of your own and solve it",
                ],
                "mastery_check": [
                    "Solve a single-step addition word problem within twenty",
                    "Draw a picture that matches the problem",
                    "Write a correct addition number sentence with plus and equals",
                ],
                "spiral_review": [
                    "Revisit addition facts within twenty, the computation the word problem rests on",
                ],
            },
            "classical": {
                "narrative_introduction": "Number is not only counted, it is reasoned with. A word problem sets a small story before the mind and asks a question of it. The reasoner must read with care, find what is given and what is asked, see that two groups are being joined, and so know that the answer is found by adding. To solve it is to turn a story into a number sentence.",
                "memory_work": {
                    "chants": [
                        "Chant the steps: read the story, find the numbers, name the action, write the sentence, and check",
                        "Chant the sign of joining: when groups are put together, we add, and the answer is the whole",
                    ],
                    "recitations": [
                        "Recite that to add is to join groups together, and that the number sentence tells the story in the language of number",
                    ],
                },
                "copywork": [
                    "Copy a word problem and the number sentence that solves it, neatly, one beneath the other",
                ],
                "recitation_routine": "Begin each lesson by reciting the steps of solving a word problem before any new problem is met.",
                "history_integration": "Tell that word problems are very old, that the arithmetic of merchants and builders was always set as stories of real goods and real needs, and that to reason from a story to a number is an ancient and useful art.",
                "read_aloud_suggestions": [
                    "A story in which amounts are gathered or combined, read aloud so the child hears a real question of how many altogether",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A beautifully illustrated story or counting book in which things are gathered together, with real artwork and never a worksheet",
                ],
                "short_lesson_flow": "Take a real, small situation, perhaps apples gathered into a basket, and tell it as a little story with true numbers. Let the child act it out with the real things, draw what happened, and say the number sentence. Keep the numbers honest and the lesson short and calm. Stop while interest holds.",
                "narration_prompt": "Tell me the story of the problem in your own words. What was being put together, and how many were there altogether?",
                "real_world_objects": [
                    "Real things to gather and count: apples, acorns, blocks, beads",
                    "A basket or bowl into which two groups are joined",
                    "The child's own day, full of real moments of more arriving",
                ],
                "nature_connection": "Outdoors, gather things into two small groups, pinecones found by the path and pinecones found by the tree, and ask the real question of how many were gathered altogether.",
                "habit_focus": "The habit of attention: reading a story closely enough to know truly what it asks.",
            },
            "montessori": {
                "prepared_materials": [
                    "The golden bead material for representing the quantities in a story",
                    "Counters and small objects for acting a problem out",
                    "Word problem cards the child may read and choose",
                    "Paper for drawing the problem and writing the number sentence",
                ],
                "presentation": {
                    "three_period_lesson": "With a problem acted in beads: this is the joining, the two groups put together; show me the joining; what is happening to the groups in this story?",
                    "steps": [
                        "The child reads or hears a word problem and acts it out with golden beads or counters",
                        "The child names the numbers given and sees that the two groups are being joined",
                        "The child draws the problem and writes the number sentence, then checks the answer against the beads",
                    ],
                },
                "control_of_error": "The golden beads are the control: the answer written in the number sentence must match the quantity the joined beads make, so a wrong sentence is revealed by the beads themselves.",
                "abstraction_pathway": "From acting a story out with golden beads, to drawing the two groups, toward reading a word problem and writing its number sentence with no material at hand.",
                "extensions": [
                    "Solve problems with larger quantities using the golden beads",
                    "Write original word problems for another child to act out",
                    "Begin to meet problems that carry an extra number not needed for the answer",
                ],
                "observation_focus": "Watch for the child reading the whole story before reaching for an answer, and choosing addition because groups are joined rather than because numbers are present.",
            },
            "unschooling": {
                "invitations": [
                    "Let the child help with real counting and combining around the house",
                    "Keep counters, coins, and small toys handy for acting out questions of how many",
                    "Leave out paper for drawing and writing the math of a real situation",
                ],
                "real_world_contexts": [
                    "Counting how many altogether when two groups of things are put together",
                    "Adding up items going into the shopping cart or onto the table",
                    "Combining scores or points in a game",
                    "Gathering things and asking how many there are now",
                ],
                "conversation_starters": [
                    "You had some, and now more have come. How many do you have altogether?",
                    "How could you draw what just happened so we can see it?",
                    "Can you tell me that as a math sentence, with a plus in it?",
                ],
                "resource_bank": [
                    "Counters, coins, blocks, and toys for acting out",
                    "Paper and pencils for drawing and writing",
                    "The countless real moments of combining in daily life",
                ],
                "parent_role": "Notice the real moments when groups are joined and how-many-altogether is a true question, and wonder it aloud together. Let the child act it out with real things, and put the math into words and into a number sentence only as far as the child enjoys.",
                "observation_documentation": "Over time, note whether the child makes sense of an addition story, finds the key numbers, draws or acts it out, and can express it as a number sentence. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Comprehension required for word problems",
            "science": "Science problems: measuring, counting, comparing",
            "history": "Historical problems: armies, populations, distances",
        },
    },
    "mf-24": {
        "enriched": True,
        "learning_objectives": [
            "Solve single-step subtraction word problems",
            "Identify subtraction situations: take away, comparison, missing part",
            "Draw pictures for subtraction problems",
            "Write subtraction number sentences",
        ],
        "teaching_guidance": {
            "introduction": "Subtraction word problems come in three types: take away (had 10, ate 3, how many left?), comparison (Tom has 8, Sara has 5, how many more does Tom have?), and missing part (there are 12 total, 7 are red, how many are blue?). Act each type out with objects.",
            "scaffolding_sequence": [
                "Act out take-away problems with objects",
                "Act out comparison problems: line up two groups and compare",
                "Act out missing-part problems: cover some and find how many are hidden",
                "Draw pictures for each type",
                "Write number sentences with - and =",
            ],
            "socratic_questions": [
                "Is this problem about taking away or comparing?",
                "What numbers do you see?",
                "Can you draw what's happening?",
            ],
            "practice_activities": [
                "Act out subtraction stories",
                "Draw and solve problems",
                "Sort word problems by type: take away, compare, missing part",
            ],
            "real_world_connections": [
                "Spending money: had 15 cents, spent 7",
                "Eating snacks: had some, ate some, how many left?",
                "Comparing collections: who has more?",
            ],
            "common_misconceptions": [
                "Always subtracting the smaller from the larger without reading",
                "Not recognizing comparison problems as subtraction",
                "Not checking if the answer makes sense",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Solves all three types of subtraction word problems",
                "Draws matching pictures",
                "Writes correct number sentences",
            ],
            "assessment_methods": ["word problem solving", "problem type identification"],
            "sample_assessment_prompts": [
                "Amy had 12 grapes and ate 5. How many left?",
                "Is this a take-away or comparison problem?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "You have 9 cookies. You eat 4. How many are left?",
                "expected_type": "number",
                "correct_answer": "5",
                "hints": ["9 - 4"],
                "explanation": "9 - 4 = 5 cookies left.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "There are 8 ducks. 3 swim away. How many stay?",
                "expected_type": "number",
                "correct_answer": "5",
                "hints": ["8 - 3"],
                "explanation": "8 - 3 = 5 ducks stay.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Mia has 14 beads. Kai has 9 beads. How many more does Mia have?",
                "expected_type": "number",
                "correct_answer": "5",
                "hints": ["This is a comparison: 14 - 9"],
                "explanation": "14 - 9 = 5 more beads.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "There are 15 children. 8 are boys. How many are girls? Write the number sentence.",
                "expected_type": "text",
                "hints": ["15 total, 8 are boys, the rest are girls"],
                "explanation": "15 - 8 = 7 girls.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Tom had 16 marbles. He lost 7. How many does he have?",
                "type": "number",
                "correct_answer": "9",
                "target_concept": "take_away",
            },
            {
                "prompt": "Sara has 13 stickers. Lee has 8. How many more does Sara have?",
                "type": "number",
                "correct_answer": "5",
                "target_concept": "comparison",
            },
            {
                "prompt": "Draw a picture and solve: 11 birds are on a wire. 4 fly away. How many are left?",
                "type": "open_response",
                "rubric": "Mastery: picture matches, correct answer (7), number sentence. Proficient: correct answer. Developing: incorrect.",
                "target_concept": "subtraction_word_problem",
            },
        ],
        "resource_guidance": {
            "required": ["counters for acting out"],
            "recommended": ["word problem cards", "drawing paper"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Read aloud. Three subtraction types look different. Visual models for each.",
            "adhd": "Physical acting out: remove objects, count remaining.",
            "gifted": "Mixed operations (add or subtract?). Multi-step. Missing part.",
            "visual_learner": "Bar models for each type. Circle-and-cross-out for take-away.",
            "kinesthetic_learner": "Act out all three: take away, comparison, missing part.",
            "auditory_learner": "Categorize: 'Take-away, comparison, or missing-part story?'",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Subtraction word problems are math stories that come in three kinds. Take away: you had some, some went, how many are left. Comparison: one group has more than another, how many more. Missing part: the whole is known and one part is known, how many are in the other part. All three are solved by subtraction. Today we read each kind, draw it, and write a number sentence with a minus and an equals sign.",
                "gradual_release": {
                    "i_do": "Read a take-away story and act it out, removing counters. Read a comparison story and line two groups up to see the gap. Read a missing-part story and cover one part. Think aloud that each is subtraction, draw the picture, and write the number sentence with minus and equals.",
                    "we_do": "Read each kind of subtraction problem together, name its type, act it out, draw the picture, and write the number sentence.",
                    "you_do": "Child reads a subtraction word problem, names its type, draws a picture, writes a number sentence, and solves it.",
                },
                "guided_practice": [
                    "Act out take-away, comparison, and missing-part problems with counters",
                    "Sort word problems by type: take away, comparison, missing part",
                    "Draw a picture for a subtraction problem and write its number sentence",
                ],
                "independent_practice": [
                    "Solve subtraction word problems of all three types by drawing and writing the number sentence",
                    "Write a subtraction word problem of your own and solve it",
                ],
                "mastery_check": [
                    "Solve single-step subtraction word problems of all three types",
                    "Name whether a problem is take away, comparison, or missing part",
                    "Write a correct subtraction number sentence with minus and equals",
                ],
                "spiral_review": [
                    "Revisit subtraction facts within twenty, the computation these problems rest on",
                ],
            },
            "classical": {
                "narrative_introduction": "Subtraction wears three faces, and the reasoner must know each. Sometimes a thing is taken away, and we ask what remains. Sometimes two groups are set side by side, and we ask how much greater is the one. Sometimes the whole and a part are known, and we ask after the missing part. Three different stories, one operation: to read the story rightly is to know it calls for subtraction.",
                "memory_work": {
                    "chants": [
                        "Chant the three faces of subtraction: take away, compare, and find the missing part",
                        "Chant the steps: read the story, name its kind, write the sentence, and check",
                    ],
                    "recitations": [
                        "Recite that take away, comparison, and missing part are all answered by subtraction, the finding of what is left, what is more, or what is hidden",
                    ],
                },
                "copywork": [
                    "Copy a subtraction word problem and the number sentence that solves it, neatly, one beneath the other",
                ],
                "recitation_routine": "Begin each lesson by reciting the three faces of subtraction before any new problem is met.",
                "history_integration": "Tell that the arithmetic of trade and account has always asked these three questions, what is left after spending, how much one has more than another, how much of a known whole is still owing, and that naming the kind of problem is the reasoner's first task.",
                "read_aloud_suggestions": [
                    "A story in which something is spent, lost, or compared, read aloud so the child hears a real question of what remains or how many more",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A beautifully illustrated story in which things are eaten, given away, or compared, with real artwork and never a worksheet",
                ],
                "short_lesson_flow": "Take a real, small situation, perhaps grapes at snack time, and tell it as a little story with true numbers: some were eaten, how many are left. Another day tell a comparing story. Let the child act it out with the real things, draw it, and say the number sentence. Keep it short and calm.",
                "narration_prompt": "Tell me the story of the problem in your own words. Was something taken away, or were two groups compared?",
                "real_world_objects": [
                    "Real things to take from and to compare: grapes, crackers, blocks, coins",
                    "Two real groups set side by side to see which has more",
                    "The child's own day, full of real moments of some being used up",
                ],
                "nature_connection": "Outdoors, compare two real groups, the acorns under one tree and the acorns under another, and ask the true question of how many more there are under the one.",
                "habit_focus": "The habit of attention: reading a story closely enough to know which of its kinds it is.",
            },
            "montessori": {
                "prepared_materials": [
                    "The golden bead material for representing the quantities in a story",
                    "Counters and small objects for acting a problem out",
                    "Word problem cards sorted into the three kinds of subtraction",
                    "Paper for drawing the problem and writing the number sentence",
                ],
                "presentation": {
                    "three_period_lesson": "With problems acted in beads: this story takes away, this one compares, this one finds a missing part; show me a take-away story; which kind of subtraction is this?",
                    "steps": [
                        "The child reads or hears a subtraction problem and acts it out with golden beads or counters",
                        "The child names the kind of problem, take away, comparison, or missing part",
                        "The child draws the problem and writes the number sentence, then checks the answer against the beads",
                    ],
                },
                "control_of_error": "The golden beads are the control: the answer written in the number sentence must match the beads that remain, the gap between the groups, or the hidden part, so a wrong sentence is revealed by the material itself.",
                "abstraction_pathway": "From acting each kind of story out with golden beads, to drawing it, toward reading a subtraction problem, naming its kind, and writing its number sentence with no material at hand.",
                "extensions": [
                    "Solve subtraction problems with larger quantities using the golden beads",
                    "Write original problems of each of the three kinds",
                    "Sort a set of mixed word problems by operation and by kind",
                ],
                "observation_focus": "Watch for the child naming the kind of problem before solving, and recognizing comparison and missing-part stories as subtraction, not only take-away.",
            },
            "unschooling": {
                "invitations": [
                    "Let the child help with real counting at moments when things are used up or compared",
                    "Keep counters, coins, and small toys handy for acting out questions of how many",
                    "Leave out paper for drawing and writing the math of a real situation",
                ],
                "real_world_contexts": [
                    "Eating part of a snack and asking how many are left",
                    "Spending some coins and asking how much money remains",
                    "Comparing two collections and asking who has more, and how many more",
                    "Knowing a whole and one part, and asking about the missing part",
                ],
                "conversation_starters": [
                    "You had some, and some are gone now. How many are left?",
                    "You have more than I do. How many more?",
                    "We know how many there are altogether, and how many are red. How many are blue?",
                ],
                "resource_bank": [
                    "Counters, coins, blocks, and toys for acting out",
                    "Paper and pencils for drawing and writing",
                    "The countless real moments of using up and comparing in daily life",
                ],
                "parent_role": "Notice the real moments when something is taken away or two groups are compared, and wonder the question aloud together. Let the child act it out with real things, and put the math into words and a number sentence only as far as the child enjoys.",
                "observation_documentation": "Over time, note whether the child makes sense of take-away, comparison, and missing-part stories, draws or acts them out, and can express them as subtraction number sentences. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Comparison language: more, fewer, less",
            "science": "Differences in experimental data",
            "history": "Losses in events: how many remained",
        },
    },
    "mf-25": {
        "enriched": True,
        "learning_objectives": [
            "Add three single-digit numbers",
            "Use strategies: look for ten, add doubles first",
            "Understand that grouping doesn't change the sum",
            "Rearrange addends to make addition easier",
        ],
        "teaching_guidance": {
            "introduction": "Adding three numbers is the same as adding two, then adding the third. The trick: look for pairs that make 10 or doubles, and add those first. 7 + 5 + 3 is easier as 7 + 3 + 5 = 10 + 5 = 15.",
            "scaffolding_sequence": [
                "Add three numbers by adding two, then the third",
                "Look for pairs that make 10",
                "Look for doubles to add first",
                "Practice rearranging to find the easiest order",
                "Solve word problems with three addends",
            ],
            "socratic_questions": [
                "Can you find two numbers that make 10?",
                "Does it matter which two you add first?",
                "What's the easiest way to add these three?",
            ],
            "practice_activities": [
                "Three-dice addition: roll 3 dice and find the sum",
                "Number card trios: find groups of 3 that sum to a target",
                "Look for tens: circle pairs that make 10 before adding",
            ],
            "real_world_connections": [
                "Adding scores across 3 rounds of a game",
                "Counting items in 3 different bags",
                "Adding up prices of 3 items",
            ],
            "common_misconceptions": [
                "Trying to add all three at once instead of two then one",
                "Not looking for easier combinations",
                "Thinking order matters (it doesn't for addition)",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Adds three single-digit numbers correctly",
                "Identifies make-ten pairs",
                "Rearranges for efficiency",
            ],
            "assessment_methods": ["computation", "strategy identification"],
            "sample_assessment_prompts": ["What is 6 + 4 + 7?", "Which two would you add first in 3 + 8 + 7? Why?"],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is 2 + 3 + 4?",
                "expected_type": "number",
                "correct_answer": "9",
                "hints": ["2+3=5, then 5+4=9"],
                "explanation": "2 + 3 + 4 = 9.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is 7 + 5 + 3?",
                "expected_type": "number",
                "correct_answer": "15",
                "hints": ["Look for ten: 7+3=10, then 10+5=15"],
                "explanation": "7 + 3 = 10, then 10 + 5 = 15.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is 6 + 4 + 8?",
                "expected_type": "number",
                "correct_answer": "18",
                "hints": ["6+4=10, then 10+8=18"],
                "explanation": "6 + 4 = 10, then 10 + 8 = 18.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "What is 8 + 5 + 2? Show which two you add first and why.",
                "expected_type": "text",
                "hints": ["8+2=10 is a nice pair"],
                "explanation": "Add 8+2=10 first (they make ten), then 10+5=15.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "What is 9 + 1 + 6?",
                "type": "number",
                "correct_answer": "16",
                "target_concept": "three_addends",
            },
            {
                "prompt": "In 4 + 6 + 5, which two would you add first? Why?",
                "type": "open_response",
                "rubric": "Mastery: 4+6=10 first because they make ten. Proficient: correct answer, any order. Developing: no strategy.",
                "target_concept": "make_ten_strategy",
            },
        ],
        "resource_guidance": {"required": ["three dice"], "recommended": ["number cards"]},
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Write vertically. Color to group the pair added first.",
            "adhd": "Three-dice games: roll, find ten-pair, add third. Quick rounds.",
            "gifted": "Four numbers. Three two-digit numbers. Multiple ten opportunities.",
            "visual_learner": "Circle make-ten pair in color. Three-part bond diagrams.",
            "kinesthetic_learner": "Three object groups. Combine two, add third.",
            "auditory_learner": "Verbalize: '7 and 3 make ten. Ten plus 5 is fifteen.'",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Adding three numbers is just adding two, and then adding the third. But the order is the adder's to set, since addition may be grouped any way and the sum does not change. So look first for a pair that makes ten, or a pair of doubles, add those, and the third number is easy. Today we add three single-digit numbers, use the make-ten and doubles strategies, and rearrange the addends to make the work easier.",
                "gradual_release": {
                    "i_do": "Take three numbers, say 7, 5, and 3, and think aloud: 7 and 3 make ten, so I add those first, then 10 and 5 is 15. Show plainly that grouping the numbers differently gives the same sum, so it is wise to choose the easiest pair first.",
                    "we_do": "Add three numbers together: hunt for a make-ten pair or a doubles pair, add it first, then add the third, and check that a different grouping gives the same total.",
                    "you_do": "Child adds three single-digit numbers, rearranges them to add the easiest pair first, and uses the make-ten or doubles strategy.",
                },
                "guided_practice": [
                    "Add three numbers by finding and adding a make-ten pair first",
                    "Add three numbers by finding and adding a doubles pair first",
                    "Add the same three numbers in two different groupings and see the sum is the same",
                ],
                "independent_practice": [
                    "Roll three dice and find the sum, choosing the easiest pair to add first",
                    "Solve word problems that add three quantities",
                ],
                "mastery_check": [
                    "Add three single-digit numbers correctly",
                    "Find a make-ten or doubles pair and add it first",
                    "Explain that grouping the addends differently does not change the sum",
                ],
                "spiral_review": [
                    "Revisit the make-ten and doubles addition facts, the pairs the strategy depends on",
                ],
            },
            "classical": {
                "narrative_introduction": "Addition keeps a quiet law: numbers may be gathered in any grouping, and the sum is always the same. This law is the adder's freedom. Given three numbers to add, the wise reckoner does not add them blindly in their order, but looks for the easy pair, the two that make ten or the two that match, joins those first, and the third falls in with ease.",
                "memory_work": {
                    "chants": [
                        "Chant the law of grouping: numbers may be joined in any order, and the sum stays the same",
                        "Chant the easy pairs to hunt for: the two that make ten, and the two that are the same",
                    ],
                    "recitations": [
                        "Recite that to add three numbers is to add two and then the third, and that the easy pair is added first",
                    ],
                },
                "copywork": [
                    "Copy a three-number sum, then copy it again with the addends rearranged, showing the same total beneath each",
                ],
                "recitation_routine": "Begin each lesson by reciting the law of grouping and chanting the make-ten pairs before any new work.",
                "history_integration": "Tell that the law by which numbers may be grouped in any order has been known since arithmetic began, and that it is one of the plain and certain truths on which all reckoning is built.",
                "read_aloud_suggestions": [
                    "A story in which things are gathered from three sources and counted up together, read aloud so the child hears three groups joined into one",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A beautifully illustrated story or counting book in which things are gathered from three places, with real artwork and never a worksheet",
                ],
                "short_lesson_flow": "Take three small real groups, perhaps apples picked from three trees, and join them. Let the child see that the easy pair, the two that make ten, can be added first, and the third after. Try grouping them another way and see the total hold. Keep the numbers honest and the lesson short.",
                "narration_prompt": "Tell me how you added the three groups. Which two did you put together first, and why was that the easy way?",
                "real_world_objects": [
                    "Three small real groups to join: apples, acorns, beads, blocks",
                    "Three dice rolled and the spots gathered into one sum",
                    "The child's own day, with its three rounds of a game or three bags to count",
                ],
                "nature_connection": "Outdoors, gather things from three places, the pebbles by the path, by the tree, and by the water, and add the three small heaps into one count, choosing the easy pair first.",
                "habit_focus": "The habit of thinking before acting: looking for the easy pair before beginning to add.",
            },
            "montessori": {
                "prepared_materials": [
                    "The colored bead bars, three bars to be joined into one quantity",
                    "The addition strip board for combining numbers",
                    "Number cards for setting out three addends to rearrange",
                ],
                "presentation": {
                    "three_period_lesson": "With three bead bars: these two make ten, the easy pair to join first; show me the pair that makes ten; which two bars make the easy pair?",
                    "steps": [
                        "Lay out three bead bars and count the whole quantity they make",
                        "Find the pair that makes ten, or the matching pair, and join it first, then add the third bar",
                        "Rearrange the three bars into a different grouping and confirm the same total",
                    ],
                },
                "control_of_error": "The bead bars are the control: counted out, the three bars make one fixed quantity, so whatever the order they are joined the child finds the same length and sees that grouping does not change the sum.",
                "abstraction_pathway": "From joining three concrete bead bars and counting the whole, to choosing the easy pair by sight, toward adding three numbers in the mind by making ten first.",
                "extensions": [
                    "Add four bead bars, hunting for more than one easy pair",
                    "Find all the ways three numbers can be grouped and see each gives one sum",
                    "Solve three-addend word problems with the beads",
                ],
                "observation_focus": "Watch for the child seeking the make-ten or doubles pair before adding, and trusting that the order of joining does not change the total.",
            },
            "unschooling": {
                "invitations": [
                    "Keep three dice and number cards out for free adding games",
                    "Leave out collections that come in three groups: three jars, three baskets, three piles",
                    "Have paper handy for adding up the math of real situations",
                ],
                "real_world_contexts": [
                    "Adding scores across three rounds of a game",
                    "Counting up items gathered from three different places",
                    "Adding the prices of three things being bought",
                    "Combining three small handfuls or piles into one count",
                ],
                "conversation_starters": [
                    "We have three numbers to add. Which two would be the easy ones to put together first?",
                    "Can you find two of these that make ten?",
                    "Does it matter which two you add first? Try it another way and see.",
                ],
                "resource_bank": [
                    "Dice, number cards, and counters kept available",
                    "Games that score across several rounds",
                    "Real moments of gathering things from three places",
                ],
                "parent_role": "When three amounts come up to be added, in a game, at the shop, around the house, wonder aloud together which pair is the easy one to join first. Let the child discover by trying that the order of adding does not change the total, rather than being told it as a rule.",
                "observation_documentation": "Over time, note whether the child adds three numbers, hunts for an easy make-ten or doubles pair, and trusts that grouping the addends differently keeps the same sum. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Adding three things in a story",
            "science": "Combining three experimental trials",
            "history": "Adding populations of three cities",
        },
    },
    "mf-26": {
        "enriched": True,
        "learning_objectives": [
            "Develop mental math strategies for addition and subtraction",
            "Use counting on, making ten, doubles, and breaking apart",
            "Choose the best strategy for a given problem",
            "Explain strategies used",
        ],
        "teaching_guidance": {
            "introduction": "Mental math means solving in your head without pencil, paper, or fingers. It's not about speed; it's about having STRATEGIES. Good mental math thinkers don't just know the answer. They know HOW they got it and can pick the best approach.",
            "scaffolding_sequence": [
                "Name the strategies: counting on, making ten, doubles, breaking apart",
                "Practice each strategy with 5 problems",
                "For each new problem, ask: which strategy works best here?",
                "Practice explaining: 'I solved it by...'",
                "Mental math challenges: solve without writing anything",
            ],
            "socratic_questions": [
                "What strategy did you use? Is there a faster one?",
                "For 8+7, would you count on or make ten? Why?",
                "How would you solve 15-8 in your head?",
            ],
            "practice_activities": [
                "Strategy sort: match problems to their best strategy",
                "Mental math relay: solve problems out loud, explain strategy",
                "Number talks: share different strategies for the same problem",
            ],
            "real_world_connections": [
                "Quickly adding prices in your head at a store",
                "Calculating change mentally",
                "Adding up game scores without paper",
            ],
            "common_misconceptions": [
                "Thinking mental math means memorization only",
                "Using only one strategy for every problem",
                "Believing finger counting is always bad (it's a starting point, not an endpoint)",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Solves addition/subtraction within 20 mentally using named strategies",
                "Chooses appropriate strategy for each problem",
                "Explains strategy clearly",
            ],
            "assessment_methods": ["oral mental math", "strategy explanation", "strategy selection"],
            "sample_assessment_prompts": [
                "Solve 9+6 in your head and tell me your strategy",
                "Which strategy works best for 15-7?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Solve in your head: 6 + 3. What strategy did you use?",
                "expected_type": "text",
                "hints": ["Counting on: start at 6, count 7, 8, 9"],
                "explanation": "9. Counting on from 6: 7, 8, 9.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Solve in your head: 8 + 7. Name your strategy.",
                "expected_type": "text",
                "hints": ["Make ten: 8+2=10, then 5 more = 15", "Or doubles: 7+7=14, plus 1 = 15"],
                "explanation": "15. Make-ten or doubles-plus-one.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Solve in your head: 14 - 6. Name your strategy.",
                "expected_type": "text",
                "hints": ["Think addition: 6 + ? = 14", "Or subtract through ten: 14-4=10, 10-2=8"],
                "explanation": "8. Think addition: 6+8=14, so 14-6=8.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "For 9 + 5, explain two different strategies you could use.",
                "expected_type": "text",
                "hints": ["Try make-ten AND counting on"],
                "explanation": "Strategy 1: Make ten. 9+1=10, 10+4=14. Strategy 2: Count on from 9: 10,11,12,13,14.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Solve 7 + 8 mentally. Explain your strategy.",
                "type": "open_response",
                "rubric": "Mastery: correct (15) with named strategy. Proficient: correct with some explanation. Developing: correct but no strategy.",
                "target_concept": "mental_math",
            },
            {
                "prompt": "Which strategy would you use for 16-9? Why?",
                "type": "open_response",
                "rubric": "Mastery: names think-addition or subtract-through-ten with reasoning. Proficient: names a strategy. Developing: no strategy.",
                "target_concept": "strategy_selection",
            },
        ],
        "resource_guidance": {
            "required": ["none, mental math is tool-free"],
            "recommended": ["strategy reference cards", "number talk prompts"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Name strategies verbally. Mental math removes written barriers. Strength-based.",
            "adhd": "Number talks: short, social, varied. 2-3 minutes per problem.",
            "gifted": "Two-digit mental math. Multiple strategies per problem. Invent new ones.",
            "visual_learner": "Draw strategy diagrams: number line hops, bond splits.",
            "kinesthetic_learner": "Fingers for tracking strategy steps, not counting.",
            "auditory_learner": "Think-alouds: verbalize every step. Partner sharing.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Mental math is solving in the head, with no pencil and no fingers. It is not a race; it rests on strategies. There are several: counting on from the larger number, making ten, using a known doubles fact, and breaking a number apart. A strong mental mathematician does not only know the answer, they know how they found it and can choose the best way. Today we name and use these strategies, choose the one that fits each problem, and explain our thinking.",
                "gradual_release": {
                    "i_do": "Solve a problem aloud each way: for 8 plus 7, make ten, 8 and 2 is 10, then 5 more is 15, or use doubles, 7 and 7 is 14, one more is 15. For 14 minus 6, think addition: 6 and what makes 14. Name each strategy as I use it.",
                    "we_do": "Solve addition and subtraction problems within twenty in our heads together, naming the strategy each time, and talking about which strategy fits best.",
                    "you_do": "Child solves addition and subtraction within twenty mentally, chooses an appropriate strategy, and explains the strategy used.",
                },
                "guided_practice": [
                    "Practice each strategy in turn: counting on, making ten, doubles, breaking apart",
                    "Match problems to the strategy that suits them best",
                    "Solve a problem and say aloud, I solved it by",
                ],
                "independent_practice": [
                    "Solve a mixed set of problems mentally, naming the strategy for each",
                    "Solve one problem two different ways and compare the strategies",
                ],
                "mastery_check": [
                    "Solve addition and subtraction within twenty mentally, using a named strategy",
                    "Choose a strategy that fits the particular problem",
                    "Explain the strategy used clearly",
                ],
                "spiral_review": [
                    "Revisit the make-ten facts and doubles facts, the known facts the strategies build upon",
                ],
            },
            "classical": {
                "narrative_introduction": "The mind itself is the first and best instrument of arithmetic. To reckon in the head is no mere trick of speed; it is the having of strategies and the choosing well among them. Counting on, making ten, calling on a known double, breaking a number apart: these are the tools of mental reckoning, and the trained mind knows each, and knows which to take up for the task at hand.",
                "memory_work": {
                    "chants": [
                        "Chant the four strategies: count on, make ten, use a double, break apart",
                        "Chant the make-ten and doubles facts daily, the known facts on which mental reckoning stands",
                    ],
                    "recitations": [
                        "Recite that mental math is not speed but strategy, and that the reckoner must know how the answer was found",
                    ],
                },
                "copywork": [
                    "Copy the names of the four mental strategies, and beside each a problem it suits",
                ],
                "recitation_routine": "Begin each lesson with a short oral warm-up: a few problems solved in the head, each with its strategy named, the known facts rehearsed cumulatively.",
                "history_integration": "Tell that before there was paper to spare or any machine to reckon, all arithmetic was done in the head or aloud, and that merchants, builders, and navigators carried their sums in the mind, as the trained reckoner still can.",
                "read_aloud_suggestions": [
                    "A story in which a character must reckon something quickly in their head, read aloud so the child hears mental arithmetic put to use",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A beautifully illustrated story in which a character works something out in their head, with real artwork and never a worksheet",
                ],
                "short_lesson_flow": "Begin the morning with a few minutes of oral, mental arithmetic, calm and unhurried. Pose a problem; let the child solve it in their head and tell not only the answer but how they found it. A few problems are plenty. Stop while the mind is still fresh and willing.",
                "narration_prompt": "Tell me how you worked that out in your head. Which way did you choose, and why was it the good way?",
                "real_world_objects": [
                    "No materials at all, for mental math is done in the head",
                    "The real small sums of the day, prices, scores, minutes, worked out aloud",
                    "A quiet moment at the start of the day kept for oral reckoning",
                ],
                "nature_connection": "On a walk, pose small real sums in the head, how many birds if three more join the five, how many petals on two flowers, and let the child reckon them aloud in the open air.",
                "habit_focus": "The habit of mental effort: holding numbers in the mind and working with them there, without reaching for pencil or fingers.",
            },
            "montessori": {
                "prepared_materials": [
                    "No new material, the child draws on long work with the bead bars, the golden beads, and the strip boards",
                    "Strategy reference cards naming counting on, making ten, doubles, and breaking apart",
                    "Problem cards the child may choose and solve in the head",
                ],
                "presentation": {
                    "three_period_lesson": "With the strategy cards: this strategy is making ten, this is using a double; show me the making-ten strategy; which strategy is this?",
                    "steps": [
                        "The child solves a problem in the head, having met the quantities long before in the concrete materials",
                        "The child names the strategy used: counting on, making ten, a double, or breaking apart",
                        "The child meets a new problem and chooses the strategy that best fits it",
                    ],
                },
                "control_of_error": "The long concrete work is the control: a child who has built these quantities many times with the beads carries an inner sense of them, and a mental answer that does not feel right is checked back against the known facts and the materials.",
                "abstraction_pathway": "From building every quantity with the concrete materials, to picturing those materials in the mind, toward reckoning addition and subtraction with no material and no picture, by strategy alone.",
                "extensions": [
                    "Solve a problem by two different strategies and compare them",
                    "Take up mental math with larger, two-digit quantities",
                    "Hold a number talk, sharing different strategies for one problem",
                ],
                "observation_focus": "Watch for the child reckoning without reaching for the materials or fingers, choosing a strategy that fits, and able to say how the answer was found.",
            },
            "unschooling": {
                "invitations": [
                    "Pose small math puzzles aloud as part of ordinary talk",
                    "Keep games that call for quick scoring and adding within reach",
                    "Let the child be the one to work out real sums: the change, the total, the score",
                ],
                "real_world_contexts": [
                    "Adding up prices in the head while shopping",
                    "Working out the change from a purchase",
                    "Keeping a running score in a game without paper",
                    "Figuring how many minutes until something, or how many of something are needed",
                ],
                "conversation_starters": [
                    "How could you work that out in your head?",
                    "You got the answer fast, how did you do it? Tell me your way.",
                    "Is there another way you could have figured that out?",
                ],
                "resource_bank": [
                    "Games that involve scoring and quick adding",
                    "The countless real sums of shopping, cooking, and daily life",
                    "An adult who thinks aloud through their own mental math",
                ],
                "parent_role": "Do your own mental math out loud so the child hears that there are many ways to reach an answer, and pose small real sums as a natural part of talk. Ask how the child worked it out, with genuine interest, and never push for speed over understanding.",
                "observation_documentation": "Over time, note whether the child solves small sums in the head, draws on strategies like making ten and doubles, and can say how the answer was reached. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Mental math while reading: estimating pages",
            "science": "Quick calculations during experiments",
            "history": "Mental arithmetic for dates between events",
        },
    },
    "mf-27": {
        "enriched": True,
        "learning_objectives": [
            "Estimate quantities before counting",
            "Estimate sums before adding",
            "Develop number sense for reasonableness",
            "Use benchmarks: about 10, about 20, about 50",
        ],
        "teaching_guidance": {
            "introduction": "Estimation is educated guessing using what you know about numbers. Before counting a jar of beans, look and guess: about 10? 20? 50? Then count and compare. Over time, estimates get closer. Estimation builds number sense.",
            "scaffolding_sequence": [
                "Estimate a small group (5-10): guess then count",
                "Estimate a medium group (10-30): use a benchmark of 10",
                "Estimate sums: about how much is 8+9?",
                "Compare estimate to actual: how close were you?",
                "Practice 'is my answer reasonable?' after solving problems",
            ],
            "socratic_questions": [
                "About how many do you think are here? What made you guess that?",
                "Is 8+9 closer to 10 or to 20?",
                "You got 47 for 23+25. Does that seem reasonable?",
            ],
            "practice_activities": [
                "Estimation jars: guess how many, then count",
                "Estimate then measure: how long is this table in paper clips?",
                "Reasonableness check: is 5+6=56 reasonable? Why not?",
            ],
            "real_world_connections": [
                "Estimating grocery costs before checkout",
                "Estimating time: about how long will this take?",
                "Estimating distance: about how far is the park?",
            ],
            "common_misconceptions": [
                "Thinking estimation is just random guessing",
                "Not using benchmarks",
                "Being upset when estimate isn't exact",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Estimates within 20% of actual for groups of 10-30",
                "Estimates sums within 5 of actual",
                "Checks reasonableness of answers",
            ],
            "assessment_methods": ["estimation tasks", "reasonableness checking"],
            "sample_assessment_prompts": ["About how many beans are in this jar?", "Is 7+8=58 reasonable?"],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "About how much is 4 + 5? (Don't calculate. Estimate.)",
                "expected_type": "text",
                "correct_answer": "about 10",
                "hints": ["Both are close to 5. 5+5=10."],
                "explanation": "About 10. The exact answer is 9.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "A student says 6 + 7 = 67. Is that reasonable?",
                "expected_type": "text",
                "correct_answer": "no",
                "hints": ["Both numbers are less than 10. Can their sum be 67?"],
                "explanation": "No. 6+7 should be close to 13, not 67.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "About how many stars are here: * * * * * * * * * * * * * * (don't count, estimate)",
                "expected_type": "text",
                "hints": ["Look at a group of 5 as a benchmark"],
                "explanation": "About 14. Using a benchmark of 5, roughly 3 groups.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "You estimate a jar has about 25 beans. You count and get 22. Was your estimate good? Why?",
                "expected_type": "text",
                "hints": ["How close was 25 to 22?"],
                "explanation": "Yes. 25 is only 3 away from 22. A good estimate is close, not exact.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Is 9 + 8 = 78 reasonable? Explain.",
                "type": "open_response",
                "rubric": "Mastery: no, both less than 10 so sum must be less than 20. Proficient: says no with some reasoning. Developing: unsure.",
                "target_concept": "reasonableness",
            },
            {
                "prompt": "Estimate: about how much is 7 + 6?",
                "type": "text",
                "correct_answer": "about 13",
                "target_concept": "estimation",
            },
        ],
        "resource_guidance": {
            "required": ["jars with countable items"],
            "recommended": ["estimation mats with benchmarks"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 10},
        "accommodations": {
            "dyslexia": "Oral and visual. No reading or writing. Strong area for many.",
            "adhd": "Estimation jars and guessing games. Surprise maintains engagement.",
            "gifted": "Larger numbers. Percentage error. When is 'good enough'?",
            "visual_learner": "Benchmark groups visible: group of 10 and 20 as reference.",
            "kinesthetic_learner": "Grab handful, estimate, count. Physical interaction.",
            "auditory_learner": "Talk through: 'About 20 because this looks like two groups of ten.'",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Estimation is an educated guess, made using what you already know about numbers. Before counting a jar of beans, you look and judge: about ten, about twenty, about fifty. Before adding, you judge about how big the answer should be. A benchmark, a known group of ten or twenty, helps the eye judge. Estimation builds number sense and lets you check whether an answer is reasonable. Today we estimate quantities and sums, use benchmarks, and check answers for reasonableness.",
                "gradual_release": {
                    "i_do": "Look at a group without counting and think aloud: this looks like about two groups of ten, so about twenty. Estimate a sum: eight and nine are both near ten, so about twenty. Then count or compute and compare. Show how to ask, is this answer reasonable.",
                    "we_do": "Estimate quantities and sums together, using a benchmark of ten, then count or add and see how close the estimate was, and check answers for reasonableness.",
                    "you_do": "Child estimates a quantity and a sum before counting or adding, uses a benchmark, and checks whether an answer is reasonable.",
                },
                "guided_practice": [
                    "Estimate a quantity using a benchmark group of ten, then count and compare",
                    "Estimate a sum before adding, then add and compare",
                    "Decide whether a given answer is reasonable and say why",
                ],
                "independent_practice": [
                    "Estimate the count of several jars or groups, then count and see how close",
                    "After solving problems, check each answer for reasonableness",
                ],
                "mastery_check": [
                    "Estimate a quantity of ten to thirty, coming reasonably close",
                    "Estimate a sum before adding",
                    "Judge whether an answer is reasonable and explain why",
                ],
                "spiral_review": [
                    "Revisit benchmark groups of ten and twenty, the reference points estimation leans on",
                ],
            },
            "classical": {
                "narrative_introduction": "Not every question of number asks for an exact count. Often the wise answer is a judged one: about how many, about how much. Estimation is that judgment, an educated guess resting on a known measure, a benchmark of ten or twenty held in the mind. And once a sum is reckoned, estimation guards it, for it asks the steadying question: is this answer reasonable?",
                "memory_work": {
                    "chants": [
                        "Chant the benchmarks: about ten, about twenty, about fifty",
                        "Chant the guard of every answer: is this reasonable, could it truly be so",
                    ],
                    "recitations": [
                        "Recite that an estimate is an educated guess, made with a benchmark, and that a good estimate is close, not exact",
                    ],
                },
                "copywork": [
                    "Copy a few estimates beside their true counts, neatly, so the eye sees how near a good estimate comes",
                ],
                "recitation_routine": "Begin each lesson by reciting the benchmarks and the question of reasonableness before any new estimating.",
                "history_integration": "Tell that before exact measure was always at hand, people lived by good estimation, judging a harvest, a flock, a journey by eye and by experience, and that the judging of about how many is an old and practical wisdom.",
                "read_aloud_suggestions": [
                    "A story in which a character judges an amount by eye, read aloud so the child hears estimation at work",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A beautifully illustrated book full of countable things, birds, leaves, stars, that invites the child to guess and then look, never a workbook",
                ],
                "short_lesson_flow": "Make estimation a small, glad habit of the day rather than a lesson. Before counting anything, the steps to the gate, the apples in the bowl, the books on the shelf, pause and guess together. Then count, and see how near the guess came. Keep it light and unhurried.",
                "narration_prompt": "Tell me your guess before we count. What made you guess that number? How close was it?",
                "real_world_objects": [
                    "Everyday countable things: steps, apples, books, buttons, birds",
                    "A jar of beans or pebbles to guess at and then count",
                    "A known group of ten kept as a benchmark for the eye",
                ],
                "nature_connection": "Outdoors, estimate before counting: about how many petals on the flower, how many birds in the flock, how many steps to the big tree, then count and compare in the nature notebook.",
                "habit_focus": "The habit of attention and of judgment: looking carefully enough to make a thoughtful guess, and being content that a good estimate is close.",
            },
            "montessori": {
                "prepared_materials": [
                    "Benchmark sets, a clear group of ten and a group of twenty, kept for the eye to refer to",
                    "Estimation jars holding countable quantities",
                    "An estimation mat for recording the guess and then the true count",
                ],
                "presentation": {
                    "three_period_lesson": "With the benchmark sets: this is a group of ten, this a group of twenty; show me the group of twenty; how many is this benchmark group?",
                    "steps": [
                        "Look at a quantity beside the benchmark of ten and judge, without counting, about how many",
                        "Record the estimate, then count the quantity truly",
                        "Compare the estimate with the true count and see how near it came",
                    ],
                },
                "control_of_error": "The true count is the control: after the estimate is made and recorded, the child counts the real quantity and sees plainly how close the guess was, so the material itself teaches the eye to judge better.",
                "abstraction_pathway": "From judging a quantity beside a concrete benchmark of ten, to estimating with the benchmark only pictured in the mind, toward estimating sums and judging the reasonableness of any answer.",
                "extensions": [
                    "Estimate larger quantities and sums",
                    "Keep a record of estimates and true counts and watch the estimates draw closer",
                    "Use estimation to check the reasonableness of completed work",
                ],
                "observation_focus": "Watch for the child using a benchmark to judge rather than guessing wildly, and growing content that a good estimate is close, not exact.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a guessing jar filled with something countable and changed often",
                    "Make estimating a playful part of ordinary moments",
                    "Leave out collections worth guessing at and then counting",
                ],
                "real_world_contexts": [
                    "Guessing the grocery total before reaching the checkout",
                    "Judging about how long something will take",
                    "Guessing how far away the park is, or how many steps to the door",
                    "Guessing how many are in a jar, a bowl, or a basket before counting",
                ],
                "conversation_starters": [
                    "About how many do you think are in there? What makes you guess that?",
                    "Do you think this will cost closer to ten dollars or twenty?",
                    "We got an answer of fifty. Does that seem about right to you?",
                ],
                "resource_bank": [
                    "A guessing jar kept filled and changed",
                    "The real estimating moments of shopping, cooking, and travel",
                    "Collections of things to guess at and count",
                ],
                "parent_role": "Wonder aloud about about-how-many and about-how-much as real questions come up in the day, and make a glad game of guessing and then finding out. Welcome every guess, celebrate a close one, and let the child see that estimation is a useful, everyday way of thinking, not a test.",
                "observation_documentation": "Over time, note whether the child estimates before counting, leans on benchmarks, comes reasonably close, and checks whether answers seem reasonable. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Estimating how long a book takes",
            "science": "Estimating before measuring",
            "history": "Estimating historical populations and distances",
        },
    },
    "mf-28": {
        "enriched": True,
        "learning_objectives": [
            "Know all number bonds to 20",
            "Use number bonds to solve addition and subtraction",
            "Understand part-whole relationships",
            "Represent number bonds visually",
        ],
        "teaching_guidance": {
            "introduction": "A number bond shows how a number breaks into two parts. 8 breaks into 3 and 5, or 4 and 4, or 6 and 2. Knowing all bonds for key numbers makes both addition and subtraction fast.",
            "scaffolding_sequence": [
                "Learn all bonds for 5: 0+5, 1+4, 2+3",
                "Learn all bonds for 10: 0+10, 1+9, 2+8, 3+7, 4+6, 5+5",
                "Learn bonds for 11-20",
                "Draw number bond diagrams",
                "Use bonds to solve: 10-7=? Bond is 7 and 3, answer is 3",
            ],
            "socratic_questions": [
                "What two numbers make 10? How many ways?",
                "If the whole is 15 and one part is 8, what is the other part?",
                "How does knowing bonds for 10 help you add 8+5?",
            ],
            "practice_activities": [
                "Number bond flash cards",
                "Ten-frame bonds: place counters and see how many empty",
                "Bond puzzles: fill in the missing part",
            ],
            "real_world_connections": [
                "Making change: costs 7, pay 10, change is 3",
                "Sharing: 12 items split two ways",
                "Recipes: need 10 cups total, have 6, need 4 more",
            ],
            "common_misconceptions": [
                "Only knowing bonds one way",
                "Not connecting bonds to subtraction",
                "Thinking bonds only apply to 10",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "States all bonds for 10 from memory",
                "Uses bonds to solve subtraction quickly",
                "Draws number bond diagrams correctly",
            ],
            "assessment_methods": ["oral bond recall", "diagram drawing", "problem solving"],
            "sample_assessment_prompts": ["Tell me all pairs that make 10", "Draw a bond for 14 with parts 6 and 8"],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "The whole is 10. One part is 6. What is the other part?",
                "expected_type": "number",
                "correct_answer": "4",
                "hints": ["6 + ? = 10"],
                "explanation": "4. The bond for 10 with 6 is 6 and 4.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What two numbers make 10? Give one pair.",
                "expected_type": "text",
                "correct_answer": "any valid pair like 3 and 7",
                "hints": ["Think: what + what = 10?"],
                "explanation": "Many answers: 1+9, 2+8, 3+7, 4+6, 5+5.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "The whole is 15. One part is 9. Other part?",
                "expected_type": "number",
                "correct_answer": "6",
                "hints": ["9 + ? = 15"],
                "explanation": "6. 9 + 6 = 15.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Use a number bond to solve 12 - 5.",
                "expected_type": "number",
                "correct_answer": "7",
                "hints": ["12 = 5 + ?"],
                "explanation": "7. The bond for 12 is 5 and 7.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "List ALL number bonds for 8.",
                "expected_type": "text",
                "hints": ["Start with 0+8 and work up"],
                "explanation": "0+8, 1+7, 2+6, 3+5, 4+4.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Name all pairs that make 10.",
                "type": "text",
                "rubric": "Mastery: all 6 pairs. Proficient: 4-5 pairs. Developing: 1-3 pairs.",
                "target_concept": "bonds_for_10",
            },
            {
                "prompt": "Whole is 16, one part is 9. Other part?",
                "type": "number",
                "correct_answer": "7",
                "target_concept": "number_bonds",
            },
            {
                "prompt": "How do number bonds help you subtract?",
                "type": "open_response",
                "rubric": "Mastery: explains subtraction as finding the other part. Proficient: gives example. Developing: cannot explain.",
                "target_concept": "bonds_and_subtraction",
            },
        ],
        "resource_guidance": {
            "required": ["number bond diagram templates"],
            "recommended": ["ten-frame boards", "bond flashcards"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Visual bond diagrams. Three-circle format is intuitive.",
            "adhd": "Bond games: flash whole, race to name parts. Quick-fire.",
            "gifted": "Bonds to 100. Three parts. Algebraic: a+b=15, a=7, b=?",
            "visual_learner": "Color bond diagrams. Part-whole mats. Visual cards.",
            "kinesthetic_learner": "Snap cube trains: break 12 into parts. Record. Break differently.",
            "auditory_learner": "Chant: 'Ten is five and five, six and four, seven and three.'",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "A number bond shows how a whole number breaks into two parts. Eight breaks into 3 and 5, into 4 and 4, into 6 and 2: each is a bond of eight. Knowing every bond for the key numbers, ten above all, makes both addition and subtraction quick, since each bond holds an addition fact and a subtraction fact at once. Today we learn the number bonds to twenty, draw them, and use them to add and subtract.",
                "gradual_release": {
                    "i_do": "Take ten counters and break them into two parts again and again, naming each bond: 6 and 4, 7 and 3, 5 and 5. Draw the three-part bond diagram, the whole above, the two parts below. Show that the bond of 7 and 3 within ten solves both 7 plus 3 and 10 minus 7.",
                    "we_do": "Break key numbers into all their bonds together, draw the bond diagrams, and use a known bond to solve an addition and a subtraction.",
                    "you_do": "Child states the bonds for ten and other key numbers, draws bond diagrams, and uses bonds to solve addition and subtraction.",
                },
                "guided_practice": [
                    "Break a whole into all its two-part bonds with counters",
                    "Draw number bond diagrams, the whole above and two parts below",
                    "Use a known bond to solve a subtraction: the whole and one part are given, find the other",
                ],
                "independent_practice": [
                    "Write all the number bonds for the key numbers up to twenty",
                    "Use bonds to solve mixed addition and subtraction problems",
                ],
                "mastery_check": [
                    "State all the bonds for ten from memory",
                    "Use a number bond to solve addition and subtraction",
                    "Draw a number bond diagram correctly, the whole and two parts",
                ],
                "spiral_review": [
                    "Revisit the make-ten addition facts, which are the number bonds for ten",
                ],
            },
            "classical": {
                "narrative_introduction": "Every whole number is made of parts, and to know a number truly is to know the parts that make it. This is the part-whole law: a whole and its two parts are bound together, and the bond holds three facts at once, for if any two are known the third is found. Hold all the bonds of ten and twenty firmly, and addition and subtraction both lie open.",
                "memory_work": {
                    "chants": [
                        "Chant the bonds of ten: ten is one and nine, two and eight, three and seven, four and six, five and five",
                        "Chant the part-whole law: the whole is the two parts joined, and a part is the whole less the other part",
                    ],
                    "recitations": [
                        "Recite that a number bond holds an addition fact and a subtraction fact together, and that to know the whole and one part is to know the other",
                    ],
                },
                "copywork": [
                    "Copy a number and all its bonds beneath it, neatly, the whole and each pair of parts set in order",
                ],
                "recitation_routine": "Begin each lesson by chanting the bonds of ten before any new bond is learned, so the key bonds are rehearsed cumulatively.",
                "history_integration": "Tell that the breaking of a whole into its parts is among the first truths of arithmetic, and that reckoners have always built swift calculation on the firm knowing of these small, sure facts.",
                "read_aloud_suggestions": [
                    "A story in which a whole group is split into two parts in different ways, read aloud so the child hears a number bond at work",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A beautifully illustrated counting or sharing book in which a group is split into two parts, with real artwork and never a worksheet",
                ],
                "short_lesson_flow": "Take a small handful of real things, perhaps ten acorns, and split them into two parts on the table. Name the bond: six and four. Gather them and split them another way. Let the child find, calmly, all the ways one number breaks in two. A few minutes is enough. Stop while interest holds.",
                "narration_prompt": "Tell me the ways we split the ten acorns. How many pairs of parts did you find?",
                "real_world_objects": [
                    "Ten or more real things to split into two parts: acorns, beads, buttons, shells",
                    "A ten-frame, or a board with ten spaces, to fill and see how many are empty",
                    "Two small bowls into which a whole is parted",
                ],
                "nature_connection": "Outdoors, gather a small number of like things and split the heap into two parts in every way it will go, finding all the bonds of that number among real leaves or stones.",
                "habit_focus": "The habit of attention: noticing that one whole holds many pairs of parts within it.",
            },
            "montessori": {
                "prepared_materials": [
                    "The addition strip board, on which a whole appears as two colored strips",
                    "The colored bead bars, joined with a golden ten-bar for the bonds beyond ten",
                    "Number bond diagram cards, a whole and its two parts",
                ],
                "presentation": {
                    "three_period_lesson": "With the bead bars making a whole: this is a bond of ten, six and four; show me a bond of ten; what bond is this?",
                    "steps": [
                        "Build a whole number with the bead bars or the strip board, then show its two parts",
                        "Find every way the whole breaks into two parts, naming each bond",
                        "Use a known bond to solve a subtraction: set the whole and one part, find the part that completes it",
                    ],
                },
                "control_of_error": "The materials are the control: the two part-strips must together exactly match the whole on the strip board, and the bead bars laid against the whole reveal at once when a pair of parts does not make it, so a wrong bond will not fit.",
                "abstraction_pathway": "From building a whole and breaking it into parts with the beads and strips, to drawing the bond diagram, toward holding all the bonds of ten and twenty in the mind and using them to reckon.",
                "extensions": [
                    "Find the bonds for the teen numbers and for twenty with the teen beads",
                    "Use bonds to solve subtraction by finding the missing part",
                    "Explore three-part bonds of a single whole",
                ],
                "observation_focus": "Watch for the child finding all the bonds of a number, not only one, and seeing that the whole and one part give the other.",
            },
            "unschooling": {
                "invitations": [
                    "Keep collections of small countable things, beads, coins, buttons, within reach for free splitting",
                    "Leave out a ten-frame or an egg carton trimmed to ten spaces to fill and split",
                    "Have paper handy for drawing the part-whole diagrams a child invents",
                ],
                "real_world_contexts": [
                    "Splitting a handful of snacks or toys into two shares",
                    "Making change: a thing costs seven, you pay ten, the change is three",
                    "Working out how many more are needed: ten cups in the recipe, six already in, four to go",
                    "Noticing the two parts of a full set, the eaten and the left",
                ],
                "conversation_starters": [
                    "You have ten. If some are here, how many are there?",
                    "What are all the ways you could split these into two groups?",
                    "If the whole is fifteen and this part is nine, what is the other part?",
                ],
                "resource_bank": [
                    "Collections of small things to split and combine",
                    "A ten-frame or egg carton for filling and parting",
                    "The real splitting and sharing of snacks, coins, and toys",
                ],
                "parent_role": "Notice the everyday moments when a whole is split into two parts, sharing, change, what is left, and wonder aloud about the parts and the whole. Let the child discover the many ways a number breaks in two by handling real things, rather than memorizing a table.",
                "observation_documentation": "Over time, note whether the child knows the parts that make ten and other numbers, sees that the whole and one part give the other, and uses these bonds to add and subtract. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Word families are like number bonds",
            "science": "Part-whole: legs on 3 insects (6+6+6)",
            "history": "Dividing groups: armies, resources",
        },
    },
    "mf-29": {
        "enriched": True,
        "learning_objectives": [
            "Sort objects by color, shape, size, and other attributes",
            "Classify objects into groups with clear rules",
            "Explain sorting rules",
            "Sort the same objects in different ways",
        ],
        "teaching_guidance": {
            "introduction": "Sorting and classifying is how we organize the world. Give the child a mixed collection and ask them to put things into groups. The key question: what is your RULE? Can you sort them a different way?",
            "scaffolding_sequence": [
                "Sort by one attribute: all reds together, all blues together",
                "Name the sorting rule",
                "Sort the same objects a different way",
                "Sort by two attributes: big AND red vs big AND blue",
                "Classify: does this object belong? Why?",
            ],
            "socratic_questions": [
                "What is your rule for these groups?",
                "Can you sort these a different way?",
                "Does this button belong in this group? Why?",
            ],
            "practice_activities": [
                "Button sorting: by color, then size, then shape",
                "Nature collection sorting: leaves by shape, size, color",
                "Venn diagram sorting: red objects, round objects, both",
            ],
            "real_world_connections": [
                "Sorting laundry: whites and colors",
                "Organizing toys into bins by type",
                "Grocery store aisles",
            ],
            "common_misconceptions": [
                "Changing the rule mid-sort",
                "Thinking there's only one right way",
                "Not being able to articulate the rule",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Sorts by at least 3 different attributes",
                "Explains sorting rule clearly",
                "Sorts same collection multiple ways",
            ],
            "assessment_methods": ["hands-on sorting", "rule explanation", "re-sorting challenge"],
            "sample_assessment_prompts": ["Sort these buttons. What's your rule?", "Now sort them a different way."],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "You have red, blue, and green blocks. How would you sort them into 3 groups?",
                "expected_type": "text",
                "correct_answer": "by color",
                "hints": ["What's different about them?"],
                "explanation": "Sort by color: reds together, blues together, greens together.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You sorted shapes by color. Now sort them a DIFFERENT way. What would you use?",
                "expected_type": "text",
                "hints": ["What else is different besides color?"],
                "explanation": "By shape or by size.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "A group has: big red circle, big blue circle, small red square. Which doesn't belong if the rule is 'circles only'?",
                "expected_type": "text",
                "correct_answer": "small red square",
                "hints": ["Which is not a circle?"],
                "explanation": "The small red square.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "You have 12 objects: some big, some small, some red, some blue. Sort into 4 groups using TWO attributes.",
                "expected_type": "text",
                "hints": ["Big red, big blue, small red, small blue"],
                "explanation": "Four groups: big+red, big+blue, small+red, small+blue.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Sort these 10 objects. Explain your rule.",
                "type": "open_response",
                "rubric": "Mastery: clear groups with stated rule. Proficient: consistent groups, vague rule. Developing: inconsistent groups.",
                "target_concept": "sorting",
            },
            {
                "prompt": "Now sort the same objects a different way.",
                "type": "open_response",
                "rubric": "Mastery: completely different attribute. Proficient: different but similar rule. Developing: cannot re-sort.",
                "target_concept": "multiple_classifications",
            },
        ],
        "resource_guidance": {
            "required": ["mixed collection of sortable objects"],
            "recommended": ["sorting mats", "Venn diagram circles"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Non-reading. Real objects with obvious visual/tactile differences.",
            "adhd": "Sort real collections they care about: LEGO, cards, rocks.",
            "gifted": "Two-attribute Venn. Hierarchies. Design own sorting rules.",
            "visual_learner": "Sorting mats with labeled columns. Color-coded categories.",
            "kinesthetic_learner": "Handle and move every object. Sort into containers.",
            "auditory_learner": "State rule aloud: 'My rule is SHAPE. Circles here, squares here.'",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Sorting is putting things into groups by what they share. Classifying is the same with a clear, stated rule. The most important question is, what is your rule. A good sorter can name the rule, keep to it through the whole sort, and then sort the same things again by a different rule. Today we sort objects by color, shape, size, and other attributes, name our rules, and sort the same collection in more than one way.",
                "gradual_release": {
                    "i_do": "Take a mixed collection and sort it by one attribute, all the red things together, all the blue, naming the rule aloud: my rule is color. Then gather them and sort the very same things a different way, by shape. Show plainly that the rule must hold for every object, start to finish.",
                    "we_do": "Sort a collection together by one attribute, name the rule, check that every object obeys it, then sort the same collection again by a different attribute.",
                    "you_do": "Child sorts a collection by an attribute, names the rule, and sorts the same objects again a different way.",
                },
                "guided_practice": [
                    "Sort a collection by one attribute and name the rule",
                    "Sort the same collection again by a different attribute",
                    "Decide whether an object belongs in a group and say why",
                ],
                "independent_practice": [
                    "Sort a collection by three different attributes in turn, naming each rule",
                    "Sort by two attributes at once: big and red, big and blue, small and red, small and blue",
                ],
                "mastery_check": [
                    "Sort a collection by at least three different attributes",
                    "Explain the sorting rule clearly",
                    "Sort the same collection in more than one way",
                ],
                "spiral_review": [
                    "Revisit naming the attributes of objects: color, shape, and size",
                ],
            },
            "classical": {
                "narrative_introduction": "To classify is to bring order to a heap of things, and orderly knowledge begins here. The mind looks at many objects and asks, by what shall these be grouped, and having chosen, holds to that rule with discipline. Yet the same things may be ordered by another rule entirely, and the wise sorter knows that the rule is chosen, not given.",
                "memory_work": {
                    "chants": [
                        "Chant the sorter's question: by what rule shall these be grouped, color, shape, or size",
                        "Chant the sorter's discipline: name the rule, hold the rule, and let it govern every object",
                    ],
                    "recitations": [
                        "Recite that to classify is to group by a stated rule, and that one collection may be sorted truly in many ways",
                    ],
                },
                "copywork": [
                    "Copy the names of the attributes, color, shape, and size, and beside each a thing it could sort",
                ],
                "recitation_routine": "Begin each lesson by reciting the attributes by which things may be sorted before any new sorting work.",
                "history_integration": "Tell that the ordering of things into kinds is the beginning of every science, that scholars of old set the plants, the animals, and the stars each into their classes, and that all systematic knowledge rests on such sorting.",
                "read_aloud_suggestions": [
                    "A story or true account in which things are gathered and set in order, read aloud so the child hears classification at work",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A beautifully illustrated book about nature's variety, leaves, shells, birds, that invites the child to notice and group, never a workbook",
                ],
                "short_lesson_flow": "Bring in a real collection, perhaps leaves or shells gathered on a walk, and let the child handle them and group them however they wish. Ask gently, what is your rule. Then wonder together whether they could be grouped another way. Keep it calm and unhurried, and let the child's own noticing lead.",
                "narration_prompt": "Tell me how you grouped your collection. What was your rule? Could you group it another way?",
                "real_world_objects": [
                    "A real collection from a nature walk: leaves, shells, stones, seed pods",
                    "Buttons, beads, or the family's own household objects to group",
                    "Sorting trays or small bowls to hold the groups",
                ],
                "nature_connection": "On a nature walk, gather one kind of thing, leaves or stones, and at home sort them by shape, by size, by color, noticing nature's variety and recording the groups in the nature notebook.",
                "habit_focus": "The habit of attention and order: looking closely enough to see how things are alike and unlike, and arranging them with care.",
            },
            "montessori": {
                "prepared_materials": [
                    "Sorting trays and baskets of objects that vary by one clear attribute at a time",
                    "Real practical-life materials, buttons, beans, spoons, to sort",
                    "The geometric cabinet and color tablets, which classify by shape and by color",
                ],
                "presentation": {
                    "three_period_lesson": "With a sorted collection: this group is sorted by color; show me a group sorted by color; by what rule is this group sorted?",
                    "steps": [
                        "Choose a collection and sort it by a single attribute into its groups",
                        "Name the rule, and check that every object in each group obeys it",
                        "Gather the collection and sort it again by a different attribute",
                    ],
                },
                "control_of_error": "The collection itself is the control: an object that does not match the others in its group stands out plainly to the eye, and the child, looking, sees the misfit and moves it without being told.",
                "abstraction_pathway": "From sorting concrete objects by one plain attribute, to sorting by two attributes at once, toward classifying by a rule chosen and named in the mind.",
                "extensions": [
                    "Sort by two attributes at once, and explore overlapping groups",
                    "Classify a collection in a hierarchy, broad groups divided into smaller ones",
                    "Sort the natural and made objects of the whole prepared environment",
                ],
                "observation_focus": "Watch for the child holding to one rule through a whole sort, naming it, and seeing that the same collection can be sorted truly in more than one way.",
            },
            "unschooling": {
                "invitations": [
                    "Keep collections the child loves, rocks, cards, toy animals, in open trays for free sorting",
                    "Leave out bowls, trays, and bins that invite grouping",
                    "Let the child take part in the real sorting work of the household",
                ],
                "real_world_contexts": [
                    "Sorting the laundry into whites and colors",
                    "Putting toys away into bins by type",
                    "Sorting the recycling, the cutlery drawer, or a button jar",
                    "Organizing a collection: cards, stickers, rocks, figures",
                ],
                "conversation_starters": [
                    "How did you decide which things go together? What is your rule?",
                    "Could you sort these a completely different way?",
                    "Does this one belong in this group? Why, or why not?",
                ],
                "resource_bank": [
                    "The child's own collections, kept where they can be sorted freely",
                    "Trays, bowls, and bins for grouping",
                    "The real sorting tasks of everyday life",
                ],
                "parent_role": "Welcome the child into the real sorting work of the home, and notice aloud the many ways a thing could be grouped. Ask about the child's rule with genuine curiosity, and let their own collections and their own logic, rather than a worksheet, be where sorting is practiced.",
                "observation_documentation": "Over time, note whether the child sorts by various attributes, holds to a rule through a whole sort, can say what the rule is, and sees that one collection may be grouped in many ways. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Sorting words by beginning sound or family",
            "science": "Classification is core science: living things, rocks, materials",
            "history": "Categorizing artifacts, cultures, time periods",
        },
    },
    "mf-30": {
        "enriched": True,
        "learning_objectives": [
            "Demonstrate mastery of all foundational math skills",
            "Apply skills to novel problems",
            "Explain mathematical thinking clearly",
            "Show confidence with numbers",
        ],
        "teaching_guidance": {
            "introduction": "This is a comprehensive review and celebration of everything learned. It's not a stressful test. It's a chance for the child to show how much they've grown. Mix oral, written, and hands-on tasks. Celebrate what they know.",
            "scaffolding_sequence": [
                "Warm up with favorite activities from earlier topics",
                "Work through a mix of problems covering all major areas",
                "Include both computation and word problems",
                "End with a challenging problem that connects multiple skills",
                "Celebrate completion and discuss what the child is most proud of",
            ],
            "socratic_questions": [
                "Which math skill are you most proud of learning?",
                "What was the hardest thing you learned? What made it click?",
                "What do you want to learn next in math?",
            ],
            "practice_activities": [
                "Math portfolio review: look at early work and compare to now",
                "Mixed practice: 2-3 problems from each major topic",
                "Create a 'math book' showing what you know",
            ],
            "real_world_connections": [
                "Plan a simple party: count guests, calculate supplies needed",
                "Set up a pretend store: price items, make change",
                "Measure and draw a map of your room",
            ],
            "common_misconceptions": [
                "Test anxiety: frame as celebration, not judgment",
                "Thinking they need to be perfect",
                "Forgetting strategies under pressure",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Scores 80%+ across all foundational skill areas",
                "Explains at least 2 strategies clearly",
                "Applies math to a real-world scenario",
            ],
            "assessment_methods": ["mixed computation", "word problems", "oral explanation", "hands-on tasks"],
            "sample_assessment_prompts": [
                "Solve 5 computation problems from different topics",
                "Solve 2 word problems",
                "Explain how you solved your favorite problem",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is 8 + 6?",
                "expected_type": "number",
                "correct_answer": "14",
                "hints": ["Make ten: 8+2=10, then 4 more"],
                "explanation": "14.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is 15 - 7?",
                "expected_type": "number",
                "correct_answer": "8",
                "hints": ["Think: 7 + ? = 15"],
                "explanation": "8.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What number has 7 tens and 3 ones?",
                "expected_type": "number",
                "correct_answer": "73",
                "hints": ["7 tens = 70, plus 3"],
                "explanation": "73.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You have 2 dimes and 3 nickels. How many cents?",
                "expected_type": "number",
                "correct_answer": "35",
                "hints": ["2 dimes = 20 cents. 3 nickels = 15 cents."],
                "explanation": "20 + 15 = 35 cents.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "You have 16 stickers. You want to share them equally with a friend. How many does each person get? Is it an even split?",
                "expected_type": "text",
                "hints": ["16 divided into 2 equal groups"],
                "explanation": "8 each. 16 is even, so it splits equally: 8 and 8.",
            },
        ],
        "assessment_items": [
            {"prompt": "Solve: 9 + 7", "type": "number", "correct_answer": "16", "target_concept": "addition_to_20"},
            {
                "prompt": "Solve: 13 - 5",
                "type": "number",
                "correct_answer": "8",
                "target_concept": "subtraction_within_20",
            },
            {
                "prompt": "Write 86 in expanded form.",
                "type": "text",
                "correct_answer": "80 + 6",
                "target_concept": "place_value",
            },
            {
                "prompt": "Order least to greatest: 52, 25, 48, 84",
                "type": "text",
                "correct_answer": "25, 48, 52, 84",
                "target_concept": "ordering",
            },
            {
                "prompt": "What is your favorite math strategy? Explain how it works.",
                "type": "open_response",
                "rubric": "Mastery: names a real strategy, explains clearly with example. Proficient: names strategy with partial explanation. Developing: cannot name a strategy.",
                "target_concept": "mathematical_thinking",
            },
        ],
        "resource_guidance": {
            "required": ["all previously used materials available for reference"],
            "recommended": ["portfolio of past work for comparison"],
        },
        "time_estimates": {"first_exposure": 30, "practice_session": 20, "assessment": 20},
        "accommodations": {
            "dyslexia": "Oral assessment options for every section. No writing barriers.",
            "adhd": "3-4 short sessions across 2 days. Movement breaks between.",
            "gifted": "Challenge problems into developing level. Show their ceiling.",
            "visual_learner": "Manipulatives, diagrams, picture-based problems available.",
            "kinesthetic_learner": "Hands-on stations: build with blocks, measure, sort.",
            "auditory_learner": "Oral narration: tell everything about addition. Verbal demo.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "This is the capstone review of the foundational math level. It is not a stressful test but a comprehensive check and a celebration: a chance for the child to show, across all the major areas, how much they have grown. We mix oral, written, and hands-on tasks covering counting, place value, addition and subtraction, money, fractions, and more, and we end by celebrating what the child knows.",
                "gradual_release": {
                    "i_do": "Explain warmly that this is a showing of all that has been learned, not a trial, and model the spirit of it by working a problem aloud, naming the strategy and showing calm, confident thinking.",
                    "we_do": "Warm up together with a favorite activity from an earlier topic, and talk through what the review will cover so the child meets each part without surprise.",
                    "you_do": "Child works independently through a mix of computation, word problems, and hands-on tasks across all foundational areas, and explains their mathematical thinking, while the parent notes what is solid and what needs more practice.",
                },
                "guided_practice": [
                    "Warm up with a favorite activity from an earlier topic",
                    "Work a mix of problems covering each major area, with light support where needed",
                    "Explain aloud the thinking behind a solved problem",
                ],
                "independent_practice": [
                    "Work through computation and word problems independently across all areas",
                    "Apply math to a real-world task: plan a small party, run a pretend store, measure a room",
                ],
                "mastery_check": [
                    "Show mastery across all foundational skill areas",
                    "Apply skills to a novel problem and to a real-world scenario",
                    "Explain mathematical thinking and at least two strategies clearly",
                ],
                "spiral_review": [
                    "Revisit any skill area found not yet solid before moving to the developing level",
                ],
            },
            "classical": {
                "narrative_introduction": "Every stage of learning closes with a gathering-up of what has been won, and this is that moment for foundational mathematics. It is no trial to be feared but a gateway: a comprehensive showing of counting, place value, calculation, money, and measure, and an honest judgment that the child stands ready for the developing level. The assessment opens the gate; it does not bar it.",
                "memory_work": {
                    "chants": [
                        "Recite again the cornerstones of the foundational level: counting and place value, addition and subtraction, money, fractions, and patterns",
                        "Recite the marks of a mathematician: to reckon truly, to reason through a problem, and to explain the thinking",
                    ],
                    "recitations": [
                        "Recite the number facts and the strategies built across the level, the gathered fruit of the year's work",
                    ],
                },
                "recitation_routine": "Make the review itself a cumulative recitation: the child reckons and reasons, drawing on every skill built across the foundational level, oldest and newest together.",
                "history_integration": "Tell that learning has always been marked by such gateways, that in older schooling a stage was completed and confirmed before the next began, and that to pass this gate is to take up the long tradition of those who reason with number.",
                "read_aloud_suggestions": [
                    "A story of a problem reasoned through with number, read aloud so the child hears mathematics put to confident use",
                    "A more challenging book of mathematical puzzles, held ready as a reward of the developing level to come",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A beautifully illustrated book of real mathematical interest, held ready as the first of the developing level",
                    "The child's own math notebook, looked through together to see the year's growth",
                ],
                "short_lesson_flow": "There is no stressful test. Over an ordinary day or two, set the child a few real, worthy problems, some oral, some with real objects, and let them work and narrate their thinking. You will see at once what is sure and what is still tender. Frame the whole as a glad showing of how far they have come, and end by celebrating it together.",
                "narration_prompt": "Tell me how you solved that. Which math do you feel surest of now, and what are you proudest of learning this year?",
                "real_world_objects": [
                    "Real objects for hands-on tasks: coins, counters, a ruler, things to sort and measure",
                    "The child's own math notebook, showing the year's work from first to last",
                    "A real task to carry out: planning a small celebration, measuring a room, running a pretend shop",
                ],
                "nature_connection": "Set a closing task out of doors: measure the garden bed, count and sort a nature collection, or tally the birds, so the child shows their mathematics among the living things they love.",
                "habit_focus": "The habit of attention and of confidence: meeting a problem calmly, reasoning it through, and trusting the mind that has been trained all year.",
            },
            "montessori": {
                "prepared_materials": [
                    "The familiar mathematics materials of the foundational level, used now as the child works, not as a test",
                    "Real tasks and problem cards spanning all the major areas",
                    "The child's own ongoing work record kept across the level",
                ],
                "presentation": {
                    "three_period_lesson": "There is no new naming here; instead the adult watches the child in the third period of every lesson long since given, recalling and applying number, operation, and measure independently in real work.",
                    "steps": [
                        "The adult prepares the environment with the full range of materials and real tasks, and observes the child at work",
                        "The adult notes which skills, counting, place value, calculation, money, fractions, the child applies fluently and independently",
                        "The adult and child review the work record together and see that the foundational mathematics is complete",
                    ],
                },
                "control_of_error": "The materials are the control, as they have always been: in real work a skill not yet secure reveals itself plainly through the material, with no test required, so the adult's judgment rests on what the child actually does.",
                "abstraction_pathway": "From the concrete materials of the foundational level long since internalized, the child has reached confident, abstract reckoning; this review simply confirms that the abstraction is complete and the next stage may begin.",
                "extensions": [
                    "Move into the developing level's work without delay once competence is observed",
                    "Carry the work record forward into the next stage",
                    "Let the child set their own mathematical work and goals for the level to come",
                ],
                "observation_focus": "Watch, across the child's ordinary work, for sound counting and place value, fluent calculation, and reasoning applied to novel and real problems, the signs that the foundational level is truly complete.",
            },
            "unschooling": {
                "invitations": [
                    "Keep math present in everyday life: coins, measuring tools, dice, games, things to count and sort",
                    "Leave out richer, more challenging math materials and puzzles for when the child reaches for them",
                    "Let the child take a real part in the cooking, building, shopping, and planning of the household",
                ],
                "real_world_contexts": [
                    "Counting and making change in real shopping",
                    "Measuring and halving while cooking and building",
                    "Keeping score and reckoning in games",
                    "Planning a real event: how many guests, how much food, how much it costs",
                ],
                "conversation_starters": [
                    "How did you figure that out? Tell me your way.",
                    "What math do you find easy now that used to be hard?",
                    "What would you like to be able to do with numbers next?",
                ],
                "resource_bank": [
                    "The math of everyday life: money, cooking, building, games, time",
                    "Richer math materials and puzzles kept within reach",
                    "An adult who reckons aloud and welcomes the child into real math tasks",
                ],
                "parent_role": "There is no test. You already know your child's mathematics, because you see them use it, counting change, halving a recipe, keeping score, measuring a shelf. Notice that competence and confidence as they show themselves in real life, follow the child into richer math as their own appetite grows, and trust what you have watched unfold.",
                "observation_documentation": "Over time, simply note the math the child uses in the course of real life: whether they count and calculate with confidence, reason through new problems, explain their thinking, and reach without prompting for harder challenges. This lived noticing, not any test, shows that the foundational mathematics is sound and the child is ready for whatever comes next.",
            },
        },
        "connections": {
            "reading": "Reading word problems on assessment",
            "science": "Measurement and data sections connect to science",
            "history": "Timeline and ordering connect to historical sequencing",
        },
    },
    "mf-31": {
        "enriched": True,
        "learning_objectives": [
            "Count a set of up to five objects, touching each object exactly once",
            "Say the number words 1 through 5 in the correct fixed order",
            "Match each spoken number word to one object (one-to-one correspondence)",
            "Answer how many are in a set of one to five after counting",
        ],
        "teaching_guidance": {
            "introduction": "Counting begins by touching one object as we say one number. Today we count small sets up to five, saying one number word for each thing we touch, in the steady order one, two, three, four, five.",
            "scaffolding_sequence": [
                "Count sets of two and three objects, touching each once",
                "Count a set of four, then a set of five, lined up in a row",
                "Count five objects in a scattered pile by moving each to a counted group",
            ],
            "socratic_questions": [
                "Did you touch every one exactly once?",
                "What was the last number you said? So how many are there?",
                "What number comes right after three when we count?",
            ],
            "practice_activities": [
                "Touch-and-count rows of two to five counters",
                "Move objects one at a time into a counted pile while saying each number",
                "Count fingers held up, one to five",
            ],
            "real_world_connections": [
                "Counting out five crackers for a snack",
                "Counting the buttons on a shirt up to five",
                "Counting toes on one foot",
            ],
            "common_misconceptions": [
                "Skipping an object or counting one twice; address by having the child slide each object to a 'counted' pile as it is counted",
                "Reciting numbers faster than touching; address by slowing to one touch per word, hand over hand if needed",
                "Not knowing the last number tells the total; address by asking 'how many?' right after counting and accepting only the last count word",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Counts any set of one to five with accurate one-to-one correspondence",
                "Says 1 to 5 in order from memory",
                "States the total as the last number counted",
            ],
            "assessment_methods": ["object counting", "oral counting", "observation"],
            "sample_assessment_prompts": [
                "Count these four blocks for me, touching each one",
                "Show me five fingers and count them",
                "How many bears are here? Count them",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Count these stars: * * *  How many are there?",
                "expected_type": "number",
                "correct_answer": "3",
                "hints": ["Touch each star as you say a number"],
                "explanation": "There are 3 stars: 1, 2, 3.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Count these dots: . . . . How many?",
                "expected_type": "number",
                "correct_answer": "4",
                "hints": ["Point to each dot once"],
                "explanation": "There are 4 dots.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Hold up 5 fingers and count them. How many?",
                "expected_type": "number",
                "correct_answer": "5",
                "hints": ["One number for each finger"],
                "explanation": "Five fingers: 1, 2, 3, 4, 5.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "There are 2 red blocks and you add 1 more. Count them all. How many?",
                "expected_type": "number",
                "correct_answer": "3",
                "hints": ["Count the blocks you can see, one touch each"],
                "explanation": "2 blocks and 1 more makes 3 when you count them.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Count these in a circle: o o o o o  How many?",
                "expected_type": "number",
                "correct_answer": "5",
                "hints": ["Pick a starting one and go around once; remember where you began"],
                "explanation": "Going around once and stopping where you started gives 5.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Point to and count the four corners of a square. What number do you end on?",
                "expected_type": "text",
                "hints": ["Touch one corner at a time"],
                "explanation": "You end on 4, because a square has four corners: 1, 2, 3, 4.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Some buttons are mixed in a pile of 5. Tell how you would count them without missing any.",
                "expected_type": "text",
                "hints": [
                    "Think about moving each button as you count",
                    "How do you make sure you do not count one twice?",
                ],
                "explanation": "Slide each button to a new pile as you count it; when the first pile is empty you have counted every one, ending at 5.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Count out loud from 1 to 5 and then tell which number is the biggest of these.",
                "expected_type": "text",
                "hints": ["The last number you say is the largest here"],
                "explanation": "Counting 1, 2, 3, 4, 5; the largest is 5 because it comes last.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Count these objects and write the number: # # #",
                "type": "number",
                "target_concept": "count_to_5",
                "correct_answer": "3",
            },
            {
                "prompt": "Count these objects and write the number: # # # # #",
                "type": "number",
                "target_concept": "count_to_5",
                "correct_answer": "5",
            },
            {
                "prompt": "Say the numbers from 1 to 5 in order.",
                "type": "open_response",
                "target_concept": "counting_order",
                "rubric": "Mastery: 1-5 in order, no errors. Proficient: one self-correction. Developing: misses or reorders a number.",
            },
            {
                "prompt": "How many fingers are on one hand? Count them.",
                "type": "number",
                "target_concept": "cardinality",
                "correct_answer": "5",
            },
            {
                "prompt": "How do you make sure you count every object only once?",
                "type": "open_response",
                "target_concept": "counting_strategy",
                "rubric": "Mastery: explains touching/moving each once. Proficient: mentions being careful. Developing: cannot explain.",
            },
        ],
        "resource_guidance": {
            "required": ["small counting objects (up to 5 per set)", "child's own hands"],
            "recommended": ["five-frame card", "large soft counters"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 8},
        "accommodations": {
            "dyslexia": "Keep to oral counting and touching; no numeral writing yet. Use objects of one color to reduce visual load.",
            "adhd": "Very short bursts of 3-5 minutes. Count while clapping or tapping each object.",
            "gifted": "Extend immediately to counting sets of up to ten and counting two small sets to compare.",
            "visual_learner": "Line objects on a five-frame so the quantity is seen at a glance.",
            "kinesthetic_learner": "Move each object into a pile while counting; count steps or jumps to five.",
            "auditory_learner": "Chant 1-2-3-4-5 rhythmically; clap on each number.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Counting means one number word for one object. Today we count sets up to five and say how many in all.",
                "gradual_release": {
                    "i_do": "Model counting three counters aloud, touching each once, then say three tells how many in all.",
                    "we_do": "Count a set of four and then five together, the child touching while you say the words, then swap roles.",
                    "you_do": "Child counts sets of three, four, and five independently and says how many each time.",
                },
                "guided_practice": [
                    "Touch-count rows of counters with the teacher confirming each touch",
                    "Match a set to the spoken number word",
                ],
                "independent_practice": [
                    "Count five small piles set out on the table",
                    "Count fingers and toes up to five",
                ],
                "mastery_check": [
                    "Count five objects with one-to-one correspondence",
                    "Say 1 to 5 in order",
                    "State the total after counting",
                ],
                "spiral_review": [
                    "Re-count the first five of a larger set toward counting to 20 (mf-01) to keep one-to-one touch steady"
                ],
            },
            "classical": {
                "narrative_introduction": "Before great towers of numbers can be built, the first five stones must be set true. We learn one, two, three, four, five so surely they never wobble.",
                "memory_work": {
                    "chants": [
                        "Forward chant 1 to 5, clear and steady, daily",
                        "Echo chant: the teacher says a number, the child says the next",
                    ],
                    "recitations": ["A short five-count finger rhyme recited at the start of math time"],
                },
                "recitation_routine": "Begin each lesson by reciting yesterday's count to five before counting any objects, so the order is reviewed cumulatively.",
                "history_integration": "Count five marks on a simple line for the child's own age, tying small numbers to the start of a timeline.",
                "read_aloud_suggestions": [
                    "A gentle counting picture book read aloud, pausing to count to five together"
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 8,
                "living_book_suggestions": [
                    "A single beautiful counting picture book with real, lovely pictures, never a busy workbook"
                ],
                "short_lesson_flow": "Bring out a small basket of five real objects (acorns, shells). Count them once, calmly, together, then stop while interest is high.",
                "narration_prompt": "Tell me about the things we counted. How many were there?",
                "real_world_objects": [
                    "Five acorns gathered on a walk",
                    "Five place settings being laid",
                    "Five stairs counted while climbing",
                ],
                "nature_connection": "On the next nature walk, count five found things and lay them in a row to admire.",
                "habit_focus": "The habit of attention: touch each thing once, count to the end without rushing.",
            },
            "montessori": {
                "prepared_materials": [
                    "Number rods 1 to 5 (length shows quantity)",
                    "Sandpaper numerals 1 to 5",
                    "Cards and counters for one to five",
                ],
                "presentation": {
                    "three_period_lesson": "Naming: place three counters, this is three. Recognition: show me three. Recall: how many is this? Move slowly to the third period.",
                    "steps": [
                        "Lay out a small quantity of counters",
                        "Count them by touching each once",
                        "Pair counters to self-check; a leftover reveals a miscount",
                    ],
                },
                "control_of_error": "With a fixed quantity of counters, a miscount leaves a leftover or a gap the child sees and corrects.",
                "abstraction_pathway": "From rods felt as length, to counters touched, toward holding the small quantity in mind.",
                "extensions": [
                    "Build the numbers one to five with the number rods",
                    "Find sets of five things around the room",
                ],
                "observation_focus": "Watch for steady touching, one per word, and the child choosing to repeat the work.",
            },
            "unschooling": {
                "invitations": [
                    "Leave a small bowl of five smooth stones within reach",
                    "Set out five blocks on a low shelf and say nothing",
                ],
                "real_world_contexts": [
                    "Handing out five crackers, one to each person",
                    "Counting five steps up to the door",
                    "Counting five toes during bath time",
                ],
                "conversation_starters": [
                    "I wonder how many stones are in the bowl?",
                    "Can you give everyone one cracker?",
                ],
                "resource_bank": [
                    "A counting picture book left available",
                    "A bowl of interesting small objects to handle",
                ],
                "parent_role": "Notice where small counting already happens in the day and join it; answer real questions, count aloud yourself, and let curiosity lead.",
                "observation_documentation": "Over days, jot how high the child counts confidently and whether each object gets one touch; this replaces any test.",
            },
        },
        "connections": {
            "reading": "Number words one to five as early sight words",
            "science": "Counting a few specimens found outdoors",
            "history": "Counting small sets of years on a personal timeline",
        },
    },
    "mf-32": {
        "enriched": True,
        "learning_objectives": [
            "Count a set of up to ten objects with one-to-one correspondence",
            "Say the number words 1 through 10 in the correct order",
            "State how many are in a set of up to ten after counting",
            "Count ten objects arranged in a line and in a scattered pile",
        ],
        "teaching_guidance": {
            "introduction": "Now we count further, all the way to ten. We still touch one object for each number word, in the steady order one through ten, and the last number tells how many.",
            "scaffolding_sequence": [
                "Count six and seven objects in a row",
                "Count eight, nine, then ten in a row",
                "Count ten objects scattered, moving each to a counted pile",
            ],
            "socratic_questions": [
                "How do you know you reached ten and not nine?",
                "What is the last number you said? How many is that?",
                "Which number comes right after seven?",
            ],
            "practice_activities": [
                "Touch-count rows of six to ten counters",
                "Count ten objects into an egg-carton row",
                "Count to ten on fingers, both hands",
            ],
            "real_world_connections": [
                "Counting ten crackers for snack",
                "Counting ten steps up the stairs",
                "Counting ten toys into a basket",
            ],
            "common_misconceptions": [
                "Losing track past five; address by grouping into a five and then counting on",
                "Saying numbers faster than touching past five; address by one touch per word, slowing down",
                "Recounting from one when asked 'how many'; address by accepting the last count word as the total",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Counts any set up to ten with one-to-one correspondence",
                "Says 1-10 from memory",
                "States the total as the last number",
            ],
            "assessment_methods": ["object counting", "oral counting", "observation"],
            "sample_assessment_prompts": [
                "Count these eight beads",
                "Show ten fingers and count them",
                "How many shells are in this pile?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Count these dots: . . . . . . How many?",
                "expected_type": "number",
                "correct_answer": "6",
                "hints": ["Touch each dot once"],
                "explanation": "There are 6 dots.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Count to 10 on your fingers. How many fingers?",
                "expected_type": "number",
                "correct_answer": "10",
                "hints": ["Both hands, one number each"],
                "explanation": "Ten fingers in all.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Count these stars: * * * * * * * How many?",
                "expected_type": "number",
                "correct_answer": "7",
                "hints": ["Point to each star once"],
                "explanation": "There are 7 stars.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "There are 9 blocks. Count them and tell how many.",
                "expected_type": "number",
                "correct_answer": "9",
                "hints": ["Slide each block as you count"],
                "explanation": "Counting all of them gives 9.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Count these scattered o o o o o o o o. How many?",
                "expected_type": "number",
                "correct_answer": "8",
                "hints": ["Move each to a counted pile so none is missed"],
                "explanation": "Moving each once gives 8.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Count from 1 to 10 out loud, then tell which number comes just before 10.",
                "expected_type": "text",
                "hints": ["Listen for the number right before ten"],
                "explanation": "Counting 1-10, the number just before 10 is 9.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "You counted a pile and reached 10. A friend says it is 9. How could you check who is right?",
                "expected_type": "text",
                "hints": ["Could you count again, moving each one?"],
                "explanation": "Count again carefully, moving each object once; the last number you reach is the true total.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Count a set of 10 by first making a group of 5, then counting on. Tell how you did it.",
                "expected_type": "text",
                "hints": ["Five first, then keep going: 6, 7, 8, 9, 10"],
                "explanation": "Make five, then count on 6, 7, 8, 9, 10 to reach ten without losing track.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Count these objects and write the number: # # # # # #",
                "type": "number",
                "target_concept": "count_to_10",
                "correct_answer": "6",
            },
            {
                "prompt": "Count these objects and write the number: # # # # # # # # # #",
                "type": "number",
                "target_concept": "count_to_10",
                "correct_answer": "10",
            },
            {
                "prompt": "Count these objects and write the number: # # # # # # # #",
                "type": "number",
                "target_concept": "count_to_10",
                "correct_answer": "8",
            },
            {
                "prompt": "Say the numbers from 1 to 10 in order.",
                "type": "open_response",
                "target_concept": "counting_order",
                "rubric": "Mastery: 1-10 in order, no errors. Proficient: one self-correction. Developing: misses or reorders a number.",
            },
            {
                "prompt": "How do you keep from losing count when you reach a big pile?",
                "type": "open_response",
                "target_concept": "counting_strategy",
                "rubric": "Mastery: explains moving/grouping each once. Proficient: mentions care. Developing: cannot explain.",
            },
        ],
        "resource_guidance": {
            "required": ["counting objects (up to 10 per set)", "ten-frame or egg carton"],
            "recommended": ["ten-frame card", "large counters"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 8},
        "accommodations": {
            "dyslexia": "Oral and touch counting; no numeral writing required. Use single-color objects.",
            "adhd": "Short 5-minute bursts; count while clapping or stepping.",
            "gifted": "Extend to counting to twenty and counting two sets to compare totals.",
            "visual_learner": "Use a ten-frame so ten is seen as full at a glance.",
            "kinesthetic_learner": "Move each object into a pile; count ten jumps or claps.",
            "auditory_learner": "Chant 1-10 rhythmically; sing a counting song to ten.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "We count to ten by touching one object per number, and the last number tells how many.",
                "gradual_release": {
                    "i_do": "Model counting seven counters aloud, touching each once, then say seven in all.",
                    "we_do": "Count eight and then ten together, child touching while you say words, then swap.",
                    "you_do": "Child counts sets of six, eight, and ten independently and states each total.",
                },
                "guided_practice": [
                    "Touch-count rows of six to ten with the teacher confirming",
                    "Match a set up to ten to its spoken number",
                ],
                "independent_practice": ["Count ten small piles on the table", "Count to ten on fingers and toes"],
                "mastery_check": [
                    "Count ten objects with one-to-one correspondence",
                    "Say 1-10 in order",
                    "State the total after counting",
                ],
                "spiral_review": [
                    "Re-count a set of five (mf-31) first, then count on to ten to keep one-to-one touch steady"
                ],
            },
            "classical": {
                "narrative_introduction": "The count grows from five to ten. Once these ten are sure, the hand of arithmetic has all its fingers.",
                "memory_work": {
                    "chants": ["Forward chant 1 to 10 daily, clear and rhythmic", "Echo chant numbers six to ten"],
                    "recitations": ["A ten-count finger rhyme recited at the start of math time"],
                },
                "recitation_routine": "Begin each lesson by reciting the count to five from yesterday before extending to ten, reviewing cumulatively.",
                "history_integration": "Count ten marks on a simple line, one per year, extending the personal timeline.",
                "read_aloud_suggestions": ["A rhythmic counting-to-ten picture book read aloud with expression"],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": ["A lovely counting picture book that reaches ten with real, calm pictures"],
                "short_lesson_flow": "Bring out ten real objects in a basket. Count them once together, calmly, then stop while interest holds.",
                "narration_prompt": "Tell me about what we counted. How many were there altogether?",
                "real_world_objects": [
                    "Ten acorns gathered outdoors",
                    "Ten beans set in a row",
                    "Ten steps counted while walking",
                ],
                "nature_connection": "On a walk, count a set of ten found things and lay them in a row in the nature notebook.",
                "habit_focus": "The habit of attention: count carefully all the way to ten without rushing or losing the place.",
            },
            "montessori": {
                "prepared_materials": [
                    "Number rods 1 to 10",
                    "Sandpaper numerals",
                    "Spindle boxes (quantities to nine, then ten)",
                    "Cards and counters one to ten",
                ],
                "presentation": {
                    "three_period_lesson": "Naming: place eight counters, this is eight. Recognition: show me eight. Recall: how many? Move slowly to recall.",
                    "steps": [
                        "Lay out a quantity of counters",
                        "Touch-count each once",
                        "Pair counters to self-check; a leftover reveals a miscount",
                    ],
                },
                "control_of_error": "Spindle and counter quantities are fixed, so a miscount leaves a gap or a leftover the child sees and fixes.",
                "abstraction_pathway": "From rods felt as length, to counters touched, toward holding the quantity to ten in mind.",
                "extensions": ["Build numbers to ten with the number rods", "Count a short bead chain to ten"],
                "observation_focus": "Watch for sustained, careful counting and the free choice to repeat the work.",
            },
            "unschooling": {
                "invitations": [
                    "Leave a bowl of ten interesting buttons within reach",
                    "Set out a set of ten blocks and say nothing",
                ],
                "real_world_contexts": [
                    "Sharing ten snacks fairly",
                    "Counting ten stairs each climb",
                    "Counting ten coins during pretend shopping",
                ],
                "conversation_starters": [
                    "I wonder how many are in here? Want to find out?",
                    "Can everyone get the same number?",
                ],
                "resource_bank": ["A counting picture book left out", "A bowl of small objects to handle and count"],
                "parent_role": "Notice where counting to ten already lives in the day and join it; answer real questions and count aloud yourself.",
                "observation_documentation": "Over days, note how high the child counts confidently and whether one-to-one touch holds to ten; this replaces a test.",
            },
        },
        "connections": {
            "reading": "Number words to ten as sight words",
            "science": "Counting up to ten specimens on a nature table",
            "history": "Ten marks on a personal timeline",
        },
    },
    "mf-33": {
        "enriched": True,
        "learning_objectives": [
            "Name the quantity of a set of one to five shown briefly, without counting",
            "Recognize standard dice and dot patterns for one through five",
            "Show the matching number of fingers for a named quantity one to five",
            "Explain that some small amounts can be 'just seen' without counting",
        ],
        "teaching_guidance": {
            "introduction": "Sometimes we do not need to count one by one. Our eyes can see small amounts all at once. Today we practice seeing how many, up to five, in a single glance.",
            "scaffolding_sequence": [
                "Flash a set of two or three for a moment, name it",
                "Flash four and five in standard patterns, name them",
                "Flash scattered small sets, name them",
            ],
            "socratic_questions": [
                "How many did you see? Did you have to count, or did you just know?",
                "What pattern did the dots make?",
                "Can you show that many fingers fast?",
            ],
            "practice_activities": [
                "Quick-flash dot cards one to five",
                "Roll a die and name the face without counting",
                "Show fingers for a called number quickly",
            ],
            "real_world_connections": [
                "Seeing three eggs left in a carton at a glance",
                "Reading a dice face in a board game",
                "Seeing two shoes by the door",
            ],
            "common_misconceptions": [
                "Counting every dot when the amount could be seen; address by flashing the card too briefly to count, building the glance",
                "Not recognizing a pattern when rearranged; address by showing the same quantity in several arrangements",
                "Guessing wildly for four versus five; address by anchoring five as a full hand and four as one less",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Names sets of one to five at a glance without counting",
                "Recognizes dice and standard dot patterns",
                "Shows fingers for a named small number quickly",
            ],
            "assessment_methods": ["dot pattern cards", "oral response", "observation"],
            "sample_assessment_prompts": [
                "I will flash this card; tell me how many",
                "What number is on this dice face?",
                "Show me four fingers fast",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "I show . . for a moment. How many dots?",
                "expected_type": "number",
                "correct_answer": "2",
                "hints": ["Just look, do not count"],
                "explanation": "Two dots can be seen at a glance.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "How many dots on this dice face: : (two rows of two)?",
                "expected_type": "number",
                "correct_answer": "4",
                "hints": ["The four corners pattern"],
                "explanation": "The square pattern is 4.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Show three fingers as fast as you can. How many?",
                "expected_type": "number",
                "correct_answer": "3",
                "hints": ["Just put up three"],
                "explanation": "Three fingers shown quickly.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "I flash five dots in a dice pattern. How many, without counting?",
                "expected_type": "number",
                "correct_answer": "5",
                "hints": ["A full dice five has four corners and one middle"],
                "explanation": "The dice-five pattern is 5.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "I flash four scattered dots. How many?",
                "expected_type": "number",
                "correct_answer": "4",
                "hints": ["Try to see it as two and two"],
                "explanation": "Four dots, seen as two pairs.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Which is faster to know at a glance: 3 dots or 9 dots? Why?",
                "expected_type": "text",
                "hints": ["Think about which small amount your eyes just see"],
                "explanation": "3 dots is faster; small amounts up to about five can be seen at once, while 9 must be counted or grouped.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "I show two dots, then two more dots beside them. How many in all, at a glance?",
                "expected_type": "number",
                "correct_answer": "4",
                "hints": ["See two and two together"],
                "explanation": "Two and two seen together is 4 without counting each.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Explain how you can 'just know' there are five without counting one by one.",
                "expected_type": "text",
                "hints": ["Think about a full hand or the dice five"],
                "explanation": "Five matches a full hand or the dice-five pattern, so the eyes recognize the whole shape as five at once.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Flash card shows three dots. How many? (no counting)",
                "type": "number",
                "target_concept": "subitize_3",
                "correct_answer": "3",
            },
            {
                "prompt": "Dice face shown: how many pips? : :",
                "type": "number",
                "target_concept": "subitize_5",
                "correct_answer": "5",
            },
            {
                "prompt": "Flash card shows four dots. How many?",
                "type": "number",
                "target_concept": "subitize_4",
                "correct_answer": "4",
            },
            {
                "prompt": "Show the number of fingers for 'two' as fast as you can.",
                "type": "open_response",
                "target_concept": "finger_subitize",
                "rubric": "Mastery: shows 2 instantly. Proficient: a brief pause. Developing: counts up to two.",
            },
            {
                "prompt": "How do you know how many without counting each one?",
                "type": "open_response",
                "target_concept": "subitizing_strategy",
                "rubric": "Mastery: names seeing the pattern/whole. Proficient: says 'I just see it.' Developing: still counts each.",
            },
        ],
        "resource_guidance": {
            "required": ["dot pattern cards 1-5", "a die"],
            "recommended": ["five-frame cards", "finger pattern cards"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 8},
        "accommodations": {
            "dyslexia": "Use bold, high-contrast dots; keep flashes brief and oral, no writing.",
            "adhd": "Make it a quick game with short turns; flash, name, move on.",
            "gifted": "Add quantities to ten and brief two-part flashes (e.g., 3 and 2).",
            "visual_learner": "Use clear, standard patterns (dice, five-frame) shown briefly.",
            "kinesthetic_learner": "Pair the glance with showing fingers for the same amount.",
            "auditory_learner": "Say the number aloud the instant the card appears; chant the pattern.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Some small amounts we can see at once. Today we practice naming up to five at a glance.",
                "gradual_release": {
                    "i_do": "Model flashing three dots and naming three immediately, saying I did not count, I saw it.",
                    "we_do": "Flash four and five together, the child naming the amount, then swap who flashes.",
                    "you_do": "Child names flashed sets of one to five independently, without counting.",
                },
                "guided_practice": [
                    "Flash-and-name dot cards with the teacher confirming",
                    "Match a flashed amount to the right number card",
                ],
                "independent_practice": [
                    "Name a stack of flashed cards one to five",
                    "Show fingers for called small numbers",
                ],
                "mastery_check": [
                    "Names one to five at a glance",
                    "Recognizes dice and dot patterns",
                    "Shows fingers for a named small number",
                ],
                "spiral_review": ["Re-count a small set (mf-31) by touch to confirm a quick glance was right"],
            },
            "classical": {
                "narrative_introduction": "The trained eye knows a small number the way the ear knows a familiar rhyme: all at once, without labor.",
                "memory_work": {
                    "chants": [
                        "Pattern chant: name the dice faces one to five in order",
                        "Flash-and-say: see it, say it",
                    ],
                    "recitations": ["A short rhyme that names small quantities, recited daily"],
                },
                "recitation_routine": "Begin by naming yesterday's patterns from memory before adding today's, reviewing the forms cumulatively.",
                "history_integration": "Notice small fixed groups in art or architecture (three arches, five points of a star).",
                "read_aloud_suggestions": ["A picture book with clear small groupings to spot and name aloud"],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 8,
                "living_book_suggestions": ["A picture book whose illustrations hold small, clear groupings to notice"],
                "short_lesson_flow": "Show a small group of real objects briefly, cover it, and ask how many were seen; uncover to confirm, calmly.",
                "narration_prompt": "How many did you see when I uncovered them? Did you have to count?",
                "real_world_objects": ["Three eggs in a bowl", "Five petals on a flower", "Two birds on a branch"],
                "nature_connection": "On a walk, notice small fixed numbers in nature: a clover's three leaves, a star's five points.",
                "habit_focus": "The habit of attentive seeing: take in the whole small group at once.",
            },
            "montessori": {
                "prepared_materials": [
                    "Dot pattern cards",
                    "Counters arranged in standard patterns",
                    "A die with clear pips",
                ],
                "presentation": {
                    "three_period_lesson": "Naming: show a four pattern, this is four. Recognition: which card shows four? Recall: how many here?",
                    "steps": [
                        "Show a patterned card briefly",
                        "The child names the quantity",
                        "Reveal counters to self-check by pairing",
                    ],
                },
                "control_of_error": "The fixed pattern card can be checked against counters; a mismatch shows the child to look again.",
                "abstraction_pathway": "From seen patterns, to named quantities, toward instantly holding small amounts as ideas.",
                "extensions": [
                    "Make the same quantity in two different arrangements",
                    "Find small fixed groups around the room",
                ],
                "observation_focus": "Watch whether the child names quickly without touching each dot, and chooses to repeat.",
            },
            "unschooling": {
                "invitations": [
                    "Leave dominoes or dice out where the child plays",
                    "Set out cards with small dot groups and say nothing",
                ],
                "real_world_contexts": [
                    "Reading a dice face in a family game",
                    "Seeing two cookies left on a plate",
                    "Noticing three ducks on a pond",
                ],
                "conversation_starters": ["How many do you think, without counting?", "Did you just see it?"],
                "resource_bank": ["Dice and domino games left available", "Picture books with clear small groupings"],
                "parent_role": "Play dice and domino games for fun and let the child read the faces naturally; never drill the glance.",
                "observation_documentation": "Notice over time whether the child reads small amounts at sight in real play; this is the evidence, not a test.",
            },
        },
        "connections": {
            "reading": "Recognizing letter groups at a glance parallels seeing small quantities",
            "science": "Noticing small fixed counts in nature (petals, legs)",
            "history": "Spotting small repeated groups in patterns of the past",
        },
    },
    "mf-34": {
        "enriched": True,
        "learning_objectives": [
            "Place counters on a ten-frame to show any number from zero to ten",
            "Read a quantity shown on a ten-frame using five as a benchmark",
            "Recognize a full ten-frame as ten and an empty frame as zero",
            "Describe a number above five as 'five and some more'",
        ],
        "teaching_guidance": {
            "introduction": "A ten-frame is two rows of five boxes. We fill it left to right, top row first. It helps us see a number quickly, because a full top row is five and a full frame is ten.",
            "scaffolding_sequence": [
                "Fill the top row to show numbers up to five",
                "Fill into the second row for six to ten",
                "Read frames built by the teacher at a glance",
            ],
            "socratic_questions": [
                "How many are filled? How do you know without counting each?",
                "How many more would make ten?",
                "Is the top row full? So how many is that?",
            ],
            "practice_activities": [
                "Build called numbers on a ten-frame",
                "Flash a built frame and name it",
                "Show 'one more' and 'one less' by adding or removing a counter",
            ],
            "real_world_connections": [
                "An egg carton row holding up to ten eggs",
                "Ten muffins in a tin with some cups empty",
                "Ten parking spaces with some cars",
            ],
            "common_misconceptions": [
                "Filling out of order so the frame cannot be read at a glance; address by always filling top-left first, left to right",
                "Counting every cell instead of using five as a benchmark; address by pointing out a full top row is five, then counting on",
                "Confusing filled and empty cells; address by using a single counter color on a clean frame",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Builds 0-10 on a ten-frame in order",
                "Reads frames using the five benchmark",
                "Names a full frame as ten",
            ],
            "assessment_methods": ["ten-frame building", "oral response", "demonstration"],
            "sample_assessment_prompts": [
                "Build seven on the ten-frame",
                "How many are on this frame?",
                "How many more make ten?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Build 4 on a ten-frame. How many cells are filled?",
                "expected_type": "number",
                "correct_answer": "4",
                "hints": ["Fill the top row left to right"],
                "explanation": "Four cells filled, all in the top row.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "A ten-frame is completely full. How many counters?",
                "expected_type": "number",
                "correct_answer": "10",
                "hints": ["A full frame is two rows of five"],
                "explanation": "A full ten-frame is 10.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "The top row of five is full and the bottom row is empty. How many?",
                "expected_type": "number",
                "correct_answer": "5",
                "hints": ["A full top row is the five benchmark"],
                "explanation": "A full top row is 5.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "A ten-frame shows a full top row and 2 in the bottom. How many?",
                "expected_type": "number",
                "correct_answer": "7",
                "hints": ["Five and two more"],
                "explanation": "Five and two more is 7.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You have 6 on the frame. How many more cells to fill to make ten?",
                "expected_type": "number",
                "correct_answer": "4",
                "hints": ["Count the empty cells"],
                "explanation": "6 and 4 more make 10, so 4 empty cells remain.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Explain how a ten-frame helps you see 8 without counting all eight.",
                "expected_type": "text",
                "hints": ["Think about the full top row plus the bottom"],
                "explanation": "You see the full top row as five and count on the three in the bottom: five, six, seven, eight.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "A frame shows 9. Tell two things you know: how many more make ten, and how many empty cells.",
                "expected_type": "text",
                "hints": ["Empty cells and 'more to ten' are the same here"],
                "explanation": "One more makes ten, and there is one empty cell, because 9 and 1 make 10.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Build 5 two different ways on the ten-frame and tell which is easier to read.",
                "expected_type": "text",
                "hints": ["One full top row versus scattered cells"],
                "explanation": "A full top row of five is easier to read at a glance than five scattered cells, because the benchmark is whole.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Build 6 on a ten-frame, then say how many.",
                "type": "open_response",
                "target_concept": "ten_frame_build",
                "rubric": "Mastery: fills top row then one more, says 6. Proficient: builds 6 out of order. Developing: cannot reach 6.",
            },
            {
                "prompt": "A ten-frame shows a full top row and 3 below. How many?",
                "type": "number",
                "target_concept": "read_ten_frame",
                "correct_answer": "8",
            },
            {
                "prompt": "How many more counters make ten if 7 are on the frame?",
                "type": "number",
                "target_concept": "make_ten",
                "correct_answer": "3",
            },
            {
                "prompt": "A full ten-frame shows what number?",
                "type": "number",
                "target_concept": "ten_benchmark",
                "correct_answer": "10",
            },
            {
                "prompt": "Why is a ten-frame helpful for seeing numbers quickly?",
                "type": "open_response",
                "target_concept": "ten_frame_reasoning",
                "rubric": "Mastery: names five/ten benchmarks. Proficient: says it is organized. Developing: cannot explain.",
            },
        ],
        "resource_guidance": {
            "required": ["ten-frame mat", "ten counters"],
            "recommended": ["double ten-frame", "two-color counters"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Use a large, high-contrast frame and one counter color; keep talk oral.",
            "adhd": "Short builds; let the child place counters with hands, one challenge at a time.",
            "gifted": "Use a double ten-frame to show numbers to twenty and 'ten and some more'.",
            "visual_learner": "Color the top row of five lightly so the benchmark stands out.",
            "kinesthetic_learner": "Place real counters by hand into the frame; tap full rows.",
            "auditory_learner": "Say the build aloud: five and two more is seven.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "A ten-frame shows numbers in order, with five as a half and ten as full. Today we build and read numbers to ten.",
                "gradual_release": {
                    "i_do": "Model building seven: fill the top row, say five, then place two more, six, seven.",
                    "we_do": "Build six and nine together, naming the five benchmark, then the child reads frames you build.",
                    "you_do": "Child builds called numbers zero to ten and reads frames independently using the five benchmark.",
                },
                "guided_practice": [
                    "Build numbers on the frame with the teacher confirming the benchmark",
                    "Read flashed frames and name the quantity",
                ],
                "independent_practice": ["Build a set of called numbers on the frame", "Match frames to number cards"],
                "mastery_check": [
                    "Builds 0-10 in order on the frame",
                    "Reads frames using five as a benchmark",
                    "Names a full frame as ten",
                ],
                "spiral_review": [
                    "Re-count a small set (mf-32) by touch, then place it on the frame to confirm the quantity"
                ],
            },
            "classical": {
                "narrative_introduction": "The ten-frame is a small orderly house for the numbers to ten; each number has its own steady arrangement, learned once and known forever.",
                "memory_work": {
                    "chants": [
                        "Chant the build: one, two, three, four, five fills the top; six, seven, eight, nine, ten fills below",
                        "Recite how many empty cells remain for each number",
                    ],
                    "recitations": ["A short rhyme naming five and ten as the friendly benchmarks"],
                },
                "recitation_routine": "Begin by rebuilding yesterday's numbers on the frame from memory before adding today's.",
                "history_integration": "Notice orderly rows and columns in old mosaics and tiled floors, where quantity is arranged to be seen.",
                "read_aloud_suggestions": ["A counting book that arranges objects in neat rows to admire"],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 12,
                "living_book_suggestions": ["A counting book whose pictures group objects in tidy, lovely rows"],
                "short_lesson_flow": "Lay real objects (acorns, beans) into a ten-frame drawn on paper, filling in order, then read the number calmly together.",
                "narration_prompt": "Tell me about the number you made. How did the frame help you see it?",
                "real_world_objects": [
                    "Eggs settling into a carton",
                    "Stones laid in two neat rows",
                    "Muffins in a tin",
                ],
                "nature_connection": "On a nature table, arrange found objects in a ten-frame and notice how the rows make the count easy.",
                "habit_focus": "The habit of orderliness: place each thing in its cell, filling neatly in order.",
            },
            "montessori": {
                "prepared_materials": ["Printed ten-frame mat", "Red and blue counters", "Number cards 0-10"],
                "presentation": {
                    "three_period_lesson": "Naming: build eight, this is eight. Recognition: build me eight. Recall: how many on this frame?",
                    "steps": [
                        "Place counters left to right, top row first",
                        "Pause at five to note the benchmark",
                        "Self-check by comparing the frame to a number card",
                    ],
                },
                "control_of_error": "The fixed frame reveals error: a gap in the top row or an extra in the bottom shows the build is wrong.",
                "abstraction_pathway": "From counters placed in the frame, to reading the arrangement, toward picturing the number's shape.",
                "extensions": [
                    "Build numbers to ten with two colors to show parts",
                    "Find how many more make ten for each number",
                ],
                "observation_focus": "Watch for orderly placement and the child reading frames without counting each cell.",
            },
            "unschooling": {
                "invitations": [
                    "Leave an egg carton trimmed to ten cups with small objects nearby",
                    "Set out a ten-frame card and loose counters, say nothing",
                ],
                "real_world_contexts": [
                    "Filling an egg carton with collected stones",
                    "Setting ten cupcakes in a tin with empty cups",
                    "Loading ten items into a divided tray",
                ],
                "conversation_starters": ["I wonder how many fit in here?", "How many spaces are still empty?"],
                "resource_bank": [
                    "An egg carton and a basket of small objects",
                    "A printed ten-frame left available with counters",
                ],
                "parent_role": "Offer the frame as a fun tray to fill and let the child arrange real objects; talk about full and empty without making it a lesson.",
                "observation_documentation": "Notice whether the child fills in order and reads 'full' as ten in real play; this is the record, not a test.",
            },
        },
        "connections": {
            "reading": "Reading left-to-right, top-to-bottom mirrors filling the frame",
            "science": "Arranging specimens in orderly trays to count them",
            "history": "Tally rows as an early organized record of quantity",
        },
    },
    "mf-35": {
        "enriched": True,
        "learning_objectives": [
            "State that the last number counted tells how many are in the set",
            "Answer 'how many' right after counting without starting over",
            "Count the same set in a different order and get the same total",
            "Explain that rearranging objects does not change how many there are",
        ],
        "teaching_guidance": {
            "introduction": "When we finish counting, the very last number we said tells how many in all. We do not need to count again. And it does not matter where we start, the total stays the same.",
            "scaffolding_sequence": [
                "Count a set, then answer how many without recounting",
                "Count the same set starting from a different object",
                "Spread out a counted set and confirm the total is unchanged",
            ],
            "socratic_questions": [
                "What was the last number you said? So how many are there?",
                "If you start counting from a different one, will the total change?",
                "I moved them apart. Are there still the same number? How do you know?",
            ],
            "practice_activities": [
                "Count-and-tell: count, then state the total once",
                "Count a set forwards, then count it from the other end",
                "Rearrange a counted set and ask 'how many now?'",
            ],
            "real_world_connections": [
                "Knowing six cookies are on the plate after counting once",
                "Telling a parent how many shoes are by the door",
                "Reporting how many blocks are in the tower",
            ],
            "common_misconceptions": [
                "Recounting from one when asked 'how many'; address by stopping after the count and accepting only the last word as the total",
                "Thinking spreading objects out makes more; address by counting the spread set to show the total is unchanged",
                "Giving a different total when starting elsewhere; address by counting the same set two ways and comparing",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "States the total as the last count word",
                "Gives the same total counting in any order",
                "Answers 'how many' without recounting",
            ],
            "assessment_methods": ["object counting", "oral response", "observation"],
            "sample_assessment_prompts": [
                "Count these, then tell me how many",
                "Count them again starting here; how many?",
                "I spread them out; how many now?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "You count 7 blocks: 1, 2, 3, 4, 5, 6, 7. How many blocks?",
                "expected_type": "number",
                "correct_answer": "7",
                "hints": ["The last number you said is the total"],
                "explanation": "7, because the last count word tells how many.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "You count to 5 and stop. How many are there?",
                "expected_type": "number",
                "correct_answer": "5",
                "hints": ["What was the last number?"],
                "explanation": "5, the last number counted.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "You count a set and end on 9. How many?",
                "expected_type": "number",
                "correct_answer": "9",
                "hints": ["No need to count again"],
                "explanation": "9 is the total.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You counted 6 shells. Your friend slides them apart. How many shells now?",
                "expected_type": "number",
                "correct_answer": "6",
                "hints": ["Did any shell leave?"],
                "explanation": "Still 6; moving them does not change how many.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You count 8 toys left to right. If you count them right to left, what total do you get?",
                "expected_type": "number",
                "correct_answer": "8",
                "hints": ["The order does not change the count"],
                "explanation": "8 either way; the total stays the same.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "After counting, why do you not need to count again to say how many?",
                "expected_type": "text",
                "hints": ["Think about the last number you said"],
                "explanation": "Because the last number counted already tells the total, so saying it answers 'how many.'",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "A child counts 5 cars, then a grown-up asks how many and the child counts again. What should the child do instead?",
                "expected_type": "text",
                "hints": ["What did the last count tell?"],
                "explanation": "Just say five, the last number from the first count, because that already tells how many.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "You have 7 buttons in a line. You make them into a circle. Explain how you know there are still 7.",
                "expected_type": "text",
                "hints": ["Were any added or taken away?"],
                "explanation": "No buttons were added or removed, so the total is still 7; rearranging never changes how many.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Count these objects, then tell how many without counting again: # # # # # #",
                "type": "number",
                "target_concept": "cardinality",
                "correct_answer": "6",
            },
            {
                "prompt": "You count and end on 8. How many are there?",
                "type": "number",
                "target_concept": "last_count",
                "correct_answer": "8",
            },
            {
                "prompt": "You counted 5 stones, then spread them apart. How many now?",
                "type": "number",
                "target_concept": "order_irrelevance",
                "correct_answer": "5",
            },
            {
                "prompt": "Count this set starting from the other end. Do you get the same total?",
                "type": "open_response",
                "target_concept": "count_order",
                "rubric": "Mastery: same total, explains order does not matter. Proficient: same total. Developing: different total.",
            },
            {
                "prompt": "Why does the last number you count tell how many?",
                "type": "open_response",
                "target_concept": "cardinality_reasoning",
                "rubric": "Mastery: states last word is the total. Proficient: partial. Developing: recounts to answer.",
            },
        ],
        "resource_guidance": {
            "required": ["counting objects", "a small tray to rearrange sets"],
            "recommended": ["number cards", "two-color counters"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 8},
        "accommodations": {
            "dyslexia": "Keep oral; let the child say only the total, no writing. Use few objects to reduce load.",
            "adhd": "Brief count-and-tell turns; celebrate stopping after the count.",
            "gifted": "Extend to predicting the total before recounting a rearranged set.",
            "visual_learner": "Circle or box the last object counted to anchor the total.",
            "kinesthetic_learner": "Physically slide objects apart, then recount to feel the total is the same.",
            "auditory_learner": "Say the total aloud once, firmly, after counting.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "After counting, the last number tells how many, and the total does not change if we move the objects. Today we practice telling how many.",
                "gradual_release": {
                    "i_do": "Model counting six, then saying six tells how many, without counting again.",
                    "we_do": "Count a set together, then the child says the total; rearrange it and confirm together it is unchanged.",
                    "you_do": "Child counts sets and states the total once, and confirms a rearranged set has the same total.",
                },
                "guided_practice": [
                    "Count-and-tell with the teacher confirming the last word is the total",
                    "Recount a rearranged set to confirm the total",
                ],
                "independent_practice": [
                    "Count five sets and state each total once",
                    "Rearrange counted sets and report 'how many'",
                ],
                "mastery_check": [
                    "States the total as the last count word",
                    "Gives the same total in any order",
                    "Answers 'how many' without recounting",
                ],
                "spiral_review": [
                    "Re-count by touch using one-to-one correspondence (mf-03), then state the total once"
                ],
            },
            "classical": {
                "narrative_introduction": "A wise rule: the last word of the count is the name of the whole. Say it once, and you have said how many.",
                "memory_work": {
                    "chants": [
                        "Chant: count to the end, the last is how many",
                        "Echo: the teacher counts a set, the child names the total",
                    ],
                    "recitations": ["A short saying recited daily: the last number tells how many"],
                },
                "recitation_routine": "Begin by recalling yesterday's rule, the last number tells how many, before counting today's sets.",
                "history_integration": "Count years on a timeline and state the total span, naming the last mark as the count of years.",
                "read_aloud_suggestions": ["A counting book whose last page states the total, read aloud"],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 8,
                "living_book_suggestions": ["A gentle counting book that ends by telling the whole amount"],
                "short_lesson_flow": "Count a small basket of real objects together, then ask how many; accept the last number, and rearrange to show it holds.",
                "narration_prompt": "How many were there? How do you know without counting again?",
                "real_world_objects": [
                    "Shells counted and then spread on a cloth",
                    "Acorns counted in a line and then a pile",
                    "Spoons counted at the table",
                ],
                "nature_connection": "On a walk, count found treasures and state the total, then notice the total holds when they are laid out differently.",
                "habit_focus": "The habit of truthfulness: say the real total once, and trust it.",
            },
            "montessori": {
                "prepared_materials": ["Cards and counters", "A small mat for rearranging sets", "Number cards 1-10"],
                "presentation": {
                    "three_period_lesson": "Naming: count seven, this is seven in all. Recognition: which set is seven? Recall: how many here?",
                    "steps": [
                        "Count a set with one-to-one touch",
                        "State the last number as the total",
                        "Rearrange and confirm the total by recounting",
                    ],
                },
                "control_of_error": "Counting the same fixed set twice in different orders gives the same total; a different answer shows a miscount to correct.",
                "abstraction_pathway": "From counting each object, to naming the last word as the whole, toward trusting the total without recounting.",
                "extensions": [
                    "Count a set in several orders to confirm the total",
                    "Predict the total of a rearranged known set",
                ],
                "observation_focus": "Watch whether the child states the total without recounting and trusts it after rearranging.",
            },
            "unschooling": {
                "invitations": [
                    "Leave counted collections out where the child returns to them",
                    "Set a bowl of objects and a tray to pour them between",
                ],
                "real_world_contexts": [
                    "Telling how many cookies are on the plate",
                    "Reporting how many pets are in the room",
                    "Saying how many people are at dinner",
                ],
                "conversation_starters": [
                    "How many do you think there are?",
                    "If we move them around, are there still the same number?",
                ],
                "resource_bank": [
                    "Collections the child already counts and loves",
                    "Trays and bowls for pouring sets back and forth",
                ],
                "parent_role": "Answer real 'how many' questions in daily life and notice aloud when a moved set is still the same amount, never turning it into a drill.",
                "observation_documentation": "Over time, note whether the child states totals confidently and knows rearranging keeps the amount; this is the evidence.",
            },
        },
        "connections": {
            "reading": "The last word of a count names the whole, as the last word of a sentence completes it",
            "science": "Reporting how many specimens were found",
            "history": "Stating the total number of events counted on a timeline",
        },
    },
    "mf-36": {
        "enriched": True,
        "learning_objectives": [
            "Recite the numbers from ten down to one in order",
            "Count backward starting from any number within ten",
            "State the number that comes just before a given number (one fewer)",
            "Connect counting back one with taking one away",
        ],
        "teaching_guidance": {
            "introduction": "We can count the other way too, going down. Counting backward from ten goes ten, nine, eight, all the way to one. Each step back is one fewer.",
            "scaffolding_sequence": [
                "Count down from five to one",
                "Count down from eight, then from ten",
                "Start at a given number and count down to one",
            ],
            "socratic_questions": [
                "What comes just before seven when we count down?",
                "Each step back, do we have one more or one fewer?",
                "Where should we stop when counting down?",
            ],
            "practice_activities": [
                "Countdown chants from ten",
                "Remove one object at a time, naming the new amount",
                "Step backward on a floor number line",
            ],
            "real_world_connections": [
                "Counting down seconds before a jump",
                "Counting down stairs while going down",
                "Counting down days until an event",
            ],
            "common_misconceptions": [
                "Reverting to forward counting; address by anchoring 'down' with a physical downward motion or removing an object each step",
                "Skipping a number going down; address by slowing and removing one object per number",
                "Not connecting back-one with one fewer; address by taking one object away and naming the smaller count",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Counts backward from 10 to 1 accurately",
                "Counts down from any number within ten",
                "Names the number that is one fewer",
            ],
            "assessment_methods": ["oral counting", "object removal", "observation"],
            "sample_assessment_prompts": [
                "Count down from 10 to 1",
                "Start at 7 and count down",
                "What number is one fewer than 9?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Count backward: 5, 4, 3, ... what comes next?",
                "expected_type": "number",
                "correct_answer": "2",
                "hints": ["Each step is one fewer"],
                "explanation": "After 3 going down comes 2.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Count down from 10. What number do you say right after 10?",
                "expected_type": "number",
                "correct_answer": "9",
                "hints": ["One fewer than ten"],
                "explanation": "9 comes after 10 going down.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What number is one fewer than 6?",
                "expected_type": "number",
                "correct_answer": "5",
                "hints": ["Count back one"],
                "explanation": "One fewer than 6 is 5.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Start at 8 and count down to 1. What is the last number you say?",
                "expected_type": "number",
                "correct_answer": "1",
                "hints": ["Keep going down until you reach the smallest"],
                "explanation": "Counting down from 8 ends at 1.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You have 7 blocks and take 1 away. Counting down, how many now?",
                "expected_type": "number",
                "correct_answer": "6",
                "hints": ["One fewer than seven"],
                "explanation": "7 take away 1 is 6, the next number going down.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Tell how counting backward is different from counting forward.",
                "expected_type": "text",
                "hints": ["Think about getting bigger or smaller"],
                "explanation": "Counting forward goes up by one each time, while counting backward goes down by one each time.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "A rocket counts down 5, 4, 3, 2, 1. What word usually comes after 1 in a countdown, and why?",
                "expected_type": "text",
                "hints": ["What happens when the countdown ends?"],
                "explanation": "Blast off (or zero); the countdown ends at one (or zero) because there are no smaller counting numbers left to say.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Count down from 9 and clap each time. Tell how many claps you made.",
                "expected_type": "text",
                "hints": ["One clap per number from 9 to 1"],
                "explanation": "Nine claps, one for each number from 9 down to 1.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Count backward from 10 to 1.",
                "type": "open_response",
                "target_concept": "backward_10",
                "rubric": "Mastery: 10-1 in order, no errors. Proficient: one self-correction. Developing: reverts to forward or skips.",
            },
            {
                "prompt": "What number is one fewer than 8?",
                "type": "number",
                "target_concept": "one_fewer",
                "correct_answer": "7",
            },
            {
                "prompt": "Start at 6 and count down. What is the next number?",
                "type": "number",
                "target_concept": "count_down",
                "correct_answer": "5",
            },
            {
                "prompt": "You have 5 and take 1 away. Counting down, how many?",
                "type": "number",
                "target_concept": "back_one_subtraction",
                "correct_answer": "4",
            },
            {
                "prompt": "How is counting backward different from counting forward?",
                "type": "open_response",
                "target_concept": "reverse_reasoning",
                "rubric": "Mastery: names up vs down by one. Proficient: says 'the other way.' Developing: cannot explain.",
            },
        ],
        "resource_guidance": {
            "required": ["counting objects to remove", "a number track 0-10"],
            "recommended": ["floor number line", "countdown picture cards"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 8},
        "accommodations": {
            "dyslexia": "Keep oral; pair each step with removing an object so 'down' is felt, no writing.",
            "adhd": "Make it a quick countdown game with a physical motion each number.",
            "gifted": "Extend to counting back from twenty and counting back by twos.",
            "visual_learner": "Use a vertical number line and move a marker down each step.",
            "kinesthetic_learner": "Step down stairs or squat lower with each number counted back.",
            "auditory_learner": "Chant the countdown rhythmically; clap softer as numbers shrink.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "We can count down as well as up. Today we recite ten to one and count down from any number, one fewer each step.",
                "gradual_release": {
                    "i_do": "Model counting down from ten, removing one counter each number, naming the new amount.",
                    "we_do": "Count down from eight together, the child removing a counter each step, then swap.",
                    "you_do": "Child counts backward from ten and from given starting numbers independently.",
                },
                "guided_practice": [
                    "Countdown with the teacher removing one object per number",
                    "Count back from a called number to one",
                ],
                "independent_practice": [
                    "Recite the countdown from ten",
                    "Count down from five different starting numbers",
                ],
                "mastery_check": [
                    "Counts backward from 10 to 1",
                    "Counts down from any number within ten",
                    "Names one fewer",
                ],
                "spiral_review": [
                    "Re-count forward to ten with objects (mf-32) first, then reverse to count down from ten"
                ],
            },
            "classical": {
                "narrative_introduction": "As a column can be read top to bottom, so the count can be said in reverse; the child who knows ten to one knows the ladder both ways.",
                "memory_work": {
                    "chants": [
                        "Backward chant 10 to 1, clear and steady, daily",
                        "Echo: the teacher says a number, the child says the one before it",
                    ],
                    "recitations": ["A short countdown rhyme recited at the start of math time"],
                },
                "recitation_routine": "Begin by reciting yesterday's countdown before counting down any objects, reviewing the reverse order cumulatively.",
                "history_integration": "Count down the days of a short calendar toward an event, tying countdown to the passage of time.",
                "read_aloud_suggestions": ["A picture book with a countdown story, read aloud with anticipation"],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 8,
                "living_book_suggestions": ["A gentle countdown picture book with lovely, calm pictures"],
                "short_lesson_flow": "Lay out ten real objects and remove one at a time, naming the new amount, counting down together calmly.",
                "narration_prompt": "Tell me about counting down. What happened to the number each time?",
                "real_world_objects": [
                    "Ten stones removed one by one",
                    "Ten steps counted going down",
                    "Counting down spoons cleared from the table",
                ],
                "nature_connection": "On a walk, count down found objects as they are put away one by one into a basket.",
                "habit_focus": "The habit of attention: say each number going down, once, without slipping back to forward.",
            },
            "montessori": {
                "prepared_materials": [
                    "Number rods to remove in order",
                    "Number cards 1-10",
                    "Counters to take away one at a time",
                ],
                "presentation": {
                    "three_period_lesson": "Naming: from ten, take one, this is nine. Recognition: show me one fewer than nine. Recall: what comes before this going down?",
                    "steps": [
                        "Lay out ten counters",
                        "Remove one and name the new amount",
                        "Continue down to one, self-checking the shrinking set",
                    ],
                },
                "control_of_error": "Removing one counter each step makes the smaller quantity visible; a wrong name shows a leftover or a missing step to correct.",
                "abstraction_pathway": "From removing one object at a time, to reciting the reverse order, toward counting down in the mind.",
                "extensions": ["Count down by twos from ten", "Build the descending number-rod stair"],
                "observation_focus": "Watch whether the child counts down smoothly and connects each step with one fewer object.",
            },
            "unschooling": {
                "invitations": [
                    "Leave a countdown calendar to an event the child cares about",
                    "Put out blocks and let the child knock one down at a time",
                ],
                "real_world_contexts": [
                    "Counting down before a jump or a race",
                    "Counting down stairs while descending",
                    "Counting down sleeps until a trip",
                ],
                "conversation_starters": ["How many are left now?", "Want to count down before we go?"],
                "resource_bank": ["Countdown picture books left available", "A simple calendar to mark off days"],
                "parent_role": "Use natural countdowns in real life (blast-off play, days till a visit) and count down together for the fun of it, never as drill.",
                "observation_documentation": "Notice whether the child counts down confidently in real moments and knows each step is one fewer; this is the record.",
            },
        },
        "connections": {
            "reading": "Counting down letters or steps in a sequence read in reverse",
            "science": "Counting down seconds in a simple experiment",
            "history": "Counting down days remaining on a timeline",
        },
    },
    "mf-37": {
        "enriched": True,
        "learning_objectives": [
            "Recite the numbers from twenty down to one in order",
            "Count backward starting from any number within twenty",
            "Count back smoothly across the teen numbers (e.g., 14, 13, 12)",
            "State the number that is one fewer for any number to twenty",
        ],
        "teaching_guidance": {
            "introduction": "Now we count down from a bigger number, twenty. The trickiest part is the teen numbers, so we go slowly: twenty, nineteen, eighteen, and on down to one.",
            "scaffolding_sequence": [
                "Count down from twelve to one",
                "Count down from sixteen through the teens",
                "Count down from twenty, slowing at the teens",
            ],
            "socratic_questions": [
                "What comes just before fourteen going down?",
                "Which numbers are trickiest to say backward? Why?",
                "Where do we stop counting down?",
            ],
            "practice_activities": [
                "Countdown chants from twenty",
                "Move a marker down a 0-20 number line each step",
                "Count down while removing teen-sized sets",
            ],
            "real_world_connections": [
                "Counting down a longer countdown to lift-off",
                "Counting down pages left in a short book",
                "Counting down minutes on a timer",
            ],
            "common_misconceptions": [
                "Stumbling on teen numbers in reverse; address by practicing fourteen-thirteen-twelve slowly with a number line",
                "Slipping back to forward counting mid-teen; address by a steady downward finger trace on a number line",
                "Skipping from twenty straight to ten; address by naming every teen on the way down",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Counts backward from 20 to 1 accurately",
                "Counts down from any number within twenty",
                "Handles the teen numbers in reverse",
            ],
            "assessment_methods": ["oral counting", "number-line tracing", "observation"],
            "sample_assessment_prompts": [
                "Count down from 20 to 1",
                "Start at 15 and count down",
                "What is one fewer than 13?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Count down: 20, 19, 18, ... what comes next?",
                "expected_type": "number",
                "correct_answer": "17",
                "hints": ["One fewer than eighteen"],
                "explanation": "After 18 going down comes 17.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What number is one fewer than 14?",
                "expected_type": "number",
                "correct_answer": "13",
                "hints": ["Count back one"],
                "explanation": "One fewer than 14 is 13.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Count down from 12. What do you say right after 12?",
                "expected_type": "number",
                "correct_answer": "11",
                "hints": ["One fewer than twelve"],
                "explanation": "11 comes after 12 going down.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Start at 16 and count down to 10. What is the last number you say?",
                "expected_type": "number",
                "correct_answer": "10",
                "hints": ["Stop at ten"],
                "explanation": "Counting down from 16 to 10 ends at 10.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What comes just before 15 when counting backward?",
                "expected_type": "number",
                "correct_answer": "16",
                "hints": ["Going down, what is one more than 15 comes just before it"],
                "explanation": "Going down, 16 comes just before 15.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Which is harder to say backward, the teens or the small numbers? Explain.",
                "expected_type": "text",
                "hints": ["Think about which words are less familiar in reverse"],
                "explanation": "The teens are harder backward because the teen words are less familiar in reverse than small numbers like three, two, one.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "A countdown goes from 20. List the numbers from 20 down to 16.",
                "expected_type": "text",
                "hints": ["Each is one fewer than the last"],
                "explanation": "20, 19, 18, 17, 16.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "You count down from 18 and clap each time until you reach 8. How many claps?",
                "expected_type": "number",
                "correct_answer": "11",
                "hints": ["Count the numbers from 18 down to 8, including both"],
                "explanation": "From 18 down to 8 is 11 numbers, so 11 claps.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Count backward from 20 to 1.",
                "type": "open_response",
                "target_concept": "backward_20",
                "rubric": "Mastery: 20-1 in order, no errors. Proficient: one self-correction in the teens. Developing: skips or reverts to forward.",
            },
            {
                "prompt": "What number is one fewer than 17?",
                "type": "number",
                "target_concept": "one_fewer_teen",
                "correct_answer": "16",
            },
            {
                "prompt": "Start at 13 and count down. What is the next number?",
                "type": "number",
                "target_concept": "count_down_teen",
                "correct_answer": "12",
            },
            {
                "prompt": "Count down from 20 to 15. Write the numbers.",
                "type": "open_response",
                "target_concept": "countdown_sequence",
                "rubric": "Mastery: 20,19,18,17,16,15 correct. Proficient: one slip. Developing: misses teens.",
            },
            {
                "prompt": "Why are the teen numbers tricky to say backward?",
                "type": "open_response",
                "target_concept": "teen_reasoning",
                "rubric": "Mastery: explains unfamiliar teen words. Proficient: says they are hard. Developing: cannot explain.",
            },
        ],
        "resource_guidance": {
            "required": ["a 0-20 number line", "counting objects"],
            "recommended": ["floor number line to 20", "countdown cards"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Trace a number line with a finger going down; keep oral, slow at the teens.",
            "adhd": "Short countdown games; a physical step down per number, focus on the teens.",
            "gifted": "Extend to counting back by twos from twenty and counting back from thirty.",
            "visual_learner": "Use a vertical 0-20 line; move a bright marker down each step.",
            "kinesthetic_learner": "Walk a floor number line backward from twenty.",
            "auditory_learner": "Chant the countdown, saying the teen numbers extra clearly.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "We extend counting down to twenty, slowing through the teens. Today we recite twenty to one and count down from any number to twenty.",
                "gradual_release": {
                    "i_do": "Model counting down from twenty, tracing a number line, slowing on the teen numbers.",
                    "we_do": "Count down from sixteen together, the child tracing the line, then swap roles.",
                    "you_do": "Child counts backward from twenty and from given teen starting numbers independently.",
                },
                "guided_practice": [
                    "Countdown with the teacher tracing the number line through the teens",
                    "Count back from a called teen number to ten",
                ],
                "independent_practice": [
                    "Recite the countdown from twenty",
                    "Count down from five teen starting numbers",
                ],
                "mastery_check": [
                    "Counts backward from 20 to 1",
                    "Handles the teen numbers in reverse",
                    "Counts down from any number to twenty",
                ],
                "spiral_review": ["Re-count down from ten (mf-36) first, then extend the countdown up to twenty"],
            },
            "classical": {
                "narrative_introduction": "Having learned the ladder to twenty, the child now descends it surely, naming each teen rung in reverse as confidently as in order.",
                "memory_work": {
                    "chants": [
                        "Backward chant 20 to 1 daily, saying the teens clearly",
                        "Echo: the teacher names a teen, the child names the one before it going down",
                    ],
                    "recitations": ["A longer countdown rhyme to twenty recited at the start of math time"],
                },
                "recitation_routine": "Begin by reciting yesterday's countdown from ten before extending the reverse count to twenty.",
                "history_integration": "Count down a twenty-day calendar to a coming event, tying the long countdown to time.",
                "read_aloud_suggestions": ["A countdown story to twenty read aloud with building anticipation"],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": ["A countdown picture book that reaches twenty with calm, lovely pictures"],
                "short_lesson_flow": "Trace a hand-drawn 0-20 line and count down together, slowing to name each teen number clearly and calmly.",
                "narration_prompt": "Tell me about counting down from twenty. Which numbers were trickiest?",
                "real_world_objects": [
                    "Twenty steps counted going down",
                    "Counting down beads removed from a string",
                    "Counting down days on a short calendar",
                ],
                "nature_connection": "On a walk, count down twenty paces aloud, naming each teen carefully.",
                "habit_focus": "The habit of perseverance: count all the way down through the harder teen numbers without giving up.",
            },
            "montessori": {
                "prepared_materials": ["A 0-20 number line", "Teen board materials", "Counters or bead bars to remove"],
                "presentation": {
                    "three_period_lesson": "Naming: from fourteen, one fewer is thirteen. Recognition: show me one fewer than fifteen. Recall: what comes before this going down?",
                    "steps": [
                        "Lay the teen quantity with bead bars",
                        "Remove one and name the new teen number",
                        "Continue down through the teens, self-checking each step",
                    ],
                },
                "control_of_error": "Removing one bead at a time through the teens makes each smaller number visible; a wrong name leaves a mismatch to fix.",
                "abstraction_pathway": "From bead bars removed one at a time, to reciting the teens in reverse, toward counting down to twenty in the mind.",
                "extensions": ["Count down by twos from twenty", "Descend the teen board naming each number"],
                "observation_focus": "Watch for smooth reverse counting across the teens and the child self-correcting a teen slip.",
            },
            "unschooling": {
                "invitations": [
                    "Leave a twenty-day countdown calendar to an event the child awaits",
                    "Put out a long bead string the child can pull off one at a time",
                ],
                "real_world_contexts": [
                    "A long countdown before a launch in play",
                    "Counting down a flight of stairs to twenty",
                    "Counting down sleeps on a calendar",
                ],
                "conversation_starters": [
                    "How many are left now, counting down?",
                    "Want to count down from twenty together?",
                ],
                "resource_bank": [
                    "Countdown picture books to twenty left available",
                    "A simple twenty-day calendar to cross off",
                ],
                "parent_role": "Count down from twenty in genuine moments the child cares about and enjoy the teens together, never drilling them.",
                "observation_documentation": "Notice whether the child counts down through the teens confidently in real play; this is the record, not a test.",
            },
        },
        "connections": {
            "reading": "Counting down through a longer sequence read in reverse",
            "science": "Counting down a longer set of observations",
            "history": "Counting down days remaining on a longer timeline",
        },
    },
    "mf-38": {
        "enriched": True,
        "learning_objectives": [
            "Begin counting from a given number instead of starting at one",
            "State the number that comes next after any number within twenty",
            "Count on a stated number of steps from a starting number",
            "Connect counting on with adding more",
        ],
        "teaching_guidance": {
            "introduction": "We do not always have to start at one. We can start at a number we already know and count on from there. If I have eight and count on, I say nine, ten, eleven.",
            "scaffolding_sequence": [
                "Say the next number after a given number",
                "Start at a number and count on to twenty",
                "Count on a few steps from a starting number",
            ],
            "socratic_questions": [
                "What number comes right after twelve?",
                "If you already have nine, why start over at one?",
                "Count on three from six; where do you land?",
            ],
            "practice_activities": [
                "Next-number flashcards",
                "Start-and-continue counting to twenty",
                "Count on from a hidden number of objects plus visible more",
            ],
            "real_world_connections": [
                "Continuing to count guests as more arrive",
                "Counting on points as a game continues",
                "Counting on stairs from a landing",
            ],
            "common_misconceptions": [
                "Always restarting at one; address by hiding the first part and prompting 'you already have eight, count on'",
                "Saying the start number again as the first 'on' step; address by counting on starting with the next number, not repeating the start",
                "Not seeing counting on as adding; address by counting on from a set while adding objects one at a time",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Starts counting from any given number to twenty",
                "Says the next number after any number",
                "Counts on a stated number of steps",
            ],
            "assessment_methods": ["oral counting", "next-number tasks", "observation"],
            "sample_assessment_prompts": [
                "What comes after 14?",
                "Start at 9 and count on to 15",
                "Count on 4 from 11",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What number comes right after 7?",
                "expected_type": "number",
                "correct_answer": "8",
                "hints": ["The next counting number"],
                "explanation": "After 7 comes 8.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Start at 13 and say the next number.",
                "expected_type": "number",
                "correct_answer": "14",
                "hints": ["Just one more"],
                "explanation": "After 13 comes 14.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What comes after 19?",
                "expected_type": "number",
                "correct_answer": "20",
                "hints": ["The next number to twenty"],
                "explanation": "After 19 comes 20.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Start at 10 and count on to 14. What numbers do you say?",
                "expected_type": "text",
                "hints": ["Begin with 11, not 10"],
                "explanation": "11, 12, 13, 14, counting on from ten.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You have 8 blocks and count on 3 more. Where do you land?",
                "expected_type": "number",
                "correct_answer": "11",
                "hints": ["9, 10, 11"],
                "explanation": "Counting on 3 from 8 gives 9, 10, 11, landing on 11.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Why is counting on from 12 faster than starting at 1?",
                "expected_type": "text",
                "hints": ["What do you already know?"],
                "explanation": "You already know there are twelve, so you start at twelve and count only the new ones, instead of recounting from one.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "There are 9 marbles in a cup (you cannot see them) and 4 more on the table. Count on to find the total.",
                "expected_type": "number",
                "correct_answer": "13",
                "hints": ["Start at nine, then count the four: 10, 11, 12, 13"],
                "explanation": "Counting on from 9: 10, 11, 12, 13, so there are 13 in all.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Start at 6 and count on by ones until you reach 12. How many numbers did you say after 6?",
                "expected_type": "number",
                "correct_answer": "6",
                "hints": ["Count the steps: 7, 8, 9, 10, 11, 12"],
                "explanation": "From 7 up to 12 is 6 numbers, so you said 6 numbers after 6.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "What number comes right after 16?",
                "type": "number",
                "target_concept": "next_number",
                "correct_answer": "17",
            },
            {
                "prompt": "Start at 11 and count on to 15.",
                "type": "open_response",
                "target_concept": "count_on",
                "rubric": "Mastery: 12,13,14,15 starting after 11. Proficient: one slip. Developing: restarts at 1.",
            },
            {
                "prompt": "You have 7 and count on 5 more. Where do you land?",
                "type": "number",
                "target_concept": "count_on_total",
                "correct_answer": "12",
            },
            {
                "prompt": "What comes after 18?",
                "type": "number",
                "target_concept": "next_number_teen",
                "correct_answer": "19",
            },
            {
                "prompt": "Why is it faster to count on than to start at one?",
                "type": "open_response",
                "target_concept": "count_on_reasoning",
                "rubric": "Mastery: explains starting from the known amount. Proficient: says it is quicker. Developing: cannot explain.",
            },
        ],
        "resource_guidance": {
            "required": ["counting objects", "a number track 0-20"],
            "recommended": ["number line to 20", "next-number cards"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Keep oral; hide the start set so the child must count on, not recount. No writing.",
            "adhd": "Short turns; physically tap forward on a number line for each 'on' step.",
            "gifted": "Extend to counting on larger jumps and counting on by twos.",
            "visual_learner": "Use a number line and slide a marker forward for each step counted on.",
            "kinesthetic_learner": "Step forward on a floor number line, counting on from a landing.",
            "auditory_learner": "Say only the new numbers aloud, not the starting number again.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "We can start counting from a number we know and count on. Today we say the next number and count on to twenty.",
                "gradual_release": {
                    "i_do": "Model holding eight in a closed hand and counting on, nine, ten, eleven, adding a finger each time.",
                    "we_do": "Count on together from a given number, the child adding objects as you say each next number, then swap.",
                    "you_do": "Child starts from given numbers and counts on a stated number of steps independently.",
                },
                "guided_practice": [
                    "Next-number practice with the teacher confirming",
                    "Count on a few steps from a called start, with objects",
                ],
                "independent_practice": [
                    "Count on to twenty from five different starts",
                    "Count on a stated number of steps and say the total",
                ],
                "mastery_check": [
                    "Starts counting from any given number",
                    "Says the next number to twenty",
                    "Counts on a stated number of steps",
                ],
                "spiral_review": [
                    "Re-count to twenty from one (mf-01) first, then practice starting partway and counting on"
                ],
            },
            "classical": {
                "narrative_introduction": "To count on is the first step of addition: the child holds a number in mind and adds to it, naming each new number in turn.",
                "memory_work": {
                    "chants": [
                        "Chant: name the next number after each number to twenty",
                        "Echo: the teacher says a number, the child says the next",
                    ],
                    "recitations": ["A short rhyme about counting on from where you are, recited daily"],
                },
                "recitation_routine": "Begin by reciting the full count to twenty, then practice starting partway and counting on, reviewing the sequence cumulatively.",
                "history_integration": "Count on years from the child's birth year on a timeline, adding one for each year since.",
                "read_aloud_suggestions": ["A story where a character counts on as more things arrive, read aloud"],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A picture book where a growing group is counted on as more join, with lovely pictures"
                ],
                "short_lesson_flow": "Hold a small known set, then add real objects one at a time, counting on calmly to find the new total together.",
                "narration_prompt": "Tell me how you found the total by counting on. Where did you start?",
                "real_world_objects": [
                    "Counting on guests as they arrive",
                    "Counting on stones added to a small pile",
                    "Counting on steps from a landing",
                ],
                "nature_connection": "On a walk, count on found objects added to a basket that already holds a few.",
                "habit_focus": "The habit of attention: hold the first number in mind and count only the new ones.",
            },
            "montessori": {
                "prepared_materials": [
                    "Counters with a known set hidden under a cup",
                    "Number cards 0-20",
                    "A number line",
                ],
                "presentation": {
                    "three_period_lesson": "Naming: here are eight, count on, nine, ten. Recognition: start at nine and count on. Recall: what is the next number?",
                    "steps": [
                        "Place a known set under a cup",
                        "Count on as objects are added one at a time",
                        "Self-check by lifting the cup and counting all",
                    ],
                },
                "control_of_error": "Lifting the cup to count the whole set checks the count-on total; a mismatch shows a miscount to correct.",
                "abstraction_pathway": "From counting on with hidden sets and added objects, to counting on aloud, toward adding by counting on in the mind.",
                "extensions": ["Count on by twos from a starting number", "Count on from several hidden quantities"],
                "observation_focus": "Watch whether the child starts from the known number without recounting and counts only the new objects.",
            },
            "unschooling": {
                "invitations": [
                    "Leave a growing collection the child adds to over days",
                    "Set out a pile and more objects nearby, say nothing",
                ],
                "real_world_contexts": [
                    "Counting on points as a game goes",
                    "Counting on snacks as more are served",
                    "Counting on guests as they arrive",
                ],
                "conversation_starters": [
                    "You already have some, how many are there now?",
                    "Want to count on instead of starting over?",
                ],
                "resource_bank": [
                    "Collections the child adds to over time",
                    "Board games where you count on spaces from where your piece sits",
                ],
                "parent_role": "In real moments, model counting on from what is already there (the score, the pile) rather than recounting, and let the child join.",
                "observation_documentation": "Notice whether the child counts on from a known amount in real play rather than starting at one; this is the record.",
            },
        },
        "connections": {
            "reading": "Counting on parallels reading on from where a sentence left off",
            "science": "Counting on new observations added to earlier ones",
            "history": "Counting on years from a known date on a timeline",
        },
    },
    "mf-39": {
        "enriched": True,
        "learning_objectives": [
            "Write the numerals 0 through 10 legibly",
            "Form each numeral starting at the correct point with the proper strokes",
            "Match each written numeral to a set of that many objects",
            "Self-correct a reversed or malformed numeral",
        ],
        "teaching_guidance": {
            "introduction": "Now we learn to write the number symbols. Each numeral starts in a certain place and is made with steady strokes. We write zero through ten and match each to the right amount.",
            "scaffolding_sequence": [
                "Trace numerals 0-5 in the air and on paper",
                "Trace and copy numerals 6-10",
                "Write a numeral to label a counted set",
            ],
            "socratic_questions": [
                "Where does this numeral start?",
                "Does your numeral face the right way?",
                "Which set matches the numeral you wrote?",
            ],
            "practice_activities": [
                "Air-write then paper-trace each numeral",
                "Copy numerals from a model with start dots",
                "Label counted sets with the matching numeral",
            ],
            "real_world_connections": [
                "Writing the number of days on a chart",
                "Labeling how many in a drawing",
                "Writing one's age",
            ],
            "common_misconceptions": [
                "Reversing numerals like 3 or 7; address by marking the starting dot and tracing over a model several times",
                "Starting a numeral at the wrong point; address by using start-dot models and naming the path aloud",
                "Writing a numeral that does not match the quantity; address by counting the set and checking the numeral against it",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Writes 0-10 legibly with correct formation",
                "Starts each numeral correctly",
                "Matches written numerals to quantities",
            ],
            "assessment_methods": ["numeral writing", "tracing", "symbol-quantity matching"],
            "sample_assessment_prompts": [
                "Write the number 6",
                "Trace this 8 and then write your own",
                "Write the numeral for this set of 4",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Write the numeral that means 'three'.",
                "expected_type": "number",
                "correct_answer": "3",
                "hints": ["Start at the top and make two curves"],
                "explanation": "The numeral 3 stands for three.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Write the numeral for a set of 5 objects.",
                "expected_type": "number",
                "correct_answer": "5",
                "hints": ["Count the set first, then write"],
                "explanation": "Five objects are written as 5.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Write the numeral that comes after 6.",
                "expected_type": "number",
                "correct_answer": "7",
                "hints": ["What comes after six?"],
                "explanation": "After 6 is 7.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Count this set of 8 and write the numeral.",
                "expected_type": "number",
                "correct_answer": "8",
                "hints": ["Count carefully, then form the 8 with two loops"],
                "explanation": "Eight objects are written as 8.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Write the numerals from 0 to 5 in order.",
                "expected_type": "text",
                "hints": ["Start each at its correct point"],
                "explanation": "0, 1, 2, 3, 4, 5 written in order.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Your 7 looks backward. Tell how to fix it.",
                "expected_type": "text",
                "hints": ["Where should the 7 start?"],
                "explanation": "Start at the top-left, draw straight across, then slant down to the right so the 7 faces forward.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Write the numeral for 'nine' and draw a set with that many dots.",
                "expected_type": "text",
                "hints": ["Form the 9, then make nine dots"],
                "explanation": "Write 9 and draw nine dots, matching the symbol to the quantity.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Write 0 to 10 and circle the numerals that are easy to reverse.",
                "expected_type": "text",
                "hints": ["Think about 2, 3, 6, 7, 9"],
                "explanation": "Write 0-10; numerals like 2, 3, 6, 7, and 9 are easy to reverse and need careful starting points.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Write the numerals from 0 to 10 in order.",
                "type": "open_response",
                "target_concept": "numeral_formation",
                "rubric": "Mastery: 0-10 legible, correct orientation. Proficient: one reversal. Developing: several reversals or gaps.",
            },
            {
                "prompt": "Write the numeral for this set of 6 objects.",
                "type": "number",
                "target_concept": "symbol_quantity",
                "correct_answer": "6",
            },
            {
                "prompt": "Write the numeral that means 'four'.",
                "type": "number",
                "target_concept": "numeral_writing",
                "correct_answer": "4",
            },
            {
                "prompt": "Write the numeral that comes after 8.",
                "type": "number",
                "target_concept": "next_numeral",
                "correct_answer": "9",
            },
            {
                "prompt": "How do you keep a numeral from facing backward?",
                "type": "open_response",
                "target_concept": "formation_reasoning",
                "rubric": "Mastery: names correct start point/path. Proficient: says 'check the way it faces.' Developing: cannot explain.",
            },
        ],
        "resource_guidance": {
            "required": ["pencil and paper", "numeral models with start dots"],
            "recommended": ["sand tray or whiteboard", "numeral tracing cards"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Use start-dot models and verbal stroke cues; allow tracing in sand or on a whiteboard before paper.",
            "adhd": "Short writing bursts; trace one numeral well rather than many quickly.",
            "gifted": "Extend to writing teen numerals and writing numerals to label larger sets.",
            "visual_learner": "Use numerals with directional arrows and start dots.",
            "kinesthetic_learner": "Form numerals large in sand or in the air before writing small.",
            "auditory_learner": "Say the stroke path aloud while writing (top, around, down).",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Each numeral has a correct starting point and path. Today we write zero to ten and match each to its amount.",
                "gradual_release": {
                    "i_do": "Model forming a 6 aloud: start at the top, curve down and around into a loop, naming the path.",
                    "we_do": "Trace and write a few numerals together, the child following the start dots, then writing alone.",
                    "you_do": "Child writes 0 to 10 independently and labels counted sets with the right numeral.",
                },
                "guided_practice": [
                    "Trace numerals over models with the teacher cueing the path",
                    "Write a numeral to match a counted set",
                ],
                "independent_practice": ["Write 0 to 10 from memory", "Label five counted sets with numerals"],
                "mastery_check": [
                    "Writes 0-10 legibly with correct formation",
                    "Starts each numeral correctly",
                    "Matches numerals to quantities",
                ],
                "spiral_review": [
                    "Re-count a set to ten with objects (mf-32), then write the matching numeral to label it"
                ],
            },
            "classical": {
                "narrative_introduction": "The hand is trained as the voice is: by careful repetition, the forms of the numerals become as sure and neat as well-copied letters.",
                "memory_work": {
                    "chants": [
                        "Chant the stroke path for each numeral as it is formed",
                        "Recite the numerals in order while pointing to each written form",
                    ],
                    "recitations": ["A short rhyme naming the shapes of the numbers, recited daily"],
                },
                "copywork": ["Copy the numerals 0 to 10 in order, neatly, building the memory of their forms"],
                "recitation_routine": "Begin each lesson by tracing yesterday's numerals from memory before adding new ones, reviewing the forms cumulatively.",
                "history_integration": "Copy the numerals for the years on a simple personal timeline, joining number-writing to chronology.",
                "read_aloud_suggestions": ["A well-made counting book whose clear numerals can be admired and copied"],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 12,
                "living_book_suggestions": ["A counting book with beautiful, clear numerals worth copying"],
                "short_lesson_flow": "Form a numeral large in a sand tray, naming its path, then copy it once neatly on paper; keep the lesson short and calm.",
                "narration_prompt": "Tell me about the numeral you wrote. Where did you start it?",
                "real_world_objects": [
                    "Numbers written to label a nature notebook count",
                    "House numbers noticed on a walk",
                    "The numeral for the child's age",
                ],
                "nature_connection": "Write the numeral for a count of found objects in the nature notebook beside a small drawing.",
                "habit_focus": "The habit of neatness: form each numeral carefully, the right way round, taking pride in the work.",
            },
            "montessori": {
                "prepared_materials": [
                    "Sandpaper numerals 0-10",
                    "Sand tray",
                    "Cards and counters to match numerals to quantities",
                ],
                "presentation": {
                    "three_period_lesson": "Naming: trace the sandpaper six, this is six. Recognition: trace me six. Recall: what number is this?",
                    "steps": [
                        "Trace the sandpaper numeral with two fingers, saying its name",
                        "Form the numeral in the sand tray",
                        "Lay the matching quantity of counters beside it to self-check",
                    ],
                },
                "control_of_error": "The sandpaper numeral and the counter quantity together reveal error: a malformed or mismatched numeral is felt and seen.",
                "abstraction_pathway": "From tracing the textured numeral, to writing it in sand, toward writing it on paper from the held form.",
                "extensions": [
                    "Write the numerals while building the matching teen quantities",
                    "Match written numerals to bead bars",
                ],
                "observation_focus": "Watch for correct tracing direction, careful formation, and the child matching each numeral to its quantity.",
            },
            "unschooling": {
                "invitations": [
                    "Leave numeral stamps, magnets, or stencils within reach",
                    "Put out a whiteboard and markers near where the child plays",
                ],
                "real_world_contexts": [
                    "Writing how many on a drawing the child made",
                    "Writing the number of pets or toys on a label",
                    "Writing one's own age on artwork",
                ],
                "conversation_starters": [
                    "Want to write how many you counted?",
                    "What number would you put on your picture?",
                ],
                "resource_bank": [
                    "Numeral magnets, stamps, and stencils left available",
                    "A whiteboard and markers for free use",
                ],
                "parent_role": "Offer playful ways to make numerals (stamps, magnets, sand) and write real numbers the child wants to label, never as handwriting drill.",
                "observation_documentation": "Notice over time whether the child forms numerals to label real things and self-corrects reversals; this is the record.",
            },
        },
        "connections": {
            "reading": "Numeral formation parallels letter formation in early writing",
            "science": "Writing the count of specimens on a label",
            "history": "Writing year numerals on a personal timeline",
        },
    },
    "mf-40": {
        "enriched": True,
        "learning_objectives": [
            "Write the numerals 11 through 20 legibly",
            "Form two-digit teen numerals with the digits in the correct order",
            "Match a teen numeral to a set of that many objects",
            "Recognize that a teen numeral shows one ten and some ones",
        ],
        "teaching_guidance": {
            "introduction": "Teen numbers are written with two digits: a 1 for the ten, then a digit for the ones. Fourteen is 1 then 4. Today we write eleven through twenty and match each to its amount.",
            "scaffolding_sequence": [
                "Trace teen numerals 11-15 over models",
                "Trace and copy 16-20",
                "Write a teen numeral to label a counted teen set",
            ],
            "socratic_questions": [
                "Which digit shows the ten? Which shows the ones?",
                "Are your two digits in the right order?",
                "Does this teen numeral match the set?",
            ],
            "practice_activities": [
                "Trace then write each teen numeral",
                "Build a teen on a ten-frame and write its numeral",
                "Label teen sets with the matching numeral",
            ],
            "real_world_connections": [
                "Writing the day's date when it is in the teens",
                "Labeling a count of fifteen objects",
                "Writing a teen house number",
            ],
            "common_misconceptions": [
                "Reversing digit order (writing 41 for 14); address by saying 'ten first, then ones' and using ten-frame models",
                "Writing teen numbers as one digit; address by showing the ten and the ones separately, then together as two digits",
                "Mismatching numeral and quantity; address by building the teen on a double ten-frame and checking the numeral",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Writes 11-20 legibly with correct formation",
                "Orders the two digits correctly",
                "Matches teen numerals to quantities",
            ],
            "assessment_methods": ["numeral writing", "ten-frame matching", "symbol-quantity matching"],
            "sample_assessment_prompts": [
                "Write the number 14",
                "Build 16 and write its numeral",
                "Write the numeral for this set of 18",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Write the numeral that means 'eleven'.",
                "expected_type": "number",
                "correct_answer": "11",
                "hints": ["A one for the ten, then a one for the one"],
                "explanation": "Eleven is written 11.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Write the numeral that comes after 14.",
                "expected_type": "number",
                "correct_answer": "15",
                "hints": ["What comes after fourteen?"],
                "explanation": "After 14 is 15.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Write the numeral for 'twenty'.",
                "expected_type": "number",
                "correct_answer": "20",
                "hints": ["A two and a zero"],
                "explanation": "Twenty is written 20.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Build 13 on ten-frames, then write the numeral.",
                "expected_type": "number",
                "correct_answer": "13",
                "hints": ["A full ten and three more"],
                "explanation": "A ten and three ones is written 13.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Write the teen numerals from 11 to 15 in order.",
                "expected_type": "text",
                "hints": ["Each starts with a 1 for the ten"],
                "explanation": "11, 12, 13, 14, 15 written in order.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "A child wrote 71 for seventeen. Tell what went wrong and the right way.",
                "expected_type": "text",
                "hints": ["Which digit shows the ten?"],
                "explanation": "The digits are in the wrong order; seventeen is a ten and seven ones, written 17, with the 1 for the ten first.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Write the numeral for 'nineteen' and show it as one ten and nine ones.",
                "expected_type": "text",
                "hints": ["Write 19, then 10 and 9"],
                "explanation": "Nineteen is 19, which is one ten (10) and nine ones (9).",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Write 11 to 20 and circle the one that is a ten with no extra ones.",
                "expected_type": "text",
                "hints": ["Which teen-range number is exactly two tens or one ten and zero ones?"],
                "explanation": "Write 11-20; circle 20 (or note 10 hides in each), since 10 is a ten with no extra ones and 20 is two tens.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Write the numerals from 11 to 20 in order.",
                "type": "open_response",
                "target_concept": "teen_formation",
                "rubric": "Mastery: 11-20 legible, digits ordered correctly. Proficient: one reversal. Developing: several digit-order errors.",
            },
            {
                "prompt": "Write the numeral for this set of 16 objects.",
                "type": "number",
                "target_concept": "teen_symbol_quantity",
                "correct_answer": "16",
            },
            {
                "prompt": "Write the numeral that means 'twelve'.",
                "type": "number",
                "target_concept": "teen_numeral",
                "correct_answer": "12",
            },
            {
                "prompt": "Write the numeral that comes after 18.",
                "type": "number",
                "target_concept": "next_teen_numeral",
                "correct_answer": "19",
            },
            {
                "prompt": "In the numeral 15, which digit shows the ten? Explain.",
                "type": "open_response",
                "target_concept": "place_in_writing",
                "rubric": "Mastery: names the 1 as the ten. Proficient: partial. Developing: cannot explain.",
            },
        ],
        "resource_guidance": {
            "required": ["pencil and paper", "double ten-frame", "teen numeral models"],
            "recommended": ["place-value cards", "teen tracing cards"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Use ten-frame models with the numeral; allow tracing before paper; say 'ten first, then ones.'",
            "adhd": "Short bursts; form one teen numeral well with a build beside it.",
            "gifted": "Extend to writing numerals past twenty and to writing two-digit numbers from spoken words.",
            "visual_learner": "Color the tens digit and ones digit differently to show their roles.",
            "kinesthetic_learner": "Build the teen on frames, then write large before small.",
            "auditory_learner": "Say the digits aloud in order while writing (one ten, four ones).",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Teen numerals have two digits: the ten, then the ones. Today we write eleven to twenty and match each to its amount.",
                "gradual_release": {
                    "i_do": "Model writing 14 aloud: a 1 for the ten, then a 4 for the ones, beside a full ten-frame and four more.",
                    "we_do": "Build and write a few teens together, the child placing the digits in order, then writing alone.",
                    "you_do": "Child writes 11 to 20 independently and labels teen sets with the right numeral.",
                },
                "guided_practice": [
                    "Trace teen numerals over models with the teacher cueing digit order",
                    "Build a teen and write its numeral",
                ],
                "independent_practice": ["Write 11 to 20 from memory", "Label five teen sets with numerals"],
                "mastery_check": [
                    "Writes 11-20 legibly",
                    "Orders the two digits correctly",
                    "Matches teen numerals to quantities",
                ],
                "spiral_review": [
                    "Re-form the single-digit numerals 0-10 (mf-39) first, then build each teen as a ten and ones to write 11-20"
                ],
            },
            "classical": {
                "narrative_introduction": "The teen numerals teach the eye its first two-digit forms: the ten standing first, the ones beside it, a small order to be learned exactly.",
                "memory_work": {
                    "chants": [
                        "Chant each teen as ten and ones while writing it",
                        "Recite the teen numerals in order pointing to each written form",
                    ],
                    "recitations": ["A short rhyme naming the teens as ten-and-some-more, recited daily"],
                },
                "copywork": ["Copy the teen numerals 11 to 20 neatly in order, the ten digit first"],
                "recitation_routine": "Begin by tracing yesterday's teen numerals from memory before adding more, reviewing the forms cumulatively.",
                "history_integration": "Copy teen year-numerals on a timeline of a decade, joining two-digit writing to chronology.",
                "read_aloud_suggestions": ["A counting book whose teen numerals are clearly shown to copy"],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 12,
                "living_book_suggestions": ["A counting book showing the teens with clear, lovely two-digit numerals"],
                "short_lesson_flow": "Build a teen on a ten-frame, name it as ten and ones, and copy its numeral once, neatly; keep the lesson short.",
                "narration_prompt": "Tell me about the teen number you wrote. Which digit is the ten?",
                "real_world_objects": [
                    "Writing a teen count in the nature notebook",
                    "Noticing teen house numbers on a walk",
                    "Writing the date when it is in the teens",
                ],
                "nature_connection": "Write the teen numeral for a count of found objects beside a small drawing in the nature notebook.",
                "habit_focus": "The habit of neatness: place the two digits in the right order, carefully formed.",
            },
            "montessori": {
                "prepared_materials": [
                    "Sandpaper teen numerals or printed models",
                    "Teen board with bead bars",
                    "Place-value cards (tens and ones)",
                ],
                "presentation": {
                    "three_period_lesson": "Naming: build fourteen, ten and four, write 14. Recognition: write me fourteen. Recall: what number is this?",
                    "steps": [
                        "Build the teen on the teen board with a ten and ones",
                        "Write the two digits in order, ten first",
                        "Lay place-value cards over the numeral to self-check",
                    ],
                },
                "control_of_error": "The place-value cards and bead bars reveal a digit-order error: 41 will not match a ten and four ones.",
                "abstraction_pathway": "From building the teen with ten and ones, to writing the two digits, toward writing teen numerals from the held idea.",
                "extensions": [
                    "Write teen numerals while building each on the teen board",
                    "Match written teens to place-value cards",
                ],
                "observation_focus": "Watch for correct digit order, careful formation, and the child matching each teen numeral to ten-and-ones.",
            },
            "unschooling": {
                "invitations": [
                    "Leave place-value cards or magnetic digits within reach",
                    "Put out a whiteboard near the teen-numbered things in the home",
                ],
                "real_world_contexts": [
                    "Writing a teen count on a drawing",
                    "Writing a teen date on a calendar",
                    "Labeling a collection of a teen number of items",
                ],
                "conversation_starters": [
                    "Want to write how many you counted? It is in the teens.",
                    "Which two digits make fourteen?",
                ],
                "resource_bank": [
                    "Magnetic digits and place-value cards left available",
                    "A whiteboard for free number-writing",
                ],
                "parent_role": "Offer playful materials for making teen numerals and write real teen numbers the child cares about, never as drill.",
                "observation_documentation": "Notice whether the child forms teen numerals with the digits in order in real labeling; this is the record.",
            },
        },
        "connections": {
            "reading": "Writing two-digit teen numerals parallels writing short words letter by letter",
            "science": "Labeling a teen count of specimens",
            "history": "Writing teen year-numerals on a timeline",
        },
    },
    "mf-41": {
        "enriched": True,
        "learning_objectives": [
            "Count by ones from any number up to one hundred twenty",
            "Cross decade boundaries smoothly (e.g., 39 to 40, 99 to 100, 109 to 110)",
            "Continue the counting sequence past one hundred",
            "Read and say three-digit numbers up to 120 in the counting sequence",
        ],
        "teaching_guidance": {
            "introduction": "We keep counting past one hundred, all the way to one hundred twenty. The tricky spots are the turns at each ten, like fifty-nine to sixty, and the turn past one hundred.",
            "scaffolding_sequence": [
                "Count across a single decade turn (e.g., 28 to 32)",
                "Count from 95 to 105 across the hundred",
                "Count from a given number up toward 120",
            ],
            "socratic_questions": [
                "What number comes right after 109?",
                "What is the tricky turn here, and what comes next?",
                "After ninety-nine, what number do we say?",
            ],
            "practice_activities": [
                "Count along a 120 chart, pointing to each number",
                "Count across decade turns from given starts",
                "Count a large set by ones toward 120",
            ],
            "real_world_connections": [
                "Counting a large collection of stickers past one hundred",
                "Counting pages in a longer book",
                "Counting steps on a long walk",
            ],
            "common_misconceptions": [
                "Stopping or restarting at one hundred; address by practicing 98, 99, 100, 101 as a smooth turn",
                "Saying 'twenty-ten' instead of thirty at a decade turn; address by drilling the turns 29-30, 39-40 on a chart",
                "Skipping a decade (jumping 89 to 100); address by tracing each number on a 120 chart across the turn",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Counts by ones to 120",
                "Crosses every decade and the hundred smoothly",
                "Counts from any starting number toward 120",
            ],
            "assessment_methods": ["oral counting", "120-chart tracing", "observation"],
            "sample_assessment_prompts": [
                "Count from 95 to 110",
                "What comes after 119?",
                "Start at 78 and count to 90",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Count on: 100, 101, 102, ... what comes next?",
                "expected_type": "number",
                "correct_answer": "103",
                "hints": ["One more than 102"],
                "explanation": "After 102 comes 103.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What number comes right after 109?",
                "expected_type": "number",
                "correct_answer": "110",
                "hints": ["The turn past 109"],
                "explanation": "After 109 comes 110.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What comes after 119?",
                "expected_type": "number",
                "correct_answer": "120",
                "hints": ["The last number here"],
                "explanation": "After 119 comes 120.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Count from 98 to 103. What numbers do you say?",
                "expected_type": "text",
                "hints": ["Cross one hundred carefully"],
                "explanation": "98, 99, 100, 101, 102, 103.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What number comes right after 99?",
                "expected_type": "number",
                "correct_answer": "100",
                "hints": ["The turn past ninety-nine"],
                "explanation": "After 99 comes 100.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Why do people sometimes stumble right after 99 or 109?",
                "expected_type": "text",
                "hints": ["Think about the decade and hundred turns"],
                "explanation": "Those are turning points where the next ten or hundred begins, so the next word changes a lot, which is easy to stumble on.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Start at 88 and count to 92, writing each number.",
                "expected_type": "text",
                "hints": ["Cross the 89-90 turn carefully"],
                "explanation": "88, 89, 90, 91, 92, crossing the decade turn at 90.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "How many numbers do you say counting from 110 to 120, including both?",
                "expected_type": "number",
                "correct_answer": "11",
                "hints": ["Count the numbers 110, 111, ... 120"],
                "explanation": "From 110 to 120 inclusive is 11 numbers.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Count by ones from 95 to 110.",
                "type": "open_response",
                "target_concept": "count_past_100",
                "rubric": "Mastery: 95-110 in order, crosses 100 smoothly. Proficient: one slip. Developing: stops or restarts at 100.",
            },
            {
                "prompt": "What number comes right after 109?",
                "type": "number",
                "target_concept": "decade_turn",
                "correct_answer": "110",
            },
            {
                "prompt": "What comes after 119?",
                "type": "number",
                "target_concept": "count_to_120",
                "correct_answer": "120",
            },
            {
                "prompt": "Start at 79 and count to 83.",
                "type": "open_response",
                "target_concept": "decade_crossing",
                "rubric": "Mastery: 79,80,81,82,83 correct. Proficient: one slip at 80. Developing: misses the turn.",
            },
            {
                "prompt": "Why is the count just after 99 a tricky spot?",
                "type": "open_response",
                "target_concept": "boundary_reasoning",
                "rubric": "Mastery: explains the hundred turn. Proficient: says it is hard. Developing: cannot explain.",
            },
        ],
        "resource_guidance": {
            "required": ["a 120 chart", "a large set of objects to count"],
            "recommended": ["pointer for the chart", "groups of ten to bundle"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Trace a 120 chart with a finger; keep oral; rehearse the decade and hundred turns slowly.",
            "adhd": "Short counting sprints across one turn at a time; use a pointer on the chart.",
            "gifted": "Extend to counting to 200 and counting by tens past one hundred.",
            "visual_learner": "Use a color-banded 120 chart so each decade stands out.",
            "kinesthetic_learner": "Point to each number on a wall chart while stepping in place.",
            "auditory_learner": "Chant across the turns, saying the new decade word extra clearly.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "We count past one hundred to 120, with care at each ten and at the hundred. Today we count across the turns.",
                "gradual_release": {
                    "i_do": "Model counting from 98 to 103 on a chart, pointing and slowing across one hundred.",
                    "we_do": "Count across a decade turn together, the child pointing on the chart, then swap.",
                    "you_do": "Child counts from given starts up toward 120, crossing decades and the hundred independently.",
                },
                "guided_practice": [
                    "Count across turns with the teacher pointing on the 120 chart",
                    "Count from a called number across one hundred",
                ],
                "independent_practice": [
                    "Count from five different starts toward 120",
                    "Count a large set by ones past one hundred",
                ],
                "mastery_check": [
                    "Counts by ones to 120",
                    "Crosses decades and the hundred smoothly",
                    "Counts from any starting number",
                ],
                "spiral_review": [
                    "Re-count to one hundred (mf-04) first, then extend smoothly past one hundred to 120"
                ],
            },
            "classical": {
                "narrative_introduction": "The counting ladder, once reaching one hundred, climbs on without end; here the child learns to step past the hundred surely, to 120.",
                "memory_work": {
                    "chants": [
                        "Chant across the decade turns: 28, 29, 30; 99, 100, 101",
                        "Recite the count from ninety to one hundred ten",
                    ],
                    "recitations": ["A counting rhyme that crosses one hundred, recited daily"],
                },
                "recitation_routine": "Begin by counting yesterday's range before extending past one hundred, reviewing the sequence cumulatively.",
                "history_integration": "Count years across a century mark on a timeline, tying the hundred turn to history.",
                "read_aloud_suggestions": ["A counting book that reaches beyond one hundred, read aloud"],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 12,
                "living_book_suggestions": ["A counting book that goes past one hundred with calm, clear numbers"],
                "short_lesson_flow": "Count a real collection of small objects past one hundred together on a chart, calmly crossing each turn.",
                "narration_prompt": "Tell me about counting past one hundred. Which turns were tricky?",
                "real_world_objects": [
                    "Counting a jar of buttons past one hundred",
                    "Counting pages of a longer book",
                    "Counting paces on a long walk",
                ],
                "nature_connection": "On a long walk, count paces past one hundred aloud, naming each decade turn clearly.",
                "habit_focus": "The habit of perseverance: keep counting carefully across the harder turns without losing the place.",
            },
            "montessori": {
                "prepared_materials": [
                    "A 120 chart",
                    "Golden beads or bundles of ten and hundred",
                    "Number cards past one hundred",
                ],
                "presentation": {
                    "three_period_lesson": "Naming: after ninety-nine comes one hundred. Recognition: point to one hundred ten. Recall: what comes after this?",
                    "steps": [
                        "Lay out ten bundles to make one hundred",
                        "Count on past one hundred with single beads",
                        "Self-check the count against the 120 chart",
                    ],
                },
                "control_of_error": "The bead bundles and chart together reveal a missed turn: a gap at a decade shows the count to redo.",
                "abstraction_pathway": "From counting beads past one hundred, to reciting the sequence, toward counting to 120 in the mind.",
                "extensions": ["Count by tens past one hundred", "Lay number cards in order to 120"],
                "observation_focus": "Watch for smooth counting across the decade and hundred turns and the child self-correcting a slip.",
            },
            "unschooling": {
                "invitations": [
                    "Leave a 120 chart and a jar of countable objects out",
                    "Put out a long bead string or chain to count past one hundred",
                ],
                "real_world_contexts": [
                    "Counting a big collection past one hundred",
                    "Counting a long list of items",
                    "Counting many steps on a walk",
                ],
                "conversation_starters": [
                    "I wonder how many are in this jar, more than a hundred?",
                    "Want to keep counting past one hundred?",
                ],
                "resource_bank": ["A 120 chart left available", "Big collections the child likes to count"],
                "parent_role": "When the child wants to count a big pile, count alongside past one hundred for the joy of it, helping at the tricky turns, never drilling.",
                "observation_documentation": "Notice whether the child counts past one hundred and crosses the turns in real counting; this is the record.",
            },
        },
        "connections": {
            "reading": "Reading on through a longer text parallels counting on past one hundred",
            "science": "Counting a large set of observations past one hundred",
            "history": "Counting years across a century on a timeline",
        },
    },
    "mf-42": {
        "enriched": True,
        "learning_objectives": [
            "Locate any number from one to one hundred on a hundreds chart",
            "Recognize that moving one space right adds one",
            "Recognize that moving one space down adds ten",
            "Use rows (tens) and columns (ones) to find numbers efficiently",
        ],
        "teaching_guidance": {
            "introduction": "The hundreds chart is a map of numbers one to one hundred, ten in each row. Moving right one space adds one. Moving down one space adds ten. This helps us find and compare numbers fast.",
            "scaffolding_sequence": [
                "Find given numbers by row and column",
                "Move right and name the new number (+1)",
                "Move down and name the new number (+10)",
            ],
            "socratic_questions": [
                "If you move one space right, what happens to the number?",
                "If you move one space down, how much bigger is it?",
                "Which row holds the forties?",
            ],
            "practice_activities": [
                "Find-the-number races on the chart",
                "Move right/down/left/up and name the result",
                "Color a row or column and describe the pattern",
            ],
            "real_world_connections": [
                "Using a calendar grid to find a date",
                "Reading a seating chart by row and seat",
                "Finding a number on a locker chart",
            ],
            "common_misconceptions": [
                "Thinking down adds one (like right); address by tracing a column and noticing each step down adds ten",
                "Losing the row when scanning; address by sliding a finger along the row first, then down the column",
                "Confusing rows and columns; address by naming 'across is ones, down is tens' while pointing",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Finds numbers to 100 on the chart quickly",
                "Knows +1 is right and +10 is down",
                "Uses rows and columns to locate numbers",
            ],
            "assessment_methods": ["chart navigation", "oral response", "demonstration"],
            "sample_assessment_prompts": [
                "Find 47 on the chart",
                "Move one space down from 23. What number?",
                "Which row has the seventies?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "On a hundreds chart, you are on 34 and move one space right. What number now?",
                "expected_type": "number",
                "correct_answer": "35",
                "hints": ["Right adds one"],
                "explanation": "Moving right from 34 gives 35.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "You are on 50 and move one space down. What number?",
                "expected_type": "number",
                "correct_answer": "60",
                "hints": ["Down adds ten"],
                "explanation": "Moving down from 50 gives 60.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which number is just to the right of 19?",
                "expected_type": "number",
                "correct_answer": "20",
                "hints": ["Right adds one"],
                "explanation": "Just right of 19 is 20.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You are on 27 and move down one space. What number?",
                "expected_type": "number",
                "correct_answer": "37",
                "hints": ["Down adds ten"],
                "explanation": "Down from 27 is 37.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Start at 45. Move right 2 spaces. Where do you land?",
                "expected_type": "number",
                "correct_answer": "47",
                "hints": ["Two ones to the right"],
                "explanation": "Right twice from 45 lands on 47.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Explain why moving straight down on the chart adds ten each time.",
                "expected_type": "text",
                "hints": ["Each row holds ten numbers"],
                "explanation": "Each row has ten numbers, so the number directly below is exactly ten more, one for each space in the row.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "You are on 33. Move down 1 and right 1. What number do you reach?",
                "expected_type": "number",
                "correct_answer": "44",
                "hints": ["Down adds ten, right adds one: 33 to 43 to 44"],
                "explanation": "Down to 43, then right to 44.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Without counting one by one, tell how to jump from 22 to 52 on the chart.",
                "expected_type": "text",
                "hints": ["How many tens is that? Which direction?"],
                "explanation": "Move straight down three rows, because each row down adds ten and 52 is thirty more than 22.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "On a hundreds chart, you are on 41 and move one space down. What number?",
                "type": "number",
                "target_concept": "plus_ten_down",
                "correct_answer": "51",
            },
            {
                "prompt": "You are on 68 and move one space right. What number?",
                "type": "number",
                "target_concept": "plus_one_right",
                "correct_answer": "69",
            },
            {
                "prompt": "Which row of the chart holds the eighties?",
                "type": "open_response",
                "target_concept": "row_structure",
                "rubric": "Mastery: names the row starting at 81 (or 80s row). Proficient: points near it. Developing: cannot locate.",
            },
            {
                "prompt": "Start at 25 and move down 2 spaces. Where do you land?",
                "type": "number",
                "target_concept": "multi_down",
                "correct_answer": "45",
            },
            {
                "prompt": "Why does moving down a column add ten each step?",
                "type": "open_response",
                "target_concept": "chart_reasoning",
                "rubric": "Mastery: ten per row. Proficient: says 'it gets bigger by ten.' Developing: cannot explain.",
            },
        ],
        "resource_guidance": {
            "required": ["a hundreds chart", "a marker or counter to move"],
            "recommended": ["laminated chart and dry-erase marker", "movable game token"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Use a large, color-banded chart; trace rows and columns with a finger; keep oral.",
            "adhd": "Short find-and-move games; one move at a time, celebrate quick finds.",
            "gifted": "Extend to +10/-10 jumps and to a 120 chart with multi-step moves.",
            "visual_learner": "Shade alternating rows or columns so the grid structure stands out.",
            "kinesthetic_learner": "Move a physical token on a floor-sized chart, stepping right and down.",
            "auditory_learner": "Say each move aloud: right is plus one, down is plus ten.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "The hundreds chart maps the numbers in rows of ten. Right adds one, down adds ten. Today we find numbers and move on the chart.",
                "gradual_release": {
                    "i_do": "Model finding 47 by sliding along the forties row to the seven, then move down to show 57 is ten more.",
                    "we_do": "Find numbers and make right/down moves together, the child moving the marker, then swap.",
                    "you_do": "Child finds called numbers and makes right/down moves, naming each result independently.",
                },
                "guided_practice": [
                    "Find-and-move tasks with the teacher confirming the rule",
                    "Make a stated right or down move and name the result",
                ],
                "independent_practice": [
                    "Find ten called numbers on the chart",
                    "Make right and down moves from given starts",
                ],
                "mastery_check": [
                    "Finds numbers to 100 quickly",
                    "Knows +1 is right and +10 is down",
                    "Uses rows and columns to locate numbers",
                ],
                "spiral_review": [
                    "Re-count to one hundred (mf-04), then place those numbers on the chart to see the rows-of-ten structure"
                ],
            },
            "classical": {
                "narrative_introduction": "The hundreds chart is an orderly tablet of the numbers, ten to a line; once its rule is known, the eye moves on it as on a familiar page.",
                "memory_work": {
                    "chants": [
                        "Chant a row across (forty-one, forty-two, ...) and a column down (five, fifteen, twenty-five)",
                        "Recite the rule: across adds one, down adds ten",
                    ],
                    "recitations": ["A short saying recited daily: rows are tens, columns are ones"],
                },
                "recitation_routine": "Begin by reading yesterday's row and column from memory before exploring new ones, reviewing the structure cumulatively.",
                "history_integration": "Compare the chart's grid to an old census or tally laid out in orderly rows and columns.",
                "read_aloud_suggestions": ["A number book that lays numbers in neat rows to study"],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 12,
                "living_book_suggestions": ["A number book whose pages arrange numbers in tidy rows to admire"],
                "short_lesson_flow": "Explore a real hundreds chart together: find a few numbers, notice that down adds ten, calmly, then stop.",
                "narration_prompt": "Tell me what you noticed about moving down the chart. What changed?",
                "real_world_objects": [
                    "Finding a date on a calendar grid",
                    "Reading a seat by row and number",
                    "Locating a house number on a street map of numbers",
                ],
                "nature_connection": "Notice orderly rows and columns in nature and design (windows in a building, cells in a honeycomb).",
                "habit_focus": "The habit of orderliness: read across the row first, then down the column, without rushing.",
            },
            "montessori": {
                "prepared_materials": [
                    "A hundreds chart",
                    "Golden bead tens to show the +10 down move",
                    "Number tiles to place on the chart",
                ],
                "presentation": {
                    "three_period_lesson": "Naming: this is the row of forties. Recognition: find the column of ones ending in three. Recall: what number is here?",
                    "steps": [
                        "Slide along a row to find the ones",
                        "Move down a column to add ten",
                        "Self-check by laying a ten-bead beside a down move",
                    ],
                },
                "control_of_error": "A ten-bead laid beside a down move shows the jump is exactly ten; a wrong landing is seen and corrected.",
                "abstraction_pathway": "From moving a marker on the chart, to knowing the right/down rules, toward picturing the chart in the mind.",
                "extensions": [
                    "Place number tiles to rebuild a row or column",
                    "Make +10 and -10 jumps and verify with bead tens",
                ],
                "observation_focus": "Watch whether the child uses rows and columns to find numbers and applies the +1/+10 rule without counting.",
            },
            "unschooling": {
                "invitations": [
                    "Leave a hundreds chart on the wall where the child plays",
                    "Put out a chart and a game token to move freely",
                ],
                "real_world_contexts": [
                    "Finding a day on the calendar grid",
                    "Finding a seat number by row",
                    "Finding a number on a board-game track",
                ],
                "conversation_starters": [
                    "Can you find that number on the chart?",
                    "What do you notice when you go straight down?",
                ],
                "resource_bank": ["A hundreds chart left on the wall", "Board games with numbered grids"],
                "parent_role": "Let the child explore the chart as a map and notice the patterns in their own play; answer questions and point out the down-adds-ten rule only when it sparks curiosity.",
                "observation_documentation": "Notice whether the child finds numbers by row and column and senses the +1/+10 moves in real play; this is the record.",
            },
        },
        "connections": {
            "reading": "Reading a grid by row and column parallels reading a chart or table",
            "science": "Reading data tables arranged in rows and columns",
            "history": "Reading a timeline or census laid out in an orderly grid",
        },
    },
    "mf-43": {
        "enriched": True,
        "learning_objectives": [
            "Write any numeral from zero to one hundred legibly",
            "Form two-digit numerals with the tens digit first and the ones digit second",
            "Write the numeral that matches a spoken number name to one hundred",
            "Write one hundred as 100",
        ],
        "teaching_guidance": {
            "introduction": "We can write every number to one hundred. A two-digit number is written with the tens first, then the ones: forty-six is 4 then 6. One hundred is written 100. Today we write numbers to one hundred from their names.",
            "scaffolding_sequence": [
                "Write two-digit numbers within one decade (e.g., 31-39)",
                "Write two-digit numbers across decades from names",
                "Write numbers to one hundred shown on a chart",
            ],
            "socratic_questions": [
                "Which digit do you write first, the tens or the ones?",
                "How do you write one hundred?",
                "Does your numeral match the number I said?",
            ],
            "practice_activities": [
                "Write numerals dictated by name",
                "Build a number with tens and ones, then write it",
                "Write the numeral for a chart-marked number",
            ],
            "real_world_connections": [
                "Writing a two-digit age",
                "Writing the day's date",
                "Writing a two-digit house or page number",
            ],
            "common_misconceptions": [
                "Reversing digits (writing 64 for forty-six); address by saying 'tens first, then ones' and building with place-value cards",
                "Writing 'fifty' as 500 or 005; address by showing fifty as five tens and zero ones, 50",
                "Writing one hundred as 1000 or 010; address by showing ten tens bundle to one hundred, written 100",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Writes any numeral to 100 legibly",
                "Orders tens and ones correctly",
                "Writes the numeral for a spoken number",
            ],
            "assessment_methods": ["numeral writing", "dictation", "place-value building"],
            "sample_assessment_prompts": [
                "Write fifty-three",
                "Build 72 and write it",
                "Write the number for one hundred",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Write the numeral for 'thirty'.",
                "expected_type": "number",
                "correct_answer": "30",
                "hints": ["Three tens and zero ones"],
                "explanation": "Thirty is written 30.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Write the numeral that comes after 49.",
                "expected_type": "number",
                "correct_answer": "50",
                "hints": ["The next ten"],
                "explanation": "After 49 is 50.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Write the numeral for 'sixty-two'.",
                "expected_type": "number",
                "correct_answer": "62",
                "hints": ["Tens first, then ones"],
                "explanation": "Sixty-two is 62.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Build 47 with tens and ones, then write the numeral.",
                "expected_type": "number",
                "correct_answer": "47",
                "hints": ["Four tens and seven ones"],
                "explanation": "Four tens and seven ones is written 47.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Write the numeral for 'one hundred'.",
                "expected_type": "number",
                "correct_answer": "100",
                "hints": ["A one and two zeros"],
                "explanation": "One hundred is written 100.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "A child wrote 73 for thirty-seven. Tell what went wrong.",
                "expected_type": "text",
                "hints": ["Which digit is the tens?"],
                "explanation": "The digits are reversed; thirty-seven is three tens and seven ones, written 37, with the tens digit first.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Write these in order: forty, forty-five, fifty.",
                "expected_type": "text",
                "hints": ["Tens first for each"],
                "explanation": "40, 45, 50.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Write the numeral for 'eighty' and show it as tens and ones.",
                "expected_type": "text",
                "hints": ["Eight tens and zero ones"],
                "explanation": "Eighty is 80, which is eight tens (80) and zero ones (0).",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Write the numeral for 'fifty-eight'.",
                "type": "number",
                "target_concept": "two_digit_numeral",
                "correct_answer": "58",
            },
            {
                "prompt": "Write the numeral that comes after 89.",
                "type": "number",
                "target_concept": "decade_numeral",
                "correct_answer": "90",
            },
            {
                "prompt": "Build 36 with tens and ones, then write the numeral.",
                "type": "number",
                "target_concept": "place_value_writing",
                "correct_answer": "36",
            },
            {
                "prompt": "Write the numeral for 'one hundred'.",
                "type": "number",
                "target_concept": "hundred_numeral",
                "correct_answer": "100",
            },
            {
                "prompt": "In the numeral 74, which digit shows the tens? Explain.",
                "type": "open_response",
                "target_concept": "place_in_writing_100",
                "rubric": "Mastery: names the 7 as seven tens. Proficient: partial. Developing: cannot explain.",
            },
        ],
        "resource_guidance": {
            "required": ["pencil and paper", "place-value cards (tens and ones)"],
            "recommended": ["base-ten blocks", "hundreds chart"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Use place-value cards and say 'tens first'; allow building before writing; trace if needed.",
            "adhd": "Short dictation bursts; write one two-digit number well with a build beside it.",
            "gifted": "Extend to writing three-digit numbers and writing numbers from base-ten pictures.",
            "visual_learner": "Color the tens and ones digits differently to show their roles.",
            "kinesthetic_learner": "Build the number with blocks, then write large before small.",
            "auditory_learner": "Say the digits in order while writing (five tens, three ones).",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Two-digit numbers are written tens first, then ones; one hundred is 100. Today we write numbers to one hundred from their names.",
                "gradual_release": {
                    "i_do": "Model writing 46 aloud: four tens, then six ones, beside four ten-rods and six ones.",
                    "we_do": "Build and write a few two-digit numbers together, the child placing digits in order, then writing alone.",
                    "you_do": "Child writes dictated numbers to one hundred and writes 100 independently.",
                },
                "guided_practice": [
                    "Write dictated numbers with the teacher confirming digit order",
                    "Build a number and write its numeral",
                ],
                "independent_practice": [
                    "Write ten dictated two-digit numbers",
                    "Write the numbers shown on a hundreds chart",
                ],
                "mastery_check": [
                    "Writes any numeral to 100 legibly",
                    "Orders tens and ones correctly",
                    "Writes the numeral for a spoken number",
                ],
                "spiral_review": [
                    "Re-form the teen numerals 11-20 (mf-40) first, then extend to writing all two-digit numbers to one hundred"
                ],
            },
            "classical": {
                "narrative_introduction": "Every number to one hundred now has its written form; the hand, trained on the teens, writes the tens and ones in their fixed and proper order.",
                "memory_work": {
                    "chants": [
                        "Chant a two-digit number as tens and ones while writing it",
                        "Recite the decade numerals: ten, twenty, thirty, to one hundred",
                    ],
                    "recitations": ["A short saying recited daily: tens first, then ones"],
                },
                "copywork": ["Copy the decade numerals and a few two-digit numbers neatly, tens digit first"],
                "recitation_routine": "Begin by writing yesterday's numbers from memory before adding more, reviewing the forms cumulatively.",
                "history_integration": "Copy two-digit year-numerals on a timeline of a century, joining number-writing to chronology.",
                "read_aloud_suggestions": ["A number book whose two-digit numerals are clearly shown to copy"],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 12,
                "living_book_suggestions": [
                    "A number book showing the numbers to one hundred with clear, lovely numerals"
                ],
                "short_lesson_flow": "Build a two-digit number with rods, name it as tens and ones, and copy its numeral once, neatly; keep it short.",
                "narration_prompt": "Tell me about the number you wrote. Which digit is the tens?",
                "real_world_objects": [
                    "Writing a two-digit count in the nature notebook",
                    "Noticing two-digit house numbers on a walk",
                    "Writing the date",
                ],
                "nature_connection": "Write the two-digit numeral for a count of found objects beside a small drawing in the nature notebook.",
                "habit_focus": "The habit of neatness: place the tens and ones in the right order, each carefully formed.",
            },
            "montessori": {
                "prepared_materials": ["Place-value cards to 100", "Golden bead tens and ones", "Number cards to 100"],
                "presentation": {
                    "three_period_lesson": "Naming: build forty-six, four tens and six ones, write 46. Recognition: write me forty-six. Recall: what number is this?",
                    "steps": [
                        "Build the number with ten-bars and unit beads",
                        "Write the tens digit, then the ones digit",
                        "Lay place-value cards over the numeral to self-check",
                    ],
                },
                "control_of_error": "The place-value cards reveal a reversal: 64 will not match four tens and six ones, so the child sees and fixes it.",
                "abstraction_pathway": "From building with tens and ones, to writing the two digits in order, toward writing numbers to one hundred from the held idea.",
                "extensions": [
                    "Write numbers while building each with golden beads",
                    "Match written numbers to place-value cards",
                ],
                "observation_focus": "Watch for correct digit order, careful formation, and the child matching each numeral to its tens and ones.",
            },
            "unschooling": {
                "invitations": [
                    "Leave place-value cards or magnetic digits within reach",
                    "Put out a whiteboard near two-digit-numbered things in the home",
                ],
                "real_world_contexts": [
                    "Writing a two-digit count on a drawing",
                    "Writing the date on a calendar",
                    "Labeling a collection with its two-digit number",
                ],
                "conversation_starters": ["Want to write how many you counted?", "Which digit comes first, the tens?"],
                "resource_bank": [
                    "Magnetic digits and place-value cards left available",
                    "A whiteboard for free number-writing",
                ],
                "parent_role": "Offer playful materials for making numbers and write real two-digit numbers the child cares about, never as handwriting drill.",
                "observation_documentation": "Notice whether the child writes two-digit numbers with the digits in order when labeling real things; this is the record.",
            },
        },
        "connections": {
            "reading": "Writing two-digit numerals parallels spelling short words letter by letter",
            "science": "Labeling a two-digit count of specimens",
            "history": "Writing two-digit year-numerals on a timeline",
        },
    },
    "mf-44": {
        "enriched": True,
        "learning_objectives": [
            "Begin counting from any number within one hundred instead of from one",
            "Count on by ones across a decade boundary (e.g., 28, 29, 30)",
            "Count on a stated number of steps from a two-digit starting number",
            "Use counting on from a larger number to find a total",
        ],
        "teaching_guidance": {
            "introduction": "Counting on works with bigger numbers too. We start at a number we know, like thirty-eight, and count on, crossing each ten carefully: thirty-nine, forty, forty-one.",
            "scaffolding_sequence": [
                "Say the next number after a two-digit number",
                "Count on across a decade turn from a given start",
                "Count on a few steps from a two-digit number",
            ],
            "socratic_questions": [
                "What number comes right after 49?",
                "Why start at sixty-three instead of one?",
                "Count on five from 28; where do you land?",
            ],
            "practice_activities": [
                "Next-number practice with two-digit starts",
                "Count on across decade turns",
                "Count on from a hidden two-digit set plus visible more",
            ],
            "real_world_connections": [
                "Continuing to count a collection from where you left off",
                "Counting on points from a two-digit score",
                "Counting on more steps from a landing",
            ],
            "common_misconceptions": [
                "Restarting at one for two-digit starts; address by hiding the first part and prompting 'you have thirty-eight, count on'",
                "Stumbling at the decade turn while counting on; address by rehearsing 39-40, 49-50 on a chart",
                "Repeating the start number as the first 'on' step; address by counting on with the next number, not the start",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Starts counting from any number within one hundred",
                "Counts on across decade turns",
                "Counts on a stated number of steps",
            ],
            "assessment_methods": ["oral counting", "next-number tasks", "observation"],
            "sample_assessment_prompts": [
                "What comes after 59?",
                "Start at 38 and count on to 43",
                "Count on 4 from 67",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What number comes right after 47?",
                "expected_type": "number",
                "correct_answer": "48",
                "hints": ["One more"],
                "explanation": "After 47 comes 48.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Start at 62 and say the next number.",
                "expected_type": "number",
                "correct_answer": "63",
                "hints": ["Just one more"],
                "explanation": "After 62 comes 63.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What comes after 79?",
                "expected_type": "number",
                "correct_answer": "80",
                "hints": ["The next ten"],
                "explanation": "After 79 comes 80.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Start at 38 and count on to 42. What numbers do you say?",
                "expected_type": "text",
                "hints": ["Cross forty carefully; begin with 39"],
                "explanation": "39, 40, 41, 42, counting on from thirty-eight.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You have 45 stickers and count on 3 more. Where do you land?",
                "expected_type": "number",
                "correct_answer": "48",
                "hints": ["46, 47, 48"],
                "explanation": "Counting on 3 from 45 gives 46, 47, 48.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Why is it faster to count on from 70 than to start at 1?",
                "expected_type": "text",
                "hints": ["What do you already know?"],
                "explanation": "You already know there are seventy, so you start at seventy and count only the new ones instead of recounting from one.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "There are 29 marbles in a bag (you cannot see them) and 4 more on the table. Count on to find the total.",
                "expected_type": "number",
                "correct_answer": "33",
                "hints": ["Start at 29: 30, 31, 32, 33"],
                "explanation": "Counting on from 29: 30, 31, 32, 33, so 33 in all.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Count on from 58 to 63. How many numbers did you say after 58?",
                "expected_type": "number",
                "correct_answer": "5",
                "hints": ["59, 60, 61, 62, 63"],
                "explanation": "From 59 to 63 is 5 numbers, so you said 5 numbers after 58.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "What number comes right after 69?",
                "type": "number",
                "target_concept": "next_two_digit",
                "correct_answer": "70",
            },
            {
                "prompt": "Start at 47 and count on to 51.",
                "type": "open_response",
                "target_concept": "count_on_100",
                "rubric": "Mastery: 48,49,50,51 starting after 47, crosses 50. Proficient: one slip. Developing: restarts at 1.",
            },
            {
                "prompt": "You have 56 and count on 4 more. Where do you land?",
                "type": "number",
                "target_concept": "count_on_total_100",
                "correct_answer": "60",
            },
            {
                "prompt": "Start at 88 and count on 3. Where do you land?",
                "type": "number",
                "target_concept": "decade_count_on",
                "correct_answer": "91",
            },
            {
                "prompt": "Why is counting on from a big number faster than starting at one?",
                "type": "open_response",
                "target_concept": "count_on_reasoning_100",
                "rubric": "Mastery: explains starting from the known amount. Proficient: says it is quicker. Developing: cannot explain.",
            },
        ],
        "resource_guidance": {
            "required": ["counting objects", "a hundreds chart"],
            "recommended": ["number line to 100", "two-digit start cards"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Hide the start set so the child counts on; rehearse decade turns; keep oral.",
            "adhd": "Short turns; tap forward on a chart for each 'on' step, one decade turn at a time.",
            "gifted": "Extend to counting on by tens and counting on across the hundred.",
            "visual_learner": "Use a number line or chart and slide a marker forward for each step.",
            "kinesthetic_learner": "Step forward on a floor chart, counting on from a two-digit landing.",
            "auditory_learner": "Say only the new numbers aloud, crossing each ten clearly.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "We start counting from a two-digit number and count on, crossing each ten with care. Today we count on within one hundred.",
                "gradual_release": {
                    "i_do": "Model holding thirty-eight in mind and counting on, thirty-nine, forty, forty-one, across the ten.",
                    "we_do": "Count on across a decade turn together, the child adding objects as you say each next number, then swap.",
                    "you_do": "Child starts from two-digit numbers and counts on a stated number of steps independently.",
                },
                "guided_practice": [
                    "Next-number practice with two-digit starts, teacher confirming",
                    "Count on across a decade turn from a called start",
                ],
                "independent_practice": [
                    "Count on to a target from five two-digit starts",
                    "Count on a stated number of steps and say the total",
                ],
                "mastery_check": [
                    "Starts counting from any number within one hundred",
                    "Counts on across decade turns",
                    "Counts on a stated number of steps",
                ],
                "spiral_review": [
                    "Re-count to one hundred from one (mf-04) first, then practice starting partway and counting on across the tens"
                ],
            },
            "classical": {
                "narrative_introduction": "Counting on from a larger number is addition in seed: the child holds a two-digit number and adds to it, crossing each ten in its turn.",
                "memory_work": {
                    "chants": [
                        "Chant the next number after each two-digit number across a decade",
                        "Echo: the teacher says a two-digit number, the child says the next",
                    ],
                    "recitations": ["A short rhyme about counting on from where you are, recited daily"],
                },
                "recitation_routine": "Begin by reciting the full count past a decade, then practice starting partway and counting on, reviewing the sequence cumulatively.",
                "history_integration": "Count on years from a two-digit point on a timeline, adding one for each year since.",
                "read_aloud_suggestions": [
                    "A story where a count grows from a larger number as more arrive, read aloud"
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 12,
                "living_book_suggestions": [
                    "A picture book where a larger group is counted on as more join, with calm pictures"
                ],
                "short_lesson_flow": "Hold a known two-digit set, then add real objects one at a time, counting on calmly across a ten to the new total.",
                "narration_prompt": "Tell me how you found the total by counting on. Where did you start?",
                "real_world_objects": [
                    "Counting on items added to a larger collection",
                    "Counting on points from a two-digit score",
                    "Counting on steps from a landing partway up",
                ],
                "nature_connection": "On a long walk, count on found objects added to a basket that already holds many.",
                "habit_focus": "The habit of attention: hold the larger number in mind and count only the new ones, carefully across each ten.",
            },
            "montessori": {
                "prepared_materials": [
                    "Counters with a known two-digit set hidden",
                    "Golden beads",
                    "A hundreds chart",
                ],
                "presentation": {
                    "three_period_lesson": "Naming: here are thirty-eight, count on, thirty-nine, forty. Recognition: start at forty and count on. Recall: what is the next number?",
                    "steps": [
                        "Set a known two-digit quantity aside",
                        "Count on as objects are added, crossing the ten",
                        "Self-check by counting the whole set",
                    ],
                },
                "control_of_error": "Counting the whole set checks the count-on total; a mismatch at a decade turn shows the count to redo.",
                "abstraction_pathway": "From counting on with hidden two-digit sets, to counting on aloud across the tens, toward adding by counting on in the mind.",
                "extensions": [
                    "Count on by tens from a two-digit start",
                    "Count on from several hidden two-digit quantities",
                ],
                "observation_focus": "Watch whether the child starts from the known two-digit number and counts on smoothly across decade turns.",
            },
            "unschooling": {
                "invitations": [
                    "Leave a growing collection the child adds to over days",
                    "Set out a larger pile and more objects nearby, say nothing",
                ],
                "real_world_contexts": [
                    "Counting on points from a two-digit game score",
                    "Counting on items as more are added to a big collection",
                    "Counting on stairs from a landing",
                ],
                "conversation_starters": [
                    "You already have a bunch, how many now?",
                    "Want to count on instead of starting over?",
                ],
                "resource_bank": [
                    "Larger collections the child adds to over time",
                    "Board games where you count on spaces from a two-digit position",
                ],
                "parent_role": "In real moments with bigger numbers, model counting on from what is already there rather than recounting, and let the child join.",
                "observation_documentation": "Notice whether the child counts on from a two-digit amount across the tens in real play; this is the record.",
            },
        },
        "connections": {
            "reading": "Counting on within one hundred parallels reading on through a longer passage",
            "science": "Counting on new observations added to a larger set",
            "history": "Counting on years from a two-digit point on a timeline",
        },
    },
    "mf-45": {
        "enriched": True,
        "learning_objectives": [
            "Match two groups one to one to compare them",
            "Decide which group has more and which has fewer",
            "Recognize when two groups are the same (equal)",
            "Explain that a group with leftovers after matching has more",
        ],
        "teaching_guidance": {
            "introduction": "To compare two groups, we match them one to one, pairing each object in one group with one in the other. If one group has leftovers, it has more. If they pair up evenly, they are the same.",
            "scaffolding_sequence": [
                "Match two small groups and name more or fewer",
                "Match equal groups and name them the same",
                "Match groups with one leftover and explain which has more",
            ],
            "socratic_questions": [
                "When we matched them, which group had some left over?",
                "Did every object find a partner? Then what do we know?",
                "Which has more? How can you be sure without counting?",
            ],
            "practice_activities": [
                "One-to-one matching of two object rows",
                "Pair-and-decide more/fewer/same games",
                "Draw lines to match two groups in a picture",
            ],
            "real_world_connections": [
                "Deciding who has more crackers",
                "Matching cups to saucers to see if there are enough",
                "Pairing socks to find an extra",
            ],
            "common_misconceptions": [
                "Judging 'more' by how spread out a group looks; address by matching one to one so length does not fool the eye",
                "Saying 'same' when one group has a leftover; address by pointing to the unmatched object that makes it more",
                "Not matching carefully and double-pairing; address by drawing one connecting line per object",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Matches two groups one to one",
                "Decides more, fewer, or same correctly",
                "Explains that a leftover means more",
            ],
            "assessment_methods": ["one-to-one matching", "oral response", "demonstration"],
            "sample_assessment_prompts": [
                "Match these two rows; which has more?",
                "Are these groups the same? Show me",
                "Which group has fewer?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Row A has 4 dots, Row B has 2 dots. Which row has more?",
                "expected_type": "text",
                "hints": ["Match them one to one"],
                "explanation": "Row A has more, because after matching two pairs, Row A still has objects left over.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Group A: 3 stars. Group B: 3 stars. Are they the same?",
                "expected_type": "text",
                "hints": ["Do they pair up evenly?"],
                "explanation": "Yes, the same; every star in A pairs with one in B, with none left over.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Row A has 5, Row B has 1. Which has fewer?",
                "expected_type": "text",
                "hints": ["Which runs out first when matching?"],
                "explanation": "Row B has fewer; it runs out of objects to match after one pair.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You have 6 cups and 6 saucers. Are there the same number? How do you know?",
                "expected_type": "text",
                "hints": ["Pair each cup with a saucer"],
                "explanation": "The same; each cup matches one saucer with none left over, so the groups are equal.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Two rows look different lengths but each has 4 objects. Which has more?",
                "expected_type": "text",
                "hints": ["Match them, do not trust the length"],
                "explanation": "Neither; matching one to one shows they are the same, even though one row looks longer when spread out.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Group A has 7, Group B has 5. After matching, how many are left over in A, and what does that tell you?",
                "expected_type": "number",
                "correct_answer": "2",
                "hints": ["Match five pairs, then count A's leftovers"],
                "explanation": "Two are left over in A, which tells us A has more, by two.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Explain how to compare two groups without counting them.",
                "expected_type": "text",
                "hints": ["Think about pairing each object"],
                "explanation": "Match each object in one group with one in the other; if a group has leftovers it has more, if they pair evenly they are the same.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Row A: 2 apples. Row B: 5 apples. Which has more, and how do you know by matching?",
                "expected_type": "text",
                "hints": ["Pair the two apples first"],
                "explanation": "Row B has more; after pairing the two apples, Row B still has three apples with no partners.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Row A has 5 dots, Row B has 3 dots. Which has more?",
                "type": "open_response",
                "target_concept": "compare_more",
                "rubric": "Mastery: A, explains leftover after matching. Proficient: A by counting. Developing: judges by look.",
            },
            {
                "prompt": "Group A has 4, Group B has 4. Are they the same? How do you know?",
                "type": "open_response",
                "target_concept": "compare_same",
                "rubric": "Mastery: same, explains even pairing. Proficient: same by counting. Developing: unsure.",
            },
            {
                "prompt": "Two rows: 6 and 2. Which has fewer?",
                "type": "open_response",
                "target_concept": "compare_fewer",
                "rubric": "Mastery: the 2-row, explains it runs out. Proficient: correct by counting. Developing: judges by spread.",
            },
            {
                "prompt": "Match a row of 4 cups to a row of 4 saucers. Are there enough saucers?",
                "type": "open_response",
                "target_concept": "matching_enough",
                "rubric": "Mastery: yes, each cup has a saucer. Proficient: yes by counting. Developing: cannot match.",
            },
            {
                "prompt": "How can you tell which group has more without counting?",
                "type": "open_response",
                "target_concept": "comparison_reasoning",
                "rubric": "Mastery: names one-to-one matching and leftovers. Proficient: says 'match them.' Developing: cannot explain.",
            },
            {
                "prompt": "Group A has 7, Group B has 5. After matching, how many more are in Group A?",
                "type": "number",
                "target_concept": "how_many_more",
                "correct_answer": "2",
            },
        ],
        "resource_guidance": {
            "required": ["two sets of matchable objects", "a mat with two rows"],
            "recommended": ["cups and saucers or pegs and holes", "connecting cubes"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 8},
        "accommodations": {
            "dyslexia": "Use distinct, matchable objects and draw connecting lines; keep oral, no numerals.",
            "adhd": "Short pair-and-decide games; one comparison at a time with hands-on matching.",
            "gifted": "Extend to comparing three groups and to telling how many more or fewer.",
            "visual_learner": "Line the two groups in neat rows and draw lines between matched pairs.",
            "kinesthetic_learner": "Physically pair objects (cup on saucer) to feel which has a leftover.",
            "auditory_learner": "Say the result aloud: this group has more because one is left over.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "To compare groups, we match them one to one; leftovers mean more, even pairs mean the same. Today we compare by matching.",
                "gradual_release": {
                    "i_do": "Model matching a row of five to a row of three, pairing each, then pointing to the two left over in the larger group.",
                    "we_do": "Match two groups together, the child pairing objects, then naming more, fewer, or same; then swap.",
                    "you_do": "Child matches pairs of groups and names more, fewer, or same independently, explaining the leftover.",
                },
                "guided_practice": [
                    "Match-and-name with the teacher confirming the pairing",
                    "Decide more, fewer, or same for matched groups",
                ],
                "independent_practice": [
                    "Compare five pairs of groups by matching",
                    "Match cups to saucers and tell if there are enough",
                ],
                "mastery_check": [
                    "Matches two groups one to one",
                    "Decides more, fewer, or same correctly",
                    "Explains that a leftover means more",
                ],
                "spiral_review": [
                    "State the total of each group as the last count (mf-35), then match the groups one to one to compare"
                ],
            },
            "classical": {
                "narrative_introduction": "To compare is to set two quantities side by side and pair them; the truth of more or fewer is shown by the leftover, not by how the groups happen to look.",
                "memory_work": {
                    "chants": [
                        "Chant the comparison words: more, fewer, same",
                        "Recite the rule: match them, leftovers mean more",
                    ],
                    "recitations": ["A short saying recited daily: match to compare"],
                },
                "recitation_routine": "Begin by recalling yesterday's rule, match one to one, before comparing today's groups, reviewing the idea cumulatively.",
                "history_integration": "Compare two groups on a timeline (e.g., kings of two short lines) by matching them one to one.",
                "read_aloud_suggestions": ["A story where two groups are compared fairly, read aloud"],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 8,
                "living_book_suggestions": ["A picture book where characters share and compare groups fairly"],
                "short_lesson_flow": "Lay two small groups of real objects in rows, match them one to one together, and name more, fewer, or same, calmly.",
                "narration_prompt": "Tell me which group had more. How did you know?",
                "real_world_objects": [
                    "Cups and saucers matched at tea",
                    "Matching mittens to find an extra",
                    "Pairing shoes to see if any is missing",
                ],
                "nature_connection": "On a walk, compare two small collections of found things by matching them one to one.",
                "habit_focus": "The habit of fairness: match carefully and judge by the truth of the pairing, not by appearances.",
            },
            "montessori": {
                "prepared_materials": [
                    "Pairs of matchable objects (cups and saucers, pegs and holes)",
                    "A two-row comparison mat",
                    "Number cards for later linking",
                ],
                "presentation": {
                    "three_period_lesson": "Naming: this group has more. Recognition: show me the group with fewer. Recall: are these the same?",
                    "steps": [
                        "Lay two groups in matching rows",
                        "Pair each object across the rows",
                        "The leftover, or even pairing, reveals more, fewer, or same",
                    ],
                },
                "control_of_error": "The one-to-one matching is self-correcting: an unmatched object plainly shows the group with more.",
                "abstraction_pathway": "From matching real objects, to naming more/fewer/same, toward comparing quantities by number later.",
                "extensions": ["Compare three groups by matching", "Find how many more by counting the leftovers"],
                "observation_focus": "Watch whether the child matches one to one and judges by the leftover rather than by how spread out a group looks.",
            },
            "unschooling": {
                "invitations": [
                    "Leave pairs of things that invite matching (cups and saucers, nuts and bolts)",
                    "Set out two bowls of objects to compare freely",
                ],
                "real_world_contexts": [
                    "Deciding who has more snacks by lining them up",
                    "Matching cups to people to see if there are enough",
                    "Pairing socks and finding an odd one",
                ],
                "conversation_starters": ["Who has more? How could we be sure?", "Are there enough for everyone?"],
                "resource_bank": [
                    "Pairs of matchable objects left available",
                    "Picture books about sharing and fairness",
                ],
                "parent_role": "In real sharing moments, match groups one to one together to decide fairly who has more, letting the question arise naturally rather than as a lesson.",
                "observation_documentation": "Notice whether the child compares groups by matching and judges fairly in real life; this is the record, not a test.",
            },
        },
        "connections": {
            "reading": "Matching words to pictures parallels matching two groups one to one",
            "science": "Comparing the sizes of two sets of specimens",
            "history": "Comparing the lengths of two short timelines by matching",
        },
    },
}
