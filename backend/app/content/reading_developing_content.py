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
}
