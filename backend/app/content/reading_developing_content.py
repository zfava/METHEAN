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
    "rd-02": {
        "enriched": True,
        "learning_objectives": [
            "Choose and complete an early chapter book at the child's instructional level across multiple days",
            "Hold the thread of a narrative across chapter boundaries: return to the book the next day knowing where the story is",
            "Recognize the structure of a chapter book: short chapters, sustained characters, a beginning / middle / end at the book scale",
            "Build reading stamina from 15 minutes toward 30 minutes of continuous independent silent reading",
            "Articulate a book preference: name what kind of chapter book the child likes and ask for more like it",
        ],
        "teaching_guidance": {
            "introduction": (
                "Foundational reading lived inside the picture book and the short decodable text: one sitting, one story, "
                "begin and finish on the same day. Chapter books are different in kind. The story is too long for one "
                "sitting; the child carries the narrative in mind across hours and days; the chapter break is the first "
                "place reading stops without the story ending. The skill is not reading harder words (the words on early "
                "chapter pages are often easier than the picture-book vocabulary) but holding more story longer. The "
                "right first chapter books are short-chapter, character-driven, illustrated where it helps: Frog and Toad, "
                "Mercy Watson, Magic Tree House, Henry and Mudge, Junie B. Jones, then The Boxcar Children, Charlotte's "
                "Web, Mr. Popper's Penguins, then up the ladder."
            ),
            "scaffolding_sequence": [
                "Tour the chapter book together: the cover, the title page, the table of contents, the first chapter heading; explain that the book has parts called chapters",
                "Read the first chapter aloud to the child while the child follows along in the book; talk about who the characters are and where the story starts",
                "Child reads the second chapter independently (or with parent on alternating pages); at the end, retell what happened in this chapter",
                "Stop at the end of a chapter even if the child wants to keep reading; mark the place with a bookmark and put the book in a known spot",
                "Next day, before reading the next chapter, ask the child to tell what happened so far; then continue",
                "Build the daily reading habit: a chosen reading time, a chosen reading place, a chosen book; the child reads the next chapter or 15 to 20 minutes, whichever is longer",
                "Across one book, log which chapter was the child's favorite and why; this builds the habit of having preferences",
                "When the book is finished, celebrate it: the child names what they liked, asks for another book like it, and starts the next",
            ],
            "socratic_questions": [
                "We're about to read chapter three. Before we start, can you tell me what happened in chapters one and two?",
                "This chapter ended on something exciting. Why do you think the author made it stop right there?",
                "You liked Frog and Toad. What was it about that book that you liked? What kind of book should we look for next?",
                "The book is long enough that we won't finish today. How does it feel to leave a story in the middle and come back tomorrow?",
                "If you imagine the story so far in your head, what do you see?",
            ],
            "practice_activities": [
                "Pick a first chapter book together at the library or bookstore; the child chooses among three the parent has pre-selected at the instructional level",
                "Daily chapter-or-twenty-minutes reading habit, same time and place each day, with a bookmark left at the stopping place",
                "Keep a 'books I have read' list on the wall or in a notebook; add each finished book to the list with the date",
                "After finishing a book, the child tells a parent or sibling what the book was about in three or four sentences (a real audience, real telling)",
                "Read aloud the first chapter or two of a book the child will then read independently; sometimes the parent's voice gets the child into a book they would otherwise put down",
            ],
            "real_world_connections": [
                "Going to the library on a regular schedule and choosing the next chapter book together",
                "Having a chosen reading time before bed when chapter books fit naturally into the day",
                "Trading books with a sibling, cousin, or friend who is reading at the same level",
                "Talking with a grandparent or older relative about a chapter book the relative also read as a child",
                "Watching a beloved chapter book read aloud as an audiobook on a long car ride, then picking up the physical book to reread",
            ],
            "common_misconceptions": [
                "Thinking the child must finish a chapter book in one sitting. Chapter books are multi-day reading by design; the chapter break is the natural stopping point.",
                "Pushing the child to longer books before stamina is built. Frog and Toad at full attention is better than Harry Potter at half attention.",
                "Treating the chapter book as a vocabulary test. The point at this band is sustained narrative comprehension, not unfamiliar-word counts.",
                "Insisting the child finish every book they start. The child who finishes 8 of 10 chosen books has built more than the child who slogs through 10 of 10. Permission to abandon is part of becoming a real reader.",
                "Choosing books for the child by parent literary taste alone. The child's preferences are the engine of reading volume; honor what the child wants to read.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Completes an early chapter book across one to two weeks at 15 to 30 minutes per day",
                "Can recall and retell the gist of yesterday's reading before continuing today",
                "Names the chapter structure: short chapters, sustained characters, a beginning and end at book scale",
                "Sustains 20+ minutes of continuous independent silent reading",
                "Articulates a preference: 'I like books about ___; the part I liked best was ___'",
            ],
            "proficiency_indicators": [
                "Completes a chapter book across two to three weeks with support",
                "Recalls main events of prior chapters with prompting",
                "Sustains 10 to 15 minutes of continuous reading",
            ],
            "developing_indicators": [
                "Loses the thread between chapters; needs a full reread to continue",
                "Sustains under 10 minutes of continuous reading",
                "Cannot name a book preference yet",
            ],
            "assessment_methods": [
                "completed-book log across a month",
                "before-reading retelling check (what happened so far?)",
                "after-book retelling (what was the book about, in your own words?)",
                "independent reading stamina log",
            ],
            "sample_assessment_prompts": [
                "Tell me what happened in the chapters you have read so far.",
                "After you finish this book, tell me what the book was about. What was your favorite part?",
                "How long did you read today without stopping?",
                "What kind of book do you want next? Tell me what you liked about this one so I know what to look for.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What does a 'chapter' mean in a chapter book?",
                "expected_type": "multiple_choice",
                "options": [
                    "A different book by the same author",
                    "A section of one book, with the rest of the book continuing the same story",
                    "A picture in the book",
                    "A word that's hard to read",
                ],
                "correct_answer": "A section of one book, with the rest of the book continuing the same story",
                "hints": [
                    "Look at the table of contents at the start of the book. Each line is one chapter.",
                ],
                "explanation": (
                    "A chapter is one section of a book. A chapter book has several chapters that together tell one story. "
                    "When one chapter ends, the next chapter continues the same story."
                ),
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": (
                    "You read three chapters of a chapter book yesterday. Today, before you start chapter four, what is "
                    "the best thing to do?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "Skip chapter four and read chapter five instead.",
                    "Start over from chapter one.",
                    "Take a moment to remember what happened in chapters one to three, then read chapter four.",
                    "Read chapter four very fast.",
                ],
                "correct_answer": "Take a moment to remember what happened in chapters one to three, then read chapter four.",
                "hints": [
                    "The story keeps going from where you left off. You need the story so far in your head.",
                ],
                "explanation": (
                    "Chapter books are written so each chapter continues the story. Spending a moment to remember the "
                    "story so far lets you read the new chapter with the right context."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "You picked a chapter book but after two chapters you don't really like it. What should you do?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "Force yourself to finish even though you don't like it.",
                    "Tell someone in your family why you don't like it and pick a different book.",
                    "Throw the book away.",
                    "Pretend to read it but actually do something else.",
                ],
                "correct_answer": "Tell someone in your family why you don't like it and pick a different book.",
                "hints": [
                    "Real readers abandon books they don't connect with. Naming why helps you find the next book.",
                ],
                "explanation": (
                    "Permission to abandon a book is part of being a real reader. Telling someone why you didn't like it "
                    "helps everyone find the next book that you will love. Forcing a bad fit damages the habit of reading."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "How long should you try to read your chapter book each day at this stage?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "5 minutes.",
                    "About 15 to 20 minutes, or one chapter, whichever is longer.",
                    "Two hours.",
                    "Until you finish the whole book in one sitting.",
                ],
                "correct_answer": "About 15 to 20 minutes, or one chapter, whichever is longer.",
                "hints": [
                    "Daily reading builds stamina. Long forced sessions burn the habit out.",
                ],
                "explanation": (
                    "Daily 15 to 20 minutes (or one chapter) is the target stamina-building habit. As stamina grows the "
                    "child will naturally want longer sessions; let the want lead."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "You finished your chapter book. The next thing to do is to tell someone what it was about. Practice now: "
                    "in three or four sentences, what would you say about the last chapter book you finished?"
                ),
                "expected_type": "text",
                "hints": [
                    "Name the main character and the situation, then say one or two main things that happened, then say what you liked.",
                ],
                "explanation": (
                    "A good book retelling at this band has: the main character or characters, the situation or problem, "
                    "one or two main things that happened, and the child's own response. It's a short telling, not a "
                    "summary of every event."
                ),
            },
        ],
        "assessment_items": [
            {
                "prompt": (
                    "Tell me what happened so far in the chapter book you are reading. (Asked before continuing into the "
                    "next chapter.)"
                ),
                "type": "open_response",
                "target_concept": "cross_chapter_retention",
                "rubric": (
                    "Mastery: names the main characters, the situation, and the main events of the chapters read so far in "
                    "coherent order. Proficient: names main characters and gist with some prompting. Developing: cannot "
                    "recall yesterday's reading without a reread."
                ),
            },
            {
                "prompt": "Tell me about the last chapter book you finished. What was it about, and what was your favorite part?",
                "type": "open_response",
                "target_concept": "book_level_retelling_and_preference",
                "rubric": (
                    "Mastery: 3 to 5 sentence retelling that captures the book's situation and main events, plus a "
                    "specific named favorite part. Proficient: shorter retelling, generic favorite. Developing: cannot "
                    "retell or articulate preference."
                ),
            },
            {
                "prompt": "How long can you read your current chapter book without stopping? Show me by reading until you naturally want a break.",
                "type": "open_response",
                "target_concept": "independent_reading_stamina",
                "rubric": (
                    "Mastery: sustains 20+ minutes. Proficient: 10 to 15 minutes. Developing: under 10 minutes."
                ),
            },
        ],
        "resource_guidance": {
            "required": [
                "early chapter books at the child's instructional level (Frog and Toad, Mercy Watson, Magic Tree House, Henry and Mudge, Junie B. Jones, then The Boxcar Children, Charlotte's Web, Mr. Popper's Penguins)",
                "a chosen reading place at home (a corner, a chair, a bedside spot)",
                "a bookmark and a known place for the current book between sittings",
            ],
            "recommended": [
                "a weekly library trip to keep books flowing in",
                "a 'books I have read' list (wall poster, notebook, or app) the child keeps themselves",
                "audiobooks of beloved chapter books for car trips and bedtime listening",
            ],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 20, "assessment": 15},
        "accommodations": {
            "dyslexia": (
                "Pair audiobooks with the printed book so the child hears the fluent voice while their eyes follow the "
                "text; many dyslexic readers love long books they would not yet read alone. Use the easiest chapter books "
                "(Frog and Toad, Mercy Watson) at this band, where the story interest is high and the text load is light. "
                "Read alternating pages aloud with the child."
            ),
            "adhd": (
                "Short-chapter books (Magic Tree House, Mercy Watson) are easier than long-chapter books at this band. "
                "Allow standing or fidgeting while reading. A clear 15-minute timer with a known stop is easier than open-"
                "ended stamina building. Reading on the move (bedtime, car, after lunch) works for many ADHD readers."
            ),
            "gifted": (
                "Move sooner to longer chapter books with more sustained narratives (Roald Dahl, E. B. White, Beverly Cleary, "
                "Kate DiCamillo, Lemony Snicket as the upper edge of the band). Introduce the idea of a series so the "
                "child reads several books with the same characters in a row. Honor wide reading volume as the goal."
            ),
            "visual_learner": "Books with illustrations across the band help (Frog and Toad, Henry and Mudge, Magic Tree House). Good light on the reading place.",
            "kinesthetic_learner": (
                "Read aloud at bedtime so the child can fidget and listen at once. Track with a finger or bookmark for the "
                "harder pages. Standing or walking while listening to an audiobook builds the same skill."
            ),
            "auditory_learner": "Audiobook-and-print pairing is especially effective. Read aloud first chapters to get the child into the book's voice.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": (
                    "Chapter books mark the move from reading one story in one sitting to holding one story across days. "
                    "Today and across this week we will choose, begin, and finish an early chapter book together, building "
                    "the habit of daily reading and the ability to remember the story across chapters."
                ),
                "gradual_release": {
                    "i_do": (
                        "Show the cover and title page; read the table of contents aloud; read the first chapter aloud while "
                        "the child follows. Name the chapter break and the bookmark, and show how the book waits in its "
                        "spot for tomorrow."
                    ),
                    "we_do": (
                        "Read the second chapter together, taking alternating pages or paragraphs. At the chapter break, "
                        "stop and have the child tell what has happened so far in the story."
                    ),
                    "you_do": (
                        "Child reads the next chapter independently for the daily 15 to 20 minutes (or one chapter). At "
                        "the end of the book, the child tells a parent or sibling what the book was about."
                    ),
                },
                "guided_practice": [
                    "Daily chapter-or-15-minutes habit at a chosen time and place",
                    "Before-reading retelling: tell the story so far, then continue",
                    "After-book retelling: 3 to 5 sentences about the book to a real audience",
                ],
                "independent_practice": [
                    "Choose the next book from three pre-selected options at instructional level",
                    "Keep the 'books I have read' list across the term",
                ],
                "mastery_check": [
                    "Completes an early chapter book across 1 to 2 weeks",
                    "Can recall yesterday's reading before continuing today",
                    "Sustains 20+ minutes of independent reading",
                ],
                "spiral_review": [
                    "Return to a favorite finished book occasionally for an easy fluent reread",
                ],
            },
            "classical": {
                "narrative_introduction": (
                    "The chapter book is the first long-form text the reader carries in mind. To read it well is an act of "
                    "memory and attention sustained across days, the grammar-stage habit that makes all later reading "
                    "possible. We choose worthy books and we read them daily, attentively, with the story held entire in "
                    "mind."
                ),
                "memory_work": {
                    "chants": [
                        "Recite the chapter book habit: a chapter or fifteen minutes, every day, the same time and place",
                        "Recite the daily prompt: before today's chapter, tell what has happened so far",
                    ],
                    "recitations": [
                        "Memorize and recite one short passage of beautiful language from the chapter book in progress each week",
                    ],
                },
                "copywork": [
                    "Copy one sentence of fine language from the chapter book in progress each week, into the copybook, attending to its punctuation and rhythm",
                ],
                "recitation_routine": (
                    "Each lesson begins with the child telling what has happened so far in the chapter book, then reads the "
                    "next chapter; the narrative is recited cumulatively across the days of the book."
                ),
                "history_integration": (
                    "Choose chapter books that sit along the chronological spine (historical fiction at the right age: "
                    "Little House series, Mr. Popper's Penguins, The Courage of Sarah Noble) so the reading practice runs "
                    "with the history sequence."
                ),
                "read_aloud_suggestions": [
                    "Read aloud a slightly more advanced chapter book each evening alongside the child's own independent chapter book; the parent voice carries the harder language while the child reads their own at independent level",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "Living chapter books with truly beautiful language and real story interest: Charlotte's Web, The Little House series, Mr. Popper's Penguins, Mrs. Frisby and the Rats of NIMH (upper edge), Frog and Toad, Mercy Watson at the entry",
                    "Avoid twaddle: thin series-pulp written down to the child rarely earns the reader; choose the books worth the time even at the easy end",
                ],
                "short_lesson_flow": (
                    "Sit together, the child with the book in hand. The child reads a chapter (or a portion that fits the "
                    "20-minute lesson) attentively, once and well. At the end, the child narrates the chapter to the parent "
                    "in their own words. Stop while the reading is still a pleasure; the next day continues the same book."
                ),
                "narration_prompt": (
                    "Tell me the chapter you just read in your own words. What did you most enjoy in it?"
                ),
                "real_world_objects": [
                    "The chapter book itself, kept where the child can return to it daily",
                    "A small reading nook with good light and quiet",
                    "A simple reading journal where the child copies a favorite sentence and notes the book and chapter",
                ],
                "nature_connection": (
                    "Some chapter books at this band are themselves nature-attentive (Charlotte's Web, The Little House "
                    "books, the early Magic Tree House books); the chapter book practice supports the nature notebook by "
                    "modeling careful observation of small things."
                ),
                "habit_focus": (
                    "The habit of attention sustained across many days. The chapter book is the first place the child "
                    "experiences a story too long for one sitting; the daily habit makes this kind of reading the child's "
                    "own."
                ),
            },
            "montessori": {
                "prepared_materials": [
                    "A reading corner stocked with chapter books at and just above the child's independent level, the child choosing freely",
                    "A 'books I have read' list the child keeps themselves, with the date each book was finished",
                    "A bookmark and a known place for the current book between sittings",
                    "A small notebook for copying one favorite sentence per book, when the child wants to",
                ],
                "presentation": {
                    "three_period_lesson": (
                        "This is a chapter. Show me where this chapter ends. Where does the next chapter begin? Where does "
                        "the book wait until tomorrow? The chapter, the bookmark, the spot are introduced calmly, then "
                        "handed to the child as the child's own."
                    ),
                    "steps": [
                        "The guide shows the chapter book, the table of contents, the chapter break, and the bookmark spot",
                        "The child chooses among offered chapter books at their independent level",
                        "The child reads a chapter (or 15 to 20 minutes) in the reading corner each day",
                        "At the end of each book, the child adds it to their own 'books I have read' list with the date",
                    ],
                },
                "control_of_error": (
                    "The story itself is the control: a child who has lost the thread will say so when asked to retell, and "
                    "will return to the bookmark on their own to reread. The guide does not correct; the guide notices and "
                    "the child mends."
                ),
                "abstraction_pathway": (
                    "From listening to a chapter book read aloud, to reading chapters together, toward reading whole chapter "
                    "books independently and choosing the next book from the shelf with confidence."
                ),
                "extensions": [
                    "When a book in a series is loved, the child reads the next book in the series",
                    "When the child has finished several books by one author, name the author and look for more",
                    "Begin a small reading journal with one copied sentence per book",
                ],
                "observation_focus": (
                    "Watch for the child returning to the reading corner freely, sustaining longer reading sessions across "
                    "the term, naming book preferences in their own words, and beginning to choose the next book without "
                    "the guide picking it."
                ),
            },
            "unschooling": {
                "invitations": [
                    "Keep a generous, well-curated shelf of early chapter books at the child's reading level within reach",
                    "Make weekly library trips a family habit, with the child choosing books for themselves",
                    "Leave audiobooks of beloved chapter books alongside the print versions for car trips and bedtime",
                    "Make a cozy reading nook with good light and quiet where long uninterrupted reading is easy",
                ],
                "real_world_contexts": [
                    "Bedtime reading time set aside as the child's own",
                    "Long car trips with audiobooks the whole family listens to together",
                    "Sharing favorite chapter books with siblings, cousins, friends at the same reading level",
                    "Talking with grandparents about chapter books they read as children",
                ],
                "conversation_starters": [
                    "What part of the book are you in? Tell me what's happening.",
                    "Did you like that book? What kind of book do you want next?",
                    "Want to listen to the audiobook of your next book on our car trip?",
                    "Should we try a book by that author you liked? They wrote a lot more.",
                ],
                "resource_bank": [
                    "Many inviting chapter books at and around the child's reading level",
                    "Audiobooks paired with the print, especially for long car trips",
                    "Series the child can fall into and read several of in a row",
                    "A library card the child uses freely",
                ],
                "parent_role": (
                    "Talk about books in the family conversation the way other families talk about TV or sports. Honor the "
                    "child's preferences. Welcome the abandoned books as readily as the finished ones. Never time the "
                    "reading; trust that volume builds the habit and the habit builds the reader."
                ),
                "observation_documentation": (
                    "Across a term, note the books finished, the books abandoned, the kinds of books the child returns to, "
                    "and the growing length of their daily reading. This noticing replaces any test or stamina log."
                ),
            },
        },
        "connections": {
            "math": "Sustained attention to a chapter book builds the same stamina muscle as sustained attention to a multi-step math problem",
            "science": "A child who can hold a chapter-book story in mind can begin to hold a science narrative (the life cycle, the experiment, the explanation) in mind too",
            "history": "Historical fiction chapter books (Little House, Mr. Popper) are an early door into the history sequence",
            "writing": "Reading whole chapter books is the precondition for writing one's own short stories with chapters",
        },
    },
    "rd-03": {
        "enriched": True,
        "learning_objectives": [
            "Narrate a multi-paragraph passage (3 to 6 paragraphs, 300 to 800 words) in coherent order after a single attentive reading or hearing",
            "Retain and report specific details: names of characters, settings, key events, and the order in which events happened",
            "Organize the retelling: a beginning that names who and where, a middle that carries the main events, an end that resolves",
            "Listen or read with the narration in mind: attend on first hearing knowing the retelling will come",
            "Distinguish between narration (the child's own retelling of the text) and personal response (what the child thought or felt about it); both have a place, narration is the prior skill",
        ],
        "teaching_guidance": {
            "introduction": (
                "Foundational oral narration (rf-15) lived inside the single paragraph or short page: read or hear one "
                "paragraph, retell it. At the developing level the passage stretches to several paragraphs, sometimes a "
                "whole short chapter or a several-page nonfiction explanation. The skill grows in three ways: the child "
                "holds more text in mind before retelling, organizes a longer retelling into a sensible order, and "
                "attends with the narration in mind on the first reading or hearing. This is the central Charlotte Mason "
                "practice, and it is also a workhorse comprehension assessment across philosophies; a child who can "
                "narrate a passage clearly has understood it."
            ),
            "scaffolding_sequence": [
                "Start with a single paragraph the child can retell easily (rf-15 level) to refresh the habit",
                "Move to a two-paragraph passage; before reading, tell the child they will narrate it at the end",
                "Read or have the child read a 3-paragraph passage attentively, once and well; ask for the narration",
                "If the narration is thin, ask one specific follow-up (who was in the passage? what happened first? what happened next?); do not re-read the passage",
                "Across a week, extend to 4, 5, and 6 paragraphs as the child can hold them",
                "Vary the source: a chapter of a chapter book, a science passage, a history passage, a poem with narrative content",
                "Practice both modes: oral narration of a passage read aloud by the parent, AND oral narration of a passage the child has just read silently themselves",
                "Introduce the organizing prompt for longer passages: 'tell me first who is in the story and where it is, then tell me what happened, then tell me how it ended'",
            ],
            "socratic_questions": [
                "Before we read, what would help you remember this passage well enough to tell me about it after?",
                "You told me about the second part of the passage but skipped the first. Can you go back and start at the beginning?",
                "You said the boy went into the forest. What happened in the forest, in the order it happened?",
                "Was there a part of the passage you forgot? Listen again to just this sentence... does that bring it back?",
                "If you were going to tell this passage to someone who has never heard it, what would they need to know first?",
            ],
            "practice_activities": [
                "Read-aloud-and-narrate: the parent reads a chosen 3 to 6 paragraph passage attentively once; the child narrates",
                "Silent-and-narrate: the child reads a chosen passage silently themselves; immediately tells it back",
                "Tell-it-to-someone-else: after the child narrates the parent, the child then tells the same passage to a sibling, grandparent, or recorder; the second telling is often more organized",
                "Daily narration habit: choose one passage a day, in one subject (reading, science, history, biography); the child narrates and the parent simply listens",
                "Narrate across days: read a chapter today, narrate it; tomorrow, narrate yesterday's chapter before reading today's",
            ],
            "real_world_connections": [
                "Telling a parent about a movie or show the child watched without you",
                "Reporting on a field trip or a visit to a relative's house",
                "Recounting a chapter of a book to a younger sibling at bedtime",
                "Telling a grandparent over the phone what the family did this week",
                "Explaining a science demonstration or a history story to a parent who missed it",
            ],
            "common_misconceptions": [
                "Confusing narration with summary. Narration is the child's full telling in their own words, with the events in order; summary is shorter and more abstract. Narration is the prior skill and is the developing-band target.",
                "Asking the child to write down the narration. Oral narration is the band-appropriate practice; written narration is the next skill (rd-04). Mixing them too early burdens both.",
                "Re-reading the passage when the child's narration is thin. The point of narration is attention on the first reading; re-reading on demand teaches the child to attend less the first time.",
                "Grading or correcting the narration in real time. Narration is the child's own work; the parent listens. If a detail is misremembered, the next narration is the place to do better, not the current one.",
                "Letting personal response replace narration ('I liked the part where...'). Personal response is welcome AFTER the narration; the narration itself stays in the text.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Narrates a 4 to 6 paragraph passage coherently after a single attentive reading or hearing",
                "Includes the main characters, the setting, the main events in order, and the resolution",
                "Organizes the retelling clearly: beginning, middle, end",
                "Distinguishes narration from personal response when prompted",
                "Sustains the habit of narrating without resentment or struggle across a daily practice",
            ],
            "proficiency_indicators": [
                "Narrates a 3 to 4 paragraph passage with main events in order, some prompting on omissions",
                "Sometimes skips a part or jumbles the order; recovers with one follow-up prompt",
            ],
            "developing_indicators": [
                "Narrates only the most recent or most striking part; cannot give the passage in order",
                "Needs a re-read to narrate anything; cannot attend with the narration in mind on the first hearing",
            ],
            "assessment_methods": [
                "daily oral narration of a passage of increasing length",
                "narration across days (yesterday's chapter narrated today)",
                "narration to a real audience (sibling, grandparent, recording)",
                "narration of varied source types (fiction, science, history, biography)",
            ],
            "sample_assessment_prompts": [
                "Tell me about the passage you just read, in your own words. Start at the beginning.",
                "Tell me what we read yesterday in the chapter book, before we start today's chapter.",
                "Tell your little sister what happened in the science reading today, so she knows.",
                "Tell this passage to the recorder so we can listen back to it together.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What does it mean to 'narrate' a passage you have just read?",
                "expected_type": "multiple_choice",
                "options": [
                    "To read the passage again out loud, word for word.",
                    "To tell the passage back in your own words, in the order it happened.",
                    "To write a list of every detail in the passage.",
                    "To say whether you liked it.",
                ],
                "correct_answer": "To tell the passage back in your own words, in the order it happened.",
                "hints": [
                    "Narration is the child's own retelling, not a re-reading.",
                ],
                "explanation": (
                    "Narration is telling the passage back in your own words. It includes the main events in the order they "
                    "happened. It is NOT re-reading the passage and it is NOT just saying you liked it."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "You are about to read a chapter and your parent says: 'I'll ask you to tell it to me when you are done.' "
                    "What is the best thing to do while you read?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "Skim quickly so you finish faster.",
                    "Read attentively and notice who is in the chapter and what happens, knowing you will tell it back.",
                    "Memorize the exact words of the chapter.",
                    "Skip to the end so you know what happens.",
                ],
                "correct_answer": "Read attentively and notice who is in the chapter and what happens, knowing you will tell it back.",
                "hints": [
                    "Narration rewards attention on the first reading. You don't need to memorize words; you need to follow the story.",
                ],
                "explanation": (
                    "The point of narration is to learn to attend with full attention the first time. You don't memorize "
                    "exact words; you notice the characters, the setting, and the events as they unfold, so you can tell "
                    "them back."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "You narrate a chapter, and you forget to mention the part where the dog ran away. What is the best "
                    "thing to do?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "Insist you didn't forget anything.",
                    "Add the part about the dog when you remember, even if it's out of order. Next time, try to attend to the whole chapter.",
                    "Refuse to narrate again.",
                    "Re-read the whole chapter immediately.",
                ],
                "correct_answer": "Add the part about the dog when you remember, even if it's out of order. Next time, try to attend to the whole chapter.",
                "hints": [
                    "Forgetting a part is normal; the practice grows over time, not in one session.",
                ],
                "explanation": (
                    "Forgetting parts is normal at first; the practice grows over weeks. Add what you remember, and try to "
                    "attend to the whole chapter next time. Re-reading on demand teaches you to attend less the first time."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "After narrating the chapter, your parent asks: 'And what did you think of it?' Is this part of the "
                    "narration?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "Yes, it is exactly what narration means.",
                    "No, but it is welcome after the narration. Narration is the retelling of the text itself; personal response comes after.",
                    "Yes, and the narration is unnecessary if you give a strong opinion.",
                    "No, and your parent should not ask.",
                ],
                "correct_answer": "No, but it is welcome after the narration. Narration is the retelling of the text itself; personal response comes after.",
                "hints": [
                    "Narration is the child's own telling of the text. Personal response is a separate, welcome practice.",
                ],
                "explanation": (
                    "Narration is the retelling of the text itself, in the child's own words, in order. Personal response "
                    "('I liked the part where...', 'I thought the character was wrong to...') is a different welcome "
                    "practice that lives alongside narration. Both have a place; they are not the same."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "Practice now: take a passage you have recently read (a chapter of your chapter book, a science "
                    "reading, a history reading), and narrate it to whoever is around. Was it easier or harder than "
                    "you expected? Why?"
                ),
                "expected_type": "text",
                "hints": [
                    "Notice what you did to remember the order of events.",
                    "Notice what you forgot, and how you noticed you forgot it.",
                ],
                "explanation": (
                    "Self-noticing during narration is part of the practice. With time the child develops their own "
                    "internal sense of 'have I told the main parts in order'. Naming what was easy and what was hard "
                    "feeds the next narration."
                ),
            },
        ],
        "assessment_items": [
            {
                "prompt": (
                    "Read this 4 to 6 paragraph passage attentively once, then tell it back to me in your own words. "
                    "(Use any grade-level reading or chapter excerpt.)"
                ),
                "type": "open_response",
                "target_concept": "extended_oral_narration",
                "rubric": (
                    "Mastery: includes main characters, setting, main events in order, and resolution; coherent organization "
                    "(beginning / middle / end); little or no prompting needed. Proficient: most main events in order with "
                    "one or two prompts. Developing: only the most striking part; events out of order; needs re-read."
                ),
            },
            {
                "prompt": (
                    "Yesterday we read a chapter of your chapter book. Before we read today's chapter, tell me what "
                    "happened in yesterday's chapter."
                ),
                "type": "open_response",
                "target_concept": "narration_across_days",
                "rubric": (
                    "Mastery: clear retelling of yesterday's chapter with main events in order. Proficient: gist with some "
                    "prompting. Developing: cannot recall without a reread."
                ),
            },
            {
                "prompt": (
                    "Tell this same passage to your sibling (or to a recording). Did the second telling change?"
                ),
                "type": "open_response",
                "target_concept": "narration_to_real_audience",
                "rubric": (
                    "Mastery: organizes the retelling better for the second audience; adds context the listener needs. "
                    "Proficient: similar retelling, audience-aware. Developing: identical or worse second telling."
                ),
            },
        ],
        "resource_guidance": {
            "required": [
                "passages at the child's reading or listening level, 3 to 6 paragraphs in length (chapters, science readings, history readings, biographies)",
                "a real audience for narrations (parent, sibling, grandparent, recorder)",
                "a daily narration habit slot in the day",
            ],
            "recommended": [
                "a narration notebook the parent keeps with brief notes on what the child narrated each day across the term, to see growth",
                "audiobooks of beloved passages for narration after listening (a different mode from narration after reading)",
                "a small recorder or phone for self-narrations the child can listen back to",
            ],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 15},
        "accommodations": {
            "dyslexia": (
                "Start narration on parent-read-aloud passages, not silent-reading passages, so the comprehension is not "
                "limited by decoding effort. Long oral narration of a listened passage is a real strength path for many "
                "dyslexic readers. Extend to silent-read narration gradually as fluency builds."
            ),
            "adhd": (
                "Short passages (3 paragraphs) and frequent narration (daily) rather than long passages with weekly "
                "narration. Allow the child to walk or fidget during narration. Real audiences (sibling, grandparent on "
                "video call) add motivation and structure."
            ),
            "gifted": (
                "Extend to longer passages (whole short chapters or full nonfiction articles) sooner. Introduce narration "
                "of more complex texts (Plutarch's Lives at age, simpler Shakespeare in prose retelling at age). The child "
                "narrates not only what happened but begins to organize the retelling by theme as well as by sequence."
            ),
            "visual_learner": "Allow the child to make a small sketch alongside the narration if it helps them organize the retelling.",
            "kinesthetic_learner": "Let the child walk while narrating. Some children narrate best while doing something else with their hands (drawing, building, knitting).",
            "auditory_learner": "Record-and-listen-back is especially effective for self-noticing. Narrating to a real listener strengthens the practice.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": (
                    "Oral narration of longer passages is one of the central comprehension practices at this band. The "
                    "child reads or hears a 3 to 6 paragraph passage attentively once, then tells it back in their own "
                    "words, in order. The practice grows the habit of attending to a whole passage the first time and of "
                    "organizing a coherent retelling."
                ),
                "gradual_release": {
                    "i_do": (
                        "The parent models a narration of a passage they have just read aloud: 'this passage was about a "
                        "boy named Jack who lived in a small village. He went into the forest to gather wood. In the "
                        "forest he met a fox who could speak...' The model is the child's first sight of what a narration "
                        "is."
                    ),
                    "we_do": (
                        "Parent and child take turns narrating sections of a passage: the parent narrates paragraph one, "
                        "the child paragraph two, the parent paragraph three. Then the child narrates the whole passage "
                        "by stringing the sections together."
                    ),
                    "you_do": (
                        "The child reads or hears a 3 to 6 paragraph passage attentively, once and well, then narrates it "
                        "back to the parent without prompts. The parent listens without correcting in real time."
                    ),
                },
                "guided_practice": [
                    "Daily oral narration of one passage from the day's reading",
                    "Vary the source type across the week (fiction, science, history, biography)",
                    "Practice narration across days: yesterday's chapter today, before today's chapter",
                ],
                "independent_practice": [
                    "Child narrates to a real audience (sibling, grandparent, recorder) at the child's chosen time",
                    "Child develops the habit of attending with the narration in mind on the first reading",
                ],
                "mastery_check": [
                    "Narrates a 4 to 6 paragraph passage coherently after a single attentive reading",
                    "Includes main characters, setting, main events in order, and resolution",
                    "Sustains the daily habit without resentment",
                ],
                "spiral_review": [
                    "Return to easier and shorter passages occasionally to keep the practice fluent",
                    "Re-narrate a passage from earlier in the term to notice growth",
                ],
            },
            "classical": {
                "narrative_introduction": (
                    "Narration is among the oldest of the grammar-stage practices: the child attends to a text once and "
                    "well, then tells it back. The practice trains the memory, the order of mind, and the tongue all at "
                    "once. The Greeks and the medieval schoolmen knew it; Charlotte Mason brought it to a fine point; we "
                    "carry it on."
                ),
                "memory_work": {
                    "chants": [
                        "Recite the narration prompt: tell me first who is in the passage and where it is, then tell me what happened, then tell me how it ended",
                        "Recite the narration rule: attend on the first reading; tell it back in your own words; in order",
                    ],
                    "recitations": [
                        "Memorize one fine sentence from each week's narrated passage and recite it cumulatively across the term, so the language of the readings is held in the ear",
                    ],
                },
                "copywork": [
                    "Copy one well-formed sentence from each week's narrated passage into the copybook, attending to its rhythm and punctuation, so the language is held by the hand as well as by the tongue",
                ],
                "recitation_routine": (
                    "Begin each lesson with the prior day's narration recited from memory; then read or hear the new "
                    "passage and narrate it; the practice grows cumulatively across the term."
                ),
                "history_integration": (
                    "Choose narration passages from history along the chronological spine: Plutarch in age-appropriate "
                    "form, Bible stories, the lives of great figures, the founding documents at age. The narration "
                    "practice and the history sequence reinforce each other."
                ),
                "read_aloud_suggestions": [
                    "Worthy short prose for daily narration: Aesop's fables, biographies in plain language, well-written nature writing, the great stories told well",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "Living books with truly beautiful, careful language across the subjects: A Child's History of the World, Burgess's Bird Book and Animal Book, James Herriot's stories, the Boxcar Children for fiction, Hans Christian Andersen, the Blue Fairy Book",
                    "Avoid twaddle: narration is shaped by what is narrated; thin texts make thin narrations",
                ],
                "short_lesson_flow": (
                    "Sit together with the book. Read aloud (or have the child read) one passage attentively, once and "
                    "well. The child immediately narrates it in their own words. The parent listens without correcting "
                    "in the moment. Stop while the practice is still alive; the next day continues."
                ),
                "narration_prompt": (
                    "Tell me back the passage we just read. In your own words. Take your time."
                ),
                "real_world_objects": [
                    "A living book the family is reading together",
                    "The reading nook or table where narration happens daily",
                    "A small notebook the parent keeps with brief notes on what the child narrated each day across the term",
                ],
                "nature_connection": (
                    "After a nature walk, the child narrates what they saw and did, in order; the same skill that narrates "
                    "a chapter narrates a real experience"
                ),
                "habit_focus": (
                    "The habit of attention sustained across a whole passage. The narration is its own discipline: one "
                    "careful reading, one careful retelling. Across years this grows into the adult's habit of saying what "
                    "they have understood in their own words."
                ),
            },
            "montessori": {
                "prepared_materials": [
                    "A shelf of passages at the child's level for daily narration: short chapters, science readings, history readings, biographies",
                    "A small recorder or phone the child may use to narrate to themselves and play back",
                    "A simple notebook the child may keep with the date and topic of each narration",
                ],
                "presentation": {
                    "three_period_lesson": (
                        "This is a narration: you tell me back what you have read in your own words. Show me how you start "
                        "your narration; how you keep it in order; how you bring it to an end. The form is shown, then "
                        "handed to the child as the child's own practice."
                    ),
                    "steps": [
                        "The child chooses or is offered a passage of appropriate length",
                        "The child reads or hears the passage attentively, once and well",
                        "The child immediately narrates it, either to an adult, to a small listener, or to a recorder",
                        "The child notices for themselves what they remembered well and what was harder to hold",
                    ],
                },
                "control_of_error": (
                    "The recorder is the control: the child plays back their own narration and hears what is clear, what "
                    "is jumbled, and what was forgotten. The adult does not correct; the child mends on the next narration."
                ),
                "abstraction_pathway": (
                    "From narrating a single paragraph (rf-15) to narrating a multi-paragraph passage to narrating a chapter "
                    "to narrating an entire short book; each step taken when the prior one is effortless."
                ),
                "extensions": [
                    "Narrate across days: yesterday's chapter today before starting today's chapter",
                    "Narrate a passage to a real audience the child has chosen (a younger sibling at bedtime, a grandparent on a video call)",
                    "Narrate from multiple subject areas across a week (chapter book, science, history, biography)",
                ],
                "observation_focus": (
                    "Watch for the narration becoming more organized over the term: a clear beginning that names who and "
                    "where, a middle that carries events in order, an end that resolves. Watch also for the child noticing "
                    "their own forgetting and attending more carefully on the next reading."
                ),
            },
            "unschooling": {
                "invitations": [
                    "Read aloud generously and let the child tell you about it when they want to, without pressure",
                    "Make space at meals or in the car for the child to tell about what they have been reading, watching, or doing",
                    "Set up real audiences for the child's tellings (a grandparent on a video call, a younger sibling at bedtime, a friend over for the afternoon)",
                ],
                "real_world_contexts": [
                    "Telling a parent about a chapter of a chapter book at bedtime",
                    "Telling a grandparent about the week in a phone call",
                    "Telling a sibling about a show or book they didn't see",
                    "Recapping a field trip or visit to a relative",
                ],
                "conversation_starters": [
                    "What's been happening in your book lately? I want to hear all about it.",
                    "I missed that part of the show. Tell me what happened.",
                    "Want to tell your sister about the chapter you read today?",
                    "What was the science reading about? I love hearing you explain things.",
                ],
                "resource_bank": [
                    "Many real audiences for tellings (family, friends, video calls, audio recorders)",
                    "Generous reading-aloud time where the child can tell back as much or as little as they want",
                    "No forced narration sessions; narration grows from the child's own wish to tell",
                ],
                "parent_role": (
                    "Be a real listener. Welcome the child's tellings of books, shows, days, conversations. Notice when the "
                    "tellings grow longer, more organized, more confident across months. Never grade a telling; respond to "
                    "it as a real listener responds to a real story."
                ),
                "observation_documentation": (
                    "Across a term, note the kinds of things the child narrates spontaneously, the length and coherence of "
                    "tellings, the audiences chosen, and the topics returned to. This noticing replaces any test."
                ),
            },
        },
        "connections": {
            "math": "The order-of-events skill in narration is the same skill that orders the steps of a multi-step math problem in writing",
            "science": "Narrating a science passage is the comprehension check for that passage; a child who can narrate it has understood it",
            "history": "Plutarch and other historical narrations have been the central history texts of the classical tradition for centuries; narration is the way they were learned",
            "writing": "Oral narration is the prior skill to written narration (rd-04), which is the prior skill to all of expository writing",
        },
    },
    "rd-04": {
        "enriched": True,
        "learning_objectives": [
            "After narrating a passage orally, write one to three sentences capturing the main events of the passage",
            "Use complete sentences with capitals at the start and periods at the end",
            "Choose words for clarity, not just length: the written narration is shorter than the spoken one by design",
            "Write a beginning sentence that names who and where, and an ending sentence that says how the passage resolved or what it left to think about",
            "Develop the habit of sitting down to a daily short writing without resistance: the page is short, the topic is known, the prior oral narration has done the cognitive work",
        ],
        "teaching_guidance": {
            "introduction": (
                "Written narration is the bridge from oral narration to all of expository writing. The child has already "
                "told the passage out loud (rd-03); now they pick up a pencil and write one to three sentences that "
                "capture the main events. The skill is not generating new ideas (oral narration already did that) but "
                "transferring an organized telling onto the page in a few well-formed sentences. The keys: keep it short, "
                "let the oral narration carry the thinking, do not let the writing burden the reading. The writing here is "
                "in service of comprehension, not in service of writing-as-a-subject; the writing-as-a-subject work lives "
                "in the writing strand, not in reading-developing."
            ),
            "scaffolding_sequence": [
                "Begin with a one-sentence written narration: after the child has narrated orally, ask 'in one sentence, what was the passage about?'",
                "Have the child say the sentence aloud first, then write it down; the saying-it-aloud is the planning step",
                "Move to a two-sentence written narration: the first sentence names who and where; the second sentence carries the main event",
                "Move to a three-sentence written narration: beginning (who and where), middle (what happened), end (how it resolved or what it leaves us with)",
                "Always keep the writing short: 3 sentences maximum at this band; the temptation to write more is the temptation that ruins the habit",
                "Read what the child wrote back aloud together; the child notices for themselves whether it captures the passage",
                "Vary the source: chapter-book chapter, science reading, history passage, biography; one short written narration a day across one term builds the habit",
                "Allow strategic scribe support: for the youngest in this band, the parent may write down the child's spoken sentence the first few times, then the child takes over the pencil",
            ],
            "socratic_questions": [
                "You just told me the passage. If you had to write only one sentence, which sentence would catch the most of it?",
                "Read what you wrote back to yourself. Does it say what the passage said?",
                "Is there anything important you left out? Is there anything you put in that does not need to be there?",
                "If you read your sentence to someone who had never read the passage, what would they know? What would they not know?",
                "How do you start a sentence on the page? How do you end one?",
            ],
            "practice_activities": [
                "Daily 1-to-3 sentence written narration habit, the same time as the oral narration, with a chosen passage from the day's reading",
                "Read-aloud back: the child reads their written narration aloud and notices whether it captures the passage",
                "Across-the-week growth: start the week at 1 sentence, end the week at 3 sentences, on the same kind of passage",
                "Share the written narrations: the child reads their week's narrations to a parent at the end of the week, the parent simply listens",
                "Keep a small narration notebook with the date, the source, and the 1-to-3 sentences for each day; across a term the notebook becomes the child's own evidence of growth",
            ],
            "real_world_connections": [
                "Writing a short text message or note about a book to a relative who shares the child's reading",
                "Writing a sentence under a drawing in a nature notebook",
                "Writing a card to thank a grandparent who sent a book",
                "Writing the bedtime gist of what the family read aloud, before sleep",
                "Writing the title and one sentence about each chapter in a reading journal as the child finishes a chapter",
            ],
            "common_misconceptions": [
                "Treating written narration as a long composition. The point at this band is one to three sentences. Long writing burns the habit.",
                "Letting handwriting struggle dominate the practice. If handwriting is hard, the parent may scribe the first few times. The point is the comprehension and sentence-level expression, not the handwriting workout.",
                "Skipping the oral narration before writing. Oral narration is the planning step. Without it, written narration feels like blank-page composition, which is a different harder skill.",
                "Correcting every spelling and punctuation error in the moment. Note one or two corrections per day at most; the writing habit is more fragile than the editing habit.",
                "Reading-developing written narration is NOT a writing-strand replacement. The writing strand has its own work; this is reading-comprehension-expressed-in-writing, kept short on purpose.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Writes 1 to 3 well-formed sentences after oral narration that capture the main events of the passage in order",
                "Uses capitals at the start of sentences and end punctuation",
                "Names who and where in the first sentence; names how it resolved or what it leaves us with in the last sentence",
                "Sustains a daily short written narration habit across a term without resistance",
            ],
            "proficiency_indicators": [
                "Writes 1 to 2 sentences capturing the gist with some support on word choice or sentence boundaries",
                "Most sentences have capitals and end punctuation",
            ],
            "developing_indicators": [
                "Writes a fragment or a single word; needs scribe support to capture a sentence",
                "Capitals and end punctuation inconsistent",
            ],
            "assessment_methods": [
                "daily written narration entry of 1 to 3 sentences",
                "weekly review of the week's narrations: does the set show growth?",
                "read-aloud-back check: the child reads what they wrote and confirms it captures the passage",
            ],
            "sample_assessment_prompts": [
                "You just narrated the chapter aloud. Now write me one sentence that captures the main thing that happened.",
                "Write two sentences about today's reading: the first names who and where; the second tells what happened.",
                "Write three sentences about your science passage: beginning, middle, end.",
                "Read me back the sentences you just wrote. Do they capture the passage?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": (
                    "What is a 'written narration' at this stage?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "A long composition about your reading.",
                    "One to three sentences capturing the main events of a passage you have just narrated aloud.",
                    "Copying the passage word for word.",
                    "A drawing instead of writing.",
                ],
                "correct_answer": "One to three sentences capturing the main events of a passage you have just narrated aloud.",
                "hints": [
                    "Written narration at this band is SHORT on purpose: 1 to 3 sentences.",
                ],
                "explanation": (
                    "Written narration at this band is short by design. The child has already done the oral narration; the "
                    "writing is the brief capture, not a long composition."
                ),
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": (
                    "What should you do BEFORE you write your written narration?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "Read the passage three more times.",
                    "Narrate the passage aloud first; the oral narration is the planning step.",
                    "Skip the writing entirely.",
                    "Copy the first sentence of the passage.",
                ],
                "correct_answer": "Narrate the passage aloud first; the oral narration is the planning step.",
                "hints": [
                    "Oral narration prepares the writing.",
                ],
                "explanation": (
                    "Oral narration is the planning step. After saying the gist aloud, the writing becomes much easier. "
                    "Skipping the oral step makes the writing feel like a hard blank-page composition."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "Read this short passage in your head: 'Maya went to the lake with her grandfather. They sat on a log "
                    "and watched the herons fish in the shallow water. When the sun got low, they walked home along the "
                    "path.' Now write a one-sentence written narration."
                ),
                "expected_type": "text",
                "hints": [
                    "Name who, where, and the main thing that happened.",
                    "Start with a capital, end with a period.",
                ],
                "explanation": (
                    "A strong one-sentence narration might be: 'Maya and her grandfather went to the lake to watch the "
                    "herons fish, and then walked home at sunset.' It names who, where, what they did, and how it ended, "
                    "all in one sentence."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "You wrote: 'maya and her grandfather went to the lake they watched herons'. What are the two things "
                    "to fix?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "Add a drawing and a date.",
                    "Capitalize 'Maya' at the start, and split into two sentences with end punctuation.",
                    "Make it longer.",
                    "Use more interesting words.",
                ],
                "correct_answer": "Capitalize 'Maya' at the start, and split into two sentences with end punctuation.",
                "hints": [
                    "Sentence boundaries are the editing focus at this band.",
                ],
                "explanation": (
                    "At this band the two editing points are: capital at the start of each sentence, and end punctuation. "
                    "The content is fine; the form is fixed up."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "You have been writing a 1-to-3 sentence narration every day for two weeks. You read this week's "
                    "narrations next to last week's. What should you look for to notice your growth?"
                ),
                "expected_type": "text",
                "hints": [
                    "Look at sentence completeness, at capturing the main event, at order, and at the habit itself.",
                ],
                "explanation": (
                    "Look for: sentences that are more complete and well-formed; narrations that capture the main events "
                    "rather than just one striking detail; events more often in order; the writing happening more easily "
                    "and willingly. Across weeks the growth is small but real."
                ),
            },
        ],
        "assessment_items": [
            {
                "prompt": (
                    "After your daily oral narration, write 1 to 3 sentences capturing the main events of the passage. "
                    "Read what you wrote back to me."
                ),
                "type": "open_response",
                "target_concept": "daily_short_written_narration",
                "rubric": (
                    "Mastery: 1 to 3 well-formed sentences capturing the main events; capitals and end punctuation; "
                    "first sentence names who and where. Proficient: gist captured with some sentence-form issues. "
                    "Developing: fragment, single word, or scribe-dependent."
                ),
            },
            {
                "prompt": "Read me the written narrations from this week. Where do you see growth from Monday to Friday?",
                "type": "open_response",
                "target_concept": "self_noticing_of_growth",
                "rubric": (
                    "Mastery: names a real change (longer sentences, better capture, more in order). Proficient: notices "
                    "with prompting. Developing: cannot articulate."
                ),
            },
            {
                "prompt": "Write three sentences about today's reading: beginning, middle, end.",
                "type": "open_response",
                "target_concept": "three_sentence_structured_narration",
                "rubric": (
                    "Mastery: three sentences in beginning / middle / end order, well-formed. Proficient: three sentences "
                    "with some structural issues. Developing: fewer than three sentences or out of order."
                ),
            },
        ],
        "resource_guidance": {
            "required": [
                "a passage at the child's reading or listening level for the daily oral-then-written narration",
                "a notebook or composition book for the daily written narration",
                "a pencil and eraser; legible handwriting on lined paper",
            ],
            "recommended": [
                "a parent-scribe option for the youngest in the band (the parent writes the child's spoken sentence the first few times)",
                "a weekly read-back ritual where the child reads the week's narrations aloud to a parent",
                "a small, well-bound notebook the child takes pride in (the physical object matters at this band)",
            ],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 10},
        "accommodations": {
            "dyslexia": (
                "Allow parent-scribe support for as long as it serves the child; the comprehension goal does not require "
                "the child to do the handwriting in this practice. Phonetic spelling is acceptable; the editing focus is "
                "sentence boundaries (capital and period), not spelling. A keyboard is an acceptable substitute for the "
                "pencil if it serves the child."
            ),
            "adhd": (
                "Keep the writing short: 1 sentence, often, is enough. Allow standing or movement before sitting down to "
                "the write. The daily 5-minute write is easier than the weekly 30-minute write."
            ),
            "gifted": (
                "Move to longer written narrations (5 to 8 sentences with paragraph structure) sooner. Introduce variations: "
                "narrating the same passage to two different audiences. Keep the written narration short relative to the "
                "oral narration; the temptation to over-write is real for gifted writers and the habit is more important "
                "than the length."
            ),
            "visual_learner": (
                "Allow a small sketch alongside the narration. Use lined paper with a generous space between lines."
            ),
            "kinesthetic_learner": (
                "Let the child walk or pace while saying the sentence aloud before writing it down. The motion is the "
                "planning step; the writing is the capture."
            ),
            "auditory_learner": (
                "Say the sentence aloud before writing it. Read the written narration aloud at the end. The voice is the "
                "guide to the sentence boundary."
            ),
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": (
                    "Written narration is the bridge from oral narration to all of expository writing. The child orally "
                    "narrates a passage, then writes 1 to 3 sentences capturing the main events. The practice grows the "
                    "habit of writing short, clear sentences in service of comprehension."
                ),
                "gradual_release": {
                    "i_do": (
                        "The parent models a one-sentence written narration after their own oral narration. The parent "
                        "writes the sentence on a piece of paper for the child to see, and reads it back aloud."
                    ),
                    "we_do": (
                        "Parent and child compose a one-sentence narration together: the child says the sentence aloud, "
                        "the parent suggests adjustments, the child writes it down. The capital and the period are "
                        "explicitly noted."
                    ),
                    "you_do": (
                        "After the daily oral narration, the child writes 1 to 3 sentences independently. The parent "
                        "listens to the read-aloud-back and notes one or two small things; corrections are minimal at "
                        "this band."
                    ),
                },
                "guided_practice": [
                    "Daily 1-to-3 sentence written narration after the oral narration",
                    "Read-aloud-back: the child reads what they wrote",
                    "Weekly week-review: read the week's narrations aloud at the end of the week",
                ],
                "independent_practice": [
                    "Keep the narration notebook with the date and the source",
                    "Across the term, the notebook becomes the child's own evidence of growth",
                ],
                "mastery_check": [
                    "Writes 1 to 3 well-formed sentences daily after oral narration",
                    "Sentence boundaries (capital and period) consistent",
                    "Sustains the daily habit across the term without resistance",
                ],
                "spiral_review": [
                    "Re-read narrations from earlier in the term to notice growth",
                    "Re-narrate (orally and in writing) an earlier passage to see how the practice has matured",
                ],
            },
            "classical": {
                "narrative_introduction": (
                    "Written narration is the grammar-stage move from telling to writing. The child has already learned "
                    "to attend, to remember, and to retell aloud; now the pencil takes up the same act. The hand learns "
                    "what the tongue already knows. This is the practice that, daily and patiently, makes the later "
                    "expository writing easy."
                ),
                "memory_work": {
                    "chants": [
                        "Recite the rule of the sentence: a sentence begins with a capital, ends with a period or other mark, and tells one thing whole",
                        "Recite the narration prompt: say it aloud first, then write what you said",
                    ],
                    "recitations": [
                        "Recite cumulative favorite sentences from the week's narrations; the child's own well-formed sentences are worth keeping",
                    ],
                },
                "copywork": [
                    "Copy one well-formed sentence from the day's reading into the copybook before writing the narration; the sentence the child sees becomes the model for the sentence the child writes",
                ],
                "recitation_routine": (
                    "Each lesson: oral narration first, then written narration of 1 to 3 sentences. The week's written "
                    "narrations are read aloud on Friday cumulatively."
                ),
                "history_integration": (
                    "Choose narration passages from the chronological spine; the written narrations across a term form a "
                    "running gloss on the history sequence in the child's own hand"
                ),
                "read_aloud_suggestions": [
                    "Worthy short prose for daily narration: Aesop, Plutarch in age-appropriate retellings, biographies, well-written nature writing; the child's written narrations will be as good as the language being narrated",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "Living books with truly fine language across the subjects (see rd-03); narration is shaped by what is narrated",
                    "Avoid twaddle for narration: thin sources make thin narrations",
                ],
                "short_lesson_flow": (
                    "After the daily oral narration, the child writes 1 to 3 sentences in the narration notebook. The "
                    "parent listens to the read-aloud-back and welcomes the writing without correcting in the moment. The "
                    "next day continues."
                ),
                "narration_prompt": (
                    "Now write me one or two sentences about what you just told me. Read it back to me when you are done."
                ),
                "real_world_objects": [
                    "A simple, well-bound narration notebook the child takes pride in",
                    "A sharpened pencil and an eraser kept with the notebook",
                    "A quiet table or lap-desk where the daily writing happens",
                ],
                "nature_connection": (
                    "After a nature observation, write one or two sentences in the nature notebook about what was seen; "
                    "the same narration habit, on the natural world"
                ),
                "habit_focus": (
                    "The habit of short, daily, sustained writing in service of comprehension. The hand learns what the "
                    "tongue already knows. Across years this grows into the adult's ability to write a short clear "
                    "account of what they have understood."
                ),
            },
            "montessori": {
                "prepared_materials": [
                    "A composition book the child manages as their own narration notebook",
                    "Sentence-strip cards modeling well-formed sentences with capitals and end marks, available in the writing area",
                    "Date and source stamp or template the child uses to head each day's entry",
                ],
                "presentation": {
                    "three_period_lesson": (
                        "This is a one-sentence written narration: it begins with a capital, ends with a period, and "
                        "tells one whole thing. Show me a one-sentence written narration of the passage you just told me. "
                        "How would you change it to be a two-sentence narration?"
                    ),
                    "steps": [
                        "After the oral narration, the child opens the notebook to the next page",
                        "The child says the sentence aloud first, then writes it",
                        "The child reads back what they wrote",
                        "Across the term the child moves from one to two to three sentences without prompting",
                    ],
                },
                "control_of_error": (
                    "The read-aloud-back is the control: the child hears whether what they wrote says what they meant. "
                    "Sentence-strip cards in the writing area show the form of a well-made sentence; the child compares "
                    "their own sentence to the model and adjusts without correction from outside."
                ),
                "abstraction_pathway": (
                    "From the parent scribing the child's spoken sentence, to the child writing one sentence after oral "
                    "narration, to the child writing 2 to 3 sentences with clear structure, toward writing without the "
                    "prior oral narration step (which lives in the writing strand, not here)"
                ),
                "extensions": [
                    "Add a date and source to each entry; the notebook becomes a real reading journal",
                    "Copy one beautiful sentence from each week's reading alongside the narration",
                    "Read a finished narration aloud to a real audience (sibling, grandparent, recorder)",
                ],
                "observation_focus": (
                    "Watch for sentence form firming up across the term, for the child writing without resistance, for "
                    "narrations capturing main events rather than scattered details, and for the child's own pride in the "
                    "notebook as it grows."
                ),
            },
            "unschooling": {
                "invitations": [
                    "Keep a small notebook the child likes (a chosen cover, a chosen size) where they may write about their reading whenever they want",
                    "Pin or tape the child's short written narrations on the fridge or a family bulletin board where the household sees them",
                    "Welcome any short writing about books, days, events: birthday cards, thank-you notes, a sentence under a drawing, a recipe tried",
                ],
                "real_world_contexts": [
                    "Writing a thank-you card to a relative who sent a book",
                    "Writing a one-sentence label for a drawing in a nature notebook",
                    "Writing a text or email to a grandparent about a book or a day",
                    "Writing a recipe card the family uses",
                    "Writing a one-sentence book recommendation to a friend",
                ],
                "conversation_starters": [
                    "Want to write a sentence about your book on a card to grandma?",
                    "I love what you just said about the chapter. Want to write it down?",
                    "Should we put a sentence under your drawing?",
                ],
                "resource_bank": [
                    "Notebooks, cards, paper, pens, and pencils kept available",
                    "Real audiences for the child's short writings (family on the fridge, grandparents by mail, friends in cards)",
                    "No forced writing sessions; written narration grows from the oral narration habit and from real reasons to write",
                ],
                "parent_role": (
                    "Welcome the child's short writings warmly. Honor the spelling that gets the meaning across. Notice "
                    "growth across months. Never grade a written narration; respond to it as a real reader responds to "
                    "a real note."
                ),
                "observation_documentation": (
                    "Across a term, note the short writings that have entered the family life (cards, labels, notes, the "
                    "child's own notebook), the kinds of things the child writes spontaneously, and the growing sentence "
                    "form. This noticing replaces any test."
                ),
            },
        },
        "connections": {
            "math": "The sentence-boundary skill (one thought, complete, with a capital and a period) is the same orderly habit that frames a math-problem answer",
            "science": "Short written narrations of science readings are the precursor to the science notebook and to lab-report writing",
            "history": "Daily written narrations of history passages accumulate into the child's own running history journal across the term",
            "writing": "Written narration is the bridge from oral narration to all of expository writing; the writing strand picks up here and goes further",
        },
    },
    "rd-05": {
        "enriched": True,
        "learning_objectives": [
            "Distinguish fiction (a made-up story) from nonfiction (an account of real things) and give the reason for the distinction in one's own words",
            "Identify common fiction sub-genres in age-appropriate texts: realistic fiction, fantasy, mystery, adventure, historical fiction",
            "Identify common nonfiction sub-genres: informational text, biography, how-to / procedural, opinion / persuasive (introductory)",
            "Use text features to confirm genre: a fiction book's cover and chapter structure differ from a nonfiction book's table of contents, headings, captions, and index",
            "Choose a book for a real purpose and name the genre that fits the purpose ('I want to know about volcanoes, so I need an informational book')",
        ],
        "teaching_guidance": {
            "introduction": (
                "Foundational reading let the child enjoy stories and facts side by side without naming the difference: "
                "Frog and Toad and a book about frogs lived on the same shelf. The developing level makes the category "
                "explicit. The child learns that fiction is a made-up story (even if it draws on real things) and "
                "nonfiction is an account of real things (even if it tells the story of a real life). They learn the "
                "sub-genres within each, and they learn that books announce their genre through their physical and "
                "structural features: a fiction book typically has a cover with the title and the author, illustrations "
                "inside, chapters with chapter numbers and sometimes chapter titles, a continuous narrative voice; a "
                "nonfiction book typically has a table of contents with topics, headings inside the text, captions under "
                "pictures, bold or italic vocabulary, and often a glossary and an index at the back. This is the first "
                "metalinguistic turn in reading: the child reads ABOUT books, not just IN them."
            ),
            "scaffolding_sequence": [
                "Lay out three pairs of books on the table: a chapter book and an informational book on a similar topic (e.g. Charlotte's Web and a book about real pigs)",
                "Pick up each book in turn and ask: is this a story someone made up, or is this an account of real things?",
                "Open each book and notice the difference in structure: a story has chapters and unfolds in time; an informational book has topics and unfolds by subject",
                "Introduce the words fiction and nonfiction explicitly; use them across the next several reading sessions",
                "Move to sub-genres of fiction: realistic fiction (could happen, but didn't), fantasy (could not happen the way the story tells it), mystery (something to figure out), adventure (a journey with stakes), historical fiction (a story set in a real time in the past)",
                "Move to sub-genres of nonfiction: informational text (tells about a topic), biography (tells about a real person's life), how-to / procedural (tells you how to do something), opinion / persuasive (tells you what the author thinks; introduced lightly)",
                "Practice with the household's actual book collection: child sorts the family's books into fiction and nonfiction piles, then into sub-genre piles",
                "Practice choosing for purpose: 'I want to learn about ___; what kind of book do I need?' and 'I want to enjoy a long story tonight; what kind of book do I want?'",
            ],
            "socratic_questions": [
                "Is this book about real things or made-up things? How do you know?",
                "The cover of this book has a picture of a real volcano on it. Does that mean it is nonfiction? What else should you check?",
                "Can a nonfiction book tell a story? (Yes, a biography tells the story of a real life.) Can a fiction book teach you real things? (Yes, historical fiction can teach you about a real time period, even though the characters and plot are made up.)",
                "What kind of book is Charlotte's Web? It has a pig who talks. Is that fiction or nonfiction, and what sub-genre?",
                "What kind of book is a biography of Harriet Tubman? Is it fiction or nonfiction? Why?",
                "You want to learn how to build a birdhouse. What kind of book do you need?",
            ],
            "practice_activities": [
                "Book sort: lay out 10 to 15 books from the household library and have the child sort them into fiction and nonfiction piles, then into sub-genre piles within each",
                "Cover-and-table-of-contents inspection: practice deciding genre from the outside of the book and the first inside pages, before reading",
                "Library visit with a genre goal: 'today let's find a realistic fiction book' or 'today let's find a how-to book about something you want to learn to do'",
                "Genre journal: at the end of each chapter book or nonfiction book the child finishes, log the title, the genre, and the sub-genre",
                "Pair-reading: pair a fiction and a nonfiction book on a similar topic (Charlotte's Web with a book about real farm animals; Magic Tree House about a historical time with a real biography from that time) and read them in parallel",
            ],
            "real_world_connections": [
                "Choosing a book at the library or bookstore for a real reason (a school project, a hobby, a long car trip)",
                "Recognizing the difference between a story aunt tells at dinner (a real account = nonfiction in spirit) and a story a grandfather makes up at bedtime (fiction in spirit)",
                "Reading the back cover of a movie or show to decide if it is based on a true story or is entirely made up",
                "Recognizing news (nonfiction by intent) vs novels (fiction by intent) in the home library",
                "Recognizing instructions (how-to nonfiction) vs stories about cooking (which might be either fiction or memoir)",
            ],
            "common_misconceptions": [
                "Thinking 'fiction' means 'fake' and so is somehow lesser. Fiction is the made-up story; fiction can be deeply true about human nature even though the events did not happen.",
                "Thinking 'nonfiction' means 'true in every word'. Nonfiction is an account of real things, but accounts can be more or less accurate; even a true biography is the author's selection of what to tell.",
                "Treating a single illustration or cover as the genre signal. The cover gives a clue; the structure of the book (chapters with continuous narrative vs topics with headings) is the stronger signal.",
                "Believing a fiction book cannot teach you anything real. Historical fiction, realistic fiction, and even fantasy can teach about people, places, and times; the difference is the made-up frame, not the truth-value of every detail.",
                "Forcing every book into a single sub-genre. Real books often blend (a historical fiction mystery; an informational text with a narrative thread). The sub-genre names are tools, not boxes.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Distinguishes fiction from nonfiction with confidence on books the child has not seen before, using structural and content cues",
                "Names common sub-genres of fiction (realistic fiction, fantasy, mystery, adventure, historical fiction) and nonfiction (informational, biography, how-to, opinion / persuasive) with examples from the child's own reading",
                "Uses text features (cover, table of contents, headings, captions, glossary, index) to confirm genre",
                "Chooses books for a real purpose and names the genre that fits the purpose",
                "Recognizes that fiction and nonfiction are categories, not value judgments: a fiction book can be deeply true and a nonfiction book can be the author's selection",
            ],
            "proficiency_indicators": [
                "Distinguishes fiction from nonfiction reliably; sub-genres named with some prompting",
                "Uses some text features to confirm genre",
            ],
            "developing_indicators": [
                "Confuses fiction and nonfiction; needs prompting on most books",
                "Sub-genre names not yet held",
            ],
            "assessment_methods": [
                "book sort against the household library",
                "cover-and-table-of-contents inspection on unfamiliar books",
                "genre journal of finished books",
                "library-trip genre goal: the child finds a book matching a named genre",
            ],
            "sample_assessment_prompts": [
                "Here is a stack of 10 books. Sort them into fiction and nonfiction.",
                "Now sort the fiction pile into sub-genres. What sub-genres do you have?",
                "Pick up this book you have never seen. Without reading the inside, tell me what genre you think it is and how you can tell.",
                "I want to learn how to make bread. What kind of book do I need?",
                "Read the genre journal entries from last month. What genre did you read the most? What genre have you not read at all?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is the main difference between fiction and nonfiction?",
                "expected_type": "multiple_choice",
                "options": [
                    "Fiction is short and nonfiction is long.",
                    "Fiction is a made-up story; nonfiction is an account of real things.",
                    "Fiction is for children and nonfiction is for adults.",
                    "Fiction has illustrations and nonfiction does not.",
                ],
                "correct_answer": "Fiction is a made-up story; nonfiction is an account of real things.",
                "hints": [
                    "Think about whether the events in the book really happened or were made up.",
                ],
                "explanation": (
                    "Fiction is a made-up story; nonfiction is an account of real things. Both can be long or short, both "
                    "can have illustrations, both can be for any age."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "Charlotte's Web has a pig named Wilbur and a spider named Charlotte who can write words in her web. "
                    "Is Charlotte's Web fiction or nonfiction? What sub-genre?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "Nonfiction; informational text.",
                    "Fiction; realistic fiction.",
                    "Fiction; fantasy.",
                    "Nonfiction; biography.",
                ],
                "correct_answer": "Fiction; fantasy.",
                "hints": [
                    "Spiders cannot really write words in webs.",
                    "Fantasy is fiction that includes things that cannot happen in the real world.",
                ],
                "explanation": (
                    "Charlotte's Web is fiction (the events are made up) and fantasy (a spider writing words in a web "
                    "cannot happen in the real world). It is a great example of fantasy being deeply true about love, "
                    "friendship, and loss even though the events did not happen."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "A book is called 'Harriet Tubman: Conductor on the Underground Railroad'. The cover has a portrait of "
                    "Harriet Tubman. Inside there is a table of contents with chapters like 'Childhood' and 'The First "
                    "Escape'. What genre is this book?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "Fiction; historical fiction.",
                    "Nonfiction; biography.",
                    "Fiction; adventure.",
                    "Nonfiction; how-to.",
                ],
                "correct_answer": "Nonfiction; biography.",
                "hints": [
                    "A biography tells the story of a real person's life.",
                    "Harriet Tubman was a real person. The chapters follow her actual life.",
                ],
                "explanation": (
                    "This is a biography: a nonfiction account of a real person's life. Even though it tells a story (her "
                    "life as a story), it is nonfiction because Harriet Tubman was a real person and the events described "
                    "really happened."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "You want to learn how to fold a paper airplane. What kind of book do you need?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "A realistic fiction book about a boy who flies a paper airplane.",
                    "A how-to / procedural book that shows the steps to fold one.",
                    "A fantasy book about a magic airplane.",
                    "A biography of a famous paper-airplane folder.",
                ],
                "correct_answer": "A how-to / procedural book that shows the steps to fold one.",
                "hints": [
                    "What kind of book teaches you to DO something?",
                ],
                "explanation": (
                    "A how-to (procedural) book is the nonfiction sub-genre that teaches the reader to do something with "
                    "steps. The fiction options might be enjoyable, but they will not teach you how to fold the airplane."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "A book about the American Revolution has chapters and a continuous story about a fictional 12-year-old "
                    "boy who lives in Boston in 1773 and gets caught up in the Boston Tea Party. The cover shows the boy "
                    "in colonial clothes, and the author's note at the back says 'the boy is invented, but the events of "
                    "the Tea Party are described as they really happened'. What genre is this book?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "Fiction; historical fiction.",
                    "Nonfiction; biography.",
                    "Nonfiction; informational text.",
                    "Fiction; fantasy.",
                ],
                "correct_answer": "Fiction; historical fiction.",
                "hints": [
                    "The main character is made up but the historical setting is real.",
                    "Historical fiction is fiction set in a real time period.",
                ],
                "explanation": (
                    "Historical fiction is the sub-genre that uses a made-up character or plot in a real historical "
                    "setting. The author's note is the giveaway: the boy is invented, but the events around him really "
                    "happened. Historical fiction can teach a lot about a real time period even though the foreground story "
                    "is fiction."
                ),
            },
        ],
        "assessment_items": [
            {
                "prompt": "Sort these 10 books into fiction and nonfiction piles. Tell me how you decided for each.",
                "type": "open_response",
                "target_concept": "fiction_nonfiction_sort",
                "rubric": (
                    "Mastery: correct sort with reasons that name structural or content cues. Proficient: correct sort "
                    "with reasons that are partial. Developing: incorrect sort or no reasons given."
                ),
            },
            {
                "prompt": "Now sort the fiction pile into sub-genres. What sub-genres did you find? What sub-genre is missing from the household library?",
                "type": "open_response",
                "target_concept": "fiction_sub_genre_recognition",
                "rubric": (
                    "Mastery: names at least three common fiction sub-genres present in the sort and one that is missing. "
                    "Proficient: names two sub-genres. Developing: cannot name sub-genres."
                ),
            },
            {
                "prompt": "I want to find a book that will teach me about real birds and how to identify them. What genre and sub-genre do I need? Where in the household library should I look?",
                "type": "open_response",
                "target_concept": "purpose_to_genre_mapping",
                "rubric": (
                    "Mastery: names nonfiction informational text or field guide; points to where in the library it lives. "
                    "Proficient: names nonfiction without sub-genre. Developing: names a fiction book or cannot answer."
                ),
            },
            {
                "prompt": "Open this book you have never seen before. Without reading the inside, tell me what genre you think it is and what features helped you decide.",
                "type": "open_response",
                "target_concept": "cover_and_text_feature_inspection",
                "rubric": (
                    "Mastery: names the genre and cites at least two cues (cover style, table of contents structure, "
                    "headings, illustrations). Proficient: names the genre with one cue. Developing: names the genre by "
                    "guess without cues."
                ),
            },
        ],
        "resource_guidance": {
            "required": [
                "the household library: a mixed collection of fiction and nonfiction books for the child to sort and inspect",
                "a few clear examples of each major sub-genre (realistic fiction, fantasy, mystery, adventure, historical fiction; informational, biography, how-to, opinion / persuasive)",
                "library card or regular library access to broaden the genre exposure",
            ],
            "recommended": [
                "a genre journal: a small notebook where the child logs the title, genre, and sub-genre of each book they finish",
                "a labeled shelf or bin system in the home library that groups books by genre",
                "a library tour with a librarian: ask the children's librarian to show how the library groups books by genre",
            ],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 15, "assessment": 15},
        "accommodations": {
            "dyslexia": (
                "Genre awareness builds on listening as much as on reading. Read aloud examples of each sub-genre; the "
                "child sorts and categorizes by listening to the genre cues. Audiobooks across genres deepen the "
                "category sense without adding decoding load."
            ),
            "adhd": (
                "The book-sort activity is hands-on and engaging; many children with ADHD prefer this kind of "
                "categorization to passive instruction. Keep the sort to 10 to 15 books; longer is overwhelming. Use "
                "physical piles rather than a list."
            ),
            "gifted": (
                "Introduce more sub-genres: science fiction (often grouped under fantasy but worth distinguishing for "
                "the gifted reader), folktale and legend, memoir as distinct from biography, persuasive vs informational "
                "as a sharper distinction. Begin to notice cross-genre or hybrid books."
            ),
            "visual_learner": (
                "Build a genre wall: a poster with sub-genre boxes and a representative book cover in each, that grows "
                "across the year. The visual category map anchors the sub-genre names."
            ),
            "kinesthetic_learner": (
                "The book-sort activity is the central practice for this child; let them physically move and stack the "
                "books. Set up genre-labeled bins on the floor and sort into them."
            ),
            "auditory_learner": (
                "Discuss genre cues aloud. Listen to a few minutes of audiobook from each sub-genre and notice the "
                "differences in narrator voice (a how-to book sounds different from a story)."
            ),
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": (
                    "Today we learn the basic categories of books: fiction (made-up story) and nonfiction (account of "
                    "real things), and the sub-genres within each. We will sort the household library, inspect books "
                    "by their structure, and learn to choose books for a real purpose by their genre."
                ),
                "gradual_release": {
                    "i_do": (
                        "Hold up three pairs of books and name each as fiction or nonfiction with the reason: 'this is "
                        "fiction, a made-up story about a pig'; 'this is nonfiction, an account of real pigs'. Show the "
                        "structural differences inside each: chapters vs headings, narrative voice vs topic structure."
                    ),
                    "we_do": (
                        "Sort a small set of books together with the child, taking turns deciding fiction or nonfiction "
                        "and naming the sub-genre. Discuss any ambiguous cases together."
                    ),
                    "you_do": (
                        "Child sorts the household library independently and keeps a genre journal of finished books "
                        "across the term."
                    ),
                },
                "guided_practice": [
                    "Book sort with the parent's set of 10 to 15 books",
                    "Cover-and-table-of-contents inspection on unfamiliar books",
                    "Library trip with a genre goal",
                ],
                "independent_practice": [
                    "Daily genre journal entry for each book finished",
                    "Sub-genre reading goals across a term ('this month I want to read at least one biography and one how-to')",
                ],
                "mastery_check": [
                    "Distinguishes fiction from nonfiction reliably on unfamiliar books",
                    "Names sub-genres within each with examples",
                    "Chooses books for purpose by genre",
                ],
                "spiral_review": [
                    "Re-sort the household library at the end of the term; notice how many books have been read and how the categories have grown",
                ],
            },
            "classical": {
                "narrative_introduction": (
                    "The kinds of books are old and worth naming. The Greeks knew that the made-up story (mythos) and the "
                    "account of real things (historia) were different acts of telling. The medieval scholars named "
                    "biography (the life of a saint), the chronicle (the account of years), the romance (the made-up "
                    "adventure). To learn the kinds of books is to take up the long habit of careful naming."
                ),
                "memory_work": {
                    "chants": [
                        "Recite the rule: fiction is a made-up story; nonfiction is an account of real things",
                        "Recite the sub-genres of fiction: realistic fiction, fantasy, mystery, adventure, historical fiction",
                        "Recite the sub-genres of nonfiction: informational text, biography, how-to, opinion",
                    ],
                    "recitations": [
                        "Memorize one fine sentence from each sub-genre the child encounters this term, to hold the language of each kind of book",
                    ],
                },
                "copywork": [
                    "Copy one well-formed sentence from a book of each major sub-genre across the term into the copybook; the language of each genre lives in the hand",
                ],
                "recitation_routine": (
                    "Begin each new reading session with the genre of the book named: 'today we are reading a biography; "
                    "biography is the nonfiction sub-genre that tells the life of a real person.'"
                ),
                "history_integration": (
                    "Pair historical fiction and biographies and informational texts along the chronological spine. The "
                    "child sees how three different kinds of books tell about the same time."
                ),
                "read_aloud_suggestions": [
                    "A worthy book from each major sub-genre across the term, so the ear knows the difference: realistic fiction (Charlotte's Web), fantasy (The Lion the Witch and the Wardrobe), mystery (Encyclopedia Brown), adventure (My Side of the Mountain), historical fiction (The Witch of Blackbird Pond, Sarah Plain and Tall), biography (Abraham Lincoln by D'Aulaire), informational text (a beautifully written nature book), how-to (a real craft or cooking book)",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "Beautiful examples of each sub-genre, real books with real literary or expository quality, never twaddle",
                    "Living biography: D'Aulaire's, Genevieve Foster, Jean Fritz at age",
                    "Living informational text: Holling C. Holling (Paddle-to-the-Sea), Burgess (Burgess Bird Book), Robert McCloskey, real nature writing",
                    "Living realistic fiction and historical fiction: McCloskey, Wilder, MacLachlan, Brink, Speare",
                ],
                "short_lesson_flow": (
                    "Sit at the table with a small stack of varied books from the home shelf. Look at one together: who "
                    "wrote it, what is it about, is it a story made up or an account of real things? Talk about it. The "
                    "lesson is calm; the categorization is a noticing, not a quiz."
                ),
                "narration_prompt": (
                    "Tell me what kind of book this is and how you know. What sub-genre is it within that kind?"
                ),
                "real_world_objects": [
                    "The household library, real books on real shelves the child can sort and shelve",
                    "A library card and weekly library visits",
                    "A simple genre journal kept across the term",
                ],
                "nature_connection": (
                    "Nature writing is a strong example of living informational text. A field guide is a strong example "
                    "of how-to nonfiction. Both can be brought outside on a walk and used in the field."
                ),
                "habit_focus": (
                    "The habit of careful noticing: knowing the kind of book in hand before deciding how to read it. The "
                    "fiction reader sinks into the story; the nonfiction reader looks for the topic and the structure; "
                    "the careful reader knows which mode they are in."
                ),
            },
            "montessori": {
                "prepared_materials": [
                    "A genre-sort tray with cards (FICTION / NONFICTION; the sub-genre names within each) and a small set of cover-image cards or actual short books for sorting",
                    "A labeled bookshelf in the reading area with genre sections the child can shelve and reshelve",
                    "A genre journal the child keeps with the title, genre, and sub-genre of each book finished",
                    "Field-trip cards: a library tour with the librarian, an introduction to how the library is organized by genre",
                ],
                "presentation": {
                    "three_period_lesson": (
                        "This is a biography; this is a how-to; this is a fantasy. Show me a biography on the shelf. Show "
                        "me a fantasy. What kind of book is this one? The names are given slowly across many days; the "
                        "third period is only when the recognition is sure."
                    ),
                    "steps": [
                        "The guide presents the fiction / nonfiction distinction with a clear pair of books",
                        "The guide presents one sub-genre at a time, with several examples and the name",
                        "The child sorts books in the reading area, freely, returning to the sort across days and weeks",
                        "The child keeps the genre journal as their own work",
                    ],
                },
                "control_of_error": (
                    "The book itself is the control: the table of contents, the chapter structure, the captions, the "
                    "author's note all confirm or correct a tentative genre call. The child compares their call to the "
                    "evidence inside the book and adjusts without correction from outside."
                ),
                "abstraction_pathway": (
                    "From sorting concrete books on a tray, to naming the genre of any new book on first inspection, "
                    "toward reading a book differently because of its genre (sinking into fiction, looking for the topic "
                    "and structure in nonfiction)"
                ),
                "extensions": [
                    "Add a sub-genre to the sort each week as the child encounters it",
                    "Sort the household library and propose a new shelving arrangement to the family",
                    "Visit the library and notice how the library is organized by genre",
                ],
                "observation_focus": (
                    "Watch for the child reaching for a particular kind of book for a particular purpose, naming the genre "
                    "in their own talk, and beginning to balance their reading across sub-genres rather than staying in "
                    "one favorite."
                ),
            },
            "unschooling": {
                "invitations": [
                    "Keep a generous shelf of varied books across all the major sub-genres within reach",
                    "Take regular library trips and let the child wander the children's section, noticing how the library groups books",
                    "Leave a small basket of how-to books near the child's hobby or project area",
                    "Talk about books across genres in the family conversation: 'I'm reading a biography of Lincoln, what are you reading?'",
                ],
                "real_world_contexts": [
                    "Choosing a library book for a real project the child is working on",
                    "Recognizing the genre of a movie or show ('this is based on a true story, so it's like a biography'; 'this is a fantasy')",
                    "Sorting the household library together when reorganizing or moving",
                    "Recommending books to a friend by genre ('if you liked X, you'll like Y, they're both adventure stories')",
                ],
                "conversation_starters": [
                    "Is the book you're reading a made-up story or about real things?",
                    "What kind of book do you feel like tonight? Story, or learning something?",
                    "Want me to find you a how-to book about the thing you're trying to build?",
                ],
                "resource_bank": [
                    "A varied home library across all major sub-genres",
                    "Library card, used freely",
                    "Audiobooks across genres for car trips and bedtime",
                    "A bin or shelf for current-interest nonfiction the child has chosen for themselves",
                ],
                "parent_role": (
                    "Talk about books in the family conversation as if genre were a real thing the household notices. "
                    "Welcome the child's preferences, including the long stretches in one genre. Notice across months "
                    "whether they're widening or staying in one place; both are fine; widening can be invited but not "
                    "forced."
                ),
                "observation_documentation": (
                    "Across a term, note the genres the child returns to, the genres the child has not touched, and the "
                    "real-world choices the child makes by genre. This noticing replaces any test."
                ),
            },
        },
        "connections": {
            "math": "Sorting and classification are the same skills used in math when sorting shapes, numbers, or sets; genre is one more sort",
            "science": "Nonfiction informational text is the central reading mode for science; recognizing it as a category supports the reading-of-science",
            "history": "Biography and historical fiction together carry much of the elementary history sequence; recognizing the genre tells the child which mode to read in",
            "writing": "Recognizing the kinds of writing in published books prepares the child to write within those kinds (writing a how-to, writing a short biography, writing a story); writing-strand connections continue from here",
        },
    },
    "rd-06": {
        "enriched": True,
        "learning_objectives": [
            "Describe a character's traits, motivations, and changes using specific evidence from the text",
            "Distinguish character TRAITS (what the character is like, generally) from MOTIVATIONS (why the character did this specific thing) from CHANGES (how the character grew or shifted across the story)",
            "Cite a specific page, paragraph, or scene as evidence when claiming a character trait",
            "Compare two characters within one story (or one character across two stories) on trait, motivation, and change",
            "Distinguish what the text actually says about a character from what the reader has imagined or assumed",
        ],
        "teaching_guidance": {
            "introduction": (
                "Foundational comprehension (rf-14) named characters and noticed what they did. Developing character "
                "analysis is a genuine step up: the child describes WHO the character is (traits), WHY they do what they "
                "do (motivations), and HOW they change across the story (arc), and they support each claim with specific "
                "evidence from the text. This is the entry to all of literary reading: from this skill grow theme "
                "(rd-22), inference about character (rd-14), and eventually full literary analysis at the intermediate "
                "and advanced bands. The discipline of CITING EVIDENCE is the key habit: the child says 'I think Wilbur "
                "is humble because on page 47 he says...' rather than 'I think Wilbur is humble'. The evidence is the "
                "whole point."
            ),
            "scaffolding_sequence": [
                "Choose a chapter book or story the child has read with characters worth thinking about (Charlotte's Web, Mrs. Frisby, The Lion the Witch and the Wardrobe, Roald Dahl, anything with characters who change)",
                "Name a character together. Ask: what is this character like? Take three or four words the child offers (brave, lonely, curious, stubborn)",
                "For each trait word, ask: where in the book does that show? Find the page or scene. This is the evidence move.",
                "Move to motivation: 'why did the character do X in chapter Y?' The motivation is in the situation plus what the character is like; find the evidence in the surrounding pages",
                "Move to change: 'how is the character at the end different from at the beginning?' Find an early scene and a late scene; compare",
                "Practice the language of evidence: 'on page X' or 'in the chapter where Y happens' or 'when the character says Z'",
                "Compare two characters in one story (Wilbur and Templeton; Lucy and Edmund) on trait, motivation, change",
                "Distinguish what the text says from what the reader assumed: 'where in the book does it actually say that?'; if the answer is 'it doesn't, I just thought so', name the assumption and look again",
            ],
            "socratic_questions": [
                "What is this character like? Give me three words.",
                "For each word, where in the book does that show?",
                "Why did the character do that specific thing in chapter Y? What in the story makes that make sense?",
                "How is the character at the end of the book different from at the beginning? What changed them?",
                "You said the character was kind. Where does that show? Read me the sentence.",
                "You said the character was bad. Does the book actually say that, or have you decided that yourself? Is there evidence for both sides?",
            ],
            "practice_activities": [
                "Character profile card: pick a character from the current book; on a card, name three traits with one piece of text evidence for each",
                "Two-character comparison: pick two characters in one story; draw a two-column chart with traits, motivations, and arcs for each; note where they overlap and where they differ",
                "Why-did-they-do-that exercise: pick one decision a character made and walk through the motivations using the text",
                "Beginning-and-end snapshot: pick a character; describe them in three sentences at the beginning of the book and three sentences at the end; compare",
                "Find-the-evidence game: parent makes a claim about a character ('I think Wilbur is humble'); child finds the page that supports or challenges the claim",
            ],
            "real_world_connections": [
                "Talking about characters in family read-alouds at dinner ('Why did she say that to him?')",
                "Discussing characters in movies and shows with the same evidence discipline ('Where does it show that the character changed?')",
                "Recognizing similar character types across many stories (the loyal friend, the wise teacher, the trickster)",
                "Talking about real people (in biographies, in family stories) with the same vocabulary of traits, motivations, and arcs",
            ],
            "common_misconceptions": [
                "Confusing what the child has imagined or assumed about a character with what the text actually says. The evidence move is the antidote.",
                "Treating character traits as a static label. A character can be brave AND afraid; the both-at-once is what makes characters real.",
                "Skipping motivation and going straight to judgment ('she was mean'). The why is the harder, richer question.",
                "Believing a character must change to be a good character. Some characters in some stories do not change, and that's part of the story; the absence of change is itself worth noticing.",
                "Treating the parent's reading of a character as the right answer. Multiple readings of a character can be valid as long as each is grounded in the text.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Names three or more traits for a chosen character with specific text evidence for each",
                "Articulates the motivation for at least one significant character decision, with evidence",
                "Describes how a character changes across the story with a clear beginning and end snapshot",
                "Compares two characters within or across stories on trait, motivation, and arc",
                "Distinguishes evidence-grounded claims from assumptions and revises when the evidence challenges the claim",
            ],
            "proficiency_indicators": [
                "Names traits and one or two pieces of evidence",
                "Can describe character change at a general level",
            ],
            "developing_indicators": [
                "Names what the character did, but cannot articulate traits",
                "Cannot cite evidence for claims about the character",
            ],
            "assessment_methods": [
                "character profile card with text evidence",
                "two-character comparison chart",
                "oral discussion with the parent on a chapter book the child has read",
                "find-the-evidence challenge on parent-made claims",
            ],
            "sample_assessment_prompts": [
                "Tell me three things about [character] and where in the book each one shows.",
                "Why did [character] do [specific thing] in [chapter / scene]? What in the book made that make sense?",
                "How is [character] at the end of the book different from at the beginning?",
                "Compare [character A] and [character B]. How are they alike? How are they different?",
                "I think [character] is [trait]. Do you agree? Where does the book support or challenge that?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is a 'character trait'?",
                "expected_type": "multiple_choice",
                "options": [
                    "What the character does in one scene.",
                    "A general thing that is true about who the character is.",
                    "The character's name.",
                    "What the character looks like.",
                ],
                "correct_answer": "A general thing that is true about who the character is.",
                "hints": [
                    "Think of words like brave, kind, curious, stubborn, lonely.",
                ],
                "explanation": (
                    "A character trait is a general thing about who the character is, not just what they did in one "
                    "scene. Brave, kind, curious, stubborn, lonely are all traits."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "When you claim a character is 'brave', what should you do next?",
                "expected_type": "multiple_choice",
                "options": [
                    "Just trust your feeling.",
                    "Find a specific scene in the book where the character was brave; that scene is the evidence.",
                    "Ask someone else if they agree.",
                    "Read the book again from the beginning.",
                ],
                "correct_answer": "Find a specific scene in the book where the character was brave; that scene is the evidence.",
                "hints": [
                    "Character analysis at this band requires evidence from the text.",
                ],
                "explanation": (
                    "The discipline of character analysis is to support every claim with specific text evidence. 'I "
                    "think Wilbur is brave because on page X he...' is the form. The scene is the evidence."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is the difference between a character trait and a character motivation?",
                "expected_type": "multiple_choice",
                "options": [
                    "They are the same thing.",
                    "A trait is what the character is like in general; a motivation is WHY the character did one specific thing.",
                    "A trait is good; a motivation is bad.",
                    "A trait is in the book; a motivation is what you imagine.",
                ],
                "correct_answer": "A trait is what the character is like in general; a motivation is WHY the character did one specific thing.",
                "hints": [
                    "Trait is general (kind); motivation is specific (she helped him because she remembered being lost herself).",
                ],
                "explanation": (
                    "A trait answers 'what is this character like?' and a motivation answers 'why did this character do "
                    "this thing?' Both come from the text; both call for evidence."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "Pick a character from a chapter book you have read. In one paragraph, tell me: three traits, with "
                    "evidence; one motivation, with evidence; and one way the character changed across the book."
                ),
                "expected_type": "text",
                "hints": [
                    "Three traits, each with a page or scene where it shows.",
                    "One motivation: a specific decision the character made, and why.",
                    "One change: who the character was at the start vs at the end.",
                ],
                "explanation": (
                    "A complete character analysis at this band has: traits (with evidence), motivation (for a specific "
                    "decision, with evidence), and arc (the change from start to end). The paragraph reads like: 'X is "
                    "[trait] because in [scene] she [act]. X is also [trait] and [trait]. When she did [specific thing] "
                    "she did it because [motivation grounded in story]. At the start of the book she was [snapshot], by "
                    "the end she had [become / learned / lost...].'"
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "You and your sister are reading the same book. You think the character is brave. Your sister thinks "
                    "the character is reckless. Can you both be right? What should you do with this disagreement?"
                ),
                "expected_type": "text",
                "hints": [
                    "Both views may be grounded in different scenes from the text.",
                    "A real reader-discussion welcomes both readings if both are evidence-grounded.",
                ],
                "explanation": (
                    "Both can be right. The character may be brave in one scene and reckless in another; many real "
                    "characters are both. The honest discussion compares the scenes each reader is drawing from, "
                    "rather than insisting on one reading. This is how real literary conversation works."
                ),
            },
        ],
        "assessment_items": [
            {
                "prompt": "Tell me three traits of [character] from your chapter book. For each trait, name a scene that shows it.",
                "type": "open_response",
                "target_concept": "character_trait_with_evidence",
                "rubric": (
                    "Mastery: three distinct traits with specific scene-level evidence for each. Proficient: two traits "
                    "with evidence, or three with general evidence. Developing: traits named without evidence or actions "
                    "named as traits."
                ),
            },
            {
                "prompt": "Why did [character] do [specific significant act] in the book? Walk me through the motivation.",
                "type": "open_response",
                "target_concept": "character_motivation_with_evidence",
                "rubric": (
                    "Mastery: motivation grounded in character traits and story situation, with evidence. Proficient: "
                    "motivation named but not fully grounded. Developing: cannot articulate motivation."
                ),
            },
            {
                "prompt": "How is [character] at the end of the book different from at the beginning? Give me a snapshot of each.",
                "type": "open_response",
                "target_concept": "character_arc",
                "rubric": (
                    "Mastery: clear beginning snapshot, clear end snapshot, named change. Proficient: rough snapshots, "
                    "general change. Developing: cannot describe change or insists there is none without considering."
                ),
            },
            {
                "prompt": "Compare [character A] and [character B] in this book. How are they alike? How are they different?",
                "type": "open_response",
                "target_concept": "character_comparison",
                "rubric": (
                    "Mastery: alike-and-different across trait, motivation, and arc with evidence. Proficient: alike-and-"
                    "different at trait level. Developing: cannot compare or compares only on what they did."
                ),
            },
        ],
        "resource_guidance": {
            "required": [
                "a chapter book with characters worth thinking about (Charlotte's Web, The Lion the Witch and the Wardrobe, Mrs. Frisby and the Rats of NIMH, Roald Dahl, Sarah Plain and Tall, The Penderwicks, anything with characters who change)",
                "a character profile card template (three trait boxes with evidence space; one motivation box; one change box)",
                "a two-character comparison chart template",
            ],
            "recommended": [
                "a wide variety of characters across reading: villains, sidekicks, mentors, tricksters",
                "biographies (real people analyzed with the same vocabulary)",
                "discussion partner: a parent, sibling, or friend who has read the same book and will discuss it as a real reader",
            ],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 20, "assessment": 20},
        "accommodations": {
            "dyslexia": (
                "Build character analysis on listened books (read-alouds, audiobooks). The skill is interpretive, not "
                "decoding. The child can give rich character analysis on books they cannot yet read alone."
            ),
            "adhd": (
                "Use short character cards rather than long written analyses. Quick verbal back-and-forth with the parent "
                "is often more productive than written work at this band. Choose chapters with action-driven character "
                "moments so the evidence is vivid."
            ),
            "gifted": (
                "Move to more complex characters with mixed motives (Edmund in Narnia, Templeton in Charlotte's Web, "
                "Snape later). Introduce the idea that great characters resist simple labels. Begin the conversation "
                "about character archetypes (the trickster, the mentor, the foil) lightly."
            ),
            "visual_learner": "Use the character profile card with sketches alongside trait words. Visual maps of character relationships help.",
            "kinesthetic_learner": "Act out a scene to feel the character's motivation. Role-play a character interview ('if I were the character, why did I do X?').",
            "auditory_learner": "Discuss character traits aloud with a real reader (parent, sibling, friend who has read the book). The conversation IS the practice.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": (
                    "Today we move from naming characters to analyzing them. We will describe what characters are like "
                    "(traits), why they do what they do (motivations), and how they change across the story (arc). The "
                    "central discipline is citing specific evidence from the text for every claim."
                ),
                "gradual_release": {
                    "i_do": (
                        "The parent picks a character from a shared book and models the analysis aloud: 'I think Wilbur "
                        "is humble because on page 47 he says he doesn't deserve all this attention. He is also fearful "
                        "(see chapter 4 when Charlotte first speaks to him) and grateful (see how he treats Charlotte "
                        "throughout). When he does X he does it because Y. At the start of the book he was Z; by the "
                        "end he had become...'"
                    ),
                    "we_do": (
                        "Parent and child build a character profile card together for a second character, taking turns "
                        "proposing a trait and finding evidence."
                    ),
                    "you_do": (
                        "Child builds a character profile card for a third character independently, then shares with the "
                        "parent in conversation."
                    ),
                },
                "guided_practice": [
                    "Character profile card for one character per finished book",
                    "Two-character comparison chart at the end of each book",
                    "Find-the-evidence challenge: parent makes a claim, child finds the page",
                ],
                "independent_practice": [
                    "Daily character noticing during chapter book reading: keep a small character notebook",
                    "Across a term, build a portrait of how characters change across multiple books",
                ],
                "mastery_check": [
                    "Names traits, motivations, and arc for a character with text evidence",
                    "Compares characters within and across books",
                    "Distinguishes evidence-grounded claims from assumptions",
                ],
                "spiral_review": [
                    "Re-analyze a character from an earlier book; notice what the child can see now that they could not see then",
                ],
            },
            "classical": {
                "narrative_introduction": (
                    "Character is at the heart of every great story. The Greeks gave us the names of the moral types; "
                    "the Romans wrote lives that taught by their characters; the Christian and medieval traditions told "
                    "the saints' lives and the romance heroes. To analyze a character is to take up a long, deep human "
                    "habit: noticing what kind of person this is, why they do what they do, and how they grow."
                ),
                "memory_work": {
                    "chants": [
                        "Recite the three character questions: what is the character like (trait), why did they do that (motivation), how did they change (arc)",
                        "Recite the evidence rule: every claim about a character is backed by a specific scene or line from the book",
                    ],
                    "recitations": [
                        "Memorize a passage that shows a character's essential quality (Charlotte's spider-web messages; Lucy's first words in Narnia; the moment a hero shows themselves)",
                    ],
                },
                "copywork": [
                    "Copy one passage that reveals a character's essence into the copybook; the language of revelation is held in the hand",
                ],
                "recitation_routine": (
                    "At the close of each chapter book, the child gives a brief oral character analysis: trait, "
                    "motivation, arc, with evidence. The analyses across the term form the child's own running gallery "
                    "of characters they have met."
                ),
                "history_integration": (
                    "Plutarch's Lives and the biographies of great figures in history are the classical ground of "
                    "character analysis. Apply the same vocabulary of trait, motivation, and arc to real people in the "
                    "history sequence."
                ),
                "read_aloud_suggestions": [
                    "Chapter books with characters worthy of analysis: Charlotte's Web, The Lion the Witch and the Wardrobe, Mrs. Frisby, The Wind in the Willows, Little House series, A Wrinkle in Time",
                    "Age-appropriate biographies and lives: D'Aulaire, Genevieve Foster, Jean Fritz",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "Living chapter books with rich characters: Charlotte's Web, The Wind in the Willows, Wind in the Door, the Little House series, anything by Beverly Cleary, Roald Dahl, Madeleine L'Engle",
                    "Living biographies: D'Aulaire's, Genevieve Foster, Jean Fritz, James Daugherty",
                ],
                "short_lesson_flow": (
                    "After a chapter or at the end of a book, sit together and talk about a character as real readers "
                    "do. The parent asks one question (what is this character like? what is this character's most "
                    "important moment?) and listens. The child's noticings are honored; the evidence move is invited "
                    "gently ('where in the book does that show?')."
                ),
                "narration_prompt": (
                    "Tell me about [character]. What is the character like? Why did they do [specific thing]? How are "
                    "they different at the end of the book?"
                ),
                "real_world_objects": [
                    "The chapter book or biography in hand, ready to flip to specific pages",
                    "A character notebook the child keeps with one page per character they have met across the term",
                    "A discussion partner (parent, sibling, friend) who reads the same books",
                ],
                "nature_connection": (
                    "Notice how nature observation also calls for evidence-grounded claims: 'the cardinal returns to "
                    "the feeder each morning' rests on the same habit as 'Wilbur is grateful'; both rest on what has "
                    "actually been seen or read"
                ),
                "habit_focus": (
                    "The habit of careful noticing grounded in evidence. The character is what the text shows; the "
                    "reader is the one who notices and is honest about what they see."
                ),
            },
            "montessori": {
                "prepared_materials": [
                    "Character profile cards as a template the child uses with each finished book",
                    "A character library the child keeps: one card per character with traits, motivations, and arc, growing across the term",
                    "Two-character comparison charts as a separate template",
                    "A 'find the evidence' card set: parent-made claims about characters from books the child has read",
                ],
                "presentation": {
                    "three_period_lesson": (
                        "This is a character trait: a general thing about who the character is. This is a motivation: "
                        "why the character did one specific thing. This is an arc: how the character changed across "
                        "the story. Show me a trait, a motivation, and an arc for this character; for this one; for "
                        "this one. The three are introduced slowly across many days; the third period is only when the "
                        "distinction is sure."
                    ),
                    "steps": [
                        "The guide presents one term at a time across a few days (trait, then motivation, then arc)",
                        "The child fills out a character profile card for a chosen character",
                        "Across the term the child's character library grows; the child returns to old cards and "
                        "deepens them as they re-read or remember more",
                        "The child compares characters across books they have read",
                    ],
                },
                "control_of_error": (
                    "The text itself is the control: the child returns to the book to confirm or correct a claim. The "
                    "adult does not correct; the text does."
                ),
                "abstraction_pathway": (
                    "From naming what the character did, to naming what the character is like with evidence, to "
                    "articulating motivations and arcs, toward seeing characters as full constructed persons whose "
                    "traits, motivations, and growth can be read with attention and discussed with respect"
                ),
                "extensions": [
                    "Build a character map of relationships across a book (lines between characters showing affection, opposition, change)",
                    "Compare characters across books that share a theme (the orphan child, the loyal friend, the wise teacher)",
                    "Apply the character vocabulary to a real person in a biography",
                ],
                "observation_focus": (
                    "Watch for the child reaching for evidence on their own when making a character claim, for the "
                    "character library growing organically, and for the child's spontaneous comparison of characters "
                    "across books they have read."
                ),
            },
            "unschooling": {
                "invitations": [
                    "Talk about characters in books, movies, and shows at dinner the way real readers talk about characters they love",
                    "Welcome the child's strong opinions about characters and probe gently for evidence",
                    "Read books with great characters together and discuss them as real readers (not as a lesson)",
                ],
                "real_world_contexts": [
                    "Dinner conversation about a chapter book read at bedtime",
                    "Family movie nights followed by character discussion",
                    "Talking about real people in a biography or family story with the same vocabulary",
                    "Discussing characters in shared books with friends or cousins",
                ],
                "conversation_starters": [
                    "What did you think of [character] in your book? Are they brave or reckless?",
                    "Why do you think [character] did that? What in the story makes that make sense?",
                    "Has [character] changed since the beginning? How?",
                    "Who do you like better, [A] or [B]? Why?",
                ],
                "resource_bank": [
                    "A varied library of books with rich characters",
                    "A discussion partner: parent, older sibling, grandparent, friend",
                    "Audiobooks for shared listening that enables family character discussion",
                ],
                "parent_role": (
                    "Be a real reader-conversation partner. Welcome the child's readings of characters and ask, "
                    "gently, where in the book the evidence is. Notice across months whether the child reaches for "
                    "evidence on their own."
                ),
                "observation_documentation": (
                    "Across a term, note the characters the child has analyzed, the depth of their readings, the "
                    "discussions that have happened, and the moments when the child has changed their reading of a "
                    "character based on evidence. This noticing replaces any test."
                ),
            },
        },
        "connections": {
            "math": "The discipline of citing evidence for a claim is the same as the math habit of showing the work that supports an answer",
            "science": "Evidence-grounded claims about characters parallel evidence-grounded claims about natural phenomena; both rest on what was actually observed or read",
            "history": "Character analysis applied to real historical figures is one of the central history-and-biography reading skills",
            "writing": "Knowing how characters work in published stories prepares the child to write their own characters with traits, motivations, and arcs",
        },
    },
    "rd-07": {
        "enriched": True,
        "learning_objectives": [
            "Identify the setting of a story: where and when it takes place, and the relevant details (weather, season, era, social context)",
            "Explain how setting influences events and characters: a story set on a frozen island in winter is shaped by that fact",
            "Map the plot structure of a story: exposition, rising action, climax, falling action, resolution (with age-appropriate vocabulary)",
            "Identify the central PROBLEM (or conflict) the story raises and how it is resolved (or left unresolved)",
            "Compare two stories on how each uses setting to shape its plot",
        ],
        "teaching_guidance": {
            "introduction": (
                "Foundational reading let the child enjoy the story's events without naming the underlying structure. "
                "Developing-level setting-and-plot work makes the structure visible. The child names WHERE and WHEN the "
                "story happens, sees how the setting shapes what can happen (Sarah Plain and Tall could not happen in a "
                "city; Charlotte's Web could not happen in a desert), and traces the plot's curve from the situation at "
                "the start (exposition), through the building tension (rising action), to the turning point (climax), "
                "and through the falling action to the resolution. The vocabulary (exposition, climax, resolution) is "
                "introduced at age but used precisely: these are real terms that will serve the child through all of "
                "literary study."
            ),
            "scaffolding_sequence": [
                "Begin with setting alone: pick a story the child knows well. Ask: where does this story happen? When does it happen? What is the place like?",
                "Move to setting-influences-plot: ask 'could this story happen anywhere else? What if it were set in a city instead of a farm?' The child sees that setting is not just backdrop",
                "Introduce the plot vocabulary slowly: exposition (the situation at the beginning), rising action (events that build tension), climax (the turning point), falling action (what happens after the climax), resolution (how things settle)",
                "Use a plot-mountain diagram (a triangle shape) and place the major events of a known story on it",
                "Identify the central problem (or conflict): every story poses a problem (person vs person, person vs nature, person vs self, person vs society) and resolves it (or leaves it open)",
                "Apply to a second story; then a third; the vocabulary settles in through repeated use across books",
                "Compare two stories with different settings: how does each setting shape what is possible in the story?",
                "Move to noticing setting and plot during first reading, not just after: 'we are in the rising action now; the tension is building'",
            ],
            "socratic_questions": [
                "Where and when does this story happen? What details show it?",
                "Could this story happen in a different setting? What would change?",
                "What is the main problem in this story? Who is involved in the problem?",
                "Where on the plot mountain are we right now in the book?",
                "What was the turning point of the story? What changed at that moment?",
                "How does the story end? Is the problem fully resolved, partly resolved, or left open?",
            ],
            "practice_activities": [
                "Plot mountain for a finished chapter book: draw the triangle, place the major events on it, label exposition / rising action / climax / falling action / resolution",
                "Setting analysis card: for a chosen book, describe place, time, weather, season, era, social context; then describe how each of these shapes the story",
                "Setting-swap thought experiment: pick a beloved story and imagine it in a different setting; what changes? What stays the same?",
                "Conflict naming: for several books, name the central conflict by type (person vs person, person vs nature, person vs self, person vs society)",
                "Two-book comparison: pick two books with very different settings; chart how each setting shapes its plot",
            ],
            "real_world_connections": [
                "Recognizing setting in movies and shows: where and when does this take place? How does that shape the story?",
                "Recognizing plot structure in family stories told at the table: where is the rising action, the turning point?",
                "Noticing how a setting changes a real-life story: a road trip story and a stay-at-home story differ in what can happen",
                "Discussing news stories with the same vocabulary of conflict (person vs nature in a hurricane story; person vs society in a civil-rights story)",
            ],
            "common_misconceptions": [
                "Treating setting as decoration. Setting shapes what is possible in the story; a good author does not pick the setting arbitrarily.",
                "Thinking the climax is the most exciting scene. Climax is the TURNING POINT, where the story shifts from rising action to falling action; the most exciting and the turning are often the same but not always.",
                "Believing every story must have a clean five-part plot mountain. Many fine stories blend, restart, or refuse the shape; the plot mountain is a useful map, not a requirement.",
                "Naming conflict only as person vs person. The four classical conflict types (person vs person, person vs nature, person vs self, person vs society) are the starter vocabulary; some stories involve more than one.",
                "Insisting the resolution must be happy or clean. Resolution means HOW the problem ends; it can be sad, ambiguous, or open.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Names the setting of a story with specific details (place, time, era, season, social context)",
                "Explains how setting shapes the events or characters of the story with a specific example",
                "Maps the plot of a finished story on a plot mountain with major events placed correctly",
                "Identifies the central conflict by type (person vs person / nature / self / society)",
                "Compares two stories on how each setting shapes its plot",
            ],
            "proficiency_indicators": [
                "Names setting at place-and-time level with some detail",
                "Maps plot with most events in correct order; one or two structural labels confused",
            ],
            "developing_indicators": [
                "Names setting only as 'where it happens'; misses time and detail",
                "Cannot place events on a plot structure; lists events without structure",
            ],
            "assessment_methods": [
                "plot mountain diagram for a finished book",
                "setting analysis card",
                "two-book setting comparison",
                "oral discussion of plot structure during chapter reading",
            ],
            "sample_assessment_prompts": [
                "Draw a plot mountain for the book you just finished. Label the parts and place the major events.",
                "Tell me about the setting of this story. Where, when, and what details matter?",
                "How does the setting shape the story? What couldn't happen if the setting were different?",
                "What is the central conflict in this story, and what type is it?",
                "Compare the setting of [book A] and [book B]. How does each setting shape its story differently?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is the 'setting' of a story?",
                "expected_type": "multiple_choice",
                "options": [
                    "The main character.",
                    "Where and when the story takes place, with the details that matter.",
                    "The author's name.",
                    "How long the book is.",
                ],
                "correct_answer": "Where and when the story takes place, with the details that matter.",
                "hints": [
                    "Think place, time, and the world the story is set in.",
                ],
                "explanation": (
                    "Setting is where and when a story takes place, plus the details that matter (weather, era, social "
                    "context). It is not just the background; it shapes what can happen."
                ),
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is the 'climax' of a story?",
                "expected_type": "multiple_choice",
                "options": [
                    "The very last sentence of the book.",
                    "The turning point of the story, where things shift from building tension to settling toward an ending.",
                    "The funniest scene.",
                    "The first time the main character appears.",
                ],
                "correct_answer": "The turning point of the story, where things shift from building tension to settling toward an ending.",
                "hints": [
                    "Climax is the turning point on the plot mountain.",
                ],
                "explanation": (
                    "The climax is the turning point: the moment where the story stops building tension and starts moving "
                    "toward its resolution. It is often the most exciting scene, but the key feature is the TURN, not the "
                    "excitement."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "Charlotte's Web is set on a farm. Could the same story happen if it were set in a city apartment? "
                    "Why or why not?"
                ),
                "expected_type": "text",
                "hints": [
                    "What couldn't happen in an apartment? Why does the farm setting matter?",
                ],
                "explanation": (
                    "Charlotte's Web could not happen in a city apartment. The barn animals, the freedom Wilbur has to "
                    "explore, the County Fair plot, the rhythms of farm seasons are all woven into what makes the story "
                    "possible. The farm is not background; it is what allows the story."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "What are the four classical types of conflict in stories?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "Person vs person, person vs nature, person vs self, person vs society.",
                    "Beginning, middle, end, epilogue.",
                    "Hero, villain, mentor, sidekick.",
                    "Past, present, future, dream.",
                ],
                "correct_answer": "Person vs person, person vs nature, person vs self, person vs society.",
                "hints": [
                    "Conflict types: who or what is the main character struggling with?",
                ],
                "explanation": (
                    "The four classical conflict types are person vs person, person vs nature, person vs self, person vs "
                    "society. Many stories involve more than one; the strongest stories often have a person-vs-self "
                    "thread under the surface conflict."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "Draw a plot mountain (or describe it in words) for a chapter book you have read. Label the five "
                    "parts and place at least one major event in each."
                ),
                "expected_type": "text",
                "hints": [
                    "Exposition (the situation at the start), rising action (events building tension), climax (the "
                    "turning point), falling action (what happens after), resolution (how it settles).",
                ],
                "explanation": (
                    "A complete plot mountain has: exposition (who and where at the start, before the problem is in full "
                    "force); rising action (events that build the tension toward the turning point); climax (the turn); "
                    "falling action (what unfolds because of the turn); resolution (how the problem ends). Each part "
                    "has at least one major event from the book."
                ),
            },
        ],
        "assessment_items": [
            {
                "prompt": "Tell me about the setting of [book the child has just finished]: place, time, era, and the details that matter.",
                "type": "open_response",
                "target_concept": "setting_with_details",
                "rubric": (
                    "Mastery: place, time, era, and at least two relevant details. Proficient: place and time. "
                    "Developing: just place."
                ),
            },
            {
                "prompt": "How does the setting shape this story? What couldn't happen if the setting were different?",
                "type": "open_response",
                "target_concept": "setting_shapes_plot",
                "rubric": (
                    "Mastery: specific example of how setting enables a specific event or character choice. Proficient: "
                    "general statement that setting matters. Developing: cannot articulate."
                ),
            },
            {
                "prompt": "Draw a plot mountain for the book. Place the major events on it and label each part.",
                "type": "open_response",
                "target_concept": "plot_mountain_mapping",
                "rubric": (
                    "Mastery: five parts labeled correctly, major events placed accurately. Proficient: most parts "
                    "labeled, events mostly in order. Developing: cannot use the plot mountain structure."
                ),
            },
            {
                "prompt": "What is the central conflict in this story? What type is it? Are there any other conflicts running alongside?",
                "type": "open_response",
                "target_concept": "conflict_identification_and_type",
                "rubric": (
                    "Mastery: central conflict named correctly with type; secondary conflict noticed. Proficient: central "
                    "conflict named and typed. Developing: cannot articulate conflict."
                ),
            },
        ],
        "resource_guidance": {
            "required": [
                "a chapter book or short novel the child has finished and can think back through",
                "a plot mountain template (a printable triangle with the five labels)",
                "a setting analysis card template",
            ],
            "recommended": [
                "a pair of books with strikingly different settings for comparison work (Sarah Plain and Tall vs The Tale of Despereaux; Charlotte's Web vs Stuart Little)",
                "movies and shows for parallel setting-and-plot conversation outside reading time",
                "a story notebook where the child collects plot mountains across the year",
            ],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 20, "assessment": 20},
        "accommodations": {
            "dyslexia": (
                "Work with read-aloud books and audiobooks. The plot-and-setting work is interpretive, not decoding. "
                "The child can give rich analysis of stories they cannot yet read alone."
            ),
            "adhd": (
                "Use the plot mountain as a visible artifact rather than long verbal discussion. Drawing on a big sheet "
                "of paper with markers engages the kinesthetic channel."
            ),
            "gifted": (
                "Introduce more sophisticated plot structures: nested stories, dual timelines, in medias res openings. "
                "Discuss how some great books deliberately resist the simple plot mountain."
            ),
            "visual_learner": (
                "The plot mountain is itself a visual tool. Add color and event illustrations to the mountain."
            ),
            "kinesthetic_learner": (
                "Act out the climax of a story. Walk a real plot mountain on the floor (chalked outline) with major "
                "events posted along it."
            ),
            "auditory_learner": "Discuss plot and setting aloud with a real reader who has read the same book.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": (
                    "Today we name the structure that lives inside every story. Setting is where and when, with the "
                    "details that matter. Plot is the curve from the start situation, through rising tension, to the "
                    "turning point, and on to the resolution. The vocabulary (exposition, rising action, climax, "
                    "falling action, resolution) is the same vocabulary the child will use through all of literary "
                    "study; we introduce it now precisely."
                ),
                "gradual_release": {
                    "i_do": (
                        "The parent draws a plot mountain on a sheet of paper. Names each part. Walks through a story "
                        "they both know, placing the major events on the mountain with the parts labeled."
                    ),
                    "we_do": (
                        "Parent and child build a plot mountain together for a recently finished book. Take turns "
                        "proposing events; agree where on the mountain each event sits."
                    ),
                    "you_do": (
                        "Child builds a plot mountain independently for a next book; reads it back to the parent."
                    ),
                },
                "guided_practice": [
                    "Plot mountain for each finished chapter book",
                    "Setting analysis card for each finished book",
                    "Two-book setting comparison once a term",
                ],
                "independent_practice": [
                    "Keep a story-structure notebook with plot mountains across the year",
                    "Notice setting and plot during first reading: 'we are in the rising action now'",
                ],
                "mastery_check": [
                    "Names setting with details and explains how it shapes the story",
                    "Builds a complete plot mountain with major events placed correctly",
                    "Identifies central conflict by type",
                ],
                "spiral_review": [
                    "Re-map a plot mountain for an early-term book; notice what the child sees now that they did not see then",
                ],
            },
            "classical": {
                "narrative_introduction": (
                    "Aristotle named the parts of plot in his Poetics: the beginning, the middle, the end, and the "
                    "turning that joins them. Twenty-three centuries later we still teach his shape, because it is the "
                    "honest shape of how stories work. To learn it is to enter a tradition of careful naming that runs "
                    "through every later literary study."
                ),
                "memory_work": {
                    "chants": [
                        "Recite the five parts of plot: exposition, rising action, climax, falling action, resolution",
                        "Recite the four conflict types: person vs person, person vs nature, person vs self, person vs society",
                        "Recite the setting questions: where, when, and what details matter",
                    ],
                    "recitations": [
                        "Memorize one passage that opens a story (the exposition) and one passage that resolves it (the resolution) from a beloved book; the beginnings and endings of great stories are worth keeping",
                    ],
                },
                "copywork": [
                    "Copy one well-formed opening sentence and one well-formed closing sentence from a finished book; the shape of stories lives in their first and last words",
                ],
                "recitation_routine": (
                    "At the close of each chapter book, the child recites the plot mountain aloud and names the central "
                    "conflict; across the term the child's repertoire of story structures grows."
                ),
                "history_integration": (
                    "The great myths and the great histories all have plot structure: name the rising action in the "
                    "Iliad, the turning in Odyssey, the resolution in Aeneid (in age-appropriate retellings). The "
                    "vocabulary serves the entire chronological spine."
                ),
                "read_aloud_suggestions": [
                    "Books with strong plot structure for analysis: Charlotte's Web, The Lion the Witch and the Wardrobe, Sarah Plain and Tall, The Boxcar Children, The Tale of Despereaux",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "Living chapter books with clear plot and rich setting: Charlotte's Web, The Wind in the Willows, Sarah Plain and Tall, The Boxcar Children, The Tale of Despereaux",
                    "Living biographies for parallel work on plot of a real life",
                ],
                "short_lesson_flow": (
                    "After a chapter book is finished, sit together and trace the plot in conversation. The parent asks "
                    "one or two structural questions ('where do you think the story turned?'); the child answers in "
                    "their own words; the parent listens and asks for the evidence."
                ),
                "narration_prompt": (
                    "Tell me about the setting and the plot of [book]. Where and when does it happen? What is the central "
                    "problem? How does the story turn and how does it end?"
                ),
                "real_world_objects": [
                    "A simple plot mountain drawn on a notebook page",
                    "The book itself, ready to flip to specific scenes",
                    "A story notebook where the child collects plot maps across the year",
                ],
                "nature_connection": (
                    "Setting in books often mirrors real settings the child knows: notice how a real meadow or a real "
                    "winter day matches the setting of a book"
                ),
                "habit_focus": (
                    "The habit of seeing the shape of a thing: a story has a shape, and the careful reader notices it"
                ),
            },
            "montessori": {
                "prepared_materials": [
                    "A plot mountain template laminated for repeated use with dry-erase markers",
                    "A setting analysis card template",
                    "Event cards from a known story that the child arranges on the plot mountain",
                    "A two-book comparison chart template",
                ],
                "presentation": {
                    "three_period_lesson": (
                        "This is the exposition; this is the rising action; this is the climax; this is the falling "
                        "action; this is the resolution. Show me the climax of this story; show me the exposition. What "
                        "part of the plot is this event from?"
                    ),
                    "steps": [
                        "The guide presents one plot term at a time across several days",
                        "The child arranges event cards from a known story on the plot mountain",
                        "The child builds a plot mountain for a chosen book independently",
                        "Across the term the child's gallery of plot mountains grows",
                    ],
                },
                "control_of_error": (
                    "The book itself is the control: the child can flip to a scene and check whether their placement on "
                    "the plot mountain holds up. The adult does not correct; the text does."
                ),
                "abstraction_pathway": (
                    "From naming events in order, to placing events on a plot mountain, to noticing the plot mountain "
                    "during first reading, toward seeing the shape of a story without needing the template"
                ),
                "extensions": [
                    "Compare plot mountains across books in the same genre",
                    "Notice how some great books resist the simple plot mountain (cyclic plots, frame stories, nested stories)",
                    "Apply the plot mountain to a real life (a biography, a family story)",
                ],
                "observation_focus": (
                    "Watch for the child noticing plot structure during reading, not just after; for the spontaneous use "
                    "of the vocabulary (climax, rising action); and for the recognition of conflict type across books"
                ),
            },
            "unschooling": {
                "invitations": [
                    "Talk about story structure in books and movies the family enjoys together",
                    "Leave a few story-structure books on the shelf (How to Read Literature Like a Professor for Kids, etc.) for casual browsing",
                    "Welcome the child's own plot-mountain drawings without making them assigned work",
                ],
                "real_world_contexts": [
                    "Discussing the plot of a family movie at dinner",
                    "Noticing the plot of a real story (a family adventure, a news event)",
                    "Talking about the setting of a book the family is reading aloud and how it shapes what can happen",
                ],
                "conversation_starters": [
                    "Where do you think the story turned in your book?",
                    "Could this story happen if it were set somewhere else?",
                    "What is the main problem in the story? Does it get solved?",
                ],
                "resource_bank": [
                    "A varied library of books with strong plots and rich settings",
                    "Discussion partners (parent, sibling, friends) who read the same books",
                    "Story-structure picture books and reference books left available",
                ],
                "parent_role": (
                    "Talk about plot and setting the way real readers talk about the books they love. Welcome the child's "
                    "noticings. Notice across months whether the child reaches for the vocabulary on their own."
                ),
                "observation_documentation": (
                    "Across a term, note how the child has come to see and describe the structure of stories. Plot "
                    "vocabulary appearing in casual conversation is the real sign of mastery."
                ),
            },
        },
        "connections": {
            "math": "The plot mountain is a graphical structure; mapping events onto its shape is a literary version of the line-graph skill in math",
            "science": "Setting in stories parallels environment in science: both shape what is possible in the system",
            "history": "Historical fiction's settings are real historical settings; learning to read setting carefully supports the history sequence",
            "writing": "Knowing the plot mountain is the precondition for writing one's own structured stories with clear turning points",
        },
    },
    "rd-08": {
        "enriched": True,
        "learning_objectives": [
            "Identify cause-and-effect relationships in both fiction and nonfiction texts: this happened, and BECAUSE OF THAT, this followed",
            "Recognize signal words and phrases that mark cause and effect: because, so, therefore, as a result, due to, consequently, since",
            "Distinguish a cause-and-effect relationship from a sequence: 'A happened, then B happened' is sequence; 'A happened, and BECAUSE OF A, B happened' is cause and effect",
            "Trace a chain of causes and effects through a story or explanatory passage",
            "Apply the same skill in nonfiction (history, science): name the cause of an event and trace its effects",
        ],
        "teaching_guidance": {
            "introduction": (
                "Cause and effect is the logical glue that makes stories and explanations cohere. In a story, the "
                "character's choices have consequences; in a science passage, the conditions produce the result; in a "
                "history passage, the situation gives rise to the event. The skill at this band is twofold: recognize "
                "the SIGNAL WORDS that mark cause-and-effect relationships, and distinguish cause-and-effect from "
                "simple sequence (A happened then B happened, vs A happened and BECAUSE OF A, B happened). The signal "
                "words because, so, therefore, since, as a result, consequently, due to are the workhorse vocabulary; "
                "the child learns to notice them in reading and to use them in their own talking and writing."
            ),
            "scaffolding_sequence": [
                "Start with everyday cause-and-effect: 'I went outside without a coat, SO I got cold.' Notice the signal word.",
                "Introduce the signal words explicitly: because, so, therefore, as a result, since, due to, consequently. Make a wall chart.",
                "Find signal words in a real text. Read a paragraph; circle every signal word; notice what came before and what came after each one.",
                "Distinguish cause-effect from sequence with a clear contrast: 'I ate breakfast, then I went to school' (sequence) vs 'I ate breakfast, SO I had energy for school' (cause and effect).",
                "Trace a single cause-and-effect in a story: 'Wilbur was scared he would be killed; BECAUSE of that, Charlotte made a plan to save him.' The because is the engine of plot.",
                "Build a cause-and-effect chain: in a longer passage, one effect becomes the cause of the next thing. Draw it as a chain of arrows.",
                "Apply the same skill to nonfiction: 'The Pilgrims came to North America BECAUSE they wanted religious freedom; AS A RESULT, they founded a colony in Plymouth.' Cause-effect is how history is told.",
                "Apply to science: 'The water was heated to 100C; AS A RESULT, it boiled.' Cause-effect is how science is explained.",
            ],
            "socratic_questions": [
                "Did A cause B, or did A just happen before B?",
                "What signal word would you use to connect these two events?",
                "Why did the character do that? What caused that decision?",
                "Trace it back: what caused the cause? Can you go one more step back?",
                "Trace it forward: what did this effect cause next?",
                "If A had not happened, would B still have happened? (This is a cause check.)",
            ],
            "practice_activities": [
                "Signal-word hunt: in a chosen paragraph, circle every signal word the child finds; for each, draw an arrow from cause to effect",
                "Cause-and-effect chain: in a story, pick a major event and trace the chain back and forward (what caused this? what did it cause? what did that cause?)",
                "Sequence-vs-cause sort: parent gives sentences; child sorts each as 'sequence only' or 'cause and effect'",
                "Why-because game: parent makes a statement ('the character got lost in the woods'); child must explain WHY, using a signal word",
                "Apply across subjects: name a cause-and-effect from yesterday's history reading; name one from yesterday's science reading; name one from the chapter book",
            ],
            "real_world_connections": [
                "Naming the cause and effect in family decisions: 'we left early SO we wouldn't hit traffic'",
                "Tracing the consequences of choices in everyday life",
                "Recognizing the signal words in news headlines and articles",
                "Tracing the chain of causes in a real-world event the family discusses",
                "Applying the skill to the child's own behavior: 'I didn't sleep enough last night, AS A RESULT I'm tired today'",
            ],
            "common_misconceptions": [
                "Confusing sequence with cause-and-effect. Sequence is order; cause-and-effect is causation. Two events can be in sequence without one causing the other.",
                "Assuming every signal word marks cause-and-effect. 'Since' can mean 'because' OR 'from the time that'; 'so' can mean 'therefore' OR 'very' ('so cold!'). Context is key.",
                "Treating cause-and-effect as a single link. Many real causes are chains, and one effect can have multiple causes.",
                "Stopping at the first cause. Asking 'what caused the cause?' opens up depth.",
                "Believing cause-and-effect lives only in nonfiction. Fiction runs on it: every plot is a chain of causes and effects.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Identifies cause-and-effect relationships in unfamiliar texts (fiction and nonfiction) using signal words",
                "Distinguishes cause-and-effect from sequence in mixed sentences",
                "Traces a chain of three or more cause-and-effect links in a story or explanation",
                "Uses cause-and-effect signal words correctly in their own talking and writing",
                "Applies the skill across subjects: literature, history, science",
            ],
            "proficiency_indicators": [
                "Recognizes cause-and-effect in clearly-signaled passages",
                "Uses 'because' and 'so' in own talking; other signal words still emerging",
            ],
            "developing_indicators": [
                "Confuses sequence with cause-and-effect",
                "Cannot identify a cause-and-effect link without prompting",
            ],
            "assessment_methods": [
                "signal-word identification in a chosen passage",
                "sequence-vs-cause-and-effect sort",
                "cause-and-effect chain diagram for a major story event",
                "cross-subject application: name cause-and-effect from history, science, and literature in the same week",
            ],
            "sample_assessment_prompts": [
                "Read this paragraph. Circle every signal word for cause-and-effect.",
                "For each sentence, tell me whether it shows sequence only or cause-and-effect.",
                "Take this event from the book and trace it back: what caused it? What caused that?",
                "Tell me one cause-and-effect from your history reading this week.",
                "Use 'as a result' in your own sentence about today.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is the difference between 'sequence' and 'cause and effect'?",
                "expected_type": "multiple_choice",
                "options": [
                    "They are the same thing.",
                    "Sequence is the order things happened; cause and effect is when one thing makes another thing happen.",
                    "Sequence is in fiction; cause and effect is in nonfiction.",
                    "Sequence is short; cause and effect is long.",
                ],
                "correct_answer": "Sequence is the order things happened; cause and effect is when one thing makes another thing happen.",
                "hints": [
                    "Sequence is A then B. Cause and effect is A so B (because of A).",
                ],
                "explanation": (
                    "Sequence is the order things happened: A, then B. Cause and effect is causal: A happened, and BECAUSE "
                    "OF A, B followed. The two often look similar but are different."
                ),
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which of these is a cause-and-effect signal word?",
                "expected_type": "multiple_choice",
                "options": [
                    "Tomorrow.",
                    "Because.",
                    "Maybe.",
                    "Quickly.",
                ],
                "correct_answer": "Because.",
                "hints": [
                    "Signal words for cause-and-effect: because, so, therefore, as a result, since, due to, consequently.",
                ],
                "explanation": (
                    "'Because' is the most common signal word for cause-and-effect. Others include so, therefore, as a "
                    "result, since (when it means 'because'), due to, and consequently."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "Read these two sentences: 'I ate breakfast, then I went to school.' 'I ate breakfast, so I had energy "
                    "for school.' Which one shows cause-and-effect?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "The first sentence (I ate breakfast, then I went to school).",
                    "The second sentence (I ate breakfast, so I had energy for school).",
                    "Both equally.",
                    "Neither.",
                ],
                "correct_answer": "The second sentence (I ate breakfast, so I had energy for school).",
                "hints": [
                    "Look for the signal word 'so'.",
                    "The first sentence is just sequence (one event then another); the second sentence shows that eating CAUSED having energy.",
                ],
                "explanation": (
                    "The first sentence is sequence: A then B. The second sentence has 'so', which signals that eating "
                    "breakfast CAUSED having energy. The 'so' makes it cause-and-effect."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "In Charlotte's Web, Wilbur is scared he will be killed for bacon. Charlotte decides to save him. She "
                    "writes 'SOME PIG' in her web. The townspeople come to see the miracle pig. Wilbur becomes famous and "
                    "is saved. Trace one cause-and-effect link in this chain."
                ),
                "expected_type": "text",
                "hints": [
                    "Pick any two consecutive events and connect them with a signal word.",
                    "For example: 'Charlotte wrote SOME PIG in her web, AS A RESULT the townspeople came to see Wilbur.'",
                ],
                "explanation": (
                    "Each event in the chain causes the next: Wilbur was scared he would be killed BECAUSE he was going "
                    "to be slaughtered. AS A RESULT Charlotte decided to save him. SO she wrote SOME PIG in her web. "
                    "BECAUSE of the words in the web, the townspeople came. AS A RESULT Wilbur became famous. THEREFORE "
                    "he was saved. Every link is a cause-and-effect."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "Cause-and-effect is everywhere in real life and in real subjects. Name one cause-and-effect from "
                    "yesterday's chapter book reading, one from yesterday's history reading, and one from yesterday's "
                    "science reading. Use a different signal word for each."
                ),
                "expected_type": "text",
                "hints": [
                    "Pick three different sources and three different signal words.",
                ],
                "explanation": (
                    "Cause-and-effect is the engine of stories, histories, and science explanations alike. A typical "
                    "answer might be: 'In my chapter book, the character ran away BECAUSE her parents wouldn't listen. "
                    "In history, the colonists protested THEREFORE the king made it worse. In science, the cup got cold "
                    "AS A RESULT of being in the freezer.' Three subjects, three signal words, three real cause-and-"
                    "effects."
                ),
            },
        ],
        "assessment_items": [
            {
                "prompt": "Read this paragraph and identify every cause-and-effect signal word. For each, draw an arrow from cause to effect.",
                "type": "open_response",
                "target_concept": "signal_word_identification",
                "rubric": (
                    "Mastery: identifies all cause-and-effect signal words with arrows correctly drawn. Proficient: "
                    "identifies most. Developing: identifies sequence words as cause-and-effect or misses signals."
                ),
            },
            {
                "prompt": "Sort these sentences: which show sequence only, and which show cause-and-effect?",
                "type": "open_response",
                "target_concept": "sequence_vs_cause_distinction",
                "rubric": (
                    "Mastery: sorts correctly with reasons. Proficient: sorts correctly without reasons. Developing: "
                    "sorts incorrectly or confuses the categories."
                ),
            },
            {
                "prompt": "Trace a cause-and-effect chain through a major event in the book you are reading. At least three links.",
                "type": "open_response",
                "target_concept": "cause_effect_chain_tracing",
                "rubric": (
                    "Mastery: three or more links with signal words connecting each. Proficient: two-link chain. "
                    "Developing: cannot trace a chain."
                ),
            },
            {
                "prompt": "Name one cause-and-effect from each of literature, history, and science this week.",
                "type": "open_response",
                "target_concept": "cross_subject_application",
                "rubric": (
                    "Mastery: three different subjects, three different signal words, three real cause-and-effect "
                    "relationships. Proficient: three subjects with similar signal words. Developing: cannot apply "
                    "across subjects."
                ),
            },
        ],
        "resource_guidance": {
            "required": [
                "a wall chart or reference card with the signal words (because, so, therefore, as a result, since, due to, consequently)",
                "a chapter book and a nonfiction reading the child is currently working with",
                "a signal-word hunt template (a paragraph with space for circling)",
            ],
            "recommended": [
                "a cause-and-effect chain template (boxes connected by labeled arrows)",
                "news articles for cause-and-effect practice in real-world writing",
                "a chosen science or history reading with strong cause-and-effect structure",
            ],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 15},
        "accommodations": {
            "dyslexia": "Begin with oral cause-and-effect work (real-life examples, family conversations). The skill is logical, not decoding-dependent. Move to written work as fluency permits.",
            "adhd": "Use the signal-word chart and physical arrow-drawing rather than long discussion. Quick verbal back-and-forth ('what caused that? what did THAT cause?') keeps engagement.",
            "gifted": "Move to multi-causal events (events with several causes). Introduce the idea that history and science often involve chains of causes rather than single causes. Begin to notice when cause-and-effect arguments are weak or contested.",
            "visual_learner": "Use chain-of-arrows diagrams. Color-code causes and effects.",
            "kinesthetic_learner": "Physical sort: print sentences on cards, sort into 'sequence' and 'cause-and-effect' piles. Walk through a cause-and-effect chain by stepping from event to event on the floor.",
            "auditory_learner": "Discuss cause-and-effect aloud with a real partner. Listening for signal words in family conversation is a real practice.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": (
                    "Today we learn to recognize cause-and-effect, the logical glue of stories and explanations. We "
                    "learn the signal words (because, so, therefore, as a result, since, due to, consequently) and "
                    "practice distinguishing cause-and-effect from sequence. The skill applies across reading, history, "
                    "and science."
                ),
                "gradual_release": {
                    "i_do": "Parent reads a paragraph aloud and points out the signal words; explains the cause-effect link each one marks.",
                    "we_do": "Together with the child, hunt for signal words in a second paragraph and discuss the links.",
                    "you_do": "Child works through a third paragraph independently, identifying signals and tracing links.",
                },
                "guided_practice": [
                    "Signal-word hunt in a chosen paragraph",
                    "Sequence-vs-cause sort with parent-prepared sentence cards",
                    "Cause-and-effect chain for one major event in the current book",
                ],
                "independent_practice": [
                    "Daily noticing: name one cause-and-effect from today's reading across subjects",
                    "Apply the signal words in writing: use 'because' or 'as a result' in a written narration",
                ],
                "mastery_check": [
                    "Identifies cause-and-effect in unfamiliar texts using signal words",
                    "Distinguishes cause-and-effect from sequence",
                    "Traces a multi-link chain",
                ],
                "spiral_review": [
                    "Return to earlier readings and find cause-and-effect that was missed on first reading",
                ],
            },
            "classical": {
                "narrative_introduction": (
                    "Cause-and-effect is the logical structure of all explanation. Aristotle named the four causes; the "
                    "medieval logicians refined them; modern history and science still rest on the same habit of asking "
                    "WHY. To learn cause-and-effect is to take up the central question of every careful reader: not "
                    "just what happened, but WHY."
                ),
                "memory_work": {
                    "chants": [
                        "Recite the signal words: because, so, therefore, as a result, since, due to, consequently",
                        "Recite the question: not just what happened, but why? what caused this? what did this cause?",
                    ],
                    "recitations": [
                        "Memorize one well-formed cause-and-effect sentence from each week's reading; the language of causation lives in the ear",
                    ],
                },
                "copywork": [
                    "Copy one well-formed cause-and-effect sentence per week into the copybook; the signal words and the structure live in the hand",
                ],
                "recitation_routine": "After each reading, the child names one cause-and-effect aloud, using a signal word.",
                "history_integration": "History is the chronicle of cause-and-effect: the king did this AS A RESULT of that; the war broke out BECAUSE of these tensions. Apply the vocabulary to history daily.",
                "read_aloud_suggestions": [
                    "Real history (D'Aulaire, Foster, Fritz) and real science writing where causes and effects are clearly chained",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "Living books across the subjects where cause-and-effect is the logical structure of the writing",
                    "Aesop's fables, where every story turns on a cause-and-effect lesson",
                ],
                "short_lesson_flow": "After a reading, the parent asks a 'why?' or 'what caused that?' question. The child answers with a signal word. The conversation is brief and real.",
                "narration_prompt": "What happened in the reading, and why did it happen? Use 'because' or 'as a result' in your telling.",
                "real_world_objects": [
                    "The signal-word chart on the wall of the reading area",
                    "A small notebook where the child notes one cause-and-effect per day across subjects",
                ],
                "nature_connection": "Cause-and-effect in nature observation: 'the leaves changed color BECAUSE of the cold'; 'the bird returned to the feeder AS A RESULT of the warm afternoon'. The signal words apply to real observation as much as to texts.",
                "habit_focus": "The habit of asking why. The careful reader and the careful observer both ask not just what but why.",
            },
            "montessori": {
                "prepared_materials": [
                    "Signal-word cards: a card for each signal word with example sentences on the back",
                    "Sentence-sort cards: sentences printed individually for sorting into sequence and cause-and-effect piles",
                    "Cause-and-effect chain templates the child can fill in for stories and explanations",
                ],
                "presentation": {
                    "three_period_lesson": "This is a cause-and-effect sentence; this is a sequence-only sentence. Show me a cause-and-effect; show me a sequence. Is this one cause-and-effect or sequence?",
                    "steps": [
                        "The guide presents the signal-word cards and reads examples aloud",
                        "The child sorts sentence cards into sequence and cause-and-effect piles",
                        "The child traces a cause-and-effect chain for an event in a chosen story",
                        "Across the term, the child notices cause-and-effect spontaneously during reading",
                    ],
                },
                "control_of_error": "The signal-word cards are the control: a sentence sorted into 'cause-and-effect' should contain a signal word or imply causation; if it doesn't, the child can move it.",
                "abstraction_pathway": "From sorting concrete sentence cards, to identifying cause-and-effect in unfamiliar passages, toward writing one's own cause-and-effect explanations across subjects.",
                "extensions": [
                    "Notice cause-and-effect in nature observation",
                    "Apply cause-and-effect to history and science readings",
                    "Begin to notice multi-causal events (more than one cause for an effect)",
                ],
                "observation_focus": "Watch for the child reaching for signal words in their own talking and writing across subjects.",
            },
            "unschooling": {
                "invitations": [
                    "Pose 'why' questions casually in family conversation: 'Why do you think she said that?' 'What do you think caused that?'",
                    "Welcome the child's cause-and-effect noticings without making them a lesson",
                    "Leave a few interesting cause-and-effect-themed books available (Rube Goldberg machines, science of dominoes, history of events)",
                ],
                "real_world_contexts": [
                    "Discussing why something happened in a family decision, a news story, or a personal experience",
                    "Naming the consequences of choices in real life",
                    "Talking about cause-and-effect in shows and movies",
                ],
                "conversation_starters": [
                    "Why do you think that happened?",
                    "What do you think caused that?",
                    "What do you think the result will be?",
                    "If we hadn't done that, what would have happened?",
                ],
                "resource_bank": [
                    "Books and shows that explore cause-and-effect at every level",
                    "Real-world conversation about why things happen",
                    "A discussion partner who welcomes 'why' questions",
                ],
                "parent_role": "Be a curious 'why' asker yourself. Model cause-and-effect thinking in your own talk. Welcome the child's own questions.",
                "observation_documentation": "Across a term, note when the child reaches for signal words spontaneously in their own talking and writing. This is the real sign of internalization.",
            },
        },
        "connections": {
            "math": "Cause-and-effect in word problems: the SAME signal words mark mathematical relationships ('she had 10 apples and gave 3 away, AS A RESULT she had 7 left')",
            "science": "Cause-and-effect is the logical structure of all scientific explanation: condition X causes result Y",
            "history": "History is the chronicle of cause-and-effect; the central skill of history-reading is identifying causes and tracing effects",
            "writing": "Using cause-and-effect signal words in writing makes the writing logical and connected; this is the precondition for expository writing",
        },
    },
    "rd-09": {
        "enriched": True,
        "learning_objectives": [
            "Compare and contrast two texts on a shared topic or by the same author, identifying both similarities and differences",
            "Use a Venn diagram or a two-column comparison chart as the visual tool for comparison",
            "Compare across dimensions: theme, setting, characters, point of view, style, conclusion",
            "Compare a fiction and a nonfiction text on the same topic, noticing how genre shapes the treatment",
            "Move beyond surface comparison ('they both have a dog') to substantive comparison ('they both treat loyalty as the central virtue, but one tests it through danger and the other through patience')",
        ],
        "teaching_guidance": {
            "introduction": (
                "Comparing texts is the move from reading one book to reading books in conversation. The child puts two "
                "books side by side and notices what they share and where they differ. The skill grows in two ways: the "
                "child learns the visual tools (Venn diagram, two-column chart) that hold comparison clearly, and the "
                "child learns to compare across DIMENSIONS rather than at a single point. Theme, setting, characters, "
                "point of view, style, conclusion: each is a dimension along which two texts can be compared. The best "
                "comparisons move past 'both have X' to 'both treat Y, but in different ways'. This is the entry to all "
                "of comparative literary reading."
            ),
            "scaffolding_sequence": [
                "Start with two clearly similar texts: two picture-book retellings of the same fairy tale; two books on the same animal; two books by the same author",
                "Use a Venn diagram (two overlapping circles): one circle for unique-to-book-A, one for unique-to-book-B, the overlap for what they share",
                "Fill in the diagram together: surface items first (both have a girl named Cinderella; only one has fairy godmother) then deeper items (both treat goodness as rewarded; the older version's reward is different from the newer version's)",
                "Move to a two-column comparison chart: each row is a DIMENSION (theme, setting, characters, point of view, style, conclusion); each column is one book; fill in the cells",
                "Practice the comparison sentence form: 'Both books X. But book A Y, while book B Z.' This sentence structure carries substantive comparison.",
                "Compare a fiction and a nonfiction text on the same topic: a novel about a hurricane and a science book about hurricanes; notice how genre shapes treatment",
                "Compare two books by the same author: how is the author's style consistent? Where does it differ?",
                "Move toward author-level comparison: two authors writing about the same theme; how does each take it on?",
            ],
            "socratic_questions": [
                "What do these two books have in common? Start with one obvious thing, then go deeper.",
                "Where do these two books differ? What does each book do that the other doesn't?",
                "How do they treat the same theme differently?",
                "If you had to recommend one of these to a friend who liked the other, what would you say?",
                "Why might an author choose to write about the same topic as another author? What does each one add?",
                "Can a fiction and a nonfiction book on the same topic both be 'true'? What kind of truth does each offer?",
            ],
            "practice_activities": [
                "Venn diagram of two fairy-tale retellings: one classical version, one modern retelling",
                "Two-column chart of two books by the same author: dimensions in rows, books in columns, child fills in cells",
                "Fiction-and-nonfiction pairing: pick a topic the child loves (whales, knights, volcanoes, dogs); read a fiction book and a nonfiction book on the topic; compare them",
                "Comparison sentence drill: parent provides two books the child has read; child writes three comparison sentences using the 'Both books X. But A Y, while B Z' form",
                "Same-theme-different-authors pair: pick a theme (friendship, courage, loss); find two books that treat it differently; compare",
            ],
            "real_world_connections": [
                "Comparing movie adaptations of the same book ('the book and the movie both show X, but the book Y while the movie Z')",
                "Comparing two news sources on the same event",
                "Comparing two recipes for the same dish (a grandparent's recipe vs a cookbook's recipe)",
                "Comparing two field guides on the same plant or animal",
                "Discussing two retellings of a family story told by different relatives",
            ],
            "common_misconceptions": [
                "Stopping at the surface ('both have a dog'). Surface comparisons are the warm-up; substantive comparison happens at the level of theme, treatment, or stance.",
                "Forcing every comparison into the same number of similarities and differences. Some comparisons have many similarities and few differences, or vice versa; the comparison should follow the texts.",
                "Treating comparison as a contest ('which one is better?'). Comparison is not ranking; it is noticing.",
                "Believing two books on the same topic must say the same things. Different authors with different purposes can produce very different books on the same topic; the comparison shows the difference.",
                "Skipping fiction-nonfiction pairs because they 'aren't the same kind'. Fiction and nonfiction on the same topic make for some of the richest comparisons.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Builds a complete Venn diagram or two-column chart comparing two books across multiple dimensions",
                "Writes comparison sentences in the 'Both X, but A Y while B Z' form with substantive content",
                "Notices similarities and differences beyond the surface level",
                "Compares a fiction and a nonfiction text on the same topic, noting how genre shapes treatment",
                "Can compare two authors or two stylistic approaches",
            ],
            "proficiency_indicators": [
                "Fills in a Venn diagram at the surface level reliably",
                "Comparison sentences are correct but stay at one level",
            ],
            "developing_indicators": [
                "Names what each book is about but cannot articulate a comparison",
                "Confuses comparison with judgment ('this one is better')",
            ],
            "assessment_methods": [
                "Venn diagram of two books",
                "two-column comparison chart across dimensions",
                "comparison sentence-writing in 'Both X, but A Y while B Z' form",
                "fiction-and-nonfiction pairing analysis on a chosen topic",
            ],
            "sample_assessment_prompts": [
                "Build a Venn diagram for these two books. What do they share? What is unique to each?",
                "Fill in this two-column chart. The rows are theme, setting, characters, point of view, conclusion.",
                "Write three comparison sentences about these two books using the 'Both X, but A Y while B Z' form.",
                "Compare this fiction book and this nonfiction book on the same topic. How does the genre change what each book does?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is a Venn diagram, and how is it used for comparing texts?",
                "expected_type": "multiple_choice",
                "options": [
                    "A list of all the events in one book.",
                    "Two overlapping circles where unique-to-A goes in one, unique-to-B in the other, and shared things go in the overlap.",
                    "A drawing of the main character.",
                    "A plot mountain.",
                ],
                "correct_answer": "Two overlapping circles where unique-to-A goes in one, unique-to-B in the other, and shared things go in the overlap.",
                "hints": [
                    "Visual tool: two circles that overlap in the middle.",
                ],
                "explanation": (
                    "A Venn diagram is two overlapping circles. Things unique to book A go in A's circle; things unique "
                    "to book B go in B's; things they share go in the overlap. It is the simplest visual tool for "
                    "comparison."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "Which comparison is more substantive: 'Both books have a dog' OR 'Both books treat loyalty as the "
                    "central virtue, but one tests it through danger and the other through patience'?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "The first one (both books have a dog).",
                    "The second one (both treat loyalty, in different ways).",
                    "They are equally substantive.",
                    "Neither is a real comparison.",
                ],
                "correct_answer": "The second one (both treat loyalty, in different ways).",
                "hints": [
                    "Surface comparison vs deep comparison.",
                ],
                "explanation": (
                    "The second comparison is substantive: it identifies a shared THEME (loyalty) and names the DIFFERENT "
                    "TREATMENT (danger vs patience). The first is a surface observation. Both have a place, but the "
                    "substantive comparison is the goal at this band."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "What are some DIMENSIONS along which you can compare two books?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "Theme, setting, characters, point of view, style, conclusion.",
                    "Color of the cover, number of pages, year published, price.",
                    "Just plot.",
                    "Comparison is not by dimension.",
                ],
                "correct_answer": "Theme, setting, characters, point of view, style, conclusion.",
                "hints": [
                    "Substantive dimensions, not surface ones.",
                ],
                "explanation": (
                    "The dimensions of comparison include theme, setting, characters, point of view, style, and "
                    "conclusion. Cover color and price are surface; theme and treatment are substantive."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "Write a comparison sentence about two books you have read, in the form: 'Both books X. But book A "
                    "Y, while book B Z.'"
                ),
                "expected_type": "text",
                "hints": [
                    "Name something both books share (theme or topic), then name how each treats it differently.",
                ],
                "explanation": (
                    "A strong comparison sentence might read: 'Both Charlotte's Web and The Tale of Despereaux treat "
                    "courage as the central virtue. But Charlotte's Web shows courage as quiet, patient, planning "
                    "ahead, while The Tale of Despereaux shows courage as a small mouse facing dangers larger than "
                    "himself.' Shared theme; different treatment; named specifically."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "You are comparing a fiction book about whales (a novel where a whale is a character) with a "
                    "nonfiction book about whales (an informational book). How does the genre change what each book "
                    "can do?"
                ),
                "expected_type": "text",
                "hints": [
                    "What does fiction add that nonfiction can't? What does nonfiction add that fiction shouldn't?",
                ],
                "explanation": (
                    "Fiction can give a whale interiority, motivation, a relationship with humans; the truth fiction "
                    "offers is about feeling and meaning. Nonfiction can give accurate facts about whale biology, "
                    "behavior, migration, conservation; the truth nonfiction offers is about reality. Both are valuable; "
                    "neither is a substitute for the other."
                ),
            },
        ],
        "assessment_items": [
            {
                "prompt": "Build a Venn diagram comparing two books the child has recently read. Fill in unique-to-A, unique-to-B, and shared.",
                "type": "open_response",
                "target_concept": "venn_diagram_comparison",
                "rubric": (
                    "Mastery: at least three items in each section, with substantive items in the overlap (theme, "
                    "treatment, not just surface). Proficient: items in each section at the surface level. Developing: "
                    "diagram incomplete or items confused."
                ),
            },
            {
                "prompt": "Fill in a two-column comparison chart. Rows: theme, setting, characters, point of view, conclusion. Columns: book A, book B.",
                "type": "open_response",
                "target_concept": "multi_dimension_comparison",
                "rubric": (
                    "Mastery: all five rows filled in for both books with specific content. Proficient: most rows "
                    "filled in. Developing: chart incomplete or general."
                ),
            },
            {
                "prompt": "Write three comparison sentences in the 'Both X, but A Y while B Z' form about two books you have read.",
                "type": "open_response",
                "target_concept": "comparison_sentence_writing",
                "rubric": (
                    "Mastery: three substantive comparison sentences with shared element and named different treatments. "
                    "Proficient: three sentences at the surface level. Developing: cannot produce three sentences in "
                    "the form."
                ),
            },
            {
                "prompt": "Compare this fiction and this nonfiction book on the same topic. How does the genre change what each book can do?",
                "type": "open_response",
                "target_concept": "fiction_nonfiction_pairing",
                "rubric": (
                    "Mastery: substantive comparison identifying what each genre adds and what each cannot do. "
                    "Proficient: surface-level comparison. Developing: cannot articulate genre difference."
                ),
            },
        ],
        "resource_guidance": {
            "required": [
                "two finished books for the comparison (same topic, same author, or same theme)",
                "a Venn diagram template (two overlapping circles)",
                "a two-column comparison chart template",
            ],
            "recommended": [
                "fairy-tale retellings: a classical version and a modern retelling (Cinderella, Snow White, Little Red Riding Hood)",
                "fiction-nonfiction pairs on the child's favorite topics (whales, knights, dragons, volcanoes, dogs)",
                "two books by the same author (Beverly Cleary, Roald Dahl, Kate DiCamillo, E. B. White)",
            ],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 20, "assessment": 20},
        "accommodations": {
            "dyslexia": "Use audiobooks for one or both books to remove decoding load. Comparison is an interpretive skill that lives at the level of meaning, not decoding.",
            "adhd": "Use the Venn diagram on a large sheet of paper as a visible artifact. Fill it in over multiple short sessions rather than one long one.",
            "gifted": "Compare three books at once instead of two. Compare across more sophisticated dimensions (style, voice, structure, the author's stance). Begin to compare authors rather than just books.",
            "visual_learner": "The Venn diagram and the two-column chart are themselves visual tools. Add color coding to highlight shared themes.",
            "kinesthetic_learner": "Sort comparison statements onto a large floor Venn diagram by stepping into each section.",
            "auditory_learner": "Discuss the comparison aloud with a real partner who has read both books.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": (
                    "Today we put two books side by side and notice what they share and where they differ. We use Venn "
                    "diagrams and two-column charts as the visual tools. We compare across dimensions (theme, setting, "
                    "characters, point of view, style, conclusion) and we move beyond surface comparison to substantive "
                    "comparison."
                ),
                "gradual_release": {
                    "i_do": "Parent builds a Venn diagram for two books, naming what is unique to each and what they share.",
                    "we_do": "Parent and child build a Venn diagram for a second pair, taking turns proposing items.",
                    "you_do": "Child builds a comparison chart for a third pair independently.",
                },
                "guided_practice": [
                    "Venn diagram of two books",
                    "Two-column chart across five dimensions",
                    "Comparison sentence writing in the 'Both X, but A Y while B Z' form",
                ],
                "independent_practice": [
                    "Compare each new chapter book to one already read",
                    "Build a comparison chart at the end of each pair",
                ],
                "mastery_check": [
                    "Substantive Venn diagram across two books",
                    "Multi-dimension comparison chart",
                    "Three substantive comparison sentences",
                ],
                "spiral_review": [
                    "Return to earlier comparisons; refine them with the deeper reading the child can now bring",
                ],
            },
            "classical": {
                "narrative_introduction": (
                    "Comparison is one of the oldest acts of reading. The Greeks compared their heroes; Plutarch's Lives "
                    "explicitly paired one Greek with one Roman so the reader could compare. To compare two texts is to "
                    "enter a long tradition of reading books in conversation, not in isolation."
                ),
                "memory_work": {
                    "chants": [
                        "Recite the six dimensions of comparison: theme, setting, characters, point of view, style, conclusion",
                        "Recite the comparison sentence form: both X, but A Y, while B Z",
                    ],
                    "recitations": [
                        "Memorize one comparison sentence per week from the child's reading; the language of comparison lives in the ear",
                    ],
                },
                "copywork": [
                    "Copy one well-formed comparison sentence per week into the copybook; the structure of comparison lives in the hand",
                ],
                "recitation_routine": "At the end of each chapter book, the child compares it to one previously read book using the dimension vocabulary.",
                "history_integration": "Plutarch's Lives is the central classical model: parallel lives of Greek and Roman figures compared side by side. Apply the comparison vocabulary to history and biography.",
                "read_aloud_suggestions": [
                    "Pairs worth comparing: two retellings of a fairy tale, two books by the same author, two biographies of the same historical figure",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "Pairs of living books that compare richly: two by the same author, two on the same topic, two retellings of the same tale",
                ],
                "short_lesson_flow": "Lay two finished books side by side. Ask one good comparison question. The child answers in their own words; the parent listens and asks for the evidence in each book.",
                "narration_prompt": "Tell me what these two books share and where they differ. Take your time.",
                "real_world_objects": [
                    "Two finished books side by side on the reading table",
                    "A Venn diagram drawn on a notebook page",
                    "A comparison notebook kept across the term",
                ],
                "nature_connection": "Comparison in nature observation: two species of birds at the feeder; two leaves from different trees; two days of weather. The skill of comparison applies to the natural world as readily as to texts.",
                "habit_focus": "The habit of seeing books in conversation rather than in isolation.",
            },
            "montessori": {
                "prepared_materials": [
                    "Venn diagram template laminated for dry-erase use",
                    "Two-column chart template with dimension labels (theme, setting, characters, point of view, conclusion)",
                    "Pairs of books arranged for comparison work (same topic, same author, same theme pairs)",
                    "Comparison sentence cards modeling the 'Both X, but A Y while B Z' form",
                ],
                "presentation": {
                    "three_period_lesson": "This is what these books share; this is what is unique to A; this is what is unique to B. Show me a shared element; show me an A-only element; show me a B-only element.",
                    "steps": [
                        "The guide presents a pair of books and a blank Venn diagram",
                        "Child fills in the diagram freely, returning to the books for evidence",
                        "Child moves to the multi-dimension chart for a deeper comparison",
                        "Across the term the child develops a library of comparisons in their notebook",
                    ],
                },
                "control_of_error": "The books themselves are the control: a child returns to the books to confirm or refine each comparison item.",
                "abstraction_pathway": "From filling in surface items in a Venn diagram, to filling in substantive items, to writing comparison sentences without the diagram, toward seeing two books in conversation at the first reading.",
                "extensions": [
                    "Three-way comparisons of three books on a theme",
                    "Author comparisons: how does one author's stance differ from another's?",
                    "Fiction-and-nonfiction pairings as a regular practice",
                ],
                "observation_focus": "Watch for the child reaching for comparison spontaneously when reading two books in proximity.",
            },
            "unschooling": {
                "invitations": [
                    "Keep pairs of books visible: two retellings of a tale, two books on the child's favorite topic, two books by a favorite author",
                    "Welcome comparison talk at the table: 'I noticed both books had X' or 'these two books are different in Y way'",
                    "Make fiction-and-nonfiction pairs on the child's interest topics",
                ],
                "real_world_contexts": [
                    "Comparing a book and its movie adaptation",
                    "Comparing two grandparents' versions of a family story",
                    "Comparing two news sources on the same event",
                    "Comparing two recipes for the same dish",
                ],
                "conversation_starters": [
                    "What did these two books have in common?",
                    "What did each one do that the other didn't?",
                    "Which one did you prefer, and what made the difference?",
                    "If you had to pick one to recommend to a friend, which would it be and why?",
                ],
                "resource_bank": [
                    "Pairs of books on the child's interest topics",
                    "Movie adaptations of beloved books",
                    "A discussion partner who reads alongside",
                ],
                "parent_role": "Welcome the child's comparisons as real reader-conversation. Ask 'where in each book does that show?' to invite evidence-grounded comparison.",
                "observation_documentation": "Across a term, note the comparisons the child makes spontaneously in conversation. These are the real signs of internalized comparison habits.",
            },
        },
        "connections": {
            "math": "Comparison in mathematics (greater than, less than, equal to) shares the same logical move as comparison in reading: noticing where two things differ and where they share",
            "science": "Compare-and-contrast is a central scientific skill: two species, two specimens, two conditions, two results",
            "history": "Comparing two historical figures or two events is the central skill of historical reading; Plutarch's Lives is the classical model",
            "writing": "Writing a compare-and-contrast essay is the writing-strand application of this reading skill",
        },
    },
    "rd-10": {
        "enriched": True,
        "learning_objectives": [
            "Read and enjoy a variety of poetry forms: lyric, narrative, humorous, nature, free verse",
            "Identify rhyme scheme using letter notation (AABB, ABAB, ABCB, etc.)",
            "Identify rhythm and meter at the introductory level: where the beat lands, where the line speeds up or slows down",
            "Identify stanza structure: a stanza is to a poem what a paragraph is to prose; count the stanzas, notice the pattern",
            "Notice imagery and sound: what does the poem ask you to see, hear, smell, taste, touch? What sounds repeat?",
            "Memorize and recite a chosen poem with expression: poetry is meant to be heard, not just read on the page",
        ],
        "teaching_guidance": {
            "introduction": (
                "Foundational reading included poetry recitation (rf-17) and nursery rhymes (rf-18); poems were enjoyed "
                "as music. Developing poetry appreciation lifts the level of attention. The child still enjoys the music "
                "but also notices the structure: rhyme scheme, rhythm, stanza, imagery. They meet a wider variety of "
                "poetry forms (lyric, narrative, humorous, nature, free verse) and learn the vocabulary that names what "
                "they hear and see. The central practice remains MEMORIZATION AND RECITATION; poetry is heard, not just "
                "read. A child who has memorized two dozen poems by the end of the developing level has the music of "
                "the language in the ear."
            ),
            "scaffolding_sequence": [
                "Begin with poems the child already loves: nursery rhymes, A. A. Milne, Shel Silverstein, Jack Prelutsky, the rhyming picture books the child knows",
                "Introduce rhyme scheme as a notation: mark each rhyme with a letter ('cat' = A; 'hat' = A; 'tree' = B; 'me' = B → AABB). Practice on a known poem first.",
                "Move to other patterns: ABAB (alternating rhyme), ABCB (rhyming only lines 2 and 4), free verse (no rhyme), couplets (AABB...)",
                "Introduce rhythm by clapping the beat. Some lines are dum-da-dum-da (iambic); some are dum-da-da-dum-da-da (rolling); some have no fixed meter (free verse)",
                "Introduce stanza as the paragraph of poetry: count the stanzas, notice if they are equal or different in length",
                "Introduce imagery: 'what does this line ask you to see / hear / smell / taste / feel?' Mark the sense each line invokes",
                "Introduce sound devices lightly: alliteration (Peter Piper picked a peck of pickled peppers), onomatopoeia (buzz, crash, hiss)",
                "Tour the forms: read a lyric poem (a personal feeling poem), a narrative poem (a poem that tells a story), a humorous poem (Shel Silverstein, Ogden Nash), a nature poem (Frost, Mary Oliver at age), a free-verse poem (Carl Sandburg, Langston Hughes)",
                "Memorize one short poem and recite it with expression at the end of each week",
            ],
            "socratic_questions": [
                "How does the poem sound? Where does the beat land?",
                "What is the rhyme scheme? Mark it with letters.",
                "How many stanzas does the poem have? Are they the same length?",
                "What does the poem ask you to see or hear?",
                "What is the poem really about? (For a poem with figurative content, the topic and the subject may differ.)",
                "Why did the poet choose those specific words? What other words could have gone there?",
                "Recite the poem you memorized this week with expression. Where did your voice rise? Where did it pause?",
            ],
            "practice_activities": [
                "Rhyme-scheme marking: mark the rhyme scheme of a familiar poem in letters",
                "Stanza count: count the stanzas of a poem and notice the pattern",
                "Imagery walk: read a poem and circle every sensory image",
                "Memorize and recite: pick a short poem each week, memorize across the week, recite Friday with expression for the family",
                "Form tour: across a term, read at least one poem of each form (lyric, narrative, humorous, nature, free verse)",
                "Poem-of-the-day: a poem read aloud at breakfast or bedtime, with one quick noticing each day",
            ],
            "real_world_connections": [
                "Reciting memorized poems at family gatherings",
                "Recognizing song lyrics as poetry (every song lyric has rhyme scheme, rhythm, stanza)",
                "Writing greeting cards and birthday wishes in verse",
                "Listening to spoken-word poetry (age-appropriate) and audiobooks of poetry collections",
                "Noticing rhyme and rhythm in nursery rhymes recited to younger siblings",
            ],
            "common_misconceptions": [
                "Believing poetry must rhyme to be poetry. Free verse has no rhyme but is still poetry. Walt Whitman, Carl Sandburg, much of contemporary poetry is free verse.",
                "Treating rhythm and meter as a math problem. Rhythm is felt first in the ear; the letter notation is a tool for naming what is already heard.",
                "Reading a poem only once. Poems repay rereading; the second and third readings hear things the first reading missed.",
                "Reading a poem silently when the poem asks to be heard. Read aloud, even alone; the music is the point.",
                "Believing the poem is about its surface topic. A poem about a road might be about choice (Frost); a poem about a stopped horse might be about death (Frost); the subject can be one thing, the topic another. At this band the child notices the possibility without forcing every poem to have hidden depths.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Identifies rhyme scheme of an unfamiliar poem using letter notation",
                "Distinguishes stanzas and notices stanza pattern",
                "Identifies imagery in a poem and names the sense each invokes",
                "Recognizes major poetry forms (lyric, narrative, humorous, nature, free verse) and names which form a chosen poem belongs to",
                "Memorizes and recites at least one short poem each week with expression",
            ],
            "proficiency_indicators": [
                "Marks rhyme scheme on a familiar poem reliably",
                "Counts stanzas and recognizes imagery with prompting",
                "Memorizes a short poem with some support",
            ],
            "developing_indicators": [
                "Reads poems as if they were prose, with no attention to sound or structure",
                "Cannot distinguish a poem from prose at a glance",
            ],
            "assessment_methods": [
                "rhyme-scheme marking on an unfamiliar poem",
                "imagery walk on a chosen poem",
                "weekly memorized poem recitation with expression",
                "form identification: name the form of a chosen poem",
            ],
            "sample_assessment_prompts": [
                "Read this poem aloud. What is the rhyme scheme? Mark it with letters.",
                "How many stanzas does this poem have? Are they the same length?",
                "Circle every image in this poem. What sense does each invoke?",
                "What form is this poem (lyric, narrative, humorous, nature, free verse)?",
                "Recite the poem you memorized this week. Read it with expression.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Mark the rhyme scheme of this poem with letters: 'Roses are red, / Violets are blue, / Sugar is sweet, / And so are you.'",
                "expected_type": "text",
                "hints": [
                    "The end-words are red, blue, sweet, you. Which rhyme?",
                ],
                "explanation": (
                    "Red and sweet do not rhyme, so they are different letters. Blue and you rhyme. The rhyme scheme is "
                    "ABCB (line 1 = A, line 2 = B, line 3 = C, line 4 = B again because it rhymes with line 2)."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is a 'stanza'?",
                "expected_type": "multiple_choice",
                "options": [
                    "A single line of a poem.",
                    "A group of lines in a poem, like a paragraph in prose; usually separated from other stanzas by a blank line.",
                    "The first word of every line.",
                    "The rhyme at the end of a poem.",
                ],
                "correct_answer": "A group of lines in a poem, like a paragraph in prose; usually separated from other stanzas by a blank line.",
                "hints": [
                    "Think paragraph, but for poems.",
                ],
                "explanation": (
                    "A stanza is a group of lines in a poem, like a paragraph in prose. Stanzas are usually separated by "
                    "blank lines. Some poems have many short stanzas; others have a few long stanzas; some have only "
                    "one stanza."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "Does poetry have to rhyme?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "Yes, all poetry must rhyme.",
                    "No; free verse is poetry without rhyme. Many poets (Walt Whitman, Carl Sandburg, much contemporary poetry) write free verse.",
                    "Only nursery rhymes are real poetry.",
                    "Yes, if it doesn't rhyme it is prose.",
                ],
                "correct_answer": "No; free verse is poetry without rhyme. Many poets (Walt Whitman, Carl Sandburg, much contemporary poetry) write free verse.",
                "hints": [
                    "Free verse is poetry without fixed rhyme or meter.",
                ],
                "explanation": (
                    "Free verse is poetry without fixed rhyme or meter. It still has poetic qualities: imagery, sound, "
                    "rhythm shaped by line breaks rather than meter, attention to specific words. Whitman, Sandburg, "
                    "Langston Hughes, much of contemporary poetry is free verse."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "Read this Robert Frost line: 'Whose woods these are I think I know.' What images does it ask you "
                    "to see? What does the line sound like (rhythm)?"
                ),
                "expected_type": "text",
                "hints": [
                    "Images: think about what you can picture from these words.",
                    "Rhythm: clap the line. Where does the beat land?",
                ],
                "explanation": (
                    "The line asks you to picture woods (a forest, snowy in the full poem) and a speaker who might or "
                    "might not be trespassing. The rhythm is iambic tetrameter: da-DUM da-DUM da-DUM da-DUM (whose-WOODS "
                    "these-ARE I-THINK I-KNOW). The steady beat is part of the poem's contemplative feel."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "Pick a short poem you love (under 16 lines) and tell me: the rhyme scheme, the number of stanzas, "
                    "one image you remember, and what form the poem is (lyric, narrative, humorous, nature, free verse)."
                ),
                "expected_type": "text",
                "hints": [
                    "Apply each vocabulary item to a real poem.",
                ],
                "explanation": (
                    "Applying the vocabulary to a poem the child loves is the real practice. A complete answer names "
                    "the rhyme scheme (or notes the poem is free verse), counts the stanzas, identifies a specific "
                    "image, and names the form. This is what poetry appreciation at the developing band looks like."
                ),
            },
        ],
        "assessment_items": [
            {
                "prompt": "Read this unfamiliar poem aloud. Mark the rhyme scheme with letters.",
                "type": "open_response",
                "target_concept": "rhyme_scheme_identification",
                "rubric": (
                    "Mastery: correct letter notation for any common pattern (AABB, ABAB, ABCB, free verse). Proficient: "
                    "correct for simple patterns. Developing: cannot mark rhyme scheme."
                ),
            },
            {
                "prompt": "How many stanzas does this poem have? Are they the same length? What pattern do you notice?",
                "type": "open_response",
                "target_concept": "stanza_structure",
                "rubric": (
                    "Mastery: counts correctly, names pattern. Proficient: counts correctly. Developing: cannot identify "
                    "stanzas."
                ),
            },
            {
                "prompt": "Circle every image in this poem and tell me what sense each invokes.",
                "type": "open_response",
                "target_concept": "imagery_identification",
                "rubric": (
                    "Mastery: identifies most images and names sense for each. Proficient: identifies some images. "
                    "Developing: cannot identify images."
                ),
            },
            {
                "prompt": "Recite your memorized poem for me. Read it with expression and pause where the poem asks you to.",
                "type": "open_response",
                "target_concept": "memorized_recitation",
                "rubric": (
                    "Mastery: full poem from memory, confident expression, appropriate pauses. Proficient: full poem "
                    "with some prompting, basic expression. Developing: partial memorization or flat delivery."
                ),
            },
        ],
        "resource_guidance": {
            "required": [
                "a poetry collection or anthology at the child's level (A Child's Garden of Verses, When We Were Very Young, Where the Sidewalk Ends, A Light in the Attic, Oxford Book of Children's Verse)",
                "a recitation notebook where the child copies memorized poems",
                "a quiet recital space (a chair, a poetry corner, the family table at the right moment)",
            ],
            "recommended": [
                "audiobooks of poetry collections for modeling fluent expressive recitation",
                "an anthology that covers multiple forms (lyric, narrative, humorous, nature, free verse) for the form tour",
                "Robert Frost, Christina Rossetti, A. A. Milne, Robert Louis Stevenson, Shel Silverstein, Jack Prelutsky, Langston Hughes, Naomi Shihab Nye for variety",
            ],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 15},
        "accommodations": {
            "dyslexia": "Poetry is especially valuable for dyslexic readers because the short lines, repeated patterns, and oral tradition reward listening as much as reading. Memorize by hearing; recite by heart; the written form is the trace, not the source.",
            "adhd": "Short poems with clear rhythm hold attention better than long ones. Memorize in 2-line chunks across several days. Recite to a real audience as the motivation.",
            "gifted": "Move to more complex forms (sonnet, villanelle, sestina at the upper edge of the band). Introduce specific poets with depth (Frost in winter, Dickinson, Hughes, Oliver). Begin to discuss what poems are 'about' beyond their surface topic.",
            "visual_learner": "Mark rhyme scheme and stanza breaks visually on a printed copy. Color-code images by sense.",
            "kinesthetic_learner": "Clap the rhythm of a line. Walk a poem (a step per beat). Recite while walking or moving.",
            "auditory_learner": "Listen to poems read aloud (podcasts, audiobooks, recordings of poets reading their own work). Memorize by ear before reading on paper.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": (
                    "Today we move from enjoying poems as music to noticing how poems are made. We learn the vocabulary: "
                    "rhyme scheme, rhythm, stanza, imagery, form. We meet five forms (lyric, narrative, humorous, nature, "
                    "free verse). And we keep the central practice: memorize one short poem each week and recite it with "
                    "expression."
                ),
                "gradual_release": {
                    "i_do": "Parent reads a poem aloud, then explains the rhyme scheme, stanzas, imagery, and form.",
                    "we_do": "Together with the child, work through a second poem: mark rhyme scheme, count stanzas, find images.",
                    "you_do": "Child applies the vocabulary to a third poem independently and recites their memorized poem of the week.",
                },
                "guided_practice": [
                    "Rhyme-scheme marking on a poem each week",
                    "Imagery walk on a poem each week",
                    "Memorize-and-recite weekly",
                ],
                "independent_practice": [
                    "Read poetry daily for ten minutes",
                    "Across the term, read at least one poem of each major form",
                ],
                "mastery_check": [
                    "Marks rhyme scheme of unfamiliar poems",
                    "Identifies form of unfamiliar poems",
                    "Memorizes and recites a short poem each week",
                ],
                "spiral_review": [
                    "Re-recite earlier memorized poems each Friday cumulatively",
                ],
            },
            "classical": {
                "narrative_introduction": (
                    "Poetry is older than prose. The earliest stories were poems. The Iliad, the Odyssey, the Beowulf, "
                    "the Psalms: all poems, all memorized and recited for centuries before they were written down. To "
                    "learn poetry is to take up an ancient art that lives in the ear before it lives on the page."
                ),
                "memory_work": {
                    "chants": [
                        "Recite the elements of poetry: rhyme, rhythm, stanza, imagery, form",
                        "Recite the five forms: lyric (a feeling), narrative (a story), humorous (a laugh), nature (the natural world), free verse (no fixed meter or rhyme)",
                    ],
                    "recitations": [
                        "Memorize and recite a short poem each week, building a cumulative repertoire across the term",
                        "Build a recitation book the child reads from at family gatherings",
                    ],
                },
                "copywork": [
                    "Copy each memorized poem into the recitation notebook neatly, attending to its line breaks and punctuation",
                ],
                "recitation_routine": "Begin each lesson with the recitation of a poem from earlier weeks; add the new poem; the repertoire grows cumulatively.",
                "history_integration": "Poetry across the chronological spine: nursery rhymes (folk), Robert Louis Stevenson (Victorian), Frost (twentieth century), Hughes (Harlem Renaissance), contemporary poets at the upper edge.",
                "read_aloud_suggestions": [
                    "A daily poem at breakfast or bedtime, drawn from a real anthology",
                    "Classical and traditional poetry: Christina Rossetti, Robert Louis Stevenson, A. A. Milne, Robert Frost; modern poets at age",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A Child's Garden of Verses (Stevenson), When We Were Very Young (Milne), Now We Are Six (Milne), A Light in the Attic (Silverstein), Where the Sidewalk Ends (Silverstein), the Oxford Book of Children's Verse",
                ],
                "short_lesson_flow": (
                    "Read a poem aloud, slowly, twice. Talk about it briefly. The child memorizes one poem per week and "
                    "recites it Friday. The poem is enjoyed first; the analysis is light and serves the enjoyment, not "
                    "the other way around."
                ),
                "narration_prompt": "Tell me about the poem we just read. What did you see, hear, feel?",
                "real_world_objects": [
                    "A poetry anthology kept in the reading nook",
                    "A recitation notebook with the child's memorized poems copied in",
                    "A quiet recital chair or corner",
                ],
                "nature_connection": "Read nature poems outdoors during walks. Copy a favorite line into the nature notebook with a small drawing.",
                "habit_focus": "The habit of attention to language. Poetry rewards close attention; the child who attends to one poem well has practiced the habit that will serve all later literary reading.",
            },
            "montessori": {
                "prepared_materials": [
                    "A poetry shelf in the reading area with anthologies the child chooses freely",
                    "A recitation notebook the child manages as their own",
                    "Rhyme-scheme marking sheets and stanza-counting templates",
                    "A 'poems I have memorized' list the child keeps with the date each was learned",
                ],
                "presentation": {
                    "three_period_lesson": "This is a rhyme scheme; this is a stanza; this is an image. Show me a rhyme; show me a stanza; show me an image. Mark the rhyme scheme of this poem.",
                    "steps": [
                        "The guide reads aloud a poem and points out the rhyme scheme, stanzas, and imagery",
                        "The child works through poems freely with the marking sheets",
                        "The child chooses a poem to memorize each week and adds it to their recitation notebook",
                        "Across the term the child's memorized repertoire grows",
                    ],
                },
                "control_of_error": "The poem itself is the control: a rhyme scheme is either correct or not; the child reads the line again and adjusts.",
                "abstraction_pathway": "From enjoying poems as music, to noticing their structure with vocabulary, toward reading any new poem with full attention to form and content at the first reading.",
                "extensions": [
                    "Memorize a longer poem (a Frost or a Shakespeare passage at the upper edge of the band)",
                    "Build a personal anthology of favorite poems",
                    "Recite for a real audience: family gathering, video to a grandparent, school presentation",
                ],
                "observation_focus": "Watch for the child returning to the poetry shelf freely, for the memorized repertoire growing, and for the child reaching for poetry vocabulary in their own talk.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a generous poetry shelf with a wide variety of forms and poets",
                    "Read a poem aloud at breakfast or bedtime as a family habit",
                    "Welcome the child's memorization without making it assigned work",
                    "Listen to spoken-word poetry, audiobooks of poetry, recordings of poets reading their own work",
                ],
                "real_world_contexts": [
                    "Reciting memorized poems at family gatherings",
                    "Reading song lyrics as poetry",
                    "Writing greeting cards in verse for birthdays and holidays",
                    "Listening to poems on long car trips",
                ],
                "conversation_starters": [
                    "What's a poem you've been thinking about?",
                    "Want to memorize a poem this week? Pick one you love.",
                    "Read me that poem aloud. I want to hear it.",
                    "Did you notice how the poem sounds different from a story?",
                ],
                "resource_bank": [
                    "A wide variety of poetry anthologies kept available",
                    "Audiobooks and spoken-word recordings of poetry",
                    "Song lyrics treated as poetry where the child notices them",
                    "A discussion partner who loves poetry alongside the child",
                ],
                "parent_role": "Love poetry yourself, visibly. Read aloud often. Welcome the child's memorizations and recitations. Welcome the child's strong opinions about poems.",
                "observation_documentation": "Across a term, note the poems the child has chosen to memorize, the poets they return to, and the way they talk about poems. This noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Rhyme scheme and meter are patterns: identifying patterns is the same math-and-music skill",
            "science": "Many great nature poems (Frost, Mary Oliver, Wordsworth) are nature observation in compressed form; the poem teaches close attention to the natural world",
            "history": "Memorizing poems is one of the oldest educational practices; the child enters a tradition that runs back to before writing",
            "writing": "Reading poetry trains the child to write with attention to sound, rhythm, and specific words; this feeds all later writing",
        },
    },
    "rd-11": {
        "enriched": True,
        "learning_objectives": [
            "Read and enjoy myths from Greek, Roman, and Norse traditions in age-appropriate retellings",
            "Understand mythology as the literature of ancient peoples: how they explained the natural world, their gods, their heroes, and the human condition",
            "Identify the major gods, heroes, and origin stories of at least one mythological tradition",
            "Recognize common myth-types: origin stories (creation, why the seasons change), hero quests, transformations, cautionary tales",
            "Distinguish reading myth as literature (which we do) from reading myth as belief instruction (which we do not); read the traditions on their own terms without imposing modern judgments",
        ],
        "teaching_guidance": {
            "introduction": (
                "Mythology is the literature of the ancient world: how Greeks and Romans, Norse peoples, and many other "
                "traditions explained the natural world, named their gods, told the stories of their heroes, and "
                "passed down their wisdom and their warnings. At this band the child reads mythology as literature, "
                "for the stories, the characters, the moral and literary substance, not as belief instruction and not "
                "as religion in any practicing sense. The child meets Athena and Odysseus and Thor and Loki and "
                "Persephone as characters in foundational stories of Western (and other) traditions. Honest content "
                "note: classical mythology includes violence, family conflict, and adult themes; age-appropriate "
                "retellings (D'Aulaire, Padraic Colum, Edith Hamilton in the upper edge) handle the content "
                "responsibly. The child reads the traditions ON THEIR OWN TERMS: ancient peoples are not naive; their "
                "myths carry real human truth alongside the imagination."
            ),
            "scaffolding_sequence": [
                "Begin with Greek mythology in retellings: D'Aulaire's Book of Greek Myths is the standard starting point; Padraic Colum's The Children's Homer is a longer prose retelling",
                "Introduce the twelve Olympian gods: Zeus, Hera, Poseidon, Demeter, Athena, Apollo, Artemis, Ares, Hephaestus, Aphrodite, Hermes, Dionysus (and Hades, often counted alongside)",
                "Read the origin stories: Gaia and Uranus, the Titans, the rise of the Olympians, the creation of humans, Pandora's jar",
                "Read several hero stories: Perseus and Medusa, Theseus and the Minotaur, Atalanta, Hercules and his twelve labors, Jason and the Argonauts",
                "Move to Norse mythology: D'Aulaire's Book of Norse Myths is the parallel starting point; meet Odin, Thor, Loki, Freya, Frigg, Heimdall; the Aesir vs the Vanir; the trickster figure Loki; Ragnarok",
                "Read parallel myth-types across traditions: the creation story (Greek vs Norse vs others); the trickster (Hermes / Loki / many traditions); the hero quest",
                "Discuss the function of myth: explaining seasons (Persephone), teaching consequences (Icarus, Pandora), naming the world (constellations come from myth)",
                "Honor each tradition on its own terms: Greek gods are different from Norse gods in temperament and structure; the child notices the differences without ranking them",
            ],
            "socratic_questions": [
                "What does this myth explain about the world?",
                "What kind of myth is this: origin, hero, transformation, or cautionary?",
                "Who is the trickster in this tradition? What does the trickster do?",
                "How is this Greek god different from this Norse god? Same role, different temperament: what changes?",
                "What does this myth teach about consequences? About courage? About hubris?",
                "Why might ancient peoples have made this story up? What in their lives might it have answered for them?",
            ],
            "practice_activities": [
                "Read a myth a day from D'Aulaire's Greek or Norse myths across the term",
                "Build a gods chart: name, domain, symbols, relationships, key stories",
                "Map the hero quest: pick one hero (Perseus, Theseus, Hercules, Sigurd), trace their quest in the plot-mountain form from rd-07",
                "Compare two traditions: Greek and Norse creation stories side by side; Greek and Norse views of the afterlife",
                "Retell a favorite myth orally and in writing, applying rd-03 and rd-04 narration skills",
                "Notice myth references in modern stories, names (Apollo, Athena, Mercury are everywhere), and brands",
            ],
            "real_world_connections": [
                "Recognizing mythological names in space (planets, moons, missions), in brands (Nike, Athena, Apollo), and in everyday English (panic from Pan, herculean, narcissistic)",
                "Recognizing mythological allusions in books, movies, and shows the family watches (Percy Jackson is built entirely on Greek myth; Marvel's Thor draws on Norse)",
                "Talking about the constellations and naming the myths behind them (Orion, Cassiopeia, Andromeda)",
                "Visiting a museum's classical or Viking collection if available; recognizing the figures depicted",
                "Reading parallel myths from other traditions the family knows (West African Anansi stories, Indigenous origin stories, Hindu epics) with the same respect and attention",
            ],
            "common_misconceptions": [
                "Treating myths as childish or naive. Myths carry real human truth; the ancient peoples who told them were as wise about people as we are.",
                "Imposing modern moral judgments on ancient stories. Read the stories on their own terms first; the child can think about them critically AFTER understanding them as they were told.",
                "Confusing mythology with religion. The child reads myth as literature; they are not learning Greek religion or Norse religion as a practicing matter. (Reverence for the traditions and curiosity about their meaning are both fine.)",
                "Treating one tradition as 'better' than another. Greek and Norse mythology have different temperaments and shapes; neither is superior; both are worth reading.",
                "Reading edited-for-children versions as if they were the originals. The retellings are doors into the originals; the originals (Homer, the Eddas) wait for later bands.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Names the twelve Olympian gods with their domains",
                "Tells at least three Greek hero stories in their own words",
                "Names the major Norse gods (Odin, Thor, Loki, Freya, Frigg) with their characters",
                "Identifies the type of a myth (origin, hero, transformation, cautionary) when given one to read",
                "Compares a Greek and a Norse myth on the same type (creation, hero, trickster)",
                "Recognizes mythological allusions in modern names, places, and stories",
            ],
            "proficiency_indicators": [
                "Names several Olympian gods and tells one or two hero stories",
                "Identifies myth type with prompting",
            ],
            "developing_indicators": [
                "Knows the names of one or two gods but cannot place their domain or stories",
            ],
            "assessment_methods": [
                "gods chart compilation",
                "hero quest plot mountain",
                "myth-type identification on unfamiliar myths",
                "two-tradition comparison (Greek vs Norse)",
                "modern-allusion recognition: name the myth behind a modern reference",
            ],
            "sample_assessment_prompts": [
                "Name the twelve Olympian gods and one thing each is the god of.",
                "Tell me the story of Perseus and Medusa in your own words.",
                "Compare the Greek creation story (Gaia and Uranus) with the Norse creation story (Ymir, the Aesir).",
                "What kind of myth is the story of Pandora? Why is it that kind?",
                "Where do we see Greek mythology in modern names and stories?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Who is the king of the Greek Olympian gods?",
                "expected_type": "multiple_choice",
                "options": [
                    "Apollo.",
                    "Zeus.",
                    "Hades.",
                    "Hermes.",
                ],
                "correct_answer": "Zeus.",
                "hints": [
                    "He throws lightning bolts and rules from Mount Olympus.",
                ],
                "explanation": (
                    "Zeus is the king of the Olympian gods, ruler of the sky, thrower of lightning, husband of Hera. "
                    "His Roman name is Jupiter."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is a 'myth'?",
                "expected_type": "multiple_choice",
                "options": [
                    "A lie someone made up.",
                    "A traditional story, often involving gods or heroes, that ancient peoples told to explain the world or pass down wisdom.",
                    "A modern fantasy novel.",
                    "A history book.",
                ],
                "correct_answer": "A traditional story, often involving gods or heroes, that ancient peoples told to explain the world or pass down wisdom.",
                "hints": [
                    "Myths are old, traditional, and often involve gods.",
                ],
                "explanation": (
                    "A myth is a traditional story from an ancient tradition, often involving gods or heroes, that "
                    "explains something about the world or passes down wisdom. Myths are NOT just lies; they are "
                    "literature that often carries real truth about people."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "Pandora opened a jar that was forbidden to her, and out came all the troubles of the world. What "
                    "type of myth is this?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "Origin myth.",
                    "Hero quest.",
                    "Transformation myth.",
                    "Cautionary tale.",
                ],
                "correct_answer": "Cautionary tale.",
                "hints": [
                    "What does this myth warn against?",
                ],
                "explanation": (
                    "The Pandora story is a cautionary tale: it warns against curiosity that overrides clear "
                    "instructions, and it explains how trouble entered the world. (Many myths are mixed types; this "
                    "one is mostly cautionary with an origin-of-trouble element.)"
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "Both Greek and Norse traditions have a trickster figure. Who is each, and how are they similar "
                    "and different?"
                ),
                "expected_type": "text",
                "hints": [
                    "Greek: Hermes. Norse: Loki.",
                    "Both deceive and cause trouble, but they have different temperaments and roles.",
                ],
                "explanation": (
                    "Greek trickster: Hermes, messenger of the gods, thief in his childhood (he stole Apollo's cattle), "
                    "charming and clever, generally on the side of the Olympians. Norse trickster: Loki, blood-brother "
                    "of Odin, often makes mischief and sometimes catastrophe, increasingly opposed to the Aesir, plays "
                    "a major role in Ragnarok. Both deceive; Hermes is generally benevolent in the Greek stories, while "
                    "Loki turns destructive over the Norse arc."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "Name three mythological references you can find in the modern world (places, names, brands, "
                    "stories) and explain the myth behind each."
                ),
                "expected_type": "text",
                "hints": [
                    "Look at planets, brands, sports teams, book titles, names you know.",
                ],
                "explanation": (
                    "Examples: the planet Mars is named for the Roman god of war (Greek Ares); the brand Nike is named "
                    "for the Greek goddess of victory; the Apollo space program was named for the Greek god of "
                    "(among other things) reason and the sun; the word 'panic' comes from the god Pan; 'herculean' "
                    "means as strong as Hercules; 'narcissistic' comes from Narcissus who fell in love with his own "
                    "reflection. Mythology is everywhere in modern English and modern culture."
                ),
            },
        ],
        "assessment_items": [
            {
                "prompt": "Name the twelve Olympian gods and give one detail about each (their domain, their symbol, or a famous story).",
                "type": "open_response",
                "target_concept": "olympian_gods_recall",
                "rubric": (
                    "Mastery: names at least 10 of the 12 with details for most. Proficient: 6 to 9 with some "
                    "details. Developing: fewer than 6 named."
                ),
            },
            {
                "prompt": "Tell me the story of Perseus and Medusa in your own words. Apply the rd-03 narration skill.",
                "type": "open_response",
                "target_concept": "hero_quest_narration",
                "rubric": (
                    "Mastery: complete narration with main events in order, including the divine help (Athena, Hermes), "
                    "the encounter with the Graeae, the defeat of Medusa, and the return. Proficient: gist with some "
                    "events. Developing: scattered events out of order."
                ),
            },
            {
                "prompt": "Compare a Greek and a Norse myth on the same type (creation, trickster, hero, end-of-world). Use the rd-09 comparison skill.",
                "type": "open_response",
                "target_concept": "cross_tradition_comparison",
                "rubric": (
                    "Mastery: substantive comparison naming what is shared and what is different across the two "
                    "traditions on the same myth type. Proficient: surface comparison. Developing: cannot compare."
                ),
            },
            {
                "prompt": "Find three mythological references in modern names, places, or stories you encounter this week. Tell me the myth behind each.",
                "type": "open_response",
                "target_concept": "modern_allusion_recognition",
                "rubric": (
                    "Mastery: three real references with the myths correctly named. Proficient: two references. "
                    "Developing: cannot identify mythological allusions."
                ),
            },
        ],
        "resource_guidance": {
            "required": [
                "D'Aulaire's Book of Greek Myths (the standard age-appropriate starting point)",
                "D'Aulaire's Book of Norse Myths",
                "A gods-chart template the child fills in across the term",
            ],
            "recommended": [
                "Padraic Colum's The Children's Homer for a longer prose retelling of the Iliad and Odyssey",
                "Edith Hamilton's Mythology for the upper edge of the band",
                "Roger Lancelyn Green's Tales of the Greek Heroes",
                "Kevin Crossley-Holland's The Norse Myths for the upper edge",
                "A children's atlas of the ancient world to ground the geography",
            ],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 20, "assessment": 20},
        "accommodations": {
            "dyslexia": "Audiobooks of D'Aulaire are excellent; the language is rich and the stories carry well by ear. Mythology lives in the oral tradition; audio is honest.",
            "adhd": "Short individual myth chapters at a time. Hero stories with clear plot arcs (Perseus, Theseus, Hercules's labors) hold attention better than the more diffuse god-relationship material.",
            "gifted": "Move to Edith Hamilton, then to direct (age-appropriate) reading of the Iliad and Odyssey in prose retelling. Begin to notice the structural elements of myth (the hero's journey as a pattern). Introduce comparative mythology lightly.",
            "visual_learner": "The D'Aulaire illustrations are themselves great teaching. Build a wall chart of the Olympian gods with images.",
            "kinesthetic_learner": "Act out a myth with the family. Build a 3D model of Mount Olympus or Asgard. Walk the constellations outside at night.",
            "auditory_learner": "Audiobooks of myth collections. Discuss the stories aloud with a real listener.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": (
                    "Today and across this term we read the myths of the Greeks and the Norse: how they told the world, "
                    "named their gods, and remembered their heroes. We read them as literature, with attention and "
                    "respect, on their own terms. We learn the twelve Olympian gods, several hero stories, the major "
                    "Norse gods, and the types of myth (origin, hero, transformation, cautionary)."
                ),
                "gradual_release": {
                    "i_do": "Parent reads aloud a D'Aulaire myth, naming each god as they appear and explaining one detail.",
                    "we_do": "Together with the child, read the next myth; the child names the gods that appear and the parent fills in.",
                    "you_do": "Child reads a myth independently and tells it back, naming the gods and identifying the type.",
                },
                "guided_practice": [
                    "Myth-a-day reading from D'Aulaire",
                    "Gods chart compilation across the term",
                    "Hero quest plot mountain for each major hero",
                ],
                "independent_practice": [
                    "Reading favorite myths from the household library",
                    "Recognizing mythological allusions in real-world contexts (names, brands, modern stories)",
                ],
                "mastery_check": [
                    "Names twelve Olympian gods with domains",
                    "Tells three hero stories in own words",
                    "Identifies myth types on unfamiliar myths",
                    "Compares Greek and Norse on the same myth type",
                ],
                "spiral_review": [
                    "Return to early myths after several weeks; the child sees connections they did not see before",
                ],
            },
            "classical": {
                "narrative_introduction": (
                    "The myths of the Greeks and Romans are the foundational literature of the Western tradition. "
                    "Homer is the father of European poetry; Ovid's Metamorphoses shaped two millennia of Western art "
                    "and literature; the gods and heroes are everywhere in the language, the names, the imagination. "
                    "Norse mythology is the parallel inheritance of northern Europe and is itself foundational. To "
                    "learn these is to take up the long inheritance of careful storytelling."
                ),
                "memory_work": {
                    "chants": [
                        "Recite the twelve Olympians: Zeus, Hera, Poseidon, Demeter, Athena, Apollo, Artemis, Ares, Hephaestus, Aphrodite, Hermes, Dionysus",
                        "Recite the four types of myth: origin, hero, transformation, cautionary",
                        "Recite the major Norse gods: Odin, Thor, Loki, Freya, Frigg, Heimdall, Tyr",
                    ],
                    "recitations": [
                        "Memorize and recite a passage from a beloved myth across the term (Homer's invocation, a passage from D'Aulaire, a Viking saga line)",
                    ],
                },
                "copywork": [
                    "Copy the genealogies and the Olympian table into the copybook; the structure of the pantheon lives in the hand",
                ],
                "recitation_routine": "At each new myth, recite the gods that appear and place them in the family tree of Olympus.",
                "history_integration": "Mythology is the literature of the ancient world along the chronological spine: Bronze Age Greece, Viking Age Scandinavia. Pair mythology reading with the history of the period.",
                "read_aloud_suggestions": [
                    "D'Aulaire's Greek and Norse myth books, Padraic Colum's prose retellings, Edith Hamilton for the upper edge",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "D'Aulaire's Book of Greek Myths and Book of Norse Myths (living books par excellence)",
                    "Padraic Colum's The Children's Homer, The Golden Fleece, The Children of Odin",
                    "Roger Lancelyn Green's Tales of the Greek Heroes and Tales of Troy and Greece",
                ],
                "short_lesson_flow": "Read one myth aloud per session; the child narrates it back; talk briefly about the type of myth and the gods involved. Stop while interest is still high.",
                "narration_prompt": "Tell me the myth in your own words. Which gods were in it? What type of myth was it?",
                "real_world_objects": [
                    "A growing gods chart on the wall of the reading area",
                    "A map of ancient Greece and ancient Scandinavia",
                    "A constellation chart that shows the mythological names",
                ],
                "nature_connection": "The constellations are mythology written in the night sky. Walk outside on a clear night and find Orion, the Big Dipper (the Great Bear), Cassiopeia. The names are the myths.",
                "habit_focus": "The habit of reading the great stories with attention and respect, on their own terms.",
            },
            "montessori": {
                "prepared_materials": [
                    "D'Aulaire's myth books in the reading area",
                    "A gods chart the child completes across the term, with cards for each god the child meets",
                    "A myth-type sort: cards naming origin, hero, transformation, cautionary; the child sorts known myths into the types",
                    "A constellation chart with the mythological figures",
                ],
                "presentation": {
                    "three_period_lesson": "This is Zeus; this is Athena; this is Hermes. Show me Zeus; show me Athena; show me Hermes. Who is this god?",
                    "steps": [
                        "The guide presents each Olympian god with their symbol and domain",
                        "The child fills in the gods chart as they encounter each in reading",
                        "The child sorts myths into types as they read them",
                        "Across the term the child builds their own gods library and myth-type collection",
                    ],
                },
                "control_of_error": "The text itself is the control: a child can return to D'Aulaire to confirm a god's domain or a myth's type.",
                "abstraction_pathway": "From individual myths, to recognizing types and gods across many myths, toward seeing the structure of an entire tradition.",
                "extensions": [
                    "Compare multiple traditions (Greek, Norse, others the family knows) on shared myth types",
                    "Build a constellation map with the mythological figures",
                    "Move toward direct reading of age-appropriate Iliad and Odyssey",
                ],
                "observation_focus": "Watch for the child reaching for mythological vocabulary in their own talking and for recognizing references in modern contexts.",
            },
            "unschooling": {
                "invitations": [
                    "Keep D'Aulaire and the other myth retellings on the shelf within reach",
                    "Watch age-appropriate films and shows that draw on mythology (Disney's Hercules, Percy Jackson, Marvel's Thor for the upper edge with a critical eye)",
                    "Visit museums with classical or Viking collections when possible",
                    "Talk about the constellations on summer nights outside",
                ],
                "real_world_contexts": [
                    "Recognizing mythological names in space (planets, missions)",
                    "Recognizing mythological names in sports teams and brands",
                    "Recognizing mythological allusions in books and movies the family enjoys",
                    "Visiting a museum's mythological collection",
                ],
                "conversation_starters": [
                    "Did you know that planet is named for a god? Want to know what they were the god of?",
                    "I noticed your book mentioned Athena. Do you know her story?",
                    "Want to hear the Greek version of how the world was made? It's wild.",
                ],
                "resource_bank": [
                    "D'Aulaire and other myth books on the shelf",
                    "Audiobooks for car trips",
                    "Films and shows that draw on mythology",
                    "A constellation chart or app",
                ],
                "parent_role": "Love the myths yourself, visibly. Welcome the child's questions. Read aloud with energy.",
                "observation_documentation": "Across a term, note which gods the child returns to, which heroes captivate them, and which traditions they want more of. Follow the interest.",
            },
        },
        "connections": {
            "math": "Many myths involve genealogies and family trees; reading the Olympian family tree is the same skill as reading any structured chart",
            "science": "The constellations are mythology in the night sky; many planetary and stellar names are mythological; astronomy and myth are entwined",
            "history": "Mythology is the literature of the ancient world; reading myth supports the history sequence in the period",
            "writing": "Many modern stories are built on mythological frameworks; learning to read myth prepares the child to recognize and use mythological structures in their own writing",
        },
    },
    "rd-12": {
        "enriched": True,
        "learning_objectives": [
            "Use context clues to determine the meaning of an unfamiliar word in a sentence or passage",
            "Recognize the four common types of context clue: definition, example, synonym, antonym",
            "Distinguish when context is sufficient (the word's meaning is clear from the surrounding text) from when it is insufficient (the word must be looked up or asked about)",
            "Develop the habit of trying context first before stopping to look up or ask, so reading flow is preserved",
            "Track new words learned across a term as a real-world vocabulary log",
        ],
        "teaching_guidance": {
            "introduction": (
                "Foundational reading (rf-19) built vocabulary through direct instruction. Developing vocabulary takes "
                "up the central skill that an independent reader uses for the rest of their reading life: figuring out "
                "an unfamiliar word from the words around it. The skill rests on four types of context clue: "
                "DEFINITION (the sentence defines the word for you), EXAMPLE (the sentence gives an example), SYNONYM "
                "(the sentence pairs the word with a known synonym), ANTONYM (the sentence pairs the word with its "
                "opposite, often signaled by 'but' or 'unlike'). The child also learns when context is INSUFFICIENT "
                "and the word should be looked up or asked about; the habit of trying context first is what keeps "
                "reading flow alive."
            ),
            "scaffolding_sequence": [
                "Begin with a sentence that defines its key word explicitly: 'A philologist, that is, a person who studies the history of language, traveled the world collecting old words.' Show the child the definition clue.",
                "Introduce the example clue: 'The bird had carnivorous habits; it ate small mice, frogs, and other live prey.' Show how 'small mice, frogs, and other live prey' is the example that reveals 'carnivorous'.",
                "Introduce the synonym clue: 'The path was narrow and constricted by the trees on both sides.' Show how 'narrow' is the synonym that reveals 'constricted'.",
                "Introduce the antonym clue: 'Unlike his lazy brother, Tom was diligent and finished his work early.' Show how 'lazy' (the opposite) reveals 'diligent'.",
                "Practice each clue type on multiple sentences from the child's actual reading",
                "Move to passages where the context clue is across multiple sentences, not within one",
                "Practice the 'context-first, look-up-second' habit: when the child meets an unfamiliar word, try context first; if context is insufficient or the meaning is critical, then look up",
                "Keep a vocabulary log: title of the book, the new word, the sentence it appeared in, the meaning the child worked out, and (if looked up) the dictionary confirmation",
            ],
            "socratic_questions": [
                "What words around this unfamiliar word might tell you what it means?",
                "Does the sentence give a definition? An example? A synonym? An opposite?",
                "Can you make a smart guess at the meaning from what you read? Does the guess make the rest of the sentence make sense?",
                "Is this a word you can figure out, or one where context isn't enough? How do you know?",
                "What was the new word from yesterday's reading? Did you remember it today?",
            ],
            "practice_activities": [
                "Context-clue type identification: in a passage, find an unfamiliar word and name which type of clue (definition / example / synonym / antonym) the surrounding text uses",
                "Make-a-smart-guess practice: read a sentence with an unfamiliar word; guess the meaning from context; check against a dictionary",
                "Vocabulary log: across a term, log every new word the child meets and figures out (with the sentence, the guess, and the confirmation)",
                "Word-of-the-day from current reading: pick one good context-rich sentence each day and work through it together",
                "Read-aloud-and-pause: parent reads a passage aloud; pauses on an unfamiliar word; child works out the meaning from context",
            ],
            "real_world_connections": [
                "Working out unfamiliar words during chapter book reading without stopping the flow",
                "Working out unfamiliar terms in nonfiction (science vocabulary, history vocabulary) where context often defines explicitly",
                "Recognizing the same skill in adult conversation: most new words an adult learns are picked up from context",
                "Working out signs, menus, and instructions in real-world situations",
                "Recognizing context clues in subtitles and dubbed media",
            ],
            "common_misconceptions": [
                "Believing every unfamiliar word should be looked up. Looking up every word destroys reading flow. Context first is the rule.",
                "Believing context is always sufficient. Sometimes context is too thin (especially for technical vocabulary or precise meanings); the dictionary or asking is the correct move then.",
                "Treating a context-guess as a final answer. A smart guess from context is a working hypothesis; the next several sentences usually confirm or correct it.",
                "Skipping unfamiliar words entirely. Skipping costs comprehension; context-from-trying is much better than skipping.",
                "Believing dictionary work is always more careful than context. A dictionary gives one or two definitions; a context-grounded guess is the meaning IN THIS SENTENCE, which is what reading actually needs.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Names the four context-clue types and gives an example of each",
                "Determines the meaning of an unfamiliar word from context in unfamiliar passages",
                "Distinguishes when context is sufficient from when it is insufficient and chooses to look up or ask appropriately",
                "Sustains the context-first habit during chapter book reading without stopping the flow",
                "Keeps a vocabulary log across a term as evidence of growth",
            ],
            "proficiency_indicators": [
                "Identifies clear context clues with prompting",
                "Makes reasonable guesses at meaning from context",
            ],
            "developing_indicators": [
                "Stops at every unfamiliar word; cannot proceed without looking up",
                "Skips unfamiliar words without trying context",
            ],
            "assessment_methods": [
                "context-clue type identification on prepared passages",
                "make-a-smart-guess exercises with dictionary confirmation",
                "vocabulary log review across the term",
                "real-time reading observation during chapter book reading",
            ],
            "sample_assessment_prompts": [
                "Read this sentence. What does the underlined word mean? What clue helped you?",
                "For each of these four sentences, name which type of context clue is used.",
                "Show me your vocabulary log. What word was hardest? What word do you remember best?",
                "When you read your chapter book and meet a new word, what do you do?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": (
                    "What does 'feline' mean in this sentence? 'The feline, a small black cat, slept in the sunbeam.'"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "A type of bird.",
                    "A cat.",
                    "A piece of furniture.",
                    "A kind of weather.",
                ],
                "correct_answer": "A cat.",
                "hints": [
                    "Look for the example clue in the sentence.",
                ],
                "explanation": (
                    "The sentence gives an EXAMPLE: 'the feline, a small black cat'. The example tells you that a "
                    "feline is a cat. This is the example context-clue type."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "What does 'diligent' mean? 'Unlike his lazy brother, Tom was diligent and finished his homework "
                    "early every day.'"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "Lazy.",
                    "Hardworking.",
                    "Tired.",
                    "Funny.",
                ],
                "correct_answer": "Hardworking.",
                "hints": [
                    "Look for the antonym clue: 'unlike his lazy brother'.",
                ],
                "explanation": (
                    "The sentence pairs 'diligent' with its opposite ('unlike his lazy brother'). The antonym tells you "
                    "that diligent is the OPPOSITE of lazy, which is hardworking. The 'unlike' signal word marks the "
                    "antonym context-clue type."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What are the four common types of context clue?",
                "expected_type": "multiple_choice",
                "options": [
                    "Beginning, middle, end, epilogue.",
                    "Definition, example, synonym, antonym.",
                    "Fiction, nonfiction, poetry, drama.",
                    "Past, present, future, dream.",
                ],
                "correct_answer": "Definition, example, synonym, antonym.",
                "hints": [
                    "Four ways a sentence can reveal an unfamiliar word.",
                ],
                "explanation": (
                    "The four common context-clue types are: DEFINITION (the sentence defines the word), EXAMPLE (the "
                    "sentence gives an example), SYNONYM (the sentence pairs the word with a known synonym), and "
                    "ANTONYM (the sentence pairs the word with its opposite, often with 'unlike' or 'but')."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "You meet an unfamiliar word in your chapter book. What should you do FIRST?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "Stop and look it up immediately.",
                    "Try context first: re-read the sentence and see if the surrounding words tell you what it means. If context is enough, keep reading. If not, look up or ask.",
                    "Skip it and keep reading.",
                    "Give up on the book.",
                ],
                "correct_answer": "Try context first: re-read the sentence and see if the surrounding words tell you what it means. If context is enough, keep reading. If not, look up or ask.",
                "hints": [
                    "Context first preserves reading flow; look-up second when needed.",
                ],
                "explanation": (
                    "The context-first habit preserves reading flow. Most unfamiliar words can be figured out from "
                    "context. When context isn't enough (technical terms, precise meanings, words where the meaning "
                    "really matters), looking up or asking is the right second step. Stopping at every word destroys "
                    "reading; skipping every word destroys comprehension."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "Read this passage and find an unfamiliar word. Use context to guess its meaning. Then say what "
                    "type of context clue helped you."
                ),
                "expected_type": "text",
                "hints": [
                    "Pick any word the child does not immediately know; apply the four-type vocabulary.",
                ],
                "explanation": (
                    "A complete answer names the unfamiliar word, the guess at meaning from context, and which of the "
                    "four types (definition / example / synonym / antonym) helped. With practice this becomes "
                    "automatic; the child reads without conscious effort, and context-from-trying handles 90% of "
                    "unfamiliar words."
                ),
            },
        ],
        "assessment_items": [
            {
                "prompt": "For each of these four sentences (one per type), name the type of context clue used and the meaning of the underlined word.",
                "type": "open_response",
                "target_concept": "four_type_clue_identification",
                "rubric": (
                    "Mastery: identifies type and meaning for all four. Proficient: identifies type for three. "
                    "Developing: confuses types or cannot identify meaning."
                ),
            },
            {
                "prompt": "Read this passage and find three unfamiliar words. For each, work out the meaning from context and name the clue type.",
                "type": "open_response",
                "target_concept": "context_application_in_passage",
                "rubric": (
                    "Mastery: three words with meanings and clue types correctly identified. Proficient: two words. "
                    "Developing: cannot apply in extended passage."
                ),
            },
            {
                "prompt": "Show me your vocabulary log from this term. What word was hardest to figure out? What word stuck best?",
                "type": "open_response",
                "target_concept": "vocabulary_log_review",
                "rubric": (
                    "Mastery: log shows consistent entries across the term with reflection. Proficient: log shows "
                    "entries but less reflection. Developing: log empty or scattered."
                ),
            },
        ],
        "resource_guidance": {
            "required": [
                "a current chapter book or nonfiction reading with appropriate vocabulary stretch",
                "a vocabulary log (a notebook page with columns for book title, the new word, the sentence, the guess, the confirmation)",
                "a dictionary at the child's level (a children's dictionary, the family dictionary)",
            ],
            "recommended": [
                "an online or app-based dictionary the child can use for quick check after context",
                "a thesaurus for exploring synonyms and antonyms",
                "subscription to a vocabulary-rich children's magazine (Cricket, Cobblestone, Highlights) for context-clue practice",
            ],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 15, "assessment": 15},
        "accommodations": {
            "dyslexia": "Practice context-clue work on read-aloud passages, not just silent reading. The skill is about meaning, not decoding; remove the decoding load when teaching the skill.",
            "adhd": "Short context-clue exercises rather than long ones. The vocabulary log can be brief: a one-line entry per word.",
            "gifted": "Move to harder texts where context clues are more subtle. Introduce Latin and Greek roots as another context resource. Begin to notice when a single English word has multiple meanings and context disambiguates.",
            "visual_learner": "Highlight the context clue in color on a printed passage. Color-code the four clue types.",
            "kinesthetic_learner": "Sort sentence-strip cards into the four clue-type piles. Physical movement helps the category settle.",
            "auditory_learner": "Discuss context clues aloud. Read sentences aloud to hear how the clue works in the rhythm.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": (
                    "Today we learn the central reader's skill of figuring out unfamiliar words from context. We learn "
                    "the four types of context clue (definition, example, synonym, antonym) and we practice the "
                    "context-first habit that preserves reading flow."
                ),
                "gradual_release": {
                    "i_do": "Parent reads aloud a sentence with an unfamiliar word and works through the context to determine meaning, naming the clue type.",
                    "we_do": "Together with the child, work through several sentences identifying clue types and meanings.",
                    "you_do": "Child applies context-clue skill to their own current reading and keeps the vocabulary log.",
                },
                "guided_practice": [
                    "Daily context-clue practice on a chosen sentence from current reading",
                    "Weekly vocabulary log review",
                    "Apply context-first habit during chapter book reading",
                ],
                "independent_practice": [
                    "Keep vocabulary log across the term",
                    "Read widely with the context-first habit",
                ],
                "mastery_check": [
                    "Names four clue types with examples",
                    "Applies context-clue skill to unfamiliar passages",
                    "Keeps a real vocabulary log",
                ],
                "spiral_review": [
                    "Return to vocabulary log entries from weeks ago; check that the words are remembered",
                ],
            },
            "classical": {
                "narrative_introduction": (
                    "Vocabulary built by wide reading and careful attention is the mark of the educated reader. The "
                    "child who learns to figure out words from context owns a tool that serves the rest of their "
                    "reading life. This is the central reader's skill, older than printed dictionaries."
                ),
                "memory_work": {
                    "chants": [
                        "Recite the four clue types: definition, example, synonym, antonym",
                        "Recite the rule: context first, look-up second",
                    ],
                    "recitations": [
                        "Memorize one well-formed sentence containing a rich vocabulary word each week",
                    ],
                },
                "copywork": [
                    "Copy the day's vocabulary log entry into the copybook with the sentence and the meaning",
                ],
                "recitation_routine": "At each reading, the child names one new word and its context-derived meaning.",
                "history_integration": "Many English words have Latin and Greek roots; etymology supports context clues. Introduce a few common roots and prefixes lightly as the child encounters them.",
                "read_aloud_suggestions": [
                    "Books with rich vocabulary at and just above the child's reading level (E. B. White, Roald Dahl, the Magic Tree House series)",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "Living books with rich vocabulary that invite context-clue practice naturally",
                ],
                "short_lesson_flow": "During reading aloud or silent reading, when the child meets an unfamiliar word, pause briefly to try context together. If context is enough, continue; if not, look up. The flow of reading is preserved.",
                "narration_prompt": "Tell me about a new word you met today. How did you figure it out?",
                "real_world_objects": [
                    "A vocabulary log in the child's reading notebook",
                    "A family dictionary kept near the reading area",
                ],
                "nature_connection": "Nature writing often introduces rich vocabulary (specific species names, weather and landform terms) that the child works out from context.",
                "habit_focus": "The habit of attention to language. The careful reader notices an unfamiliar word and works it out; the careless reader skips.",
            },
            "montessori": {
                "prepared_materials": [
                    "Context-clue type cards with examples on the back",
                    "Sentence-strip cards for sorting into the four clue types",
                    "A vocabulary log the child manages",
                    "A children's dictionary in the reading area",
                ],
                "presentation": {
                    "three_period_lesson": "This is a definition clue; this is an example clue; this is a synonym clue; this is an antonym clue. Show me an example clue; show me a synonym clue. What type is this sentence?",
                    "steps": [
                        "The guide presents the four clue types with worked examples",
                        "The child sorts sentence strips into the four piles",
                        "The child applies context-clue skill to their own reading and keeps the vocabulary log",
                        "Across the term the child develops fluency in context-clue work without thinking about types",
                    ],
                },
                "control_of_error": "The dictionary is the control: a context-guess can be confirmed against the dictionary entry.",
                "abstraction_pathway": "From sorting concrete sentence strips, to identifying clue types in unfamiliar passages, to applying context-clue skill automatically during reading.",
                "extensions": [
                    "Latin and Greek roots as another context resource",
                    "Multiple-meaning words and how context disambiguates",
                    "Vocabulary growth measurement across a term",
                ],
                "observation_focus": "Watch for the child applying context first during reading without prompting.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a children's dictionary visible in the reading area",
                    "Welcome the child's questions about new words; share your own questions about words you encounter",
                    "Read widely and aloud, with rich vocabulary, so context-clue practice happens naturally",
                ],
                "real_world_contexts": [
                    "Figuring out new words during chapter book reading",
                    "Asking about words encountered in conversation, on signs, in shows",
                    "Building vocabulary through wide and varied reading",
                ],
                "conversation_starters": [
                    "Did you meet any interesting new words today?",
                    "How did you figure out what that meant?",
                    "What does that word mean to you in this sentence?",
                ],
                "resource_bank": [
                    "A wide and rich home library",
                    "A children's dictionary or family dictionary kept available",
                    "Audiobooks for hearing rich vocabulary in use",
                ],
                "parent_role": "Be a curious word-lover yourself. Look up words in front of the child. Welcome the child's questions about words. Read aloud books with rich vocabulary.",
                "observation_documentation": "Across a term, note the child's spontaneous vocabulary in talking and writing. New words used easily are the real sign of internalization.",
            },
        },
        "connections": {
            "math": "Word-problem reading often hinges on understanding key vocabulary; context-clue skill supports math reading directly",
            "science": "Science vocabulary is often introduced with explicit definitions in the text; the definition clue is especially common in science writing",
            "history": "Historical vocabulary is often unfamiliar; context-clue skill is the key to reading history at this level",
            "writing": "A growing vocabulary supports the child's own writing; words met in reading appear in writing weeks or months later",
        },
    },
    "rd-13": {
        "enriched": True,
        "learning_objectives": [
            "Condense a multi-paragraph passage or short chapter into a brief summary that captures the main idea and the essential supporting details",
            "Distinguish summarizing (compressing to essentials in your own words) from retelling or narrating (telling the events in order at length)",
            "Identify and discard nonessential details when summarizing: lovely descriptions, minor side actions, parenthetical dialogue",
            "Use the someone-wanted-but-so-then frame as a working tool for summarizing a narrative chapter",
            "Use the topic-and-most-important-points frame as a working tool for summarizing a nonfiction passage",
        ],
        "teaching_guidance": {
            "introduction": (
                "rd-06 built character analysis; the child is now equipped to read for what matters in a story. "
                "Summarizing is the move from telling everything that happened (narration) to telling what mattered "
                "(summary). The difference is essential. A narration of a chapter might run several minutes; a summary "
                "of the same chapter runs two or three sentences. Summarizing is a higher-order skill than narration "
                "because it asks the child to JUDGE which details are essential and which are not. Two frames carry "
                "the child a long way at this band: SOMEONE-WANTED-BUT-SO-THEN for narrative (Who. What did they "
                "want. What got in the way. So what did they do. Then what happened.) and TOPIC-AND-MOST-IMPORTANT-"
                "POINTS for nonfiction (What is this about. What are the two or three most important things it "
                "says.). Both frames are tools, not formulas: as the child grows, summaries become natural prose."
            ),
            "scaffolding_sequence": [
                "Begin with a single short paragraph from a familiar story; parent and child together produce a one-sentence summary",
                "Move to a chapter from a current chapter book; apply the someone-wanted-but-so-then frame and produce a two-to-three-sentence summary",
                "Practice the test of essentiality: read the summary; does it tell the main idea? If not, what is missing? Does it carry side details? If so, what can be cut?",
                "Distinguish summary from narration explicitly: narrate the chapter (take five minutes), then summarize the chapter (take thirty seconds). Compare.",
                "Move to a nonfiction passage (a magazine article, an encyclopedia entry, a science text); apply the topic-and-most-important-points frame",
                "Summarize across longer text: a whole story (not just a chapter), a whole article",
                "Practice graduated tightness: summarize the same chapter in 5 sentences, then in 3, then in 1. Show the trade-offs.",
                "Apply the skill in conversation: 'tell me what your book was about today' should now produce a real summary, not a chapter-by-chapter retelling",
            ],
            "socratic_questions": [
                "What is this passage mostly about? In one sentence.",
                "Who is the someone? What did they want? What got in the way? So what did they do? Then what happened?",
                "What is essential to the story? What is interesting but not essential?",
                "If you only had ten words to tell someone what this chapter is about, which ten words?",
                "Is that a summary, or a retelling? How can you tell the difference?",
            ],
            "practice_activities": [
                "Daily one-sentence summary of the current chapter the child is reading independently",
                "Someone-wanted-but-so-then frame applied to chapters of a chapter book; written in the reading notebook",
                "Topic-and-most-important-points frame applied to a short nonfiction passage each week",
                "Summary-versus-narration practice: narrate a chapter, then summarize the same chapter, then compare them aloud",
                "Graduated-tightness practice: summarize the same story in five sentences, then three, then one. Discuss what is lost and what survives.",
            ],
            "real_world_connections": [
                "Telling a friend, parent, or sibling what a book is about without retelling the whole thing",
                "Writing a book recommendation card for the library or for a friend",
                "Telling someone what happened in a TV show or movie without giving every scene",
                "Reading the back-cover blurb of a book; recognizing it as a summary written to invite a reader",
                "Summarizing the news, a magazine article, a podcast episode",
            ],
            "common_misconceptions": [
                "Believing summarizing is the same as retelling. They are different: retelling tells everything; summarizing tells what matters.",
                "Believing a good summary is a long summary. A good summary is the SHORTEST version that still carries the main idea and essential details.",
                "Believing every detail is essential. Most details are not. The judgment of essentiality is the heart of the skill.",
                "Believing summarizing is the same for fiction and nonfiction. The frames differ: narrative leans on character and conflict; nonfiction leans on topic and main points.",
                "Believing summarizing is something the child does once. Summarizing is a habit applied to every reading, every day.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Produces a brief, accurate summary of a narrative chapter using the someone-wanted-but-so-then frame",
                "Produces a brief, accurate summary of a nonfiction passage using the topic-and-most-important-points frame",
                "Distinguishes a summary from a retelling and can produce either when asked",
                "Discards nonessential details deliberately, naming why each cut detail was not essential",
                "Adapts summary length to context: one sentence when asked for the gist, three to five when asked for fuller summary",
            ],
            "proficiency_indicators": [
                "Produces a summary that includes the main idea but carries extra detail",
                "Distinguishes summary from retelling with prompting",
            ],
            "developing_indicators": [
                "Retells in full instead of summarizing",
                "Produces summaries that miss the main idea or include only side details",
            ],
            "assessment_methods": [
                "scored summaries of chapters and passages against a rubric",
                "summary-versus-narration discrimination tasks",
                "graduated-tightness exercises",
                "real-time observation during reading discussion: does the child summarize or retell?",
            ],
            "sample_assessment_prompts": [
                "Read this chapter. In two or three sentences, tell me what the chapter is about.",
                "Use the someone-wanted-but-so-then frame on this chapter.",
                "Summarize this nonfiction article in one sentence. Then in three sentences. What did the longer version add?",
                "Is this a summary or a retelling? How can you tell?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is the difference between a summary and a retelling?",
                "expected_type": "multiple_choice",
                "options": [
                    "There is no difference; they are the same thing.",
                    "A summary is short and tells what matters; a retelling tells everything in order.",
                    "A summary is for fiction; a retelling is for nonfiction.",
                    "A retelling is a kind of summary that uses fewer words.",
                ],
                "correct_answer": "A summary is short and tells what matters; a retelling tells everything in order.",
                "hints": [
                    "Think about the length and what is included in each.",
                ],
                "explanation": (
                    "A retelling tells the events in order at full length. A summary compresses the passage to its main "
                    "idea and essential details, in much fewer words. Summarizing asks the reader to judge which "
                    "details matter."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What does the someone-wanted-but-so-then frame help you do?",
                "expected_type": "multiple_choice",
                "options": [
                    "Memorize a chapter word for word.",
                    "Summarize a narrative chapter by naming who, what they wanted, what got in the way, what they did, and what happened.",
                    "List all the characters in a book.",
                    "Find the rhyme scheme of a poem.",
                ],
                "correct_answer": "Summarize a narrative chapter by naming who, what they wanted, what got in the way, what they did, and what happened.",
                "hints": [
                    "It is a frame for narrative summary.",
                ],
                "explanation": (
                    "The someone-wanted-but-so-then frame walks the reader through a narrative summary: Someone (who), "
                    "wanted (their goal), but (the obstacle), so (what they did), then (the result). Five quick beats "
                    "produce a real summary of a narrative chapter."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is the topic-and-most-important-points frame for?",
                "expected_type": "multiple_choice",
                "options": [
                    "Summarizing nonfiction by naming what it is about and the two or three most important things it says.",
                    "Writing a poem.",
                    "Memorizing a story.",
                    "Reading a graphic novel.",
                ],
                "correct_answer": "Summarizing nonfiction by naming what it is about and the two or three most important things it says.",
                "hints": [
                    "It is the nonfiction parallel to the someone-wanted-but-so-then frame.",
                ],
                "explanation": (
                    "Nonfiction is organized around topic and supporting points, not around a character's goal. The "
                    "topic-and-most-important-points frame matches the structure: what is this about (the topic), and "
                    "what are the two or three most important things it says (the points)."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "You have just finished a chapter of your book. Your friend asks 'what was that chapter about?' "
                    "What should you do?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "Retell every event in order from beginning to end.",
                    "Summarize the chapter in two or three sentences using the someone-wanted-but-so-then frame.",
                    "Say 'I don't know' and change the subject.",
                    "Read the whole chapter aloud to them.",
                ],
                "correct_answer": "Summarize the chapter in two or three sentences using the someone-wanted-but-so-then frame.",
                "hints": [
                    "What does the friend want? A short, helpful answer.",
                ],
                "explanation": (
                    "A friend asking 'what was it about' wants a summary, not a retelling. Two or three sentences "
                    "delivered through the someone-wanted-but-so-then frame produce a real, useful summary. This is "
                    "the everyday use of the skill."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "Summarize a chapter of your current book first in five sentences, then in three sentences, then "
                    "in one. What did each shorter version have to leave out?"
                ),
                "expected_type": "text",
                "hints": [
                    "Tighter summaries keep the essential and drop the nonessential.",
                ],
                "explanation": (
                    "Graduated-tightness practice shows the child what is essential and what is not. The five-sentence "
                    "version may carry secondary points; the three-sentence version keeps the main goal, obstacle, and "
                    "outcome; the one-sentence version distills the gist. Each cut teaches judgment."
                ),
            },
        ],
        "assessment_items": [
            {
                "prompt": "Read this assigned chapter. Summarize it in two or three sentences using the someone-wanted-but-so-then frame.",
                "type": "open_response",
                "target_concept": "narrative_summary_with_frame",
                "rubric": (
                    "Mastery: summary names the someone, the want, the obstacle, the action, the result; stays within "
                    "two or three sentences; captures the main idea. Proficient: includes most beats; may include some "
                    "nonessential detail. Developing: produces a retelling rather than a summary, or misses the main "
                    "idea."
                ),
            },
            {
                "prompt": "Read this short nonfiction passage. Summarize it in two or three sentences using the topic-and-most-important-points frame.",
                "type": "open_response",
                "target_concept": "nonfiction_summary_with_frame",
                "rubric": (
                    "Mastery: names the topic and the two or three most important points; stays brief; captures what "
                    "the passage is really about. Proficient: names topic but carries side details. Developing: cannot "
                    "distinguish main points from supporting detail."
                ),
            },
            {
                "prompt": "Summarize this chapter in five sentences, then in three, then in one. What did each shorter version leave out, and why?",
                "type": "open_response",
                "target_concept": "graduated_tightness_judgment",
                "rubric": (
                    "Mastery: produces all three lengths; names what each cut left out and why each cut was acceptable. "
                    "Proficient: produces all three lengths but cannot articulate why. Developing: cannot produce the "
                    "tightest versions."
                ),
            },
        ],
        "resource_guidance": {
            "required": [
                "a current chapter book the child is reading independently",
                "a short nonfiction passage (one to three paragraphs) for summary practice",
                "the child's reading notebook for written summaries",
            ],
            "recommended": [
                "a wall card with the two summary frames (someone-wanted-but-so-then; topic-and-most-important-points)",
                "back-cover blurbs from familiar books as examples of professional summaries",
                "a magazine subscription with short articles at the child's reading level",
            ],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 15, "assessment": 20},
        "accommodations": {
            "dyslexia": "Practice summary on read-aloud chapters first. The skill is about judgment of essentiality, not decoding; reduce the decoding load when teaching it.",
            "adhd": "Keep summary work brief. One sentence on the day's reading is enough. The graduated-tightness exercise can be done across several days rather than in one sitting.",
            "gifted": "Move to longer text (a whole short story; a whole article). Introduce thesis-and-support as a more abstract frame. Begin to summarize across multiple sources on a topic.",
            "visual_learner": "Use a graphic organizer for the someone-wanted-but-so-then frame: five boxes in a row. Fill each box, then write the summary from the boxes.",
            "kinesthetic_learner": "Act the someone-wanted-but-so-then frame with hand motions or stepping motions for the five beats. The body movement helps the structure settle.",
            "auditory_learner": "Speak the summary aloud before writing. Many strong summaries are first spoken, then written down from the spoken version.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": (
                    "Today we learn to summarize. Summarizing is the skill of saying what a passage is about in much "
                    "fewer words than the passage itself. We learn two frames: one for stories (someone-wanted-but-so-"
                    "then) and one for nonfiction (topic-and-most-important-points). Summary is different from "
                    "retelling, and it is one of the most useful skills a reader can have."
                ),
                "gradual_release": {
                    "i_do": "Parent reads a chapter aloud and demonstrates summarizing with the someone-wanted-but-so-then frame, naming each beat as it goes.",
                    "we_do": "Together with the child, summarize a second chapter using the frame. The child names the beats; parent helps with judgment of essentiality.",
                    "you_do": "Child summarizes a chapter on their own and writes the summary in the reading notebook.",
                },
                "guided_practice": [
                    "Daily one-sentence or two-sentence summary of the day's reading",
                    "Weekly nonfiction summary on a short article using the topic-and-points frame",
                    "Periodic graduated-tightness practice on a familiar story",
                ],
                "independent_practice": [
                    "Maintain the daily summary habit in the reading notebook",
                    "Use summary in conversation when asked about books",
                ],
                "mastery_check": [
                    "Produces clean summaries with the frames",
                    "Distinguishes summary from retelling",
                    "Adapts length to context (gist versus fuller summary)",
                ],
                "spiral_review": [
                    "Return to summaries from earlier in the term; check that they still feel accurate and tight",
                ],
            },
            "classical": {
                "narrative_introduction": (
                    "The educated reader knows the difference between everything a book says and what a book is about. "
                    "Summary is the skill of saying what a book is about. Ancient writers prized the brief, dense "
                    "saying: the epigram, the apothegm, the moral of the tale. To summarize is to honor a text by "
                    "naming what is essential in it."
                ),
                "memory_work": {
                    "chants": [
                        "Recite the narrative frame: someone, wanted, but, so, then",
                        "Recite the nonfiction frame: topic, most important points",
                    ],
                    "recitations": [
                        "Memorize a brief summary of a major work (a one-paragraph summary of The Odyssey or a chosen classic)",
                    ],
                },
                "copywork": [
                    "Copy a well-formed back-cover blurb from a familiar book as a model of professional summary",
                ],
                "recitation_routine": "At each reading session the child gives a brief spoken summary of the chapter just finished.",
                "history_integration": "Summarizing the deeds of a historical figure or the events of a historical period uses the same frames. History at this level is largely a discipline of well-formed summary.",
                "read_aloud_suggestions": [
                    "Books with strong narrative arcs that summarize cleanly: The Wind in the Willows, Stuart Little, the Narnia chronicles, Anne of Green Gables",
                    "Anthologies of short retellings (D'Aulaire, retold myths and legends) where each piece is already a kind of summary",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "Living books whose chapters carry a clear arc that the child can summarize",
                ],
                "short_lesson_flow": "After the reading, the child gives a brief spoken summary of what was read. Across weeks, written summary is introduced gradually alongside narration. Narration remains; summary is a related but distinct discipline.",
                "narration_prompt": "Now give me a narration. Now give me a summary. How are they different?",
                "real_world_objects": [
                    "The reading notebook for written summaries",
                    "A wall card with the two summary frames near the reading area",
                ],
                "nature_connection": "Nature observation also invites summary: at the end of a nature walk, what was the most important thing you saw today? In one sentence.",
                "habit_focus": "The habit of saying clearly what a passage was about. Narration and summary together build a reader who knows what they have read.",
            },
            "montessori": {
                "prepared_materials": [
                    "A frame card with the five beats of someone-wanted-but-so-then in clear print",
                    "A frame card with the topic-and-most-important-points beats",
                    "A small set of short passages (one narrative, one nonfiction, one descriptive) for summary practice",
                    "A graphic-organizer template for the narrative frame",
                ],
                "presentation": {
                    "three_period_lesson": "This is a summary; this is a retelling; this is a graduated-tightness exercise. Show me a summary; show me a retelling. Is this a summary or a retelling?",
                    "steps": [
                        "The guide presents the someone-wanted-but-so-then frame with a worked example",
                        "The child applies the frame to a short familiar passage",
                        "The guide presents the topic-and-most-important-points frame with a nonfiction example",
                        "The child applies that frame to a nonfiction passage",
                        "Across the term the child develops the habit of summarizing daily",
                    ],
                },
                "control_of_error": "The control is the chapter itself: a summary is accurate if a reader who has not read the chapter can grasp what it was about from the summary alone.",
                "abstraction_pathway": "From filling in the frame's beats one by one, to writing summaries as flowing prose, to choosing summary length to suit the audience.",
                "extensions": [
                    "Summary of multiple chapters as a single piece",
                    "Summary of an entire short book",
                    "Comparison of two summaries of the same chapter; what each emphasizes",
                ],
                "observation_focus": "Watch for the child summarizing rather than retelling without prompting. Watch for confident judgment about which details are essential.",
            },
            "unschooling": {
                "invitations": [
                    "Ask the child what their current book is about; receive a real summary as the answer over time",
                    "Read back-cover blurbs together; talk about how the writer chose what to include",
                    "Recommend books to each other in summary form",
                ],
                "real_world_contexts": [
                    "Telling a friend or sibling what a book or show was about",
                    "Writing brief recommendations on a family book wall or shared reading log",
                    "Summarizing podcast episodes, news stories, or a documentary watched together",
                ],
                "conversation_starters": [
                    "What was your book about today?",
                    "If you only had ten words to tell me what that chapter was about, what would you say?",
                    "Was that a summary or a retelling? Which did I ask for?",
                ],
                "resource_bank": [
                    "A home library with strong storytelling and accessible nonfiction",
                    "Magazines and articles at the child's level for short-form summary practice",
                    "Back-cover blurbs as professional summary models",
                ],
                "parent_role": "Model summary in your own conversation. Tell the child what your book or article was about in summary form. Welcome the child's summaries and ask follow-up questions about what was left out.",
                "observation_documentation": "Note when the child shifts from retelling to summarizing in everyday conversation. The shift signals internalization.",
            },
        },
        "connections": {
            "math": "Word problems often require summarizing what is being asked; the same judgment of essentials transfers directly",
            "science": "Summarizing a science article or experiment writeup uses the topic-and-points frame; science learning depends heavily on summary",
            "history": "Telling what happened in a historical period or what a figure did uses summary; this is the central skill of reading history at any level",
            "writing": "Writing a summary is itself a writing exercise; the discipline of compression strengthens the child's own writing across genres",
        },
    },
    "rd-14": {
        "enriched": True,
        "learning_objectives": [
            "Distinguish what the text says explicitly from what the text implies (what is stated versus what is inferred)",
            "Combine text evidence with prior knowledge to draw a logical inference about character feeling, motive, setting, or implied event",
            "Name the text evidence that supports an inference: 'I think X because the text says Y'",
            "Recognize when an inference is supported by the text and when it is a guess that goes beyond the text",
            "Apply the skill to both narrative and nonfiction (an author's implied stance; an experiment's implied conclusion)",
        ],
        "teaching_guidance": {
            "introduction": (
                "Inference is the conceptual turn of the developing reading band. Foundational comprehension (rf-12 "
                "through rf-14) asked the child to retrieve what the text says. Developing summarization (rd-13) asked "
                "the child to judge what mattered. Inference (rd-14) asks the child to read between the lines: to "
                "understand what the author IMPLIES but does not state directly. The skill rests on two ingredients: "
                "TEXT EVIDENCE (the words actually on the page) and PRIOR KNOWLEDGE (what the reader already knows "
                "about the world). The child combines the two to draw a logical conclusion. The discipline is that "
                "every inference must be supportable: 'I think X because the text says Y.' Without text evidence, an "
                "inference becomes a guess; with text evidence, it becomes real reading."
            ),
            "scaffolding_sequence": [
                "Begin with the simplest inference frame: 'It is raining. The puddles are spreading on the sidewalk.' What does this text tell you? (It is raining.) What does it imply? (It has been raining long enough to make puddles spread.) Show how the inference combines text plus knowledge.",
                "Introduce the I-think-X-because-the-text-says-Y sentence frame. Every inference uses it.",
                "Practice inferring character feeling: 'Tom slammed the door and refused to come down for dinner.' What is Tom feeling? (Angry / upset / hurt.) What text evidence? (He slammed the door; he refused dinner.)",
                "Practice inferring setting: 'They lit the lamps and pulled the curtains. The fire crackled.' When? (Evening or night, before electric light.) Why? (Lamps and fire suggest the era and time of day.)",
                "Practice inferring motive: 'Anna left the cookies on the windowsill and waited by the gate.' Why? (She was probably waiting for someone she expected to be lured by the cookies.) What in the text suggests it?",
                "Distinguish supported inferences from wild guesses: an inference must rest on text evidence; a guess does not.",
                "Apply to nonfiction: 'The early settlers carried very little with them; what they took, they made themselves.' What does this imply? (They made things by hand; they could not buy what they needed.) Inference works in nonfiction too.",
                "Read longer passages and identify multiple inferences with their supporting text evidence",
            ],
            "socratic_questions": [
                "What does the text actually say? What does it not say?",
                "What can you figure out from what the text says, even though the text doesn't say it directly?",
                "What in the text makes you think that?",
                "Is that an inference (supported by the text) or a guess (not supported by the text)?",
                "What do you already know about the world that helped you make that inference?",
            ],
            "practice_activities": [
                "Inference frame practice: read a short passage; answer 'what does the text imply?'; complete the I-think-X-because-the-text-says-Y sentence",
                "Stated-versus-implied sort: read a passage with several statements; for each, label STATED or IMPLIED",
                "Inference-versus-guess discrimination: present pairs of claims about a passage; for each, label INFERENCE (supported) or GUESS (unsupported)",
                "Character-feeling inference practice on chapters of current reading: stop at moments and ask 'how is the character feeling? what tells you?'",
                "Nonfiction inference practice: a science or history paragraph; what does the author imply about a topic? what evidence?",
            ],
            "real_world_connections": [
                "Reading other people's feelings and intentions in everyday social life (a friend's body language; a sibling's tone)",
                "Reading advertising critically (what does the ad imply about the product without saying it?)",
                "Reading news and opinion writing (what does the author imply about the subject?)",
                "Reading visual media (what does a movie scene imply through lighting, music, and setting?)",
                "Reading silence (when someone does not say something, what does that imply?)",
            ],
            "common_misconceptions": [
                "Believing inference is the same as guessing. Guesses are unsupported; inferences are supported by text evidence.",
                "Believing inference is finding information the text states. That is retrieval, not inference. Inference is what the text implies but does not state.",
                "Believing every interpretation is valid. Interpretations supported by text are valid; interpretations unsupported by text are not.",
                "Believing inference is only for fiction. Nonfiction writers also imply much: an author's stance, an experiment's significance, a historical figure's character.",
                "Believing prior knowledge alone produces inference. Prior knowledge plus text evidence produces inference; prior knowledge alone produces assumption.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Distinguishes stated information from implied information in a passage",
                "Makes inferences that combine text evidence with prior knowledge",
                "Cites text evidence using the I-think-X-because-the-text-says-Y frame",
                "Discriminates supported inferences from unsupported guesses",
                "Applies inference to nonfiction as well as narrative",
            ],
            "proficiency_indicators": [
                "Makes inferences with some text support; may sometimes guess",
                "Distinguishes inference from retrieval with prompting",
            ],
            "developing_indicators": [
                "Cannot reliably distinguish stated from implied",
                "Inferences are guesses unsupported by text",
            ],
            "assessment_methods": [
                "scored inference items on assigned passages",
                "stated-versus-implied sort tasks",
                "inference-versus-guess discrimination tasks",
                "real-time reading observation: does the child notice implication during discussion?",
            ],
            "sample_assessment_prompts": [
                "Read this passage. What does it say directly? What does it imply? Use the I-think-X-because-the-text-says-Y frame.",
                "Label each of these statements about the passage STATED or IMPLIED.",
                "Which of these claims is a supported inference, and which is a guess? Defend your answer with text evidence.",
                "Read this nonfiction paragraph. What does the author imply about the topic?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": (
                    "Read the sentence: 'Tom slammed the door and refused to come down for dinner.' What is Tom most "
                    "likely feeling?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "Happy and excited.",
                    "Angry or upset.",
                    "Sleepy.",
                    "Hungry.",
                ],
                "correct_answer": "Angry or upset.",
                "hints": [
                    "Slamming a door and refusing dinner are clues about feeling.",
                ],
                "explanation": (
                    "The text doesn't say 'Tom is angry'; it shows actions (slamming the door, refusing dinner) that "
                    "imply anger or upset. The reader combines text evidence (the actions) with prior knowledge (people "
                    "slam doors when angry) to infer the feeling. This is a clean inference."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is the difference between an inference and a guess?",
                "expected_type": "multiple_choice",
                "options": [
                    "There is no difference.",
                    "An inference is supported by text evidence and prior knowledge; a guess is not supported by the text.",
                    "An inference is for fiction; a guess is for nonfiction.",
                    "An inference uses harder words than a guess.",
                ],
                "correct_answer": "An inference is supported by text evidence and prior knowledge; a guess is not supported by the text.",
                "hints": [
                    "Inference rests on evidence.",
                ],
                "explanation": (
                    "Inference combines text evidence with prior knowledge to reach a conclusion the text doesn't "
                    "state directly. A guess goes beyond the text without support. The discipline of inference is "
                    "always being able to say 'I think X because the text says Y'."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "Read: 'They lit the lamps and pulled the curtains. The fire crackled on the hearth.' When does "
                    "this scene most likely take place?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "A summer afternoon.",
                    "An evening or night, in a time before electric lights.",
                    "A modern morning in a city apartment.",
                    "Inside a moving car.",
                ],
                "correct_answer": "An evening or night, in a time before electric lights.",
                "hints": [
                    "Lamps, curtains pulled, fire on a hearth: what do these clues suggest about time and era?",
                ],
                "explanation": (
                    "The text doesn't state the time or era. The reader infers from the details: lamps (rather than "
                    "electric lights) and a fire on a hearth (rather than central heating) suggest an earlier era; "
                    "lit lamps and pulled curtains suggest evening or night. Text plus prior knowledge produces a "
                    "confident inference about setting."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "The text says: 'Anna left a plate of cookies on the windowsill and waited by the gate.' Which is "
                    "an INFERENCE (supported by the text), and which is a GUESS (not supported)?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "Inference: Anna was expecting someone she wanted to lure with cookies. Guess: Anna had a brown dog named Max.",
                    "Inference: Anna had a brown dog named Max. Guess: Anna was expecting someone.",
                    "Both are inferences.",
                    "Both are guesses.",
                ],
                "correct_answer": "Inference: Anna was expecting someone she wanted to lure with cookies. Guess: Anna had a brown dog named Max.",
                "hints": [
                    "Which claim has text evidence behind it?",
                ],
                "explanation": (
                    "The text supports 'Anna was expecting someone she wanted to lure with cookies' (the cookies plus "
                    "the waiting are evidence). The text says nothing about a dog named Max, so that claim is a guess "
                    "unsupported by the text. The discipline: every inference must rest on text evidence."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "Read a chapter of your current book. Find one moment where the text implies something it does "
                    "not say directly. Complete: 'I think ____ because the text says ____.'"
                ),
                "expected_type": "text",
                "hints": [
                    "Look for moments of character feeling, motive, or setting that the text shows but does not state.",
                ],
                "explanation": (
                    "A complete answer names a real moment of implication, the inference itself, and the specific text "
                    "evidence behind it. With practice the child runs inference automatically while reading; this "
                    "explicit frame is the training wheel that lets the skill settle in."
                ),
            },
        ],
        "assessment_items": [
            {
                "prompt": "Read this passage. List two things the text states directly and two things the text implies. Use the I-think-X-because-the-text-says-Y frame for each implication.",
                "type": "open_response",
                "target_concept": "stated_versus_implied_discrimination",
                "rubric": (
                    "Mastery: identifies two stated and two implied items, each with text evidence for the implied "
                    "ones. Proficient: identifies stated and implied but text evidence is partial. Developing: "
                    "cannot distinguish stated from implied."
                ),
            },
            {
                "prompt": "Read this passage. Make three inferences about character, setting, or motive. Cite text evidence for each.",
                "type": "open_response",
                "target_concept": "inference_with_evidence",
                "rubric": (
                    "Mastery: three inferences each tied to specific text evidence. Proficient: inferences correct "
                    "but evidence is general. Developing: claims are guesses without text support."
                ),
            },
            {
                "prompt": "Read this nonfiction paragraph. What does the author imply about the topic? Cite text evidence.",
                "type": "open_response",
                "target_concept": "nonfiction_inference",
                "rubric": (
                    "Mastery: identifies the author's implied stance with text evidence. Proficient: identifies the "
                    "implication but evidence is partial. Developing: misses the implication."
                ),
            },
        ],
        "resource_guidance": {
            "required": [
                "a current chapter book with character-rich moments suitable for inference work",
                "short nonfiction passages with a clear authorial stance",
                "the child's reading notebook for written inference work",
            ],
            "recommended": [
                "a wall card with the I-think-X-because-the-text-says-Y frame",
                "picture books that imply more than they state (Chris Van Allsburg, Anthony Browne) as low-decoding inference practice",
                "wordless picture books and short films for inference practice without text load",
            ],
        },
        "time_estimates": {"first_exposure": 30, "practice_session": 20, "assessment": 20},
        "accommodations": {
            "dyslexia": "Practice inference on read-aloud passages and on wordless or low-text picture books. The skill is about implication, not decoding; remove the decoding load.",
            "adhd": "Brief, frequent inference moments rather than long inference exercises. One inference per chapter is enough at first; build from there.",
            "gifted": "Move to texts with subtler implication: poetry, literary fiction, persuasive nonfiction. Introduce the idea of unreliable narration and how it complicates inference.",
            "visual_learner": "Use two-column notes: text says / I infer. The visual layout makes the structure of inference explicit.",
            "kinesthetic_learner": "Act out the inferred feeling or motive. The body's enactment confirms the inference.",
            "auditory_learner": "Discuss inferences aloud before writing. Hearing the I-think-X-because-the-text-says-Y frame spoken helps the structure settle.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": (
                    "Today we learn to read between the lines. Inference is the skill of figuring out what the author "
                    "implies but does not state directly. We learn the I-think-X-because-the-text-says-Y frame, and "
                    "we practice the difference between an inference (supported by the text) and a guess (not "
                    "supported by the text)."
                ),
                "gradual_release": {
                    "i_do": "Parent reads a passage aloud, names what the text states and what the text implies, and demonstrates the inference frame with text evidence.",
                    "we_do": "Together with the child, work through several passages identifying stated, implied, and the supporting evidence.",
                    "you_do": "Child applies inference to their own current reading and records inferences with text evidence in the reading notebook.",
                },
                "guided_practice": [
                    "Daily inference moment in current reading: one stated, one implied, with evidence",
                    "Weekly nonfiction inference: what does the author imply?",
                    "Stated-versus-implied sort tasks on prepared passages",
                ],
                "independent_practice": [
                    "Run inference automatically during chapter book reading",
                    "Record memorable inferences with evidence in the reading notebook",
                ],
                "mastery_check": [
                    "Distinguishes stated from implied",
                    "Cites text evidence for inferences",
                    "Discriminates inference from guess",
                ],
                "spiral_review": [
                    "Return to earlier inferences in the reading notebook; check that the evidence still supports them",
                ],
            },
            "classical": {
                "narrative_introduction": (
                    "Reading between the lines is the mark of the educated reader. Ancient writers prized the reader "
                    "who could draw the implied meaning, the moral, the unspoken truth. To infer is to honor a text by "
                    "reading what it really says, both on the surface and beneath."
                ),
                "memory_work": {
                    "chants": [
                        "Recite the rule: I think X because the text says Y",
                        "Recite the discipline: an inference rests on text evidence; a guess does not",
                    ],
                    "recitations": [
                        "Memorize a short passage rich in implication and recite it; discuss what the passage implies as well as states",
                    ],
                },
                "copywork": [
                    "Copy a sentence rich in implication into the copybook; write below it 'this implies _____ because _____'",
                ],
                "recitation_routine": "At each reading session the child names one inference with evidence from the day's reading.",
                "history_integration": "Reading history depends heavily on inference: a historical document or letter implies much that is not stated. Letters of George Washington or Anne Frank's diary practice inference under real conditions.",
                "read_aloud_suggestions": [
                    "Books with strong characterization that imply much through action: Charlotte's Web, The Wind in the Willows, The Lion the Witch and the Wardrobe",
                    "Short stories with a turn or twist that depend on the reader's inference",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "Living books that imply more than they state; books whose characters reveal themselves through action",
                ],
                "short_lesson_flow": "During reading, pause at moments where the text implies something not stated. The child names the implication and the text evidence. Inference becomes a habit woven into reading aloud, not a separate exercise.",
                "narration_prompt": "What did the text say about this moment? What did it imply about how the character felt? What in the words made you think so?",
                "real_world_objects": [
                    "The reading notebook for recorded inferences",
                    "A wall card with the I-think-X-because-the-text-says-Y frame",
                ],
                "nature_connection": "Nature observation invites inference: tracks in the snow imply an animal; pressed grass implies it bedded down; the broken branch implies wind or weight. Nature reading and text reading share the same discipline.",
                "habit_focus": "The habit of attention to implication. The careful reader notices what is shown without being told.",
            },
            "montessori": {
                "prepared_materials": [
                    "Inference card sets: a short passage on one side, possible inferences on the other, with text-evidence prompts",
                    "Stated-versus-implied sort cards",
                    "Inference-versus-guess sort cards",
                    "A reading notebook for the child's own inferences with evidence",
                ],
                "presentation": {
                    "three_period_lesson": "This is what the text says; this is what the text implies; this is the text evidence. Show me what the text says; show me what the text implies. Is this stated or implied?",
                    "steps": [
                        "The guide presents an inference with explicit naming of stated, implied, and evidence",
                        "The child sorts stated-versus-implied cards",
                        "The child works through inference-versus-guess sorts",
                        "The child applies inference to their own reading and keeps an inference log",
                        "Across the term the child runs inference fluently without explicit framing",
                    ],
                },
                "control_of_error": "The control is the text itself: an inference holds if the evidence really is in the text. The child can always return to the passage to check.",
                "abstraction_pathway": "From sorting prepared cards, to making inferences with explicit frame, to running inference automatically during reading.",
                "extensions": [
                    "Unreliable narration and how it complicates inference",
                    "Inference about an author's stance in persuasive writing",
                    "Inference across multiple texts (what do two accounts of the same event together imply?)",
                ],
                "observation_focus": "Watch for spontaneous inferences with evidence during reading discussion. Watch for the child distinguishing supported inference from unsupported guess.",
            },
            "unschooling": {
                "invitations": [
                    "Talk about characters' feelings and motives during shared reading; welcome the child's interpretations",
                    "Discuss advertising, news, and shows in inference terms: what is the maker implying without saying?",
                    "Read picture books that imply more than they state; talk about what is shown but not told",
                ],
                "real_world_contexts": [
                    "Reading other people's feelings in everyday social life",
                    "Reading what advertising and media imply",
                    "Reading body language, tone, silence, and other non-spoken signals",
                ],
                "conversation_starters": [
                    "What do you think the character was feeling? What made you think so?",
                    "Is that something the text actually says, or something you figured out from what the text says?",
                    "What is the writer or maker hinting at without saying it out loud?",
                ],
                "resource_bank": [
                    "Picture books that imply rather than state (Chris Van Allsburg, Anthony Browne)",
                    "Wordless picture books and short films for inference practice",
                    "Family conversations about characters, motives, and implications",
                ],
                "parent_role": "Model inference openly. Share your own inferences about characters and situations with the I-think-X-because-the-text-says-Y frame. Welcome the child's inferences and ask 'what made you think so?'",
                "observation_documentation": "Note when the child spontaneously talks about a character's implied feeling, motive, or situation; note when the child distinguishes supported inference from guess. These are the real markers of internalization.",
            },
        },
        "connections": {
            "math": "Reading word problems demands inference: what is the problem really asking? what is implied by the numbers?",
            "science": "Reading science writing demands inference: what does the data suggest beyond what the writer states? what is the experiment's implied conclusion?",
            "history": "History writing is built on inference: a letter, a treaty, a journal entry implies much about a person or period beyond what is stated",
            "writing": "Strong writing implies as well as states; learning to read for implication informs the child's own writing toward show-don't-tell technique",
        },
    },
    "rd-15": {
        "enriched": True,
        "learning_objectives": [
            "Identify an author's purpose in a passage as one of the four common purposes: inform, persuade, entertain, or explain",
            "Recognize the text clues that reveal each purpose: tone, structure, word choice, evidence, vivid description, opinion words",
            "Identify the intended audience the author is writing for (children, adults, specialists, general readers)",
            "Recognize that one passage may have more than one purpose, with one purpose primary",
            "Apply purpose-and-audience reading to advertising and persuasive nonfiction as critical reading skill",
        ],
        "teaching_guidance": {
            "introduction": (
                "Building on genre identification (rd-05) which named fiction versus nonfiction, author's purpose asks "
                "the deeper question: WHY did the author write this? At this band the four common purposes are: "
                "INFORM (give the reader facts: encyclopedia entries, science writing, news), PERSUADE (move the "
                "reader to think or do something: ads, editorials, opinion pieces), ENTERTAIN (give the reader "
                "pleasure: novels, stories, poems, jokes), and EXPLAIN (show the reader how something works or why "
                "something happened: how-to writing, instructional writing). Closely related: WHO is the author "
                "writing for? Different audiences (children, adults, specialists) get different writing. Purpose plus "
                "audience together teach the child to read CRITICALLY: not only what the text says but why it says it "
                "and to whom. This is the foundation of media literacy."
            ),
            "scaffolding_sequence": [
                "Introduce the four common purposes with one clear example of each: an encyclopedia entry (inform), an ad (persuade), a chapter from a chapter book (entertain), a how-to recipe (explain)",
                "Show the text clues for each purpose: inform uses facts and neutral tone; persuade uses opinion words ('best', 'must', 'should') and emotional appeal; entertain uses vivid description and story structure; explain uses steps, sequence words, and how-or-why structure",
                "Practice the discrimination on a set of short passages: read each, name the purpose, name one text clue",
                "Introduce audience: who is the author writing for? Compare a children's encyclopedia entry on whales with a marine biology textbook on the same topic. Same purpose; different audience; very different writing.",
                "Move to mixed-purpose passages: a science writer might both inform and entertain; a memoir might both entertain and persuade. Name the primary purpose and the secondary purpose.",
                "Apply the skill to advertising: every ad is persuade-purpose; what are the persuasion techniques? what claims does it make? what does it leave out?",
                "Apply the skill to news versus opinion: a news article informs (or tries to); an opinion piece persuades. Show the child examples of each from a real newspaper or magazine.",
                "Sustain the practice across genres and texts so 'why did the author write this?' becomes a habit alongside 'what did the author say?'",
            ],
            "socratic_questions": [
                "Why do you think the author wrote this? To inform, persuade, entertain, or explain?",
                "What in the text makes you think that? Tone, word choice, structure, evidence, opinions?",
                "Who is the author writing for? How can you tell?",
                "Is this trying to convince you of something? What is it trying to convince you of, and how?",
                "Could this passage have more than one purpose? Which is primary?",
            ],
            "practice_activities": [
                "Purpose identification on prepared short passages: read each, name purpose and one text clue",
                "Purpose-and-audience sort cards: a stack of short passages sorted into inform / persuade / entertain / explain piles",
                "Same-topic-different-purpose comparison: read two pieces on the same topic written for different purposes (e.g., an encyclopedia entry on dogs and an ad for dog food). Compare.",
                "Ad analysis: bring in or describe an ad; name its purpose (always persuade); name the persuasion techniques; name what the ad omits",
                "News-versus-opinion practice: read a news article and an opinion piece from the same publication; name how each reveals its purpose",
            ],
            "real_world_connections": [
                "Recognizing the purpose of an advertisement (always persuade) is core media literacy",
                "Distinguishing news from opinion in newspapers and online (the line is increasingly blurred and worth teaching young)",
                "Recognizing the purpose of school assignments, instructions, and consent forms",
                "Reading product packaging critically: which claims are informational, which are persuasive?",
                "Recognizing persuasion in everyday situations: a sibling asking for something, a friend recommending something, a sales pitch",
            ],
            "common_misconceptions": [
                "Believing all writing has one and only one purpose. Many passages mix purposes; the question is which is PRIMARY.",
                "Believing inform and explain are the same. Inform gives facts; explain shows how or why. Different purposes; different structures.",
                "Believing entertainment is the lowest purpose. All four purposes are equally important; great writing can serve any of them well.",
                "Believing only ads persuade. Opinion pieces, editorials, persuasive essays, and many social-media posts also persuade.",
                "Believing purpose is hidden. Purpose is usually clear from text clues if the reader looks for them.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Names the four common purposes and gives one example of each",
                "Identifies the purpose of an unfamiliar passage with text clues",
                "Identifies the intended audience and how the author addresses that audience",
                "Recognizes mixed purposes and names the primary purpose",
                "Applies purpose-and-audience reading to advertising and persuasive nonfiction",
            ],
            "proficiency_indicators": [
                "Identifies purpose with prompting",
                "Identifies audience with prompting",
            ],
            "developing_indicators": [
                "Cannot reliably distinguish the four purposes",
                "Treats all writing as the same regardless of purpose",
            ],
            "assessment_methods": [
                "scored purpose-identification items on prepared passages",
                "sort tasks across the four purposes",
                "ad analysis tasks",
                "real-time discussion of purpose during reading",
            ],
            "sample_assessment_prompts": [
                "Read this passage. What is the author's purpose? What text clue tells you?",
                "Sort these short passages into inform / persuade / entertain / explain piles.",
                "Read this advertisement. What is its purpose? What persuasion techniques are used? What is left out?",
                "Read this news article and this opinion piece on the same topic. How does each reveal its purpose?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What are the four common purposes for which an author writes?",
                "expected_type": "multiple_choice",
                "options": [
                    "Beginning, middle, end, epilogue.",
                    "Inform, persuade, entertain, explain.",
                    "Fiction, nonfiction, poetry, drama.",
                    "Comedy, tragedy, history, romance.",
                ],
                "correct_answer": "Inform, persuade, entertain, explain.",
                "hints": [
                    "Four reasons an author has for writing.",
                ],
                "explanation": (
                    "The four common author's purposes are: INFORM (give facts), PERSUADE (move the reader), ENTERTAIN "
                    "(give pleasure), and EXPLAIN (show how or why). These four cover most of what writers do."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is the purpose of an advertisement?",
                "expected_type": "multiple_choice",
                "options": [
                    "To inform you about a product.",
                    "To persuade you to buy or want the product.",
                    "To entertain you with funny pictures.",
                    "To explain how the product was made.",
                ],
                "correct_answer": "To persuade you to buy or want the product.",
                "hints": [
                    "Ads may inform or entertain on the surface, but their real purpose is something else.",
                ],
                "explanation": (
                    "Every advertisement has the same primary purpose: to persuade the reader to buy or want the "
                    "product. Ads may inform (give facts about the product) or entertain (be funny) along the way, "
                    "but persuasion is the goal. Recognizing this is the first step of media literacy."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "A passage uses words like 'best', 'must', 'should', and gives strong opinions. What is the most "
                    "likely purpose?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "Inform.",
                    "Persuade.",
                    "Entertain.",
                    "Explain.",
                ],
                "correct_answer": "Persuade.",
                "hints": [
                    "Opinion words and strong claims are clues to purpose.",
                ],
                "explanation": (
                    "Opinion words ('best', 'must', 'should'), strong claims, and emotional appeals are the text clues "
                    "of persuade-purpose writing. Inform-purpose writing uses neutral tone and presents facts without "
                    "trying to move the reader."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "A children's science book about volcanoes uses vivid description, sound words, and exciting "
                    "comparisons (a volcano is described as 'a mountain breathing fire'). What are the purposes, and "
                    "which is primary?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "Only inform.",
                    "Both inform and entertain, with inform primary; the vivid language is meant to teach about volcanoes in a memorable way.",
                    "Only entertain.",
                    "Only persuade.",
                ],
                "correct_answer": "Both inform and entertain, with inform primary; the vivid language is meant to teach about volcanoes in a memorable way.",
                "hints": [
                    "Mixed purposes are common; ask which one drives the rest.",
                ],
                "explanation": (
                    "The book combines two purposes. The primary purpose is to INFORM (it teaches about volcanoes); "
                    "the secondary purpose is to ENTERTAIN (vivid language and sound words keep the reader engaged). "
                    "Recognizing mixed purposes is more sophisticated than naming one alone."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "Pick a piece of writing in your home (a book, an ad, a sign, a letter, a packaging label). Name "
                    "its purpose and audience, with the text clues that reveal each."
                ),
                "expected_type": "text",
                "hints": [
                    "Anything written has a purpose and an audience; apply the four-purpose vocabulary.",
                ],
                "explanation": (
                    "A complete answer names the piece, the purpose (one of the four), the audience the author is "
                    "addressing, and the specific text clues for each. With practice the child runs purpose-and-"
                    "audience reading automatically on everything they encounter."
                ),
            },
        ],
        "assessment_items": [
            {
                "prompt": "For each of these four short passages, name the author's purpose and one text clue that reveals it.",
                "type": "open_response",
                "target_concept": "four_purpose_identification",
                "rubric": (
                    "Mastery: identifies all four purposes correctly with text clue for each. Proficient: three of four. "
                    "Developing: confuses purposes or cannot name clues."
                ),
            },
            {
                "prompt": "Read this advertisement. Name its purpose, the persuasion techniques used, and what the ad does not say or leaves out.",
                "type": "open_response",
                "target_concept": "ad_analysis_for_purpose",
                "rubric": (
                    "Mastery: identifies persuade purpose; names two or more techniques; names what the ad omits. "
                    "Proficient: identifies purpose and one technique. Developing: cannot read the ad critically."
                ),
            },
            {
                "prompt": "Read this passage. Identify the audience the author is writing for. How can you tell?",
                "type": "open_response",
                "target_concept": "audience_identification",
                "rubric": (
                    "Mastery: identifies audience with multiple text clues (vocabulary level, examples used, "
                    "assumptions made). Proficient: identifies audience with one clue. Developing: cannot identify "
                    "audience."
                ),
            },
        ],
        "resource_guidance": {
            "required": [
                "a small library of short passages representing the four purposes (an encyclopedia entry, an ad, a story excerpt, a how-to passage)",
                "a real advertisement (from a magazine, online, or junk mail) for analysis",
                "a news article and an opinion piece on the same topic for purpose comparison",
            ],
            "recommended": [
                "a wall card listing the four purposes with their text clues",
                "a children's magazine subscription (Cricket, Cobblestone, Highlights) for varied purposes in one place",
                "a media-literacy resource for older developing-band children",
            ],
        },
        "time_estimates": {"first_exposure": 30, "practice_session": 15, "assessment": 20},
        "accommodations": {
            "dyslexia": "Practice purpose identification on read-aloud passages. Use audio (a radio news segment versus a radio ad versus a podcast story) so purpose is heard, not decoded.",
            "adhd": "Brief purpose identification: one passage, one purpose, one clue. Repeat across several short sessions rather than one long session.",
            "gifted": "Move to subtler purposes: literary nonfiction that informs and entertains; persuasive essays that hide their persuasion behind information; satire whose purpose is layered. Introduce bias and propaganda concepts.",
            "visual_learner": "Use color-coded sort cards: blue for inform, red for persuade, green for entertain, yellow for explain. Visual sort builds the discrimination quickly.",
            "kinesthetic_learner": "Physically sort passage cards into four piles on the floor or table.",
            "auditory_learner": "Read purposes aloud and listen for tone differences. Tone (neutral, urgent, vivid, instructional) often signals purpose.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": (
                    "Today we learn to ask 'why did the author write this?' We name the four common purposes: inform, "
                    "persuade, entertain, explain. We learn the text clues that reveal each one. We learn that one "
                    "passage may have more than one purpose, with one primary. And we learn to read advertising and "
                    "persuasive writing critically."
                ),
                "gradual_release": {
                    "i_do": "Parent reads four short passages aloud, names each purpose, points out the text clues that reveal each one.",
                    "we_do": "Together with the child, work through several more passages, naming purpose and clues. Discuss mixed-purpose passages.",
                    "you_do": "Child identifies purpose and audience on assigned passages and on real-world materials they find at home.",
                },
                "guided_practice": [
                    "Daily purpose identification on a chosen short passage",
                    "Weekly ad analysis: one ad, examined for purpose and technique",
                    "Periodic news-versus-opinion practice",
                ],
                "independent_practice": [
                    "Apply purpose-and-audience reading automatically across all reading",
                    "Recognize and name persuasion in real-world contexts",
                ],
                "mastery_check": [
                    "Names the four purposes",
                    "Identifies purpose with text clues on unfamiliar passages",
                    "Reads advertising critically",
                ],
                "spiral_review": [
                    "Return to earlier ad analyses; have the techniques changed in the ads the child sees this week?",
                ],
            },
            "classical": {
                "narrative_introduction": (
                    "Ancient rhetoricians named the purposes of speech and writing carefully: to inform, to persuade, "
                    "to delight, to instruct. Aristotle and Cicero wrote on this directly. The educated reader has "
                    "always known to ask not only what a writer says but why they say it. The skill is older than "
                    "literacy itself."
                ),
                "memory_work": {
                    "chants": [
                        "Recite the four purposes: inform, persuade, entertain, explain",
                        "Recite the rule: every ad's purpose is to persuade",
                    ],
                    "recitations": [
                        "Memorize a brief definition of each purpose with one example",
                    ],
                },
                "copywork": [
                    "Copy a sentence from each purpose into the copybook; label each with its purpose",
                ],
                "recitation_routine": "At each reading session the child names the purpose of the day's passage with text evidence.",
                "history_integration": "Reading historical documents demands purpose identification: the Declaration of Independence persuades; an old recipe explains; a journal entertains and informs. The classical tradition of rhetoric is the parent of this skill.",
                "read_aloud_suggestions": [
                    "Anthologies with mixed-purpose pieces (informational essays, persuasive editorials, narrative stories) so the child meets each purpose in turn",
                    "Aesop's Fables and similar works where purpose mixes entertainment with moral instruction",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "Living books across the four purposes; the child meets each purpose in good company",
                ],
                "short_lesson_flow": "After reading, ask 'why did this writer write this?' and 'who were they writing for?'. Discuss briefly. Across weeks the child builds the habit of asking these questions of everything they read.",
                "narration_prompt": "What was the writer trying to do in this passage, and how could you tell?",
                "real_world_objects": [
                    "A wall card with the four purposes and their clues",
                    "A small folder for collecting examples of each purpose from real reading",
                ],
                "nature_connection": "Books about nature serve different purposes: a field guide informs; a poem about a tree entertains; an essay on conservation persuades. The same topic, different purposes; different writing.",
                "habit_focus": "The habit of asking why a writer wrote what they wrote. This is the habit of critical reading.",
            },
            "montessori": {
                "prepared_materials": [
                    "Sort cards for the four purposes: a passage on the card, the four purposes labeled on the sorting tray",
                    "Cards showing text clues for each purpose",
                    "A small library of real-world examples (an ad, a news clip, a story excerpt, a how-to passage)",
                    "A media-literacy work for ad analysis",
                ],
                "presentation": {
                    "three_period_lesson": "This is inform; this is persuade; this is entertain; this is explain. Show me inform; show me persuade. Is this inform or persuade?",
                    "steps": [
                        "The guide presents the four purposes with clear examples",
                        "The child sorts passage cards into the four piles",
                        "The child analyzes a real advertisement for purpose and technique",
                        "The child applies purpose identification to their own reading",
                        "Across the term purpose recognition becomes automatic",
                    ],
                },
                "control_of_error": "The control is the text and its clues: a sort can be checked by re-reading the passage and locating the purpose clues.",
                "abstraction_pathway": "From sorting prepared cards by purpose, to identifying purpose in unfamiliar passages, to reading advertising and media critically without prompting.",
                "extensions": [
                    "Bias and propaganda as advanced purpose questions",
                    "Mixed-purpose writing and how to weight purposes",
                    "Audience analysis beyond children-versus-adults",
                ],
                "observation_focus": "Watch for the child spontaneously naming purpose during reading. Watch for the child recognizing persuasion in everyday materials without prompting.",
            },
            "unschooling": {
                "invitations": [
                    "Talk about why writers, advertisers, and makers create what they create; welcome the child's noticing",
                    "Read the same topic across different purposes (a magazine article on dogs and a dog food ad) and discuss the differences",
                    "Welcome the child's critical reading of media they encounter; treat persuasion as something to name openly",
                ],
                "real_world_contexts": [
                    "Recognizing the purpose of ads in everyday life",
                    "Distinguishing news from opinion in shared reading",
                    "Reading product packaging, signs, and instructions with purpose-eyes",
                ],
                "conversation_starters": [
                    "Why do you think the writer wrote this?",
                    "Who do you think they were writing it for?",
                    "Is this trying to convince you of something? How is it doing it?",
                ],
                "resource_bank": [
                    "Newspapers, magazines, and websites with mixed-purpose content",
                    "Advertising in many forms for critical reading practice",
                    "Family conversation about media and persuasion",
                ],
                "parent_role": "Model critical reading of purpose. Talk openly about the persuasion in ads you encounter. Ask the child why they think a writer wrote what they wrote. Welcome the child's purpose-and-audience analysis as part of normal reading life.",
                "observation_documentation": "Note when the child spontaneously identifies the purpose of an ad, a news headline, or a sign. Note their growing critical reading of media.",
            },
        },
        "connections": {
            "math": "Math word problems are written to inform and explain; recognizing the purpose helps the child read them clearly",
            "science": "Science writing crosses multiple purposes: research papers inform; science journalism informs and entertains; advocacy writing persuades. Recognizing these is part of scientific literacy.",
            "history": "Historical documents serve purposes: laws persuade or instruct; chronicles inform; memoirs entertain and inform. Purpose-reading is central to historical literacy.",
            "writing": "Knowing the author's purposes lets the child choose their own purpose deliberately when writing; they learn to write to inform, persuade, entertain, or explain on purpose",
        },
    },
    "rd-16": {
        "enriched": True,
        "learning_objectives": [
            "Read classic fables (Aesop, Panchatantra, Anansi tales) and identify the moral or lesson each fable teaches",
            "Read classic fairy tales (Grimm, Perrault, Andersen, retellings from many cultures) and recognize common fairy tale elements and patterns",
            "Recognize the structural difference between fable and fairy tale: fables are short with a stated moral; fairy tales are longer with magical elements",
            "Identify recurring fairy tale conventions: 'once upon a time', threes (three brothers, three tasks), magical creatures, kings and queens, good and evil, happily ever after",
            "Compare versions of the same tale across cultures: many traditions have Cinderella-style tales, trickster tales, or origin tales",
        ],
        "teaching_guidance": {
            "introduction": (
                "rd-02 introduced chapter books; the child now meets the foundational literature of childhood: fables "
                "and fairy tales. These are the oldest stories in human culture, told in some form by every people. "
                "Fables (Aesop's tales, Anansi stories, Panchatantra) are short, often with animal characters, and "
                "carry a MORAL: a stated lesson at the end. Fairy tales (Grimm, Perrault, Andersen) are longer, "
                "carry MAGICAL ELEMENTS (witches, wishes, enchantments), and use recurring conventions ('once upon a "
                "time', threes, kings and queens, happily ever after). The child reads these as literature, recognizes "
                "their patterns, and notices that many cultures tell similar tales. Honest content note: traditional "
                "Grimm tales carry violence and frightening images; many children's editions soften these. Choose the "
                "edition that matches the child."
            ),
            "scaffolding_sequence": [
                "Begin with a small collection of Aesop's fables. Read several aloud; identify the moral of each.",
                "Introduce fables from other traditions: Anansi the Spider tales (West African), Panchatantra tales (Indian), Native American animal tales. Notice that many traditions teach lessons through animal stories.",
                "Move to fairy tales: start with familiar ones (Cinderella, Little Red Riding Hood, Three Little Pigs) before unfamiliar ones",
                "Identify the recurring fairy tale conventions: 'once upon a time' opening, threes (three brothers, three wishes, three tasks), magical creatures, kings and queens, the contest of good and evil, happily ever after",
                "Read Grimm and Perrault tales in good editions; honor the older, sometimes darker tone where the child is ready",
                "Read Hans Christian Andersen tales: more literary, more melancholy, ('The Little Match Girl', 'The Ugly Duckling'). Andersen wrote literary fairy tales rather than retelling folk tales.",
                "Compare versions of the same tale: Cinderella appears in hundreds of cultures (Yeh-Shen from China, Mufaro's Beautiful Daughters from Zimbabwe, Cendrillon from France). Notice the shared core and the cultural variations.",
                "Discuss what fairy tales and fables teach: courage, kindness, cleverness, caution, the consequences of greed or cruelty",
            ],
            "socratic_questions": [
                "What is the moral of this fable? In your own words.",
                "What fairy tale conventions did you notice in this story?",
                "How is this fairy tale similar to one you already know? How is it different?",
                "Why might so many cultures have a Cinderella-like story?",
                "What is the difference between a fable and a fairy tale?",
            ],
            "practice_activities": [
                "Daily fable or fairy tale read-aloud with brief discussion of moral or convention",
                "Moral identification: read a fable; in one sentence, state the moral",
                "Convention spotting: read a fairy tale; list the conventions used (opening, threes, magical creature, good vs evil, ending)",
                "Cross-cultural comparison: read two versions of the same tale (Cinderella from two cultures); name what is shared and what is different",
                "Story-pattern application: read a less familiar tale and predict what will happen based on conventions; check after",
            ],
            "real_world_connections": [
                "Recognizing fable and fairy tale patterns in modern stories, movies, and books",
                "Understanding cultural references: 'crying wolf', 'sour grapes', 'the goose that laid the golden egg' all come from fables",
                "Recognizing the moral or lesson in stories the child encounters",
                "Understanding that fairy tale patterns (the quest, the magical helper, the impossible task) appear in much modern fantasy literature",
                "Recognizing why stories like these have lasted for centuries: they teach what cultures want their children to know",
            ],
            "common_misconceptions": [
                "Believing fairy tales are only for very young children. Fairy tales are the literature of all ages; the same tales reward different readings as the reader grows.",
                "Believing fables and fairy tales are the same. They are different forms: fables are short with stated morals; fairy tales are longer with magical elements.",
                "Believing fairy tales are all European. Every culture has fairy tales; the Western canon is one tradition among many.",
                "Believing the moral of a fable is hidden. The moral is usually stated at the end (the line that begins 'And the moral is...').",
                "Believing fairy tales must be soft and sanitized. The traditional versions often carry violence, hardship, and dark themes; older editions reveal this.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Identifies the moral of a fable in own words",
                "Names several fairy tale conventions and recognizes them in unfamiliar tales",
                "Distinguishes fable from fairy tale by form",
                "Compares two versions of the same tale across cultures",
                "Has read a substantial body of fables and fairy tales across traditions",
            ],
            "proficiency_indicators": [
                "Identifies moral with prompting",
                "Names some fairy tale conventions",
            ],
            "developing_indicators": [
                "Treats every story the same regardless of form",
                "Cannot identify morals or conventions",
            ],
            "assessment_methods": [
                "moral identification on unfamiliar fables",
                "convention spotting on unfamiliar fairy tales",
                "cross-cultural comparison tasks",
                "discussion of read tales for understanding",
            ],
            "sample_assessment_prompts": [
                "Read this fable. State the moral in your own words.",
                "Read this fairy tale. List four conventions you recognized.",
                "Read these two Cinderella versions from different cultures. What is shared? What differs?",
                "Tell me about your favorite fable or fairy tale and why it matters to you.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is the difference between a fable and a fairy tale?",
                "expected_type": "multiple_choice",
                "options": [
                    "They are the same thing.",
                    "Fables are short with stated morals (often using animals); fairy tales are longer with magical elements and recurring conventions.",
                    "Fables are for adults; fairy tales are for children.",
                    "Fables are written down; fairy tales are spoken.",
                ],
                "correct_answer": "Fables are short with stated morals (often using animals); fairy tales are longer with magical elements and recurring conventions.",
                "hints": [
                    "Think about length, characters, and what each form teaches.",
                ],
                "explanation": (
                    "Fables are short tales (often with animal characters) that end with a stated moral or lesson. "
                    "Fairy tales are longer tales with magical elements, characters like kings and witches, and "
                    "recurring conventions ('once upon a time', threes, happily ever after). Both forms are old; both "
                    "teach; the structure differs."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Which of these is a common fairy tale convention?",
                "expected_type": "multiple_choice",
                "options": [
                    "Math problems.",
                    "Things happening in threes (three brothers, three tasks, three wishes).",
                    "Footnotes and citations.",
                    "Chapter numbers.",
                ],
                "correct_answer": "Things happening in threes (three brothers, three tasks, three wishes).",
                "hints": [
                    "Many fairy tale events come in threes.",
                ],
                "explanation": (
                    "Fairy tale conventions include 'once upon a time' openings, things happening in threes (three "
                    "brothers, three tasks, three wishes), magical creatures (witches, fairies, talking animals), "
                    "kings and queens, the contest of good and evil, and the happily-ever-after ending. The three-pattern "
                    "is one of the most universal."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "In Aesop's fable of the Tortoise and the Hare, what is the moral?",
                "expected_type": "multiple_choice",
                "options": [
                    "Always run as fast as you can.",
                    "Slow and steady wins the race.",
                    "Never race against a hare.",
                    "Tortoises are better than hares.",
                ],
                "correct_answer": "Slow and steady wins the race.",
                "hints": [
                    "Think about what each character did and what won.",
                ],
                "explanation": (
                    "The moral of the Tortoise and the Hare is 'slow and steady wins the race' (or 'persistence beats "
                    "speed without focus'). The hare was faster but lazy and overconfident; the tortoise was slow but "
                    "steady. The fable teaches a lesson about character and habit, not about who is literally faster."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "Many cultures have a Cinderella-like story (Yeh-Shen, Mufaro's Beautiful Daughters, Cendrillon, "
                    "Vasilisa). What does this suggest?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "Only one culture has the real version; the others are wrong.",
                    "Many cultures share themes (cruel stepmothers, hidden virtue, transformation, justice) and tell similar stories with cultural variations.",
                    "The stories were all copied from the same book.",
                    "Only adults can read these tales.",
                ],
                "correct_answer": "Many cultures share themes (cruel stepmothers, hidden virtue, transformation, justice) and tell similar stories with cultural variations.",
                "hints": [
                    "Common human themes appear in stories worldwide.",
                ],
                "explanation": (
                    "Common human themes (cruel stepmothers, hidden virtue, transformation, justice) appear in many "
                    "cultures, so many cultures tell Cinderella-like stories. Each culture shapes the tale with its "
                    "own setting, magical helpers, and details. The shared core teaches what cultures across the world "
                    "have valued."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "Pick a fairy tale you know. Name three conventions it uses and what those conventions add to the "
                    "story."
                ),
                "expected_type": "text",
                "hints": [
                    "Once upon a time, threes, magical helpers, kings, the good-evil contest, happily ever after.",
                ],
                "explanation": (
                    "A complete answer names three conventions, the tale they appear in, and what each adds (e.g., "
                    "the three-tasks convention builds rhythm and lets the hero learn through repetition). Recognizing "
                    "conventions makes the reader more powerful, not less moved by the tale."
                ),
            },
        ],
        "assessment_items": [
            {
                "prompt": "Read this fable. State the moral in your own words and explain how the events of the fable teach it.",
                "type": "open_response",
                "target_concept": "fable_moral_identification",
                "rubric": (
                    "Mastery: moral stated accurately in own words; clear connection to fable events. Proficient: "
                    "moral identified but in textbook phrasing without connection to events. Developing: cannot "
                    "identify moral."
                ),
            },
            {
                "prompt": "Read this fairy tale. List four conventions used and explain how each one functions in the story.",
                "type": "open_response",
                "target_concept": "fairy_tale_convention_analysis",
                "rubric": (
                    "Mastery: four conventions identified with function. Proficient: three conventions identified. "
                    "Developing: fewer than three or cannot explain function."
                ),
            },
            {
                "prompt": "Read these two Cinderella tales from different cultures. What is shared between them? What is different? Why might both versions exist?",
                "type": "open_response",
                "target_concept": "cross_cultural_tale_comparison",
                "rubric": (
                    "Mastery: identifies shared core and cultural variations; reasons about why similar tales appear "
                    "across cultures. Proficient: identifies similarities and differences without reasoning. "
                    "Developing: cannot compare."
                ),
            },
        ],
        "resource_guidance": {
            "required": [
                "an Aesop's Fables collection (any good children's edition)",
                "a fairy tale anthology (Grimm, Perrault, or Andersen retellings appropriate for the child's age)",
                "at least two cross-cultural fairy tale collections (West African Anansi tales; Asian, African, or Latin American fairy tales)",
            ],
            "recommended": [
                "Cinderella variations across cultures (Yeh-Shen, Mufaro's Beautiful Daughters) for comparison work",
                "Andersen's fairy tales (a literary fairy tale tradition distinct from folk retellings)",
                "Trickster tale collections (Anansi, Coyote, Br'er Rabbit) from various traditions",
                "Picture book retellings (Trina Schart Hyman, Jan Brett) for visual richness",
            ],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 20, "assessment": 25},
        "accommodations": {
            "dyslexia": "Read fairy tales aloud or use audiobooks. The genre is meant to be heard; the cadence of 'once upon a time' carries the form. Decoding load drops away when the tale is heard.",
            "adhd": "Short fables suit short attention. Build up to longer fairy tales gradually.",
            "gifted": "Move to longer, more literary fairy tales (Andersen, MacDonald's 'The Princess and the Goblin'). Introduce comparative folklore (how the Brothers Grimm collected and edited their tales).",
            "visual_learner": "Use richly illustrated editions (Trina Schart Hyman, Jan Brett). The visual tradition of fairy tales is part of the form.",
            "kinesthetic_learner": "Act out fables and fairy tales in family or small group. Many of these tales were originally performed or told aloud.",
            "auditory_learner": "Audiobooks of fairy tale collections (the storyteller tradition is alive in good audiobook narration). Listen to professional storytellers tell tales aloud.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": (
                    "Today we begin to read fables and fairy tales: the oldest stories in human culture. Fables are "
                    "short and end with a stated moral; fairy tales are longer and use magical elements and recurring "
                    "patterns. We learn the conventions of each form and meet the foundational tales from many cultures."
                ),
                "gradual_release": {
                    "i_do": "Parent reads an Aesop's fable aloud, states the moral, identifies it as a fable; then reads a familiar fairy tale, points out conventions as they appear.",
                    "we_do": "Together read fables and fairy tales; child identifies morals and conventions with support.",
                    "you_do": "Child reads independently from an anthology, identifies morals and conventions, and discusses tales with the family.",
                },
                "guided_practice": [
                    "Daily fable or fairy tale reading from the anthology",
                    "Moral or convention identification at each reading",
                    "Weekly cross-cultural comparison",
                ],
                "independent_practice": [
                    "Read fables and fairy tales widely",
                    "Recognize fairy tale patterns in modern stories and movies",
                ],
                "mastery_check": [
                    "States the moral of an unfamiliar fable",
                    "Names conventions in an unfamiliar fairy tale",
                    "Compares two cross-cultural tales",
                ],
                "spiral_review": [
                    "Return to favorite tales periodically; notice what the older reader sees that the younger reader missed",
                ],
            },
            "classical": {
                "narrative_introduction": (
                    "Fables and fairy tales are the foundation of literature. Aesop wrote in ancient Greece; the "
                    "Panchatantra was old in India long before Aesop; Anansi stories carry the wisdom of West "
                    "African peoples. These tales taught children for thousands of years and still teach. The "
                    "classical reader meets the oldest literature first; the rest builds on it."
                ),
                "memory_work": {
                    "chants": [
                        "Recite the moral of three favorite Aesop fables",
                        "Recite the openings of three fairy tales the child knows ('once upon a time...')",
                    ],
                    "recitations": [
                        "Memorize one short fable in full and recite it",
                        "Memorize the moral of the Tortoise and the Hare, the Boy Who Cried Wolf, the Ant and the Grasshopper",
                    ],
                },
                "copywork": [
                    "Copy a favorite fable's moral into the copybook",
                    "Copy the opening of a beloved fairy tale into the copybook",
                ],
                "recitation_routine": "At each reading session the child names the form (fable or fairy tale), the source culture if known, and the moral or main theme.",
                "history_integration": "Fables and fairy tales come from real historical sources: Aesop was a slave in ancient Greece; the Brothers Grimm collected German tales in the early 1800s; the Panchatantra was compiled in ancient India. Reading these tales is also a small history lesson.",
                "read_aloud_suggestions": [
                    "D'Aulaire's Book of Greek Myths (which contains fable-like origin tales)",
                    "Andrew Lang's Fairy Books (the Blue, Red, Green, and other 'colored' fairy books, classic collections)",
                    "Walter de la Mare's Stories from the Bible and other classic anthologies",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "Aesop's Fables (any well-illustrated children's edition)",
                    "Andrew Lang's Fairy Books",
                    "Grimm's Fairy Tales in a faithful but age-suited edition",
                    "Cross-cultural fairy tale collections",
                ],
                "short_lesson_flow": "Read one fable or fairy tale per reading session. Discuss briefly: what was the moral? What conventions did you notice? Across weeks the child builds a deep store of foundational tales.",
                "narration_prompt": "Tell me the tale in your own words. What was the moral or the lesson?",
                "real_world_objects": [
                    "A beautiful family edition of an Aesop or fairy tale anthology",
                    "A reading log of tales read with brief notes",
                ],
                "nature_connection": "Many fables use animal characters and natural settings; their moral often relates to natural wisdom (the ant's industry; the fox's cunning). Nature observation supports fable reading.",
                "habit_focus": "The habit of receiving a tale and reflecting on its meaning. Tales are not just for amusement; they are formation.",
            },
            "montessori": {
                "prepared_materials": [
                    "A small library shelf of fables and fairy tales the child can choose from independently",
                    "Cards showing fairy tale conventions with examples",
                    "Cross-cultural tale pairings: same theme, two cultures, for comparison work",
                    "Illustrated fable cards: image on one side, fable text on the other, moral named",
                ],
                "presentation": {
                    "three_period_lesson": "This is a fable; this is a fairy tale. Show me a fable; show me a fairy tale. Is this a fable or a fairy tale?",
                    "steps": [
                        "The guide reads aloud a fable and a fairy tale, naming each form's features",
                        "The child sorts tale cards into fable and fairy tale piles",
                        "The child reads independently from the shelf and identifies morals and conventions",
                        "The child compares cross-cultural tale pairs",
                        "Across the term the child develops a deep knowledge of foundational tales from many cultures",
                    ],
                },
                "control_of_error": "The tale text is the control: morals are stated at the end of fables; conventions are visible in fairy tales.",
                "abstraction_pathway": "From hearing tales told, to reading them independently, to recognizing their conventions in modern literature.",
                "extensions": [
                    "Cross-cultural folklore studies (a culture's tales tell what it values)",
                    "The history of fairy tale collecting (Grimm, Perrault, Andersen)",
                    "Modern fairy tale retellings and what they keep or change",
                ],
                "observation_focus": "Watch for the child returning to favorite tales again and again. Watch for the child recognizing fairy tale patterns in modern stories without prompting.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a beautiful, child-accessible collection of fables and fairy tales in the reading area",
                    "Read fables and tales aloud as a regular family practice; welcome the child's questions and observations",
                    "Notice fairy tale patterns in movies and shows the family watches together",
                ],
                "real_world_contexts": [
                    "Recognizing fairy tale patterns in modern fantasy literature (Harry Potter, Narnia, The Lord of the Rings)",
                    "Recognizing fable wisdom in everyday situations ('don't cry wolf', 'sour grapes')",
                    "Recognizing the universality of certain themes across cultures",
                ],
                "conversation_starters": [
                    "What did this tale make you think about?",
                    "Have you heard a story like this before?",
                    "What might this story be trying to teach?",
                ],
                "resource_bank": [
                    "A wide and deep home library of folk and fairy tales from many cultures",
                    "Audiobook collections of fables and fairy tales",
                    "Family storytelling traditions",
                ],
                "parent_role": "Tell the tales yourself if you can; the oral tradition is alive when a parent tells the story rather than reads it. Welcome the child's interpretations; do not insist on a single 'correct' reading of a tale.",
                "observation_documentation": "Note the tales the child returns to most often; the tale a child loves at one age says something about the child. Note the child's recognition of patterns in modern stories.",
            },
        },
        "connections": {
            "math": "Many fables (the Pied Piper, the Crow and the Pitcher) carry simple math or logic puzzles in their plots; the child can sometimes see the math under the story",
            "science": "Animal fables often draw on real animal behavior; comparing the fable's animal with the real animal teaches the move from folklore to natural science",
            "history": "Each tale tradition has a historical home: Aesop in Greece, Grimm in Germany, Anansi in West Africa. The tales are a soft introduction to the history of cultures.",
            "writing": "Children often write their own fables and fairy tales naturally; the conventions of the forms give the child a structure to build their own stories on",
        },
    },
    "rd-17": {
        "enriched": True,
        "learning_objectives": [
            "Read biographies and autobiographies of notable people at the child's reading level",
            "Identify key life events, achievements, and character qualities that made each person significant",
            "Distinguish biography (written about a person by someone else) from autobiography (written by the person)",
            "Recognize that biographies vary in honesty: hagiography idealizes; honest biography includes both strengths and flaws",
            "Make connections between a biographical subject's life context and their accomplishments",
        ],
        "teaching_guidance": {
            "introduction": (
                "Building on chapter book reading (rd-02), the child now reads biography and autobiography: the lives "
                "of real people. The form teaches the child that real people did real things, with effort, character, "
                "and often hardship. Strong biography names KEY EVENTS (the moments that shaped the person), "
                "ACHIEVEMENTS (what they accomplished and why it mattered), and CHARACTER QUALITIES (the traits that "
                "made the accomplishment possible). Distinguish BIOGRAPHY (written about a person) from AUTOBIOGRAPHY "
                "(written by the person themselves). Honest content note: many children's biographies are HAGIOGRAPHIC "
                "(presenting the subject as a saint without faults); good biography includes both strengths and "
                "flaws, both achievements and mistakes. Choose biographies that honor the child's intelligence."
            ),
            "scaffolding_sequence": [
                "Begin with the David Adler / Kathleen Krull / Russell Freedman tradition of well-written biographies for children",
                "Start with figures the child already knows by name: George Washington, Harriet Tubman, Helen Keller, Jackie Robinson, Marie Curie, Anne Frank, Leonardo da Vinci",
                "Practice the three-part frame: key events, achievements, character qualities. Read a biography; identify each.",
                "Distinguish biography from autobiography: read examples of each; note the first-person voice in autobiography",
                "Move beyond the single canonical figure: read biographies of people in the same field across cultures (scientists from many countries; civil rights leaders from many movements)",
                "Introduce the idea of honest biography: a person's flaws and mistakes are part of the real story; idealizing them teaches less than the honest account",
                "Read short autobiography: passages from Helen Keller, Anne Frank, Roald Dahl's Boy, Ji-li Jiang's Red Scarf Girl",
                "Make life-context connections: how did the person's time and place shape what they did? what might they have done if born in a different era?",
            ],
            "socratic_questions": [
                "What were the key events of this person's life?",
                "What did they achieve? Why did it matter?",
                "What character qualities made the achievement possible?",
                "What was difficult or imperfect about this person? How does honest reading of their flaws help us understand them?",
                "How did their time and place shape what they could and could not do?",
            ],
            "practice_activities": [
                "Three-part frame practice: read a biography; in three sentences, name key events, achievements, character qualities",
                "Biography-versus-autobiography sort: read short passages, label each form, name the clue (third person versus first person)",
                "Cross-cultural figure pairing: read biographies of two scientists, two leaders, or two artists from different cultures; compare their lives and contexts",
                "Honest biography practice: read a biography that includes the subject's flaws; discuss how the flaws make the achievements clearer",
                "Subject choice and reading: child picks a figure they want to know about; reads a biography about them; presents what they learned",
            ],
            "real_world_connections": [
                "Recognizing biography as the form most adult nonfiction reading takes (history, science writing, memoir)",
                "Recognizing biographical accounts in news (profiles of public figures, athletes, artists)",
                "Family biography: hearing the life stories of grandparents and family members",
                "Recognizing autobiography in interview formats: podcasts and articles where people tell their own stories",
                "Understanding that every person's life is a kind of biography; their own life is the autobiography they are still writing",
            ],
            "common_misconceptions": [
                "Believing biography is the same as fiction. Biographies are nonfiction; events and details are meant to be true, even when narrative is used.",
                "Believing biography subjects were always great. People who did great things were often ordinary in many ways and flawed in others; honest biography shows this.",
                "Believing biography means hero-worship. Biography means accurate portrayal; a strong biography lets the reader judge the subject rather than telling them how to feel.",
                "Believing only famous people get biographies. Many strong biographies are of ordinary people whose lives illuminate a time or place.",
                "Believing autobiography is more honest than biography. Autobiography can hide as much as it reveals; both forms require critical reading.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Identifies key events, achievements, and character qualities of a biographical subject",
                "Distinguishes biography from autobiography",
                "Recognizes when a biography is hagiographic versus when it is honest",
                "Makes life-context connections (how did time and place shape the person)",
                "Has read a substantial body of biographies across fields and cultures",
            ],
            "proficiency_indicators": [
                "Identifies key events and achievements with prompting",
                "Distinguishes biography from autobiography with prompting",
            ],
            "developing_indicators": [
                "Cannot identify what made a subject significant",
                "Treats biography as just another story",
            ],
            "assessment_methods": [
                "three-part frame writing on assigned biographies",
                "biography-versus-autobiography sort",
                "cross-cultural biography comparison",
                "discussion of read biographies for depth of understanding",
            ],
            "sample_assessment_prompts": [
                "Read this biography. Name three key events, the subject's main achievement, and two character qualities.",
                "Read these passages. Which is biography and which is autobiography? How can you tell?",
                "Read these two biographies of scientists. How were their lives shaped by their times?",
                "Tell me about a biography you read recently. Why was the subject significant?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is the difference between a biography and an autobiography?",
                "expected_type": "multiple_choice",
                "options": [
                    "There is no difference.",
                    "A biography is written about a person by someone else; an autobiography is written by the person themselves.",
                    "A biography is fiction; an autobiography is nonfiction.",
                    "A biography is long; an autobiography is short.",
                ],
                "correct_answer": "A biography is written about a person by someone else; an autobiography is written by the person themselves.",
                "hints": [
                    "Bio = life; the auto-prefix means self.",
                ],
                "explanation": (
                    "A biography is the story of a person's life written by someone else (third person). An "
                    "autobiography is the story of a person's life written by that person themselves (first person). "
                    "Both are nonfiction; both tell about a real life; the voice differs."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "When reading a biography, what three things should you look for to understand why the person was "
                    "significant?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "Their height, weight, and birthday.",
                    "Key life events, achievements, and character qualities.",
                    "Their favorite color, food, and hobby.",
                    "How many siblings they had.",
                ],
                "correct_answer": "Key life events, achievements, and character qualities.",
                "hints": [
                    "Three things that explain why the person mattered.",
                ],
                "explanation": (
                    "Key events shaped the person's life. Achievements are what they accomplished. Character qualities "
                    "are the traits that made the achievements possible. These three together explain why a person was "
                    "significant and how their life unfolded."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "A biography says only good things about its subject and leaves out any mistakes or flaws. What "
                    "kind of biography is this?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "An honest biography.",
                    "A hagiographic biography (one that idealizes its subject without showing their flaws).",
                    "An autobiography.",
                    "A fictional biography.",
                ],
                "correct_answer": "A hagiographic biography (one that idealizes its subject without showing their flaws).",
                "hints": [
                    "When a biography only praises, something is missing.",
                ],
                "explanation": (
                    "Hagiographic biography (the word comes from the Greek for 'writing about saints') idealizes its "
                    "subject without showing flaws. Honest biography includes both strengths and flaws; the flaws make "
                    "the achievements clearer and the person more real. Critical readers recognize hagiography and "
                    "look for honest accounts."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "Why does the time and place a person lives in matter for understanding their biography?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "It doesn't; people achieve the same things regardless of time and place.",
                    "Time and place shape what is possible and what is hard; a scientist in 1850 worked differently from one today; a leader in one country faced different challenges from one in another.",
                    "Only the time matters, not the place.",
                    "Only the place matters, not the time.",
                ],
                "correct_answer": "Time and place shape what is possible and what is hard; a scientist in 1850 worked differently from one today; a leader in one country faced different challenges from one in another.",
                "hints": [
                    "Context shapes a life; a person's choices happen within their world.",
                ],
                "explanation": (
                    "Time and place shape what is possible, what is difficult, and what counts as significant. "
                    "Marie Curie's achievements in physics took place when women were rarely admitted to laboratories. "
                    "Harriet Tubman's work happened under slavery in the United States. Understanding the context "
                    "deepens understanding of the person."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "Read a biography of your choice. Write three sentences: key events, achievements, character qualities."
                ),
                "expected_type": "text",
                "hints": [
                    "One sentence on each part of the three-part frame.",
                ],
                "explanation": (
                    "A complete answer names the biography read, then writes one sentence each on the three parts of "
                    "the frame. With practice this kind of brief summary becomes natural and is a real reader's tool "
                    "for absorbing biographical reading."
                ),
            },
        ],
        "assessment_items": [
            {
                "prompt": "Read this assigned biography. Write a three-sentence summary using the key-events / achievements / character-qualities frame.",
                "type": "open_response",
                "target_concept": "biography_three_part_frame",
                "rubric": (
                    "Mastery: three sentences, one per part, all accurate. Proficient: three sentences but one part "
                    "weak. Developing: cannot apply the frame."
                ),
            },
            {
                "prompt": "Read these two biographies of figures from different cultures who did similar work. Compare their lives. How did their times and places shape what they did?",
                "type": "open_response",
                "target_concept": "cross_cultural_biography_compare",
                "rubric": (
                    "Mastery: identifies parallel work; names how context shaped each life; notes both similarities "
                    "and differences. Proficient: identifies parallels but weaker on context. Developing: cannot compare."
                ),
            },
            {
                "prompt": "Read this biography passage. Is it hagiographic (idealizing) or honest (including flaws as well as achievements)? Cite text evidence.",
                "type": "open_response",
                "target_concept": "honest_versus_hagiographic",
                "rubric": (
                    "Mastery: identifies the type with evidence; explains why the type matters for readers. "
                    "Proficient: identifies type with weak evidence. Developing: cannot distinguish."
                ),
            },
        ],
        "resource_guidance": {
            "required": [
                "biographies for children at the child's reading level (the David Adler 'A Picture Book of...' series and the Kathleen Krull 'Lives of...' series are widely available starting points)",
                "at least one autobiography or first-person account (Anne Frank's Diary in an age-suited edition; passages from Helen Keller's The Story of My Life)",
                "biographies of figures from multiple cultures and fields (science, art, history, civil rights, exploration)",
            ],
            "recommended": [
                "Russell Freedman's biographies (Lincoln, Eleanor Roosevelt, the Wright Brothers) as exemplars of strong children's biography",
                "Ji-li Jiang's Red Scarf Girl, Roald Dahl's Boy, and other accessible autobiographies",
                "Children's reference works on notable figures across history",
            ],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 20, "assessment": 25},
        "accommodations": {
            "dyslexia": "Read biographies aloud or use audiobooks. Many of the most engaging biographies for children are also strong audiobooks.",
            "adhd": "Picture book biographies (David Adler, Doreen Rappaport) suit shorter attention. Build up to longer biographies gradually.",
            "gifted": "Move to longer, more analytical biographies. Introduce the idea of historiography (how biographers approach their subjects differently). Read multiple biographies of the same figure and compare them.",
            "visual_learner": "Use illustrated biographies. The Kathleen Krull 'Lives of...' series uses portraits and visual elements heavily.",
            "kinesthetic_learner": "Pair biography reading with hands-on activity: build a small model of an invention, cook a food from a historical period, walk a famous historical route.",
            "auditory_learner": "Audiobook biographies and biographical podcasts. The audio form often works particularly well for biography.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": (
                    "Today we read biographies: the stories of real people who did real things. We learn the three-part "
                    "frame for understanding a biography: key events, achievements, character qualities. We distinguish "
                    "biography (about a person) from autobiography (by the person). We learn to read with honesty, "
                    "seeing both strengths and flaws."
                ),
                "gradual_release": {
                    "i_do": "Parent reads a biography aloud, names key events, achievements, and character qualities as they appear; demonstrates how to read for these.",
                    "we_do": "Together work through a second biography; child names elements with support.",
                    "you_do": "Child reads a biography of their choice, applies the three-part frame, and presents what they learned.",
                },
                "guided_practice": [
                    "Weekly biography reading from the family or library collection",
                    "Apply the three-part frame after each biography",
                    "Periodic cross-cultural biography comparison",
                ],
                "independent_practice": [
                    "Read biographies widely across fields and cultures",
                    "Begin to write brief biographical sketches of figures the child admires",
                ],
                "mastery_check": [
                    "Applies three-part frame to unfamiliar biographies",
                    "Distinguishes biography from autobiography",
                    "Recognizes honest versus hagiographic accounts",
                ],
                "spiral_review": [
                    "Return to biographies read earlier; what does the older reader see that the younger reader missed?",
                ],
            },
            "classical": {
                "narrative_introduction": (
                    "Plutarch wrote his Lives of the Greeks and Romans more than two thousand years ago, and his "
                    "biographies are still read. The classical tradition holds biography as essential reading: the "
                    "study of great lives shapes the reader's own character. The classical reader meets virtuous and "
                    "flawed figures alike and reflects on their lives."
                ),
                "memory_work": {
                    "chants": [
                        "Recite the three-part frame: key events, achievements, character qualities",
                        "Name three figures from each major era the child is studying (ancient, medieval, modern)",
                    ],
                    "recitations": [
                        "Memorize one short passage from a notable autobiography or biography",
                    ],
                },
                "copywork": [
                    "Copy a notable quotation from a biographical subject (Lincoln, Anne Frank, Marie Curie) into the copybook with attribution",
                ],
                "recitation_routine": "At each biography reading the child gives a one-paragraph oral summary using the three-part frame.",
                "history_integration": "Biography is the soul of history at this level. Read biographies of the major figures of each historical period the child studies; the events of history become the lives of the people who lived them.",
                "read_aloud_suggestions": [
                    "Children's adaptations of Plutarch's Lives (if available; otherwise modern biographical anthologies of ancient figures)",
                    "Russell Freedman's biographies of major figures (Lincoln, the Wright Brothers, Eleanor Roosevelt)",
                    "Lives of leaders, scientists, artists, and reformers across cultures",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 25,
                "living_book_suggestions": [
                    "Russell Freedman's biographies as exemplars of the living biography",
                    "Kathleen Krull's 'Lives of...' series for shorter biographical sketches",
                    "Autobiographies suited to the child's age: Helen Keller, Anne Frank (in age-suited editions), Roald Dahl",
                ],
                "short_lesson_flow": "Read a chapter or section of a biography during reading time. Narrate. Across weeks the child reads the full biography and absorbs the person's life.",
                "narration_prompt": "Tell me about this person's life. What did they do, and what qualities made it possible?",
                "real_world_objects": [
                    "A reading log of biographies read with brief notes",
                    "A wall of portraits of figures the child has read about",
                ],
                "nature_connection": "Read biographies of naturalists and scientists (Audubon, Beatrix Potter, John Muir, Rachel Carson, Jane Goodall) whose work emerged from nature observation. Their lives and their nature work entwine.",
                "habit_focus": "The habit of attentive reading of a person's life; the habit of looking for what made their life significant rather than skimming.",
            },
            "montessori": {
                "prepared_materials": [
                    "A shelf of biographies of figures from many cultures and fields",
                    "Cards for each biographical subject with portrait, key events, and main achievement",
                    "A timeline (paper or fabric) where the child places biographical subjects in their historical context",
                    "A biography-versus-autobiography sort set",
                ],
                "presentation": {
                    "three_period_lesson": "This is a key event; this is an achievement; this is a character quality. Show me a key event from this person's life. Is this an achievement or a character quality?",
                    "steps": [
                        "The guide introduces the three-part frame with a worked example",
                        "The child reads a biography from the shelf and applies the frame in writing or speaking",
                        "The child places the subject on the timeline",
                        "The child compares biographies of two figures from different times or cultures",
                        "Across the term the child develops a wide knowledge of significant lives",
                    ],
                },
                "control_of_error": "The biography itself is the control: the reader can return to it to verify events, achievements, and qualities.",
                "abstraction_pathway": "From picture-book biographies, to longer biographies, to autobiographies and primary sources, to writing one's own brief biographical sketches.",
                "extensions": [
                    "Reading multiple biographies of the same figure to compare interpretations",
                    "Reading primary sources (letters, diaries) alongside biography",
                    "Beginning genealogical work on the family's own history",
                ],
                "observation_focus": "Watch for the child's growing curiosity about real lives. Watch for the child seeking out biographies on their own.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a wide collection of biographies in the home and visible",
                    "Tell stories from your own life and your family's; oral biography is the start",
                    "Welcome the child's interest in any figure; help them find a good biography on that person",
                ],
                "real_world_contexts": [
                    "Watching documentaries and biographical films together",
                    "Hearing grandparents and relatives tell their life stories",
                    "Recognizing biographical content in news, podcasts, and shows",
                ],
                "conversation_starters": [
                    "Whose life would you most like to read about? Why?",
                    "What is the most interesting thing you learned about this person?",
                    "What qualities did they have that you might want to develop?",
                ],
                "resource_bank": [
                    "A wide and varied biography collection in the home library",
                    "Documentary films and biographical podcasts",
                    "Family oral history",
                ],
                "parent_role": "Be a biographer yourself: tell the child about your life, your parents' lives, your relatives' lives. Welcome the child's biographical curiosity. Read biographies alongside the child.",
                "observation_documentation": "Note which figures the child is drawn to. Note what they take from a life: not the facts but the qualities and questions.",
            },
        },
        "connections": {
            "math": "Biographies of mathematicians (Pythagoras, Newton, Ramanujan, Emmy Noether, Katherine Johnson) make math feel like a human enterprise",
            "science": "Biographies of scientists ground the science the child is learning in the lives of those who discovered or invented it",
            "history": "Biography and history are continuous at this level; the events of history are the lives of the people who lived them",
            "writing": "Writing brief biographical sketches of family members or admired figures is a natural extension; biography teaches the structure of nonfiction narrative",
        },
    },
    "rd-18": {
        "enriched": True,
        "learning_objectives": [
            "Use headings and subheadings to predict what a section is about and to find specific information quickly",
            "Use captions to extract information about images, photos, diagrams, and maps in nonfiction",
            "Use bold words to identify key terms that the text will define or use repeatedly",
            "Use a glossary at the back of a book to look up unfamiliar key terms",
            "Use a table of contents and an index to locate specific information in a nonfiction book",
        ],
        "teaching_guidance": {
            "introduction": (
                "Foundational nonfiction reading (rf-09) and chapter book reading (rd-02) gave the child the building "
                "blocks of nonfiction. Text features are the navigation tools the child needs to read nonfiction "
                "efficiently. HEADINGS and SUBHEADINGS organize a text into sections; the reader scans these to "
                "preview content and to locate specific information. CAPTIONS carry the meaning of images, photos, "
                "diagrams, and maps. BOLD WORDS mark key terms the text will define. A GLOSSARY at the back gives "
                "definitions; a TABLE OF CONTENTS at the front lists chapters; an INDEX at the back lists topics "
                "alphabetically with page numbers. Strong nonfiction readers use all these features fluently; weak "
                "readers ignore them and lose efficiency."
            ),
            "scaffolding_sequence": [
                "Begin with a well-designed children's nonfiction book (DK, Scholastic, National Geographic Kids). Open to a page and name every text feature on it.",
                "Practice using headings to predict: read the heading, predict what the section will discuss, then read to check",
                "Practice reading captions for content: cover the text, read the caption of an image, name what the image is about, then read the text to confirm",
                "Practice bold-word notice: scan a page for bold words; predict that each will be defined nearby; check by finding the definition in the surrounding text or glossary",
                "Practice using the glossary: encounter a bold word; turn to the back of the book to look it up; return to the text",
                "Practice using the table of contents: 'Find the section on volcanoes' becomes 'open the table of contents, find the relevant chapter, turn to that page'",
                "Practice using the index: 'Find pages that mention sharks' becomes 'turn to the index, find sharks, list the pages, turn to each one'",
                "Apply text-feature reading to research-style tasks: the child has a question, uses the features to locate the answer in a nonfiction book",
            ],
            "socratic_questions": [
                "What is this section about? What in the heading told you?",
                "What does this caption tell you that the image alone doesn't?",
                "What bold words are on this page? Where is each one defined?",
                "Where in this book would you go to find information about X?",
                "How do the text features help you read this book faster and better?",
            ],
            "practice_activities": [
                "Text-feature spotting: open a nonfiction page; list every text feature visible (heading, subheading, caption, bold word, sidebar, map, diagram, etc.)",
                "Heading-prediction practice: read a heading; predict the section's content; read to check",
                "Caption-only practice: cover the text; read only captions of images; produce a brief summary of what the page is about",
                "Glossary use: track use of the glossary across a week of nonfiction reading; note words looked up",
                "Information-locating task: given a question and a nonfiction book, use the table of contents and the index to find the answer",
            ],
            "real_world_connections": [
                "Reading textbooks (math, science, history) efficiently using text features",
                "Reading magazines and websites where headings, captions, and bold words structure the page",
                "Reading reference works (encyclopedias, field guides, cookbooks) using table of contents and index",
                "Reading newspapers and online news where headlines and captions organize the page",
                "Reading manuals and instructions where headings break information into useable steps",
            ],
            "common_misconceptions": [
                "Believing headings are decoration to skip. Headings carry meaning; skipping them costs comprehension and speed.",
                "Believing captions are optional. Captions often carry information the text doesn't repeat; skipping them misses content.",
                "Believing bold words are just style. Bold words mark key terms; the text will define them and use them repeatedly.",
                "Believing the table of contents and index are for adults. These are tools the child can and should use from this band on.",
                "Believing fluent reading means reading every word in order. Fluent nonfiction reading uses text features to skim, scan, and dive selectively.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Names and uses the common text features (heading, subheading, caption, bold word, glossary, table of contents, index)",
                "Uses headings to predict and to locate sections",
                "Uses captions to extract image information",
                "Uses the glossary to look up bold words",
                "Uses the table of contents and the index to locate specific information",
            ],
            "proficiency_indicators": [
                "Recognizes text features but uses them inconsistently",
                "Uses some features but not others",
            ],
            "developing_indicators": [
                "Reads nonfiction as if it were continuous prose, ignoring text features",
                "Cannot locate specific information in a nonfiction book",
            ],
            "assessment_methods": [
                "text-feature spotting tasks on prepared nonfiction pages",
                "information-locating tasks using table of contents and index",
                "real-time observation: does the child use features automatically during nonfiction reading?",
                "scored answers to questions that require text-feature use",
            ],
            "sample_assessment_prompts": [
                "Open this nonfiction book. List five text features on this page and what each one tells you.",
                "Find the answer to this question in this book. Tell me how you used the table of contents or index.",
                "Read this page using only the headings and captions (cover the body text). What is this page about?",
                "Find three bold words on this page. Where is each one defined?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is a heading in a nonfiction book?",
                "expected_type": "multiple_choice",
                "options": [
                    "Decoration; you can skip it.",
                    "A title for a section that tells you what the section is about.",
                    "The first word of every paragraph.",
                    "Words that are in capital letters.",
                ],
                "correct_answer": "A title for a section that tells you what the section is about.",
                "hints": [
                    "Headings introduce sections.",
                ],
                "explanation": (
                    "A heading is a title for a section of a book, telling the reader what the section will be about. "
                    "Subheadings divide sections further. Strong readers use headings to predict, preview, and locate "
                    "content. Headings are not decoration; they are navigation."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": (
                    "You want to find information about whales in a book about ocean animals. Which tool helps you "
                    "most?"
                ),
                "expected_type": "multiple_choice",
                "options": [
                    "The cover.",
                    "The table of contents or the index.",
                    "The author's biography.",
                    "The dedication page.",
                ],
                "correct_answer": "The table of contents or the index.",
                "hints": [
                    "Both list where to find information; the index lists topics alphabetically.",
                ],
                "explanation": (
                    "The table of contents (at the front) lists chapters and sections in order; the index (at the "
                    "back) lists topics alphabetically with page numbers. Either tool helps you find whales quickly. "
                    "Fluent nonfiction readers use both."
                ),
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What does a bold word in a nonfiction book usually signal?",
                "expected_type": "multiple_choice",
                "options": [
                    "The word is angry.",
                    "The word is a key term that the text will define or use repeatedly.",
                    "The word is misspelled.",
                    "The word is unimportant.",
                ],
                "correct_answer": "The word is a key term that the text will define or use repeatedly.",
                "hints": [
                    "Bold print marks importance.",
                ],
                "explanation": (
                    "Bold words mark key terms the author wants the reader to notice. These terms are typically "
                    "defined nearby (in the surrounding text or in a glossary at the back). Bold words are a signal: "
                    "stop here, learn this term, expect to meet it again."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "What is the purpose of a caption under an image in a nonfiction book?",
                "expected_type": "multiple_choice",
                "options": [
                    "Decoration.",
                    "To tell you what the image is showing and to add information about it that the text may not repeat.",
                    "To name the artist.",
                    "Captions are optional and most readers skip them.",
                ],
                "correct_answer": "To tell you what the image is showing and to add information about it that the text may not repeat.",
                "hints": [
                    "Captions extend the image into language.",
                ],
                "explanation": (
                    "A caption identifies what the image is showing and often adds information the text does not "
                    "repeat (the date a photo was taken, the location, a specific name, a scientific note). Strong "
                    "readers read captions; weak readers skip them. Captions are real content."
                ),
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": (
                    "Pick a nonfiction book in your home. Open to a page. Use the text features (headings, captions, "
                    "bold words, glossary, table of contents, index) to navigate. Describe how each one helped you "
                    "understand the page faster."
                ),
                "expected_type": "text",
                "hints": [
                    "Use as many features as the page offers.",
                ],
                "explanation": (
                    "A complete answer names the book, the page, the features used, and what each contributed. With "
                    "practice this kind of feature-aware reading becomes automatic; the child reads nonfiction much "
                    "faster and with better comprehension than a reader who ignores features."
                ),
            },
        ],
        "assessment_items": [
            {
                "prompt": "Open this assigned nonfiction page. Identify five text features and explain what each one tells you.",
                "type": "open_response",
                "target_concept": "text_feature_identification",
                "rubric": (
                    "Mastery: five features named with clear explanation of each. Proficient: four features. "
                    "Developing: three or fewer, or cannot explain function."
                ),
            },
            {
                "prompt": "I need to find information about (specific topic) in this book. Use the table of contents or index to find it. Show me how.",
                "type": "open_response",
                "target_concept": "information_locating_task",
                "rubric": (
                    "Mastery: locates information using table of contents or index efficiently, explains process. "
                    "Proficient: locates with prompting. Developing: cannot locate."
                ),
            },
            {
                "prompt": "Read this page using only the headings and captions (cover the body text). In one sentence, what is this page about? Then uncover the text and check.",
                "type": "open_response",
                "target_concept": "headings_and_captions_only_reading",
                "rubric": (
                    "Mastery: accurate one-sentence summary from features alone; close match after uncovering text. "
                    "Proficient: summary general but accurate. Developing: cannot use features alone."
                ),
            },
        ],
        "resource_guidance": {
            "required": [
                "well-designed children's nonfiction books with rich text features (DK Eyewitness series, National Geographic Kids, Scholastic nonfiction)",
                "a children's encyclopedia or reference book with table of contents and index",
                "a textbook the child uses for any subject, as a real-world site for text-feature practice",
            ],
            "recommended": [
                "a magazine subscription with strong design (National Geographic Kids, Kids Discover) for text-feature practice in a different medium",
                "field guides (birds, trees, rocks) where text features carry much of the information",
                "cookbooks, which use headings, captions, and indexes heavily and offer real-world feature use",
            ],
        },
        "time_estimates": {"first_exposure": 30, "practice_session": 20, "assessment": 25},
        "accommodations": {
            "dyslexia": "Practice text-feature reading on books with large clear print. Audio versions help with text bodies, but headings, captions, and bold words still need to be visually used. Verbal naming of features supports the visual recognition.",
            "adhd": "Brief text-feature spotting sessions: one page, one feature focus per session. Build up across days.",
            "gifted": "Move to denser reference works (junior versions of encyclopedias, atlases, almanacs) where text-feature fluency unlocks much faster reading.",
            "visual_learner": "Use highlighters or sticky notes to mark different text features on a sample page with consent of book owner; color-code headings, captions, bold words.",
            "kinesthetic_learner": "Physical scavenger hunts: 'find a heading; find a caption; find a bold word; find the glossary entry for that word' across the book.",
            "auditory_learner": "Say each text feature aloud and what it does. Discuss the function of each feature in conversation.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": (
                    "Today we learn the navigation tools of nonfiction. Strong nonfiction readers use headings to "
                    "predict, captions to extract image information, bold words to spot key terms, the glossary to "
                    "look them up, the table of contents to find chapters, and the index to find topics. Weak readers "
                    "ignore these features and read more slowly with less comprehension."
                ),
                "gradual_release": {
                    "i_do": "Parent opens a nonfiction book, points out every text feature on a page, names what each does and demonstrates use.",
                    "we_do": "Together work through a nonfiction page using all the text features.",
                    "you_do": "Child uses text features independently on their own nonfiction reading; uses table of contents and index to answer specific questions.",
                },
                "guided_practice": [
                    "Daily text-feature use during nonfiction reading",
                    "Weekly information-locating tasks using table of contents and index",
                    "Periodic feature-only reading: extract meaning from headings and captions alone",
                ],
                "independent_practice": [
                    "Use text features automatically across all nonfiction reading",
                    "Apply text-feature skills to textbooks and reference materials",
                ],
                "mastery_check": [
                    "Identifies all common text features",
                    "Uses table of contents and index efficiently",
                    "Reads nonfiction faster and with better comprehension using features",
                ],
                "spiral_review": [
                    "Periodically test feature use on unfamiliar nonfiction books",
                ],
            },
            "classical": {
                "narrative_introduction": (
                    "The book itself is an invention; the table of contents, the index, the page number, and the "
                    "heading were all developed over centuries to help readers find what they needed. Medieval "
                    "manuscripts had no page numbers; the index was a revolution in scholarship. To use these tools "
                    "is to honor the long tradition of careful reading."
                ),
                "memory_work": {
                    "chants": [
                        "Recite the common text features: heading, subheading, caption, bold word, glossary, table of contents, index",
                        "Recite the rule: headings predict; captions extend; bold words mark key terms; glossary defines; table of contents lists chapters; index lists topics",
                    ],
                    "recitations": [
                        "Memorize the order of the front matter and back matter in a typical book (title page, table of contents, body, glossary, index)",
                    ],
                },
                "copywork": [
                    "Copy three well-formed headings from a current nonfiction book into the copybook as models of concise informative title-writing",
                ],
                "recitation_routine": "At each nonfiction reading the child names a text feature they used and what it told them.",
                "history_integration": "The history of the book is itself worth a lesson: how the table of contents, the index, the page number, the chapter, the heading, and the caption developed across centuries to make reading more efficient.",
                "read_aloud_suggestions": [
                    "Well-structured reference books used together; pause periodically to talk about how the features help",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "Living nonfiction books with strong design (Holling C. Holling's Paddle-to-the-Sea has captioned illustrations; many high-quality children's nonfiction books carry rich features)",
                ],
                "short_lesson_flow": "During nonfiction reading, pause briefly to name and use the text features. Across weeks the child uses features automatically. Do not separate feature-instruction from reading; weave them together.",
                "narration_prompt": "Tell me about the page. What did the heading tell you? What did the captions show?",
                "real_world_objects": [
                    "A handful of well-designed children's nonfiction books in the reading area",
                    "A magnifying glass or a finger pointer to highlight features as they are noticed",
                ],
                "nature_connection": "Field guides are nature books that depend entirely on text features: each entry uses captions, bold names, and clear headings. Reading a field guide is a strong text-feature practice.",
                "habit_focus": "The habit of using the tools the book provides. The child who uses text features reads more efficiently and remembers more.",
            },
            "montessori": {
                "prepared_materials": [
                    "A small set of nonfiction books with rich text features available on the shelf",
                    "Text-feature cards: heading, subheading, caption, bold word, glossary, table of contents, index, each with explanation",
                    "Information-locating cards: questions to be answered using a specific book on the shelf",
                    "A magnifying glass and a card pointer for highlighting features as the child works",
                ],
                "presentation": {
                    "three_period_lesson": "This is a heading; this is a caption; this is a bold word; this is a glossary entry. Show me a heading; show me a caption. Is this a heading or a caption?",
                    "steps": [
                        "The guide presents each text feature with a worked example in a real book",
                        "The child sorts text-feature cards",
                        "The child uses features to answer information-locating cards",
                        "The child applies feature use to their own nonfiction reading",
                        "Across the term feature use becomes automatic",
                    ],
                },
                "control_of_error": "The book itself is the control: a wrong page can be checked against the index or table of contents.",
                "abstraction_pathway": "From naming and pointing to features, to using them deliberately to navigate, to using them automatically without thinking.",
                "extensions": [
                    "Reading textbooks for other subjects using feature fluency",
                    "Using primary reference works (atlas, encyclopedia, dictionary)",
                    "Beginning to design simple text features in the child's own writing (headings for a report)",
                ],
                "observation_focus": "Watch for the child using features without prompting during reading. Watch for the child reaching for the table of contents or index when they have a question.",
            },
            "unschooling": {
                "invitations": [
                    "Have well-designed nonfiction books, magazines, and reference works visible and accessible in the home",
                    "Use text features openly when reading nonfiction with the child; say 'let me check the index' or 'the caption says X'",
                    "Welcome the child's curiosity about reference works and let them spend time browsing",
                ],
                "real_world_contexts": [
                    "Using cookbooks (table of contents, index, headings)",
                    "Using field guides on walks (headings, captions, bold names)",
                    "Using websites and apps where headings and search are the text-feature equivalents",
                ],
                "conversation_starters": [
                    "Where in this book would we look up X?",
                    "What does the caption on this picture say?",
                    "How could we find the answer without reading the whole book?",
                ],
                "resource_bank": [
                    "Reference works (children's encyclopedia, atlas, almanac)",
                    "Field guides for nature interests",
                    "Magazines, cookbooks, manuals as everyday feature-rich texts",
                ],
                "parent_role": "Use text features visibly in your own reading. Show the child your own table-of-contents check or index lookup. Make feature use a natural part of family reading life.",
                "observation_documentation": "Note the child's spontaneous use of text features. Note the child reaching for index, table of contents, or glossary without being told.",
            },
        },
        "connections": {
            "math": "Math textbooks rely heavily on headings, bold terms, and indexes; text-feature fluency is essential for math learning",
            "science": "Science writing uses headings, captions on diagrams, bold key terms, and glossaries; mastering features is mastering science reading",
            "history": "History textbooks use timelines, maps, captions, and indexes; text-feature use is the key to reading history",
            "writing": "When the child writes their own nonfiction (a report, a short article), they can now use headings and captions deliberately to structure their writing",
        },
    },
}
