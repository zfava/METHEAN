"""Pre-enriched content for phonics_reading/developing template nodes.

Mirrors the shape and depth of math_developing_content (the proven
developing-level bar) and reading_foundational_content (the proven
reading shape). Every node carries the full apparatus: enriched flag,
learning_objectives, teaching_guidance (introduction, scaffolding,
socratic questions, practice activities, real-world connections,
common misconceptions), assessment_criteria with tiered indicators
where the topic invites them, practice_items, assessment_items,
resource_guidance, time_estimates, accommodations across six learner
profiles, philosophy_specific with all five native variants at Option
B fidelity, and connections.

The developing level is a genuine step up from foundational: fluency
moves from decodable to grade-level texts; comprehension extends from
sentence and paragraph to chapter and cross-chapter; oral narration
extends to multi-paragraph passages and a new written-narration act
is introduced; genre awareness becomes explicit and metalinguistic;
character, setting, plot, cause and effect, summarizing, inference,
poetry, literary elements, figurative language, and research enter as
named skills. The capstone rd-25 is a cumulative readiness check
modeled on the foundational and math-developing capstones.

Mythology (rd-11) and fables / fairy tales (rd-16) are presented as
the traditions present themselves, with conventional content notes
where appropriate; the child reads ancient myth as historical
literature, not as belief instruction.
"""

READING_DEVELOPING_CONTENT = {
    "rd-01": {
        "enriched": True,
        "learning_objectives": [
            "Read grade-level texts (not decodable readers) at 90 or more words per minute with 95% or higher accuracy",
            "Read with prosody: natural phrasing, expressive intonation, pause at punctuation, stress on important words",
            "Self-correct meaning-changing errors without prompting, and self-monitor comprehension while reading",
            "Sustain independent silent reading for 20 to 30 minutes across one sitting and resume the next day",
            "Perform a short rehearsed passage (reader's theater or poetry) for a real audience with confident phrasing and character voice",
        ],
        "teaching_guidance": {
            "introduction": (
                "Foundational fluency was built on decodable texts so the child could meet only the phonics patterns they "
                "already knew. Developing fluency steps off the decodable rails and onto real grade-level texts, where the "
                "child meets ordinary English at the rate ordinary English moves. The target is not speed for its own sake "
                "but reading that sounds like talking, with the meaning carried by phrasing and stress so the listener "
                "follows the sense, not just the words. Repeated reading, phrase-cued reading, and reader's theater are "
                "the three workhorse practices; the books are real books at the child's instructional level."
            ),
            "scaffolding_sequence": [
                "Choose grade-level texts at the child's instructional level (95% or higher accuracy at a cold read); parent confirms by sampling a page",
                "Model fluent reading aloud: parent reads a passage, then the child echoes it back trying to match the phrasing",
                "Choral reading: parent and child read aloud together at one pace, with the parent leading slightly so the child rides the fluent rhythm",
                "Phrase-cued reading: take a paragraph, mark natural phrase breaks with light pencil slashes, read phrase by phrase, then read it again with the slashes erased",
                "Repeated reading: child reads the same 100 to 150 word passage three times across three days; track WPM each time and celebrate personal best",
                "Reader's theater: prepare a short scene with assigned character parts, rehearse two or three times, perform for a real audience (sibling, grandparent, video)",
                "Poetry performance: memorize a short poem with attention to where the voice rises and where it pauses; recite it confidently",
                "Build stamina: gradually extend silent independent reading from 10 minutes toward 20 and then 30, with a chapter book the child has chosen",
            ],
            "socratic_questions": [
                "When you finished that paragraph, did it sound like talking or like reading? Read it again and try to make it sound more like talking.",
                "You read 'I can't believe it' in a flat voice. How would you really say that if you couldn't believe something? Show me with your voice.",
                "When you got to that long word and stumbled, what did you do next? Did the sentence make sense to you?",
                "Look at the punctuation in this sentence. Where does your voice slow down? Where does it stop? Where does it rise?",
                "You read this passage three times now. Which time felt the smoothest, and why do you think so?",
            ],
            "practice_activities": [
                "Repeated reading across three days: pick a 100 to 150 word passage from a favorite book, read it once each day, track WPM and self-rated smoothness",
                "Reader's theater with the family: choose a chapter with two or three speaking characters, assign parts, rehearse, perform",
                "Record-and-listen: child records themselves reading a paragraph, listens back, notes one place to improve, reads it again",
                "Poetry recital: child picks a short poem they love, memorizes it across a week, recites for the household at dinner",
                "Audiobook follow-along: child reads along in the physical book while listening to a skilled narrator, then reads the same passage aloud trying to match the narrator's phrasing",
            ],
            "real_world_connections": [
                "Reading a recipe aloud to the cook in the kitchen so the cook can keep their hands in the work",
                "Reading a picture book aloud to a younger sibling at bedtime with character voices",
                "Reading a chosen passage aloud to a grandparent over the phone or video call",
                "Reading the lines of a play or a game's instructions aloud at the table",
                "Reading aloud the words of a song the family is learning together",
            ],
            "common_misconceptions": [
                "Thinking fluency means reading fast. Speed without accuracy and meaning is not fluency; a fluent reader sounds like a person talking, not a person racing.",
                "Reading in a flat or robot voice because every word is now decodable. Expression is part of fluency; punctuation and meaning shape the voice.",
                "Skipping unknown words to keep the pace up. Fluency includes self-correction; meaning-breaking errors are repaired, not ignored.",
                "Believing the timed one-minute read is the only measure. Timed reads are one diagnostic among several; reader's theater, repeated reading, and sustained silent reading build fluency more than timing does.",
                "Treating reader's theater as performance for grades. The point is rehearsed expressive reading; the audience is whoever will listen, and the success is heard, not scored.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Reads grade-level prose at 90 or more WPM with 95% or higher accuracy on a cold read",
                "Reads with natural phrasing, appropriate pauses, and expression matching the punctuation and meaning",
                "Self-corrects meaning-changing errors without prompting; self-monitors comprehension and stops to repair confusion",
                "Sustains independent silent reading for 20 minutes or more across one sitting and resumes the same chapter the next day",
                "Performs a short rehearsed passage with confident phrasing and recognizable character voice or appropriate poetic delivery",
            ],
            "proficiency_indicators": [
                "Reads grade-level prose at 70 to 89 WPM with 90 to 94% accuracy",
                "Emerging prosody: most punctuation observed, expression beginning to match meaning",
                "Self-corrects some errors with brief prompting",
                "Sustains independent reading for 10 to 15 minutes",
            ],
            "developing_indicators": [
                "Reads grade-level prose under 70 WPM with under 90% accuracy and frequent word-by-word reading",
                "Flat or monotone delivery; punctuation observed inconsistently",
                "Rarely self-corrects; skips unknown words or guesses without checking meaning",
                "Sustains independent reading under 10 minutes",
            ],
            "assessment_methods": [
                "timed one-minute oral reading on grade-level cold text",
                "running record for accuracy and self-correction across a 100 to 200 word passage",
                "prosody rubric (Multidimensional Fluency Scale or equivalent) on a rehearsed passage",
                "reader's theater or recital performance observed by the parent",
                "independent reading stamina log kept across a week",
            ],
            "sample_assessment_prompts": [
                "Read this grade-level passage aloud for one minute while I count the words. (Use a cold passage of 200 or more words at grade level.)",
                "Read this sentence with expression: 'I can't believe it!' she whispered. 'The egg is hatching!'",
                "Read this paragraph and then tell me what happened in your own words.",
                "Perform your rehearsed passage for me now. (Reader's theater piece or memorized poem prepared across the week.)",
                "How long can you read your chapter book today without stopping? Set a timer and read until you naturally want to pause.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": (
                    "Read this sentence smoothly, as if telling someone the story: "
                    "'The old dog walked slowly down the path, sniffing at every leaf.'"
                ),
                "expected_type": "text",
                "correct_answer": "The old dog walked slowly down the path, sniffing at every leaf.",
                "hints": [
                    "Group the words into natural phrases: 'The old dog / walked slowly / down the path, / sniffing at every leaf.'",
                    "Read the whole sentence without stopping between words.",
                ],
                "explanation": (
                    "A fluent reader groups words into phrases rather than reading word by word. Try the slashes on paper "
                    "first if needed, then read it without them."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "Read this with expression: 'Wait!' shouted Mara. 'Don't open that door!'"
                ),
                "expected_type": "text",
                "correct_answer": "'Wait!' shouted Mara. 'Don't open that door!'",
                "hints": [
                    "The exclamation marks tell you the voice is urgent.",
                    "The dialogue tag 'shouted' tells you how Mara is speaking.",
                ],
                "explanation": (
                    "Exclamation marks mean strong feeling; the dialogue tag tells you Mara is shouting. Make the voice loud "
                    "and urgent. The narrator's part stays in your reading voice."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "You are reading a chapter book and you come to the word 'although'. You can read it, but the sentence "
                    "doesn't quite make sense. What should you do?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "Keep reading and hope it makes sense later.",
                    "Stop, re-read the sentence from the beginning, and think about what 'although' might mean.",
                    "Skip the rest of the page.",
                    "Ask someone immediately, even before trying.",
                ],
                "correct_answer": "Stop, re-read the sentence from the beginning, and think about what 'although' might mean.",
                "hints": [
                    "Fluent readers self-monitor comprehension and stop when meaning breaks down.",
                    "Re-reading from the start of the sentence often clarifies the meaning.",
                ],
                "explanation": (
                    "The first thing a fluent reader does when meaning breaks down is stop and re-read the sentence. If that "
                    "still doesn't clarify it, use context from the surrounding sentences, then ask if needed."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "Read this passage three times across three days. Each day, record how many words you read in one minute. "
                    "What should you expect to happen across the three days? "
                    "'The barn cat watched the field mouse from the rafter. Her eyes never left the small grey shape. When "
                    "the mouse moved at last, the cat dropped silently to the hay below.'"
                ),
                "expected_type": "text",
                "hints": [
                    "Each repeat reading builds automaticity. The brain recognizes the words faster.",
                    "Expression and phrasing should improve along with rate.",
                ],
                "explanation": (
                    "Across three days you should see the rate climb (more words in the same minute) AND the smoothness "
                    "improve. By the third reading the passage should sound like talking. This is the point of repeated "
                    "reading."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "You are rehearsing a reader's theater scene with two characters: a brave knight and a tired old wizard. "
                    "How should the knight's voice differ from the wizard's voice?"
                ),
                "expected_type": "text",
                "hints": [
                    "Think about pitch, pace, and energy for each character.",
                    "There is no one right answer; reader's theater rewards a clear choice.",
                ],
                "explanation": (
                    "The knight's voice is probably firmer, faster, more energetic. The wizard's voice is probably slower, "
                    "lower, with more pauses. The point is to make a clear choice and hold it across the scene; that is "
                    "what reader's theater builds."
                ),
            },
        ],
        "assessment_items": [
            {
                "prompt": (
                    "Read this grade-level cold passage aloud for one minute. (Use any unfamiliar grade-level passage of 200+ "
                    "words.)"
                ),
                "type": "open_response",
                "target_concept": "reading_rate_grade_level",
                "rubric": (
                    "Mastery: 90+ WPM at 95%+ accuracy with prosody. Proficient: 70 to 89 WPM at 90 to 94% accuracy, "
                    "emerging prosody. Developing: under 70 WPM at under 90% accuracy, word-by-word."
                ),
            },
            {
                "prompt": (
                    "Read this dialogue with expression: '\"Hurry up!\" Tom whispered. \"They'll hear us!\" Lily froze. "
                    "\"Maybe they already have,\" she said.'"
                ),
                "type": "open_response",
                "target_concept": "prosody_and_dialogue",
                "rubric": (
                    "Mastery: clearly distinct voices for Tom and Lily, urgency on the exclamations, the narrator's words "
                    "in the reader's own voice. Proficient: some character distinction, most punctuation observed. "
                    "Developing: flat or undifferentiated."
                ),
            },
            {
                "prompt": (
                    "Tell me about how long you can read your current chapter book without stopping. What helps you read "
                    "longer? What makes you want to stop?"
                ),
                "type": "open_response",
                "target_concept": "reading_stamina_and_self_monitoring",
                "rubric": (
                    "Mastery: names a stamina of 20+ minutes and articulates supportive conditions and break triggers. "
                    "Proficient: names 10 to 15 minutes and one or two conditions. Developing: names under 10 minutes or "
                    "cannot articulate."
                ),
            },
            {
                "prompt": "Perform the reader's theater piece (or recite the poem) you rehearsed across the week.",
                "type": "open_response",
                "target_concept": "rehearsed_performance",
                "rubric": (
                    "Mastery: confident phrasing, clear character or poetic voice, audience-aware delivery. Proficient: "
                    "rehearsed and mostly fluent, some expression. Developing: hesitant, words read but not performed."
                ),
            },
        ],
        "resource_guidance": {
            "required": [
                "real grade-level chapter books or trade books at the child's instructional level (95%+ accuracy on cold read)",
                "a timer or clock for one-minute reads",
                "a reader's theater script (a chapter with two or three speaking characters, or a published reader's theater piece)",
            ],
            "recommended": [
                "poetry collections (Robert Frost, Christina Rossetti, A. A. Milne, Karla Kuskin, Naomi Shihab Nye, Langston Hughes for the age)",
                "audiobooks of grade-level books paired with the printed text",
                "a personal reading log to track titles, pages, and stamina across the week",
            ],
        },
        "time_estimates": {"first_exposure": 30, "practice_session": 20, "assessment": 15},
        "accommodations": {
            "dyslexia": (
                "Stay at the child's instructional level (95%+ accuracy at cold read); frustration-level texts kill fluency. "
                "Allow finger or bookmark tracking. Repeated reading on the same passage across days builds automaticity "
                "more than fresh harder text. Audiobook-plus-print pairing is especially valuable here."
            ),
            "adhd": (
                "Short passages (50 to 100 words) for repeated reading. Reader's theater adds engagement. Allow standing or "
                "walking while reading aloud. A 5-minute timer for sustained reading with a clear stop point is easier than "
                "open-ended stamina building."
            ),
            "gifted": (
                "Move to more complex texts with varied sentence structures and richer vocabulary. Introduce multi-character "
                "reader's theater. Begin reading chapter books with chapters of 10+ pages and longer narrative arcs."
            ),
            "visual_learner": (
                "Use a reading window or finger tracker to focus on one line at a time. Larger fonts and generous line "
                "spacing if available. Strong task lighting on the page."
            ),
            "kinesthetic_learner": (
                "Track with a finger or bookmark. Stand while reading aloud. Use hand gestures during reader's theater to "
                "embody character voices."
            ),
            "auditory_learner": (
                "Record-and-listen is especially effective. Audiobooks at natural speed model fluent pacing. Echo reading "
                "with the parent before independent reading."
            ),
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": (
                    "Fluency at the developing level is read with natural phrasing, expressive voice, and self-correction "
                    "on grade-level texts the child can read with 95% or better accuracy. Today we build rate, accuracy, "
                    "and prosody on real books, not decodable readers."
                ),
                "gradual_release": {
                    "i_do": (
                        "Read a paragraph aloud as a model, grouping words into phrases, letting the voice rise on a "
                        "question and lift on an exclamation, slowing where the meaning is dense. Mark a sentence into "
                        "phrases with light pencil slashes."
                    ),
                    "we_do": (
                        "Read a paragraph together at one pace, then echo one sentence the child reads back. Read a marked "
                        "sentence phrase by phrase together, then with the marks erased."
                    ),
                    "you_do": (
                        "Child reads the same 100 to 150 word passage three times across three days, growing smoother each "
                        "time, with expression that matches the text. Child also reads independently from their chapter "
                        "book for the daily stamina target."
                    ),
                },
                "guided_practice": [
                    "Echo and choral reading of a short grade-level passage with the parent",
                    "Phrase-cued reading: read a marked passage phrase by phrase, then again unmarked",
                    "Repeated reading of a 100 to 150 word passage across three days with WPM tracked",
                ],
                "independent_practice": [
                    "Daily independent silent reading from a chosen chapter book, building stamina toward 20+ minutes",
                    "Weekly reader's theater rehearsal and Friday performance for a household audience",
                ],
                "mastery_check": [
                    "Read a grade-level cold passage at 90+ WPM with 95%+ accuracy and natural prosody",
                    "Self-correct meaning-changing errors without prompting",
                    "Sustain 20+ minutes of independent reading",
                ],
                "spiral_review": [
                    "Return to familiar passages for warm-up before harder text",
                    "Daily one-minute read on a known passage to keep rate and confidence sharp",
                ],
            },
            "classical": {
                "narrative_introduction": (
                    "To read aloud well is among the oldest of the grammar-stage arts. The reader is the voice of the text: "
                    "every phrase grouped, every mark of punctuation honored, every line spoken so that a listener follows "
                    "the sense as it unfolds. Practiced daily on worthy texts, the voice grows confident and the ear sharp."
                ),
                "memory_work": {
                    "chants": [
                        "Chant the marks of expression: a question lifts at its end, an exclamation carries energy, a period comes to rest, a comma pauses briefly",
                        "Chant a marked sentence in its natural phrases, so the ear learns to group words into meaning rather than read them one at a time",
                    ],
                    "recitations": [
                        "Memorize and recite a worthy short poem each week, performing it with full phrasing and expression so fluency is built by heart on language worth keeping",
                    ],
                },
                "copywork": [
                    "Copy the passage being practiced for fluency, attending especially to its punctuation, so the marks that guide the voice are also known by the hand",
                ],
                "recitation_routine": (
                    "Each lesson begins with the recitation of a poem from earlier weeks, then adds the new fluency passage; "
                    "the reader's repertoire grows cumulatively across the term."
                ),
                "history_integration": (
                    "Choose fluency texts from history and from the great stories along the chronological spine, so that the "
                    "rate and expression are built on texts worth the time."
                ),
                "read_aloud_suggestions": [
                    "Well-written prose and poetry just above the child's own reading level, read aloud daily by the parent for the music and rhythm of the language",
                    "Classical and traditional poetry for memorization: Christina Rossetti, Robert Louis Stevenson, A. A. Milne, Robert Frost",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "Early chapter books with beautiful language and real story interest: Frog and Toad, Mercy Watson, Magic Tree House at this band, then The Boxcar Children, Charlotte's Web, Mr. Popper's Penguins",
                    "Poetry collections with real literary quality: Robert Frost, A. A. Milne, Robert Louis Stevenson, A Child's Garden of Verses, the Oxford Book of Children's Verse",
                ],
                "short_lesson_flow": (
                    "Read aloud a passage from a living book together, unhurried, caring for the sound of the language. "
                    "Let the child read a single page or paragraph attentively and well, and tell it back. Stop while the "
                    "reading is still a pleasure; the next day continues."
                ),
                "narration_prompt": (
                    "Tell me back the passage you just read. Which part did you most enjoy reading aloud, and why?"
                ),
                "real_world_objects": [
                    "A favorite chapter book the child returns to daily, kept in the reading nook",
                    "A poetry collection the child keeps as their own",
                    "A reading journal where favorite lines and titles are copied across the term",
                ],
                "nature_connection": (
                    "Read aloud a short nature passage or poem outdoors during a walk, then copy a favorite line into the "
                    "nature notebook with a small drawing."
                ),
                "habit_focus": (
                    "The habit of attention and of reading well: one careful, expressive reading rather than many hurried "
                    "or careless ones. The voice carries the meaning; the listener trusts the reader."
                ),
            },
            "montessori": {
                "prepared_materials": [
                    "A reading corner stocked with chapter books at and just above the child's independent level, freely chosen",
                    "Phrase-marked passages prepared for the child's repeated-reading work, kept in a folder the child manages",
                    "Reader's theater scripts and short poetry pieces for expressive reading practice",
                    "A small recorder so the child can hear their own reading and reread to mend it",
                ],
                "presentation": {
                    "three_period_lesson": (
                        "With a marked passage: this is a phrase, read as one group; show me where this phrase ends; how "
                        "should this phrase sound? Modeled, then handed to the child for free practice."
                    ),
                    "steps": [
                        "The guide reads a passage aloud as a model of phrasing and expression",
                        "The child chooses a text at their independent level and reads it freely, returning to reread as they wish",
                        "The child reads aloud to a small listener (a sibling, a stuffed audience, a recorder) and listens back to their own reading",
                        "The child prepares a reader's theater piece or poem across several days and performs it for a real audience",
                    ],
                },
                "control_of_error": (
                    "The child reading aloud and listening, whether to a real listener or to a recording, hears for themselves "
                    "where the reading stumbled or fell flat, and rereads to mend it without adult correction."
                ),
                "abstraction_pathway": (
                    "From echoing a modeled reading, to repeating a chosen passage freely, toward reading any new grade-level "
                    "text smoothly and with expression at the first attempt."
                ),
                "extensions": [
                    "Prepare and perform a reader's theater piece with assigned character voices",
                    "Move into richer chapter books as fluency grows; let the child set their own stamina target each week",
                    "Begin reading aloud to a younger sibling daily as the child's own real audience",
                ],
                "observation_focus": (
                    "Watch for the child grouping words into phrases, reading with expression, self-correcting freely, and "
                    "choosing to sustain longer and longer reading sessions on their own."
                ),
            },
            "unschooling": {
                "invitations": [
                    "Keep a generous shelf of inviting chapter books and poetry at and around the child's reading level within reach",
                    "Leave audiobooks alongside their printed books, so a fluent voice can be heard and followed",
                    "Make a cozy reading nook with good light, soft seating, and no distractions, where long uninterrupted reading is easy",
                    "Set up a small recital corner where the child can read aloud to a real audience (sibling, grandparent, video call) when they want to",
                ],
                "real_world_contexts": [
                    "Reading favorite chapter books aloud to younger siblings or pets",
                    "Reading a recipe aloud to the cook who has both hands in the work",
                    "Reading the lines of a play or a board game's instructions aloud",
                    "Reading along with audiobooks during long car trips",
                    "Reading aloud over the phone or video call to a grandparent who loves the same books",
                ],
                "conversation_starters": [
                    "Would you read me that part again? It sounded wonderful the way you said it.",
                    "How do you think this character would say that line?",
                    "Want to read this chapter aloud to your little sister tonight?",
                    "I heard you reading to yourself just now. Would you mind reading me the next page?",
                ],
                "resource_bank": [
                    "Many inviting chapter books at and around the child's reading level",
                    "Audiobooks paired with the printed books, especially for long car trips",
                    "Comics, poetry, plays, and reader's theater scripts kept available, never assigned",
                    "A recorder (a phone is enough) so the child can hear their own reading when they want to",
                ],
                "parent_role": (
                    "Read aloud to and with the child often. Give them real reasons and real audiences to read aloud for. "
                    "Let abundant time with loved books build fluency. Never time the reading or rank it; follow what the "
                    "child wants to read and notice the growth across months."
                ),
                "observation_documentation": (
                    "Across a term, note whether the child's reading is growing smoother and more expressive, whether they "
                    "self-correct meaning-changing errors, and whether they sustain longer and longer contented reading "
                    "sessions on their own. This noticing replaces any test."
                ),
            },
        },
        "connections": {
            "math": "Reading fluency is like automatic math-fact recall: when basic moves are automatic, the mind is free for harder thinking",
            "science": "Fluent reading allows the child to read and follow real science experiment instructions independently",
            "history": "Fluent readers can engage with simple biographies and historical narratives directly",
            "writing": "Reading with attention to punctuation and phrasing trains the writing hand to use those same marks deliberately",
        },
    },
}
