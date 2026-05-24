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
