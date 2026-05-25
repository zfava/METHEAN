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
    "lit-craft-050": {
        "node_type": "craft",
        "strand": "drama",
        "band": "emerging",
        "prerequisites": ["close reading: emerging"],
        "objective": (
            "Hear that a play is the transcript of an absent performance, not a story "
            "told by a narrator; follow who is speaking on the page; read stage "
            "directions as instructions, not narration; read a short scene aloud with "
            "another reader, taking different parts."
        ),
        "core_understanding": (
            "A play looks like a story but is not one. There is no narrator. The page "
            "is what the actors are given to perform; the work itself is the "
            "performance. Reading a play silently is reading half of it. At this band "
            "the child meets this difference: the lines belong to characters, the "
            "italic bits belong to the staging, and the play comes alive when read "
            "aloud with another person taking another part."
        ),
        "analytical_moves": [
            "Identify each character's lines by the name preceding them",
            "Read stage directions as instructions for what happens, not as part of any character's speech",
            "Take a part and read aloud with another reader taking another part",
            "Notice that no one is telling the story: only the characters speak",
            "Mark where a stage direction tells you something important happens (an entrance, an exit, a gesture)",
        ],
        "seminar_questions": [
            "Who is speaking now? How do you know?",
            "What did the stage direction just tell you that no character said?",
            "If we are reading this aloud, what is missing that would be there on a stage?",
        ],
        "writing_invitations": [
            "Copy out a short exchange between two characters, marking the stage directions",
            (
                "Write a one-line stage direction for something that happens between "
                "two lines (a glance, a touch, a turn away) and read the scene with "
                "your direction in place"
            ),
        ],
        "exemplar_texts": [
            "A children's adaptation of Shakespeare presented as dialogue (a scene from Lamb's Tales acted as a script)",
            "A short scene from an Aesop fable adapted for performance",
            "A read-aloud version of a folk tale written as dialogue between two voices",
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "Drama is among the oldest forms of teaching by performance. Before "
                    "the child meets the play as a text to be studied, they meet it as "
                    "a script to be spoken aloud. The classical tradition holds that "
                    "the voice of the play lives in the voice of the speaker; the page "
                    "is a record, not the thing itself."
                ),
                "memory_work": {
                    "recitations": [
                        "A short exchange of two or three lines recited from a chosen scene, with the child taking one part and the mentor taking the other",
                    ],
                },
                "copywork": [
                    "A short stage direction copied neatly, with the two surrounding lines of dialogue copied above and below it",
                ],
                "recitation_routine": (
                    "Each session opens with the recited exchange from the previous; "
                    "the new lesson begins with naming the next two characters who "
                    "will share the page."
                ),
                "read_aloud_suggestions": [
                    "A short scene from a children's adaptation of Shakespeare (Lamb's Tales)",
                    "A short folk tale adapted as dialogue between two voices",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A worthy children's adaptation of Shakespeare",
                    "A child-suitable book of short plays drawn from classic stories",
                ],
                "short_lesson_flow": (
                    "Read a short scene aloud as a family or with the child taking one "
                    "part. The child narrates back what happened, naming each "
                    "character. Then ask: did anyone tell the story to us, or did the "
                    "people in the play tell it themselves?"
                ),
                "narration_prompt": (
                    "Tell back what we just read, and tell me which character said "
                    "what, and what the stage directions said happened."
                ),
                "real_world_objects": [
                    "The book held by the reader, with stage directions easy to see",
                    "Two voices: the child's and a fellow reader's",
                ],
                "nature_connection": (
                    "A play is to ordinary storytelling what a bird seen alive is to a "
                    "picture in a book: the thing has only been there in front of us "
                    "when we have heard the voices."
                ),
                "habit_focus": (
                    "The habit of hearing different voices in a written page, and the "
                    "habit of taking a part rather than reading silently."
                ),
            },
            "traditional": {
                "introduction": (
                    "Explicit instruction in the parts of a printed play: the "
                    "character names, the lines that follow them, and the stage "
                    "directions. Practice in reading aloud with another reader, "
                    "taking parts."
                ),
                "gradual_release": {
                    "i_do": (
                        "Teacher reads a short scene aloud, naming each character "
                        "before reading their lines and pausing to read stage "
                        "directions in a different voice or to act them out."
                    ),
                    "we_do": "Teacher and child read the scene together, alternating characters.",
                    "you_do": (
                        "Child takes a part with another reader (a sibling or peer) "
                        "and reads the scene through; mentor watches and confirms the "
                        "stage directions were not skipped."
                    ),
                },
                "independent_practice": [
                    "A short scene read aloud with another reader, with the child noting one stage direction they had to act",
                ],
            },
            "unschooling": {
                "invitations": [
                    "Keep a shelf of children's plays and worthy adaptations of Shakespeare",
                    "Read aloud as a household at meals or evenings; let the child join in when they are ready",
                ],
                "real_world_contexts": [
                    "A puppet show or backyard production the child stages themselves",
                    "A family read-aloud where parts are passed around as people want them",
                ],
                "conversation_starters": [
                    "Who said what just now?",
                    "What did the page tell us that nobody said out loud?",
                    "Want to take one of the parts?",
                ],
                "resource_bank": [
                    "A shelf of children's plays and adapted classics",
                    "Voices willing to read parts when invited",
                ],
                "parent_role": (
                    "Read aloud yourself with the lines in your voice, take a part, "
                    "and welcome the child's part when they ask for one. The child "
                    "meets drama by joining in, not by being assigned."
                ),
                "observation_documentation": (
                    "Over time, notice whether the child begins to take parts on "
                    "their own, asks to read aloud, and acts out stage directions "
                    "when the page describes them. This noticing replaces any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": (
                "Montessori at this band does not carry a distinct method for reading "
                "dramatic literature; the elementary prepared environment centers on "
                "the great-lesson narratives and the grammar materials. Children's "
                "dramatic play in the Montessori environment is welcomed but is not "
                "framed as the reading of a written play."
            ),
        },
    },
    "lit-craft-051": {
        "node_type": "craft",
        "strand": "drama",
        "band": "developing",
        "prerequisites": ["drama: emerging", "close reading: developing", "character: emerging"],
        "objective": (
            "Read a scene with multiple characters and track who is on stage at every "
            "moment; recognize the soliloquy as a character speaking when no one else "
            "is on stage and the aside as a brief direct address to the audience while "
            "others are on stage but not meant to hear; begin to feel dramatic irony "
            "when the audience knows what a character does not."
        ),
        "core_understanding": (
            "At this band the reader meets the conventions that make drama what it "
            "is. The soliloquy is a character thinking out loud, alone, in a way they "
            "would never speak to another character. The aside is a brief direct "
            "address to the audience while others are on stage but not hearing it. "
            "Both are the playwright's way of giving the audience access to what no "
            "narrator can give them, because there is no narrator. Dramatic irony "
            "arises when the audience knows what a character does not: this is one "
            "of the deepest moves the form makes, and at this band it is recognized "
            "when it appears in a scene the reader has met."
        ),
        "analytical_moves": [
            "Track who is on stage at every moment of a scene; entrances and exits matter",
            (
                "Identify a soliloquy by its character-alone-on-stage convention and "
                "explain what the character reveals that they would never say to "
                "another character"
            ),
            ("Identify an aside and explain what the audience hears that the other characters on stage do not"),
            "Name a moment of dramatic irony in a scene already read: where the audience knows what a character does not, and how we know it",
            (
                "Read a stage direction as a meaningful choice the playwright made "
                "(an entrance, an exit, a refusal to look at someone, a touch withheld)"
            ),
        ],
        "seminar_questions": [
            "Who is on stage when this character is alone, and what does the character say only because they are alone?",
            "Where in this scene does the audience know something a character does not? How do we know it?",
            "What did the stage direction just tell us, and what does it change about the scene?",
        ],
        "writing_invitations": [
            (
                "Write a short paragraph about a soliloquy you read, naming what the "
                "character reveals that they would never tell another character on stage"
            ),
            (
                "Write the paragraph that explains where in a scene the audience "
                "knows what a character does not, and what the scene gains by the gap"
            ),
        ],
        "exemplar_texts": [
            (
                "A short Shakespearean soliloquy (Hamlet's first soliloquy 'O that "
                "this too too solid flesh'; Macbeth's 'Is this a dagger which I see "
                "before me')"
            ),
            (
                "A scene of dramatic irony (the cross-gartering scene with Malvolio "
                "in Twelfth Night; the tomb scene in Romeo and Juliet where the "
                "audience knows Juliet is not dead)"
            ),
            (
                "A short play or scene accessible to a developing reader (a Greek "
                "myth dramatized for young readers; a scene from Wilder's Our Town)"
            ),
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "After the play is met as a script to be spoken, the reader meets "
                    "the conventions that make drama distinct. Soliloquy and aside, "
                    "recognized in the classical curriculum since the grammar school "
                    "of the Renaissance, are not narration in disguise; they are the "
                    "playwright's solution to what narration cannot do in a form that "
                    "has no narrator."
                ),
                "memory_work": {
                    "recitations": [
                        "A soliloquy of eight to sixteen lines recited from memory at the seminar's opening",
                    ],
                },
                "copywork": [
                    "The recited soliloquy copied into the kept commonplace book",
                ],
                "recitation_routine": (
                    "Each seminar opens from a recited soliloquy or speech; the "
                    "first question is taken from what the speaker would never say "
                    "to another character on stage."
                ),
                "read_aloud_suggestions": [
                    "A scene from Shakespeare read aloud in parts before discussion",
                    "A short Greek tragedy (or a portion of one) in a worthy modern translation read aloud",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A worthy edition of a Shakespearean play (Folger; Arden student editions) read at home aloud",
                    "A volume of dramatic readings drawn from Greek myth",
                ],
                "short_lesson_flow": (
                    "Read a short scene aloud, taking parts where possible. The "
                    "child narrates the scene, naming who was on stage and what each "
                    "character said. When a soliloquy appears, ask: nobody else is "
                    "on stage here; what is the character telling us that they would "
                    "never tell another character?"
                ),
                "narration_prompt": (
                    "Tell back the scene, and tell me who was on stage when, and "
                    "what the character said when no one was listening except us."
                ),
                "real_world_objects": [
                    "A worthy edition of the play in the reader's hands, with character names easy to find",
                ],
                "nature_connection": (
                    "A soliloquy is to a play what a creature standing still in a "
                    "clearing is to the forest: the only moment we see them whole, "
                    "because there is no one else they are aware of."
                ),
                "habit_focus": (
                    "The habit of asking who is on stage, and the habit of hearing a "
                    "soliloquy as the playwright's way of letting us in."
                ),
            },
            "traditional": {
                "introduction": (
                    "Explicit instruction in the conventions of soliloquy, aside, "
                    "and dramatic irony, with practice in identifying each in a "
                    "short scene and writing the paragraph that explains it."
                ),
                "gradual_release": {
                    "i_do": (
                        "Teacher reads a soliloquy aloud and names it: this "
                        "character is alone on stage; this is what they would not "
                        "say to anyone else. Teacher then reads an aside and "
                        "explains the convention. Teacher reads a moment of dramatic "
                        "irony and explains what the audience knows that the "
                        "character does not."
                    ),
                    "we_do": (
                        "Class works through a scene together, identifying "
                        "soliloquy, aside, or dramatic irony as each appears, and "
                        "naming what each reveals or conceals."
                    ),
                    "you_do": (
                        "Student identifies independently a soliloquy, an aside, or "
                        "a moment of dramatic irony in a new scene and writes a "
                        "short paragraph explaining it."
                    ),
                },
                "independent_practice": [
                    "A short notebook entry on a soliloquy, an aside, or a moment of dramatic irony from the play under study",
                ],
            },
            "unschooling": {
                "invitations": [
                    "Keep a shelf of worthy editions of Shakespeare and accessible Greek tragedy",
                ],
                "real_world_contexts": [
                    "A family viewing of a live or filmed performance of the play the child is reading",
                    "A long evening discussing why a character said what they said when they were alone",
                    "A read-aloud of a soliloquy because the reader wanted to hear it out loud",
                ],
                "conversation_starters": [
                    "Why is he alone on the stage right now? What does that let him say?",
                    "Did anyone else just hear that? Was that for us?",
                    "We know more than she does right now. How did we get to know it?",
                ],
                "resource_bank": [
                    "A shelf of plays; a streaming service or library DVDs of worthy performances of those plays",
                ],
                "parent_role": (
                    "Be a fellow reader who has their own beloved soliloquies and "
                    "welcomes the child's. Read a scene together aloud; watch a "
                    "performance afterward. Drama meets the unschooler in the "
                    "cadence of speech."
                ),
                "observation_documentation": (
                    "Over time, notice whether the child begins to ask 'why is he "
                    "alone' or 'are we the only ones who heard that' on their own. "
                    "This noticing replaces any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": (
                "Montessori at this band does not carry a distinct method for the "
                "analytical reading of dramatic convention. The Montessori "
                "adolescent program has elements of drama in the prepared "
                "environment but is not the same practice as the close reading of "
                "staged conventions in a written play; the practice here is drawn "
                "from the seminar tradition and the long Charlotte Mason habit of "
                "reading aloud."
            ),
        },
    },
    "lit-craft-052": {
        "node_type": "craft",
        "strand": "drama",
        "band": "proficient",
        "prerequisites": ["drama: developing", "close reading: proficient", "narrative craft: proficient"],
        "objective": (
            "Read dramatic structure as the playwright's argument (the turn or "
            "peripeteia, the recognition or anagnorisis); read the chorus in Greek "
            "tragedy as a function (commentator, mediator, audience-surrogate); "
            "argue what a staged choice (a silence, an entrance, a prop, a refusal) "
            "does to meaning; defend a small original reading of a play scene-by-scene "
            "from the lines themselves."
        ),
        "core_understanding": (
            "A play does not have a narrator, so the playwright's argument is "
            "carried entirely by the structure (who is on stage when, what happens "
            "between scenes, when the turn comes, when recognition arrives), by the "
            "staged choices (a soliloquy here and not there; a silence at the moment "
            "one would expect speech; a prop set down deliberately), and by the "
            "system of voices, none of which is authoritative. The proficient reader "
            "reads the play whole and articulates its argument. They meet the Greek "
            "chorus as a structural function rather than as background noise: a "
            "commentator on the action, a mediator between audience and stage, a "
            "voice of the community whose own commitments the play tests. They also "
            "meet Aristotle's vocabulary for dramatic structure (peripeteia, the "
            "turn; anagnorisis, the recognition) and use it as the carpenter uses a "
            "name for a joint: not to label the work but to see it."
        ),
        "analytical_moves": [
            "Identify the turn (peripeteia) in a play and articulate what changes for whom",
            (
                "Identify the recognition (anagnorisis) and articulate what the "
                "character now knows that they did not before, and what the audience "
                "now knows about them"
            ),
            (
                "Read the chorus as a function: name what work the chorus is doing in "
                "a scene (commenting, mediating, voicing the community's stake)"
            ),
            (
                "Argue what a staged choice (a silence, an entrance, a prop, a refusal "
                "to speak) does to the meaning of a scene"
            ),
            (
                "Defend a small original reading of a play from scene-and-line "
                "evidence, returning to the text for every claim"
            ),
        ],
        "seminar_questions": [
            "Where does this play turn, and what does the turn cost?",
            "Where is the recognition, and what does the character know now that we already knew?",
            "What is the chorus doing in this scene that no single character could do?",
            "What would change about this play if a soliloquy here became a dialogue, or if a silence became a speech?",
        ],
        "writing_invitations": [
            "Write an analytical paragraph identifying the turn in a chosen play and arguing what the turn does to the work's meaning",
            (
                "Choose one staged moment (a silence, an entrance, a prop, a "
                "refusal) and write the paragraph that argues what the staging does "
                "that dialogue alone could not"
            ),
        ],
        "exemplar_texts": [
            "A Greek tragedy with a clear chorus role (Sophocles' Antigone; Aeschylus' Agamemnon)",
            "A Shakespeare play whose structure rewards proficient attention (Macbeth's tightness; the mirror plotting of Twelfth Night)",
            "A modern play where staging is meaning (Beckett's Waiting for Godot; Pinter's silences)",
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "Aristotle gave us the vocabulary the proficient reader needs: "
                    "peripeteia, the turn; anagnorisis, the recognition. The "
                    "classical seminar applies them as the carpenter applies a name "
                    "for a joint: not to label the work but to see it. The Greek "
                    "chorus, properly read, is not background but a function the "
                    "play needs."
                ),
                "memory_work": {
                    "recitations": [
                        "A choral passage of a Greek tragedy recited at the seminar's opening, or a soliloquy from Shakespeare central to the play's turn",
                    ],
                },
                "copywork": [
                    "The recited passage copied into the commonplace book, with the structural function (turn / recognition / chorus) noted in the margin",
                ],
                "recitation_routine": (
                    "Each seminar opens from the recited passage; the first question "
                    "is taken from where in the play's structure that passage sits."
                ),
                "read_aloud_suggestions": [
                    "A full Greek tragedy read aloud whole in a worthy translation",
                    "A Shakespeare play of clear structure (Macbeth, Othello) read whole across a few sessions",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 40,
                "living_book_suggestions": [
                    "A whole Greek tragedy in a worthy translation, read across a term",
                    "A whole Shakespeare play, read aloud with parts taken, paired with a live or filmed performance",
                ],
                "short_lesson_flow": (
                    "The proficient student reads the play whole at a sustained "
                    "pace, narrating each scene. The reader marks moments of "
                    "soliloquy, the turn, and the recognition as they meet them. At "
                    "a scene's end one such moment is taken up: copied into the "
                    "commonplace book, discussed, and tested against the rest of "
                    "the play. The chorus passages are returned to and asked: what "
                    "is the chorus doing here?"
                ),
                "narration_prompt": (
                    "Tell back the scene, and tell me which moment was where the "
                    "play turned, and which moment was where someone recognized something."
                ),
                "real_world_objects": [
                    "The whole play in the reader's hands, marked at structural moments",
                    "A performance to attend or watch alongside the reading",
                ],
                "nature_connection": (
                    "A play's structure is to its meaning what a watershed is to a "
                    "river: the shape the water of voice and action moves along."
                ),
                "habit_focus": (
                    "The habit of asking where the play turns and where recognition "
                    "comes, and the habit of returning to the line for the staged "
                    "choice that makes the meaning."
                ),
            },
            "traditional": {
                "introduction": (
                    "Explicit instruction in dramatic structure (peripeteia and "
                    "anagnorisis), in the function of the chorus, in reading staged "
                    "choices as meaning, and in writing the short analytical "
                    "paragraph that defends a reading from scene-and-line evidence."
                ),
                "gradual_release": {
                    "i_do": (
                        "Teacher works a scene on the board: names the turn, names "
                        "the recognition, names what the chorus is doing in the "
                        "passage, and drafts a short paragraph defending a reading "
                        "of the staged choice, quoting the lines."
                    ),
                    "we_do": (
                        "Class works through a chosen scene together, identifying "
                        "the turn or the recognition, naming the chorus function, "
                        "and drafting together a paragraph defending a small original reading."
                    ),
                    "you_do": (
                        "Student writes an independent analytical paragraph on the "
                        "turn, the recognition, or a chosen staged choice in the "
                        "play under study, with quoted evidence."
                    ),
                },
                "independent_practice": [
                    "The analytical paragraph on the turn, recognition, chorus function, or a staged choice from the play under study",
                ],
            },
            "unschooling": {
                "invitations": [
                    "Keep the long shelf of Greek tragedy in worthy translation and Shakespeare in worthy editions, available, never assigned",
                ],
                "real_world_contexts": [
                    "A live or filmed performance of the play the reader has been living with",
                    "A long conversation about what the chorus is doing in a tragedy the reader keeps returning to",
                    "A piece of writing the reader produced because a moment in the play turned for them and they wanted to say so",
                ],
                "conversation_starters": [
                    "Where does this play turn? Read me the lines.",
                    "What is the chorus telling us that the characters cannot?",
                    "What changes for the character in the moment they recognize? What changes for us?",
                ],
                "resource_bank": [
                    "A shelf of plays; a streaming service or library DVDs of worthy performances",
                    "A reader-companion willing to argue a chosen turn or recognition as a fellow reader",
                ],
                "parent_role": (
                    "Be a fellow reader who has lived with the same plays in their "
                    "own returning. Watch a performance together; argue afterward. "
                    "The proficient reading of a play often comes from the second "
                    "or third encounter, not the first."
                ),
                "observation_documentation": (
                    "Over time, notice whether the reader begins to identify turn "
                    "and recognition on their own, to ask what the chorus is doing "
                    "without prompting, and to defend a small reading from the "
                    "lines. This noticing replaces any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": (
                "Montessori's literature pedagogy at the elementary and "
                "early-secondary level does not carry a distinct method for the "
                "structural analysis of drama or for reading the chorus as a "
                "function; the practice here is drawn from the seminar tradition "
                "and the long Charlotte Mason habit of reading aloud across a term."
            ),
        },
    },
    "lit-craft-053": {
        "node_type": "craft",
        "strand": "drama",
        "band": "advanced",
        "prerequisites": ["drama: proficient", "close reading: advanced", "theme and meaning: proficient"],
        "objective": (
            "Argue the play's full dramatic argument as the very way the play means "
            "(not its content but the shape it has when staged choices, structural "
            "turns, the system of voices, and chorus function are held together as "
            "one whole); set the play against its inheritance (a revenge tragedy "
            "against the revenge-tragedy tradition; a Greek tragedy against its "
            "predecessors and successors); honor what the play refuses to settle; "
            "write the sustained essay arguing both the play's claim and what the "
            "play refuses."
        ),
        "core_understanding": (
            "At this band the play is no longer separable from how it is staged. "
            "The work's argument is the staged whole: every silence, every entrance, "
            "every choric passage, every soliloquy, every refusal to speak operates "
            "together to make the meaning. A play has no narrator; nothing is "
            "authoritative; the reader holds a system of voices and the staging that "
            "exhibits them. The reader also meets the inheritance: a revenge tragedy "
            "carries everything earlier revenge tragedies have done; a Greek tragedy "
            "is in conversation with the ones before and the ones after; the writer "
            "is doing something to the tradition. The play often refuses to settle: "
            "that refusal is itself an argument. The advanced essay names both what "
            "the play claims and what the play refuses, and holds them together."
        ),
        "analytical_moves": [
            "Argue the play's full dramatic argument as the very way it means rather than as content it delivers",
            (
                "Set the play against its inheritance: name what tradition the play "
                "belongs to and what the writer is doing to it"
            ),
            "Identify and honor what the play refuses to settle, and argue what is gained by leaving it unsettled",
            (
                "Defend a sustained reading scene-by-scene with staged choice, "
                "structural turn, and choric function as evidence"
            ),
            (
                "Hear another reader's account of the play's argument and locate "
                "where in the text and in the tradition that account draws its evidence"
            ),
        ],
        "seminar_questions": [
            "What is this play's whole argument, and how do its staged choices operate together to make it?",
            "What tradition of drama is this play working with, and where is the playwright doing something the tradition had not done?",
            "What does this play refuse to settle, and what would be lost if it settled it?",
            "Where would another reader's reading of this play diverge from yours, and what staged moment would they cite?",
        ],
        "writing_invitations": [
            (
                "Write a sustained essay arguing a chosen play's whole dramatic "
                "argument as the very way the play means, holding three or four "
                "scenes in productive tension and naming the play's inheritance"
            ),
            "Write the paragraph arguing what a chosen play refuses to settle and what is gained by the refusal",
        ],
        "exemplar_texts": [
            (
                "A Shakespeare tragedy held whole and against its inheritance (Hamlet "
                "against the revenge-tragedy tradition; King Lear against the "
                "medieval Lear story; Othello against Cinthio)"
            ),
            (
                "A Greek tragedy in dialogue with its predecessors and successors "
                "(Sophocles' Oedipus against earlier myth; Antigone in conversation "
                "with later treatments by Anouilh and Brecht)"
            ),
            (
                "A modern play that intervenes in an inheritance (Beckett's Endgame "
                "against the well-made play; Stoppard's Rosencrantz and Guildenstern "
                "Are Dead against Hamlet)"
            ),
        ],
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "Drama meets the long seminar and the genealogy of forms. The "
                    "reader brings the play's whole argument as a hypothesis; the "
                    "seminar tests it, and the inheritance of the play's form is "
                    "brought into the room. Aristotle's vocabulary, the chorus "
                    "tradition, the revenge tradition, the inheritance the "
                    "playwright is doing something to: all of these converge."
                ),
                "memory_work": {
                    "recitations": [
                        "A passage central to the play's whole argument, recited at the seminar's opening",
                        "A passage from another play in the inheritance the work intervenes in",
                    ],
                },
                "copywork": [
                    "The recited passage copied into the kept commonplace book, with the inheritance the play intervenes in noted in the margin",
                ],
                "recitation_routine": (
                    "Each seminar opens from two recited passages: one from the play "
                    "under study, one from elsewhere in the inheritance; the first "
                    "question is taken from what each lets the other see, and the "
                    "discussion returns to the staged text for every claim."
                ),
                "read_aloud_suggestions": [
                    "A scene at the heart of the play's argument read aloud at the seminar's opening",
                    "A scene from another play in the inheritance read aloud beside it",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 50,
                "living_book_suggestions": [
                    "A whole Shakespeare play or Greek tragedy held across a term, read aloud and paired with a performance",
                    "A second play earlier in the inheritance, read alongside or after to bring the inheritance into the commonplace work",
                ],
                "short_lesson_flow": (
                    "The advanced student reads the play whole at a sustained pace, "
                    "narrating each scene honestly. Staged choices and structural "
                    "turns are slipped or marked. At a scene's end one passage is "
                    "taken up: copied into the commonplace book, discussed, and "
                    "tested against the rest of the play and against passages from "
                    "other plays in the inheritance. The essay forms across the long "
                    "span of the whole play."
                ),
                "narration_prompt": (
                    "Tell back what you read, and tell me what the whole play is "
                    "doing, and which scene you would set down as the place we most "
                    "clearly see the argument, and which scene from another play in "
                    "the inheritance you would set beside it."
                ),
                "real_world_objects": [
                    "The whole play, marked at the scenes decisive for the dramatic argument",
                    "A commonplace book gathering dramatic passages across many plays and across the inheritance",
                ],
                "nature_connection": (
                    "A play's whole argument is to its scenes what a season is to "
                    "its days: not a thing one sees in any one but the long pattern "
                    "that emerges from many held together."
                ),
                "habit_focus": (
                    "The habit of holding a whole play's argument as a hypothesis to "
                    "be tested against the staged text, and the habit of bringing "
                    "the inheritance of the form into the reading."
                ),
            },
            "traditional": {
                "introduction": (
                    "Explicit instruction in arguing a play's full dramatic "
                    "argument, in setting the play against its inheritance, in "
                    "honoring what the play refuses to settle, and in writing the "
                    "sustained essay that holds the play's claim and what the play "
                    "refuses together."
                ),
                "gradual_release": {
                    "i_do": (
                        "Teacher works a chosen play on the board: names the play's "
                        "whole argument as a hypothesis, identifies the inheritance "
                        "the play intervenes in, names what the play refuses to "
                        "settle, and drafts the opening of a sustained essay quoting "
                        "two scenes from the play and one from the inheritance."
                    ),
                    "we_do": (
                        "Class gathers the decisive scenes of a chosen play, weighs "
                        "the play against its inheritance, names what the play "
                        "refuses to settle, and drafts together the body of the "
                        "sustained essay."
                    ),
                    "you_do": (
                        "Student writes an independent sustained essay on a chosen "
                        "play, arguing its whole dramatic argument, naming the "
                        "inheritance, honoring what the play refuses to settle, and "
                        "holding three or four scenes in productive tension, and "
                        "revises after seminar."
                    ),
                },
                "independent_practice": [
                    "The sustained essay on a self-chosen play, arguing its whole dramatic argument and naming the inheritance",
                    "A paragraph naming and defending what the play refuses to settle",
                ],
            },
            "unschooling": {
                "invitations": [
                    "Keep the long shelf of Shakespeare and Greek tragedy and modern drama the reader has returned to over years, available, never assigned",
                ],
                "real_world_contexts": [
                    "A reader who has lived with a single Shakespeare play across years and watched the whole argument surface as the patterns surfaced from many returns and many performances",
                    "A piece of writing the reader produced because the play refused to settle and the reader needed to say so",
                    "A long conversation between two readers who have each lived with the same play in their own returning, each bringing their own scene",
                ],
                "conversation_starters": [
                    "What do you think this whole play is doing now, after all these returns and all these performances?",
                    "Which other play that you have lived with does this one finally speak to?",
                    "What does this play refuse to settle, and what would be lost if it settled it?",
                ],
                "resource_bank": [
                    "A shelf of plays gathered slowly across many years; a library of filmed performances",
                    "A reader-companion of long acquaintance who has also done their long returning and can bring a scene from another play into the room",
                ],
                "parent_role": (
                    "By this band the parent has fully stepped back to fellow "
                    "reader. They are someone who has done their own long returning "
                    "to their own beloved plays, and they name a scene from another "
                    "play in the inheritance when the reader finds the connection. "
                    "The parent does not orchestrate the inheritance; they receive "
                    "what the reader has brought up out of their own returning."
                ),
                "observation_documentation": (
                    "Over time, notice whether the reader returns to a small handful "
                    "of beloved plays across years, whether the whole arguments "
                    "surface in their conversation without prompting, and whether "
                    "they begin to feel the inheritance because their own returning "
                    "led them into it. The pattern surfacing is the noticing; it "
                    "replaces any test."
                ),
            },
        },
        "philosophy_neutral": {
            "montessori": (
                "Montessori's literature pedagogy at the elementary and "
                "early-secondary level does not carry a distinct method for arguing "
                "a play's full dramatic argument or for placing the play in the "
                "inheritance it intervenes in; the practice here is drawn from the "
                "long seminar tradition and the matured Charlotte Mason habit of "
                "reading aloud and commonplace work across years."
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
    "lit-work-005": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "The Saga of the Volsungs (selection: the Sigurd-Fafnir cycle)",
            "author": "anonymous",
            "date": "c. 13th-century Icelandic compilation of older oral material",
            "genre": "Old Norse saga",
            "form": "prose with embedded verse, in modern English translation",
        },
        "minimum_band": "developing",
        "content_notes": (
            "Combat, the killing of the dragon Fafnir, the doomed-treasure motif; "
            "the saga's full text continues into a darker ending the selection does "
            "not reach, and a reader who continues will meet treachery, kin-killing, "
            "and the eventual ruin of the line; honest information, not a gate."
        ),
        "craft_focus": [
            "The dragon-slaying tradition: Sigurd kills Fafnir, the parent of all dragon-slayings in the Northern lineage",
            "The doomed treasure (the gold of Andvari, the ring) as a recurring symbol the saga and its inheritors return to",
            "The prose-with-verse mode of saga, where the embedded verse marks the moments that matter most",
            "The hero who acquires through cunning and instruction, not only through force",
            "Fate and prophecy as structural givens, not as plot surprises",
        ],
        "entry": (
            "Developing: follow Sigurd-and-Fafnir as a hero-and-dragon story, "
            "narrate the killing and what comes with the treasure, notice the "
            "embedded verse where the saga slows. Proficient: name the "
            "dragon-slaying as a figurative system the saga and its inheritors "
            "return to, hold the doomed gold beside the heroic action, read the "
            "prose-with-verse mode as a craft choice, ask what the saga counts as "
            "victory. Advanced: argue what the saga does to the dragon-slaying "
            "inheritance, set Sigurd's gold beside Tolkien's ring and beside "
            "Beowulf's dragon-hoard, read prophecy as the saga's structural "
            "argument rather than as plot mechanism. Mastery: original argument "
            "about the doomed-treasure inheritance from the Northern lineage "
            "forward into Tolkien."
        ),
        "close_reading_passages": [
            "Regin's instruction and the forging of the sword Gram: how does the saga prepare the killing?",
            "The killing of Fafnir and the speech of the dying dragon: what does Fafnir tell Sigurd, and how does the saga make us hear it?",
            "Sigurd takes the treasure: what does the saga let us know that Sigurd does not yet know?",
        ],
        "structural_analysis": (
            "Prophecy and fate are given at the outset; the action moves toward "
            "them rather than away from them, and the saga's craft is in what it "
            "slows and what it lets the embedded verse interrupt. The "
            "dragon-slaying sits at the center, and the doomed treasure carries "
            "the saga's argument from before Sigurd's birth to after his death."
        ),
        "thematic_lines": [
            "Heroism as inseparable from cunning, instruction, and inheritance, not as solitary force",
            "The doomed treasure: gold the saga marks as already cursed before it is taken",
            "Fate and prophecy as the saga's structural givens, asking the reader to watch how rather than whether",
        ],
        "comparative_threads": [
            "lit-work-004 (Beowulf): the cousin dragon-slaying and the cousin doomed-hoard in the same Northern lineage",
            "lit-work-inh-004 (Tolkien's The Lord of the Rings): the doomed ring and Smaug-the-dragon come directly out of this material; Tolkien's own scholarly work on the Volsungs",
        ],
        "seminar_questions": [
            "Why does the saga give the prophecy first, and what does that do to how we read the killing?",
            "What does the saga gain by letting the dying dragon speak?",
            "Is Sigurd the same kind of hero as Beowulf? Where does the saga insist they differ?",
        ],
        "writing_invitations": [
            "The analytical paragraph on a moment where embedded verse interrupts the prose, naming what the verse does that the prose could not",
            "The essay on the doomed treasure as a figurative system set beside Beowulf's dragon-hoard",
            "At advanced, the comparative essay on the dragon-slaying inheritance from the Volsungs through Beowulf to Tolkien's Smaug",
        ],
        "context": (
            "The Volsunga saga, an Icelandic prose compilation made c. 1200-1270 "
            "from older oral material that also produced the Poetic Edda; the "
            "central source for the Northern dragon-slaying tradition and the most "
            "cited direct ancestor of Tolkien's invented mythology; supplied as fact."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "The foundational Northern saga of dragon-slaying and doomed "
                    "treasure; Sigurd examined rhetorically and ethically against "
                    "the heroic tradition."
                ),
                "memory_work": {
                    "recitations": [
                        "Recitation of a moment of embedded verse from the Sigurd-Fafnir cycle in a worthy translation"
                    ],
                },
                "recitation_routine": (
                    "Seminar opens from the recited verse; the discussion takes "
                    "its first question from why the saga chose to slow at that moment."
                ),
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy translation of the Saga of the Volsungs, read aloud as a living book (Jesse Byock's Penguin translation; William Morris's older verse-and-prose version)",
                ],
                "short_lesson_flow": (
                    "A living book read aloud and narrated; the Sigurd-Fafnir "
                    "cycle followed and told back, the kennings and embedded "
                    "verses noticed, deepening to analysis of the doomed treasure "
                    "as the bands move up."
                ),
                "narration_prompt": (
                    "Tell back the part we read today, and tell me what you noticed about Sigurd or the gold this time."
                ),
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy translation of the Saga of the Volsungs on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in dragons, doomed treasure, the Northern world, or the sources behind Tolkien leads, no imposed apparatus",
                ],
                "parent_role": (
                    "Read aloud and discuss where the student's interest leads; "
                    "bring Beowulf and Tolkien into the conversation when the "
                    "student finds the lineage on their own."
                ),
                "observation_documentation": (
                    "Over time, notice whether the student returns to the saga "
                    "and traces the dragon-slaying or the doomed-treasure forward "
                    "into Beowulf or Tolkien. This noticing replaces any test."
                ),
            },
            "traditional": {
                "introduction": "Structured study of the saga form and the dragon-slaying tradition where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-006": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Oedipus Rex (Oedipus the King)",
            "author": "Sophocles",
            "date": "c. 429 BCE",
            "genre": "Greek tragedy",
            "form": "verse tragedy in five episodes with choral odes",
        },
        "minimum_band": "proficient",
        "content_notes": (
            "Parricide, incest (offstage; the play uncovers what has already happened "
            "long before), suicide, self-blinding (offstage but graphically reported); "
            "the play's ethical and emotional weight is in the recognition, not in any "
            "depicted violence. Honest information, not a gate."
        ),
        "craft_focus": [
            "Dramatic structure: the in-medias-res opening and the unrelenting progress of recognition",
            "Anagnorisis (recognition) and peripeteia (turn) as the structural backbone (lit-craft-052)",
            "The chorus of Theban elders as commentator, mediator, and voice of the polis (lit-craft-052)",
            "The figure of the king who is also the answer to the riddle (lit-craft-013)",
            "Dramatic irony: the audience knows from the first scene what Oedipus discovers at the last (lit-craft-051)",
        ],
        "entry": (
            "Proficient: meet the play whole, name peripeteia and anagnorisis where "
            "they fall, read the chorus as function, feel the dramatic irony as the "
            "audience holds what Oedipus does not. Advanced: argue what the play "
            "refuses to settle (is Oedipus chosen, fated, or undone by his own "
            "thoroughness; does the play endorse the knowing or mourn it); set the "
            "play against the inheritance of the Theban material and against the "
            "later Oedipus at Colonus. Mastery: original argument about how the play "
            "shapes the tragic form for everything after."
        ),
        "close_reading_passages": [
            "The opening scene of the suppliants and the priest's appeal: how does the play introduce a city already in plague, and what does Oedipus claim to be?",
            "The exchange with Tiresias: what does Tiresias know, what does he refuse to say plainly, and what does Oedipus hear that he will not hear?",
            "The messenger's report and the recognition: how does the play give the recognition that has been there all along, and what does the chorus say at the moment of seeing?",
        ],
        "structural_analysis": (
            "The play begins after the truth is in place; the action is the bringing "
            "of that truth into the king's knowing. Every episode tightens the "
            "chain; every choral ode holds the city's stake; the recognition arrives "
            "and the king is the one who could not see. The structure is the "
            "argument: tragedy is not what is hidden becoming known but the price "
            "exacted by knowing."
        ),
        "thematic_lines": [
            "Knowing and not-knowing: whether the play counts the seeking of truth as virtue or as the form the doom takes",
            "Fate and choice: the play holds both without resolving which has the more weight; competing readings have been held for two and a half millennia",
            "The king as the city: Oedipus is the answer to the riddle and the city's plague at once; what the play asks the polis to do with that doubling",
        ],
        "comparative_threads": [
            "Antigone (lit-work-007): the same Theban material across the same playwright; what each play does with Creon",
            "The Oresteia (lit-work-008): the parallel question of inherited bloodshed and the founding of public justice; Aeschylus and Sophocles reading the same problem differently",
            "Aristotle's Poetics: Oedipus as the play Aristotle uses to define tragedy; the analysis the play makes possible",
        ],
        "seminar_questions": [
            "Does the play endorse Oedipus's seeking of the truth, mourn it, or hold both at once? Which lines tell you?",
            "What is the chorus doing in this play that no single character could do? Where do they speak for the city, and where do they speak for the audience?",
            "Where is the recognition, exactly? Is it a single moment, or a tightening across many?",
        ],
        "writing_invitations": [
            "The analytical paragraph on the chorus of Theban elders, naming what work the chorus is doing in one chosen ode",
            "The essay on whether the play counts knowing as virtue, with two or three passages held in tension",
            "At advanced, the comparative paragraph setting Oedipus against an inheritance the play is working with (the Theban myth as the earlier tellings have it; what Sophocles does to the inheritance)",
        ],
        "context": (
            "Performed at the City Dionysia in Athens in or around 429 BCE; one of "
            "seven surviving Sophoclean tragedies; the play Aristotle uses in the "
            "Poetics to define peripeteia and anagnorisis; supplied as fact, "
            "interpretation left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": (
                    "The play Aristotle uses to define tragedy; the Greek seminar text on knowing and the price of knowing."
                ),
                "memory_work": {
                    "recitations": ["Recitation of a choral ode in a worthy modern translation"],
                },
                "recitation_routine": (
                    "Seminar opens from the recited ode; the discussion takes its first question from what the chorus saw that the king did not."
                ),
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy translation of Oedipus Rex (Robert Fagles; David Grene) read aloud as a living book, parts taken",
                ],
                "short_lesson_flow": (
                    "A living book read aloud and narrated; the chorus heard aloud "
                    "where possible, deepening to analysis of the recognition as the bands move up."
                ),
                "narration_prompt": (
                    "Tell back the episode we read today, and tell me what the chorus said about it, and what Oedipus did not yet know."
                ),
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy translation of Oedipus Rex on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in fate, knowing, or the Theban material leads; a filmed performance watched together",
                ],
                "parent_role": (
                    "Read aloud and discuss where the student's interest leads; bring the chorus's voice into the room when you can. No imposed apparatus."
                ),
                "observation_documentation": (
                    "Over time, notice whether the student returns to the play and brings the recognition into other reading. This noticing replaces any test."
                ),
            },
            "traditional": {
                "introduction": "Structured study of Greek tragic conventions and the play's structural backbone where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-007": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Antigone",
            "author": "Sophocles",
            "date": "c. 441 BCE",
            "genre": "Greek tragedy",
            "form": "verse tragedy in five episodes with choral odes",
        },
        "minimum_band": "proficient",
        "content_notes": (
            "The hanging of Antigone (offstage; reported), the suicides of Haemon "
            "and Eurydice (offstage; reported), the burial that drives the action "
            "and the ritual prohibition the play places against the city's edict; "
            "honest information, not a gate."
        ),
        "craft_focus": [
            "The collision of binding claims as the play's structural argument: Antigone's against Creon's, neither given up by the play",
            "The chorus of Theban elders as commentator and mediator, never as the play's voice (lit-craft-052)",
            "Antigone and Creon as the work's argument: each the structural function of their position (lit-craft-013, lit-craft-014)",
            "What the play refuses to settle: which law commands when two binding claims contend (lit-craft-023)",
            "The choric odes (especially Ode 1, on what mankind is) as the place where the city looks at itself",
        ],
        "entry": (
            "Proficient: meet the play whole, name peripeteia and anagnorisis where "
            "they fall on Creon, read the chorus as function, hear Antigone's and "
            "Creon's claims as binding without giving up either. Advanced: argue "
            "what the play refuses to settle (which law commands; what is gained by "
            "leaving the question unresolved); set the play against later "
            "treatments (Anouilh, Brecht) and against the Theban material more "
            "broadly. Mastery: original argument about the play's place in the "
            "tradition of the contending claim."
        ),
        "close_reading_passages": [
            "The opening exchange between Antigone and Ismene: how does the play frame the choice, and what does Ismene's refusal let the play do?",
            "The first choral ode (on what mankind is and on the city's law): how does the chorus name the human, and what is the chorus quietly asking the audience to hold?",
            "The exchange between Creon and Haemon: how does the play hear the son's argument, and where does Creon refuse to hear?",
        ],
        "structural_analysis": (
            "Two binding claims at the play's outset, neither given up: a sister's "
            "ritual duty to bury her brother, a city's edict that the brother who "
            "attacked the city not be buried. The play unrolls each claim through "
            "its consequences and refuses to declare which commands. The structure "
            "is the argument: tragedy is not the punishment of the wrong but the "
            "cost of holding two rights at once."
        ),
        "thematic_lines": [
            "Divine law and civic law: which commands; competing readings the play sustains",
            "Family and the polis: where each ends and where each refuses to give way",
            "Antigone's silence and Creon's late knowing: what each character has at the end that they did not at the beginning",
        ],
        "comparative_threads": [
            "Oedipus Rex (lit-work-006): the same Theban material across the same playwright; what each play does with Creon",
            "The Oresteia (lit-work-008): the parallel founding question of public justice and the contending claim",
            "Modern responses (Anouilh's Antigone of 1944; Brecht's adaptation): how the play has been read against later moments of contending claim",
        ],
        "seminar_questions": [
            "Which law does the play say commands, divine or civic? Where does the play refuse to say?",
            "What is the chorus doing in the ode on mankind? Is the chorus on a side?",
            "Is Antigone admired wholly, mourned, or both? Where does the play hold something back?",
        ],
        "writing_invitations": [
            "The analytical paragraph on the first choral ode, naming what the chorus lets the audience hear that no character can say",
            "The essay on what the play refuses to settle between Antigone's claim and Creon's",
            "At advanced, the comparative paragraph setting Sophocles's Antigone against a later treatment of the same material",
        ],
        "context": (
            "Performed at the City Dionysia in Athens c. 441 BCE; the third (by "
            "subject) of the three Theban plays though composed first; the central "
            "Greek tragedy on the binding contending claim; supplied as fact, "
            "interpretation left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The Greek seminar text on the contending claim and what the city does with the law it has made.",
                "memory_work": {
                    "recitations": ["Recitation of the first choral ode in a worthy modern translation"],
                },
                "recitation_routine": "Seminar opens from the recited ode; the discussion takes its first question from what the chorus said about being human.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy translation of Antigone (Fagles; Heaney's The Burial at Thebes) read aloud as a living book, parts taken",
                ],
                "short_lesson_flow": "A living book read aloud and narrated; the contending claims followed and told back, deepening to analysis of the play's refusal to settle as the bands move up.",
                "narration_prompt": "Tell back the episode we read today, and tell me what Antigone said and what Creon said, and which one the play would have us think was right.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy translation of Antigone on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in contending claims, civil disobedience, or the city leads; a filmed performance watched together",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; let the contending claim be a contending claim. No imposed resolution.",
                "observation_documentation": "Over time, notice whether the student returns to the play and brings the contending claim into other reading. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of Greek tragic conventions and the play's contending-claim structure where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-008": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "The Oresteia (Agamemnon, The Libation Bearers, The Eumenides)",
            "author": "Aeschylus",
            "date": "458 BCE",
            "genre": "Greek tragedy",
            "form": "trilogy of verse tragedies with choral odes",
        },
        "minimum_band": "advanced",
        "content_notes": (
            "The murder of Agamemnon (in his bath, on his return), the killing of "
            "Clytemnestra by her son Orestes, the pursuit of Orestes by the Furies, "
            "the establishment of the court of the Areopagus; offstage violence "
            "reported, the trilogy moves from blood-vengeance to founded law. "
            "Honest information, not a gate."
        ),
        "craft_focus": [
            "The trilogy as one dramatic argument: three plays read as a single whole (lit-craft-053)",
            "The chorus across three plays: elders of Argos, the libation bearers, the Furies turned Eumenides (lit-craft-052 and lit-craft-053)",
            "Clytemnestra and Orestes as characters bearing the work's argument (lit-craft-014)",
            "The system of voices and the founding of public justice (lit-craft-023)",
            "Figurative networks across the trilogy: blood, net, lion, the loom (lit-craft-042)",
        ],
        "entry": (
            "Advanced: read the three plays as one dramatic argument and follow the "
            "transformation from inherited bloodshed to founded law; read each "
            "chorus as the function its play needs; argue what Aeschylus does to "
            "the inherited material that his audience knew already; honor what the "
            "trilogy refuses to settle (the Furies are placated, but the Furies "
            "are not gone). Mastery: original argument about how the trilogy founds "
            "the Western tragic form's question about justice."
        ),
        "close_reading_passages": [
            "Clytemnestra's welcome of Agamemnon at the palace door and the carpet scene: how does the play stage the entrance to the house, and what does the staging do that no soliloquy could?",
            "Cassandra before the palace, hearing what no one else hears: how does the play give a chorus of one its truth, and what does the dramatic irony achieve?",
            "The closing of The Eumenides: Athena's verdict and the transformation of the Furies; what does the trilogy refuse to settle even at the end?",
        ],
        "structural_analysis": (
            "Three plays, one argument: Agamemnon shows the inherited vendetta "
            "(blood for blood for blood); The Libation Bearers shows the next "
            "vendetta (Orestes killing his mother to avenge his father); The "
            "Eumenides shows the founding of the court that breaks the cycle. The "
            "Furies pursue Orestes across plays; Apollo defends; Athena founds the "
            "Areopagus. The trilogy is the structural argument that public justice "
            "is what breaks vendetta, and that nothing about the Furies has been "
            "merely erased."
        ),
        "thematic_lines": [
            "Vendetta and founded justice: what the polis must do with the inherited claim of blood",
            "The Furies before and after: a power not abolished but housed; how the polis incorporates what cannot be banished",
            "Clytemnestra as agent and as the vendetta's continuance: a character the trilogy makes the audience hold without flattening",
        ],
        "comparative_threads": [
            "Oedipus Rex (lit-work-006) and Antigone (lit-work-007): the Sophoclean treatment of the same questions (knowing, contending claim) handled differently by Aeschylus's predecessor and successor",
            "Hamlet (lit-work-011): Shakespeare's inheritance of the inherited-vendetta problem; what the revenger does when there is no Areopagus yet",
            "The Iliad (lit-work-002): the unbroken vendetta of the heroic age; what Aeschylus's polis does that Achilles's camp could not",
        ],
        "seminar_questions": [
            "Where in the trilogy is the turn? Is it Orestes's killing, Athena's vote, or somewhere else?",
            "What does the trilogy say about Clytemnestra that it never says plainly? Where does it refuse to say?",
            "Are the Furies placated, transformed, or housed? What does the play refuse to settle about them?",
        ],
        "writing_invitations": [
            "The analytical paragraph on the carpet scene, naming what staging does that dialogue alone could not",
            "The essay on what the trilogy says about justice and what the trilogy refuses to settle about the Furies",
            "The sustained essay on the chorus across the three plays, naming what each chorus does that the others could not",
        ],
        "context": (
            "Performed at the City Dionysia in Athens in 458 BCE; the only complete "
            "Greek tragic trilogy to survive; foundational text for the founding "
            "of the Areopagus and for the Western tragic argument about justice; "
            "supplied as fact, interpretation left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The foundational trilogy on the founding of public justice; the only complete Greek tragic trilogy to survive.",
                "memory_work": {
                    "recitations": ["Recitation of a choral ode from Agamemnon in a worthy modern translation"],
                },
                "recitation_routine": "Seminar opens from the recited ode; the discussion takes its first question from what the chorus of elders knows and refuses to say.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy translation of the Oresteia (Robert Fagles; Ted Hughes; Anne Carson's An Oresteia for a modern composite reading) read aloud across a term",
                ],
                "short_lesson_flow": "A living book read aloud and narrated across the three plays; the long arc followed, the Furies tracked, deepening to analysis of the founding scene as the bands move up.",
                "narration_prompt": "Tell back the episode we read today, and tell me what the Furies are doing now, and what has changed since the last sitting.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy translation of the Oresteia on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in justice, vendetta, or the founding of law leads; a filmed performance of one play watched together",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; bring the long arc into the room across many sittings.",
                "observation_documentation": "Over time, notice whether the student begins to ask what justice does with what vengeance leaves behind. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of the trilogy form and the transformation across the three plays where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-009": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "The Bacchae",
            "author": "Euripides",
            "date": "c. 405 BCE (posthumously performed)",
            "genre": "Greek tragedy",
            "form": "verse tragedy with choral odes",
        },
        "minimum_band": "advanced",
        "content_notes": (
            "The dismemberment of Pentheus by his mother Agave in Dionysian frenzy "
            "(offstage; reported in detail by the messenger and shown after the "
            "fact when Agave returns with her son's head), maenadic violence, the "
            "god's punishment of Thebes; offstage violence is reported with full "
            "tragic intensity. Honest information, not a gate."
        ),
        "craft_focus": [
            "The play's refusal to settle between god and city, between piety and reason (lit-craft-053)",
            "Dionysus as a character on stage who is also the god the play is about (lit-craft-014)",
            "The chorus of bacchants as the god's voice and the audience's discomfort (lit-craft-052)",
            "Pentheus's cross-dressing and the staging of recognition that arrives too late (lit-craft-053)",
            "Figurative networks: the bull, the mountain, the wand, the dismemberment as figural and literal (lit-craft-042)",
        ],
        "entry": (
            "Advanced: read the play as Euripides's late and most discomforting "
            "argument about what a city does with a god it does not understand; "
            "argue what the play refuses to settle (is Dionysus just, vindictive, "
            "or beyond the categories the play offers; is Pentheus the rationalist "
            "the play warns against or the city's last defender); set the play "
            "against the inheritance of Athenian tragedy and against later "
            "treatments of Dionysus. Mastery: original argument about the place of "
            "the play in the late Euripidean turn and in the long argument about "
            "reason and ecstasy."
        ),
        "close_reading_passages": [
            "The opening prologue spoken by Dionysus in disguise: how does the play stage a god speaking to the audience while in disguise to the characters?",
            "The exchange between Pentheus and the disguised Dionysus, where Pentheus consents to be dressed as a woman: how does the play stage Pentheus's loss of self before the dismemberment?",
            "Agave's return with the head and the slow recovery of her sight: what does the play do with the recognition that arrives too late?",
        ],
        "structural_analysis": (
            "A god comes to a city that has refused him; the city's king refuses "
            "him; the god destroys the king through the king's own mother. The "
            "structure does not punish a wrongdoer and reward a saint; it shows a "
            "city undone by what it would not include and a god whose justice the "
            "play does not endorse. Every choric ode raises the god's claim; "
            "every Pentheus scene tightens the disaster; the recognition arrives "
            "in Agave, not in Pentheus."
        ),
        "thematic_lines": [
            "Reason and ecstasy: what the polis must do with the power it cannot domesticate; whether the play sides with Pentheus or with Dionysus, or neither",
            "Recognition arriving too late: the tragic form taken to a particular extreme",
            "The chorus's faith and the audience's discomfort: a play whose chorus the audience does not always want to follow",
        ],
        "comparative_threads": [
            "The Oresteia (lit-work-008): two plays about a city incorporating what it cannot abolish; what the Furies become against what Dionysus refuses to become",
            "Oedipus Rex (lit-work-006): two tragedies of late and devastating recognition; what each does with the recognized character",
            "Modern responses (Wole Soyinka's The Bacchae of Euripides; Donna Tartt's The Secret History as inheritor): how the play has been read against later moments of reason against ecstasy",
        ],
        "seminar_questions": [
            "Does the play endorse Dionysus, Pentheus, both, or neither? Where does the play refuse to say?",
            "What does the chorus of bacchants ask the audience to hold, and where does the audience pull back?",
            "What does the play do with Agave's recognition that no earlier tragedy had done?",
        ],
        "writing_invitations": [
            "The analytical paragraph on the scene where Pentheus is dressed, naming what the staging does that no soliloquy could",
            "The essay on what the play refuses to settle between reason and ecstasy",
            "The sustained essay on the chorus of bacchants as a function the play needs and the audience resists",
        ],
        "context": (
            "Composed in the last years of Euripides's life at the court of "
            "Archelaus of Macedon; performed posthumously at the City Dionysia c. "
            "405 BCE; one of the last great Athenian tragedies; supplied as fact, "
            "interpretation left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The late Euripidean tragedy on the polis and the god it refuses; the seminar text on reason and ecstasy.",
                "memory_work": {
                    "recitations": ["Recitation of a choral ode of the bacchants in a worthy modern translation"],
                },
                "recitation_routine": "Seminar opens from the recited ode; the discussion takes its first question from what the chorus claims that the audience may not be ready to grant.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy translation of The Bacchae (William Arrowsmith; Anne Carson's Bakkhai) read aloud across a few sittings, parts taken",
                ],
                "short_lesson_flow": "A living book read aloud and narrated; the god's claim and the king's refusal followed through to recognition, deepening to analysis of the play's refusal to settle as the bands move up.",
                "narration_prompt": "Tell back the scene we read today, and tell me what the bacchants said and whether you believed them.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy translation of The Bacchae on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in reason and ecstasy, in the city's outsiders, or in late Euripides leads; a filmed performance watched together",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; let the play's discomfort be discomfort. No imposed resolution.",
                "observation_documentation": "Over time, notice whether the student returns to the play and brings its question into other reading. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of late Euripidean tragedy and the play's refusal-to-settle structure where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-010": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Inferno (Divine Comedy, Part 1)",
            "author": "Dante Alighieri",
            "date": "c. 1308-1320 (Inferno composed c. 1308-1314)",
            "genre": "medieval Christian epic poetry",
            "form": "narrative poem in terza rima, thirty-four cantos",
        },
        "minimum_band": "advanced",
        "content_notes": (
            "Sustained images of punishment and physical torment in each circle of "
            "Hell, often described in vivid corporeal detail; political invective "
            "against contemporary Florentines and named historical figures; "
            "presentation of damnation as deserved within the poem's theological "
            "frame; the poem holds particular damnations the reader is invited to "
            "weigh and sometimes to resist. Honest information, not a gate."
        ),
        "craft_focus": [
            "Close reading across modes: the meditative-narrative poem read with the same sustained attention as a novel (lit-craft-004)",
            "The contrapasso as figurative system: each punishment a figure for the sin (lit-craft-043)",
            "The inherited descent figure: Aeneas's katabasis, the underworld of Odyssey 11, transformed (lit-craft-043)",
            "Theme as the work's argument: the structured cosmos in which moral order is the law of the place (lit-craft-023)",
            "The voice of the pilgrim and the voice of the poet: who knows what when, and what the gap does to the reader (lit-craft-031 in the family of moves)",
        ],
        "entry": (
            "Advanced: read the Inferno whole and read the contrapasso as a "
            "figurative system that makes the theology available; place the poem "
            "against its inheritance (Virgil as guide and Virgil as the inherited "
            "epic; the descent from Homer); argue what the poem refuses to settle "
            "(the readings the reader is invited to resist; the damnations the "
            "poem invites grief over); follow the gap between the pilgrim's knowing "
            "and the poet's knowing. Mastery: original argument about how the "
            "Inferno does theology by figure, and what that argument asks of the "
            "reader who does not share its frame."
        ),
        "close_reading_passages": [
            "The opening tercets and the dark wood: how does the poem begin in the middle of life, and what does the simile of the man who escapes the sea do to the reader's footing?",
            "Canto 5 (the second circle, the lustful; Paolo and Francesca): what does the poem do by making the pilgrim faint and by giving the damned the most beautiful speech?",
            "Canto 33 (Count Ugolino in the ice): how does the poem stage a damnation it invites grief over without contradicting the cosmology that placed him there?",
        ],
        "structural_analysis": (
            "Thirty-four cantos descending through nine circles into the center "
            "of the earth, the structure built so that the punishment in each "
            "circle is a figure for the sin: lust whirled in the wind, gluttons "
            "lying in foul rain, traitors frozen in ice. The terza rima locks "
            "every tercet into the next, the form a structural argument that the "
            "cosmos is interlocked. The pilgrim narrates as one who has been "
            "there; the poet narrates as one who has written. The gap between "
            "the two is part of the poem's argument."
        ),
        "thematic_lines": [
            "Moral order as the law of the place: the cosmos as theological argument, the contrapasso as its figure",
            "Sympathy and judgment: the damnations the reader is asked to weigh, the readings the poem invites and the readings it invites resistance to",
            "The inheritance the poem is doing something to: classical epic descent transformed by Christian eschatology",
        ],
        "comparative_threads": [
            "The Aeneid (lit-work-003): Virgil as the pilgrim's guide and as the poem's most-cited classical predecessor; the descent in Aeneid 6 as the direct ancestor of the Inferno's structure",
            "The Odyssey (lit-work-001): the older descent of Odysseus in book 11 as the inheritance behind Virgil's, and through Virgil behind Dante's",
            "Milton's Paradise Lost (to be authored): the next great Christian epic and the inheritance Dante shapes for it",
        ],
        "seminar_questions": [
            "Where does the poem invite resistance to its own judgments? Which lines give you the resistance?",
            "Where is the pilgrim's knowing different from the poet's? What does the gap do?",
            "Is the contrapasso always just within the poem's frame? Where does the figure exceed the theology?",
        ],
        "writing_invitations": [
            "The analytical paragraph on one circle and its contrapasso, naming what the figure does that direct theological statement could not",
            "The essay on a damnation the poem invites grief over (Francesca, Ugolino, Brunetto), naming what the poem makes the reader hold",
            "The comparative paragraph setting the descent of Inferno against the descent of Aeneid 6, naming what Dante does to the inheritance",
        ],
        "context": (
            "Composed in vernacular Tuscan in exile from Florence between roughly "
            "1308 and 1320; the first part of a three-part Christian epic that "
            "established the Italian literary language and shaped Western "
            "imagination of the afterlife for seven centuries; supplied as fact, "
            "interpretation left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The foundational medieval Christian epic; the Western seminar text on the moral cosmos, with Virgil as the named guide.",
                "memory_work": {
                    "recitations": ["Recitation of the opening tercets of Canto 1 in a worthy modern translation"],
                },
                "recitation_routine": "Seminar opens from the recited opening; the discussion takes its first question from where the pilgrim finds himself and what the recital of the dark wood asks of the reader.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy translation of Inferno (Robert and Jean Hollander; Mark Musa; Allen Mandelbaum) read aloud across a term, paired with notes and a worthy commentary",
                ],
                "short_lesson_flow": "A living book read aloud across cantos and narrated each sitting; the descent followed circle by circle, the contrapasso noticed, deepening to analysis of the moral cosmos as the bands move up.",
                "narration_prompt": "Tell back the canto we read today, and tell me which damnation you found yourself resisting, and which line gave you the resistance.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy translation of Inferno on the shelf with a worthy commentary alongside, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in the afterlife, in moral order, or in the long inheritance from Virgil leads",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; let the damnations be weighed honestly; bring Virgil into the room when Dante does.",
                "observation_documentation": "Over time, notice whether the student returns to particular damnations and finds their own readings forming. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of medieval Christian cosmology and the contrapasso as figurative system where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-011": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Hamlet",
            "author": "William Shakespeare",
            "date": "c. 1600-1601",
            "genre": "English Renaissance drama",
            "form": "verse tragedy with prose interludes, five acts",
        },
        "minimum_band": "advanced",
        "content_notes": (
            "Murder by poisoning (before the play and within); the staged play of "
            "the murder, the death of Ophelia (offstage, between scenes; her "
            "grief and unraveling are on stage), the duel at the close, multiple "
            "deaths; the play's emotional weight is in Hamlet's interior and in "
            "the gap between what he says he will do and what he does. Honest "
            "information, not a gate."
        ),
        "craft_focus": [
            "The soliloquy as the playwright's argument against narration: Hamlet's seven major soliloquies as the play's interior (lit-craft-051, lit-craft-053)",
            "The play against the revenge-tragedy inheritance: what Shakespeare does to the type (lit-craft-053)",
            "Hamlet as a character who is also the play's argument: hesitation as the work's question (lit-craft-014)",
            "Unreliable interiority: Hamlet's own speeches as a near-relation of the unreliable narrator's gap (lit-craft-031)",
            "Theme advanced: what the play refuses to settle about action, conscience, theatre as truth-telling (lit-craft-023)",
        ],
        "entry": (
            "Advanced: read the play whole and against the revenge-tragedy "
            "tradition the play is doing something to; argue the seven soliloquies "
            "as the play's interior argument; hold Hamlet's hesitation as the "
            "work's question rather than the work's flaw; honor what the play "
            "refuses to settle (conscience, action, what the play-within-the-play "
            "does to truth-telling). Mastery: original argument about Hamlet as "
            "the play that revises the revenge tradition's basic claim."
        ),
        "close_reading_passages": [
            "The ghost scene on the battlements (Act 1 Scene 5): how does the play stage the inherited injunction, and what does the ghost ask Hamlet to do that the play will spend four more acts hesitating over?",
            "The 'to be or not to be' soliloquy (Act 3 Scene 1): what does the soliloquy do that no exchange with another character could; where does the speech know itself and where does it not?",
            "The play within the play and the closet scene (Act 3 Scenes 2 and 4): what does the staged play do, and how does the closet scene with Gertrude reframe what we have just watched?",
        ],
        "structural_analysis": (
            "Five acts in which the ghost's injunction sits unfulfilled for four "
            "and a half; the play is structured so that what would be the climax "
            "in any other revenge tragedy is what does not happen here. The "
            "soliloquies carry the interior argument; the play-within-the-play "
            "makes theatre itself a means of truth-telling; the duel at the end "
            "is the action arriving when its motive has nearly been forgotten. "
            "The structure is the play's argument: revenge as a frame the play "
            "refuses to fill on the frame's own terms."
        ),
        "thematic_lines": [
            "Conscience and action: what the play counts as virtue when revenge is the inherited duty",
            "Theatre as truth-telling: the play-within-the-play's claim that staged fiction can show what direct accusation cannot",
            "What is rotten in Denmark: a court whose corruption Hamlet sees and the play does not let any one character cleanse",
        ],
        "comparative_threads": [
            "The Oresteia (lit-work-008): the inherited-vendetta problem treated by founding the law-court; Hamlet has no Areopagus, and the play asks what the revenger does without one",
            "The revenge-tragedy tradition (Thomas Kyd's The Spanish Tragedy of c. 1587 as the named predecessor; Marlowe's tragedies as the contemporary type) which Shakespeare is doing something to",
            "Macbeth (lit-work-012) and King Lear (lit-work-013): the other late Shakespearean tragedies, each handling conscience and action differently",
            "Stoppard's Rosencrantz and Guildenstern Are Dead (1966) as an explicit later inheritor",
        ],
        "seminar_questions": [
            "What does Hamlet's hesitation argue, in the play's own terms? Where does the play refuse to call the hesitation a flaw?",
            "What does the play-within-the-play know that the rest of the play cannot say plainly?",
            "Is conscience the play's hero or its trap? Which lines tell you?",
        ],
        "writing_invitations": [
            "The analytical paragraph on one of the seven soliloquies, naming what the speech reveals that Hamlet would never say to another character",
            "The essay on what the play does to the revenge-tragedy inheritance, with passages from the play and references to the tradition",
            "The sustained essay on hesitation as the play's argument rather than as the prince's failing",
        ],
        "context": (
            "Composed for the Lord Chamberlain's Men around 1600-1601, drawing on "
            "the Norse Amleth legend through Saxo Grammaticus and Belleforest, and "
            "on the revenge-tragedy type established in England by Kyd's The "
            "Spanish Tragedy; the play has been continuously performed and read "
            "for four centuries; supplied as fact, interpretation left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The Shakespearean tragedy the seminar tradition keeps returning to; the play that revises the revenge form and gives the West its most-quoted soliloquies.",
                "memory_work": {
                    "recitations": ["Recitation of one of the seven major soliloquies"],
                },
                "recitation_routine": "Seminar opens from the recited soliloquy; the discussion takes its first question from what the speech says only because Hamlet is alone.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of Hamlet (Folger; Arden 3) read aloud across a term with parts taken, paired with a live or filmed performance",
                ],
                "short_lesson_flow": "A living book read aloud across acts and narrated each sitting; the soliloquies returned to, the ghost's injunction tracked, deepening to analysis of the play's refusal to give revenge what it usually asks for.",
                "narration_prompt": "Tell back the scene we read today, and tell me what Hamlet said when he was alone, and whether he did the thing he said he would do.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of Hamlet on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in soliloquy, in conscience and action, or in Shakespeare leads; performances watched together",
                ],
                "parent_role": "Be a fellow reader who has lived with the play in their own returning. Watch a performance together; read a soliloquy aloud when the student wants to hear it.",
                "observation_documentation": "Over time, notice whether the student returns to the play, takes up particular soliloquies, and begins to feel the hesitation as the play's question. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of the soliloquy as dramatic interior and the play's place in the revenge-tragedy tradition where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-012": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Macbeth",
            "author": "William Shakespeare",
            "date": "c. 1606",
            "genre": "English Renaissance drama",
            "form": "verse tragedy with prose interludes, five acts",
        },
        "minimum_band": "proficient",
        "content_notes": (
            "The murder of Duncan (offstage, immediately reported), the murder of "
            "Banquo (onstage), the murder of Lady Macduff and her children "
            "(onstage), the deaths of Lady Macbeth and Macbeth; the play moves "
            "quickly and the violence accumulates as the consequences of the first "
            "act unfold; sleepwalking and visions of blood throughout. Honest "
            "information, not a gate."
        ),
        "craft_focus": [
            "The play's tight structure: the shortest of the great tragedies, every scene compounds the last (lit-craft-052)",
            "The three witches as choric function: not a Greek chorus but a near-relation, speaking from outside the social order (lit-craft-052)",
            "Macbeth's interior across the soliloquies: the dagger, 'tomorrow and tomorrow and tomorrow' (lit-craft-051, lit-craft-013)",
            "Figurative networks: blood that will not wash, sleep murdered, the unsexed wish (lit-craft-042)",
            "Lady Macbeth as the work's argument running alongside Macbeth's (lit-craft-013)",
        ],
        "entry": (
            "Proficient: meet the play whole, name where the play turns (the "
            "decision at the door, the killing of Duncan, the moment Macbeth "
            "loses sleep), read the witches as a choric function, follow the "
            "figurative network of blood and sleep. Advanced: argue what the play "
            "does to inherited ambition and to the regicide story; hold "
            "Macbeth's interior alongside Lady Macbeth's; honor what the play "
            "refuses to settle about the witches' agency. Mastery: original "
            "argument about the play's tightness as its dramatic argument."
        ),
        "close_reading_passages": [
            "The witches' first scene and the encounter on the heath: how does the play stage the meeting that sets everything off, and what does the staging refuse to make the witches' agency settle?",
            "The dagger soliloquy (Act 2 Scene 1): what does the speech reveal about what Macbeth is becoming, and what does the play do by giving him the dagger he sees but cannot touch?",
            "Lady Macbeth's sleepwalking (Act 5 Scene 1): how does the play stage the consequence of the first act on a character who would not have predicted it of herself?",
        ],
        "structural_analysis": (
            "Five acts in a compressed timeline; every scene carries the weight "
            "of the first murder; the figurative network (blood, sleep, the "
            "unsexed wish, the future tense) compounds across acts. The witches "
            "open and close the moral atmosphere; Lady Macbeth's resolve and "
            "Macbeth's hesitation invert across the middle acts; by the end the "
            "tomorrow speech has lost the future the play started with. The "
            "structure is the play's argument: ambition is not a single act but "
            "what the single act sets in motion."
        ),
        "thematic_lines": [
            "Ambition and consequence: the play's question is not whether Macbeth wanted the crown but what wanting it does",
            "Witches and agency: the play refuses to say whether the witches cause or only foresee; the refusal is itself an argument",
            "Sleep and blood as the work's figurative system: each returning across acts, each carrying meaning the dialogue cannot say plainly",
        ],
        "comparative_threads": [
            "Hamlet (lit-work-011) and King Lear (lit-work-013): the three late Shakespearean tragedies; what each does with conscience, action, and aftermath",
            "Holinshed's Chronicles and the Scottish-history inheritance: what Shakespeare takes from the historical Macbeth and what he changes",
            "Verdi's Macbeth and Kurosawa's Throne of Blood as twentieth-century inheritors that read the play through its tightness",
        ],
        "seminar_questions": [
            "Where does the play turn? Is it the witches' meeting, the decision at the door, or somewhere else?",
            "What do the witches cause and what do they only foresee? Where does the play refuse to say?",
            "What does the tomorrow speech know at the end that the dagger soliloquy did not?",
        ],
        "writing_invitations": [
            "The analytical paragraph on the dagger soliloquy, naming what the speech reveals that no exchange could",
            "The essay on the figurative system of blood and sleep across the play",
            "At advanced, the comparative paragraph setting the play against the Scottish-history inheritance",
        ],
        "context": (
            "Composed for the King's Men around 1606, drawing on Holinshed's "
            "Chronicles and on contemporary anxiety about regicide following the "
            "Gunpowder Plot; performed for King James, whose lineage the play "
            "addresses through Banquo; the shortest of Shakespeare's major "
            "tragedies; supplied as fact, interpretation left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The Shakespearean tragedy of tightest structure; the seminar text on ambition and consequence.",
                "memory_work": {
                    "recitations": ["Recitation of the dagger soliloquy or the tomorrow speech"],
                },
                "recitation_routine": "Seminar opens from the recited soliloquy; the discussion takes its first question from where in the play the speech sits and what it knows.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of Macbeth (Folger; Arden 3) read aloud across a few weeks with parts taken, paired with a worthy performance",
                ],
                "short_lesson_flow": "A living book read aloud across acts and narrated; the figurative network of blood and sleep noticed as it returns, deepening to analysis of the play's tightness as the bands move up.",
                "narration_prompt": "Tell back the scene we read today, and tell me whether the blood or the sleep came back, and what Macbeth said when he was alone.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of Macbeth on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in ambition, in the supernatural in drama, or in Shakespeare leads; performances watched together",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; let the witches' agency stay unsettled when the play leaves it unsettled.",
                "observation_documentation": "Over time, notice whether the student returns to the play and follows the figurative network into other reading. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of the play's tight structure and figurative network where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-013": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "King Lear",
            "author": "William Shakespeare",
            "date": "c. 1605-1606",
            "genre": "English Renaissance drama",
            "form": "verse tragedy with prose interludes, five acts; substantially different Quarto (1608) and Folio (1623) texts",
        },
        "minimum_band": "advanced",
        "content_notes": (
            "The blinding of Gloucester on stage; the suicides and assumed suicides; "
            "the storm scenes and Lear's madness; the death of Cordelia and Lear at "
            "the close; the play offers no consolation and ends with the surviving "
            "characters carrying what cannot be undone. Honest information, not a "
            "gate."
        ),
        "craft_focus": [
            "What the play refuses to settle: justice, gods, kindness, the meaning of nothing (lit-craft-053)",
            "Two plots that mirror and diverge: Lear and his daughters, Gloucester and his sons (lit-craft-052)",
            "The Fool as a near-choric function, speaking truth the play will not let any other character say (lit-craft-052)",
            "Lear's interior across the storm scenes: madness as a kind of clarity the kingdom forbade (lit-craft-014, lit-craft-053)",
            "The Quarto/Folio question: two versions of the ending, neither editorially abolished; what the textual situation tells us about the play (lit-craft-053)",
        ],
        "entry": (
            "Advanced: read the play whole and read the two plots as one structural "
            "argument; honor what the play refuses to settle (kindness, justice, "
            "the gods; the death of Cordelia is not redeemed by the play); read "
            "the Fool as a function the play needs and then takes away; argue what "
            "the storm scenes do that no dialogue between agents could; meet the "
            "Quarto and Folio endings as part of the work, not an editorial "
            "embarrassment. Mastery: original argument about what the play does to "
            "the inherited Lear story (Holinshed; the older anonymous King Leir) "
            "by refusing the redemption the source supplied."
        ),
        "close_reading_passages": [
            "The opening love-test (Act 1 Scene 1): how does the play stage Lear's demand and Cordelia's refusal, and what does the staging do that no narration of the same moment could?",
            "The storm scenes and the heath (Act 3): how does the play stage Lear's madness as a kind of clarity, and what does the Fool do across these scenes?",
            "The closing scene with Cordelia and Lear (Act 5 Scene 3): how does the play stage an ending the inherited story redeemed and the play refuses to redeem?",
        ],
        "structural_analysis": (
            "Two plots, mirroring and diverging: Lear divides his kingdom by a "
            "love-test and is undone by Goneril and Regan; Gloucester is undone by "
            "Edmund and saved, briefly, by Edgar. The play's structural argument "
            "is the doubling: the two plots are not subplot and main plot but two "
            "stories the play needs to hold together. The storm scenes break the "
            "kingdom open; the Fool's disappearance after Act 3 is itself a "
            "structural choice the play does not explain; the closing scene "
            "refuses the consolation the source story had given."
        ),
        "thematic_lines": [
            "Nothing: the word the play turns on and turns again, from Cordelia's refusal to Lear's recognition",
            "Kindness in the play's full sense (kind, of the same kin) as the virtue the play insists on without rewarding",
            "What the gods do or do not do: the play offers competing readings and does not resolve them",
        ],
        "comparative_threads": [
            "Hamlet (lit-work-011) and Macbeth (lit-work-012): the late tragedies, each refusing consolation differently",
            "The anonymous King Leir (c. 1590) and Holinshed's Chronicles: the inherited Lear story that gave Shakespeare a redemptive ending; what Shakespeare refuses",
            "Beckett's Endgame (1957) as the modern inheritor of an ending the world will not redeem",
        ],
        "seminar_questions": [
            "What does the play do by refusing to redeem the ending the source supplied?",
            "Where does the Fool go after Act 3, and what does the play argue by removing him?",
            "Is the storm a place of madness or of clarity? Where does the play refuse to choose?",
        ],
        "writing_invitations": [
            "The analytical paragraph on the word 'nothing' as it returns across the play",
            "The essay on what the play refuses to settle about the gods and kindness, holding three or four passages in productive tension",
            "The comparative paragraph setting Shakespeare's ending against the redemptive ending of the older Lear story",
        ],
        "context": (
            "Composed for the King's Men around 1605-1606; the Quarto of 1608 and "
            "the Folio of 1623 carry substantially different texts (different "
            "scenes, different endings) and modern editors handle the two-text "
            "problem in different ways; the play has been a touchstone of Western "
            "tragic argument for four centuries; supplied as fact, interpretation "
            "left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The Shakespearean tragedy that refuses the consolation its source supplied; the seminar text on kindness, nothing, and the gods.",
                "memory_work": {
                    "recitations": ["Recitation of a speech from the storm scenes, or Cordelia's first refusal"],
                },
                "recitation_routine": "Seminar opens from the recited passage; the discussion takes its first question from where in the play the speech sits and what the play refuses to redeem.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of King Lear (Folger; Arden 3, conscious of the Quarto/Folio question) read aloud across a term, paired with a worthy performance",
                ],
                "short_lesson_flow": "A living book read aloud across acts and narrated; the two plots followed alongside each other, the Fool's lines noticed, deepening to analysis of the play's refusals as the bands move up.",
                "narration_prompt": "Tell back the scene we read today, and tell me what the Fool said, and what Lear had not yet seen.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of King Lear on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in tragedy, in kindness, or in Shakespeare's late refusals leads; performances watched together",
                ],
                "parent_role": "Be a fellow reader who has lived with the play in their own returning. Let the play's refusal of consolation be honored; do not paper over the closing scene.",
                "observation_documentation": "Over time, notice whether the student returns to the play and begins to feel its refusals as part of its argument. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of the two-plot structure, the Fool, and the Quarto/Folio question where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-014": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "The Sonnets (selection from the sequence of 154)",
            "author": "William Shakespeare",
            "date": "composed across the 1590s into the early 1600s; published 1609",
            "genre": "Renaissance lyric poetry",
            "form": "fourteen-line sonnet in the English form (three quatrains and a couplet, iambic pentameter, rhyme scheme abab cdcd efef gg)",
        },
        "minimum_band": "proficient",
        "content_notes": (
            "The sequence holds love, desire, jealousy, the procreation argument, "
            "the rival poet, the young man, the dark lady; the sequence does not "
            "resolve into a narrative and the reader is asked to hold what the "
            "speaker holds. Honest information, not a gate."
        ),
        "craft_focus": [
            "Close reading proficient on a single sonnet: the volta as the turn (lit-craft-003)",
            "Figurative networks within and across sonnets: time, the rose, the mirror, the line of writing (lit-craft-042)",
            "Theme as the work's argument: writing as preservation, time as the work's antagonist (lit-craft-022)",
            "The speaker as a constructed voice (lit-craft-014 in the family of moves): the sonnet's I is not Shakespeare and not a fixed character",
        ],
        "entry": (
            "Proficient: read individual sonnets whole; identify the volta and "
            "argue how the couplet earns or refuses what the quatrains set up; "
            "follow figurative networks (time, the rose, the line) across two or "
            "three sonnets that share them. Advanced: read the sequence as a "
            "sequence and ask what shape it has when 154 sonnets are held together "
            "without a story; set Shakespeare's sonnets against the inherited "
            "Petrarchan tradition the speaker quietly argues with. Mastery: "
            "original argument about the speaker as a constructed voice and what "
            "the sequence does that no other Renaissance lyric sequence had done."
        ),
        "close_reading_passages": [
            "Sonnet 18 ('Shall I compare thee to a summer's day'): how does the poem refuse the comparison it offers, and what does the couplet claim about writing?",
            "Sonnet 73 ('That time of year thou mayst in me behold'): three quatrains, three figures for late life; what does each figure refuse, and what does the couplet ask in return?",
            "Sonnet 130 ('My mistress' eyes are nothing like the sun'): a sonnet against the inherited praise tradition; what does the speaker do to Petrarchism, and what does the couplet rescue from the refusal?",
        ],
        "structural_analysis": (
            "Each sonnet is a fourteen-line argument: three quatrains build a "
            "case, the volta (often at line 9 or at the couplet) turns it, and "
            "the closing couplet claims or refuses what the quatrains set up. "
            "Across the sequence the figures recur (time, the rose, the line of "
            "writing, the mirror, the lease) and accumulate meaning by return. "
            "The sequence is not a narrative; it is the speaker's argument with "
            "himself, with the addressee, and with time, held across 154 "
            "fourteen-line propositions."
        ),
        "thematic_lines": [
            "Writing as the work's only stay against time; the speaker's claim that the line will outlast the loved",
            "The Petrarchan inheritance and what the speaker refuses about it: a tradition of praise tested by a speaker who keeps refusing its terms",
            "The young man, the dark lady, the rival poet: presences the sequence circles without resolving",
        ],
        "comparative_threads": [
            "Petrarch's Rerum vulgarium fragmenta (the Canzoniere): the inherited sonnet sequence Shakespeare is doing something to",
            "Donne's Holy Sonnets: the contemporary metaphysical alternate path; the same form bent toward different ends",
            "Hamlet (lit-work-011), Macbeth (lit-work-012), King Lear (lit-work-013): Shakespeare's other body of work and what it tells us about the same author across forms",
            "Later sonnet sequences (Elizabeth Barrett Browning's Sonnets from the Portuguese; Heaney's Glanmore Sonnets) as inheritors of the form",
        ],
        "seminar_questions": [
            "Where in this sonnet does the turn fall, and what does the couplet earn or refuse?",
            "What does the sequence do that no single sonnet could do?",
            "What does the speaker refuse about the inherited praise tradition, and what does the speaker keep from it?",
        ],
        "writing_invitations": [
            "The analytical paragraph on a single sonnet, naming the volta and what the couplet claims or refuses",
            "The essay on a figurative network (time, the rose, the line of writing) across three or four sonnets that share it",
            "At advanced, the essay on the speaker as a constructed voice and what the sequence does that no narrative could",
        ],
        "context": (
            "Composed across the 1590s into the early 1600s; published in 1609 in "
            "a quarto whose ordering and dedication have been argued over for "
            "four centuries; the central English Renaissance lyric sequence and "
            "the form's defining English example; supplied as fact, "
            "interpretation left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The defining English Renaissance lyric sequence; the seminar text on the sonnet's compressed argument.",
                "memory_work": {
                    "recitations": ["Recitation of a chosen sonnet from memory"],
                },
                "recitation_routine": "Seminar opens from the recited sonnet; the discussion takes its first question from where the turn falls and what the couplet does.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of the Sonnets (Stephen Booth; Helen Vendler's reading commentary; the Arden) read aloud one or two at a sitting",
                ],
                "short_lesson_flow": "A sonnet read aloud whole and narrated; the volta found, the couplet weighed; figurative networks noticed across a few sonnets that share them, deepening to analysis of the sequence as the bands move up.",
                "narration_prompt": "Tell back the sonnet we just read, and tell me where it turned and what the couplet earned or refused.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of the Sonnets on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in love poetry, in form, or in Shakespeare leads; a sonnet read aloud because the reader wanted to hear it",
                ],
                "parent_role": "Be a fellow reader who has lived with particular sonnets in their own returning. Read one aloud when the reader wants to hear it. Let the sequence be a sequence, not a story.",
                "observation_documentation": "Over time, notice whether the student returns to particular sonnets and begins to feel the sequence's figurative networks across them. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of the English sonnet form and the volta where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-015": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "The Canterbury Tales (selections: General Prologue, the Knight's Tale, the Miller's Tale, the Wife of Bath's Prologue and Tale)",
            "author": "Geoffrey Chaucer",
            "date": "c. 1387-1400 (unfinished at Chaucer's death)",
            "genre": "medieval frame narrative",
            "form": "narrative poem in Middle English; mixed meter, predominantly iambic pentameter couplets; tales in many forms (romance, fabliau, sermon, exemplum)",
        },
        "minimum_band": "proficient",
        "content_notes": (
            "Sexual material in the fabliaux (notably the Miller's Tale and the "
            "Reeve's), bawdy humor, medieval anti-Semitic content in the "
            "Prioress's Tale (not in this selection), the Wife of Bath's frank "
            "treatment of marriage and her own desire; the work holds its "
            "fourteenth-century world without polishing it. Honest information, "
            "not a gate."
        ),
        "craft_focus": [
            "Character proficient: each tale-teller is the work's argument about themselves; the tale fits the teller (lit-craft-013)",
            "Voice as constructed within voice: the General Prologue's narrator describing the pilgrims who tell the tales (lit-craft-008 in the family of moves)",
            "Theme as the tale-and-teller in conversation: the Knight tells a romance; the Miller answers with a fabliau (lit-craft-022)",
            "The Wife of Bath's Prologue as a single character's sustained argument against the clerical tradition that has constructed her (lit-craft-014 in entry)",
        ],
        "entry": (
            "Proficient: read the General Prologue and three or four tales with "
            "their teller-portraits; argue how each tale fits its teller and what "
            "the placement of tales does to each other (Knight then Miller; the "
            "Wife of Bath then the Clerk in the Marriage Group); read in a worthy "
            "modern translation alongside the Middle English original where "
            "possible. Advanced: argue what Chaucer does to the inherited "
            "tradition (Boccaccio's Decameron, the romance tradition, the "
            "fabliau, the clerical anti-feminist tradition the Wife of Bath "
            "argues with); read the Marriage Group as a sustained argument across "
            "several tales. Mastery: original argument about the frame as the "
            "work's structural argument and Chaucer's place in establishing the "
            "English literary tradition."
        ),
        "close_reading_passages": [
            "The General Prologue (the opening 'Whan that Aprille'): how does the narrator introduce the pilgrimage, and what stance does the narrator take toward the pilgrims he is about to describe?",
            "The opening of the Knight's Tale and the opening of the Miller's Tale: how does the placement of one tale against the next argue something neither tale alone does?",
            "The Wife of Bath's Prologue (her account of her five husbands): how does Chaucer give a character a sustained argument against the tradition that has constructed her, and what does the prologue do that her tale alone could not?",
        ],
        "structural_analysis": (
            "A frame narrative on pilgrimage to Canterbury, with a host who "
            "proposes a tale-telling contest; the General Prologue introduces "
            "the pilgrims through a narrator who is among them but also above "
            "them; the tales are told by characters who have just been "
            "introduced, and each tale fits or strains against its teller. The "
            "structure is the work's argument: voices in conversation, no "
            "authoritative narrator, the moral and literary frame negotiated "
            "across many tellers."
        ),
        "thematic_lines": [
            "Tale and teller: the tale fits its teller, and the teller is constructed by the tale they choose",
            "Authority and experience: the Wife of Bath's argument with the clerical tradition that defined women in her time",
            "Estates and the social order: how the General Prologue presents the medieval estates and what the narrator does and does not say about them",
        ],
        "comparative_threads": [
            "Boccaccio's Decameron: the immediate inherited model of the tale-telling frame; what Chaucer does that the Decameron did not",
            "The romance tradition (the Knight's Tale draws on Boccaccio's Teseida) and the fabliau tradition (the Miller's Tale's continental cousins)",
            "The clerical anti-feminist tradition (Jerome's Against Jovinian and the Wife's own quoted sources): the inheritance the Wife of Bath argues with",
            "Later English frame narratives and tale-telling cycles (Bocaccio's Italian successors; the inheritance forward into Spenser's Faerie Queene and beyond)",
        ],
        "seminar_questions": [
            "How does the tale fit the teller in the Knight's Tale, and how does the Miller's Tale argue against the Knight's by being placed next?",
            "What does the Wife of Bath's Prologue do that her Tale alone could not?",
            "Where in the General Prologue is the narrator on a side? Where does he refuse to be on one?",
        ],
        "writing_invitations": [
            "The analytical paragraph on a portrait from the General Prologue, naming what the narrator says and what he carefully does not say",
            "The essay on how a tale fits its teller, holding two or three passages from the prologue and the tale together",
            "At advanced, the essay on the Wife of Bath's Prologue as an argument with the inherited tradition that defined her",
        ],
        "context": (
            "Composed in London in the last decade of Chaucer's life; "
            "unfinished at his death in 1400; the founding work of English "
            "literary tradition in the vernacular; supplied as fact, "
            "interpretation left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The founding work of English vernacular literary tradition; the seminar text on voices in conversation.",
                "memory_work": {
                    "recitations": [
                        "Recitation of the opening of the General Prologue in Middle English or a worthy modern translation"
                    ],
                },
                "recitation_routine": "Seminar opens from the recited opening; the discussion takes its first question from what the narrator says about the pilgrims he is about to describe.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of the Canterbury Tales (Nevill Coghill's modern verse translation; the Riverside Chaucer for the Middle English; David Wright's prose translation) read aloud across a term",
                ],
                "short_lesson_flow": "A living book read aloud across the chosen tales, the General Prologue first; the tale and the teller held alongside each other; deepening to analysis of how the placement of tales argues across them.",
                "narration_prompt": "Tell back the portrait or the tale we read today, and tell me what the teller is doing by telling that tale.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of the Canterbury Tales on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in voices, in medieval life, or in the founding of English literature leads; readings in Middle English heard aloud",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; let the bawdier tales be themselves; honor the Wife of Bath as her own argument.",
                "observation_documentation": "Over time, notice whether the student returns to particular pilgrims and begins to feel the conversation across tales. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of the frame narrative, the estates tradition, and the tale-and-teller match where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-016": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Don Quixote",
            "author": "Miguel de Cervantes Saavedra",
            "date": "Part 1 published 1605; Part 2 published 1615",
            "genre": "early modern Spanish novel",
            "form": "prose narrative; the supposed translation of a manuscript by 'Cide Hamete Benengeli'; layered narration; embedded tales",
        },
        "minimum_band": "advanced",
        "content_notes": (
            "Comic violence (the beatings the knight takes, often described "
            "without sentimentality); period attitudes toward conversos and "
            "Moors; the cruelty visited on Quixote by the Duke and Duchess in "
            "Part 2; the death of Quixote at the close. The novel is both "
            "comedy and elegy at once. Honest information, not a gate."
        ),
        "craft_focus": [
            "Layered, unreliable narration: the narrator's claim to be translating Cide Hamete Benengeli; the prologue's I; the gaps and the asides (lit-craft-031)",
            "Character advanced: the inherited romance hero set against itself; what the novel does to the chivalric type (lit-craft-014)",
            "Theme advanced: what the novel refuses to settle about Quixote (madman, holy fool, the last reader of romances); the novel as the founding of the modern novel form (lit-craft-023)",
            "The figurative system of romances inside the novel: the books Quixote has read are constantly present in his speech and his vision (lit-craft-043)",
        ],
        "entry": (
            "Advanced: read the novel whole (both parts; Part 2 is essential to "
            "the work) and read the layered narration as the work's argument "
            "about what fiction is; argue what Cervantes does to the chivalric "
            "inheritance the knight has read into himself; hold Quixote as "
            "madman and as holy fool at once, refusing the binary the novel "
            "refuses; meet Part 2 as a meta-fictional turn where characters "
            "have read Part 1. Mastery: original argument about the novel as "
            "the founding of the modern novel form and what every later novel "
            "owes to the move."
        ),
        "close_reading_passages": [
            "The opening of Part 1 and the prologue: how does the narrator stage his own claim to be presenting a found manuscript, and what does the prologue's I do that the narrator of the chapters cannot?",
            "The windmills (Part 1, chapter 8): how does the novel stage the moment everyone remembers, and what does the staging do to the question of whether Quixote is mad?",
            "The encounter with the spurious Quixote in Part 2 (chapter 59) and the closing of Part 2: how does the novel respond to the publication of the false Avellaneda continuation, and how does the novel let Quixote die?",
        ],
        "structural_analysis": (
            "Two parts (1605 and 1615) bound together by Cervantes's response in "
            "Part 2 to the publication of a spurious continuation by another "
            "writer. The narration claims to be a translation of a manuscript by "
            "Cide Hamete Benengeli, but the manuscript itself contains "
            "interruptions, missing pages, and an editor's interventions; there "
            "is no single authoritative voice. Part 1 establishes the knight, "
            "his squire, and the world's resistance to his romance; Part 2 "
            "establishes a world that has read Part 1 and treats Quixote "
            "accordingly. The structure is the work's argument: fiction read "
            "into the world remakes the world that reads the fiction."
        ),
        "thematic_lines": [
            "Madman or holy fool: the novel holds Quixote as both and refuses to settle which",
            "What romance does when it is taken literally; what literature does in a world that no longer believes it",
            "The friendship of Quixote and Sancho: the novel's most steady reality, against the changing illusions",
        ],
        "comparative_threads": [
            "The chivalric romance tradition (Amadís de Gaula and the other romances Quixote has read; the same tradition Ariosto is doing something else to in Orlando Furioso); the inheritance the novel works against",
            "The Aeneid (lit-work-003) and the older epic inheritance behind chivalric romance",
            "Later novels that owe themselves to Cervantes: Sterne's Tristram Shandy as the first overt inheritor; the modern novel from Cervantes forward",
            "Borges's 'Pierre Menard, Author of the Quixote' as the most direct twentieth-century engagement with the novel's question about what writing is",
        ],
        "seminar_questions": [
            "Is Quixote mad or a holy fool? Where does the novel refuse to say?",
            "What does the layered narration (Cide Hamete, the translator, the editor, the I of the prologue) do that a single voice could not?",
            "What changes in Part 2 because the world has read Part 1, and what does the novel argue by making that change?",
        ],
        "writing_invitations": [
            "The analytical paragraph on the windmills, naming what the staging does to the question of Quixote's madness",
            "The essay on the layered narration as the work's argument",
            "The sustained essay on what the novel does to the chivalric inheritance and on Part 2 as the meta-fictional turn",
        ],
        "context": (
            "Composed and published in Madrid; Part 1 (1605) was an immediate "
            "success across Europe, prompting both translations and a spurious "
            "continuation that drew Cervantes's response in Part 2 (1615); "
            "commonly named the founding work of the modern novel; supplied as "
            "fact, interpretation left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The founding work of the modern novel; the seminar text on layered narration and on what fiction read into the world does.",
                "memory_work": {
                    "recitations": [
                        "Recitation of the opening of Part 1 ('En un lugar de la Mancha...') in Spanish or a worthy modern translation"
                    ],
                },
                "recitation_routine": "Seminar opens from the recited opening; the discussion takes its first question from where the narrator stands and what 'En un lugar de la Mancha' refuses to say.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy translation of Don Quixote (Edith Grossman; John Rutherford; Tobias Smollett's older version) read aloud across a term, in chunks, with Sancho and Quixote's exchanges taken in parts",
                ],
                "short_lesson_flow": "A living book read aloud in long chunks and narrated; the friendship of Quixote and Sancho followed across the changing illusions; deepening to analysis of the layered narration as the bands move up.",
                "narration_prompt": "Tell back the chapter we read today, and tell me whether the world saw what Quixote saw, and whether Sancho did.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy translation of Don Quixote on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in heroes, in madness, in friendship, or in what fiction does leads",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; let the question of Quixote's madness stay unsettled; bring romances into the room when the novel does.",
                "observation_documentation": "Over time, notice whether the student returns to the novel, holds Quixote as both madman and holy fool, and brings the layered narration into other reading. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of layered narration and the novel's relation to the chivalric inheritance where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-017": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Paradise Lost",
            "author": "John Milton",
            "date": "first published 1667 (ten books); revised twelve-book edition 1674",
            "genre": "Christian epic poetry",
            "form": "blank verse epic in twelve books; classical epic conventions (invocation, in medias res opening, epic similes) bent to Christian subject",
        },
        "minimum_band": "advanced",
        "content_notes": (
            "Cosmic warfare and the casting down of the rebel angels; the "
            "temptation and fall of Adam and Eve and the expulsion from "
            "Paradise; sustained theological argument in Milton's particular "
            "Protestant frame; the poem holds Satan with a power that has "
            "troubled readers for three and a half centuries. Honest "
            "information, not a gate."
        ),
        "craft_focus": [
            "Close reading across modes: the meditative epic in dense blank verse and inverted Latinate syntax (lit-craft-004)",
            "Figurative argument: the fall as the work's full figurative system; light and dark; height and depth; the conscious epic similes (lit-craft-043)",
            "Character advanced: Satan as the inherited tragic hero recast; what Milton does to the heroic tradition (lit-craft-014)",
            "Theme advanced: the justification of God's ways and what the poem refuses to settle about Satan (lit-craft-023)",
        ],
        "entry": (
            "Advanced: read the poem whole and read the blank verse as the "
            "argument; argue what Milton does to the classical epic he is "
            "consciously inheriting (Virgil first, then Homer through Virgil); "
            "hold the Satan question (heroic, villain, both, and what the poem "
            "does with each reading) as the work's central refusal to settle "
            "easily; read the figurative system of light and dark as "
            "constitutive of meaning. Mastery: original argument about the "
            "poem's place in the inheritance from Virgil and Dante and forward "
            "into Romantic poetry."
        ),
        "close_reading_passages": [
            "The opening invocation of Book 1: how does Milton invoke the Holy Spirit and announce the argument, and what does the long suspended syntax do to the reader's footing?",
            "Satan's first speech in Book 1 ('Better to reign in Hell, than serve in Heaven'): what does the speech reveal, and where does the poem refuse to let the reader simply agree or simply refuse?",
            "Eve's account of her own creation in Book 4 and the temptation in Book 9: how does the poem give Eve her own consciousness, and what does Book 9 do that no third-person narration of the same events could?",
        ],
        "structural_analysis": (
            "Twelve books built consciously inside the classical epic form Milton "
            "is inheriting: an invocation, an in-medias-res opening (the angels "
            "already cast down), epic similes, councils, journeys, set-piece "
            "battles, and a conscious doubling of Aeneid and Iliad halves. "
            "Inside that form, Christian material: the fall, the cosmic war, "
            "the temptation, the expulsion. The structure is the work's "
            "argument: pagan epic bent to Christian subject; what the form can "
            "hold and what it strains under."
        ),
        "thematic_lines": [
            "The Satan question: heroic in his refusal, villain in his pride, and what the poem does to keep the reader holding both",
            "Justification: the poem's stated argument is to justify the ways of God to men; what justification means in the poem's terms",
            "Free will and obedience: the poem's structural argument that the fall must be free to be a fall",
        ],
        "comparative_threads": [
            "The Aeneid (lit-work-003): Milton's most-consciously-imitated classical epic; the structural doubling and the inheritance of epic conventions",
            "The Iliad (lit-work-002) and the Odyssey (lit-work-001) through Virgil",
            "Dante's Inferno (lit-work-010): the previous great Christian epic; Milton's Satan against Dante's; the inheritance Milton works inside and against",
            "Genesis: the biblical source the poem expands and the reader is invited to weigh against the poem's expansion",
            "Romantic inheritors (Blake's claim that Milton was of the devil's party; Shelley's Prometheus Unbound) as the poem's most decisive afterlife",
        ],
        "seminar_questions": [
            "Is Satan heroic, villain, or what? Where does the poem refuse to settle which?",
            "What does the blank verse do that rhyme could not, and what does Milton say in his preface about why he chose it?",
            "How does the poem justify the ways of God to men, and where does the poem leave the justification to the reader?",
        ],
        "writing_invitations": [
            "The analytical paragraph on the opening invocation, naming what the long suspended sentence does to the reader's footing",
            "The essay on Satan as the inherited tragic hero recast, holding two or three of his major speeches in productive tension",
            "The sustained essay on the poem's place in the epic inheritance from Virgil through Dante, with passages from each",
        ],
        "context": (
            "Composed in Milton's blindness after the Restoration of the English "
            "monarchy in 1660 and Milton's own political eclipse; first "
            "published in 1667 in ten books, revised into a twelve-book edition "
            "in 1674; the foundational long poem in English after Spenser; "
            "supplied as fact, interpretation left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The foundational English Christian epic; the seminar text on the Satan question and on epic form bent to Christian subject.",
                "memory_work": {
                    "recitations": ["Recitation of the opening invocation of Book 1"],
                },
                "recitation_routine": "Seminar opens from the recited invocation; the discussion takes its first question from where the long sentence resolves and what it claims.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of Paradise Lost (the Norton Critical edition; the Oxford World's Classics) read aloud across a term, with the blank verse sounded out",
                ],
                "short_lesson_flow": "A living book read aloud across the twelve books and narrated; the blank verse heard for its sound, the figurative networks noticed, deepening to analysis of the Satan question as the bands move up.",
                "narration_prompt": "Tell back the book we read today, and tell me what Satan said, and whether the poem let you simply agree or simply refuse.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of Paradise Lost on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in Genesis, in epic, in the Satan figure, or in Milton's blindness leads",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; let the Satan question stay unsettled; bring Virgil and Dante into the room when the poem invokes them.",
                "observation_documentation": "Over time, notice whether the student returns to the poem, holds Satan with the poem's full ambivalence, and begins to feel the inheritance from Virgil and Dante. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of the blank verse line, the epic conventions Milton inherits, and the Satan question where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-018": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Gulliver's Travels",
            "author": "Jonathan Swift",
            "date": "first published 1726 (with revisions in 1735)",
            "genre": "satirical prose fiction",
            "form": "four-part prose narrative in the form of a traveler's memoir; first-person narration by Lemuel Gulliver",
        },
        "minimum_band": "proficient",
        "content_notes": (
            "Excretory and bodily humor (especially in Lilliput); a graphic "
            "scene of public humiliation among the Brobdingnagians; satirical "
            "violence including Gulliver's account of European warfare to the "
            "King of Brobdingnag; Book 4's depiction of the Yahoos is "
            "intentionally repellent and has been read both as misanthropy and "
            "as moral provocation. Honest information, not a gate."
        ),
        "craft_focus": [
            "Unreliable narration: Gulliver as the narrator the satire works through, increasingly unreliable as the voyages progress; the gap between Gulliver and Swift (lit-craft-031)",
            "Figurative system of the satire: scale (tiny, giant), proportion, the rational animal, the body politic figured as a body (lit-craft-042 at proficient; lit-craft-043 at advanced)",
            "Theme advanced: what the satire refuses to settle about reason, humanity, and the Yahoo (lit-craft-023)",
            "Voice realized through staged speech: the King of Brobdingnag and the Master Houyhnhnm as positions the satire stages (lit-craft-013 at proficient)",
        ],
        "entry": (
            "Proficient: read the four voyages whole; follow the satire's "
            "figurative move of changing scale and proportion across the first "
            "three books; meet the Houyhnhnms and Yahoos in Book 4 and feel the "
            "satire's turn. Advanced: argue what Gulliver knows when and where "
            "Gulliver and Swift diverge; argue what the satire refuses to "
            "settle about reason and the human; set the work against the "
            "travel-narrative tradition Swift is parodying. Mastery: original "
            "argument about Book 4 and the satire's place in the long inheritance "
            "of satire from Lucian forward."
        ),
        "close_reading_passages": [
            "The Lilliput court and the war over which end to break an egg (Book 1): how does the satire stage the politics of England's religious controversies by miniaturizing them?",
            "Gulliver's account of European warfare to the King of Brobdingnag (Book 2, chapter 6): how does the satire stage a defense of contemporary Europe that the satire itself refuses to endorse?",
            "Gulliver's return home from the Houyhnhnms (Book 4, last chapter): how does the satire stage Gulliver's revulsion from his own family, and where does the satire refuse to let the reader simply agree or simply refuse?",
        ],
        "structural_analysis": (
            "Four voyages of escalating satiric reach: Lilliput, where the "
            "miniaturization deflates contemporary English politics; "
            "Brobdingnag, where the magnification deflates Gulliver's defense "
            "of Europe; Laputa and the academy of Lagado, where the satire "
            "moves to abstract reason and projection; the Houyhnhnms and "
            "Yahoos, where the satire moves to what the rational animal is. "
            "The structure is the satire's argument: the more closely the "
            "reader follows Gulliver, the more sharply the reader is invited "
            "to see what Gulliver does not."
        ),
        "thematic_lines": [
            "Reason and the rational animal: the satire's deepest question, sharpened to a point in Book 4",
            "Scale as a satiric tool: what magnification and miniaturization expose that direct argument could not",
            "Gulliver as a vehicle the satire trusts and then withdraws trust from: where the reader and the narrator come apart",
        ],
        "comparative_threads": [
            "Lucian's True History and the ancient satiric travel inheritance",
            "Contemporary travel narratives Swift is parodying (the genuine voyages-and-discoveries literature of his moment)",
            "Voltaire's Candide (1759) as a sibling satire of the rational pretensions of Swift's century",
            "Orwell's 1984 (to be authored) as a political-satire descendant of Swift",
        ],
        "seminar_questions": [
            "Where do Gulliver and Swift diverge? In Book 4 especially, what does the satire let the reader see that Gulliver does not?",
            "Is Book 4 misanthropy, moral provocation, or both? Where does the work refuse to say?",
            "What does scale do in the satire that direct argument could not?",
        ],
        "writing_invitations": [
            "The analytical paragraph on a moment of scale-shift in Book 1 or Book 2, naming what the figure exposes",
            "The essay on Gulliver's account to the King of Brobdingnag, naming what the satire refuses to endorse",
            "The sustained essay on Book 4 and the question of the Yahoo: what the work refuses to settle",
        ],
        "context": (
            "Composed in Swift's later years in Dublin; published anonymously in "
            "1726 and an immediate sensation; the central English-language "
            "satire of the eighteenth century; supplied as fact, interpretation "
            "left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The central English-language satire of the eighteenth century; the seminar text on satire, scale, and the question of the rational animal.",
                "memory_work": {
                    "recitations": [
                        "Recitation of a chosen passage from the King of Brobdingnag's response to Gulliver"
                    ],
                },
                "recitation_routine": "Seminar opens from the recited passage; the discussion takes its first question from where the satire stages a position it then refuses to endorse.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of Gulliver's Travels (the unexpurgated text; the Penguin or Oxford World's Classics) read aloud across a term",
                ],
                "short_lesson_flow": "A living book read aloud across the four voyages and narrated; the figurative move of scale noticed across the first three books; deepening to analysis of Book 4 as the bands move up.",
                "narration_prompt": "Tell back the voyage we read today, and tell me what Gulliver thought it meant, and what the satire let you see that Gulliver did not.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of Gulliver's Travels on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in satire, in political and human folly, or in the question of the rational animal leads",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; let Book 4 be Book 4; do not paper over the satire's provocations.",
                "observation_documentation": "Over time, notice whether the student returns to particular voyages and begins to feel the gap between Gulliver and Swift. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of satire as a form, the figurative move of scale, and the unreliable narrator where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-019": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Pride and Prejudice",
            "author": "Jane Austen",
            "date": "first published 1813 (drafted earlier as 'First Impressions')",
            "genre": "English Regency novel",
            "form": "third-person novel with free indirect discourse; embedded letters at structural turning points",
        },
        "minimum_band": "proficient",
        "content_notes": (
            "Money, marriage as economic settlement, and the social pressures "
            "on women in early-nineteenth-century England; Lydia's elopement "
            "and its near-ruination of the family; the militia officer Wickham "
            "as a sustained false suitor. Honest information, not a gate."
        ),
        "craft_focus": [
            "Free indirect discourse: the proficient narrative-craft move named explicitly in lit-craft-008; Austen's narrator inhabits Elizabeth's mind without disappearing into it",
            "Character proficient: Elizabeth, Darcy, the Bennet parents, and the secondary characters as constructed positions (lit-craft-013)",
            "Theme proficient: marriage, money, pride and prejudice as the title earns over the plot (lit-craft-022)",
            "Ironic narration: the novel's opening sentence as a sustained study in irony; the family of moves with the unreliable narrator (lit-craft-031)",
        ],
        "entry": (
            "Proficient: read the novel whole, follow Elizabeth's growing "
            "understanding through free indirect discourse, name where pride "
            "and prejudice belong to Darcy and where to Elizabeth and where to "
            "both; meet the two great letters (Darcy's letter at Hunsford, "
            "Mr. Bennet's later) as structural turning points. Advanced: argue "
            "what the novel does with marriage as economic settlement and "
            "where the novel refuses to settle the question of romantic love "
            "versus prudent match; set the novel against the inherited "
            "marriage-plot tradition (Richardson, Burney) it is doing "
            "something to. Mastery: original argument about Austen's place in "
            "the formation of free indirect discourse as the defining tool of "
            "the nineteenth-century novel."
        ),
        "close_reading_passages": [
            "The opening sentence and the first chapter: how does the famous opening sentence stage a claim the novel both holds and refuses, and what does the Bennet household reveal in its first exchange?",
            "Darcy's first proposal at Hunsford and his letter the following morning (volume 2, chapters 11-12 in most editions): how does the novel stage a misjudgment that the reader and Elizabeth must both work through, and what does the letter do that the proposal could not?",
            "Lady Catherine's confrontation with Elizabeth at Longbourn (volume 3, chapter 14 in most editions): how does the novel stage the scene where Elizabeth defends her own right to refuse and where her refusal opens the way to her acceptance?",
        ],
        "structural_analysis": (
            "Three volumes built around two great misjudgments: Elizabeth "
            "misreads Darcy at the Meryton assembly and Darcy misreads "
            "Elizabeth at the first proposal; the novel's central work is the "
            "correction of both by reading more carefully. Free indirect "
            "discourse lets the narrator stand inside Elizabeth's perception "
            "and outside it at once; the embedded letters mark the structural "
            "turns. The structure is the novel's argument: the marriage that "
            "matters is the one in which both characters have learned to read "
            "themselves."
        ),
        "thematic_lines": [
            "Pride and prejudice as faults distributed and earned by the plot; the title is not a label but a result",
            "Marriage as economic settlement and as something else; the novel holds both without giving either up",
            "Reading other people: the novel's deepest theme, exercised by Elizabeth and by the reader",
        ],
        "comparative_threads": [
            "Richardson's Pamela and Clarissa (Austen's most-named eighteenth-century novelistic inheritance); the epistolary form Austen has absorbed into third-person free indirect discourse",
            "Frances Burney's Evelina and Cecilia (Austen's named contemporary precursors)",
            "Charlotte Brontë's Jane Eyre (lit-work-021) and George Eliot's Middlemarch as later inheritors of Austen's narrative technique",
            "Modern adaptations and reworkings (Helen Fielding's Bridget Jones's Diary; the long film and television history) as twentieth- and twenty-first-century inheritors",
        ],
        "seminar_questions": [
            "Where in the novel does pride belong to Darcy and where to Elizabeth, and where to both at once?",
            "What does Darcy's letter do that his first proposal could not?",
            "Is the novel's marriage at the end a romance the novel endorses or a romance the novel ironizes? Where does the novel refuse to say?",
        ],
        "writing_invitations": [
            "The analytical paragraph on the opening sentence, naming what the irony does that direct statement could not",
            "The essay on free indirect discourse in a chosen scene, naming where the narrator stands inside and outside Elizabeth at once",
            "At advanced, the essay on marriage as economic settlement and as love in the novel, holding three or four passages in productive tension",
        ],
        "context": (
            "Composed in Hampshire across the 1790s and revised in the early "
            "1810s; published in 1813; one of six completed novels by Austen "
            "and the most widely read; supplied as fact, interpretation left "
            "to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The defining Regency novel and the central English example of free indirect discourse; the seminar text on reading other people.",
                "memory_work": {
                    "recitations": ["Recitation of the novel's opening sentence and the paragraph that follows"],
                },
                "recitation_routine": "Seminar opens from the recited opening; the discussion takes its first question from what the universally-acknowledged truth is and who acknowledges it.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of Pride and Prejudice (the Norton; the Penguin; the Oxford World's Classics) read aloud across a term, with the dialogue and the letters voiced separately",
                ],
                "short_lesson_flow": "A living book read aloud across the three volumes and narrated; Elizabeth's growing understanding followed sitting by sitting; deepening to analysis of free indirect discourse as the bands move up.",
                "narration_prompt": "Tell back the chapter we read today, and tell me what Elizabeth thought and where the narrator agreed and where the narrator gently did not.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of Pride and Prejudice on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in marriage, in irony, in social comedy, or in Austen leads; the long history of adaptations watched together",
                ],
                "parent_role": "Be a fellow reader who has lived with the novel in their own returning. Read a scene aloud with parts taken when the reader wants to hear the voices.",
                "observation_documentation": "Over time, notice whether the student returns to particular scenes and begins to feel free indirect discourse as the novel's central instrument. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of free indirect discourse and the marriage-plot tradition where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-020": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Frankenstein; or, The Modern Prometheus",
            "author": "Mary Wollstonecraft Shelley",
            "date": "first published anonymously 1818; revised edition 1831",
            "genre": "early-nineteenth-century novel; sometimes the founding work of science fiction",
            "form": "epistolary frame (Walton's letters) enclosing Victor Frankenstein's first-person narrative, which encloses the Creature's first-person narrative",
        },
        "minimum_band": "proficient",
        "content_notes": (
            "The creation of the Creature and his subsequent abandonment; the "
            "murders of William, Justine (executed for William's murder), "
            "Henry Clerval, and Elizabeth; Victor's pursuit of the Creature "
            "into the Arctic and Victor's death; the novel asks the reader "
            "throughout who the monster is and refuses to settle the question. "
            "Honest information, not a gate."
        ),
        "craft_focus": [
            "Nested narrators: Walton's letters around Victor's narrative around the Creature's narrative; each frame reframes what came before (lit-craft-008)",
            "Character advanced: the Promethean inherited type and the Creature as the inherited Adam-and-Satan reader of Paradise Lost (lit-craft-014)",
            "Theme advanced: creation and responsibility; what the novel refuses to settle about who is the monster (lit-craft-022 at proficient, lit-craft-023 at advanced)",
            "Figurative system: light, fire, ice; the figure of the spark and the figure of the wasteland (lit-craft-042)",
        ],
        "entry": (
            "Proficient: read the novel whole, track the three nested narratives "
            "and what each frame argues; meet the Creature's account in Volume 2 "
            "as the heart of the novel; follow the figurative system of fire and "
            "ice. Advanced: argue what the novel does to the Prometheus "
            "inheritance and to Paradise Lost (which the Creature reads and "
            "argues with himself about); honor what the novel refuses to "
            "settle about who is the monster. Mastery: original argument about "
            "the novel as the founding work of a tradition that runs from "
            "Shelley through Wells, Stevenson, and forward."
        ),
        "close_reading_passages": [
            "Walton's letters that open the novel: how does the epistolary frame stage the listener whose stand-in we are about to become?",
            "The Creature's account of finding Paradise Lost and reading himself into it (Volume 2): how does the novel stage the Creature's reading, and what does the Creature's identification with both Adam and Satan do?",
            "The closing scene with the Creature standing over Victor's body: how does the novel let the Creature speak last, and where does the novel refuse to let the reader simply judge?",
        ],
        "structural_analysis": (
            "Three nested narratives: Walton writes letters home to his "
            "sister; in those letters Walton transcribes Victor's first-person "
            "account; in Victor's account the Creature delivers his own "
            "first-person account. Each narrator has his own interest in the "
            "story, and the novel never collapses the three into one "
            "authoritative voice. The structure is the work's argument: every "
            "account of who made the monster is filtered through someone who "
            "had a reason to tell it the way they did."
        ),
        "thematic_lines": [
            "Creation and responsibility: who owes what to whom when one being makes another",
            "Who is the monster: the question the novel refuses to settle; competing readings have been held for two centuries",
            "Knowledge and its costs: the Prometheus subtitle's claim, weighed by the novel rather than asserted",
        ],
        "comparative_threads": [
            "Paradise Lost (lit-work-017): the Creature reads it and recognizes himself in both Adam and Satan; the novel makes Milton's poem one of its own structural references",
            "Greek Prometheus (the subtitle); the Aeschylean Prometheus Bound through Percy Shelley's Prometheus Unbound",
            "Coleridge's 'Rime of the Ancient Mariner' which Walton quotes; the contemporary Romantic inheritance",
            "Later inheritors: H. G. Wells's Island of Doctor Moreau; the long science-fiction tradition that begins here; the film tradition that has largely refused the novel's framing of who the monster is",
        ],
        "seminar_questions": [
            "Who is the monster, in the novel's own terms? Where does the novel refuse to say?",
            "What does the Creature's reading of Paradise Lost let the novel argue that direct statement could not?",
            "What does the Walton frame do that the novel without it could not?",
        ],
        "writing_invitations": [
            "The analytical paragraph on the Creature's account of finding and reading Paradise Lost, naming what the identification with Adam and with Satan does to the question of who he is",
            "The essay on the nested-narrator structure as the novel's argument",
            "At advanced, the essay on the novel's inheritance from Milton and from Greek Prometheus, holding passages from each in productive tension",
        ],
        "context": (
            "Begun in 1816 at the Villa Diodati on Lake Geneva as part of the "
            "ghost-story contest with Percy Shelley, Byron, and Polidori; "
            "published anonymously in 1818 when the author was twenty; revised "
            "and republished under her name in 1831; one of the foundational "
            "works of the modern novel and of the tradition that became "
            "science fiction; supplied as fact, interpretation left to the "
            "student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The foundational nineteenth-century novel of creation and responsibility; the seminar text on who the monster is.",
                "memory_work": {
                    "recitations": ["Recitation of the Creature's first speech to Victor on the glacier"],
                },
                "recitation_routine": "Seminar opens from the recited speech; the discussion takes its first question from what the Creature claims from his maker and what the novel does with the claim.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of Frankenstein (either the 1818 or 1831 text, with notes on the differences; the Norton; the Penguin) read aloud across a term, with parts taken for the embedded narratives",
                ],
                "short_lesson_flow": "A living book read aloud across the three nested narratives and narrated; the Creature's account given its full weight; deepening to analysis of the Paradise Lost inheritance as the bands move up.",
                "narration_prompt": "Tell back the chapter we read today, and tell me whose voice told it, and what that voice wanted us to think.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of Frankenstein on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in creation, in monsters, in Romantic poetry, or in the early history of science fiction leads",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; let the question of who the monster is stay unsettled.",
                "observation_documentation": "Over time, notice whether the student returns to the novel and brings the Creature's reading of Paradise Lost into other reading. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of the nested-narrator frame and the novel's place in Romantic and proto-science-fiction tradition where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-021": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Jane Eyre",
            "author": "Charlotte Brontë (published initially under the pseudonym Currer Bell)",
            "date": "first published 1847",
            "genre": "Victorian Bildungsroman with Gothic elements",
            "form": "first-person retrospective novel in five settings (Gateshead, Lowood, Thornfield, Marsh End, Ferndean); direct address to the reader at structural moments",
        },
        "minimum_band": "proficient",
        "content_notes": (
            "The Reed household's cruelty in Gateshead; the privations and "
            "deaths at Lowood School; the revelation of Bertha Mason, Rochester's "
            "first wife, kept in the attic at Thornfield; the fire at Thornfield "
            "and Rochester's blinding; St. John Rivers's marriage proposal as a "
            "pressure on Jane's selfhood; the novel holds Bertha as a presence "
            "the reader is invited to weigh and that later readings (notably "
            "Jean Rhys's Wide Sargasso Sea) have reframed. Honest information, "
            "not a gate."
        ),
        "craft_focus": [
            "First-person retrospective voice with direct address to the reader (lit-craft-008)",
            "Character proficient: Jane as the work's argument; her insistence on her own equality and self-sovereignty (lit-craft-013; named as exemplar text in lit-craft-013)",
            "Gothic figurative network: the red room at Gateshead, the dying fires at Lowood, Thornfield and its attic, the chestnut tree split by lightning (lit-craft-042)",
            "Theme proficient: equality, conscience, the right of the self to refuse what would erase it (lit-craft-022)",
        ],
        "entry": (
            "Proficient: read the novel whole across its five settings; follow "
            "Jane's first-person retrospective voice and the direct address to "
            "the reader as a structural choice; meet the Gothic figurative "
            "network and the revelation of Bertha as the structural turn at "
            "Thornfield. Advanced: argue what the novel does to the inherited "
            "Bildungsroman tradition and what it does that no earlier "
            "first-person Bildungsroman by a woman had done; honor what the "
            "novel does and does not do with Bertha; meet Jean Rhys's Wide "
            "Sargasso Sea as the work that argues with this novel's treatment "
            "of Bertha. Mastery: original argument about Jane Eyre's place in "
            "the formation of the first-person novel of conscience."
        ),
        "close_reading_passages": [
            "The red room at Gateshead (Chapter 2): how does the novel stage the first cruelty done to Jane, and how does the red room become a figure the novel returns to?",
            "Jane and Rochester in the garden after the chestnut tree is split by lightning (Volume 2, near the end of the Thornfield section): how does the novel stage a betrothal that the next chapters will undo, and what does the lightning-split tree do to the reader?",
            "Jane's refusal of St. John Rivers's proposal (Volume 3): how does the novel stage a different kind of erasure than the one at Thornfield, and what does Jane refuse here that completes what she refused there?",
        ],
        "structural_analysis": (
            "Five settings, each a stage of Jane's formation: Gateshead "
            "(childhood cruelty), Lowood (schooling under privation), "
            "Thornfield (the great trial), Marsh End (a different test of "
            "self-erasure under Christian duty), Ferndean (the marriage on "
            "Jane's own terms). The first-person retrospective voice holds "
            "the older Jane's understanding around the younger Jane's "
            "experience; the direct address to the reader (most famously "
            "'Reader, I married him') marks structural turns and binds the "
            "reader as a witness. The structure is the novel's argument: a "
            "self that refuses every offer to be erased is the self the marriage "
            "is finally on."
        ),
        "thematic_lines": [
            "Equality and self-sovereignty: Jane's claim that she is the equal of any she meets, and what the novel does with her insistence",
            "Conscience as the work's compass: the novel's deepest commitment, and what the novel does when conscience pulls against love",
            "Bertha Mason as presence: the novel holds Bertha as the obstacle and as a presence later readings have read against the novel's framing",
        ],
        "comparative_threads": [
            "Pride and Prejudice (lit-work-019): the previous English Bildungsroman of a young woman's reading of others; what Brontë does that Austen did not",
            "Frankenstein (lit-work-020): the previous novel of a figure constructed and refused her own account; the two together form a near-pair",
            "Emily Brontë's Wuthering Heights (1847; to be authored): sister's novel published the same year, very different reading of love and household",
            "Jean Rhys's Wide Sargasso Sea (1966) as the postcolonial reply that gives Bertha her own account; an inheritor that argues with the novel",
        ],
        "seminar_questions": [
            "Where does Jane refuse to be erased, and where does the novel call her refusal the right one?",
            "What does the novel do with Bertha that the novel refuses to do explicitly, and how do later readings reframe what the novel does?",
            "What does the direct address to the reader do that no third-person narration could?",
        ],
        "writing_invitations": [
            "The analytical paragraph on the red room as a figure the novel returns to",
            "The essay on Jane's refusal of St. John Rivers and what it completes about her refusal at Thornfield",
            "At advanced, the essay on the novel's treatment of Bertha read alongside Wide Sargasso Sea",
        ],
        "context": (
            "Composed in Haworth, Yorkshire, by Charlotte Brontë and published "
            "under the male pseudonym Currer Bell in 1847; the central Victorian "
            "first-person novel of a young woman's formation; one of three "
            "Brontë novels published that year; supplied as fact, interpretation "
            "left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The central Victorian first-person novel of conscience; the seminar text on equality and self-sovereignty in nineteenth-century English fiction.",
                "memory_work": {
                    "recitations": [
                        "Recitation of Jane's declaration to Rochester ('I am no bird; and no net ensnares me')"
                    ],
                },
                "recitation_routine": "Seminar opens from the recited declaration; the discussion takes its first question from what Jane claims for herself and what the novel grants and refuses to grant.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of Jane Eyre (the Norton; the Penguin; the Oxford World's Classics) read aloud across a term",
                ],
                "short_lesson_flow": "A living book read aloud across the five settings and narrated; the Gothic figurative network noticed as it returns; deepening to analysis of the direct address as the bands move up.",
                "narration_prompt": "Tell back the chapter we read today, and tell me what Jane refused and what she said to the reader directly.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of Jane Eyre on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in nineteenth-century novels, in self-sovereignty, or in the Gothic leads; the long film history available",
                ],
                "parent_role": "Be a fellow reader who has lived with the novel in their own returning. Read aloud the famous declarations when the reader wants to hear them.",
                "observation_documentation": "Over time, notice whether the student returns to particular scenes and begins to ask what the novel does with Bertha. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of first-person retrospective narration and the Gothic figurative network where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-022": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Wuthering Heights",
            "author": "Emily Brontë (published initially under the pseudonym Ellis Bell)",
            "date": "first published 1847",
            "genre": "Victorian Gothic novel",
            "form": "double-framed narrative: Lockwood's diary encloses Nelly Dean's oral account; two-generation family chronicle",
        },
        "minimum_band": "advanced",
        "content_notes": (
            "Sustained cruelty and violence within the two households across "
            "two generations; Heathcliff's revenge against Hindley and against "
            "Edgar Linton; the deaths of Catherine, Hindley, Edgar, and "
            "Heathcliff himself; emotional and physical abuse of children "
            "across the second generation; the novel does not stand outside "
            "what it shows and does not redeem its violence by the close. "
            "Honest information, not a gate."
        ),
        "craft_focus": [
            "Double-framed unreliable narration: Lockwood's diary encloses Nelly Dean's oral account, and Nelly has her own stake in what she tells (lit-craft-031)",
            "Nested narration: every account is filtered through Nelly through Lockwood (lit-craft-008)",
            "Character advanced: Heathcliff as a figure the novel refuses to make categorizable (lit-craft-014)",
            "Figurative system: the moors, the two houses (the Heights and the Grange), windows and doors, ghosts at the window (lit-craft-042 at proficient; lit-craft-043 at advanced)",
            "What the novel refuses to settle about love, vengeance, the second generation's partial repair (lit-craft-023)",
        ],
        "entry": (
            "Advanced: read the novel whole and read both narrators with "
            "suspicion: Lockwood as outsider misreading what he records, Nelly "
            "as housekeeper whose account is shaped by her position and her "
            "loyalties; argue what the novel does that no straightforward "
            "narration could; hold Heathcliff as a figure the novel refuses to "
            "categorize; read the two generations as a structural argument. "
            "Mastery: original argument about the novel's place in nineteenth-"
            "century English fiction as the work that most thoroughly refuses "
            "the consolation Victorian fiction commonly offered."
        ),
        "close_reading_passages": [
            "Lockwood's nightmare at the window (chapter 3): how does the novel open with its outermost narrator's encounter with the ghost, and what does the staging do to what we will later read of Catherine and Heathcliff?",
            "Catherine's declaration about Heathcliff ('I am Heathcliff'): how does the novel stage a claim of identification that the rest of the novel will both honor and undo?",
            "The closing scenes at the Heights with the second generation: how does the novel stage a partial reconciliation, and where does it refuse to redeem what the first generation did?",
        ],
        "structural_analysis": (
            "Two generations across two households (Wuthering Heights, "
            "Thrushcross Grange), framed by Lockwood's diary in the present "
            "and Nelly Dean's oral account of the past; the doubled household "
            "and doubled generation are the novel's structural argument; "
            "every narrator is partial; the novel refuses to give the reader "
            "the consolation of an outside view. The structure is the "
            "argument: the novel of household and inheritance with no "
            "authoritative voice to tell us what either is for."
        ),
        "thematic_lines": [
            "Love and vengeance as the same passion or as opposed passions: the novel holds Heathcliff's love and his revenge as inseparable and refuses to settle which the novel is about",
            "The two generations: what the second generation partially repairs and what it cannot",
            "The moors as the novel's figurative other: the place outside the houses where the rules the houses live by do not reach",
        ],
        "comparative_threads": [
            "Jane Eyre (lit-work-021): sister's novel published the same year; very different reading of love and household; the two together form a near-pair of opposed Victorian novels",
            "The Gothic tradition (Walpole, Radcliffe, Maturin); Frankenstein (lit-work-020) as the earlier nineteenth-century work that also refused to settle who its monster was",
            "Later inheritors: Sylvia Plath's poetry; the long film history of the novel that has not known what to do with it",
        ],
        "seminar_questions": [
            "Whom does the novel trust as a narrator? Anyone?",
            "Where does the novel honor Catherine's claim to be Heathcliff and where does it undo it?",
            "Does the second generation repair what the first did, partially repair it, or refuse to repair it? Where does the novel refuse to say?",
        ],
        "writing_invitations": [
            "The analytical paragraph on Lockwood's nightmare, naming what the staging does to everything that follows",
            "The essay on Nelly Dean's reliability and what is at stake in her telling the story she tells",
            "The sustained essay on Heathcliff as a figure the novel refuses to make categorizable",
        ],
        "context": (
            "Composed in Haworth, Yorkshire, by Emily Brontë and published "
            "under the male pseudonym Ellis Bell in 1847; one of three Brontë "
            "novels published that year; widely misread in its century and "
            "central to twentieth-century arguments about narrative reliability; "
            "supplied as fact, interpretation left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The Victorian novel that most thoroughly refuses the consolation its century commonly offered; the seminar text on double-framed unreliable narration.",
                "memory_work": {
                    "recitations": ["Recitation of Catherine's declaration about Heathcliff"],
                },
                "recitation_routine": "Seminar opens from the recited declaration; the discussion takes its first question from what Catherine claims and how the novel both honors and undoes it.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of Wuthering Heights (the Norton; the Penguin; the Oxford World's Classics) read aloud across a term, with Lockwood's and Nelly's voices kept distinct",
                ],
                "short_lesson_flow": "A living book read aloud across the two generations and narrated; the framing of every account by Nelly through Lockwood noticed; deepening to analysis of the novel's refusals as the bands move up.",
                "narration_prompt": "Tell back the chapter we read today, and tell me whose voice told it, and whether you believed them.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of Wuthering Heights on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in the Brontës, in the Gothic, or in nineteenth-century novels that refuse easy reading leads",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; do not paper over the novel's violence or its refusal to redeem; let Nelly's account be Nelly's account.",
                "observation_documentation": "Over time, notice whether the student returns to the novel and begins to read Nelly with suspicion. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of double-framed narration and the two-generation structure where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-023": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Great Expectations",
            "author": "Charles Dickens",
            "date": "serialized 1860-61",
            "genre": "Victorian Bildungsroman",
            "form": "first-person retrospective novel in three stages of Pip's expectations; originally serialized; two endings exist, the published one and the earlier draft",
        },
        "minimum_band": "proficient",
        "content_notes": (
            "The opening encounter with Magwitch in the graveyard and Pip's "
            "terror; Miss Havisham's arrested wedding and her treatment of "
            "Estella; the violent death of Mrs. Joe; the fire that injures "
            "Miss Havisham; Magwitch's pursuit and death; the novel ends in "
            "two versions, both of which the editor of a worthy edition will "
            "include and discuss. Honest information, not a gate."
        ),
        "craft_focus": [
            "First-person retrospective: Pip the narrator looking back at Pip the boy, with a sustained gap between the two (lit-craft-008)",
            "Character proficient: Pip, Joe, Magwitch, Miss Havisham, Estella as constructed figures the novel needs (lit-craft-013)",
            "Theme proficient: expectations, gentility, the gift that does not come from where Pip thought (lit-craft-022)",
            "The gap between older Pip's understanding and younger Pip's: a near-relation of unreliable narration in the family of moves (lit-craft-031)",
        ],
        "entry": (
            "Proficient: read the novel whole across its three stages of "
            "Pip's expectations; follow the first-person retrospective voice "
            "and the gap between Pip-the-narrator and Pip-the-protagonist; "
            "meet the great revelation about the source of the expectations "
            "as the structural turn. Advanced: argue what Dickens does to the "
            "Bildungsroman tradition; meet both endings as part of the novel; "
            "honor what the novel refuses to settle about gentility, "
            "expectation, and the unearned gift. Mastery: original argument "
            "about Dickens's place in the formation of the Bildungsroman "
            "alongside Brontë and George Eliot."
        ),
        "close_reading_passages": [
            "The opening in the graveyard with Magwitch (chapter 1): how does the novel stage Pip's first encounter, and what does the staging do to everything the novel will later let us learn about Magwitch?",
            "The revelation of the source of Pip's expectations (Volume 2): how does the novel stage the turn, and what does Pip-the-narrator know about it that Pip-the-protagonist did not?",
            "The two endings (the published ending and the earlier ending Dickens drafted): how does each ending change what the novel argues about expectation and what is finally given?",
        ],
        "structural_analysis": (
            "Three stages of Pip's expectations (the forge and Satis House; "
            "Pip in London; the return of Magwitch and the unraveling); the "
            "novel is structured so that what Pip and the reader believe to be "
            "the source of the expectations is overturned by the truth, and "
            "what the truth then asks Pip to do is the work of the last "
            "stage. The first-person retrospective voice holds the older "
            "Pip's understanding around the younger Pip's experience without "
            "collapsing into either."
        ),
        "thematic_lines": [
            "Expectations: what they cost, who they come from, and what they ask",
            "Gentility and the working life: the novel weighs the forge against London and refuses to flatten the comparison",
            "The unearned gift and what it asks of the receiver: Magwitch's gift and Pip's response across the novel",
        ],
        "comparative_threads": [
            "Jane Eyre (lit-work-021): the previous English first-person Bildungsroman; the same form turned to different ends",
            "Dickens's earlier novels (David Copperfield is the prior first-person retrospective); what Dickens has tightened in this one",
            "Joyce's Dubliners (lit-work-029, in this batch) and A Portrait of the Artist as a Young Man: the first-person retrospective opened toward modernism",
        ],
        "seminar_questions": [
            "Where in the novel is the turn, and what does it cost?",
            "What does Pip-the-narrator know about himself that Pip-the-protagonist did not?",
            "Which ending does the novel argue for, the published one or the earlier draft? What does each let the novel claim?",
        ],
        "writing_invitations": [
            "The analytical paragraph on the opening graveyard scene, naming what the staging does to everything we later learn about Magwitch",
            "The essay on the gap between Pip-the-narrator and Pip-the-protagonist across the three stages",
            "The comparative paragraph on the two endings and what each lets the novel argue",
        ],
        "context": (
            "Serialized in Dickens's weekly periodical 'All the Year Round' "
            "across 1860-61; the most tightly constructed of Dickens's late "
            "novels and the most-taught of his Bildungsromans; supplied as "
            "fact, interpretation left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The tightest of Dickens's first-person novels; the seminar text on expectation and the unearned gift.",
                "memory_work": {
                    "recitations": ["Recitation of the opening paragraph in the graveyard"],
                },
                "recitation_routine": "Seminar opens from the recited opening; the discussion takes its first question from what the young Pip thought he saw and what the narrator now lets us see.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of Great Expectations (the Norton; the Penguin; the Oxford World's Classics) read aloud across a term, ideally including both endings",
                ],
                "short_lesson_flow": "A living book read aloud across the three stages and narrated; the gap between narrator-Pip and protagonist-Pip noticed; deepening to analysis of the turn and the two endings as the bands move up.",
                "narration_prompt": "Tell back the chapter we read today, and tell me what Pip thought then and what the narrator quietly knows now.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of Great Expectations on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in Dickens, in coming-of-age, or in what gifts ask of those who receive them leads",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; let both endings be available; do not impose a reading of which Dickens 'should' have chosen.",
                "observation_documentation": "Over time, notice whether the student returns to particular scenes and begins to feel the gap between the two Pips. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of first-person retrospective Bildungsroman and the novel's two endings where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-024": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Moby-Dick; or, The Whale",
            "author": "Herman Melville",
            "date": "first published 1851",
            "genre": "nineteenth-century American novel; hybrid form (narrative, drama, encyclopedia, sermon, scientific catalogue)",
            "form": "first-person narration by Ishmael, interrupted by 'Cetology' chapters, dramatic chapters with stage directions, philosophical essays, and other forms; 135 chapters and an epilogue",
        },
        "minimum_band": "advanced",
        "content_notes": (
            "Whaling violence in detail, including the killing and rendering "
            "of sperm whales; the sinking of the Pequod and the death of all "
            "hands but one; period attitudes toward race that the novel both "
            "exhibits and complicates (Ishmael's friendship with Queequeg; "
            "the depiction of the Pequod's mixed crew); the novel does not "
            "redeem its disaster. Honest information, not a gate."
        ),
        "craft_focus": [
            "Hybrid form: prose narrative interrupted by Cetology chapters, dramatic scenes with stage directions, philosophical and theological essays (lit-craft-008 strained past its proficient definition; lit-craft-053 in its dramatic chapters)",
            "Ishmael as a narrator who appears and disappears: the I that opens the novel recedes into a third-person witness for long stretches (lit-craft-031 in the family of moves)",
            "Ahab as inherited tragic hero in the family of Lear and Macbeth; what Melville does to the Shakespearean inheritance (lit-craft-014)",
            "The white whale as figurative system: the chapter 'The Doubloon' makes the multiple readings explicit (lit-craft-043)",
            "What the novel refuses to settle about what the whale means (lit-craft-023)",
        ],
        "entry": (
            "Advanced: read the novel whole including the Cetology chapters "
            "and the dramatic interludes, treating them as part of the work "
            "rather than as digressions; argue what Melville does to "
            "Shakespeare (Lear, Macbeth) and to Paradise Lost (Ahab in the "
            "Satanic inheritance); read the doubloon chapter as the novel's "
            "explicit instruction in how to read its central figure; honor "
            "what the novel refuses to settle about the whale. Mastery: "
            "original argument about the novel's hybrid form and its place in "
            "American literature."
        ),
        "close_reading_passages": [
            "The opening ('Call me Ishmael') and the first paragraphs: how does the novel stage its narrator, and what does the choice of self-naming do?",
            "'The Doubloon' (chapter 99): how does the novel stage multiple characters reading the same gold coin and seeing different things, and what is the novel telling the reader about the whale by staging this?",
            "Ahab's confrontation with the whale across the last three chapters and the epilogue: how does the novel let the disaster come and the one survivor speak, and what does the epilogue's quotation from Job do to the close?",
        ],
        "structural_analysis": (
            "A first-person novel that abandons its first person for long "
            "stretches; an epic that interrupts itself with whale anatomy and "
            "with dramatic dialogues complete with stage directions; a tragedy "
            "of an inherited Shakespearean figure mounted on an American "
            "whaler. The form is the work's argument: the whale exceeds any "
            "single mode of telling, so the novel uses every mode it can. The "
            "doubloon chapter is the novel's instruction in itself: the whale "
            "is what each character reads it to be, and the novel refuses to "
            "rank the readings."
        ),
        "thematic_lines": [
            "What the white whale means: the novel refuses to settle, and the doubloon chapter makes the refusal structural",
            "Ahab as Shakespearean inheritance: the late tragic figure mounted on a nineteenth-century American ship",
            "The Pequod as the polis: a mixed crew under a king whose obsession destroys what the crew was for",
        ],
        "comparative_threads": [
            "King Lear (lit-work-013) and Macbeth (lit-work-012): Ahab as the Shakespearean tragic inheritance Melville is consciously working with",
            "Paradise Lost (lit-work-017): Ahab in the Satanic inheritance; Melville read Milton closely",
            "The Bible: Job (the epilogue's quotation), Jonah (the sermon early in the novel), the white robes of Revelation",
            "Later inheritors: Faulkner; Pynchon's Mason & Dixon; the long American tradition of the encyclopedic novel",
        ],
        "seminar_questions": [
            "What does the whale mean? Where does the novel refuse to say, and how does the doubloon chapter stage the refusal?",
            "Why does the novel abandon Ishmael for chapters at a time, and what does the hybrid form let the novel do?",
            "How does Ahab read against Lear and against Macbeth? What does Melville do to the Shakespearean inheritance?",
        ],
        "writing_invitations": [
            "The analytical paragraph on the doubloon chapter, naming what the novel argues by staging multiple readings of the same figure",
            "The essay on the hybrid form as the novel's argument",
            "The sustained essay on Ahab in the Shakespearean and Miltonic inheritance, with passages from the play and the poem held in productive tension",
        ],
        "context": (
            "Composed in Pittsfield, Massachusetts, while Melville was reading "
            "Shakespeare closely; dedicated to Nathaniel Hawthorne; commercially "
            "unsuccessful in Melville's lifetime; recovered as a foundational "
            "American novel in the twentieth century; supplied as fact, "
            "interpretation left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The hybrid American epic that absorbs Shakespeare and the Bible into a nineteenth-century whaler; the seminar text on what the novel form can hold.",
                "memory_work": {
                    "recitations": ["Recitation of the opening paragraph"],
                },
                "recitation_routine": "Seminar opens from the recited opening; the discussion takes its first question from the choice of self-naming and what the imperative 'Call me Ishmael' does.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of Moby-Dick (the Norton Critical edition with its full apparatus is the standard) read aloud across two terms, with the Cetology chapters and dramatic chapters voiced as the novel asks",
                ],
                "short_lesson_flow": "A living book read aloud across the 135 chapters and narrated; the Cetology chapters and dramatic interludes treated as part of the work; deepening to analysis of the doubloon chapter and the hybrid form as the bands move up.",
                "narration_prompt": "Tell back the chapter we read today, and tell me what mode the chapter was in, and what the novel let that mode do.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of Moby-Dick on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in whales, in obsession, in the encyclopedic novel, or in Shakespeare's nineteenth-century inheritors leads",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; do not paper over the Cetology chapters; let them be themselves; honor what the whale will not settle into.",
                "observation_documentation": "Over time, notice whether the student returns to the novel and brings its hybrid form into other reading. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of the hybrid form, the Shakespearean inheritance, and the doubloon chapter where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-025": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Crime and Punishment",
            "author": "Fyodor Dostoevsky",
            "date": "serialized 1866",
            "genre": "Russian psychological novel",
            "form": "third-person novel with close access to Raskolnikov's interior; polyphonic crowd of characters each with their own claim; six parts and an epilogue",
        },
        "minimum_band": "advanced",
        "content_notes": (
            "The double murder of the pawnbroker Alyona Ivanovna and her "
            "sister Lizaveta described in close detail; sustained access to "
            "Raskolnikov's feverish psychological deterioration; the suffering "
            "of the Marmeladov family and Sonya's situation; suicide; the "
            "novel does not stand outside what it shows. Honest information, "
            "not a gate."
        ),
        "craft_focus": [
            "Close third-person psychological narration: the technique that gives the reader Raskolnikov's interior without making him the first-person narrator (lit-craft-008)",
            "Polyphonic novel: many characters each with a sustained claim, the novel refusing to make any one of them authoritative (lit-craft-014 at advanced)",
            "Raskolnikov as the inherited extraordinary-man / Napoleon type set against itself by what he does (lit-craft-014)",
            "Theme advanced: what the novel argues about the extraordinary-man theory and what it refuses to settle about Raskolnikov's late conversion (lit-craft-023)",
            "Raskolnikov's self-justifying interior monologue as a near-relation of the unreliable narrator (lit-craft-031)",
        ],
        "entry": (
            "Advanced: read the novel whole and follow the close third-person "
            "psychological narration through Raskolnikov's deterioration; "
            "argue what the novel does to the extraordinary-man theory by "
            "letting Raskolnikov act on it; hold the polyphonic crowd of "
            "characters (Sonya, Razumikhin, Porfiry, Marmeladov, Svidrigailov, "
            "Dunya) each with their own claim; honor what the novel refuses "
            "to settle about Raskolnikov's late conversion in the epilogue. "
            "Mastery: original argument about Dostoevsky's place in the "
            "formation of psychological narration and the polyphonic novel."
        ),
        "close_reading_passages": [
            "Raskolnikov's first decision and the murder (Part 1): how does the novel stage the act, and what does the close third-person access do to the reader's complicity?",
            "Raskolnikov's exchanges with Porfiry (Parts 3-4): how does the novel stage an investigator who knows what the reader knows and is not yet ready to act, and what does the staging do to the question of confession?",
            "The epilogue and Raskolnikov's late turn: how does the novel stage what some readers receive as conversion and others as the novel imposing what its argument did not earn?",
        ],
        "structural_analysis": (
            "Six parts and an epilogue; the crime in Part 1, the long "
            "psychological aftermath across the middle, the confession at the "
            "end of Part 6, the epilogue's reframing. The close third-person "
            "narration holds the reader inside Raskolnikov's mind without "
            "making him the first-person narrator; the polyphonic crowd of "
            "other characters each carries a sustained claim the novel refuses "
            "to flatten. The structure is the work's argument: a psychology so "
            "thoroughly entered cannot stand outside itself; the late "
            "conversion is the question, not the answer."
        ),
        "thematic_lines": [
            "The extraordinary-man theory: the novel does not argue against it abstractly; it lets Raskolnikov act on it and watches",
            "Suffering and the possibility of return: Sonya's claim and what the novel does and does not let Raskolnikov hear",
            "The polyphonic crowd: each major character carries a claim the novel takes seriously; the novel refuses to make any of them authoritative",
        ],
        "comparative_threads": [
            "Macbeth (lit-work-012): the Shakespearean predecessor of the protagonist after the deed",
            "Hamlet (lit-work-011): the inherited figure of the man who cannot act, set against Raskolnikov who can",
            "The Brothers Karamazov (Dostoevsky's later novel): the polyphonic form developed further; not in this batch",
            "War and Peace (lit-work-026, next in this batch): Tolstoy and Dostoevsky as the two great nineteenth-century Russian novelists who used the form very differently",
        ],
        "seminar_questions": [
            "What does the novel argue about the extraordinary-man theory by letting Raskolnikov act on it?",
            "Is the epilogue's conversion earned by the novel, imposed by the novel, or held by the novel as a question? Where does the novel refuse to say?",
            "What does the close third-person psychological narration do that no first-person could?",
        ],
        "writing_invitations": [
            "The analytical paragraph on Raskolnikov's interior monologue before the murder, naming what the close third-person access does to the reader",
            "The essay on the polyphonic crowd, holding Sonya's, Porfiry's, and Svidrigailov's claims in productive tension",
            "The sustained essay on what the novel refuses to settle about the late conversion",
        ],
        "context": (
            "Serialized in 'The Russian Messenger' across 1866; composed while "
            "Dostoevsky was in serious debt and under contract for two novels "
            "at once; the first of the four great late novels; supplied as "
            "fact, interpretation left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The foundational psychological novel of the nineteenth century; the seminar text on what the novel can do with interior access.",
                "memory_work": {
                    "recitations": [
                        "Recitation of a passage of Raskolnikov's interior monologue in a worthy modern translation"
                    ],
                },
                "recitation_routine": "Seminar opens from the recited passage; the discussion takes its first question from what Raskolnikov is reasoning toward and where the reasoning fails.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy translation of Crime and Punishment (Pevear and Volokhonsky; Garnett's older version; Oliver Ready's recent translation) read aloud across a term",
                ],
                "short_lesson_flow": "A living book read aloud across the six parts and the epilogue, narrated; the psychological narration noticed for what it does; deepening to analysis of the polyphonic crowd and the epilogue as the bands move up.",
                "narration_prompt": "Tell back the chapter we read today, and tell me what Raskolnikov was reasoning toward, and where the reasoning broke.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy translation of Crime and Punishment on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in psychology, in ideas tested by action, or in nineteenth-century Russian fiction leads",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; let the polyphonic crowd be polyphonic; do not collapse Sonya into the novel's answer.",
                "observation_documentation": "Over time, notice whether the student returns to the novel and brings the polyphonic form into other reading. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of close third-person psychological narration and the polyphonic novel where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-026": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "War and Peace",
            "author": "Leo Tolstoy",
            "date": "serialized 1865-1867; book publication 1869",
            "genre": "Russian novel of nation and family across war and peace",
            "form": "four books and two epilogues; omniscient third-person with sustained essayistic interludes; hundreds of named characters across noble households and historical figures",
        },
        "minimum_band": "advanced",
        "content_notes": (
            "The Napoleonic invasions of Russia in detail, including the "
            "battles of Schöngraben, Austerlitz, and Borodino; the burning of "
            "Moscow; the deaths of major characters across the long span; "
            "Tolstoy's essayistic polemic against the historians' theory of "
            "great men; Pierre's captivity; the novel does not gentle its "
            "violence or its losses. Honest information, not a gate."
        ),
        "craft_focus": [
            "Omniscient narration with sustained essayistic interludes: the novel includes essays on the philosophy of history that are part of the work (lit-craft-008)",
            "Character advanced: dozens of characters held with sustained interiority across hundreds of pages; what the form does that no shorter novel could (lit-craft-014)",
            "Theme advanced: Tolstoy's argument against the great-man theory of history; what the novel refuses to settle about who or what makes history (lit-craft-023)",
            "Figurative networks across the long span: the oak that buds again, the Moscow that burns, the ice that breaks (lit-craft-042 at proficient; lit-craft-043 at advanced)",
        ],
        "entry": (
            "Advanced: read the novel whole across its long span (most "
            "students will take a year or more); follow the major characters "
            "(Andrei, Pierre, Natasha, Marya, the Rostovs, the Bolkonskys) "
            "across the four books; meet the essayistic interludes as part of "
            "the work rather than as digressions; argue what Tolstoy refuses "
            "about the great-man theory and what the second epilogue does "
            "that the narrative could not. Mastery: original argument about "
            "the novel's place in the form's long history and what the "
            "essayistic intrusion does to the novel as a form."
        ),
        "close_reading_passages": [
            "Andrei at Austerlitz looking up at the sky (Book 3 in most editions): how does the novel stage a moment that recurs in Andrei's interior across the rest of the novel?",
            "Natasha at the ball (Book 6 in most editions): how does the novel stage a young woman's first experience of the social world that the novel is otherwise weighing skeptically?",
            "Pierre in captivity with Platon Karataev: how does the novel stage a peasant figure whose claim on the novel's philosophy is hard to read either as endorsed or as refused?",
        ],
        "structural_analysis": (
            "Four books and two epilogues, the second epilogue an essay on "
            "the philosophy of history that is part of the work. The novel "
            "moves between two great noble households (the Rostovs and the "
            "Bolkonskys) and the historical events that engulf them; the "
            "omniscient narrator alternates close access to many characters "
            "with sustained essayistic polemic against the historians. The "
            "structure is the work's argument: history is not made by Napoleon; "
            "history is made by the millions of acts the historians cannot "
            "see, and only the form that holds both the lives and the "
            "essayistic polemic can argue this."
        ),
        "thematic_lines": [
            "The great-man theory of history and Tolstoy's argument against it: not abstract, but tested across the novel's long span",
            "War and peace as the two states the novel holds together: each is what the other makes visible",
            "Marriage, family, and household across generations: the lives the historians cannot see and the novel can",
        ],
        "comparative_threads": [
            "Crime and Punishment (lit-work-025): the contemporary Russian novelist using the form very differently",
            "The Iliad (lit-work-002): the older epic of war that Tolstoy was widely read alongside; the comparison was already established in nineteenth-century criticism",
            "The Aeneid (lit-work-003): the older epic of nation-founding the novel quietly engages",
            "Later inheritors: Vasily Grossman's Life and Fate as the twentieth-century Russian successor",
        ],
        "seminar_questions": [
            "What does the novel refuse about the great-man theory of history, and how does the second epilogue argue what the narrative has been arguing?",
            "What does the omniscient narrator with essayistic interludes let the novel do that no other form could?",
            "What does the novel let Platon Karataev claim, and where does it refuse to either endorse or refuse the claim?",
        ],
        "writing_invitations": [
            "The analytical paragraph on a single battle scene, naming what the novel does with the historical event and what it does with the personal one",
            "The essay on the novel's argument against the great-man theory, holding two or three essayistic interludes alongside the narrative moments they comment on",
            "The sustained essay on the second epilogue as part of the work",
        ],
        "context": (
            "Serialized in 'The Russian Messenger' across 1865-1867 and "
            "published in book form in 1869; composed over six years; "
            "Tolstoy's first long novel and one of the longest novels in the "
            "Western canon; supplied as fact, interpretation left to the "
            "student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The longest of the great nineteenth-century novels; the seminar text on the form when stretched to hold history, philosophy, and a multitude of lives.",
                "memory_work": {
                    "recitations": ["Recitation of Andrei's sky passage at Austerlitz in a worthy modern translation"],
                },
                "recitation_routine": "Seminar opens from the recited passage; the discussion takes its first question from what Andrei sees and what the rest of the novel does with it.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy translation of War and Peace (Pevear and Volokhonsky; Briggs; Maude's older version) read aloud across a year, in long chunks",
                ],
                "short_lesson_flow": "A living book read aloud across the four books and the epilogues, narrated; the major characters followed across the long span; deepening to analysis of the essayistic interludes as the bands move up.",
                "narration_prompt": "Tell back the chapter we read today, and tell me which character was being given to us, and what the narrator quietly let us see about them.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy translation of War and Peace on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in nineteenth-century Russia, in the Napoleonic wars, in the long novel, or in the philosophy of history leads",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; the year-long reading is the practice; let the essayistic interludes be themselves.",
                "observation_documentation": "Over time, notice whether the student returns to particular characters across the year and brings the essayistic interludes into other reading. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of the omniscient narrator with essayistic intrusion and the form of the long novel where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-027": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Adventures of Huckleberry Finn",
            "author": "Mark Twain (Samuel Clemens)",
            "date": "first published in the United Kingdom 1884; in the United States 1885",
            "genre": "American picaresque novel",
            "form": "first-person novel in Huck's sustained vernacular voice; episodic journey down the Mississippi River",
        },
        "minimum_band": "proficient",
        "content_notes": (
            "Sustained use of nineteenth-century vernacular including the "
            "racial slur 'nigger' throughout, in Huck's voice and in the "
            "voices of other speakers; depictions of slavery, racial violence, "
            "and the institution of slave-catching; the long-standing debate "
            "about whether the novel exhibits the racism of its setting or "
            "endorses it has not been settled and the novel is taught with "
            "that debate in the room. The Phelps farm closing chapters, in "
            "which Tom Sawyer's romance-driven games extend Jim's captivity, "
            "are themselves the subject of long-standing criticism by readers "
            "including Ernest Hemingway and Toni Morrison. Honest information, "
            "not a gate."
        ),
        "craft_focus": [
            "First-person vernacular voice sustained across a whole novel: Huck's voice is the novel's instrument and its limitation (lit-craft-008)",
            "Huck as a narrator who tells the truth about what he sees and what he does not yet understand the moral weight of (lit-craft-031 in the family of moves)",
            "Character proficient: Huck and Jim; what the friendship is and what the novel refuses to settle about it (lit-craft-013)",
            "The river as the work's figurative through-line: the raft as the only place the rules of the shore do not reach (lit-craft-042)",
            "Theme proficient and advanced: conscience and law in the Mississippi valley; what the novel does that no didactic novel could (lit-craft-022, lit-craft-023)",
        ],
        "entry": (
            "Proficient: read the novel whole in Huck's sustained voice; "
            "follow the river as the work's figurative through-line; meet "
            "the moment when Huck decides he will 'go to hell' rather than "
            "betray Jim and weigh what the novel argues by giving Huck that "
            "decision in a voice that does not understand its own moral "
            "weight. Advanced: hold the Phelps-farm closing chapters as part "
            "of the work the reader is asked to weigh; argue what the novel "
            "does that no third-person narration could and where the novel's "
            "use of its setting's racism does and does not align with the "
            "novel's argument; meet the long debate about the closing as "
            "part of reading the novel honestly. Mastery: original argument "
            "about the novel's place in the formation of American vernacular "
            "fiction and in the long debate the novel has provoked."
        ),
        "close_reading_passages": [
            "The opening of the novel and Huck's reference back to Tom Sawyer: how does the novel stage its narrator, and what does the first-paragraph claim about Mr. Mark Twain do?",
            "The decision on the raft where Huck tears up the letter and says he will 'go to hell' rather than turn Jim in: how does the novel stage a moral choice in a voice that misnames itself, and what does the novel argue by giving Huck that decision?",
            "The Phelps-farm chapters at the close: how does the novel stage Tom Sawyer's romance-driven games extending Jim's captivity, and what does the novel argue by ending where it does?",
        ],
        "structural_analysis": (
            "An episodic journey down the Mississippi, the raft alternating "
            "with shore episodes that the novel uses to weigh the world the "
            "raft has briefly escaped. The first-person vernacular voice is "
            "sustained throughout; the novel's structural argument is the "
            "alternation between river and shore, and the closing chapters "
            "either complete the argument or strain it, depending on the "
            "reader."
        ),
        "thematic_lines": [
            "Conscience versus law in a society whose law has institutionalized slavery: Huck's decision and what the novel argues by it",
            "The friendship of Huck and Jim and what the novel refuses to settle about whether it survives the closing",
            "American vernacular as the novel's instrument: what the form does that earlier American novels could not",
        ],
        "comparative_threads": [
            "Don Quixote (lit-work-016): the picaresque ancestor; the journey with a companion that tests the world",
            "Defoe's Robinson Crusoe and the captivity-narrative tradition; what Twain inherits and refuses",
            "Hemingway's claim that 'all modern American literature comes from one book by Mark Twain'; the long American debt to the vernacular voice",
            "Toni Morrison's introduction to a worthy edition; the long debate about the novel's treatment of Jim and the closing as part of reading the novel honestly",
        ],
        "seminar_questions": [
            "What does the novel argue by giving Huck the 'go to hell' decision in a voice that misnames itself?",
            "Where in the novel does the vernacular voice know what Huck does not?",
            "Does the Phelps-farm closing complete the novel's argument or strain it? What does the long debate let you see?",
        ],
        "writing_invitations": [
            "The analytical paragraph on the 'go to hell' decision, naming what the staging does that no third-person narration could",
            "The essay on the river as the work's figurative through-line",
            "The sustained essay on the closing chapters and the long debate about them, with passages from the novel and references to its critics",
        ],
        "context": (
            "Composed across the 1870s and 1880s; the long-promised sequel to "
            "The Adventures of Tom Sawyer; the central American novel of the "
            "Mississippi valley and the first to make a vernacular voice the "
            "novel's instrument across a whole work; supplied as fact, "
            "interpretation left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The central American novel of the Mississippi valley; the seminar text on the vernacular voice and the moral decision made in a voice that misnames itself.",
                "memory_work": {
                    "recitations": ["Recitation of the 'go to hell' passage on the raft"],
                },
                "recitation_routine": "Seminar opens from the recited passage; the discussion takes its first question from what Huck says and what Huck does not yet know he is saying.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of Adventures of Huckleberry Finn (the Norton Critical edition, which includes the long debate; the Library of America) read aloud across a term, with the vernacular voice heard in its full register",
                ],
                "short_lesson_flow": "A living book read aloud across the river journey and narrated; the alternation between raft and shore noticed; deepening to analysis of the closing chapters and the debate about them as the bands move up.",
                "narration_prompt": "Tell back the chapter we read today, and tell me what Huck thought he was doing and what the novel quietly let you see.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of Adventures of Huckleberry Finn on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in the Mississippi, in friendship, in the vernacular, or in the long debate about American literature and race leads",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; do not paper over the vernacular's racial language or the closing's strain; let the debate be the debate.",
                "observation_documentation": "Over time, notice whether the student returns to the novel and begins to ask their own questions about the closing. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of vernacular first-person narration and the long debate about the novel's closing where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-028": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Heart of Darkness",
            "author": "Joseph Conrad",
            "date": "first serialized in Blackwood's Magazine 1899; published in 'Youth: a Narrative, and Two Other Stories' 1902",
            "genre": "late-Victorian / early-modernist novella",
            "form": "double-framed: an unnamed outer narrator records Marlow's oral account aboard the yawl Nellie; Marlow's account is the central narrative",
        },
        "minimum_band": "advanced",
        "content_notes": (
            "Sustained depiction of the Belgian Congo under King Leopold II's "
            "regime, including the chain gang, the grove of death, the "
            "language Marlow uses about Africans, and the violence done in "
            "the name of ivory; period imperial racism in Marlow's account "
            "and in the novella's broader frame. Chinua Achebe's 1975 essay "
            "'An Image of Africa: Racism in Conrad's Heart of Darkness' is "
            "part of how the novella is read; the long argument it began has "
            "not been settled and is part of reading the novella honestly. "
            "Honest information, not a gate."
        ),
        "craft_focus": [
            "Double-framed narration: the outer narrator (recording Marlow) and Marlow's oral account aboard the Nellie (lit-craft-008)",
            "Marlow as unreliable: what he claims, what he refuses to claim, what the novella lets the reader see past him (lit-craft-031)",
            "Figurative system: darkness and light; the river as descent in the inheritance from Aeneid 6 and Inferno; the inverted moral compass (lit-craft-043)",
            "Theme advanced: what the novella refuses to settle about imperialism, about Kurtz, about what the journey discovers; the Achebe debate as part of the work (lit-craft-023)",
        ],
        "entry": (
            "Advanced: read the novella whole, taking the double frame "
            "seriously: an outer narrator records Marlow's oral telling, and "
            "Marlow himself is one of the listeners' company; meet the "
            "figurative system of darkness and light as the novella's "
            "argument and as the place where readers have most disagreed; "
            "read Achebe's essay alongside the novella as part of reading it "
            "honestly; argue what the novella refuses to settle about Kurtz, "
            "about Marlow, and about itself. Mastery: original argument "
            "about the novella's place in the long inheritance from epic "
            "descent forward into modernism, and about what Achebe's reading "
            "has done to the work."
        ),
        "close_reading_passages": [
            "The opening on the Nellie at the Thames mouth: how does the novella stage the outer frame, and what does the outer narrator's reference to 'one of the dark places of the earth' do to the frame?",
            "Marlow's account of the grove of death (near the Outer Station): how does the novella stage the colony's reality, and what does Marlow's voice claim and refuse to claim?",
            "Kurtz's last words ('The horror! The horror!') and Marlow's lie to the Intended: how does the novella stage two endings, and what does each let the work refuse to settle?",
        ],
        "structural_analysis": (
            "Two frames: the outer narrator on the Nellie at the Thames mouth, "
            "and Marlow's oral telling that occupies most of the novella. "
            "The river is the journey, the figurative system is darkness "
            "against light, the moral compass is inverted (the colony is "
            "called civilizing and is shown to be its opposite); the closing "
            "lie to the Intended frames the whole. The structure is the "
            "work's argument: a story told to listeners in the dusk, every "
            "claim filtered through Marlow, no authoritative voice."
        ),
        "thematic_lines": [
            "Imperialism and what the novella claims about it: the long debate the novella has provoked is part of reading it",
            "Kurtz as the limit case the novella refuses to categorize",
            "What darkness means in the novella, and what Achebe's reading does to the figurative system",
        ],
        "comparative_threads": [
            "The Aeneid (lit-work-003) and Inferno (lit-work-010): the descent figure the novella inherits and bends to colonial imagery",
            "Achebe's 'An Image of Africa: Racism in Conrad's Heart of Darkness' (1975) as the essay that has been part of how the novella is read for fifty years",
            "Apocalypse Now (Coppola, 1979) as the most direct cinematic inheritor; how the film reads the novella against the Vietnam War",
            "Later postcolonial fiction that argues with the novella (Tayeb Salih's Season of Migration to the North; Caryl Phillips's writing on Conrad)",
        ],
        "seminar_questions": [
            "What does the double frame do that no single voice could?",
            "What does the novella refuse to settle about Kurtz, and where does Marlow refuse to say what he saw?",
            "What does Achebe's reading let you see about the novella's figurative system, and what does the novella refuse to grant Achebe's reading?",
        ],
        "writing_invitations": [
            "The analytical paragraph on the closing lie to the Intended, naming what the novella argues by making the lie Marlow's final act",
            "The essay on the figurative system of darkness and light, holding Achebe's reading in productive tension with the novella's claims",
            "The sustained essay on the descent inheritance from epic into the novella's colonial frame",
        ],
        "context": (
            "Composed in 1899 after Conrad's own months on the Congo in 1890; "
            "serialized in Blackwood's Magazine and collected in 1902; the "
            "central English-language novella of late-imperial fiction and "
            "early modernism; supplied as fact, interpretation left to the "
            "student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The central late-Victorian and early-modernist novella; the seminar text on double-framed narration and on what the novella's figurative system claims.",
                "memory_work": {
                    "recitations": ["Recitation of the opening on the Nellie or the closing lie to the Intended"],
                },
                "recitation_routine": "Seminar opens from the recited passage; the discussion takes its first question from where the outer narrator stands and what the frame lets Marlow do.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of Heart of Darkness (the Norton Critical edition with Achebe's essay; the Penguin) read aloud across a few weeks, with Marlow's voice held distinct from the outer narrator's",
                ],
                "short_lesson_flow": "A living book read aloud and narrated; the double frame held; Achebe's essay brought into the room when the novella's figurative system raises it; deepening to analysis of the closing as the bands move up.",
                "narration_prompt": "Tell back the passage we read today, and tell me what Marlow said and what the novella let you see past him.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of Heart of Darkness on the shelf, available, never assigned, and Achebe's essay alongside",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in modernism, in empire, in the long descent figure, or in the long Achebe debate leads",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; let Achebe's reading into the room; let the question stay unsettled.",
                "observation_documentation": "Over time, notice whether the student returns to the novella and reads Marlow with the suspicion the novella's frame invites. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of double-framed narration and the Achebe debate where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-029": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Dubliners",
            "author": "James Joyce",
            "date": "first published 1914",
            "genre": "early-modernist short-story collection",
            "form": "fifteen stories ordered by life stage (childhood, adolescence, maturity, public life) and culminating in 'The Dead'",
        },
        "minimum_band": "proficient",
        "content_notes": (
            "Period attitudes throughout the stories; the death of a priest "
            "in 'The Sisters'; the priest-figure in 'An Encounter'; the failure "
            "and humiliation across the maturity stories; the long quiet "
            "devastation of 'The Dead'; the stories are not consoling and "
            "the collection refuses to redeem the paralysis it names. Honest "
            "information, not a gate."
        ),
        "craft_focus": [
            "Free indirect discourse adjusted story by story to the consciousness at the center of each: a child's lexicon in the early stories, an adult's in the later (lit-craft-008)",
            "The epiphany as the work's central technique: a sudden small revelation against which the rest of the story is read (lit-craft-022, lit-craft-023)",
            "Character proficient: each story's center constructed precisely (lit-craft-013)",
            "Dublin as the work's figurative through-line: the same city across fifteen stories, returning streets, repeated phrases, recurring objects (lit-craft-042)",
            "The arrangement of the stories by life stage as the collection's structural argument (lit-craft-022)",
        ],
        "entry": (
            "Proficient: read the collection whole in its ordering; follow "
            "free indirect discourse as it adjusts story by story to each "
            "center; meet the epiphany as the collection's central technique "
            "and notice that what each story shows is sometimes what its "
            "center cannot yet see; meet 'The Dead' as the collection's "
            "culminating story. Advanced: argue the collection as an "
            "argument about paralysis and what fiction can do in its "
            "presence; set Joyce's free indirect discourse against Austen's "
            "and Flaubert's; meet 'The Dead' as the story that completes the "
            "collection's argument. Mastery: original argument about "
            "Dubliners as the formation of the modernist short story."
        ),
        "close_reading_passages": [
            "'The Sisters' opening: how does the collection begin with a child's lexicon and the death of a priest, and what does the staging do to set up the rest of the collection?",
            "'Araby' and the boy's late realization in the bazaar: how does the story stage an epiphany the boy cannot yet articulate, and what does the free indirect discourse do that direct statement could not?",
            "'The Dead' and the final paragraphs: how does the story stage Gabriel's late seeing, and what does the snow falling general all over Ireland do to the close of the collection?",
        ],
        "structural_analysis": (
            "Fifteen stories in four life-stages (childhood, adolescence, "
            "maturity, public life) plus the culminating 'The Dead'. Free "
            "indirect discourse adjusts story by story; the city of Dublin "
            "is the same across them, with returning streets and repeated "
            "phrases; the epiphany sits at or near the end of most stories "
            "and is often what the center of the story cannot yet articulate. "
            "The structure is the collection's argument: paralysis named "
            "across a life span, the city itself the figure, and 'The Dead' "
            "the story that holds them all together."
        ),
        "thematic_lines": [
            "Paralysis: Joyce's own named subject for the collection; what it means to be paralyzed in a city that does not name it",
            "Epiphany: the small revelation against which the rest of the story is read; what the form does that no longer story could",
            "'The Dead' as the collection's culmination: a long quiet devastation that holds the whole collection together",
        ],
        "comparative_threads": [
            "Pride and Prejudice (lit-work-019): the previous English novel of free indirect discourse Joyce is consciously inheriting from",
            "Flaubert's Madame Bovary and his short stories: the continental free-indirect-discourse master Joyce was reading",
            "Chekhov's short stories: the named master of the modern short story Joyce was reading; the form Joyce is doing something specific to",
            "Hemingway's In Our Time and the long Anglophone short-story tradition Joyce sets in motion",
        ],
        "seminar_questions": [
            "Where in each story does free indirect discourse let the story know more than its center does?",
            "What does the epiphany in each story do that direct statement could not?",
            "What does 'The Dead' complete that the earlier stories had only named?",
        ],
        "writing_invitations": [
            "The analytical paragraph on the epiphany in a chosen story, naming what the story knows and what its center cannot yet see",
            "The essay on the city of Dublin as the collection's figurative through-line",
            "The sustained essay on 'The Dead' as the story that holds the collection together",
        ],
        "context": (
            "Composed across 1904-07; long delayed in publication by printer "
            "and publisher objections to material in particular stories; "
            "published in 1914; the foundational English-language modernist "
            "short-story collection; supplied as fact, interpretation left "
            "to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The foundational modernist short-story collection; the seminar text on free indirect discourse and the epiphany.",
                "memory_work": {
                    "recitations": ["Recitation of the final paragraph of 'The Dead' ('His soul swooned slowly...')"],
                },
                "recitation_routine": "Seminar opens from the recited final paragraph; the discussion takes its first question from how the close holds the whole collection together.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of Dubliners (the Norton; the Penguin) read aloud across a term, one story per sitting, with 'The Dead' read whole across two sittings",
                ],
                "short_lesson_flow": "A living book read aloud across the fifteen stories and narrated; the epiphany noticed; the city of Dublin tracked across stories; deepening to analysis of 'The Dead' as the bands move up.",
                "narration_prompt": "Tell back the story we read today, and tell me where the moment came that changed how you read the rest, and what the center of the story did with it.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of Dubliners on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in the short story, in Joyce, in Dublin, or in early modernism leads",
                ],
                "parent_role": "Read aloud one story at a sitting; let 'The Dead' be 'The Dead'; do not rush across stories.",
                "observation_documentation": "Over time, notice whether the student returns to particular stories and begins to feel the epiphany as the form's central technique. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of free indirect discourse adjusted to consciousness and the epiphany as a short-story technique where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-030": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Mrs Dalloway",
            "author": "Virginia Woolf",
            "date": "first published 1925",
            "genre": "high-modernist novel",
            "form": "third-person free indirect discourse moving between consciousnesses across a single June day in 1923 London; unbroken in narrative time; sustained 'tunnels' connecting characters who never meet",
        },
        "minimum_band": "advanced",
        "content_notes": (
            "Septimus Warren Smith's shell shock from the First World War and "
            "his suicide; Clarissa's reflection on Septimus's death at her "
            "evening party; the period treatment of mental illness "
            "(Bradshaw's regime of 'proportion') which the novel weighs "
            "skeptically; period attitudes throughout; the novel does not "
            "redeem what it shows. Honest information, not a gate."
        ),
        "craft_focus": [
            "Free indirect discourse moving between consciousnesses without break: the novel's central technical achievement (lit-craft-008 strained to its limit)",
            "Clarissa and Septimus as paired characters who never meet: the novel's structural argument across two unrelated lives (lit-craft-014)",
            "Theme advanced: what the novel does with one day's London after the war; what it refuses to settle about Clarissa, about Septimus, about what the party is for (lit-craft-023)",
            "Figurative networks: Big Ben's strokes against the time of the consciousnesses, flowers, the airplane writing in smoke, the old woman across the way (lit-craft-042 at proficient; lit-craft-043 at advanced)",
        ],
        "entry": (
            "Advanced: read the novel whole in its single-day form; follow "
            "the free indirect discourse as it moves between consciousnesses "
            "without break (the famous 'tunnels' Woolf described in her "
            "diary); meet Septimus and Clarissa as paired across a novel "
            "where they never meet; argue what the novel does with the day "
            "after the war and what it refuses to settle. Mastery: original "
            "argument about the novel's place in modernist fiction and what "
            "it does to free indirect discourse that Austen and Flaubert did "
            "not."
        ),
        "close_reading_passages": [
            "The opening ('Mrs Dalloway said she would buy the flowers herself'): how does the novel open in Clarissa's voice without quotation, and what does the free indirect discourse do in the first paragraphs?",
            "The airplane writing in smoke (early in the novel): how does the novel use a single object in the sky to move between multiple consciousnesses below it, and what does the technique do?",
            "Clarissa learning of Septimus's death at her party (near the close): how does the novel stage a connection between two characters who have never met, and what does Clarissa do with what she hears?",
        ],
        "structural_analysis": (
            "A single day in June 1923 in London, unbroken in narrative time, "
            "with free indirect discourse moving between consciousnesses "
            "through what Woolf called 'tunnels' connecting characters who "
            "do not all meet. Big Ben's strokes give the day its public "
            "rhythm; the consciousnesses give it their private times. "
            "Clarissa's party at the close gathers the day; Septimus's "
            "suicide enters the party as news Clarissa is told. The "
            "structure is the work's argument: a city, a day, and the "
            "tunnels of consciousness underneath both."
        ),
        "thematic_lines": [
            "What the day after the war holds: the public time of Big Ben against the private times of the consciousnesses",
            "Septimus and Clarissa: paired across the novel; what the novel argues by connecting them without making them meet",
            "Sir William Bradshaw and his regime of 'proportion': the novel's skeptical weighing of the institutional response to suffering",
        ],
        "comparative_threads": [
            "Dubliners (lit-work-029): Joyce's earlier modernist free indirect discourse; what Woolf has done with the technique that Joyce did not",
            "Pride and Prejudice (lit-work-019): Austen as Woolf's named English ancestor in free indirect discourse",
            "Joyce's Ulysses (1922): the same single-day form attempted in the same decade; Woolf read it and her response was complicated",
            "Later inheritors: Michael Cunningham's The Hours (1998) as the most direct fictional engagement; the long line of modernist consciousness-novels Woolf shapes",
        ],
        "seminar_questions": [
            "How does the free indirect discourse move between consciousnesses, and where does Woolf's technique go beyond Austen's or Joyce's?",
            "What does the novel do by connecting Septimus and Clarissa without making them meet?",
            "What does Clarissa do with the news of Septimus's death, and what does the novel refuse to say about her response?",
        ],
        "writing_invitations": [
            "The analytical paragraph on the opening sentence and the first paragraphs, naming what the free indirect discourse does that direct narration could not",
            "The essay on the airplane sequence as the novel's instruction in its own technique",
            "The sustained essay on Septimus and Clarissa as paired characters and what the novel argues by connecting them",
        ],
        "context": (
            "Composed in 1923-24 and published in 1925; one of Woolf's two "
            "great novels of the mid-1920s (To the Lighthouse follows in "
            "1927); central to high modernism in English; supplied as fact, "
            "interpretation left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The high-modernist novel of consciousness in a single day; the seminar text on what free indirect discourse can do when it moves between minds.",
                "memory_work": {
                    "recitations": ["Recitation of the opening sentence and the first paragraph"],
                },
                "recitation_routine": "Seminar opens from the recited opening; the discussion takes its first question from where Clarissa's voice ends and the narrator's begins, and whether the question is the right one.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of Mrs Dalloway (the Harcourt; the Penguin Modern Classics) read aloud across a few weeks",
                ],
                "short_lesson_flow": "A living book read aloud across the single day and narrated; the tunnels of consciousness noticed as they connect; deepening to analysis of the Septimus / Clarissa pairing as the bands move up.",
                "narration_prompt": "Tell back the passage we read today, and tell me whose consciousness we were inside, and whose we moved into.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of Mrs Dalloway on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in modernism, in London, in the aftermath of the First World War, or in consciousness-novels leads",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; let the tunnels be tunnels; do not collapse Septimus into Clarissa or Clarissa into Woolf.",
                "observation_documentation": "Over time, notice whether the student returns to particular passages and begins to feel the free indirect discourse as the novel's central instrument. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of free indirect discourse moving between consciousnesses and the single-day modernist novel where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-031": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "date": "first published 1925",
            "genre": "modernist American novel",
            "form": "first-person narration by Nick Carraway, a participant in the events he tells; short novel in nine chapters with a brief epilogue",
        },
        "minimum_band": "proficient",
        "content_notes": (
            "Period attitudes throughout, including Tom Buchanan's open "
            "racism and antisemitism (notably toward Meyer Wolfsheim); the "
            "death of Myrtle Wilson under Daisy's driving and the killing of "
            "Gatsby by George Wilson; the novel does not stand outside Tom's "
            "speech but does not endorse it either. Honest information, not "
            "a gate."
        ),
        "craft_focus": [
            "First-person participant-observer narration: Nick as both teller and figure in the story (lit-craft-008)",
            "Unreliable narration in a quieter form: Nick's claim to honesty and the ways his honesty is interested (lit-craft-031)",
            "Character proficient: Gatsby as the work's argument, glimpsed by everyone else; Daisy, Tom, Jordan as constructed positions (lit-craft-013)",
            "Figurative system: the green light at the end of Daisy's dock; the eyes of Doctor T. J. Eckleburg; the valley of ashes (lit-craft-042 at proficient; lit-craft-043 at advanced)",
            "Theme proficient: the long pursuit and what is pursued; the famous closing image of the boats against the current (lit-craft-022)",
        ],
        "entry": (
            "Proficient: read the novel whole in Nick's voice; follow the "
            "figurative system of the green light, the valley of ashes, and "
            "Eckleburg's eyes; meet the death of Myrtle and the killing of "
            "Gatsby as the structural turns; close on the boats against the "
            "current. Advanced: argue what Nick claims about his own honesty "
            "and where the claim falters; argue what the novel does to the "
            "pursuit-novel inheritance (Conrad as Fitzgerald's named "
            "influence); honor what the novel refuses to settle about "
            "Gatsby. Mastery: original argument about the novel's place in "
            "American modernism and what it does to the figure of the long "
            "pursuit."
        ),
        "close_reading_passages": [
            "The opening on Nick's father's advice and the first sight of Gatsby reaching toward the green light (chapter 1): how does the novel stage the narrator's claim to reserve judgment and immediately give us the gesture that the novel will return to?",
            "The valley of ashes and the eyes of Doctor T. J. Eckleburg (chapter 2): how does the novel stage a figure that no character interprets correctly and that the novel refuses to fix?",
            "The closing paragraphs ('So we beat on, boats against the current'): how does the novel stage a closing that holds the whole work, and what does the present tense of the close do?",
        ],
        "structural_analysis": (
            "Nine chapters in Nick's first-person voice, the novel's central "
            "events glimpsed through him: Gatsby's parties, the reunion with "
            "Daisy, the Plaza Hotel confrontation, the deaths in the valley "
            "of ashes, the funeral. The figurative system holds the work "
            "together (green light, valley of ashes, Eckleburg's eyes); the "
            "closing paragraphs reframe the whole. The structure is the "
            "novel's argument: a long pursuit recovered after the fact by "
            "the only listener who cared to listen."
        ),
        "thematic_lines": [
            "The long pursuit and what is pursued: the novel refuses to settle whether Daisy is what Gatsby was after or whether she was the figure for something else",
            "What the green light means and what Eckleburg's eyes mean: the figures the novel refuses to fix",
            "Nick's claim to honesty and what the novel does with it",
        ],
        "comparative_threads": [
            "Heart of Darkness (lit-work-028): the participant-observer narrator Fitzgerald is consciously inheriting; Conrad as Fitzgerald's named influence",
            "Eliot's The Waste Land (1922, in this batch as lit-work-037): the contemporary modernist treatment of the valley of ashes' kind of landscape; Fitzgerald read Eliot and wrote to him about Gatsby",
            "Hemingway's The Sun Also Rises (1926) as the contemporary American novel of the same generation",
            "Toni Morrison's writing on Gatsby as part of the long American reading of the novel's race politics",
        ],
        "seminar_questions": [
            "Where does Nick's claim to honesty hold and where does it falter?",
            "What does the green light mean, and where does the novel refuse to say?",
            "Is Gatsby admirable, mourned, or both? What does the famous closing image earn?",
        ],
        "writing_invitations": [
            "The analytical paragraph on the closing paragraphs ('So we beat on'), naming what the change to first person plural and present tense does",
            "The essay on the figurative system of the green light, the ashes, and Eckleburg's eyes",
            "At advanced, the essay on Nick's reliability and where the novel lets the reader see past him",
        ],
        "context": (
            "Composed on the French Riviera and at Great Neck, Long Island, "
            "across 1923-24; published in 1925 to mixed reviews and middling "
            "sales; recovered as a foundational American novel after "
            "Fitzgerald's death; supplied as fact, interpretation left to the "
            "student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The crystalline American modernist novel of the long pursuit; the seminar text on the participant-observer narrator and on figures the novel refuses to fix.",
                "memory_work": {
                    "recitations": ["Recitation of the closing paragraphs"],
                },
                "recitation_routine": "Seminar opens from the recited closing; the discussion takes its first question from what the closing earns and what the novel refuses to settle.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of The Great Gatsby (the Scribner; the Cambridge edition) read aloud across two or three weeks",
                ],
                "short_lesson_flow": "A living book read aloud across the nine chapters and narrated; the figurative system noticed as it returns; deepening to analysis of the closing as the bands move up.",
                "narration_prompt": "Tell back the chapter we read today, and tell me what Nick said about it and what the novel let you see past him.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of The Great Gatsby on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in American modernism, in the long pursuit, or in narrators whose honesty is interested leads",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; let the figurative system stay open; do not fix the green light.",
                "observation_documentation": "Over time, notice whether the student returns to the closing and begins to feel the figurative system as the novel's instrument. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of the participant-observer narrator and the novel's figurative system where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-032": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Nineteen Eighty-Four",
            "author": "George Orwell (Eric Arthur Blair)",
            "date": "first published 1949",
            "genre": "twentieth-century dystopian novel",
            "form": "third-person novel with sustained close access to Winston Smith's consciousness, in three parts and a structurally significant Appendix on Newspeak",
        },
        "minimum_band": "proficient",
        "content_notes": (
            "Sustained depiction of state surveillance, propaganda, "
            "doublethink, the Two Minutes Hate, and torture (including the "
            "graphic interrogation scenes in Room 101 in Part 3); the "
            "destruction of Winston's selfhood at the close; the novel does "
            "not redeem its dystopia. Honest information, not a gate."
        ),
        "craft_focus": [
            "Third-person narration close to Winston's consciousness across most of the novel (lit-craft-008)",
            "Theme: totalitarian language and the relationship between language and thought; Newspeak as constructed-language argument (lit-craft-022; lit-craft-023 for the inclusion of the Appendix as part of the work)",
            "The Appendix on Newspeak as structurally part of the work: its past-tense framing has been read as evidence that the novel's dystopia did not last (lit-craft-023)",
            "Figurative system: the telescreen, Big Brother's face, the room above Charrington's shop, the glass paperweight (lit-craft-042)",
            "Winston's consciousness as the lens through which we see; what the novel lets us see past him (lit-craft-031)",
        ],
        "entry": (
            "Proficient: read the novel whole including the Appendix; follow "
            "the close third-person access to Winston; meet the figurative "
            "system (telescreen, the paperweight, Charrington's shop) as the "
            "work returns to it; meet Room 101 as the structural turn. "
            "Advanced: argue what the Appendix on Newspeak does structurally "
            "(its past-tense framing has been read as evidence that the "
            "dystopia did not last); argue what the novel claims about the "
            "relationship between language and thought; honor what the "
            "novel refuses to settle. Mastery: original argument about the "
            "novel's place in the twentieth-century political-fiction "
            "tradition Orwell helped form."
        ),
        "close_reading_passages": [
            "The opening on the clocks striking thirteen: how does the novel stage its first sentence and what does the small disturbance do?",
            "Winston in the room above Charrington's shop: how does the novel stage the brief place outside the telescreen, and what does the staging do to the reader who has begun to hope?",
            "The Appendix on Newspeak and its past-tense framing: how does the novel argue something by including the Appendix, and what does the tense let some readers infer?",
        ],
        "structural_analysis": (
            "Three parts: Part 1 establishes Winston, Oceania, and the regime; "
            "Part 2 stages the affair with Julia and the brief place outside; "
            "Part 3 stages the interrogation in the Ministry of Love and the "
            "destruction of Winston's selfhood. The novel ends with Winston's "
            "broken consent. The Appendix on Newspeak follows: its past-tense "
            "framing of Oceania's principal language has been read by some "
            "readers as evidence that the regime did not last. The structure "
            "is the novel's argument: the destruction is enacted in the "
            "narrative; the Appendix is the question."
        ),
        "thematic_lines": [
            "Totalitarian language and thought: the novel's claim that controlling language controls what can be thought",
            "Truth and historical record: the Ministry of Truth, doublethink, the falsified past",
            "What the Appendix lets the reader hope: the past-tense framing as a structural argument the novel does not state",
        ],
        "comparative_threads": [
            "Gulliver's Travels (lit-work-018): Swift as the political-satire ancestor; the figurative system bent to political argument",
            "Animal Farm (Orwell's 1945 shorter dystopia): the earlier work that established the political fable Orwell uses here",
            "Huxley's Brave New World (1932): the contemporary alternate dystopia; Orwell read it and wrote about it",
            "Margaret Atwood's The Handmaid's Tale (1985) as direct later inheritor including its own past-tense appendix-frame",
        ],
        "seminar_questions": [
            "What does the Appendix on Newspeak do that the narrative did not?",
            "Does the novel argue that controlling language controls thought, or does the novel hold the claim as a question? Where does the novel refuse to say?",
            "What does Room 101 do to Winston, and what does the novel argue about the limits of resistance?",
        ],
        "writing_invitations": [
            "The analytical paragraph on the opening sentence, naming what the small disturbance does to everything the novel will later show",
            "The essay on the Appendix on Newspeak as part of the work, with attention to the past tense and what some readers have inferred from it",
            "At advanced, the sustained essay on what the novel claims about language and thought, holding the narrative and the Appendix in productive tension",
        ],
        "context": (
            "Composed on the Hebridean island of Jura in the late 1940s "
            "while Orwell was dying of tuberculosis; published in 1949; the "
            "central English-language political-fiction title of the "
            "twentieth century; supplied as fact, interpretation left to "
            "the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The central English-language political-fiction title of the twentieth century; the seminar text on totalitarian language and on the structural argument of the Appendix.",
                "memory_work": {
                    "recitations": ["Recitation of the opening sentence and the first paragraph"],
                },
                "recitation_routine": "Seminar opens from the recited opening; the discussion takes its first question from the clocks striking thirteen.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of Nineteen Eighty-Four (the Houghton Mifflin Harcourt; the Penguin Modern Classics) read aloud across a few weeks, with the Appendix read as part of the work",
                ],
                "short_lesson_flow": "A living book read aloud across the three parts and the Appendix, narrated; Winston's consciousness followed; deepening to analysis of the Appendix's past-tense framing as the bands move up.",
                "narration_prompt": "Tell back the chapter we read today, and tell me what Winston thought and what the novel let you see past him.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of Nineteen Eighty-Four on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in language and power, in twentieth-century politics, or in dystopian fiction leads",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; let the Appendix be read; do not collapse the novel into a slogan.",
                "observation_documentation": "Over time, notice whether the student returns to the Appendix and begins to ask what the past tense does. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of the third-person close access and the Appendix on Newspeak as structural argument where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-033": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Selected poems of John Donne (Songs and Sonnets, Holy Sonnets, selected sermons)",
            "author": "John Donne",
            "date": "composed across the 1590s-1620s; Songs and Sonnets published posthumously 1633; sermons preached and printed in the 1620s",
            "genre": "English metaphysical poetry and prose",
            "form": "lyric poetry (sonnets, songs, elegies, holy sonnets) and devotional prose (sermons, Meditations Upon Emergent Occasions); dense conceit-driven verse",
        },
        "minimum_band": "proficient",
        "content_notes": (
            "Sustained sensuous and erotic figure in the love poems; sustained "
            "mortality and devotional self-examination in the Holy Sonnets "
            "and Meditations; the violence of religious figure in poems such "
            "as 'Batter my heart, three-personed God'; nothing in Donne is "
            "merely decorative. Honest information, not a gate."
        ),
        "craft_focus": [
            "Close reading proficient on a single dense lyric (lit-craft-003); advanced on a sequence (lit-craft-004)",
            "The metaphysical conceit as a figurative system unique to Donne and his contemporaries: a comparison sustained past the point where direct statement would suffice (lit-craft-042 at proficient; lit-craft-043 at advanced)",
            "The same form (sonnet, lyric) used for sacred and erotic ends, both in Donne's voice and across the body of work (lit-craft-022; lit-craft-023)",
            "The voice of the speaker as a constructed dramatic position (lit-craft-014 in the family of moves)",
        ],
        "entry": (
            "Proficient: read individual poems whole, find the conceit, follow "
            "it past the point of expected resolution, name what the conceit "
            "claims at the end that direct statement could not; meet the Holy "
            "Sonnets and the love poems alongside each other and notice that "
            "the same forms are being used for sacred and erotic ends. "
            "Advanced: read across the body of work and argue what Donne does "
            "to the inherited Petrarchan tradition and to the inherited "
            "devotional tradition at once; meet Donne's sermons and "
            "Meditations as prose that does what the lyrics do. Mastery: "
            "original argument about Donne's place in the formation of "
            "English metaphysical verse and his revival in the twentieth "
            "century by T. S. Eliot."
        ),
        "close_reading_passages": [
            "'A Valediction: Forbidding Mourning' and the compass conceit: how does the figure of two-feet-of-a-compass work, and how does the poem extend it past the point where a less ambitious figure would stop?",
            "'The Flea': how does the speaker stage an argument by extending the figure of the flea, and what does the poem refuse to settle about the speaker's claim?",
            "'Batter my heart, three-personed God' (Holy Sonnet 14): how does the poem use violent erotic figure for devotional address, and what does the form refuse to keep separate?",
        ],
        "structural_analysis": (
            "Each Donne lyric builds a conceit, extends it past expected "
            "resolution, and tests it; the closing turn (in sonnets, the "
            "couplet; in songs, the final stanza) either holds the conceit or "
            "refuses it. Across the body of work the same forms are used "
            "for sacred and erotic ends, and the boundary the Renaissance "
            "tradition would have kept Donne explicitly refuses. The sermons "
            "and Meditations carry the same procedure in prose. The "
            "structure across the body of work is the argument: a single "
            "rhetorical method applied wherever attention is needed."
        ),
        "thematic_lines": [
            "Sacred and erotic in the same forms: the body of work refuses to keep them separate",
            "The conceit as the work's instrument: a figure extended past where direct statement would suffice; what the extension does",
            "Death, devotion, and the constructed speaker: the Holy Sonnets and Meditations as the prose-and-verse pair of Donne's late period",
        ],
        "comparative_threads": [
            "The Sonnets of Shakespeare (lit-work-014): the contemporary English lyric sequence; how Donne's conceit differs from the Shakespearean sonnet's volta",
            "Petrarch's Canzoniere: the inherited tradition Donne argues with; what the metaphysical conceit does that Petrarchan figure could not",
            "George Herbert's The Temple: Donne's contemporary devotional poet, working the same forms differently",
            "T. S. Eliot's essay 'The Metaphysical Poets' (1921) and Eliot's lit-work-037 The Waste Land: Donne's twentieth-century revival was driven by Eliot",
        ],
        "seminar_questions": [
            "How far does the conceit extend in a chosen poem, and what does the extension do that direct statement could not?",
            "What does Donne refuse to keep separate that the Renaissance tradition kept separate?",
            "How does the Holy Sonnet 14 use erotic figure for devotional address, and what does the form let it claim?",
        ],
        "writing_invitations": [
            "The analytical paragraph on a single conceit in a chosen poem, naming what its extension does",
            "The essay on a love poem read alongside a Holy Sonnet, naming what the body of work refuses to keep separate",
            "At advanced, the essay on Donne's place in twentieth-century modernist taste, with Eliot's 1921 essay alongside",
        ],
        "context": (
            "Composed across Donne's life as Jack Donne the young man and Dr. "
            "John Donne the Dean of St. Paul's; the Songs and Sonnets "
            "circulated in manuscript and were printed posthumously in 1633; "
            "Donne's reputation rose and fell across the centuries and was "
            "decisively revived by Eliot in the twentieth century; supplied "
            "as fact, interpretation left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The central English metaphysical poet; the seminar text on the conceit and on the same forms used for sacred and erotic ends.",
                "memory_work": {
                    "recitations": ["Recitation of a chosen Holy Sonnet or song"],
                },
                "recitation_routine": "Seminar opens from the recited poem; the discussion takes its first question from how far the conceit extends and what the extension does.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of the major poems of John Donne (the Norton; the Penguin Major Works edited by John Carey) read aloud one or two at a sitting",
                ],
                "short_lesson_flow": "A poem read aloud whole and narrated; the conceit found, the extension named; deepening to analysis of the body of work as the bands move up.",
                "narration_prompt": "Tell back the poem we just read, and tell me how the conceit moved and what the close earned.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of Donne's major works on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in metaphysical verse, in sacred-and-erotic figure, or in twentieth-century revivals of seventeenth-century taste leads",
                ],
                "parent_role": "Be a fellow reader who has lived with particular Donne poems in their own returning. Read one aloud when the reader wants to hear it.",
                "observation_documentation": "Over time, notice whether the student returns to particular poems and follows a conceit past where they first thought it ended. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of the metaphysical conceit and Donne's place in English lyric tradition where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-034": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "British Romantic Poetry (selections from Blake, Wordsworth, Coleridge, Byron, Shelley, Keats)",
            "author": "William Blake, William Wordsworth, Samuel Taylor Coleridge, George Gordon (Lord Byron), Percy Bysshe Shelley, John Keats",
            "date": "the Romantic moment roughly 1789-1832",
            "genre": "British Romantic-period poetry",
            "form": "varied: lyric, ballad, ode, sonnet, fragment, dramatic verse; collected here as a survey of the six major poets",
        },
        "minimum_band": "proficient",
        "content_notes": (
            "Blake's prophetic books contain difficult mythic material; "
            "Wordsworth and Coleridge's 'Lyrical Ballads' include the disturbing "
            "'The Thorn'; Byron's 'Don Juan' is satirically erotic; Shelley's "
            "'The Mask of Anarchy' responds to the Peterloo Massacre with "
            "graphic political imagery; Keats writes about death from very near "
            "it. The Romantic moment is a moment of revolution, exile, and "
            "early death; the survey holds that. Honest information, not a "
            "gate."
        ),
        "craft_focus": [
            "Close reading on a dense lyric, with the work varying by form (ballad, ode, sonnet, fragment, prophetic book) (lit-craft-003 at proficient; lit-craft-004 at advanced)",
            "Figurative system varies by poet: Blake's contraries, Wordsworth's spots of time, Coleridge's haunted lyric, Shelley's wind and west, Keats's urn and bird (lit-craft-042 at proficient; lit-craft-043 at advanced)",
            "Theme advanced: Romanticism's central concerns held across six poets (nature, the self, imagination, the sublime, history, the artist) (lit-craft-022; lit-craft-023)",
            "Character advanced: the Romantic speaker as a constructed I the era invented; the body of work across poets is the argument (lit-craft-014)",
        ],
        "entry": (
            "Proficient: read selections from each poet in their own voice "
            "and form; find the figurative system that is each poet's "
            "instrument (Blake's contraries, Wordsworth's spots of time, "
            "Coleridge's haunted lyric, Shelley's wind, Keats's urn); read "
            "the great odes and ballads whole. Advanced: argue what each "
            "poet does to the inheritance from Milton (the most-named "
            "predecessor across all six) and what the six together do that "
            "becomes Romanticism as a category; honor that the category is a "
            "later construction the poets themselves did not share. Mastery: "
            "original argument about one poet's place in the Romantic moment "
            "or about what Romanticism gave to the long line of poetry that "
            "followed."
        ),
        "close_reading_passages": [
            "Blake, 'The Tyger' from Songs of Experience: how does the poem stage its question, and what does the form refuse to answer?",
            "Wordsworth, 'Lines Composed a Few Miles Above Tintern Abbey': how does the poem stage a return to a place, and what does the poet say has changed in him and what has the place taught?",
            "Keats, 'Ode on a Grecian Urn': how does the poem stage the address to a silent figure, and what does the close ('Beauty is truth, truth beauty') do that the rest of the poem has earned or has not?",
        ],
        "structural_analysis": (
            "Six poets across roughly fifty years, with no single form or "
            "movement uniting them in their own time. The category 'Romantic' "
            "is a later construction. What links the body of work is: a "
            "constructed first-person I as the poems' instrument; nature, "
            "imagination, history, and the sublime as recurring concerns; a "
            "conscious inheritance from Milton most of all; a willingness to "
            "let form follow concern rather than the other way around. The "
            "structure of the survey is the argument: read enough of each "
            "poet to hear them differently, and you hear what later readers "
            "have meant by Romanticism."
        ),
        "thematic_lines": [
            "Nature as the self's other and the self's mirror: the central Romantic question handled differently by each poet",
            "Imagination as the source: what each poet claims for the imaginative act, and where the claims diverge",
            "Revolution and its aftermath: the Romantic moment is the moment of the French Revolution and its undoing; the poetry holds the politics",
        ],
        "comparative_threads": [
            "Paradise Lost (lit-work-017): the most-named predecessor across all six poets; Blake especially read himself against Milton",
            "Donne (lit-work-033): the seventeenth-century pole the Romantics did not yet have the taste for; their inheritance is largely Miltonic",
            "Frankenstein (lit-work-020): Mary Shelley's novel as part of the same Romantic moment; the prose Romantic counterpart to the poetry",
            "T. S. Eliot (lit-work-037): the modernist who argued explicitly with Romantic taste and revived the metaphysical poets against it",
            "American Romantic inheritors: Whitman (lit-work-035) and Dickinson (lit-work-036), both of whom read the British Romantics with care",
        ],
        "seminar_questions": [
            "What does each poet do that no other on the list does?",
            "What is the figurative system that is each poet's instrument, and where does each poet refuse to use the others'?",
            "Where does the Romantic I claim more than the poem earns, and where does it earn more than it claims?",
        ],
        "writing_invitations": [
            "The analytical paragraph on a single poem, naming its figurative system and what the form lets the system claim",
            "The essay on one poet's argument with Milton, with passages from both held in productive tension",
            "At advanced, the comparative essay setting two Romantic poets against each other on a shared theme",
        ],
        "context": (
            "The Romantic moment in British poetry roughly 1789-1832, "
            "overlapping with the French Revolution, the Napoleonic Wars, "
            "and the early industrial transformation of Britain; the six "
            "major figures did not constitute a single school in their own "
            "time; the category 'Romantic' is largely a later construction; "
            "supplied as fact, interpretation left to the student. Any of "
            "the six poets is authorable as its own work node in a later "
            "batch."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The Romantic moment in British poetry; the seminar text on the constructed first-person I and the figurative systems each major poet invented.",
                "memory_work": {
                    "recitations": ["Recitation of a poem from each major Romantic poet across the survey"],
                },
                "recitation_routine": "Seminar opens from the recited poem; the discussion takes its first question from the poet's figurative instrument and what the poem claims with it.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy anthology of British Romantic poetry (the Norton Anthology of English Literature, Volume D; the Oxford Anthology) read aloud across a term, one or two poems per sitting",
                ],
                "short_lesson_flow": "An anthology read aloud poem by poem and narrated; the figurative instrument of each poet found; deepening to analysis of the body of work across poets as the bands move up.",
                "narration_prompt": "Tell back the poem we just read, and tell me what the poet's instrument was, and where the poem refused to settle.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy anthology of British Romantic poetry on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in Romantic-period poetry, in nature and the imagination, or in the long inheritance from Milton leads",
                ],
                "parent_role": "Be a fellow reader who has lived with particular Romantic poems in their own returning. Read one aloud when the reader wants to hear it.",
                "observation_documentation": "Over time, notice whether the student returns to particular poems and begins to feel one poet's instrument as distinct from another's. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of one or two poems per major Romantic poet and the figurative systems each invented where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-035": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Leaves of Grass (selections, across editions 1855-1892)",
            "author": "Walt Whitman",
            "date": "first edition 1855; revised and expanded across six editions through 1892",
            "genre": "nineteenth-century American free-verse poetry",
            "form": "long-line free verse; the catalog as the central rhetorical instrument; cycles of poems gathered into a single evolving book",
        },
        "minimum_band": "proficient",
        "content_notes": (
            "Sustained embodied and sensuous imagery throughout, including "
            "explicit treatment of the body, sexuality, and grief; the Civil "
            "War poems collected in 'Drum-Taps' and the elegy for Lincoln "
            "'When Lilacs Last in the Dooryard Bloom'd'; period attitudes "
            "the poems both exhibit and complicate; the book grows across "
            "Whitman's life and the late editions are not the same book as "
            "the first. Honest information, not a gate."
        ),
        "craft_focus": [
            "Long-line free verse: a meter not given by tradition, invented by Whitman for the embodied first-person voice (lit-craft-003/004)",
            "The catalog as figurative system: lists that accumulate and refuse selection (lit-craft-042 at proficient; lit-craft-043 at advanced)",
            "Character advanced: the first-person speaker as a cosmos (the speaker who 'contains multitudes') is itself the work's argument (lit-craft-014)",
            "Theme advanced: democracy, embodiment, sexuality, the elegy for Lincoln; what the book argues by being a book that keeps becoming itself (lit-craft-023)",
        ],
        "entry": (
            "Proficient: read 'Song of Myself' whole and the major shorter "
            "poems ('Crossing Brooklyn Ferry,' 'I Sing the Body Electric,' "
            "'Out of the Cradle Endlessly Rocking'); find the long line and "
            "the catalog as Whitman's instruments. Advanced: read the elegy "
            "'When Lilacs Last in the Dooryard Bloom'd' against the Civil "
            "War; read the multiple editions as part of the work and argue "
            "what the late Whitman does to the early. Mastery: original "
            "argument about Whitman's place in American poetry and what his "
            "embodied speaker did to the lyric tradition."
        ),
        "close_reading_passages": [
            "The opening sections of 'Song of Myself' (sections 1-6, including the catalog of what the speaker is and 'A child said What is the grass?'): how does the poem stage its speaker, and what does the long line let the speaker do?",
            "'Crossing Brooklyn Ferry': how does the poem stage an address across time to a reader who will be where the speaker was, and what does the figure of the ferry do?",
            "'When Lilacs Last in the Dooryard Bloom'd': how does the poem stage an elegy for Lincoln by holding the lilac, the star, and the bird together, and what does the figurative system do that direct elegy could not?",
        ],
        "structural_analysis": (
            "Leaves of Grass is one book that grew across six editions from "
            "1855 to 1892; the late editions are not the same book as the "
            "first, and the differences are part of the work. Inside the "
            "book, the long line is the central rhythmic invention, the "
            "catalog the central rhetorical instrument, and the first-person "
            "speaker the central figure. The structure is the work's "
            "argument: a single embodied voice that contains multitudes, "
            "growing across a life."
        ),
        "thematic_lines": [
            "Democracy and the embodied I: the speaker who claims to contain multitudes and what the catalog does with the claim",
            "Sexuality and the body: explicit in the poems and refusing the disembodied lyric tradition the period largely held",
            "The elegy for Lincoln and the Civil War poems: the book turning to mourn at the historical moment that broke the country",
        ],
        "comparative_threads": [
            "The British Romantics (lit-work-034): the inheritance Whitman read; what Whitman does to the Romantic I",
            "Emerson's essays ('The Poet'): Whitman's named teacher and the explicit American source",
            "Dickinson (lit-work-036): the contemporary American poet who made the opposite formal choice; the two together are the American poetry of the nineteenth century",
            "Later inheritors: Allen Ginsberg's Howl; Langston Hughes; the long American debt to the long line",
        ],
        "seminar_questions": [
            "What does the long line let Whitman do that no metered line could?",
            "What does the catalog claim about democracy and embodiment?",
            "What does the elegy for Lincoln do that direct statement of grief could not?",
        ],
        "writing_invitations": [
            "The analytical paragraph on a catalog passage, naming what the accumulation does that selection could not",
            "The essay on 'When Lilacs Last in the Dooryard Bloom'd' as elegy",
            "At advanced, the essay on the multiple editions as part of the work",
        ],
        "context": (
            "Composed in Brooklyn and Washington across Whitman's adult life; "
            "the first edition (1855) self-published in twelve poems; the "
            "final 'Deathbed' edition (1892) contains hundreds; the founding "
            "work of distinctively American verse; supplied as fact, "
            "interpretation left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The founding work of distinctively American verse; the seminar text on the long line, the catalog, and the embodied first-person speaker.",
                "memory_work": {
                    "recitations": [
                        "Recitation of a passage from 'Song of Myself' or 'When Lilacs Last in the Dooryard Bloom'd'"
                    ],
                },
                "recitation_routine": "Seminar opens from the recited passage; the discussion takes its first question from what the long line lets the speaker do.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of Leaves of Grass (the Norton with multiple editions; the Library of America) read aloud across a term, with the catalogs heard aloud",
                ],
                "short_lesson_flow": "A living book read aloud across selected poems and narrated; the long line and catalog noticed; deepening to analysis of the multiple-edition question as the bands move up.",
                "narration_prompt": "Tell back the passage we read today, and tell me what the long line let Whitman say, and what the catalog gathered.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of Leaves of Grass on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in American poetry, in the body, in democracy, or in the long line leads",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; the long line is heard before it is named; let Whitman be his own teacher.",
                "observation_documentation": "Over time, notice whether the student returns to particular poems and begins to feel the long line as Whitman's instrument. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of the long line, the catalog, and Whitman's place in American poetry where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-036": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Selected poems of Emily Dickinson (from the nearly 1,800 poems)",
            "author": "Emily Dickinson",
            "date": "composed across the 1850s-1880s; only a handful published in Dickinson's lifetime; first significant publication 1890; full scholarly edition 1955 (Johnson) and 1998 (Franklin)",
            "genre": "nineteenth-century American lyric poetry",
            "form": "short lyrics, predominantly in ballad and common meter, with characteristic dashes and slant rhyme; nearly all unpublished in the poet's lifetime",
        },
        "minimum_band": "proficient",
        "content_notes": (
            "Sustained engagement with death, doubt, and the limits of "
            "knowing; intense compression that can be difficult on first "
            "reading; the poems were largely unpublished in the poet's "
            "lifetime and the editorial history of the poems (the early "
            "editors' regularizations and the later scholarly recoveries) "
            "is itself part of reading Dickinson honestly. Honest "
            "information, not a gate."
        ),
        "craft_focus": [
            "Close reading on a dense short lyric: every word and every dash bearing weight (lit-craft-003 at proficient; lit-craft-004 at advanced)",
            "Dickinson's dashes and slant rhyme as a figurative-syntactic system: the dash holds what the line cannot say (lit-craft-042 at proficient; lit-craft-043 at advanced)",
            "Theme advanced: death, doubt, the limits of knowing; faith held alongside its refusal (lit-craft-023)",
            "The constructed speaker: not Dickinson but the lyric I she keeps inventing across the poems (lit-craft-014)",
            "The editorial history as part of reading the poems honestly (lit-craft-023 in the family of moves)",
        ],
        "entry": (
            "Proficient: read individual poems whole, slowly; find the work "
            "the dash and the slant rhyme do; read the poems in their "
            "Johnson or Franklin numbering rather than by editorial title; "
            "meet the major themes (death, faith, knowing) as the poems "
            "return to them. Advanced: read the editorial history as part "
            "of the work (Mabel Loomis Todd's 1890 edition regularized the "
            "dashes; the twentieth-century scholarly editions restored "
            "them); argue what Dickinson does to the lyric tradition with a "
            "form she largely kept to herself. Mastery: original argument "
            "about Dickinson's place in nineteenth-century American poetry "
            "alongside Whitman."
        ),
        "close_reading_passages": [
            "'Because I could not stop for Death' (Fr 479; Jo 712): how does the poem stage the carriage ride, and what does the form do to the figure of death?",
            "'I heard a Fly buzz when I died' (Fr 591; Jo 465): how does the poem stage the speaker's own death and the fly, and what does the form refuse to say?",
            "'Tell all the truth but tell it slant' (Fr 1263; Jo 1129): how does the poem name its own method, and what does the imperative claim about lyric form?",
        ],
        "structural_analysis": (
            "Each Dickinson lyric is a compressed argument worked through "
            "ballad or common meter, with the dashes holding what the line "
            "would otherwise have to commit to. The slant rhyme refuses the "
            "closure that perfect rhyme would supply. Across the body of "
            "work, the same speaker (or several speakers) returns to a small "
            "set of concerns (death, faith, knowing, the eye that sees, the "
            "self that survives) and works them through one short poem at a "
            "time. The structure across the body of work is the argument: "
            "the lyric handled at the limit of what compression can do."
        ),
        "thematic_lines": [
            "Death as the work's recurring subject and the work's refusal to settle what death is",
            "Faith and doubt held alongside each other: Dickinson refuses to give either up",
            "The dash as the syntactic figure for what cannot be said: a punctuation mark made to do the work of a metaphor",
        ],
        "comparative_threads": [
            "Whitman (lit-work-035): the contemporary American poet who made the opposite formal choice; the two together are the American poetry of the nineteenth century",
            "Donne (lit-work-033): the seventeenth-century English compression Dickinson read; the slant rhyme and dash have something of Donne's procedure done in short form",
            "Hopkins (the Victorian English near-contemporary): the other nineteenth-century poet whose form was kept largely to himself",
            "Later inheritors: Marianne Moore; Elizabeth Bishop; the long American debt to Dickinson's compression",
        ],
        "seminar_questions": [
            "What does a Dickinson dash do that a comma or a semicolon could not?",
            "What does the slant rhyme refuse to settle that perfect rhyme would have settled?",
            "Where does the body of work hold faith and doubt at the same time, and where does it refuse to choose?",
        ],
        "writing_invitations": [
            "The analytical paragraph on a single poem, naming what the dashes do and what the slant rhymes refuse",
            "The essay on three poems handling death, holding them in productive tension",
            "At advanced, the essay on the editorial history as part of the work",
        ],
        "context": (
            "Composed in near isolation in Amherst, Massachusetts, across "
            "the 1850s-1880s; nearly 1,800 poems found in manuscript at "
            "Dickinson's death; first significant publication in 1890 by "
            "Mabel Loomis Todd and Thomas Wentworth Higginson, with the "
            "dashes regularized and titles imposed; full scholarly editions "
            "by Thomas H. Johnson (1955) and R. W. Franklin (1998); supplied "
            "as fact, interpretation left to the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "One of the two great American poets of the nineteenth century; the seminar text on the lyric at the limit of compression.",
                "memory_work": {
                    "recitations": ["Recitation of one or two short Dickinson poems"],
                },
                "recitation_routine": "Seminar opens from the recited poem; the discussion takes its first question from where the dash sits and what the form refuses to settle.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of Dickinson (the Franklin Reading Edition; the Norton Critical edition; the Johnson edition for the older numbering) read aloud one or two poems at a sitting",
                ],
                "short_lesson_flow": "A short poem read aloud and narrated; the dashes heard as part of the line, the slant rhyme noticed; deepening to analysis of the body of work as the bands move up.",
                "narration_prompt": "Tell back the poem we just read, and tell me where the dash held something the words refused to say.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of Dickinson on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in compressed lyric, in death and faith held together, or in poetry that was kept largely to itself leads",
                ],
                "parent_role": "Read aloud one poem at a sitting; the slow pace is the practice; let the dashes be heard.",
                "observation_documentation": "Over time, notice whether the student returns to particular poems and begins to hear the dash as a figure. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of the compressed lyric and the dash as syntactic figure where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-037": {
        "node_type": "work",
        "track": "classics",
        "work": {
            "title": "Selected poems and essays of T. S. Eliot (The Love Song of J. Alfred Prufrock, The Waste Land, Four Quartets; The Metaphysical Poets and Tradition and the Individual Talent)",
            "author": "T. S. Eliot",
            "date": "Prufrock 1915; The Waste Land 1922; Tradition and the Individual Talent 1919; The Metaphysical Poets 1921; Four Quartets 1936-43",
            "genre": "Anglo-American modernist poetry and criticism",
            "form": "fragmentary modernist verse with multiple voices and dense allusion; critical essays that shaped how modernism read its inheritance",
        },
        "minimum_band": "advanced",
        "content_notes": (
            "The Waste Land is fragmentary by design; Eliot's allusions are "
            "to Western, Sanskrit, and other traditions; period antisemitic "
            "passages in poems including 'Burbank with a Baedeker' and "
            "stretches of Sweeney material that Eliot's later editors and "
            "critics have weighed without resolving; the late religious "
            "turn of Four Quartets is in Anglo-Catholic register the reader "
            "is invited to weigh, not adopt. Honest information, not a gate."
        ),
        "craft_focus": [
            "Close reading across modes on a fragmentary modernist poem of dense allusion (lit-craft-004)",
            "Figurative system as inheritance: every allusion is a piece of the work's argument and brings its source with it (lit-craft-043)",
            "Multiple speakers, no authoritative voice: The Waste Land is voiced by Tiresias and many others, none of them the poet (lit-craft-031, lit-craft-014)",
            "Theme advanced: what the poems refuse to settle about the modern world, about the inheritance the poet is in argument with (lit-craft-023)",
            "The critical essays as part of the work: 'The Metaphysical Poets' revived Donne; 'Tradition and the Individual Talent' argued the inheritance the poems enact",
        ],
        "entry": (
            "Advanced: read The Waste Land whole, with the notes Eliot "
            "supplied as part of the work (and held suspiciously as part of "
            "the work, as Eliot himself later did); follow the allusions to "
            "Dante, Shakespeare, Webster, the Buddha, the Upanishads, Donne, "
            "the Grail material; read Eliot's two great essays alongside the "
            "poems; meet Four Quartets as the late religious turn the poems "
            "make. Mastery: original argument about Eliot's place in "
            "Anglo-American modernism and what his criticism did to twentieth-"
            "century taste."
        ),
        "close_reading_passages": [
            "'The Love Song of J. Alfred Prufrock' (1915): how does the poem stage a speaker who cannot complete his question, and what does the dramatic monologue inheritance (from Browning) become here?",
            "The Waste Land, Part 1 ('The Burial of the Dead'): how does the poem stage its fragmented voices and the famous epigraph from Petronius's Satyricon, and what does the opening sequence claim?",
            "Four Quartets, 'Little Gidding' (1942): how does the late Eliot stage a return to a place of religious resonance, and what does the meeting with the 'familiar compound ghost' do?",
        ],
        "structural_analysis": (
            "Across Eliot's career: a single dramatic monologue (Prufrock); "
            "a long fragmented poem of multiple voices (The Waste Land); a "
            "four-part meditative sequence (Four Quartets); and a body of "
            "criticism that shaped how the poems were read and how the "
            "inheritance the poems work from was reread. The Waste Land is "
            "the central work: its multiple voices are filtered through "
            "Tiresias (per Eliot's note) but no one in the poem speaks for "
            "the poet, and the closing Sanskrit (Shantih shantih shantih) "
            "is part of the argument. The structure across the body of work "
            "is the argument: modernism enacted in the poems, theorized in "
            "the essays, and turned at the close to a religious resolution "
            "the early poems did not promise."
        ),
        "thematic_lines": [
            "Fragmentation as the modern form: not a failure of unity but the work's argument about the time it was made in",
            "Inheritance as constitutive: every Eliot allusion brings its source with it, and the poems are made of the inheritance",
            "The late religious turn: Four Quartets as resolution the earlier poems did not promise; what the body of work argues by ending where it does",
        ],
        "comparative_threads": [
            "Donne (lit-work-033): Eliot's 1921 essay 'The Metaphysical Poets' revived Donne in the twentieth century; Eliot's poems learned from Donne",
            "Dante's Inferno (lit-work-010): Eliot's most-quoted predecessor in The Waste Land and across Four Quartets; the inheritance is decisive",
            "The British Romantics (lit-work-034): the inheritance Eliot explicitly argued against in his criticism; Romanticism as the taste he undertook to displace",
            "Ezra Pound (Eliot's contemporary and editor of The Waste Land): the parallel modernism; the dedication to Pound as 'il miglior fabbro' (the better maker) is part of the poem",
            "William Carlos Williams (the American counter-modernism): the alternative the American tradition kept developing",
        ],
        "seminar_questions": [
            "What does the fragmentation of The Waste Land argue that a unified poem could not?",
            "What does each allusion bring with it, and where does the poem refuse to translate or paraphrase?",
            "What does Four Quartets earn that the earlier poems did not have access to?",
        ],
        "writing_invitations": [
            "The analytical paragraph on 'The Burial of the Dead', naming what the fragmentary form does in the opening sequence",
            "The essay on a single allusion (Dante's; Shakespeare's; the Upanishadic close) as part of the work",
            "The sustained essay on Eliot's two great essays alongside the poems, naming what the criticism did to twentieth-century taste",
        ],
        "context": (
            "Composed across Eliot's career from his American youth through "
            "his English citizenship, his Anglo-Catholic conversion in 1927, "
            "and the war years; The Waste Land was edited by Ezra Pound from "
            "a longer draft and is dedicated to him; Four Quartets was "
            "composed during the Second World War, with 'Little Gidding' "
            "(1942) at its end; supplied as fact, interpretation left to "
            "the student."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The central poet of Anglo-American modernism; the seminar text on the fragmentary form, the dense allusion, and the inheritance the poems enact.",
                "memory_work": {
                    "recitations": [
                        "Recitation of the opening of 'The Burial of the Dead' or the closing of 'Little Gidding'"
                    ],
                },
                "recitation_routine": "Seminar opens from the recited passage; the discussion takes its first question from what the allusion brings and what the poem refuses to translate.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of Eliot (the Faber Selected Poems; the Norton Critical edition of The Waste Land; the Library of America volumes) read aloud across a term, paired with the two great essays",
                ],
                "short_lesson_flow": "A living book read aloud across the major poems and the essays, narrated; the allusions tracked one at a time without rushing; deepening to analysis of the fragmentary form as the bands move up.",
                "narration_prompt": "Tell back the passage we read today, and tell me what the voice was doing and what the allusion brought with it.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of Eliot's poems and essays on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in modernism, in fragmentation as form, or in the long inheritance the poems work with leads",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; let the allusions be researched when the reader wants; do not paper over the difficulty.",
                "observation_documentation": "Over time, notice whether the student returns to particular passages and begins to track the allusions as part of the work. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of the fragmentary modernist form and Eliot's criticism alongside the poems where chosen.",
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
    "lit-work-inh-005": {
        "node_type": "work",
        "track": "inheritance",
        "work": {
            "title": "Historia Regum Britanniae (History of the Kings of Britain), selections from Books IX-XI (the Arthurian portion)",
            "author": "Geoffrey of Monmouth",
            "date": "c. 1136",
            "genre": "medieval Latin chronicle (presented as history, functioning as romance)",
            "form": "Latin prose chronicle in twelve books; the Arthurian portion runs across Books IX-XI",
        },
        "minimum_band": "proficient",
        "content_notes": (
            "Battlefield violence including the catalog of slain in Arthur's "
            "continental campaign; the treason of Mordred and the wounding "
            "of Arthur at Camlann; Geoffrey's narrative is presented as "
            "factual history but contemporary scholars and many medieval "
            "readers (notably William of Newburgh) recognized the work as "
            "literary invention; the work's claim to be a translation from "
            "an 'ancient British book' is part of its strategy. Honest "
            "information, not a gate."
        ),
        "craft_focus": [
            "Close reading proficient on Latin chronicle prose in a worthy translation (lit-craft-003)",
            "Character proficient: Arthur as constructed founding figure; Merlin; Mordred (lit-craft-013)",
            "Theme proficient and advanced: the founding-myth shape of the chronicle; what Geoffrey claims to be doing and what the work actually does (lit-craft-022; lit-craft-023)",
            "The unreliable claim of the source manuscript as a structural device (lit-craft-031 in the family of moves)",
        ],
        "entry": (
            "Proficient: read the Arthurian portion of the Historia whole in "
            "a worthy modern translation; follow the founding-myth shape of "
            "the work; meet Merlin's first major appearance in Western "
            "literature; meet Arthur as the figure Geoffrey invents into "
            "European literature. Advanced: argue what Geoffrey does by "
            "presenting his work as history rather than as romance, and "
            "what the claim of an 'ancient British book' lets the work do; "
            "set the Historia against Bede's earlier Ecclesiastical History "
            "of the English People (which Geoffrey was rewriting against). "
            "Mastery: original argument about Geoffrey's role in inventing "
            "the literary Arthur for medieval Europe."
        ),
        "close_reading_passages": [
            "The Prophecies of Merlin (the inset prophetic Book VII; often read alongside or before the Arthurian books): how does Geoffrey stage Merlin's prophecies, and what does the inset do to the work's claim to be history?",
            "Arthur's coronation and the Continental campaign (Book IX): how does the chronicle stage Arthur's rise and his European war, and what does the scale of the campaign claim?",
            "The treason of Mordred and the wounding at Camlann (Book XI): how does the chronicle stage the fall, and what does the wording of Arthur being carried to Avalon ('for the healing of his wounds') do?",
        ],
        "structural_analysis": (
            "Twelve books of British history from Brutus the Trojan to "
            "Cadwallader; the Arthurian portion in Books IX-XI is the work's "
            "longest and most elaborated sequence. Geoffrey writes as a "
            "chronicler claiming to translate from an ancient British book, "
            "but the Arthurian sequence has no surviving prior source and is "
            "largely Geoffrey's invention or his synthesis of folk material. "
            "The structure is the work's argument: a founding myth for the "
            "Britons in the form of a Latin chronicle that medieval Europe "
            "received as fact and that established the Arthurian world for "
            "every later inheritor."
        ),
        "thematic_lines": [
            "Founding myth as chronicle: the work's claim to be history and what the form lets it do",
            "Arthur as the figure invented for European literature: the moment from which every later Arthurian inheritor descends",
            "The 'ancient British book' as Geoffrey's structural device: a claim modern scholarship has not located but that the medieval audience largely accepted",
        ],
        "comparative_threads": [
            "Bede's Ecclesiastical History of the English People (731): the earlier chronicle Geoffrey was rewriting against; Bede had treated the Britons sparingly, Geoffrey makes them central",
            "lit-work-inh-006 Sir Gawain and the Green Knight: the alliterative-romance inheritance that develops the Arthurian world Geoffrey set in motion",
            "lit-work-inh-007 Le Morte d'Arthur: Malory's prose compilation; Geoffrey is one of the named English-language predecessors Malory and his French sources both draw from",
            "Wace's Roman de Brut (c. 1155) and Layamon's Brut (c. 1200): the Anglo-Norman and Middle English verse adaptations that transmitted Geoffrey's Arthur into the romance tradition",
        ],
        "seminar_questions": [
            "What does Geoffrey gain by presenting the Arthurian sequence as history rather than as romance?",
            "What does the inset of Merlin's prophecies do to the work's claim to be a chronicle?",
            "How does the wording of Arthur being carried to Avalon leave the ending unsettled, and what do later inheritors do with the opening Geoffrey left?",
        ],
        "writing_invitations": [
            "The analytical paragraph on the wounding-and-Avalon passage, naming what the chronicle refuses to settle",
            "The essay on Geoffrey's claim to translate from an ancient British book and what the claim lets the work do",
            "The comparative paragraph setting Geoffrey's Arthur against the Arthur of a later inheritor (Malory or T. H. White)",
        ],
        "context": (
            "Composed in the 1130s by a Welsh-Norman cleric attached to "
            "Oxford; presented as a translation from an ancient British "
            "book whose existence modern scholarship has not confirmed; "
            "received widely across medieval Europe as factual history; "
            "the foundational text of the literary Arthur; supplied as fact, "
            "interpretation left to the student."
        ),
        "lineage": (
            "Matter of Britain. Source position: Geoffrey of Monmouth is the "
            "foundational source of the literary Arthur for medieval Europe. "
            "The figure passes from Geoffrey into Wace's Roman de Brut, "
            "Layamon's Brut, the French Vulgate Cycle, Chrétien de Troyes, "
            "and through that tradition into Malory's Le Morte d'Arthur "
            "(lit-work-inh-007) and onward to every later English-language "
            "Arthurian inheritor (Tennyson lit-work-inh-008; T. H. White "
            "lit-work-inh-009; Cornwell lit-work-inh-010)."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The foundational Latin chronicle that introduces the literary Arthur to medieval Europe; the seminar text on founding myth in chronicle form.",
                "memory_work": {
                    "recitations": [
                        "Recitation of the passage of Arthur's wounding and being carried to Avalon in a worthy modern translation"
                    ],
                },
                "recitation_routine": "Seminar opens from the recited passage; the discussion takes its first question from how the chronicle leaves the ending unsettled.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy translation of the Historia Regum Britanniae (Lewis Thorpe's Penguin Classics translation; Michael Faletra's Broadview edition) read aloud across the Arthurian portion",
                ],
                "short_lesson_flow": "A living book read aloud across Books IX-XI and narrated; the chronicle's claim to be history weighed against what it actually does; deepening to analysis of the Avalon ending as the bands move up.",
                "narration_prompt": "Tell back the portion we read today, and tell me whether the chronicle is reporting or inventing, and where you can tell.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy translation of Geoffrey's Historia on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in Arthurian origins, in founding myth, or in medieval chronicle leads",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; let the chronicle's invention be itself; trace forward into the inheritance.",
                "observation_documentation": "Over time, notice whether the student returns to Geoffrey and follows the Arthurian thread forward into Malory and the modern inheritors. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of medieval Latin chronicle and Geoffrey's role in inventing the literary Arthur where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-inh-006": {
        "node_type": "work",
        "track": "inheritance",
        "work": {
            "title": "Sir Gawain and the Green Knight",
            "author": "the Gawain poet (anonymous)",
            "date": "c. 1370-1390",
            "genre": "Middle English alliterative Arthurian romance",
            "form": "verse romance in 2,530 lines arranged in 101 stanzas of alliterative long-line with a short rhyming 'bob and wheel' tail; preserved in a single manuscript (BL Cotton Nero A.x) alongside Pearl, Cleanness, and Patience",
        },
        "minimum_band": "proficient",
        "content_notes": (
            "The beheading game at the poem's opening, in which the Green "
            "Knight invites a blow and survives; sustained hunt scenes in "
            "Fitt 3 including the dismembering of deer, boar, and fox in "
            "detail consistent with medieval hunting manuals; bedroom "
            "scenes with the Lady which are erotically charged but never "
            "consummated; the wounding of Gawain at the Green Chapel. "
            "Honest information, not a gate."
        ),
        "craft_focus": [
            "Close reading on dense Middle English alliterative verse, in modern translation alongside the original where possible (lit-craft-003 at proficient; lit-craft-004 at advanced)",
            "Character: Gawain as the constructed knight whose courtesy is the poem's argument (lit-craft-013); Bertilak / the Green Knight as the figure the poem refuses to flatten (lit-craft-014 at advanced)",
            "Figurative system: the green of the Green Knight, the pentangle on Gawain's shield, the girdle Gawain accepts and keeps, the three hunts braided with the three bedroom temptations (lit-craft-042 at proficient; lit-craft-043 at advanced)",
            "Theme: courtesy, integrity, the test of a knight whose word is the poem's measure of him (lit-craft-022; lit-craft-023)",
            "Structural braiding: three hunts intercut with three bedroom scenes; the parallel meanings the form makes (lit-craft-008 in the family of moves)",
        ],
        "entry": (
            "Proficient: read the poem whole in a worthy modern translation, "
            "with the Middle English original on the facing page where "
            "possible; follow the four fitts (the New Year's challenge, the "
            "journey to the Green Chapel, the hunts and bedroom scenes at "
            "Bertilak's castle, the return to the Chapel); meet the pentangle "
            "digression in Fitt 2 and the girdle's role across Fitts 3 and 4. "
            "Advanced: argue what the poem refuses to settle about Gawain's "
            "failure (he keeps the girdle and is wounded for it), what "
            "Bertilak's laughter at the close does, and how the intricate "
            "braiding makes meaning. Mastery: original argument about the "
            "Gawain poet's place in the alliterative tradition the "
            "fourteenth century revived and lost again."
        ),
        "close_reading_passages": [
            "The Green Knight's first arrival at Camelot (Fitt 1): how does the poem stage the New Year's interruption, and what does the description of the Green Knight refuse to fix?",
            "The pentangle digression on Gawain's shield (Fitt 2): how does the poet stage an explicit emblem with five interlocking fives, and what does the digression claim about Gawain that the rest of the poem will test?",
            "The third hunt and the third bedroom scene (Fitt 3): how does the poem braid the fox-hunt against the Lady's third offer (the green girdle), and what does Gawain do that he will pay for at the Chapel?",
        ],
        "structural_analysis": (
            "Four fitts in 101 stanzas, each stanza alliterative long-line "
            "closing with a short rhyming bob and wheel. Fitt 1: the New "
            "Year's beheading game at Camelot. Fitt 2: Gawain's year-long "
            "preparation and journey, with the pentangle digression. Fitt "
            "3: three days at Bertilak's castle, where three hunts are "
            "intercut stanza by stanza with three bedroom temptations and "
            "three exchanges of winnings between Gawain and his host. Fitt "
            "4: the return to the Green Chapel, the wounding, and the long "
            "explanation. The structural braiding is the poem's argument: "
            "the test was not the blow but the bargain Gawain made, and "
            "the bargain was made in the bedroom where Gawain thought "
            "courtesy alone was at stake."
        ),
        "thematic_lines": [
            "Courtesy and the keeping of one's word: the poem's measure of a knight",
            "Failure and the marking of it: Gawain keeps the girdle and is wounded for it; he returns wearing the girdle as his sign and Arthur's court makes it a fashion; the poem refuses to settle whether the wound was punishment, mercy, or instruction",
            "The Green Knight's identity: Bertilak and the Green Knight are the same person, and the explanation does not exhaust what the figure means",
        ],
        "comparative_threads": [
            "lit-work-inh-005 Geoffrey of Monmouth: the Arthurian world Geoffrey set in motion; the Gawain poet develops it in alliterative-romance form",
            "lit-work-inh-007 Le Morte d'Arthur: Malory's Gawain is a different Gawain than the Gawain poet's; the comparison is decisive for any reading of either",
            "The Pearl Poet's other works (Pearl, Cleanness, Patience) preserved in the same single manuscript: the body of work of one anonymous poet",
            "Tolkien's edition and translation of Sir Gawain (with E. V. Gordon 1925; Tolkien's solo translation published posthumously 1975): the poem shaped Tolkien's scholarly engagement with Middle English alliterative verse and his work on lit-work-inh-004 The Lord of the Rings",
            "Simon Armitage's modern verse translation (2007) as the most-read recent inheritor in English",
        ],
        "seminar_questions": [
            "What does the pentangle digression claim about Gawain, and where in the rest of the poem is the claim tested?",
            "Why does the poem braid the three hunts against the three bedroom scenes stanza by stanza? What does the form make visible that direct statement could not?",
            "What does Gawain's failure with the girdle mean, and where does the poem refuse to settle the question?",
        ],
        "writing_invitations": [
            "The analytical paragraph on the third hunt and third bedroom scene, naming what the braiding makes visible",
            "The essay on the green girdle as a figure the poem refuses to fix",
            "At advanced, the essay on what the poem refuses to settle about Gawain's failure",
        ],
        "context": (
            "Composed in the West Midlands of England in the second half of "
            "the fourteenth century by a poet whose other works (Pearl, "
            "Cleanness, Patience) survive only in the same single "
            "manuscript and whose name is unknown; recovered for English "
            "literary tradition in the nineteenth century; central to the "
            "fourteenth-century alliterative revival; supplied as fact, "
            "interpretation left to the student."
        ),
        "lineage": (
            "Matter of Britain. Source position: the foundational English "
            "Arthurian romance in the alliterative tradition. Inherits the "
            "Arthurian world Geoffrey of Monmouth (lit-work-inh-005) set in "
            "motion. The Gawain of this poem is a different Gawain than "
            "Malory's (lit-work-inh-007) and the comparison is part of how "
            "the inheritance branches. The poem shaped Tolkien's "
            "(lit-work-inh-004) lifelong scholarly engagement with Middle "
            "English alliterative verse; Tolkien co-edited the standard "
            "edition and translated the poem himself."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The central Middle English alliterative Arthurian romance; the seminar text on the braided structure and the test of a knight's word.",
                "memory_work": {
                    "recitations": [
                        "Recitation of the opening stanza in Middle English or a worthy modern translation"
                    ],
                },
                "recitation_routine": "Seminar opens from the recited opening; the discussion takes its first question from how the poem stages the New Year's interruption.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of Sir Gawain and the Green Knight (the Tolkien translation; Simon Armitage's verse translation; the Norton Critical edition with the Middle English) read aloud across the four fitts",
                ],
                "short_lesson_flow": "A living book read aloud across the four fitts and narrated; the three-hunts / three-bedroom braiding noticed; deepening to analysis of the girdle as the bands move up.",
                "narration_prompt": "Tell back the fitt we read today, and tell me what Gawain did and what the poem made you notice he did.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of Sir Gawain on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in Arthurian romance, in Middle English verse, or in Tolkien's scholarly background leads",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; let the green girdle stay open; bring Tolkien's translation into the room when the student wants to hear it.",
                "observation_documentation": "Over time, notice whether the student returns to the poem and begins to feel the braiding as the poem's argument. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of Middle English alliterative verse and the poem's braided structure where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
    "lit-work-inh-007": {
        "node_type": "work",
        "track": "inheritance",
        "work": {
            "title": "Le Morte d'Arthur (selections, with attention to the opening books and the last two)",
            "author": "Sir Thomas Malory",
            "date": "composed in prison c. 1469-70; printed by William Caxton 1485; the Winchester Manuscript (rediscovered 1934) preserves a different, less-edited textual version",
            "genre": "late-medieval English Arthurian prose compilation",
            "form": "prose narrative cycle in twenty-one books (Caxton) or eight tales (Winchester); the longest sustained English Arthurian work; channels Geoffrey, the French Vulgate Cycle, and earlier into a single Round-Table narrative",
        },
        "minimum_band": "advanced",
        "content_notes": (
            "Sustained battlefield violence throughout; the killing of "
            "innocents in the May Day infant-massacre Arthur orders to "
            "destroy Mordred; the adulterous love of Lancelot and "
            "Guinevere; the killings of Gareth and Gaheris at Lancelot's "
            "hand and the wars that follow; the final battle at Camlann "
            "and the deaths of Arthur and Mordred; the book is a long "
            "elegy for a fellowship that destroys itself. Honest "
            "information, not a gate."
        ),
        "craft_focus": [
            "Close reading advanced on late Middle English prose, in the Caxton or Winchester text with modernization where chosen (lit-craft-004)",
            "Narrative craft advanced: the long compilation as one structural argument across many borrowed sources; Malory's seams and unifications (lit-craft-008 strained past proficient; lit-craft-031 in the family of moves for the question of when Malory is repeating his source and when revising)",
            "Character advanced: Arthur, Lancelot, Guinevere, Gawain, Mordred across the long span; the fellowship as the work's argument (lit-craft-014)",
            "Theme advanced: the whole work as elegy for the Round Table; what the cycle refuses to settle about Lancelot's adultery, about Arthur's responsibility, about whether the fellowship was always doomed (lit-craft-023)",
            "Figurative system: the sword, the cup, the seat at the Round Table, the queen's chamber, the boat that takes Arthur to Avalon (lit-craft-042 at proficient; lit-craft-043 at advanced)",
        ],
        "entry": (
            "Advanced: read the work whole over a long span (most readers "
            "take a year); meet the Winchester Manuscript's eight tales or "
            "Caxton's twenty-one books and follow the long argument across; "
            "argue what Malory does to the inheritance he is compiling (the "
            "French Vulgate Cycle, the alliterative Morte Arthure, Geoffrey "
            "through the chronicle tradition); honor what the book refuses "
            "to settle about Lancelot, about Arthur, about whether the "
            "fellowship was always going to fall. Mastery: original "
            "argument about Malory's place in establishing the English-"
            "language Arthurian canon every later inheritor reaches back to."
        ),
        "close_reading_passages": [
            "The drawing of the sword from the stone (Caxton Book 1; the opening tales in Winchester): how does Malory stage Arthur's accession, and what does the prose's plainness do that a more elaborate telling could not?",
            "The first meeting of Lancelot and Guinevere and the long sequence of Lancelot's quests (Caxton Books 6 and 18 especially): how does Malory stage a love the cycle will not let succeed, and what does the prose let the reader feel about Lancelot's interior?",
            "The final battle at Camlann, the wounding, and the passing to Avalon (Caxton Book 21): how does Malory stage the end of the fellowship, and what does the famous Latin epitaph 'Hic iacet Arthurus, Rex quondam, Rexque futurus' (here lies Arthur, the once and future king) do at the close?",
        ],
        "structural_analysis": (
            "A late-medieval prose compilation drawing on the French "
            "Vulgate Cycle (Lancelot-Grail), the post-Vulgate, the "
            "alliterative Morte Arthure, the stanzaic Morte Arthur, and "
            "earlier chronicle material going back to Geoffrey of Monmouth. "
            "Caxton edited the work into twenty-one books for the 1485 "
            "print; the Winchester Manuscript (rediscovered 1934) "
            "preserves an earlier form in eight tales, with different "
            "chapter divisions and fewer editorial unifications. The "
            "structure is the work's argument: a fellowship gathered, "
            "glorified, and undone, across the long span the cycle requires."
        ),
        "thematic_lines": [
            "The Round Table as the cycle's central figure: the fellowship is what the work is about and what the work loses",
            "Adultery, loyalty, and the doom of the fellowship: Malory refuses to settle whether Lancelot's love destroys the order or merely reveals what was destroying it",
            "Once and future: the book's final phrase ('Rex quondam, Rexque futurus') the inheritance bequeaths to every later English-language Arthurian work",
        ],
        "comparative_threads": [
            "lit-work-inh-005 Geoffrey of Monmouth: the ultimate English-language ancestor through the chronicle tradition",
            "lit-work-inh-006 Sir Gawain and the Green Knight: Malory's Gawain is a different Gawain, more compromised; the comparison illuminates both works",
            "The French Vulgate Cycle (Lancelot-Grail; the post-Vulgate Roman du Graal): Malory's largest single source, in French, which he both translates and edits sharply",
            "lit-work-inh-008 Tennyson's Idylls of the King: the Victorian inheritor that reads Malory through Victorian moral lens",
            "lit-work-inh-009 T. H. White's The Once and Future King: the modern inheritor whose chapter epigraphs and explicit references name Malory throughout; White's title is from Malory's epitaph",
            "lit-work-inh-010 Cornwell's Warlord Chronicles: the post-Roman historical recasting; Cornwell's foreword names Malory and explicitly diverges from him",
        ],
        "seminar_questions": [
            "What does Malory refuse to settle about Lancelot? Where in the work is the question sharpest?",
            "What does the Winchester text show that the Caxton text edited out, and what does the editorial history let you see about Malory?",
            "What does the epitaph at the close ('here lies Arthur, the once and future king') do that no explicit statement could?",
        ],
        "writing_invitations": [
            "The analytical paragraph on the drawing of the sword from the stone, naming what the plain prose does that elaboration could not",
            "The essay on Lancelot and Guinevere as the cycle's central failure, with passages from the middle and the close",
            "The sustained essay on what the book refuses to settle about whether the fellowship was doomed, holding three or four passages in productive tension",
        ],
        "context": (
            "Composed in prison by a knight named Sir Thomas Malory across "
            "the late 1460s; printed by Caxton in 1485 in the form that "
            "circulated for four and a half centuries; the Winchester "
            "Manuscript (an earlier, less-edited form) was rediscovered in "
            "1934 and has since been published in scholarly editions; the "
            "foundational English-language Arthurian compilation; supplied "
            "as fact, interpretation left to the student."
        ),
        "lineage": (
            "Matter of Britain. Source position: the foundational "
            "English-language Arthurian prose compilation that channels "
            "Geoffrey of Monmouth (lit-work-inh-005), the French Vulgate "
            "Cycle, and the older alliterative and stanzaic Morte poems "
            "into a single cycle. Every later English-language Arthurian "
            "work descends from Malory in some way: Tennyson "
            "(lit-work-inh-008) reads Malory through Victorian lens; "
            "T. H. White (lit-work-inh-009) takes his title from Malory's "
            "closing Latin epitaph and uses Malory as chapter source; "
            "Cornwell (lit-work-inh-010) explicitly diverges from Malory "
            "while drawing on the same materials."
        ),
        "philosophy": {
            "classical": {
                "narrative_introduction": "The foundational English-language Arthurian prose compilation; the seminar text on the cycle's long fall and on the late-medieval English prose Malory invented for it.",
                "memory_work": {
                    "recitations": [
                        "Recitation of the closing Latin epitaph and the surrounding passage of Arthur's passing"
                    ],
                },
                "recitation_routine": "Seminar opens from the recited closing; the discussion takes its first question from what the epitaph claims and what the work has earned.",
            },
            "charlotte_mason": {
                "living_book_suggestions": [
                    "A worthy edition of Le Morte d'Arthur (the Norton with the Winchester text; the Penguin two-volume Cooper edition based on Caxton; the Oxford World's Classics) read aloud across a year, in chunks",
                ],
                "short_lesson_flow": "A living book read aloud across the long span and narrated; the fellowship watched as it gathers and as it falls; deepening to analysis of the Winchester/Caxton question as the bands move up.",
                "narration_prompt": "Tell back the chapter we read today, and tell me what the fellowship gained or lost in it.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a worthy edition of Le Morte d'Arthur on the shelf, available, never assigned",
                ],
                "real_world_contexts": [
                    "Available and discussed where a student's interest in the long Arthurian cycle, in late-medieval prose, or in the inheritance from Geoffrey forward into every modern Arthurian retelling leads",
                ],
                "parent_role": "Read aloud and discuss where the student's interest leads; the year-long reading is the practice; let Lancelot and Guinevere be themselves.",
                "observation_documentation": "Over time, notice whether the student returns to particular tales and brings Malory into other reading. This noticing replaces any test.",
            },
            "traditional": {
                "introduction": "Structured study of late-medieval English prose, the cycle structure, and the Winchester/Caxton textual question where chosen.",
            },
        },
        "philosophy_neutral": {
            "montessori": "No distinct doctoral-literature method at this level.",
        },
    },
}
