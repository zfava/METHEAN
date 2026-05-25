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
    "lit-craft-004": {
        "node_type": "craft",
        "strand": "close reading",
        "band": "advanced",
        "prerequisites": ["close reading: proficient"],
        "objective": (
            "Bring sustained close reading as an inquiry method to whole difficult "
            "works across multiple modes (literary fiction, drama, poetry, the "
            "meditative essay, history, philosophy); hold attention through "
            "bewilderment when a first reading defeats the surface; place two "
            "passages side by side from different works and articulate what each "
            "lets us see in the other; build literary argument supported by multiple "
            "passages held in productive tension across a sustained piece of writing."
        ),
        "core_understanding": (
            "At the proficient band close reading became a habit one brings to a "
            "chosen difficult work. At the advanced band the habit becomes a "
            "discipline: an inquiry method, not a school exercise. The advanced "
            "reader meets work whose surface defeats first reading and learns to "
            "remain with it; reads across modes (the dramatic monologue, the "
            "meditative essay, the historian's argument, the philosopher's example) "
            "and feels what each mode asks of close reading; sets passages from "
            "different works beside one another and lets each illuminate the other; "
            "and writes a sustained argument that does not flatten its evidence into "
            "a single thesis but holds multiple passages in productive tension. The "
            "habit is now ready to be turned on anything written with care."
        ),
        "analytical_moves": [
            "Sustain attention through bewilderment on a difficult work whose surface defeats first reading",
            (
                "Read close attention into modes outside literary fiction (drama, the "
                "meditative essay, the historian's account, the philosopher's example)"
            ),
            "Set two passages from different works side by side and articulate what each lets us see in the other",
            (
                "Build a sustained piece of literary argument that holds multiple "
                "passages in productive tension rather than flattening them to a "
                "single thesis"
            ),
            "Distinguish a reading the words can support from a reading they cannot, and abandon the latter without resentment",
        ],
        "seminar_questions": [
            "Where in this work does the surface refuse a first reading, and what changes when you return?",
            "What does this work let us see that no other mode of writing could let us see in the same way?",
            "If we set this passage beside that one from another work, what does each let us see in the other?",
        ],
        "writing_invitations": [
            (
                "Write a sustained piece of literary argument on a chosen work that "
                "holds two or three passages in productive tension, returning to "
                "each across the essay"
            ),
            (
                "Write the comparative paragraph that places a passage from one work "
                "beside a passage from another and argues what each lets us see in the other"
            ),
        ],
        "exemplar_texts": [
            "A difficult modernist novel held whole (a Faulkner; a Woolf; a Joyce after Dubliners)",
            "A dramatic work whose surface yields slowly (a Shakespeare tragedy whole; Beckett; Ibsen)",
            (
                "A meditative essay or philosophical passage whose careful prose "
                "rewards sustained close reading (Augustine; Boethius; an essay of "
                "Montaigne; a central passage of a Plato dialogue)"
            ),
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "Close reading meets the long seminar tradition. The reader "
                    "brings difficult work; the seminar tests what the words can be "
                    "made to support. Across modes (drama, essay, history, "
                    "philosophy) the same discipline operates: return to the words, "
                    "defend the reading from them, hear another reading respectfully "
                    "and locate where in the text it draws its evidence. Rhetorical "
                    "analysis and interpretive habit converge here into the kind of "
                    "attention that a scholarly life is built on."
                ),
                "memory_work": {
                    "recitations": [
                        "A passage of demanding prose or poetry recited at the seminar's opening, chosen because the seminar has more than one reading of it",
                    ],
                },
                "copywork": [
                    "The recited passage copied into the kept commonplace book, with both candidate readings noted in the margin",
                ],
                "recitation_routine": (
                    "Each seminar opens from a recited passage of disputed reading; "
                    "the first question is taken from the lines just heard, and the "
                    "discussion returns to the text for every claim."
                ),
                "read_aloud_suggestions": [
                    "A scene from a difficult dramatic work read aloud at the seminar's opening",
                    "A demanding passage of meditative prose read aloud whole before discussion",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 50,
                "living_book_suggestions": [
                    "A difficult modernist novel held whole across a term, narrated sitting by sitting",
                    "A difficult dramatic work read whole, with the most demanding scenes returned to in commonplace work",
                    "A volume of meditative essays read across a year, one essay per sitting",
                ],
                "short_lesson_flow": (
                    "The advanced student reads the difficult work at a sustained "
                    "pace, narrating each sitting honestly even when the surface "
                    "defeated first reading. Passages worth attending to are marked "
                    "or slipped as they are met. At the chapter's or essay's end, a "
                    "passage of disputed or layered reading is taken up: copied into "
                    "the commonplace book, discussed, and tested against the rest of "
                    "the work and against passages from other works it brings to "
                    "mind. The habit matures from sustained attention to a single "
                    "difficult work into the discipline that brings sustained "
                    "attention to anything written with care."
                ),
                "narration_prompt": (
                    "Tell back what you read, and tell me which passage you would "
                    "set down as the one whose reading is most worth disputing, and "
                    "what other passage, in this book or another, you would set beside it."
                ),
                "real_world_objects": [
                    "The whole difficult work, marked at passages worth disputing",
                    "A commonplace book gathering passages across whole years and several traditions",
                ],
                "nature_connection": (
                    "The advanced close reader is to the world of writing what a "
                    "naturalist of long practice is to a forest: at home in any "
                    "species, able to see what is rare without losing the view of the "
                    "common, and able to set one creature beside another and feel "
                    "what each tells about the other."
                ),
                "habit_focus": (
                    "The habit of sustained attention across whole difficult works, "
                    "the habit of returning to the text for every claim, and the "
                    "habit of setting one work beside another."
                ),
            },
            "traditional": {
                "introduction": (
                    "Explicit instruction in close reading scaled to a sustained "
                    "piece of literary argument; modeled comparative reading across "
                    "two works; the analytical essay supported by passages held in tension."
                ),
                "gradual_release": {
                    "i_do": (
                        "Teacher works a difficult passage on the board, sets it "
                        "beside a second passage from another work, and drafts a "
                        "paragraph of literary argument that holds both in tension, "
                        "quoting each line by line."
                    ),
                    "we_do": (
                        "Class chooses two passages (one from the work under study, "
                        "one from another) and drafts together a sustained piece of "
                        "literary argument that holds them in productive tension."
                    ),
                    "you_do": (
                        "Student writes an independent sustained piece of literary "
                        "argument on a chosen work, holding two or three passages in "
                        "tension, with one passage from another work brought in as "
                        "comparative evidence, and revises after seminar."
                    ),
                },
                "independent_practice": [
                    "The sustained essay on a self-chosen work, holding multiple passages in tension",
                    "A comparative paragraph placing a passage from the work beside a passage from another work in the tradition",
                ],
            },
            "unschooling": {
                "invitations": [
                    "Keep the long shelf of difficult, worthy works across many modes (novels, drama, essays, philosophy, history) available, never assigned",
                    "Keep the commonplace book matured into a habit, with comparative slips between works the reader keeps coming back to",
                ],
                "real_world_contexts": [
                    "A reader who has returned to a difficult novel across years, watching their reading change as they returned",
                    "An essay or piece of literary writing the reader produced because two books, met years apart, started to talk to each other in the reader's mind",
                    "A long conversation with a fellow reader who has read the same work and brings a passage from a third work into the table",
                ],
                "conversation_starters": [
                    "When did this book change for you, and which passage was where it changed?",
                    "What other book have you read that this one set you thinking about? Read me the passage where the connection lives.",
                    "Where do the words refuse the reading you wish they supported? Which words say so?",
                ],
                "resource_bank": [
                    "A shelf of difficult, worthy work across genres and modes, gathered slowly",
                    "A reader-companion of long acquaintance who has read across many traditions and is willing to bring a passage from elsewhere",
                ],
                "parent_role": (
                    "By this band the parent has become a fellow reader who has read "
                    "alongside the student for years and brings a passage from "
                    "another work into the room when the student finds a connection. "
                    "The parent does not assign and does not examine; they name what "
                    "they themselves found in their own returning. The student is in "
                    "charge of their reading; the parent is a witness who can be asked."
                ),
                "observation_documentation": (
                    "Over time, notice whether the student returns to difficult "
                    "works on their own across years, writes because the work moved "
                    "them to write, sets passages from different works beside one "
                    "another without prompting, and abandons a reading the words "
                    "cannot support without resentment. This noticing replaces any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": (
                "Montessori's literature pedagogy at the elementary and "
                "early-secondary level does not carry a distinct method for the "
                "kind of sustained, comparative close reading of difficult works "
                "across modes that this band names; the practice here is drawn from "
                "the long seminar tradition and the matured Charlotte Mason habit "
                "of narration and commonplace work across years rather than from "
                "the prepared environment."
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
        "prerequisites": ["lit-craft-006", "close reading: developing"],
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
        "prerequisites": ["lit-craft-007", "close reading: proficient"],
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
        "prerequisites": ["close reading: developing", "lit-craft-010"],
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
    "lit-craft-013": {
        "node_type": "craft",
        "strand": "character",
        "band": "proficient",
        "prerequisites": ["lit-craft-010", "lit-craft-011", "close reading: proficient"],
        "objective": (
            "Hold a literary character as a constructed person whose interior life the "
            "reader infers from the writer's particular choices (voice, action, "
            "silence, the eyes of others, what the character does not say or cannot "
            "see); build a small original reading of a character defensible from the "
            "words on the page; and recognize when a character also serves a "
            "structural function in the work without flattening them to that function."
        ),
        "core_understanding": (
            "A character is not a person and not only a function; they are the "
            "structured place in a work where a particular inner life is offered for "
            "the reader's inference. At the proficient band the reader sees how the "
            "writer's choices, what is said and what is withheld, what is acted on and "
            "what is fled from, what others see and what the character cannot, "
            "together make the character available. The reader can carry a small "
            "original reading from the text and defend it against another reader's by "
            "returning to specific lines. They can also see when a character does work "
            "for the form of the book (the foil who lights another by contrast, the "
            "choric voice who interprets the action) without losing the person inside "
            "the function."
        ),
        "analytical_moves": [
            (
                "Read a character through the specific choices of voice, action, "
                "silence, and the eyes of others, naming which the writer foregrounds"
            ),
            (
                "Distinguish a character from the function they may also serve in the "
                "work (foil, choric voice, antagonist), and hold both"
            ),
            (
                "Identify the gap between a character's self-understanding and what "
                "the text lets the reader see, and reason about why that gap is there"
            ),
            "Build a small original reading of a character supported line by line from the text",
            (
                "Hear another reader's different reading of the same character and "
                "locate where in the text it draws its evidence"
            ),
        ],
        "seminar_questions": [
            (
                "Which of this writer's choices is most decisive for our sense of this "
                "character: voice, action, silence, or what others see in them?"
            ),
            (
                "Where does this character understand themselves, and where do we "
                "understand them in spite of themselves? Which words tell you?"
            ),
            "Does this character also serve a function in the work? Does that function exhaust them?",
        ],
        "writing_invitations": [
            (
                "Write a short analytical paragraph defending one specific reading of "
                "a chosen character, quoting two or three lines that ground the reading"
            ),
            (
                "Write the paragraph that holds a character as both a person and a "
                "function within the work, naming each and naming what is at stake in "
                "holding both"
            ),
        ],
        "exemplar_texts": [
            (
                "A novel whose character work rewards line-level attention (Pride and "
                "Prejudice; Jane Eyre; Middlemarch read across a term; Bleak House)"
            ),
            (
                "A novel in which a character also serves a structural function (the "
                "foils in any Austen; the choric voices of Greek tragedy)"
            ),
            "A short story whose whole weight is a character (Chekhov; Joyce's Dubliners; Eudora Welty)",
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "Character meets the seminar. The reader brings a reading; the "
                    "seminar tests both the reading and the words it is built upon. "
                    "Rhetorical close attention and the older tradition of moral "
                    "portrait converse: by what particular choices does this writer "
                    "make this character available, and what does that availability "
                    "ask of us?"
                ),
                "memory_work": {
                    "recitations": [
                        "A speech or self-revealing passage from a chosen character, recited at the seminar's opening",
                    ],
                },
                "copywork": [
                    "The recited passage copied into the kept commonplace book, with the line that bears most weight underlined",
                ],
                "recitation_routine": (
                    "Each seminar opens from a recited passage of a character; the "
                    "first question is taken from the lines just heard and returns to "
                    "the text for every claim."
                ),
                "read_aloud_suggestions": [
                    "A scene of strong character voice read aloud at the seminar's opening",
                    "A short story whose weight is a character, read aloud whole",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 40,
                "living_book_suggestions": [
                    "A worthy novel in which character work is the substance, read whole at a sustained pace",
                    "A volume of short stories whose weight is character",
                ],
                "short_lesson_flow": (
                    "The proficient student reads the whole book at a sustained pace, "
                    "narrating each sitting. As characters emerge they are watched: "
                    "what they say, what they will not say, what others see in them. A "
                    "passage worth attending to is slipped or noted; at the chapter's "
                    "end one such passage is taken up, copied into the commonplace "
                    "book, and discussed. A small reading of the character is allowed "
                    "to form across the long span and tested against the whole work."
                ),
                "narration_prompt": (
                    "Tell back the chapter you read, and tell me which line of which "
                    "character you would set down as the one that bears most weight, and why."
                ),
                "real_world_objects": [
                    "The whole novel, marked with the reader's own slips at the character's decisive lines",
                    "A commonplace book gathering character passages across many works",
                ],
                "nature_connection": (
                    "To watch a character across a whole book is to watch as one "
                    "watches a bird across the years: the same creature in different "
                    "lights, slowly known."
                ),
                "habit_focus": (
                    "The habit of returning to a character's particular lines for "
                    "evidence, and the habit of holding more than one reading of a "
                    "person at the same time."
                ),
            },
            "traditional": {
                "introduction": (
                    "Explicit instruction in reading character through the writer's "
                    "particular choices, in distinguishing character from function, "
                    "and in writing the short analytical paragraph that defends a "
                    "reading from the words."
                ),
                "gradual_release": {
                    "i_do": (
                        "Teacher reads a passage aloud, names the writer's choices "
                        "that make the character available (this line of voice, this "
                        "silence, this action), and writes a short paragraph on the "
                        "board defending one reading of the character, quoting the passage."
                    ),
                    "we_do": (
                        "Class chooses a candidate character from the work under "
                        "study, gathers two or three decisive passages, and drafts "
                        "together a short paragraph defending a small original "
                        "reading, quoting the lines that ground it."
                    ),
                    "you_do": (
                        "Student writes an independent analytical paragraph defending "
                        "a chosen reading of a chosen character, with two or three "
                        "quoted passages as evidence, and revises after hearing a "
                        "different reading at seminar."
                    ),
                },
                "independent_practice": [
                    "The analytical paragraph on a self-chosen character from the work under study",
                    "A short revision of the paragraph after seminar discussion",
                ],
            },
            "unschooling": {
                "invitations": [
                    "Keep the long shelf of novels and story collections of real substance, available, never assigned",
                    "Keep a commonplace book and small slips for marking character passages in books the reader cares about",
                ],
                "real_world_contexts": [
                    "A long conversation about a character a reader has come to love or distrust in a book they chose",
                    "A piece of writing the reader composed because a character in a book asked something of them",
                    "A read-aloud of a chosen passage so a fellow reader can hear what the reader heard in it",
                ],
                "conversation_starters": [
                    "Who is this character, really? Which lines made you see them that way?",
                    "Are they only themselves in the book, or are they also doing some work for the writer?",
                    "Where do they know themselves, and where do we know them in spite of themselves?",
                ],
                "resource_bank": [
                    "A shelf of difficult, worthy novels and stories whose character work rewards attention",
                    "A reader-companion willing to discuss a chosen character as a fellow reader, not as an examiner",
                ],
                "parent_role": (
                    "Take the reader's character seriously, and ask the reader to "
                    "take theirs seriously by going back to the lines. Be a fellow "
                    "reader who has their own reading and is willing to hear another."
                ),
                "observation_documentation": (
                    "Over time, notice whether the reader returns to characters "
                    "across books, defends a reading from the words, and hears a "
                    "different reading without giving up their own. This noticing "
                    "replaces any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": (
                "Montessori's literature pedagogy at the elementary and "
                "early-secondary level does not carry a distinct method for the "
                "sustained close reading of literary character; the practice here is "
                "drawn from the seminar tradition and the long Charlotte Mason habit "
                "of narration across whole books rather than from the prepared environment."
            ),
        },
    },
    "lit-craft-014": {
        "node_type": "craft",
        "strand": "character",
        "band": "advanced",
        "prerequisites": ["lit-craft-013", "narrative craft: proficient", "close reading: proficient"],
        "objective": (
            "Read character as part of a work's argument (this character is here "
            "because the work needed this kind of presence to make its meaning); "
            "trace character types across the tradition (the picaresque rogue, the "
            "choric daughter, the unreliable confessor) and ask what a writer does "
            "with the inherited type; read how the writer's point-of-view choice "
            "shapes which character becomes available; and write the argumentative "
            "essay that situates a chosen character inside the work's claim about its world."
        ),
        "core_understanding": (
            "At the proficient band character was held as a constructed person "
            "whose interior life the reader infers from the writer's particular "
            "choices, with the structural function (foil, choric voice) held "
            "alongside the person. At the advanced band the reader sees how a "
            "character is part of a work's argument: a character is here because "
            "the work needed this kind of presence to mean what it means. The "
            "reader also meets the inheritance: certain character types travel "
            "through the tradition (the rogue, the choric daughter, the unreliable "
            "confessor) and each writer does something particular with the "
            "inherited type. Point-of-view choice (the strand met at proficient) "
            "is now seen as decisive for which character becomes available at all. "
            "The reader writes the essay that argues a character's place inside "
            "the work's claim about its world."
        ),
        "analytical_moves": [
            (
                "Read a character as part of the work's argument and articulate "
                "what the work needed this presence to do that no other could"
            ),
            (
                "Identify the inherited character type a writer is working with and "
                "argue what this writer does with the inheritance (extending, "
                "complicating, refusing it)"
            ),
            (
                "Read how the writer's point-of-view choice makes this character "
                "available in this way and not another, and ask what a different "
                "point of view would have made of the same character"
            ),
            (
                "Write the argumentative essay that situates a chosen character "
                "inside the work's claim about its world, with multiple passages "
                "held in productive tension"
            ),
            (
                "Hear another reader's situating of the same character and locate "
                "where in the work and in the tradition that situating draws its evidence"
            ),
        ],
        "seminar_questions": [
            "What does the work need this character to do that no other presence could?",
            "Which inherited character type is this writer working with, and what is the writer doing to it?",
            (
                "If this work were told from a different point of view, which "
                "character would change most, and what does that tell you about who "
                "this character is in this work?"
            ),
        ],
        "writing_invitations": [
            (
                "Write an argumentative essay situating a chosen character inside "
                "the work's claim about its world, holding two or three passages in "
                "productive tension and naming at least one craft choice (point of "
                "view, structural placement, recurring image) decisive for the character"
            ),
            (
                "Write the comparative paragraph that sets a character beside an "
                "inherited type from the tradition and argues what this writer makes "
                "of the inheritance"
            ),
        ],
        "exemplar_texts": [
            "A novel whose central character is doing the work of the writer's argument (Middlemarch's Dorothea; Bleak House's Esther; Crime and Punishment's Raskolnikov)",
            (
                "A novel in conversation with an inherited character type (Don "
                "Quixote and the picaresque rogue; Hamlet and the revenger; Tess "
                "and the fallen-woman type)"
            ),
            "A short story whose character is what the work needed (a Chekhov; a Eudora Welty; a Flannery O'Connor)",
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "Character meets the long seminar. The reader brings a "
                    "character and asks why this work needed this presence; the "
                    "seminar tests both the answer and the words it is built upon, "
                    "and brings the tradition's inherited types into the room. "
                    "Rhetorical analysis, moral portrait, and the genealogy of "
                    "character types converge: by what particular choices does this "
                    "writer make this character available, what inheritance is at "
                    "work, and what does that availability ask of the work's argument?"
                ),
                "memory_work": {
                    "recitations": [
                        "A passage in which a chosen character carries the work's argument, recited at the seminar's opening",
                    ],
                },
                "copywork": [
                    "The recited passage copied into the kept commonplace book, with the inherited type the writer is working with noted in the margin",
                ],
                "recitation_routine": (
                    "Each seminar opens from a recited passage of character; the "
                    "first question is taken from the lines just heard, and the "
                    "discussion brings into the room at least one passage from "
                    "elsewhere in the tradition working the same character type."
                ),
                "read_aloud_suggestions": [
                    "A scene in which a chosen character bears the weight of the work's argument, read aloud at the seminar's opening",
                    "A passage from another work in the tradition handling the same inherited character type",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 50,
                "living_book_suggestions": [
                    "A worthy novel whose central character carries the work's argument, read whole at a sustained pace",
                    "A second work in the tradition handling the same inherited character type, read alongside or after",
                ],
                "short_lesson_flow": (
                    "The advanced student reads the work whole at a sustained pace, "
                    "narrating each sitting. As the central character emerges they "
                    "are watched not only as a person but as a presence the work "
                    "needs. Passages worth attending to are slipped or marked; at a "
                    "chapter's end one is taken up, copied into the commonplace "
                    "book, and discussed: what is the work doing through this "
                    "character that nothing else could do, and what inherited type "
                    "is the writer working with? When a second work in the same "
                    "tradition is read, the commonplace book holds the comparative passage."
                ),
                "narration_prompt": (
                    "Tell back the chapter you read, and tell me what the book "
                    "needed this character to do that no other presence could, and "
                    "which other character, in this book or another, you would set beside them."
                ),
                "real_world_objects": [
                    "The whole novel, marked at the passages decisive for the character's place in the work's argument",
                    "A commonplace book gathering character passages and the inherited types they belong to across many works",
                ],
                "nature_connection": (
                    "To see a character as part of a work's argument is to see them "
                    "as the naturalist sees a keystone species: not only as the "
                    "creature it is, but as the role its being there makes possible "
                    "for everything else in the place."
                ),
                "habit_focus": (
                    "The habit of asking what a work needed a character to do, and "
                    "the habit of bringing the tradition's inherited types into the "
                    "reading of a particular character."
                ),
            },
            "traditional": {
                "introduction": (
                    "Explicit instruction in reading character as part of a work's "
                    "argument, in tracing inherited character types across the "
                    "tradition, in seeing how point-of-view choice makes a character "
                    "available, and in writing the argumentative essay that situates "
                    "a character inside the work's claim about its world."
                ),
                "gradual_release": {
                    "i_do": (
                        "Teacher works a chosen character on the board: names the "
                        "inherited type the writer is working with, identifies the "
                        "point-of-view choice that makes the character available, "
                        "and drafts the opening of an argumentative essay situating "
                        "the character inside the work's argument, quoting two passages."
                    ),
                    "we_do": (
                        "Class chooses a candidate character from the work under "
                        "study, identifies the inherited type, gathers two or three "
                        "decisive passages, and drafts together the body of the "
                        "argumentative essay situating the character inside the "
                        "work's argument, quoting the lines that ground it."
                    ),
                    "you_do": (
                        "Student writes an independent argumentative essay "
                        "situating a chosen character inside the work's argument, "
                        "naming the inherited type and the decisive point-of-view "
                        "choice, holding two or three passages in productive "
                        "tension, and revises after seminar."
                    ),
                },
                "independent_practice": [
                    "The argumentative essay on a self-chosen character from the work under study",
                    "A comparative paragraph placing the character beside an inherited type from the tradition",
                ],
            },
            "unschooling": {
                "invitations": [
                    "Keep the long shelf of difficult novels and stories whose characters reward returning, available, never assigned",
                    "Keep the commonplace book matured into a habit, with character passages set beside passages from other works whose characters work the same type",
                ],
                "real_world_contexts": [
                    "A reader who has returned to a beloved character across years and watched their reading of the character change",
                    "A long conversation in which two readers who love the same character bring a character from another book into the room",
                    "A piece of writing the reader produced because a character they have lived with finally asked something of them",
                ],
                "conversation_starters": [
                    "What does this book need this character to do that no other character could?",
                    "Which character in another book reminds you of this one? Read me the passage where the connection lives.",
                    "If this story were told by someone else, which character would change the most? What does that tell you about who they are here?",
                ],
                "resource_bank": [
                    "A shelf of difficult, worthy novels and stories gathered slowly across years, where the same character types recur in different writers' hands",
                    "A reader-companion of long acquaintance who has read across many traditions and can recognize an inherited type without naming it as a lesson",
                ],
                "parent_role": (
                    "By this band the parent has stepped back to fellow reader. They "
                    "are someone who has lived with the same kind of character in "
                    "their own returning, and they name the connection when the "
                    "student finds it: 'I think she's doing something like what "
                    "Dorothea does in Middlemarch; have you read that one yet?' The "
                    "parent does not assign the comparative work; they receive the "
                    "student's, and bring their own as another reader at the table."
                ),
                "observation_documentation": (
                    "Over time, notice whether the student returns to characters "
                    "across years and across books, recognizes inherited types on "
                    "their own when the type recurs, and writes about a character "
                    "because the character finally asked it of them. The pattern "
                    "surfaces because the reader returned; the noticing replaces any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": (
                "Montessori's literature pedagogy at the elementary and "
                "early-secondary level does not carry a distinct method for reading "
                "character as part of a work's argument or for the genealogy of "
                "inherited character types across the tradition; the practice here "
                "is drawn from the seminar tradition and the matured Charlotte "
                "Mason habit of narration and commonplace work across years rather "
                "than from the prepared environment."
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
            "lit-craft-020",
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
    "lit-craft-022": {
        "node_type": "craft",
        "strand": "theme and meaning",
        "band": "proficient",
        "prerequisites": ["theme and meaning: developing", "close reading: proficient"],
        "objective": (
            "Name more than one theme at work in a story or poem and articulate how "
            "they relate (reinforcing, complicating, or contending with one another); "
            "distinguish a writer's theme from a reader's moralized takeaway; "
            "articulate how specific craft choices (structure, point of view, imagery, "
            "plot rhythm) make a theme available; and defend a small original reading "
            "of a chosen theme line by line from the text."
        ),
        "core_understanding": (
            "A work of literary substance carries more than one theme, and its themes "
            "are not always at peace with one another. The proficient reader holds "
            "the work as a meaning-bearing whole in which craft choices and themes "
            "are continuous: a point-of-view choice, a recurring image, a scene's "
            "place in the structure are not decoration but the very way the theme "
            "becomes available. The reader also learns to distinguish theme from "
            "moral, the writer's reading from the reader's projection, and to defend "
            "a reading from the words rather than from received summary."
        ),
        "analytical_moves": [
            "Name more than one theme at work in a single text, in short sentences each grounded in a specific passage",
            "Show how two themes in the same work reinforce, complicate, or contend with each other",
            "Distinguish the theme the work supports from the moral a reader might wish onto it",
            (
                "Articulate how a specific craft choice (point of view, imagery, "
                "structure) makes a chosen theme available to the reader"
            ),
            ("Defend a small original reading of a chosen theme line by line, returning to the text for every claim"),
        ],
        "seminar_questions": [
            "What more than one theme is this work doing, and where in the text do you see each?",
            "Where do the themes of this work meet, and what happens when they do?",
            (
                "What is the difference between what this work says about its world "
                "and what we might want it to say? Which words tell you?"
            ),
        ],
        "writing_invitations": [
            (
                "Write a short analytical paragraph naming two themes at work in a "
                "chosen story or poem, quoting one passage for each, and arguing "
                "whether they reinforce, complicate, or contend with each other"
            ),
            (
                "Choose one craft choice in a work (a point of view, a recurring "
                "image, the placement of a scene) and write the paragraph that argues "
                "how that choice makes a chosen theme available"
            ),
        ],
        "exemplar_texts": [
            (
                "A worthy novel held whole in which more than one theme is plainly at "
                "work (To Kill a Mockingbird; A Wrinkle in Time; The Hobbit; Pride "
                "and Prejudice)"
            ),
            "A short story whose themes admit more than one reading (Chekhov; Joyce's Dubliners; Flannery O'Connor)",
            "A poem in which the theme rests on a specific craft choice (a Frost lyric; a Hopkins; a Wilfred Owen)",
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "Theme meets the seminar. The reader does not arrive with the "
                    "moral they had hoped to find; they arrive with the words, and "
                    "from the words a reading. The seminar tests it. Rhetorical and "
                    "interpretive habits converse: by what particular choices does "
                    "this writer make this theme available, and which theme, of more "
                    "than one possible, is bearing the weight of the work?"
                ),
                "memory_work": {
                    "recitations": [
                        "A passage central to a chosen theme of the work, recited from memory at the seminar's opening",
                    ],
                },
                "copywork": [
                    "The recited passage copied into the kept commonplace book, with the lines that bear the theme underlined",
                ],
                "recitation_routine": (
                    "Each seminar opens from a recited passage; the first question is "
                    "taken from the lines just heard and returns to the text for "
                    "every claim about theme."
                ),
                "read_aloud_suggestions": [
                    "A chapter at the heart of a chosen theme, read aloud at the seminar's opening",
                    "A poem whose theme rests on its form, read aloud whole more than once",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 40,
                "living_book_suggestions": [
                    "A worthy novel of layered theme, read whole at a sustained pace, not excerpted",
                    "A volume of poems or short stories read across a term, one at a sitting",
                ],
                "short_lesson_flow": (
                    "The proficient student reads the whole book at a sustained pace, "
                    "narrating each sitting. As themes emerge they are noted; passages "
                    "worth attending to are slipped or marked. At a chapter's end, one "
                    "such passage is taken up, copied into the commonplace book, and "
                    "discussed: which theme is at work here, and how is the writer "
                    "making it available? A small reading is allowed to form across "
                    "the long span and tested against the whole work."
                ),
                "narration_prompt": (
                    "Tell back the chapter you read, and tell me which themes you "
                    "saw at work, and which passage you would set down as the place "
                    "we most clearly see one of them, and why."
                ),
                "real_world_objects": [
                    "The whole novel, marked with the reader's own slips at the passages where theme is most plainly at work",
                    "A commonplace book gathering theme passages across many works",
                ],
                "nature_connection": (
                    "Theme in literature is to a book what a season is to the year: "
                    "not a thing one sees in any moment, but the long shape one comes "
                    "to feel from many moments held together."
                ),
                "habit_focus": (
                    "The habit of holding more than one theme in a work and returning "
                    "to the text for the evidence, and the habit of distinguishing "
                    "what the work says from what one wished it to say."
                ),
            },
            "traditional": {
                "introduction": (
                    "Explicit instruction in identifying more than one theme in a "
                    "work, in articulating how craft choices make theme available, in "
                    "distinguishing theme from moral, and in writing the short "
                    "analytical paragraph that defends a reading from the words."
                ),
                "gradual_release": {
                    "i_do": (
                        "Teacher reads a passage aloud, names two themes at work in "
                        "it, points to the craft choice (this point of view, this "
                        "image, this placement) that makes one of them available, and "
                        "writes a short paragraph on the board defending the reading, "
                        "quoting the passage line by line."
                    ),
                    "we_do": (
                        "Class chooses a candidate theme from the work under study, "
                        "gathers two or three decisive passages, and drafts together "
                        "a paragraph defending a small original reading, naming the "
                        "craft choice that makes the theme available, quoting the "
                        "lines that ground it."
                    ),
                    "you_do": (
                        "Student writes an independent analytical paragraph defending "
                        "a chosen reading of a chosen theme, naming one craft choice "
                        "that makes the theme available, with two or three quoted "
                        "passages as evidence, and revises after hearing a different "
                        "reading at seminar."
                    ),
                },
                "independent_practice": [
                    "The analytical paragraph on a self-chosen theme from the work under study",
                    "A short revision of the paragraph after seminar discussion",
                ],
            },
            "unschooling": {
                "invitations": [
                    "Keep the long shelf of novels, poetry, and story collections of real thematic substance, available, never assigned",
                    "Keep a commonplace book and small slips for marking theme passages in books the reader cares about",
                ],
                "real_world_contexts": [
                    "A long evening conversation about what a book is really doing, conducted as a real argument between readers",
                    "A piece of writing the reader composed because a theme in a book wanted writing back",
                    "A read-aloud of a passage so a fellow reader can hear which theme the reader heard in it",
                ],
                "conversation_starters": [
                    "What did this book turn out to be about, more than one thing?",
                    (
                        "Which choice the writer made (whose voice tells, which image "
                        "keeps coming back, which scene is where) lets you see the theme?"
                    ),
                    "What does the book say about its world, and what do we wish it said? Are they the same?",
                ],
                "resource_bank": [
                    "A shelf of difficult, worthy books whose themes reward attention",
                    "A reader-companion willing to argue a chosen theme as a fellow reader, not as an examiner",
                ],
                "parent_role": (
                    "Take the reader's reading seriously and ask them to take yours "
                    "seriously by going back to the lines. Be a fellow reader who "
                    "holds your own reading, is willing to hear another, and willing "
                    "to be moved by it."
                ),
                "observation_documentation": (
                    "Over time, notice whether the reader returns to themes across "
                    "books, defends a reading from the words, distinguishes theme "
                    "from moral, and holds more than one reading without giving up "
                    "their own. This noticing replaces any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": (
                "Montessori's literature pedagogy at the elementary and "
                "early-secondary level does not carry a distinct method for the "
                "sustained interpretive reading of theme; the practice here is drawn "
                "from the seminar tradition and the long Charlotte Mason habit of "
                "narration across whole books rather than from the prepared environment."
            ),
        },
    },
    "lit-craft-023": {
        "node_type": "craft",
        "strand": "theme and meaning",
        "band": "advanced",
        "prerequisites": ["theme and meaning: proficient", "close reading: proficient"],
        "objective": (
            "Argue a work's full thematic system as the very way the work means (not "
            "just naming themes and tying them to craft choices, but arguing that "
            "how the work means is its themes operating together as a structured "
            "whole); set the work's themes against its genre and against the "
            "inheritance the work intervenes in; honor what the work refuses to "
            "settle; and write the sustained essay that argues both the work's claim "
            "and what the work refuses, holding the two together."
        ),
        "core_understanding": (
            "At the proficient band the reader named more than one theme, "
            "articulated their relations, and tied each to a specific craft choice. "
            "At the advanced band the themes are no longer separable from the way "
            "the work means: the work's full thematic system is its very meaning, "
            "and a theme is not a thing the work contains but the shape the work has "
            "when its parts are held together. The reader meets the work's genre and "
            "the inheritance the work intervenes in: a tragedy is not a neutral "
            "form, a coming-of-age novel arrives carrying everything earlier "
            "coming-of-age novels have done with the form, and the writer is doing "
            "something to the inheritance. The reader also learns to honor what the "
            "work refuses to settle. The essay at this band argues both what the "
            "work claims and what the work refuses, and holds them together."
        ),
        "analytical_moves": [
            "Argue the work's full thematic system as constitutive of its meaning rather than as content the work delivers",
            "Set the work's themes against its genre and against the inheritance the work intervenes in",
            "Identify and honor what the work refuses to settle (genuine ambiguity, multiple endings, claims withheld)",
            (
                "Write the sustained essay that argues both the work's claim and "
                "what the work refuses, holding the two together"
            ),
            (
                "Hear another reader's account of the work's argument and locate "
                "where in the text and in the tradition that account draws its evidence"
            ),
        ],
        "seminar_questions": [
            "What is this work's whole argument, and how do its themes operate together to make it?",
            "Which inheritance does this work belong to, and where is the writer doing something the inheritance had not done?",
            "What does this work refuse to settle, and what is gained by leaving it unsettled?",
        ],
        "writing_invitations": [
            (
                "Write a sustained essay arguing a chosen work's whole thematic "
                "system as the very way the work means, holding three or four "
                "passages in productive tension and naming the work's place in its "
                "genre and its inheritance"
            ),
            "Write the paragraph that argues what a chosen work refuses to settle and what is gained by leaving it open",
        ],
        "exemplar_texts": [
            "A novel whose thematic system is its meaning (The Brothers Karamazov; Middlemarch held whole; Toni Morrison's Beloved)",
            "A tragedy in conversation with its genre (a Shakespeare tragedy whole, set beside a Greek tragedy in translation)",
            (
                "A modern novel that intervenes in an inheritance (Joyce's Ulysses "
                "against the epic; Charlotte Brontë's Jane Eyre against the "
                "bildungsroman of its day)"
            ),
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "Theme meets the long seminar and the genealogy of forms. The "
                    "reader brings the work's full argument as a hypothesis, the "
                    "seminar tests it, and the inheritance of the work's genre is "
                    "brought into the room. Rhetorical analysis and the history of "
                    "forms converge: by what particular choices does this writer "
                    "make this argument available, what does the inheritance the "
                    "work belongs to make possible and what does it foreclose, and "
                    "where does the work refuse to settle the question?"
                ),
                "memory_work": {
                    "recitations": [
                        "A passage in which the whole work's argument is most plainly at work, recited at the seminar's opening",
                        "A passage from another work in the inheritance the work intervenes in",
                    ],
                },
                "copywork": [
                    "The recited passage copied into the kept commonplace book, with the inheritance the work intervenes in noted in the margin",
                ],
                "recitation_routine": (
                    "Each seminar opens from two recited passages: one from the work "
                    "under study and one from elsewhere in the inheritance; the "
                    "first question is taken from what each lets the other see, and "
                    "the discussion returns to the text for every claim."
                ),
                "read_aloud_suggestions": [
                    "A scene at the heart of the work's argument read aloud at the seminar's opening",
                    "A passage from elsewhere in the work's inheritance, read aloud beside it",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 50,
                "living_book_suggestions": [
                    "A worthy novel whose argument is its themes operating as a structured whole, read whole at a sustained pace, narrated sitting by sitting",
                    "A second work earlier in the inheritance, read alongside or after to bring the inheritance into the commonplace work",
                ],
                "short_lesson_flow": (
                    "The advanced student reads the work whole at a sustained pace, "
                    "narrating each sitting. As the work's whole argument emerges, "
                    "passages worth attending to are slipped or marked. At a "
                    "chapter's end one is taken up, copied into the commonplace "
                    "book, and discussed: what is the work's whole argument, what "
                    "inheritance is it intervening in, and what does it refuse to "
                    "settle? When the second work in the inheritance is read, the "
                    "commonplace book holds the comparative passage. The essay is "
                    "allowed to form across the long span of the whole work."
                ),
                "narration_prompt": (
                    "Tell back what you read, and tell me what you think the whole "
                    "work is doing, and which passage you would set down as the "
                    "place we most clearly see the whole argument at work, and which "
                    "passage you would set beside it from another book in the inheritance."
                ),
                "real_world_objects": [
                    "The whole novel, marked at the passages decisive for the work's full argument",
                    "A commonplace book gathering thematic passages across many works and across the inheritance",
                ],
                "nature_connection": (
                    "The whole argument of a worthy book is to the work what the "
                    "shape of a season is to the year: not a thing one sees in any "
                    "moment but the long pattern that emerges from the many moments "
                    "held together."
                ),
                "habit_focus": (
                    "The habit of holding a whole work's argument as a hypothesis to "
                    "be tested against the text, and the habit of bringing the "
                    "inheritance of the work's genre into the reading."
                ),
            },
            "traditional": {
                "introduction": (
                    "Explicit instruction in arguing a work's full thematic system, "
                    "in setting the work against its genre and its inheritance, in "
                    "honoring what the work refuses to settle, and in writing the "
                    "sustained essay that holds the work's claim and what the work "
                    "refuses together."
                ),
                "gradual_release": {
                    "i_do": (
                        "Teacher works a chosen work on the board: names the work's "
                        "whole argument as a hypothesis, identifies the inheritance "
                        "the work intervenes in, names what the work refuses to "
                        "settle, and drafts the opening of a sustained essay that "
                        "holds the claim and the refusal together, quoting two "
                        "passages from the work and one from the inheritance."
                    ),
                    "we_do": (
                        "Class gathers the decisive passages of a chosen work, "
                        "weighs the work against its inheritance, names what the "
                        "work refuses to settle, and drafts together the body of "
                        "the sustained essay arguing both the work's claim and what "
                        "the work refuses."
                    ),
                    "you_do": (
                        "Student writes an independent sustained essay on a chosen "
                        "work, arguing its whole thematic system, naming the "
                        "inheritance the work intervenes in, honoring what the work "
                        "refuses to settle, and holding three or four passages in "
                        "productive tension, and revises after seminar."
                    ),
                },
                "independent_practice": [
                    "The sustained essay on a self-chosen work, arguing its whole thematic system and naming the inheritance",
                    "A paragraph naming and defending what the work refuses to settle",
                ],
            },
            "unschooling": {
                "invitations": [
                    "Keep the long shelf of difficult, worthy works the reader has returned to over years, available, never assigned",
                    "Keep the commonplace book matured into a habit, with passages from different works in conversation rather than in isolation",
                ],
                "real_world_contexts": [
                    "A reader who has lived with a single difficult novel across years and watched its whole argument surface as the patterns surfaced from many returns",
                    "A piece of writing the reader produced because two beloved books finally said something to each other in the reader's mind",
                    "A long conversation between two readers who have each lived with the same work in their own returning, each bringing their own passage",
                ],
                "conversation_starters": [
                    "What do you think this whole book is doing now, after all these returns?",
                    "Which other book that you have lived with does this one finally speak to? Read me the lines where they meet.",
                    "What does this book refuse to settle, and what would be lost if it settled it?",
                ],
                "resource_bank": [
                    "A shelf of difficult, worthy work gathered slowly across many years, where the reader's returns have made certain books theirs",
                    "A reader-companion of long acquaintance who has also done their long returning and can recognize a connection without naming it as a lesson",
                ],
                "parent_role": (
                    "By this band the parent has fully stepped back to fellow "
                    "reader. They are someone who has done their own long returning "
                    "to their own beloved works, and they name a connection when "
                    "the student finds one: 'I felt something like that when I "
                    "returned to King Lear last summer; have you read it lately?' "
                    "The parent does not orchestrate the inheritance the work "
                    "intervenes in; they receive what the student has brought up "
                    "out of their own returning and offer, as another reader at the "
                    "table, the passage their own returning gave them. The student "
                    "is leading their own reading life. The parent is now a witness "
                    "who can be asked, a reader whose long returnings furnished a "
                    "small library the student is also returning to, and a fellow "
                    "at the table when the student wants company."
                ),
                "observation_documentation": (
                    "Over time, notice whether the student returns to a small "
                    "handful of beloved works across years rather than chasing the "
                    "next book, whether the patterns surface in their conversation "
                    "about those works without prompting, and whether they begin to "
                    "feel the inheritance because their own returning led them into "
                    "it. The whole-argument reading and the work's genre and "
                    "inheritance show up because the student returned, not because "
                    "they were assigned. The pattern surfacing is the noticing; it "
                    "replaces any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": (
                "Montessori's literature pedagogy at the elementary and "
                "early-secondary level does not carry a distinct method for arguing "
                "a work's full thematic system or for placing the work in the "
                "inheritance it intervenes in; the practice here is drawn from the "
                "long seminar tradition and the matured Charlotte Mason habit of "
                "narration and commonplace work across years rather than from the "
                "prepared environment."
            ),
        },
    },
    "lit-craft-031": {
        "node_type": "craft",
        "strand": "narrative craft",
        "band": "advanced",
        "prerequisites": ["lit-craft-008", "close reading: proficient"],
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
    "lit-craft-041": {
        "node_type": "craft",
        "strand": "figurative language and symbol",
        "band": "developing",
        "prerequisites": ["figurative language and symbol: emerging", "close reading: developing"],
        "objective": (
            "Name simile and metaphor as two distinct figures, find each in a story or "
            "poem, distinguish them from literal description, and notice when an image "
            "or object in a story carries meaning beyond itself, proposing what it "
            "might stand for and pointing to the lines that support the reading."
        ),
        "core_understanding": (
            "Comparison is one of writing's most ordinary and most powerful tools. A "
            "simile says one thing is like another; a metaphor says one thing is "
            "another, without the bridge of 'like' or 'as.' Both ask the reader to "
            "hold two things together. At the developing band the reader also meets a "
            "second move: an image or object in a story may carry weight beyond its "
            "plain self, recurring or set apart so its meaning grows. Naming the figure "
            "and noticing the charged image is the developing reader's work; the "
            "proficient analysis of why the writer chose it comes later."
        ),
        "analytical_moves": [
            "Identify a simile in a passage and name the two things compared",
            (
                "Identify a metaphor and explain how it differs from a simile: no 'like' "
                "or 'as,' the writer claims the two are the same thing"
            ),
            "Distinguish a figurative description from a literal one in the same text",
            (
                "Notice an image or object that appears more than once, or that the "
                "writer sets apart, and propose what it might stand for"
            ),
            "Point to the lines in the text that support the proposed meaning",
        ],
        "seminar_questions": [
            (
                "Where in this passage does the writer compare two things? Is it a "
                "simile or a metaphor, and how can you tell?"
            ),
            "Why might the writer have chosen this figure of speech instead of plain saying?",
            "Does anything in this story keep coming back? What might it carry, and where do you see it?",
        ],
        "writing_invitations": [
            (
                "Write a short paragraph about a poem or scene that names the simile or "
                "metaphor, the two things compared, and what the comparison helps the "
                "reader see or feel"
            ),
            (
                "Choose a recurring image from a story you have read, quote the lines "
                "where it appears, and write what you think it stands for"
            ),
        ],
        "exemplar_texts": [
            (
                "A poem in which simile and metaphor sit close together (a Frost lyric "
                "such as Mending Wall; a short Dickinson; a Hopkins)"
            ),
            (
                "A worthy children's novel with a charged recurring image (the river in "
                "The Wind in the Willows; the lamp-post in The Lion, the Witch and the "
                "Wardrobe; the locket in The Secret Garden)"
            ),
            "A fable or folk tale whose central object turns symbolic (the magic mirror, the golden key)",
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "After comparison has been heard, the names arrive. Simile and "
                    "metaphor are not new things, only new words for what the reader "
                    "already noticed. The recurring image is offered as the next layer: "
                    "a writer may set a single image, returned to and returned to, and "
                    "let it carry more than its plain self."
                ),
                "memory_work": {
                    "recitations": [
                        "A simile recited from a chosen poem",
                        "A metaphor recited from a chosen poem",
                    ],
                },
                "copywork": [
                    (
                        "A line containing a simile and a line containing a metaphor, "
                        "copied side by side, with each figure named in the margin"
                    ),
                ],
                "recitation_routine": (
                    "Each session opens with yesterday's lines recited; the new lesson "
                    "begins from 'what is compared today, and is it a simile or a metaphor?'"
                ),
                "read_aloud_suggestions": [
                    "A poem rich in both simile and metaphor read aloud whole",
                    (
                        "A chapter of a worthy children's novel in which a recurring "
                        "image appears, read aloud across several sittings"
                    ),
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A worthy children's novel in which an image or object carries weight across the book",
                    "A volume of poems with clear and lively comparison",
                ],
                "short_lesson_flow": (
                    "Read the passage or short poem aloud, attentively. The child "
                    "narrates. Then ask: did you hear a comparison? Is it a simile or a "
                    "metaphor? What two things? Over time, when reading a longer book, "
                    "notice together when an image keeps coming back, and ask the child "
                    "what they think it stands for and where they see it in the text."
                ),
                "narration_prompt": (
                    "Tell back what we read, and tell me what was compared, whether it "
                    "was a simile or a metaphor, and whether any image kept coming back."
                ),
                "real_world_objects": [
                    "The whole book or poem in hand, marked at recurring images with the child's own slips",
                    (
                        "A small commonplace book in which simile, metaphor, and "
                        "recurring image are gathered as they are met"
                    ),
                ],
                "nature_connection": (
                    "The recurring image in literature is to a book what a nature "
                    "notebook is to the year: the same thing observed many times, and "
                    "meaning growing in it because it has been returned to."
                ),
                "habit_focus": (
                    "The habit of naming a figure when one is heard, and the habit of "
                    "noticing when an image is set apart or returned to and asking what it carries."
                ),
            },
            "traditional": {
                "introduction": (
                    "Explicit instruction in simile and metaphor as distinct figures of "
                    "speech, with practice in identifying each, and an introduction to "
                    "the recurring image or charged object as a doorway to symbol."
                ),
                "gradual_release": {
                    "i_do": (
                        "Teacher reads a passage aloud and names each figure as it "
                        "appears: 'The clouds were like ships under sail: simile, with "
                        "the word like, comparing clouds and ships. The road was a "
                        "ribbon of moonlight: metaphor, no like, the road is called a "
                        "ribbon. They are two ways of comparing.'"
                    ),
                    "we_do": (
                        "Class works through a second passage together, surfacing "
                        "similes and metaphors and naming the two things compared in "
                        "each. Then the teacher introduces a recurring image from a book "
                        "the class is reading, and together they list the places it "
                        "appears and propose what it might stand for."
                    ),
                    "you_do": (
                        "Student finds and names similes and metaphors independently in "
                        "a new passage and proposes a reading of a recurring image from "
                        "the book under study, with quoted evidence."
                    ),
                },
                "independent_practice": [
                    "A short notebook entry of similes and metaphors found and named in a chosen passage",
                    "A short paragraph proposing the meaning of a recurring image from the book under study",
                ],
            },
            "unschooling": {
                "invitations": [
                    "Keep poetry and worthy children's novels rich in figure and image within reach",
                    "Use simile and metaphor of your own in plain talk so the child hears that grown people use them too",
                ],
                "real_world_contexts": [
                    "Catching a metaphor in a song lyric and asking what two things are being held together",
                    (
                        "Noticing a recurring object in a movie or book the child is "
                        "loving, and wondering aloud what it carries"
                    ),
                    "Drawing a recurring image and writing a line under it about what it might mean",
                ],
                "conversation_starters": [
                    "Was that a simile or a metaphor? Which words tell you?",
                    "Why do you think the writer said it that way instead of saying it plainly?",
                    "Does anything in this book keep coming back? What do you think it carries?",
                ],
                "resource_bank": [
                    "A shelf of poetry, worthy children's novels, and folk tales in which image and figure are at work",
                    "A reader-companion willing to wonder about a recurring image as a fellow reader, not as an examiner",
                ],
                "parent_role": (
                    "Be a reader who notices figures and images aloud when you meet "
                    "them, and welcome the child's noticings as a fellow reader. Trust "
                    "the names (simile, metaphor) when they become useful, and not "
                    "before; the figure is heard before it is named."
                ),
                "observation_documentation": (
                    "Over time, notice whether the child names simile and metaphor on "
                    "their own when they meet them, and whether they begin to wonder at "
                    "recurring images in stories without prompting. This noticing "
                    "replaces any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": (
                "Montessori at this band does not carry a distinct method for naming "
                "simile and metaphor or for reading the recurring image as a doorway "
                "to symbol; the elementary literature work in the prepared environment "
                "centers on the great-lesson narratives, the grammar boxes, and the "
                "child's chosen reading rather than on figures of speech."
            ),
        },
    },
    "lit-craft-042": {
        "node_type": "craft",
        "strand": "figurative language and symbol",
        "band": "proficient",
        "prerequisites": ["figurative language and symbol: developing", "close reading: proficient"],
        "objective": (
            "Read figurative language as part of how a work makes meaning, not as "
            "decoration: trace a network of related images or symbols across the "
            "work and articulate how they function together; distinguish a "
            "conventional symbol (the rose, the journey) from a writer's particular "
            "figurative invention; defend a small original reading of a symbol or "
            "figurative system from specific passages; and recognize when a figure "
            "resists a single reading and hold the openness without giving up evidence."
        ),
        "core_understanding": (
            "At the proficient band the reader sees that figurative language is not "
            "ornament: in a worthy work the figures do work. A network of related "
            "images may carry the work's meaning more powerfully than any direct "
            "statement; a symbol may bring in a long inheritance of meaning the "
            "writer is using or refusing; a metaphor may be the way an idea becomes "
            "available at all. The reader tracks these figures across the whole "
            "work, distinguishes inherited symbols from a writer's particular "
            "inventions, and defends a reading by returning to the lines. They also "
            "learn to honor figures that resist a single reading and to hold more "
            "than one without surrendering the discipline of evidence."
        ),
        "analytical_moves": [
            "Track a network of related images or symbols across a whole work and articulate how the network functions together",
            (
                "Distinguish a conventional symbol (the rose, the journey, the storm) "
                "from a writer's particular figurative invention in this work"
            ),
            (
                "Read figurative language as in service of theme and character, "
                "naming what work the figure does in the meaning of the whole"
            ),
            (
                "Defend a small original reading of a symbol or figurative system "
                "line by line, returning to the text for every claim"
            ),
            (
                "Hold a figure that resists a single reading, naming the more than "
                "one reading the words support and what is gained by leaving it open"
            ),
        ],
        "seminar_questions": [
            "Which images in this work travel together, and what do they do in concert that none of them does alone?",
            "Where does this writer use an inherited symbol and where do they invent their own? Which words tell you?",
            "Is there a figure in this work that refuses to settle into one reading? What does that refusal do?",
        ],
        "writing_invitations": [
            (
                "Write a short analytical paragraph arguing how a network of related "
                "images in a chosen work makes a theme or a character available, "
                "quoting two or three passages"
            ),
            (
                "Write the paragraph defending a small original reading of a single "
                "symbol from a work, naming whether it is inherited or invented and "
                "grounding the reading line by line"
            ),
        ],
        "exemplar_texts": [
            (
                "A worthy novel whose figurative network is part of how it means "
                "(Moby-Dick; The Scarlet Letter; A Wrinkle in Time; The Lord of the Rings)"
            ),
            "A poem in which figure is the work's substance, not its decoration (a Hopkins; a Dickinson; a Yeats lyric)",
            (
                "A short story whose central object turns symbolic in the writer's "
                "particular way (Joyce's Araby; O'Connor's A Good Man Is Hard to Find; Welty)"
            ),
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "Figure meets the seminar. The reader has named simile and "
                    "metaphor and has heard a recurring image carry weight. At this "
                    "band a further step: the figures travel together, and what they "
                    "do together is the work's meaning. Rhetorical tradition and "
                    "interpretive habit converse: which figures has this writer "
                    "chosen, which has the writer inherited from the long tradition, "
                    "and what does the writer make them do?"
                ),
                "memory_work": {
                    "recitations": [
                        "A passage in which a figure or a symbolic image bears the weight of the work, recited at the seminar's opening",
                    ],
                },
                "copywork": [
                    "The recited passage copied into the kept commonplace book, with the figurative words underlined",
                ],
                "recitation_routine": (
                    "Each seminar opens from a recited passage of figure or symbol; "
                    "the first question is taken from the lines just heard and "
                    "returns to the text for every claim."
                ),
                "read_aloud_suggestions": [
                    "A chapter rich in a chosen figurative network, read aloud at the seminar's opening",
                    "A poem whose substance is figure, read aloud whole more than once",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 40,
                "living_book_suggestions": [
                    "A worthy novel whose figurative work is sustained across the book, read whole at a sustained pace",
                    "A volume of poetry in which figure is the substance, read across a term",
                ],
                "short_lesson_flow": (
                    "The proficient student reads the whole work at a sustained "
                    "pace, narrating each sitting. The recurring images and symbols "
                    "are marked or slipped as they are met. At a chapter's end one "
                    "passage of figurative weight is taken up, copied into the "
                    "commonplace book, and discussed: how does this figure travel "
                    "through the book, is it the writer's own or an inheritance, and "
                    "what does it do in the meaning of the whole?"
                ),
                "narration_prompt": (
                    "Tell back the chapter you read, and tell me which images "
                    "travel together in the book, and which one passage you would "
                    "set down as the place we most clearly see them at work."
                ),
                "real_world_objects": [
                    "The whole novel, marked with the reader's own slips at the passages where figurative work is plainest",
                    "A commonplace book gathering figurative passages across many works",
                ],
                "nature_connection": (
                    "The recurring image in a novel is to a book what a single bird "
                    "returned to across a year is to a nature notebook: not the same "
                    "in any one moment, but slowly known by the many."
                ),
                "habit_focus": (
                    "The habit of seeing figure as the work's meaning rather than as "
                    "its decoration, and the habit of returning to the text for "
                    "evidence rather than relying on received reading."
                ),
            },
            "traditional": {
                "introduction": (
                    "Explicit instruction in tracking a figurative network across a "
                    "work, in distinguishing inherited from invented symbol, in "
                    "reading figure in service of theme and character, and in "
                    "writing the short analytical paragraph that defends a reading "
                    "from the words."
                ),
                "gradual_release": {
                    "i_do": (
                        "Teacher reads passages aloud in which a network of related "
                        "images appears, names the images, names whether each is "
                        "inherited or invented in this writer, and writes a short "
                        "paragraph on the board arguing what the network does in the "
                        "work's meaning, quoting the passages line by line."
                    ),
                    "we_do": (
                        "Class gathers two or three passages of a chosen figurative "
                        "network from the work under study, weighs whether the "
                        "figures are inherited or invented, and drafts together a "
                        "paragraph defending a small original reading of the "
                        "network, quoting the lines that ground it."
                    ),
                    "you_do": (
                        "Student writes an independent analytical paragraph "
                        "defending a chosen reading of a figurative network or a "
                        "single symbol from the work under study, naming inherited "
                        "and invented elements and grounding the reading line by "
                        "line, and revises after hearing a different reading at seminar."
                    ),
                },
                "independent_practice": [
                    "The analytical paragraph on a self-chosen figurative network or symbol from the work under study",
                    "A short revision of the paragraph after seminar discussion",
                ],
            },
            "unschooling": {
                "invitations": [
                    "Keep the long shelf of novels, poetry, and stories rich in figurative substance, available, never assigned",
                    "Keep a commonplace book and small slips for marking figurative passages in books the reader cares about",
                ],
                "real_world_contexts": [
                    "A long evening conversation about why a writer keeps returning to a single image and what it does in the whole book",
                    "A piece of writing the reader composed because a symbol in a book asked something of them",
                    "A read-aloud of a passage so a fellow reader can hear the network the reader has begun to see",
                ],
                "conversation_starters": [
                    "Which images keep coming back in this book, and what do they do together?",
                    "Is this writer using the symbol the way it always gets used, or making it their own? Which words tell you?",
                    "Is there a figure in here that will not settle into one meaning? What does that openness do?",
                ],
                "resource_bank": [
                    "A shelf of difficult, worthy books whose figurative work rewards attention",
                    "A reader-companion willing to argue a chosen figure or symbol as a fellow reader, not as an examiner",
                ],
                "parent_role": (
                    "Be a reader who notices figurative networks aloud when you meet "
                    "them and welcomes the reader's noticings as a fellow reader. "
                    "Take the openness of figures seriously: a figure that refuses "
                    "one reading is doing work."
                ),
                "observation_documentation": (
                    "Over time, notice whether the reader tracks figurative networks "
                    "across books, distinguishes inherited from invented symbols, "
                    "defends a reading line by line, and honors figures that resist "
                    "a single reading. This noticing replaces any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": (
                "Montessori's literature pedagogy at the elementary and "
                "early-secondary level does not carry a distinct method for the "
                "analytical reading of figurative networks and symbol; the practice "
                "here is drawn from the seminar tradition and the long Charlotte "
                "Mason habit of narration across whole books rather than from the "
                "prepared environment."
            ),
        },
    },
    "lit-craft-043": {
        "node_type": "craft",
        "strand": "figurative language and symbol",
        "band": "advanced",
        "prerequisites": ["figurative language and symbol: proficient", "lit-craft-031", "close reading: proficient"],
        "objective": (
            "Read irony as the writer's gap between figure and literal claim, a "
            "refusal that itself bears meaning; read the work's full figurative "
            "system as constitutive of its meaning rather than supportive of it; "
            "trace inherited figures (the wasteland, the journey, the descent, the "
            "threshold) across the tradition and ask what this writer does with the "
            "inheritance; recognize when a figure does work the work cannot do in "
            "plain language at all."
        ),
        "core_understanding": (
            "At the proficient band the reader tracked figurative networks across a "
            "whole work, distinguished inherited from invented symbol, and defended "
            "a small original reading line by line. At the advanced band the figure "
            "is the work's argument and not its support: certain things a work "
            "needs to mean cannot be said plainly, and a writer chooses figure "
            "because plain language cannot carry the meaning. The reader also meets "
            "irony as figure's farthest reach: a gap between the literal claim and "
            "what the work lets the reader infer, a refusal of plain saying that "
            "itself does the work. (Irony in this sense is a near-relation of the "
            "unreliable narrator's gap, which is why the narrative-craft advanced "
            "node sits in the prerequisite chain.) The reader brings the tradition "
            "to the figure: an inherited figure carries with it everything earlier "
            "writers have done with it, and a writer using it is doing something to "
            "an inheritance."
        ),
        "analytical_moves": [
            "Read irony as the writer's gap between figure and literal claim and argue what the refusal of plain saying is doing in the work",
            "Argue the work's full figurative system as constitutive of its meaning rather than as a layer added on top of it",
            "Trace an inherited figure across the tradition and argue what this writer does with the inheritance",
            "Identify a meaning the work makes available only through figure and could not make available in plain language at all",
            "Write the sustained essay that argues a work's figurative argument, holding multiple passages in productive tension",
        ],
        "seminar_questions": [
            "Where in this work does plain saying fail, and what does the figure do that plain saying could not?",
            "Which inherited figure is this work working with, and what is the writer doing to it?",
            "Where does this work say one thing and let the reader infer another, and what is gained by the gap?",
        ],
        "writing_invitations": [
            (
                "Write a sustained essay arguing a chosen work's figurative argument "
                "as the very way the work means, holding three or four passages in "
                "productive tension and naming the inherited figures the work is "
                "working with"
            ),
            (
                "Write the paragraph that argues what a single ironic moment in a "
                "work is refusing to say plainly and what is gained by the refusal"
            ),
        ],
        "exemplar_texts": [
            (
                "A novel whose figurative system is its meaning (Moby-Dick; The "
                "Scarlet Letter; T. S. Eliot's The Waste Land if poetry is included; "
                "Tolkien's Lord of the Rings against the inheritance of the quest)"
            ),
            "A novel whose central move is ironic (Pride and Prejudice's narrator; a Mark Twain; an Austen)",
            (
                "A poem whose figurative argument the reader has lived with long "
                "enough to feel its inheritance (a Hopkins set against the "
                "tradition of devotional poetry; a Yeats set against Romantic "
                "inheritance)"
            ),
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "Figure meets the long seminar and the genealogy of figures. The "
                    "reader has tracked networks across a work and named inherited "
                    "symbol; now the figure is the argument, irony is its farthest "
                    "reach, and the tradition's stock of figures comes into the "
                    "room. Rhetorical analysis and the history of figures converge: "
                    "by what particular choices does this writer make this "
                    "figurative argument available, which inherited figures has the "
                    "writer taken up, and where does the work refuse to say plainly "
                    "what figure does for it?"
                ),
                "memory_work": {
                    "recitations": [
                        "A passage in which a work's whole figurative argument is most plainly at work, recited at the seminar's opening",
                        "A passage from elsewhere in the tradition handling the same inherited figure",
                    ],
                },
                "copywork": [
                    "The recited passage copied into the kept commonplace book, with the inherited figure the writer is working with noted in the margin",
                ],
                "recitation_routine": (
                    "Each seminar opens from two recited passages: one from the work "
                    "under study and one from elsewhere in the inheritance of the "
                    "figure; the first question is taken from what each lets the "
                    "other see, and the discussion returns to the text for every claim."
                ),
                "read_aloud_suggestions": [
                    "A passage at the heart of a work's figurative argument, read aloud at the seminar's opening",
                    "A passage from elsewhere in the tradition working the same inherited figure, read aloud beside it",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 50,
                "living_book_suggestions": [
                    "A worthy novel whose figurative argument is sustained across the work, read whole at a sustained pace",
                    "A second work earlier in the inheritance of the same figure, read alongside or after to bring the inheritance into the commonplace work",
                ],
                "short_lesson_flow": (
                    "The advanced student reads the work whole at a sustained pace, "
                    "narrating each sitting. As the figurative argument emerges, "
                    "passages are slipped or marked, including moments of irony "
                    "where the work refuses plain saying. At a chapter's end one "
                    "passage is taken up, copied into the commonplace book, and "
                    "discussed: what figurative argument is this work making, what "
                    "inherited figures is the writer working with, and where does "
                    "the figure do work that plain language could not? When the "
                    "second work in the inheritance is read, the commonplace book "
                    "holds the comparative passage."
                ),
                "narration_prompt": (
                    "Tell back what you read, and tell me which figure in the work "
                    "is doing what plain saying could not, and which passage from "
                    "elsewhere in the inheritance you would set beside it."
                ),
                "real_world_objects": [
                    "The whole work, marked at passages where the figurative argument is most plainly at work and where irony refuses plain saying",
                    "A commonplace book gathering figurative passages and the inherited figures they belong to across many works",
                ],
                "nature_connection": (
                    "A figurative argument in a worthy book is to the work what a "
                    "long-watched feature of a landscape is to a naturalist: not a "
                    "thing seen at a glance, but the meaning a place carries that "
                    "only the long returning reveals."
                ),
                "habit_focus": (
                    "The habit of asking what plain language could not do that the "
                    "figure does, and the habit of bringing the inheritance of "
                    "figures into the reading of a particular work."
                ),
            },
            "traditional": {
                "introduction": (
                    "Explicit instruction in reading irony as figure's gap between "
                    "literal claim and inference, in arguing a work's full "
                    "figurative system as the very way the work means, in tracing "
                    "inherited figures across the tradition, and in writing the "
                    "sustained essay that argues the work's figurative argument."
                ),
                "gradual_release": {
                    "i_do": (
                        "Teacher works a chosen work on the board: names the work's "
                        "figurative argument as a hypothesis, identifies the "
                        "inherited figures the writer is working with, points to a "
                        "moment of irony where the work refuses plain saying, and "
                        "drafts the opening of a sustained essay that argues the "
                        "figurative argument, quoting two passages from the work "
                        "and one from the inheritance."
                    ),
                    "we_do": (
                        "Class gathers the decisive figurative passages of a chosen "
                        "work, weighs the writer's use of an inherited figure, "
                        "identifies moments of ironic refusal, and drafts together "
                        "the body of the sustained essay arguing the figurative argument."
                    ),
                    "you_do": (
                        "Student writes an independent sustained essay on a chosen "
                        "work, arguing its figurative argument, naming the "
                        "inherited figures it works with, identifying a moment of "
                        "irony as figure's refusal, and holding three or four "
                        "passages in productive tension, and revises after seminar."
                    ),
                },
                "independent_practice": [
                    "The sustained essay on a self-chosen work, arguing its figurative argument and naming the inherited figures",
                    "A paragraph on a single ironic moment in the work, arguing what the refusal is doing",
                ],
            },
            "unschooling": {
                "invitations": [
                    "Keep the long shelf of difficult, worthy works rich in figurative substance, the ones the reader has returned to over years, available, never assigned",
                    "Keep the commonplace book matured into a habit, with figurative passages from different works set in conversation rather than in isolation",
                ],
                "real_world_contexts": [
                    "A reader who has lived with a single figurative network across years and watched it surface as the patterns surfaced from many returns",
                    "A piece of writing the reader produced because a moment of irony in a long-beloved book finally became plain to them as refusal",
                    "A long conversation in which two readers who have each lived with the same work bring the same inherited figure from different books into the room",
                ],
                "conversation_starters": [
                    "What does this figure in this book do that plain saying could not? When did that become plain to you?",
                    "Which other book that you have lived with works the same figure? Read me the passage where the connection lives.",
                    "Where does this book say one thing and let you infer another? When did you start to feel the gap?",
                ],
                "resource_bank": [
                    "A shelf of difficult, worthy work in which figure is the substance, gathered slowly across many years",
                    "A reader-companion of long acquaintance who has done their own long returning to figurative work and can recognize an inherited figure without naming it as a lesson",
                ],
                "parent_role": (
                    "By this band the parent has fully stepped back to fellow "
                    "reader. They are someone who has done their own long returning "
                    "to figurative work in their own beloved books, and they name a "
                    "connection when the student finds one: 'I felt something like "
                    "that when I returned to The Waste Land last winter; have you "
                    "read it lately?' The parent does not catalogue the inheritance "
                    "of figures; they receive what the student has brought up out "
                    "of their own returning and offer, as another reader at the "
                    "table, the passage their own returning gave them. The student "
                    "is leading their own reading life; the parent is a witness "
                    "whose long returnings furnished a small library the student "
                    "is also returning to."
                ),
                "observation_documentation": (
                    "Over time, notice whether the student returns to figurative "
                    "work in their beloved books across years, whether moments of "
                    "irony surface as refusal in their conversation about those "
                    "books without prompting, and whether they begin to recognize "
                    "an inherited figure when it recurs because their own returning "
                    "led them into it. The figurative argument shows up because "
                    "the student returned; the noticing replaces any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": (
                "Montessori's literature pedagogy at the elementary and "
                "early-secondary level does not carry a distinct method for arguing "
                "a work's full figurative system, for tracing inherited figures "
                "across the tradition, or for reading irony as figure's refusal of "
                "plain saying; the practice here is drawn from the long seminar "
                "tradition and the matured Charlotte Mason habit of narration and "
                "commonplace work across years rather than from the prepared environment."
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
    "lit-work-002": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "The Iliad",
            "author": "Homer",
            "date": "c. 8th century BCE",
            "genre": "epic",
            "form": "epic poem",
        },
        "minimum_band": "proficient",
        "content_notes": (
            "Pervasive battlefield violence, the deaths of named warriors at length, "
            "the desecration of Hector's body; honest information, not a gate."
        ),
        "craft_focus": [
            "The wrath structure: a single emotion as the poem's whole arc",
            "Embedded speech: the great set-piece speeches (Achilles to the embassy; Priam's appeal)",
            "Hector and the cost on the other side",
            "The Homeric simile, especially in the killing-scenes where simile slows the violence",
            "The hero as the work's argument (what the poem needs Achilles to be)",
        ],
        "entry": (
            "Proficient: meet the wrath of Achilles as the poem's single arc, follow "
            "embedded speech as a way characters become available, name the structural "
            "function of the simile. Advanced: argue what the poem refuses to settle "
            "about Achilles, set Achilles against the inherited warrior-hero type, "
            "read the simile as a figurative system. Mastery: original argument about "
            "what the Iliad does to the warrior-hero tradition and what it asks its "
            "inheritors to do with the form."
        ),
        "close_reading_passages": [
            "The proem and the question of wrath: what does the poem say it is about, and what does the wrath include?",
            "The embassy to Achilles (Book 9): what does Achilles refuse, and what does the language of his refusal reveal?",
            "Priam's visit to Achilles (Book 24): how does the poem end, and what does the ending refuse to say?",
        ],
        "structural_analysis": (
            "A single emotion, the wrath of Achilles, gives the poem its arc; the "
            "action begins and ends not at the war's beginning or end but at the rise "
            "and softening of that wrath. The structure makes the poem's argument: "
            "the warrior-hero's choice is named through what the wrath leaves out and "
            "what it admits at the end."
        ),
        "thematic_lines": [
            "What the poem counts as honor, and the cost of demanding it absolutely",
            "Hector and the cost on the other side: a poem of one side that lets the other side be seen",
            "Mortality, time, and the meaning of choosing the short, bright life",
        ],
        "comparative_threads": [
            "lit-work-001 (Odyssey): the hero who returns set beside the hero who chooses honor",
            "lit-work-003 (Aeneid): the founder set against the warrior; Virgil's conscious reply to Homer",
        ],
        "seminar_questions": [
            "Is the wrath of Achilles fully justified by the poem, and where does the poem refuse to say?",
            "What does Hector let us see that Achilles cannot, and what does the poem do with that?",
            "What changes when Priam crosses the lines? Does Achilles change, or only soften?",
        ],
        "writing_invitations": [
            "The analytical paragraph on a single Homeric simile, naming what it slows and what it expands",
            "The essay on whether the poem endorses Achilles",
            "At advanced, the comparative essay setting Achilles against an inherited warrior-hero type the poem is working with",
        ],
        "context": (
            "The oral epic tradition, the world of bronze-age siege and aristocratic "
            "honor, the poem at the head of the Western canon alongside the Odyssey; "
            "supplied as fact, interpretation left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "The foundational great-books seminar text on heroic honor; the wrath of Achilles examined rhetorically and ethically."
                ),
                "memory_work": {
                    "recitations": ["Recitation of the proem"],
                },
                "recitation_routine": (
                    "Seminar opens from the recited proem; the discussion takes its "
                    "first question from the line that names what the wrath includes."
                ),
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy translation of the Iliad, read aloud as a living book (Fitzgerald, Lattimore, or Wilson)",
                ],
                "short_lesson_flow": (
                    "A living book read aloud and narrated; the wrath followed sitting "
                    "by sitting, deepening to analysis of the great set-piece speeches "
                    "as the bands move up."
                ),
                "narration_prompt": (
                    "Tell back the part we read today, and tell me what you noticed about Achilles or Hector this time."
                ),
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy translation of the Iliad on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in heroes, honor, or war leads, no imposed apparatus",
                ],
                "parent_role": ("Read aloud and discuss where the student's interest leads; no imposed apparatus."),
                "observation_documentation": (
                    "Over time, notice whether the student returns to the poem and "
                    "follows its questions into other reading. This noticing replaces any test."
                ),
            },
            "traditional": {
                "introduction": "Structured study of epic conventions and the great set-piece speeches where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-003": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "The Aeneid",
            "author": "Virgil",
            "date": "c. 29-19 BCE",
            "genre": "epic",
            "form": "epic poem",
        },
        "minimum_band": "proficient",
        "content_notes": (
            "Battlefield violence; the suicide of Dido; the killing of Turnus at "
            "the poem's close, on which the poem ends without comment; honest "
            "information, not a gate."
        ),
        "craft_focus": [
            "The conscious reply to Homer: the first six books as Odyssey, the second six as Iliad",
            "Pietas as the hero's defining quality and its cost",
            "The Virgilian simile and its conscious differences from Homer's",
            "The ending that refuses to comment on the killing of Turnus",
            "Dido as the figure the poem cannot quite leave behind",
        ],
        "entry": (
            "Proficient: meet Aeneas as the reluctant founder, follow the conscious "
            "reply to Homer, name pietas as the hero's defining quality and ask "
            "what it costs. Advanced: read the simile as Virgil's revision of "
            "Homer's, argue what the poem refuses to settle about the killing of "
            "Turnus, set Aeneas against the inheritance of the warrior-hero. "
            "Mastery: original argument about what the Aeneid does to the epic "
            "tradition and what the empire it founds is, in the poem's own measure."
        ),
        "close_reading_passages": [
            "The proem and the question of what the poem invokes: arms and the man, but in what order?",
            "The fall of Troy as Aeneas tells it (Book 2): what does the first-person frame let the poem do?",
            "The killing of Turnus and the poem's last lines: what does the poem refuse to say?",
        ],
        "structural_analysis": (
            "Twelve books built consciously as a reply to Homer: the first six echo "
            "the Odyssey (wandering, the descent to the underworld), the second six "
            "echo the Iliad (war in Italy, the killing). The structure is the "
            "poem's argument: the founder must do both the journey and the war, "
            "and the cost of both is the poem."
        ),
        "thematic_lines": [
            "Pietas: duty, piety, devotion to family, gods, and the founded city",
            "The cost of founding: who pays, and what is paid",
            "Dido and the woman the foundation leaves behind",
        ],
        "comparative_threads": [
            "lit-work-001 (Odyssey): the model for the journey half of the poem",
            "lit-work-002 (Iliad): the model for the war half; together they form the conscious shadow the Aeneid argues with",
        ],
        "seminar_questions": [
            "Does Aeneas's pietas exonerate the killing of Turnus, and does the poem think so?",
            "What does the poem do with Dido that it cannot quite undo?",
            "Why does Virgil write so consciously inside Homer? What does the doubling argue?",
        ],
        "writing_invitations": [
            "The analytical paragraph on a Virgilian simile set beside a Homeric simile, naming what each lets the reader see",
            "The essay on whether the killing of Turnus is just, in the poem's own measure",
            "At advanced, the comparative essay on Aeneas against an inherited hero type the poem is consciously working with",
        ],
        "context": (
            "The poem composed for the Augustan moment, the foundational text of "
            "imperial Rome and a deeply Roman reading of Greek epic; supplied as "
            "fact, interpretation left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "The foundational Latin epic in conversation with Homer; pietas examined rhetorically and ethically."
                ),
                "memory_work": {
                    "recitations": ["Recitation of the proem"],
                },
                "recitation_routine": (
                    "Seminar opens from the recited proem; the discussion takes its "
                    "first question from the order of arma virumque (arms and the "
                    "man) and what that order tells."
                ),
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy translation of the Aeneid, read aloud as a living book (Fitzgerald, Mandelbaum, or Sarah Ruden)",
                ],
                "short_lesson_flow": (
                    "A living book read aloud and narrated; the journey followed "
                    "and the war followed, deepening to analysis of Virgil's "
                    "conscious reply to Homer as the bands move up."
                ),
                "narration_prompt": (
                    "Tell back the part we read today, and tell me what you noticed about Aeneas (or Dido, or Turnus) this time."
                ),
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy translation of the Aeneid on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in Rome, duty, or the cost of founding leads, no imposed apparatus",
                ],
                "parent_role": ("Read aloud and discuss where the student's interest leads; no imposed apparatus."),
                "observation_documentation": (
                    "Over time, notice whether the student returns to the poem and "
                    "brings it into conversation with the Homeric epics. This "
                    "noticing replaces any test."
                ),
            },
            "traditional": {
                "introduction": "Structured study of epic conventions and Virgil's conscious revision of Homer where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-004": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Beowulf",
            "author": "anonymous",
            "date": "c. 8th-11th century, oral tradition older still",
            "genre": "epic",
            "form": "alliterative epic-elegiac poem in modern English translation",
        },
        "minimum_band": "developing",
        "content_notes": (
            "Monster combat, the killing of Grendel and the dragon, an elegiac "
            "mood throughout, mortality; honest information, not a gate."
        ),
        "craft_focus": [
            "The three-combat structure: youth (Grendel), maturity (Grendel's mother), age (the dragon)",
            "The kenning as figurative system (whale-road for sea, bone-house for body, ring-giver for king)",
            "The elegiac digressions: the doomed hall, fame and what outlives it, wyrd (fate)",
            "The hero who is also a king and a man who dies",
            "The Christian-pagan interweave the poem makes its own",
        ],
        "entry": (
            "Developing: follow Beowulf-Grendel-the-mother-the-dragon as a hero "
            "story across three ages and narrate it; notice kennings without "
            "analyzing them. Proficient: name the three-combat structure, hold the "
            "elegiac mood beside the heroic action, read the kennings as a "
            "figurative system, ask what the poem counts as fame. Advanced: argue "
            "what the poem does to the inherited dragon-slayer type, read the "
            "elegiac as constitutive of the poem's meaning, set the "
            "Christian-pagan interweave as the poem's unsettled question. "
            "Mastery: original argument about what Beowulf does to the "
            "heroic-elegiac form and how Tolkien (and others) inherit it."
        ),
        "close_reading_passages": [
            "The opening (Hwaet!) and the lineage of Hrothgar's hall: how does the poem begin, and what does the beginning tell us about what the poem cares to remember?",
            "The fight with Grendel's mother in the mere: what does the underwater fight do that the hall-fight could not?",
            "The dragon and the elegy of the last survivor: what does the poem hold up at the end, the hero or the doom?",
        ],
        "structural_analysis": (
            "Three combats across the hero's life (Grendel in youth, Grendel's "
            "mother in maturity, the dragon in age), set in a frame of elegiac "
            "digressions about lineage, the doomed hall, and the men who came "
            "before. The structure makes the poem's argument: heroism is whole "
            "only when set beside its end, and what the hero builds is held "
            "against what time takes."
        ),
        "thematic_lines": [
            "Fame (lof) and what outlives the hero",
            "Wyrd (fate) and the doomed hall: every gold-given hall the poem names is already burning in another digression",
            "The Christian-pagan interweave: a Christian narrator looking back at a pre-Christian world he loves",
        ],
        "comparative_threads": [
            "lit-work-inh-004 (Tolkien's The Lord of the Rings): the lineage cites Beowulf directly; Tolkien's own essay 'The Monsters and the Critics' on this very poem",
            "lit-work-005 (Saga of the Volsungs): the cousin dragon-slaying and the cousin doomed-hoard in the Northern lineage",
        ],
        "seminar_questions": [
            "What does the poem do by setting every great hall it names already in a digression about that hall's coming end?",
            "Is Beowulf admired wholly by the poem, or does the poem hold something back?",
            "Why three combats, and why an old hero at the dragon?",
        ],
        "writing_invitations": [
            "The analytical paragraph on a kenning of your own choosing, naming what it lets the reader see",
            "The essay on whether the poem endorses heroism in age the way it endorses heroism in youth",
            "At advanced, the comparative essay on the dragon set beside the dragon of the Volsungs or of Tolkien's Smaug",
        ],
        "context": (
            "The single Old English heroic epic to survive whole (in the Nowell "
            "Codex, c. 1000 CE), oral tradition older still; the founding work of "
            "English-language epic and the central node of the Northern epic "
            "inheritance; supplied as fact."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "The founding English-language epic; the heroic-elegiac mode examined rhetorically and ethically."
                ),
                "memory_work": {
                    "recitations": ["Recitation of the opening (Hwaet! ...) in a worthy translation"],
                },
                "recitation_routine": (
                    "Seminar opens from the recited opening; the discussion takes "
                    "its first question from what the poem chooses to remember at "
                    "its first breath."
                ),
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy translation of Beowulf, read aloud as a living book (Heaney's verse translation; Tolkien's own prose translation when available)",
                ],
                "short_lesson_flow": (
                    "A living book read aloud and narrated; the three combats "
                    "followed across the hero's life, the kennings noticed, "
                    "deepening to analysis of the elegiac frame as the bands move up."
                ),
                "narration_prompt": (
                    "Tell back the part we read today, and tell me which kenning stayed with you, or which hall we were told would burn."
                ),
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy translation of Beowulf on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in monsters, heroes, dragons, and the long lineage Tolkien drew from leads, no imposed apparatus",
                ],
                "parent_role": (
                    "Read aloud and discuss where the student's interest leads; "
                    "bring Tolkien (and the Volsungs) into the conversation when "
                    "the student finds the lineage."
                ),
                "observation_documentation": (
                    "Over time, notice whether the student returns to the poem and "
                    "traces its lineage forward into Tolkien or sideways into the "
                    "Norse material. This noticing replaces any test."
                ),
            },
            "traditional": {
                "introduction": "Structured study of the three-combat structure, the kenning, and the elegiac frame where chosen.",
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
