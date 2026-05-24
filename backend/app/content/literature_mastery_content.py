"""Literary mastery strand content.

Two node shapes live here: lit-craft-NNN (craft spine) and
lit-work-NNN / lit-work-inh-NNN (Western classics and the inheritance
canon). The schemas and validation are in app.services.node_content;
see literary_craft_node and literary_work_node in NODE_CONTENT_SCHEMA
and validate_literature.

Philosophy handling follows Option B: every node includes classical
and charlotte_mason as native dicts; the other philosophies are
included only where genuinely distinct, and otherwise recorded with a
reason in philosophy_neutral. Unschooling variants never carry lesson,
sequence, or graded-assessment keys.

This file holds the three gold-standard exemplars: lit-craft-031 (the
unreliable narrator), lit-work-001 (the Odyssey, classics), and
lit-work-inh-004 (Tolkien's The Lord of the Rings, inheritance). They
set the in-code bar against which the engines author the rest of the
strand.
"""

LITERATURE_MASTERY_CONTENT: dict[str, dict] = {
    "lit-craft-001": {
        "node_type": "craft",
        "strand": "close reading",
        "band": "emerging",
        "prerequisites": [],
        "objective": (
            "Notice exactly what the text says, in age-appropriate, concrete form: tell "
            "back a short passage in the writer's own words and name one specific word "
            "the writer chose, distinguishing what the text says from what we already "
            "knew or expected."
        ),
        "core_understanding": (
            "Reading begins with attention to the actual words on the page. Close "
            "reading is the habit of looking at what is there, not what is summarized, "
            "remembered, or wished for. At this band the seed of the habit is laid by "
            "listening, telling back, and pointing at one specific word the writer chose."
        ),
        "analytical_moves": [
            "Tell back what the text actually said, in the text's own words, when asked",
            "Point to one specific word the writer chose and say it aloud",
            "Distinguish what the text shows from what we already knew or expected",
            "Point to the exact phrase that gives evidence for what you think",
        ],
        "seminar_questions": [
            "What did the writer say, exactly?",
            "Which word did the writer choose for that, and what does that word make you picture?",
            "Does the story say so, or are we adding that?",
        ],
        "writing_invitations": [
            "Copy a single chosen sentence from the day's read-aloud and circle the word you noticed most",
            (
                "Draw the picture the chosen sentence puts in your mind and write one "
                "word from the sentence under your drawing"
            ),
        ],
        "exemplar_texts": [
            "A short, fine picture book read aloud (a Beatrix Potter tale; a McCloskey)",
            "A Mother Goose verse or a short Aesop fable",
            "A single page of a chapter book read one paragraph at a time (Charlotte's Web; Frog and Toad)",
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "The first habit of every reader is hearing the words exactly. We "
                    "listen to the line, tell it back, and say one specific word the "
                    "writer chose."
                ),
                "memory_work": {
                    "recitations": [
                        "A single short line from the day's read-aloud, recited",
                    ],
                },
                "copywork": [
                    "The recited line copied once, slowly, by hand",
                ],
                "recitation_routine": (
                    "Begin each session by reciting the line carried over from yesterday before the new line is met."
                ),
                "read_aloud_suggestions": [
                    "A short picture book or single page read aloud with care",
                    "A Mother Goose verse or a short Aesop fable",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A worthy picture book or chapter book, read aloud one page at a time",
                ],
                "short_lesson_flow": (
                    "Read a short passage aloud once, attentively. The child tells back "
                    "what they heard in their own words. Then we ask: which word stood "
                    "out? Which word did the writer choose? The smallest amount of text, "
                    "attended to truly, is the whole lesson."
                ),
                "narration_prompt": "Tell me what the writer said, just what was said.",
                "real_world_objects": [
                    "A worthy book in hand, not a worksheet",
                    "A small slip of paper for copying the noticed line",
                ],
                "nature_connection": (
                    "Close reading is to a sentence what looking is to a leaf: notice "
                    "exactly what is there, and name what you actually saw."
                ),
                "habit_focus": (
                    "The habit of attention: hearing the words as the writer wrote them, before any opinion is offered."
                ),
            },
            "traditional": {
                "introduction": "Explicit, modeled noticing on a short, age-appropriate passage.",
                "gradual_release": {
                    "i_do": (
                        "Teacher reads a single line aloud and names one specific word "
                        "the writer chose: 'The writer said small, not little. Small.'"
                    ),
                    "we_do": (
                        "Teacher reads the next line and, together with the child, names "
                        "one specific word the writer chose, saying it aloud."
                    ),
                    "you_do": (
                        "Child picks one specific word the writer chose from a new short "
                        "line, says it aloud, and then copies the line."
                    ),
                },
            },
            "unschooling": {
                "invitations": [
                    "Keep beautiful, well-written picture books and chapter books within reach",
                    "Read aloud often, slowly enough that any single word can be noticed",
                ],
                "real_world_contexts": [
                    "Bedtime stories, car-ride books, and the picture books the child returns to",
                    "The line of a song, rhyme, or read-aloud the child says back without prompting",
                ],
                "conversation_starters": [
                    "Did you hear that word? Which one stood out to you?",
                    "Want me to read that line again? It is a good one.",
                ],
                "resource_bank": [
                    "A shelf of worthy picture books and short read-alouds",
                    "A growing list of lines the child loved enough to ask about again",
                ],
                "parent_role": (
                    "Read aloud well, lingering on a word that pleases you so the child "
                    "hears that words are worth noticing. Welcome any word the child "
                    "names back, and trust that attention to words grows from being "
                    "delighted in them."
                ),
                "observation_documentation": (
                    "Over time, notice whether the child points at words on the page, "
                    "asks 'what did it say?' rather than restating, and remembers a "
                    "specific word from a story. This noticing replaces any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": (
                "Montessori at this level focuses on word-building, phonemic awareness, "
                "sentence analysis, and the grammar materials rather than a distinct "
                "close-reading method."
            ),
        },
    },
    "lit-craft-002": {
        "node_type": "craft",
        "strand": "close reading",
        "band": "developing",
        "prerequisites": ["close reading: emerging"],
        "objective": (
            "Name the practice of close reading and apply it with support: select a "
            "specific quotation from a text, restate what it actually says in the "
            "writer's own words, and offer a small inference grounded in the language on "
            "the page."
        ),
        "core_understanding": (
            "Close reading proceeds by quotation. The reader points at the exact words; "
            "what those words say (and only what they say) is the evidence. Inferences "
            "are welcome, but each must be grounded in the language. At this band the "
            "habit becomes named and conscious, and the child begins to copy chosen "
            "passages into a commonplace book of their own."
        ),
        "analytical_moves": [
            "Choose a single short passage worth attending to",
            "Quote it exactly, with quotation marks, and read it aloud once more",
            "Say what the passage literally says before saying what it suggests",
            "Distinguish the text's claim from one's own opinion, summary, or wish",
        ],
        "seminar_questions": [
            "What does this passage say, exactly? Which words?",
            ("What does it suggest beyond what it says directly, and which words make you think so?"),
            "Could two careful readers reach different inferences from the same words? Why?",
        ],
        "writing_invitations": [
            (
                "Choose a passage you find striking from today's reading and write a "
                "short paragraph quoting it and saying what the words actually say"
            ),
            ("Take a passage you have summarized and rewrite the analysis quoting the actual words instead"),
        ],
        "exemplar_texts": [
            (
                "A passage from a Newbery-honored novel (Charlotte's Web; The Lion, the "
                "Witch and the Wardrobe; Bridge to Terabithia)"
            ),
            "A short fable, parable, or folk tale",
            "A page of a Beatrix Potter tale or a passage of The Wind in the Willows",
            "A short poem suitable to the age (Stevenson's A Child's Garden of Verses)",
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "Close reading is now named as a habit, and the writer's exact words "
                    "become evidence in a small rhetorical practice. We choose the "
                    "passage, quote it, and reason from the words themselves."
                ),
                "memory_work": {
                    "recitations": [
                        "A chosen passage of two or three sentences, recited from memory",
                    ],
                },
                "copywork": [
                    "The chosen passage copied exactly into a commonplace book, with quotation marks",
                ],
                "recitation_routine": (
                    "Begin each session by reciting the previous session's chosen "
                    "passage; the new lesson opens from the recited words."
                ),
                "read_aloud_suggestions": [
                    "A chapter of a worthy novel, read aloud at the rate of one chapter a sitting",
                    "A short poem read aloud twice before discussion",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    (
                        "Living books of the first order at this age: Charlotte's Web, "
                        "The Wind in the Willows, the Narnia chronicles, Heidi"
                    ),
                ],
                "short_lesson_flow": (
                    "Read a passage aloud, attentively, then the child narrates it. "
                    "Together choose one striking sentence from the passage; the child "
                    "copies it into the commonplace book. Ask, gently: what do these "
                    "exact words say, and what do they suggest? The smallest analysis, "
                    "grounded in the chosen line."
                ),
                "narration_prompt": (
                    "Tell back what we read; then tell me which sentence you would keep "
                    "for your commonplace book, and what its words say."
                ),
                "real_world_objects": [
                    "A commonplace book in which chosen passages are copied",
                    "The living book itself, marked with small slips at chosen passages",
                ],
                "nature_connection": (
                    "Choosing a passage worth attending to is the same habit as choosing "
                    "a bird or a leaf worth attending to: notice exactly, hold it long "
                    "enough to copy, and let the writing record what looking found."
                ),
                "habit_focus": (
                    "The habit of grounding any inference in the words on the page rather "
                    "than in summary, memory, or wish."
                ),
            },
            "traditional": {
                "introduction": (
                    "Explicit instruction in selecting a passage, quoting it accurately, "
                    "and writing a short paragraph grounded in the words themselves."
                ),
                "gradual_release": {
                    "i_do": (
                        "Teacher chooses a passage, quotes it on the board with quotation "
                        "marks, says what the words literally say, and offers one small "
                        "inference, naming the words that support it."
                    ),
                    "we_do": (
                        "Class chooses a passage together, quotes it, restates it, and "
                        "weighs one or two possible inferences, defending each from the "
                        "words on the page."
                    ),
                    "you_do": (
                        "Student chooses a passage from the day's reading, quotes it "
                        "exactly, and writes a short paragraph saying what the words say "
                        "and what they suggest, naming the language that grounds the "
                        "inference."
                    ),
                },
                "independent_practice": [
                    "A short close-reading paragraph on a chosen passage, with the quotation set off and quoted accurately",
                ],
            },
            "unschooling": {
                "invitations": [
                    "Keep a commonplace book or notebook the child can use freely for lines they love",
                    "Read aloud often from books worth quoting and copy a favorite line yourself when one strikes you",
                ],
                "real_world_contexts": [
                    "A line from a favorite book copied to keep or share",
                    "A passage the child quotes back to a sibling or grandparent because they liked how it sounded",
                    "A line written into a card or note for someone the child cares about",
                ],
                "conversation_starters": [
                    "Want to copy that line? It is a good one.",
                    "What did those exact words say? Read it again.",
                    "Does the book say that, or are we adding it?",
                ],
                "resource_bank": [
                    "A commonplace book and good pens within reach",
                    "A shelf of well-written novels, poems, and tales worth quoting",
                ],
                "parent_role": (
                    "Be a fellow reader who quotes back what they loved. When the child "
                    "shares a line, ask gently what the words say before discussing what "
                    "they suggest; let real reading and real lines do the teaching."
                ),
                "observation_documentation": (
                    "Over time, notice whether the child begins to quote rather than "
                    "summarize when discussing a book, copies lines they love, and "
                    "distinguishes what the text says from what they add. This noticing "
                    "replaces any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": (
                "Montessori does not carry a distinct close-reading method at this band; "
                "literature work at this age stays within word study, sentence analysis, "
                "and the grammar materials rather than the analytical reading of passages."
            ),
        },
    },
    "lit-craft-003": {
        "node_type": "craft",
        "strand": "close reading",
        "band": "proficient",
        "prerequisites": ["close reading: developing"],
        "objective": (
            "Apply close reading independently to whole difficult works: locate passages "
            "that bear interpretive weight, hold a small original reading defensible "
            "from the words on the page, and articulate it in both spoken and written "
            "argument."
        ),
        "core_understanding": (
            "Close reading is no longer a discrete classroom exercise but a habit one "
            "brings to any text. The proficient reader trusts their own attention to "
            "find the passages that matter, and can defend a reading from the words "
            "themselves rather than from received opinion. This is the doorway to the "
            "Socratic seminar: the table at which a small original reading, well "
            "grounded, becomes the substance of the conversation."
        ),
        "analytical_moves": [
            "Read a difficult work whole, with attention, on first encounter",
            "Mark or note passages that bear interpretive weight as they are read",
            "Return to a marked passage and articulate why it matters to the work",
            "Build a short defensible reading from one or two specific passages",
            "Hear a different reading respectfully and name where in the text it draws its evidence",
        ],
        "seminar_questions": [
            "Which passage in this work feels most central to its meaning, and why?",
            "Where does this work invite more than one reading, and which words make it so?",
            "What does this writer let us see only by what they refuse to say?",
        ],
        "writing_invitations": [
            (
                "Write a short analytical paragraph defending one specific reading of a "
                "chosen passage, with the words quoted and the reading grounded line by line"
            ),
            (
                "Choose two passages from the same work that complicate each other and "
                "write the paragraph that holds them together"
            ),
        ],
        "exemplar_texts": [
            (
                "A novel of literary substance read whole (Pride and Prejudice; Jane "
                "Eyre; To Kill a Mockingbird; a great Russian novel in a worthy translation)"
            ),
            "A short story by a careful prose writer (Chekhov; Joyce's Dubliners; Flannery O'Connor)",
            "A whole poem by a poet whose lines reward sustained attention (Donne; Hopkins; Bishop)",
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "Close reading meets the Socratic seminar. The reader brings a "
                    "passage and a reading; the seminar tests both. Rhetoric and "
                    "interpretation begin to converse: what does the writer claim, and "
                    "by what words does the writer secure the claim?"
                ),
                "memory_work": {
                    "recitations": [
                        "A passage central to the work, recited from memory at the seminar's opening",
                    ],
                },
                "copywork": [
                    "The recited passage copied into a kept notebook of close-read passages",
                ],
                "recitation_routine": (
                    "Each seminar opens from a recited passage; the discussion takes its "
                    "first question from the lines just heard, and returns to the text "
                    "for every claim."
                ),
                "read_aloud_suggestions": [
                    "A chapter of the novel under study, read aloud at the seminar's opening",
                    "A short story read aloud whole before the discussion begins",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 45,
                "living_book_suggestions": [
                    "A worthy novel read whole at a sustained pace, not excerpted",
                    "A volume of short stories or poems read across a term, one at a sitting",
                ],
                "short_lesson_flow": (
                    "The proficient student reads the whole work at a sustained pace, "
                    "narrating each sitting. Passages worth attending to are slipped or "
                    "noted as they are met. At the end of a chapter or a poem, one or "
                    "two such passages are taken up: copied into the commonplace book, "
                    "discussed, and tested against the rest of the work. The habit is "
                    "now across the long span of a whole book, not the single page."
                ),
                "narration_prompt": (
                    "Tell back the chapter you read, and tell me which passage you "
                    "would set down as the one that bears most weight, and why."
                ),
                "real_world_objects": [
                    "The whole novel, marked with the reader's own slips at chosen passages",
                    "A commonplace book gathering passages across many works over the year",
                ],
                "nature_connection": (
                    "The proficient close reader is to a difficult book what a "
                    "naturalist of long practice is to a forest: at home in the whole, "
                    "able to notice the one thing worth attending to without losing the "
                    "view of all the rest."
                ),
                "habit_focus": (
                    "The habit of sustained attention across a whole work, and the habit "
                    "of returning to the text for evidence rather than relying on memory."
                ),
            },
            "traditional": {
                "introduction": (
                    "Explicit instruction in locating passages that bear interpretive "
                    "weight, in defending a reading from the words, and in writing the "
                    "short analytical paragraph that quotes its evidence."
                ),
                "gradual_release": {
                    "i_do": (
                        "Teacher reads a passage aloud, names what about its language "
                        "makes it bear weight in the work, and writes a short paragraph "
                        "defending one reading of it on the board, quoting the passage."
                    ),
                    "we_do": (
                        "Class chooses a candidate passage from the work under study, "
                        "weighs it against other candidates, and drafts a short paragraph "
                        "together defending one reading, quoting the passage line by line."
                    ),
                    "you_do": (
                        "Student locates a passage independently, drafts a short "
                        "analytical paragraph defending one specific reading of it, and "
                        "revises after hearing a peer's different reading at seminar."
                    ),
                },
                "independent_practice": [
                    "The analytical paragraph on a self-chosen passage from the work under study",
                    "A short revision of the paragraph after seminar discussion",
                ],
            },
            "unschooling": {
                "invitations": [
                    "Keep the long shelf: novels, story collections, and poems of real substance, available, never assigned",
                    "Keep a commonplace book and small slips for marking passages in books the reader cares about",
                ],
                "real_world_contexts": [
                    "A difficult book a student has chosen and loves, returned to and quoted from",
                    "A long evening conversation about a passage the student wanted to read aloud to someone",
                    "A piece of writing the student composed because a book moved them to write back",
                ],
                "conversation_starters": [
                    "Which passage in that book do you keep coming back to? Read it to me?",
                    "What do you think the writer is doing there, in those exact words?",
                    "Is there more than one way to read that? Which words make it so?",
                ],
                "resource_bank": [
                    "A shelf of difficult, worthy books available for the long pull",
                    "A reader-companion willing to discuss a chosen passage as a fellow reader",
                ],
                "parent_role": (
                    "Be a fellow reader who takes the student's chosen book seriously and "
                    "their chosen passage as seriously as one's own. Discussion follows "
                    "the student's reading; the parent contributes their own reading as "
                    "another reader at the table, not as an examiner."
                ),
                "observation_documentation": (
                    "Over time, notice whether the student returns to difficult books on "
                    "their own, marks passages, defends a reading from the words, and "
                    "hears a different reading without giving up their own. This noticing "
                    "replaces any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": (
                "Montessori's literature pedagogy at the elementary and early-secondary "
                "level does not carry a distinct method for the sustained close reading "
                "of whole difficult works; the practice here is drawn from the seminar "
                "tradition rather than from the prepared environment."
            ),
        },
    },
    "lit-craft-031": {
        "node_type": "craft",
        "strand": "narrative craft",
        "band": "advanced",
        "prerequisites": ["point of view: proficient", "close reading: proficient"],
        "objective": (
            "Recognize when a narrator's account cannot be fully trusted, identify the "
            "textual signals of unreliability, and analyze what the gap between the "
            "narrator's telling and the reader's inference does to a work's meaning."
        ),
        "core_understanding": (
            "A narrator is a constructed voice, not a window; the distance between what "
            "the narrator believes or claims and what the text lets the reader see is "
            "itself a source of meaning. Unreliability arises from naivety, "
            "self-deception, limited knowledge, or deliberate deception."
        ),
        "analytical_moves": [
            "Locate where the narrator's account conflicts with other evidence in the text",
            "Distinguish unreliability from simple limited perspective",
            "Ask what the author achieves by withholding a trustworthy voice",
            "Track how growing distrust reshapes earlier passages on reread",
        ],
        "seminar_questions": [
            "Where does the text first invite you to doubt the narrator, and how?",
            (
                "Is this narrator deceiving us, deceiving themselves, or simply unable to "
                "know, and does the distinction change the book?"
            ),
            "What does the author gain that a reliable narrator would lose?",
        ],
        "writing_invitations": [
            "Rewrite a scene from a reliable narrator's view and analyze what is lost",
            (
                "Write the analytical paragraph arguing for a specific source of a chosen "
                "narrator's unreliability, with textual evidence"
            ),
        ],
        "exemplar_texts": [
            "The governess in James's The Turn of the Screw",
            "Nabokov's Humbert",
            "Ishiguro's Stevens",
            "Poe's confessing narrators",
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "Framed as rhetorical analysis: how does the author persuade the reader past the narrator?"
                ),
                "memory_work": {
                    "recitations": [
                        "Recitation of a passage close-read for the signals of unreliability",
                    ],
                },
                "recitation_routine": (
                    "A Socratic seminar on where trust breaks and why, opening from the recited passage."
                ),
            },
            "charlotte_mason": {
                "short_lesson_flow": (
                    "A single attentive reading, then narration, then the question: did "
                    "you believe the teller, and when did that change? The student's own "
                    "dawning doubt is the way in."
                ),
                "narration_prompt": (
                    "Tell back what you read; then tell me whether you believed the teller, and when that changed."
                ),
                "real_world_objects": [
                    "The novel itself, read whole, not excerpted",
                    "A commonplace book in which the passages where trust shifts are copied",
                ],
            },
            "traditional": {
                "introduction": (
                    "Explicit instruction in the signals of unreliability, modeled "
                    "analysis, and an independent analytical paragraph."
                ),
                "gradual_release": {
                    "i_do": ("Teacher reads a passage aloud and names each signal of unreliability as it appears."),
                    "we_do": (
                        "Class works through a second passage together, surfacing signals "
                        "and weighing the source of the unreliability."
                    ),
                    "you_do": (
                        "Student writes an independent analytical paragraph naming the "
                        "source of a chosen narrator's unreliability, supported by textual "
                        "evidence."
                    ),
                },
                "independent_practice": [
                    "The analytical paragraph on a chosen narrator from the exemplar list",
                ],
            },
            "unschooling": {
                "conversation_starters": [
                    "Wait, do you believe this narrator? When did that change?",
                    ("If the narrator is lying, what does that do to what we thought happened earlier?"),
                ],
                "parent_role": (
                    "Discussion sparked by the student's own \"wait, I don't think we can "
                    'trust this guy" while reading something they chose; no imposed '
                    "apparatus, the insight followed where it arises."
                ),
                "observation_documentation": (
                    "Over time, notice whether the student begins to ask of any book "
                    "whose voice this is and whether to believe it. This noticing replaces "
                    "any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": "Montessori has no distinct doctoral-literature method for this skill.",
        },
    },
    "lit-work-001": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "The Odyssey",
            "author": "Homer",
            "date": "c. 8th century BCE",
            "genre": "epic",
            "form": "epic poem",
        },
        "minimum_band": "developing",
        "content_notes": ("Epic violence, including the killing of the suitors; honest information, not a gate."),
        "craft_focus": [
            "Narrative structure (in medias res, the frame, nested storytelling)",
            "The epic hero",
            "Theme: homecoming, hospitality, identity, cunning vs force",
            "The Homeric simile",
        ],
        "entry": (
            "Developing: follow and narrate the journey home and meet the idea of the "
            "hero and the long road. Proficient: structure and theme. Advanced: the "
            "Homeric simile, the ethics of hospitality, Odysseus's cunning as a value "
            "the poem examines rather than simply praises. Mastery: comparative reading "
            "against the Aeneid and what the poem holds up as virtue."
        ),
        "close_reading_passages": [
            "The proem and its statement of theme: what does the poem say it is about?",
            ("A Homeric simile, for how it works: what does the figure expand and what does it slow?"),
            "The recognition scene with the scar, for how identity is built and revealed.",
        ],
        "structural_analysis": (
            "The in-medias-res opening, the embedded first-person tale, the delayed "
            "homecoming, and what the structure does to the theme of identity and return."
        ),
        "thematic_lines": [
            "What the poem counts as virtue, and whether it fully endorses Odysseus",
            "Hospitality as the social order the poem cares about",
            "Homecoming as literal and interior journey",
        ],
        "comparative_threads": [
            "The Aeneid (the hero who founds vs the hero who returns)",
            "Later returns and journeys across the canon",
        ],
        "seminar_questions": [
            "Is Odysseus admirable, and does the poem think so entirely?",
            "Why does Homer begin in the middle and let Odysseus tell his own adventures?",
            "What does hospitality mean in this world, and what happens when it is broken?",
        ],
        "writing_invitations": [
            "Compose a Homeric simile of your own and analyze its parts",
            "The analytical essay on whether the poem endorses its hero",
            "At mastery, the comparative seminar paper with the Aeneid",
        ],
        "context": (
            "The oral epic tradition, the world of guest-friendship, the poem at the "
            "head of the Western canon; supplied as fact, interpretation left to the "
            "student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "The foundational great-books seminar text; the hero examined rhetorically and ethically."
                ),
                "memory_work": {
                    "recitations": ["Recitation of the proem"],
                },
                "recitation_routine": (
                    "Seminar opens from the recited proem; the discussion takes its first "
                    "question from the lines just heard."
                ),
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy translation of the Odyssey, read aloud as a living book",
                ],
                "short_lesson_flow": (
                    "A living book read aloud and narrated, the journey followed and told "
                    "back, deepening to analysis as the bands move up."
                ),
                "narration_prompt": (
                    "Tell back the part we read today, and tell me what you noticed about Odysseus this time."
                ),
            },
            "unschooling": {
                "invitations": [
                    ("Keep a worthy translation of the Odyssey on the shelf, available, never assigned"),
                ],
                "real_world_contexts": [
                    (
                        "Available and discussed where a student's interest in myth and "
                        "adventure leads, no imposed apparatus."
                    ),
                ],
                "parent_role": (
                    "Read aloud and discuss where the student's interest in myth and "
                    "adventure leads; no imposed apparatus."
                ),
                "observation_documentation": (
                    "Over time, notice whether the student returns to the poem and follows "
                    "its threads into other reading. This noticing replaces any test."
                ),
            },
            "traditional": {
                "introduction": "Structured study of epic conventions where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-inh-004": {
        "node_type": "work",
        "track": "inheritance",
        "work": {
            "title": "The Lord of the Rings",
            "author": "J.R.R. Tolkien",
            "date": "1954-55",
            "genre": "mythopoeic novel",
            "form": "novel",
        },
        "minimum_band": "proficient",
        "content_notes": ("War, death, and the corruption of power; honest information, not a gate."),
        "craft_focus": [
            "Invented mythology and world-building",
            "The heroic and the anti-heroic",
            "Theme: power and its renunciation, mercy, mortality",
            ("Literary inheritance: a modern author consciously rebuilding an ancient tradition"),
        ],
        "lineage": (
            "Tolkien, a scholar of Beowulf and Old Norse, set out to give England the "
            "mythology he felt it lacked. Read against its sources as craft: the "
            "dragon-sickness and cursed hoard from the Norse and Beowulf; the elegiac "
            "northern courage of facing certain defeat; the philological roots of the "
            "invented languages. The comparative work is the point."
        ),
        "entry": (
            "Proficient: read against its sources for inherited motif. Advanced: "
            "interlace structure, the long defeat and eucatastrophe, the temptation of "
            "the Ring. Mastery: the comparative seminar paper tracing a motif from "
            "Beowulf or the Eddas into Tolkien."
        ),
        "close_reading_passages": [
            (
                "An elegiac, ubi-sunt passage set beside the same note in Beowulf and the "
                "Eddas (Beowulf and Eddas quoted from public-domain translation; Tolkien "
                "analyzed, not reproduced)."
            ),
            "A passage on the temptation of the Ring, for how power is dramatized.",
        ],
        "structural_analysis": (
            "The interlace structure, the long defeat and the eucatastrophe (Tolkien's "
            "coined term), the found-manuscript frame."
        ),
        "thematic_lines": [
            "Whether the renunciation of power is the true subject",
            "Mercy (the sparing of Gollum) as the hinge of the plot",
            "Mortality as gift and burden",
        ],
        "comparative_threads": [
            "Beowulf (the dragon, the hoard, northern courage)",
            "The Volsunga Saga and the cursed ring",
            "Malory and the elegiac end of a heroic age",
            "Wagner's Ring for contrast and Tolkien's resistance to that comparison",
        ],
        "seminar_questions": [
            (
                "Tolkien said the book is about death and the desire for deathlessness, "
                "not power; reading it, which do you find truer?"
            ),
            "Why does the story turn on acts of mercy rather than strength?",
            "What did Tolkien take from Beowulf, what did he change, and why?",
        ],
        "writing_invitations": [
            ("The comparative essay tracing one motif from Beowulf or the Eddas into Tolkien"),
            (
                "An act of sub-creation: build a small consistent invented world or "
                "language fragment, then analyze what makes invented mythology cohere."
            ),
        ],
        "context": (
            "Tolkien's scholarship, the philological method, the early-twentieth-century "
            "moment and the Great War behind the long defeat; supplied as fact, "
            "interpretation left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "The seminar on inheritance and on power; the work as a modern entry in the epic tradition."
                ),
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "The Lord of the Rings, a living book of the first order",
                ],
                "short_lesson_flow": (
                    "A living book of the first order, read and narrated, then "
                    "comparative analysis as the bands move up."
                ),
            },
            "unschooling": {
                "invitations": [
                    "Keep The Lord of the Rings on the shelf, ready for whoever picks it up",
                ],
                "real_world_contexts": [
                    (
                        "A book children choose and love; followed where their passion "
                        "leads, the lineage discussed as curiosity opens it."
                    ),
                ],
                "parent_role": (
                    "Genuinely strong here; followed where the student's passion leads, "
                    "the lineage discussed as curiosity opens it, no imposed apparatus."
                ),
                "observation_documentation": (
                    "Over time, notice whether the student begins to chase the lineage "
                    "into Beowulf, the Eddas, or other rooted reading. This noticing "
                    "replaces any test."
                ),
            },
            "traditional": {
                "introduction": "Structured study of world-building and theme where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
}
