"""Pre-enriched content for Reading Foundational template nodes."""

READING_FOUNDATIONAL_CONTENT = {
    "rf-01": {
        "enriched": True,
        "learning_objectives": [
            "Identify all 26 uppercase letters by name",
            "Identify all 26 lowercase letters by name",
            "Match uppercase to lowercase letters",
            "Distinguish letters from numbers and symbols",
        ],
        "teaching_guidance": {
            "introduction": "Letters are the building blocks of reading. Each has a name, a shape (two shapes: uppercase and lowercase), and sounds. Start with the letters in the child's own name, making learning personal and meaningful.",
            "scaffolding_sequence": [
                "Learn letters in the child's first name",
                "Learn uppercase letters in groups of 3-4 using multisensory methods",
                "Practice identifying learned letters in real books and signs",
                "Introduce lowercase alongside uppercase partners",
                "Match uppercase-lowercase pairs through games and sorting",
                "Identify all 26 in random order, both cases",
            ],
            "socratic_questions": [
                "What letter does your name start with? Can you find it on this page?",
                "This letter looks like that one. How are they different?",
                "Can you find the letter M hiding somewhere in this room?",
            ],
            "practice_activities": [
                "Letter hunt: find specific letters in books, signs, packaging",
                "Form letters with playdough, sand, or finger paint",
                "Sort magnetic letters into uppercase and lowercase",
            ],
            "real_world_connections": [
                "Reading stop signs and store names",
                "Finding letters on a keyboard",
                "Letters on license plates during car rides",
            ],
            "common_misconceptions": [
                "Confusing b/d, p/q, m/w (normal at this age, not dyslexia)",
                "Thinking uppercase and lowercase are different letters",
                "Confusing letter names with letter sounds",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Names all 26 uppercase letters in random order",
                "Names all 26 lowercase letters in random order",
                "Matches all uppercase-lowercase pairs",
            ],
            "assessment_methods": ["letter card identification", "letter sorting", "environmental print reading"],
            "sample_assessment_prompts": [
                "What letter is this? (random cards)",
                "Match these uppercase letters with lowercase partners",
                "Find 5 letters you know on this cereal box",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What letter is this: A",
                "expected_type": "text",
                "correct_answer": "A",
                "hints": ["This is the first letter of the alphabet"],
                "explanation": "This is the letter A, the first letter of the alphabet.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Is this a letter or a number: 7",
                "expected_type": "text",
                "correct_answer": "number",
                "hints": ["Letters are in the alphabet. Numbers are for counting."],
                "explanation": "7 is a number, not a letter.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is the lowercase partner of B?",
                "expected_type": "text",
                "correct_answer": "b",
                "hints": ["The lowercase version is smaller and shaped a bit differently"],
                "explanation": "The lowercase partner of B is b.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Which two letters look very similar: b and d, or b and z?",
                "expected_type": "text",
                "correct_answer": "b and d",
                "hints": ["One pair is a mirror image"],
                "explanation": "b and d look similar because they are mirror images. This is why many children confuse them.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Name 5 letters you can find in the word ELEPHANT.",
                "expected_type": "text",
                "hints": ["Look at each letter one at a time"],
                "explanation": "E, L, E, P, H, A, N, T. Any 5 of these: E, L, P, H, A, N, T.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Name this letter (show random uppercase).",
                "type": "text",
                "target_concept": "uppercase_recognition",
                "rubric": "Mastery: names instantly. Proficient: names with brief hesitation. Developing: confuses with similar letters.",
            },
            {
                "prompt": "Name this letter (show random lowercase).",
                "type": "text",
                "target_concept": "lowercase_recognition",
                "rubric": "Mastery: names all instantly. Proficient: hesitates on q, g, j. Developing: confuses b/d, p/q.",
            },
            {
                "prompt": "Match these 10 uppercase letters with their lowercase partners.",
                "type": "open_response",
                "target_concept": "case_matching",
                "rubric": "Mastery: 10/10 correct. Proficient: 8-9 correct. Developing: 5-7 correct.",
            },
        ],
        "resource_guidance": {
            "required": ["alphabet cards (upper and lowercase)", "alphabet books"],
            "recommended": ["magnetic letters", "sandpaper letters", "alphabet puzzles"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 5},
        "accommodations": {
            "dyslexia": "Multisensory essential: see it, say it, trace it, build it. Extra time on b/d/p/q.",
            "adhd": "Letter hunts with movement. 2-3 letters per session max. Use games.",
            "gifted": "Move to letter sounds once names are solid. Begin CVC blending early.",
            "visual_learner": "Large colorful letter cards. Letter wall display.",
            "kinesthetic_learner": "Sandpaper letters. Form with playdough. Write in sand trays.",
            "auditory_learner": "Alphabet song variations. Say letter name while tracing.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Every letter has a name and two shapes, uppercase and lowercase. Today we learn to name all twenty-six in both cases, starting with the letters in your own name.",
                "gradual_release": {
                    "i_do": "Name letter cards aloud, beginning with the child's name letters; explicitly contrast easily confused pairs like b and d by their forms.",
                    "we_do": "Name letters together in small groups of three or four; sort magnetic letters into uppercase and lowercase; match pairs together.",
                    "you_do": "Child names all twenty-six in random order, both cases, and matches the pairs independently.",
                },
                "guided_practice": [
                    "Letter-card drills in small sets",
                    "Uppercase-to-lowercase matching games",
                ],
                "independent_practice": [
                    "Trace and name each letter",
                    "Letter-hunt worksheet in real print",
                ],
                "mastery_check": [
                    "Name all 26 uppercase and all 26 lowercase in random order",
                    "Match every uppercase to its lowercase",
                ],
                "spiral_review": [
                    "Return regularly to previously confused pairs (b/d, p/q, m/w)",
                ],
            },
            "classical": {
                "narrative_introduction": "The alphabet is the first great memory work of reading: twenty-six letters, each with a name and a form, learned in order and held by heart. Once known cold, they carry everything that follows.",
                "memory_work": {
                    "chants": [
                        "Recite or sing the alphabet A to Z daily, clearly and unrushed, pointing to each letter as it is named",
                    ],
                    "recitations": [
                        "A short alphabet rhyme committed to memory",
                    ],
                },
                "copywork": [
                    "Copy the letters in order, uppercase then lowercase, forming each carefully; this is the beginning of penmanship",
                ],
                "recitation_routine": "Recite the full alphabet at the start of each lesson, then dwell on the names and forms of a few letters.",
                "history_integration": "Tell, simply and age-appropriately, that our letters are an old human invention passed down over a very long time, tying the alphabet to the narrative of history.",
                "read_aloud_suggestions": [
                    "A beautifully illustrated classic alphabet book, read aloud for its language and pictures",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "One lovely alphabet picture book with real artwork, not a busy phonics workbook",
                ],
                "short_lesson_flow": "Look together at a single beautiful alphabet page. Find the letters of the child's own name on it. Form one or two letters in a sand tray or with a finger. Stop while interest is still high.",
                "narration_prompt": "Which letters did you find today, and where did you see them?",
                "real_world_objects": [
                    "Letters on signs during a walk",
                    "The child's own name on their belongings",
                    "Letters in the title of the current read-aloud",
                ],
                "nature_connection": "Look for letter shapes in nature, such as a forked branch shaped like Y, and note a found letter or word in the nature notebook.",
                "habit_focus": "Careful attention to one letter at a time, building the habit of looking closely.",
            },
            "montessori": {
                "prepared_materials": [
                    "Sandpaper letters (lowercase introduced first, traced while voicing the sound)",
                    "The large movable alphabet",
                    "Object and picture cards for initial sounds",
                    "Metal insets for the hand control that supports letter formation",
                ],
                "presentation": {
                    "three_period_lesson": "With the sandpaper letters, trace and voice (this says mmm); show me the m; what is this? Montessori introduces lowercase and the sound before the name and the capital.",
                    "steps": [
                        "Trace the textured letter in its writing direction while voicing it",
                        "Match small objects or picture cards to their initial letter",
                        "Compose the child's own name with the movable alphabet",
                    ],
                },
                "control_of_error": "The sandpaper texture guides the finger along the correct path, and the matching cards carry a control set, so a mismatch is visible to the child.",
                "abstraction_pathway": "From tracing the textured form (muscular memory of the shape), to composing with the movable alphabet, toward recognizing and naming letters in any print.",
                "extensions": [
                    "Build short, familiar words with the movable alphabet",
                    "Sort a basket of objects by their initial letter",
                ],
                "observation_focus": "Note sustained tracing and the child's spontaneous return to the letters, and watch that letter sounds and letter names are kept distinct. Note: authentic Montessori teaches lowercase and sounds first, deliberately diverging from an uppercase-first, letter-names framing; fidelity to the philosophy is intended.",
            },
            "unschooling": {
                "invitations": [
                    "Magnetic or foam letters on the fridge",
                    "Letter stamps, blocks, and a chalkboard left out",
                    "The child's name posted large where they will see it",
                    "Alphabet books available on a low shelf",
                ],
                "real_world_contexts": [
                    "The child's own name on their things",
                    "Letters on signs, packaging, and screens",
                    "Typing letters on a keyboard or tablet",
                    "Letters in the names of people they love",
                ],
                "conversation_starters": [
                    "That sign starts with the same letter as your name, see it?",
                    "What letter do you feel like making?",
                    "Whose name starts with B?",
                ],
                "resource_bank": [
                    "Alphabet books",
                    "Magnetic and foam letters",
                    "A label maker or letter stamps",
                    "A keyboard or a drawing app",
                    "The child's name in big letters",
                ],
                "parent_role": "Point out the letters that matter to the child first, their own initial and family names, answer what letter is that naturally, model writing in front of them, and follow their interests.",
                "observation_documentation": "Note which letters the child recognizes and writes spontaneously, especially the personally meaningful ones, and whether they tell letters apart from numbers in real print. No test; recognition emerges through meaningful print over time.",
            },
        },
        "connections": {
            "math": "Alphabetical order is sequential like number order",
            "science": "Labeling nature journal drawings",
            "history": "Letters as symbols: ancient alphabets",
        },
    },
    "rf-02": {
        "enriched": True,
        "learning_objectives": [
            "Segment spoken words into individual sounds",
            "Blend individual sounds to form words",
            "Identify beginning, middle, and ending sounds",
            "Manipulate sounds: add, delete, and substitute phonemes",
        ],
        "teaching_guidance": {
            "introduction": "Phonemic awareness is the ability to hear and work with individual sounds in spoken words. This happens WITHOUT print. It is purely auditory. The child listens, speaks, and manipulates sounds with their ears and voice before ever connecting sounds to letters.",
            "scaffolding_sequence": [
                "Identify rhyming words: do cat and hat rhyme?",
                "Isolate beginning sounds: what sound does 'dog' start with?",
                "Isolate ending sounds: what sound does 'cat' end with?",
                "Segment words into sounds: 'map' has three sounds: /m/ /a/ /p/",
                "Blend sounds into words: /s/ /u/ /n/ makes 'sun'",
                "Manipulate: change /c/ in 'cat' to /b/ and you get 'bat'",
            ],
            "socratic_questions": [
                "What sound do you hear at the beginning of 'fish'?",
                "If I say /d/ /o/ /g/, what word am I saying?",
                "What happens if I change the /c/ in 'cap' to /m/?",
            ],
            "practice_activities": [
                "Rhyming games: I say cat, you say a word that rhymes",
                "Sound boxes: push a counter into a box for each sound",
                "I Spy by sound: I spy something that starts with /b/",
            ],
            "real_world_connections": [
                "Hearing rhymes in songs and poems",
                "Playing I Spy with beginning sounds",
                "Clapping syllables in names",
            ],
            "common_misconceptions": [
                "Confusing letter names with letter sounds",
                "Thinking phonemic awareness requires letters (it doesn't)",
                "Struggling with middle vowel sounds (hardest position)",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Segments a CVC word into 3 sounds accurately",
                "Blends 3 sounds into a word",
                "Substitutes beginning sounds to make new words",
            ],
            "assessment_methods": ["oral segmenting", "oral blending", "sound manipulation games"],
            "sample_assessment_prompts": [
                "Tell me each sound in the word 'sit'",
                "What word do these sounds make: /r/ /u/ /n/?",
                "Change the first sound in 'hat' to /s/. What word?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Do 'cat' and 'bat' rhyme?",
                "expected_type": "text",
                "correct_answer": "yes",
                "hints": ["Rhyming words end with the same sound"],
                "explanation": "Yes, cat and bat rhyme because they both end with the /at/ sound.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What sound does 'sun' start with?",
                "expected_type": "text",
                "correct_answer": "/s/",
                "hints": ["Say 'sun' slowly and listen to the very first sound"],
                "explanation": "Sun starts with the /s/ sound.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What word do these sounds make: /c/ /a/ /t/?",
                "expected_type": "text",
                "correct_answer": "cat",
                "hints": ["Push the sounds together smoothly"],
                "explanation": "Blending /c/ /a/ /t/ together makes 'cat'.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "How many sounds are in the word 'ship'?",
                "expected_type": "number",
                "correct_answer": "3",
                "hints": ["sh makes ONE sound, not two"],
                "explanation": "Ship has 3 sounds: /sh/ /i/ /p/. The 'sh' is one sound even though it uses two letters.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Change the /m/ in 'map' to /t/. What new word do you get?",
                "expected_type": "text",
                "correct_answer": "tap",
                "hints": ["Keep the /a/ /p/ the same, just change the first sound"],
                "explanation": "Changing /m/ to /t/ in 'map' makes 'tap'.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Segment 'dog' into its individual sounds.",
                "type": "text",
                "correct_answer": "/d/ /o/ /g/",
                "target_concept": "segmenting",
            },
            {
                "prompt": "Blend these sounds: /f/ /i/ /sh/. What word?",
                "type": "text",
                "correct_answer": "fish",
                "target_concept": "blending",
            },
            {
                "prompt": "Say 'stop' without the /s/. What word is left?",
                "type": "text",
                "correct_answer": "top",
                "target_concept": "deletion",
            },
        ],
        "resource_guidance": {
            "required": ["no materials needed - this is purely oral"],
            "recommended": ["sound boxes with counters", "Elkonin boxes"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 10},
        "accommodations": {
            "dyslexia": "Phonemic awareness is often the core deficit. Go slowly. Extra repetition. Multisensory: tap sounds on arm.",
            "adhd": "Quick oral games. Stand up and sit down for each sound. Rhyming competitions.",
            "gifted": "Move quickly to 4-5 phoneme words. Phoneme addition and deletion.",
            "visual_learner": "Use colored counters in sound boxes to visualize each sound.",
            "kinesthetic_learner": "Tap arm for each sound. Jump for each sound. Physical segmenting.",
            "auditory_learner": "Pure strength area. Rhyming games, songs, chants.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Phonemic awareness is hearing the separate sounds inside spoken words. It is done with the ears and the voice, never with letters. Today we listen for the sounds in words, push them together to blend, and pull them apart to segment.",
                "gradual_release": {
                    "i_do": "Model with the word sun: say it slowly, stretching each sound, /s/ /u/ /n/, tapping one finger for each. Then push the three fingers together while saying sun. Name the first, middle, and last sound aloud.",
                    "we_do": "Segment and blend together on short three-sound words: the child pushes a counter for each sound heard while you both say it, then swap, you say the separate sounds and the child blends the word. Play beginning-sound I Spy together.",
                    "you_do": "Child segments three-sound words into their separate sounds, blends three sounds you say into a word, and changes the first sound of a word to make a new one, all out loud.",
                },
                "guided_practice": [
                    "Sound boxes: push one counter into a box for each sound heard in a spoken word",
                    "Rhyme sorting: decide aloud whether two spoken words rhyme",
                    "Beginning-sound match: group spoken picture names by their first sound",
                ],
                "independent_practice": [
                    "Say it slow then say it fast: the child stretches a word into its sounds, then blends it back together",
                    "Sound swap: the child changes the first or last sound of a spoken word and says the new word",
                ],
                "mastery_check": [
                    "Segment a three-sound word into its three sounds with no help",
                    "Blend three spoken sounds into the correct word",
                    "Substitute a beginning sound to make a new word",
                ],
                "spiral_review": [
                    "Return to rhyming and beginning-sound isolation before practicing the harder middle-sound and manipulation work",
                ],
            },
            "classical": {
                "narrative_introduction": "Spoken words are built of small sounds, and the trained ear can hear them one by one. Before a single letter is met, the grammar stage trains that ear through chant, rhyme, and recitation said aloud, until the sounds of language are familiar and sure.",
                "memory_work": {
                    "chants": [
                        "Chant alliterative lines daily, the same beginning sound repeated, so the ear learns to catch the first sound of a word",
                        "Clap and chant the syllables, and then the separate sounds, of short and familiar words",
                        "Chant rhyming pairs in a steady rhythm so the matching end sounds are felt as well as heard",
                    ],
                    "recitations": [
                        "Memorize and recite traditional nursery rhymes, said aloud daily, for their true rhyme and rhythm",
                        "Learn a few tongue twisters by heart and say them slowly, then quickly, to feel the repeated sounds on the tongue",
                    ],
                },
                "recitation_routine": "Begin each lesson by reciting a rhyme already known by heart, listening together for its rhyming words and its repeated sounds, before adding a new one; the ear's training is cumulative, never assumed.",
                "history_integration": "These rhymes and verses are an old inheritance, passed down by ear from one generation of children to the next long before they were ever written; learning them by listening joins the child to that oral tradition.",
                "read_aloud_suggestions": [
                    "A well-made collection of children's poetry, rich in rhyme and rhythm, read aloud with relish and a little above the child's own level so the ear is fed on the music of language",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A treasury of traditional nursery rhymes and a book of well-made children's poetry, chosen for true rhyme, strong rhythm, and lovely language, to be read and said aloud",
                ],
                "short_lesson_flow": "Say a familiar nursery rhyme together, delighting in it first. Then play gently with its sounds for a few minutes: find the words that rhyme, say one word slowly to hear its separate sounds, change a first sound to make a funny new word. Stop while the child is still enjoying it.",
                "narration_prompt": "Tell me the rhyming words you heard. Can you say me another word that would rhyme with them?",
                "real_world_objects": [
                    "A small basket of familiar objects whose names are played with sound by sound",
                    "The names of family members, said slowly and listened to one sound at a time",
                ],
                "nature_connection": "On a walk, listen for and name the sounds that are heard, and play with the sounds in the names of found things: a bird, a leaf, a stone, each said slowly to hear every sound.",
                "habit_focus": "The habit of attentive listening: hearing a word fully and exactly, and the habit of delight in the music and rhyme of words.",
            },
            "montessori": {
                "prepared_materials": [
                    "Baskets of small, familiar objects or miniatures gathered for the sound games",
                    "A quiet, unhurried space where the guide and child can listen closely together",
                    "No letters or print: the sound games precede the sandpaper letters and stay purely oral",
                ],
                "presentation": {
                    "three_period_lesson": "Adapted for the sound game. Naming: I spy, with my little eye, something that begins with /m/. Recognition: can you find something that begins with /m/? Recall: you found the mat; what sound does mat begin with? Spoken sounds only, never letter names.",
                    "steps": [
                        "Begin the I Spy sound game with beginning sounds the child hears most easily",
                        "Move to ending sounds, and then to the harder middle vowel sounds",
                        "Later, say a word in its separate sounds for the child to blend, and say a whole word for the child to break apart",
                    ],
                },
                "control_of_error": "These are oral games, so the control of error lives in the shared listening: the guide says the sound clearly, and the chosen object either does or does not begin with it, which the child hears for themselves. The guide stays light and never turns it into a drill.",
                "abstraction_pathway": "From hearing whole spoken words, to hearing and isolating the single sounds inside them, toward (in the work that follows this node) joining each sound to its sandpaper letter. This node stays in the purely oral phase.",
                "extensions": [
                    "Play the sound game with the names of family members and favorite things",
                    "Move to four and five sound words, and to taking a sound away to leave a new word",
                ],
                "observation_focus": "Watch which sound positions the child hears with ease and which are still hard, usually the middle vowel, and watch for the child asking to play the game again. Note: Montessori teaches these sound games before the sandpaper letters, so this work is deliberately kept free of print.",
            },
            "unschooling": {
                "invitations": [
                    "Sing and say nursery rhymes, jump-rope rhymes, and silly songs together, often",
                    "Play rhyming and sound games in the car, in a line, at bath time, whenever a moment opens",
                    "Make up nonsense words and silly rhymes together and laugh at them",
                ],
                "real_world_contexts": [
                    "Rhymes and repeated sounds in songs, picture books, and poems",
                    "Clapping or singing the syllables and sounds in the child's own name and family names",
                    "Tongue twisters and alliteration noticed in everyday talk",
                    "I Spy by sound, played on a walk or a drive",
                ],
                "conversation_starters": [
                    "That word sounds a lot like another word, can you hear it?",
                    "What does your name start with if you say it really slowly?",
                    "I am thinking of something in this room that starts with /b/. Can you guess it?",
                ],
                "resource_bank": [
                    "A treasury of nursery rhymes and a book of children's poetry, kept available",
                    "Songs, chants, and recordings of rhymes and stories",
                    "Picture books with strong rhyme and rhythm, read again and again because the child loves them",
                ],
                "parent_role": "Fill the day with rhyme, song, and sound play, and follow the child's delight in it. Say words slowly and playfully when a child is curious, answer real questions about how words sound, and let silly word play be its own reward rather than turning it into a lesson.",
                "observation_documentation": "Over time, notice whether the child enjoys and produces rhymes, can hear a word's first sound, and begins to pull words apart and push sounds together in play. This noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Counting sounds in words is like counting objects",
            "science": "Listening carefully to identify sounds in nature",
            "history": "Oral traditions: stories passed down by sound",
        },
    },
    "rf-03": {
        "enriched": True,
        "learning_objectives": [
            "Produce the sound each consonant makes",
            "Identify consonant sounds in initial position",
            "Identify consonant sounds in final position",
            "Distinguish between similar consonant sounds",
        ],
        "teaching_guidance": {
            "introduction": "Now we connect sounds to letters. Each consonant letter makes a specific sound. B says /b/, D says /d/, M says /m/. Start with letters that have consistent sounds (b, d, f, h, j, k, l, m, n, p, r, s, t, v, w, z) before introducing letters with multiple sounds (c, g) or silent letters.",
            "scaffolding_sequence": [
                "Introduce 3-4 consonant sounds at a time with picture cards",
                "Practice initial sounds: B is for ball, boat, bear",
                "Practice final sounds: what sound does 'web' end with?",
                "Distinguish similar sounds: /b/ vs /p/, /d/ vs /t/, /f/ vs /v/",
                "Identify consonant sounds in any position",
                "Apply to reading: see the letter, say the sound",
            ],
            "socratic_questions": [
                "What sound does the letter T make? What words start with that sound?",
                "Do B and P sound the same? How are they different?",
                "What letter makes the last sound in the word 'dog'?",
            ],
            "practice_activities": [
                "Picture sorts: sort pictures by beginning sound",
                "Sound-letter matching: hear a sound, point to the letter",
                "Beginning sound bingo",
            ],
            "real_world_connections": [
                "Letters on street signs make sounds",
                "First letter of your name makes your name's first sound",
                "Sounding out simple words on food packages",
            ],
            "common_misconceptions": [
                "Adding a vowel to consonant sounds: saying 'buh' instead of /b/",
                "Confusing voiced/unvoiced pairs: b/p, d/t, g/k",
                "Not realizing c can say /k/ or /s/",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Produces correct sound for 21 consonant letters",
                "Identifies beginning consonant sound in 10 words",
                "Identifies ending consonant sound in 10 words",
            ],
            "assessment_methods": ["letter-sound cards", "picture sorts by sound", "oral identification"],
            "sample_assessment_prompts": [
                "What sound does this letter make? (flash cards)",
                "What letter makes the first sound in 'tiger'?",
                "What letter makes the last sound in 'drum'?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What sound does the letter M make?",
                "expected_type": "text",
                "correct_answer": "/m/",
                "hints": ["Think of words: mom, map, milk"],
                "explanation": "M makes the /m/ sound, like in 'mom'.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What letter makes the first sound in 'dog'?",
                "expected_type": "text",
                "correct_answer": "d",
                "hints": ["Say 'dog' slowly. What's the first sound? What letter makes that sound?"],
                "explanation": "Dog starts with /d/, which is the letter D.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What letter makes the LAST sound in 'cat'?",
                "expected_type": "text",
                "correct_answer": "t",
                "hints": ["Say 'cat' and listen to the very end"],
                "explanation": "Cat ends with the /t/ sound, which is the letter T.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Name 3 words that start with the /s/ sound.",
                "expected_type": "text",
                "hints": ["Think of things you can see: sun, sand, ..."],
                "explanation": "Examples: sun, sit, soap, sand, six, snake.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "The letters B and P sound similar. What is different about them?",
                "expected_type": "text",
                "hints": ["Put your hand on your throat. Say /b/, then say /p/."],
                "explanation": "B is voiced (your throat vibrates) and P is unvoiced (just a puff of air). They are made in the same mouth position.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Say the sound for each letter: T, S, M, B, R.",
                "type": "open_response",
                "target_concept": "consonant_sounds",
                "rubric": "Mastery: all 5 correct and clean (no added vowel). Proficient: 4-5 correct. Developing: adds vowel sounds ('tuh' instead of /t/).",
            },
            {
                "prompt": "What letter makes the first sound in 'jump'?",
                "type": "text",
                "correct_answer": "j",
                "target_concept": "initial_consonant",
            },
            {
                "prompt": "What letter makes the last sound in 'bell'?",
                "type": "text",
                "correct_answer": "l",
                "target_concept": "final_consonant",
            },
        ],
        "resource_guidance": {
            "required": ["letter-sound cards", "picture cards for sorting"],
            "recommended": ["alphabet chart with pictures", "sound wall"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Extra time on voiced/unvoiced pairs. Multisensory: feel throat vibration for voiced sounds.",
            "adhd": "Quick-fire letter-sound games. Sort picture cards physically. 5-minute focused sessions.",
            "gifted": "Move quickly through consistent consonants. Introduce c/g duality and silent letters early.",
            "visual_learner": "Letter-sound cards with pictures. Sound wall display.",
            "kinesthetic_learner": "Mouth position awareness: feel where tongue and lips go for each sound.",
            "auditory_learner": "Pure auditory drills: hear the sound, name the letter. Sound discrimination games.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Each consonant letter stands for a sound: B says /b/, M says /m/, T says /t/. Today we learn to see a consonant and say its sound cleanly, to hear that sound at the start and the end of words, and to tell apart sounds that are easily confused.",
                "gradual_release": {
                    "i_do": "Model with a letter-sound card: name the sound cleanly, /m/, not muh, and give example words, mom, map, milk. Contrast a confusable pair by mouth position: hand on the throat, /b/ hums, /p/ is only a puff of air.",
                    "we_do": "Name the sounds together from cards in small groups of three or four. Sort picture cards by their beginning sound together, then listen for ending sounds, then swap roles.",
                    "you_do": "Child produces the clean sound for each consonant card, names the beginning and the ending consonant sound in spoken words, and tells apart a confused pair such as /b/ and /p/.",
                },
                "guided_practice": [
                    "Letter-sound card drills in small sets",
                    "Picture sorts by beginning consonant sound",
                    "Sound-to-letter matching: hear a sound, point to the letter that makes it",
                ],
                "independent_practice": [
                    "Trace each consonant while saying its clean sound",
                    "Beginning-sound hunt: find and record consonant sounds in real print",
                ],
                "mastery_check": [
                    "Produce the correct, clean sound for each consonant letter, with no added vowel",
                    "Identify the beginning consonant sound in ten spoken words",
                    "Identify the ending consonant sound in ten spoken words",
                ],
                "spiral_review": [
                    "Return regularly to the easily confused voiced and unvoiced pairs, b and p, d and t, f and v",
                ],
            },
            "classical": {
                "narrative_introduction": "Every consonant letter is a fixed sign for a fixed sound. Learn each sound surely, one at a time and mastered before the next, and the letters become a key that will unlock every word.",
                "memory_work": {
                    "chants": [
                        "Chant each consonant letter joined to its sound: B, /b/; D, /d/; M, /m/",
                        "Chant a string of example words for a sound, all beginning alike, so the ear fixes the sound to the letter",
                    ],
                    "recitations": [
                        "Recite the consonant sounds learned so far, in order, before each new one is added",
                    ],
                },
                "copywork": [
                    "Copy each consonant letter, uppercase and lowercase, while saying its sound aloud, so the hand, the eye, and the ear learn the letter together",
                ],
                "recitation_routine": "Begin each lesson by reciting the sounds already mastered before introducing the next; one sound is taught at a time, cumulatively, and never assumed.",
                "history_integration": "Tell, simply, the old story that letters were invented so that the sounds of speech could be written down and kept; learning each letter-sound joins the child to that long human work.",
                "read_aloud_suggestions": [
                    "A beautifully illustrated alphabet or sound book, read aloud, dwelling on the sound each letter makes",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "The family's current living book and a lovely alphabet picture book, where real, worthy words carry the consonant sounds, never a busy phonics workbook",
                ],
                "short_lesson_flow": "In a book being read together, pause on one good word. Say it slowly, listen for its first sound, and look at the letter that makes it. Notice the same sound at the end of another word. Attend to one or two letters only, gently, and stop while interest is high.",
                "narration_prompt": "Tell me the sound we found today, and a word of your own that begins with it.",
                "real_world_objects": [
                    "Words on signs and labels noticed on a walk",
                    "The child's own name and the names of family members",
                    "Letters in the title of the current read-aloud",
                ],
                "nature_connection": "On a nature walk, name the things that are found and listen for their beginning sounds and the letters that make them; note one found word in the nature notebook.",
                "habit_focus": "The habit of careful listening and careful looking: hearing the true, clean sound and matching it to the letter that makes it.",
            },
            "montessori": {
                "prepared_materials": [
                    "The sandpaper consonant letters, traced while the sound is voiced",
                    "Object and picture cards gathered for initial and final sounds",
                    "The large movable alphabet",
                ],
                "presentation": {
                    "three_period_lesson": "With the sandpaper letters, voicing the sound and never the letter name: this says /m/, traced this way; show me /m/; what does this say? Move slowly and lightly.",
                    "steps": [
                        "Trace the sandpaper consonant in its writing direction while voicing its clean sound",
                        "Match small objects or picture cards to the letter of their beginning sound, and later their ending sound",
                        "Play the I Spy sound game, finding things by the sound a letter makes",
                    ],
                },
                "control_of_error": "The sandpaper texture guides the finger along the letter's true path, and the matching object and picture cards carry a control set, so a wrong match shows itself to the child.",
                "abstraction_pathway": "From tracing the textured letter while voicing its sound (the sound, the shape, and the writing movement joined in the hand), toward seeing a consonant in any printed word and saying its sound at once.",
                "extensions": [
                    "Build short, familiar words with the movable alphabet",
                    "Sort a basket of objects by their ending consonant sound",
                ],
                "observation_focus": "Watch that the child voices the clean sound rather than adding a vowel, that the letter sound and the letter name are kept distinct, and that the child returns to the sandpaper letters by choice.",
            },
            "unschooling": {
                "invitations": [
                    "Keep magnetic or foam letters on the fridge and letter-sound picture books on a low shelf",
                    "Post the child's name large where they will see it daily",
                    "Leave a label maker or letter stamps out for free play",
                ],
                "real_world_contexts": [
                    "Sounding out the first letter of signs, labels, and names that catch the child's eye",
                    "The first sound of the child's own name and the names of people they love",
                    "Letters and their sounds met on packaging, screens, and street signs",
                    "Typing letters on a keyboard and hearing the sounds they spell",
                ],
                "conversation_starters": [
                    "That sign starts with the same sound as your name. Can you hear it?",
                    "What sound do you think this letter makes?",
                    "I am thinking of something here that starts with the /s/ sound.",
                ],
                "resource_bank": [
                    "Alphabet and letter-sound picture books, kept available",
                    "Magnetic and foam letters",
                    "A label maker or letter stamps, and the child's name in big letters",
                ],
                "parent_role": "Point out letters and the sounds they make as they arise in real print, saying the clean sound rather than adding a vowel. Answer what does that say naturally, and follow the child's interest in the letters and sounds that matter to them first.",
                "observation_documentation": "Over time, note which consonant sounds the child produces cleanly, whether they hear consonant sounds at the start and the end of real words, and whether they connect letters to sounds in the print they care about. This noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Letters and numbers are both symbols that represent something",
            "science": "Initial sounds of animal names during nature study",
            "history": "The invention of the alphabet: how humans started writing sounds",
        },
    },
    "rf-04": {
        "enriched": True,
        "learning_objectives": [
            "Produce the short sound for each vowel: a, e, i, o, u",
            "Identify short vowels in spoken CVC words",
            "Distinguish between the five short vowel sounds",
            "Read words with short vowel patterns",
        ],
        "teaching_guidance": {
            "introduction": "Every word needs a vowel. The five vowels (a, e, i, o, u) each have a short sound heard in simple words: apple, egg, igloo, octopus, umbrella. Short vowels are the first vowel sounds children learn because they appear in CVC words.",
            "scaffolding_sequence": [
                "Introduce short a with picture key word: apple. Practice in words: cat, hat, map",
                "Introduce short i: igloo. Words: sit, pig, big",
                "Introduce short o: octopus. Words: hot, dog, top",
                "Introduce short u: umbrella. Words: cup, bug, run",
                "Introduce short e: egg. Words: bed, pet, red",
                "Mix all five: sort words by vowel sound",
            ],
            "socratic_questions": [
                "What vowel sound do you hear in the middle of 'cat'?",
                "Do 'sit' and 'set' have the same middle sound?",
                "How many vowels are there? Can you name them?",
            ],
            "practice_activities": [
                "Vowel sort: picture cards sorted by middle vowel sound",
                "Vowel hand signs: a hand motion for each short vowel",
                "Word building with letter tiles: change the vowel to make new words (bat, bit, bot, but)",
            ],
            "real_world_connections": [
                "Short vowels in the child's name and family names",
                "Vowel sounds in animal names: cat, dog, pig, hen, bug",
                "Short vowel words on food packages: milk, egg, jam",
            ],
            "common_misconceptions": [
                "Short e and short i sound very similar (bed vs bid) and are the hardest to distinguish",
                "Confusing vowel names with vowel sounds (the letter A says /a/ not 'ay' in short vowel words)",
                "Thinking y is always a consonant (it acts as a vowel in words like 'gym')",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Produces all 5 short vowel sounds on demand",
                "Identifies the short vowel in 10 CVC words",
                "Distinguishes short e from short i in paired words",
            ],
            "assessment_methods": ["vowel sound production", "medial vowel identification", "word sorting by vowel"],
            "sample_assessment_prompts": [
                "What short sound does the letter 'o' make?",
                "What vowel sound do you hear in 'cup'?",
                "Sort these words by their vowel sound: cat, pin, dog, bed, run",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What short sound does the letter A make?",
                "expected_type": "text",
                "correct_answer": "/a/ as in apple",
                "hints": ["Think of the word 'apple'"],
                "explanation": "Short A says /a/ as in apple, cat, map.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What vowel sound do you hear in the word 'dog'?",
                "expected_type": "text",
                "correct_answer": "short o",
                "hints": ["Listen to the middle sound: d-O-g"],
                "explanation": "Dog has a short O sound in the middle.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Change the vowel in 'cat' to make a word with short 'u'. What word?",
                "expected_type": "text",
                "correct_answer": "cut",
                "hints": ["Keep the c and t, change the a to u"],
                "explanation": "Changing a to u: cat becomes cut.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Which two words have the same vowel sound: bed, bad, red?",
                "expected_type": "text",
                "correct_answer": "bed and red",
                "hints": ["Listen to the middle sound of each"],
                "explanation": "Bed and red both have short e. Bad has short a.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Name one word for each short vowel: a, e, i, o, u.",
                "expected_type": "text",
                "hints": ["Short a: cat. Short e: bed. Keep going..."],
                "explanation": "Examples: cat (a), bed (e), pig (i), dog (o), cup (u).",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Say the short sound for each vowel: a, e, i, o, u.",
                "type": "open_response",
                "target_concept": "short_vowels",
                "rubric": "Mastery: all 5 correct. Proficient: 4 correct, may confuse e/i. Developing: 2-3 correct.",
            },
            {
                "prompt": "What vowel do you hear in 'run'?",
                "type": "text",
                "correct_answer": "u",
                "target_concept": "medial_vowel",
            },
            {
                "prompt": "What vowel do you hear in 'sit'?",
                "type": "text",
                "correct_answer": "i",
                "target_concept": "medial_vowel",
            },
        ],
        "resource_guidance": {
            "required": ["vowel picture cards (apple, egg, igloo, octopus, umbrella)"],
            "recommended": ["letter tiles for word building", "vowel sorting mats"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Short e/i distinction is especially hard. Use exaggerated mouth position. Keyword pictures on desk.",
            "adhd": "Vowel songs with movement. Change vowel in word = jump to new spot.",
            "gifted": "Introduce long vowels as contrast. Compare short and long in word pairs: cap/cape.",
            "visual_learner": "Color code each vowel. Vowel chart with pictures always visible.",
            "kinesthetic_learner": "Hand signs for each vowel. Move mouth exaggeratedly for each sound.",
            "auditory_learner": "Vowel songs. Echo games: teacher says sound, child repeats with a word.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Every word needs a vowel. The five vowels each have a short sound, heard in apple, egg, igloo, octopus, and umbrella. Today we produce each short vowel sound, hear it in the middle of CVC words, and read words that follow the short vowel pattern.",
                "gradual_release": {
                    "i_do": "Model with a key-word picture: show apple, say short a, /a/, then read cat, hat, map, stretching the middle sound. Contrast the hardest pair, short e and short i, by exaggerating the mouth position in bed and bid.",
                    "we_do": "Produce the short vowel sounds together with the key-word pictures. Build words with letter tiles, changing only the vowel, bat to bit to but, and sort picture cards by their middle vowel sound.",
                    "you_do": "Child produces all five short vowel sounds on demand, names the middle vowel in spoken CVC words, and reads short vowel words independently.",
                },
                "guided_practice": [
                    "Vowel sorts: sort picture cards by their middle vowel sound",
                    "Word building with letter tiles, changing the vowel to make a new word",
                    "Read CVC words with a key-word picture available as a cue",
                ],
                "independent_practice": [
                    "Read a short list of CVC words aloud",
                    "Sort a set of written words by their vowel sound",
                ],
                "mastery_check": [
                    "Produce all five short vowel sounds on demand",
                    "Identify the short vowel in ten spoken CVC words",
                    "Distinguish short e from short i in paired words",
                ],
                "spiral_review": [
                    "Return regularly to the short e and short i contrast, the hardest pair to tell apart",
                ],
            },
            "classical": {
                "narrative_introduction": "The five vowels are the voices of our words; no word can be spoken without one. Learn each short sound surely, one vowel mastered before the next, and the short vowel words open themselves to be read.",
                "memory_work": {
                    "chants": [
                        "Chant each vowel with its key word and short sound: a, apple, /a/; e, egg, /e/",
                        "Chant a string of short vowel words that share a sound: cat, hat, map, ran",
                    ],
                    "recitations": [
                        "Recite the five vowels and their short sounds in order, a few practiced each day until all are held",
                    ],
                },
                "copywork": [
                    "Copy the vowels and short vowel CVC words neatly while saying their sounds aloud, so the written word and its sounds are learned together",
                ],
                "recitation_routine": "Begin each lesson by reciting the vowels and short sounds mastered so far before introducing the next vowel; the work is cumulative and never assumed.",
                "history_integration": "Tell, simply, that every written language has needed vowels to carry the voice of its words; the five short sounds join the child to that universal work of writing speech.",
                "read_aloud_suggestions": [
                    "A rich read-aloud above the child's level for the ear, and simple, worthy short vowel readers for the child's own first reading",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "The family's current living book and a lovely picture book built on simple words, gentle and real, never a busy phonics workbook",
                ],
                "short_lesson_flow": "In a book read together, pause on one short CVC word. Say it slowly, hear the vowel resting in the middle, and look at the letter that makes it. Attend to a single vowel, gently, and stop while the child is still interested.",
                "narration_prompt": "Tell me the vowel sound we heard in the middle today, and another little word of your own that has it.",
                "real_world_objects": [
                    "Short vowel words in the child's name and family names",
                    "Simple words on labels: milk, egg, jam",
                    "Words in the title of the current read-aloud",
                ],
                "nature_connection": "On a nature walk, name the small creatures and things that are found, cat, bug, hen, fox, and listen for the short vowel resting in the middle; note one in the nature notebook.",
                "habit_focus": "The habit of careful attention to the middle of a word, the vowel that is easiest to rush past and miss.",
            },
            "montessori": {
                "prepared_materials": [
                    "The sandpaper vowels, traced while the short sound is voiced",
                    "The large movable alphabet, with the vowels in blue and the consonants in red",
                    "Object and picture cards for short vowel CVC words",
                ],
                "presentation": {
                    "three_period_lesson": "With the sandpaper vowels, voicing the short sound: this says /a/; show me /a/; what does this say? Slowly, and with the short sound, not the letter name.",
                    "steps": [
                        "Trace the sandpaper vowel in its writing direction while voicing its short sound",
                        "Build a CVC word with the movable alphabet, the blue vowel set between two red consonants so its place is plain",
                        "Change the blue vowel for another and read the new word the change has made",
                    ],
                },
                "control_of_error": "The blue and red coloring of the movable alphabet makes the vowel's place in the word visible, and the object and picture cards carry a control set, so sounding the word out reveals a mismatch to the child.",
                "abstraction_pathway": "From tracing and voicing the sandpaper vowel, to building and changing the colored vowel in the movable alphabet (the vowel's role in the word made visible), toward reading short vowel words in any printed text.",
                "extensions": [
                    "Build many CVC words for one vowel, then for another, with the movable alphabet",
                    "Work through the object boxes of short vowel words, one box for each vowel",
                ],
                "observation_focus": "Watch whether the child hears the middle vowel, especially the close pair of short e and short i, and whether the child returns to the movable alphabet and the word building by choice.",
            },
            "unschooling": {
                "invitations": [
                    "Keep magnetic letters and letter tiles within reach for free word building",
                    "Leave simple short vowel picture books and readers on a low shelf",
                    "Post the child's name and a few short, meaningful words where they will be seen",
                ],
                "real_world_contexts": [
                    "Short vowel sounds in the family's own names",
                    "Simple words met on labels, packaging, and signs",
                    "Building and changing little words with magnetic letters in play",
                    "Reading the first short words the child wants to read in a loved book",
                ],
                "conversation_starters": [
                    "What sound do you hear right in the middle of cat?",
                    "Do sit and set sound the same in the middle, or different?",
                    "Can you change bat into bit? What did you change?",
                ],
                "resource_bank": [
                    "Magnetic letters and letter tiles",
                    "Simple short vowel readers and picture books, kept available",
                    "Word-building games and the child's name in big letters",
                ],
                "parent_role": "When a child wants to build or read a word, say its sounds slowly, including the short vowel resting in the middle, and follow the words the child cares about. Answer real questions about how words sound, and let the child's own attempts to read do the teaching rather than a drill.",
                "observation_documentation": "Over time, note which short vowels the child produces and hears, whether they catch the middle vowel of a CVC word, whether short e and short i are still blurred, and whether they are beginning to read short vowel words. This noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Vowels appear in number words: five has long i, ten has short e",
            "science": "Vowel sounds in science words: bug, egg, sun, hot, wet",
            "history": "Vowels in every language: universal building blocks of speech",
        },
    },
    "rf-05": {
        "enriched": True,
        "learning_objectives": [
            "Blend three sounds to read CVC words",
            "Segment CVC words into three sounds for spelling",
            "Read CVC words with all five short vowels",
            "Build fluency reading CVC word lists",
        ],
        "teaching_guidance": {
            "introduction": "CVC (consonant-vowel-consonant) words are the first real words a child reads. They blend three known sounds together: c-a-t becomes 'cat.' This is the moment reading clicks. Use letter tiles so the child can physically push sounds together.",
            "scaffolding_sequence": [
                "Model blending with 2-3 words: /c/ /a/ /t/ - cat",
                "Child blends with teacher support: say each sound, then blend",
                "Child blends independently with CVC word cards",
                "Reverse: hear a word, segment into sounds, spell with tiles",
                "Read CVC words in simple phrases: 'the big cat sat'",
                "Build speed: read CVC word lists fluently",
            ],
            "socratic_questions": [
                "What sounds do you hear in 'map'?",
                "If you push /s/ /i/ /t/ together fast, what word do you get?",
                "You can read 'cat.' What if I change the c to an h?",
            ],
            "practice_activities": [
                "Word building with letter tiles: build, read, change one letter, read again",
                "CVC word bingo",
                "Decodable sentence strips using only CVC words",
            ],
            "real_world_connections": [
                "CVC words are everywhere: the, cat, dog, run, big, hot, red",
                "Reading simple labels and signs",
                "Writing notes: 'I can sit. The dog is big.'",
            ],
            "common_misconceptions": [
                "Sounding out each letter separately without blending into a word",
                "Guessing from the first letter instead of decoding all three sounds",
                "Reading too fast before accuracy is established",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Reads 30 CVC words correctly in one minute",
                "Spells 10 CVC words from dictation",
                "Reads CVC words in connected text",
            ],
            "assessment_methods": ["word list reading", "spelling dictation", "decodable text reading"],
            "sample_assessment_prompts": [
                "Read these words: cat, pin, dog, bed, run, hat, fix, log, wet, cup",
                "Spell these words: sit, map, rug",
                "Read this sentence: The fat cat sat on a mat.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Blend these sounds into a word: /s/ /a/ /t/",
                "expected_type": "text",
                "correct_answer": "sat",
                "hints": ["Push the sounds together smoothly: sss-aaa-t"],
                "explanation": "Blending /s/ /a/ /t/ makes 'sat'.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Read this word: PIG",
                "expected_type": "text",
                "correct_answer": "pig",
                "hints": ["Sound it out: /p/ /i/ /g/"],
                "explanation": "P-I-G: /p/ /i/ /g/ = pig.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Spell the word 'cup'. What letters do you need?",
                "expected_type": "text",
                "correct_answer": "c-u-p",
                "hints": ["Listen: /c/ /u/ /p/. What letter makes each sound?"],
                "explanation": "Cup is spelled c-u-p.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Change the first letter in 'hat' to 's'. What new word?",
                "expected_type": "text",
                "correct_answer": "sat",
                "hints": ["Keep the -at, change h to s"],
                "explanation": "Changing h to s: hat becomes sat.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Read this sentence: The big red bus ran.",
                "expected_type": "text",
                "correct_answer": "The big red bus ran.",
                "hints": ["Sound out each word you don't know"],
                "explanation": "Each word is decodable: the (sight word), big, red, bus, ran.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Read these 5 words: cat, pin, mug, bed, fox.",
                "type": "open_response",
                "target_concept": "cvc_reading",
                "rubric": "Mastery: reads all 5 accurately in under 10 seconds. Proficient: reads 4-5 with some sounding out. Developing: reads 2-3 with support.",
            },
            {
                "prompt": "Spell the word 'net'.",
                "type": "text",
                "correct_answer": "net",
                "target_concept": "cvc_spelling",
            },
            {
                "prompt": "What sounds are in 'hop'?",
                "type": "text",
                "correct_answer": "/h/ /o/ /p/",
                "target_concept": "segmenting",
            },
        ],
        "resource_guidance": {
            "required": ["letter tiles or magnetic letters", "CVC word cards"],
            "recommended": ["decodable readers", "word family flip books"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Extra blending practice with continuous sounds (mmm-aaa-p) before stop sounds. Finger tapping each sound.",
            "adhd": "Word building races. Letter tile manipulation keeps hands busy. Decodable games.",
            "gifted": "Move to CCVC and CVCC words quickly (stop, lamp). Introduce blends.",
            "visual_learner": "Letter tiles in bright colors. Arrows showing left-to-right blending direction.",
            "kinesthetic_learner": "Slide finger under each letter while blending. Push tiles together physically.",
            "auditory_learner": "Exaggerated blending: stretch each sound, then snap together.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "CVC words are the first real words a child reads: three known sounds blended in order, so c, a, t becomes cat. Today we blend three sounds to read CVC words with all five short vowels, take words apart into sounds to spell them, and build smooth, fluent reading.",
                "gradual_release": {
                    "i_do": "Model blending with letter tiles: lay c, a, t, say each sound, push the tiles together, sweep a finger underneath, and read cat. Then model segmenting: hear map, say each sound, and build it with tiles.",
                    "we_do": "Blend with support, the child saying each sound and then blending the whole word. Together, segment a spoken word and spell it with tiles, and read a CVC word inside a simple phrase.",
                    "you_do": "Child blends CVC word cards independently, segments spoken words into sounds to spell them, and reads a short CVC word list smoothly.",
                },
                "guided_practice": [
                    "Blend CVC words by pushing letter tiles together",
                    "Read word families together: cat, hat, mat, sat",
                    "Segment a spoken word and spell it with tiles",
                ],
                "independent_practice": [
                    "Read CVC word cards and simple decodable phrases",
                    "Reread a familiar CVC list to build smoothness and speed",
                ],
                "mastery_check": [
                    "Blend any CVC word with any of the five short vowels",
                    "Segment a CVC word into its three sounds to spell it",
                    "Read a short CVC word list fluently",
                ],
                "spiral_review": [
                    "Revisit the short vowel sounds and the consonant sounds before building harder CVC fluency",
                ],
            },
            "classical": {
                "narrative_introduction": "The CVC word is the first true brick of reading: three sounds, blended in their order, become a word. Master this pattern surely, before any other, and every later pattern of reading is built upon it.",
                "memory_work": {
                    "chants": [
                        "Chant word families in rhythm: cat, hat, mat, sat, pat",
                        "Chant the blending sweep: /c/, /a/, /t/, cat",
                        "Chant short lists of CVC words gathered by their vowel",
                    ],
                    "recitations": [
                        "Read aloud a short list of CVC words each day, cleanly and without rushing, until the pattern is sure",
                    ],
                },
                "copywork": [
                    "Copy CVC words neatly while sounding them out, joining the reading of a word to the writing of it",
                ],
                "recitation_routine": "Begin each lesson by re-reading the CVC words and word families learned so far before adding new ones; the pattern is rehearsed cumulatively, never assumed.",
                "history_integration": "Tell, simply, that writing a word by joining its letter-sounds is an old human craft; reading these first words joins the child to that long story.",
                "read_aloud_suggestions": [
                    "A rich read-aloud above the child's level for the ear, and simple, worthy decodable books for the child's own first reading",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "Simple, worthy decodable books whose short sentences tell of real things, alongside the family's current living read-aloud",
                ],
                "short_lesson_flow": "Read a few CVC words, or one short decodable sentence, together and attentively, blending each word with care. Talk for a moment about what it says. Take one short turn only, and stop while the child is still glad to be reading.",
                "narration_prompt": "Tell me what the words said, and which word you are most proud of having read.",
                "real_world_objects": [
                    "The child's own name and short names of family members",
                    "Short words on labels and signs",
                    "The words in a simple decodable book about real things",
                ],
                "nature_connection": "Read or write little CVC words for things found on a walk, bug, cat, hen, sun, and note one of them in the nature notebook.",
                "habit_focus": "The habit of careful, unhurried reading: sounding each word truly through, rather than guessing it from its first letter.",
            },
            "montessori": {
                "prepared_materials": [
                    "The large movable alphabet, vowels in blue and consonants in red",
                    "The pink series object boxes, small objects matched to short-vowel CVC words",
                    "The pink series word cards and picture cards",
                ],
                "presentation": {
                    "three_period_lesson": "With a built word and its object: this says cat; show me cat; what does this say? The word built, sounded, and then read.",
                    "steps": [
                        "Build a CVC word with the movable alphabet, sounding each letter as it is laid down",
                        "Sweep beneath the word to blend the sounds and read it",
                        "Match the pink series word cards to their objects, sounding each word out to check",
                    ],
                },
                "control_of_error": "Each pink series word card has its own object or picture, so a word that does not match the object it is paired with reveals a misread to the child without an adult's word.",
                "abstraction_pathway": "From building the word with the movable alphabet (the word made by the hand, sound by sound), to reading the pink series cards, toward reading CVC words in any book with no material at all.",
                "extensions": [
                    "Work through longer pink series word lists and read pink series phrases",
                    "Write CVC words from the objects in the pink series boxes",
                ],
                "observation_focus": "Watch for the moment blending clicks into reading, for the child reading the word rather than only building it, and for free return to the pink series work.",
            },
            "unschooling": {
                "invitations": [
                    "Keep letter tiles and magnetic letters within reach for free word building",
                    "Leave simple decodable books and picture books on a low shelf",
                    "Post the child's name and a few short, meaningful words where they will be seen",
                ],
                "real_world_contexts": [
                    "Reading the first short words a child wants to read, on signs, labels, and in a loved book",
                    "Building and reading little words with magnetic letters in play",
                    "Short words in the names of people and pets the child loves",
                ],
                "conversation_starters": [
                    "Can you sound that word out with me? /c/, /a/, /t/.",
                    "What little word could you make with these letters?",
                    "You read sun. What other word has that sound in the middle?",
                ],
                "resource_bank": [
                    "Magnetic letters and letter tiles",
                    "Simple decodable readers and picture books, kept available",
                    "Word-building games and the child's name in big letters",
                ],
                "parent_role": "When a child wants to read a word, sound it slowly alongside them and let them blend it themselves. Follow the words the child cares about, celebrate the moment reading clicks, and let real reading attempts do the teaching rather than a drill.",
                "observation_documentation": "Over time, note whether the child blends three sounds into a word, segments words to spell them, reads CVC words across all five short vowels, and whether the reading is growing smooth. This noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Three parts (C-V-C) like three addends",
            "science": "CVC science words: bug, sun, log, wet, hot, fog",
            "history": "The first words people wrote were simple like CVC words",
        },
    },
    "rf-06": {
        "enriched": True,
        "learning_objectives": [
            "Read words with initial consonant blends (bl, cr, st, tr, etc.)",
            "Read words with final consonant blends (nd, mp, st, nk, etc.)",
            "Distinguish blends from digraphs",
            "Spell words with blends",
        ],
        "teaching_guidance": {
            "introduction": "Consonant blends are two or three consonant letters whose sounds blend together but each is still heard: 'bl' in 'black' blends /b/ and /l/ - you hear both. This is different from digraphs (sh, ch) where two letters make one new sound.",
            "scaffolding_sequence": [
                "Introduce initial l-blends: bl, cl, fl, gl, pl, sl",
                "Introduce initial r-blends: br, cr, dr, fr, gr, pr, tr",
                "Introduce initial s-blends: sc, sk, sl, sm, sn, sp, st, sw",
                "Introduce final blends: nd, nk, nt, mp, st, ft, lk, lt",
                "Read blend words in sentences",
                "Distinguish blends from digraphs",
            ],
            "socratic_questions": [
                "In the word 'stop,' how many sounds do you hear at the beginning?",
                "Can you hear both the /s/ and /t/ in 'stop'?",
                "How is 'ch' different from 'cl'? In 'ch' you hear one sound, in 'cl' you hear...?",
            ],
            "practice_activities": [
                "Blend sorting: sort words by initial blend",
                "Build blend words with letter tiles",
                "Blend word ladders: change one blend to make a new word",
            ],
            "real_world_connections": [
                "Blend words everywhere: stop, green, blue, black, drink, sleep",
                "Street signs: STOP, SLOW",
                "Daily words: brush, step, plant, drink, sleep",
            ],
            "common_misconceptions": [
                "Dropping one sound from the blend (saying 'top' instead of 'stop')",
                "Inserting a vowel between blend letters ('suh-top' instead of 'stop')",
                "Confusing blends and digraphs",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Reads words with initial blends accurately",
                "Reads words with final blends accurately",
                "Spells blend words from dictation",
            ],
            "assessment_methods": ["blend word lists", "dictation", "reading in context"],
            "sample_assessment_prompts": [
                "Read: stop, clap, frog, drum, plant",
                "Spell: trip, band, stamp",
                "Read: The frog swam to the flat rock and sat in the sun.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Read this word: STOP",
                "expected_type": "text",
                "correct_answer": "stop",
                "hints": ["Blend the s and t together: /st/, then add /o/ /p/"],
                "explanation": "S-T-O-P: blend /st/ with /o/ /p/ = stop.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Read this word: CLAP",
                "expected_type": "text",
                "correct_answer": "clap",
                "hints": ["/cl/ then /a/ /p/"],
                "explanation": "C-L-A-P: /cl/ /a/ /p/ = clap.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Read this word: STAMP",
                "expected_type": "text",
                "correct_answer": "stamp",
                "hints": ["Initial blend /st/, short a, final blend /mp/"],
                "explanation": "ST-A-MP: initial blend st, vowel a, final blend mp.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Spell the word 'trip'.",
                "expected_type": "text",
                "correct_answer": "trip",
                "hints": ["Initial blend /tr/, short i, ends with /p/"],
                "explanation": "Trip: t-r-i-p.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Read this sentence: The frog hid in the grass by the pond.",
                "expected_type": "text",
                "correct_answer": "The frog hid in the grass by the pond.",
                "hints": ["Watch for blends: fr, gr, nd"],
                "explanation": "Blend words: frog (fr), grass (gr), pond (nd).",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Read these blend words: black, step, frog, drum, plant.",
                "type": "open_response",
                "target_concept": "blends",
                "rubric": "Mastery: all 5 accurate and fluent. Proficient: 4-5 with some sounding out. Developing: drops blend sounds.",
            },
            {
                "prompt": "Spell 'best'.",
                "type": "text",
                "correct_answer": "best",
                "target_concept": "final_blend_spelling",
            },
            {
                "prompt": "Is 'bl' a blend or a digraph? Why?",
                "type": "open_response",
                "target_concept": "blend_vs_digraph",
                "rubric": "Mastery: blend because you hear both sounds. Proficient: says blend. Developing: confuses with digraph.",
            },
        ],
        "resource_guidance": {
            "required": ["letter tiles including blend cards", "blend word lists"],
            "recommended": ["decodable readers with blends", "blend sorting mats"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Practice blends with continuous sounds first (sl, sn, sm) before stop-sound blends (st, sk, sp).",
            "adhd": "Blend building with magnetic letters on a cookie sheet. Physical word construction.",
            "gifted": "Three-letter blends: str, spr, scr. CCVCC words: stamp, drink.",
            "visual_learner": "Blend cards with both letters together. Color the blend as one unit.",
            "kinesthetic_learner": "Slide two letter tiles together to physically show blending.",
            "auditory_learner": "Exaggerate each sound in the blend, then speed up until blended.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "A consonant blend is two or three consonants whose sounds you still hear each of: the bl in black is /b/ and /l/, both heard. That is different from a digraph like sh, where two letters make one new sound. Today we read words with initial and final blends, spell them, and tell blends apart from digraphs.",
                "gradual_release": {
                    "i_do": "Model reading black: stretch the blend, /b/ /l/, hear both consonants, then read the whole word. Build a blend word with letter tiles. Contrast a blend, st in stop, with a digraph, sh in ship, naming the difference.",
                    "we_do": "Read blend words together by family, the l-blends, then the r-blends, then the s-blends, then the final blends. Spell a blend word with tiles together, and sort words into blends and digraphs.",
                    "you_do": "Child reads words with initial and final blends, spells blend words with tiles, and sorts blends from digraphs.",
                },
                "guided_practice": [
                    "Read blend words by family with letter tiles, hearing each consonant",
                    "Read words with final blends such as nd, mp, st, nk",
                    "Sort a set of words into blends and digraphs",
                ],
                "independent_practice": [
                    "Read blend words inside simple sentences",
                    "Spell blend words from dictation with tiles or by writing",
                ],
                "mastery_check": [
                    "Read words with initial and with final consonant blends",
                    "Spell a word that contains a blend",
                    "Explain how a blend differs from a digraph",
                ],
                "spiral_review": [
                    "Revisit CVC blending and the single consonant sounds before practicing harder blend words",
                ],
            },
            "classical": {
                "narrative_introduction": "A blend is a meeting of consonants in which each keeps its own sound. Learn the blends in their orderly families, the l-blends, the r-blends, the s-blends, and the final blends, and harder words open themselves to be read.",
                "memory_work": {
                    "chants": [
                        "Chant a blend family in rhythm: bl, cl, fl, gl, pl, sl",
                        "Chant blend words that share a blend: stop, step, star, stem",
                        "Chant the distinction: a blend keeps both sounds, a digraph makes one new sound",
                    ],
                    "recitations": [
                        "Recite the blend families learned so far before a new family is added",
                    ],
                },
                "copywork": [
                    "Copy blend words neatly while sounding the blend aloud, so each consonant of the cluster is heard and written",
                ],
                "recitation_routine": "Begin each lesson by re-reading the blends and blend words mastered so far before adding the next family; the work is cumulative and never assumed.",
                "history_integration": "Tell, simply, that these clusters of consonants were carried into our spelling from older forms of the language; the blends are a small piece of the long history of words.",
                "read_aloud_suggestions": [
                    "A rich read-aloud for the ear, and decodable books that bring blend words into real sentences",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "Simple decodable books in which blend words appear in real sentences, alongside the family's current living read-aloud",
                ],
                "short_lesson_flow": "In a book read together, meet a word that holds a blend. Say it slowly, and hear that both consonants of the blend are sounded. Attend to a single blend, gently, and stop while the child is still interested.",
                "narration_prompt": "Tell me the blend word we read today, and another word of your own that begins or ends the same way.",
                "real_world_objects": [
                    "Blend words noticed on signs and labels, such as stop and exit",
                    "Blend sounds in the names of people and places the child knows",
                    "Words in the current read-aloud that hold a blend",
                ],
                "nature_connection": "On a nature walk, notice the blend words for things that are found, frog, snail, crab, stem, and note one in the nature notebook.",
                "habit_focus": "The habit of careful listening for every sound: hearing each consonant of a cluster rather than dropping one.",
            },
            "montessori": {
                "prepared_materials": [
                    "The large movable alphabet for building blend words",
                    "The green series object boxes, objects matched to words with blends and longer patterns",
                    "The green series word cards and picture cards",
                ],
                "presentation": {
                    "three_period_lesson": "With a built blend word and its object: this says flag; show me flag; what does this say? The word built, the blend sounded, and then read.",
                    "steps": [
                        "Build a blend word with the movable alphabet, sounding each consonant of the blend as it is laid down",
                        "Sweep beneath the word to blend the sounds and read it",
                        "Match the green series word cards to their objects, sounding each blend out to check",
                    ],
                },
                "control_of_error": "Each green series word card has its own object or picture, so a word that does not match its pair reveals a dropped consonant or a misread to the child.",
                "abstraction_pathway": "From building the blend word with the movable alphabet (each consonant of the cluster sounded by the hand), to reading the green series cards, toward reading blend words in any text.",
                "extensions": [
                    "Work through longer green series word lists and final-blend words",
                    "Sort words into blends and digraphs with the materials",
                ],
                "observation_focus": "Watch that the child sounds every consonant of a blend rather than dropping one, and returns to the green series work by choice.",
            },
            "unschooling": {
                "invitations": [
                    "Keep letter tiles within reach, including ones that make building blend words easy",
                    "Leave decodable books that hold blend words on a low shelf",
                    "Set out word-building games and post a few blend words where they will be seen",
                ],
                "real_world_contexts": [
                    "Reading blend words that appear on signs, such as stop and exit",
                    "Blend sounds in the names of people, pets, and places the child loves",
                    "Building and reading blend words with magnetic letters in play",
                ],
                "conversation_starters": [
                    "That word has two sounds pushed together at the start. Can you hear them both, /s/ and /t/?",
                    "What other words start the same way as stop?",
                    "Is ship two sounds blended, or two letters making one new sound?",
                ],
                "resource_bank": [
                    "Magnetic letters and letter tiles",
                    "Decodable readers that include blend words, kept available",
                    "Word-building games",
                ],
                "parent_role": "When a blend word comes up in real reading, sound the cluster slowly together so each consonant is heard, and follow the words the child wants to read. Let real reading attempts do the teaching rather than a drill.",
                "observation_documentation": "Over time, note whether the child reads initial and final blends, hears every consonant of a cluster, tells a blend apart from a digraph, and spells words with blends. This noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Blending sounds is like adding groups: two sounds combined",
            "science": "Blend words in science: plant, stem, frost, blend, crust",
            "history": "Blend words in history: draft, grand, craft, trench",
        },
    },
    "rf-07": {
        "enriched": True,
        "learning_objectives": [
            "Read CVCe words where the silent e makes the vowel say its name",
            "Spell CVCe words accurately from dictation",
            "Explain the silent-e rule in child-friendly language",
            "Compare CVC and CVCe word pairs to identify the vowel sound change",
        ],
        "teaching_guidance": {
            "introduction": "The silent-e pattern is one of the most powerful phonics rules a child learns. When an e sits at the end of a word, it doesn't make a sound itself — instead it reaches back over the consonant and makes the vowel 'say its name.' Compare 'cap' to 'cape': the e changes the short /a/ to a long /ā/. This is sometimes called 'magic e' or 'bossy e.'",
            "scaffolding_sequence": [
                "Use letter tiles to build a CVC word like 'cap,' then physically add an e tile to the end and read 'cape'",
                "Practice with a-e pairs: cap/cape, tap/tape, mat/mate, pan/pane",
                "Extend to i-e pairs: pin/pine, kit/kite, rid/ride, bit/bite",
                "Extend to o-e pairs: hop/hope, rob/robe, not/note, cod/code",
                "Practice u-e pairs: cub/cube, tub/tube, cut/cute, us/use",
                "Read CVCe words in isolation from flash cards without the CVC comparison",
                "Read CVCe words in connected sentences and short passages",
                "Spell CVCe words from dictation without seeing the word first",
            ],
            "socratic_questions": [
                "What happens to the vowel sound when I add an e to the end of 'hop'?",
                "The word is 'pine.' Does the e at the end make a sound? What does it do instead?",
                "If I cover up the e in 'cape,' what word do I have now? What changed?",
                "How can you tell if a word has a long vowel or a short vowel just by looking at it?",
            ],
            "practice_activities": [
                "CVC-to-CVCe flip cards: write a CVC word on a card with a flap that adds e, read both versions",
                "Magic e wand: use a craft stick labeled 'e' and touch it to CVC word cards to transform them",
                "Word pair memory game: match CVC cards to their CVCe partners (cap/cape, hop/hope)",
                "Sentence building: use letter tiles to build sentences using CVCe words (The kite can ride the wind)",
            ],
            "real_world_connections": [
                "CVCe words on road signs and store names: SALE, HOME, BIKE",
                "Recipe words: bake, cake, rice, wine (grape juice for kids)",
                "Nature words: pine, lake, stone, vine, cave",
                "Everyday objects: tape, rope, tube, bone, cube",
            ],
            "common_misconceptions": [
                "Pronouncing the final e as a separate sound ('cape-uh' instead of 'cape')",
                "Applying the silent-e rule to words where it doesn't work (have, give, come — these are exceptions)",
                "Forgetting the silent e when spelling: writing 'hop' when meaning 'hope'",
                "Thinking every word ending in e follows the CVCe pattern (words like 'three' and 'these' are different patterns)",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Reads 20 CVCe words accurately without hesitation",
                "Spells 10 CVCe words correctly from dictation",
                "Explains that the silent e makes the vowel say its name",
            ],
            "proficiency_indicators": [
                "Reads most CVCe words with brief sounding out",
                "Spells CVCe words correctly most of the time, occasionally forgetting the final e",
            ],
            "developing_indicators": [
                "Reads CVCe words when given the CVC comparison as a hint",
                "Needs reminding that the e is silent and changes the vowel",
            ],
            "assessment_methods": ["word list reading", "CVC/CVCe pair sorting", "spelling dictation"],
            "sample_assessment_prompts": [
                "Read these words: cake, pine, home, tube, lake",
                "Sort these words into short vowel and long vowel groups: cap, cape, hop, hope, kit, kite",
                "Spell these words: bike, rope, name",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Read this word: CAKE",
                "expected_type": "text",
                "correct_answer": "cake",
                "hints": ["The e at the end is silent. It makes the a say its name: /ā/"],
                "explanation": "C-A-K-E: the silent e makes the a say /ā/. The word is 'cake.'",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What happens when you add an e to the word 'hop'?",
                "expected_type": "text",
                "correct_answer": "hope",
                "hints": ["The e makes the o say its name: /ō/"],
                "explanation": "Adding e to 'hop' makes 'hope.' The o changes from short /o/ to long /ō/.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Which word has a long vowel sound: 'cap' or 'cape'?",
                "expected_type": "multiple_choice",
                "options": ["cap", "cape"],
                "correct_answer": "cape",
                "hints": ["Look for the silent e at the end"],
                "explanation": "Cape has a long vowel because the silent e makes the a say its name.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Spell the word that means a flying toy on a string (rhymes with 'bite').",
                "expected_type": "text",
                "correct_answer": "kite",
                "hints": ["It has a long i sound. Don't forget the silent e!"],
                "explanation": "Kite is spelled k-i-t-e. The silent e makes the i say /ī/.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Read this sentence: The snake hid in the cave by the lake.",
                "expected_type": "text",
                "correct_answer": "The snake hid in the cave by the lake.",
                "hints": ["Find the CVCe words: snake, cave, lake. The e is silent in each one."],
                "explanation": "Three CVCe words: snake (long a), cave (long a), lake (long a). The silent e makes each vowel long.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Read these CVCe words: rope, bike, cute, name, stone.",
                "type": "open_response",
                "target_concept": "cvce_reading",
                "rubric": "Mastery: reads all 5 fluently. Proficient: reads 4-5 with some sounding out. Developing: reads short vowel sound instead of long.",
            },
            {
                "prompt": "Spell 'home'.",
                "type": "text",
                "correct_answer": "home",
                "target_concept": "cvce_spelling",
            },
            {
                "prompt": "What does the silent e do in the word 'pine'?",
                "type": "open_response",
                "target_concept": "silent_e_rule",
                "rubric": "Mastery: explains that e makes the i say its name. Proficient: says it changes the sound. Developing: cannot explain.",
            },
        ],
        "resource_guidance": {
            "required": ["letter tiles or magnetic letters", "CVC/CVCe word pair cards"],
            "recommended": ["decodable readers featuring CVCe words", "magic e wand (craft stick with e)"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Use Orton-Gillingham multisensory approach: see the word, say the sounds, trace it, write it. Color the silent e in red so it stands out visually. Practice CVC/CVCe pairs side by side with physical letter tiles.",
            "adhd": "Keep sessions to 10-15 minutes. Use the magic e wand as a physical prop to maintain engagement. Turn CVC-to-CVCe transformations into a game with points.",
            "gifted": "Introduce CVCe exception words (have, give, come, love) as challenge words. Begin two-syllable words with silent-e syllables (cupcake, mistake).",
            "visual_learner": "Color-code the silent e differently from other letters. Use arrows showing the e 'reaching back' to change the vowel.",
            "kinesthetic_learner": "Physically slide an e tile onto CVC words. Karate-chop between sounds while decoding.",
            "auditory_learner": "Emphasize the vowel sound change aloud: 'hop... hope!' Exaggerate the long vowel.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "The silent e is a powerful rule. An e at the end of a word makes no sound itself; it reaches back over the consonant and makes the vowel say its name, so cap becomes cape. Today we read and spell CVCe words and learn the rule that governs them.",
                "gradual_release": {
                    "i_do": "Model with letter tiles: build cap, read it, then add an e tile to the end and read cape. Explain that the silent e changed the short /a/ to the long /a/, the vowel saying its name.",
                    "we_do": "Build CVC-to-CVCe pairs together, tap and tape, pin and pine, reading both and naming what the e did. Spell a CVCe word from dictation together.",
                    "you_do": "Child reads CVCe words, spells them from dictation, explains the silent-e rule in their own words, and compares a CVC and CVCe pair to name the vowel-sound change.",
                },
                "guided_practice": [
                    "CVC-to-CVCe flip cards: read the word, add the e, read it again",
                    "Match CVC word cards to their CVCe partners",
                    "Read CVCe words inside simple sentences",
                ],
                "independent_practice": [
                    "Read CVCe word lists and short passages",
                    "Spell CVCe words from dictation",
                ],
                "mastery_check": [
                    "Read CVCe words with all four long-vowel patterns accurately",
                    "Spell CVCe words from dictation",
                    "Explain the silent-e rule and name the vowel change in a CVC and CVCe pair",
                ],
                "spiral_review": [
                    "Revisit short-vowel CVC reading alongside CVCe so the two patterns stay distinct",
                ],
            },
            "classical": {
                "narrative_introduction": "Among the first great rules of reading is the silent e: the letter that says nothing yet changes everything, reaching back across the consonant to make the vowel say its name. Learn the rule surely, and a whole class of words opens to be read.",
                "memory_work": {
                    "chants": [
                        "Chant CVC and CVCe pairs in rhythm: cap, cape; tap, tape; pin, pine",
                        "Chant the rule: a silent e at the end makes the vowel say its name",
                        "Chant CVCe word sets gathered by their vowel",
                    ],
                    "recitations": [
                        "Recite the silent-e rule, and read CVCe word lists aloud cleanly, mastering the a-e words before the i-e, o-e, and u-e words",
                    ],
                },
                "copywork": [
                    "Copy CVCe words and CVC-to-CVCe pairs neatly while reading them, so the silent e is written as carefully as it is read",
                ],
                "recitation_routine": "Begin each lesson by reciting the rule and re-reading the CVCe words learned so far before adding new ones; one vowel pattern is mastered before the next, cumulatively.",
                "history_integration": "Tell, simply, that the silent e is a relic of older English, where that final e was once truly sounded; our spelling has kept the letter even after its sound fell away.",
                "read_aloud_suggestions": [
                    "A rich read-aloud for the ear, and simple readers built on the silent-e pattern for the child's own reading",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "The family's current living read-aloud and simple readers in which CVCe words appear in real, worthy sentences",
                ],
                "short_lesson_flow": "In a book read together, meet a CVCe word. Say it, and notice the e at the end that says nothing yet makes the vowel say its name. Compare it for a moment with a short-vowel word. Take one short turn, and stop while the child is still glad to be reading.",
                "narration_prompt": "Tell me what the silent e did to the word we read, and another word of your own where it does the same thing.",
                "real_world_objects": [
                    "CVCe words on signs and store fronts, such as SALE, HOME, and BIKE",
                    "Nature words that follow the pattern: pine, lake, stone, vine, cave",
                    "Everyday objects whose names are CVCe words: tape, rope, bone, cube",
                ],
                "nature_connection": "On a nature walk, notice CVCe words for things that are found, pine, lake, vine, stone, and write one of them in the nature notebook.",
                "habit_focus": "The habit of attentive looking: noticing the quiet e at a word's end that changes how the whole word is read.",
            },
            "montessori": {
                "prepared_materials": [
                    "The large movable alphabet for building CVC words and adding the silent e",
                    "The green series CVCe word cards with their matching objects",
                    "The blue-to-green series materials that bridge from short vowels to the silent-e pattern",
                ],
                "presentation": {
                    "three_period_lesson": "With a built CVCe word and its object: this says cape; show me cape; what does this say? The word built, the change heard, and then read.",
                    "steps": [
                        "Build a CVC word with the movable alphabet and read it",
                        "Add the silent e to the end and read aloud how the vowel changes to say its name",
                        "Match the green series CVCe word cards to their objects, reading each to check",
                    ],
                },
                "control_of_error": "Each green series CVCe word card has its own object or picture, so a word that does not match its pair reveals a misread to the child without an adult's word.",
                "abstraction_pathway": "From building the CVC word and adding the e by hand (the silent-e rule made physical), to reading the green series cards, toward reading CVCe words in any book with no material.",
                "extensions": [
                    "Work through green series CVCe word lists and read CVCe phrases",
                    "Spell CVCe words from the objects in the green series boxes",
                ],
                "observation_focus": "Watch for the child applying the silent-e rule by choice, reading the vowel long, and not sounding the final e as a separate sound.",
            },
            "unschooling": {
                "invitations": [
                    "Keep letter tiles within reach, including a spare e tile or a craft stick labelled e to add to words",
                    "Leave simple readers that use CVCe words on a low shelf",
                    "Post a few CVCe words that matter to the child where they will be seen",
                ],
                "real_world_contexts": [
                    "CVCe words on signs and store names, such as SALE, HOME, and BIKE",
                    "CVCe words in loved books and in the names of people and places",
                    "Building and transforming CVC words into CVCe words with magnetic letters in play",
                ],
                "conversation_starters": [
                    "What happens if we add an e to the end of hop?",
                    "This word ends in e, but you do not hear it. What do you think it is doing?",
                    "If I cover the e in cape, what word do you have now? What changed?",
                ],
                "resource_bank": [
                    "Magnetic letters and letter tiles",
                    "Simple decodable readers that include CVCe words, kept available",
                    "Word-building games",
                ],
                "parent_role": "When a CVCe word comes up in real reading, point out the silent e and what it does to the vowel, and follow the words the child wants to read. Let real reading attempts do the teaching rather than a drill.",
                "observation_documentation": "Over time, note whether the child reads CVCe words, applies the silent-e rule on their own, spells words with the silent e, and can compare a CVC and CVCe pair. This noticing replaces any test.",
            },
        },
        "connections": {
            "math": "The silent e changes value like a zero changes place value: 1 vs 10",
            "science": "CVCe words in nature: stone, lake, pine, vine, bone, cave",
            "history": "The English language borrowed the silent-e pattern; spelling has a history",
        },
    },
    "rf-08": {
        "enriched": True,
        "learning_objectives": [
            "Read words containing common vowel teams: ai, ay, ee, ea, oa, ow",
            "Identify the vowel team and its sound within a word",
            "Spell words with vowel team patterns from dictation",
            "Apply the generalization that the first vowel usually says its name in a vowel team",
        ],
        "teaching_guidance": {
            "introduction": "Vowel teams are two vowels that work together to make one sound. The old rhyme 'when two vowels go walking, the first one does the talking' works for many common teams: ai and ay both say /ā/, ee and ea often say /ē/, oa says /ō/. This builds directly on silent-e knowledge — the child already knows long vowel sounds, now they learn a second way to spell them.",
            "scaffolding_sequence": [
                "Introduce ai/ay as two ways to spell long a: use letter tiles to build 'rain' and 'play'",
                "Sort ai words (rain, train, wait, mail) and ay words (play, day, say, stay) — notice ay usually comes at the end",
                "Introduce ee/ea as two ways to spell long e: 'tree' and 'read'",
                "Sort ee words (tree, sleep, feet, green) and ea words (read, meat, beach, team)",
                "Introduce oa/ow as two ways to spell long o: 'boat' and 'snow'",
                "Mix all vowel teams: sort words by their vowel team pattern",
                "Read sentences and short passages containing vowel team words",
                "Spell vowel team words from dictation, choosing the correct team for the word",
            ],
            "socratic_questions": [
                "You see two vowels next to each other in 'rain.' Which vowel sound do you hear — the a or the i?",
                "The word 'play' ends with ay, and the word 'rain' has ai in the middle. When do you use ay and when do you use ai?",
                "Can you find two vowel letters sitting together in the word 'beach'? What sound do they make together?",
                "How is the long a in 'cake' (silent e) different from the long a in 'rain' (vowel team)?",
            ],
            "practice_activities": [
                "Vowel team sorting: write words on index cards and sort into ai, ay, ee, ea, oa, ow piles",
                "Vowel team word building: use letter tiles to build and read words, swapping vowel teams to see what changes",
                "Vowel team hunt in books: find and list words with vowel teams during independent reading time",
                "Sentence dictation: parent reads sentences with vowel team words, child writes them",
            ],
            "real_world_connections": [
                "Vowel team words in daily life: rain, day, tree, road, snow, green, play",
                "Reading recipes: beat, cream, oat, wheat, steam",
                "Weather words: rain, hail, snow, sleet, heat, breeze",
                "Nature words during outdoor time: leaf, stream, toad, snail, oak, seed",
            ],
            "common_misconceptions": [
                "Trying to sound out each vowel separately ('r-a-i-n' as three syllables instead of one)",
                "Confusing when to use ai vs ay (ai is typically mid-word, ay is typically at word end)",
                "Thinking ea always says /ē/ — it can also say /ĕ/ as in 'bread' and 'head' (teach these as exceptions after the main pattern)",
                "Applying 'first vowel talks' to all vowel pairs — ow can say /ō/ as in 'snow' or /ow/ as in 'cow' (two sounds)",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Reads words with all six vowel teams accurately and fluently",
                "Spells vowel team words correctly, choosing the right team for position in word",
                "Identifies the vowel team and its sound in unfamiliar words",
            ],
            "proficiency_indicators": [
                "Reads most vowel team words with brief sounding out",
                "Spells vowel team words correctly but sometimes confuses ai/ay or ee/ea",
            ],
            "developing_indicators": [
                "Reads vowel team words when reminded of the vowel team rule",
                "Attempts to sound out each vowel separately before self-correcting",
            ],
            "assessment_methods": ["vowel team word lists", "word sorting by pattern", "spelling dictation"],
            "sample_assessment_prompts": [
                "Read these words: train, green, boat, play, beach, snow",
                "Sort these words by vowel team: rain, tree, road, day, seat, grow",
                "Spell these words: wait, sleep, coat",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Read this word: RAIN",
                "expected_type": "text",
                "correct_answer": "rain",
                "hints": ["The ai vowel team makes the long a sound: /ā/"],
                "explanation": "R-AI-N: the vowel team ai says /ā/. The word is 'rain.'",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What vowel team do you see in the word 'tree'?",
                "expected_type": "multiple_choice",
                "options": ["ea", "ee", "oa", "ai"],
                "correct_answer": "ee",
                "hints": ["Look at the two vowels sitting next to each other"],
                "explanation": "Tree has the vowel team ee, which makes the long e sound /ē/.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Read this word: BEACH",
                "expected_type": "text",
                "correct_answer": "beach",
                "hints": ["The ea vowel team usually says /ē/, like the ee in 'tree'"],
                "explanation": "B-EA-CH: the vowel team ea says /ē/. The word is 'beach.'",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Which word has the 'oa' vowel team?",
                "expected_type": "multiple_choice",
                "options": ["boat", "boot", "bone", "blow"],
                "correct_answer": "boat",
                "hints": ["Look for two vowels: o and a sitting next to each other"],
                "explanation": "Boat has the oa vowel team. Boot has oo, bone has silent e, blow has ow.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Read this sentence: The goat sat on the road and waited in the rain.",
                "expected_type": "text",
                "correct_answer": "The goat sat on the road and waited in the rain.",
                "hints": ["Find the vowel teams: goat (oa), road (oa), waited (ai), rain (ai)"],
                "explanation": "Four vowel team words: goat and road use oa (long o), waited and rain use ai (long a).",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Read these vowel team words: mail, green, boat, stay, leaf, grow.",
                "type": "open_response",
                "target_concept": "vowel_teams",
                "rubric": "Mastery: reads all 6 fluently. Proficient: reads 5-6 with some sounding out. Developing: sounds out each vowel separately.",
            },
            {
                "prompt": "Spell 'steam'.",
                "type": "text",
                "correct_answer": "steam",
                "target_concept": "vowel_team_spelling",
            },
            {
                "prompt": "Sort these words by their vowel sound: rain, tree, boat, play, meat, road.",
                "type": "open_response",
                "target_concept": "vowel_team_sorting",
                "rubric": "Mastery: correctly groups long a (rain, play), long e (tree, meat), long o (boat, road). Proficient: most correct. Developing: confuses groups.",
            },
        ],
        "resource_guidance": {
            "required": ["letter tiles with vowel team cards", "vowel team word cards"],
            "recommended": ["vowel team sorting mats", "decodable readers featuring vowel teams"],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Teach one vowel team pair at a time (ai/ay first, then ee/ea, then oa/ow). Use color-coded vowel team cards — same color for teams that make the same sound. Multisensory: trace the vowel team while saying its sound.",
            "adhd": "Vowel team sorting races with a timer. Keep sessions to 10-12 minutes. Use physical word cards that the child can move and stack rather than pencil-and-paper work.",
            "gifted": "Introduce less common vowel teams: ow (two sounds), ou, ey, ie. Discuss why English has multiple spellings for the same sound (historical origins from different languages).",
            "visual_learner": "Highlight or underline the vowel team in every word. Use a vowel team chart posted at the reading area with example words.",
            "kinesthetic_learner": "Build words with magnetic letters. Physically sort word cards into vowel team categories.",
            "auditory_learner": "Chant vowel team sounds: 'ai says /ā/, ay says /ā/.' Read vowel team words aloud in pairs.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Vowel teams are two vowels that work together to make one sound. The old rhyme, when two vowels go walking the first one does the talking, holds for many of them: ai and ay say long a, ee and ea often say long e, oa says long o. Today we read and spell words with the common vowel teams.",
                "gradual_release": {
                    "i_do": "Model building rain and play with letter tiles, naming the team and its sound each time, and pointing out that ay usually comes at a word's end while ai sits in the middle.",
                    "we_do": "Sort ai and ay words together, then ee and ea, then oa and ow. Build and read vowel-team words together, and spell one from dictation, choosing the right team.",
                    "you_do": "Child reads vowel-team words, names the team and its sound, spells vowel-team words from dictation, and applies the generalization that the first vowel usually says its name.",
                },
                "guided_practice": [
                    "Vowel-team sorting: sort word cards into ai, ay, ee, ea, oa, ow piles",
                    "Word building with letter tiles, swapping vowel teams to see what changes",
                    "Identify the vowel team and its sound within a written word",
                ],
                "independent_practice": [
                    "Read vowel-team words in sentences and short passages",
                    "Spell vowel-team words from dictation, choosing the correct team",
                ],
                "mastery_check": [
                    "Read words with the common vowel teams accurately",
                    "Identify the vowel team and its sound in a word",
                    "Spell vowel-team words from dictation and state the first-vowel generalization",
                ],
                "spiral_review": [
                    "Revisit the silent-e long vowels alongside the vowel teams so the two ways of spelling a long vowel stay distinct",
                ],
            },
            "classical": {
                "narrative_introduction": "There is more than one way to spell a long vowel. The vowel teams are pairs of vowels that walk together so that the first one may speak. Learn the teams in their order, one pair mastered before the next, and a wide class of words opens to be read.",
                "memory_work": {
                    "chants": [
                        "Chant the old rhyme as the rule: when two vowels go walking, the first one does the talking",
                        "Chant each team with its sound: ai says long a, ay says long a, ee says long e, oa says long o",
                        "Chant word sets gathered by their vowel team",
                    ],
                    "recitations": [
                        "Recite the vowel teams and their sounds in order, mastering one pair before the next is added",
                    ],
                },
                "copywork": [
                    "Copy vowel-team words neatly in their family groups while reading them, so the team is written as carefully as it is read",
                ],
                "recitation_routine": "Begin each lesson by reciting the rhyme and the teams learned so far before adding the next pair; the work is cumulative and never assumed.",
                "history_integration": "Tell, simply, that English keeps several spellings for one sound because it gathered its words from many older languages; the vowel teams are a piece of that long inheritance.",
                "read_aloud_suggestions": [
                    "A rich read-aloud for the ear, and readers that bring vowel-team words into real sentences",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "The family's current living read-aloud and simple readers in which vowel-team words appear in real, worthy sentences",
                ],
                "short_lesson_flow": "In a book read together, meet a word that holds a vowel team. Notice the two vowels walking side by side and the single sound they make together. Attend to one team, gently, and stop while the child is still interested.",
                "narration_prompt": "Tell me the two vowels you found walking together, and the one sound they made.",
                "real_world_objects": [
                    "Vowel-team words on signs and in the names of people and places",
                    "Weather words such as rain, hail, snow, and sleet",
                    "Nature words such as leaf, stream, toad, oak, and seed",
                ],
                "nature_connection": "On a nature walk, find vowel-team words for things that are seen, leaf, stream, toad, oak, and write one of them in the nature notebook.",
                "habit_focus": "The habit of careful looking: seeing two vowels together as one team that makes one sound, rather than sounding each vowel apart.",
            },
            "montessori": {
                "prepared_materials": [
                    "The green series phonogram cards for ai, ay, ee, ea, oa, and ow, each with matching objects or pictures",
                    "The large movable alphabet for building vowel-team words",
                    "Phonogram folders, one for each vowel team, holding its word cards",
                ],
                "presentation": {
                    "three_period_lesson": "With a phonogram and a word: this team, ai, says long a; show me a word with ai; what does this team say? The phonogram handled, sounded, and read.",
                    "steps": [
                        "Introduce a phonogram, such as ai, with the sound it makes",
                        "Build words with the movable alphabet that use the phonogram, and read them",
                        "Match the green series phonogram word cards to their objects, sounding each team out to check",
                    ],
                },
                "control_of_error": "The green series object and card pairs, and the phonogram folders, carry a control, so a misread or a wrong sort reveals itself to the child without an adult's verdict.",
                "abstraction_pathway": "From handling the phonogram and building words with it (the team made physical in the hand), to reading the green series cards, toward reading and spelling vowel-team words in any text.",
                "extensions": [
                    "Work through a phonogram folder for each vowel team and read green series phrases",
                    "Sort words by their vowel team with the materials",
                ],
                "observation_focus": "Watch for the child reading a vowel team as a single sound, and choosing the right team when spelling a word.",
            },
            "unschooling": {
                "invitations": [
                    "Keep letter tiles within reach for free word building with vowel teams",
                    "Leave readers that use vowel-team words on a low shelf",
                    "Let vowel-team words show up naturally on a weather chart or on nature labels at child height",
                ],
                "real_world_contexts": [
                    "Vowel-team words met in everyday life: rain, day, tree, road, snow, play",
                    "Reading recipe and weather words such as beat, cream, hail, and breeze",
                    "Nature words during outdoor time: leaf, stream, toad, snail, oak, seed",
                    "Reading vowel-team words in loved books",
                ],
                "conversation_starters": [
                    "There are two vowels next to each other in rain. Which vowel sound do you hear?",
                    "What sound do these two vowels make when they are together?",
                    "Can you find two vowel letters sitting side by side in this word?",
                ],
                "resource_bank": [
                    "Magnetic letters and letter tiles",
                    "Readers that include vowel-team words, kept available",
                    "Word-building games",
                ],
                "parent_role": "When a vowel-team word comes up in real reading, point out the team and the sound it makes, and follow the words the child cares about. Let real reading attempts do the teaching rather than a drill.",
                "observation_documentation": "Over time, note whether the child reads the common vowel teams, identifies the team and its sound, spells vowel-team words, and is beginning to use the generalization that the first vowel usually talks. This noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Pairs of vowels making one sound is like pairs of digits making one number (tens and ones)",
            "science": "Vowel team words in weather: rain, heat, snow, steam, stream, leaf",
            "history": "Different vowel teams came from different languages that English absorbed",
        },
    },
    "rf-09": {
        "enriched": True,
        "learning_objectives": [
            "Read words containing consonant digraphs sh, ch, th, wh, and ck",
            "Spell words with digraphs in initial and final positions",
            "Distinguish between consonant digraphs and consonant blends",
            "Identify which digraph makes the sound heard in a spoken word",
        ],
        "teaching_guidance": {
            "introduction": "Consonant digraphs are two letters that team up to make one completely new sound — a sound that neither letter makes alone. The sh in 'ship' doesn't sound like /s/ or /h/; it makes a unique /sh/ sound. This is fundamentally different from blends (like 'st' in 'stop') where you hear both individual letter sounds. Children already met the digraph concept briefly in rf-06; now they master all five common digraphs.",
            "scaffolding_sequence": [
                "Introduce sh with picture cards: ship, shell, fish, dish — listen for the /sh/ sound and feel the air flow",
                "Introduce ch: chip, cheese, bench, lunch — feel how the tongue touches the roof of the mouth",
                "Introduce th (both voiced and unvoiced): this, that, thick, bath — feel the tongue between the teeth",
                "Introduce wh: whale, wheel, white, when — compare to /w/ alone (some dialects merge these)",
                "Introduce ck: duck, truck, sock, stick — this digraph only appears at the end of short-vowel words",
                "Sort words by digraph: create five columns and sort picture or word cards",
                "Read sentences containing multiple digraphs: 'The chick sat on the ship deck.'",
                "Spell digraph words from dictation, choosing the correct digraph",
            ],
            "socratic_questions": [
                "In the word 'ship,' how many sounds do you hear at the beginning — one or two? How is that different from 'slip'?",
                "Put your hand in front of your mouth and say 'thin.' Now say 'fin.' Do you feel the difference?",
                "The word 'duck' ends with ck. Why do you think we need two letters when /k/ is just one sound?",
                "Can you think of a word that starts with 'ch'? Now one that starts with 'sh'? How are those beginning sounds different?",
            ],
            "practice_activities": [
                "Digraph picture sorts: cut out pictures from magazines and sort by beginning digraph sound",
                "Digraph hunt in the kitchen: find items with digraph sounds (cheese, chips, dish, shelf, whisk, chicken)",
                "Build digraph words with letter tiles, treating each digraph as a single unit on one tile",
                "Digraph bingo: call out words and mark the square with the matching digraph",
            ],
            "real_world_connections": [
                "Digraph words at mealtimes: cheese, chips, wheat, chicken, fish, mash",
                "Digraph words in the home: chair, shelf, bath, kitchen, chimney, threshold",
                "Digraph words outdoors: path, bush, shell, whale, thistle, bench",
                "Digraph words for people: child, mother (th), father (th), teacher (ch, th)",
            ],
            "common_misconceptions": [
                "Confusing digraphs with blends: a digraph makes ONE new sound (sh → /sh/), while a blend preserves BOTH sounds (sl → /s/ + /l/)",
                "Pronouncing th as /f/ or /v/ (common in some dialects — not an error in speech, but children need to map 'th' to the letters correctly for reading and spelling)",
                "Not recognizing that th has two sounds: unvoiced /th/ as in 'thin' and voiced /th/ as in 'this'",
                "Using ck incorrectly: ck only follows a short vowel in a single-syllable word (duck, not dake). After a long vowel, use k or ke.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Reads words with all five common digraphs accurately in any position",
                "Spells digraph words correctly from dictation",
                "Explains how a digraph is different from a blend",
            ],
            "proficiency_indicators": [
                "Reads most digraph words accurately with occasional hesitation on th words",
                "Spells common digraph words correctly but may confuse ck placement",
            ],
            "developing_indicators": [
                "Reads digraph words when reminded that the two letters make one sound",
                "Sounds out each letter of the digraph separately before self-correcting",
            ],
            "assessment_methods": ["digraph word lists", "digraph sorting", "spelling dictation", "reading in context"],
            "sample_assessment_prompts": [
                "Read these words: ship, chop, thin, when, duck",
                "Is 'sh' a blend or a digraph? How do you know?",
                "Spell these words: fish, lunch, thick, whip, clock",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Read this word: SHIP",
                "expected_type": "text",
                "correct_answer": "ship",
                "hints": ["The sh makes one sound: /sh/. Then /i/ /p/."],
                "explanation": "SH-I-P: the digraph sh says /sh/, then short i, then /p/ = 'ship.'",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What digraph do you hear at the beginning of 'cheese'?",
                "expected_type": "multiple_choice",
                "options": ["sh", "ch", "th", "wh"],
                "correct_answer": "ch",
                "hints": ["Say 'cheese' slowly. What sound do you hear first?"],
                "explanation": "Cheese begins with the digraph ch, which makes the /ch/ sound.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Read this word: THICK",
                "expected_type": "text",
                "correct_answer": "thick",
                "hints": ["Two digraphs: th at the start and ck at the end"],
                "explanation": "TH-I-CK: digraph th says /th/, short i, digraph ck says /k/ = 'thick.'",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Is 'bl' in 'black' a blend or a digraph?",
                "expected_type": "multiple_choice",
                "options": ["blend", "digraph"],
                "correct_answer": "blend",
                "hints": ["Can you hear BOTH the /b/ and the /l/ in 'black'?"],
                "explanation": "Bl is a blend because you hear both /b/ and /l/. In a digraph, two letters make one new sound you can't split apart.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Spell the word 'crunch.' What digraph does it contain?",
                "expected_type": "text",
                "correct_answer": "crunch, ch",
                "hints": ["Start with the blend cr, then the short u, then a digraph at the end"],
                "explanation": "Crunch: c-r-u-n-c-h. It contains the digraph ch at the end (nch).",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Read these digraph words: shell, chunk, three, whip, stuck.",
                "type": "open_response",
                "target_concept": "digraphs",
                "rubric": "Mastery: reads all 5 fluently. Proficient: reads 4-5 with sounding out. Developing: tries to separate digraph into two sounds.",
            },
            {
                "prompt": "Spell 'lunch'.",
                "type": "text",
                "correct_answer": "lunch",
                "target_concept": "digraph_spelling",
            },
            {
                "prompt": "What is the difference between a blend and a digraph?",
                "type": "open_response",
                "target_concept": "blend_vs_digraph",
                "rubric": "Mastery: clearly explains one new sound vs two separate sounds. Proficient: gives an example. Developing: cannot distinguish.",
            },
        ],
        "resource_guidance": {
            "required": ["digraph letter cards (sh, ch, th, wh, ck as single tiles)", "picture cards for sorting"],
            "recommended": ["digraph word lists", "decodable readers with digraph words"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Teach each digraph as a single unit on one card — never separate the letters. Use Orton-Gillingham multisensory method: see the digraph, say the sound, trace both letters as one unit. Add tactile cues: feel throat vibration for voiced th vs no vibration for unvoiced th.",
            "adhd": "One digraph per session (5 sessions total). Use physical picture sorts with large cards the child can move. Digraph scavenger hunts around the house for movement breaks.",
            "gifted": "Introduce less common digraphs: ph (/f/ as in phone), gh (/f/ as in laugh), kn (/n/ as in knee). Discuss why English has silent letters.",
            "visual_learner": "Digraph cards in a distinct color (all digraphs in blue, for example). Digraph chart posted at reading area.",
            "kinesthetic_learner": "Mouth awareness: feel where tongue and lips go for each digraph. Build words with physical tiles, treating digraphs as one piece.",
            "auditory_learner": "Listen for digraph sounds in a read-aloud and clap when you hear one. Digraph chants: 'sh says /sh/, ch says /ch/.'",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "A consonant digraph is two letters that team up to make one new sound, a sound neither letter makes alone. The sh in ship is not /s/ or /h/; it is one /sh/ sound. That is different from a blend, where both letter sounds are heard. Today we read and spell words with sh, ch, th, wh, and ck.",
                "gradual_release": {
                    "i_do": "Model reading ship, the sh making a single /sh/ sound. Build a digraph word with letter tiles, treating the digraph as one unit on one tile. Contrast a digraph, sh with one sound, against a blend, sl with two sounds.",
                    "we_do": "Read digraph words together by digraph, then sort picture and word cards into digraph columns. Spell a digraph word together, and sort digraphs from blends.",
                    "you_do": "Child reads words with all five digraphs in initial and final position, spells digraph words, and tells digraphs apart from blends.",
                },
                "guided_practice": [
                    "Digraph picture sorts into five columns, one per digraph",
                    "Build digraph words with letter tiles, the digraph as a single unit",
                    "Sort a set of words into digraphs and blends",
                ],
                "independent_practice": [
                    "Read sentences containing several digraphs",
                    "Spell digraph words from dictation, choosing the correct digraph",
                ],
                "mastery_check": [
                    "Read words with sh, ch, th, wh, and ck accurately",
                    "Spell digraph words in initial and final position",
                    "Explain how a digraph differs from a blend",
                ],
                "spiral_review": [
                    "Revisit consonant blends so the digraph and blend distinction stays clear",
                ],
            },
            "classical": {
                "narrative_introduction": "A digraph is a pair of letters that, joined, make a single new sound that neither could make alone. Learn the five common digraphs in order, one mastered before the next, and many words come within reach of reading.",
                "memory_work": {
                    "chants": [
                        "Chant each digraph with its sound: sh says /sh/, ch says /ch/, th says /th/",
                        "Chant digraph words that share a digraph, hearing the one sound the pair makes",
                        "Chant the distinction: a digraph makes one new sound, a blend keeps both",
                    ],
                    "recitations": [
                        "Recite the digraphs and their sounds learned so far before a new one is added",
                    ],
                },
                "copywork": [
                    "Copy digraph words neatly while sounding the digraph as one sound, the two letters written and read as one",
                ],
                "recitation_routine": "Begin each lesson by reciting the digraphs mastered so far before adding the next; one digraph is mastered before the next, cumulatively.",
                "history_integration": "Tell, simply, that these letter pairs were one way older writers found to spell sounds the single letters could not; the digraphs are part of the long history of our spelling.",
                "read_aloud_suggestions": [
                    "A rich read-aloud for the ear, and readers that bring the digraphs into real sentences",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "The family's current living read-aloud and simple readers in which digraph words appear in real, worthy sentences",
                ],
                "short_lesson_flow": "In a book read together, pause at a digraph word. Notice the two letters that join to make one new sound. Attend to a single digraph, gently, and stop while the child is still interested.",
                "narration_prompt": "Tell me the two letters that made one sound today, and another word of your own that has them.",
                "real_world_objects": [
                    "Digraph words at mealtimes: cheese, chips, fish, mash",
                    "Digraph words in the home: chair, shelf, bath, kitchen",
                    "Digraph words outdoors: path, shell, bench, bush",
                ],
                "nature_connection": "On a nature walk, notice digraph words for things that are found, shell, thistle, bush, path, and write one of them in the nature notebook.",
                "habit_focus": "The habit of careful listening and looking: hearing the one new sound the letter pair makes, rather than two.",
            },
            "montessori": {
                "prepared_materials": [
                    "The digraph sandpaper letters, both letters on one board, traced while the single sound is voiced",
                    "The green series digraph word cards with their matching objects",
                    "The large movable alphabet, the digraph treated as one unit",
                ],
                "presentation": {
                    "three_period_lesson": "With a digraph sandpaper board: this says /sh/, traced this way; show me /sh/; what does this say? The one sound, never the two letter names.",
                    "steps": [
                        "Trace the digraph board while voicing its single sound",
                        "Build digraph words with the movable alphabet, treating the digraph as one unit",
                        "Match the green series digraph word cards to their objects, sounding each digraph out to check",
                    ],
                },
                "control_of_error": "Each green series digraph word card has its own object or picture, so a word that does not match its pair reveals a misread to the child without an adult's word.",
                "abstraction_pathway": "From tracing the digraph board while voicing its one sound (the pair made one in the hand), to reading the green series cards, toward reading digraph words in any text.",
                "extensions": [
                    "Work through green series digraph word lists and read digraph phrases",
                    "Sort words into digraphs and blends with the materials",
                ],
                "observation_focus": "Watch that the child reads the digraph as a single sound and does not split it into two.",
            },
            "unschooling": {
                "invitations": [
                    "Keep letter tiles within reach, including digraph tiles that hold the pair as one unit",
                    "Leave readers that use digraph words on a low shelf",
                    "Let digraph words show up naturally on kitchen and household labels",
                ],
                "real_world_contexts": [
                    "Digraph words met at meals and in the home: cheese, dish, chair, bath",
                    "Digraph words outdoors: shell, path, bush",
                    "Digraph sounds in family words such as mother, father, and child",
                ],
                "conversation_starters": [
                    "In ship, how many sounds do you hear at the start, one or two? How is it different from slip?",
                    "Put your hand in front of your mouth and say thin, then say fin. Do you feel the difference?",
                    "Can you think of a word that starts with ch? Now one that starts with sh?",
                ],
                "resource_bank": [
                    "Magnetic letters and letter tiles",
                    "Decodable readers that include digraph words, kept available",
                    "Word-building games",
                ],
                "parent_role": "When a digraph word comes up in real reading, point out the pair of letters and the one sound they make, and follow the words the child wants to read. Let real reading attempts do the teaching rather than a drill.",
                "observation_documentation": "Over time, note whether the child reads the five digraphs, hears one new sound for each, tells a digraph apart from a blend, and spells digraph words. This noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Two digits can make one number (place value), two letters can make one sound (digraph)",
            "science": "Digraph words in science: shell, whale, thick, thin, shade, chill",
            "history": "Digraphs come from the history of English: 'th' is an ancient Germanic sound",
        },
    },
    "rf-10": {
        "enriched": True,
        "learning_objectives": [
            "Read the first 100 high-frequency sight words instantly without sounding out",
            "Spell the 25 most common sight words from memory",
            "Read sight words accurately in connected text",
            "Distinguish between decodable words and sight words that must be memorized",
        ],
        "teaching_guidance": {
            "introduction": "Sight words are the glue that holds sentences together. Words like 'the,' 'was,' 'said,' 'there,' and 'could' appear on nearly every page but don't follow regular phonics rules. Children need to recognize these instantly by sight so they can focus their decoding energy on the content words. Introduce 3-5 new sight words per week alongside ongoing phonics instruction.",
            "scaffolding_sequence": [
                "Introduce 3 sight words with flash cards: see the word, say the word, trace the word with a finger",
                "Practice reading the new words in simple phrases: 'the dog,' 'was big,' 'said Mom'",
                "Write each word three times while saying it aloud (look, say, cover, write, check)",
                "Play a memory matching game with the accumulated sight word cards",
                "Read the words in context: simple decodable sentences that include the sight words",
                "Cumulative review: shuffle all learned sight words and read through the stack daily",
                "Spell sight words from dictation: parent says the word, child writes it",
                "Read sight words fluently within authentic texts and stories",
            ],
            "socratic_questions": [
                "Can you sound out the word 'said' using the phonics rules you know? What makes this word tricky?",
                "You already know 'the.' How many times can you find 'the' on this page?",
                "What is the difference between words you can sound out and words you just have to know by heart?",
                "Which of these words have you seen the most in your books: 'the,' 'cat,' or 'elephant'?",
            ],
            "practice_activities": [
                "Sight word flash card review: aim for instant recognition within 2 seconds per word",
                "Sight word memory game: lay cards face down, flip two at a time, read both words aloud when a match is found",
                "Sight word sentences: parent gives the child 5 sight word cards and the child builds a sentence using them",
                "Sight word hunt: pick 3 words and search for them in a book, tallying how many times each appears",
            ],
            "real_world_connections": [
                "Sight words are everywhere in print: 'the,' 'and,' 'is,' 'to' on signs, labels, and instructions",
                "Reading recipes: 'the,' 'and,' 'with,' 'from,' 'to' connect the ingredient words",
                "Writing notes and lists: most connecting words are sight words",
                "Reading aloud to younger siblings: sight words let you read smoothly",
            ],
            "common_misconceptions": [
                "Thinking sight words can be sounded out with regular phonics — many are irregular (said, was, the, of, could)",
                "Confusing similar-looking sight words: was/saw, there/their/they're, where/were",
                "Believing sight words don't need practice once learned — review is essential for long-term retention",
                "Spending too long on sight words at the expense of phonics — sight words supplement, not replace, phonics instruction",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Reads 80+ of the first 100 sight words instantly (under 2 seconds each)",
                "Spells the 25 most common sight words correctly from dictation",
                "Reads sight words fluently in connected text without pausing",
            ],
            "proficiency_indicators": [
                "Reads 60-80 sight words instantly, needs a moment for others",
                "Spells most common sight words with occasional errors (sed for said)",
            ],
            "developing_indicators": [
                "Reads 30-60 sight words, attempts to sound out the rest",
                "Recognizes sight words in flash card drill but not always in text",
            ],
            "assessment_methods": [
                "flash card timed recognition",
                "sight word reading in context",
                "spelling dictation",
            ],
            "sample_assessment_prompts": [
                "Read these words as fast as you can: the, was, said, have, they, could, there, from, were, would",
                "Spell these words: said, the, was, they, have",
                "Read this sentence fluently: They said they could have the one from over there.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Read this word: THE",
                "expected_type": "text",
                "correct_answer": "the",
                "hints": ["This is the most common word in English. You see it on almost every page."],
                "explanation": "'The' is the most common sight word. It appears in nearly every sentence.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which of these is a sight word that you cannot sound out with phonics rules?",
                "expected_type": "multiple_choice",
                "options": ["cat", "said", "stop", "jump"],
                "correct_answer": "said",
                "hints": ["Try to sound out each word. Which one doesn't follow the rules?"],
                "explanation": "'Said' is a sight word — if you try to sound it out (/s/ /a/ /i/ /d/), you get the wrong pronunciation. You have to memorize it.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Spell the word 'they' from memory.",
                "expected_type": "text",
                "correct_answer": "they",
                "hints": ["It starts with th. The ending is tricky — it's not spelled like it sounds."],
                "explanation": "They is spelled t-h-e-y. The 'ey' makes the long a sound, which is unusual.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Read this sentence: She said she could have one from the store.",
                "expected_type": "text",
                "correct_answer": "She said she could have one from the store.",
                "hints": ["The sight words are: she, said, could, have, one, from, the"],
                "explanation": "This sentence contains 7 sight words: she, said, could, have, one, from, the. Only 'store' follows regular phonics.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "How many sight words can you find in this sentence? 'They were going to find their friend over there.'",
                "expected_type": "number",
                "correct_answer": "7",
                "hints": ["Sight words are common words that don't follow regular phonics rules"],
                "explanation": "Seven sight words: they, were, going, to, find, their, there. (Some lists also include 'over' and 'friend'.)",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Read these 10 sight words as quickly as you can: was, they, said, have, from, could, there, would, been, were.",
                "type": "open_response",
                "target_concept": "sight_word_recognition",
                "rubric": "Mastery: reads all 10 within 15 seconds. Proficient: reads 8-10, some hesitation. Developing: reads 5-7, tries to sound out the rest.",
            },
            {
                "prompt": "Spell 'because'.",
                "type": "text",
                "correct_answer": "because",
                "target_concept": "sight_word_spelling",
            },
            {
                "prompt": "What makes sight words different from words you can sound out?",
                "type": "open_response",
                "target_concept": "sight_word_concept",
                "rubric": "Mastery: explains they don't follow phonics rules and must be memorized. Proficient: says you have to remember them. Developing: cannot explain.",
            },
        ],
        "resource_guidance": {
            "required": ["sight word flash cards (first 100)", "lined paper for practice writing"],
            "recommended": ["sight word ring (cards on a binder ring for portable review)", "simple decodable readers"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 10},
        "accommodations": {
            "dyslexia": "Multisensory sight word practice is critical: see it, say it, spell it aloud, trace it in sand or salt, write it. Introduce only 2-3 new words per week. Use colored overlays if visual stress is present. Review cumulative words daily — spaced repetition is essential.",
            "adhd": "Flash card races against a timer (beat your own record). Sight word hopscotch: write words in chalk and hop to each one while reading it. Keep review sessions to 5 minutes, twice daily rather than one long session.",
            "gifted": "Move to second and third 100 sight words once the first 100 are mastered. Begin noticing patterns in irregular words (word origins, silent letters). Start a personal reading log.",
            "visual_learner": "Color-code tricky parts of sight words (the 'ai' in 'said' in red). Sight word wall display, grouped by pattern or visual similarity.",
            "kinesthetic_learner": "Write sight words in sand, salt, shaving cream, or with finger paint. Stamp words with letter stamps. Build with magnetic letters.",
            "auditory_learner": "Spell words aloud rhythmically. Create mnemonics: 'said — S-A-I-D, silly ants in dirt.' Sing sight word songs.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Sight words are the glue of sentences: the, was, said, there appear on nearly every page but do not follow the regular phonics rules. We learn to recognize them instantly by sight, so decoding energy is free for the content words. Today we learn new sight words, read them in text, and tell sight words from decodable words.",
                "gradual_release": {
                    "i_do": "Model with a sight word card: see the word, say the word, trace the word with a finger. Read it inside a short phrase. Model the look, say, cover, write, check routine for spelling it.",
                    "we_do": "Read new sight words together inside simple phrases. Do the look-say-cover-write-check routine together, and read the sight words inside a decodable sentence.",
                    "you_do": "Child reads the learned sight words instantly, spells the most common ones from memory, and reads them accurately in connected text.",
                },
                "guided_practice": [
                    "Flash-card review aiming for instant recognition within two seconds",
                    "Sight word memory matching with the accumulated cards",
                    "Read sight words inside simple phrases and sentences",
                ],
                "independent_practice": [
                    "Cumulative review: read through the whole accumulated sight word stack daily",
                    "Spell sight words from dictation",
                ],
                "mastery_check": [
                    "Read the learned sight words instantly within about two seconds each",
                    "Spell the most common sight words from memory",
                    "Read sight words accurately within connected text",
                ],
                "spiral_review": [
                    "Shuffle and reread all learned sight words daily so earlier words are not lost",
                ],
            },
            "classical": {
                "narrative_introduction": "Some of the most common words in English will not yield to the phonics rules. The, said, was, of must simply be known by heart. Learn a few each week and review them cumulatively, and these words become instant and sure.",
                "memory_work": {
                    "chants": [
                        "Chant the spelling of a common sight word letter by letter: s, a, i, d, said",
                        "Chant small groups of sight words together until they are firm",
                        "Chant the trickiest words, the ones the phonics rules will not explain",
                    ],
                    "recitations": [
                        "Read aloud the accumulated sight words daily, cumulatively, before adding three to five new ones",
                    ],
                },
                "copywork": [
                    "Copy the sight words, and copy short sentences that feature them, neatly and while reading them",
                ],
                "recitation_routine": "Begin each lesson by reading through the whole accumulated stack of sight words before any new words are added; the set is rehearsed cumulatively, never assumed.",
                "history_integration": "Tell, simply, that these little words are old and worn smooth by long use, their spellings kept from an earlier English even as their sounds drifted away from the rules.",
                "read_aloud_suggestions": [
                    "A rich read-aloud for the ear, and simple readers thick with the common sight words for the child's own reading",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 8,
                "living_book_suggestions": [
                    "The family's current living read-aloud and simple, worthy readers in which the common words recur naturally on every page",
                ],
                "short_lesson_flow": "In a book read together, the child meets the same small words again and again. Gently point to one, this little word is the, and let the repeated reading of real text do most of the work. Take one short turn, and stop while the child is still glad to be reading.",
                "narration_prompt": "After reading, tell me one little word that you saw many times on the page.",
                "real_world_objects": [
                    "The common words on signs, labels, and simple instructions",
                    "The little connecting words in the current read-aloud",
                    "The common words in a note or list written at home",
                ],
                "nature_connection": "In a short caption the child writes under a nature-notebook drawing, notice together the little connecting words they used.",
                "habit_focus": "The habit of attentive reading: letting the eye learn the common words by truly attending to real and worthy text.",
            },
            "montessori": {
                "prepared_materials": [
                    "Puzzle word cards, the words that do not follow the rules, presented honestly as puzzle words",
                    "Sight word booklets that the child assembles and keeps",
                    "The large movable alphabet for building the puzzle words",
                ],
                "presentation": {
                    "three_period_lesson": "With a puzzle word card: this word is said; show me said; what is this word? Presented honestly as a word to be known whole, not sounded out.",
                    "steps": [
                        "Present a puzzle word, naming it and explaining that it is a word we come to know by sight",
                        "The child traces or builds the word with the movable alphabet",
                        "The child adds the word to a small sight word booklet they assemble and keep",
                    ],
                },
                "control_of_error": "These words are known by memory, so the control is gentle: it lies in the child's own assembled booklet and in re-reading, and above all in meeting the word again in real text. There is no self-correcting material, and the guide names this honestly.",
                "abstraction_pathway": "From handling and tracing the puzzle word, to assembling it into the booklet, toward recognizing it instantly in any text with no card at all.",
                "extensions": [
                    "Grow the sight word booklet as new puzzle words are met",
                    "Read the puzzle words within the reading series and in real books",
                ],
                "observation_focus": "Watch for instant recognition, and for the child meeting the puzzle words calmly as known wholes rather than trying to sound them out.",
            },
            "unschooling": {
                "invitations": [
                    "Leave simple readers thick with the common words on a low shelf",
                    "Keep magnetic letters and word cards within reach",
                    "Post a few of the most common words where the child will see them daily",
                ],
                "real_world_contexts": [
                    "The common words everywhere in real print: signs, labels, instructions, recipes",
                    "The same small words met again and again in a loved book read many times",
                    "The connecting words in notes and lists written at home",
                ],
                "conversation_starters": [
                    "Can you sound out the word said? What makes this word tricky?",
                    "You already know the word the. How many times can you find it on this page?",
                    "Which words can you sound out, and which ones do you just know by heart?",
                ],
                "resource_bank": [
                    "Simple readers and favorite books read again and again",
                    "Magnetic letters and word cards",
                    "The most common words posted where they are seen",
                ],
                "parent_role": "Read aloud often and follow the child's finger to the small words that recur. When a child wants a word, simply tell them, and let the repeated reading of real, loved text make the common words familiar rather than drilling them.",
                "observation_documentation": "Over time, note which common words the child recognizes instantly, whether they meet them calmly as known words rather than sounding them out, and whether their reading of real text is growing smooth. This noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Sight words in math: 'more,' 'less,' 'than,' 'equal,' 'and' are all high-frequency words",
            "science": "Sight words connect content words in science reading: 'The plant was green and very tall'",
            "history": "Many sight words are the oldest words in English, surviving from Anglo-Saxon times",
        },
    },
    "rf-11": {
        "enriched": True,
        "learning_objectives": [
            "Read grade-level decodable text at 40 or more words per minute with accuracy",
            "Self-correct errors that change meaning without prompting",
            "Read with appropriate expression, pausing at punctuation and stressing important words",
            "Monitor comprehension while reading and stop when something doesn't make sense",
            "Build reading stamina to sustain independent reading for 10-15 minutes",
        ],
        "teaching_guidance": {
            "introduction": "Fluency is the bridge between decoding and comprehension. A child who reads word-by-word with great effort has no mental energy left to understand what the words mean. Fluent readers recognize words automatically, group them into phrases, and read with expression — freeing the mind to think about the meaning. Fluency develops through practice with texts at the child's independent reading level.",
            "scaffolding_sequence": [
                "Model fluent reading: parent reads a passage aloud, then the child reads the same passage (echo reading)",
                "Practice paired reading: parent and child read aloud together at the same pace (choral reading)",
                "Child reads a short familiar passage three times, noting improvement in speed and smoothness each time",
                "Introduce phrase-cued reading: mark natural phrase breaks with a pencil slash and read phrase by phrase",
                "Practice reading with expression: show how a question sounds different from a statement, how an exclamation has energy",
                "Time one-minute reads with familiar texts to measure words per minute — celebrate personal bests, never compare to others",
                "Extend to slightly more challenging texts, maintaining accuracy above 95%",
                "Build stamina: gradually increase independent reading time from 5 minutes to 15 minutes",
            ],
            "socratic_questions": [
                "When you read that sentence, did it sound like talking? How could you make it sound more like you're telling someone a story?",
                "You read 'The dog ran fast' all as one flat line. How would you really say that if you were excited about a dog running?",
                "You stopped in the middle of a word and started over. What did you notice that made you go back and fix it?",
                "This sentence ends with a question mark. How should your voice change when you read a question?",
            ],
            "practice_activities": [
                "Repeated reading: choose a short passage (50-100 words) and read it three times, trying to be smoother each time",
                "Reader's theater: read a favorite story aloud with parent and child taking different character voices",
                "Record and listen: record the child reading, play it back so they hear their own fluency and expression",
                "Poetry performance: memorize and perform a short poem with expression and appropriate pacing",
            ],
            "real_world_connections": [
                "Reading recipes aloud while cooking together — fluency makes the instructions usable",
                "Reading picture book stories to younger siblings or stuffed animals",
                "Reading road signs and billboards quickly while driving — fluent readers process text fast",
                "Reading the steps in a building project or craft instructions smoothly enough to follow them",
            ],
            "common_misconceptions": [
                "Thinking faster is always better — speed without accuracy or comprehension is not fluency",
                "Reading in a monotone robot voice even when reading 'correctly' — expression is part of fluency",
                "Skipping unknown words instead of attempting them — fluency includes self-correction strategies",
                "Believing fluency must be taught with timed drills — timed reads are ONE tool, not the only approach; reading real books builds fluency naturally",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Reads grade-level decodable text at 40+ words per minute with 95%+ accuracy",
                "Self-corrects meaning-changing errors without prompting",
                "Reads with natural phrasing, appropriate pauses, and expression matching the text",
            ],
            "proficiency_indicators": [
                "Reads at 30-40 words per minute with 90%+ accuracy",
                "Self-corrects some errors, reads with emerging expression",
            ],
            "developing_indicators": [
                "Reads word-by-word at fewer than 30 words per minute",
                "Rarely self-corrects; reads in a flat monotone",
            ],
            "assessment_methods": [
                "timed oral reading (one minute)",
                "running record for accuracy",
                "expression rubric",
            ],
            "sample_assessment_prompts": [
                "Read this passage aloud for one minute while I count the words (grade-level decodable text)",
                "Read this sentence with expression: 'Oh no!' said the cat. 'The fish got away!'",
                "Read this paragraph and tell me what happened in the story.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Read this sentence smoothly, like you are talking: The cat sat on the mat.",
                "expected_type": "text",
                "correct_answer": "The cat sat on the mat.",
                "hints": ["Read the whole sentence without stopping between words. Make it sound natural."],
                "explanation": "A fluent reader reads this as a smooth phrase, not word by word: 'The-cat-sat-on-the-mat.'",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "How should your voice change when you see a question mark at the end of a sentence?",
                "expected_type": "text",
                "hints": ["Think about how your voice sounds when you ask someone a question in real life"],
                "explanation": "Your voice should go up at the end of a question. This is called intonation. It tells the listener you are asking, not telling.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Read this with expression: 'Stop!' yelled the man. 'That is my hat!'",
                "expected_type": "text",
                "correct_answer": "'Stop!' yelled the man. 'That is my hat!'",
                "hints": ["The exclamation marks mean the man is yelling. Make your voice sound excited and loud."],
                "explanation": "Fluent reading uses expression. Exclamation marks mean strong feeling — read with energy and emphasis.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You are reading and you come across a word you don't know. What should you do?",
                "expected_type": "multiple_choice",
                "options": [
                    "Skip it and keep going",
                    "Stop reading completely",
                    "Try to sound it out, and if it still doesn't make sense, ask for help",
                    "Guess from the first letter only",
                ],
                "correct_answer": "Try to sound it out, and if it still doesn't make sense, ask for help",
                "hints": ["Good readers have strategies for hard words. What's the best first step?"],
                "explanation": "The best strategy is to try sounding it out first. If that doesn't work, use context clues or ask for help. Skipping or guessing leads to missed meaning.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Read this passage three times. Which time was the smoothest? 'The frog jumped from the log into the pond. Splash! The water went everywhere. The duck was not happy at all.'",
                "expected_type": "text",
                "hints": ["Each time you read it, try to sound more natural. Group words into phrases."],
                "explanation": "Repeated reading builds fluency. The third time should be the smoothest because your brain recognizes the words faster each time. Phrase groups: 'The frog jumped / from the log / into the pond.'",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Read this passage aloud for one minute. (Use any grade-level decodable text of 60+ words.)",
                "type": "open_response",
                "target_concept": "reading_rate",
                "rubric": "Mastery: 40+ WPM with expression. Proficient: 30-40 WPM, mostly accurate. Developing: under 30 WPM, word-by-word.",
            },
            {
                "prompt": "Read this sentence with expression: 'Can you believe it?' she whispered. 'The egg is hatching!'",
                "type": "open_response",
                "target_concept": "expression",
                "rubric": "Mastery: whispers the first part, builds excitement for the second. Proficient: some expression change. Developing: reads flat.",
            },
            {
                "prompt": "What do you do when you read a word wrong and the sentence stops making sense?",
                "type": "open_response",
                "target_concept": "self_correction",
                "rubric": "Mastery: describes going back and re-reading. Proficient: says they try again. Developing: says they skip it.",
            },
        ],
        "resource_guidance": {
            "required": ["decodable readers at the child's level", "a timer or clock for one-minute reads"],
            "recommended": [
                "poetry collections for performance reading",
                "audiobooks of familiar stories for modeling fluency",
            ],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Use texts at the child's independent level (95%+ accuracy) — frustration-level text kills fluency. Allow finger tracking. Repeated reading of the same passage builds automaticity. Consider audiobooks paired with physical books for modeling.",
            "adhd": "Short passages (50-75 words) for repeated reading. Reader's theater adds engagement. Time challenges (beat your own record) add motivation. Reading aloud to a pet or stuffed animal makes it purposeful.",
            "gifted": "Move to more complex texts with varied sentence structures. Introduce reader's theater scripts with multiple characters. Begin chapter book read-alouds where the child reads one chapter per sitting.",
            "visual_learner": "Use a reading window (card with a rectangular cutout) to focus on one line at a time. Increase font size if needed. Good lighting is essential.",
            "kinesthetic_learner": "Track with a finger or bookmark. Stand up while reading aloud. Walk slowly while reading from a book held in hand.",
            "auditory_learner": "Record and play back reading for self-assessment. Listen to audiobooks at natural speed to internalize fluent pacing. Echo reading with the parent.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Fluency is the bridge between decoding and understanding. A fluent reader recognizes words at once, groups them into phrases, and reads with expression, so the mind is free to think about meaning. Today we build accuracy, smoothness, and expression with text at the child's own reading level.",
                "gradual_release": {
                    "i_do": "Read a passage aloud as a model, grouping words into phrases and letting the voice rise for a question and lift for an exclamation. Then mark a sentence into natural phrases with light pencil slashes.",
                    "we_do": "Read a passage together at one pace, then echo a sentence the child reads back. Read a marked sentence phrase by phrase together, and practice making a question and a statement sound different.",
                    "you_do": "Child reads a short familiar passage three times, growing smoother each time, reads with expression that matches the text, and self-corrects errors that change the meaning.",
                },
                "guided_practice": [
                    "Echo and choral reading of a short passage with the parent",
                    "Phrase-cued reading: read a marked sentence phrase by phrase",
                    "Repeated reading of a fifty to one hundred word passage, smoother each time",
                ],
                "independent_practice": [
                    "Read familiar books independently, building stamina from five minutes toward fifteen",
                    "One-minute reads of familiar text, celebrating personal bests, never comparing to others",
                ],
                "mastery_check": [
                    "Read grade-level decodable text at forty or more words per minute with high accuracy",
                    "Self-correct meaning-changing errors without prompting",
                    "Read with natural phrasing, appropriate pauses, and fitting expression",
                ],
                "spiral_review": [
                    "Return to easier, familiar passages to keep accuracy and expression strong before harder text",
                ],
            },
            "classical": {
                "narrative_introduction": "To read aloud well is an art the grammar stage prizes. The reader makes the words sound as living speech, phrased and expressive, so a listener understands. Practiced daily, reading aloud becomes smooth, sure, and a pleasure to hear.",
                "memory_work": {
                    "chants": [
                        "Chant a marked sentence in its natural phrases, so the ear learns to group words rather than read them one by one",
                        "Chant the marks of expression: a question lifts at its end, an exclamation carries energy, a period comes to rest",
                    ],
                    "recitations": [
                        "Memorize and recite short, worthy poems and passages, performing them with phrasing and expression so that fluency is built by heart",
                    ],
                },
                "copywork": [
                    "Copy a short passage that is being read for fluency, attending to its punctuation, so the marks that guide the voice are known by the hand",
                ],
                "recitation_routine": "Begin each lesson by reciting a memorized passage from a former day, then read aloud the current passage; the reader's repertoire grows cumulatively.",
                "history_integration": "Read aloud and recite passages drawn from history and from the great stories, so that fluency is practiced on texts worth the time, along the chronological spine.",
                "read_aloud_suggestions": [
                    "Well-written prose and poetry, a little above the child's own reading level, read aloud daily for the music and rhythm of the language",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "Living books chosen for truly beautiful language, never twaddle, that the child will want to read aloud well",
                ],
                "short_lesson_flow": "Read aloud together from a living book, unhurried, caring for the sound of the language rather than for speed. Let the child read a passage attentively, once and well, and then tell it back. Stop while the reading is still a pleasure.",
                "narration_prompt": "Tell me back the passage you just read. What happened, and which part did you most enjoy reading aloud?",
                "real_world_objects": [
                    "A recipe read aloud smoothly while cooking together",
                    "A picture book read aloud to a younger sibling",
                    "Signs and labels read at a glance during the day",
                ],
                "nature_connection": "Read aloud a short nature passage or poem outdoors, and copy a favorite line into the nature notebook.",
                "habit_focus": "The habit of attention and of reading well: one careful, expressive reading rather than a hurried or careless one.",
            },
            "montessori": {
                "prepared_materials": [
                    "A reading corner holding a variety of texts at and just above the child's independent level",
                    "Familiar books and short passages the child may choose and reread freely",
                    "Poetry and reader's-theater pieces for expressive reading",
                ],
                "presentation": {
                    "three_period_lesson": "With a marked passage: this is a phrase, read as one group; show me where this phrase ends; how should this phrase sound? Reading modeled, then handed to the child.",
                    "steps": [
                        "The guide reads a passage aloud as a model of phrasing and expression",
                        "The child chooses a text at their independent level and reads it, returning to reread it freely",
                        "The child reads aloud to a small listener or records and listens back to their own reading",
                    ],
                },
                "control_of_error": "The child reading aloud and listening, to a listener or to a recording, hears for themselves where the reading stumbled or fell flat, and rereads to mend it without an adult's correction.",
                "abstraction_pathway": "From echoing a modeled reading, to rereading a chosen text freely, toward reading any new text smoothly and with expression at the first attempt.",
                "extensions": [
                    "Prepare and perform a reader's-theater piece with character voices",
                    "Choose and progress through richer texts as fluency grows",
                ],
                "observation_focus": "Watch for the child grouping words into phrases, reading with expression, self-correcting freely, and choosing to read for sustained, contented stretches.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a generous shelf of inviting books at and around the child's reading level within reach",
                    "Leave audiobooks alongside their printed books, so a fluent voice can be heard and followed",
                    "Make a cozy reading nook where long, uninterrupted reading is easy",
                ],
                "real_world_contexts": [
                    "Reading favorite stories aloud to younger siblings, pets, or stuffed animals",
                    "Reading a recipe aloud smoothly enough to cook from it",
                    "Reading the lines of a play or a game's instructions aloud",
                    "Reading signs, comics, and captions met through the day",
                ],
                "conversation_starters": [
                    "Would you read me that part again? It sounded wonderful the way you said it.",
                    "How do you think this character would say that line?",
                    "Want to read this story to your little brother tonight?",
                ],
                "resource_bank": [
                    "Many inviting books at and around the child's reading level",
                    "Audiobooks paired with their printed texts",
                    "Comics, poetry, and play scripts kept available",
                ],
                "parent_role": "Read aloud to and with the child often, give them real reasons and real audiences to read aloud for, and let abundant time with loved books build fluency. Never time or rank the reading; follow what the child wants to read.",
                "observation_documentation": "Over time, note whether the child's reading is growing smoother and more expressive, whether they self-correct meaning-changing errors, and whether they can sustain contented independent reading. This noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Fluency in reading is like fluency in math facts — automatic recall frees the mind for harder thinking",
            "science": "Fluent reading allows a child to read and follow science experiment instructions independently",
            "history": "Fluent readers can engage with simple historical narratives and biographies",
        },
    },
    "rf-12": {
        "enriched": True,
        "learning_objectives": [
            "Identify the main idea of a short passage in one sentence",
            "Distinguish the main idea from supporting details",
            "Retell what a passage is mostly about without including every detail",
            "Identify 2-3 key supporting details that explain or prove the main idea",
        ],
        "teaching_guidance": {
            "introduction": "Comprehension is the whole point of reading. The main idea is what a passage is mostly about — the big umbrella that covers all the details. A child who can identify the main idea can tell you in one sentence what a whole paragraph or story is about. This is the first comprehension skill because it teaches children to read for meaning, not just for words.",
            "scaffolding_sequence": [
                "Start with pictures: show a photograph and ask 'What is this picture mostly about?' before applying to text",
                "Read a 3-sentence paragraph aloud and model finding the main idea: 'This paragraph is mostly about...'",
                "Read a short passage together and identify the main idea versus the details using a hand metaphor (palm = main idea, fingers = details)",
                "Practice with passages where the main idea is stated in the first sentence (explicit main idea)",
                "Progress to passages where the main idea must be inferred from the details",
                "Have the child write the main idea of a passage in one sentence",
                "Practice distinguishing main idea from interesting-but-secondary details",
                "Apply to both fiction (what is the story mostly about?) and nonfiction (what is this passage mostly about?)",
            ],
            "socratic_questions": [
                "If you had to tell someone what this whole passage is about in just one sentence, what would you say?",
                "You mentioned that the dog was brown. Is the color of the dog the MAIN thing this story is about, or is that a detail?",
                "What would be a good title for this passage? A title usually captures the main idea.",
                "Which sentence tells you the most about what the whole passage is about?",
            ],
            "practice_activities": [
                "Main idea in a hand: trace the child's hand — write the main idea on the palm and details on each finger",
                "Title match: read short passages and choose the best title from three options",
                "Detail detective: after reading, sort sentence strips into 'main idea' and 'detail' piles",
                "Retell in one sentence: after reading any passage, the child summarizes in exactly one sentence",
            ],
            "real_world_connections": [
                "Summarizing a nature walk: 'What was our walk mostly about?' 'We saw birds at the pond.'",
                "Telling Dad about a book: you don't retell every word — you share the main idea",
                "News summaries: headlines capture the main idea of a story in a few words",
                "Movie descriptions: a one-sentence summary is the main idea of the whole film",
            ],
            "common_misconceptions": [
                "Confusing the topic with the main idea: the topic is one or two words (dogs); the main idea is a complete thought (Dogs need daily exercise to stay healthy)",
                "Picking the most interesting detail instead of the main idea — an exciting detail isn't always the central point",
                "Retelling every detail instead of summarizing — children often want to include everything rather than identifying what's MOST important",
                "Thinking the main idea is always the first sentence — sometimes it's implied and must be figured out from the details",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "States the main idea of a passage in one clear sentence",
                "Identifies 2-3 supporting details that connect to the main idea",
                "Distinguishes between main idea and details consistently",
            ],
            "proficiency_indicators": [
                "Identifies the main idea with some support or prompting",
                "Can name details but sometimes confuses a detail with the main idea",
            ],
            "developing_indicators": [
                "Retells details but cannot identify what the passage is mostly about",
                "Needs the main idea to be explicitly stated in the first sentence to find it",
            ],
            "assessment_methods": ["oral retelling", "main idea in one sentence", "detail sorting"],
            "sample_assessment_prompts": [
                "Read this paragraph and tell me in one sentence what it is mostly about.",
                "Which of these three sentences is the main idea? (provide one main idea and two details)",
                "Name two details that support the main idea of this passage.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Read this passage: 'Dogs need water every day. They need food every day. They need walks and play time. Dogs need people to take care of them.' What is the main idea?",
                "expected_type": "text",
                "hints": ["What is the whole passage mostly about? Try to say it in one sentence."],
                "explanation": "The main idea is: Dogs need people to take care of them every day. The details (water, food, walks) support this big idea.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Is this a main idea or a detail? 'The cat was orange.'",
                "expected_type": "multiple_choice",
                "options": ["main idea", "detail"],
                "correct_answer": "detail",
                "hints": [
                    "A main idea tells what the WHOLE passage is about. A detail gives one specific piece of information."
                ],
                "explanation": "The color of the cat is one specific piece of information — a detail, not the main idea of a passage.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Read this: 'Bees are very important. They help flowers grow by spreading pollen. They make honey that people and animals eat. Without bees, many plants would not survive.' Which sentence is the main idea?",
                "expected_type": "text",
                "correct_answer": "Bees are very important.",
                "hints": ["Which sentence is like an umbrella that covers all the other sentences?"],
                "explanation": "'Bees are very important' is the main idea. The other sentences are details that explain WHY bees are important.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: The main idea is always the first sentence of a passage.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": [
                    "Think about whether the main idea could be somewhere else, or even not directly stated at all."
                ],
                "explanation": "False. The main idea can be anywhere in a passage, or it might not be directly stated — you have to figure it out from the details.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Read this: 'Maria planted seeds in the garden. She watered them every morning. She pulled the weeds around them. She watched tiny green sprouts push through the dirt.' What is the main idea? (It is not directly stated.)",
                "expected_type": "text",
                "hints": ["What are ALL these sentences about? What is Maria doing overall?"],
                "explanation": "The implied main idea is: Maria took care of her garden so her plants would grow. No single sentence states this — you have to figure it out from all the details together.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Read a short paragraph and tell me what it is mostly about in one sentence.",
                "type": "open_response",
                "target_concept": "main_idea",
                "rubric": "Mastery: states main idea in one clear sentence. Proficient: close but includes extra details. Developing: retells details without identifying the main idea.",
            },
            {
                "prompt": "Name two details from the passage that support the main idea.",
                "type": "open_response",
                "target_concept": "supporting_details",
                "rubric": "Mastery: names 2+ relevant details and connects them to the main idea. Proficient: names details. Developing: cannot distinguish details.",
            },
            {
                "prompt": "What would be a good title for this passage?",
                "type": "open_response",
                "target_concept": "main_idea_title",
                "rubric": "Mastery: title captures the main idea precisely. Proficient: title is related but too broad or narrow. Developing: title reflects a detail, not the main idea.",
            },
        ],
        "resource_guidance": {
            "required": [
                "short reading passages at the child's level (fiction and nonfiction)",
                "paper for writing main idea sentences",
            ],
            "recommended": [
                "main idea graphic organizer (hand or umbrella template)",
                "leveled reading books with comprehension questions",
            ],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Read passages aloud to the child first so comprehension is not blocked by decoding difficulty. Use shorter passages (3-5 sentences). Provide the main idea as a sentence frame: 'This passage is mostly about ___.'",
            "adhd": "Use high-interest passages about topics the child cares about (animals, sports, space). Keep passages short (4-6 sentences). Use the physical hand organizer — tactile interaction helps focus.",
            "gifted": "Use longer passages and chapter-level summaries. Introduce the concept of theme (the lesson or message) alongside main idea. Practice main idea identification in nonfiction articles about science and history.",
            "visual_learner": "Main idea umbrella graphic organizer: umbrella = main idea, raindrops = details. Highlight the main idea sentence in one color and details in another.",
            "kinesthetic_learner": "Sort physical sentence strips into main idea vs detail piles. Use hand metaphor with actual hand tracing.",
            "auditory_learner": "Oral retelling: 'Tell me in one sentence what that was about.' Discuss before writing. Think-aloud modeling by the parent.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Comprehension is the whole point of reading. The main idea is what a passage is mostly about, the big umbrella that covers all the details. Today we find the main idea, state it in one sentence, and tell it apart from the supporting details.",
                "gradual_release": {
                    "i_do": "Read a short three-sentence paragraph aloud, then model finding its heart: this paragraph is mostly about. Use the hand metaphor, the palm for the main idea and the fingers for the details, and contrast the topic, a word or two, with the main idea, a whole thought.",
                    "we_do": "Read a short passage together, name its main idea and its details with the hand metaphor, and choose the best title from a few options together.",
                    "you_do": "Child reads a passage, states its main idea in one sentence, names two or three key supporting details, and tells a main idea apart from a detail.",
                },
                "guided_practice": [
                    "Main idea in a hand: write the main idea on the palm and a detail on each finger",
                    "Title match: read a passage and choose the best title from three",
                    "Sort sentence strips into a main-idea pile and a detail pile",
                ],
                "independent_practice": [
                    "Write the main idea of a passage in one sentence",
                    "Retell in one sentence what a passage was mostly about, after reading it",
                ],
                "mastery_check": [
                    "State the main idea of a short passage in one sentence",
                    "Distinguish the main idea from the supporting details",
                    "Name two or three key details that explain or prove the main idea",
                ],
                "spiral_review": [
                    "Revisit the difference between a topic and a main idea on familiar passages",
                ],
            },
            "classical": {
                "narrative_introduction": "A passage, like a building, rests on one central truth, with many details set upon it. To find the main idea is to find that central truth. The fable, which states its moral plainly, is the clearest school of this skill.",
                "memory_work": {
                    "chants": [
                        "Chant the distinction: the topic is a word or two; the main idea is a whole thought",
                    ],
                    "recitations": [
                        "Memorize and recite short fables, and recite each fable's moral, which is its main idea distilled into a sentence",
                    ],
                },
                "copywork": [
                    "Copy the one-sentence main idea of a passage neatly, and copy the moral of a fable",
                ],
                "recitation_routine": "Begin each lesson by reciting a memorized fable and naming its moral as its main idea before turning to new passages; the repertoire of fables grows cumulatively.",
                "history_integration": "Find and state the main idea of short narrative passages drawn from history, so the skill is practiced on texts along the chronological spine.",
                "read_aloud_suggestions": [
                    "Fables and well-made short passages, read aloud and paused over to name what each one is mostly about",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "Living books and well-told short passages worth narrating, in language beautiful enough to hold the child's full attention",
                ],
                "short_lesson_flow": "Read a short passage aloud once, attentively. The child then narrates it back in their own words. In the telling, the heart of the passage comes out on its own; name it gently as the main idea. Stop while the child is still interested.",
                "narration_prompt": "Tell me back what you read, and then, in just one sentence, tell me what it was mostly about.",
                "real_world_objects": [
                    "A nature walk summarized in a sentence afterward",
                    "A book told to a parent, sharing the heart of it and not every word",
                    "Headlines that capture a story in a few words",
                ],
                "nature_connection": "After a nature walk, the child says in one sentence what the walk was mostly about, and writes that sentence in the nature notebook.",
                "habit_focus": "The habit of attention: reading or listening once, fully, so that the whole passage can be told back truly.",
            },
            "montessori": {
                "prepared_materials": [
                    "Reading cards holding short passages",
                    "Main-idea cards and detail cards for matching and sorting",
                    "Control cards that carry the answer for self-checking",
                ],
                "presentation": {
                    "three_period_lesson": "With a passage and the main-idea cards: this is the main idea of the passage; show me the main idea; what is this passage mostly about?",
                    "steps": [
                        "Read a passage card",
                        "Choose the main-idea card that fits the passage, then check it against the control card",
                        "Sort the detail cards beneath the main idea they support",
                    ],
                },
                "control_of_error": "The control card carries the answer, so the child checks the main idea they chose for themselves and corrects it without an adult's word.",
                "abstraction_pathway": "From matching a passage to a given main-idea card, to sorting its details beneath it, toward stating a passage's main idea in one's own sentence with no cards at all.",
                "extensions": [
                    "Work with passages where the main idea must be inferred from the details",
                    "Write the main idea of a chosen passage in one sentence",
                ],
                "observation_focus": "Watch for the child distinguishing the central idea of a passage from a striking but secondary detail.",
            },
            "unschooling": {
                "invitations": [
                    "Keep varied reading within reach: storybooks, magazines, comics, and nonfiction the child is drawn to",
                    "Talk often and naturally about stories, books, and films the family shares",
                    "Leave news headlines and book blurbs where the child will notice their brief summaries",
                ],
                "real_world_contexts": [
                    "Telling someone what a book or a film was mostly about",
                    "Reading headlines, which capture a story's main idea in a few words",
                    "Summing up a day or an outing in a sentence",
                    "Describing to a friend what a game or a show is about",
                ],
                "conversation_starters": [
                    "If you had to tell me in just one sentence what that was about, what would you say?",
                    "What would be a good title for that? A title usually catches the main idea.",
                    "Was the brown dog the main thing the story was about, or just a detail?",
                ],
                "resource_bank": [
                    "Varied storybooks, magazines, and nonfiction kept available",
                    "Films and shows the family discusses together",
                    "Picture books and short articles for talking over",
                ],
                "parent_role": "After stories, walks, and films, ask naturally what it was mostly about, and model summing things up in one sentence. Follow what the child chooses to read, and treat the conversation as real talk rather than a quiz.",
                "observation_documentation": "Over time, note whether the child can say what something is mostly about in one sentence, tells the main idea apart from the details, and can name the details that support it. This noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Main idea is like finding the total in a word problem — what is the BIG question being asked?",
            "science": "Every science experiment has a main idea: what are we trying to find out?",
            "history": "Summarizing a historical event: what is the main thing that happened?",
        },
    },
    "rf-13": {
        "enriched": True,
        "learning_objectives": [
            "Retell the events of a story in the correct order from beginning to end",
            "Identify and use sequence signal words: first, next, then, after, finally",
            "Arrange story events in chronological order when given out of sequence",
            "Describe a story's structure as having a beginning, middle, and end",
        ],
        "teaching_guidance": {
            "introduction": "Stories happen in order. Understanding sequence — what happened first, next, and last — is how children organize meaning from text. Sequence signal words like 'first,' 'then,' 'next,' 'after that,' and 'finally' are road signs that guide the reader through a story's events. This skill builds directly on main idea: once a child knows WHAT a passage is about, they need to understand the ORDER in which things happen.",
            "scaffolding_sequence": [
                "Start with the child's own life: 'Tell me what you did today, in order. What happened first? Then what?'",
                "Read a simple three-event story aloud and retell it together: beginning, middle, end",
                "Introduce signal words (first, next, then, finally) using a daily routine the child knows well",
                "Read a short story and draw three pictures showing beginning, middle, and end",
                "Give the child 4-5 sentence strips from a familiar story and have them arrange in order",
                "Practice retelling unfamiliar stories using signal words without looking back at the text",
                "Identify signal words within a passage and explain how they help the reader track order",
                "Apply sequencing to nonfiction: how-to texts, recipes, science procedures",
            ],
            "socratic_questions": [
                "What happened at the very beginning of this story, before anything else?",
                "You told me the boy found the treasure. What happened right BEFORE he found it?",
                "The story says 'then the rabbit ran home.' What word tells us this happened after something else?",
                "If I mixed up the events in this story, would it still make sense? Why or why not?",
            ],
            "practice_activities": [
                "Story sequence cards: draw or write events on index cards, scramble them, put them back in order",
                "Retelling with props: use small toys or figures to act out a story in order after reading it",
                "Recipe sequencing: follow a simple recipe and notice the order words (first mix, then pour, next bake)",
                "Daily routine timeline: the child draws their day in order on a strip of paper",
            ],
            "real_world_connections": [
                "Following recipe steps in order while cooking: first measure, then mix, next bake",
                "Telling a parent about something that happened: 'First we went to the park, then we saw ducks'",
                "Building or crafting projects: the steps must happen in order for the project to work",
                "Retelling a family event: 'First we drove there, then we set up the tent, finally we made a campfire'",
            ],
            "common_misconceptions": [
                "Retelling the most exciting event first instead of the first event — children often start with what they found most interesting rather than what happened first",
                "Confusing the order of events with the order of sentences on the page — sometimes stories use flashbacks or non-chronological ordering",
                "Leaving out the middle of the story — children often remember the beginning and end but skip the events in between",
                "Not recognizing 'after,' 'before,' and 'while' as sequence words because they're less obvious than 'first' and 'next'",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Retells a story with at least 4 events in the correct order",
                "Uses 3+ sequence signal words naturally in retelling",
                "Arranges scrambled story events in correct chronological order",
            ],
            "proficiency_indicators": [
                "Retells events mostly in order with one or two reversals",
                "Uses 'first' and 'then' but may not use other signal words",
            ],
            "developing_indicators": [
                "Retells random events from the story without clear order",
                "Needs prompting ('What happened first? Then what?') to sequence events",
            ],
            "assessment_methods": ["oral retelling", "sentence strip ordering", "written sequence using signal words"],
            "sample_assessment_prompts": [
                "Tell me what happened in this story from the beginning to the end.",
                "Put these four events in the order they happened in the story.",
                "Use the words 'first,' 'next,' 'then,' and 'finally' to retell this story.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Read this story: 'Sam woke up. He ate breakfast. He brushed his teeth. He went to play outside.' What happened first?",
                "expected_type": "multiple_choice",
                "options": ["He ate breakfast", "Sam woke up", "He went to play outside", "He brushed his teeth"],
                "correct_answer": "Sam woke up",
                "hints": ["Look at the very first thing that happened in the story."],
                "explanation": "Sam woke up first. That is the beginning of the story, before everything else happened.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What happened AFTER Sam ate breakfast?",
                "expected_type": "text",
                "correct_answer": "He brushed his teeth.",
                "hints": ["Find 'ate breakfast' in the story. What happens in the next sentence?"],
                "explanation": "After eating breakfast, Sam brushed his teeth. Then he went to play outside.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Read this: 'First, the caterpillar ate many leaves. Then, it made a cocoon. Next, it rested inside the cocoon for a long time. Finally, a butterfly came out.' How many signal words can you find?",
                "expected_type": "number",
                "correct_answer": "4",
                "hints": [
                    "Signal words tell the ORDER of events. Look for words like 'first,' 'then,' 'next,' 'finally.'"
                ],
                "explanation": "Four signal words: first, then, next, finally. These tell us the order of events.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "These events are scrambled. Put them in order: (A) The bird flew away. (B) A bird built a nest. (C) Eggs hatched into baby birds. (D) The bird laid three eggs.",
                "expected_type": "text",
                "correct_answer": "B, D, C, A",
                "hints": ["Think about what has to happen first for the next thing to be possible."],
                "explanation": "Correct order: B (built nest), D (laid eggs), C (eggs hatched), A (bird flew away). Each event leads to the next.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Retell this story using the signal words 'first,' 'next,' 'then,' and 'finally': 'Lucy found a box. She opened it. Inside was a puppy. She named it Spot.'",
                "expected_type": "text",
                "hints": ["Start with 'First, Lucy...' and use a new signal word for each event."],
                "explanation": "Example: First, Lucy found a box. Next, she opened it. Then, she saw a puppy inside. Finally, she named it Spot.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Retell this story from beginning to end, using signal words.",
                "type": "open_response",
                "target_concept": "sequence_retelling",
                "rubric": "Mastery: retells 4+ events in order with signal words. Proficient: mostly in order, uses some signal words. Developing: events out of order, no signal words.",
            },
            {
                "prompt": "What signal word tells you something happened last?",
                "type": "text",
                "correct_answer": "finally",
                "target_concept": "signal_words",
            },
            {
                "prompt": "Arrange these three events in order from a story you just read.",
                "type": "open_response",
                "target_concept": "event_ordering",
                "rubric": "Mastery: all three correct. Proficient: two correct. Developing: random order.",
            },
        ],
        "resource_guidance": {
            "required": ["short stories with clear sequential events", "index cards or sentence strips for sequencing"],
            "recommended": ["sequence graphic organizer (timeline or numbered boxes)", "signal word reference card"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Read stories aloud so decoding doesn't interfere with comprehension. Use picture sequence cards rather than text. Provide a signal word bank the child can reference.",
            "adhd": "Use stories about high-interest topics. Act out the story physically with props, then retell. Keep stories to 4-5 events maximum to avoid overwhelm.",
            "gifted": "Introduce more complex sequence structures: parallel events, flashbacks. Practice sequencing longer passages with 6-8 events. Begin written retelling.",
            "visual_learner": "Story maps and timeline graphic organizers. Draw the events in order. Color-code signal words.",
            "kinesthetic_learner": "Act out the story. Arrange physical cards on a table or floor. Walk along a timeline taped to the floor.",
            "auditory_learner": "Oral retelling games. Retell to a partner. Listen for signal words during read-alouds.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Stories happen in order. Understanding what came first, next, and last is how a reader organizes meaning. Signal words such as first, next, then, after, and finally are road signs through a story. Today we retell stories in order, use the signal words, and name a story's beginning, middle, and end.",
                "gradual_release": {
                    "i_do": "Read a simple three-event story aloud and model retelling it: at the beginning, then in the middle, and at the end. Point out the signal words and explain that they tell the reader the order.",
                    "we_do": "Retell a short story together using the signal words, and arrange a few scrambled sentence strips from a familiar story into the right order together.",
                    "you_do": "Child retells a story's events in the correct order using signal words, arranges scrambled events chronologically, and names the story's beginning, middle, and end.",
                },
                "guided_practice": [
                    "Arrange scrambled story-event cards back into the correct order",
                    "Retell a story with the signal words first, next, then, after, finally",
                    "Draw three pictures showing a story's beginning, middle, and end",
                ],
                "independent_practice": [
                    "Retell an unfamiliar story in order without looking back at the text",
                    "Number the events of a passage one through four",
                ],
                "mastery_check": [
                    "Retell a story's events in the correct order from beginning to end",
                    "Use the sequence signal words correctly",
                    "Arrange out-of-order story events into chronological order",
                ],
                "spiral_review": [
                    "Revisit retelling the order of the child's own familiar daily routine before sequencing new stories",
                ],
            },
            "classical": {
                "narrative_introduction": "Every story moves in order, one event giving rise to the next. To retell a story rightly, in the order it happened, is the first work of narrative, and the ground on which all later composition is built.",
                "memory_work": {
                    "chants": [
                        "Chant the sequence signal words in order: first, next, then, after that, finally",
                        "Chant the shape of a story: a beginning, a middle, and an end",
                    ],
                    "recitations": [
                        "Memorize and recite short fables and myths whose events run in a clear order, retelling them in sequence from beginning to end",
                    ],
                },
                "copywork": [
                    "Copy a short ordered retelling of a story, the signal words and their commas kept in place",
                ],
                "recitation_routine": "Begin each lesson by retelling, in order, a fable or story already memorized before turning to a new one; the repertoire of well-ordered stories grows cumulatively.",
                "history_integration": "Retell the events of a simple history story in the order they happened, placing them on a timeline, so sequencing is practiced on the chronological spine itself.",
                "read_aloud_suggestions": [
                    "Fables, myths, and well-told tales with clear, strong sequences of events, read aloud",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "Living storybooks with clear, well-shaped sequences of events, told in language worth one attentive reading",
                ],
                "short_lesson_flow": "Read a short story aloud once, attentively, without re-reading. The child then narrates it back, and the telling naturally comes out in order, from beginning to end. Stop while the child is still glad to be telling.",
                "narration_prompt": "Tell me the story back in your own words, from what happened first all the way to how it ended.",
                "real_world_objects": [
                    "The events of the child's own day, told in order",
                    "The steps of a recipe followed in order while cooking",
                    "A family outing retold from first to last",
                ],
                "nature_connection": "After a nature walk, the child retells the walk in order, first, next, finally, and may draw a small ordered strip of it in the nature notebook.",
                "habit_focus": "The habit of attention: listening once, fully, so that the whole story can be told back in its true order without re-reading.",
            },
            "montessori": {
                "prepared_materials": [
                    "Story sequence cards, with the correct order numbered on the back for self-checking",
                    "Story strips the child arranges into order independently",
                    "Small figures and objects for acting a story out in sequence",
                ],
                "presentation": {
                    "three_period_lesson": "With the sequence cards: this card is the beginning; show me the beginning; where in the story does this card belong?",
                    "steps": [
                        "Read or recall a short story",
                        "Lay the scrambled sequence cards in the order the events happened",
                        "Turn the cards over and check the order against the numbers on the back",
                    ],
                },
                "control_of_error": "The numbers on the back of the sequence cards let the child check the order they built for themselves and correct it without an adult's word.",
                "abstraction_pathway": "From arranging the picture sequence cards by hand, to ordering written story strips, toward retelling any story in correct order with no cards at all.",
                "extensions": [
                    "Sequence the steps of a recipe or a how-to text",
                    "Act a story out in order with small figures after reading it",
                ],
                "observation_focus": "Watch for the child holding the order of events steadily and using the signal words as they retell.",
            },
            "unschooling": {
                "invitations": [
                    "Keep storybooks with strong, clear sequences within reach",
                    "Leave small figures and props out for acting stories through in order",
                    "Let simple recipes and craft instructions be available, where order genuinely matters",
                ],
                "real_world_contexts": [
                    "Telling a parent about something that happened, first this, then that",
                    "Following a recipe in order while cooking: first measure, then mix, next bake",
                    "Building or crafting, where the steps must come in the right order to work",
                    "Retelling a family trip from beginning to end",
                ],
                "conversation_starters": [
                    "What happened at the very beginning, before anything else?",
                    "You said the boy found the treasure. What happened right before that?",
                    "If we mixed up the steps of this recipe, would it still work? Why not?",
                ],
                "resource_bank": [
                    "Storybooks with clear sequences, kept available",
                    "Small figures and props for acting stories out",
                    "Simple recipes and craft instructions",
                ],
                "parent_role": "Invite the child to tell back stories and real happenings in order, and notice aloud the order words in recipes and instructions you use together. Follow the stories the child loves, and treat the retelling as real sharing rather than a quiz.",
                "observation_documentation": "Over time, note whether the child retells events in the correct order, uses the sequence signal words, can reorder scrambled events, and speaks of a story as having a beginning, a middle, and an end. This noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Sequence in math: first add, then subtract. Order of operations is a sequence.",
            "science": "Science experiments follow a sequence: first hypothesize, then test, then observe results",
            "history": "History IS sequence: events happen in chronological order on a timeline",
        },
    },
    "rf-14": {
        "enriched": True,
        "learning_objectives": [
            "Identify the main characters in a story and describe their roles",
            "Describe character traits using evidence from the text (what the character says, does, and thinks)",
            "Explain how a character feels at different points in a story and why",
            "Compare two characters within the same story or across stories",
        ],
        "teaching_guidance": {
            "introduction": "Characters are the people (or animals, or creatures) that stories happen to. Understanding characters means more than naming them — it means noticing what they say, what they do, how they feel, and why they behave the way they do. This is the beginning of empathy in reading: the child starts to see the world through someone else's eyes. It also builds the foundation for literary analysis that deepens throughout education.",
            "scaffolding_sequence": [
                "Start with a familiar character from a favorite book: describe what they look like, how they act, what they are like as a person",
                "Read a short story and name all the characters — distinguish main characters from minor ones",
                "Introduce character traits as describing words: brave, kind, silly, shy, curious — find evidence in the text",
                "Track a character's feelings throughout a story: how did they feel at the beginning? The middle? The end? What changed?",
                "Ask WHY a character did what they did — what motivated them? What did they want?",
                "Compare two characters: How are they alike? How are they different?",
                "Use evidence from the text to support descriptions: 'I think she is brave because she...'",
                "Apply character analysis to nonfiction: real people in biographies and history",
            ],
            "socratic_questions": [
                "What kind of person is this character? What words would you use to describe them?",
                "The character said something mean. Does that make them a mean person, or were they just having a bad day? How do you know?",
                "How do you think the character felt when that happened? What clues in the story tell you that?",
                "If you met this character in real life, would you want to be friends? Why or why not?",
            ],
            "practice_activities": [
                "Character portrait: draw the character and write 3 describing words around the picture, with evidence from the story",
                "Character feelings timeline: draw the character's face showing their emotion at the beginning, middle, and end of the story",
                "Hot seat: pretend to BE the character while a parent asks you questions. Answer as the character would.",
                "Character comparison: draw two characters side by side and list what is the same and different about them",
            ],
            "real_world_connections": [
                "Describing real people uses the same skills: 'Grandma is patient because she always waits for me'",
                "Understanding why siblings or friends behave the way they do — character motivation in real life",
                "Noticing character traits in people from history or current events",
                "Recognizing that real people (like characters) can feel different emotions at different times",
            ],
            "common_misconceptions": [
                "Describing only what a character LOOKS like rather than what they are LIKE as a person (appearance vs traits)",
                "Thinking characters are all good or all bad — real characters (like real people) are complex mixtures",
                "Confusing what happened TO a character with what a character IS — 'She fell down' describes an event, not a trait",
                "Assuming the character feels the same way the child would feel — different characters respond differently to the same situation",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Names main characters and describes 2+ traits with text evidence for each",
                "Tracks how a character's feelings change throughout a story",
                "Explains character motivation using evidence from the text",
            ],
            "proficiency_indicators": [
                "Names characters and gives 1-2 traits but may not cite specific text evidence",
                "Identifies how a character feels at one point in the story",
            ],
            "developing_indicators": [
                "Names characters but describes them only by appearance",
                "Cannot explain why a character acted a certain way",
            ],
            "assessment_methods": ["character description", "feelings tracking", "character comparison"],
            "sample_assessment_prompts": [
                "Tell me about the main character. What kind of person are they? How do you know?",
                "How did the character feel at the beginning of the story? How did they feel at the end? What changed?",
                "Compare these two characters: How are they alike? How are they different?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Read this: 'Tom shared his lunch with a boy who had no food. He helped his little sister tie her shoes. He always said please and thank you.' What word best describes Tom?",
                "expected_type": "multiple_choice",
                "options": ["mean", "kind", "scared", "silly"],
                "correct_answer": "kind",
                "hints": ["Look at what Tom DOES. What kind of person shares, helps, and says please?"],
                "explanation": "Tom is kind. The evidence: he shares, helps his sister, and uses polite words. These are kind actions.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "In a story, a girl screams and runs when she sees a spider. How is the girl feeling?",
                "expected_type": "text",
                "correct_answer": "scared",
                "hints": ["What would make someone scream and run away?"],
                "explanation": "The girl is scared. Screaming and running are actions that show fear.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Read this: 'Maya wanted to climb the tall tree, but her hands were shaking. She took a deep breath and grabbed the first branch. Step by step, she made it to the top.' What character trait does Maya show?",
                "expected_type": "text",
                "hints": [
                    "Maya was afraid but she did it anyway. What do we call someone who does something even though they are scared?"
                ],
                "explanation": "Maya is brave (or courageous). She was scared (her hands were shaking) but she climbed the tree anyway. Bravery is doing something even when you're afraid.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: A character who does one bad thing is always a bad character.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": [
                    "Think about real people. If your friend makes one mistake, does that make them a bad person?"
                ],
                "explanation": "False. Characters, like real people, are complex. A character can make a mistake and still be a good character overall. We look at everything they do, not just one action.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Read this: 'At the beginning of the story, Jack was angry and wouldn't talk to anyone. By the end, he was laughing and playing with his friends.' How did Jack's feelings change? Why do you think they changed?",
                "expected_type": "text",
                "hints": [
                    "Compare the beginning to the end. What was different? Think about what might have happened in the middle."
                ],
                "explanation": "Jack changed from angry to happy. Something in the middle of the story caused his feelings to change — maybe his friends helped him, or he solved a problem. Characters' feelings often change as the story progresses.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Describe the main character using three words. Give evidence from the story for each word.",
                "type": "open_response",
                "target_concept": "character_traits",
                "rubric": "Mastery: three traits with text evidence. Proficient: two traits with some evidence. Developing: describes appearance only.",
            },
            {
                "prompt": "How did the character feel at the end of the story? What in the story tells you that?",
                "type": "open_response",
                "target_concept": "character_feelings",
                "rubric": "Mastery: names feeling and cites specific text evidence. Proficient: names feeling. Developing: guesses without evidence.",
            },
            {
                "prompt": "Why did the character do what they did at the climax of the story?",
                "type": "open_response",
                "target_concept": "character_motivation",
                "rubric": "Mastery: explains motivation with text evidence. Proficient: gives a reasonable guess. Developing: says 'I don't know.'",
            },
        ],
        "resource_guidance": {
            "required": ["story books with well-developed characters", "paper for character portraits"],
            "recommended": [
                "character trait word list (brave, kind, curious, stubborn, shy, etc.)",
                "character comparison graphic organizer",
            ],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Read stories aloud so the child focuses on comprehension, not decoding. Use picture books with expressive illustrations that show character feelings. Provide a word bank of character trait words.",
            "adhd": "Use stories with action-oriented characters the child identifies with. Character 'hot seat' role play adds physical engagement. Keep character discussions to 10 minutes.",
            "gifted": "Analyze morally complex characters who are neither all good nor all bad. Compare characters across different books. Begin discussing how authors create characters through word choice.",
            "visual_learner": "Character trait webs with the character in the center and traits branching out. Draw character expressions at different story points.",
            "kinesthetic_learner": "Hot seat role play: BE the character and answer questions. Act out scenes to understand character motivation.",
            "auditory_learner": "Discuss characters aloud like talking about a real person. 'What would you say to this character?' Voice-act the character's lines.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "A character is a person, animal, or creature that a story happens to. To understand a character is to look past what they look like and notice what they say, what they do, and what they think, since those are the evidence of what kind of person they are. Today we name the main characters, describe their traits using evidence from the text, explain how a character feels and why, and compare two characters.",
                "gradual_release": {
                    "i_do": "Read a short passage aloud and think aloud: name the main character, then point to a line and say, she gave away her lunch, so I would call her generous. Name a feeling and the line that shows it. Set two characters side by side and name one likeness and one difference.",
                    "we_do": "Read a story together, list the characters and mark the main ones, and for each trait find the line in the text that proves it. Track one character's feelings from beginning to end together.",
                    "you_do": "Child names the main characters and their roles, gives at least two traits for a character with text evidence for each, explains how the character feels at two points and why, and compares two characters.",
                },
                "guided_practice": [
                    "List a story's characters and sort main characters from minor ones",
                    "Name a character trait and underline the words in the text that prove it",
                    "Track a character's feelings at the beginning, middle, and end of a story",
                ],
                "independent_practice": [
                    "Write three trait words for a main character, each with a line of text evidence",
                    "Compare two characters in writing: one way they are alike, one way they differ",
                ],
                "mastery_check": [
                    "Name the main characters and describe each one's role",
                    "Give two traits for a character, each supported by evidence from the text",
                    "Explain how and why a character's feelings change, and compare two characters",
                ],
                "spiral_review": [
                    "Revisit retelling a story's events, since a character's traits and feelings are read out of what happens",
                ],
            },
            "classical": {
                "narrative_introduction": "Stories have always been a school of the human heart. The people in a tale show us courage and cowardice, kindness and cruelty, and by watching them we learn to know such things in ourselves. To study a character is to ask not only what they did but what kind of soul would do it, and what their words, deeds, and thoughts reveal.",
                "memory_work": {
                    "chants": [
                        "Chant the questions of character study: what does the character say, what does the character do, what does the character think, and what does that reveal",
                        "Chant a list of trait words in pairs: brave and timid, generous and selfish, honest and false, patient and hasty",
                    ],
                    "recitations": [
                        "Recite a short, noble speech of a worthy character, and tell what virtue it shows",
                    ],
                },
                "copywork": [
                    "Copy a sentence in which a character's words or deeds reveal a virtue or a fault, and underline the words that show it",
                ],
                "recitation_routine": "Begin each lesson by recalling characters met before and the virtue or fault each displayed, so the gallery of characters is rehearsed cumulatively.",
                "history_integration": "Tell that the oldest stories, the fables of Aesop and the tales of heroes, were told to teach character, and that the men and women of history are themselves characters whose traits and motives can be weighed.",
                "read_aloud_suggestions": [
                    "A fable or hero tale with a character of clear and weighable virtue, read aloud for its moral force",
                    "A story whose chief character is neither wholly good nor wholly bad, so the child learns that a soul is a mixture",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A living book whose characters are real and complex, drawn with truth rather than as flat good or bad figures, never a contrived reader",
                ],
                "short_lesson_flow": "Read a portion of a living book in which a character acts or speaks. Pause and let the child narrate what the character did. Then talk about the character as though about a real person met in life: what kind of person is this, and how do you know? Keep it warm and unhurried.",
                "narration_prompt": "Tell me about this character as though you had met them. What kind of person are they, and would you trust them? Why?",
                "real_world_objects": [
                    "The living book itself, returned to again and again as the character is met in new chapters",
                    "A commonplace book where the child may note a character worth remembering",
                ],
                "nature_connection": "Notice that animals met in nature study, like characters, have their own ways: a cautious squirrel, a bold robin, a patient spider, and that watching them closely is the same attention a character asks for.",
                "habit_focus": "The habit of attention and of just judgment: knowing a person, real or in a book, by their words and deeds rather than by first appearance.",
            },
            "montessori": {
                "prepared_materials": [
                    "A shelf of well-chosen storybooks with real, complex characters",
                    "Character trait word cards, a printed bank of describing words such as brave, generous, timid, and curious",
                    "A character journal in which the child records a character, traits, and the text evidence",
                    "Three-part work: a character card, a trait card, and an evidence card to match",
                ],
                "presentation": {
                    "three_period_lesson": "With the trait cards and a known character: this character is generous, see how she shared; show me a character who is generous; what kind of character is this?",
                    "steps": [
                        "After a story, the child names the main characters and their roles",
                        "The child chooses a trait card and finds the line in the book that gives evidence for it",
                        "The child records the character, the trait, and the evidence in the character journal, and may compare two characters",
                    ],
                },
                "control_of_error": "The text itself is the control: a trait card can only be matched to a character if a line in the book supports it, and the child returns to the page to check, so an unsupported trait does not hold.",
                "abstraction_pathway": "From naming a character by what they plainly do, to matching a trait word to a line of evidence, toward describing a character's inner motive and feelings with no cards at all.",
                "extensions": [
                    "Keep an ongoing character journal across many books",
                    "Compare two characters from different stories on a self-made chart",
                    "Trace one character's changing feelings through a whole book",
                ],
                "observation_focus": "Watch for the child returning to the text for evidence rather than guessing, and beginning to speak of why a character acts, not only what they do.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a rich and varied bookshelf within reach, with characters of many kinds",
                    "Leave out drawing materials beside a favorite book for spontaneous character portraits",
                    "Have audiobooks and read-aloud time available so strong characters can be met without the work of decoding",
                ],
                "real_world_contexts": [
                    "Talking about characters in the books, films, and shows the child already loves",
                    "Wondering aloud about why a friend or family member acted as they did, the same skill turned on real people",
                    "Noticing characters in the stories of history and in the news",
                    "Playing pretend and stepping into a character's shoes",
                ],
                "conversation_starters": [
                    "What kind of person is that character? What makes you say so?",
                    "Why do you think they did that? What did they want?",
                    "How do you think the character felt right then? Have you ever felt that way?",
                    "Those two characters, how are they alike, and how are they different?",
                ],
                "resource_bank": [
                    "A wide home library and library visits for books with memorable characters",
                    "Audiobooks and films that tell strong stories",
                    "Drawing and dress-up materials for character play",
                ],
                "parent_role": "Talk about characters the way you would talk about real people you both know, with genuine curiosity rather than quizzing. Follow the child's own attachments to characters, and let conversations about why people, real and imagined, behave as they do arise naturally.",
                "observation_documentation": "Over time, note whether the child names main characters, describes them by what they say and do rather than how they look, explains their feelings and motives, and compares one to another. This noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Characters in math word problems have needs and goals — understanding the character helps solve the problem",
            "science": "Scientists have character traits: curiosity, persistence, honesty. Discussing famous scientists as characters.",
            "history": "Historical figures are characters in the story of history — what motivated them? What traits did they show?",
        },
    },
    "rf-15": {
        "enriched": True,
        "learning_objectives": [
            "Retell a passage in own words after a single reading or hearing",
            "Include key details — characters, setting, and major events — in the retelling",
            "Maintain chronological sequence during narration without prompting",
            "Develop the habit of attentive listening that produces coherent oral retelling",
        ],
        "teaching_guidance": {
            "introduction": "Oral narration is the simplest and most powerful comprehension tool available to a homeschool family. After reading a passage ONCE, the child retells it in their own words. This single practice trains attention (you must listen carefully because you only hear it once), comprehension (you must understand it to retell it), memory (you must hold the information), and language production (you must organize it into speech). Charlotte Mason called narration the act of 'knowing,' and it requires no worksheets, no special materials — just a book and a listener.",
            "scaffolding_sequence": [
                "Start with very short passages (2-3 sentences) and ask 'Tell me what happened' immediately after reading",
                "Gradually lengthen passages to one paragraph, then two, then a full page",
                "Model narration first: parent reads and narrates, then the child tries",
                "Resist prompting: give the child time to organize thoughts before narrating (10-15 seconds of silence is fine)",
                "If the child struggles, ask ONE open question: 'What happened first?' — then let them continue",
                "Practice daily with different text types: fiction, nonfiction, poetry, biography",
                "Build toward narrating a full chapter of a read-aloud after a single hearing",
                "Introduce narration variations: 'Tell it as if you were the main character' or 'Tell only the most important parts'",
            ],
            "socratic_questions": [
                "Tell me what happened in that passage. Take your time — I'm listening.",
                "You told me about the beginning and the end. What happened in the middle?",
                "That was a good narration. Was there anything you left out that you think is important?",
                "If you were telling a friend about this story, what would you make sure to include?",
            ],
            "practice_activities": [
                "Daily narration: after every read-aloud, the child narrates what they heard. Make this a habit, not an assignment.",
                "Narration to an audience: the child narrates to a sibling, grandparent, or stuffed animal — having a listener adds purpose",
                "Narration drawing: after narrating orally, draw a picture of the most important scene",
                "Narration chain: parent reads one passage and narrates; child reads the next passage and narrates. Take turns.",
            ],
            "real_world_connections": [
                "Telling a parent about what happened at a playdate or field trip — natural narration",
                "Recounting a nature observation: 'Tell me about the bird we watched'",
                "Narrating the steps of a project you completed: 'Tell Dad what we built today'",
                "Retelling a family story or memory: narration of real life",
            ],
            "common_misconceptions": [
                "Thinking the child must remember EVERY detail — narration is about the key ideas, not word-for-word recall",
                "Prompting too much: over-questioning turns narration into an interrogation. Ask one question, then let the child lead.",
                "Believing narration is too simple to be effective — research shows oral retelling is one of the strongest comprehension strategies available",
                "Expecting polished narration immediately — like any skill, narration improves with daily practice over weeks and months",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Narrates a full passage in own words with key details and correct sequence after a single reading",
                "Narrates without prompting, organizing the retelling independently",
                "Includes characters, setting, and main events in narration",
            ],
            "proficiency_indicators": [
                "Narrates most of the passage but may need one prompt to recall a section",
                "Includes key events but may omit setting or minor characters",
            ],
            "developing_indicators": [
                "Recalls only one or two details and needs multiple prompts",
                "Retells events out of order or mixes up characters",
            ],
            "assessment_methods": [
                "oral narration after read-aloud",
                "narration with increasing passage length",
                "unprompted retelling",
            ],
            "sample_assessment_prompts": [
                "I'm going to read this passage once. Then you tell me everything that happened, in your own words.",
                "Tell me about the story we just read. Start at the beginning.",
                "What were the most important things that happened in that chapter?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Listen to this short story: 'A little frog sat on a lily pad. A big fish jumped out of the water. The frog hopped away quickly.' Now retell it in your own words.",
                "expected_type": "text",
                "hints": [
                    "Start with what was happening at the beginning. Then tell what happened. Then tell how it ended."
                ],
                "explanation": "A good narration includes: the frog sitting on the lily pad (beginning), the fish jumping (event), and the frog hopping away (ending). The child should use their own words, not memorize the exact sentences.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "After hearing a story, what should you do FIRST before you start narrating?",
                "expected_type": "multiple_choice",
                "options": [
                    "Open the book and re-read it",
                    "Think about what happened, then start talking",
                    "Ask the parent to tell you what happened",
                    "Write it down first",
                ],
                "correct_answer": "Think about what happened, then start talking",
                "hints": ["Narration means YOU retell it. You heard it once — now think and talk."],
                "explanation": "Before narrating, take a moment to think about what happened in the story. Organize your thoughts, then start talking. No re-reading — you only get one chance to listen.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You narrated a story but forgot to mention WHERE it took place. Why is the setting important to include in a narration?",
                "expected_type": "text",
                "hints": ["Think about how knowing WHERE a story happens helps the listener picture it."],
                "explanation": "The setting helps the listener understand the story. A story that takes place on a mountain is very different from one at the beach. Including the setting makes the narration more complete and helps the listener picture what happened.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: A good narration must include every single detail from the passage.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["Think about what 'key details' means versus 'every detail.'"],
                "explanation": "False. A good narration includes the KEY details — the most important events, characters, and setting. You don't need to remember every single word or minor detail.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Listen to a longer story about a boy who lost his dog, searched the whole town, and finally found the dog at the fire station. Narrate this story, but tell it from the DOG'S perspective.",
                "expected_type": "text",
                "hints": [
                    "Instead of 'the boy searched,' think about what the DOG was doing and feeling during the story."
                ],
                "explanation": "Narrating from a different perspective is an advanced skill. The dog might have wandered off exploring, ended up at the fire station, and then been happy when the boy arrived. This exercises both comprehension and creative thinking.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "After a single reading, narrate what happened in this passage.",
                "type": "open_response",
                "target_concept": "oral_narration",
                "rubric": "Mastery: retells with key details, correct order, own words, no prompting. Proficient: retells most with 1 prompt. Developing: needs multiple prompts, sparse details.",
            },
            {
                "prompt": "What characters were in the story and what were they like?",
                "type": "open_response",
                "target_concept": "narration_characters",
                "rubric": "Mastery: names characters and describes traits. Proficient: names characters. Developing: cannot recall character names.",
            },
            {
                "prompt": "Where and when did this story take place?",
                "type": "open_response",
                "target_concept": "narration_setting",
                "rubric": "Mastery: describes setting with specific details. Proficient: gives general setting. Developing: cannot recall setting.",
            },
        ],
        "resource_guidance": {
            "required": ["quality read-aloud books at or slightly above the child's level", "a patient listener"],
            "recommended": [
                "narration journal for drawing scenes after narrating",
                "timer for building listening stamina",
            ],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 10},
        "accommodations": {
            "dyslexia": "Read aloud TO the child for narration practice — this separates comprehension from decoding. Start with very short passages (3 sentences). Accept narration in any form: drawing, acting out, or oral retelling.",
            "adhd": "Use high-interest books to sustain attention during the reading. Keep passages short initially (1 paragraph). Allow the child to stand or move while narrating. Narration to a real audience (sibling, grandparent) increases motivation.",
            "gifted": "Increase passage length rapidly. Introduce perspective narration (retell from a different character's viewpoint). Begin written narration alongside oral narration.",
            "visual_learner": "Allow drawing before or after narrating. Mental imagery: 'Picture the story in your mind like a movie before you tell me.'",
            "kinesthetic_learner": "Act out the story with props before narrating. Walk around while narrating. Use hand gestures.",
            "auditory_learner": "Strong natural fit. Record narrations and play them back. Narrate to different audiences for variety.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Narration is retelling. After hearing or reading a passage one time, the child tells it back in their own words. Because the passage is heard only once, narration trains attentive listening; because it must be retold, it trains comprehension, memory, and clear speech. Today we retell a passage in our own words, including the key details, the characters, the setting, and the major events, and we keep the events in the order they happened.",
                "gradual_release": {
                    "i_do": "Read a short passage aloud once, pause to think, then narrate it back: name the characters and the setting, tell the events in order, and keep to the key details rather than every word. Say plainly that the passage is not re-read.",
                    "we_do": "Read a short passage together once, then build the narration together: who was in it, where it happened, and what happened first, next, and last.",
                    "you_do": "Child listens to or reads a passage once, then retells it in their own words, unprompted, including the characters, setting, and major events in the order they occurred.",
                },
                "guided_practice": [
                    "Retell a two or three sentence passage immediately after a single reading",
                    "Retell a one-paragraph passage, naming the characters and setting",
                    "Retell with the events kept in the order they happened, beginning to end",
                ],
                "independent_practice": [
                    "Narrate a longer passage or a full page after a single reading, without prompting",
                    "Narrate daily after each read-aloud, lengthening the passage over time",
                ],
                "mastery_check": [
                    "Retell a passage in own words after a single reading, with no prompting",
                    "Include the characters, the setting, and the major events in the retelling",
                    "Keep the events of the retelling in correct chronological order",
                ],
                "spiral_review": [
                    "Revisit identifying a story's beginning, middle, and end, which gives the narration its order",
                ],
            },
            "classical": {
                "narrative_introduction": "Long before writing, all knowledge was carried by the telling: a tale heard once was held in the mind and told again. Narration is that ancient art. To hear a passage a single time, attend to it closely, and then tell it back faithfully in one's own words is the first and truest test of knowing, and it is the seed of all later composition.",
                "memory_work": {
                    "chants": [
                        "Chant what a good narration carries: the characters, the place, and the events in their right order",
                        "Chant the narrator's rule: listen once, listen well, then tell it true",
                    ],
                    "recitations": [
                        "Recite a short, well-told tale committed to memory, the recited word and the narrated word both being the practice of telling",
                    ],
                },
                "recitation_routine": "Begin each lesson by having the child narrate the previous reading from memory before any new passage is read; yesterday's telling is rehearsed before today's.",
                "history_integration": "Tell that the long poems and histories of old were composed and carried entirely by memory and the spoken voice, passed from teller to teller, and that narration keeps that art alive.",
                "read_aloud_suggestions": [
                    "A well-told tale with a clear line of events, read aloud once and then narrated back",
                    "A passage of fine narrative prose, read for its order and its language, then retold",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A living book of real literary worth, its language and its events both worth holding in the mind, never a dull reader",
                ],
                "short_lesson_flow": "Read a single passage of a living book aloud, once, calmly and with no interruption. Close the book. Wait quietly while the child gathers their thoughts, giving them unhurried silence. Then the child tells it back in their own words while you listen without correcting or prompting. Stop while attention is still whole.",
                "narration_prompt": "Tell me about the passage we just heard. Take your time, I am listening, and I will not stop you.",
                "real_world_objects": [
                    "The living book, read from once and then closed before the telling",
                    "A narration notebook in which the child may draw the scene they told",
                ],
                "nature_connection": "After a nature walk, ask the child to narrate what they saw, the same telling-back turned upon the living book of the outdoors: the bird, the weather, the small creature watched.",
                "habit_focus": "The habit of attention: listening so fully the first time that the passage is truly the child's own and can be told back whole.",
            },
            "montessori": {
                "prepared_materials": [
                    "A shelf of child-selected storybooks for independent reading and narration",
                    "Story picture cards a child may lay in order to support an early narration",
                    "A narration journal for drawing or, later, writing the retold scene",
                    "A quiet, prepared spot where a child may narrate to a listener without interruption",
                ],
                "presentation": {
                    "three_period_lesson": "With story picture cards from a known tale: this picture shows what happened first, this what happened next; show me what happened first; what part of the story is this?",
                    "steps": [
                        "The child reads or hears a passage once, in a quiet, prepared place",
                        "The child pauses, then retells the passage in their own words to a listener, uninterrupted",
                        "The child may lay the story picture cards in order or draw the scene in the narration journal to confirm the retelling",
                    ],
                },
                "control_of_error": "The story picture cards are the control of error for an early narrator: laid out of order, the story will not run true, and reordering them sets the retelling right. As the child grows, the book itself is the control, reopened only after the telling to check what was held.",
                "abstraction_pathway": "From retelling with picture cards in hand, to retelling a heard passage with no aid, toward narrating a long chapter after a single hearing and, in time, writing the narration down.",
                "extensions": [
                    "Narrate to a younger child or to a small group",
                    "Narrate across subjects, retelling a passage of history or a nature observation",
                    "Move from oral narration toward written narration in the journal",
                ],
                "observation_focus": "Watch for the child narrating unprompted, keeping the events in order, and including characters and setting, and watch whether attention during the single reading is whole.",
            },
            "unschooling": {
                "invitations": [
                    "Keep audiobooks and read-aloud time available so good stories are always within reach",
                    "Leave out drawing materials so a child may picture a story after hearing it",
                    "Have a cozy listening spot where telling and being told are part of daily life",
                ],
                "real_world_contexts": [
                    "Telling a parent all about a playdate, an outing, or a film, real-life narration",
                    "Recounting a nature walk: telling what bird or creature was watched",
                    "Retelling a favorite book to a sibling, a grandparent, or a stuffed animal",
                    "Passing on a family story heard from a grandparent",
                ],
                "conversation_starters": [
                    "Tell me about the part of the book we just read, I would love to hear it",
                    "What happened on your adventure today? Start at the beginning.",
                    "Could you tell that story to your little brother? He has not heard it.",
                    "What was the best part, and what happened right before it?",
                ],
                "resource_bank": [
                    "A wide home library, audiobooks, and library visits for stories worth retelling",
                    "Drawing materials for picturing a story after hearing it",
                    "Willing listeners: family, friends, and even a favorite toy",
                ],
                "parent_role": "Be a genuine, delighted listener whenever the child wants to tell about a book, a day, or an adventure, without quizzing or correcting. Tell stories yourself so retelling is simply part of how the family talks, and let the child's own eagerness to share carry the skill.",
                "observation_documentation": "Over time, note whether the child retells stories and events in their own words, keeps them in order, and includes who, where, and what happened, listening well enough the first time to tell it back. This noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Narrating the steps of a math solution: 'First I added, then I...' — oral explanation of process",
            "science": "Narrating observations from a nature walk or science experiment",
            "history": "Narrating what happened in a historical event after reading about it",
        },
    },
    "rf-16": {
        "enriched": True,
        "learning_objectives": [
            "Listen to a read-aloud of quality literature and answer questions about the text",
            "Respond to a read-aloud through discussion, drawing, or simple writing",
            "Make connections between a read-aloud text and personal experience",
            "Build comprehension skills through shared reading at a level above independent reading ability",
        ],
        "teaching_guidance": {
            "introduction": "Read-alouds open a door to language, stories, and ideas that are beyond what a child can read independently. When a parent reads aloud, the child accesses richer vocabulary, more complex sentence structures, and deeper stories than they could decode on their own. The child's JOB during a read-aloud is to listen, think, and respond — through discussion, drawing, or writing. This builds comprehension muscles that transfer directly to independent reading as decoding catches up.",
            "scaffolding_sequence": [
                "Begin with picture books the child loves — build the habit of listening and talking about what you read together",
                "After reading, ask simple questions: 'What was your favorite part? Why?'",
                "Introduce prediction pauses: stop mid-page and ask 'What do you think will happen next?'",
                "After reading, the child draws a picture showing their favorite scene or the most important event",
                "Expand responses to discussion: 'How did that story make you feel? Does it remind you of anything?'",
                "Introduce simple written response: the child writes one sentence about the story after narrating orally",
                "Progress to chapter books read over multiple sessions, discussing each chapter",
                "Encourage the child to ask THEIR OWN questions about the text — what confused them, what they wonder about",
            ],
            "socratic_questions": [
                "What was your favorite part of what we just read, and why?",
                "Did anything in this story surprise you? What did you expect to happen instead?",
                "Does this story remind you of anything in your own life?",
                "If you could ask the author one question about this story, what would you ask?",
            ],
            "practice_activities": [
                "Read-aloud response journal: after each read-aloud, the child draws a picture and writes (or dictates) one sentence",
                "Discussion walk: go for a walk after reading and talk about the story while moving — fresh air stimulates thinking",
                "Story comparison: after reading two books on a similar topic, discuss how they are alike and different",
                "Reader's theater from the read-aloud: parent and child act out a scene from the book they just read",
            ],
            "real_world_connections": [
                "Read-alouds about cooking lead to actually cooking a recipe from the book",
                "Read-alouds about nature lead to outdoor exploration: 'Let's go look for the kind of bird we read about'",
                "Read-alouds about historical events lead to family discussions about 'what would we have done?'",
                "Read-alouds become shared family references: 'Remember when the character did that? This is like that!'",
            ],
            "common_misconceptions": [
                "Thinking read-alouds are only for children who can't read yet — read-alouds benefit children at EVERY level because they expose them to language beyond their decoding ability",
                "Rushing through the read-aloud without pausing for discussion — the conversation is as valuable as the reading",
                "Believing the child must sit perfectly still during a read-aloud — some children listen better while drawing, fidgeting quietly, or lying on the floor",
                "Stopping read-alouds once the child can read independently — continue read-alouds through elementary years and beyond",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Answers comprehension questions about a read-aloud with specific details from the text",
                "Responds to a read-aloud through drawing, discussion, or writing that shows understanding",
                "Makes meaningful connections between the text and personal experience",
            ],
            "proficiency_indicators": [
                "Answers basic questions about the read-aloud but may miss details",
                "Responds with a drawing or sentence that relates to the story",
            ],
            "developing_indicators": [
                "Listens but has difficulty recalling details from the read-aloud",
                "Response (drawing or writing) is unrelated to the text or very vague",
            ],
            "assessment_methods": ["comprehension discussion", "response journal review", "prediction accuracy"],
            "sample_assessment_prompts": [
                "Tell me two things that happened in the chapter we just read.",
                "Draw a picture that shows the most important part of today's read-aloud.",
                "How does this story connect to something in your own life?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "After a read-aloud, your parent asks 'What was your favorite part?' Is it okay to say 'I don't know'?",
                "expected_type": "multiple_choice",
                "options": [
                    "Yes, it's always fine to say that",
                    "No — think about it for a moment, then pick the part you liked best and explain why",
                    "No — you must always choose the most exciting part",
                ],
                "correct_answer": "No — think about it for a moment, then pick the part you liked best and explain why",
                "hints": ["Part of being a good listener is thinking about what you heard. Give yourself a moment."],
                "explanation": "It's better to pause, think, and then share something you noticed or liked. There is no wrong favorite part — the goal is to think about the text and respond honestly.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Why do parents read books aloud that you could read yourself?",
                "expected_type": "text",
                "hints": [
                    "Think about the difference between what you CAN read alone and what you can UNDERSTAND when someone reads to you."
                ],
                "explanation": "Read-alouds let you hear stories that are above your reading level. You can understand and enjoy harder books when someone reads them to you, and this builds your vocabulary and comprehension for when you read those books on your own later.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "After a read-aloud about a girl who moved to a new town, you draw a picture of your own first day at a new activity. What kind of response is this?",
                "expected_type": "multiple_choice",
                "options": [
                    "A text-to-self connection",
                    "A prediction",
                    "A summary",
                    "A character description",
                ],
                "correct_answer": "A text-to-self connection",
                "hints": ["You connected the story to something in YOUR life. What is that called?"],
                "explanation": "This is a text-to-self connection. You connected the character's experience (moving to a new town) to your own experience (being new somewhere). This deepens comprehension.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "During a read-aloud, your parent stops in the middle and asks 'What do you think will happen next?' Why do they do this?",
                "expected_type": "text",
                "hints": ["Making predictions shows you are THINKING while listening, not just hearing words."],
                "explanation": "Predicting what will happen next shows active listening and thinking. It means you understand what has happened so far and are using clues to think ahead. This is a key comprehension strategy.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "You just heard a chapter about a character who faced a difficult choice. Write one sentence about what you would have done in that situation and why.",
                "expected_type": "text",
                "hints": ["There is no wrong answer. Think about what YOU would do and explain your reasoning."],
                "explanation": "A good response connects the text to your own thinking. For example: 'I would have told the truth because lying always makes things worse.' This shows comprehension AND personal reflection.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "After today's read-aloud, tell me what happened and what you thought about it.",
                "type": "open_response",
                "target_concept": "read_aloud_comprehension",
                "rubric": "Mastery: retells key events AND shares personal response. Proficient: retells events OR shares response. Developing: vague or unrelated response.",
            },
            {
                "prompt": "Draw a picture showing the most important part of the story and explain why you chose it.",
                "type": "open_response",
                "target_concept": "read_aloud_response",
                "rubric": "Mastery: drawing clearly relates to story with thoughtful explanation. Proficient: drawing relates to story. Developing: drawing is unrelated.",
            },
            {
                "prompt": "Does this story remind you of anything in your own life? Tell me about it.",
                "type": "open_response",
                "target_concept": "text_to_self",
                "rubric": "Mastery: makes specific connection with clear explanation. Proficient: makes a general connection. Developing: says 'no' or cannot connect.",
            },
        ],
        "resource_guidance": {
            "required": ["quality picture books or chapter books for read-aloud", "drawing supplies for response"],
            "recommended": [
                "read-aloud response journal (notebook for drawings and sentences)",
                "comfortable reading spot",
            ],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 5},
        "accommodations": {
            "dyslexia": "Read-alouds are a strength area for dyslexic children — listening comprehension often far exceeds reading comprehension. Use this time to build vocabulary, discussion skills, and story knowledge that will support reading as decoding develops.",
            "adhd": "Allow movement during read-alouds: drawing, squeezing a stress ball, lying on the floor. Choose high-interest books with action and humor. Keep read-aloud sessions to 15-20 minutes. Pause for brief discussion rather than saving all questions for the end.",
            "gifted": "Use read-alouds for above-level chapter books with complex themes. Encourage the child to ask their own questions and make predictions. Introduce literary discussion: 'Why do you think the author chose to end the chapter that way?'",
            "visual_learner": "Picture books with rich illustrations support comprehension. Drawing as the primary response mode. Use picture walks before reading.",
            "kinesthetic_learner": "Act out scenes after reading. Use props or stuffed animals to represent characters. Allow fidget tools during listening.",
            "auditory_learner": "Natural strength. Audiobooks alongside physical books. Discussion-heavy response. The child may want to retell the story aloud rather than draw or write.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "A read-aloud lets a child meet stories, vocabulary, and ideas richer than they could yet decode alone. During a read-aloud the child's work is to listen, think, and respond, by discussion, by drawing, or by simple writing. Today we listen to quality literature read aloud, answer questions about the text, respond to it, and make connections between the story and our own lives.",
                "gradual_release": {
                    "i_do": "Read a passage of quality literature aloud, modeling attentive listening: pause to wonder aloud what may happen next, answer a question about the text with a detail from it, and say plainly, this part reminds me of something in my own life.",
                    "we_do": "Read a passage together, then answer questions about it together, draw or talk about the favorite part, and name one way the story connects to the child's experience.",
                    "you_do": "Child listens to a read-aloud of quality literature, answers questions about the text with details, responds through discussion, drawing, or a written sentence, and makes a connection to their own life.",
                },
                "guided_practice": [
                    "Answer who, where, and what-happened questions after a read-aloud",
                    "Draw the most important scene and tell why it was chosen",
                    "Name one way the story connects to the child's own experience",
                ],
                "independent_practice": [
                    "Keep a response journal: after each read-aloud, draw and write or dictate one sentence",
                    "Follow a chapter book over several sessions, discussing each chapter",
                ],
                "mastery_check": [
                    "Answer comprehension questions about a read-aloud with specific details from the text",
                    "Respond to a read-aloud through drawing, discussion, or writing that shows understanding",
                    "Make a meaningful connection between the text and personal experience",
                ],
                "spiral_review": [
                    "Revisit retelling a passage in order, since comprehension of a read-aloud rests on holding its events",
                ],
            },
            "classical": {
                "narrative_introduction": "A good book read aloud is a feast set before the mind. Through the reader's voice the child meets language finer, stories larger, and ideas deeper than their own decoding could yet reach. To listen well to such a book, to weigh what is true and good and beautiful in it, and to answer it with one's own thought, is to be fed by the best that has been written.",
                "memory_work": {
                    "chants": [
                        "Chant the listener's work: listen well, think upon it, and answer with your own thought",
                        "Chant the three things to seek in a good book: what is true, what is good, what is beautiful",
                    ],
                    "recitations": [
                        "Recite a memorable passage or saying drawn from a read-aloud, so its language is kept by heart",
                    ],
                },
                "copywork": [
                    "Copy a fine sentence from the read-aloud, chosen for its beauty or its truth, neatly and with care",
                ],
                "recitation_routine": "Begin each session by recalling and reciting from the previous read-aloud before the next portion is read, so the great books met are rehearsed cumulatively.",
                "history_integration": "Tell that for most of history books were costly and few, and reading aloud was how a whole household shared a story, and that the practice joins the child to a long line of listeners.",
                "read_aloud_suggestions": [
                    "A work of great literature pitched above the child's own reading level, read aloud for its language and its ideas",
                    "A biography or historical tale that sets a worthy life before the child",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A living book, rich in language and idea, well above the child's independent reading level, never an abridged or twaddly version",
                ],
                "short_lesson_flow": "Settle somewhere comfortable and read a portion of a living book aloud, with feeling and without rushing. Read it once. Then close the book and let the child narrate it back, telling what they heard. A short, warm conversation may follow if it arises naturally. Stop while the book is still longed for.",
                "narration_prompt": "Tell me about the part of the book we just heard. What stayed with you most?",
                "real_world_objects": [
                    "The living book itself, a beautiful edition worth returning to",
                    "A narration or nature notebook where the child may draw a scene from the reading",
                ],
                "nature_connection": "When a read-aloud touches on a bird, a tree, or a season, carry it outdoors: go and look for the very thing the book described, and note it in the nature notebook.",
                "habit_focus": "The habit of attention: listening to a worthy book so fully that it becomes the child's own and can be told back.",
            },
            "montessori": {
                "prepared_materials": [
                    "A shelf of beautiful, child-selected books for shared reading",
                    "A response shelf with drawing materials, simple writing paper, and small figures for acting out a scene",
                    "A read-aloud response journal kept by the child",
                    "A quiet, comfortable reading corner prepared for listening",
                ],
                "presentation": {
                    "three_period_lesson": "With examples of response: this is a connection to your own life, this is a question about the story; show me a connection to your own life; what kind of response is this?",
                    "steps": [
                        "The child chooses a book and the adult reads it aloud in the prepared reading corner",
                        "After the reading, the child and adult talk about the text, the child answering and asking questions",
                        "The child chooses how to respond, by drawing, by writing, or by acting the scene with small figures, and records it in the response journal",
                    ],
                },
                "control_of_error": "The book itself is the control: a question about the text is answered by returning to the page, and the child sees when a recollection does not match what the book says. A response that wanders from the story is gently brought back to it.",
                "abstraction_pathway": "From listening and responding with a drawing close to the page, to discussing the text and asking one's own questions, toward holding a chapter book across many sessions and responding in writing.",
                "extensions": [
                    "Follow a chapter book over many sessions, with a response after each chapter",
                    "Compare two books on a like theme",
                    "Move from drawn response toward written response in the journal",
                ],
                "observation_focus": "Watch for the child listening with attention, answering with details from the text, asking their own questions, and connecting the story to their own life.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a rich, varied library within reach and read aloud generously, on the couch and at bedtime",
                    "Leave out drawing and writing materials so a child may respond to a story however they wish",
                    "Have audiobooks playing in the car and at quiet times so good stories are always at hand",
                ],
                "real_world_contexts": [
                    "Cuddling up for a read-aloud simply because the story is loved, not as a lesson",
                    "Reading a book about cooking and then making the recipe together",
                    "Reading about a bird or a place and then going to look for it",
                    "A story becoming a shared family reference talked about long after the reading",
                ],
                "conversation_starters": [
                    "What was your favorite part? What made you love it?",
                    "What do you think will happen next?",
                    "Did that remind you of anything that happened to you?",
                    "If you could ask the author one thing, what would it be?",
                ],
                "resource_bank": [
                    "A wide home library, audiobooks, and frequent library visits",
                    "Drawing, writing, and craft materials for responding to stories",
                    "Comfortable, inviting spots for reading together",
                ],
                "parent_role": "Read aloud often and with delight, choosing books above what the child can yet read alone, and follow their interests in what to read next. Talk about the stories as a real conversation rather than a quiz, and let connections to life and further exploration arise on their own.",
                "observation_documentation": "Over time, note whether the child listens with engagement to read-alouds, talks about the text, asks questions, responds through drawing or writing, and connects stories to their own life. This noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Read-alouds about math concepts (counting books, shape stories) build mathematical vocabulary",
            "science": "Read-alouds about nature, animals, and experiments build science vocabulary and curiosity",
            "history": "Read-alouds of historical fiction and biography bring history to life in ways textbooks cannot",
        },
    },
    "rf-17": {
        "enriched": True,
        "learning_objectives": [
            "Memorize and recite at least one poem with appropriate rhythm, expression, and feeling",
            "Identify rhyme and rhythm patterns in poems",
            "Express personal preferences for poems and explain why certain poems appeal to them",
            "Recognize that poetry uses language differently from prose — compressed, musical, image-rich",
        ],
        "teaching_guidance": {
            "introduction": "Poetry is language at its most musical. Children are naturally drawn to rhythm, rhyme, and the sound of words — they love tongue twisters, silly rhymes, and songs. Poetry recitation builds memory, trains the ear for language patterns, develops expression and public speaking confidence, and introduces children to beautiful language. Memorizing and performing poems is a skill that develops fluency, rhythm awareness, and a love of language.",
            "scaffolding_sequence": [
                "Begin with short, rhythmic poems the child enjoys — read them aloud together multiple times, emphasizing the beat",
                "Clap or tap the rhythm of a poem while reading it — make the beat physical and audible",
                "Identify rhyming words in the poem: 'Which words sound the same at the end?'",
                "Memorize a 4-line poem together: parent says a line, child repeats; build up line by line",
                "Practice reciting with expression: loud/soft, fast/slow, happy/serious to match the poem's mood",
                "Perform the memorized poem for a family member — recitation becomes a real performance",
                "Extend to longer poems (8-12 lines) and introduce poems without rhyme (free verse)",
                "Build a personal poetry collection: the child selects favorite poems and copies them into a special notebook",
            ],
            "socratic_questions": [
                "What do you notice about how this poem sounds when you read it aloud? Does it have a beat?",
                "Which words rhyme in this poem? Can you find all the rhyming pairs?",
                "How does this poem make you feel? Is it happy, sad, funny, or peaceful? What words give you that feeling?",
                "What pictures do you see in your mind when you hear this poem?",
            ],
            "practice_activities": [
                "Poetry teatime: once a week, read poems aloud over a special snack. Each family member shares a favorite.",
                "Rhythm walk: go for a walk and recite a memorized poem in rhythm with your steps",
                "Poem illustration: draw what you see in your mind while hearing a poem — visualizing the imagery",
                "Poetry performance: memorize a poem and present it to the family with expression and gestures",
            ],
            "real_world_connections": [
                "Song lyrics are poetry set to music — children who love songs already love poetry",
                "Jump rope rhymes, clapping games, and playground chants are all forms of poetry",
                "Greeting cards often contain short poems — read the poems in cards you receive",
                "Nature inspires poetry: after observing something beautiful outdoors, try describing it in poetic language",
            ],
            "common_misconceptions": [
                "Thinking all poems must rhyme — free verse is poetry too, and many great poems don't rhyme",
                "Reading poems in a flat, word-by-word monotone instead of with the rhythm and expression the poem demands",
                "Believing poetry is 'hard' or 'boring' — children who dislike poetry usually haven't found the right poems yet. Start with humor and silliness.",
                "Thinking memorization is outdated — memorized poems become permanent possessions of the mind, available for comfort, joy, and reference throughout life",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Recites a memorized poem of 4+ lines with appropriate rhythm and expression",
                "Identifies rhyming words and basic rhythm patterns in poems",
                "Expresses why they like or dislike a particular poem with specific reasons",
            ],
            "proficiency_indicators": [
                "Recites most of a memorized poem with some prompting",
                "Identifies some rhyming words in a poem",
            ],
            "developing_indicators": [
                "Can recite a few lines with significant prompting",
                "Enjoys hearing poems but cannot yet identify rhyme or rhythm",
            ],
            "assessment_methods": [
                "poem recitation performance",
                "rhyme and rhythm identification",
                "poetry preference discussion",
            ],
            "sample_assessment_prompts": [
                "Recite the poem you memorized. Use your best expression!",
                "Listen to this poem. Which words rhyme?",
                "Here are three poems. Which one is your favorite? Tell me why.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Listen to this poem: 'Twinkle, twinkle, little star, / How I wonder what you are.' Which two words rhyme?",
                "expected_type": "text",
                "correct_answer": "star and are",
                "hints": ["Rhyming words sound the same at the end. Listen to the last word of each line."],
                "explanation": "'Star' and 'are' rhyme — they end with the same sound. Rhyming words are a key feature of many poems.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "True or false: All poems have to rhyme.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["Think about whether you've ever heard a poem that didn't rhyme."],
                "explanation": "False. Many poems rhyme, but some poems (called free verse) do not. Poetry is about using language in special, musical ways — rhyme is just one tool.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Read this poem aloud: 'The fog comes / on little cat feet. / It sits looking / over harbor and city / on silent haunches / and then moves on.' Does this poem rhyme? What makes it a poem even without rhyme?",
                "expected_type": "text",
                "hints": [
                    "Even without rhyme, poems use imagery (pictures in words) and rhythm. What picture does this poem create?"
                ],
                "explanation": "This poem (by Carl Sandburg) does not rhyme, but it creates a vivid image: fog behaving like a quiet cat. Poetry uses imagery, rhythm, and creative comparisons — not just rhyme.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "When reciting a poem, which is more important?",
                "expected_type": "multiple_choice",
                "options": [
                    "Speaking as fast as possible",
                    "Reading every word perfectly but in a flat voice",
                    "Using rhythm and expression to bring the poem to life",
                    "Speaking very quietly so you don't make mistakes",
                ],
                "correct_answer": "Using rhythm and expression to bring the poem to life",
                "hints": ["Think about what makes a poem performance enjoyable to listen to."],
                "explanation": "Expression and rhythm bring a poem to life. A flat reading loses the music of the poem. Speed and volume matter less than feeling and rhythm.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Choose a short poem (4-8 lines) that you know. Recite it from memory with expression. Then explain why you chose this poem.",
                "expected_type": "text",
                "hints": [
                    "Pick a poem you genuinely enjoy. Practice it a few times before performing. Think about why this poem matters to you."
                ],
                "explanation": "A good recitation includes: all words from memory, appropriate rhythm (following the poem's natural beat), expression (louder and softer, faster and slower to match the meaning), and a personal connection to why this poem was chosen.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Recite a memorized poem with expression.",
                "type": "open_response",
                "target_concept": "recitation",
                "rubric": "Mastery: complete poem from memory with rhythm and expression. Proficient: mostly from memory, some expression. Developing: needs significant prompting.",
            },
            {
                "prompt": "Clap the rhythm of this poem as I read it aloud.",
                "type": "open_response",
                "target_concept": "rhythm",
                "rubric": "Mastery: claps accurately on the beat. Proficient: claps with some rhythmic awareness. Developing: random clapping.",
            },
            {
                "prompt": "Which poem do you like best? Why?",
                "type": "open_response",
                "target_concept": "poetry_preference",
                "rubric": "Mastery: names poem and gives specific reasons. Proficient: names poem with vague reasons. Developing: cannot express preference.",
            },
        ],
        "resource_guidance": {
            "required": [
                "anthology of children's poetry or individual poem collections",
                "space for recitation performance",
            ],
            "recommended": ["poetry notebook for copying favorite poems", "audio recordings of poems read by poets"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 10},
        "accommodations": {
            "dyslexia": "Hear poems read aloud rather than reading independently. Memorize by ear: parent says a line, child repeats. Use poems with strong rhythm and repetition — these are easier to memorize. Visual text is secondary to auditory memorization.",
            "adhd": "Start with funny, action-filled poems that hold attention. Add movement to recitation: march, clap, gesture. Keep memorization sessions to 5-8 minutes. Poetry with a strong beat channels physical energy.",
            "gifted": "Introduce longer poems and poems with deeper meaning. Encourage the child to write their own poems. Discuss figurative language: simile, metaphor, personification. Compare different poets' styles.",
            "visual_learner": "Illustrate poems. Read from attractively printed poem cards. Write poems in calligraphy or colorful lettering.",
            "kinesthetic_learner": "Add gestures and movements to recitation. March or sway to the rhythm. Act out the poem's imagery.",
            "auditory_learner": "Listen to audio recordings of poets. Emphasize the musical quality of language. Sing-song recitation is fine — let the rhythm take over.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Poetry is language at its most musical, made to be heard. A poem is shorter than a story, but every word is chosen, and it works by rhythm, by rhyme, and by images that paint a picture in the mind. Today we memorize and recite a poem with rhythm, expression, and feeling, identify the rhyme and rhythm in poems, tell which poems we like and why, and notice how a poem's language differs from a story's.",
                "gradual_release": {
                    "i_do": "Read a short poem aloud, tapping the beat, then recite a line with expression, louder and softer, to match its feeling. Point out a pair of rhyming words and an image the poem paints. Model memorizing: say a line, then say it again from memory.",
                    "we_do": "Read a poem together and tap its rhythm, find the rhyming pairs, and memorize it line by line, the adult saying a line and the child echoing it, building up the whole.",
                    "you_do": "Child recites a memorized poem of four or more lines with rhythm and expression, identifies its rhyme and rhythm, and says which poems they like and why.",
                },
                "guided_practice": [
                    "Clap or tap the rhythm of a poem while reading it aloud",
                    "Find and name the rhyming pairs in a short poem",
                    "Memorize a four-line poem line by line by echoing the adult",
                ],
                "independent_practice": [
                    "Recite the memorized poem with expression for a family member",
                    "Choose a favorite poem and tell, with reasons, why it appeals",
                ],
                "mastery_check": [
                    "Recite a memorized poem of four or more lines with appropriate rhythm and expression",
                    "Identify the rhyme and rhythm patterns in a poem",
                    "Express a poetry preference and explain it with specific reasons",
                ],
                "spiral_review": [
                    "Revisit hearing rhyming words and syllable beats, the ear-training that poetry rests on",
                ],
            },
            "classical": {
                "narrative_introduction": "Before books were common, the great things were said in verse, for verse is easy to remember and beautiful to hear. To memorize a poem is to make it your own forever, a possession of the mind no one can take. The poet says much in few words, with rhythm and rhyme and images, and to recite a poem well is to give that beauty back aloud.",
                "memory_work": {
                    "chants": [
                        "Recite the day's poem aloud together, line upon line, until it is held by heart",
                        "Chant the marks of a poem: rhythm to walk by, rhyme to ring, and images to see",
                    ],
                    "recitations": [
                        "Recite the memorized poem with rhythm, expression, and feeling, adding it to a growing repertoire that is reviewed cumulatively",
                    ],
                },
                "copywork": [
                    "Copy a favorite poem, or a verse of it, neatly into a personal poetry notebook, the hand learning the lines as it writes",
                ],
                "recitation_routine": "Begin each lesson by reciting poems learned before, oldest first and then the newest, so the repertoire of poems is rehearsed cumulatively and never lost.",
                "history_integration": "Tell that for most of history poems and long verse were carried entirely in memory, recited by heart, and that to memorize a poem is to join that long tradition of keeping words alive by voice.",
                "read_aloud_suggestions": [
                    "A poem of real beauty, well within the child's liking, read aloud for its music before it is memorized",
                    "An anthology of fine children's poems, dipped into often and read aloud for delight",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A beautiful, well-chosen anthology of real poetry for children, never a watered-down or twaddly verse collection",
                ],
                "short_lesson_flow": "Read a poem aloud, beautifully and unhurried, perhaps more than once because it is loved. Do not pull it apart. Over days, the poem is heard again and again until it is known by heart almost without effort. Let the child recite it when it is ready. Keep it short and joyful.",
                "narration_prompt": "Tell me about the poem we have been hearing. What pictures does it put in your mind, and how does it make you feel?",
                "real_world_objects": [
                    "A beautiful poetry anthology, returned to again and again",
                    "A personal poetry notebook where the child copies and keeps loved poems",
                    "A pot of tea and a small treat for a weekly poetry teatime",
                ],
                "nature_connection": "Choose poems about the season, the rain, the trees, or a bird, and read them outdoors or just after a nature walk, so the poem and the living thing it sings of are met together.",
                "habit_focus": "The habit of attention: hearing a poem so fully that it settles into memory of its own accord.",
            },
            "montessori": {
                "prepared_materials": [
                    "Poetry cards, each a single poem beautifully printed, that the child may choose and read independently",
                    "A personal poetry anthology the child copies favorite poems into",
                    "A quiet recitation corner where a poem may be performed for a listener",
                ],
                "presentation": {
                    "three_period_lesson": "With the poetry cards: this poem rhymes, hear star and are; show me a poem that rhymes; does this poem rhyme?",
                    "steps": [
                        "The child chooses a poetry card and reads or hears the poem, tapping its rhythm",
                        "The child memorizes the poem at their own pace, returning to the card as often as needed",
                        "The child recites the poem to a listener and copies a loved poem into the personal anthology",
                    ],
                },
                "control_of_error": "The printed poetry card is the control: the child checks their recitation against the card and sees at once any line dropped or word changed, correcting it themselves without an adult marking it wrong.",
                "abstraction_pathway": "From reading a poem off the card and tapping its beat, to holding the poem in memory, toward reciting it with rhythm and feeling and choosing freely the poems that speak to them.",
                "extensions": [
                    "Build a personal anthology of self-chosen poems over time",
                    "Sort poetry cards by those that rhyme and those that do not",
                    "Recite a poem to a younger child or a small group",
                ],
                "observation_focus": "Watch for the child returning to the card to check accuracy, choosing poems with genuine preference, and reciting with rhythm rather than a flat monotone.",
            },
            "unschooling": {
                "invitations": [
                    "Keep beautiful poetry anthologies and illustrated poem books within reach",
                    "Leave out a notebook and good pens for copying or writing poems",
                    "Have audio recordings of poems and poets available to listen to freely",
                ],
                "real_world_contexts": [
                    "Singing songs, whose lyrics are poetry set to music",
                    "Jump rope rhymes, clapping games, and playground chants",
                    "Reading the verse inside a greeting card",
                    "Making up silly rhymes and tongue twisters for fun",
                ],
                "conversation_starters": [
                    "Does this poem have a beat? Can you feel it when you say it?",
                    "Which words rhyme here? Can you hear them?",
                    "Which poem is your favorite? What do you love about it?",
                    "What pictures come into your mind when you hear this poem?",
                ],
                "resource_bank": [
                    "A home shelf of varied poetry, funny, beautiful, and strange",
                    "Recordings of poems and of songs",
                    "A notebook for copying or writing poems, kept available",
                ],
                "parent_role": "Read and recite poems aloud for the pure pleasure of them, share the poems you love, and follow the child's own taste, including the silly and the funny. Let poems be memorized because they are loved and worth keeping, never assigned, and recite them together when the mood is right.",
                "observation_documentation": "Over time, note whether the child recites poems they have taken to heart, feels the rhythm and hears the rhyme, has favorites they can speak about, and senses that a poem's language is its own kind. This noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Rhythm in poetry is pattern, just like patterns in mathematics. Counting syllables is counting.",
            "science": "Nature poetry connects to nature study: poems about trees, rain, animals, seasons",
            "history": "Poems mark historical moments: war poetry, patriotic verse, protest songs as poetry",
        },
    },
    "rf-18": {
        "enriched": True,
        "learning_objectives": [
            "Recite five or more traditional nursery rhymes from memory",
            "Clap, march, or move to the rhythm of a nursery rhyme",
            "Identify rhyming words within familiar nursery rhymes",
            "Understand that nursery rhymes are part of a shared cultural tradition passed down through generations",
        ],
        "teaching_guidance": {
            "introduction": "Nursery rhymes are a child's first literature. 'Jack and Jill,' 'Humpty Dumpty,' 'Hey Diddle Diddle' — these are more than cute songs. They build phonemic awareness (hearing sounds in words), develop rhythm and rhyme sensitivity (critical for reading), expand vocabulary, train memory, and connect the child to a cultural tradition stretching back centuries. Children who know nursery rhymes by age 4 tend to be stronger readers by age 8.",
            "scaffolding_sequence": [
                "Sing or chant nursery rhymes with the child during daily routines: while getting dressed, during bath time, while riding in the car",
                "Add finger plays and hand motions to rhymes: 'Itsy Bitsy Spider,' 'Pat-a-cake,' 'This Little Piggy'",
                "Clap the beat while saying a rhyme — make the rhythm physical and explicit",
                "Pause before the rhyming word and let the child fill it in: 'Jack and Jill went up the ___'",
                "Identify rhyming pairs explicitly: 'Jill and hill — those rhyme! They end with the same sound.'",
                "Recite familiar rhymes from memory without the parent's prompting",
                "Introduce less common nursery rhymes to expand the repertoire",
                "Create silly new versions of familiar rhymes by changing words — demonstrates understanding of structure and rhyme",
            ],
            "socratic_questions": [
                "Which two words rhyme in 'Jack and Jill went up the hill'?",
                "Can you clap the beat while you say 'Humpty Dumpty sat on a wall'? How many claps?",
                "What is your favorite nursery rhyme? What do you like about it?",
                "Can you change one word in 'Twinkle Twinkle Little Star' to make a silly new version?",
            ],
            "practice_activities": [
                "Nursery rhyme sing-along: dedicate 5 minutes each morning to singing or chanting rhymes together",
                "Rhyme illustration: draw a picture for a nursery rhyme and retell it from the picture",
                "Nursery rhyme acting: act out Humpty Dumpty, Jack and Jill, or Little Miss Muffet with household props",
                "Fill-in-the-rhyme: parent says the rhyme but pauses before key rhyming words for the child to complete",
            ],
            "real_world_connections": [
                "Nursery rhymes are songs: many are set to familiar tunes the child already knows",
                "Grandparents and older relatives know these same rhymes — shared cultural connection across generations",
                "Playground chants and jump rope rhymes are the modern descendants of nursery rhymes",
                "Lullabies are a form of nursery rhyme: 'Rock-a-bye Baby,' 'Twinkle Twinkle Little Star'",
            ],
            "common_misconceptions": [
                "Thinking nursery rhymes are only for babies — they are appropriate and valuable for children ages 2-6 and provide the foundation for phonemic awareness",
                "Believing a child 'knows' a rhyme because they can say it along WITH you — true memorization means reciting independently",
                "Not realizing that nursery rhymes build reading readiness: research shows strong correlation between nursery rhyme knowledge and later reading success",
                "Rushing through nursery rhymes without emphasizing the rhythm and rhyme — the musical quality IS the point; say them slowly enough to hear the patterns",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Recites five or more nursery rhymes independently from memory",
                "Claps or moves to the rhythm of a rhyme accurately",
                "Identifies at least two rhyming pairs in familiar nursery rhymes",
            ],
            "proficiency_indicators": [
                "Recites 3-4 rhymes independently, needs prompting for others",
                "Claps along with a rhyme but may lose the beat occasionally",
            ],
            "developing_indicators": [
                "Knows parts of several rhymes but cannot recite any completely on their own",
                "Enjoys hearing rhymes but does not yet identify rhyming words",
            ],
            "assessment_methods": ["independent recitation", "rhyme identification", "rhythm clapping"],
            "sample_assessment_prompts": [
                "Can you say 'Humpty Dumpty' all by yourself?",
                "Which words rhyme in 'Jack and Jill went up the hill'?",
                "Clap along with me as I say this rhyme. Can you keep the beat?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Finish this nursery rhyme: 'Jack and Jill went up the ___'",
                "expected_type": "text",
                "correct_answer": "hill",
                "hints": ["It rhymes with 'Jill.' Think of a word that sounds like Jill."],
                "explanation": "'Jack and Jill went up the hill.' Hill rhymes with Jill — they both end with the /ill/ sound.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which two words rhyme in this line: 'Humpty Dumpty sat on a wall'?",
                "expected_type": "multiple_choice",
                "options": [
                    "Humpty and Dumpty",
                    "sat and wall",
                    "Dumpty and wall",
                    "None of these — the rhyme is in the next line",
                ],
                "correct_answer": "None of these — the rhyme is in the next line",
                "hints": ["The rhyming word for 'wall' comes in the next line: 'Humpty Dumpty had a great ___'"],
                "explanation": "'Wall' rhymes with 'fall' in the next line: 'Humpty Dumpty had a great fall.' Rhymes often pair the last words of two different lines.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Say the nursery rhyme 'Twinkle, Twinkle, Little Star' all the way through. How many rhyming pairs can you find?",
                "expected_type": "number",
                "correct_answer": "3",
                "hints": ["Listen to the last word of every two lines. Do they rhyme?"],
                "explanation": "Three rhyming pairs in the first verse: star/are, high/sky, world/... (The traditional version has star/are, high/sky, and depending on the version, additional pairs).",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Clap the rhythm of 'Mary had a little lamb.' How many claps for the first line?",
                "expected_type": "number",
                "correct_answer": "7",
                "hints": ["Clap once for each syllable: Ma-ry had a lit-tle lamb"],
                "explanation": "Seven syllables (claps): Ma-ry-had-a-lit-tle-lamb. Each syllable gets one clap. This rhythm awareness builds phonemic awareness.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Make up a silly new version of 'Twinkle Twinkle Little Star' by changing some words but keeping the rhyme pattern. Share your version.",
                "expected_type": "text",
                "hints": ["Keep the rhythm the same but change some words. Make sure the end-words still rhyme!"],
                "explanation": "Example: 'Twinkle, twinkle, little car, / Racing fast, you'll go so far.' The rhythm stays the same and the new end-words (car/far) still rhyme. This shows understanding of both rhythm and rhyme.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Recite three different nursery rhymes from memory.",
                "type": "open_response",
                "target_concept": "nursery_rhyme_recitation",
                "rubric": "Mastery: recites 3+ rhymes independently. Proficient: recites 2 independently, needs prompting for others. Developing: knows parts but cannot complete any.",
            },
            {
                "prompt": "Find the rhyming words in 'Hey Diddle Diddle.'",
                "type": "open_response",
                "target_concept": "rhyme_identification",
                "rubric": "Mastery: identifies diddle/fiddle and moon/spoon. Proficient: identifies one pair. Developing: cannot identify rhyming words.",
            },
            {
                "prompt": "Clap along with 'Baa, Baa, Black Sheep' and keep the beat.",
                "type": "open_response",
                "target_concept": "rhythm",
                "rubric": "Mastery: claps on the beat consistently. Proficient: mostly on the beat. Developing: random clapping.",
            },
        ],
        "resource_guidance": {
            "required": [
                "collection of nursery rhymes (book or printed)",
                "no special materials — just voice and hands",
            ],
            "recommended": [
                "nursery rhyme picture books with illustrations",
                "recordings of nursery rhymes set to music",
            ],
        },
        "time_estimates": {"first_exposure": 10, "practice_session": 5, "assessment": 10},
        "accommodations": {
            "dyslexia": "Nursery rhymes are purely oral — no reading required. Emphasize the rhyming pairs to build phonemic awareness. Repeat rhymes daily; the repetition builds the sound awareness that dyslexic children need most.",
            "adhd": "Add movement to every rhyme: jumping, clapping, marching, dancing. Keep sessions to 5 minutes (2-3 rhymes). Perform rhymes as a game or race. Nursery rhyme action songs channel energy productively.",
            "gifted": "Discuss the historical origins of nursery rhymes (many have surprising backstories). Write original rhymes using the same patterns. Memorize longer traditional poems alongside nursery rhymes.",
            "visual_learner": "Illustrated nursery rhyme books where pictures match the words. Draw pictures to go with favorite rhymes.",
            "kinesthetic_learner": "Finger plays (Itsy Bitsy Spider, Pat-a-cake) combine movement with language. Act out rhymes with the whole body.",
            "auditory_learner": "Sing nursery rhymes to melodies. Emphasize the musical quality. Listen to recorded versions and sing along.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Nursery rhymes are a child's first poems, learned by heart and said aloud. Jack and Jill, Humpty Dumpty, Hey Diddle Diddle: they carry a strong beat and clear rhymes, and saying them trains the ear for the sounds inside words, which is the ground of reading. Today we recite five or more nursery rhymes from memory, clap and move to their rhythm, find the rhyming words, and learn that these rhymes have been passed down for generations.",
                "gradual_release": {
                    "i_do": "Say a nursery rhyme aloud with a strong, clear beat, clapping along. Say it again and stop before the rhyming word, showing how Jill and hill ring together. Name the rhyme as one many families have known for a very long time.",
                    "we_do": "Say nursery rhymes together, clapping or marching the beat, and fill in the rhyming word when the adult pauses, naming the rhyming pairs.",
                    "you_do": "Child recites five or more nursery rhymes from memory, claps or moves to the rhythm, and points out the rhyming words.",
                },
                "guided_practice": [
                    "Recite familiar nursery rhymes, the adult pausing for the child to fill in the rhyming word",
                    "Clap, march, or tap the beat while saying a rhyme",
                    "Name the rhyming pairs in well-known rhymes",
                ],
                "independent_practice": [
                    "Recite several nursery rhymes all the way through, without prompting",
                    "Say a rhyme while keeping its beat with claps or steps",
                ],
                "mastery_check": [
                    "Recite five or more nursery rhymes from memory, independently",
                    "Clap or move to the rhythm of a rhyme, keeping the beat",
                    "Identify rhyming pairs within familiar nursery rhymes",
                ],
                "spiral_review": [
                    "Revisit hearing and matching rhyming sounds, which the rhymes practice over and over",
                ],
            },
            "classical": {
                "narrative_introduction": "Nursery rhymes are the first memory work of childhood. Long before a child can read, these little verses, said and sung for hundreds of years, can be carried whole in the mind. They are handed from grandparent to parent to child, an unbroken line of voices, and learning them by heart is the child's first taking up of that inheritance.",
                "memory_work": {
                    "chants": [
                        "Recite a nursery rhyme together daily, clapping its beat, until it is held by heart",
                        "Build the repertoire one rhyme at a time: Jack and Jill, Humpty Dumpty, Hey Diddle Diddle, and more",
                    ],
                    "recitations": [
                        "Recite each learned nursery rhyme from memory, reviewing the whole collection cumulatively so none is forgotten",
                    ],
                },
                "recitation_routine": "Begin each lesson by reciting the nursery rhymes already learned before adding a new one, so the whole collection is rehearsed cumulatively.",
                "history_integration": "Tell that many nursery rhymes are hundreds of years old, that the child's grandparents and great-grandparents knew these very same rhymes, and that to learn them is to join hands with all who said them before.",
                "read_aloud_suggestions": [
                    "A treasury of traditional nursery rhymes, said and sung aloud daily until they are known by heart",
                    "A beautifully illustrated Mother Goose collection, read aloud for its pictures and its old, musical language",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 5,
                "living_book_suggestions": [
                    "A beautifully illustrated traditional nursery rhyme treasury, with real artwork worthy of a child's first book",
                ],
                "short_lesson_flow": "Weave nursery rhymes gently into the day rather than sitting down to teach them: sing one while dressing, chant one in the car, say one at bath time. Add hand motions and claps. Through this happy daily repetition the rhymes are learned by heart, with no drilling. A few minutes is plenty.",
                "narration_prompt": "Say your favorite nursery rhyme to me. What happens in it, and which words sound the same?",
                "real_world_objects": [
                    "A nursery rhyme treasury, looked at together for its pictures",
                    "The child's own hands, for finger plays like Itsy Bitsy Spider and Pat-a-cake",
                    "Everyday moments, dressing, the car, the bath, that carry the rhymes",
                ],
                "nature_connection": "Say the rhymes that sing of weather, animals, and nature, Rain Rain Go Away, Baa Baa Black Sheep, Little Bo Peep, out of doors, when the rain or the sheep or the season is really there to see.",
                "habit_focus": "The habit of joyful attention: delighting in the sound and rhythm of words said and sung together.",
            },
            "montessori": {
                "prepared_materials": [
                    "Nursery rhyme cards, each with a clear illustration, that the child may choose during circle or work time",
                    "A basket of small objects and finger puppets for acting out rhymes",
                    "Recordings of nursery rhymes the child may choose to play",
                ],
                "presentation": {
                    "three_period_lesson": "With the rhyme cards: this is Humpty Dumpty, see him on the wall; show me the card for Humpty Dumpty; which rhyme is this?",
                    "steps": [
                        "The child chooses a rhyme card and the adult says or sings the rhyme, clapping the beat",
                        "The child says the rhyme along, then independently, and claps or marches its rhythm",
                        "The child acts the rhyme with small objects or finger puppets and may choose a new rhyme to learn",
                    ],
                },
                "control_of_error": "The familiar rhyme is its own control: a rhyme has a fixed shape, and a missed or changed word breaks the beat and the rhyme, which the child hears at once and sets right by returning to the known verse.",
                "abstraction_pathway": "From hearing and joining in a rhyme, to reciting it independently with its beat, toward holding a whole collection of rhymes by heart and choosing freely which to say.",
                "extensions": [
                    "Choose and learn new, less common rhymes to widen the collection",
                    "Sort the rhyme cards by favorites or by topic, animals, weather, people",
                    "Recite a rhyme to a younger child",
                ],
                "observation_focus": "Watch for the child reciting rhymes independently, keeping the beat with claps or steps, and beginning to notice the words that rhyme.",
            },
            "unschooling": {
                "invitations": [
                    "Keep nursery rhyme books and Mother Goose treasuries within easy reach",
                    "Have recordings of nursery rhymes and rhyme songs available to play",
                    "Leave a little room in the day for finger plays and clapping games",
                ],
                "real_world_contexts": [
                    "Singing and chanting rhymes during everyday routines, dressing, the car, bath time, bedtime",
                    "Playing finger games like Itsy Bitsy Spider, Pat-a-cake, and This Little Piggy",
                    "Hearing the same rhymes from grandparents and older relatives",
                    "Clapping games and jump rope rhymes with other children",
                ],
                "conversation_starters": [
                    "Which words sound the same in Jack and Jill went up the hill?",
                    "Can you clap along while we say Humpty Dumpty?",
                    "What is your favorite rhyme? Shall we say it together?",
                    "Did you know Grandma knew this very same rhyme when she was little?",
                ],
                "resource_bank": [
                    "Nursery rhyme books and Mother Goose treasuries",
                    "Recordings of nursery rhymes set to music",
                    "Family elders, who carry the same rhymes",
                ],
                "parent_role": "Say and sing nursery rhymes freely throughout ordinary days, in the car, at bath time, at bedtime, simply because they are merry and loved. Add claps and finger plays, share the rhymes from your own childhood, and let the child join in and pick favorites at their own pace.",
                "observation_documentation": "Over time, note whether the child says nursery rhymes from memory, claps or moves to their beat, hears the rhyming words, and delights in rhymes shared across the family. This noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Counting rhymes: 'One, Two, Buckle My Shoe' is a counting rhyme that combines math and language",
            "science": "Rhymes about weather, animals, and nature: 'Rain, rain, go away,' 'Baa Baa Black Sheep,' 'Little Bo Peep'",
            "history": "Many nursery rhymes are hundreds of years old — they connect children to a living oral tradition",
        },
    },
    "rf-19": {
        "enriched": True,
        "learning_objectives": [
            "Use context clues (surrounding words and sentences) to determine the meaning of an unfamiliar word",
            "Use pictures and illustrations to support understanding of unknown words in a text",
            "Sort words into categories and recognize word families that share meaning",
            "Use three or more new vocabulary words accurately in conversation within a week of learning them",
        ],
        "teaching_guidance": {
            "introduction": "Vocabulary is the fuel for comprehension. A child who knows more words understands more of what they read. Children learn most words indirectly — through conversation, being read to, and reading independently. But direct instruction in vocabulary strategies (using context clues, recognizing word parts, sorting words by category) gives children tools to unlock new words on their own. The goal is not to memorize definitions but to make words part of the child's active speaking and thinking vocabulary.",
            "scaffolding_sequence": [
                "Start with words the child encounters in daily life and read-alouds — 'That word is fascinating. Do you know what it means? Let's figure it out.'",
                "Model using context clues: read a sentence with an unknown word and think aloud about what it might mean based on the rest of the sentence",
                "Use pictures and illustrations in books as clues to word meaning: 'The picture shows a muddy pig. What do you think sloppy means here?'",
                "Introduce word categories: group words by topic (food words, feeling words, movement words) to build conceptual webs",
                "Practice using new words in sentences: after learning a word, the child creates their own sentence using it",
                "Introduce simple word parts: common prefixes (un-, re-) and suffixes (-ful, -less, -ness) that change word meaning",
                "Play vocabulary games: 'Use the word enormous in a sentence' or 'What's another word for happy?'",
                "Track new words in a personal word journal: write the word, a kid-friendly definition, and a picture or sentence",
            ],
            "socratic_questions": [
                "You don't know what 'enormous' means. Can the other words in the sentence help you figure it out?",
                "The sentence says 'The tiny kitten was timid.' If the kitten is tiny and hiding behind its mother, what do you think timid means?",
                "Can you think of a word that means the opposite of 'enormous'? Words that are opposites help us understand both words better.",
                "You learned the word 'curious' yesterday. Can you use it in a sentence about something from your own life?",
            ],
            "practice_activities": [
                "Word of the day: introduce one rich vocabulary word each morning. Use it throughout the day in conversation.",
                "Context clue detective: while reading together, stop at an unfamiliar word and figure out its meaning from the surrounding sentences",
                "Word category sort: write words on cards and sort them into groups (color words, size words, emotion words, animal words)",
                "Synonym and antonym matching: match words to their synonyms (big/enormous) and antonyms (big/tiny)",
            ],
            "real_world_connections": [
                "Cooking introduces vocabulary: simmer, whisk, fold, dice, mince, sauté",
                "Nature walks build vocabulary: canopy, habitat, burrow, migration, camouflage",
                "Building projects introduce vocabulary: measure, level, plumb, fasten, brace",
                "Daily life is full of rich vocabulary opportunities: frustrated, relieved, exhausted, delighted, furious",
            ],
            "common_misconceptions": [
                "Thinking vocabulary is learned by memorizing dictionary definitions — words are learned through meaningful context, not isolation",
                "Assuming a child will 'just pick up' all the words they need — while much vocabulary IS absorbed naturally, explicit instruction and discussion of interesting words accelerates growth significantly",
                "Over-correcting a child's word choice instead of expanding it — say 'Yes, and another word for that is...' rather than 'Don't say that, say this.'",
                "Limiting vocabulary to age-appropriate words — children can learn and use sophisticated words (exhausted, magnificent, furious) when they encounter them in meaningful contexts",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Uses context clues to correctly determine the meaning of an unfamiliar word in a passage",
                "Uses three or more recently learned words accurately in conversation or writing",
                "Sorts words into meaningful categories and explains the groupings",
            ],
            "proficiency_indicators": [
                "Uses context clues with some support from an adult",
                "Uses some new vocabulary words but may not always use them accurately",
            ],
            "developing_indicators": [
                "Attempts to use context clues but often guesses incorrectly",
                "Recognizes recently taught words but does not use them independently",
            ],
            "assessment_methods": [
                "context clue tasks",
                "vocabulary usage in conversation",
                "word sorting and categorization",
            ],
            "sample_assessment_prompts": [
                "Read this sentence: 'The dog was famished after missing two meals.' What do you think famished means?",
                "Use the word 'enormous' in a sentence about something real.",
                "Sort these words into two groups and tell me why you grouped them that way: happy, angry, joyful, furious, cheerful, upset",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Read this sentence: 'The cat was so tiny it could fit in my hand.' What does tiny mean?",
                "expected_type": "multiple_choice",
                "options": ["very big", "very small", "very fast", "very old"],
                "correct_answer": "very small",
                "hints": ["If the cat can fit in your hand, how big is it?"],
                "explanation": "Tiny means very small. The context clue 'could fit in my hand' tells us the cat is very small.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "The sentence says: 'The dog was famished after missing two meals.' What do you think famished means?",
                "expected_type": "text",
                "correct_answer": "very hungry",
                "hints": ["If the dog missed TWO meals, how would it be feeling?"],
                "explanation": "Famished means very hungry. The context clue 'after missing two meals' helps us figure out that famished is about hunger.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Which word does NOT belong in this group: happy, joyful, cheerful, furious?",
                "expected_type": "multiple_choice",
                "options": ["happy", "joyful", "cheerful", "furious"],
                "correct_answer": "furious",
                "hints": ["Three of these words are about the same feeling. One is about a VERY different feeling."],
                "explanation": "Furious does not belong. Happy, joyful, and cheerful are all words for being glad. Furious means very angry — the opposite group.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "The word 'unhappy' starts with 'un-'. If 'un-' means 'not,' what does 'unhappy' mean?",
                "expected_type": "text",
                "correct_answer": "not happy",
                "hints": ["Un- means not. So un + happy = ?"],
                "explanation": "Unhappy means 'not happy.' The prefix un- changes the meaning to the opposite. Other un- words: unkind (not kind), unsafe (not safe), unfair (not fair).",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Read this: 'The old house was dilapidated. The roof sagged, the paint peeled, and the windows were broken.' Use the clues in the sentences to explain what dilapidated means.",
                "expected_type": "text",
                "hints": [
                    "Look at the details after the word: sagging roof, peeling paint, broken windows. What kind of condition is the house in?"
                ],
                "explanation": "Dilapidated means falling apart or in very bad condition. The context clues (sagging roof, peeling paint, broken windows) all describe a house that is old and deteriorating. Using surrounding details to figure out a hard word is the heart of the context clue strategy.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Read this sentence with an unknown word. Use context clues to tell me what the word means.",
                "type": "open_response",
                "target_concept": "context_clues",
                "rubric": "Mastery: correctly determines meaning and explains which clues helped. Proficient: gets close to the meaning. Developing: guesses without using context.",
            },
            {
                "prompt": "Use the word 'magnificent' in a sentence.",
                "type": "open_response",
                "target_concept": "vocabulary_usage",
                "rubric": "Mastery: uses the word accurately in a meaningful sentence. Proficient: uses the word but meaning is slightly off. Developing: cannot use the word in a sentence.",
            },
            {
                "prompt": "Sort these words into groups: enormous, tiny, huge, small, gigantic, little. Explain your groups.",
                "type": "open_response",
                "target_concept": "word_categorization",
                "rubric": "Mastery: sorts into big/small groups and explains. Proficient: sorts correctly. Developing: mixes up the groups.",
            },
        ],
        "resource_guidance": {
            "required": [
                "books at and slightly above the child's reading level",
                "index cards or notebook for word journal",
            ],
            "recommended": ["thesaurus (child-friendly)", "word-of-the-day calendar or list"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 10},
        "accommodations": {
            "dyslexia": "Focus on oral vocabulary building through conversation and read-alouds. Use pictures to anchor new words. Provide the word orally and in context rather than asking the child to read it independently. Word journals can include drawings instead of written definitions.",
            "adhd": "Word-of-the-day as a quick morning routine (2 minutes). Vocabulary games with physical components: vocabulary charades, word sort races. Short, frequent exposures to new words rather than long vocabulary sessions.",
            "gifted": "Introduce Tier 2 and Tier 3 vocabulary (academic and domain-specific words). Explore etymology: where do words come from? Introduce Latin and Greek roots. Encourage the child to use new words in their writing.",
            "visual_learner": "Word walls with illustrations. Color-code word categories. Draw pictures for new vocabulary words.",
            "kinesthetic_learner": "Vocabulary charades: act out word meanings. Sort physical word cards. Build words with letter tiles.",
            "auditory_learner": "Discuss new words in conversation. Use new words in sentences aloud. Word games played verbally: 'Give me another word for...'",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Vocabulary is the fuel of reading: the more words a child knows, the more they understand. New words need not be looked up one by one. A reader can often unlock a hard word by the clues around it, by the picture on the page, or by the family of words it belongs to. Today we use context clues and illustrations to figure out unfamiliar words, sort words into categories of shared meaning, and put new words to use in our own speech.",
                "gradual_release": {
                    "i_do": "Read a sentence with a hard word and think aloud: the dog was famished after missing two meals, so famished must mean very hungry, the surrounding words told me. Use a picture as a clue. Sort a few words into a meaning group, then use a new word in a sentence of my own.",
                    "we_do": "Meet unfamiliar words together: figure out each from the sentence around it or the picture, sort word cards into categories, and make sentences using new words.",
                    "you_do": "Child uses context clues and illustrations to determine an unfamiliar word's meaning, sorts words into meaningful categories, and uses three or more newly learned words accurately within a week.",
                },
                "guided_practice": [
                    "Read sentences with unfamiliar words and use the surrounding words as clues",
                    "Use a book's pictures to help unlock the meaning of an unknown word",
                    "Sort word cards into categories of shared meaning",
                ],
                "independent_practice": [
                    "Keep a word journal: each new word with a kid-friendly meaning and a picture or sentence",
                    "Use newly learned words in conversation and writing across the week",
                ],
                "mastery_check": [
                    "Use context clues to determine the meaning of an unfamiliar word in a passage",
                    "Sort words into meaningful categories and explain the groupings",
                    "Use three or more recently learned words accurately within a week",
                ],
                "spiral_review": [
                    "Revisit reading for meaning, since context clues depend on understanding the sentence around the word",
                ],
            },
            "classical": {
                "narrative_introduction": "Words are the coin of thought: the richer a child's store of words, the more finely they can think and speak. Many words are kin, built from the same root, and to know one is to hold a key to its whole family. To weigh the words around an unknown one, and so divine its meaning, is an art the careful reader practices all their life.",
                "memory_work": {
                    "chants": [
                        "Chant the reader's question for a hard word: what do the words around it tell, and what does the picture show",
                        "Chant a small family of words built from one root, hearing the meaning they share",
                    ],
                    "recitations": [
                        "Recite the meanings of new words learned, with a sentence for each, reviewing earlier words cumulatively",
                    ],
                },
                "copywork": [
                    "Copy a fine sentence that holds a new word, so the word is kept in the hand with the context that explains it",
                ],
                "recitation_routine": "Begin each lesson by reciting words learned before and using each in a sentence, so the growing store of words is rehearsed cumulatively.",
                "history_integration": "Tell that very many English words descend from older tongues, Latin and Greek, and that a single root, carried down the centuries, can be found living inside a whole family of words used today.",
                "read_aloud_suggestions": [
                    "A book written in rich, well-chosen language, read aloud so the ear meets fine words in their natural setting",
                    "A story whose context makes a new word's meaning plain, read aloud and paused upon",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A living book written in rich, beautiful, undumbed-down language, the best soil for new words to be met in",
                ],
                "short_lesson_flow": "There is no separate vocabulary lesson. Read a living book aloud, and when a beautiful or unfamiliar word arrives, pause just long enough to relish it: wonder together what it means from the sentence and the picture, say it once with pleasure, and read on. The child's narration afterward will quietly show which words have been taken in.",
                "narration_prompt": "Tell me about what we read. Was there a word you loved the sound of, or one you puzzled out?",
                "real_world_objects": [
                    "The living book itself, the source of words met in their true context",
                    "A commonplace book where a child may copy a sentence holding a word worth keeping",
                    "The real things, in the kitchen, the garden, the workshop, that new words name",
                ],
                "nature_connection": "On a nature walk, give the real things their true names, canopy, burrow, habitat, camouflage, so the rich word and the living thing it names are met together and remembered as one.",
                "habit_focus": "The habit of attention: noticing words, delighting in them, and letting beautiful language be heard often enough to be absorbed.",
            },
            "montessori": {
                "prepared_materials": [
                    "Classified nomenclature cards, sets of word, picture, and definition cards grouped by topic",
                    "Word category sorting cards, words to be grouped by shared meaning",
                    "A personal word journal",
                    "Books rich in language for self-directed reading",
                ],
                "presentation": {
                    "three_period_lesson": "With the nomenclature cards: this word is enormous, see the great whale in the picture; show me the word enormous; what does this word mean?",
                    "steps": [
                        "The child works with a set of classified nomenclature cards, matching each word to its picture and its definition",
                        "The child sorts word cards into categories of shared meaning and names each group",
                        "The child meets new words in self-chosen reading, uses context and picture to unlock them, and records them in the word journal",
                    ],
                },
                "control_of_error": "The nomenclature cards are the control: the word, picture, and definition match only in one way, so a mismatched card shows the child the error, and the matched set itself confirms a meaning guessed from context.",
                "abstraction_pathway": "From matching a word to its picture and definition on the cards, to sorting words into families of shared meaning, toward unlocking a new word from context alone and carrying it into one's own speech.",
                "extensions": [
                    "Make classified card sets for new topics of interest",
                    "Explore word roots and how prefixes such as un- and re- change meaning",
                    "Use newly learned words in self-directed writing",
                ],
                "observation_focus": "Watch for the child using context and pictures to unlock words rather than waiting to be told, and beginning to use new words in their own speech.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a wide, varied library of books written in rich language within reach",
                    "Leave out a word journal or notebook for words the child wants to keep",
                    "Have a child-friendly thesaurus and picture dictionary available to browse",
                ],
                "real_world_contexts": [
                    "Cooking, which brings words like simmer, whisk, fold, dice, and saute",
                    "Nature walks, which bring words like canopy, habitat, burrow, and camouflage",
                    "Building and fixing projects, which bring words like measure, level, fasten, and brace",
                    "Naming feelings precisely in everyday life: frustrated, relieved, delighted, furious",
                ],
                "conversation_starters": [
                    "That is an interesting word. What do you think it means? What in the sentence gives you a clue?",
                    "Can you think of another word that means almost the same as happy?",
                    "These words seem to go together. What makes them a family?",
                    "You learned curious yesterday. Can you use it to tell me about something?",
                ],
                "resource_bank": [
                    "A rich and varied home library and frequent library visits",
                    "A child-friendly thesaurus and picture dictionary",
                    "Everyday life, full of real work with its own rich words",
                ],
                "parent_role": "Use rich, precise words in everyday talk rather than simplifying, and expand rather than correct the child's word choices: yes, and another word for that is. Wonder aloud about interesting words as they come up, and let real conversation, real books, and real work be the place new words are met.",
                "observation_documentation": "Over time, note whether the child unlocks unfamiliar words from context and pictures, groups words by shared meaning, and takes new words into their own speech. This noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Math vocabulary: sum, difference, product, quotient, equal, greater, less — specific words with precise meanings",
            "science": "Science is full of vocabulary: observe, predict, hypothesis, experiment, data, conclusion",
            "history": "Historical vocabulary: revolution, independence, democracy, monarchy, treaty — words that unlock historical understanding",
        },
    },
    "rf-20": {
        "enriched": True,
        "learning_objectives": [
            "Demonstrate left-to-right, top-to-bottom reading directionality",
            "Identify the front cover, back cover, title, and author of a book",
            "Point to individual words as they are read, showing understanding of word boundaries",
            "Understand that print carries meaning and that spoken words can be written down and read back",
        ],
        "teaching_guidance": {
            "introduction": "Before children can read, they need to understand HOW print works. Print concepts are the rules of written language: we read left to right, top to bottom, front to back. Words are separated by spaces. The title tells what the book is about. The author is who wrote it. These concepts seem obvious to adults, but children must learn them through explicit modeling. Every time you read together, you are teaching print concepts.",
            "scaffolding_sequence": [
                "During read-alouds, run your finger under the words as you read — the child sees that print moves left to right",
                "Point out the front cover, back cover, and spine of a book. Ask the child to show you each part.",
                "Show the title and author on a cover: 'This is the title — it tells us the name of the book. This is the author — the person who wrote it.'",
                "Point to individual words: 'See this word? It says the. Now I'll point to the next word.' Show that spaces separate words.",
                "Read a sentence and have the child count how many words they see (count the separate groups of letters)",
                "Have the child 'read' a familiar book by turning pages front-to-back and pointing to words left-to-right",
                "Write a sentence the child dictates and read it back — showing that spoken words become print",
                "The child identifies title and author on unfamiliar books independently",
            ],
            "socratic_questions": [
                "Where do I start reading on this page — at the top or the bottom? On the left or the right?",
                "Can you point to the title of this book? What does the title tell us?",
                "How do you know where one word ends and the next word begins?",
                "If I write down what you just said, could someone else read it? Why?",
            ],
            "practice_activities": [
                "Book exploration: give the child a new book and ask them to show you the front cover, title, and author before reading",
                "Word counting: read a short sentence aloud and have the child count the words by touching each one",
                "Dictation writing: the child says a sentence, the parent writes it, and the child reads it back while pointing to each word",
                "Library sorting: during library visits, the child finds the title and author on book covers to decide which books to check out",
            ],
            "real_world_connections": [
                "Print is everywhere: cereal boxes, street signs, labels, instructions — all follow the same left-to-right convention",
                "Writing the child's name: their name is print, and it carries meaning (it identifies them)",
                "Grocery lists are print: the parent writes words, and those words mean something when you get to the store",
                "Recipes: print tells you what to do step by step, and the order matters (top to bottom)",
            ],
            "common_misconceptions": [
                "Thinking pictures are what you 'read' — pictures support reading, but reading means decoding the printed words",
                "Pointing to random parts of the page instead of tracking left to right — this is normal early on and resolves with modeling",
                "Not understanding that spaces separate words — young children often write words crammed together (ILIKECATS) until they learn about word spacing",
                "Confusing the author with the illustrator — both are credited on the cover but have different roles",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Demonstrates left-to-right, top-to-bottom directionality consistently",
                "Identifies title and author on any book cover",
                "Points to individual words accurately while someone reads aloud",
            ],
            "proficiency_indicators": [
                "Demonstrates directionality most of the time with occasional right-to-left drift",
                "Identifies the title but may confuse author with illustrator",
            ],
            "developing_indicators": [
                "Needs reminding to start on the left side of the page",
                "Cannot yet distinguish title from other text on the cover",
            ],
            "assessment_methods": [
                "book handling observation",
                "word pointing during shared reading",
                "cover identification",
            ],
            "sample_assessment_prompts": [
                "Show me where I should start reading on this page.",
                "Point to the title of this book. Who wrote it?",
                "Point to each word as I read this sentence.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "When you read a page, where do you start?",
                "expected_type": "multiple_choice",
                "options": ["Bottom right", "Top left", "Middle of the page", "Anywhere you want"],
                "correct_answer": "Top left",
                "hints": ["Think about which direction we read: left to right, top to bottom."],
                "explanation": "We start reading at the top left of a page and move to the right, then down to the next line. This is true for all English text.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What does the TITLE of a book tell you?",
                "expected_type": "text",
                "correct_answer": "The name of the book",
                "hints": ["The title is usually the biggest words on the front cover."],
                "explanation": "The title tells you the name of the book. It usually gives you a hint about what the book is about.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "How many words are in this sentence: 'The big dog ran fast.'?",
                "expected_type": "number",
                "correct_answer": "5",
                "hints": ["Count the groups of letters separated by spaces."],
                "explanation": "Five words: The, big, dog, ran, fast. Each group of letters separated by a space is one word.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is the difference between the author and the illustrator of a book?",
                "expected_type": "text",
                "hints": ["One person wrote the words. The other person drew the pictures."],
                "explanation": "The author wrote the words (the story or information). The illustrator drew the pictures. Sometimes one person does both.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Your little sibling opens a book and starts 'reading' from the back page. What would you tell them about how books work?",
                "expected_type": "text",
                "hints": ["Think about where you start reading a book and which direction you go."],
                "explanation": "You would explain that we start at the front cover, read left to right on each page, and turn pages forward (left to right) until we reach the back. Books have a beginning and an end, and the story only makes sense in order.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Show me the front cover, title, and author of this book.",
                "type": "open_response",
                "target_concept": "book_parts",
                "rubric": "Mastery: identifies all three correctly. Proficient: identifies two of three. Developing: cannot distinguish parts.",
            },
            {
                "prompt": "Point to each word as I read this sentence aloud.",
                "type": "open_response",
                "target_concept": "word_tracking",
                "rubric": "Mastery: points accurately to each word. Proficient: mostly accurate, may skip a word. Developing: points randomly.",
            },
            {
                "prompt": "Where do I start reading on this page?",
                "type": "open_response",
                "target_concept": "directionality",
                "rubric": "Mastery: points to top left immediately. Proficient: points to top left after brief hesitation. Developing: points elsewhere.",
            },
        ],
        "resource_guidance": {
            "required": ["picture books and other printed materials", "the child's own name written on paper"],
            "recommended": ["big books with large print for shared reading", "pointer stick for tracking text"],
        },
        "time_estimates": {"first_exposure": 10, "practice_session": 5, "assessment": 5},
        "accommodations": {
            "dyslexia": "Extra practice with directionality — use a green dot on the left margin (go) and a red dot on the right (stop). Large print books. Finger tracking is essential, not optional.",
            "adhd": "Interactive book exploration rather than sit-and-listen. Let the child hold the book and turn pages. Point to words with a fun pointer (toy wand, craft stick).",
            "gifted": "Move quickly through print concepts to actual reading. Introduce concepts of punctuation (period, question mark) and their meanings. Begin writing sentences with proper word spacing.",
            "visual_learner": "Big books with large, clear print. Color-code the title and author. Highlight word spaces.",
            "kinesthetic_learner": "Handle books physically: open, close, turn pages. Point to every word with a finger. Build sentences with word cards and physical spaces between them.",
            "auditory_learner": "Talk through the concepts: 'I start here. I read this way. This word says...' Verbal narration of the reading process.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Before a child can read, they must learn how print works. Print has rules: we read left to right and top to bottom, and we turn pages front to back. Spaces separate one word from the next. A book has a front cover, a back cover, a title that names it, and an author who wrote it. And print carries meaning: words spoken aloud can be written down and read back. Today we learn these rules of print.",
                "gradual_release": {
                    "i_do": "During a read-aloud, run a finger under the words, left to right and top to bottom, so the path of print is seen. Name the front cover, the back cover, the title, and the author. Point to single words and show the spaces between them. Say a sentence, write it down, and read it back.",
                    "we_do": "Explore a book together: find the front cover, the title, and the author. Point to each word of a sentence in turn, counting the words by the spaces. The child says a sentence and watches it be written and read back.",
                    "you_do": "Child shows left-to-right and top-to-bottom directionality, names the front cover, back cover, title, and author, points to single words, and tells that spoken words can be written and read back.",
                },
                "guided_practice": [
                    "Run a finger under the words during a shared read-aloud, left to right and top to bottom",
                    "Find and name the front cover, back cover, title, and author of a book",
                    "Point to each word of a short sentence and count the words by the spaces",
                ],
                "independent_practice": [
                    "Explore an unfamiliar book and identify its title and author",
                    "Dictate a sentence, watch it written, and point to each word while reading it back",
                ],
                "mastery_check": [
                    "Demonstrate left-to-right, top-to-bottom directionality on a page",
                    "Identify the front cover, back cover, title, and author of a book",
                    "Point accurately to individual words, showing word boundaries",
                ],
                "spiral_review": [
                    "Revisit handling a book the right way up and turning pages front to back",
                ],
            },
            "classical": {
                "narrative_introduction": "Print is speech made to last. The words a person says vanish on the air, but written down they stay, and may be read back by anyone, in any year. Yet print keeps rules: it runs left to right and top to bottom, it gathers letters into words and parts the words with spaces, and a book names itself by its title and names its maker, the author. To learn these rules is the doorway to reading.",
                "memory_work": {
                    "chants": [
                        "Chant the way of print: left to right, top to bottom, front of the book to the back",
                        "Chant the parts of a book: front cover, back cover, the title that names it, the author who wrote it",
                    ],
                    "recitations": [
                        "Recite that spaces part the words, that the title names the book and the author wrote it, and that spoken words written down can be read back",
                    ],
                },
                "recitation_routine": "Begin each lesson by reciting the way of print, left to right and top to bottom, and naming the parts of the book in hand.",
                "history_integration": "Tell that writing is one of the great inventions, that before it all words had to be remembered, and that not every language runs as English does, for some are written right to left, so the way of print is a thing each people has settled.",
                "read_aloud_suggestions": [
                    "A beautifully made book, read aloud with a finger tracking the print, so the child sees the way of print while hearing the story",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A beautiful picture book, well made and well loved, the kind worth handling and returning to often",
                ],
                "short_lesson_flow": "There is no separate lesson. At every read-aloud, simply hold the book so the child sees it, name its title and author once, and run your finger gently under the words as you read. Through this quiet, daily modeling, day after day, the rules of print are learned without a single worksheet.",
                "narration_prompt": "Show me the front of this book and tell me its name. Where on the page should we start to read?",
                "real_world_objects": [
                    "Real, beautiful picture books, held and explored",
                    "The child's own name, written out, their first piece of meaningful print",
                    "Print in the real world: signs, labels, a grocery list, a recipe",
                ],
                "nature_connection": "In the nature notebook, write beneath the child's drawing the words they tell you, so the child sees their own spoken words about a leaf or a bird become print that can be read back.",
                "habit_focus": "The habit of attention: watching the finger move under the words and seeing how print is followed.",
            },
            "montessori": {
                "prepared_materials": [
                    "The sandpaper letters, where a symbol is traced and given its sound",
                    "The movable alphabet, with which words are built from letters and parted by spaces",
                    "A shelf of well-made books for handling: finding the cover, the title, the author",
                    "Cards on which the child's own dictated words are written",
                ],
                "presentation": {
                    "three_period_lesson": "With a book in hand: this is the title, it names the book; show me the title; what is this part of the book called?",
                    "steps": [
                        "Handle a book: find the front cover, the back cover, the title, and the author",
                        "Follow the print during a reading, the finger moving left to right and top to bottom",
                        "Build a short message with the movable alphabet, leaving a space between each word, and read it back",
                    ],
                },
                "control_of_error": "The movable alphabet is the control: a word run together with no spaces cannot be read back cleanly, and the child, sounding it out, hears that the spaces are needed; the book itself shows that print followed out of order makes no sense.",
                "abstraction_pathway": "From tracing single sandpaper letters as symbols that carry sound, to building spaced words with the movable alphabet, toward following whole lines of print and knowing how a book is ordered.",
                "extensions": [
                    "Build longer messages with the movable alphabet, carefully spaced",
                    "Find the title and author on many books and sort them",
                    "Label real objects in the room with small written cards",
                ],
                "observation_focus": "Watch for the child following print left to right without drift, leaving spaces between words, and treating print as something that carries meaning.",
            },
            "unschooling": {
                "invitations": [
                    "Keep beautiful, varied books all around the house, within easy reach",
                    "Leave out paper and pens so a child may watch their words be written",
                    "Let the child see real print in use: lists, labels, notes, recipes",
                ],
                "real_world_contexts": [
                    "Being read to daily, watching a finger move under the words",
                    "Seeing their own name and reading it as print that means them",
                    "Watching a grocery list or a note be written, then used",
                    "Noticing print everywhere: signs, cereal boxes, labels, instructions",
                ],
                "conversation_starters": [
                    "Where should we start reading on this page? Which way do the words go?",
                    "Can you find the name of this book? Who do you think wrote it?",
                    "If I write down what you just said, could Grandma read it later?",
                ],
                "resource_bank": [
                    "A rich home library and frequent library visits",
                    "Paper and pens for writing down the child's words",
                    "The print of everyday life: signs, lists, labels, mail",
                ],
                "parent_role": "Read aloud daily and let the child see the book, run a finger under the words, and name the title and author as a natural part of it. Write down the child's own words when they ask, and point out print in the world, letting curiosity rather than drill lead the way.",
                "observation_documentation": "Over time, note whether the child follows print left to right and top to bottom, names the parts of a book, points to single words, and understands that print carries meaning. This noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Math also reads left to right: 2 + 3 = 5 is read in order. Number lines go left to right.",
            "science": "Science books have titles, authors, and diagrams with labels — all print concepts",
            "history": "Books as inventions: not all languages read left to right (Hebrew, Arabic, Chinese). Print conventions have a history.",
        },
    },
    "rf-21": {
        "enriched": True,
        "learning_objectives": [
            "Listen attentively to a story or informational text read aloud for 10-15 minutes",
            "Answer comprehension questions about a text heard (not read) aloud",
            "Ask relevant questions about what was heard, demonstrating engagement and curiosity",
            "Demonstrate focused listening by maintaining attention and minimizing distracting behaviors",
        ],
        "teaching_guidance": {
            "introduction": "Listening comprehension is the gateway to reading comprehension. Before children can understand text they read themselves, they must be able to understand text they HEAR. A child's listening comprehension level is typically two or more years above their independent reading level — meaning read-alouds expose them to richer language than they can decode alone. Building the habit of attentive listening is foundational: a child who cannot listen carefully to a story cannot narrate it, cannot discuss it, and will struggle when they must read independently.",
            "scaffolding_sequence": [
                "Start with very short read-alouds (3-5 minutes) of engaging picture books, building the habit of sitting and listening",
                "After reading, ask one simple question: 'What happened in the story?'",
                "Gradually increase read-aloud length to 10 minutes, then 15 minutes, building listening stamina",
                "Ask increasingly specific questions: who, what, where, when, why, how",
                "Encourage the child to ask THEIR OWN questions about the text — 'What do you wonder about?'",
                "Introduce listening with purpose: 'Listen for what the character wanted' or 'Listen for where the story takes place'",
                "Practice listening to informational text (not just stories): nature books, how-to descriptions, historical accounts",
                "Build toward one full chapter of a chapter book, discussing it afterward without re-reading",
            ],
            "socratic_questions": [
                "What was the most important thing that happened in what we just read?",
                "Was there anything that confused you or that you want to know more about?",
                "What do you think the character was feeling when that happened? What makes you think so?",
                "If I read that part again, what would you listen for this time?",
            ],
            "practice_activities": [
                "Daily read-aloud with discussion: make this a non-negotiable part of the daily routine, like meals",
                "Listening challenges: 'I'm going to read this page once. Listen for the name of the animal.' Give the child a focus for listening.",
                "Story retelling after listening: hear a story, then retell it to a family member who wasn't present",
                "Question generation: after hearing a passage, the child comes up with two questions about what was read",
            ],
            "real_world_connections": [
                "Following spoken directions: 'Go upstairs, get your shoes, and bring them down.' Listening comprehension in action.",
                "Listening to audiobooks during car rides — comprehension without print",
                "Listening to a family member tell a story about their day — real-world listening comprehension",
                "Following game rules explained verbally — you must listen carefully to play correctly",
            ],
            "common_misconceptions": [
                "Thinking a child who sits quietly is necessarily listening — some children appear attentive but are not processing; check with a question",
                "Believing fidgeting means not listening — many children (especially those with ADHD) listen BETTER when their hands are busy. Judge by comprehension, not by stillness.",
                "Expecting adult-level attention spans: a 5-year-old can typically sustain focused listening for 10-15 minutes, not 30",
                "Reading too much at once: one page or one short chapter is enough for a young listener. Quality of attention matters more than quantity of text.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Listens attentively for a full read-aloud session (10-15 minutes for age 5-6)",
                "Answers who, what, where, when, and why questions about the text",
                "Asks relevant questions about what was heard without prompting",
            ],
            "proficiency_indicators": [
                "Listens for most of the session with brief lapses in attention",
                "Answers basic questions (who, what) but struggles with why questions",
            ],
            "developing_indicators": [
                "Has difficulty sustaining attention for more than 5 minutes",
                "Cannot answer questions about what was just read aloud",
            ],
            "assessment_methods": [
                "comprehension questions after read-aloud",
                "observation of listening behavior",
                "question generation",
            ],
            "sample_assessment_prompts": [
                "What happened in the story we just read?",
                "Where did the story take place? How do you know?",
                "What is one question you have about what we just heard?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Your parent reads you a short story about a cat that got lost. What should you do while listening?",
                "expected_type": "multiple_choice",
                "options": [
                    "Play with a toy and listen at the same time",
                    "Focus on the story and make pictures in your mind",
                    "Think about what you want for lunch",
                    "Read a different book while listening",
                ],
                "correct_answer": "Focus on the story and make pictures in your mind",
                "hints": ["Good listeners create a movie in their head as they listen to a story."],
                "explanation": "Active listening means focusing on the story and making pictures in your mind. This helps you understand and remember what you hear.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "After hearing a story about a boy who found a treasure map, your parent asks 'Who found the map?' What should you do?",
                "expected_type": "text",
                "correct_answer": "Answer that the boy found the map.",
                "hints": ["Think back to what you heard. Who was the story about?"],
                "explanation": "You should answer the question using information you heard in the story. The boy found the treasure map. This shows you were listening.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You listened to a story but missed part of it because you were thinking about something else. What should you do?",
                "expected_type": "multiple_choice",
                "options": [
                    "Pretend you heard everything",
                    "Ask your parent to read that part again",
                    "Make up what you think happened",
                    "Say nothing and hope no one asks you about it",
                ],
                "correct_answer": "Ask your parent to read that part again",
                "hints": ["It's okay to miss something. Good listeners know when they've lost track and ask for help."],
                "explanation": "It's honest and smart to ask for a re-read when you've lost focus. Good listeners self-monitor — they know when they've stopped paying attention and take action to fix it.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: A child who is quietly drawing while listening to a story is not paying attention.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["Think about whether hands-busy activities help some people focus."],
                "explanation": "False. Many children listen BETTER when their hands are quietly busy (drawing, playing with clay). The test of listening is whether they can answer questions about the story, not whether they sat perfectly still.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "After hearing a story about animals in winter, come up with two questions you could ask about what you heard. Your questions should show you were thinking about the story.",
                "expected_type": "text",
                "hints": [
                    "Good questions start with why, how, what if. Think about something the story made you wonder about."
                ],
                "explanation": "Good questions might be: 'Why do some animals sleep all winter but others don't?' or 'How do birds know when to fly south?' These show active thinking about the text, not just passive hearing.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "After a read-aloud, answer: Who was in the story? What happened? Where did it take place?",
                "type": "open_response",
                "target_concept": "listening_comprehension",
                "rubric": "Mastery: answers all three accurately. Proficient: answers two of three. Developing: cannot recall key information.",
            },
            {
                "prompt": "Ask me a question about what we just read.",
                "type": "open_response",
                "target_concept": "question_generation",
                "rubric": "Mastery: asks a thoughtful question showing engagement. Proficient: asks a basic factual question. Developing: cannot generate a question.",
            },
            {
                "prompt": "Listen to this passage once, then tell me the most important thing it said.",
                "type": "open_response",
                "target_concept": "attentive_listening",
                "rubric": "Mastery: identifies the key point after one hearing. Proficient: gets the general idea. Developing: cannot recall content.",
            },
        ],
        "resource_guidance": {
            "required": ["quality read-aloud books appropriate to the child's listening level", "quiet reading space"],
            "recommended": ["audiobooks for independent listening practice", "listening comprehension question cards"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 15, "assessment": 5},
        "accommodations": {
            "dyslexia": "Listening comprehension is a strength area — use read-alouds to build vocabulary and story knowledge that will support reading. The child can comprehend text far above their decoding level when they hear it.",
            "adhd": "Allow quiet fidget activities during listening (drawing, clay, stress ball). Keep sessions short and build up. Pause frequently for brief check-ins. Give a listening focus: 'Listen for...'",
            "gifted": "Use above-level chapter books for listening. Encourage analytical questions. Introduce the concept of unreliable narrators, foreshadowing, and literary techniques.",
            "visual_learner": "Use picture books where illustrations support comprehension. Ask the child to visualize scenes. Drawing after listening reinforces comprehension.",
            "kinesthetic_learner": "Allow quiet movement during listening. Act out scenes after hearing them. Use props to represent characters.",
            "auditory_learner": "Natural strength. Audiobooks are excellent. Musical read-alouds with rhythm. The child may want to repeat phrases aloud.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Listening comprehension is the gateway to reading comprehension: a child must understand what they hear before they can understand what they read, and they can understand far harder language by ear than they can yet decode. Today we listen attentively to a text read aloud for ten to fifteen minutes, answer questions about what we heard, ask our own questions, and build the habit of focused listening.",
                "gradual_release": {
                    "i_do": "Model attentive listening: sit ready, make a picture in the mind of what is read, and when the reading stops, answer a who or what question from what was heard, and wonder aloud a real question about it.",
                    "we_do": "Listen to a read-aloud together, then answer who, what, where, when, and why questions about it, and think up a question of our own about what was heard.",
                    "you_do": "Child listens attentively to a read-aloud of ten to fifteen minutes, answers comprehension questions about what was heard, and asks a relevant question of their own.",
                },
                "guided_practice": [
                    "Listen to a short read-aloud with a purpose set beforehand, then answer questions about it",
                    "Answer who, what, where, when, and why questions about a text heard aloud",
                    "After a passage, think up one or two questions about what was heard",
                ],
                "independent_practice": [
                    "Listen to a longer read-aloud and afterward answer questions and ask one",
                    "Listen to informational text, not only stories, and tell what it said",
                ],
                "mastery_check": [
                    "Listen attentively for a full ten to fifteen minute read-aloud",
                    "Answer who, what, where, when, and why questions about a text heard aloud",
                    "Ask a relevant question about what was heard, without prompting",
                ],
                "spiral_review": [
                    "Revisit retelling a short passage, which depends on having listened with attention",
                ],
            },
            "classical": {
                "narrative_introduction": "Long before reading, there was listening. The great stories of every people were heard before they were ever read, and a child who listens well is heir to all of them. To listen is not idle: it is to attend, to hold what is said, to weigh it and wonder at it. The trained ear is the first instrument of the educated mind.",
                "memory_work": {
                    "chants": [
                        "Chant the listener's work: sit still, attend, picture it, and hold it in mind",
                        "Chant the questions to carry while listening: who, what, where, when, and why",
                    ],
                    "recitations": [
                        "Recite a short passage heard and held in mind, the proof that the ear has attended",
                    ],
                },
                "recitation_routine": "Begin each lesson by recalling and reciting from yesterday's read-aloud before today's is begun, so what is heard is held and reviewed.",
                "history_integration": "Tell that history itself began as listening, that the deeds of long ago were told aloud and heard, generation upon generation, before ever they were written, and that the attentive listener keeps that ancient tradition.",
                "read_aloud_suggestions": [
                    "A myth, fable, or hero tale, read aloud and listened to closely, of the kind first carried by the ear",
                    "A passage of fine informational prose, read aloud, so the ear learns to attend to true accounts as well as stories",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A living book worth full attention, in language richer than the child could yet read alone, never a dull or twaddly reader",
                ],
                "short_lesson_flow": "Read a portion of a living book aloud, once, with no interruption, in a quiet place. The child knows they will be asked to tell it back, and so they attend. After the single reading, the child narrates, and a real question or two may follow. Keep the reading to what attention can hold whole.",
                "narration_prompt": "Tell me what you heard. What was the most important thing, and what do you wonder about it?",
                "real_world_objects": [
                    "The living book, read from once so the ear must attend",
                    "A quiet, comfortable place kept for listening",
                    "A nature notebook or drawing paper for picturing what was heard",
                ],
                "nature_connection": "Listen out of doors: stand still on a nature walk and attend to what can be heard, the birds, the wind, the water, then tell it back, the same attentive listening turned upon the world.",
                "habit_focus": "The habit of attention: the single most important habit, trained by hearing a thing once and being expected to hold it.",
            },
            "montessori": {
                "prepared_materials": [
                    "A shelf of well-chosen books, story and informational, for shared listening",
                    "A prepared quiet corner where listening is undisturbed",
                    "Audio recordings of stories the child may choose to listen to",
                    "The silence game and other listening exercises that sharpen the ear",
                ],
                "presentation": {
                    "three_period_lesson": "With question cards: this question asks who, this one asks where; show me the question that asks where; what does this question ask?",
                    "steps": [
                        "The child settles in the prepared quiet corner and listens to a text read or played, once, with full attention",
                        "After the listening, the child answers questions about what was heard, who, what, where, when, why",
                        "The child asks a question of their own about the text and may choose the next listening",
                    ],
                },
                "control_of_error": "The text is the control: an answer is checked by returning to the book, and the child hears when their recollection does not match what was read; the silence game shows the child plainly how much the attentive ear can catch.",
                "abstraction_pathway": "From listening to a short, vivid story with full attention, to holding a longer text and answering questions about it, toward sustained attentive listening to informational text and chapter-length work.",
                "extensions": [
                    "Listen to informational texts and accounts, not only stories",
                    "Listen to a chapter and narrate it to a younger child",
                    "Use the silence game and listening walks to sharpen the ear further",
                ],
                "observation_focus": "Watch for the child attending without needing stillness imposed, answering from what was truly heard, and asking questions that show real engagement.",
            },
            "unschooling": {
                "invitations": [
                    "Read aloud generously and keep audiobooks within easy reach",
                    "Have a cozy listening spot where stories are heard",
                    "Leave out quiet hand activities, drawing, clay, that help a child listen",
                ],
                "real_world_contexts": [
                    "Listening to audiobooks on car rides and at quiet times",
                    "Hearing a family member tell a story about their day",
                    "Following spoken directions and the verbally explained rules of a game",
                    "Being read to at bedtime simply because it is loved",
                ],
                "conversation_starters": [
                    "What was the most important part of what we just heard?",
                    "Was there anything that puzzled you, or that you want to know more about?",
                    "What do you think the character was feeling? What made you think so?",
                ],
                "resource_bank": [
                    "A wide home library and a steady habit of reading aloud",
                    "Audiobooks and recorded stories",
                    "Quiet fidget materials for hands while listening",
                ],
                "parent_role": "Read aloud and tell stories often, and trust that a child listens in their own way, some best while their hands are busy. Talk about what was heard as a real conversation, follow the questions the child raises, and judge listening by understanding rather than by stillness.",
                "observation_documentation": "Over time, note whether the child attends to read-alouds, follows and recalls what was heard, answers questions about it, and asks questions of their own. This noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Listening to math word problems requires the same focused attention as listening to stories",
            "science": "Listening to descriptions of science experiments or nature observations builds scientific vocabulary",
            "history": "History was originally an oral tradition — stories told and listened to before they were written down",
        },
    },
    "rf-22": {
        "enriched": True,
        "learning_objectives": [
            "Retell a familiar story with a clear beginning, middle, and end",
            "Include at least three key details in a retelling: characters, setting, and major events",
            "Name the main characters and describe the setting of a story",
            "Organize a retelling in sequential order without skipping major events",
        ],
        "teaching_guidance": {
            "introduction": "Story retelling is the bridge between listening comprehension and narration. Where listening checks whether the child heard and understood, retelling asks them to organize that understanding and communicate it. A child who can retell a story with beginning, middle, and end — including characters, setting, and key events — has truly comprehended the story. Retelling is simpler than narration because it often uses familiar stories the child has heard multiple times.",
            "scaffolding_sequence": [
                "Start with stories the child knows well (favorite picture books read many times) — retell using the pictures as prompts",
                "Model retelling: parent retells a familiar story and the child listens to the structure",
                "Retell together: parent starts, child continues. Take turns with events.",
                "Introduce the BME framework: 'Tell me what happened at the Beginning. Now the Middle. Now the End.'",
                "Practice retelling with three key details: 'Who was in the story? Where did it happen? What was the big problem?'",
                "Retell a less familiar story after just one or two readings",
                "Retell without picture prompts — from memory alone",
                "Retell to someone who hasn't heard the story — the child becomes the storyteller",
            ],
            "socratic_questions": [
                "Who was in this story and where did it take place?",
                "What happened at the very beginning before everything else?",
                "What was the big problem in the middle of the story? How was it solved?",
                "If you were telling this story to Grandma, what would you make sure to include?",
            ],
            "practice_activities": [
                "Story retelling with props: use stuffed animals or toys to represent characters and act out the story while retelling",
                "Three-box retelling: draw three boxes labeled Beginning, Middle, End. The child draws one scene in each box, then retells using the drawings.",
                "Story stones: paint or draw story elements on stones (a character, a setting, an object). The child picks stones and retells the story incorporating them.",
                "Retelling to an audience: the child retells a favorite story to a sibling, grandparent, or friend — giving purpose to the retelling",
            ],
            "real_world_connections": [
                "Retelling what happened at a birthday party or playdate to a parent who wasn't there",
                "Retelling the plot of a movie or show the family watched together",
                "Telling Dad about the book Mom read at bedtime: natural retelling practice",
                "Retelling the sequence of a family outing: 'First we drove to the beach, then we built sandcastles...'",
            ],
            "common_misconceptions": [
                "Retelling only the ending (the most memorable part) and skipping the beginning and middle",
                "Including every tiny detail instead of focusing on key events — retelling is not word-for-word recall",
                "Retelling events out of order because the child mentions them as they come to mind rather than in story sequence",
                "Confusing retelling (what happened in THIS story) with making up a new story",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Retells a story with a clear beginning, middle, and end",
                "Includes characters, setting, and at least three key events",
                "Maintains chronological order throughout the retelling",
            ],
            "proficiency_indicators": [
                "Retells with beginning and end but may rush through or skip the middle",
                "Includes some key details but may omit characters or setting",
            ],
            "developing_indicators": [
                "Retells only one or two events, often the ending",
                "Needs significant prompting to include story elements",
            ],
            "assessment_methods": [
                "oral retelling after reading",
                "retelling with picture prompts",
                "retelling to a new listener",
            ],
            "sample_assessment_prompts": [
                "Tell me the story of 'The Three Bears' from beginning to end.",
                "Who was in the story? Where did it happen? What was the problem?",
                "Tell your sister what happened in the book we read today.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "When retelling a story, what three parts should you always include?",
                "expected_type": "multiple_choice",
                "options": [
                    "Title, author, illustrator",
                    "Beginning, middle, end",
                    "Characters, colors, sounds",
                    "First page, middle page, last page",
                ],
                "correct_answer": "Beginning, middle, end",
                "hints": ["Think about the structure of a story. Every story has three main parts."],
                "explanation": "Every retelling should include the beginning (how the story starts), the middle (what happens, including the problem), and the end (how it is resolved).",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Retell the story of 'The Three Little Pigs' in three sentences: one for the beginning, one for the middle, and one for the end.",
                "expected_type": "text",
                "hints": [
                    "Beginning: What did the pigs build? Middle: What did the wolf do? End: What happened at the third house?"
                ],
                "explanation": "Example: Beginning — Three pigs each built a house: one of straw, one of sticks, one of bricks. Middle — A wolf blew down the straw house and the stick house. End — The wolf could not blow down the brick house, and the pigs were safe.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You are retelling a story about a girl who found a puppy. You said: 'She named the puppy Max. The end.' What is missing from your retelling?",
                "expected_type": "text",
                "hints": [
                    "Think about what happened BEFORE she named the puppy. Where did she find it? Why was it lost?"
                ],
                "explanation": "The retelling is missing the beginning (how the girl found the puppy) and the middle (what happened before she decided to keep it). A good retelling includes events in order from the start of the story, not just the ending.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: A good retelling includes every single detail from the story, word for word.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["Think about the difference between retelling and memorizing."],
                "explanation": "False. A good retelling includes the KEY events — the most important things that happened. You use your own words, not the exact words from the book. You don't need every detail, just the main events.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Think of a book you know well. Retell it to someone who has never heard it before. Include the characters, setting, and the beginning, middle, and end.",
                "expected_type": "text",
                "hints": [
                    "Start by naming the characters and where the story takes place. Then tell what happened in order: first, then, finally."
                ],
                "explanation": "A complete retelling includes: who (characters), where (setting), and what happened (beginning, middle, end). A good test: could someone who never read the book understand the story from your retelling?",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Retell a familiar story with beginning, middle, and end.",
                "type": "open_response",
                "target_concept": "story_retelling",
                "rubric": "Mastery: complete BME with characters, setting, and events in order. Proficient: includes most elements, may skip the middle. Developing: only mentions one or two events.",
            },
            {
                "prompt": "Name the characters and setting of a story you just heard.",
                "type": "open_response",
                "target_concept": "story_elements",
                "rubric": "Mastery: names all main characters and describes setting. Proficient: names characters but vague on setting. Developing: cannot recall characters.",
            },
            {
                "prompt": "What was the problem in the story and how was it solved?",
                "type": "open_response",
                "target_concept": "problem_solution",
                "rubric": "Mastery: identifies problem and solution clearly. Proficient: identifies problem but not solution. Developing: cannot identify the problem.",
            },
        ],
        "resource_guidance": {
            "required": ["familiar picture books for retelling practice", "blank paper for drawing retelling scenes"],
            "recommended": ["story retelling graphic organizer (BME boxes)", "puppets or props for acted retelling"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 10},
        "accommodations": {
            "dyslexia": "Use picture books with strong illustrations for retelling cues. Read the story aloud multiple times before asking for a retelling. Accept retelling through drawing, acting, or oral language — not written.",
            "adhd": "Use high-action stories the child connects with. Retelling with props and movement. Keep retelling expectations to 2-3 minutes. Three-box drawing helps organize thoughts before speaking.",
            "gifted": "Retell from different perspectives. Add details the story didn't include (inferring). Compare retellings of the same fairy tale from different cultures.",
            "visual_learner": "Three-box BME drawing before oral retelling. Use the pictures in the book as retelling prompts.",
            "kinesthetic_learner": "Act out the story with props while retelling. Story stones with characters and objects.",
            "auditory_learner": "Record the retelling and play it back. Retell to different audiences. Practice verbal storytelling as a performance.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Retelling a story is telling it back in your own words, in the order it happened. A good retelling has three parts, a beginning, a middle, and an end, and carries the key details: who was in the story, where it took place, and the major events. Today we retell familiar stories with a clear beginning, middle, and end, name the characters and the setting, and keep the events in order.",
                "gradual_release": {
                    "i_do": "Retell a well-known story, thinking aloud: at the beginning, then the middle with its problem, then the end. Name the characters and the setting. Show plainly that the events must come in the order they happened, not jumbled.",
                    "we_do": "Retell a familiar story together, the adult and child taking turns with the events, naming the beginning, middle, and end, the characters, and the setting, keeping all in order.",
                    "you_do": "Child retells a familiar story with a clear beginning, middle, and end, names the characters and setting, and includes the major events in sequence.",
                },
                "guided_practice": [
                    "Retell a well-known story using the pictures in the book as prompts",
                    "Tell the beginning, then the middle, then the end of a familiar story",
                    "Name the characters and describe the setting of a story",
                ],
                "independent_practice": [
                    "Retell a story from memory, without picture prompts, in correct order",
                    "Retell a story to someone who has not heard it",
                ],
                "mastery_check": [
                    "Retell a familiar story with a clear beginning, middle, and end",
                    "Include the characters, the setting, and at least three major events",
                    "Keep the events of the retelling in correct sequential order",
                ],
                "spiral_review": [
                    "Revisit listening attentively to a story, since a retelling can only hold what was first taken in",
                ],
            },
            "classical": {
                "narrative_introduction": "To retell a story is to make it your own. The tale heard is gathered up and given back in your own words, in its true order: how it began, what befell in the middle, how it ended. This is the first step toward composition itself, for one who can order a story aloud is learning to order thought, and will one day order it on the page.",
                "memory_work": {
                    "chants": [
                        "Chant the three parts of every story: a beginning, a middle, and an end",
                        "Chant what a retelling must carry: the characters, the setting, and the events in their order",
                    ],
                    "recitations": [
                        "Recite a short, well-loved tale and then retell it in your own words, the recited and the retold both being the keeping of a story",
                    ],
                },
                "recitation_routine": "Begin each lesson by retelling the story from the last lesson before a new one is read, so the stories are kept and reviewed cumulatively.",
                "history_integration": "Tell that for most of human history stories were kept alive only by retelling, passed from teller to teller down the generations, and that to retell a tale faithfully is to do the work that has carried stories through all of time.",
                "read_aloud_suggestions": [
                    "A fairy tale, fable, or myth with a clear beginning, middle, and end, read aloud and then retold",
                    "A well-loved story heard many times, its shape so familiar it is easy to tell back",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A living book or well-told tale with a clear, strong shape, worth hearing and telling again, never a contrived reader",
                ],
                "short_lesson_flow": "Read a story, or a portion of one, aloud and unhurried. Close the book. Let the child tell it back in their own words, beginning, middle, and end, while you listen without correcting or prompting. The retelling is itself the lesson and the assessment both. Keep it warm and unhurried.",
                "narration_prompt": "Tell me the story back, from the very beginning to the end. Who was in it, and where did it happen?",
                "real_world_objects": [
                    "The living book itself, the story heard and then told back",
                    "Simple props or stuffed animals the child may use to act the retelling",
                    "Drawing paper for picturing the beginning, middle, and end",
                ],
                "nature_connection": "After a nature walk or an outing, ask the child to retell it as a story, beginning, middle, and end, the same telling-back turned upon a real day's events.",
                "habit_focus": "The habit of attention and of telling back: hearing a story fully and giving it again, whole and in order.",
            },
            "montessori": {
                "prepared_materials": [
                    "Story sequence cards the child arranges in order, beginning, middle, and end",
                    "A story basket with small figures and props for acting a retelling",
                    "A shelf of familiar storybooks for retelling practice",
                    "Drawing paper or a three-part beginning-middle-end frame",
                ],
                "presentation": {
                    "three_period_lesson": "With the sequence cards: this card is the beginning, this the middle, this the end; show me the beginning; which part of the story is this card?",
                    "steps": [
                        "The child hears or reads a familiar story",
                        "The child arranges the story sequence cards in order, beginning, middle, and end, naming the characters and the setting",
                        "The child retells the story aloud, using the cards or the story basket props, keeping the events in order",
                    ],
                },
                "control_of_error": "The story sequence cards are the control: arranged out of order, the story does not run true, and the child, retelling it, hears that it will not make sense until the cards are set right; the book itself confirms the true order.",
                "abstraction_pathway": "From arranging sequence cards and retelling with props in hand, to retelling a familiar story from memory alone, toward retelling a less familiar story heard only once or twice.",
                "extensions": [
                    "Retell a story to a younger child",
                    "Make sequence cards for a new story",
                    "Retell a real outing or experience in beginning-middle-end order",
                ],
                "observation_focus": "Watch for the child holding the events in their true order, including the beginning and middle and not only the end, and naming the characters and setting unprompted.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a rich shelf of storybooks within reach and read aloud often",
                    "Leave out small figures, puppets, and props for acting stories out",
                    "Have drawing materials handy for picturing a story's parts",
                ],
                "real_world_contexts": [
                    "Telling a parent what happened in a book read at bedtime",
                    "Retelling the plot of a film or show the family watched",
                    "Recounting a birthday party, a playdate, or an outing in order",
                    "Telling a sibling or grandparent a favorite story",
                ],
                "conversation_starters": [
                    "How did that story start? And then what happened? How did it end?",
                    "Who was in the story, and where did it all take place?",
                    "Could you tell that story to your brother? He has never heard it.",
                ],
                "resource_bank": [
                    "A wide home library and audiobooks for stories worth retelling",
                    "Puppets, figures, and props for acting stories out",
                    "Willing listeners: family, friends, and favorite toys",
                ],
                "parent_role": "Be a glad, genuine listener whenever the child wants to tell back a story, a film, or a day, without quizzing or correcting. Tell stories yourself and retell shared days aloud, so retelling is simply part of how the family talks, and let the child's own delight in telling carry it.",
                "observation_documentation": "Over time, note whether the child retells stories with a beginning, middle, and end, names the characters and setting, includes the major events, and keeps them in order. This noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Retelling the steps of solving a math problem: 'First I added, then I subtracted...'",
            "science": "Retelling what happened in a science experiment: observation retelling",
            "history": "Retelling a historical event in chronological order with key people and places",
        },
    },
    "rf-23": {
        "enriched": True,
        "learning_objectives": [
            "Make reasonable predictions about a story before reading, using the title, cover, and illustrations as clues",
            "Make predictions during reading about what will happen next based on story events",
            "Verify or revise predictions as new information is revealed in the text",
            "Explain the reasoning behind predictions using evidence from the text and prior knowledge",
        ],
        "teaching_guidance": {
            "introduction": "Predicting is thinking ahead while reading. When a child looks at a book cover and says 'I think this is about a dog who goes on an adventure,' they are using clues (the picture, the title) plus what they already know to make an educated guess. Predictions keep readers engaged because they create a reason to keep reading: 'Was I right? What actually happens?' The skill deepens comprehension because it requires the child to actively process information rather than passively receive it.",
            "scaffolding_sequence": [
                "Start with predictions before reading: show the cover and title. 'What do you think this book is about? Why?'",
                "Make predictions from illustrations: flip through the pictures before reading and predict the story",
                "During reading, pause at a suspenseful moment: 'What do you think will happen next? Why do you think so?'",
                "After a prediction, continue reading and check: 'Were you right? What actually happened?'",
                "Practice revising predictions: 'Your prediction was different from what happened. That's okay! What new information changed things?'",
                "Introduce using text clues (not just pictures) for predictions: 'The story says the sky is getting dark. What might happen next?'",
                "Practice predicting in nonfiction: 'This chapter is titled Hibernation. What do you predict it will explain?'",
                "The child independently pauses during reading to make and check predictions without prompting",
            ],
            "socratic_questions": [
                "Look at the cover. What do you predict this book is about? What clues are you using?",
                "The character just found a mysterious letter. What do you think is in the letter? Why?",
                "Your prediction was different from what happened. What new information surprised you?",
                "What clues in the story helped you predict what would happen next?",
            ],
            "practice_activities": [
                "Prediction stops: while reading, use a bookmark to stop at key moments. The child writes or tells their prediction before continuing.",
                "Cover predictions: before reading any new book, study the cover and make three predictions. After reading, check which were correct.",
                "Prediction journal: for chapter books, the child writes one prediction at the end of each chapter about what will happen next",
                "Mystery bag prediction: put an object in a bag, give three clues, and have the child predict what it is — same skill, different context",
            ],
            "real_world_connections": [
                "Predicting the weather by looking at the sky: 'Those dark clouds mean it might rain'",
                "Predicting what will happen in a movie or show based on clues: 'I bet the hero will escape because...'",
                "Predicting the outcome of a cooking project: 'If we add too much water, the dough will be too sticky'",
                "Predicting what a family member will say or do based on knowing their personality",
            ],
            "common_misconceptions": [
                "Thinking predictions must be correct to be good — a wrong prediction that is well-reasoned is excellent; prediction is about THINKING, not about being right",
                "Making wild guesses without evidence instead of using clues from the text and prior knowledge",
                "Feeling embarrassed when a prediction is wrong — normalizing revision is important: 'Good readers change their predictions when they get new information'",
                "Only predicting before reading, not during — predictions should happen throughout the reading process",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Makes reasonable predictions using specific evidence from the text or illustrations",
                "Revises predictions when new information contradicts them, explaining what changed",
                "Explains the reasoning behind predictions with clear connections to clues",
            ],
            "proficiency_indicators": [
                "Makes reasonable predictions but may not cite specific evidence",
                "Checks predictions after reading but doesn't always revise during reading",
            ],
            "developing_indicators": [
                "Makes random guesses rather than evidence-based predictions",
                "Does not check or revise predictions after reading further",
            ],
            "assessment_methods": [
                "prediction before reading",
                "mid-story prediction",
                "prediction-check after reading",
            ],
            "sample_assessment_prompts": [
                "Look at this cover. What do you predict the book is about? What clues are you using?",
                "We just read that the character is packing a suitcase. What do you predict will happen next?",
                "Your prediction was that the cat would find its way home. Did that happen? What actually happened?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "A book has a picture of a dog wearing a cape on the cover. The title is 'Super Dog.' What do you predict the book is about?",
                "expected_type": "text",
                "hints": ["Look at the clues: the dog, the cape, and the word 'Super' in the title."],
                "explanation": "A reasonable prediction: the book is about a dog who acts like a superhero or does something amazing. The cape and the word 'Super' are the clues. Any prediction that uses these clues is a good prediction.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What makes a prediction GOOD?",
                "expected_type": "multiple_choice",
                "options": [
                    "It is always correct",
                    "It uses clues from the text or pictures and makes sense",
                    "It is very surprising and unusual",
                    "It is the same as everyone else's prediction",
                ],
                "correct_answer": "It uses clues from the text or pictures and makes sense",
                "hints": ["Good predictions are based on EVIDENCE (clues), not random guessing."],
                "explanation": "A good prediction uses evidence — clues from the title, pictures, or text — and makes logical sense. It does NOT have to be correct. Wrong predictions that are well-reasoned are still valuable.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You are reading a story. The text says: 'Dark clouds filled the sky. The wind started to blow. The children ran inside.' What do you predict will happen next?",
                "expected_type": "text",
                "hints": ["What usually happens after dark clouds, wind, and people going inside?"],
                "explanation": "A reasonable prediction: a storm (rain, thunder) is coming. The clues are dark clouds, wind, and people seeking shelter. You combined text clues with your prior knowledge of weather.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You predicted the main character would win the race. Instead, she tripped and came in last. What should you do with your prediction?",
                "expected_type": "multiple_choice",
                "options": [
                    "Ignore the story and stick with your prediction",
                    "Feel bad about being wrong",
                    "Revise your prediction based on the new information and keep reading",
                    "Stop reading because you were wrong",
                ],
                "correct_answer": "Revise your prediction based on the new information and keep reading",
                "hints": ["Good readers adjust their thinking when the story gives new information."],
                "explanation": "Good readers revise predictions when the story surprises them. This is a sign of active reading, not failure. Ask yourself: 'What might happen now that she lost the race?'",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Read this: 'Emma looked at the empty cookie jar. She noticed crumbs on her brother's shirt. His face turned red when she asked about it.' What can you predict happened? What clues tell you that?",
                "expected_type": "text",
                "hints": [
                    "Put the clues together: empty jar + crumbs on shirt + blushing face. What does this evidence suggest?"
                ],
                "explanation": "Prediction: Emma's brother ate the cookies. The clues: the empty jar (cookies are gone), crumbs on his shirt (he was eating), and his red face (he feels guilty). This prediction uses multiple text clues combined with prior knowledge about how people behave when caught.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Look at this book cover and tell me what you predict the story will be about. What clues are you using?",
                "type": "open_response",
                "target_concept": "prediction_before_reading",
                "rubric": "Mastery: specific prediction with 2+ cited clues. Proficient: reasonable prediction with one clue. Developing: random guess, no clues.",
            },
            {
                "prompt": "We just read that the character packed a suitcase. What do you predict will happen next?",
                "type": "open_response",
                "target_concept": "prediction_during_reading",
                "rubric": "Mastery: evidence-based prediction. Proficient: reasonable guess. Developing: no prediction or unrelated guess.",
            },
            {
                "prompt": "Were your predictions correct? What actually happened? Did you change your prediction during reading?",
                "type": "open_response",
                "target_concept": "prediction_revision",
                "rubric": "Mastery: reflects on prediction accuracy and explains revision. Proficient: notes whether prediction was right. Developing: doesn't check predictions.",
            },
        ],
        "resource_guidance": {
            "required": [
                "books with engaging covers and clear plot progressions",
                "sticky notes for marking prediction points",
            ],
            "recommended": [
                "prediction journal or reading log",
                "books with cliffhanger chapter endings (for chapter book predictions)",
            ],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 5},
        "accommodations": {
            "dyslexia": "Use picture clues heavily for predictions. Read the text aloud so the child can focus on thinking, not decoding. Predictions can be given orally — no writing required.",
            "adhd": "Prediction stops at exciting moments keep the child engaged and wanting to read more. Make predictions a game: 'Let's bet! What do you think happens next?' High engagement keeps attention focused.",
            "gifted": "Introduce the concept of red herrings and foreshadowing. Predict in mystery and detective stories where prediction is the core skill. Discuss how authors plant clues for readers.",
            "visual_learner": "Use cover illustrations and interior pictures as primary prediction sources. Draw predicted scenes before reading.",
            "kinesthetic_learner": "Thumbs up/down for prediction checks. Act out predicted scenes before reading the actual events.",
            "auditory_learner": "Discuss predictions verbally before, during, and after reading. Think-aloud predictions: 'I'm thinking that...'",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Predicting is thinking ahead while reading. A good prediction is not a wild guess; it uses clues, the title, the cover, the pictures, the events so far, joined with what the reader already knows, to make an educated guess about what is coming. Predictions are checked as reading goes on, and revised when the story brings new information. Today we predict before and during reading, verify or revise our predictions, and explain the reasoning behind them.",
                "gradual_release": {
                    "i_do": "Study a cover and think aloud: the picture and the title make me predict this book is about a dog's adventure, those are my clues. Pause at a tense moment and predict what comes next, naming the clues. Read on and check; when the story surprises me, revise the prediction aloud.",
                    "we_do": "Before and during a story, make predictions together, name the clues each rests on, read on to check them, and revise them when new information changes things.",
                    "you_do": "Child makes reasonable predictions before and during reading using clues, verifies or revises them as the text reveals more, and explains the reasoning behind each.",
                },
                "guided_practice": [
                    "Study a cover and title and predict what the book is about, naming the clues",
                    "Pause at a key moment and predict what happens next, using story clues",
                    "Read on, check a prediction, and revise it if new information contradicts it",
                ],
                "independent_practice": [
                    "Make and check predictions at marked stopping points while reading",
                    "Keep a prediction journal, predicting at the end of each chapter",
                ],
                "mastery_check": [
                    "Make reasonable predictions before and during reading using specific clues",
                    "Verify or revise predictions as new information is revealed",
                    "Explain the reasoning behind a prediction with evidence and prior knowledge",
                ],
                "spiral_review": [
                    "Revisit using picture and text clues, the same clue-reading that drawing conclusions depends on",
                ],
            },
            "classical": {
                "narrative_introduction": "To read well is to read with the mind running ahead. A prediction is a small hypothesis: from the clues given, the title, the picture, the turn of events, joined to what is already known, the reader supposes what is to come. Then reading on, the supposition is tried against the truth and either confirmed or, honestly, set right. A prediction proven wrong but well reasoned is no failure; it is the mind at work.",
                "memory_work": {
                    "chants": [
                        "Chant the predictor's way: gather the clues, suppose what comes, read on, and check",
                        "Chant the honest rule: a prediction well reasoned is good, whether it proves right or wrong",
                    ],
                    "recitations": [
                        "Recite that a prediction rests on clues and prior knowledge, and is revised, not defended, when the text reveals more",
                    ],
                },
                "copywork": [
                    "Copy a prediction beside the clues it rests upon, neatly, the supposition and its evidence joined",
                ],
                "recitation_routine": "Begin each lesson by recalling yesterday's reading and whether its predictions proved true, before predicting the next portion.",
                "history_integration": "Tell that to predict from evidence is the very method by which knowledge advances, that the careful supposing of what follows from what is known, then tried against the truth, is the work of every scholar and every scientist.",
                "read_aloud_suggestions": [
                    "A story with clear clues and turns, read aloud and paused upon so predictions may be made and tried",
                    "A tale of mystery, where prediction from clues is the heart of the reading",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A living book with a strong, clear story whose events invite the child to wonder what comes next, never a contrived reader",
                ],
                "short_lesson_flow": "Read a living book aloud, and at a natural, suspenseful pause, simply wonder together: what do you think will happen next, and why? Let the child suppose, then read on to see. Keep it a warm, genuine conversation, never a worksheet, and let the curiosity itself carry the reading forward.",
                "narration_prompt": "Tell me what you thought would happen, and what made you think it. Did the story go as you supposed?",
                "real_world_objects": [
                    "The living book itself, paused upon at its turning points",
                    "The sky and weather, read for clues of what the day will bring",
                    "A reading or nature notebook where a prediction may be set down before reading on",
                ],
                "nature_connection": "Outdoors, predict from nature's clues: those dark clouds, will it rain; that bud, will it open; these tracks, where do they lead; then watch to see, the same predicting turned upon the living world.",
                "habit_focus": "The habit of attention: reading and watching closely enough to catch the clues that tell what may come.",
            },
            "montessori": {
                "prepared_materials": [
                    "A shelf of storybooks with engaging covers and clear plots",
                    "Prediction cards on which the child writes or draws a prediction before reading on",
                    "Sticky markers for marking the stopping points where a prediction is made",
                    "A prediction journal for chapter-book work",
                ],
                "presentation": {
                    "three_period_lesson": "With prediction cards: this is a prediction before reading, from the cover, this is a prediction during reading, from the events; show me a prediction made during reading; which kind of prediction is this?",
                    "steps": [
                        "Before reading, the child studies the cover and title and records a prediction with its clues",
                        "At marked stopping points during reading, the child predicts what comes next from the story's events",
                        "The child reads on, checks each prediction against the text, and revises it, noting what new information changed",
                    ],
                },
                "control_of_error": "The text is the control: reading on reveals what truly happens, and the child sees plainly whether a prediction held or must be revised, so the story itself confirms or corrects without an adult's marking.",
                "abstraction_pathway": "From predicting aloud at a single marked stop, to predicting and checking throughout a story, toward pausing of one's own accord to predict, verify, and revise while reading.",
                "extensions": [
                    "Keep a prediction journal across a whole chapter book",
                    "Predict in mystery stories, where clues are deliberately planted",
                    "Track which clues led to predictions that proved true",
                ],
                "observation_focus": "Watch for the child predicting from real clues rather than guessing, and revising a prediction calmly when the text reveals more.",
            },
            "unschooling": {
                "invitations": [
                    "Keep books with engaging covers and strong stories within reach",
                    "Have mystery stories and audiobooks available",
                    "Leave room in reading time to stop, wonder, and guess",
                ],
                "real_world_contexts": [
                    "Guessing what happens next in a film or show from the clues so far",
                    "Predicting the weather from the look of the sky",
                    "Predicting how a cooking or building project will turn out",
                    "Guessing what a person will say or do from knowing them well",
                ],
                "conversation_starters": [
                    "Look at the cover, what do you think this book is about? What makes you think so?",
                    "What do you think happens next? Why?",
                    "That is not what you expected, what surprised you, and what do you think now?",
                ],
                "resource_bank": [
                    "A wide home library, including mysteries",
                    "Films and shows whose turns can be guessed at",
                    "The everyday world, full of clues to read",
                ],
                "parent_role": "Wonder aloud about what comes next, in books, in films, in the weather, in the day, and welcome every reasoned guess whether it proves right or wrong. Show by your own example that a surprised prediction is happily revised, and let curiosity rather than correctness lead.",
                "observation_documentation": "Over time, note whether the child predicts from real clues, before and during reading, checks predictions against what happens, and revises them gladly. This noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Estimation in math IS prediction: 'I predict the answer will be about 50' before calculating",
            "science": "Hypotheses ARE predictions: scientists predict what will happen in experiments and then test it",
            "history": "Predicting consequences: 'What do you think happened after the king raised taxes?' — historical cause and effect",
        },
    },
    "rf-24": {
        "enriched": True,
        "learning_objectives": [
            "Make text-to-self connections by relating story events or characters to personal experiences",
            "Explain HOW a story connects to personal experience, not just THAT it does",
            "Use personal connections to deepen understanding of characters, events, and themes",
            "Distinguish between meaningful connections that aid comprehension and surface-level connections that don't",
        ],
        "teaching_guidance": {
            "introduction": "When a child reads about a character who is nervous on the first day at a new place and thinks 'I felt that way when we visited the new co-op,' they are making a text-to-self connection. These connections are powerful because they anchor abstract story events to real, felt experience. A child who connects personally to a text understands it more deeply, remembers it longer, and cares about it more. The key is teaching children to make connections that DEEPEN comprehension, not just surface-level links.",
            "scaffolding_sequence": [
                "Model connections during read-alouds: 'This reminds me of the time I...' — show the child what a connection sounds like",
                "After reading a passage, ask 'Does this remind you of anything that has happened to you?'",
                "Help the child articulate the connection fully: not just 'This reminds me of my dog' but 'This character is sad about losing her dog, and I felt sad like that when our fish died.'",
                "Introduce the sentence frame: 'This reminds me of ___ because ___.' The 'because' is essential.",
                "Discuss how the connection helps you understand the story better: 'Because I've felt nervous too, I understand why the character didn't want to go.'",
                "Practice distinguishing helpful connections from tangential ones: 'The story mentions a dog. I have a dog.' (surface) vs 'The character is brave even though she's scared. I was brave like that when I jumped off the high dive.' (deep)",
                "Apply connections to nonfiction: 'This book about habitats reminds me of the bird nest we found in our yard.'",
                "The child makes connections independently during reading without prompting",
            ],
            "socratic_questions": [
                "Has anything like this ever happened to you? Tell me about it.",
                "You said this reminds you of your trip to the lake. How does remembering your trip help you understand what the character is feeling?",
                "The character is making a difficult choice. Have you ever had to make a hard choice? What did you decide?",
                "Which connection helped you understand the story better: that the character has a bike like yours, or that the character felt left out like you did at the park?",
            ],
            "practice_activities": [
                "Connection journal: after reading, write or draw 'This reminds me of...' with the 'because' explanation",
                "Connection conversation: during read-alouds, both parent and child share connections — modeling deepens the child's connections",
                "Text-to-self sticky notes: while reading independently, the child places a sticky note whenever something reminds them of their own life",
                "Connection sorting: after making several connections, sort them into 'this helped me understand the story' and 'this is just something similar'",
            ],
            "real_world_connections": [
                "A story about a family moving reminds the child of their own move or a friend's move",
                "A character dealing with a new sibling connects to the child's experience when their own sibling was born",
                "A nonfiction book about gardening connects to the family's own garden",
                "A story about feeling left out connects to a real experience of being new somewhere",
            ],
            "common_misconceptions": [
                "Thinking any connection is a good connection — 'The story mentions a cat and I have a cat' is surface-level. Connections should help you understand the story, not just name something similar.",
                "Making connections that derail from the story: the child gets lost talking about their own experience and forgets about the text",
                "Believing text-to-self connections are only for fiction — nonfiction texts connect to personal experience too (a science book about weather connects to the storm you experienced)",
                "Thinking connections must be about identical experiences — a child who has never moved can still connect to a character who moves by thinking about any time they felt scared about something new",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Makes text-to-self connections that clearly relate to story events, characters, or themes",
                "Explains how the connection deepens understanding of the text",
                "Distinguishes between helpful and surface-level connections",
            ],
            "proficiency_indicators": [
                "Makes relevant connections but may not explain how they deepen understanding",
                "Connections are sometimes surface-level ('I have a dog too') rather than meaningful",
            ],
            "developing_indicators": [
                "Cannot make connections without significant prompting",
                "Connections are unrelated to the text's meaning or themes",
            ],
            "assessment_methods": [
                "oral connection sharing",
                "connection journal review",
                "prompted connection during reading",
            ],
            "sample_assessment_prompts": [
                "Does anything in this story remind you of something in your own life? Tell me about it.",
                "The character felt nervous. Have you ever felt that way? When?",
                "How does your connection help you understand the character better?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "A story is about a girl who is nervous on her first day at a new activity. Have you ever felt nervous about something new? What happened?",
                "expected_type": "text",
                "hints": [
                    "Think about a time you tried something for the first time — a new sport, a new class, a visit to a new place."
                ],
                "explanation": "A good connection shares a specific personal experience that relates to the character's feelings. For example: 'I felt nervous when I went to my first swimming lesson. My stomach hurt.' This connection helps you understand HOW the character feels.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which is a BETTER text-to-self connection?",
                "expected_type": "multiple_choice",
                "options": [
                    "The story has a dog. I have a dog.",
                    "The character is sad because his dog ran away. I felt sad like that when our cat was lost for two days.",
                ],
                "correct_answer": "The character is sad because his dog ran away. I felt sad like that when our cat was lost for two days.",
                "hints": ["Which connection helps you UNDERSTAND the character's feelings better?"],
                "explanation": "The second connection is better because it connects the FEELINGS and EXPERIENCE, not just a surface detail. Understanding the character's sadness through your own experience deepens comprehension.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Read this: 'Jake didn't want to try the new food. He pushed his plate away. But Mom said he had to take one bite. He tried it and was surprised — it was good!' Does this remind you of anything from your own life?",
                "expected_type": "text",
                "hints": ["Think about a time you didn't want to try something new but ended up liking it."],
                "explanation": "A meaningful connection might be: 'This reminds me of when I didn't want to try broccoli but then I liked it.' The connection helps you understand Jake's surprise because you've experienced that same feeling of unexpected enjoyment.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: Text-to-self connections only work with fiction stories, not nonfiction.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": [
                    "Think about whether a book about animals or weather could remind you of your own experiences."
                ],
                "explanation": "False. You can connect to nonfiction too. A book about hibernation might remind you of how sleepy you feel in winter. A book about volcanoes might connect to a trip where you saw mountains.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "A character in a story must choose between helping a friend and doing something fun. You've never faced that exact situation. Can you still make a connection? How?",
                "expected_type": "text",
                "hints": [
                    "You don't need the EXACT same experience. Think about any time you had to choose between two things when both seemed important."
                ],
                "explanation": "Yes! You don't need identical experiences. Any time you've had to make a hard choice between two important things is a valid connection. 'I had to choose between going to the park and finishing my building project. It was hard to decide.' The FEELING of having to choose is what connects.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "This story is about a character who feels lonely. Does this remind you of anything in your own life? How does your experience help you understand the character?",
                "type": "open_response",
                "target_concept": "text_to_self",
                "rubric": "Mastery: specific personal connection that deepens character understanding. Proficient: relevant connection without explaining how it helps. Developing: no connection or unrelated one.",
            },
            {
                "prompt": "Tell me one connection you made while we read today. Was it a surface connection or a deep connection?",
                "type": "open_response",
                "target_concept": "connection_quality",
                "rubric": "Mastery: describes connection and evaluates its depth. Proficient: describes connection. Developing: cannot articulate a connection.",
            },
            {
                "prompt": "How did your personal connection help you understand this story better?",
                "type": "open_response",
                "target_concept": "connection_purpose",
                "rubric": "Mastery: clearly explains how connection enhanced comprehension. Proficient: vaguely connects experience to story. Developing: cannot explain.",
            },
        ],
        "resource_guidance": {
            "required": ["books with relatable characters and situations", "connection journal or notebook"],
            "recommended": [
                "sticky notes for marking connection points during reading",
                "books chosen to match the child's current life experiences",
            ],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 5},
        "accommodations": {
            "dyslexia": "Read aloud so the child focuses on connecting, not decoding. Connections can be shared orally or through drawing. Use books about experiences the child has had — familiarity aids comprehension.",
            "adhd": "Connections channel the child's tendency to think about personal experiences DURING reading into a productive strategy rather than a distraction. Quick verbal connections during read-alouds. Keep connection discussions brief and focused.",
            "gifted": "Introduce text-to-text connections (how does this book connect to ANOTHER book?) and text-to-world connections (how does this book connect to real-world issues?). Discuss empathy: connecting to characters whose experiences are very different from your own.",
            "visual_learner": "Draw connections: split a page in half — draw the story scene on one side and the personal memory on the other.",
            "kinesthetic_learner": "Connection gestures: tap your heart when you make a connection while reading. Act out both the story scene and the personal memory.",
            "auditory_learner": "Talk through connections out loud. Parent-child conversation about shared connections. 'That reminds me of...' becomes a natural part of reading talk.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "A text-to-self connection is the link a reader makes between a story and their own life. When a child reads about a character nervous on a first day and thinks of their own first day somewhere new, they are connecting. But the connection must be a deep one, not just naming something similar. A deep connection joins feelings and experiences and helps the reader understand the character better. Today we make text-to-self connections, explain how each connection deepens understanding, and tell deep connections from surface ones.",
                "gradual_release": {
                    "i_do": "Read a passage and think aloud: this character is sad about losing her dog; I felt that same sadness when our fish died, and because I have felt it, I understand her. Show plainly the difference between a deep connection of feeling and a surface one, the story has a dog and I have a dog.",
                    "we_do": "Read together and make connections, each one stated fully with the sentence frame, this reminds me of, because, and talk about how the connection helps us understand the character.",
                    "you_do": "Child makes text-to-self connections, explains how each connection deepens understanding of the character or event, and tells a meaningful connection from a surface one.",
                },
                "guided_practice": [
                    "Make a connection using the frame: this reminds me of, because",
                    "Explain how a connection helps you understand a character's feelings",
                    "Sort connections into deep ones that aid understanding and surface ones that do not",
                ],
                "independent_practice": [
                    "Keep a connection journal: this reminds me of, with the because explained",
                    "Mark connection points with sticky notes while reading independently",
                ],
                "mastery_check": [
                    "Make text-to-self connections that relate to story events, characters, or themes",
                    "Explain how a connection deepens understanding of the text",
                    "Distinguish a meaningful connection from a surface-level one",
                ],
                "spiral_review": [
                    "Revisit describing how a character feels, since a connection deepens understanding of those feelings",
                ],
            },
            "classical": {
                "narrative_introduction": "A story read is held against the reader's own life, and where the two touch, understanding deepens. The character's fear, the character's choice, the character's loss, met in a book, is truly known only by one who has felt something of the same. The worthy connection is a connection of the heart, of feeling and experience, not a mere noticing that the book names a thing the reader happens to own.",
                "memory_work": {
                    "chants": [
                        "Chant the frame of a true connection: this reminds me of, because",
                        "Chant the test of a connection: does it help me understand, or does it only name something the same",
                    ],
                    "recitations": [
                        "Recite that a deep connection joins feeling and experience and deepens understanding, while a surface connection only names a likeness",
                    ],
                },
                "copywork": [
                    "Copy a full connection, the reminding and its because, neatly, so the connection and its reason are joined",
                ],
                "recitation_routine": "Begin each lesson by recalling a connection made in an earlier reading and how it deepened the understanding of that book.",
                "history_integration": "Tell that the lasting power of the old stories is just this, that men and women in every age have found their own joys and griefs mirrored in them, and so a tale of long ago can still be felt as one's own.",
                "read_aloud_suggestions": [
                    "A story whose feelings, fear, longing, courage, the child has known something of, read aloud so a true connection may be felt",
                    "A story of an experience close to the child's own life, chosen so connection comes readily",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A living book chosen because its life and feelings touch the child's own, full of real and relatable experience",
                ],
                "short_lesson_flow": "Read a living book aloud, and model a connection of your own simply and warmly: this reminds me of the time I. Then, when the child's narration or talk reveals a connection, receive it with interest and gently ask, how does that help you understand the character. Keep it a real conversation, never a worksheet.",
                "narration_prompt": "Tell me about the story, and tell me if anything in it reminded you of your own life. How did remembering that help you understand the character?",
                "real_world_objects": [
                    "The living book itself, its life held against the child's own",
                    "A connection or commonplace notebook for a connection worth keeping",
                    "The child's own memories and experiences, the true material of connection",
                ],
                "nature_connection": "When a book speaks of a storm, a garden, a creature, let it call up the child's own memory of the real storm, the family garden, the creature once watched, joining the book to the living world the child knows.",
                "habit_focus": "The habit of attention and of sympathy: bringing one's own felt experience to a book so its people are truly understood.",
            },
            "montessori": {
                "prepared_materials": [
                    "A shelf of books with relatable characters and situations",
                    "Connection cards the child writes a connection and its because upon",
                    "A connection journal",
                    "Sorting cards for separating deep connections from surface ones",
                ],
                "presentation": {
                    "three_period_lesson": "With connection examples: this is a deep connection, it joins a feeling, this is a surface connection, it only names a likeness; show me a deep connection; which kind of connection is this?",
                    "steps": [
                        "After reading, the child makes a connection between the text and their own experience",
                        "The child states it fully on a connection card, this reminds me of, because, and tells how it helps them understand",
                        "The child sorts their connections into deep ones that aid understanding and surface ones that do not",
                    ],
                },
                "control_of_error": "The test of understanding is the control: a connection is sorted as deep only if the child can say how it helps them understand the text, and a connection that explains nothing reveals itself as surface, so the sorting checks itself.",
                "abstraction_pathway": "From naming any likeness between book and life, to stating a connection fully with its because, toward making, of one's own accord, deep connections that genuinely deepen understanding.",
                "extensions": [
                    "Keep a connection journal across many books",
                    "Move toward text-to-text and text-to-world connections",
                    "Connect to characters whose lives differ from the child's own",
                ],
                "observation_focus": "Watch for the child making connections of feeling rather than surface likeness, and able to say how a connection deepens understanding.",
            },
            "unschooling": {
                "invitations": [
                    "Keep books with relatable, true-to-life characters within reach",
                    "Choose books that touch the child's own current experiences",
                    "Leave out drawing and writing materials for capturing a connection",
                ],
                "real_world_contexts": [
                    "A book about moving recalling the family's own move, or a friend's",
                    "A story of a new sibling recalling when the child's own sibling was born",
                    "A book about a garden, a pet, or a storm recalling the child's real one",
                    "A story of feeling left out recalling a real time of being new somewhere",
                ],
                "conversation_starters": [
                    "Has anything like this ever happened to you? Tell me about it.",
                    "How does remembering your own time help you understand how the character feels?",
                    "That character had to make a hard choice. Have you ever had to choose like that?",
                ],
                "resource_bank": [
                    "A home library chosen to match the child's life and interests",
                    "Drawing and writing materials for capturing connections",
                    "The family's own shared memories and stories",
                ],
                "parent_role": "Share your own connections to books warmly and often, this reminds me of, and welcome the child's connections with real interest rather than judgment. Choose books that touch the child's life, and let connecting be a natural part of talking about what you read together.",
                "observation_documentation": "Over time, note whether the child connects books to their own life, explains how a connection helps them understand, and senses the difference between a deep connection and a surface one. This noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Connecting math problems to real life: 'This addition problem is like when we combined two piles of blocks'",
            "science": "Connecting science readings to personal observations: 'This book about clouds reminds me of the storm we watched'",
            "history": "Connecting historical events to personal or family experiences: 'People had to leave their homes, like Grandma did when she was young'",
        },
    },
    "rf-25": {
        "enriched": True,
        "learning_objectives": [
            "Demonstrate mastery of all foundational phonics patterns: CVC, CVCe, blends, digraphs, vowel teams",
            "Read grade-level text with 90% or higher accuracy",
            "Recognize 90 or more sight words instantly",
            "Retell a passage with key details including characters, setting, and main events",
            "Demonstrate readiness for the developing reading level",
        ],
        "teaching_guidance": {
            "introduction": "This is the capstone assessment for the foundational reading level. It is not a test to pass or fail — it is a comprehensive check of all the skills the child has built. Think of it as taking inventory: what is solid, what needs more practice, and is the child ready to move into the developing level? This assessment should feel natural and low-pressure, ideally woven into a normal reading session rather than presented as a formal test.",
            "scaffolding_sequence": [
                "Begin with a comfortable warm-up: the child reads a favorite familiar book aloud for confidence",
                "Assess phonics knowledge: present words with each pattern (CVC, CVCe, blends, digraphs, vowel teams) and ask the child to read them",
                "Assess sight word recognition: present the first 100 sight words on cards and note which are instant, which require effort, which are unknown",
                "Assess fluency: have the child read a grade-level passage aloud for one minute, counting words and noting accuracy",
                "Assess comprehension: after reading a short passage, ask the child to retell it and answer questions about main idea, characters, and details",
                "Assess listening comprehension: read a passage aloud and ask questions to compare with independent reading comprehension",
                "Review results together with the child in a positive frame: 'Look at everything you can do now! Here are some things we'll keep working on.'",
                "Create a plan for next steps: which skills need continued practice, and which indicate readiness for the developing level",
            ],
            "socratic_questions": [
                "What is the hardest part of reading for you right now? What feels easy?",
                "When you come to a word you don't know, what do you do first?",
                "What kind of books do you most enjoy reading? What makes them enjoyable?",
                "How has your reading changed since you started? What can you do now that you couldn't do before?",
            ],
            "practice_activities": [
                "Self-assessment: the child reviews their own progress — 'What can I read now that I couldn't before?' — building metacognition and pride",
                "Reading celebration: mark the completion of foundational skills with a special reading event — a trip to the library, a new book, or a reading party",
                "Portfolio review: look through the child's reading work from the year — early writing, word lists, reading logs — to see growth",
                "Goal setting: the child sets their own reading goals for the developing level: 'I want to read chapter books. I want to read faster.'",
            ],
            "real_world_connections": [
                "The child can now read simple instructions, signs, labels, and notes independently — real-world reading is possible",
                "Library visits become more independent: the child can browse, read back covers, and choose books on their own",
                "The child can write simple notes and letters that other people can read",
                "Reading becomes a tool for learning about interests: animals, space, sports, cooking — reading unlocks information",
            ],
            "common_misconceptions": [
                "Treating the assessment as a high-stakes test — this should be a natural, low-pressure check-in, not a stressful exam",
                "Expecting mastery of every single skill before moving to the developing level — if most skills are solid and the child is reading with comprehension, they are ready to progress even if some skills need continued practice",
                "Comparing the child's progress to grade-level norms or other children — each child develops at their own pace, and homeschool allows for that flexibility",
                "Stopping phonics instruction once the child passes the assessment — phonics continues in the developing level with more complex patterns (multisyllable words, advanced vowel patterns)",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Reads grade-level text with 90%+ accuracy",
                "Recognizes 90+ of the first 100 sight words instantly",
                "Retells a passage with characters, setting, and key events in order",
                "Applies all foundational phonics patterns to read unfamiliar words",
            ],
            "proficiency_indicators": [
                "Reads with 80-90% accuracy, using strategies for unknown words",
                "Recognizes 70-90 sight words instantly",
                "Retells with most key elements but may omit some details",
            ],
            "developing_indicators": [
                "Reads below 80% accuracy on grade-level text",
                "Recognizes fewer than 70 sight words",
                "Retelling is incomplete or disorganized",
            ],
            "assessment_methods": [
                "oral reading fluency check (one-minute timed reading)",
                "sight word flash card assessment",
                "phonics pattern word list reading",
                "oral retelling after independent reading",
            ],
            "sample_assessment_prompts": [
                "Read this passage aloud. I'll follow along. (grade-level text, 60+ words)",
                "Read these sight words as fast as you can. (flash card stack of 100 words)",
                "Read these words: cake, train, ship, frog, beach, truck. (one word per phonics pattern)",
                "Now tell me what the passage was about. Who was in it? What happened?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Read these words that cover all the phonics patterns you've learned: cat, cake, rain, ship, frog, green. How many can you read correctly?",
                "expected_type": "text",
                "hints": [
                    "Use your phonics skills: CVC (cat), silent-e (cake), vowel team (rain), digraph (ship), blend (frog, green)."
                ],
                "explanation": "These six words test six different phonics patterns: CVC (cat), CVCe (cake), vowel team (rain), digraph (ship), initial blend (frog), and consonant blend (green). Reading all six shows mastery of foundational phonics.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What do you do when you come to a word you don't know while reading?",
                "expected_type": "multiple_choice",
                "options": [
                    "Skip it and keep going",
                    "Sound it out using phonics, then check if it makes sense",
                    "Ask someone immediately without trying",
                    "Guess from the first letter only",
                ],
                "correct_answer": "Sound it out using phonics, then check if it makes sense",
                "hints": ["Good readers have a strategy. What's the best first step?"],
                "explanation": "The best strategy: try to sound it out using phonics patterns you know. Then check: does the word make sense in the sentence? If it still doesn't work, ask for help. This shows independent reading strategies.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Read this passage and retell it: 'Ben and his dog Rex went to the park. Rex chased a squirrel up a tree. Ben laughed and threw a stick. Rex forgot about the squirrel and ran to get the stick.'",
                "expected_type": "text",
                "hints": ["Read carefully, then retell: Who is in the story? Where are they? What happened?"],
                "explanation": "A complete retelling includes: characters (Ben and Rex), setting (the park), and events in order (Rex chased a squirrel, Ben threw a stick, Rex chased the stick instead). This demonstrates both reading accuracy and comprehension.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What kind of reader are you now compared to when you started? Name three things you can do now that you couldn't do before.",
                "expected_type": "text",
                "hints": ["Think about: reading words, reading books, understanding stories, reading out loud."],
                "explanation": "Self-reflection is part of the assessment. A child might say: 'I can read chapter books now. I know my sight words. I can retell stories.' This metacognition — thinking about your own learning — is a valuable skill.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Set a reading goal for yourself. What do you want to be able to do as a reader in the next few months? Why is that goal important to you?",
                "expected_type": "text",
                "hints": [
                    "Think about books you want to read, skills you want to improve, or how you want reading to help you."
                ],
                "explanation": "Goal-setting builds ownership of learning. Examples: 'I want to read a chapter book by myself,' 'I want to read faster so I can finish more books,' 'I want to read science books about space.' The goal should be personal and motivating.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Read this grade-level passage aloud for one minute. (Use a passage of 80+ words.)",
                "type": "open_response",
                "target_concept": "fluency_assessment",
                "rubric": "Mastery: 40+ WPM, 90%+ accuracy, with expression. Proficient: 30-40 WPM, 80-90% accuracy. Developing: under 30 WPM or below 80% accuracy.",
            },
            {
                "prompt": "Read these 20 sight words as fast as you can. (Random selection from the first 100.)",
                "type": "open_response",
                "target_concept": "sight_word_assessment",
                "rubric": "Mastery: 18-20 correct in under 30 seconds. Proficient: 15-17 correct. Developing: fewer than 15 correct.",
            },
            {
                "prompt": "Retell the passage you just read. Include who, where, and what happened.",
                "type": "open_response",
                "target_concept": "comprehension_assessment",
                "rubric": "Mastery: retells with characters, setting, and events in order. Proficient: retells most elements. Developing: incomplete retelling.",
            },
            {
                "prompt": "What was the main idea of the passage?",
                "type": "open_response",
                "target_concept": "main_idea_assessment",
                "rubric": "Mastery: states main idea in one sentence. Proficient: close but includes extra details. Developing: cannot identify main idea.",
            },
        ],
        "resource_guidance": {
            "required": [
                "grade-level reading passages for assessment",
                "sight word flash cards (first 100)",
                "phonics pattern word list",
            ],
            "recommended": ["reading assessment recording form", "stopwatch or timer for fluency check"],
        },
        "time_estimates": {"first_exposure": 30, "practice_session": 20, "assessment": 30},
        "accommodations": {
            "dyslexia": "Allow extra time on all timed portions. Assess phonics knowledge through oral reading, not written spelling. Compare listening comprehension to reading comprehension to understand the gap. Celebrate growth rather than comparing to benchmarks. Consider that a dyslexic child may be ready for developing-level comprehension work while continuing foundational-level phonics.",
            "adhd": "Break the assessment into multiple short sessions (10-15 minutes each) rather than one long session. Intersperse assessment tasks with movement breaks. Make it feel like a conversation, not a test.",
            "gifted": "The child may have mastered foundational skills very quickly. Use the assessment to confirm readiness and move to the developing level without delay. Challenge with above-level reading passages. Begin discussing literary elements (plot, theme, point of view).",
            "visual_learner": "Use large, clear print for assessment passages. Minimize visual clutter on the page. Good lighting and comfortable reading position.",
            "kinesthetic_learner": "Allow the child to stand or walk while reading aloud. Use physical flash cards they can sort and handle. Break assessment into active segments.",
            "auditory_learner": "The oral portions (reading aloud, retelling, discussion) will be strengths. Ensure the environment is quiet for optimal listening during comprehension checks.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "This is the capstone check of the foundational reading level. It is not a test to pass or fail but a careful inventory: what reading skills are solid, what still needs practice, and whether the child is ready for the developing level. We check the phonics patterns (CVC, silent-e, blends, digraphs, and vowel teams), reading accuracy on grade-level text, instant recognition of sight words, and the retelling of a passage. It should feel calm and natural, woven into an ordinary reading session.",
                "gradual_release": {
                    "i_do": "Explain the parts of the check warmly and without pressure, and model the warm-up by reading a short familiar passage aloud, showing what fluent, accurate reading and a clear retelling look like.",
                    "we_do": "Begin with a comfortable warm-up together: the child reads a favorite familiar book aloud for confidence, and you talk through what each part of the check will involve so nothing is a surprise.",
                    "you_do": "Child independently reads the phonics-pattern words, the sight words, and a grade-level passage, then retells it, while the parent quietly notes what is solid and what needs more practice.",
                },
                "guided_practice": [
                    "Read a familiar book aloud as a confidence-building warm-up",
                    "Read words covering each phonics pattern: CVC, silent-e, blends, digraphs, vowel teams",
                    "Retell a short passage, naming characters, setting, and main events",
                ],
                "independent_practice": [
                    "Read a grade-level passage aloud for accuracy and fluency",
                    "Read the first one hundred sight words and note which are instant",
                ],
                "mastery_check": [
                    "Read grade-level text with ninety percent or higher accuracy",
                    "Recognize ninety or more of the first hundred sight words instantly",
                    "Apply all foundational phonics patterns and retell a passage with key details",
                ],
                "spiral_review": [
                    "Revisit any phonics pattern or sight words not yet solid before moving to the developing level",
                ],
            },
            "classical": {
                "narrative_introduction": "Every stage of learning ends with a looking-back, a gathering-up of what has been won. This is that moment for foundational reading. It is not a trial to be feared but a gateway: a comprehensive showing of the phonics, the fluency, and the comprehension the child has built, and an honest judgment that the child stands ready to pass on to the developing level. Assessment here opens the gate; it does not bar it.",
                "memory_work": {
                    "chants": [
                        "Recite again the phonics patterns mastered: CVC, silent-e, blends, digraphs, and vowel teams",
                        "Recite the marks of a reader: to read accurately, to know the sight words, and to retell what was read",
                    ],
                    "recitations": [
                        "Recite a well-loved passage learned by heart over the foundational level, the gathered fruit of the year's reading",
                    ],
                },
                "recitation_routine": "Make the check itself a cumulative recitation: the child reads and retells, drawing on every skill built across the foundational level, oldest and newest together.",
                "history_integration": "Tell that learning has always been marked by such gateways, that in older schooling a stage was completed and confirmed before the next was begun, and that to pass this gate is to join the long company of those who have learned to read.",
                "read_aloud_suggestions": [
                    "A worthy grade-level passage, read by the child aloud, fit to show the reading skill now won",
                    "A fine book held ready as the first reward of the developing level to come",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A living book the child loves and knows, read aloud by the child as the gentlest possible showing of their reading",
                    "A new and beautiful book held ready, the first of the developing level",
                ],
                "short_lesson_flow": "There is no formal test. On an ordinary day, simply listen as the child reads a passage of a living book aloud, and then let them narrate it. That is the whole assessment. You will hear at once whether the reading is fluent and accurate and whether the narration is full and ordered. If both are so, the child is ready; if not, you have seen exactly what to gently continue.",
                "narration_prompt": "Read me this passage, and then tell it back to me in your own words. Who was in it, where did it happen, and what took place?",
                "real_world_objects": [
                    "A living book, read aloud and narrated, the gentle instrument of the whole assessment",
                    "The child's own reading notebook or list of books read, showing the year's growth",
                    "Print in the real world the child can now read: signs, labels, recipes, notes",
                ],
                "nature_connection": "Let the child read aloud a passage about the natural world and then narrate it, or read the labels in their own nature notebook, so the assessment is set in the living things they love.",
                "habit_focus": "The habit of attention, shown now in full: the child who can read a passage and narrate it back has formed the habit on which all further learning rests.",
            },
            "montessori": {
                "prepared_materials": [
                    "The familiar reading materials of the foundational level, used now as the child works, not as a test",
                    "A shelf of grade-level books for the child to choose and read",
                    "The child's own ongoing reading record kept across the level",
                    "Phonics word lists and sight word cards, met as ordinary work",
                ],
                "presentation": {
                    "three_period_lesson": "There is no new naming here; instead the adult watches the child in the third period of every lesson long since given, recalling and applying letters, sounds, and words independently in real reading.",
                    "steps": [
                        "The adult prepares the environment with grade-level books and the familiar materials, and observes the child at ordinary reading work",
                        "The adult notes which phonics patterns, sight words, and comprehension skills the child applies fluently and independently",
                        "The adult and child review the child's reading record together and see that the foundational work is complete",
                    ],
                },
                "control_of_error": "The child's own reading is the control: in real, self-chosen reading, a phonics pattern not yet secure or a sight word not yet known reveals itself plainly, with no test required, so the adult's observation rests on what the child actually does.",
                "abstraction_pathway": "From the concrete materials of the foundational level long since internalized, the child has reached independent reading; this assessment simply confirms that the abstraction is complete and the next stage may begin.",
                "extensions": [
                    "Move into the developing level's reading work without delay once competence is observed",
                    "Continue the reading record into the next stage",
                    "Let the child set their own reading work and goals for the level to come",
                ],
                "observation_focus": "Watch, across the child's ordinary reading, for accurate decoding of every phonics pattern, instant sight word recognition, and full, ordered retelling, the signs that the foundational level is truly complete.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a rich and varied library, signs, menus, recipes, and notes everywhere a reader's eye can fall",
                    "Leave out books a small step beyond the child's current ease, ready for when they reach for them",
                    "Have the next, more challenging books quietly available for the child to discover",
                ],
                "real_world_contexts": [
                    "Reading signs, labels, menus, and instructions out in the world, with no help",
                    "Reading a recipe and following it, or reading the rules of a new game",
                    "Choosing and reading books from the library independently",
                    "Reading a note, a letter, or a message and writing one back",
                ],
                "conversation_starters": [
                    "What are you reading these days? What do you want to read next?",
                    "How has reading changed for you, what can you do now that you could not before?",
                    "What do you most want to be able to read or learn about now?",
                ],
                "resource_bank": [
                    "A wide home library and free, frequent library visits",
                    "The endless print of everyday life as proof of real reading",
                    "More challenging books kept within reach for when the child is ready",
                ],
                "parent_role": "There is no test. You already know your child has become a reader, because you see them read, the cereal box, the street sign, the bedtime book, the game's rules. Notice that fluency as it shows itself in real life, follow the child into harder and richer books as their own appetite grows, and trust what you have watched unfold.",
                "observation_documentation": "Over time, simply note what the child reads in the course of real life: whether they decode unfamiliar words with ease, read signs and books and instructions independently, retell what they have read, and reach without prompting for harder books. This lived noticing, not any test, shows that the child is a reader and ready for whatever comes next.",
            },
        },
        "connections": {
            "math": "Assessment skills transfer: self-reflection, goal-setting, and recognizing growth are the same in math and reading",
            "science": "Independent reading opens the door to science books, nature guides, and experiment instructions",
            "history": "Independent reading allows engagement with historical narratives, biographies, and primary sources at a basic level",
        },
    },
    "rf-26": {
        "enriched": True,
        "learning_objectives": [
            "Hold a book right-side up with the front cover facing the reader",
            "Identify the front cover, the back cover, and the spine of a book",
            "Open a book to the beginning and turn pages one at a time from front to back",
            "Show where the title is and explain that print, not the pictures, is read",
        ],
        "teaching_guidance": {
            "introduction": "Before a child can read print, they must know how a book works as an object: which way is up, where a book begins, and how to move through it one page at a time. This is concrete, hands-on handling of a real book, the very first print concept and entirely separate from sounding out words.",
            "scaffolding_sequence": [
                "Hand the child a book upside down or back to front and let them turn it the right way to start",
                "Name the front cover, the back cover, and the spine while touching each one",
                "Open to the first page and show that a book is read from the front toward the back",
                "Turn pages one at a time, holding the top corner, without skipping any",
                "Point to the title on the front cover and say that the words, not the pictures, tell the story",
            ],
            "socratic_questions": [
                "Which way does this book need to go so we can read it?",
                "Where is the front of the book? Where do we begin?",
                "Which part do we read, the pictures or the words?",
            ],
            "practice_activities": [
                "Right-side-up sort: a stack of books, the child turns each one to face the right way",
                "Page-turning practice with a sturdy board book, one page at a time",
                "Cover hunt: point to the front cover, back cover, and spine on call",
            ],
            "real_world_connections": [
                "Choosing and holding the bedtime story",
                "Carrying a library book and shelving it spine-out",
                "Handling a magazine or catalog the right way up",
            ],
            "common_misconceptions": [
                "Holding the book upside down or starting from the back: model orienting it before every reading",
                "Turning several pages at once and missing part of the story: practice one-corner, one-page turns",
                "Thinking the pictures are what is read: point to the print as you read so the words are seen to carry the story",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Takes a handed-over book and orients it right-side up, ready at the first page",
                "Names the front cover, back cover, and spine correctly",
                "Turns pages one at a time from front to back and points to print as what is read",
            ],
            "assessment_methods": [
                "observation of book handling",
                "oral naming of book parts",
                "page-turning demonstration",
            ],
            "sample_assessment_prompts": [
                "Show me how to hold this book so we can read it",
                "Point to the front cover and the back cover",
                "Turn to the next page for me, just one page",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "I hand you a book upside down. What is the first thing you do before we read?",
                "expected_type": "text",
                "correct_answer": "turn it right-side up",
                "hints": ["Look at the pictures and words: which way are they facing?"],
                "explanation": "First turn the book right-side up so the cover faces you and the words are the right way up.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which cover has the title and comes first, the front cover or the back cover?",
                "expected_type": "text",
                "correct_answer": "the front cover",
                "hints": ["It is the cover we see when the book is closed and ready to read"],
                "explanation": "The front cover has the title and is where the book begins.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Do we begin reading a book at the front or at the back?",
                "expected_type": "text",
                "correct_answer": "the front",
                "hints": ["Think about where the story starts"],
                "explanation": "A book is read from the front toward the back.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "In a picture book, which do we read, the pictures or the words?",
                "expected_type": "text",
                "correct_answer": "the words",
                "hints": ["The pictures help us, but one of these carries the story in print"],
                "explanation": "We read the words; the print carries the meaning, and the pictures help us understand it.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "How many pages should you turn at one time so you do not skip any?",
                "expected_type": "number",
                "correct_answer": "1",
                "hints": ["Hold just the top corner of a single page"],
                "explanation": "Turn one page at a time so no part of the book is skipped.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is the spine of the book?",
                "expected_type": "text",
                "correct_answer": "the joined edge where the pages are held together (the part you see on a shelf)",
                "hints": ["It is the side that faces out when a book stands on a shelf"],
                "explanation": "The spine is the bound edge that holds the pages together and shows the title on a shelf.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Your friend opens the book from the back and starts reading there. What would you tell them?",
                "expected_type": "text",
                "correct_answer": "start at the front and read toward the back",
                "hints": ["Where does a book begin?"],
                "explanation": "Tell them to start at the front cover and read forward, one page at a time, toward the back.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Pick up any book and show how you get it ready and turn to the first page. Tell me what you are doing as you go.",
                "expected_type": "text",
                "hints": ["Name the front cover and the first page, and turn one page at a time"],
                "explanation": "There is no single right sentence here; the child should orient the book right-side up, open to the front, and turn one page at a time while narrating what they do.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Hold this book ready to read.",
                "type": "open_response",
                "rubric": "Mastery: orients right-side up, front cover up, ready at the first page with no help. Proficient: orients correctly after a short pause. Developing: needs a reminder which way is up.",
                "target_concept": "book_orientation",
            },
            {
                "prompt": "Point to the front cover, the back cover, and the spine.",
                "type": "open_response",
                "rubric": "Mastery: identifies all three correctly. Proficient: identifies two. Developing: identifies one with help.",
                "target_concept": "parts_of_a_book",
            },
            {
                "prompt": "Which way do we read a book, front to back or back to front?",
                "type": "text",
                "correct_answer": "front to back",
                "target_concept": "book_directionality",
            },
            {
                "prompt": "How many pages do we turn at one time?",
                "type": "number",
                "correct_answer": "1",
                "target_concept": "one_page_at_a_time",
            },
            {
                "prompt": "Show me how you turn the pages to get to the end of the story.",
                "type": "open_response",
                "rubric": "Mastery: turns one page at a time from front to back. Proficient: mostly one at a time with an occasional double. Developing: needs help to turn single pages in order.",
                "target_concept": "page_turning",
            },
        ],
        "resource_guidance": {
            "required": ["sturdy picture books or board books the child can handle"],
            "recommended": ["a small basket of favorite books within reach", "regular library visits"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 10},
        "accommodations": {
            "dyslexia": "Book handling is a strength to build confidence on; keep it playful and separate from any letter work, which comes later.",
            "adhd": "Keep sessions short and active: a quick book-sort or page-turning race, then move on while interest is high.",
            "gifted": "Add the title page, author, and where the story begins on the first page of print; invite the child to 'show' a younger sibling.",
            "visual_learner": "Use books with a clearly different front and back cover and a visible spine title to make the parts easy to see.",
            "kinesthetic_learner": "Let the child physically sort, orient, and turn many real books; handling is the whole point.",
            "auditory_learner": "Narrate each step aloud ('front cover, open to the first page, turn one page') and have the child say it back.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "A book has a front and a back, a right way up, and a beginning; we read the words from the front toward the back, one page at a time. Today we learn to hold and open a book correctly and to name its parts.",
                "gradual_release": {
                    "i_do": "Hold up a book the wrong way, then say, 'This is upside down, watch me fix it,' and turn it right-side up. Name the front cover, back cover, and spine, touching each. Open to the first page, run a finger under the print, and say, 'We read the words, from the front toward the back.'",
                    "we_do": "Hand the child a book turned the wrong way and orient it together. Point to and name the front cover, back cover, and spine together. Turn the first few pages together, one at a time, saying 'one page' each time.",
                    "you_do": "Child takes a closed book, orients it right-side up, names the front cover, back cover, and spine, opens to the first page, and turns pages one at a time from front to back.",
                },
                "guided_practice": [
                    "Right-side-up sort done together: turn each book in a stack to face the right way",
                    "Name-the-part call-and-response: front cover, back cover, spine, first page",
                ],
                "independent_practice": [
                    "The child gets a book ready to read all by themselves and turns to the first page",
                    "The child shows a stuffed animal or sibling how to hold and open a book",
                ],
                "mastery_check": [
                    "Orients a handed-over book right-side up without help",
                    "Names front cover, back cover, and spine correctly",
                    "Turns pages one at a time from front to back",
                ],
                "spiral_review": [
                    "Begin each lesson by re-checking the precursor skill of carrying and orienting a book the right way up before any new print-concept work, since correct handling underlies everything that follows",
                ],
            },
            "classical": {
                "narrative_introduction": "A book is a made thing with an order to it: a front, a back, a beginning, and a path through it from first page to last. The grammar stage begins with knowing that order surely, before a single word is decoded.",
                "memory_work": {
                    "chants": [
                        "Chant the parts in order, touching each: 'front cover, pages, back cover, spine'",
                        "Chant the reading direction, 'front to back, one page at a time,' while turning pages",
                    ],
                    "recitations": [
                        "Recite a short, known verse about caring for books, said aloud as the book is handled gently",
                    ],
                },
                "recitation_routine": "Open each lesson by naming the parts of a familiar book aloud from memory, touching each part, before adding any new concept; the naming is cumulative and never assumed.",
                "history_integration": "Books are an old inheritance; people have bound pages and turned them in order for a very long time, and learning to handle a book joins the child to that long tradition of readers.",
                "read_aloud_suggestions": [
                    "A beautifully made picture book, handled with care and read aloud, so the child sees a book treated as something ordered and worth keeping",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A few beautiful, well-made picture books with clear covers and lovely illustrations, chosen to be handled and loved",
                ],
                "short_lesson_flow": "Settle with a lovely book and delight in it first. Then gently notice how it works: turn it right-side up, find the front cover and the spine, open to the beginning, and turn one page at a time. Stop while the child still wants more.",
                "narration_prompt": "Show me how this book begins, and tell me which part we read.",
                "real_world_objects": [
                    "Real, beautiful books from the family shelf, handled with care",
                    "A library book carried, opened, and returned",
                ],
                "nature_connection": "Take a nature picture book outdoors, hold and open it correctly to find a picture of something just seen, treating the book gently in the open air.",
                "habit_focus": "The habit of handling books gently and attentively, and of treating a book as something ordered and worth caring for.",
            },
            "montessori": {
                "prepared_materials": [
                    "A low shelf with a few real books displayed front-cover-out, within the child's reach",
                    "Sturdy, beautiful books sized for small hands",
                    "A calm, defined space for looking at a book",
                ],
                "presentation": {
                    "three_period_lesson": "Naming: 'This is the front cover. This is the spine.' Recognition: 'Show me the front cover. Show me the spine.' Recall: 'What is this part called?' touching each part of the book.",
                    "steps": [
                        "Show how to carry a book with two hands and set it down right-side up",
                        "Name the front cover, back cover, and spine, inviting the child to touch each",
                        "Open to the first page and turn pages slowly, one at a time, from front to back",
                    ],
                },
                "control_of_error": "The book itself shows the error: held upside down the pictures and words are clearly wrong-way-up, and the child sees and corrects it. The guide models care and lets the child self-correct.",
                "abstraction_pathway": "From handling the concrete book as an object, to understanding it as an ordered carrier of words read in a fixed direction, which prepares the directionality work that follows.",
                "extensions": [
                    "Return books to the shelf front-cover-out, matching each to its place",
                    "Care-of-books work: smoothing a bent page, wiping a cover, carrying carefully",
                ],
                "observation_focus": "Watch whether the child orients and opens a book without prompting, turns single pages, and treats books with care, and note their growing pleasure in choosing and handling them.",
            },
            "unschooling": {
                "invitations": [
                    "Keep inviting baskets of wonderful books within easy reach all around the home",
                    "Read together often and let the child hold the book and turn the pages whenever they want to",
                    "Visit the library and let the child carry, open, and choose books freely",
                ],
                "real_world_contexts": [
                    "Bedtime stories the child holds and opens",
                    "Cookbooks, catalogs, and magazines handled around the house",
                    "Library trips: carrying, opening, and shelving books",
                ],
                "conversation_starters": [
                    "Would you hold the book and turn the pages for us tonight?",
                    "Which way does it go so the picture is the right way up?",
                    "Where does this story start?",
                ],
                "resource_bank": [
                    "Plenty of sturdy, appealing books kept within reach",
                    "A child-height shelf or basket the child manages themselves",
                    "Library access and regular visits",
                ],
                "parent_role": "Surround the child with good books and read together joyfully, handing over the holding and page-turning whenever the child reaches for it, and answering real questions about how a book works without turning it into a drill.",
                "observation_documentation": "Over time, simply notice whether the child picks up books the right way, turns pages one at a time, and reaches for books in daily life; this lived noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Turning pages one at a time and in order is the same one-to-one, sequential care used in counting objects",
            "science": "Handling a nature guide or picture book to find and look closely at real things",
            "history": "Books pass stories down in order, front to back, the way they have been kept for generations",
        },
    },
    "rf-27": {
        "enriched": True,
        "learning_objectives": [
            "Track print from left to right across a line of text with a finger",
            "Make the return sweep from the end of one line to the start of the next",
            "Read the lines of a page from top to bottom in order",
            "Explain that English print is read left-to-right and top-to-bottom",
        ],
        "teaching_guidance": {
            "introduction": "Directionality is the path the eyes take through print: left to right along a line, then a return sweep down and back to the left for the next line, and top to bottom down the page. It is taught by tracking real print with a finger, building on knowing how a book is held and opened.",
            "scaffolding_sequence": [
                "Place a finger under the first word on the left and slide it right along the line as you read",
                "At the end of the line, sweep the finger down and back to the far left to begin the next line (the return sweep)",
                "Read the lines from the top of the page down to the bottom in order",
                "On a two-page spread, read the left page fully before the right page",
                "Let the child lead the finger while you read aloud at their pace",
            ],
            "socratic_questions": [
                "Where on the line do we start? Which way does the finger move?",
                "When we get to the end of the line, where does the finger go next?",
                "Do we read the top of the page first or the bottom first?",
            ],
            "practice_activities": [
                "Finger-tracking a big-print line while the parent reads aloud",
                "Return-sweep practice: an arrow drawn from line-end down to the next line-start",
                "Pointer reading: the child uses a craft-stick pointer to lead left-to-right",
            ],
            "real_world_connections": [
                "Following a shopping list down the page",
                "Reading a recipe line by line from the top",
                "Tracking the words in a song or rhyme chart",
            ],
            "common_misconceptions": [
                "Starting on the right or moving right-to-left: anchor each start with a green dot on the left",
                "Skipping the return sweep and jumping randomly: practice the sweep as its own move",
                "Reading the bottom line before the top: briefly number the lines to fix top-to-bottom order",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Tracks a line left to right with one finger",
                "Makes an accurate return sweep to the next line's first word",
                "Reads lines from top to bottom in order",
            ],
            "assessment_methods": [
                "finger-tracking observation",
                "return-sweep demonstration",
                "oral explanation of direction",
            ],
            "sample_assessment_prompts": [
                "Put your finger where we start reading and slide it the way we read",
                "Show me what your finger does at the end of this line",
                "Which line do we read first on this page?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "On a line of words, which side do we start reading from, the left or the right?",
                "expected_type": "text",
                "correct_answer": "the left",
                "hints": ["It is the side your finger touches first"],
                "explanation": "We start reading on the left and move to the right.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which way does your finger slide as you read along a line?",
                "expected_type": "text",
                "correct_answer": "to the right",
                "hints": ["Away from where we started"],
                "explanation": "The finger slides left to right along the line.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Do we read the top of the page first or the bottom first?",
                "expected_type": "text",
                "correct_answer": "the top",
                "hints": ["We move down the page as we read"],
                "explanation": "We read from the top of the page down to the bottom.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "When your finger reaches the end of a line, where does it go to keep reading?",
                "expected_type": "text",
                "correct_answer": "down and back to the start of the next line (the return sweep)",
                "hints": ["Down one line and all the way back to the left"],
                "explanation": "It makes a return sweep: down to the next line and back to the far left.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "On a book with two pages open side by side, which page do we read first?",
                "expected_type": "text",
                "correct_answer": "the left page",
                "hints": ["Same as where we start on a line"],
                "explanation": "We read the left page first, then the right page.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "A line has 5 words. Reading left to right, which word number do we read first?",
                "expected_type": "number",
                "correct_answer": "1",
                "hints": ["The very first word on the left"],
                "explanation": "We read the first word (on the left) first, then 2, 3, 4, 5 to the right.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Your friend points to the last word on a line and says we start there. What would you tell them?",
                "expected_type": "text",
                "correct_answer": "we start at the first word on the left, not the last word on the right",
                "hints": ["Which side comes first?"],
                "explanation": "Tell them we start at the left end of the line and read toward the right.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Read a short line aloud with me while you lead your finger under the words, then do the return sweep to the next line. Tell me what your finger is doing.",
                "expected_type": "text",
                "hints": ["Left to right, then down and back to the left"],
                "explanation": "No single right sentence; the child should track left-to-right and then sweep down and back to the next line's first word while narrating.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Show me where we start reading on this line and slide your finger the way we read.",
                "type": "open_response",
                "rubric": "Mastery: starts at the left and tracks smoothly to the right. Proficient: starts left with some uneven tracking. Developing: needs a cue for where to start or which way to go.",
                "target_concept": "left_to_right_tracking",
            },
            {
                "prompt": "Show me what your finger does at the end of the line.",
                "type": "open_response",
                "rubric": "Mastery: makes a clean return sweep to the next line's first word. Proficient: returns to the next line with a small miss. Developing: needs help to find the next line.",
                "target_concept": "return_sweep",
            },
            {
                "prompt": "Which side of a line do we start reading from?",
                "type": "text",
                "correct_answer": "the left",
                "target_concept": "starting_point",
            },
            {
                "prompt": "Do we read a page from top to bottom or bottom to top?",
                "type": "text",
                "correct_answer": "top to bottom",
                "target_concept": "top_to_bottom",
            },
            {
                "prompt": "On a line of 4 words, point to the words in the order we read them.",
                "type": "open_response",
                "rubric": "Mastery: points 1-2-3-4 left to right. Proficient: correct order with a pause. Developing: points out of order without help.",
                "target_concept": "word_order_direction",
            },
        ],
        "resource_guidance": {
            "required": ["big-print books or a printed rhyme chart the child can track with a finger"],
            "recommended": ["a craft-stick pointer", "a green dot for line starts and a red dot for line ends"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 10},
        "accommodations": {
            "dyslexia": "Use a finger or pointer and a line marker to anchor tracking; over-practice the return sweep slowly and patiently.",
            "adhd": "Keep lines short and use a bright pointer; make the return sweep a fun, exaggerated 'swoop' move.",
            "gifted": "Move to tracking smaller print and longer lines, and to reading a two-page spread in the right order independently.",
            "visual_learner": "Mark line starts green and line ends red, and draw the return-sweep arrow so the path is visible.",
            "kinesthetic_learner": "Have the child make the big return-sweep arm motion in the air before doing it on the page.",
            "auditory_learner": "Say 'left to right, sweep back' as a rhythm while tracking so the path is heard as well as seen.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "English print is read left to right along each line, and top to bottom down the page; at the end of a line we sweep back to the left to begin the next. Today we track print in that exact path.",
                "gradual_release": {
                    "i_do": "Put a finger under the first word on the left and read slowly, sliding right. At the line's end say, 'Now the return sweep,' and move down and back to the left. Read the page top to bottom this way.",
                    "we_do": "Track a line together, your hand over the child's, sliding left to right, then make the return sweep together. Do two or three lines top to bottom together.",
                    "you_do": "Child tracks each line left to right, makes the return sweep to the next line, and reads the page from top to bottom in order while you read the words aloud.",
                },
                "guided_practice": [
                    "Finger-track a known rhyme chart line by line together",
                    "Return-sweep drill: practice just the end-of-line move several times",
                ],
                "independent_practice": [
                    "The child leads the finger under the words of a familiar big-print page",
                    "The child uses a pointer to read a list from top to bottom",
                ],
                "mastery_check": [
                    "Tracks a line left to right without reversing",
                    "Makes an accurate return sweep to the next line",
                    "Reads lines top to bottom in order",
                ],
                "spiral_review": [
                    "Warm up by re-doing the book-handling steps from rf-20 (open to the first page, find where the print begins) before tracking direction, since directionality builds directly on knowing where the print starts",
                ],
            },
            "classical": {
                "narrative_introduction": "Print runs on a fixed road: left to right, line by line, top to bottom. The grammar stage walks that road with a finger until the path is sure and automatic.",
                "memory_work": {
                    "chants": [
                        "Chant 'left to right, top to bottom' while tracking a line",
                        "Chant 'down and back' at every return sweep",
                    ],
                    "recitations": [
                        "Recite a short known rhyme while finger-tracking its printed lines so the words and the path are joined",
                    ],
                },
                "recitation_routine": "Begin by tracking a familiar memorized rhyme on a chart, saying the direction aloud, before reading anything new; the path is rehearsed cumulatively.",
                "history_integration": "Different writing has run in different directions across history; English runs left to right and top to bottom, a fixed convention the child now joins.",
                "read_aloud_suggestions": [
                    "A large-print poem read aloud while the child's finger follows the printed lines",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A big-print picture book or a beautifully lettered poem chart with clear, well-spaced lines",
                ],
                "short_lesson_flow": "Enjoy a short, loved verse together, then let the child lead a finger under its words left to right, sweeping down to each new line, top to bottom. Keep it brief and gentle.",
                "narration_prompt": "Show me with your finger which way we read, and tell me what your finger does at the end of a line.",
                "real_world_objects": [
                    "A handwritten family note read left to right together",
                    "A poem chart on the wall tracked with a finger",
                ],
                "nature_connection": "Read a short labelled nature poster outdoors, tracking each line left to right and top to bottom while looking at the real plant or bird named.",
                "habit_focus": "The habit of attention: following print steadily and exactly along its proper path.",
            },
            "montessori": {
                "prepared_materials": [
                    "Large, clear print cards or sentence strips with generous spacing",
                    "A pointer sized for the child's hand",
                    "Textured line-start dots for the left margin",
                ],
                "presentation": {
                    "three_period_lesson": "Naming: 'We start here, on the left, and move this way, to the right.' Recognition: 'Show me where we start. Show me which way we go.' Recall: 'What do we do at the end of the line?'",
                    "steps": [
                        "Show tracking one line left to right with the pointer",
                        "Show the return sweep down to the next line's start",
                        "Read several lines top to bottom, inviting the child to lead",
                    ],
                },
                "control_of_error": "On a known sentence the words only make sense in the correct order, so reading in the wrong direction sounds wrong, which the child hears and corrects.",
                "abstraction_pathway": "From physically dragging a finger along the line, to internalizing the left-to-right, top-to-bottom path that all later decoding will assume.",
                "extensions": [
                    "Track longer sentences that wrap across several lines",
                    "Read a two-column list in the correct order",
                ],
                "observation_focus": "Watch whether the child starts on the left, tracks smoothly right, and finds the next line by a return sweep without prompting.",
            },
            "unschooling": {
                "invitations": [
                    "Run a finger under the words whenever you read together, so the path is seen again and again",
                    "Leave rhyme charts, lists, and labels around for the child to follow",
                    "Invite the child to be the 'pointer' who leads the words while you read",
                ],
                "real_world_contexts": [
                    "Following a grocery list down the page",
                    "Tracking the words of a favorite song on a lyric sheet",
                    "Reading a recipe line by line together",
                ],
                "conversation_starters": [
                    "Which way are we going as we read this line?",
                    "Where does your finger go when the line runs out?",
                    "Want to lead the words for us with your finger?",
                ],
                "resource_bank": [
                    "Big-print books, song sheets, and lists kept around the home",
                    "A favorite pointer or just a finger",
                    "Wall charts of loved rhymes",
                ],
                "parent_role": "Point under words naturally as you share text together, hand the lead to the child when they want it, and answer real questions about which way the words go, without drilling.",
                "observation_documentation": "Notice over time whether the child tracks left to right, sweeps to new lines, and moves down a page in order during real shared reading; that noticing is the assessment.",
            },
        },
        "connections": {
            "math": "Left-to-right, top-to-bottom order is the same orderly scanning used to read a number line or a hundreds chart",
            "science": "Following the steps of an experiment or a labelled diagram in order down the page",
            "history": "Reading a timeline or a story in its proper order, beginning to end",
        },
    },
    "rf-28": {
        "enriched": True,
        "learning_objectives": [
            "Understand that spaces separate one written word from the next",
            "Match each spoken word to one written word while reading (voice-to-print matching)",
            "Point to each word in a short, memorized line as it is said",
            "Count the number of words in a short written line",
        ],
        "teaching_guidance": {
            "introduction": "Concept of word is the bridge between speech and print: a spoken word matches exactly one written word, and the spaces show where one word ends and the next begins. It is taught with short, memorized lines that the child points to word by word, building on left-to-right tracking.",
            "scaffolding_sequence": [
                "Read a short, memorized line and touch one word for each word said",
                "Show that the white spaces are the gaps that separate the words",
                "Have the child point to each word as you both say the line slowly",
                "Stop on a word and ask, 'Which word is my finger on?'",
                "Count the words in the line by touching each one",
            ],
            "socratic_questions": [
                "How do we know where one word ends and the next begins?",
                "When I say a word, how many written words should my finger touch?",
                "How many words are in this line? How do you know?",
            ],
            "practice_activities": [
                "Point-and-say a memorized nursery rhyme line, one touch per word",
                "Cut-up sentence: rebuild a known line from word cards with spaces between",
                "Word-count: tap and count the words in short printed lines",
            ],
            "real_world_connections": [
                "Pointing to each word of a name on a label",
                "Following a short caption under a photo word by word",
                "Counting the words on a sign",
            ],
            "common_misconceptions": [
                "Pointing to a letter or syllable instead of a whole word: model touching whole words bounded by spaces",
                "Sliding past two words for one spoken word: slow down to one touch per spoken word",
                "Not seeing spaces as boundaries: highlight the spaces or use word cards with clear gaps",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Touches one written word for each spoken word in a short line",
                "Identifies the spaces as what separates words",
                "Counts the words in a short line correctly",
            ],
            "assessment_methods": ["voice-to-print pointing", "word-count demonstration", "oral explanation of spaces"],
            "sample_assessment_prompts": [
                "Point to each word as we say this line together",
                "Show me a space between two words",
                "How many words are in this line?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What separates one written word from the next on a line?",
                "expected_type": "text",
                "correct_answer": "a space",
                "hints": ["Look at the gaps between the words"],
                "explanation": "Spaces (the gaps) separate one written word from the next.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "When you say one word out loud, how many written words should your finger touch?",
                "expected_type": "number",
                "correct_answer": "1",
                "hints": ["One spoken word matches one written word"],
                "explanation": "One spoken word matches exactly one written word, so the finger touches one word.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "In the line 'I see a cat', how many words are there?",
                "expected_type": "number",
                "correct_answer": "4",
                "hints": ["Touch and count each word: I / see / a / cat"],
                "explanation": "There are 4 words: I, see, a, cat.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "We say the line 'The dog ran' together. Your finger should land on a new word each time you say a word. True or false?",
                "expected_type": "true_false",
                "correct_answer": "true",
                "hints": ["One touch for each spoken word"],
                "explanation": "True: each spoken word matches one written word, so the finger moves to a new word each time.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "In 'a big red ball', point to and count the words. How many?",
                "expected_type": "number",
                "correct_answer": "4",
                "hints": ["a / big / red / ball"],
                "explanation": "There are 4 words: a, big, red, ball.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "If my finger is on the third word of 'I like to run', which word is it?",
                "expected_type": "text",
                "correct_answer": "to",
                "hints": ["Count: I (1), like (2), to (3)"],
                "explanation": "The third word is 'to' (I, like, to, run).",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Your friend says the line 'We can play' but touches only two words. What went wrong and how do you fix it?",
                "expected_type": "text",
                "correct_answer": "they skipped a word; touch one word for each word said: We / can / play",
                "hints": ["How many words did they say? How many did they touch?"],
                "explanation": "They touched too few words; match one touch to each spoken word so all three words (We, can, play) get a touch.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Say a short line you know by heart and point to each word as you say it. Tell me how the spaces helped you.",
                "expected_type": "text",
                "hints": ["One touch per word; the spaces show where each word stops"],
                "explanation": "No single right answer; the child should point one word per spoken word and explain that the spaces marked where each word began and ended.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Point to each word as we say this short line together.",
                "type": "open_response",
                "rubric": "Mastery: one accurate touch per spoken word across the line. Proficient: matches most words with a small slip. Developing: needs help to keep one-to-one matching.",
                "target_concept": "voice_to_print_matching",
            },
            {
                "prompt": "Show me a space between two words and tell me what it does.",
                "type": "open_response",
                "rubric": "Mastery: points to a space and says it separates the words. Proficient: points to a space with a partial explanation. Developing: needs help to find the space.",
                "target_concept": "spaces_separate_words",
            },
            {
                "prompt": "How many words are in the line 'I can hop'?",
                "type": "number",
                "correct_answer": "3",
                "target_concept": "word_counting",
            },
            {
                "prompt": "When you say one word, how many written words does your finger touch?",
                "type": "number",
                "correct_answer": "1",
                "target_concept": "one_to_one_word",
            },
            {
                "prompt": "Count the words in 'the sun is hot' by touching each one.",
                "type": "open_response",
                "rubric": "Mastery: touches and counts 4 words correctly. Proficient: counts 4 with a pause or recount. Developing: miscounts without help.",
                "target_concept": "word_counting",
            },
        ],
        "resource_guidance": {
            "required": ["short memorized lines in large print (a known rhyme or sentence)"],
            "recommended": ["word cards with clear spaces", "a pointer for one-to-one touching"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Use very short, fully memorized lines and exaggerate the spaces; over-practice one-to-one pointing slowly.",
            "adhd": "Use lively, short rhymes and let the child stand and point big; keep each round quick.",
            "gifted": "Move to longer lines and to finding a specific word by its position ('point to the fourth word').",
            "visual_learner": "Highlight the spaces or put each word on a separate card so the boundaries are obvious.",
            "kinesthetic_learner": "Use physical word cards the child slides apart to see spaces, and big pointing motions.",
            "auditory_learner": "Say each word with a clear beat and have the child touch on the beat so sound and print line up.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "A spoken word matches one written word, and spaces separate the words. Today we point to each word as we say it and count the words in a line.",
                "gradual_release": {
                    "i_do": "Read a short memorized line slowly, touching one word for each word I say, and point out the spaces between words. Stop and say, 'My finger is on this word.'",
                    "we_do": "Say the line together while the child and I point to each word, one touch per spoken word, and count the words together by touching each.",
                    "you_do": "Child says a known line and touches one word for each word, shows a space between two words, and counts the words in the line.",
                },
                "guided_practice": [
                    "Point-and-say a known rhyme line together, one touch per word",
                    "Rebuild a cut-up sentence from word cards with clear spaces",
                ],
                "independent_practice": [
                    "The child points to each word of a memorized line alone",
                    "The child counts the words in several short printed lines",
                ],
                "mastery_check": [
                    "Touches one word per spoken word in a short line",
                    "Identifies spaces as word boundaries",
                    "Counts the words in a short line correctly",
                ],
                "spiral_review": [
                    "Begin by re-tracking a line left to right and doing the return sweep from rf-27, then add the one-touch-per-word matching, since voice-to-print matching rides on top of steady directional tracking",
                ],
            },
            "classical": {
                "narrative_introduction": "Speech is made of words, and on the page each word stands alone between two spaces. The grammar stage trains the eye and voice to march together, one spoken word to one written word.",
                "memory_work": {
                    "chants": [
                        "Chant a known line, one clear beat per word, touching each word in time",
                        "Chant 'one word, one space, one word' while sliding between word cards",
                    ],
                    "recitations": [
                        "Recite a memorized rhyme and then point to its printed words one by one to match voice to print",
                    ],
                },
                "recitation_routine": "Start with a rhyme already known by heart, recite it, then match the spoken words to the printed words one to one before any new line is added.",
                "history_integration": "Spacing between words is itself an old invention that made reading easier; the child uses that inheritance to tell one word from the next.",
                "read_aloud_suggestions": [
                    "A short, well-known verse in large print, recited and then matched word for word to its printed form",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A loved short poem or rhyme in clear, large print with generous spaces between words",
                ],
                "short_lesson_flow": "Say a treasured short rhyme together, then gently point to each word as you say it, noticing the little spaces that keep the words apart. Count the words once, lightly, and stop.",
                "narration_prompt": "Point to the words as you say our rhyme, and show me what keeps the words apart.",
                "real_world_objects": [
                    "A short caption under a beautiful picture, pointed to word by word",
                    "The child's name and a family member's name, each word touched",
                ],
                "nature_connection": "Match the spoken words of a short nature couplet to its printed words while looking at the real thing it names.",
                "habit_focus": "The habit of careful attention: making the voice and the pointing finger keep exact company.",
            },
            "montessori": {
                "prepared_materials": [
                    "Word cards for a short known sentence, with clear gaps when laid out",
                    "A sentence strip of a memorized line in large print",
                    "A pointer sized to the child's hand",
                ],
                "presentation": {
                    "three_period_lesson": "Naming: 'This is one word. Here is the space. This is the next word.' Recognition: 'Show me one word. Show me a space.' Recall: 'How many words are here?'",
                    "steps": [
                        "Lay out a known sentence in word cards with spaces and read it touching each word",
                        "Show that the spaces separate the words",
                        "Invite the child to point to each word while saying the line, then count the words",
                    ],
                },
                "control_of_error": "With word cards for a memorized line, a missed or doubled touch makes the saying and pointing fall out of step, which the child notices and self-corrects.",
                "abstraction_pathway": "From handling separate word cards, to seeing the printed line as a row of distinct words marked off by spaces, preparing the letter-word-sentence distinctions that follow.",
                "extensions": [
                    "Build and read longer known sentences from word cards",
                    "Find and point to a named word by its position in the line",
                ],
                "observation_focus": "Watch whether the child keeps one-to-one matching, treats spaces as boundaries, and counts words accurately without prompting.",
            },
            "unschooling": {
                "invitations": [
                    "Point to each word when you read short, loved lines together",
                    "Leave out word cards of a favorite rhyme to arrange and read",
                    "Notice and point to the separate words on signs, labels, and notes in daily life",
                ],
                "real_world_contexts": [
                    "Pointing to each word of a birthday-card message",
                    "Reading a short label or caption word by word",
                    "Counting the words on a short sign together",
                ],
                "conversation_starters": [
                    "Can you point to each word while we say it?",
                    "What keeps these words from bumping into each other?",
                    "How many words do you think are in this little line?",
                ],
                "resource_bank": [
                    "Favorite rhymes and short messages in large print",
                    "Word cards for a few loved lines",
                    "Everyday print with clear word spaces",
                ],
                "parent_role": "Point to words as you share real text, invite the child to match and count when curious, and answer genuine questions about words and spaces without turning it into drill.",
                "observation_documentation": "Over time, notice whether the child matches spoken to written words and sees spaces as boundaries during real reading together; that is the record.",
            },
        },
        "connections": {
            "math": "One spoken word to one written word is the same one-to-one correspondence used to count objects, and counting words uses counting directly",
            "science": "Matching a spoken label to its printed word when naming parts of a diagram",
            "history": "Spacing words apart is an invention that made written records easier to read",
        },
    },
    "rf-29": {
        "enriched": True,
        "learning_objectives": [
            "Distinguish a letter from a word from a sentence in print",
            "Locate the first letter and the last letter of a written word",
            "Explain that letters make words and words make sentences",
            "Point to a single letter, a single word, and a whole sentence on request",
        ],
        "teaching_guidance": {
            "introduction": "This node sorts out the units of print: letters are the small marks, a word is a group of letters with spaces around it, and a sentence is a group of words that ends with a punctuation mark. The child also finds the first and last letter of a word. It builds on knowing that spaces separate words.",
            "scaffolding_sequence": [
                "Point to a single letter, then a whole word, then a whole sentence, naming each",
                "Show that letters sit together with no spaces to make one word",
                "Show that words with spaces between them make a sentence",
                "Find the first letter (far left) and the last letter (far right) of a word",
                "Have the child point to a letter, a word, and a sentence on request",
            ],
            "socratic_questions": [
                "Is this a letter, a word, or a sentence? How can you tell?",
                "Where is the first letter of this word? Where is the last?",
                "What do letters make? What do words make?",
            ],
            "practice_activities": [
                "Letter-word-sentence sort with cards or a highlighter",
                "First-and-last letter hunt in printed words",
                "Frame it: use fingers or a card window to frame one letter, then one word, then a sentence",
            ],
            "real_world_connections": [
                "Finding the first letter of one's own name",
                "Spotting a single word on a sign versus a whole sentence",
                "Pointing to the letters in a logo",
            ],
            "common_misconceptions": [
                "Calling a single letter a word: show that a word usually has letters grouped with spaces around it",
                "Confusing the first and last letter: anchor first = far left, last = far right",
                "Thinking a sentence is just one long word: show the spaces that break it into words",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Correctly points to a letter, a word, and a sentence on request",
                "Locates the first and last letter of a given word",
                "Explains that letters make words and words make sentences",
            ],
            "assessment_methods": [
                "point-on-request observation",
                "first/last letter demonstration",
                "oral explanation",
            ],
            "sample_assessment_prompts": [
                "Point to one letter, then one word, then a whole sentence",
                "Show me the first letter and the last letter of this word",
                "What do letters build? What do words build?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Is the mark 'b' a letter or a word?",
                "expected_type": "text",
                "correct_answer": "a letter",
                "hints": ["A single mark by itself is one of these"],
                "explanation": "'b' is a single letter.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Is 'dog' a letter, a word, or a sentence?",
                "expected_type": "text",
                "correct_answer": "a word",
                "hints": ["It is a group of letters with spaces around it"],
                "explanation": "'dog' is a word: letters grouped together with spaces around it.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is the first letter of the word 'cat'?",
                "expected_type": "text",
                "correct_answer": "c",
                "hints": ["The letter on the far left"],
                "explanation": "The first letter of 'cat' is 'c' (far left).",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is the last letter of the word 'sun'?",
                "expected_type": "text",
                "correct_answer": "n",
                "hints": ["The letter on the far right"],
                "explanation": "The last letter of 'sun' is 'n' (far right).",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "How many letters are in the word 'fish'?",
                "expected_type": "number",
                "correct_answer": "4",
                "hints": ["Count each letter: f-i-s-h"],
                "explanation": "'fish' has 4 letters: f, i, s, h.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Letters group together to make a ____.",
                "expected_type": "text",
                "correct_answer": "word",
                "hints": ["What do a few letters with spaces around them make?"],
                "explanation": "Letters group together to make a word.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Look at 'The cat naps.' Is this a word or a sentence, and how can you tell?",
                "expected_type": "text",
                "correct_answer": "a sentence; it is several words with spaces and ends with a punctuation mark",
                "hints": ["Count the words; does it end with a mark?"],
                "explanation": "It is a sentence: more than one word, separated by spaces, ending with a period.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Pick any printed word and show me its first letter and its last letter. Tell me how you know which is which.",
                "expected_type": "text",
                "hints": ["First = far left, last = far right"],
                "explanation": "No single right answer; the child should point to the far-left letter as first and the far-right letter as last and explain by position.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Point to one letter, then one word, then a whole sentence.",
                "type": "open_response",
                "rubric": "Mastery: identifies all three units correctly. Proficient: identifies two correctly. Developing: identifies one with help.",
                "target_concept": "letter_word_sentence",
            },
            {
                "prompt": "Show me the first letter and the last letter of this word.",
                "type": "open_response",
                "rubric": "Mastery: points to first (far left) and last (far right) correctly. Proficient: gets one and self-corrects the other. Developing: needs help with position.",
                "target_concept": "first_and_last_letter",
            },
            {
                "prompt": "Is 's' a letter or a word?",
                "type": "text",
                "correct_answer": "a letter",
                "target_concept": "letter_vs_word",
            },
            {
                "prompt": "How many letters are in 'hat'?",
                "type": "number",
                "correct_answer": "3",
                "target_concept": "letters_in_a_word",
            },
            {
                "prompt": "Tell me what letters make and what words make.",
                "type": "open_response",
                "rubric": "Mastery: says letters make words and words make sentences. Proficient: states one relationship. Developing: needs prompting for either.",
                "target_concept": "units_of_print",
            },
        ],
        "resource_guidance": {
            "required": ["printed words and short sentences in large print"],
            "recommended": ["a highlighter or framing card", "letter tiles and word cards"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Use a framing window to isolate one unit at a time; keep first/last-letter work slow and consistent with left/right cues.",
            "adhd": "Make it a fast hunt ('find me a letter, now a word, now a sentence') with movement between finds.",
            "gifted": "Add counting letters in longer words and finding the middle letter, and identifying where a sentence ends.",
            "visual_learner": "Color-code: highlight letters one color and word boundaries another so the units stand out.",
            "kinesthetic_learner": "Build words from letter tiles and lay word cards into a sentence so units are handled physically.",
            "auditory_learner": "Say 'letter, word, sentence' aloud as each is framed so the names attach to the units by ear.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Letters are the small marks; a word is a group of letters with spaces around it; a sentence is a group of words that ends with a mark. Today we tell them apart and find a word's first and last letter.",
                "gradual_release": {
                    "i_do": "Point to a single letter and name it 'letter', then a whole word 'word', then a sentence 'sentence'. Show the first letter (far left) and last letter (far right) of a word, naming each.",
                    "we_do": "Together, point to a letter, a word, and a sentence on the page; together find the first and last letters of two or three words.",
                    "you_do": "Child points to a letter, a word, and a sentence on request and finds the first and last letter of given words.",
                },
                "guided_practice": [
                    "Sort cards into letter, word, and sentence piles together",
                    "First-and-last-letter hunt across several words",
                ],
                "independent_practice": [
                    "The child frames a letter, a word, and a sentence on a page alone",
                    "The child marks the first and last letters of words in a short line",
                ],
                "mastery_check": [
                    "Distinguishes letter, word, and sentence on request",
                    "Locates first and last letter of a word",
                    "States that letters make words and words make sentences",
                ],
                "spiral_review": [
                    "Warm up with the spaces-and-word-counting work from rf-28 (one touch per word, spaces separate words) before sorting letters from words, since the word unit is defined by the spaces learned there",
                ],
            },
            "classical": {
                "narrative_introduction": "Print is built in steps: letters into words, words into sentences. The grammar stage names these parts exactly, the small letter, the whole word, the complete sentence, so the orders of print are known and sure.",
                "memory_work": {
                    "chants": [
                        "Chant 'letters make words, words make sentences' while pointing to each unit",
                        "Chant 'first letter, last letter' while touching the far-left and far-right letters of a word",
                    ],
                    "recitations": [
                        "Recite the alphabet, then point to single letters in print, to join the named letters to the marks on the page",
                    ],
                },
                "recitation_routine": "Open by reciting the letter names known by heart, then identify a letter, a word, and a sentence in a familiar text before new work.",
                "history_integration": "The idea of building words from a small set of letters is an ancient and powerful invention; the child learns to see those building blocks.",
                "read_aloud_suggestions": [
                    "A short, well-known passage in large print used to point out single letters, whole words, and complete sentences",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A clearly printed, loved short text where single letters, words, and a sentence can be pointed to easily",
                ],
                "short_lesson_flow": "Enjoy a short, known line together, then gently notice its parts: here is one letter, here is a whole word, here is the whole sentence. Find the first and last letter of one word, and stop.",
                "narration_prompt": "Show me one letter, one word, and the whole sentence, and tell me how they are different.",
                "real_world_objects": [
                    "The child's printed name: its first letter, its whole word",
                    "A short sign read for its letters, words, and the sentence",
                ],
                "nature_connection": "On a labelled nature card, point to a single letter, the whole word for the plant or animal, and the caption sentence, while looking at the real thing.",
                "habit_focus": "The habit of careful distinction: seeing exactly what kind of unit one is looking at.",
            },
            "montessori": {
                "prepared_materials": [
                    "Movable letter tiles, word cards, and a sentence strip",
                    "A framing window to isolate a letter, a word, or a sentence",
                    "Large, clear print samples",
                ],
                "presentation": {
                    "three_period_lesson": "Naming: 'This is a letter. This is a word. This is a sentence.' Recognition: 'Show me a letter. Show me a word.' Recall: 'What is this, a letter, a word, or a sentence?'",
                    "steps": [
                        "Show a single letter tile, then build a word from tiles, then lay words into a sentence",
                        "Name each unit as it is shown",
                        "Find the first and last letters of a built word, then invite the child to do the same",
                    ],
                },
                "control_of_error": "Building up from tiles to words to a sentence makes each unit concrete, and a misnamed unit stands out against the built materials, so the child can self-correct by looking.",
                "abstraction_pathway": "From handling tiles and cards, to recognizing letters, words, and sentences in ordinary print, readying the child for letter-sound work.",
                "extensions": [
                    "Count letters in longer words and find the middle letter",
                    "Identify where one sentence ends and the next begins",
                ],
                "observation_focus": "Watch whether the child reliably distinguishes the units and finds first and last letters by position, without prompting.",
            },
            "unschooling": {
                "invitations": [
                    "Notice letters, words, and sentences naturally in the print around you",
                    "Leave out letter tiles and word cards to build with",
                    "Point out the first letter of the child's name and favorite words when it comes up",
                ],
                "real_world_contexts": [
                    "Finding the first letter of names on the family calendar",
                    "Spotting a one-word sign versus a full-sentence one",
                    "Letters in logos and on packaging",
                ],
                "conversation_starters": [
                    "Is that a letter or a whole word?",
                    "What letter does this word start with? What letter ends it?",
                    "How many words are in that little sentence?",
                ],
                "resource_bank": [
                    "Letter tiles, word cards, and everyday print",
                    "The child's name and family names in print",
                    "Favorite books and signs",
                ],
                "parent_role": "Point out letters, words, and sentences as they come up in real life, answer the child's genuine questions about first and last letters, and let the distinctions grow through use rather than drill.",
                "observation_documentation": "Over time, notice whether the child tells letters from words from sentences and finds first and last letters during ordinary reading; that noticing is the assessment.",
            },
        },
        "connections": {
            "math": "Letters build words and words build sentences, the same part-to-whole idea as ones building tens and tens building hundreds",
            "science": "Naming the parts of something and how smaller parts make a larger whole",
            "history": "An alphabet of a few letters can build every word, a powerful idea in the history of writing",
        },
    },
    "rf-30": {
        "enriched": True,
        "learning_objectives": [
            "Recognize a period, a question mark, and an exclamation point in print",
            "Explain that end punctuation shows where a sentence stops",
            "Match each end mark to how the sentence sounds (telling, asking, or excited)",
            "Find the end punctuation that marks the end of a sentence on a page",
        ],
        "teaching_guidance": {
            "introduction": "End punctuation marks show where a sentence ends and hint at how it sounds: a period for a telling sentence, a question mark for an asking sentence, an exclamation point for an excited or loud one. This is recognition in print, building on knowing what a sentence is; it is not yet about writing them.",
            "scaffolding_sequence": [
                "Show a period and say it ends a telling sentence with a small stop",
                "Show a question mark and say it ends an asking sentence (voice goes up)",
                "Show an exclamation point and say it ends an excited or loud sentence",
                "Read sentences aloud so the child hears how each end mark changes the voice",
                "Have the child find and name the end mark at the end of a sentence",
            ],
            "socratic_questions": [
                "What does this mark at the end of the sentence tell us to do?",
                "Which mark shows the sentence is a question?",
                "How should your voice sound when a sentence ends with an exclamation point?",
            ],
            "practice_activities": [
                "End-mark match: pair a telling, asking, and excited sentence to its mark",
                "Read-it-right: read a sentence with the feeling its end mark shows",
                "Mark hunt: find every period, question mark, and exclamation point on a page",
            ],
            "real_world_connections": [
                "Spotting a question mark on a sign that asks something",
                "Hearing an excited exclamation in a favorite story",
                "Noticing periods at the ends of sentences in a picture book",
            ],
            "common_misconceptions": [
                "Ignoring end marks and reading everything flat: model how the voice changes for each mark",
                "Confusing the question mark and exclamation point: contrast asking (voice up) with excited (voice strong)",
                "Thinking the mark is just decoration: show it signals the end and the tone of the sentence",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Names the period, question mark, and exclamation point on sight",
                "Explains that end punctuation marks the end of a sentence",
                "Matches each end mark to a telling, asking, or excited sentence",
            ],
            "assessment_methods": [
                "mark-naming on sight",
                "oral matching of mark to sentence type",
                "find-the-end-mark demonstration",
            ],
            "sample_assessment_prompts": [
                "Name this mark and tell me what it does",
                "Which mark ends a question?",
                "Find the end mark of this sentence and tell me how it should sound",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is the name of the mark '.' at the end of a sentence?",
                "expected_type": "text",
                "correct_answer": "a period",
                "hints": ["It is a small dot that ends a telling sentence"],
                "explanation": "'.' is a period; it ends a telling sentence.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which mark ends a question, '.' or '?'",
                "expected_type": "text",
                "correct_answer": "?",
                "hints": ["A question is when we ask something"],
                "explanation": "A question mark '?' ends an asking sentence.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What does an end mark show about a sentence?",
                "expected_type": "text",
                "correct_answer": "that the sentence is ending (it stops there)",
                "hints": ["Think about where it sits in the sentence"],
                "explanation": "An end mark shows where the sentence stops.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "The sentence 'Are you coming?' ends with which mark?",
                "expected_type": "text",
                "correct_answer": "a question mark",
                "hints": ["It is asking something"],
                "explanation": "It is a question, so it ends with a question mark '?'.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "The sentence 'Watch out!' ends with which mark?",
                "expected_type": "text",
                "correct_answer": "an exclamation point",
                "hints": ["It is said loudly or with excitement"],
                "explanation": "It is excited or loud, so it ends with an exclamation point '!'.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "How many end marks are in this line: 'I see it. Do you?'",
                "expected_type": "number",
                "correct_answer": "2",
                "hints": ["Count the marks that end each sentence: . and ?"],
                "explanation": "There are 2 end marks: a period and a question mark, so there are two sentences.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Read 'The dog ran fast!' the way the end mark tells you to. How should your voice sound, and why?",
                "expected_type": "text",
                "correct_answer": "strong or excited, because it ends with an exclamation point",
                "hints": ["What mark is at the end?"],
                "explanation": "The exclamation point means read it with excitement or strength.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Find an end mark on this page, name it, and tell me how that sentence should sound.",
                "expected_type": "text",
                "hints": ["Period = telling, question mark = asking, exclamation point = excited"],
                "explanation": "No single right answer; the child should locate an end mark, name it, and match it to telling, asking, or excited reading.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Name this mark and tell me what it does.",
                "type": "open_response",
                "rubric": "Mastery: names the mark and says it ends a sentence (with its tone). Proficient: names the mark with a partial role. Developing: needs help to name or explain.",
                "target_concept": "end_punctuation_naming",
            },
            {
                "prompt": "Match each sentence to its end mark: a telling sentence, an asking sentence, an excited sentence.",
                "type": "open_response",
                "rubric": "Mastery: matches all three (period, question mark, exclamation point). Proficient: matches two. Developing: matches one with help.",
                "target_concept": "mark_to_sentence_type",
            },
            {
                "prompt": "Which mark ends a question?",
                "type": "text",
                "correct_answer": "a question mark",
                "target_concept": "question_mark",
            },
            {
                "prompt": "How many sentences are in 'Stop! Look both ways.' (count the end marks)?",
                "type": "number",
                "correct_answer": "2",
                "target_concept": "end_marks_count_sentences",
            },
            {
                "prompt": "Find the end mark of this sentence and read the sentence the way it should sound.",
                "type": "open_response",
                "rubric": "Mastery: finds the mark and reads with matching tone. Proficient: finds the mark, tone partly matches. Developing: needs help to find or match.",
                "target_concept": "reading_with_end_punctuation",
            },
        ],
        "resource_guidance": {
            "required": ["short sentences in large print showing periods, question marks, and exclamation points"],
            "recommended": ["end-mark cards (. ? !)", "a favorite picture book with varied punctuation"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Keep sentences very short; pair each mark with a consistent gesture and voice so the mark's job is multisensory.",
            "adhd": "Make it dramatic: act out telling, asking, and excited voices, standing for the excited one.",
            "gifted": "Add reading short dialogue with mixed marks and explaining why an author chose each mark.",
            "visual_learner": "Use large, color-coded marks (. ? !) and a face icon for each tone (calm, curious, excited).",
            "kinesthetic_learner": "Assign a movement to each mark (a small stop, a shrug for a question, a jump for excitement).",
            "auditory_learner": "Read the same words with each end mark so the child hears how the voice changes; this is a strength area.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Sentences end with a mark: a period for telling, a question mark for asking, an exclamation point for excitement. Today we name these marks and hear how each one changes the voice.",
                "gradual_release": {
                    "i_do": "Point to a period and read a telling sentence with a small stop. Point to a question mark and read an asking sentence with the voice going up. Point to an exclamation point and read an excited sentence strongly. Name each mark.",
                    "we_do": "Read three short sentences together, naming each end mark and reading it with the right voice; match a set of sentences to their marks together.",
                    "you_do": "Child names the period, question mark, and exclamation point, finds the end mark of a sentence, and reads the sentence with the matching voice.",
                },
                "guided_practice": [
                    "End-mark match: pair telling, asking, and excited sentences with . ? !",
                    "Read-it-right rounds: read sentences with the voice their end mark shows",
                ],
                "independent_practice": [
                    "The child hunts a page for periods, question marks, and exclamation points and names each",
                    "The child reads short sentences aloud, matching the voice to the end mark",
                ],
                "mastery_check": [
                    "Names all three end marks on sight",
                    "Matches each mark to telling, asking, or excited",
                    "Finds the end mark that ends a sentence",
                ],
                "spiral_review": [
                    "Begin by reviewing what a sentence is from rf-29 (a group of words, several words with spaces) before adding the marks that end a sentence, since end punctuation only makes sense once the sentence unit is clear",
                ],
            },
            "classical": {
                "narrative_introduction": "Every sentence comes to a clear end, and a small mark tells how it ends: a quiet stop, a question, or a cry. The grammar stage learns to name these marks and to read them aloud with the right voice.",
                "memory_work": {
                    "chants": [
                        "Chant 'period stops, question asks, exclamation shouts' while showing each mark",
                        "Chant the three marks by name in order while pointing to them",
                    ],
                    "recitations": [
                        "Recite a short, known passage and find its end marks, reading each sentence with the voice its mark calls for",
                    ],
                },
                "recitation_routine": "Begin with a memorized line, read it aloud honoring its end mark, and name the mark, before meeting any new sentence.",
                "history_integration": "Punctuation marks were added to writing over time to guide the reader's voice; the child learns these old, useful signs.",
                "read_aloud_suggestions": [
                    "A lively short text with telling, asking, and exclaiming sentences, read aloud so each end mark is heard",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A loved picture book whose sentences naturally tell, ask, and exclaim, with clear end marks",
                ],
                "short_lesson_flow": "Read a short, delightful passage together, then notice the marks at the ends of sentences: this one tells, this one asks, this one is excited. Read each in its own voice, lightly, and stop.",
                "narration_prompt": "Find an end mark and tell me whether the sentence is telling, asking, or excited.",
                "real_world_objects": [
                    "A short note that asks a question, read with a rising voice",
                    "A sign that exclaims, read with excitement",
                ],
                "nature_connection": "Read aloud a short nature poem with an exclaiming or questioning line outdoors, letting the end mark shape the voice while looking at what is described.",
                "habit_focus": "The habit of reading with meaning: letting the punctuation guide an honest, expressive voice.",
            },
            "montessori": {
                "prepared_materials": [
                    "Cards showing a period, a question mark, and an exclamation point",
                    "Short sentence strips of telling, asking, and exclaiming sentences",
                    "A calm space for reading aloud",
                ],
                "presentation": {
                    "three_period_lesson": "Naming: 'This is a period. This is a question mark. This is an exclamation point.' Recognition: 'Show me the question mark.' Recall: 'What is this mark, and what does it do?'",
                    "steps": [
                        "Show each end mark and read a matching sentence with the right voice",
                        "Match sentence strips to their end-mark cards",
                        "Invite the child to find end marks and read the sentences with matching voice",
                    ],
                },
                "control_of_error": "Reading a question as a flat statement or an exclamation as a whisper sounds plainly wrong against the sentence's meaning, so the child hears the mismatch and adjusts.",
                "abstraction_pathway": "From matching concrete mark cards to sentences, toward reading any text with the phrasing and tone its punctuation signals.",
                "extensions": [
                    "Read short dialogue with mixed end marks",
                    "Sort a set of sentences by their end mark",
                ],
                "observation_focus": "Watch whether the child names the marks, finds them at sentence ends, and lets each mark shape the voice without prompting.",
            },
            "unschooling": {
                "invitations": [
                    "Read aloud with full, honest expression so end marks are heard in real stories",
                    "Notice question marks and exclamation points on signs, comics, and packaging",
                    "Play with reading the same sentence as a telling, a question, and an exclamation",
                ],
                "real_world_contexts": [
                    "A comic's excited 'Wow!' read with energy",
                    "A sign that asks a question, read with a rising voice",
                    "Periods ending the sentences of a bedtime story",
                ],
                "conversation_starters": [
                    "What is that mark at the end? What does it tell our voice to do?",
                    "Is this sentence telling us something or asking us something?",
                    "How would this sound with an exclamation point?",
                ],
                "resource_bank": [
                    "Favorite read-alouds, comics, and signs with varied punctuation",
                    "End-mark cards kept around for play",
                    "Everyday print that asks and exclaims",
                ],
                "parent_role": "Read expressively in daily life so end marks come alive, answer the child's real questions about the marks, and let recognition grow through enjoyed reading rather than drill.",
                "observation_documentation": "Over time, notice whether the child recognizes the end marks and lets them shape the voice during shared reading; that noticing is the record.",
            },
        },
        "connections": {
            "math": "An end mark closes a sentence the way an equals sign closes a number sentence: a signal that it is complete",
            "science": "A question mark fits the questions we ask in science before investigating",
            "history": "Punctuation was developed over time to help readers; it is part of the story of writing",
        },
    },
    "rf-31": {
        "enriched": True,
        "learning_objectives": [
            "Decide whether two spoken words rhyme by listening to their ending sounds",
            "Choose which of several spoken words rhymes with a given word",
            "Explain that rhyming words end with the same sound",
            "Notice rhyming words in songs, poems, and nursery rhymes heard aloud",
        ],
        "teaching_guidance": {
            "introduction": "Rhyming is the first step of phonological awareness and is entirely about LISTENING: two words rhyme when they end with the same sound, like cat and hat. There are no letters here at all; the child works with spoken words, songs, and rhymes by ear.",
            "scaffolding_sequence": [
                "Say two clearly rhyming words slowly (cat, hat) and stretch the matching end sound",
                "Ask whether two spoken words rhyme, starting with obvious pairs",
                "Mix in non-rhyming pairs (cat, dog) so the child must really listen",
                "Offer a choice: which of these rhymes with 'bell', shell or fish?",
                "Listen for rhymes in a familiar nursery rhyme said aloud together",
            ],
            "socratic_questions": [
                "Do these two words end with the same sound?",
                "Which word sounds like it belongs with 'cat' at the end?",
                "What part of the word do we listen to when we check for rhyme?",
            ],
            "practice_activities": [
                "Thumbs up / thumbs down: thumbs up only when a spoken pair rhymes",
                "Rhyme pick: choose the rhyming word from two or three spoken choices",
                "Rhyme hunt in a sung nursery rhyme: catch the words that rhyme",
            ],
            "real_world_connections": [
                "Catching the rhymes in a favorite song",
                "Hearing rhymes in bedtime nursery rhymes",
                "Noticing two names that happen to rhyme",
            ],
            "common_misconceptions": [
                "Matching beginning sounds instead of ending sounds: redirect attention to how the word ends",
                "Thinking words that look alike must rhyme: this is by ear, not by spelling, so keep it oral",
                "Calling words that share a middle sound rhymes: stretch the ending sound to compare",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Reliably judges whether two spoken words rhyme",
                "Picks the rhyming word from spoken choices",
                "Says that rhyming words end with the same sound",
            ],
            "assessment_methods": [
                "oral rhyme judgment",
                "rhyme-choice game",
                "listening for rhyme in a recited rhyme",
            ],
            "sample_assessment_prompts": [
                "Do 'pig' and 'wig' rhyme?",
                "Which rhymes with 'star', car or sun?",
                "Tell me two words from our rhyme that rhymed",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Do 'cat' and 'hat' rhyme? (Listen to the ending sound.)",
                "expected_type": "text",
                "correct_answer": "yes",
                "hints": ["Both end with the /at/ sound"],
                "explanation": "Yes, cat and hat rhyme because they both end with the /at/ sound.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Do 'dog' and 'log' rhyme?",
                "expected_type": "text",
                "correct_answer": "yes",
                "hints": ["Listen to the end: /og/ and /og/"],
                "explanation": "Yes, dog and log rhyme; they both end with the /og/ sound.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Do 'sun' and 'cup' rhyme?",
                "expected_type": "text",
                "correct_answer": "no",
                "hints": ["Do they end with the same sound?"],
                "explanation": "No, sun ends with /un/ and cup ends with /up/, so they do not rhyme.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Which word rhymes with 'bell', 'shell' or 'fish'?",
                "expected_type": "text",
                "correct_answer": "shell",
                "hints": ["Which one ends with /ell/?"],
                "explanation": "'shell' rhymes with 'bell' because both end with the /ell/ sound.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Which word rhymes with 'cake', 'lake' or 'milk'?",
                "expected_type": "text",
                "correct_answer": "lake",
                "hints": ["Listen for the /ake/ ending"],
                "explanation": "'lake' rhymes with 'cake'; both end with /ake/.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "How many of these rhyme with 'cat': hat, sit, bat?",
                "expected_type": "number",
                "correct_answer": "2",
                "hints": ["Check each one's ending sound against /at/"],
                "explanation": "hat and bat rhyme with cat (both /at/); sit does not. So 2 rhyme.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Your friend says 'cat' and 'car' rhyme because they both start with /c/. Are they right? Why or why not?",
                "expected_type": "text",
                "correct_answer": "no; rhyme is about the ending sound, and cat ends /at/ while car ends /ar/",
                "hints": ["Which part of the word makes a rhyme, the start or the end?"],
                "explanation": "They are wrong: rhyme depends on the ending sound, not the beginning. cat (/at/) and car (/ar/) end differently.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Listen to a short nursery rhyme with me, then tell me two words in it that rhymed.",
                "expected_type": "text",
                "hints": ["Listen for two words that end with the same sound"],
                "explanation": "No single right answer; the child should name two words from the rhyme that share an ending sound (for example, 'wall' and 'fall').",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Do 'pig' and 'wig' rhyme?",
                "type": "text",
                "correct_answer": "yes",
                "target_concept": "rhyme_judgment",
            },
            {
                "prompt": "Which word rhymes with 'star', 'car' or 'sun'?",
                "type": "text",
                "correct_answer": "car",
                "target_concept": "rhyme_choice",
            },
            {
                "prompt": "Tell me what makes two words rhyme.",
                "type": "open_response",
                "rubric": "Mastery: says they end with the same sound. Proficient: gestures at the ending sound with help. Developing: confuses with beginning sounds.",
                "target_concept": "rhyme_concept",
            },
            {
                "prompt": "Listen to this rhyme and tell me two words that rhymed.",
                "type": "open_response",
                "rubric": "Mastery: names a correct rhyming pair from the rhyme. Proficient: names one rhyming word and finds its partner with a hint. Developing: needs the pair pointed out.",
                "target_concept": "rhyme_in_context",
            },
            {
                "prompt": "Out of 'top', 'mop', and 'cup', how many rhyme with 'hop'?",
                "type": "number",
                "correct_answer": "2",
                "target_concept": "rhyme_judgment",
            },
        ],
        "resource_guidance": {
            "required": ["no materials needed: this is purely oral listening work"],
            "recommended": ["a treasury of nursery rhymes", "favorite rhyming songs and picture books read aloud"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 10},
        "accommodations": {
            "dyslexia": "Rhyme can be hard; over-model with many obvious pairs, stretch the ending sound, and keep it playful and slow.",
            "adhd": "Use quick, active rhyme games with thumbs up/down and movement; keep rounds short and lively.",
            "gifted": "Move to picking a rhyme from several choices and to generating rhymes, and to longer rhyming strings.",
            "visual_learner": "Pair each spoken word with a simple picture so the child can hold the words in mind while listening for the rhyme.",
            "kinesthetic_learner": "Jump or clap on the matching end sound; act out rhyming pairs.",
            "auditory_learner": "This is a strength area: lean on songs, chants, and recited rhymes.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Two words rhyme when they end with the same sound, like cat and hat. This is all by ear, with no letters. Today we listen to pairs of words and decide whether they rhyme, and we pick the word that rhymes.",
                "gradual_release": {
                    "i_do": "Say 'cat, hat' slowly, stretching the /at/ ending, and say, 'These rhyme, they end the same.' Then say 'cat, dog' and say, 'These do not rhyme, they end differently.'",
                    "we_do": "Judge several spoken pairs together with thumbs up for rhyme and thumbs down for no rhyme, saying the ending sounds aloud together.",
                    "you_do": "Child decides whether spoken pairs rhyme and picks which of two or three spoken words rhymes with a given word, all by listening.",
                },
                "guided_practice": [
                    "Thumbs up / thumbs down on spoken pairs together",
                    "Rhyme pick from two spoken choices together",
                ],
                "independent_practice": [
                    "The child judges a set of spoken pairs alone",
                    "The child catches rhyming words in a recited nursery rhyme",
                ],
                "mastery_check": [
                    "Judges spoken rhyme pairs reliably",
                    "Picks the rhyming word from spoken choices",
                    "States that rhyming words end with the same sound",
                ],
                "spiral_review": [
                    "Warm up with attentive listening from rf-21 (listening closely to spoken language) before judging rhymes, since hearing the ending sounds of words depends on that careful listening",
                ],
            },
            "classical": {
                "narrative_introduction": "The ear can be trained to catch the music of words, and rhyme is its first lesson: words that chime together at the end. The grammar stage feeds the ear on rhyme through chant and recitation, all aloud.",
                "memory_work": {
                    "chants": [
                        "Chant strings of rhyming words in a steady beat: cat, hat, bat, mat, sat",
                        "Chant a known rhyming couplet, leaning on the matching end sounds",
                    ],
                    "recitations": [
                        "Memorize and recite nursery rhymes daily for their true rhyme and rhythm",
                        "Recite a short rhyming poem and name its rhyming words aloud",
                    ],
                },
                "recitation_routine": "Begin each lesson by reciting a known rhyme and naming its rhyming words before adding new rhyme work; the ear's training is cumulative.",
                "history_integration": "Rhymes are an old inheritance, passed by ear from one generation of children to the next; learning them joins the child to that long oral tradition.",
                "read_aloud_suggestions": [
                    "A well-made collection of rhyming children's poetry, read aloud with relish so the ear is fed on rhyme",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A treasury of traditional nursery rhymes and a book of strongly rhyming children's poetry",
                ],
                "short_lesson_flow": "Say a beloved nursery rhyme together and delight in it. Then play gently with its rhymes: catch the two words that chime at the end, and try another pair. Stop while the child is still enjoying it.",
                "narration_prompt": "Tell me the words in our rhyme that sounded the same at the end.",
                "real_world_objects": [
                    "The names of family members or pets that happen to rhyme",
                    "Familiar objects whose names rhyme, said aloud",
                ],
                "nature_connection": "On a walk, make up a little rhyme about something seen (a 'log' by the 'fog'), enjoying the chime aloud.",
                "habit_focus": "The habit of attentive, delighted listening to the music and rhyme of words.",
            },
            "montessori": {
                "prepared_materials": [
                    "A basket of small objects or pictures whose names rhyme (cat, hat, bat)",
                    "A quiet space for listening games",
                    "No letters: rhyme games stay purely oral and precede letter work",
                ],
                "presentation": {
                    "three_period_lesson": "Adapted for sound. Naming: 'cat and hat rhyme, they end the same.' Recognition: 'Which one rhymes with cat?' Recall: 'Do these two rhyme?' All spoken, never letters.",
                    "steps": [
                        "Begin with clearly rhyming object names said aloud",
                        "Add a non-rhyming name so the child must listen",
                        "Offer a choice of names and ask which rhymes with the target",
                    ],
                },
                "control_of_error": "The shared listening is the control: the guide says the words clearly and the endings either chime or do not, which the child hears for themselves. The guide keeps it light.",
                "abstraction_pathway": "From enjoying whole rhymes, to hearing that rhyme lives in the matching ending sound, toward the finer phoneme work that follows, still oral.",
                "extensions": [
                    "Sort a basket of named objects into rhyming families by ear",
                    "Make up a rhyming name for a new object",
                ],
                "observation_focus": "Watch whether the child hears the ending match, enjoys the games, and asks to play again; note this without grading.",
            },
            "unschooling": {
                "invitations": [
                    "Sing and say rhyming songs and nursery rhymes together, often",
                    "Play rhyme games in the car, in line, or at bath time whenever a moment opens",
                    "Make up silly rhymes together and laugh at them",
                ],
                "real_world_contexts": [
                    "Rhymes in favorite songs and picture books",
                    "Rhyming names and silly nicknames in everyday talk",
                    "Jump-rope and clapping rhymes",
                ],
                "conversation_starters": [
                    "Those two words sounded the same at the end, did you hear it?",
                    "Can you hear a word that rhymes with this one?",
                    "What rhymes with your name?",
                ],
                "resource_bank": [
                    "A treasury of nursery rhymes and rhyming poetry kept available",
                    "Recordings of rhyming songs and rhymes",
                    "Rhyming picture books read again and again because the child loves them",
                ],
                "parent_role": "Fill the day with rhyme and song and follow the child's delight, saying words playfully and answering real questions about which words sound alike, without turning it into a lesson.",
                "observation_documentation": "Over time, notice whether the child enjoys rhymes, hears when words chime, and starts to point out rhymes; this noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Matching words by their ending sound is sorting by a shared attribute, the same thinking as grouping objects that are alike",
            "science": "Listening closely to compare sounds, as in noticing which animal calls sound alike",
            "history": "Rhymes have been passed down by ear for generations as a form of oral tradition",
        },
    },
    "rf-32": {
        "enriched": True,
        "learning_objectives": [
            "Produce a word that rhymes with a given spoken word",
            "Supply the missing rhyming word at the end of a familiar couplet",
            "Generate several rhyming words for one spoken word",
            "Offer a nonsense rhyme when no real word comes, showing the ending sound is matched",
        ],
        "teaching_guidance": {
            "introduction": "Producing a rhyme is harder than recognizing one: the child must search for a word that ends with the same sound. It is still purely oral, with no letters. Real words are best, but a nonsense word that rhymes shows the child has matched the ending sound, which is the skill.",
            "scaffolding_sequence": [
                "Model producing a rhyme: 'A word that rhymes with cat is... hat'",
                "Give a word and ask the child for any rhyming word",
                "Use a familiar couplet and let the child supply the last, rhyming word",
                "Encourage several rhymes for one word (cat: hat, bat, mat)",
                "Accept a nonsense rhyme (cat: zat) as evidence the ending sound is matched",
            ],
            "socratic_questions": [
                "Can you think of a word that ends like 'cat'?",
                "What word would finish this so it rhymes?",
                "Can you find another word that rhymes with it?",
            ],
            "practice_activities": [
                "Rhyme-a-word: parent says a word, child gives a rhyme",
                "Finish-the-rhyme couplets where the child supplies the last word",
                "Rhyme chains: keep adding rhyming words until you run out",
            ],
            "real_world_connections": [
                "Making up a rhyme about something during the day",
                "Finishing the rhyme in a familiar song",
                "Inventing silly rhyming nicknames",
            ],
            "common_misconceptions": [
                "Offering a word that starts the same instead of ends the same: redirect to the ending sound",
                "Thinking a rhyme must be a real word: a nonsense rhyme still shows the skill",
                "Repeating the same word back: a rhyme must be a different word with the same ending",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Produces at least one correct rhyme for a given spoken word",
                "Supplies the rhyming word to finish a familiar couplet",
                "Generates more than one rhyme for a single word",
            ],
            "assessment_methods": ["oral rhyme production", "finish-the-couplet", "rhyme-chain generation"],
            "sample_assessment_prompts": [
                "Say a word that rhymes with 'dog'",
                "Finish so it rhymes: 'The fat cat sat on the ___'",
                "Give me two words that rhyme with 'bee'",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Say a word that rhymes with 'cat'.",
                "expected_type": "text",
                "hints": ["Think of a word that ends with /at/, like h-at"],
                "explanation": "Any word ending in /at/ works: hat, bat, mat, sat, rat. A nonsense rhyme like 'zat' also shows the ending is matched.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Say a word that rhymes with 'dog'.",
                "expected_type": "text",
                "hints": ["Think of a word ending with /og/, like l-og"],
                "explanation": "Any /og/ word works: log, fog, jog, hog.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Finish so it rhymes: 'I see a bug in a ___' (rhymes with bug).",
                "expected_type": "text",
                "correct_answer": "rug",
                "hints": ["Something on the floor that ends with /ug/"],
                "explanation": "'rug' rhymes with 'bug' and fits the sentence.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Say a word that rhymes with 'tree'.",
                "expected_type": "text",
                "hints": ["Think of a word ending with /ee/, like b-ee"],
                "explanation": "Any /ee/ word works: bee, see, me, key, three.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Finish so it rhymes: 'The cat wore a funny ___' (rhymes with cat).",
                "expected_type": "text",
                "correct_answer": "hat",
                "hints": ["Something you wear that ends with /at/"],
                "explanation": "'hat' rhymes with 'cat' and fits the sentence.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Give me TWO words that rhyme with 'pig'.",
                "expected_type": "text",
                "hints": ["Words ending in /ig/, like w-ig and b-ig"],
                "explanation": "Two /ig/ words work, for example wig and big (or dig, jig).",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Your friend rhymes 'sun' with 'soap' because both start with /s/. Give a real rhyme for 'sun' and say why theirs was wrong.",
                "expected_type": "text",
                "correct_answer": "a real rhyme is 'run' (or fun, bun); theirs was wrong because rhyme is the ending sound, not the start",
                "hints": ["What ends like /un/?"],
                "explanation": "run, fun, or bun rhyme with sun; rhyme depends on the ending sound, so matching the beginning /s/ is not a rhyme.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Make a rhyme chain for 'hop': keep saying words that rhyme until you run out. Tell me your words.",
                "expected_type": "text",
                "hints": ["top, mop, pop, stop... real or silly words ending in /op/"],
                "explanation": "No single right answer; the child should produce several /op/ words (top, mop, pop, stop), and nonsense /op/ words still count as matched endings.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Finish so it rhymes: 'The fat cat sat on the ___'.",
                "type": "text",
                "correct_answer": "mat",
                "target_concept": "rhyme_cloze",
            },
            {
                "prompt": "Say a word that rhymes with 'dog'.",
                "type": "open_response",
                "rubric": "Mastery: gives a correct /og/ rhyme readily. Proficient: gives one with a hint. Developing: needs the ending sound modeled first.",
                "target_concept": "rhyme_production",
            },
            {
                "prompt": "Give me two words that rhyme with 'bee'.",
                "type": "open_response",
                "rubric": "Mastery: gives two correct /ee/ rhymes. Proficient: gives one. Developing: needs support to find any.",
                "target_concept": "rhyme_generation",
            },
            {
                "prompt": "Finish so it rhymes: 'A little bug sat on a ___'.",
                "type": "text",
                "correct_answer": "rug",
                "target_concept": "rhyme_cloze",
            },
            {
                "prompt": "Make a rhyme chain for 'cat'.",
                "type": "open_response",
                "rubric": "Mastery: produces several /at/ words. Proficient: produces two. Developing: produces one with help (nonsense rhymes count).",
                "target_concept": "rhyme_chain",
            },
        ],
        "resource_guidance": {
            "required": ["no materials needed: this is purely oral production"],
            "recommended": ["nursery rhymes and rhyming songs", "rhyming picture books to fill in the rhyme"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 10},
        "accommodations": {
            "dyslexia": "Production is hard; give the ending sound as a strong cue ('it ends with /at/...') and warmly accept nonsense rhymes as success.",
            "adhd": "Use fast, playful rhyme chains and finish-the-rhyme games with energy; keep turns short.",
            "gifted": "Ask for several rhymes per word and for finishing whole rhyming couplets the child invents.",
            "visual_learner": "Offer a picture cue of a possible rhyme to prime the search, then fade it.",
            "kinesthetic_learner": "Bounce a ball or clap on each rhyme produced in a chain.",
            "auditory_learner": "A strength area: build on songs and let the child fill in missing rhymes by ear.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Now we make rhymes, not just spot them: given a word, we find another word that ends with the same sound. It is all by ear, and a silly nonsense rhyme still counts because the ending matches.",
                "gradual_release": {
                    "i_do": "Say, 'A word that rhymes with cat is... hat. Another is bat.' Stretch the /at/ ending each time so the matching sound is clear.",
                    "we_do": "Take turns producing rhymes for a word together, and finish familiar couplets together with the rhyming word.",
                    "you_do": "Child produces a rhyme for a given word, finishes a couplet with the rhyming word, and makes a short rhyme chain.",
                },
                "guided_practice": [
                    "Take-turns rhyming for one word together",
                    "Finish-the-couplet with the rhyming word together",
                ],
                "independent_practice": [
                    "The child gives a rhyme for several words alone",
                    "The child builds a rhyme chain as long as they can",
                ],
                "mastery_check": [
                    "Produces a correct rhyme for a given word",
                    "Supplies the rhyming word to finish a couplet",
                    "Generates more than one rhyme for a word",
                ],
                "spiral_review": [
                    "Begin by re-judging a few spoken rhyme pairs from rf-31 (do these rhyme?) before producing rhymes, since making a rhyme builds directly on hearing whether two words rhyme",
                ],
            },
            "classical": {
                "narrative_introduction": "The trained ear not only hears rhyme but answers it, supplying the chiming word. The grammar stage practices this through couplets and recited rhymes, all aloud.",
                "memory_work": {
                    "chants": [
                        "Chant a rhyming word string and add one more rhyme at the end each time",
                        "Chant a couplet and pause for the child to supply the final rhyme",
                    ],
                    "recitations": [
                        "Recite a known rhyme leaving the last rhyming word for the child to say",
                    ],
                },
                "recitation_routine": "Begin with a known rhyme, pausing for the child to fill the rhyming word, before new production work; the practice is cumulative.",
                "history_integration": "Filling in a rhyme is how children have joined in songs and rhymes for generations, an old, shared pleasure of oral tradition.",
                "read_aloud_suggestions": [
                    "Predictable rhyming poems read aloud with a pause for the child to supply the rhyme",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "Predictable, strongly rhyming poems and nursery rhymes the child can help finish",
                ],
                "short_lesson_flow": "Recite a loved rhyme together, then pause at the end of a line for the child to supply the rhyming word, delighting in their answer. Try one or two more, lightly, and stop.",
                "narration_prompt": "What word finished our rhyme? Can you think of another word that would rhyme too?",
                "real_world_objects": [
                    "A small object whose name invites a rhyme to be made up about it",
                    "Family names turned into a playful rhyme",
                ],
                "nature_connection": "Make up a one-line rhyme about something found outdoors, letting the child supply the rhyming word.",
                "habit_focus": "The habit of joyful, attentive participation in the music of language.",
            },
            "montessori": {
                "prepared_materials": [
                    "A basket of objects whose names have easy rhymes to produce",
                    "A calm space for the rhyming game",
                    "No letters: production stays oral and precedes letter work",
                ],
                "presentation": {
                    "three_period_lesson": "Adapted for sound. Naming: 'cat... a rhyme is hat.' Recognition: 'Can you make a rhyme for cat?' Recall: 'Give me another rhyme for cat.' All spoken.",
                    "steps": [
                        "Model a rhyme for an object's name",
                        "Invite the child to make a rhyme for the next object",
                        "Encourage a second and third rhyme, accepting nonsense rhymes",
                    ],
                },
                "control_of_error": "The ending sound is the control: a produced word either ends the same or it does not, which the guide and child hear together; nonsense rhymes that match are honored.",
                "abstraction_pathway": "From recognizing rhyme, to actively generating words by their ending sound, deepening the oral phoneme work that follows.",
                "extensions": [
                    "Generate a whole rhyming family for an object's name",
                    "Make up a rhyming couplet about a chosen object",
                ],
                "observation_focus": "Watch whether the child can search for and produce a matching ending, and note their growing ease and pleasure.",
            },
            "unschooling": {
                "invitations": [
                    "Pause in a familiar song or rhyme and let the child fill in the rhyming word",
                    "Make up silly rhymes together throughout the day",
                    "Play rhyme-back: one person says a word, the other answers with a rhyme",
                ],
                "real_world_contexts": [
                    "Finishing the rhyme in a favorite song",
                    "Inventing rhyming nicknames or silly chants",
                    "Making a little rhyme about whatever is happening",
                ],
                "conversation_starters": [
                    "Can you think of a word that rhymes with this?",
                    "What word would finish our rhyme?",
                    "Want to play rhyme-back with me?",
                ],
                "resource_bank": [
                    "Predictable rhyming songs and books kept available",
                    "A habit of playful rhyming in daily talk",
                    "Recordings of rhyming songs to join in with",
                ],
                "parent_role": "Invite the child to fill in and make rhymes in the flow of real play and song, celebrate nonsense rhymes that match, and answer genuine questions without drilling.",
                "observation_documentation": "Over time, notice whether the child supplies and invents rhymes in play; that lived noticing is the assessment.",
            },
        },
        "connections": {
            "math": "Generating many words that fit one ending sound is like finding many examples that fit one rule or pattern",
            "science": "Producing examples that share a feature, as when naming things that share a property",
            "history": "Joining in and finishing rhymes is part of the shared oral tradition of songs and verses",
        },
    },
    "rf-33": {
        "enriched": True,
        "learning_objectives": [
            "Hear that a spoken sentence is made of separate words",
            "Tap or place a counter for each word in a short spoken sentence",
            "Count how many words are in a short spoken sentence",
            "Add a word to a spoken sentence and tell that the count went up by one",
        ],
        "teaching_guidance": {
            "introduction": "This is the largest unit of phonological awareness: hearing that speech breaks into separate words. It is entirely oral, with no print and no letters: the child listens to a spoken sentence and taps or counts the words. (This is the ear-only twin of the print-based word concept; here nothing is shown, only heard.)",
            "scaffolding_sequence": [
                "Say a short sentence slowly with a tiny pause between words",
                "Tap the table once for each word as you say the sentence",
                "Have the child tap along, one tap per word",
                "Count the taps to count the words",
                "Add one word and notice the count goes up by one",
            ],
            "socratic_questions": [
                "How many words did you hear in that sentence?",
                "Can you tap once for each word as I say it?",
                "If I add one more word, how many words now?",
            ],
            "practice_activities": [
                "Tap-the-words: one tap per spoken word, then count the taps",
                "Counter push: push a counter for each word in a spoken sentence",
                "Add-a-word: grow a sentence one word at a time and recount",
            ],
            "real_world_connections": [
                "Counting the words in a short spoken instruction",
                "Tapping the words of a spoken greeting",
                "Hearing how a sentence is longer when more words are added",
            ],
            "common_misconceptions": [
                "Tapping syllables instead of words (tapping 'rab-bit' as two): keep this at the WORD level, one tap per word",
                "Running words together and undercounting: say the sentence slowly with tiny gaps",
                "Forgetting little words like 'a' and 'the': those are words too and get a tap",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Taps once per word for a short spoken sentence",
                "Counts the words in a short spoken sentence correctly",
                "Recognizes that adding a word increases the count by one",
            ],
            "assessment_methods": ["tap-per-word demonstration", "oral word count", "add-a-word counting"],
            "sample_assessment_prompts": [
                "Tap once for each word: 'I like dogs'",
                "How many words did I just say?",
                "Now I add a word. How many words now?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "How many words are in the spoken sentence 'I run'?",
                "expected_type": "number",
                "correct_answer": "2",
                "hints": ["Tap once for each word: I (tap) run (tap)"],
                "explanation": "There are 2 words: 'I' and 'run'.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "How many words are in 'The dog barks'?",
                "expected_type": "number",
                "correct_answer": "3",
                "hints": ["The / dog / barks: one tap each"],
                "explanation": "There are 3 words: The, dog, barks.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "When you tap a spoken sentence, do you tap once for each word or once for each sound?",
                "expected_type": "text",
                "correct_answer": "once for each word",
                "hints": ["This game is about whole words"],
                "explanation": "At this step we tap once for each whole word, not each sound.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "How many words are in 'I like to play'?",
                "expected_type": "number",
                "correct_answer": "4",
                "hints": ["I / like / to / play"],
                "explanation": "There are 4 words: I, like, to, play.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Does the little word 'a' count as a word when we tap 'a big dog'?",
                "expected_type": "text",
                "correct_answer": "yes",
                "hints": ["Every word gets a tap, even little ones"],
                "explanation": "Yes, 'a' is a word and gets its own tap, so 'a big dog' is 3 words.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "I say 'We can go' (3 words), then I add 'home': 'We can go home'. How many words now?",
                "expected_type": "number",
                "correct_answer": "4",
                "hints": ["Adding one word makes the count go up by one"],
                "explanation": "Adding 'home' makes 4 words; one more word raises the count by one.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Your friend taps 'The rabbit hops' four times. Why is that wrong, and how many taps should it be?",
                "expected_type": "text",
                "correct_answer": "they tapped syllables (rab-bit); it should be 3 taps, one per word: The / rabbit / hops",
                "hints": ["Count whole words, not the beats inside a word"],
                "explanation": "They tapped the syllables in 'rabbit'; at the word level it is 3 words, so 3 taps.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Listen to a spoken sentence I say, tap once for each word, and tell me how many words there were.",
                "expected_type": "text",
                "hints": ["One tap per word, then count the taps"],
                "explanation": "No single right answer; the child should tap once per word and report the matching count for whatever sentence is said.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "How many words are in 'I see a cat'?",
                "type": "number",
                "correct_answer": "4",
                "target_concept": "sentence_word_count",
            },
            {
                "prompt": "Tap once for each word as I say 'We can play'.",
                "type": "open_response",
                "rubric": "Mastery: taps exactly 3 times, one per word. Proficient: taps 3 with a small adjustment. Developing: taps syllables or miscounts without help.",
                "target_concept": "tap_per_word",
            },
            {
                "prompt": "How many words are in 'Go now'?",
                "type": "number",
                "correct_answer": "2",
                "target_concept": "sentence_word_count",
            },
            {
                "prompt": "I say 'The cat naps' then add 'here'. How many words now?",
                "type": "number",
                "correct_answer": "4",
                "target_concept": "add_a_word",
            },
            {
                "prompt": "Tell me what each tap stands for when we tap a sentence.",
                "type": "open_response",
                "rubric": "Mastery: says each tap is one word. Proficient: says words with a prompt. Developing: confuses words with sounds or syllables.",
                "target_concept": "word_as_unit",
            },
        ],
        "resource_guidance": {
            "required": ["no materials needed: this is purely oral listening work"],
            "recommended": ["counters or blocks to push for each word", "a quiet space to listen"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 10},
        "accommodations": {
            "dyslexia": "Say sentences slowly with clear gaps; use counters the child can push so the abstract word count becomes concrete.",
            "adhd": "Use short sentences and let the child tap big or stomp each word; keep rounds brief and active.",
            "gifted": "Use longer sentences and the add-a-word game, and ask the child to make a sentence with an exact number of words.",
            "visual_learner": "Push one counter per word so the count is seen as well as heard.",
            "kinesthetic_learner": "Stomp, clap, or jump once per word, then count the movements.",
            "auditory_learner": "A strength area: rely on careful listening and counting by ear.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "A spoken sentence is made of separate words. Today we listen to short sentences and tap once for each word, then count the words. This is by ear only, no letters, and we count words, not sounds.",
                "gradual_release": {
                    "i_do": "Say 'I like dogs' slowly with tiny gaps, tapping once per word, then count: 'three words.' Then add 'too' and recount: 'four words.'",
                    "we_do": "Tap and count short spoken sentences together, one tap per word, and play add-a-word together, recounting each time.",
                    "you_do": "Child taps once per word for spoken sentences, counts the words, and tells how the count changes when a word is added.",
                },
                "guided_practice": [
                    "Tap-and-count short spoken sentences together",
                    "Add-a-word: grow a sentence and recount together",
                ],
                "independent_practice": [
                    "The child taps and counts the words in spoken sentences alone",
                    "The child makes a sentence with a chosen number of words",
                ],
                "mastery_check": [
                    "Taps once per word for a short sentence",
                    "Counts the words correctly",
                    "Knows adding a word raises the count by one",
                ],
                "spiral_review": [
                    "Warm up with attentive listening from rf-21 (listening closely to a whole spoken sentence) before breaking sentences into words, since hearing the separate words depends on careful listening to the whole",
                ],
            },
            "classical": {
                "narrative_introduction": "Speech, which seems to flow, is really built of separate words. The grammar stage trains the ear to hear those words one by one, all aloud, before any are seen in print.",
                "memory_work": {
                    "chants": [
                        "Chant a short sentence one word per beat, tapping each word",
                        "Chant 'one word, two words, three words' while adding a word each time",
                    ],
                    "recitations": [
                        "Recite a short known sentence and count its words aloud together",
                    ],
                },
                "recitation_routine": "Begin with a known short line, tap and count its words, before new sentence work; the counting is cumulative and exact.",
                "history_integration": "Hearing speech as separate words underlies all later reading and writing, the foundation on which the written word was built.",
                "read_aloud_suggestions": [
                    "Short, clearly spoken sentences read aloud for the child to tap and count by word",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A short, well-spoken line from a loved poem or story, said aloud to tap and count",
                ],
                "short_lesson_flow": "Say a short, loved line together, then gently tap once for each word and count how many words it holds. Add a word for fun and recount, then stop while it is still enjoyable.",
                "narration_prompt": "How many words were in our little sentence? Tap them with me.",
                "real_world_objects": [
                    "A short spoken instruction in the day, tapped word by word",
                    "Counters or pebbles pushed one per word",
                ],
                "nature_connection": "Say a short sentence about something seen outdoors and tap its words while looking at the thing named.",
                "habit_focus": "The habit of attentive listening: hearing a sentence as its exact, separate words.",
            },
            "montessori": {
                "prepared_materials": [
                    "A small set of counters or beads to push, one per word",
                    "A calm space for the listening game",
                    "No letters: the word-counting game stays oral",
                ],
                "presentation": {
                    "three_period_lesson": "Adapted for sound. Naming: 'I say I-run; that is two words,' pushing two counters. Recognition: 'Push a counter for each word as I speak.' Recall: 'How many words did you hear?'",
                    "steps": [
                        "Say a short sentence and push one counter per word",
                        "Invite the child to push counters as you speak",
                        "Count the counters to count the words, then add a word and recount",
                    ],
                },
                "control_of_error": "The counters are the control: if the child pushes too many or too few, the count of counters will not match the words heard on a re-say, which the child can check and correct.",
                "abstraction_pathway": "From pushing a concrete counter per spoken word, to holding the count in the mind, preparing finer syllable and phoneme counting that follows.",
                "extensions": [
                    "Count words in longer spoken sentences",
                    "Build a sentence with an exact number of counters, one per word",
                ],
                "observation_focus": "Watch whether the child keeps one counter per word (not per syllable) and counts accurately, and note their growing independence.",
            },
            "unschooling": {
                "invitations": [
                    "Play 'how many words did I say?' in the flow of the day",
                    "Tap out the words of a silly sentence together",
                    "Grow a funny sentence one word at a time and count as it grows",
                ],
                "real_world_contexts": [
                    "Counting the words in a short spoken plan ('Let us go now')",
                    "Tapping the words of a greeting or thank-you",
                    "Making up and lengthening playful sentences",
                ],
                "conversation_starters": [
                    "How many words do you think I just said?",
                    "Can you tap each word with me?",
                    "What if we add one more word, how many now?",
                ],
                "resource_bank": [
                    "A handful of counters or small toys to push per word",
                    "Playful sentences invented together",
                    "Everyday talk used for quick word-counting",
                ],
                "parent_role": "Drop quick, playful word-counting into ordinary talk, follow the child's interest, and answer real questions about words and sentences without making it a drill.",
                "observation_documentation": "Over time, notice whether the child hears sentences as separate words and counts them in play; that noticing is the record.",
            },
        },
        "connections": {
            "math": "Tapping and counting one number per word is direct one-to-one counting, and add-a-word is adding one to a count",
            "science": "Breaking a whole into its parts to count them, as when counting the parts of a plant",
            "history": "Recognizing speech as separate words underlies the invention of written language",
        },
    },
    "rf-34": {
        "enriched": True,
        "learning_objectives": [
            "Blend spoken syllables into a whole word (pen-cil into pencil)",
            "Clap or tap the syllables in a spoken word",
            "Count the syllables in a spoken word",
            "Explain that a syllable is a beat in a word, heard not spelled",
        ],
        "teaching_guidance": {
            "introduction": "Syllables are the beats inside a spoken word. The child blends syllables into a word and claps a word into its syllables, all by ear with no letters. A hand under the chin helps: the chin drops once for each syllable (each vowel beat).",
            "scaffolding_sequence": [
                "Say a word in syllables (pen...cil) and blend it into 'pencil'",
                "Clap a word into its syllables (rab-bit, two claps)",
                "Use the chin-drop trick: count how many times the chin drops",
                "Count the syllables by counting the claps",
                "Sort some words by how many syllables they have",
            ],
            "socratic_questions": [
                "If I say the parts pen...cil, what word is that?",
                "How many beats do you hear when you say this word?",
                "How many times did your chin drop?",
            ],
            "practice_activities": [
                "Clap-the-syllables for names and familiar words",
                "Blend-the-syllables: parent says parts, child says the word",
                "Syllable sort: one-clap words versus two-clap words",
            ],
            "real_world_connections": [
                "Clapping the syllables in family members' names",
                "Tapping syllables in favorite foods or animals",
                "Hearing the beats in a chanted cheer",
            ],
            "common_misconceptions": [
                "Counting sounds instead of beats (saying 'cat' has 3): syllables are beats, so 'cat' is one beat",
                "Adding a beat that is not there: use the chin-drop to check the real number of beats",
                "Thinking syllables are about letters: this is by ear; the chin-drop counts spoken beats",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Blends spoken syllables into the correct word",
                "Claps a spoken word into its correct number of syllables",
                "Counts the syllables in a spoken word",
            ],
            "assessment_methods": ["oral syllable blending", "syllable clapping", "chin-drop syllable count"],
            "sample_assessment_prompts": [
                "Blend these parts: 'ta-ble'. What word?",
                "Clap the syllables in 'butterfly'. How many?",
                "How many beats are in your own name?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Blend these spoken parts into a word: 'pen-cil'. What word?",
                "expected_type": "text",
                "correct_answer": "pencil",
                "hints": ["Push the two beats together"],
                "explanation": "Blending pen + cil makes 'pencil'.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "How many syllables (beats) are in 'cat'?",
                "expected_type": "number",
                "correct_answer": "1",
                "hints": ["Say it and feel one chin-drop"],
                "explanation": "'cat' has 1 syllable: one beat, one chin-drop.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "How many syllables are in 'rabbit'?",
                "expected_type": "number",
                "correct_answer": "2",
                "hints": ["Clap it: rab-bit"],
                "explanation": "'rabbit' has 2 syllables: rab-bit.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Blend these parts into a word: 'el-e-phant'. What word?",
                "expected_type": "text",
                "correct_answer": "elephant",
                "hints": ["Three beats pushed together"],
                "explanation": "Blending el + e + phant makes 'elephant'.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "How many syllables are in 'butterfly'?",
                "expected_type": "number",
                "correct_answer": "3",
                "hints": ["Clap it: but-ter-fly"],
                "explanation": "'butterfly' has 3 syllables: but-ter-fly.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Which word has more syllables, 'dog' or 'banana'?",
                "expected_type": "text",
                "correct_answer": "banana",
                "hints": ["Clap each: dog (1), ba-na-na (3)"],
                "explanation": "'banana' has 3 beats and 'dog' has 1, so 'banana' has more syllables.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Your friend says 'cat' has three syllables because it has three sounds. Why is that wrong, and how many syllables does 'cat' have?",
                "expected_type": "text",
                "correct_answer": "syllables are beats, not single sounds; 'cat' is one beat, so 1 syllable",
                "hints": ["Feel the chin-drops, not the separate sounds"],
                "explanation": "They counted sounds, but syllables are beats; 'cat' is one beat (one chin-drop), so 1 syllable.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Clap the syllables in your own name and tell me how many beats it has.",
                "expected_type": "text",
                "hints": ["Clap once for each beat and count the claps"],
                "explanation": "No single right answer; the child should clap one beat per syllable of their name and report the matching count.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Blend these parts: 'ta-ble'. What word?",
                "type": "text",
                "correct_answer": "table",
                "target_concept": "syllable_blending",
            },
            {
                "prompt": "How many syllables are in 'butterfly'?",
                "type": "number",
                "correct_answer": "3",
                "target_concept": "syllable_counting",
            },
            {
                "prompt": "Clap the syllables in 'pencil' and tell me how many.",
                "type": "open_response",
                "rubric": "Mastery: claps 2 beats and says 2. Proficient: claps 2 with a recount. Developing: claps sounds or miscounts without help.",
                "target_concept": "syllable_clapping",
            },
            {
                "prompt": "How many syllables are in 'sun'?",
                "type": "number",
                "correct_answer": "1",
                "target_concept": "syllable_counting",
            },
            {
                "prompt": "Tell me what a syllable is.",
                "type": "open_response",
                "rubric": "Mastery: says it is a beat in a word (one chin-drop). Proficient: gives the idea with a prompt. Developing: confuses syllables with single sounds.",
                "target_concept": "syllable_concept",
            },
        ],
        "resource_guidance": {
            "required": ["no materials needed: this is purely oral listening work"],
            "recommended": ["a hand to place under the chin", "names and picture cards to clap"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 10},
        "accommodations": {
            "dyslexia": "Use the chin-drop and clapping together so the syllable beat is felt; keep words short at first and go slowly.",
            "adhd": "Make it active: clap, stomp, or jump the syllables of fun words; keep rounds quick.",
            "gifted": "Move to four-syllable words and to syllable sorting and blending longer words.",
            "visual_learner": "Place one block per beat as you clap so the count is seen as well as felt.",
            "kinesthetic_learner": "Clap, tap, or step each syllable; the chin-drop is itself a movement cue.",
            "auditory_learner": "A strength area: chant words in syllables and blend by ear.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Words have beats called syllables. Today we push syllables together to make a word and clap a word into its beats, all by ear. A hand under the chin helps: the chin drops once for each beat.",
                "gradual_release": {
                    "i_do": "Say 'pen...cil' and blend it: 'pencil.' Then clap 'rab-bit' into two beats and say, 'two syllables,' showing the chin drop twice.",
                    "we_do": "Blend syllables into words together and clap words into syllables together, counting the claps each time.",
                    "you_do": "Child blends spoken syllables into words and claps and counts the syllables in spoken words.",
                },
                "guided_practice": [
                    "Clap-and-count the syllables in names together",
                    "Blend-the-parts into words together",
                ],
                "independent_practice": [
                    "The child claps and counts the syllables in a set of words alone",
                    "The child blends syllable parts into whole words",
                ],
                "mastery_check": [
                    "Blends spoken syllables into the correct word",
                    "Claps a word into its correct number of syllables",
                    "Counts syllables (beats), not single sounds",
                ],
                "spiral_review": [
                    "Begin by tapping and counting the words in a short spoken sentence from rf-33, then move inside one word to clap its syllables, since syllable beats are the next level down from counting whole words",
                ],
            },
            "classical": {
                "narrative_introduction": "Inside each spoken word are beats, the syllables. The grammar stage learns to hear and count these beats by chant and clap, all aloud, training the ear ever finer.",
                "memory_work": {
                    "chants": [
                        "Chant a word in its syllables, clapping each beat: but-ter-fly",
                        "Chant a list of names, clapping the syllables of each",
                    ],
                    "recitations": [
                        "Recite a rhythmic verse and clap its strong beats to feel syllable rhythm",
                    ],
                },
                "recitation_routine": "Begin by clapping the syllables of a few known words before new blending work; the beat-counting is cumulative.",
                "history_integration": "Rhythm and beat are ancient in chant, song, and verse; counting syllables trains the same sense of measured sound.",
                "read_aloud_suggestions": [
                    "Strongly rhythmic poems read aloud and clapped to feel the syllable beats",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A rhythmic, loved poem whose words invite gentle syllable clapping",
                ],
                "short_lesson_flow": "Enjoy a rhythmic rhyme together, then gently clap the beats of a few of its words and count them, using the chin-drop trick. Blend one or two words from their parts, then stop.",
                "narration_prompt": "How many beats are in this word? Clap them with me.",
                "real_world_objects": [
                    "Family names clapped into their beats",
                    "Favorite foods and animals clapped by syllable",
                ],
                "nature_connection": "Clap the syllables in the names of things found outdoors (ro-bin, but-ter-fly) while looking at them.",
                "habit_focus": "The habit of attentive listening to the rhythm and beats within words.",
            },
            "montessori": {
                "prepared_materials": [
                    "Picture cards of words with one, two, and three syllables",
                    "A small set of blocks to place one per beat",
                    "No letters: the syllable games stay oral",
                ],
                "presentation": {
                    "three_period_lesson": "Adapted for sound. Naming: 'rab-bit, two beats,' clapping twice. Recognition: 'Clap the beats in this word.' Recall: 'How many beats did you hear?'",
                    "steps": [
                        "Clap a word into its syllables and place a block per beat",
                        "Invite the child to clap and place blocks for a word",
                        "Blend syllable parts into a word, and sort words by beat count",
                    ],
                },
                "control_of_error": "The blocks make the count concrete: the number of blocks should match the claps on a re-say, which the child can check and fix.",
                "abstraction_pathway": "From clapping and placing a block per beat, to hearing and counting syllables in the mind, narrowing toward single-phoneme work.",
                "extensions": [
                    "Sort a basket of picture cards by number of syllables",
                    "Blend and clap longer words",
                ],
                "observation_focus": "Watch whether the child counts beats (not single sounds) and blends parts accurately, noting growing ease.",
            },
            "unschooling": {
                "invitations": [
                    "Clap the beats of names and favorite words in the flow of the day",
                    "Play 'guess my word' by saying it in syllable parts to blend",
                    "Chant and clap rhythmic songs and cheers together",
                ],
                "real_world_contexts": [
                    "Clapping the syllables of family and pet names",
                    "Tapping the beats of favorite foods at the table",
                    "Feeling syllable beats in songs and cheers",
                ],
                "conversation_starters": [
                    "How many beats are in your name? Let us clap it.",
                    "If I say it in parts, can you guess my word? bu-tter-fly",
                    "Which has more beats, this word or that one?",
                ],
                "resource_bank": [
                    "Songs and cheers with strong beats",
                    "Names and everyday words to clap",
                    "Picture books with rhythmic language",
                ],
                "parent_role": "Drop syllable clapping and blending into real play and song, follow the child's delight, and answer genuine questions about beats without drilling.",
                "observation_documentation": "Over time, notice whether the child blends parts into words and claps beats accurately in play; that noticing is the assessment.",
            },
        },
        "connections": {
            "math": "Counting syllable beats is one-to-one counting, and comparing which word has more beats is comparing quantities",
            "science": "Breaking a whole word into its beats is the same part-whole analysis used to study parts of objects",
            "history": "Beat and rhythm are central to the chants and songs of oral tradition",
        },
    },
    "rf-35": {
        "enriched": True,
        "learning_objectives": [
            "Take a compound word apart into its two smaller words (cowboy into cow and boy)",
            "Say a compound word with one part deleted (cowboy without cow is boy)",
            "Delete one syllable from a two-syllable word and say what remains",
            "Explain that taking a part away leaves a smaller spoken word",
        ],
        "teaching_guidance": {
            "introduction": "This step manipulates syllables: the child pulls a compound word apart and says it with one part removed. It begins with compound words (two real words joined) because the parts are meaningful and easy to hear, then extends to deleting a syllable. It is all oral, no letters.",
            "scaffolding_sequence": [
                "Take a compound word apart: 'cowboy' is 'cow' and 'boy'",
                "Delete one part: 'say cowboy without cow' (boy)",
                "Delete the other part: 'say cowboy without boy' (cow)",
                "Move to two-syllable non-compounds: 'say pencil without pen' (cil)",
                "Check by blending the remaining part back to confirm",
            ],
            "socratic_questions": [
                "What two smaller words do you hear in this word?",
                "If we take away this part, what part is left?",
                "What word is left when we drop the first beat?",
            ],
            "practice_activities": [
                "Compound take-apart: name the two words inside a compound",
                "Say-it-without: delete a named part and say what remains",
                "Build-and-break: join two words, then drop one and say the rest",
            ],
            "real_world_connections": [
                "Hearing the two words inside 'sunflower' or 'rainbow'",
                "Playing 'take a part away' with compound words during the day",
                "Noticing compound words in stories read aloud",
            ],
            "common_misconceptions": [
                "Deleting a sound instead of the named part: keep this at the syllable/word-part level",
                "Losing track of which part to remove: name the part to drop clearly and re-say the whole first",
                "Thinking the leftover must be a real word: with non-compounds the leftover beat may be nonsense, and that is fine",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Names the two words inside a compound word",
                "Says a compound word correctly with one part deleted",
                "Deletes a syllable from a two-syllable word and says what remains",
            ],
            "assessment_methods": ["compound take-apart", "say-it-without deletion", "syllable deletion"],
            "sample_assessment_prompts": [
                "What two words are in 'sunflower'?",
                "Say 'cowboy' without 'cow'",
                "Say 'pencil' without 'pen'",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What two smaller words are in 'cowboy'?",
                "expected_type": "text",
                "correct_answer": "cow and boy",
                "hints": ["Say it slowly: cow...boy"],
                "explanation": "'cowboy' is made of 'cow' and 'boy'.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Say 'cowboy' without 'cow'. What is left?",
                "expected_type": "text",
                "correct_answer": "boy",
                "hints": ["Take away the 'cow' part"],
                "explanation": "Taking 'cow' away from 'cowboy' leaves 'boy'.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What two smaller words are in 'sunflower'?",
                "expected_type": "text",
                "correct_answer": "sun and flower",
                "hints": ["Say it slowly: sun...flower"],
                "explanation": "'sunflower' is made of 'sun' and 'flower'.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Say 'sunflower' without 'flower'. What is left?",
                "expected_type": "text",
                "correct_answer": "sun",
                "hints": ["Take away the 'flower' part"],
                "explanation": "Taking 'flower' away from 'sunflower' leaves 'sun'.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Say 'rainbow' without 'rain'. What is left?",
                "expected_type": "text",
                "correct_answer": "bow",
                "hints": ["Take away the 'rain' part"],
                "explanation": "Taking 'rain' away from 'rainbow' leaves 'bow'.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Say 'pancake' without 'cake'. What is left?",
                "expected_type": "text",
                "correct_answer": "pan",
                "hints": ["Drop the 'cake' part"],
                "explanation": "Taking 'cake' away from 'pancake' leaves 'pan'.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Say 'pencil' without 'pen'. What part is left?",
                "expected_type": "text",
                "correct_answer": "cil",
                "hints": ["Drop the first beat 'pen' and say the rest"],
                "explanation": "Dropping 'pen' from 'pencil' leaves the beat 'cil'; it is fine that the leftover is not a real word.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Make your own: join two small words into a compound, then say it without one part. Tell me your word and what was left.",
                "expected_type": "text",
                "hints": ["Like cup + cake = cupcake; without cup leaves cake"],
                "explanation": "No single right answer; the child should form a compound (for example, cupcake) and correctly say the remaining part when one word is removed.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "What two words are in 'cowboy'?",
                "type": "text",
                "correct_answer": "cow and boy",
                "target_concept": "compound_segmentation",
            },
            {
                "prompt": "Say 'sunflower' without 'sun'.",
                "type": "text",
                "correct_answer": "flower",
                "target_concept": "compound_deletion",
            },
            {
                "prompt": "Say 'rainbow' without 'bow'.",
                "type": "text",
                "correct_answer": "rain",
                "target_concept": "compound_deletion",
            },
            {
                "prompt": "Say 'pencil' without 'pen' and tell me the part that is left.",
                "type": "open_response",
                "rubric": "Mastery: says the remaining beat 'cil'. Proficient: finds it after re-saying the whole word. Developing: needs the parts modeled first.",
                "target_concept": "syllable_deletion",
            },
            {
                "prompt": "Tell me what happens to a word when we take one part away.",
                "type": "open_response",
                "rubric": "Mastery: says a smaller word or part is left. Proficient: shows the idea with an example. Developing: needs prompting to hear the leftover.",
                "target_concept": "deletion_concept",
            },
        ],
        "resource_guidance": {
            "required": ["no materials needed: this is purely oral listening work"],
            "recommended": [
                "picture cards of compound words (cowboy, sunflower, rainbow)",
                "two blocks to join and pull apart",
            ],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 10},
        "accommodations": {
            "dyslexia": "Stay with clear compound words longer, use two blocks to join and remove a part, and re-say the whole word before deleting.",
            "adhd": "Make it a quick 'take-away' game with movement; keep words short and rounds brief.",
            "gifted": "Move to deleting syllables from longer non-compound words and to deleting either part on request.",
            "visual_learner": "Use two picture blocks for the two parts and physically remove one to show what is left.",
            "kinesthetic_learner": "Push two blocks together for the whole word and pull one away to feel the deletion.",
            "auditory_learner": "A strength area: do it all by ear, re-saying the whole and the remaining part.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Some words are made of two smaller words, like cowboy (cow + boy). Today we take compound words apart and say a word with one part removed, all by ear, then extend to dropping a syllable.",
                "gradual_release": {
                    "i_do": "Say 'cowboy is cow and boy.' Then say, 'cowboy without cow is... boy,' modeling the deletion. Show it again with 'sunflower' (sun + flower).",
                    "we_do": "Take compound words apart together and play 'say it without ___' together, re-saying the whole word first each time.",
                    "you_do": "Child names the two words in a compound, says a compound without a named part, and drops a syllable from a two-syllable word.",
                },
                "guided_practice": [
                    "Compound take-apart together with picture cards",
                    "Say-it-without rounds together",
                ],
                "independent_practice": [
                    "The child takes apart and deletes parts from a set of compound words alone",
                    "The child drops a syllable from two-syllable words",
                ],
                "mastery_check": [
                    "Names the two words in a compound",
                    "Says a compound with one part deleted",
                    "Deletes a syllable and says the remaining part",
                ],
                "spiral_review": [
                    "Warm up by clapping and counting the syllables of a few words from rf-34, then move to removing one of those beats, since deletion builds directly on hearing the separate syllables",
                ],
            },
            "classical": {
                "narrative_introduction": "Words can be taken apart as well as built up. The grammar stage learns to hold a word in mind, remove a part, and say what remains, training the ear to manipulate sound, all aloud.",
                "memory_work": {
                    "chants": [
                        "Chant compound pairs: 'cow plus boy is cowboy; sun plus flower is sunflower'",
                        "Chant 'take away ___, what is left?' as a steady call and response",
                    ],
                    "recitations": [
                        "Recite a short list of compound words and name the two parts of each",
                    ],
                },
                "recitation_routine": "Begin by naming the parts of a few known compound words before new deletion work; the manipulation is cumulative.",
                "history_integration": "Compounding small words into larger ones is an old way language grows; hearing the parts reveals how words are built.",
                "read_aloud_suggestions": [
                    "Stories or poems rich in compound words, read aloud to notice the parts",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A loved book or poem with clear compound words like sunflower, rainbow, or butterfly",
                ],
                "short_lesson_flow": "Enjoy a short text together, then gently play with a compound word from it: name its two parts and say it without one. Try one more, lightly, and stop.",
                "narration_prompt": "What two little words live inside this word? What is left if we take one away?",
                "real_world_objects": [
                    "A real sunflower or a toy cowboy whose name is taken apart",
                    "Two blocks joined for a compound, one removed for the deletion",
                ],
                "nature_connection": "With a real sunflower or rainbow in view, name its two word-parts and say the word without one.",
                "habit_focus": "The habit of attentive listening: holding a word in mind and hearing its parts.",
            },
            "montessori": {
                "prepared_materials": [
                    "Picture cards of compound words and of their two parts",
                    "Two blocks to join into a whole and pull apart",
                    "No letters: the take-apart games stay oral",
                ],
                "presentation": {
                    "three_period_lesson": "Adapted for sound. Naming: 'cowboy is cow and boy,' joining two blocks. Recognition: 'Say cowboy without cow.' Recall: 'What is left when we take away cow?'",
                    "steps": [
                        "Join two part-blocks and name the compound, then name each part",
                        "Remove one block and say the remaining part",
                        "Move to dropping a syllable from a two-syllable word",
                    ],
                },
                "control_of_error": "The two blocks are the control: removing one leaves exactly the other, which the child sees matches the remaining spoken part.",
                "abstraction_pathway": "From physically removing one part-block, to mentally deleting a part and hearing what remains, preparing single-phoneme manipulation later.",
                "extensions": [
                    "Delete either named part of a compound on request",
                    "Drop a syllable from longer non-compound words",
                ],
                "observation_focus": "Watch whether the child holds the whole word, removes the right part, and reports the remainder, noting growing independence.",
            },
            "unschooling": {
                "invitations": [
                    "Play 'take a part away' with compound words during the day",
                    "Notice the two little words hiding inside big words together",
                    "Join two words into a silly compound, then drop one part for fun",
                ],
                "real_world_contexts": [
                    "Hearing the parts of words like sunflower, rainbow, and pancake at home",
                    "Playing take-away word games in the car",
                    "Spotting compound words in favorite stories",
                ],
                "conversation_starters": [
                    "What two little words are hiding in this big word?",
                    "What is left if we take 'cow' out of 'cowboy'?",
                    "Want to make a silly word by joining two words?",
                ],
                "resource_bank": [
                    "Books and songs with compound words",
                    "Two blocks or toys to join and pull apart",
                    "Everyday compound words to play with",
                ],
                "parent_role": "Slip compound take-apart games into real play, follow the child's delight in finding hidden words, and answer genuine questions without making it a drill.",
                "observation_documentation": "Over time, notice whether the child hears the parts inside words and can take one away in play; that noticing is the record.",
            },
        },
        "connections": {
            "math": "Taking a part away from a whole word and saying what remains is the same idea as subtraction: whole minus part leaves the rest",
            "science": "Separating something into its parts and seeing what is left is basic part-whole analysis",
            "history": "Compounding small words into bigger ones is one of the old ways languages have grown",
        },
    },
    "rf-36": {
        "enriched": True,
        "learning_objectives": [
            "Blend a spoken onset and rime into a whole word (/c/ + at into cat)",
            "Understand that a word can start with one sound joined to a chunk",
            "Blend many words that share a rime by changing the onset (/h/ + at, /b/ + at)",
            "Push an onset and rime together smoothly with no letters",
        ],
        "teaching_guidance": {
            "introduction": "Onset-rime blending splits a one-syllable word into its onset (the beginning sound) and its rime (the vowel chunk that follows), then pushes them together: /c/ + at makes cat. It is the bridge between syllables and single phonemes, and it is entirely oral, no letters. The rime is heard as a familiar rhyme chunk.",
            "scaffolding_sequence": [
                "Say the rime chunk alone (at) so it is familiar",
                "Add an onset sound and blend: /c/ + at makes 'cat'",
                "Keep the rime and change the onset: /h/ + at, /b/ + at, /m/ + at",
                "Slow the gap between onset and rime, then push them together",
                "Try new rimes (/s/ + un, /p/ + ig) once 'at' is easy",
            ],
            "socratic_questions": [
                "If I say /c/ and then at, what word is that?",
                "What word do you get if you change the first sound to /h/?",
                "What chunk stays the same in cat, hat, and bat?",
            ],
            "practice_activities": [
                "Onset swap on one rime: /c/-at, /h/-at, /b/-at",
                "Mystery word: parent says onset then rime, child blends the word",
                "Word family build by ear: keep the rime, change the onset",
            ],
            "real_world_connections": [
                "Hearing word families in rhyming songs",
                "Playing 'guess my word' with onset and rime",
                "Noticing how cat, hat, and bat sound almost the same",
            ],
            "common_misconceptions": [
                "Leaving a big gap so it sounds like two pieces, not one word: push the parts together",
                "Changing the rime by accident: keep the rime steady, change only the first sound",
                "Thinking this needs letters: it is all by ear, blending sounds and a chunk",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Blends a spoken onset and rime into the correct word",
                "Blends several words on one rime by changing the onset",
                "Pushes onset and rime together smoothly into one word",
            ],
            "assessment_methods": ["oral onset-rime blending", "word-family blend by ear", "mystery-word blending"],
            "sample_assessment_prompts": [
                "Blend /m/ + at. What word?",
                "Blend /s/ + un. What word?",
                "Keep at and change the first sound to /r/. What word?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Blend the sounds /c/ + at. What word?",
                "expected_type": "text",
                "correct_answer": "cat",
                "hints": ["Push the first sound onto the chunk 'at'"],
                "explanation": "Blending /c/ with the rime 'at' makes 'cat'.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Blend /h/ + at. What word?",
                "expected_type": "text",
                "correct_answer": "hat",
                "hints": ["Same chunk 'at', new first sound /h/"],
                "explanation": "Blending /h/ with 'at' makes 'hat'.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Blend /s/ + it. What word?",
                "expected_type": "text",
                "correct_answer": "sit",
                "hints": ["Push /s/ onto the chunk 'it'"],
                "explanation": "Blending /s/ with 'it' makes 'sit'.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Blend /p/ + ig. What word?",
                "expected_type": "text",
                "correct_answer": "pig",
                "hints": ["First sound /p/, chunk 'ig'"],
                "explanation": "Blending /p/ with 'ig' makes 'pig'.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Keep the chunk 'at' and change the first sound to /b/. What word?",
                "expected_type": "text",
                "correct_answer": "bat",
                "hints": ["/b/ + at"],
                "explanation": "Blending /b/ with 'at' makes 'bat'.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Blend /s/ + un. What word?",
                "expected_type": "text",
                "correct_answer": "sun",
                "hints": ["First sound /s/, chunk 'un'"],
                "explanation": "Blending /s/ with 'un' makes 'sun'.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Using the chunk 'op', blend three words by changing the first sound. Tell me your three words.",
                "expected_type": "text",
                "hints": ["/t/ + op, /m/ + op, /h/ + op"],
                "explanation": "No single right answer; the child should blend three onsets onto 'op', for example top, mop, hop.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "I will say a first sound and a chunk with a pause; push them together fast and say the word: /f/ ... an.",
                "expected_type": "text",
                "correct_answer": "fan",
                "hints": ["Close the gap: /f/ + an"],
                "explanation": "Pushing /f/ and 'an' together quickly makes 'fan'.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Blend /m/ + at. What word?",
                "type": "text",
                "correct_answer": "mat",
                "target_concept": "onset_rime_blend",
            },
            {
                "prompt": "Blend /s/ + un. What word?",
                "type": "text",
                "correct_answer": "sun",
                "target_concept": "onset_rime_blend",
            },
            {
                "prompt": "Keep 'at' and change the first sound to /r/. What word?",
                "type": "text",
                "correct_answer": "rat",
                "target_concept": "onset_swap",
            },
            {
                "prompt": "Blend three words on the chunk 'ig' by changing the first sound.",
                "type": "open_response",
                "rubric": "Mastery: blends three (e.g., pig, big, wig). Proficient: blends two. Developing: blends one with help.",
                "target_concept": "word_family_blend",
            },
            {
                "prompt": "Tell me the two parts we push together to make a word like 'cat'.",
                "type": "open_response",
                "rubric": "Mastery: says the first sound (onset) and the chunk (rime). Proficient: shows the idea with an example. Developing: needs the parts modeled.",
                "target_concept": "onset_rime_concept",
            },
        ],
        "resource_guidance": {
            "required": ["no materials needed: this is purely oral listening work"],
            "recommended": ["picture cards for word families", "two blocks for onset and rime to push together"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 10},
        "accommodations": {
            "dyslexia": "Anchor one rime (at) and over-practice swapping onsets slowly; use two blocks for onset and rime to make the blend concrete.",
            "adhd": "Make it a fast 'mystery word' game; keep one rime per round and move briskly.",
            "gifted": "Use several rimes and longer word families, and ask the child to generate the family by ear.",
            "visual_learner": "Use a picture for the rime family and pictures for each blended word as cues.",
            "kinesthetic_learner": "Push two blocks together for the blend; slide them apart and back to feel onset and rime.",
            "auditory_learner": "A strength area: blend purely by ear, narrowing the gap between onset and rime.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "A short word has a first sound (the onset) and a chunk (the rime): /c/ + at makes cat. Today we push an onset and a rime together to make words, all by ear, keeping the chunk and changing the first sound.",
                "gradual_release": {
                    "i_do": "Say the rime 'at', then '/c/ + at... cat.' Keep 'at' and model '/h/ + at... hat,' '/b/ + at... bat,' pushing the parts together each time.",
                    "we_do": "Blend onset and rime together on one chunk, taking turns changing the first sound and saying the new word.",
                    "you_do": "Child blends a spoken onset and rime into a word and builds a small word family by changing the onset.",
                },
                "guided_practice": [
                    "Onset swap on one rime together (at, then it)",
                    "Mystery-word blending together",
                ],
                "independent_practice": [
                    "The child blends onset and rime for a set of words alone",
                    "The child builds a word family by ear from one rime",
                ],
                "mastery_check": [
                    "Blends a spoken onset and rime into the correct word",
                    "Builds several words on one rime by changing the onset",
                    "Pushes the parts together smoothly into one word",
                ],
                "spiral_review": [
                    "Warm up by blending two syllables into a word from rf-34 (pen-cil into pencil), then blend a smaller onset and rime, since onset-rime blending is the next finer step after syllable blending",
                ],
            },
            "classical": {
                "narrative_introduction": "A word can be split just before its vowel into a first sound and a chiming chunk, then joined again. The grammar stage practices this joining aloud, building word families by ear.",
                "memory_work": {
                    "chants": [
                        "Chant a word family by changing the onset: cat, hat, bat, mat, sat",
                        "Chant '/c/ + at is cat' as a steady call and response",
                    ],
                    "recitations": [
                        "Recite a rhyme built on one rime family and notice the shared chunk",
                    ],
                },
                "recitation_routine": "Begin by chanting a known word family before new blending, so the rime chunks are familiar and cumulative.",
                "history_integration": "Word families and rhyme chunks have shaped songs and verse for ages; hearing them reveals the patterns of spoken English.",
                "read_aloud_suggestions": [
                    "Rhyming readers and poems built on word families, read aloud to hear the shared rimes",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A loved rhyming book built on word families (the -at family, the -ig family)",
                ],
                "short_lesson_flow": "Enjoy a rhyming page together, then play gently: take a chunk like 'at' and make a few words by changing the first sound. Keep it short and delightful, then stop.",
                "narration_prompt": "What new word did we make when we changed the first sound? What chunk stayed the same?",
                "real_world_objects": [
                    "Objects whose names share a rime (cat, hat, bat said aloud)",
                    "Two blocks to join for the onset and the rime",
                ],
                "nature_connection": "Make a small word family by ear from a thing seen outdoors (log, dog, fog), enjoying the shared chunk.",
                "habit_focus": "The habit of attentive listening to the parts and patterns within words.",
            },
            "montessori": {
                "prepared_materials": [
                    "Picture cards for a word family (cat, hat, bat)",
                    "Two blocks, one for the onset and one for the rime, to push together",
                    "No letters: the blending games stay oral",
                ],
                "presentation": {
                    "three_period_lesson": "Adapted for sound. Naming: '/c/ + at is cat,' pushing two blocks together. Recognition: 'Blend /h/ + at.' Recall: 'What word did you make?'",
                    "steps": [
                        "Say the rime, then add an onset and blend, pushing two blocks together",
                        "Invite the child to blend with a new onset on the same rime",
                        "Build a small family by swapping onsets",
                    ],
                },
                "control_of_error": "The two blocks make the blend concrete: pushing them together yields one word, and a mismatched blend sounds wrong against the familiar rime, which the child hears.",
                "abstraction_pathway": "From pushing onset and rime blocks together, to blending sounds in the mind, narrowing from syllables toward single phonemes.",
                "extensions": [
                    "Build word families on several rimes",
                    "Blend onsets that are blends themselves later (this node stays single-sound onsets)",
                ],
                "observation_focus": "Watch whether the child blends smoothly into one word and keeps the rime steady while changing the onset.",
            },
            "unschooling": {
                "invitations": [
                    "Play 'guess my word' by saying an onset and a rime to blend",
                    "Make silly word families by ear during play",
                    "Sing rhyming songs and notice the word families in them",
                ],
                "real_world_contexts": [
                    "Word families heard in favorite rhyming songs and books",
                    "Blending games in the car or in line",
                    "Making up new words on a familiar chunk",
                ],
                "conversation_starters": [
                    "If I say /c/ and at, what word is that?",
                    "Can you make a word that ends with the 'at' chunk?",
                    "What word do we get if we change the first sound to /b/?",
                ],
                "resource_bank": [
                    "Rhyming songs and word-family books kept available",
                    "Two blocks or toys to push together for fun",
                    "Playful blending in everyday talk",
                ],
                "parent_role": "Slip onset-rime blending into real play and song, follow the child's delight, and answer genuine questions without turning it into a drill.",
                "observation_documentation": "Over time, notice whether the child blends onsets and rimes into words in play; that noticing is the assessment.",
            },
        },
        "connections": {
            "math": "Pushing two parts together to make a whole word is the same joining idea as combining parts to make a total",
            "science": "Combining components into a whole, then varying one component, mirrors simple controlled change",
            "history": "Word families and rhyme chunks shape the songs and verses of oral tradition",
        },
    },
    "rf-37": {
        "enriched": True,
        "learning_objectives": [
            "Break a spoken one-syllable word into its onset and rime (cat into /c/ + at)",
            "Say the beginning sound of a word separately from the rest",
            "Say the rime chunk that is left after the onset",
            "Segment many words into onset and rime by ear, with no letters",
        ],
        "teaching_guidance": {
            "introduction": "Onset-rime segmenting is the inverse of blending: the child pulls a one-syllable word apart into its first sound (onset) and the chunk that follows (rime), saying cat as /c/ + at. It is the last oral step before isolating single phonemes, and it uses no letters.",
            "scaffolding_sequence": [
                "Say a whole word slowly (cat), then chop off the first sound: /c/ ... at",
                "Name the onset (the first sound) and the rime (the chunk) separately",
                "Do it across a word family so the rime stays steady (hat: /h/ + at)",
                "Check by blending the parts back into the word",
                "Move to new rimes once 'at' words are easy",
            ],
            "socratic_questions": [
                "What is the very first sound in this word?",
                "What chunk is left after you take off the first sound?",
                "If you put the parts back together, do you get the word?",
            ],
            "practice_activities": [
                "Chop-the-first-sound: say a word, then split it into onset and rime",
                "Onset-and-rime cards: say each part as you touch two blocks",
                "Segment-then-blend: split a word, then blend it back to check",
            ],
            "real_world_connections": [
                "Hearing the first sound of a name, then the rest",
                "Playing split-the-word during everyday talk",
                "Noticing the shared chunk across a word family",
            ],
            "common_misconceptions": [
                "Splitting in the wrong place (ca + t): the split is before the vowel, onset then rime",
                "Saying the onset with an extra 'uh' (/cuh/): keep the first sound clean and short",
                "Thinking it needs letters: this is by ear, separating a sound from a chunk",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Splits a spoken word into onset and rime correctly",
                "Says the first sound separately from the rest",
                "Blends the parts back to confirm the split",
            ],
            "assessment_methods": [
                "oral onset-rime segmenting",
                "first-sound isolation within a word",
                "segment-then-blend check",
            ],
            "sample_assessment_prompts": [
                "Break 'cat' into its first sound and the rest",
                "What is the first sound in 'sun'? What is left?",
                "Split 'pig', then put it back together",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Break 'cat' into its first sound and the chunk that is left.",
                "expected_type": "text",
                "correct_answer": "/c/ + at",
                "hints": ["Chop off the very first sound, then say the rest"],
                "explanation": "'cat' splits into the onset /c/ and the rime 'at'.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is the first sound in 'hat'? What chunk is left?",
                "expected_type": "text",
                "correct_answer": "/h/ and at",
                "hints": ["First sound, then the rest"],
                "explanation": "'hat' splits into /h/ and the rime 'at'.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Break 'sit' into its first sound and the rest.",
                "expected_type": "text",
                "correct_answer": "/s/ + it",
                "hints": ["Chop the first sound off 'sit'"],
                "explanation": "'sit' splits into /s/ and the rime 'it'.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Break 'pig' into onset and rime.",
                "expected_type": "text",
                "correct_answer": "/p/ + ig",
                "hints": ["First sound, then the chunk"],
                "explanation": "'pig' splits into /p/ and the rime 'ig'.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is the rime chunk left in 'mat' after the first sound?",
                "expected_type": "text",
                "correct_answer": "at",
                "hints": ["Take off /m/ and say what is left"],
                "explanation": "After /m/, the rime 'at' is left.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Break 'sun' into onset and rime.",
                "expected_type": "text",
                "correct_answer": "/s/ + un",
                "hints": ["First sound /s/, then the chunk"],
                "explanation": "'sun' splits into /s/ and the rime 'un'.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Your friend splits 'cat' as 'ca' + 't'. Why is that not the onset-rime split, and what is the right split?",
                "expected_type": "text",
                "correct_answer": "the split goes before the vowel; the onset is /c/ and the rime is 'at', so cat is /c/ + at",
                "hints": ["The first sound comes off, the vowel stays with the chunk"],
                "explanation": "Onset-rime splits before the vowel: the onset is the first sound /c/ and the rime 'at' keeps the vowel, so cat is /c/ + at.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Split a word I say into its first sound and the rest, then blend it back to check. Use the word 'fan'.",
                "expected_type": "text",
                "hints": ["/f/ + an, then push back together to 'fan'"],
                "explanation": "The child should split 'fan' into /f/ and 'an', then blend back to 'fan'; reporting both the split and the rejoined word.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Break 'cat' into its first sound and the rest.",
                "type": "text",
                "correct_answer": "/c/ + at",
                "target_concept": "onset_rime_segment",
            },
            {
                "prompt": "What is the first sound in 'sun', and what chunk is left?",
                "type": "text",
                "correct_answer": "/s/ and un",
                "target_concept": "onset_isolation",
            },
            {
                "prompt": "Break 'mat' into onset and rime.",
                "type": "text",
                "correct_answer": "/m/ + at",
                "target_concept": "onset_rime_segment",
            },
            {
                "prompt": "Split 'pig' and then blend it back together.",
                "type": "open_response",
                "rubric": "Mastery: splits to /p/ + ig and blends back to pig. Proficient: splits with a hint and blends back. Developing: needs the split modeled.",
                "target_concept": "segment_then_blend",
            },
            {
                "prompt": "Tell me where we split a word for onset and rime.",
                "type": "open_response",
                "rubric": "Mastery: says the first sound comes off and the chunk (with the vowel) stays. Proficient: shows with an example. Developing: splits in the wrong place without help.",
                "target_concept": "onset_rime_concept",
            },
        ],
        "resource_guidance": {
            "required": ["no materials needed: this is purely oral listening work"],
            "recommended": ["two blocks for onset and rime", "word-family picture cards"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 10},
        "accommodations": {
            "dyslexia": "Model the clean first sound (no extra 'uh') and over-practice on one rime; use two blocks to pull the parts apart.",
            "adhd": "Make it a quick 'chop the word' game; keep one rime per round and move briskly.",
            "gifted": "Use varied rimes and ask the child to split, then blend back, longer one-syllable words.",
            "visual_learner": "Use two blocks (onset, rime) the child pulls apart to see the split.",
            "kinesthetic_learner": "Karate-chop the air between the first sound and the chunk to feel the split.",
            "auditory_learner": "A strength area: split and rejoin purely by ear.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "We can pull a short word apart into its first sound and its chunk: cat is /c/ + at. Today we split spoken words into onset and rime, all by ear, and blend them back to check.",
                "gradual_release": {
                    "i_do": "Say 'cat' slowly, then chop: '/c/ ... at.' Name the onset /c/ and the rime 'at,' then blend back to 'cat' to check.",
                    "we_do": "Split words into onset and rime together across a word family, then blend each back together.",
                    "you_do": "Child splits spoken one-syllable words into onset and rime and blends them back to confirm.",
                },
                "guided_practice": [
                    "Chop-the-first-sound together on a word family",
                    "Segment-then-blend together to check",
                ],
                "independent_practice": [
                    "The child splits a set of words into onset and rime alone",
                    "The child splits then blends back to self-check",
                ],
                "mastery_check": [
                    "Splits a word into the correct onset and rime",
                    "Says the first sound cleanly, separate from the chunk",
                    "Blends the parts back into the word",
                ],
                "spiral_review": [
                    "Warm up by blending an onset and rime into a word from rf-36 (/c/ + at into cat), then reverse it to split, since segmenting is the inverse of the blending just learned",
                ],
            },
            "classical": {
                "narrative_introduction": "What can be joined can be parted: a word splits into its first sound and its chunk. The grammar stage practices this parting aloud, the inverse of blending, sharpening the ear.",
                "memory_work": {
                    "chants": [
                        "Chant 'cat is /c/ + at; hat is /h/ + at' as a steady call and response",
                        "Chant a word family and split each word into onset and rime",
                    ],
                    "recitations": [
                        "Recite a word-family rhyme and split a few of its words into onset and rime",
                    ],
                },
                "recitation_routine": "Begin by splitting a couple of known word-family words before new segmenting, so the parting is cumulative.",
                "history_integration": "Hearing the first sound apart from the rest is a step toward the alphabetic idea that shaped written language.",
                "read_aloud_suggestions": [
                    "Word-family rhymes read aloud, then split into onset and rime by ear",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A loved word-family rhyme whose words split cleanly into onset and rime",
                ],
                "short_lesson_flow": "Enjoy a rhyming line together, then gently split one or two of its words into a first sound and a chunk, and blend them back. Keep it short and light, then stop.",
                "narration_prompt": "What is the first sound? What chunk is left? Can you put them back together?",
                "real_world_objects": [
                    "A name split into its first sound and the rest, said aloud",
                    "Two blocks pulled apart for onset and rime",
                ],
                "nature_connection": "Split the name of something seen outdoors into its first sound and chunk (sun: /s/ + un) while looking at it.",
                "habit_focus": "The habit of attentive listening: hearing a first sound apart from the rest of a word.",
            },
            "montessori": {
                "prepared_materials": [
                    "Two blocks to pull apart for onset and rime",
                    "Picture cards for word families",
                    "No letters: the segmenting games stay oral",
                ],
                "presentation": {
                    "three_period_lesson": "Adapted for sound. Naming: 'cat is /c/ and at,' pulling two blocks apart. Recognition: 'Split sun for me.' Recall: 'What is the first sound? What is left?'",
                    "steps": [
                        "Say a word, then pull two blocks apart for onset and rime",
                        "Invite the child to split the next word",
                        "Blend the parts back together to check",
                    ],
                },
                "control_of_error": "Blending the parts back into the original word is the control: if the split was wrong, the rejoined word will not match, which the child hears.",
                "abstraction_pathway": "From pulling onset and rime blocks apart, to splitting in the mind, the final oral step before isolating single phonemes.",
                "extensions": [
                    "Split words across several rimes",
                    "Split, change the onset, and blend a new word",
                ],
                "observation_focus": "Watch whether the child splits before the vowel, says a clean first sound, and can rejoin the parts.",
            },
            "unschooling": {
                "invitations": [
                    "Play 'chop the word' by splitting a word into its first sound and the rest",
                    "Split and rejoin silly words during play",
                    "Notice the first sound of words that come up in talk",
                ],
                "real_world_contexts": [
                    "Splitting the first sound off names and favorite words",
                    "Split-and-blend games in the car or at the table",
                    "Hearing word families in songs",
                ],
                "conversation_starters": [
                    "What is the very first sound in this word?",
                    "What is left if we take the first sound off?",
                    "Can you put the parts back together again?",
                ],
                "resource_bank": [
                    "Word-family songs and books kept available",
                    "Two blocks or toys to pull apart",
                    "Playful splitting in everyday talk",
                ],
                "parent_role": "Slip onset-rime splitting into real play, follow the child's curiosity, and answer genuine questions without making it a drill.",
                "observation_documentation": "Over time, notice whether the child can split words into a first sound and a chunk in play; that noticing is the assessment.",
            },
        },
        "connections": {
            "math": "Pulling a whole word into two parts is the same decomposition as breaking a number into parts",
            "science": "Separating a whole into named parts is basic analysis",
            "history": "Hearing the first sound apart from the rest is a step toward the alphabetic principle behind written language",
        },
    },
    "rf-38": {
        "enriched": True,
        "learning_objectives": [
            "Decide whether two or three spoken words begin with the same sound (alliteration)",
            "Pick the word that starts with a different beginning sound (odd one out)",
            "Generate a word that starts with a given beginning sound",
            "Enjoy alliteration in tongue twisters and spoken phrases, with no letters",
        ],
        "teaching_guidance": {
            "introduction": "Alliteration is words that share the same beginning sound, like silly snake. It trains the ear on initial sounds (a step toward isolating the first phoneme) and is entirely oral. It pairs naturally with tongue twisters and is great fun, all without letters.",
            "scaffolding_sequence": [
                "Say two words with the same beginning sound and stretch it (sun, sock: /s/)",
                "Ask whether two spoken words start with the same sound",
                "Play odd-one-out: which word starts differently (sun, sock, milk)",
                "Generate a word that starts with a given sound",
                "Enjoy a short tongue twister built on one beginning sound",
            ],
            "socratic_questions": [
                "Do these words start with the same sound?",
                "Which word starts with a different sound?",
                "Can you think of a word that starts with /b/?",
            ],
            "practice_activities": [
                "Same-or-different beginning sound on spoken pairs",
                "Odd-one-out by beginning sound",
                "Tongue-twister fun on one beginning sound",
            ],
            "real_world_connections": [
                "Hearing alliteration in character names and book titles read aloud",
                "Making a silly alliterative name for a pet",
                "Catching repeated beginning sounds in tongue twisters",
            ],
            "common_misconceptions": [
                "Matching ending sounds (that is rhyme) instead of beginning sounds: focus on the very first sound",
                "Matching by letter name rather than sound: this is by ear, listen to the sound",
                "Calling words that share a middle sound alliterative: only the beginning sound counts here",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Judges whether spoken words share a beginning sound",
                "Identifies the odd word by beginning sound",
                "Generates a word for a given beginning sound",
            ],
            "assessment_methods": [
                "same/different beginning-sound judgment",
                "odd-one-out",
                "beginning-sound generation",
            ],
            "sample_assessment_prompts": [
                "Do 'sun' and 'sock' start with the same sound?",
                "Which starts differently: bat, ball, dog?",
                "Tell me a word that starts with /m/",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Do 'sun' and 'sock' start with the same sound?",
                "expected_type": "text",
                "correct_answer": "yes",
                "hints": ["Listen to the very first sound: /s/ and /s/"],
                "explanation": "Yes, both start with the /s/ sound.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Do 'big' and 'ball' start with the same sound?",
                "expected_type": "text",
                "correct_answer": "yes",
                "hints": ["First sound of each: /b/ and /b/"],
                "explanation": "Yes, both start with the /b/ sound.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Do 'dog' and 'milk' start with the same sound?",
                "expected_type": "text",
                "correct_answer": "no",
                "hints": ["/d/ and /m/ are different first sounds"],
                "explanation": "No, dog starts with /d/ and milk with /m/.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Which word starts with a different sound: 'sun', 'sock', 'milk'?",
                "expected_type": "text",
                "correct_answer": "milk",
                "hints": ["Two start with /s/; one does not"],
                "explanation": "'milk' starts with /m/, while sun and sock start with /s/.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Which word starts with a different sound: 'cat', 'cup', 'dog'?",
                "expected_type": "text",
                "correct_answer": "dog",
                "hints": ["Two start with /c/; one does not"],
                "explanation": "'dog' starts with /d/, while cat and cup start with /c/.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Tell me a word that starts with the /b/ sound.",
                "expected_type": "text",
                "hints": ["Think of something whose first sound is /b/, like ball"],
                "explanation": "Any /b/ word works: ball, bat, book, bug. (Open: many answers are correct.)",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Your friend says 'cat' and 'kite' do not alliterate because one is spelled with c and one with k. Are they right? Listen to the sounds.",
                "expected_type": "text",
                "correct_answer": "no; both start with the /k/ sound, so they do alliterate (this is by ear, not by letters)",
                "hints": ["Say each word: what is the first sound you hear?"],
                "explanation": "Both begin with the /k/ sound, so they alliterate; alliteration is by sound, not by spelling.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Make a silly alliterative phrase: three words that all start with the same sound. Tell me your phrase.",
                "expected_type": "text",
                "hints": ["Like 'big blue ball' (all /b/)"],
                "explanation": "No single right answer; the child should produce three words sharing a beginning sound, for example 'silly singing snake' (all /s/).",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Do 'sun' and 'sock' start with the same sound?",
                "type": "text",
                "correct_answer": "yes",
                "target_concept": "beginning_sound_match",
            },
            {
                "prompt": "Which starts differently: 'bat', 'ball', 'dog'?",
                "type": "text",
                "correct_answer": "dog",
                "target_concept": "odd_one_out_beginning",
            },
            {
                "prompt": "Tell me a word that starts with the /m/ sound.",
                "type": "open_response",
                "rubric": "Mastery: gives a correct /m/ word readily. Proficient: gives one with a hint. Developing: needs the sound modeled first.",
                "target_concept": "beginning_sound_generation",
            },
            {
                "prompt": "Make a phrase where all the words start with the same sound.",
                "type": "open_response",
                "rubric": "Mastery: makes a 3-word alliterative phrase. Proficient: 2 words share the sound. Developing: 1 word with help.",
                "target_concept": "alliteration_production",
            },
            {
                "prompt": "Tell me what makes words alliterate.",
                "type": "open_response",
                "rubric": "Mastery: says they start with the same sound. Proficient: gives the idea with an example. Developing: confuses with rhyme.",
                "target_concept": "alliteration_concept",
            },
        ],
        "resource_guidance": {
            "required": ["no materials needed: this is purely oral listening work"],
            "recommended": ["tongue twisters", "alliterative picture books read aloud"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 10},
        "accommodations": {
            "dyslexia": "Stretch and exaggerate the beginning sound; keep pairs obvious at first and go slowly.",
            "adhd": "Use fast tongue twisters and odd-one-out with movement; keep rounds short.",
            "gifted": "Move to longer alliterative phrases and generating tongue twisters on a chosen sound.",
            "visual_learner": "Pair each word with a picture so the words are held in mind while listening for the beginning sound.",
            "kinesthetic_learner": "Tap or jump on the matching beginning sound; act out alliterative phrases.",
            "auditory_learner": "A strength area: lean on tongue twisters, chants, and listening games.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Words alliterate when they begin with the same sound, like silly snake. Today we listen to the first sound of words, decide if they match, find the odd one out, and make alliterative phrases, all by ear.",
                "gradual_release": {
                    "i_do": "Say 'sun, sock' and stretch the /s/: 'these start the same.' Then 'sun, milk': 'these start differently.' Model an odd-one-out: 'sun, sock, milk, milk is different.'",
                    "we_do": "Judge beginning sounds together, play odd-one-out together, and make a short alliterative phrase together.",
                    "you_do": "Child judges whether words share a beginning sound, finds the odd one out, and generates a word or phrase for a beginning sound.",
                },
                "guided_practice": [
                    "Same-or-different beginning sound together",
                    "Odd-one-out by beginning sound together",
                ],
                "independent_practice": [
                    "The child judges beginning sounds for a set of spoken words alone",
                    "The child makes an alliterative phrase",
                ],
                "mastery_check": [
                    "Judges shared beginning sounds reliably",
                    "Finds the odd word by beginning sound",
                    "Generates a word for a given beginning sound",
                ],
                "spiral_review": [
                    "Warm up with rhyme judgment from rf-31 (do these end the same?) and then contrast it with beginning-sound matching, since alliteration is the beginning-sound mirror of rhyme",
                ],
            },
            "classical": {
                "narrative_introduction": "Where rhyme chimes at the end, alliteration drums at the beginning: words that start alike. The grammar stage delights in this through tongue twisters and chant, all aloud.",
                "memory_work": {
                    "chants": [
                        "Chant an alliterative line, leaning on the repeated beginning sound",
                        "Chant a short tongue twister slowly, then a little faster",
                    ],
                    "recitations": [
                        "Memorize and recite a short tongue twister built on one beginning sound",
                    ],
                },
                "recitation_routine": "Begin by reciting a known tongue twister and naming its shared beginning sound before new alliteration work.",
                "history_integration": "Alliteration is ancient in poetry and proverb; old verse often binds lines by beginning sounds rather than rhyme.",
                "read_aloud_suggestions": [
                    "Alliterative poems and tongue twisters read aloud for their drumming beginnings",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A loved alliterative picture book or a gentle tongue-twister collection",
                ],
                "short_lesson_flow": "Enjoy an alliterative line or tongue twister together, then gently notice the repeated beginning sound. Decide if two words start alike, and make one silly phrase, then stop.",
                "narration_prompt": "What sound do all these words start with? Can you make your own that starts the same?",
                "real_world_objects": [
                    "Objects whose names share a beginning sound (sun, sock, soap)",
                    "A pet or toy given a silly alliterative name",
                ],
                "nature_connection": "On a walk, make an alliterative phrase about something seen ('busy buzzing bee'), enjoying the repeated sound.",
                "habit_focus": "The habit of attentive, delighted listening to the beginning sounds of words.",
            },
            "montessori": {
                "prepared_materials": [
                    "Baskets of small objects whose names share beginning sounds",
                    "A quiet space for the sound games",
                    "No letters: the alliteration games stay oral and precede letter work",
                ],
                "presentation": {
                    "three_period_lesson": "Adapted for sound. Naming: 'sun and sock both start with /s/.' Recognition: 'Which one starts with /s/?' Recall: 'Do these two start the same?' All spoken.",
                    "steps": [
                        "Sort objects whose names share a beginning sound",
                        "Add an object that starts differently for odd-one-out",
                        "Invite the child to name another object starting with the sound",
                    ],
                },
                "control_of_error": "Shared listening is the control: the guide says the words clearly and the beginnings either match or do not, which the child hears for themselves.",
                "abstraction_pathway": "From sorting objects by their beginning sound, to attending to the single initial sound, directly preparing initial-phoneme isolation.",
                "extensions": [
                    "Sort a basket of objects into beginning-sound groups",
                    "Build a silly alliterative phrase from chosen objects",
                ],
                "observation_focus": "Watch whether the child attends to the initial sound (not the ending or the letter) and enjoys the games.",
            },
            "unschooling": {
                "invitations": [
                    "Say silly tongue twisters together for fun",
                    "Make up alliterative names and phrases during play",
                    "Notice when book characters or signs alliterate",
                ],
                "real_world_contexts": [
                    "Alliterative names in favorite books and shows",
                    "Tongue twisters said in the car or at the table",
                    "Silly alliterative nicknames",
                ],
                "conversation_starters": [
                    "Do these words start with the same sound?",
                    "Can you make a silly phrase where everything starts with /b/?",
                    "Which of these starts differently?",
                ],
                "resource_bank": [
                    "Tongue twisters and alliterative books kept available",
                    "Playful alliteration in everyday talk",
                    "Recordings of fun, sound-rich rhymes",
                ],
                "parent_role": "Enjoy tongue twisters and alliterative play in daily life, follow the child's delight, and answer genuine questions about beginning sounds without drilling.",
                "observation_documentation": "Over time, notice whether the child hears and plays with shared beginning sounds; that noticing is the assessment.",
            },
        },
        "connections": {
            "math": "Sorting words by a shared beginning sound is classifying by an attribute, the same thinking as sorting objects by a feature",
            "science": "Listening to compare the start of sounds, as in comparing the onset of two noises",
            "history": "Alliteration is an ancient device in poetry and proverb across many cultures",
        },
    },
    "rf-39": {
        "enriched": True,
        "learning_objectives": [
            "Say the very first sound (phoneme) in a spoken word on its own",
            "Isolate the initial phoneme of many spoken words",
            "Say a clean first sound without an added 'uh'",
            "Group spoken words by their initial phoneme, with no letters",
        ],
        "teaching_guidance": {
            "introduction": "Isolating the initial phoneme is true phoneme-level work: the child says just the first sound of a spoken word (the first sound in 'sun' is /s/). It is finer than onset-rime because the answer is a single sound, and it is entirely oral, with no letters. A clean, short first sound (/s/, not /suh/) is the goal.",
            "scaffolding_sequence": [
                "Stretch a word that starts with a continuous sound (ssssun) to hear /s/",
                "Say just the first sound on its own: /s/",
                "Do it across words: sun /s/, map /m/, fish /f/",
                "Move to stop sounds (cat /k/, top /t/) said cleanly and short",
                "Sort a few spoken words by their first sound",
            ],
            "socratic_questions": [
                "What is the very first sound you hear in this word?",
                "Can you say just that first sound by itself?",
                "Which of these words starts with /s/?",
            ],
            "practice_activities": [
                "First-sound say: parent says a word, child says its first sound",
                "Stretch-and-catch: stretch the word and catch the first sound",
                "First-sound sort: group spoken words by their starting sound",
            ],
            "real_world_connections": [
                "Saying the first sound of one's own name",
                "Catching the first sound of objects around the house",
                "Sorting toys by the first sound of their names",
            ],
            "common_misconceptions": [
                "Saying the letter name instead of the sound: this is by ear, say the sound not the name",
                "Adding an 'uh' to stop sounds (/buh/ for /b/): keep it clean and short",
                "Giving the whole onset chunk instead of one sound: isolate a single first sound",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Says the correct initial phoneme of a spoken word",
                "Isolates first sounds across several words",
                "Produces a clean first sound without an added vowel",
            ],
            "assessment_methods": ["initial-phoneme isolation", "first-sound sorting", "stretch-and-catch"],
            "sample_assessment_prompts": [
                "What is the first sound in 'sun'?",
                "What is the first sound in 'map'?",
                "Which words start with /f/: fish, sun, fan?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is the first sound in 'sun'? (Say the sound, not the letter name.)",
                "expected_type": "text",
                "correct_answer": "/s/",
                "hints": ["Stretch it: sssun"],
                "explanation": "The first sound in 'sun' is /s/.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is the first sound in 'map'?",
                "expected_type": "text",
                "correct_answer": "/m/",
                "hints": ["Stretch it: mmmap"],
                "explanation": "The first sound in 'map' is /m/.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is the first sound in 'fish'?",
                "expected_type": "text",
                "correct_answer": "/f/",
                "hints": ["Stretch it: fffish"],
                "explanation": "The first sound in 'fish' is /f/.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is the first sound in 'cat'? (Keep it clean: /k/, not /kuh/.)",
                "expected_type": "text",
                "correct_answer": "/k/",
                "hints": ["A short, clean stop sound"],
                "explanation": "The first sound in 'cat' is /k/, said short and clean.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is the first sound in 'top'?",
                "expected_type": "text",
                "correct_answer": "/t/",
                "hints": ["A short, clean /t/"],
                "explanation": "The first sound in 'top' is /t/.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Which words start with /s/: 'sun', 'map', 'sock'?",
                "expected_type": "text",
                "correct_answer": "sun and sock",
                "hints": ["Say each first sound and check for /s/"],
                "explanation": "'sun' and 'sock' start with /s/; 'map' starts with /m/.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Your friend says the first sound in 'cat' is /kuh/. What is wrong, and what is the clean first sound?",
                "expected_type": "text",
                "correct_answer": "they added an 'uh'; the clean first sound is just /k/",
                "hints": ["Cut off the extra vowel sound"],
                "explanation": "They added a vowel; the clean initial phoneme is /k/ with no 'uh'.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "I will say three words; tell me the first sound of each: 'dog', 'leaf', 'pig'.",
                "expected_type": "text",
                "hints": ["Say each word, catch just the first sound"],
                "explanation": "The first sounds are /d/, /l/, /p/; the child should isolate one clean first sound per word.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "What is the first sound in 'sun'?",
                "type": "text",
                "correct_answer": "/s/",
                "target_concept": "initial_phoneme",
            },
            {
                "prompt": "What is the first sound in 'map'?",
                "type": "text",
                "correct_answer": "/m/",
                "target_concept": "initial_phoneme",
            },
            {
                "prompt": "Which words start with /f/: 'fish', 'sun', 'fan'?",
                "type": "text",
                "correct_answer": "fish and fan",
                "target_concept": "initial_phoneme_sort",
            },
            {
                "prompt": "Say the first sound in 'cat' cleanly.",
                "type": "open_response",
                "rubric": "Mastery: says a clean /k/ with no added vowel. Proficient: says /k/ with a slight 'uh'. Developing: gives the letter name or whole onset.",
                "target_concept": "clean_initial_phoneme",
            },
            {
                "prompt": "Tell me what we listen for when we find a word's first sound.",
                "type": "open_response",
                "rubric": "Mastery: says the single sound at the very start (not the letter name). Proficient: gives the idea with an example. Developing: confuses sound with letter name.",
                "target_concept": "initial_phoneme_concept",
            },
        ],
        "resource_guidance": {
            "required": ["no materials needed: this is purely oral listening work"],
            "recommended": [
                "small objects or picture cards to sort by first sound",
                "a mirror to watch the mouth make the first sound",
            ],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 10},
        "accommodations": {
            "dyslexia": "Start with continuous first sounds that can be stretched (/s/, /m/, /f/) before stop sounds; use a mirror to watch the mouth.",
            "adhd": "Use quick first-sound sorting with movement; keep rounds short and lively.",
            "gifted": "Move quickly to stop sounds and to sorting many words, and pair with the final-phoneme work that follows.",
            "visual_learner": "Use a mirror so the child sees the mouth shape that makes the first sound.",
            "kinesthetic_learner": "Tap the chin or clap on the first sound; sort objects physically by first sound.",
            "auditory_learner": "A strength area: stretch and catch first sounds purely by ear.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Every word begins with a single sound. Today we say just the first sound of a word, like /s/ in sun, all by ear, keeping the sound clean with no extra 'uh'.",
                "gradual_release": {
                    "i_do": "Stretch 'ssssun' and say, 'The first sound is /s/.' Do 'mmmap': '/m/.' Then a stop sound: 'cat... /k/,' clean and short.",
                    "we_do": "Find first sounds together across several words, stretching continuous sounds and keeping stop sounds clean, and sort a few words by first sound together.",
                    "you_do": "Child says the first sound of spoken words on their own and sorts words by their first sound.",
                },
                "guided_practice": [
                    "Stretch-and-catch the first sound together",
                    "First-sound sort together",
                ],
                "independent_practice": [
                    "The child says the first sound of a set of words alone",
                    "The child sorts objects by their first sound",
                ],
                "mastery_check": [
                    "Says the correct initial phoneme of a word",
                    "Isolates first sounds across several words",
                    "Keeps the first sound clean (no added vowel)",
                ],
                "spiral_review": [
                    "Warm up with the broad phoneme work of rf-02 (hearing and working with the sounds in spoken words) and then narrow to saying just the single first sound, since isolating the initial phoneme is a precise case of that phonemic awareness",
                ],
            },
            "classical": {
                "narrative_introduction": "Beneath rhyme, syllable, and onset lies the single sound, the phoneme. The grammar stage now isolates the first of these, said cleanly and aloud, the gateway to the alphabetic principle.",
                "memory_work": {
                    "chants": [
                        "Chant a list of words and their first sounds: 'sun /s/, map /m/, fish /f/'",
                        "Chant a clean stop-sound list: 'cat /k/, top /t/, pig /p/'",
                    ],
                    "recitations": [
                        "Recite an alliterative line and isolate its shared first sound",
                    ],
                },
                "recitation_routine": "Begin by isolating the first sound of a few known words before new work, keeping the sounds clean and cumulative.",
                "history_integration": "Hearing the single first sound is the very idea that gave rise to the alphabet, one mark for one sound.",
                "read_aloud_suggestions": [
                    "Sound-rich poems read aloud, then mined for the first sound of chosen words",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A loved book with clear, sound-rich words to listen to for first sounds",
                ],
                "short_lesson_flow": "Enjoy a short text together, then gently catch the first sound of a couple of its words, stretching continuous sounds. Sort two or three words by first sound, then stop.",
                "narration_prompt": "What is the very first sound in this word? Can you say just that sound?",
                "real_world_objects": [
                    "Familiar objects whose first sounds are caught and named",
                    "A mirror to watch the mouth make the first sound",
                ],
                "nature_connection": "Catch the first sound of things seen outdoors (leaf /l/, rock /r/) while looking at them.",
                "habit_focus": "The habit of fine, attentive listening to the single first sound of a word.",
            },
            "montessori": {
                "prepared_materials": [
                    "Baskets of small objects for first-sound sorting (the classic I Spy sound game)",
                    "A mirror for watching the mouth",
                    "No letters: the first-sound games precede the sandpaper letters",
                ],
                "presentation": {
                    "three_period_lesson": "Adapted for sound. Naming: 'sun begins with /s/.' Recognition: 'Find something that begins with /s/.' Recall: 'What sound does sock begin with?' Sounds only, never letter names.",
                    "steps": [
                        "Play I Spy with a beginning sound the child hears easily",
                        "Stretch continuous first sounds, then keep stop sounds clean",
                        "Sort a basket of objects by their first sound",
                    ],
                },
                "control_of_error": "The shared listening and sorting are the control: an object placed in the wrong first-sound group sounds wrong when re-said, which the child hears and fixes.",
                "abstraction_pathway": "From the oral I Spy sound game, to isolating the single first phoneme, the step Montessori places just before joining sounds to sandpaper letters; this node stays oral.",
                "extensions": [
                    "Sort many objects by first sound",
                    "Move toward the final-sound work that follows",
                ],
                "observation_focus": "Watch whether the child says a clean single first sound (not a letter name or a chunk) and sorts accurately.",
            },
            "unschooling": {
                "invitations": [
                    "Play I Spy by first sound on a walk or a drive",
                    "Catch the first sound of names and favorite words in talk",
                    "Sort toys or snacks by their first sound for fun",
                ],
                "real_world_contexts": [
                    "First sounds of family names and pets",
                    "I Spy by beginning sound in the car",
                    "Catching first sounds of objects around the house",
                ],
                "conversation_starters": [
                    "What sound does your name start with?",
                    "I am thinking of something that starts with /b/, can you guess it?",
                    "What is the very first sound in this word?",
                ],
                "resource_bank": [
                    "A habit of I Spy by sound in daily life",
                    "Small objects to sort by first sound",
                    "Sound-rich songs and books kept available",
                ],
                "parent_role": "Play first-sound games in the flow of the day, keep the sounds clean and playful, and answer genuine questions without turning it into a lesson.",
                "observation_documentation": "Over time, notice whether the child catches and says the first sound of words in play; that noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Picking out the single first sound is isolating one element from a set, the same precision as identifying one item in a group",
            "science": "Attending to the very onset of a sound is careful observation of a single feature",
            "history": "Hearing one sound at the start of a word is the insight behind the alphabet, one symbol per sound",
        },
    },
    "rf-40": {
        "enriched": True,
        "learning_objectives": [
            "Say the very last sound (phoneme) in a spoken word on its own",
            "Isolate the final phoneme of many spoken words",
            "Tell the difference between a word's first sound and its last sound",
            "Group spoken words by their ending sound, with no letters",
        ],
        "teaching_guidance": {
            "introduction": "Isolating the final phoneme is the partner of initial-phoneme work: the child says just the last sound of a spoken word (the last sound in 'cat' is /t/). The ending is often harder to hear than the beginning, so words ending in continuous sounds (/s/, /m/, /f/) come first. It is entirely oral, with no letters.",
            "scaffolding_sequence": [
                "Stretch the end of a word with a continuous final sound (busss) to hear /s/",
                "Say just the last sound on its own: /s/",
                "Do it across words: bus /s/, ham /m/, leaf /f/",
                "Move to stop sounds at the end (cat /t/, dog /g/) said cleanly",
                "Contrast first and last sound of the same word (cat: /k/ first, /t/ last)",
            ],
            "socratic_questions": [
                "What is the very last sound you hear in this word?",
                "Can you say just that ending sound by itself?",
                "What is the first sound, and what is the last sound, of this word?",
            ],
            "practice_activities": [
                "Last-sound say: parent says a word, child says its last sound",
                "Stretch-the-end: stretch the final sound and catch it",
                "First-or-last: name whether a given sound is at the start or the end",
            ],
            "real_world_connections": [
                "Saying the last sound of one's own name",
                "Catching the ending sound of objects around the house",
                "Sorting words by their ending sound",
            ],
            "common_misconceptions": [
                "Giving the first sound when asked for the last: point attention to the very end of the word",
                "Saying the letter name instead of the sound: this is by ear, the sound not the name",
                "Adding an 'uh' to a final stop sound (/tuh/ for /t/): keep it clean and short",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Says the correct final phoneme of a spoken word",
                "Isolates ending sounds across several words",
                "Distinguishes a word's first sound from its last sound",
            ],
            "assessment_methods": ["final-phoneme isolation", "first-vs-last discrimination", "ending-sound sorting"],
            "sample_assessment_prompts": [
                "What is the last sound in 'bus'?",
                "What is the last sound in 'cat'?",
                "In 'map', what is the first sound and what is the last sound?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is the last sound in 'bus'? (Say the sound, not the letter name.)",
                "expected_type": "text",
                "correct_answer": "/s/",
                "hints": ["Stretch the end: busss"],
                "explanation": "The last sound in 'bus' is /s/.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is the last sound in 'ham'?",
                "expected_type": "text",
                "correct_answer": "/m/",
                "hints": ["Stretch the end: hammm"],
                "explanation": "The last sound in 'ham' is /m/.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is the last sound in 'leaf'?",
                "expected_type": "text",
                "correct_answer": "/f/",
                "hints": ["Stretch the end: leafff"],
                "explanation": "The last sound in 'leaf' is /f/.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is the last sound in 'cat'? (Keep it clean: /t/, not /tuh/.)",
                "expected_type": "text",
                "correct_answer": "/t/",
                "hints": ["A short, clean stop sound at the end"],
                "explanation": "The last sound in 'cat' is /t/, said short and clean.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is the last sound in 'dog'?",
                "expected_type": "text",
                "correct_answer": "/g/",
                "hints": ["A short, clean /g/ at the end"],
                "explanation": "The last sound in 'dog' is /g/.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "In the word 'map', what is the first sound and what is the last sound?",
                "expected_type": "text",
                "correct_answer": "first /m/, last /p/",
                "hints": ["The very start, then the very end"],
                "explanation": "In 'map' the first sound is /m/ and the last sound is /p/.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "I say the sound /n/ is in 'sun'. Is /n/ the first sound or the last sound of 'sun'? How do you know?",
                "expected_type": "text",
                "correct_answer": "the last sound; sun starts with /s/ and ends with /n/",
                "hints": ["Say sun slowly: what is at the very end?"],
                "explanation": "/n/ is the last sound of 'sun' (which starts with /s/ and ends with /n/).",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "I will say three words; tell me the last sound of each: 'pig', 'bell', 'cup'.",
                "expected_type": "text",
                "hints": ["Say each word, catch just the ending sound"],
                "explanation": "The last sounds are /g/, /l/, /p/; the child should isolate one clean final sound per word.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "What is the last sound in 'bus'?",
                "type": "text",
                "correct_answer": "/s/",
                "target_concept": "final_phoneme",
            },
            {
                "prompt": "What is the last sound in 'cat'?",
                "type": "text",
                "correct_answer": "/t/",
                "target_concept": "final_phoneme",
            },
            {
                "prompt": "In 'map', what is the first sound and what is the last sound?",
                "type": "text",
                "correct_answer": "first /m/, last /p/",
                "target_concept": "first_vs_last",
            },
            {
                "prompt": "Say the last sound in 'dog' cleanly.",
                "type": "open_response",
                "rubric": "Mastery: says a clean /g/ with no added vowel. Proficient: says /g/ with a slight 'uh'. Developing: gives the first sound or the letter name.",
                "target_concept": "clean_final_phoneme",
            },
            {
                "prompt": "Tell me how the first sound and the last sound of a word are different.",
                "type": "open_response",
                "rubric": "Mastery: says one is at the very start and one at the very end. Proficient: shows with an example. Developing: confuses the two without help.",
                "target_concept": "first_last_concept",
            },
        ],
        "resource_guidance": {
            "required": ["no materials needed: this is purely oral listening work"],
            "recommended": [
                "small objects or picture cards to sort by ending sound",
                "a mirror to watch the mouth finish the word",
            ],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 10},
        "accommodations": {
            "dyslexia": "Final sounds are hard; begin with words ending in continuous sounds that can be stretched, and go slowly with much modeling.",
            "adhd": "Use quick ending-sound games with movement; keep words short and rounds brief.",
            "gifted": "Move to stop-sound endings and to naming both first and last sounds quickly, preparing full segmenting.",
            "visual_learner": "Use a mirror so the child sees the mouth shape that finishes the word.",
            "kinesthetic_learner": "Tap or clap on the ending sound; sort objects by their last sound.",
            "auditory_learner": "A strength area: stretch and catch ending sounds purely by ear.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Every word ends with a single sound, too. Today we say just the last sound of a word, like /t/ in cat, all by ear, and we tell the first sound from the last sound.",
                "gradual_release": {
                    "i_do": "Stretch 'busss' and say, 'The last sound is /s/.' Do 'hammm': '/m/.' Then a stop ending: 'cat... /t/,' clean and short. Contrast: 'cat starts /k/, ends /t/.'",
                    "we_do": "Find last sounds together across several words, stretching continuous endings and keeping stop endings clean, and name first versus last sounds together.",
                    "you_do": "Child says the last sound of spoken words on their own and tells a word's first sound from its last sound.",
                },
                "guided_practice": [
                    "Stretch-the-end and catch the last sound together",
                    "First-or-last: name where a given sound is, together",
                ],
                "independent_practice": [
                    "The child says the last sound of a set of words alone",
                    "The child sorts words by their ending sound",
                ],
                "mastery_check": [
                    "Says the correct final phoneme of a word",
                    "Isolates ending sounds across several words",
                    "Distinguishes the first sound from the last sound",
                ],
                "spiral_review": [
                    "Warm up by isolating the first sound of a few words from rf-39, then turn attention to the very end of the word, since hearing the last sound builds directly on the initial-sound work just learned",
                ],
            },
            "classical": {
                "narrative_introduction": "As a word has a first sound, so it has a last. The grammar stage now isolates the final phoneme, said cleanly and aloud, completing the ear's grasp of a word's edges.",
                "memory_work": {
                    "chants": [
                        "Chant a list of words and their last sounds: 'bus /s/, ham /m/, leaf /f/'",
                        "Chant first-and-last pairs: 'cat: /k/ ... /t/'",
                    ],
                    "recitations": [
                        "Recite a short verse and isolate the last sound of chosen words",
                    ],
                },
                "recitation_routine": "Begin by isolating the last sound of a few known words before new work, keeping the sounds clean and cumulative.",
                "history_integration": "Hearing each edge sound of a word completes the insight that words are built of separate sounds, the basis of the alphabet.",
                "read_aloud_suggestions": [
                    "Sound-rich poems read aloud, then mined for the last sound of chosen words",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A loved book with clear, sound-rich words to listen to for ending sounds",
                ],
                "short_lesson_flow": "Enjoy a short text together, then gently catch the last sound of a couple of its words, stretching continuous endings. Tell the first sound from the last for one word, then stop.",
                "narration_prompt": "What is the very last sound in this word? And what was its first sound?",
                "real_world_objects": [
                    "Familiar objects whose ending sounds are caught and named",
                    "A mirror to watch the mouth finish the word",
                ],
                "nature_connection": "Catch the last sound of things seen outdoors (leaf /f/, rock /k/) while looking at them.",
                "habit_focus": "The habit of fine, attentive listening to both edges of a spoken word.",
            },
            "montessori": {
                "prepared_materials": [
                    "Baskets of small objects for ending-sound sorting",
                    "A mirror for watching the mouth finish the word",
                    "No letters: the ending-sound games precede the sandpaper letters",
                ],
                "presentation": {
                    "three_period_lesson": "Adapted for sound. Naming: 'bus ends with /s/.' Recognition: 'Find something that ends with /s/.' Recall: 'What sound does ham end with?' Sounds only, never letter names.",
                    "steps": [
                        "Play the ending-sound I Spy with words ending in continuous sounds",
                        "Stretch continuous endings, then keep stop endings clean",
                        "Sort a basket of objects by their ending sound",
                    ],
                },
                "control_of_error": "The shared listening and sorting are the control: an object placed in the wrong ending-sound group sounds wrong when re-said, which the child hears and fixes.",
                "abstraction_pathway": "From the oral ending-sound game, to isolating the final phoneme, completing the edge-sound work just before full segmenting and the sandpaper letters; this node stays oral.",
                "extensions": [
                    "Sort objects by ending sound",
                    "Name both first and last sounds, preparing full segmenting",
                ],
                "observation_focus": "Watch whether the child says a clean single last sound (not the first sound or a letter name) and sorts accurately.",
            },
            "unschooling": {
                "invitations": [
                    "Play 'what does it end with?' on a walk or a drive",
                    "Catch the last sound of names and favorite words in talk",
                    "Sort toys or snacks by their ending sound for fun",
                ],
                "real_world_contexts": [
                    "Ending sounds of family names and pets",
                    "Ending-sound I Spy in the car",
                    "Catching last sounds of objects around the house",
                ],
                "conversation_starters": [
                    "What sound does your name end with?",
                    "I am thinking of something that ends with /t/, can you guess it?",
                    "What is the very last sound in this word?",
                ],
                "resource_bank": [
                    "A habit of ending-sound games in daily life",
                    "Small objects to sort by last sound",
                    "Sound-rich songs and books kept available",
                ],
                "parent_role": "Play ending-sound games in the flow of the day, keep the sounds clean and playful, and answer genuine questions without turning it into a lesson.",
                "observation_documentation": "Over time, notice whether the child catches and says the last sound of words in play; that noticing replaces any test.",
            },
        },
        "connections": {
            "math": "Telling the first sound from the last sound is attending to position in a sequence, like first and last in a line",
            "science": "Attending to the very end of a sound is careful observation of when something stops",
            "history": "Hearing each separate sound in a word is the insight that produced alphabetic writing",
        },
    },
}
