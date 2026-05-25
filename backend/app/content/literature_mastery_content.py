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
    "lit-craft-006": {
        "node_type": "craft",
        "strand": "narrative craft",
        "band": "emerging",
        "prerequisites": [],
        "objective": (
            "Notice whose voice is telling the story, in concrete, oral, age-appropriate "
            "form: say who is telling, and point to a place in the text where the teller "
            "appears."
        ),
        "core_understanding": (
            "Every story has a teller. Sometimes the teller is a person inside the "
            "story; sometimes the teller is a voice outside it. At the seed of point of "
            "view, the child learns to listen for who is talking and to notice when the "
            "'I' of the story is and is not the same person as the writer."
        ),
        "analytical_moves": [
            (
                "When listening to a story, say who is telling it: the writer, a "
                "character, or someone watching from outside?"
            ),
            "Point to a moment where the teller appears, using the word 'I' or speaking of themselves",
            (
                "Notice when the teller knows more than any one character could know, "
                "and when the teller knows only what one character knows"
            ),
        ],
        "seminar_questions": [
            "Who is telling us this story?",
            "How do you know it is them telling it?",
            "Do they see everything, or only what one person sees?",
        ],
        "writing_invitations": [
            (
                "After a read-aloud, draw the storyteller as you imagine them and write "
                "one word for who they are (a person in the story, or a voice outside it)"
            ),
            (
                "Tell a short story aloud from your own 'I' voice; then tell a short "
                "story as someone watching from outside; notice the difference"
            ),
        ],
        "exemplar_texts": [
            "A first-person picture book or short chapter book (the Frances books; Ramona, told about her)",
            "A folk tale told in the omniscient outside voice (a tale from Andrew Lang's fairy books)",
            "A simple first-person poem suitable to the age (a Stevenson from A Child's Garden of Verses)",
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "Before we name the kinds of teller, we first hear that there is a "
                    "teller. We listen, ask who is telling, and recite one line in the "
                    "teller's own voice."
                ),
                "memory_work": {
                    "recitations": [
                        "A single line in which the teller's voice can be plainly heard",
                    ],
                },
                "copywork": [
                    "The recited line copied once, slowly, with the teller named beneath it",
                ],
                "recitation_routine": (
                    "Each session begins by reciting yesterday's teller-line; the new "
                    "lesson opens with the question 'and who is telling today?'"
                ),
                "read_aloud_suggestions": [
                    "A first-person picture book whose 'I' voice is plain",
                    "A folk tale told in the outside, all-seeing voice, for contrast",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A worthy picture book or short chapter book whose teller is easily heard",
                ],
                "short_lesson_flow": (
                    "Read a short passage aloud, attentively. The child narrates. Then "
                    "ask: who is telling us this? How do you know? If today's voice is a "
                    "person in the story and yesterday's was not, set the two beside "
                    "each other and listen to the difference."
                ),
                "narration_prompt": "Tell back what we read, and tell me who is telling it.",
                "real_world_objects": [
                    "A worthy book in hand, not a worksheet",
                    "A small card on which the teller of the day's reading is named",
                ],
                "nature_connection": (
                    "Listening for who is telling is the same habit as listening for "
                    "which bird is singing: a particular voice with a particular sound, "
                    "noticed before any name for the kind of voice is offered."
                ),
                "habit_focus": (
                    "The habit of attention to voice: hearing that a story is being "
                    "told, and by whom, before any judgment of the story is offered."
                ),
            },
            "traditional": {
                "introduction": "Explicit, modeled identification of the teller on a short, age-appropriate passage.",
                "gradual_release": {
                    "i_do": (
                        "Teacher reads a passage aloud and names the teller plainly: "
                        "'This story is being told by a person inside it, by Frances, "
                        "and she calls herself I.'"
                    ),
                    "we_do": (
                        "Teacher reads a second passage and, together with the child, "
                        "names the teller and points to the words that show it."
                    ),
                    "you_do": (
                        "Child listens to a new short passage and names the teller "
                        "aloud, then points to the words that show it."
                    ),
                },
            },
            "unschooling": {
                "invitations": [
                    "Keep a mixed shelf of first-person and third-person picture books within reach",
                    "Read aloud often, and now and then wonder aloud who is telling this story",
                ],
                "real_world_contexts": [
                    "The picture book in which the child notices that the voice 'is talking to me'",
                    "A favorite bedtime story whose teller the child can name without prompting",
                    "The child telling a story of their own, choosing whether to use 'I' or 'she'",
                ],
                "conversation_starters": [
                    "Who is telling us this story?",
                    "Is it the writer, or someone in the story?",
                    "How do they know what they know?",
                ],
                "resource_bank": [
                    "A shelf with picture books in both first and third person",
                    "A growing little list of teller-voices the child has noticed",
                ],
                "parent_role": (
                    "Read aloud well, and when a teller's voice is striking, name it as "
                    "though you were noticing it for the first time. Welcome the child's "
                    "noticing without correction, and trust that the awareness of voice "
                    "grows from being delighted in."
                ),
                "observation_documentation": (
                    "Over time, notice whether the child begins to say things like 'this "
                    "one is the writer talking' or 'this one is a girl telling about "
                    "herself,' and whether the child sometimes shifts voices in their "
                    "own telling. This noticing replaces any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": (
                "Montessori at this band does not carry a distinct method for noticing "
                "the narrator of a story; the prepared environment centers on word study, "
                "sentence analysis, and the grammar materials rather than on questions "
                "of literary voice."
            ),
        },
    },
    "lit-craft-007": {
        "node_type": "craft",
        "strand": "narrative craft",
        "band": "developing",
        "prerequisites": ["point of view: emerging", "close reading: developing"],
        "objective": (
            "Name the point of view of a work: first person, third person, and within "
            "third the difference between omniscient and limited; identify the narrator "
            "as distinct from any character; quote a sentence that shows the choice."
        ),
        "core_understanding": (
            "Point of view is the writer's choice of who tells the story and how much "
            "that teller can know. Naming the choice is the first step in seeing why "
            "the writer made it. The terms first person, third person, omniscient, and "
            "limited are tools for that naming and, once they are in hand, become "
            "instruments for the close reading of any story."
        ),
        "analytical_moves": [
            "Identify the point of view of a whole work as first or third person",
            ("If first person, name who the narrator is, a character in the story or a voice from outside it"),
            (
                "If third person, ask whether the narrator knows everything (omniscient) "
                "or only what one character knows (limited)"
            ),
            "Quote a sentence that shows the point of view at work",
        ],
        "seminar_questions": [
            "Whose voice tells us this story, and how does that voice tell us?",
            ("What can we know because of who is telling, and what is hidden from us because of who is telling?"),
            "Would a different teller see this scene differently? How?",
        ],
        "writing_invitations": [
            ("Write a short paragraph naming the point of view of today's reading, with one quoted line that shows it"),
            (
                "Take a short scene you read and rewrite a few lines from a different "
                "point of view (first to third, or omniscient to limited); name what "
                "changed"
            ),
        ],
        "exemplar_texts": [
            "Sarah, Plain and Tall (Patricia MacLachlan), told in Anna's first person",
            "The Little House books (Laura Ingalls Wilder), told in third-person limited from Laura's view",
            (
                "Charlotte's Web (E.B. White), third-person omniscient, the narrator "
                "entering Wilbur, Charlotte, Templeton, and the humans by turns"
            ),
            "A short story by Beverly Cleary or Roald Dahl, examined for whose voice tells it",
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "The teller has kinds, and the kinds have names. First and third; "
                    "and within third, omniscient and limited. Naming the kind is the "
                    "first move of analysis; the rest follows from what each kind allows "
                    "and forbids the reader to know."
                ),
                "memory_work": {
                    "chants": [
                        (
                            "Chant the four POV terms in order: first person, third "
                            "person, omniscient, limited, and one example of each"
                        ),
                    ],
                    "recitations": [
                        "A sentence in which the chosen point of view is plainly at work",
                    ],
                },
                "copywork": [
                    "The recited POV-revealing sentence, copied with the kind named beneath it",
                ],
                "recitation_routine": (
                    "Each seminar opens by chanting the four terms and reciting "
                    "yesterday's POV-revealing line before the new work is opened."
                ),
                "read_aloud_suggestions": [
                    "A chapter of a first-person novel and a chapter of a third-person novel set side by side",
                    "A short story chosen for the clarity of its point of view",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    (
                        "Living books that show the variety of POV: Sarah, Plain and "
                        "Tall (first person); the Little House books (third-person "
                        "limited); Charlotte's Web (third-person omniscient)"
                    ),
                ],
                "short_lesson_flow": (
                    "Read a chapter aloud, attentively, and the child narrates. Then "
                    "ask: whose voice tells us this? Is it a person in the story, or a "
                    "voice from outside? If from outside, does it see only one person's "
                    "world, or all? Together name the kind, quietly; let the name "
                    "settle. Copy a sentence that shows the chosen voice into the "
                    "commonplace book."
                ),
                "narration_prompt": (
                    "Tell back what we read; then tell me whose voice told it, and read me one sentence that shows it."
                ),
                "real_world_objects": [
                    "Two living books in hand at once, one first person and one third, for comparing voices",
                    "A commonplace book in which POV-revealing sentences are gathered under each work's title",
                ],
                "nature_connection": (
                    "Naming a POV is like naming a bird from its song: a particular "
                    "voice has a particular sound and a particular range of what it "
                    "knows; once named, it can be heard again in any wood."
                ),
                "habit_focus": ("The habit of asking, of any book, whose voice this is, before asking what it means."),
            },
            "traditional": {
                "introduction": (
                    "Explicit instruction in the four point-of-view terms (first "
                    "person, third person, omniscient, limited), modeled identification "
                    "on a chosen passage, and a short paragraph naming the POV of a "
                    "whole work with quoted evidence."
                ),
                "gradual_release": {
                    "i_do": (
                        "Teacher reads a passage, names the point of view explicitly, "
                        "and quotes the sentence that shows it: 'This is third-person "
                        "limited; we are inside Laura's view only, and the line that "
                        "shows it is...'"
                    ),
                    "we_do": (
                        "Class identifies the POV of a second passage together, "
                        "drafting one sentence that names the kind and quoting the "
                        "evidence on the board."
                    ),
                    "you_do": (
                        "Student names the POV of a whole short work and writes a short "
                        "paragraph defending the identification with one quoted line."
                    ),
                },
                "independent_practice": [
                    "The short paragraph naming the POV of a chosen work, with one quoted line of evidence",
                    "A rewrite of a few lines of a scene from a different point of view, with a note on what changed",
                ],
            },
            "unschooling": {
                "invitations": [
                    "Keep a mixed shelf of first-person and third-person novels at the band, available, never assigned",
                    (
                        "When a child is reading and stops to comment on the voice of a "
                        "book, name the kind quietly so the language is there for the "
                        "next time"
                    ),
                ],
                "real_world_contexts": [
                    "A book the child loved enough to compare its voice to another book's voice",
                    "A piece of the child's own writing in which they chose a teller",
                    "A film, audiobook, or play in which the kind of teller is plain and discussed in passing",
                ],
                "conversation_starters": [
                    "Whose voice is telling this book? How can you tell?",
                    "Does the teller know everything, or only what one person knows?",
                    "How would this story sound if a different person told it?",
                ],
                "resource_bank": [
                    "A shelf of novels with clearly different points of view",
                    "A reader-companion who will name the kinds gently when the child notices them",
                ],
                "parent_role": (
                    "Read alongside the child and, when a voice strikes either of you, "
                    "name its kind in passing. Welcome the child's own attempts to "
                    "name; correct gently and only when it matters. Trust that the "
                    "habit of asking 'whose voice?' grows from reading widely with the "
                    "names available."
                ),
                "observation_documentation": (
                    "Over time, notice whether the child begins to name the kind of "
                    "teller in books they discuss, and whether they reach for a "
                    "POV-revealing sentence to settle a question. This noticing "
                    "replaces any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": (
                "Montessori at this band does not carry a distinct method for naming "
                "the point of view of a literary work; literature work here remains "
                "within the grammar materials and the practical study of language rather "
                "than the analytical apparatus of narrative voice."
            ),
        },
    },
    "lit-craft-008": {
        "node_type": "craft",
        "strand": "narrative craft",
        "band": "proficient",
        "prerequisites": ["point of view: developing", "close reading: proficient"],
        "objective": (
            "Identify the point of view of any literary work independently, including "
            "the variants of third person (omniscient, limited, free indirect discourse) "
            "and narrators whose distance from the action shifts; analyze how the chosen "
            "point of view shapes what the reader can see, feel, and know."
        ),
        "core_understanding": (
            "Point of view is not merely a technical choice but a structural and moral "
            "one. The writer's selection of teller and distance determines the reader's "
            "access: what is shown, what is hidden, whose interior we share, and whose "
            "remains opaque. The proficient reader treats POV as a writer's instrument "
            "and analyzes its consequences for what the work makes possible. This is "
            "the doorway from naming POV to using POV as an analytical lens, and the "
            "ground from which the unreliable-narrator question can be asked at all."
        ),
        "analytical_moves": [
            (
                "Identify the point of view of a whole literary work independently, "
                "including the variants of third person: omniscient, limited, and free "
                "indirect discourse"
            ),
            "Track shifts in narrative distance within a single work and ask what each shift does",
            "Analyze what the chosen point of view lets the reader see and what it withholds",
            "Argue for what the work gains by its specific point of view rather than another",
        ],
        "seminar_questions": [
            "What does this work let us see, and only us, because of its point of view?",
            ("Where does the narrator come closer to or further from the characters, and what happens there?"),
            "What would this work lose if it were told from a different point of view?",
        ],
        "writing_invitations": [
            (
                "Write an analytical paragraph naming the point of view of a whole work "
                "and arguing what the work gains by it, with the relevant passages quoted"
            ),
            (
                "Choose a passage of free indirect discourse and analyze how the "
                "narrator's voice and the character's voice blend, line by line"
            ),
        ],
        "exemplar_texts": [
            (
                "A novel that exploits third-person limited (To the Lighthouse moves "
                "between interior consciousnesses; Ishiguro's The Remains of the Day "
                "works the same effect from inside a first-person narrator)"
            ),
            (
                "A novel in third-person omniscient that comments on its characters "
                "(Middlemarch; War and Peace in worthy translation)"
            ),
            ("A novel of free indirect discourse (Pride and Prejudice; many of Joyce's Dubliners stories)"),
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "Point of view becomes a lens. The seminar asks not only whose voice "
                    "tells the work, but what this voice secures and what it loses; the "
                    "writer's chosen instrument is examined for what it can and cannot "
                    "play. The rhetorical question stands: how is the reader persuaded "
                    "of this seeing rather than another?"
                ),
                "memory_work": {
                    "recitations": [
                        (
                            "A passage of free indirect discourse, recited so the ear "
                            "may hear the narrator's voice and the character's voice "
                            "braided in the same line"
                        ),
                    ],
                },
                "copywork": [
                    (
                        "The recited free-indirect passage copied into a kept notebook "
                        "of POV-revealing passages, with the narrator's and the "
                        "character's words distinguished where possible"
                    ),
                ],
                "recitation_routine": (
                    "Each seminar opens from a recited passage that turns on its point "
                    "of view; the discussion takes its first question from what the "
                    "passage's chosen voice secures and what it withholds."
                ),
                "read_aloud_suggestions": [
                    "A chapter of a novel chosen for its handling of point of view, read aloud at the seminar's opening",
                    "A short story whose effect depends on its narrator (Joyce's Dubliners; a Henry James tale)",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 45,
                "living_book_suggestions": [
                    "A worthy novel whose point of view is consequential, read whole at sustained pace",
                    "A volume of short stories read across a term for variety of narrative voice",
                ],
                "short_lesson_flow": (
                    "The proficient student reads the whole work attentively, marking "
                    "passages where the narrator's distance shifts or where the voice "
                    "braids with a character's. At the end of a chapter or a story, two "
                    "or three such passages are taken up: read aloud, copied, and "
                    "discussed for what the chosen POV permits, withholds, and offers "
                    "the reader. The habit of attention to voice now bears the weight "
                    "of analytical work across a whole long book."
                ),
                "narration_prompt": (
                    "Tell back the chapter, and tell me which passage best shows how "
                    "this work's chosen voice changes what we can see; read it to me."
                ),
                "real_world_objects": [
                    "The whole novel marked at passages where POV does decisive work",
                    "A commonplace book gathering POV-revealing passages across many works over the year",
                ],
                "nature_connection": (
                    "Reading a work for its point of view is to a long novel what "
                    "tracking the movement of weather is to a long season: a habit of "
                    "attention to a thing that shapes everything else it touches."
                ),
                "habit_focus": (
                    "The habit of treating point of view as a writer's instrument and "
                    "asking, of any difficult work, what its chosen voice has made "
                    "possible and what it has cost."
                ),
            },
            "traditional": {
                "introduction": (
                    "Explicit instruction in the variants of third person (omniscient, "
                    "limited, free indirect discourse), in tracking shifts of narrative "
                    "distance, and in writing the analytical paragraph that argues what "
                    "a work gains by its chosen point of view."
                ),
                "gradual_release": {
                    "i_do": (
                        "Teacher chooses a passage that turns on POV, names the variant "
                        "explicitly, and writes a short paragraph on the board arguing "
                        "what the work gains by its choice, quoting the passage line by "
                        "line."
                    ),
                    "we_do": (
                        "Class chooses a candidate passage from the work under study, "
                        "names the variant together, and drafts the paragraph jointly, "
                        "weighing what a different POV would have changed."
                    ),
                    "you_do": (
                        "Student locates a POV-decisive passage independently, drafts "
                        "the analytical paragraph, and revises it after hearing a peer's "
                        "different reading at seminar."
                    ),
                },
                "independent_practice": [
                    "The analytical paragraph on a self-chosen POV-decisive passage, with quoted evidence",
                    (
                        "A short close analysis of a passage of free indirect discourse, "
                        "distinguishing narrator and character voice where possible"
                    ),
                ],
            },
            "unschooling": {
                "invitations": [
                    "Keep the long shelf of novels and short-story collections strong on narrative voice, available, never assigned",
                    "Keep a commonplace book and small slips for marking POV-decisive passages in books the reader cares about",
                ],
                "real_world_contexts": [
                    (
                        "A novel a student has chosen and loves, returned to for the "
                        "question of whose voice tells it and what that choice secures"
                    ),
                    "A long conversation about a passage the student wanted to read aloud because of how its voice works",
                    "A piece of the student's own writing in which they chose a teller deliberately and can say why",
                ],
                "conversation_starters": [
                    "Whose voice tells this book? What does that voice let you see, and what does it hide?",
                    "Did the narrator just come closer to that character, or pull back? What happened?",
                    "If this story were told from a different point of view, what would change?",
                ],
                "resource_bank": [
                    "A shelf of difficult, worthy novels chosen for the variety and consequence of their POVs",
                    "A reader-companion willing to discuss a chosen passage as a fellow reader",
                ],
                "parent_role": (
                    "Be a fellow reader who takes the student's chosen book seriously "
                    "and the question of its narrative voice seriously. Discussion "
                    "follows the student's reading; the parent contributes their own "
                    "reading as another reader at the table, never as an examiner."
                ),
                "observation_documentation": (
                    "Over time, notice whether the student begins to ask, of any "
                    "serious book, what its chosen voice has made possible, and whether "
                    "they reach for the passages that show it. This noticing replaces "
                    "any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": (
                "Montessori's pedagogy at this band does not carry a distinct method "
                "for the analysis of narrative voice in difficult literary works; the "
                "practice here draws from the seminar tradition rather than from the "
                "prepared environment."
            ),
        },
    },
    "lit-craft-010": {
        "node_type": "craft",
        "strand": "character",
        "band": "developing",
        "prerequisites": ["close reading: developing"],
        "objective": (
            "Identify what a character wants and what moves them to act, and articulate "
            "the difference between a character's stated reason and their underlying "
            "motive when the text makes the gap visible."
        ),
        "core_understanding": (
            "A character is most clearly understood by what they want. Desire shapes "
            "choice; motive is the engine. Characters in serious literature often want "
            "more than one thing at once, and the surface reason an action is given and "
            "the underlying motive are sometimes not the same. At this band the reader "
            "can name desire and motive in chosen scenes and quote the words that "
            "reveal each."
        ),
        "analytical_moves": [
            "Name what a character wants in a scene or chapter, in one sentence",
            ("Find a moment where the character chooses or refuses something and ask what desire drove the choice"),
            ("Distinguish a character's stated reason from their underlying motive when the text shows both"),
            "Notice when a character's wants are in conflict, and ask which one wins",
        ],
        "seminar_questions": [
            "What does this character want, and how do you know?",
            ("Did the character do this for the reason they say, or for another reason? Which words tell you?"),
            "What does this character want most when they cannot have everything they want?",
        ],
        "writing_invitations": [
            (
                "Write a short paragraph naming what a chosen character wants in one "
                "scene and the moment that reveals it, quoting the words"
            ),
            (
                "Take a character whose stated reason and underlying motive seem to "
                "differ; quote both and explain the gap"
            ),
        ],
        "exemplar_texts": [
            "Charlotte's choice to save Wilbur in Charlotte's Web",
            "Edmund's choice to follow the White Witch in The Lion, the Witch and the Wardrobe",
            "Anne Shirley's want for kinship in Anne of Green Gables",
            "Jo March's want to write in Little Women",
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "Character is the seedbed of meaning in a story, and want is the way "
                    "into character. The seminar asks plainly: what does this person "
                    "want, and is the reason they give the true one? The writer's words "
                    "are the evidence."
                ),
                "memory_work": {
                    "recitations": [
                        (
                            "The line in which a chosen character's want is first made "
                            "plain, recited at the seminar's opening"
                        ),
                    ],
                },
                "copywork": [
                    (
                        "The chosen line copied into a kept notebook of character "
                        "passages, with the character's name and the work named"
                    ),
                ],
                "recitation_routine": (
                    "Each seminar opens from the recited line; discussion takes its "
                    "first question from the want the line names."
                ),
                "read_aloud_suggestions": [
                    "A chapter from a novel chosen for the strength of its characters",
                    "A short story whose force turns on a single character's choice",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    (
                        "Living books strong on character at this age: Anne of Green "
                        "Gables, Little Women, The Lion, the Witch and the Wardrobe, "
                        "Charlotte's Web, Heidi"
                    ),
                ],
                "short_lesson_flow": (
                    "Read a chapter aloud, attentively, and the child narrates. Then ask "
                    "gently: what did this person want today, and what words showed it? "
                    "If the chapter contains a choice, ask which desire won. The chosen "
                    "line is copied into the commonplace book under the character's name."
                ),
                "narration_prompt": (
                    "Tell back what happened to this character today, and tell me what "
                    "they wanted and where you heard it."
                ),
                "real_world_objects": [
                    "The living book in hand, marked at the chapter's chosen line",
                    "A commonplace book organized so passages may be gathered under each character",
                ],
                "nature_connection": (
                    "Attention to a character's wants is the same habit as attention to "
                    "the wants of a real creature in the field: notice exactly what is "
                    "done, listen to what is said, and do not assume that the two always "
                    "agree."
                ),
                "habit_focus": (
                    "The habit of charitable attention: taking a character's words "
                    "seriously while also watching their choices, and noticing without "
                    "judgment when the two part ways."
                ),
            },
            "traditional": {
                "introduction": (
                    "Explicit instruction in naming a character's want, identifying the "
                    "moment that reveals it, and distinguishing stated reason from "
                    "underlying motive, supported by quoted evidence."
                ),
                "gradual_release": {
                    "i_do": (
                        "Teacher chooses a scene, names what the character wants in one "
                        "sentence, quotes the line that reveals it, and, where the text "
                        "shows it, names the gap between the character's stated reason "
                        "and their underlying motive."
                    ),
                    "we_do": (
                        "Class works through a second scene together, drafting one "
                        "sentence for what the character wants and quoting the line that "
                        "reveals it; together weighing whether stated reason and motive "
                        "agree."
                    ),
                    "you_do": (
                        "Student writes a short paragraph on a chosen scene naming what "
                        "the character wants, quoting the revealing line, and, where the "
                        "text supports it, identifying any gap between stated reason and "
                        "underlying motive."
                    ),
                },
                "independent_practice": [
                    "The short paragraph on a chosen character and chosen scene, with quoted evidence",
                ],
            },
            "unschooling": {
                "invitations": [
                    "Keep books strong on character on hand, available, never assigned",
                    (
                        "Welcome the child's running conversation about the people in "
                        "the books they love, as one might welcome talk about real "
                        "people the family knows"
                    ),
                ],
                "real_world_contexts": [
                    "Long conversations about a beloved character at meals or on walks",
                    ("A drawing, a letter, or a piece of fan writing the child makes about a character they love"),
                    "Comparing a character's choice to a real choice the child has watched or made",
                ],
                "conversation_starters": [
                    "What did she want, do you think? Why?",
                    "He said that, but did he mean it? What did he do?",
                    "If they could only have one thing, which one would they pick?",
                ],
                "resource_bank": [
                    "A shelf of well-loved novels with strong characters",
                    "A willing listener who will discuss a character as a real and interesting person",
                ],
                "parent_role": (
                    "Be a fellow reader who takes the characters seriously. Ask the "
                    "child what each person wants and listen to the answer; offer your "
                    "own reading when invited, as another reader at the table. Let the "
                    "child's care for the people in the book do the teaching."
                ),
                "observation_documentation": (
                    "Over time, notice whether the child begins to ask, of any character, "
                    "what they want and whether the reason they give is the true one, "
                    "and whether they reach for the words in the text when they answer. "
                    "This noticing replaces any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": (
                "Montessori at this band does not carry a distinct method for the "
                "analysis of desire and motive in fictional characters; literature work "
                "here remains within the grammar materials and the practical-life and "
                "moral imagination cultivated through chosen reading rather than through "
                "an analytical apparatus."
            ),
        },
    },
    "lit-craft-011": {
        "node_type": "craft",
        "strand": "character",
        "band": "developing",
        "prerequisites": ["close reading: developing", "desire and motive: developing"],
        "objective": (
            "Trace how a character changes across a story, naming what they were like "
            "at the start, what they are like at the end, and the events or recognitions "
            "that moved them, with quoted evidence from each stage."
        ),
        "core_understanding": (
            "Characters in serious literature are not fixed. They learn, they fail, "
            "they regret, they ripen. To trace change is to read a character across "
            "time, attending to the moments where they cross some threshold. Change is "
            "sometimes sudden and sometimes slow; sometimes the character knows it has "
            "happened, and sometimes only the reader does."
        ),
        "analytical_moves": [
            ("Name what a character is like at the start of a story or chapter, with a quoted line that shows it"),
            ("Name what the same character is like at the end of that span, with a quoted line that shows it"),
            "Identify the moment, scene, or recognition that moved them from one to the other",
            "Distinguish change the character notices in themselves from change only the reader notices",
        ],
        "seminar_questions": [
            "How is this character different at the end of the story than at the beginning?",
            "What moment moved them? Was the change sudden, or slow?",
            "Does the character know they have changed, or does only the reader know it?",
        ],
        "writing_invitations": [
            (
                "Write a short paragraph naming a chosen character at the start of the "
                "story and at the end, with quoted evidence for each, and the moment "
                "that lies between"
            ),
            (
                "Take a character who changes without noticing and write the paragraph "
                "that shows the reader what they have come to be"
            ),
        ],
        "exemplar_texts": [
            "Edmund's change from betrayal to loyalty in The Lion, the Witch and the Wardrobe",
            "Mary Lennox's softening across The Secret Garden",
            "Jess's growth across Bridge to Terabithia",
            "The journey of Despereaux in The Tale of Despereaux",
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "A character is a person met across the long line of a story. To "
                    "read a character well is to read them in time: who they were, who "
                    "they are now, and the place between where the change was made. The "
                    "seminar takes its evidence from the start-line, the end-line, and "
                    "the line that marks the threshold."
                ),
                "memory_work": {
                    "recitations": [
                        (
                            "Two lines side by side: the line where a chosen character "
                            "is shown at the start, and the line where the change is "
                            "plain at the end"
                        ),
                    ],
                },
                "copywork": [
                    (
                        "The two recited lines copied into a kept notebook of character "
                        "passages, under the character's name, with the work named and "
                        "the moment between them noted"
                    ),
                ],
                "recitation_routine": (
                    "Each seminar on a character opens by reciting their start-line and "
                    "their end-line; the discussion begins from the distance between them."
                ),
                "read_aloud_suggestions": [
                    "A chapter from a novel chosen for the clarity of a character's change",
                    "A short story whose force turns on a single recognition or threshold",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 25,
                "living_book_suggestions": [
                    (
                        "Living books strong on character change at this age: The "
                        "Secret Garden, The Lion, the Witch and the Wardrobe, Bridge to "
                        "Terabithia, The Tale of Despereaux, Heidi"
                    ),
                ],
                "short_lesson_flow": (
                    "Read a chapter aloud, attentively, and the child narrates. At the "
                    "end of a long enough span, set yesterday's chapter beside today's "
                    "and ask gently: is this person different from who they were? When "
                    "did it happen? Mark the line where it shows. The chosen lines are "
                    "copied into the commonplace book under the character's name, with "
                    "the chapter noted, so the line of change can be followed across "
                    "the whole book."
                ),
                "narration_prompt": (
                    "Tell back what happened to this person today, and tell me whether "
                    "they are different now than they were when we met them, and how "
                    "you can tell."
                ),
                "real_world_objects": [
                    "The living book itself, with small slips at the chapters where change shows",
                    "A commonplace book in which character passages are gathered under each name across the work",
                ],
                "nature_connection": (
                    "Reading a character across time is the same habit as watching a "
                    "tree across the seasons: the changes are sometimes sudden, often "
                    "slow, and the line of growth can only be seen by attending across "
                    "the long span."
                ),
                "habit_focus": (
                    "The habit of patient attention across a whole long story, and the "
                    "habit of charitable reading: noticing growth in another, real or "
                    "imagined, without judgment of who they were before."
                ),
            },
            "traditional": {
                "introduction": (
                    "Explicit instruction in tracking a character's change across a "
                    "story, in identifying the moment that marked it, and in writing "
                    "the short paragraph that shows the change with quoted evidence "
                    "from both stages."
                ),
                "gradual_release": {
                    "i_do": (
                        "Teacher chooses a character from a familiar work, names them "
                        "at the start with a quoted line, names them at the end with "
                        "another quoted line, and points to the scene that lies between."
                    ),
                    "we_do": (
                        "Class works through a second character together, drafting one "
                        "sentence for the start, one for the end, with quoted evidence, "
                        "and naming the moment that moved them."
                    ),
                    "you_do": (
                        "Student writes a short paragraph on a chosen character, "
                        "showing them at the start and the end with quoted lines, and "
                        "naming the moment that turned them."
                    ),
                },
                "independent_practice": [
                    (
                        "The short paragraph on a chosen character's change, with "
                        "quoted evidence from both stages and the threshold named"
                    ),
                ],
            },
            "unschooling": {
                "invitations": [
                    "Keep books strong on character change on hand, available, never assigned",
                    (
                        "Welcome the child's running conversation about how people in "
                        "their books are growing or shifting, as one might welcome talk "
                        "about people the family knows"
                    ),
                ],
                "real_world_contexts": [
                    ("Long conversations about a beloved character who is becoming different from who they began as"),
                    ("A drawing, a letter, or a piece of fan writing about a character at two stages of who they are"),
                    (
                        "Comparing a character's growth to a real growth the child has "
                        "noticed in themselves or someone they love"
                    ),
                ],
                "conversation_starters": [
                    "Are they the same person they were at the start of the book?",
                    "When did it happen? Was it a moment, or did it sneak up on them?",
                    "Do they know they have changed?",
                ],
                "resource_bank": [
                    "A shelf of well-loved novels with clear arcs of character change",
                    "A willing listener who will take the changes in a character seriously",
                ],
                "parent_role": (
                    "Be a fellow reader who knows the people in the book and follows "
                    "their growth with real interest. Ask what is different and listen "
                    "to the answer; offer your own reading when invited, as another "
                    "reader at the table. Let the child's care for the people in the "
                    "story do the teaching."
                ),
                "observation_documentation": (
                    "Over time, notice whether the child begins to ask, of any "
                    "character, how they are different from who they were and what "
                    "moved them, and whether they reach for the words in the text when "
                    "they answer. This noticing replaces any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": (
                "Montessori at this band does not carry a distinct method for tracing "
                "character change across a story; literature work here remains within "
                "the grammar materials and the moral imagination cultivated through "
                "chosen reading rather than through an analytical apparatus for change "
                "over time."
            ),
        },
    },
    "lit-craft-012": {
        "node_type": "craft",
        "strand": "character",
        "band": "emerging",
        "prerequisites": [],
        "objective": (
            "Notice the people in a story, name what they are like in concrete words, "
            "tell back what they do, and point to a moment in the story that shows what "
            "a character is like; tell two characters in the same story apart by "
            "something each one does."
        ),
        "core_understanding": (
            "A story is, first of all, about people, or about animals, things, or "
            "creatures that act like people. At the seed of character, the child learns "
            "to notice who the story is about, to name them, to tell what they do, and "
            "to find one moment in the story that shows what a character is like."
        ),
        "analytical_moves": [
            "Name the people in the story: who is in it?",
            "Tell what a chosen character does in the story, in the child's own words",
            ("Point to a moment in the story that shows what a character is like (kind, brave, sad, clever)"),
            "Tell apart two characters in the same story by something each one does",
        ],
        "seminar_questions": [
            "Who is this story about?",
            "What is this person like? How can you tell?",
            "What did they do today, in the story?",
        ],
        "writing_invitations": [
            "Draw the character you most cared about today, and write their name under your drawing",
            "Copy one short sentence from the story that shows what the character is like",
        ],
        "exemplar_texts": [
            (
                "A favorite picture book or short chapter book whose characters are "
                "clearly drawn (Frog and Toad; the Frances books; Winnie-the-Pooh)"
            ),
            ("A fairy tale or fable with clearly distinct characters (a Three Little Pigs; the Tortoise and the Hare)"),
            "A first chapter of a chapter book whose characters the family will follow (Charlotte's Web)",
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "A story is about people (or creatures who act like people). Before "
                    "we name the kinds of want and the kinds of change, we first hear "
                    "who is in the story and what they do."
                ),
                "memory_work": {
                    "recitations": [
                        (
                            "A single short line that shows what a chosen character is "
                            "like (a line in which they do something)"
                        ),
                    ],
                },
                "copywork": [
                    "The recited line copied once, slowly, with the character's name written beneath it",
                ],
                "recitation_routine": (
                    "Each session begins by reciting yesterday's character-line; the new "
                    "lesson opens with 'and who do we meet today?'"
                ),
                "read_aloud_suggestions": [
                    "A picture book or short chapter book whose characters are easily told apart",
                    "A fable or fairy tale with clearly drawn characters",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    (
                        "A worthy picture book or chapter book in which the characters "
                        "act and feel plainly enough that the child can speak of them"
                    ),
                ],
                "short_lesson_flow": (
                    "Read a short passage aloud, attentively. The child narrates. Then "
                    "ask gently: who was in this story? What was this one like? What did "
                    "they do? If two characters appear, set them side by side and ask "
                    "how they are different. The smallest noticing, in the child's own "
                    "words, is the whole lesson."
                ),
                "narration_prompt": ("Tell back what we read, and tell me who was in it and what they did."),
                "real_world_objects": [
                    "A worthy book in hand, with the characters easy to picture",
                    "A small card on which the names of the day's characters are written",
                ],
                "nature_connection": (
                    "Noticing the people in a story is the same habit as noticing the "
                    "creatures in a field: a particular person doing a particular thing, "
                    "attended to with care, before any name for what kind of person they "
                    "are is offered."
                ),
                "habit_focus": (
                    "The habit of charitable attention: noticing what a person in a "
                    "story actually does and says before deciding what kind of person "
                    "they are."
                ),
            },
            "traditional": {
                "introduction": "Explicit, modeled noticing of characters in a short, age-appropriate story.",
                "gradual_release": {
                    "i_do": (
                        "Teacher reads a passage aloud, names the people in it, and "
                        "tells what one of them does: 'Frog is in this one with Toad. "
                        "Frog brings Toad a letter.'"
                    ),
                    "we_do": (
                        "Teacher reads the next passage and, together with the child, "
                        "names the people and tells what each one does."
                    ),
                    "you_do": (
                        "Child listens to a new short passage, names the people in it, and tells what each one does."
                    ),
                },
            },
            "unschooling": {
                "invitations": [
                    "Keep picture books and chapter books with strong characters within reach",
                    "Read aloud often and welcome the child's running talk about the people they meet in stories",
                ],
                "real_world_contexts": [
                    "Bedtime stories in which the child names a favorite character without prompting",
                    "Pretend play in which the child takes on the part of a character from a beloved book",
                    "A drawing or a piece of fan writing about a character the child cares about",
                ],
                "conversation_starters": [
                    "Who was in that story?",
                    "What was she like? What did she do that made you think so?",
                    "How is he different from the other one?",
                ],
                "resource_bank": [
                    "A shelf of picture books and short chapter books with characters worth caring about",
                    "Dolls, animal figures, or simple props for acting out characters the child has met",
                ],
                "parent_role": (
                    "Read aloud well and talk about the people in the story as you "
                    "might talk about people you have met. Welcome the child's care for "
                    "a character without correction, and trust that attention to people "
                    "in stories grows from being delighted in them."
                ),
                "observation_documentation": (
                    "Over time, notice whether the child names characters by name, "
                    "tells what they did, and begins to compare two characters from the "
                    "same story. This noticing replaces any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": (
                "Montessori at this band does not carry a distinct method for noticing "
                "and naming the people in a story; the prepared environment centers on "
                "practical life, the sensorial materials, and the grammar materials "
                "rather than on the analysis of fictional characters."
            ),
        },
    },
    "lit-craft-020": {
        "node_type": "craft",
        "strand": "theme and meaning",
        "band": "emerging",
        "prerequisites": [],
        "objective": (
            "Tell what a story is about in age-appropriate, concrete terms, both what "
            "happens (the surface topic) and one feeling or idea the story leaves with "
            "the reader; point to the part of the story where that feeling came from."
        ),
        "core_understanding": (
            "Every story is about something. At the simplest level, a story is about "
            "what happens in it. At a slightly deeper level, a story is also about what "
            "it leaves us thinking or feeling. At the seed of theme, the child learns "
            "to tell back what happens and to name what feeling or idea the story "
            "leaves behind."
        ),
        "analytical_moves": [
            "Tell back what happens in the story, in the child's own words",
            ("Name one feeling the story left you with (happy, sad, brave, worried, surprised)"),
            "Point to the part of the story where that feeling came from",
            "Notice when two people read the same story and feel different things",
        ],
        "seminar_questions": [
            "What is this story about?",
            "How did the story leave you feeling, and where did that come from?",
            "What do you think the story is trying to show us?",
        ],
        "writing_invitations": [
            (
                "Draw the part of the story you would keep, and write one word for what "
                "the story is about under your drawing"
            ),
            "Copy a single sentence from the story that catches what the story is about",
        ],
        "exemplar_texts": [
            "A picture book whose meaning is plain and warm (The Giving Tree; Owl Moon)",
            "A fable whose lesson is named at the end (Aesop)",
            ("A simple chapter book whose theme is felt across the whole (Charlotte's Web; The Velveteen Rabbit)"),
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "Every story carries something beyond its events: a feeling, an "
                    "idea, a glimpse of how things are. Before we name it theme, the "
                    "child first hears that the story leaves something behind, and "
                    "learns to say what it is."
                ),
                "memory_work": {
                    "recitations": [
                        ("A single short line from the story that catches what it is about, recited"),
                    ],
                },
                "copywork": [
                    "The recited line copied once, slowly, with one word beneath it for what the story is about",
                ],
                "recitation_routine": (
                    "Each session begins by reciting yesterday's about-line; the new "
                    "lesson opens with 'and what was today's story about?'"
                ),
                "read_aloud_suggestions": [
                    "A picture book whose meaning carries plainly through the events",
                    "An Aesop fable whose lesson is plain at the end",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A worthy picture book or chapter book whose meaning lives in the whole story",
                ],
                "short_lesson_flow": (
                    "Read a short passage or a whole short story aloud, attentively. "
                    "The child narrates. Then ask gently: how did it leave you feeling? "
                    "What was it about? Where in the story did that feeling come from? "
                    "Let the child's own answer stand without correction."
                ),
                "narration_prompt": (
                    "Tell back what happened, and tell me how the story left you feeling, and where that came from."
                ),
                "real_world_objects": [
                    "A worthy book in hand, not a worksheet",
                    "A small card on which one word for what the story is about is written",
                ],
                "nature_connection": (
                    "Hearing what a story is about is the same habit as feeling the "
                    "mood of a real day in the woods or the kitchen: a whole has its "
                    "own feeling, beyond the sum of what is in it."
                ),
                "habit_focus": (
                    "The habit of attention to the whole story: hearing what it leaves "
                    "behind, not only what happens within it."
                ),
            },
            "traditional": {
                "introduction": (
                    "Explicit, modeled naming of what a story is about and what feeling "
                    "or idea it leaves, on a short, age-appropriate story."
                ),
                "gradual_release": {
                    "i_do": (
                        "Teacher reads a short story aloud and names plainly: 'This "
                        "story is about a spider and a pig becoming friends. It left me "
                        "feeling that friends can save each other.'"
                    ),
                    "we_do": (
                        "Teacher reads a second story and, together with the child, "
                        "names what it is about and one feeling it leaves, pointing to "
                        "where that feeling came from."
                    ),
                    "you_do": (
                        "Child listens to a new short story and tells what it is "
                        "about, names one feeling it left, and points to the part "
                        "where that feeling came from."
                    ),
                },
            },
            "unschooling": {
                "invitations": [
                    "Keep a mixed shelf of stories whose feelings are worth feeling within reach",
                    "Read aloud often and welcome the child's running talk about how a story made them feel",
                ],
                "real_world_contexts": [
                    "A bedtime story that left the child quiet and thinking afterward",
                    "A re-read of a favorite picture book because the child wanted the feeling again",
                    "A drawing or a story the child made in response to one they loved",
                ],
                "conversation_starters": [
                    "How did that story leave you feeling?",
                    "What do you think it was really about?",
                    "Did anything in it make you remember something of your own?",
                ],
                "resource_bank": [
                    "A shelf of picture books and short chapter books whose stories are worth carrying around",
                    "Quiet time after a story for the feeling to settle",
                ],
                "parent_role": (
                    "Read aloud well and let the silence after a story stay a moment. "
                    "Welcome whatever the child says about what it was about or how it "
                    "felt; offer your own response now and then as another reader. "
                    "Trust that attention to meaning grows from being moved."
                ),
                "observation_documentation": (
                    "Over time, notice whether the child begins to say things like "
                    "'this one was about being brave' or 'it made me feel sad in a "
                    "good way,' and whether they return to stories whose meaning held "
                    "them. This noticing replaces any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": (
                "Montessori at this band does not carry a distinct method for naming "
                "the meaning a story leaves; the prepared environment centers on "
                "practical life, the sensorial materials, and the grammar materials "
                "rather than on the analysis of theme."
            ),
        },
    },
    "lit-craft-021": {
        "node_type": "craft",
        "strand": "theme and meaning",
        "band": "developing",
        "prerequisites": [
            "close reading: developing",
            "what the story is about: emerging",
        ],
        "objective": (
            "Distinguish the topic of a story (what it is literally about: the events, "
            "the people, the place) from its theme (what the story shows about people, "
            "life, or the world beyond the events themselves); name the theme of a "
            "chosen story in a short sentence, grounded in a quoted passage."
        ),
        "core_understanding": (
            "The topic of a story is what it is about in the simplest sense, the "
            "events, the people, the place. The theme is something quieter and harder: "
            "what the story shows us about people, about life, about the world, beyond "
            "the events themselves. A story about a pig and a spider in a barn (topic) "
            "may also be a story about friendship and the goodness of caring for others "
            "(theme). To distinguish topic from theme is to begin the lifelong habit of "
            "reading for meaning."
        ),
        "analytical_moves": [
            "Name the topic of a story in one short sentence (what happens, who it is about)",
            ("Name the theme of the story in one short sentence (what it shows about people, life, or the world)"),
            "Tell apart topic from theme on a chosen story, saying which is which",
            "Quote a line or scene from the story that grounds the theme you named",
        ],
        "seminar_questions": [
            "What is this story about, and what is it really about?",
            ("Could two readers think the theme is different things? Which words might support each reading?"),
            "Where in the story does the theme show?",
        ],
        "writing_invitations": [
            (
                "Write a short paragraph naming the topic and the theme of a chosen "
                "story, with one quoted line that grounds the theme"
            ),
            ("Take a story you have summarized only by its topic and write the paragraph that names the theme too"),
        ],
        "exemplar_texts": [
            (
                "A novel of clear thematic substance at the band (Charlotte's Web; The "
                "Lion, the Witch and the Wardrobe; Bridge to Terabithia)"
            ),
            (
                "A folk tale or fable whose topic and theme are clearly distinct (a "
                "tale in which the lesson is unstated and must be drawn out)"
            ),
            "A short story or poem whose theme stays just beneath the surface",
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "The rhetorical tradition has long distinguished what a work is "
                    "about from what it is for. Topic is the matter; theme is the "
                    "meaning. The seminar asks both: of what does the story speak, and "
                    "what does the story say?"
                ),
                "memory_work": {
                    "recitations": [
                        ("A line from the story in which the theme can be seen at work, recited from memory"),
                    ],
                },
                "copywork": [
                    (
                        "The recited line copied into a kept notebook, with the topic "
                        "and the theme of the story written beneath in one short "
                        "sentence each"
                    ),
                ],
                "recitation_routine": (
                    "Each seminar opens by reciting the chosen line; the discussion "
                    "takes its first question from the gap between topic and theme."
                ),
                "read_aloud_suggestions": [
                    "A chapter of a novel chosen for the clarity of its theme",
                    "A short fable or parable whose theme is plain enough to name and defend",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 25,
                "living_book_suggestions": [
                    (
                        "Living books strong on theme at this age: Charlotte's Web; "
                        "The Lion, the Witch and the Wardrobe; The Secret Garden"
                    ),
                ],
                "short_lesson_flow": (
                    "Read a chapter aloud, attentively, and the child narrates. Then "
                    "ask gently: what is this story about, and what is it really "
                    "about? Let the child's own answer come first; offer your own as "
                    "another reader if invited. The chosen line that holds the theme "
                    "is copied into the commonplace book, with the topic and theme of "
                    "the work named in the child's own words."
                ),
                "narration_prompt": (
                    "Tell back the chapter, and tell me what this story is really "
                    "about, and read me the line that makes you think so."
                ),
                "real_world_objects": [
                    "The living book in hand, marked at lines where the theme shows",
                    "A commonplace book organized so each work's topic and theme can be set side by side",
                ],
                "nature_connection": (
                    "Naming the theme of a story is the same habit as naming what a "
                    "long season has been about: the events are many; the meaning is "
                    "one quiet thing under them."
                ),
                "habit_focus": (
                    "The habit of patient attention to what a whole story is really "
                    "about, beyond what happens in it, and of grounding any answer in "
                    "the words on the page."
                ),
            },
            "traditional": {
                "introduction": (
                    "Explicit instruction in distinguishing topic from theme, in "
                    "naming each in a short sentence, and in writing the short "
                    "paragraph that defends a theme with one quoted line."
                ),
                "gradual_release": {
                    "i_do": (
                        "Teacher chooses a familiar story, names its topic in one "
                        "sentence and its theme in another, and quotes a line that "
                        "shows the theme at work, naming the gap between the two."
                    ),
                    "we_do": (
                        "Class chooses a second story together, drafts a topic "
                        "sentence and a theme sentence jointly, and finds a quoted "
                        "line to ground the theme on the board."
                    ),
                    "you_do": (
                        "Student writes a short paragraph on a chosen story naming the "
                        "topic and the theme and quoting a line that grounds the theme."
                    ),
                },
                "independent_practice": [
                    (
                        "The short paragraph on a chosen story, with topic and theme "
                        "distinguished and the theme grounded in a quoted line"
                    ),
                ],
            },
            "unschooling": {
                "invitations": [
                    "Keep books strong on theme on the shelf, available, never assigned",
                    (
                        "Welcome the child's running talk about what a book they loved "
                        "is really about, as one might welcome talk about what a real "
                        "experience really meant"
                    ),
                ],
                "real_world_contexts": [
                    "A long conversation about what a book the child loved was really about",
                    "A re-read or a recommendation the child makes, with a sentence about what the book is really about",
                    ("A piece of the child's own writing that draws on the theme of a book they have read"),
                ],
                "conversation_starters": [
                    "What is this book about, and what is it really about?",
                    "Could someone think it was about something different? Why?",
                    "Where in the book does that meaning show?",
                ],
                "resource_bank": [
                    "A shelf of well-written novels and stories whose meanings reach beyond their events",
                    "A reader-companion willing to discuss what a story is really about as another reader",
                ],
                "parent_role": (
                    "Be a fellow reader who takes the child's reading of a story "
                    "seriously and offers your own as another reader's, not as a "
                    "teacher's. Ask what a story is really about and listen to the "
                    "answer; let real care for the books do the teaching."
                ),
                "observation_documentation": (
                    "Over time, notice whether the child begins to say of a book what "
                    "it is about and, separately, what it is really about, and whether "
                    "they reach for the words in the text when they answer. This "
                    "noticing replaces any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": (
                "Montessori at this band does not carry a distinct method for the "
                "analytical distinction between topic and theme in literary works; "
                "literature work here remains within the grammar materials and the "
                "moral imagination cultivated through chosen reading rather than "
                "through an analytical apparatus."
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
    "lit-craft-040": {
        "node_type": "craft",
        "strand": "figurative language and symbol",
        "band": "emerging",
        "prerequisites": [],
        "objective": (
            "Notice when a writer compares one thing to another to help us picture or "
            "feel something; find a simple comparison (with 'like' or 'as') in a story "
            "or poem, name the two things being compared, and say what the comparison "
            "helps the reader picture."
        ),
        "core_understanding": (
            "Writers sometimes describe one thing by saying it is like something else. "
            "'The moon is like a bright coin.' 'Her hair was as soft as silk.' These "
            "are comparisons. At the seed of figurative language, the child learns to "
            "hear when a writer is comparing, to find the two things being compared, "
            "and to say what the comparison helps the reader picture or feel."
        ),
        "analytical_moves": [
            "When listening to a story or poem, notice when a writer says one thing is like another",
            "Name the two things being compared (the moon and a coin; her hair and silk)",
            "Say what the comparison helps you picture or feel",
            "Try a comparison of your own: this thing is like ___",
        ],
        "seminar_questions": [
            "Did you hear the writer compare one thing to another? What two things?",
            "What does the comparison help you picture?",
            "How is the thing being talked about like the thing it is being compared to?",
        ],
        "writing_invitations": [
            ("Draw the two things the writer compared and write the comparison underneath your drawing (X is like Y)"),
            ("Try your own comparison: choose something around you and write one short line saying what it is like"),
        ],
        "exemplar_texts": [
            (
                "A picture book with rich, comparative language (Owl Moon; Stopping by "
                "Woods on a Snowy Evening read aloud)"
            ),
            (
                "A poem of simple comparison (a Christina Rossetti for children; a "
                "Stevenson from A Child's Garden of Verses)"
            ),
            "A fable or folk tale whose images turn on a comparison",
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "Comparison is among the oldest figures of speech and one of the "
                    "first the ear can hear. Before we name simile and metaphor, the "
                    "child learns to hear that a writer is comparing and to find the "
                    "two things set side by side."
                ),
                "memory_work": {
                    "recitations": [
                        "A short comparison from a chosen poem or story, recited",
                    ],
                },
                "copywork": [
                    ("The recited comparison copied once, slowly, with the two things compared circled or underlined"),
                ],
                "recitation_routine": (
                    "Each session begins by reciting yesterday's comparison; the new "
                    "lesson opens with 'and what is compared today?'"
                ),
                "read_aloud_suggestions": [
                    "A picture book or short poem rich in plain comparison",
                    "A fable whose image turns on a comparison",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A worthy picture book or short poem in which comparisons are easy to hear",
                ],
                "short_lesson_flow": (
                    "Read a short passage or whole short poem aloud, attentively. The "
                    "child narrates. Then ask gently: did you hear something compared "
                    "to something else? What two things? What did it help you picture? "
                    "Let the child try a comparison of their own about something real "
                    "in the room or out the window."
                ),
                "narration_prompt": (
                    "Tell back what we read, and tell me what the writer compared, and "
                    "what the comparison helped you see."
                ),
                "real_world_objects": [
                    "A worthy book or short poem in hand, not a worksheet",
                    "Something real to look at while trying a comparison of one's own",
                ],
                "nature_connection": (
                    "Comparison is the natural language of nature description: a "
                    "cloud like a feather, a leaf like a hand. The habit of looking and "
                    "the habit of comparing are nearly the same habit."
                ),
                "habit_focus": (
                    "The habit of seeing one thing in light of another: a small daily "
                    "act of imagination that begins in childhood and never stops."
                ),
            },
            "traditional": {
                "introduction": ("Explicit, modeled noticing of comparisons in a short, age-appropriate passage."),
                "gradual_release": {
                    "i_do": (
                        "Teacher reads a passage aloud and names the comparison "
                        "plainly: 'The writer said the moon was like a bright coin. "
                        "Moon and coin. The comparison helps me picture how round and "
                        "shiny it was.'"
                    ),
                    "we_do": (
                        "Teacher reads a second passage and, together with the child, "
                        "names the comparison, the two things, and what it helps "
                        "picture."
                    ),
                    "you_do": (
                        "Child listens to a new short passage, finds a comparison if "
                        "one is there, names the two things, and tries a comparison "
                        "of their own."
                    ),
                },
            },
            "unschooling": {
                "invitations": [
                    "Keep poetry and picture books rich in comparison within reach",
                    "Use comparisons of your own often where the child can hear them, and welcome theirs",
                ],
                "real_world_contexts": [
                    "Pointing at the sky or a leaf or a sound and saying what it is like",
                    "Listening to a song and noticing a line of comparison in the lyric",
                    "A drawing the child labels with a comparison of their own",
                ],
                "conversation_starters": [
                    "What is that like?",
                    "Did you hear the writer say one thing was like another? What two things?",
                    "How is the moon like a coin?",
                ],
                "resource_bank": [
                    "A shelf of picture books and short poems rich in comparison",
                    "A willing companion who will play the comparison game in the car or on a walk",
                ],
                "parent_role": (
                    "Notice things aloud and say what they are like when the comparison "
                    "comes to you, so the child hears that comparison is something "
                    "grown people do for love of seeing. Welcome the child's "
                    "comparisons with real interest, and trust that the figure of "
                    "speech grows from being played with."
                ),
                "observation_documentation": (
                    "Over time, notice whether the child begins to say of things in the "
                    "world that they are like other things, and whether they catch "
                    "comparisons in stories and poems without prompting. This noticing "
                    "replaces any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": (
                "Montessori at this band does not carry a distinct method for noticing "
                "figurative comparison in literature; the prepared environment centers "
                "on practical life, the sensorial materials, and the grammar materials "
                "rather than on figures of speech."
            ),
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
