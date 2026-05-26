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
                "Distinguish what the text says from what the reader assumed: 'where in the book does it actually say that?' — if the answer is 'it doesn't, I just thought so', name the assumption and look again",
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
}
