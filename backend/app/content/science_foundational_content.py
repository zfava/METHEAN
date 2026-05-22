"""Pre-enriched content for Science Foundational template nodes."""

SCIENCE_FOUNDATIONAL_CONTENT = {
    "sf-01": {
        "enriched": True,
        "learning_objectives": [
            "Use all five senses (sight, hearing, touch, smell, taste where safe) to observe objects and the natural world",
            "Describe an object using at least 3 senses with specific, accurate language",
            "Record observations in a science notebook using both words and drawings",
            "Explain that science begins with careful observation — paying close attention to what is really there",
        ],
        "teaching_guidance": {
            "introduction": "Science begins with paying attention. Before a child can understand WHY leaves change color or HOW magnets work, they must learn to OBSERVE — to really look, listen, touch, smell, and (when safe) taste the world around them. The five senses are a scientist's first tools. A child who can describe an apple as 'red, smooth, cool, slightly sweet-smelling, and crunchy when bitten' is doing real science: careful, accurate observation using multiple senses. This foundational skill makes every future science topic richer.",
            "scaffolding_sequence": [
                "Start with a familiar object (an apple, a pinecone, a rock): hold it, look at it carefully, and describe what you SEE",
                "Add another sense: close your eyes and describe what you FEEL. Is it smooth? Rough? Heavy? Warm? Cool?",
                "Add hearing: shake it, tap it, roll it. Does it make a sound? Describe what you HEAR.",
                "Add smell: carefully smell the object. Describe the smell. Not everything has a smell — that's an observation too!",
                "Add taste (only with food items): describe the taste using specific words (sweet, sour, salty, bitter, crunchy, soft)",
                "Record the observations: draw the object in a science notebook and write describing words for each sense used",
                "Go outdoors: observe a tree, a patch of grass, or the sky using all applicable senses. Record in the notebook.",
                "Compare observations: two children observe the same object. Did they notice the same things? Different things? Both are valid science.",
            ],
            "socratic_questions": [
                "You said the rock is 'brown.' Can you be more specific? What KIND of brown? Are there other colors mixed in?",
                "Close your eyes and hold this pinecone. Describe everything your hands can tell you about it without looking.",
                "We're standing outside. What sounds do you hear? How many different sounds can you count?",
                "Why do you think scientists write down their observations instead of just remembering them?",
            ],
            "practice_activities": [
                "Mystery bag: put objects in a paper bag. The child reaches in WITHOUT looking and describes what they feel. Can they identify the object by touch alone?",
                "Sound walk: go outside, stand still for 2 minutes, and list every different sound you hear. Compare lists with a family member.",
                "Nature observation station: place a natural object (leaf, flower, stone) on a table with a magnifying glass. The child draws it and writes observations for each sense.",
                "Smell jars: put different items in opaque jars (cinnamon, coffee, lemon peel, soil). The child identifies each by smell alone.",
            ],
            "real_world_connections": [
                "Cooking uses all five senses: watching bread rise (sight), hearing it sizzle (hearing), feeling dough (touch), smelling it bake (smell), tasting the result (taste)",
                "Doctors use observation: looking at skin color, listening with a stethoscope, feeling for swelling — medical science starts with senses",
                "Weather observation is daily five-senses science: see the clouds, feel the wind, hear the rain, smell the air after a storm",
                "Nature walks are automatic science labs: every step brings new things to observe with every sense",
            ],
            "common_misconceptions": [
                "Thinking observation means only LOOKING — observation uses ALL available senses, not just sight",
                "Believing that descriptions should be vague ('it's nice' or 'it's brown') — scientific observation requires SPECIFIC language: 'The bark is rough, dark gray with light patches, and smells earthy.'",
                "Assuming observation is passive — good observation is ACTIVE: the child chooses what to focus on, examines carefully, and records precisely",
                "Thinking we should always use all 5 senses — taste should only be used with known-safe food items. Safety is part of science too.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Describes an object using at least 4 senses with specific language",
                "Records observations accurately in a science notebook with drawings and words",
                "Explains that science starts with careful observation",
            ],
            "proficiency_indicators": [
                "Describes using 2-3 senses",
                "Records observations but with limited detail",
            ],
            "developing_indicators": [
                "Describes using only sight",
                "Uses vague language ('it's nice') rather than specific observations",
            ],
            "assessment_methods": [
                "multi-sense observation exercise",
                "science notebook review",
                "observation comparison",
            ],
            "sample_assessment_prompts": [
                "Describe this object using as many senses as you can. Be as specific as possible.",
                "Show me your science notebook. Point to an observation where you used 3 or more senses.",
                "Why is careful observation important in science?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Name the five senses and the body part used for each one.",
                "expected_type": "text",
                "hints": ["Think about: eyes see, ears hear... what about the other three?"],
                "explanation": "The five senses: sight (eyes), hearing (ears), touch (skin/hands), smell (nose), taste (tongue). Each sense gives us different information about the world around us.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which sense would you use to find out if a rock is smooth or rough?",
                "expected_type": "multiple_choice",
                "options": ["Sight", "Touch", "Hearing", "Taste"],
                "correct_answer": "Touch",
                "hints": ["Smooth and rough describe how something FEELS."],
                "explanation": "Touch tells you about texture: smooth, rough, bumpy, soft, hard. You would hold the rock and feel its surface with your fingers.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Go outside and stand still for 1 minute. List at least 5 things you observe using different senses.",
                "expected_type": "text",
                "hints": ["Use multiple senses: What do you SEE? HEAR? FEEL (wind, temperature)? SMELL?"],
                "explanation": "A good observation list uses multiple senses: 'I see white clouds. I hear birds singing. I feel warm wind on my face. I smell cut grass. I see an ant carrying a crumb.' Specific, multi-sense observations are the foundation of science.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: Scientists should always taste things they are observing.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["Is it safe to taste everything? What about chemicals, unknown plants, or dirty things?"],
                "explanation": "False! Taste should ONLY be used with items known to be safe (food items). Never taste unknown substances, chemicals, or wild plants. Safety is an important part of scientific practice.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Pick any natural object near you (a leaf, rock, flower, or piece of fruit). Draw it in your science notebook and describe it using at least 3 different senses. Be as specific as possible.",
                "expected_type": "text",
                "hints": [
                    "Look at it carefully: color, shape, size. Feel it: texture, weight, temperature. Smell it. Describe each observation with precise words."
                ],
                "explanation": "A strong observation includes specific details for each sense used. Example for a leaf: 'SIGHT: oval shape, dark green on top, lighter underneath, veins branching from the center. TOUCH: smooth and waxy on top, slightly fuzzy underneath, thin and flexible. SMELL: faintly earthy, fresh.' This level of detail is real scientific observation.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Describe this object using all applicable senses.",
                "type": "open_response",
                "target_concept": "multi_sense_observation",
                "rubric": "Mastery: 4+ senses with specific language. Proficient: 2-3 senses. Developing: sight only, vague descriptions.",
            },
            {
                "prompt": "Why do scientists write down their observations?",
                "type": "open_response",
                "target_concept": "recording_observations",
                "rubric": "Mastery: explains accuracy, memory, sharing, comparison. Proficient: says 'to remember.' Developing: cannot explain.",
            },
        ],
        "resource_guidance": {
            "required": [
                "science notebook (blank or lined)",
                "natural objects for observation (rocks, leaves, shells)",
            ],
            "recommended": ["magnifying glass", "collection of objects with interesting textures and smells"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Observation is primarily sensory, not text-based. Record observations through drawing with verbal labels dictated to parent. Voice recordings of observations. Real objects over written descriptions.",
            "adhd": "Outdoor observation walks channel energy. Mystery bag and smell jars are engaging games. Keep indoor observation to 10 minutes. Drawing observations keeps hands busy. Movement-based: walk to find things to observe.",
            "gifted": "Introduce the concept of quantitative vs qualitative observations (measuring vs describing). Begin using a magnifying glass for micro-observations. Start a year-long observation project (a tree through the seasons).",
            "visual_learner": "Magnifying glass work. Detailed drawings. Color comparisons. Close-up photography of natural objects.",
            "kinesthetic_learner": "Touch-based exploration is primary. Nature walks with physical collection. Sorting objects by texture. Building with natural materials.",
            "auditory_learner": "Sound walks and listening exercises. Describe observations aloud before drawing. Discuss observations as a conversation.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Science begins with observation: paying close, careful attention to what is really there. A scientist's first tools are the five senses, sight, hearing, touch, smell, and, with safe foods, taste. Today we observe objects and the natural world with all five senses, describe what we find in specific, accurate words, and record our observations in a science notebook with both words and drawings.",
                "gradual_release": {
                    "i_do": "Hold an object, an apple or a pinecone, and observe it aloud sense by sense: I see deep red with a few green streaks; I feel a smooth, cool, firm skin; I hear a faint tap when I flick it. Show that plain red becomes deep red with green streaks when looked at closely, and record the observation in the notebook with a drawing.",
                    "we_do": "Observe an object together, naming what each sense tells us, pressing for specific words rather than vague ones, and recording the observations side by side in our notebooks.",
                    "you_do": "Child observes an object using at least three senses, describes each observation in specific language, and records it in the science notebook with words and a drawing.",
                },
                "guided_practice": [
                    "Describe a familiar object using sight, then add touch, then hearing and smell",
                    "Turn a vague description into a specific one: brown into reddish-brown with darker speckles",
                    "Record an observation in the science notebook with a labeled drawing",
                ],
                "independent_practice": [
                    "Observe a natural object outdoors with all applicable senses and record it in the notebook",
                    "Build a multi-sense observation entry for several different objects",
                ],
                "mastery_check": [
                    "Describe an object using at least three senses with specific, accurate words",
                    "Record an observation in the science notebook with both words and a drawing",
                    "Explain that science begins with careful observation",
                ],
                "spiral_review": [
                    "Revisit the five senses and the body part each uses, naming them before each new observation",
                ],
            },
            "classical": {
                "narrative_introduction": "Before a single law of nature can be learned, the eye and the ear must be taught to attend. The natural philosophers of old made their discoveries first by looking, long and closely, at the world as it truly is. The five senses are the mind's windows onto creation, and to observe well, to see precisely and name exactly, is the first discipline of every science.",
                "memory_work": {
                    "chants": [
                        "Chant the five senses and their organs: sight with the eyes, hearing with the ears, touch with the skin, smell with the nose, taste with the tongue",
                        "Chant the observer's rule: look closely, name exactly, and write it down",
                    ],
                    "recitations": [
                        "Recite that science begins with careful observation, the attentive use of all the senses upon the world as it really is",
                    ],
                },
                "copywork": [
                    "Copy a sentence of fine, exact natural description and a list of precise sense words: smooth, rough, translucent, pungent, brittle",
                ],
                "recitation_routine": "Begin each lesson by reciting the five senses and the observer's rule before any new observation is made.",
                "history_integration": "Tell that the great naturalists, who first described the plants, the animals, and the heavens, built all their knowledge upon patient observation, and that careful looking has always come before careful explaining.",
                "read_aloud_suggestions": [
                    "A passage of fine nature writing, rich in exact and vivid description, read aloud so the ear meets the language of careful observation",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A beautifully illustrated nature book with real artwork that invites close looking, never a dry textbook",
                ],
                "short_lesson_flow": "Go outdoors, unhurried, and let the child choose one thing to attend to, a leaf, a stone, a beetle. Look at it long and quietly, with no rush to name or explain. Then the child draws it from life in the nature notebook, as truly as they can, and tells you what they noticed with each sense. Stop while wonder is still fresh.",
                "narration_prompt": "Tell me everything you noticed about the thing you observed. What did your eyes see, your hands feel, your nose smell?",
                "real_world_objects": [
                    "A nature notebook for drawing from life",
                    "Natural objects gathered on a walk: leaves, stones, feathers, seed pods",
                    "A magnifying glass for looking closely",
                ],
                "nature_connection": "Nature study is the heart of this lesson: the whole out-of-doors is the object of observation, and the child returns to the same tree, the same patch of ground, again and again, learning to see it truly.",
                "habit_focus": "The habit of attention: looking at a real thing long enough and closely enough to see what is truly there.",
            },
            "montessori": {
                "prepared_materials": [
                    "The sensorial materials that refine each sense: the rough and smooth boards, the color tablets, the sound cylinders, the smelling bottles",
                    "Natural objects on an observation tray with a magnifying glass",
                    "A science notebook for recording observations",
                ],
                "presentation": {
                    "three_period_lesson": "With the smelling bottles or the rough and smooth boards: this surface is rough, this one is smooth; show me the rough one; is this rough or smooth?",
                    "steps": [
                        "The child refines a sense with its sensorial material, sorting rough from smooth, matching the sound cylinders, pairing the smelling bottles",
                        "The child carries the refined sense to a real natural object, observing it closely with eyes, hands, and nose",
                        "The child records the observation in the science notebook with a careful drawing and describing words",
                    ],
                },
                "control_of_error": "The sensorial materials carry their own control: the sound cylinders pair exactly, the color tablets grade in one true order, and a mismatch is plain to the trained sense, so the child corrects without being told.",
                "abstraction_pathway": "From isolating and refining each sense with the sensorial materials, to turning the sharpened senses upon the real natural world, toward observing precisely and recording what is truly there.",
                "extensions": [
                    "Observe the same object across the day, or the seasons, noting what changes",
                    "Sort natural objects by a sensory quality: by texture, by color, by smell",
                    "Use the magnifying glass for close, detailed observation",
                ],
                "observation_focus": "Watch for the child observing with more than the eyes alone, choosing precise describing words, and attending closely before reaching to name.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a basket of interesting natural objects, with varied textures and smells, within reach",
                    "Leave out a magnifying glass, a notebook, and good drawing materials",
                    "Let observation belong to ordinary outings: walks, the garden, the kitchen",
                ],
                "real_world_contexts": [
                    "Noticing the world on a walk: the smell of rain, the sound of birds, the feel of bark",
                    "Observing in the kitchen: how dough feels, how bread smells baking, how fruit tastes",
                    "Watching the weather and the sky change with the senses",
                    "Examining a found treasure, a shell, a feather, a stone, closely",
                ],
                "conversation_starters": [
                    "What do you notice about this? Use more than just your eyes.",
                    "Close your eyes, what does it feel like, smell like, sound like?",
                    "Can you describe that more exactly? What kind of brown is it?",
                ],
                "resource_bank": [
                    "A magnifying glass and a notebook kept handy",
                    "The whole out-of-doors, full of things to observe",
                    "Beautiful nature books and field guides to browse",
                ],
                "parent_role": "Wonder aloud at what you notice, the smell of the air, the sound of the wind, and invite the child to look closer with you. Welcome their observations with genuine interest, ask gently for more exact words, and let the child's own curiosity choose what to attend to.",
                "observation_documentation": "Over time, note whether the child observes with all the senses, describes things in specific words, records what they notice, and understands that paying close attention is where science starts. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Descriptive language in science builds vocabulary used in reading and writing: smooth, rough, translucent, pungent, brittle",
            "math": "Measurement is quantitative observation: how long, how heavy, how many. Science observation leads naturally to measurement.",
            "history": "Historical observation: examining artifacts uses the same careful looking skills as science observation",
        },
    },
    "sf-02": {
        "enriched": True,
        "learning_objectives": [
            "Distinguish living things from nonliving things by identifying characteristics of life",
            "List at least 4 characteristics of living things: they grow, reproduce, need food and water, and respond to their environment",
            "Sort 10 objects correctly into living and nonliving categories with explanations",
            "Identify tricky cases (dead things, things that seem alive but aren't) and explain the reasoning",
        ],
        "teaching_guidance": {
            "introduction": "One of the first big questions in science is: what makes something ALIVE? A dog is alive. A rock is not. But WHY? Living things share characteristics: they grow, they reproduce (make more of themselves), they need food and water, and they respond to their environment (a plant turns toward sunlight, a cat runs from a loud noise). This classification — living vs nonliving — is the foundation of all biology. Once a child can identify what is alive, they can begin to study HOW life works.",
            "scaffolding_sequence": [
                "Take a nature walk and collect 10 items: leaves, rocks, sticks, feathers, acorns, pebbles, flowers, pine cones, soil, shells",
                "Sort the collection into two piles: 'things that are or were alive' and 'things that were never alive'",
                "Introduce the characteristics of life: grows, reproduces, needs food/water, responds to environment. Check each item against these criteria.",
                "Discuss tricky cases: a dead leaf WAS alive (it's a previously living thing). A cloud MOVES but was never alive (movement alone doesn't mean life).",
                "Classify pictures of objects: a fire (not alive — it grows and moves but doesn't reproduce or eat), a crystal (not alive — it 'grows' but doesn't reproduce or eat)",
                "Introduce the term 'organism' for living things: plants, animals, fungi, and bacteria are all organisms",
                "Apply to the child's world: 'Is your pet alive? Is your toy? How do you know?'",
                "Create a living/nonliving poster with drawings and labels for each category",
            ],
            "socratic_questions": [
                "A fire grows and moves. Is it alive? Why or why not?",
                "A dead tree is lying on the ground. Is it a living thing or a nonliving thing? It WAS alive... so what is it now?",
                "Your toy robot moves and makes sounds. Is it alive? What characteristics of life is it missing?",
                "If an alien visited Earth, how would they figure out which things here are alive?",
            ],
            "practice_activities": [
                "Nature walk sorting: collect 10 natural objects and sort them into living, once-living, and never-living categories",
                "Living/nonliving scavenger hunt: walk through the house and list 5 living and 5 nonliving things with explanations",
                "Tricky cases debate: is a seed alive? Is a virus alive? Is fire alive? Discuss using the characteristics of life.",
                "Characteristics of life checklist: for any object, check off which characteristics of life it has. Four or more? It's (or was) alive!",
            ],
            "real_world_connections": [
                "Food comes from living things: fruits from plants, meat from animals, bread from wheat (a plant). Everything we eat was alive.",
                "Pets are living things with needs: food, water, shelter. Understanding 'alive' means understanding responsibility for living creatures.",
                "Wood, cotton, leather, and paper all come from living things. Many of our materials started as organisms.",
                "Gardens are places where we help living things grow: understanding what plants need IS understanding characteristics of life.",
            ],
            "common_misconceptions": [
                "Thinking anything that moves is alive — cars, rivers, and fire all move but are not alive. Movement alone is not a characteristic of life.",
                "Confusing 'dead' with 'nonliving' — a dead animal WAS alive (it's a once-living thing). A rock was NEVER alive. These are different categories.",
                "Thinking plants aren't alive because they don't move visibly — plants grow, reproduce, need water and sunlight, and respond to their environment (turning toward light). They are absolutely alive.",
                "Believing all small things are nonliving — bacteria, insects, and seeds are tiny but alive. Size doesn't determine whether something is living.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Sorts 10 items correctly into living and nonliving with explanations",
                "Lists 4+ characteristics of living things",
                "Handles tricky cases (dead things, fire, clouds) with correct reasoning",
            ],
            "proficiency_indicators": [
                "Sorts most items correctly but struggles with tricky cases",
                "Lists 2-3 characteristics of living things",
            ],
            "developing_indicators": [
                "Uses only movement as the criterion for living",
                "Cannot consistently distinguish living from nonliving",
            ],
            "assessment_methods": ["object sorting", "characteristics listing", "tricky case reasoning"],
            "sample_assessment_prompts": [
                "Sort these 10 items into living and nonliving. Explain your choices.",
                "Name 4 things that make something alive.",
                "Is a dead flower living or nonliving? Explain your answer.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which of these is a living thing?",
                "expected_type": "multiple_choice",
                "options": ["A rock", "A tree", "A pencil", "A glass of water"],
                "correct_answer": "A tree",
                "hints": ["Living things grow, need food and water, and reproduce. Which one does all of these?"],
                "explanation": "A tree is a living thing: it grows, needs water and sunlight, reproduces (makes seeds), and responds to its environment (grows toward light). Rocks, pencils, and water are nonliving.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Name 3 characteristics of living things.",
                "expected_type": "text",
                "hints": ["Think about what YOUR body does: grow, eat, respond to things..."],
                "explanation": "Living things: (1) grow and develop, (2) reproduce (make more of themselves), (3) need food and water (energy), (4) respond to their environment. Any 3 of these is correct.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: Fire is alive because it grows and moves.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": [
                    "Does fire reproduce? Does it eat food? Does it respond to its environment the way a living thing does?"
                ],
                "explanation": "False. Fire grows and moves, but it does NOT reproduce, does not need food in the biological sense, and is not made of cells. It only meets 1-2 characteristics of life, not all of them. It is a chemical reaction, not a living thing.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Go on a scavenger hunt in your home. Find and list 3 living things and 3 nonliving things. Explain how you know which is which.",
                "expected_type": "text",
                "hints": [
                    "Living: people, pets, houseplants. Nonliving: furniture, toys, dishes. What makes each category different?"
                ],
                "explanation": "Living things in a home: people, pets (dog, cat, fish), houseplants. Nonliving: tables, chairs, books, cups. Living things grow, need food/water, and respond to the environment. Nonliving things do none of these.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "A seed is sitting on a shelf. It is not growing or doing anything. Is it alive? Explain your reasoning using the characteristics of life.",
                "expected_type": "text",
                "hints": [
                    "A seed looks inactive. But what happens when you plant it and add water? Does it have the POTENTIAL for life characteristics?"
                ],
                "explanation": "Yes, a seed IS alive — it is a dormant living thing. It contains a tiny plant embryo that will grow, reproduce, and respond to its environment once it has water and warmth. It has the potential for all characteristics of life, even though it appears inactive. This is a great tricky case!",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Sort these 10 items into living and nonliving. Explain one tricky choice.",
                "type": "open_response",
                "target_concept": "living_nonliving",
                "rubric": "Mastery: all correct with reasoning for tricky cases. Proficient: most correct. Developing: uses only movement as criterion.",
            },
            {
                "prompt": "List the characteristics of living things.",
                "type": "open_response",
                "target_concept": "characteristics_of_life",
                "rubric": "Mastery: 4+ characteristics with examples. Proficient: 2-3. Developing: 0-1.",
            },
        ],
        "resource_guidance": {
            "required": ["collection of natural objects for sorting", "pictures of living and nonliving things"],
            "recommended": ["magnifying glass for close observation", "poster board for living/nonliving display"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Sorting physical objects requires no reading. Oral explanations of reasoning. Draw living vs nonliving instead of writing. Labeled picture cards for visual support.",
            "adhd": "Nature walk scavenger hunt provides movement. Sorting real objects is hands-on. Tricky case debates are interactive. 10-15 minute focused sessions.",
            "gifted": "Introduce the concept of cells as the building blocks of life. Discuss viruses (are they alive? Scientists disagree!). Begin classifying living things into kingdoms: plants, animals, fungi.",
            "visual_learner": "Sorting mats with clear labels. Photographs of living and nonliving things. Color-coded categories.",
            "kinesthetic_learner": "Handle real objects. Nature walk collecting. Physical sorting into piles or trays.",
            "auditory_learner": "Discuss each item: 'Is this alive? How do you know?' Verbal reasoning is the primary assessment mode.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "One of the first great questions in science is: what makes something alive? Living things share characteristics, they grow, they reproduce, they need food and water, and they respond to their environment. Today we list the characteristics of life, sort objects into living and nonliving with explanations, and reason carefully through tricky cases like a dead leaf or a moving cloud.",
                "gradual_release": {
                    "i_do": "Hold up a leaf and a stone and think aloud: I check each against the characteristics of life, does it grow, reproduce, need food and water, respond to its surroundings. The stone meets none; the leaf, and the tree it came from, meets them all. Show plainly that a dead leaf was once living, while a stone never was.",
                    "we_do": "Check several objects against the characteristics of life together, sorting them into living, once-living, and never-living, and working through a tricky case as a pair.",
                    "you_do": "Child sorts a set of objects into living and nonliving, explains each choice by the characteristics of life, and reasons through a tricky case.",
                },
                "guided_practice": [
                    "Check objects against the four characteristics of life and sort them",
                    "Sort a nature-walk collection into living, once-living, and never-living",
                    "Reason through tricky cases: fire, a cloud, a seed, a dead leaf",
                ],
                "independent_practice": [
                    "Sort ten objects into living and nonliving and write the reason for each",
                    "Make a living and nonliving poster with labeled drawings",
                ],
                "mastery_check": [
                    "List at least four characteristics of living things",
                    "Sort ten objects correctly into living and nonliving with explanations",
                    "Reason correctly through a tricky case and explain it",
                ],
                "spiral_review": [
                    "Revisit careful observation, since deciding what is alive depends on observing what a thing really does",
                ],
            },
            "classical": {
                "narrative_introduction": "To bring order to the living world, the mind must first divide it: what is alive, and what is not. This was among the earliest acts of natural philosophy. The living are marked by sure signs, they grow, they bring forth their own kind, they take nourishment, and they answer their surroundings. To know these signs is to hold the first key of all the study of life.",
                "memory_work": {
                    "chants": [
                        "Chant the characteristics of life: the living grow, the living reproduce, the living need food and water, the living respond to their world",
                        "Chant the three kinds: the living, the once-living, and the never-living",
                    ],
                    "recitations": [
                        "Recite that movement alone does not mark life, for fire and rivers move, and that a thing is living only if it bears all the signs of life",
                    ],
                },
                "copywork": [
                    "Copy the characteristics of living things, neatly listed, and beside each an example",
                ],
                "recitation_routine": "Begin each lesson by reciting the characteristics of life before any new sorting or classifying.",
                "history_integration": "Tell that the ordering of the world into the living and the nonliving, and the living into their kinds, is the oldest work of natural philosophy, and that scholars have sought the true marks of life since the most ancient times.",
                "read_aloud_suggestions": [
                    "A passage of natural history that describes a living creature going about the business of life, read aloud so the child hears the characteristics of life at work",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A living book of natural history that shows real creatures and plants living their lives, with true artwork and never a workbook",
                ],
                "short_lesson_flow": "Take a nature walk and let the child gather what catches their eye, leaves, stones, an acorn, a feather. Back home, sort the basket calmly into things that are or were alive and things that never lived, talking it over. Let the child's own noticing of how living things behave lead the way, before any formal list. Stop while interest holds.",
                "narration_prompt": "Tell me how you sorted your basket. How could you tell which things were alive, or had once been alive?",
                "real_world_objects": [
                    "A nature-walk basket of leaves, stones, acorns, feathers, and shells",
                    "A growing houseplant and a family pet, living things to watch",
                    "A nature notebook for drawing the living and the nonliving",
                ],
                "nature_connection": "Out of doors the child meets living things going about their lives, a bird feeding, a plant turning to the light, an ant carrying a crumb, and sees the characteristics of life in action, not as a list but as a truth observed.",
                "habit_focus": "The habit of attention: watching a creature or a plant long enough to see that it grows, feeds, and answers its world.",
            },
            "montessori": {
                "prepared_materials": [
                    "Living and nonliving classification cards with clear photographs",
                    "Sorting trays for the physical classification of objects",
                    "Real specimens: a growing plant, shells, rocks, a feather, an acorn",
                    "The first of the biology nomenclature cards",
                ],
                "presentation": {
                    "three_period_lesson": "With the classification cards: this is a living thing, see that it grows and feeds; show me a living thing; is this living or nonliving?",
                    "steps": [
                        "The child sorts real specimens and cards into living and nonliving on the sorting trays",
                        "For each, the child checks the characteristics of life: does it grow, reproduce, feed, and respond",
                        "The child meets the tricky cases, the once-living and the never-living, and places them with reasoning",
                    ],
                },
                "control_of_error": "The classification cards and specimens are matched and verified, so a card placed in the wrong tray can be checked against the characteristics of life and against the card's own pairing, and the child corrects it themselves.",
                "abstraction_pathway": "From sorting real, concrete specimens by what they plainly do, to classifying pictures and tricky cases by the characteristics of life, toward grasping life as a category defined by its sure signs.",
                "extensions": [
                    "Sort the living things further into plants and animals",
                    "Care for a living plant or creature, meeting its needs as a study of life",
                    "Investigate a tricky case in depth: is a seed alive, is a virus alive",
                ],
                "observation_focus": "Watch for the child checking all the characteristics of life rather than relying on movement alone, and reasoning calmly through the once-living and never-living cases.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a basket for nature-walk treasures, the living, the once-living, and the never-living",
                    "Have a houseplant or pet the child can help tend",
                    "Leave out nature books and a magnifying glass for close looking",
                ],
                "real_world_contexts": [
                    "Caring for a pet or a plant and meeting its real needs for food, water, and care",
                    "Noticing on a walk what is alive, what was once alive, and what never lived",
                    "Wondering at the kitchen: which of our foods came from living things",
                    "Talking about tricky cases as they come up: is fire alive, is a seed alive",
                ],
                "conversation_starters": [
                    "Is this alive? How can you tell?",
                    "A fire grows and moves, does that make it alive? What is it missing?",
                    "This leaf fell off the tree, is it living or nonliving now?",
                ],
                "resource_bank": [
                    "A pet or houseplant to care for and observe",
                    "Nature books and field guides",
                    "The whole out-of-doors, full of the living and the nonliving",
                ],
                "parent_role": "Let the question of what is alive arise from real life, from caring for a pet, from a found feather, from a fire in the hearth, and wonder it through together. Welcome the child's reasoning about tricky cases, and let real living things, watched and tended, do the teaching.",
                "observation_documentation": "Over time, note whether the child tells living from nonliving, names the characteristics of life, and reasons through tricky cases like dead things, fire, and seeds. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Living/nonliving vocabulary builds reading comprehension in science texts: organism, reproduce, respond, environment",
            "math": "Sorting and classifying objects is a mathematical skill: grouping by characteristics, counting group sizes",
            "history": "Ancient civilizations understood living vs nonliving: they farmed (living plants), built with stone (nonliving), and kept animals (living)",
        },
    },
    "sf-03": {
        "enriched": True,
        "learning_objectives": [
            "Draw and label all stages of a plant life cycle: seed, sprout, seedling, mature plant, flower, fruit, seed again",
            "Grow a plant from a seed and record observations weekly in a science notebook",
            "Explain what plants need to survive: sunlight, water, soil (nutrients), and air",
            "Describe seed dispersal methods: wind, water, animals, and explosion",
        ],
        "teaching_guidance": {
            "introduction": "The plant life cycle is one of the most beautiful and accessible science topics because the child can watch it happen in real time. Plant a bean seed in a clear cup against the glass, and within days the child will see the root push down, the stem push up, and the first leaves unfurl. Over weeks, the plant grows, flowers, and produces seeds — completing the cycle. This hands-on experience makes abstract concepts (germination, photosynthesis, reproduction) concrete and unforgettable.",
            "scaffolding_sequence": [
                "Examine seeds: open a bean, an apple seed, a sunflower seed. Inside each one is a tiny baby plant (embryo) waiting to grow.",
                "Plant a bean seed in a clear plastic cup against the glass so the child can watch roots and stem develop day by day",
                "Observe and draw germination: the seed splits open, the root grows down, the stem grows up. Record in science notebook.",
                "Discuss what plants need: design a simple experiment — one plant with sunlight, one without. One with water, one without. Observe results.",
                "Study plant parts and their jobs: roots (absorb water), stem (transport), leaves (make food from sunlight), flower (reproduction), fruit (protects seeds)",
                "Watch the plant flower (if using fast-growing varieties like beans or sunflowers) and observe the transition from flower to fruit/seed",
                "Discuss seed dispersal: how do seeds travel? Wind (dandelion), water (coconut), animals (burrs), explosion (touch-me-not)",
                "Complete the cycle diagram: draw the full life cycle as a circle — seed to plant to flower to fruit to seed again",
            ],
            "socratic_questions": [
                "We planted this seed a week ago. What has changed? What do you think will happen next?",
                "One plant is in the sunlight and one is in a dark closet. Which one do you predict will grow better? Why?",
                "A dandelion puff blows in the wind. Why does the dandelion WANT its seeds to fly away?",
                "The seed has a tiny plant inside it. What does it need from the outside world to start growing?",
            ],
            "practice_activities": [
                "Bean in a bag: place a damp paper towel and a bean seed in a zip-lock bag taped to a window. Watch germination happen without soil!",
                "Sunlight experiment: grow two identical plants — one in sun, one in shade. Measure and compare growth weekly. Record in science notebook.",
                "Seed hunt: go outside and find as many different seeds as possible (acorns, dandelion fluff, burrs, pine cones, berries). Sort by dispersal method.",
                "Life cycle diagram: draw the plant life cycle as a circle with arrows. Label each stage: seed → sprout → seedling → plant → flower → fruit → seed.",
            ],
            "real_world_connections": [
                "Every fruit and vegetable in the kitchen came from a plant life cycle: the apple is the fruit, the seeds inside are the next generation",
                "Farmers understand the plant life cycle deeply: planting seeds, providing water and nutrients, harvesting crops",
                "Gardens are plant life cycles in action: the family garden is a living science experiment",
                "Trees in the neighborhood follow the same cycle: flowers in spring, fruit in summer, seeds in fall, dormancy in winter",
            ],
            "common_misconceptions": [
                "Thinking plants get their food from the soil — plants make their own food from sunlight (photosynthesis). Soil provides water and minerals, not food.",
                "Believing seeds need sunlight to germinate — most seeds germinate in the dark, underground. They need WATER and WARMTH, not light, to sprout. Sunlight is needed later for growth.",
                "Thinking all flowers are just decorative — flowers are the reproductive organs of plants. They produce seeds for the next generation.",
                "Assuming fruits are only things we eat as 'fruit' — in science, a fruit is any structure that contains seeds: tomatoes, peppers, acorns, and dandelion fluff are all fruits.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Draws and labels all stages of the plant life cycle correctly",
                "Maintains a plant growth journal with weekly observations for 4+ weeks",
                "Explains plant needs (sun, water, soil, air) with evidence from experiments",
            ],
            "proficiency_indicators": [
                "Names most life cycle stages but may omit one",
                "Records observations but not consistently weekly",
            ],
            "developing_indicators": [
                "Knows plants grow from seeds but cannot describe the full cycle",
                "Cannot explain plant needs with specificity",
            ],
            "assessment_methods": ["life cycle diagram", "plant journal review", "plant needs explanation"],
            "sample_assessment_prompts": [
                "Draw and label the life cycle of a plant, from seed back to seed.",
                "Show me your plant journal. What changed each week?",
                "What does a plant need to grow? How do you know?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What do plants need to grow?",
                "expected_type": "multiple_choice",
                "options": [
                    "Only water",
                    "Sunlight, water, soil, and air",
                    "Just soil and darkness",
                    "Only sunlight",
                ],
                "correct_answer": "Sunlight, water, soil, and air",
                "hints": [
                    "Plants need several things, not just one. Think about what you give your plant every day, plus what nature provides."
                ],
                "explanation": "Plants need sunlight (for making food through photosynthesis), water (for transport and growth), soil (for minerals and support), and air (for carbon dioxide). Remove any one and the plant will struggle or die.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "True or false: A flower is just for decoration — it doesn't serve an important purpose for the plant.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["What happens AFTER a flower blooms? What grows in its place?"],
                "explanation": "False. Flowers are the reproductive part of the plant. They produce seeds that become the next generation of plants. Without flowers, most flowering plants could not reproduce.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Plant a bean seed in a clear cup against the glass. Check it every day for a week. Draw what you see each day in your science notebook.",
                "expected_type": "text",
                "hints": [
                    "Day 1: the seed is dry. Day 2-3: it swells with water. Day 3-5: a root appears. Day 5-7: a stem pushes up. Draw what YOU see — everyone's timing is slightly different."
                ],
                "explanation": "Over about a week, you should observe: the seed absorbs water and swells, the seed coat splits, a root emerges and grows downward, then a stem pushes upward. Drawing each day creates a visual record of germination — real science in action.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Name two ways seeds travel to new places.",
                "expected_type": "text",
                "hints": ["Think about dandelion fluff, burrs that stick to your socks, and berries that birds eat."],
                "explanation": "Seeds travel by: wind (dandelion, maple helicopter), animals (burrs stick to fur, birds eat berries and spread seeds), water (coconuts float), and explosion (some pods burst open and shoot seeds). This is called seed dispersal, and it helps plants spread to new areas.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Design an experiment to find out whether plants need sunlight to grow. What would you do? What would you compare?",
                "expected_type": "text",
                "hints": [
                    "You need TWO plants that are the same in every way EXCEPT for sunlight. One gets sun, one doesn't. Everything else stays the same."
                ],
                "explanation": "A good experiment: plant two identical seeds in identical cups with the same soil and water. Place one in sunlight and one in a dark closet. Give both the same amount of water. Observe and measure them each week. The difference in growth is caused by the sunlight (the only thing that's different). This is a controlled experiment — a fundamental concept in science.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Draw and label the complete plant life cycle.",
                "type": "open_response",
                "target_concept": "plant_life_cycle",
                "rubric": "Mastery: all stages drawn in circle with labels and arrows. Proficient: most stages. Developing: only seed and plant.",
            },
            {
                "prompt": "Show me your plant journal. Describe what happened over the weeks.",
                "type": "open_response",
                "target_concept": "plant_observation",
                "rubric": "Mastery: weekly entries with drawings and measurements showing growth. Proficient: some entries. Developing: sparse records.",
            },
        ],
        "resource_guidance": {
            "required": ["bean seeds", "clear plastic cups", "soil", "water", "science notebook"],
            "recommended": [
                "magnifying glass for seed examination",
                "ruler for measuring growth",
                "fast-growing flower seeds (sunflower, marigold)",
            ],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Drawing the life cycle is the primary activity — minimal writing required. Label with single words dictated to parent if needed. The hands-on planting and observing requires no reading.",
            "adhd": "Planting seeds is hands-on and exciting. Daily 2-minute check-ins on the plant maintain engagement without long sessions. Drawing observations keeps hands busy. Outdoor seed hunts provide movement.",
            "gifted": "Introduce photosynthesis at a basic level (plants make food from sunlight + water + air). Compare life cycles of different plants. Design additional experiments (does music affect growth? does the color of light matter?).",
            "visual_learner": "Drawings of each stage are the core activity. Time-lapse videos of plant growth. Colorful life cycle posters.",
            "kinesthetic_learner": "Planting, watering, and tending plants. Seed collecting outdoors. Building a mini-greenhouse from a plastic bottle.",
            "auditory_learner": "Narrate observations aloud before drawing. Discuss predictions: 'What do you think will happen next?' Listen to audiobooks about plants.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "A plant's life runs in a cycle: a seed sprouts, grows into a seedling and then a mature plant, flowers, makes fruit, and the fruit holds new seeds, and the cycle begins again. Today we plant a seed and watch it grow, recording each week; we draw and label every stage of the life cycle; we learn what a plant needs to live, sunlight, water, soil, and air; and we learn how seeds travel to new places.",
                "gradual_release": {
                    "i_do": "Plant a bean seed against the side of a clear cup and think aloud about each stage as it comes: the root pushes down, the stem pushes up, the first leaves unfurl. Draw the stage in the notebook. Name what the plant needs, and show how a dandelion's seed is built to ride the wind.",
                    "we_do": "Tend the growing plant together, record its weekly changes in the notebook, draw the life-cycle stages, and sort a handful of seeds by how they travel.",
                    "you_do": "Child grows a plant from seed and records it weekly, draws and labels the full life cycle, explains what plants need, and describes seed dispersal.",
                },
                "guided_practice": [
                    "Plant a seed and record its changes in the science notebook each week",
                    "Draw and label the stages of the plant life cycle in a circle",
                    "Sort seeds by how they travel: wind, water, animals, explosion",
                ],
                "independent_practice": [
                    "Keep a weekly plant journal with drawings and measurements for several weeks",
                    "Design a simple experiment to show what a plant needs to grow",
                ],
                "mastery_check": [
                    "Draw and label all stages of the plant life cycle",
                    "Explain what plants need to survive: sunlight, water, soil, and air",
                    "Describe at least two ways seeds are dispersed",
                ],
                "spiral_review": [
                    "Revisit recording observations in the science notebook, the weekly habit the plant journal depends on",
                ],
            },
            "classical": {
                "narrative_introduction": "There is no plainer picture of order in nature than the life of a plant, which moves in a circle that never ends. The seed holds a sleeping plant; given water and warmth it wakes, roots downward, rises, leafs, flowers, and fruits, and the fruit yields seeds again. To know this cycle is to know one of the great recurring patterns of the living world.",
                "memory_work": {
                    "chants": [
                        "Chant the plant life cycle in order: seed, sprout, seedling, plant, flower, fruit, and seed once more",
                        "Chant what a plant needs: sunlight and water, soil and air",
                    ],
                    "recitations": [
                        "Recite the four ways seeds travel: by the wind, by the water, by the animals, and by the bursting of the pod",
                    ],
                },
                "copywork": [
                    "Copy the stages of the plant life cycle in order, neatly, and the list of what a plant needs to live",
                ],
                "recitation_routine": "Begin each lesson by reciting the stages of the plant life cycle before tending the growing plant or beginning new work.",
                "history_integration": "Tell that the understanding of the plant life cycle changed the course of human history, for when people learned to plant and harvest seeds on purpose they could settle, build, and grow, and farming itself is the plant life cycle put to work.",
                "read_aloud_suggestions": [
                    "A living account of a plant growing through the seasons, from seed to flower to seed, read aloud so the child hears the cycle told",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A beautifully illustrated living book about a plant's growth or a garden, with true botanical artwork and never a workbook",
                ],
                "short_lesson_flow": "Plant a seed together and set it where the child can watch it. Each day, a brief, glad visit: what has changed. Once a week, the child draws the plant as it now is in the nature notebook. Tend it faithfully, with no rush, and let the slow unfolding of the cycle be the lesson. The garden, indoors or out, is the classroom.",
                "narration_prompt": "Tell me how your plant has changed since last week. What do you think it will do next?",
                "real_world_objects": [
                    "A bean seed growing in a clear cup, watched daily",
                    "A nature notebook for weekly drawings of the plant",
                    "A real garden bed, or pots, the child helps tend",
                    "Seeds gathered on a walk: dandelion fluff, burrs, maple keys",
                ],
                "nature_connection": "The plant life cycle is nature study itself: the child watches their own seed, and also the trees and flowers around the home, flowering in spring, fruiting in summer, seeding in fall, and draws the seasons of growth in the nature notebook.",
                "habit_focus": "The habit of attention and of faithful care: tending a living plant daily and noticing its quiet, steady change.",
            },
            "montessori": {
                "prepared_materials": [
                    "The botany nomenclature cards: parts of a plant and stages of the life cycle, with three-part matching",
                    "Seed-sprouting trays and clear cups for watching germination",
                    "Real plants in the prepared environment for the child to water and tend",
                    "A magnifying glass for examining seeds",
                ],
                "presentation": {
                    "three_period_lesson": "With the life-cycle cards: this stage is the seedling; show me the seedling; which stage of the life cycle is this?",
                    "steps": [
                        "The child opens and examines real seeds, finding the tiny plant within",
                        "The child plants a seed and tends it, watching and recording each stage of germination and growth",
                        "The child works the botany nomenclature cards, matching each stage of the life cycle in order",
                    ],
                },
                "control_of_error": "The three-part nomenclature cards carry their own control, matching label to picture in one true way, and the growing plant is the deeper control: a plant denied water or light shows the child plainly what was missing.",
                "abstraction_pathway": "From handling real seeds and tending a real plant, to matching the life-cycle nomenclature cards, toward drawing and explaining the full cycle and a plant's needs without the materials.",
                "extensions": [
                    "Tend the classroom or home plants as practical-life care",
                    "Compare the life cycles and seeds of different plants",
                    "Investigate seed dispersal by sorting and examining many kinds of seed",
                ],
                "observation_focus": "Watch for the child tending the plant faithfully, recording its stages accurately, and grasping that the plant makes its own food while the soil gives water and minerals.",
            },
            "unschooling": {
                "invitations": [
                    "Keep seeds, pots, soil, and clear cups available for planting whenever the child wishes",
                    "Leave out a notebook and a magnifying glass beside the growing plants",
                    "Have nature books about plants and gardens within reach",
                ],
                "real_world_contexts": [
                    "Growing food or flowers in a real garden or in pots",
                    "Noticing the fruits and vegetables in the kitchen and the seeds inside them",
                    "Watching the neighborhood trees flower, fruit, and seed through the year",
                    "Collecting and wondering at seeds on a walk: dandelion fluff, burrs, acorns",
                ],
                "conversation_starters": [
                    "What do you think this seed will do if we plant it and water it?",
                    "Why do you think a dandelion wants its seeds to blow away?",
                    "What does our plant need that we have to give it?",
                ],
                "resource_bank": [
                    "Seeds, soil, pots, and a sunny windowsill or garden bed",
                    "Nature books and field guides about plants",
                    "The neighborhood trees and gardens, a plant cycle to watch all year",
                ],
                "parent_role": "Plant things alongside the child for the real joy and use of it, food to eat, flowers to enjoy, and let them tend what they plant. Wonder aloud about seeds, growth, and what the plant needs, and let the garden and the kitchen, rather than a worksheet, teach the cycle.",
                "observation_documentation": "Over time, note whether the child can tell the stages of a plant's life, knows what a plant needs, watches a plant grow with care, and understands how seeds travel. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Plant vocabulary builds reading comprehension: germination, photosynthesis, dispersal, seedling, dormant",
            "math": "Measuring plant growth in centimeters each week. Graphing growth over time. Counting seeds in a fruit.",
            "history": "The Agricultural Revolution: humans learned to plant seeds intentionally, which changed everything. Farming IS the plant life cycle, controlled.",
        },
    },
    "sf-04": {
        "enriched": True,
        "learning_objectives": [
            "Name at least 5 animal habitats and 2 animals that live in each",
            "Explain how at least one animal is adapted to its specific habitat",
            "Describe what happens when an animal's habitat is destroyed or changed",
            "Understand that animals depend on their habitat for food, water, shelter, and space",
        ],
        "teaching_guidance": {
            "introduction": "Every animal lives in a habitat — a place that provides everything it needs to survive: food, water, shelter, and space. A polar bear lives in the Arctic because it has thick fur and fat for cold temperatures and hunts seals on the ice. A cactus wren lives in the desert because it can survive on very little water and builds its nest in a cactus for protection. Animals don't just HAPPEN to live where they do — they are ADAPTED to their habitat, meaning their bodies and behaviors are designed for that specific environment.",
            "scaffolding_sequence": [
                "Start with the child's own backyard: 'What animals live near us? Why do they live HERE? What does our area provide for them?'",
                "Introduce 6 major habitats: forest, desert, ocean, grassland, wetland, polar. Show pictures of each.",
                "For each habitat, name 3-4 animals and discuss what the habitat provides: food, water, shelter, space",
                "Introduce the concept of adaptation: 'A camel has a hump to store fat for energy in the desert. That's an adaptation.'",
                "Study one animal in depth: where it lives, what it eats, how its body is adapted, what would happen if its habitat changed",
                "Discuss habitat destruction: 'What happens to forest animals when trees are cut down? Where do they go?'",
                "Create a habitat diorama: choose a habitat, build it from household materials, and populate it with drawn or toy animals",
                "Compare two habitats: how are they different? Could a desert animal survive in the ocean? Why not?",
            ],
            "socratic_questions": [
                "A polar bear has thick white fur. Why is that useful in the Arctic? Would it be useful in a desert?",
                "A fish has gills for breathing underwater. Could a fish survive on land? Why not?",
                "If all the trees in a forest were cut down, what would happen to the birds and squirrels that live there?",
                "Why don't penguins live in the jungle? What about the jungle wouldn't work for a penguin?",
            ],
            "practice_activities": [
                "Habitat diorama: choose a habitat and build it in a shoebox using paper, clay, and household materials. Add animals (drawn or toy).",
                "Animal-habitat matching game: write animal names on cards and habitat names on other cards. Match each animal to its habitat.",
                "Backyard habitat survey: explore your yard or a local park. List every animal you see and describe the habitat features they use.",
                "Adaptation investigation: pick one animal and research 3 adaptations that help it survive in its habitat. Draw the animal and label its adaptations.",
            ],
            "real_world_connections": [
                "Local wildlife depends on local habitats: the birds, squirrels, and insects in your yard all rely on the trees, plants, and water sources around your home",
                "Zoos recreate habitats: the penguin enclosure is cold with water; the reptile house is warm with heat lamps. Each exhibit matches an animal's natural habitat.",
                "Conservation is about protecting habitats: when we protect forests, wetlands, and oceans, we protect all the animals that depend on them",
                "Bird feeders and birdhouses create habitat features: providing food and shelter attracts specific species to your yard",
            ],
            "common_misconceptions": [
                "Thinking animals can easily move to a new habitat if theirs is destroyed — most animals are specially adapted to their habitat and cannot survive elsewhere",
                "Believing all deserts are hot — some deserts are cold (the Gobi, Antarctica). Desert means DRY, not necessarily hot.",
                "Assuming the ocean is one habitat — the ocean contains many habitats: coral reefs, deep sea, tidal pools, open water, kelp forests. Each has different animals.",
                "Thinking adaptation means an individual animal changes — adaptation happens over many generations through natural selection, not within one animal's lifetime",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Names 5+ habitats with 2+ animals for each",
                "Explains how one animal is adapted to its habitat with specific examples",
                "Describes consequences of habitat destruction",
            ],
            "proficiency_indicators": [
                "Names 3-4 habitats with animals",
                "Knows adaptations exist but gives general rather than specific examples",
            ],
            "developing_indicators": [
                "Names 1-2 habitats",
                "Cannot connect an animal's features to its habitat",
            ],
            "assessment_methods": ["habitat-animal matching", "adaptation explanation", "habitat description"],
            "sample_assessment_prompts": [
                "Name 5 habitats and 2 animals in each.",
                "How is a polar bear adapted to live in the Arctic?",
                "What happens to animals when their habitat is destroyed?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which habitat does a camel live in?",
                "expected_type": "multiple_choice",
                "options": ["Ocean", "Desert", "Polar", "Wetland"],
                "correct_answer": "Desert",
                "hints": [
                    "Camels have humps that store fat for energy. They can go days without water. What habitat is dry and hot?"
                ],
                "explanation": "Camels live in the desert. They are adapted to dry, hot conditions: their humps store fat for energy, they can close their nostrils during sandstorms, and they can survive long periods without water.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What four things does every animal need from its habitat?",
                "expected_type": "text",
                "hints": [
                    "Think about what YOU need to survive: something to eat, something to drink, somewhere to live, and room to move."
                ],
                "explanation": "Every animal needs: (1) food, (2) water, (3) shelter (a safe place to live and rest), and (4) space (room to move, hunt, and find mates). A habitat provides all four.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: A fish could survive in a desert if you gave it enough food.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["What does a fish use to breathe? Can it breathe air?"],
                "explanation": "False. A fish has gills adapted for breathing underwater. It cannot breathe air. Even with food, it would die without water. Animals are adapted to specific habitats — they can't simply be moved to a different one.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Pick one animal you know well. Describe its habitat and one adaptation that helps it survive there.",
                "expected_type": "text",
                "hints": [
                    "Choose any animal: a bird, a pet, a zoo animal. Where does it live in the wild? What feature of its body helps it survive there?"
                ],
                "explanation": "Example: 'A duck lives near ponds and lakes (wetland habitat). Its webbed feet are an adaptation that helps it swim efficiently through water. Its waterproof feathers keep it dry even when diving.' A good answer names the habitat, the adaptation, and explains HOW the adaptation helps.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Build a habitat diorama in a shoebox. Choose a habitat, create the environment using household materials, and add at least 3 animals that live there. Describe why each animal belongs in this habitat.",
                "expected_type": "text",
                "hints": [
                    "Pick: forest, desert, ocean, grassland, wetland, or polar. Build the environment. Add animals that actually live there. Explain their adaptations."
                ],
                "explanation": "A strong diorama shows the habitat's features (trees for forest, sand for desert, water for ocean) AND includes animals that actually live there with correct adaptations explained. Example for coral reef: blue paper for water, clay coral, drawn fish, sea turtle, and octopus — each with a note about how they're adapted to reef life.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Name 5 habitats and 2 animals for each.",
                "type": "open_response",
                "target_concept": "habitats_and_animals",
                "rubric": "Mastery: 5 habitats, 2+ animals each, all correctly matched. Proficient: 3-4 habitats. Developing: 1-2.",
            },
            {
                "prompt": "Explain how one animal is adapted to its habitat.",
                "type": "open_response",
                "target_concept": "adaptation",
                "rubric": "Mastery: specific adaptation with explanation of how it helps. Proficient: names adaptation. Developing: cannot connect features to habitat.",
            },
        ],
        "resource_guidance": {
            "required": ["pictures of different habitats and animals", "shoebox and craft supplies for diorama"],
            "recommended": ["animal reference books or cards", "magnifying glass for backyard habitat study"],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 20, "assessment": 10},
        "accommodations": {
            "dyslexia": "Pictures and dioramas are the core activities — minimal reading. Oral description of habitats and adaptations. Animal-habitat matching with picture cards rather than text.",
            "adhd": "Diorama building is highly engaging and hands-on. Backyard habitat survey involves outdoor movement. Each habitat studied in a separate 15-minute session. Animal-habitat card matching is a game.",
            "gifted": "Introduce food chains within habitats. Research an endangered species and its threatened habitat. Compare how the same animal (e.g., bears) adapts to different habitats (polar vs forest vs mountain).",
            "visual_learner": "Photographs and videos of habitats. Diorama building. Illustrated animal-habitat charts.",
            "kinesthetic_learner": "Build dioramas. Outdoor habitat walks. Animal movement imitation (waddle like a penguin, slither like a snake).",
            "auditory_learner": "Listen to nature documentaries narrated by David Attenborough. Discuss adaptations in conversation. Animal sound identification.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Every animal lives in a habitat, the place that gives it everything it needs: food, water, shelter, and space. Animals do not live just anywhere; they are adapted to their habitat, their bodies and behaviors fitted to that particular place. Today we name the major habitats and the animals in each, explain how an animal is adapted to its home, and learn what happens when a habitat is destroyed.",
                "gradual_release": {
                    "i_do": "Take one habitat, the desert, and think aloud: it is dry and hot; here lives the camel, and its hump stores fat for energy, its body is built for little water, so it is adapted to the desert. Show how a habitat gives food, water, shelter, and space, and ask what would become of the camel if the desert changed.",
                    "we_do": "Work through several habitats together, naming the animals in each, matching each animal to what its habitat provides, and naming one adaptation that fits the animal to its home.",
                    "you_do": "Child names the major habitats with animals for each, explains how an animal is adapted to its habitat, and describes what happens when a habitat is destroyed.",
                },
                "guided_practice": [
                    "Name the major habitats and two or more animals that live in each",
                    "Match an animal's adaptation to the habitat it fits: webbed feet, thick fur, gills",
                    "Discuss what happens to animals when their habitat is destroyed",
                ],
                "independent_practice": [
                    "Build a habitat diorama and explain why each animal belongs there",
                    "Study one animal in depth: its habitat, its adaptations, and the threats to its home",
                ],
                "mastery_check": [
                    "Name at least five habitats with two animals for each",
                    "Explain how one animal is adapted to its specific habitat",
                    "Describe what happens when an animal's habitat is destroyed",
                ],
                "spiral_review": [
                    "Revisit the characteristics and needs of living things, since a habitat is what supplies those needs",
                ],
            },
            "classical": {
                "narrative_introduction": "The natural world is ordered into realms, the forest, the desert, the ocean, the grassland, the wetland, the frozen poles, and each realm has its own creatures, fitted to it as a key is fitted to a lock. This fitness is called adaptation. No animal lives where it pleases; it lives where its body and its ways allow, and to study habitats is to study the deep order of nature.",
                "memory_work": {
                    "chants": [
                        "Chant the major habitats: forest and desert, ocean and grassland, wetland and frozen pole",
                        "Chant what every habitat must give: food and water, shelter and space",
                    ],
                    "recitations": [
                        "Recite that an animal is adapted to its habitat, its body and its ways fitted to the place it lives, and cannot simply be moved to another",
                    ],
                },
                "copywork": [
                    "Copy the names of the major habitats, and beside each an animal that lives there and one adaptation that fits it",
                ],
                "recitation_routine": "Begin each lesson by reciting the major habitats and what every habitat must provide before any new study.",
                "history_integration": "Tell that the naturalists who voyaged the world, charting which creatures lived in which lands, first revealed how deeply each animal belongs to its own place, and that the protecting of habitats is among the newest and most urgent of human tasks.",
                "read_aloud_suggestions": [
                    "A vivid account of a single animal living in its habitat, read aloud so the child hears how the creature and its home belong together",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A living book about an animal in its true home, written with knowledge and beauty, never a dry fact-list reader",
                ],
                "short_lesson_flow": "Begin close to home: walk in the yard or a nearby park and watch a real animal, a bird, a squirrel, an insect, in its own habitat. Notice quietly what the place gives it and how its body suits it. Read a portion of a living book about another habitat, and let the child narrate and draw the creature they met. Keep it warm and unhurried.",
                "narration_prompt": "Tell me about the animal we watched, or read of. Where does it live, and how is its body suited to that home?",
                "real_world_objects": [
                    "The yard, park, or pond, a real local habitat to observe",
                    "A nature notebook for drawing animals in their homes",
                    "Living books and beautiful animal pictures",
                ],
                "nature_connection": "The lesson begins out of doors with the habitats nearest home, the birds in the hedge, the creatures in the pond, and the child comes to know the local habitat first and most truly before studying the far ones.",
                "habit_focus": "The habit of attention: watching a creature long enough to see how it lives and how its home provides for it.",
            },
            "montessori": {
                "prepared_materials": [
                    "The continent animal cards, sorted by habitat",
                    "Animal and habitat nomenclature cards for matching",
                    "Materials for building a habitat diorama",
                    "Models or figures of animals to sort into their habitats",
                ],
                "presentation": {
                    "three_period_lesson": "With the habitat cards: this is the desert habitat; show me the desert habitat; which habitat is this?",
                    "steps": [
                        "The child sorts animal cards or figures into their habitats",
                        "For each animal, the child names an adaptation that fits it to its home",
                        "The child builds a habitat diorama, placing in it only the animals that truly belong",
                    ],
                },
                "control_of_error": "The animal and habitat cards are matched pairs, so an animal placed in the wrong habitat can be checked against its card and against its adaptations, and the child sees and corrects the mismatch.",
                "abstraction_pathway": "From sorting concrete animal cards and figures into habitats, to naming the adaptations that fit each animal to its home, toward understanding habitat as the web of food, water, shelter, and space that an animal depends upon.",
                "extensions": [
                    "Study the smaller habitats within one, the coral reef, the tidal pool, the kelp forest within the ocean",
                    "Trace a simple food chain within a habitat",
                    "Investigate an endangered animal and its threatened habitat",
                ],
                "observation_focus": "Watch for the child connecting an animal's body and behavior to its specific habitat, and understanding that an animal cannot simply be moved to another.",
            },
            "unschooling": {
                "invitations": [
                    "Keep animal books, field guides, and nature documentaries available",
                    "Leave out craft materials for building habitat dioramas",
                    "Have binoculars and a magnifying glass for watching real animals",
                ],
                "real_world_contexts": [
                    "Watching the animals in the yard, the park, and the pond and noticing what their habitat gives them",
                    "Visiting a zoo, an aquarium, or a nature center and seeing recreated habitats",
                    "Setting up a bird feeder or birdhouse and creating habitat features at home",
                    "Wondering, on a trip, why different animals live in different places",
                ],
                "conversation_starters": [
                    "Why do you think that animal lives here and not somewhere else?",
                    "What does this place give the animal that it needs?",
                    "Could this animal live in the desert, or the ocean? Why not?",
                ],
                "resource_bank": [
                    "Animal books, field guides, and nature documentaries",
                    "A local park, pond, or wood for watching real habitats",
                    "Zoos, aquariums, and nature centers",
                ],
                "parent_role": "Follow the child's love of particular animals wherever it leads, into books, documentaries, and trips to see them, and wonder aloud about why each creature lives where it does. Let real animal-watching, near home and far, rather than a worksheet, teach how an animal and its habitat belong together.",
                "observation_documentation": "Over time, note whether the child names habitats and their animals, explains how an animal is adapted to its home, and understands that an animal depends on its habitat and suffers when it is destroyed. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Animal habitat books build reading comprehension and vocabulary: habitat, adaptation, ecosystem, predator, prey, camouflage",
            "math": "Counting animals in a habitat. Comparing habitat temperatures. Measuring distances animals travel.",
            "history": "Human habitats are chosen for the same reasons: food, water, shelter. Ancient civilizations chose their locations based on the same needs as animals.",
        },
    },
    "sf-05": {
        "enriched": True,
        "learning_objectives": [
            "Name and locate 5 major organs: brain, heart, lungs, stomach, and bones (skeleton)",
            "Explain what the skeleton, heart, and lungs do in simple terms",
            "Describe at least 3 ways to keep the body healthy: exercise, nutrition, sleep",
            "Understand that the body is made of systems that work together",
        ],
        "teaching_guidance": {
            "introduction": "The human body is the most amazing machine a child will ever study — and they carry it with them everywhere. The skeleton holds you up (206 bones!). Muscles move you. The heart pumps blood to every part of your body without ever stopping. The lungs breathe in oxygen and breathe out carbon dioxide. The brain controls everything — it's the command center. At the foundational level, the goal is wonder and basic understanding: name the major parts, know what they do, and learn that taking care of your body (food, exercise, sleep) keeps the machine running well.",
            "scaffolding_sequence": [
                "Start with what the child can observe: feel your heartbeat, feel your ribs, watch your chest rise when you breathe, move your fingers and toes",
                "Introduce the skeleton: feel your bones through your skin. How many bones do you think you have? (206!) Bones protect organs and give your body shape.",
                "Introduce the heart: put your hand on your chest. Feel the beating? That's your heart pumping blood. It beats about 100,000 times per day!",
                "Introduce the lungs: take a deep breath. Feel your chest expand? Your lungs fill with air. They take in oxygen and push out carbon dioxide.",
                "Introduce the brain: tap your head gently. Your brain is inside, protected by your skull. It controls EVERYTHING: thinking, moving, seeing, feeling.",
                "Introduce the stomach and digestion: when you eat, food travels to your stomach where it's broken down into nutrients your body can use",
                "Discuss keeping the body healthy: good food (fuel), exercise (keeps the machine strong), sleep (repair time), water (keeps everything flowing)",
                "Body map project: the child lies on a large piece of paper, traces their outline, and draws/labels major organs inside",
            ],
            "socratic_questions": [
                "Put your hand on your chest. What do you feel? Why does your heart never stop beating?",
                "Take a deep breath and hold it for 5 seconds. Now breathe out. Why can't you hold your breath forever? What are your lungs doing?",
                "You ate lunch an hour ago. Where is that food right now? What's happening to it?",
                "What would happen if your skeleton suddenly disappeared? Why do bones matter?",
            ],
            "practice_activities": [
                "Body outline: trace the child on butcher paper. Draw and label: brain, heart, lungs, stomach, skeleton. Color the organs.",
                "Heart rate experiment: count heartbeats for 15 seconds at rest. Then do jumping jacks for 1 minute and count again. Why did it change?",
                "Lung capacity test: take the deepest breath you can and blow into a balloon. Measure the balloon. That's roughly how much air your lungs hold!",
                "Healthy habits tracker: for one week, track sleep hours, fruits/vegetables eaten, and minutes of exercise per day. Discuss patterns.",
            ],
            "real_world_connections": [
                "Exercise makes your heart stronger — that's why you feel your heart pound after running. Your heart is a muscle getting a workout.",
                "Eating fruits and vegetables gives your body the nutrients it needs to grow and repair — food is fuel for the body machine",
                "Sleep is when your body repairs itself: muscles heal, the brain organizes memories, and you grow. That's why children need 10-12 hours!",
                "Doctors and nurses study the body to help people stay healthy — medicine IS applied body science",
            ],
            "common_misconceptions": [
                "Thinking the heart is on the left side of the chest — it's actually in the CENTER, tilted slightly left. You feel it more on the left because the stronger left ventricle pumps harder.",
                "Believing blood is blue in veins and red in arteries — blood is ALWAYS red; veins look blue through the skin because of how light passes through tissue",
                "Thinking the stomach is behind the belly button — the stomach is actually higher, behind the lower ribs on the left side",
                "Believing bones are dead and dry — bones are ALIVE! They have blood vessels, nerves, and cells that constantly repair and rebuild. Living bones are flexible, not brittle.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Names and locates 5 major organs on a body diagram",
                "Explains what skeleton, heart, and lungs do",
                "Describes 3+ ways to keep the body healthy",
            ],
            "proficiency_indicators": [
                "Names 3-4 organs but may mislocate one",
                "Gives basic function descriptions",
            ],
            "developing_indicators": [
                "Names 1-2 organs",
                "Cannot explain organ functions",
            ],
            "assessment_methods": ["body diagram labeling", "organ function explanation", "health habits discussion"],
            "sample_assessment_prompts": [
                "On this body outline, show me where the brain, heart, lungs, and stomach are.",
                "What does your heart do? What do your lungs do?",
                "Name 3 things you can do to keep your body healthy.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What organ pumps blood through your whole body?",
                "expected_type": "multiple_choice",
                "options": ["Brain", "Heart", "Lungs", "Stomach"],
                "correct_answer": "Heart",
                "hints": ["Put your hand on your chest. What do you feel beating?"],
                "explanation": "The heart pumps blood through your entire body. It beats about 100,000 times per day, sending blood carrying oxygen and nutrients to every cell.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "True or false: Your skeleton has over 200 bones.",
                "expected_type": "true_false",
                "correct_answer": "true",
                "hints": ["An adult human skeleton has exactly 206 bones."],
                "explanation": "True. An adult human has 206 bones. Babies actually have about 270, but some fuse together as they grow. Bones support your body, protect your organs, and allow movement.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Do the heart rate experiment: count your heartbeats for 15 seconds while sitting still. Then do 20 jumping jacks and count again for 15 seconds. What happened? Why?",
                "expected_type": "text",
                "hints": [
                    "Your heart rate should be higher after exercise. Why would your heart need to beat faster when you move?"
                ],
                "explanation": "After exercise, your heart rate increases because your muscles need more oxygen and energy. The heart pumps faster to deliver more blood (carrying oxygen) to the working muscles. This is why exercise makes your heart stronger — it's a muscle getting a workout!",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Name 3 things you can do to keep your body healthy.",
                "expected_type": "text",
                "hints": ["Think about: what you eat, how you move, and how you rest."],
                "explanation": "Three ways to keep your body healthy: (1) Eat nutritious food — fruits, vegetables, proteins, whole grains give your body fuel and building materials. (2) Exercise — at least 60 minutes of active play per day keeps your heart, lungs, and muscles strong. (3) Sleep — children need 10-12 hours of sleep for their bodies to repair and grow.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Lie on a large piece of paper and have someone trace your outline. Then draw and label these organs inside: brain, heart, lungs, stomach, and skeleton (draw a few bones). Explain what each one does.",
                "expected_type": "text",
                "hints": [
                    "Brain: top of the head. Heart: center of the chest. Lungs: both sides of the chest. Stomach: upper left belly. Skeleton: ribs, spine, arm and leg bones."
                ],
                "explanation": "The body map should show: brain in the skull (controls everything), heart in center chest (pumps blood), lungs on both sides of the chest (breathe), stomach in upper abdomen (digests food), and skeleton bones throughout (support and protection). Each label should include a brief function.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Label the major organs on a body diagram and tell me what each one does.",
                "type": "open_response",
                "target_concept": "body_organs",
                "rubric": "Mastery: 5 organs correctly placed with functions. Proficient: 3-4. Developing: 1-2.",
            },
            {
                "prompt": "Why is exercise good for your heart?",
                "type": "open_response",
                "target_concept": "health",
                "rubric": "Mastery: explains that exercise strengthens the heart muscle and improves blood flow. Proficient: says exercise is healthy. Developing: cannot explain.",
            },
        ],
        "resource_guidance": {
            "required": ["large paper for body tracing", "pictures or model of human body"],
            "recommended": ["stethoscope (toy or real) for listening to heartbeat", "anatomy poster"],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Body tracing and organ drawing are visual and kinesthetic — no reading required. Oral explanations of functions. Labeled diagrams with pictures rather than text-heavy descriptions.",
            "adhd": "Heart rate experiment involves jumping jacks — physical and exciting. Body tracing is a big, active project. Study one organ per session (15 minutes). Movement breaks between topics.",
            "gifted": "Introduce body systems (circulatory, respiratory, digestive, skeletal, muscular, nervous). Research how specific organs work in more detail. Explore what happens when body systems malfunction (disease, injury).",
            "visual_learner": "Anatomy diagrams and posters. Body tracing project. Cross-section illustrations of organs.",
            "kinesthetic_learner": "Feel your own bones, heartbeat, and breathing. Body tracing. Exercise experiments. Act out how blood flows through the body.",
            "auditory_learner": "Listen to your heartbeat with a stethoscope. Discuss body functions in conversation. Songs about body parts and organs.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "The human body is a remarkable machine, and the child carries it everywhere. The skeleton holds it up, the heart pumps blood without ever resting, the lungs take in air, the stomach digests food, and the brain commands all of it. Today we name and locate the major organs, learn what the skeleton, heart, and lungs do, and learn the ways, good food, exercise, and sleep, that keep the body healthy.",
                "gradual_release": {
                    "i_do": "Place a hand on my chest and think aloud: I feel my heart beating, it pumps blood everywhere; I feel my ribs, the skeleton that shields my heart and lungs; I take a deep breath and feel my lungs fill. Name and point to each organ, and say plainly that they work together as systems.",
                    "we_do": "Find and name each major organ on our own bodies together, say what the skeleton, heart, and lungs do, and talk over the ways we keep the body healthy.",
                    "you_do": "Child names and locates the five major organs, explains what the skeleton, heart, and lungs do, and describes ways to keep the body healthy.",
                },
                "guided_practice": [
                    "Locate and name the brain, heart, lungs, stomach, and skeleton on the body",
                    "Explain in simple terms what the skeleton, heart, and lungs do",
                    "Trace a body outline and label the major organs inside",
                ],
                "independent_practice": [
                    "Make a labeled body map showing the major organs and their jobs",
                    "Keep a healthy-habits tracker of sleep, food, and exercise for a week",
                ],
                "mastery_check": [
                    "Name and locate the five major organs on a body diagram",
                    "Explain what the skeleton, heart, and lungs do",
                    "Describe at least three ways to keep the body healthy",
                ],
                "spiral_review": [
                    "Revisit the characteristics and needs of living things, since the body's systems serve those very needs",
                ],
            },
            "classical": {
                "narrative_introduction": "Of all the things a person may study, none is nearer than the body in which they live. It is a wonder of order: the bony frame that upholds it, the tireless heart, the breathing lungs, the brain that governs all. To know the names and the offices of its chief parts, and to keep it well by good food, movement, and rest, is knowledge every person should carry.",
                "memory_work": {
                    "chants": [
                        "Chant the major organs and their offices: the brain commands, the heart pumps, the lungs breathe, the stomach digests, the skeleton upholds and shields",
                        "Chant the keepers of health: good food, daily movement, and sound sleep",
                    ],
                    "recitations": [
                        "Recite that the body is made of systems that work together, no organ alone, but all serving the whole",
                    ],
                },
                "copywork": [
                    "Copy the names of the major organs, each beside its office, neatly set down",
                ],
                "recitation_routine": "Begin each lesson by reciting the major organs and their offices before any new study of the body.",
                "history_integration": "Tell that the study of the body is very old, that the Egyptians, the Greek physician Hippocrates, and the healers of China each sought to understand how the body works, and that medicine itself grew from this long and patient inquiry.",
                "read_aloud_suggestions": [
                    "A living account of how the heart, the lungs, or the skeleton does its work, read aloud with wonder rather than dry detachment",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A living book about the human body written with wonder and beauty, never a clinical or dull textbook",
                ],
                "short_lesson_flow": "Begin with the child's own body as the object of wonder: feel the heartbeat, feel the ribs, watch the chest rise with a breath, wiggle the fingers and feel the bones. Name one organ and what it does, simply and gladly. Vigorous outdoor play is itself the lesson in a strong, healthy body. Keep it short and full of wonder.",
                "narration_prompt": "Tell me what you felt when you put your hand on your chest. What is your heart doing, and why does it never stop?",
                "real_world_objects": [
                    "The child's own body: heartbeat, breath, bones felt through the skin",
                    "A balloon for feeling the lungs' work, a stopwatch for counting heartbeats",
                    "Good food, the outdoors for play, a bed for rest, the real keepers of health",
                ],
                "nature_connection": "Outdoor play, running, climbing, breathing deep of fresh air, is the body's own nature study: the child feels the heart quicken and the lungs work, and learns health through living well out of doors.",
                "habit_focus": "The habit of wonder and of care: marveling at the body's tireless work and tending it with good food, movement, and rest.",
            },
            "montessori": {
                "prepared_materials": [
                    "A human body puzzle with removable organs",
                    "Body and organ nomenclature cards for three-part matching",
                    "A model of the skeleton, and a body outline to label",
                    "Practical-life materials for body care: nutrition preparation and hygiene routines",
                ],
                "presentation": {
                    "three_period_lesson": "With the body puzzle or organ cards: this organ is the heart, it pumps the blood; show me the heart; which organ is this, and what does it do?",
                    "steps": [
                        "The child works the human body puzzle, lifting and replacing each organ in its place",
                        "The child matches the body nomenclature cards, organ to name to office",
                        "The child traces a body outline and places the organs, then carries body care into practical life, preparing food and keeping clean",
                    ],
                },
                "control_of_error": "The body puzzle and the three-part nomenclature cards carry their own control: each organ piece fits only its own place, and each card matches in one true way, so a wrong placement does not fit and the child corrects it.",
                "abstraction_pathway": "From handling the body puzzle and the organ models, to matching the nomenclature cards, toward naming the organs, their offices, and the systems they form without the materials.",
                "extensions": [
                    "Study the body systems: the circulatory, respiratory, digestive, and skeletal",
                    "Carry body care into daily practical life: preparing healthy food, hygiene routines",
                    "Examine how the organs work together as one whole",
                ],
                "observation_focus": "Watch for the child placing and naming the organs accurately, grasping each organ's office, and beginning to see the body as systems that work together.",
            },
            "unschooling": {
                "invitations": [
                    "Keep books, models, and puzzles of the human body within reach",
                    "Leave out a stethoscope, real or toy, and a stopwatch for exploring heartbeat and breath",
                    "Have large paper and pens available for body-tracing whenever the child wishes",
                ],
                "real_world_contexts": [
                    "Feeling the heart pound and the breath quicken after running and active play",
                    "Preparing and eating real food and talking about how it fuels the body",
                    "Noticing the body's need for sleep, and how rest restores it",
                    "Visits to the doctor or dentist, where the body's workings come up naturally",
                ],
                "conversation_starters": [
                    "Put your hand on your chest, what do you feel? Why does it never stop?",
                    "Where do you think your lunch is right now? What is happening to it?",
                    "What do you think your body needs to stay strong and well?",
                ],
                "resource_bank": [
                    "Body books, models, and puzzles",
                    "A stethoscope and stopwatch for exploring the body",
                    "Real food, active play, and rest, the everyday keepers of health",
                ],
                "parent_role": "Let the body's wonders come up in real life, the pounding heart after a run, the sleepiness at bedtime, the hunger before a meal, and wonder at them aloud together. Answer the child's questions about how the body works, and let healthy living, good food, movement, and rest, be lived rather than lectured.",
                "observation_documentation": "Over time, note whether the child can name and locate the major organs, say what they do, and understands the ways, food, movement, and rest, that keep the body healthy. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Body vocabulary (skeleton, organ, muscle, cardiac) builds scientific reading comprehension",
            "math": "Counting heartbeats per minute. Measuring lung capacity. Calculating hours of sleep per week.",
            "history": "Ancient civilizations studied the body: Egyptian mummification, Greek anatomy (Hippocrates), and Chinese medicine all explored how the body works.",
        },
    },
    "sf-06": {
        "enriched": True,
        "learning_objectives": [
            "Observe and record daily weather including temperature, cloud cover, precipitation, and wind for at least 2 weeks",
            "Identify 3 basic cloud types: cumulus (puffy), stratus (layered), cirrus (wispy)",
            "Describe weather patterns observed over time: trends in temperature, recurring conditions",
            "Use simple weather instruments: thermometer for temperature, wind vane or flag for wind direction",
        ],
        "teaching_guidance": {
            "introduction": "Weather is science you can observe every single day just by stepping outside. Is it sunny or cloudy? Warm or cold? Windy or still? Raining or dry? Weather observation turns the child into a real scientist: they collect data daily, record it in a journal, look for patterns, and make predictions. Over two weeks, the child builds a dataset and can say 'It was warmer this week than last week' or 'It rained three days in a row' — this is real scientific thinking using real evidence.",
            "scaffolding_sequence": [
                "Step outside together: 'What is the weather right now? Describe it using your senses: what do you see, feel, and hear?'",
                "Introduce a simple weather journal: each day, record temperature, cloud cover, wind, and precipitation",
                "Learn to read a thermometer: find an outdoor thermometer and read it at the same time each day for consistency",
                "Introduce cloud types: cumulus (big, puffy, fair weather), stratus (flat, gray, overcast), cirrus (thin, wispy, high altitude)",
                "Observe wind: which direction does it blow? How strong? Use a flag, windsock, or throw a leaf and watch which way it goes.",
                "Record 2 weeks of daily observations in the weather journal with drawings and data",
                "Look for patterns in the data: 'What was the warmest day? The coldest? Did you notice any trends?'",
                "Make a weather prediction based on observations: 'Today is cloudy and windy from the west. I predict rain tomorrow.'",
            ],
            "socratic_questions": [
                "We've recorded weather for a week. What patterns do you notice? Was each day the same?",
                "Look at those clouds. Are they puffy cumulus clouds or flat stratus clouds? What kind of weather do they usually bring?",
                "The temperature was 68 degrees yesterday and 55 degrees today. What changed? Can you think of why?",
                "Why do weather forecasters look at PATTERNS instead of just today's weather?",
            ],
            "practice_activities": [
                "Build a weather station: outdoor thermometer, homemade wind vane (pencil, straw, and paper arrow on a platform), and rain gauge (straight-sided jar with ruler markings)",
                "Daily weather journal: every morning at the same time, go outside and record temperature, clouds, wind, and precipitation in the science notebook",
                "Cloud identification walk: go outside, look up, identify cloud types, and draw them in the notebook",
                "Weather prediction challenge: based on this morning's observation, predict this afternoon's weather. Check later — were you right?",
            ],
            "real_world_connections": [
                "Farmers depend on weather: they plant, water, and harvest based on weather patterns. Understanding weather is essential for growing food.",
                "Weather forecasts on TV or apps use the same skills: observation, data collection, pattern recognition, and prediction — just with fancy equipment",
                "Dressing for the weather is daily applied science: checking the temperature and choosing clothes accordingly",
                "Planning outdoor activities (hiking, picnics, sports) requires weather awareness — a practical life skill",
            ],
            "common_misconceptions": [
                "Thinking temperature is the same everywhere at the same time — temperature varies by location, altitude, and sun exposure. The shady side of the house is cooler than the sunny side.",
                "Believing all clouds bring rain — only certain cloud types produce rain. Cumulus clouds usually mean fair weather; dark stratus or cumulonimbus clouds bring rain.",
                "Confusing weather (today's conditions) with climate (average conditions over years) — weather changes daily; climate is a long-term pattern",
                "Thinking wind comes FROM the direction it's blowing — a 'north wind' blows FROM the north TO the south. Wind is named for where it originates.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Records weather observations daily for 2+ weeks with consistent data",
                "Identifies 3 cloud types correctly",
                "Describes patterns in their weather data",
            ],
            "proficiency_indicators": [
                "Records observations most days but may miss some",
                "Identifies 1-2 cloud types",
            ],
            "developing_indicators": [
                "Records sporadically",
                "Cannot distinguish cloud types",
            ],
            "assessment_methods": ["weather journal review", "cloud identification", "pattern description"],
            "sample_assessment_prompts": [
                "Show me your weather journal. What patterns do you see over 2 weeks?",
                "Look at the sky. What kind of clouds are those?",
                "Based on today's weather, what do you predict for tomorrow?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which type of cloud is big and puffy, like cotton balls?",
                "expected_type": "multiple_choice",
                "options": ["Cumulus", "Stratus", "Cirrus"],
                "correct_answer": "Cumulus",
                "hints": [
                    "These clouds look like big fluffy pillows in the sky and usually appear on fair-weather days."
                ],
                "explanation": "Cumulus clouds are big, puffy, and white — they look like cotton balls or piles of whipped cream. They usually appear on fair-weather days. Stratus are flat and gray. Cirrus are thin and wispy.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "True or false: All clouds bring rain.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["Think about days with big white puffy clouds but no rain at all."],
                "explanation": "False. Many cloud types do NOT produce rain. White cumulus clouds usually mean fair weather. Only certain types of clouds (dark cumulonimbus, thick stratus) produce precipitation.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Go outside right now. Record today's weather in your science notebook: temperature (if you have a thermometer), cloud type, wind (none, light, strong), and precipitation (none, rain, snow). Draw what the sky looks like.",
                "expected_type": "text",
                "hints": [
                    "Use your senses: What do you SEE in the sky? What do you FEEL (temperature, wind)? Is it dry or wet?"
                ],
                "explanation": "A complete weather observation includes: temperature (or warm/cool/cold if no thermometer), cloud description with type name, wind assessment, and precipitation status. Drawing the sky adds visual detail. This daily practice IS being a scientist.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You've recorded weather for one week. The temperatures were: 65, 62, 58, 55, 60, 63, 67. Did the temperature go up or down during the week?",
                "expected_type": "text",
                "hints": [
                    "Look at the numbers in order. Did they mostly decrease, then increase? What pattern do you see?"
                ],
                "explanation": "The temperature dropped from 65 to 55 over the first 4 days, then rose back to 67 over the last 3 days. The pattern shows a cool spell in the middle of the week followed by warming. Identifying patterns in data is a core science skill.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Build a simple rain gauge using a straight-sided jar and a ruler. Place it outside. Check it after the next rainstorm. How much rain fell? Record the measurement in your weather journal.",
                "expected_type": "text",
                "hints": [
                    "Use a clear jar with straight sides (not tapered). Tape a ruler to the outside with 0 at the bottom. Place in an open area. After rain, read the water level."
                ],
                "explanation": "A rain gauge measures precipitation in inches or centimeters. After a rainstorm, read the water level against the ruler. Light rain might be 0.1 inches; a heavy storm might be 1+ inches. Record the measurement and date. Over time, you'll know how much rain falls in your area each month — real meteorological data!",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Show me your 2-week weather journal. Describe the patterns you found.",
                "type": "open_response",
                "target_concept": "weather_patterns",
                "rubric": "Mastery: 14 days recorded, patterns identified with evidence. Proficient: 10+ days, some patterns noted. Developing: sparse data, no patterns.",
            },
            {
                "prompt": "Identify the cloud types in these 3 photos.",
                "type": "open_response",
                "target_concept": "cloud_types",
                "rubric": "Mastery: all 3 correct. Proficient: 2 correct. Developing: cannot distinguish.",
            },
        ],
        "resource_guidance": {
            "required": ["science notebook for weather journal", "outdoor thermometer"],
            "recommended": [
                "materials for homemade weather station (jar for rain gauge, straw/pencil for wind vane)",
                "cloud identification chart",
            ],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 10, "assessment": 10},
        "accommodations": {
            "dyslexia": "Weather recording can use symbols instead of words: sun symbol, cloud symbol, rain drops, wind arrows. Draw weather rather than write about it. Oral weather reports.",
            "adhd": "Going outside every day for a 3-minute observation is manageable and refreshing. Building weather instruments is hands-on. Keep journal entries simple: draw and add one sentence.",
            "gifted": "Research how professional meteorologists forecast weather. Track barometric pressure. Compare local observations to official weather data. Study severe weather: hurricanes, tornadoes, blizzards.",
            "visual_learner": "Cloud identification charts with photographs. Weather symbols. Graphing temperature data over time.",
            "kinesthetic_learner": "Build weather instruments. Go outside for every observation. Feel the wind, catch rain, hold a thermometer.",
            "auditory_learner": "Oral weather reports: 'Today's weather is...' Listen to weather forecasts and compare to own observations.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Weather is science a child can do every day simply by stepping outside. Is it sunny or cloudy, warm or cold, windy or still, wet or dry? Today we observe and record the daily weather, temperature, clouds, wind, and precipitation, in a journal; we learn to name three cloud types, cumulus, stratus, and cirrus; we use simple instruments like a thermometer and a wind vane; and over two weeks we look for patterns in our data.",
                "gradual_release": {
                    "i_do": "Step outside and observe the weather aloud: I read the thermometer, I name the puffy clouds as cumulus, I watch a tossed leaf to find the wind's direction, I note that it is dry. Record each in the journal. Show how, after several days, the recorded numbers begin to show a pattern.",
                    "we_do": "Observe and record the weather together each day, reading the thermometer, naming the clouds, judging the wind, and after a week looking over the journal for patterns.",
                    "you_do": "Child observes and records the daily weather, identifies cloud types, uses simple instruments, and describes the patterns in their data.",
                },
                "guided_practice": [
                    "Record the day's temperature, clouds, wind, and precipitation in a weather journal",
                    "Identify cumulus, stratus, and cirrus clouds in the sky",
                    "Read a thermometer and find the wind's direction with a vane or a tossed leaf",
                ],
                "independent_practice": [
                    "Keep a daily weather journal with data and drawings for two weeks",
                    "Examine the two weeks of data and describe the patterns and trends",
                ],
                "mastery_check": [
                    "Record daily weather observations consistently for at least two weeks",
                    "Identify the three basic cloud types correctly",
                    "Describe patterns in the recorded weather data",
                ],
                "spiral_review": [
                    "Revisit recording observations in a notebook and reading measurements, the daily habits weather study depends on",
                ],
            },
            "classical": {
                "narrative_introduction": "The sky is a book that turns its page every day, and weather is the reading of it. For all of history people have watched the heavens to know what was coming, and the patient watcher learns that the weather is not mere chance but moves in patterns that may be observed, recorded, and even foretold. To keep a weather journal is to do what the first meteorologists did.",
                "memory_work": {
                    "chants": [
                        "Chant the three cloud types: cumulus the puffy, stratus the layered, cirrus the wispy",
                        "Chant the four things to record: the temperature, the clouds, the wind, and the rain",
                    ],
                    "recitations": [
                        "Recite that weather is the sky on a single day, while climate is the pattern of many years, and that the watcher learns the difference",
                    ],
                },
                "copywork": [
                    "Copy the names of the three cloud types, each with a few words of description, and the weather words: temperature, precipitation, forecast",
                ],
                "recitation_routine": "Begin each lesson by reciting the cloud types and the four things to record before the day's observation.",
                "history_integration": "Tell that weather has shaped the whole story of mankind, that droughts brought famine, storms scattered fleets, and hard winters turned back armies, and that people have watched and recorded the sky since the most ancient times.",
                "read_aloud_suggestions": [
                    "A vivid account of a storm, a season, or a sky, read aloud so the child hears weather described with care and wonder",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A beautifully illustrated book about clouds, the sky, and the seasons, with true artwork and never a workbook",
                ],
                "short_lesson_flow": "Step outside together each morning, just for a few minutes, and simply attend to the weather: look up at the clouds, feel the wind and the warmth, notice the wet or the dry. The child records it in the nature notebook, often with a drawing of the sky. Day after day, the journal fills, and the patterns reveal themselves. Keep it brief and faithful.",
                "narration_prompt": "Tell me about today's weather. What kind of clouds are in the sky, and how is the day different from yesterday?",
                "real_world_objects": [
                    "A nature notebook for the daily weather record",
                    "An outdoor thermometer read at the same hour each day",
                    "A flag, a windsock, or a tossed leaf for the wind",
                    "The sky itself, the day's true subject",
                ],
                "nature_connection": "Daily weather observation is a cornerstone of nature study: the child records the weather in the nature notebook beside the seasonal changes, and learns to read the sky as part of knowing the living world around them.",
                "habit_focus": "The habit of faithful attention: stepping out each day to observe the sky truly and record it without fail.",
            },
            "montessori": {
                "prepared_materials": [
                    "A weather station with an outdoor thermometer, a wind vane, and a rain gauge, some of them child-built",
                    "Cloud classification cards with photographs",
                    "A daily weather chart and a weather journal",
                    "Weather symbol cards for recording conditions",
                ],
                "presentation": {
                    "three_period_lesson": "With the cloud cards: these puffy clouds are cumulus; show me the cumulus clouds; which kind of cloud is this?",
                    "steps": [
                        "The child goes out to the weather station and reads the thermometer, the wind vane, and the rain gauge",
                        "The child observes the sky and matches the clouds to the classification cards",
                        "The child records the day's weather in the journal and, over time, reads the chart for patterns",
                    ],
                },
                "control_of_error": "The instruments are the control: the thermometer gives one true reading, the rain gauge one true level, and the cloud cards match the sky in one way, so a careless record can be checked against the instrument and corrected.",
                "abstraction_pathway": "From reading concrete instruments and matching cloud cards each day, to gathering the daily records into a chart, toward seeing the patterns in the data and predicting from them.",
                "extensions": [
                    "Build more weather instruments: a barometer, a windsock",
                    "Graph the temperature data over the weeks",
                    "Compare the home observations with the official forecast",
                ],
                "observation_focus": "Watch for the child observing and recording faithfully each day, reading the instruments accurately, and beginning to see the patterns in the gathered data.",
            },
            "unschooling": {
                "invitations": [
                    "Keep an outdoor thermometer, a journal, and materials for building weather instruments available",
                    "Leave out a cloud chart and books about weather and the sky",
                    "Let weather-watching belong to the daily rhythm of going outside",
                ],
                "real_world_contexts": [
                    "Checking the weather to decide what to wear and what to do each day",
                    "Watching a storm roll in, or the clouds change, and wondering what comes next",
                    "Building a rain gauge or wind vane and checking it after a storm",
                    "Comparing the family's own weather-watching with the forecast on a screen",
                ],
                "conversation_starters": [
                    "What is the weather doing today? How is it different from yesterday?",
                    "Look at those clouds, what do you think they will bring?",
                    "We have watched the weather all week, what pattern do you notice?",
                ],
                "resource_bank": [
                    "A thermometer, a journal, and simple weather instruments",
                    "Cloud charts and books about weather",
                    "The sky itself, free and changing every day",
                ],
                "parent_role": "Let weather-watching be part of ordinary days, dressing for it, planning around it, marveling at a storm, and wonder aloud about clouds, wind, and what tomorrow may bring. Build a rain gauge together if the child is keen, and let the real, changing sky, rather than a worksheet, be the teacher.",
                "observation_documentation": "Over time, note whether the child observes and records the weather, names the cloud types, uses simple instruments, and notices the patterns over days and weeks. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Weather vocabulary builds scientific literacy: precipitation, temperature, cumulus, barometric, forecast",
            "math": "Reading thermometers, measuring rainfall, graphing temperature over time, calculating averages — weather IS applied math",
            "history": "Weather shaped history: droughts caused famines, storms destroyed armadas, cold winters defeated armies. Weather is a historical force.",
        },
    },
    "sf-07": {
        "enriched": True,
        "learning_objectives": [
            "Describe the characteristics of each of the four seasons: temperature, daylight, weather patterns, and nature changes",
            "Explain how plants and animals respond to seasonal changes",
            "Connect seasonal changes to the Earth's tilted axis and orbit around the sun at a basic level",
            "Record seasonal observations in a nature journal across multiple seasons",
        ],
        "teaching_guidance": {
            "introduction": "The four seasons are nature's great rhythm: spring brings new growth, summer brings warmth and abundance, fall brings harvest and preparation, winter brings rest and cold. Children experience seasons naturally — they feel the temperature change, see leaves turn colors, notice days getting shorter or longer. The science of seasons connects these daily experiences to the bigger picture: Earth is tilted on its axis, and as it orbits the sun, different parts receive more or less direct sunlight, creating the seasonal cycle.",
            "scaffolding_sequence": [
                "Start with the current season: 'What season is it right now? How do you know? What tells you?'",
                "Describe each season's characteristics: temperature range, typical weather, daylight hours, what nature looks like",
                "Observe how plants change: buds in spring, full leaves in summer, color change in fall, bare branches in winter",
                "Observe how animals respond: migration, hibernation, growing thicker fur, storing food. These are seasonal behaviors.",
                "Introduce the WHY: Earth is tilted. When our part tilts toward the sun, we get more direct sunlight (summer). When it tilts away, less (winter).",
                "Use a globe and flashlight to demonstrate: tilt the globe and shine the flashlight. Where gets more light?",
                "Keep a seasonal observation journal: visit the same spot outdoors each month and record changes. Draw the same tree or garden patch across seasons.",
                "Compare seasons across the year: make a four-part poster with drawings and descriptions of the same place in each season",
            ],
            "socratic_questions": [
                "Why are days longer in summer and shorter in winter? What does that have to do with the sun?",
                "Leaves change color and fall in autumn. Why would a tree DROP its leaves? What's the advantage?",
                "Some birds fly south for winter. Why don't they just stay and deal with the cold?",
                "If it's summer here, what season is it in Australia (the Southern Hemisphere)? Why would it be different?",
            ],
            "practice_activities": [
                "Season wheel: draw a circle divided into 4 sections. In each section, draw the same scene (your house, a tree, a garden) as it looks in each season.",
                "Globe and flashlight demonstration: use a globe and flashlight in a dark room. Tilt the globe and see how direct light changes as the 'Earth' orbits.",
                "Seasonal nature walk: visit the same outdoor spot monthly. Draw what you see. Compare drawings across seasons.",
                "Animal adaptation research: pick an animal and describe what it does in each season (bear: active in summer, eats heavily in fall, hibernates in winter, emerges in spring).",
            ],
            "real_world_connections": [
                "Seasonal clothing: we change what we wear because of temperature changes — practical application of seasonal knowledge",
                "Seasonal foods: strawberries in summer, apples in fall, squash in winter. Agriculture follows the seasons.",
                "Holidays follow seasons: summer barbecues, fall harvest festivals, winter celebrations, spring planting",
                "Daylight savings time exists because of seasonal daylight changes — adjusting clocks to match the sun",
            ],
            "common_misconceptions": [
                "Thinking seasons are caused by Earth being closer or farther from the sun — seasons are caused by Earth's TILT, not its distance. (Earth is actually slightly closer to the sun during Northern Hemisphere winter!)",
                "Believing it's cold in winter because the sun is farther away — the sun is approximately the same distance. The angle of sunlight is what changes: less direct = less warming.",
                "Thinking every place on Earth has four distinct seasons — tropical regions near the equator have wet and dry seasons instead. Polar regions have extreme light/dark seasons.",
                "Assuming all trees lose their leaves in fall — only deciduous trees do. Evergreen trees (pines, spruces) keep their needles year-round.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Describes all 4 seasons with temperature, weather, daylight, and nature changes",
                "Explains plant and animal seasonal responses with examples",
                "Connects seasons to Earth's tilt at a basic level",
            ],
            "proficiency_indicators": [
                "Describes 3-4 seasons accurately",
                "Knows animals and plants change with seasons but gives limited details",
            ],
            "developing_indicators": [
                "Describes only the current season",
                "Cannot explain why seasons change",
            ],
            "assessment_methods": ["season descriptions", "seasonal change examples", "globe demonstration"],
            "sample_assessment_prompts": [
                "Describe what happens in each of the four seasons.",
                "How do animals prepare for winter? Give two examples.",
                "Why do we have seasons? Use the globe to show me.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "In which season do leaves change color and fall from trees?",
                "expected_type": "multiple_choice",
                "options": ["Spring", "Summer", "Fall (Autumn)", "Winter"],
                "correct_answer": "Fall (Autumn)",
                "hints": ["This season comes after summer and before winter. The days get shorter and cooler."],
                "explanation": "Leaves change color and fall in autumn (fall). Trees stop producing chlorophyll (the green pigment) as days shorten, revealing yellow, orange, and red pigments underneath. Then the leaves drop as the tree prepares for winter.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "True or false: Seasons happen because Earth gets closer to and farther from the sun.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["The real cause of seasons is Earth's TILT, not its distance from the sun."],
                "explanation": "False. Seasons are caused by Earth's tilted axis (23.5 degrees). When the Northern Hemisphere tilts toward the sun, we get summer (more direct sunlight). When it tilts away, we get winter (less direct sunlight). Distance from the sun barely changes and is NOT the cause.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Name one animal behavior that changes with the seasons and explain why it changes.",
                "expected_type": "text",
                "hints": [
                    "Think about: bears hibernating, birds migrating, squirrels storing acorns, dogs growing thicker fur."
                ],
                "explanation": "Example: Bears hibernate in winter because food is scarce. They eat heavily in fall to build up fat reserves, then sleep through the cold months using that stored energy. Their body temperature drops and their heart rate slows to conserve energy until spring brings food again.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Go outside and list 3 observations that tell you what season it currently is.",
                "expected_type": "text",
                "hints": [
                    "Look at: temperature, what plants look like, how much daylight there is, what animals are doing, what people are wearing."
                ],
                "explanation": "A good answer uses current direct observations. Spring example: 'Flowers are blooming. Birds are building nests. The days are getting longer and warmer.' Fall example: 'Leaves are turning yellow and red. Squirrels are collecting acorns. The air is cool in the morning.' Real observations show understanding of seasonal indicators.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Use a globe and a flashlight in a dark room. Hold the globe tilted and slowly orbit it around the flashlight. Explain what you observe about which part of the globe gets the most direct light and how that creates seasons.",
                "expected_type": "text",
                "hints": [
                    "Notice: when the top of the globe tilts TOWARD the flashlight, the northern half gets more direct light. When it tilts AWAY, the northern half gets less. What seasons would those create?"
                ],
                "explanation": "When the Northern Hemisphere tilts toward the sun (flashlight), it receives more direct light and heat — that's summer. Six months later in the orbit, the Northern Hemisphere tilts away, receiving less direct light — that's winter. Spring and fall are transitions between these extremes. The Southern Hemisphere experiences opposite seasons for the same reason.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Describe all 4 seasons: temperature, daylight, and what happens in nature.",
                "type": "open_response",
                "target_concept": "four_seasons",
                "rubric": "Mastery: all 4 described with 3+ details each. Proficient: 3-4 seasons described. Developing: 1-2 seasons.",
            },
            {
                "prompt": "Why do we have seasons? Show me with the globe.",
                "type": "open_response",
                "target_concept": "earth_tilt",
                "rubric": "Mastery: demonstrates tilt and explains direct vs indirect sunlight. Proficient: mentions tilt. Developing: says 'closer to the sun.'",
            },
        ],
        "resource_guidance": {
            "required": [
                "globe (or ball) and flashlight for demonstration",
                "science notebook for seasonal observations",
            ],
            "recommended": ["seasonal nature photographs", "calendar for tracking daylight hours"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Seasonal observation is visual: draw what you see. Globe demonstration is hands-on. Oral descriptions rather than written. Season wheel with drawings instead of text.",
            "adhd": "Outdoor seasonal walks provide movement. Globe demonstration is interactive. Season wheel art project is hands-on. Short, focused sessions — one season per session.",
            "gifted": "Track daylight hours throughout the year and graph them. Research why the equator doesn't have traditional seasons. Compare seasons in different biomes. Introduce the concepts of equinox and solstice.",
            "visual_learner": "Season wheel with detailed drawings. Photographs of the same place in different seasons. Globe and flashlight demonstration.",
            "kinesthetic_learner": "Globe demonstration with physical movement (the child IS Earth, walking around a lamp while tilting). Outdoor observation. Collect seasonal nature objects.",
            "auditory_learner": "Discuss seasonal changes in conversation. Listen to sounds that differ by season (bird songs in spring, crickets in summer, wind in fall). Oral descriptions of each season.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "The year turns through four seasons, and each has its own character: spring's new growth, summer's warmth and abundance, autumn's harvest and falling leaves, winter's cold and rest. Today we describe each season by its temperature, daylight, weather, and changes in nature; we learn how plants and animals respond to the seasons; and we learn the great cause behind them all, the tilt of the Earth as it orbits the sun.",
                "gradual_release": {
                    "i_do": "Name the current season and think aloud through its signs: the temperature, the length of the day, what the trees are doing, what the animals are doing. Then, with a globe and a flashlight, tilt the globe and show how the half tilted toward the light gets summer and the half tilted away gets winter.",
                    "we_do": "Describe each of the four seasons together, listing its temperature, daylight, weather, and changes in nature, and demonstrate the Earth's tilt with the globe and flashlight.",
                    "you_do": "Child describes all four seasons by their characteristics, explains how plants and animals respond to them, and shows with the globe why the seasons change.",
                },
                "guided_practice": [
                    "Describe each season's temperature, daylight, weather, and changes in nature",
                    "Name how plants and animals respond to each season: budding, migration, hibernation",
                    "Demonstrate the Earth's tilt with a globe and flashlight",
                ],
                "independent_practice": [
                    "Keep a seasonal nature journal, revisiting the same outdoor spot each month",
                    "Make a four-part season wheel showing the same place across the year",
                ],
                "mastery_check": [
                    "Describe all four seasons with their temperature, daylight, weather, and nature changes",
                    "Explain how plants and animals respond to seasonal change",
                    "Connect the seasons to the Earth's tilted axis and its orbit around the sun",
                ],
                "spiral_review": [
                    "Revisit recording observations in a notebook, the monthly habit the seasonal journal depends on",
                ],
            },
            "classical": {
                "narrative_introduction": "The year moves in a great and certain circle, and the four seasons are its quarters. People in every age have lived by this rhythm, planting in spring, harvesting in autumn, resting in winter. Behind the turning lies a quiet cause: the Earth leans on its axis, and as it journeys round the sun, first one half and then the other is given the fuller light.",
                "memory_work": {
                    "chants": [
                        "Chant the four seasons in their order: spring, summer, autumn, winter, and round to spring again",
                        "Chant the cause of the seasons: the Earth is tilted, and the half that leans toward the sun has summer",
                    ],
                    "recitations": [
                        "Recite that seasons come from the tilt of the Earth, not its distance from the sun, and that the angle of the light, direct or slanting, makes the warmth or the cold",
                    ],
                },
                "copywork": [
                    "Copy the names of the four seasons in order, each with a few words of its character, and the words equinox, solstice, axis, hemisphere",
                ],
                "recitation_routine": "Begin each lesson by reciting the four seasons in order and the cause of their turning before any new study.",
                "history_integration": "Tell that the seasons have governed human life since the beginning, that the first calendars were made to mark them, and that the harvest festivals and the solstice celebrations of every people are the year's turning kept as feast.",
                "read_aloud_suggestions": [
                    "A living account of the year passing through its four seasons, read aloud so the child hears the great rhythm told",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A beautifully illustrated living book that follows the turning year through its seasons, with true artwork and never a workbook",
                ],
                "short_lesson_flow": "Choose one spot out of doors, a tree, a garden corner, a stretch of hedge, and visit it together each month. Look quietly at how it has changed since the last visit, and the child draws it as it now is in the nature notebook. Across a year, the notebook itself becomes the lesson, the seasons told in the child's own drawings.",
                "narration_prompt": "Tell me how our spot has changed since we last visited it. What season are we in now, and how can you tell?",
                "real_world_objects": [
                    "One outdoor spot, a tree or garden corner, returned to month by month",
                    "A nature notebook holding a year of seasonal drawings",
                    "A globe and a flashlight for the tilt of the Earth",
                    "A seasonal nature table holding what the child gathers each season",
                ],
                "nature_connection": "Seasonal nature study is at the very heart of this lesson: the whole turning year is the subject, and the child comes to know the seasons not from a book but from a beloved place watched through all of them.",
                "habit_focus": "The habit of attention sustained over time: returning faithfully to the same place and noticing its slow, seasonal change.",
            },
            "montessori": {
                "prepared_materials": [
                    "A seasonal nature table that the child changes with each season's gathered objects",
                    "A globe and a light source for demonstrating the Earth's tilt",
                    "Season classification cards showing the year's quarters",
                    "A four-part season wheel the child completes",
                ],
                "presentation": {
                    "three_period_lesson": "With the season cards: this is autumn, the leaves turn and fall; show me autumn; which season is this?",
                    "steps": [
                        "The child observes the current season out of doors and tends the seasonal nature table with what they gather",
                        "The child works the season cards, naming each season by its characteristics",
                        "The child uses the globe and light to discover how the Earth's tilt brings the seasons in turn",
                    ],
                },
                "control_of_error": "The real, turning year is the control: the seasonal nature table and the season cards are checked against what the child sees out of doors, and a season misnamed does not match the world beyond the window.",
                "abstraction_pathway": "From observing and gathering the real, present season, to classifying all four with the cards, toward grasping the unseen cause, the tilted Earth orbiting the sun.",
                "extensions": [
                    "Track the daylight hours through the year and see them lengthen and shorten",
                    "Study how a chosen animal lives through each season",
                    "Compare the seasons of the Northern and Southern Hemispheres",
                ],
                "observation_focus": "Watch for the child reading the season from real signs out of doors, and grasping that the tilt of the Earth, not its distance, brings the seasons.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a seasonal nature table for the treasures the child gathers as the year turns",
                    "Leave out a globe and a flashlight for free exploring of the Earth and sun",
                    "Have beautiful books about the seasons and the year within reach",
                ],
                "real_world_contexts": [
                    "Dressing for the season and noticing the temperature change through the year",
                    "Eating the foods of each season: summer berries, autumn apples, winter squash",
                    "Watching the trees bud, leaf, color, and bare across the year",
                    "Keeping the family's holidays and celebrations, which follow the seasons",
                ],
                "conversation_starters": [
                    "What season is it now? How can you tell?",
                    "Why do you think the leaves fall in autumn? What is the tree doing?",
                    "When it is summer here, what season do you think it is on the other side of the world?",
                ],
                "resource_bank": [
                    "A globe and flashlight kept available",
                    "Beautiful books about the seasons and the turning year",
                    "The out-of-doors itself, changing through every season",
                ],
                "parent_role": "Live the seasons gladly with the child, the foods, the clothes, the festivals, the changing weather, and wonder aloud at the signs each season brings. Bring out the globe when the child asks why, and let the real, turning year, rather than a worksheet, teach its rhythm.",
                "observation_documentation": "Over time, note whether the child can describe each season, sees how plants and animals respond to it, and understands that the Earth's tilt brings the seasons. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Seasonal vocabulary enriches reading: equinox, solstice, migration, hibernation, deciduous, evergreen",
            "math": "Tracking temperature across seasons produces data for graphing. Counting daylight hours. Calendar math: days between equinoxes.",
            "history": "Seasons drove ancient civilizations: planting seasons, harvest festivals, winter solstice celebrations. The agricultural calendar IS the seasonal calendar.",
        },
    },
    "sf-08": {
        "enriched": True,
        "learning_objectives": [
            "Describe the 3 stages of the water cycle: evaporation, condensation, and precipitation",
            "Demonstrate evaporation and condensation with simple household experiments",
            "Explain where rain comes from and where it goes in child-friendly language",
            "Connect the water cycle to daily observations: puddles drying, steam from a pot, dew on grass",
        ],
        "teaching_guidance": {
            "introduction": "Where does rain come from? Where does a puddle go when it dries up? The water cycle answers both questions, and the child can observe every stage in their own home. Evaporation: water turns into invisible water vapor (a puddle dries up, steam rises from a pot). Condensation: water vapor cools and turns back into tiny water droplets (fog on a mirror, dew on grass, the outside of a cold glass). Precipitation: water drops in clouds get heavy and fall as rain, snow, sleet, or hail. Then the cycle starts over. The same water has been cycling for billions of years.",
            "scaffolding_sequence": [
                "Observe a puddle on a sunny day. Mark its edge with chalk. Check every hour. Where does the water go? (Evaporation!)",
                "Boil water in a pot (parent does this safely): see the steam rising. Hold a cold plate over the steam: see water droplets form. That's evaporation AND condensation in your kitchen!",
                "Fill a glass with ice water on a warm day. Watch the outside of the glass get wet. Where did that water come from? (Condensation from water vapor in the air!)",
                "Introduce the three stages with their scientific names: evaporation (liquid → gas), condensation (gas → liquid), precipitation (water falls from clouds)",
                "Draw the water cycle as a diagram: sun heats water → water evaporates → water vapor rises → condenses into clouds → falls as rain → collects in rivers/lakes → cycle repeats",
                "Make a water cycle in a bag: put water in a sealed zip-lock bag, tape it to a sunny window. Watch evaporation, condensation on the bag, and 'rain' dripping down.",
                "Connect to real life: morning dew, fog, rain, steam, puddles drying — all are water cycle stages happening around us daily",
                "Narrate the water cycle as a story: 'I am a water droplet. First I was in the ocean. The sun heated me and I floated up into the sky...'",
            ],
            "socratic_questions": [
                "You left a wet towel in the sun and now it's dry. Where did the water go? Did it disappear?",
                "We see steam rising from the pot. Is the steam the same thing as the water that was in the pot? What happened to it?",
                "The outside of your cold glass is wet, but you didn't spill anything. Where did that water come from?",
                "Rain falls into a river, the river flows to the ocean, the sun heats the ocean... then what happens? Does the cycle end?",
            ],
            "practice_activities": [
                "Water cycle in a bag: seal water in a zip-lock bag and tape it to a sunny window. Observe evaporation and condensation over hours.",
                "Puddle watch: on a sunny day, mark a puddle's outline with chalk. Check every 30 minutes and mark the new edge. The puddle shrinks as water evaporates!",
                "Cold glass condensation: fill a glass with ice water. Within minutes, the outside gets wet. The child observes and explains where the water came from.",
                "Water cycle diagram: draw and label the complete cycle — sun, evaporation arrows going up, cloud, precipitation arrows coming down, river flowing to ocean, repeat.",
            ],
            "real_world_connections": [
                "Every glass of water you drink has been through the water cycle countless times — the water in your cup may have once been in a dinosaur's lake!",
                "Laundry dries on a clothesline because of evaporation: the sun and wind turn the water in wet clothes into water vapor",
                "Fog and dew are condensation: water vapor in the air cools and becomes visible droplets. Fog is a cloud on the ground.",
                "Rain, snow, sleet, and hail are all forms of precipitation — water falling from clouds back to Earth's surface",
            ],
            "common_misconceptions": [
                "Thinking water disappears when it evaporates — it doesn't disappear! It becomes invisible water vapor (a gas) and is still in the air. It hasn't gone; it changed form.",
                "Believing clouds are made of cotton or smoke — clouds are made of tiny water droplets or ice crystals. They formed through condensation of water vapor.",
                "Thinking rain comes from the ocean directly — rain comes from clouds, which formed when water evaporated from oceans, lakes, rivers, and even plants, then condensed in the atmosphere",
                "Believing hot water evaporates but cold water doesn't — ALL water evaporates, even cold water. Hot water just evaporates faster. A cold puddle still dries up eventually.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Describes all 3 stages of the water cycle with correct vocabulary",
                "Demonstrates evaporation and condensation with experiments",
                "Explains where rain comes from in own words",
            ],
            "proficiency_indicators": [
                "Names the stages but may confuse the order or terms",
                "Can perform experiments but struggles to connect them to the water cycle",
            ],
            "developing_indicators": [
                "Knows rain falls from clouds but cannot explain the full cycle",
                "Cannot define evaporation or condensation",
            ],
            "assessment_methods": ["water cycle narration", "experiment demonstration", "diagram drawing"],
            "sample_assessment_prompts": [
                "Tell me the story of a water droplet going through the water cycle.",
                "Show me evaporation using items from the kitchen.",
                "Draw and label the water cycle.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is it called when water changes from a liquid to a gas (water vapor)?",
                "expected_type": "multiple_choice",
                "options": ["Precipitation", "Evaporation", "Condensation", "Freezing"],
                "correct_answer": "Evaporation",
                "hints": ["This happens when the sun heats water and it rises into the air as invisible vapor."],
                "explanation": "Evaporation is when liquid water changes into water vapor (a gas). The sun provides the energy. You see this when puddles dry up, steam rises from a pot, or wet clothes dry on a line.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "True or false: When a puddle dries up, the water is gone forever.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["The water didn't disappear — it changed form. Where did it go?"],
                "explanation": "False. The water evaporated — it changed from liquid to invisible water vapor and went into the air. That water vapor will eventually condense into clouds and fall as rain somewhere else. Water is never destroyed; it just cycles through different forms.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Put water in a sealed zip-lock bag and tape it to a sunny window. Check it after 2 hours. Describe what you see and explain what happened using water cycle vocabulary.",
                "expected_type": "text",
                "hints": [
                    "You should see: water droplets forming on the INSIDE of the bag near the top. That's condensation. Where did those droplets come from?"
                ],
                "explanation": "The sun heats the water in the bag (evaporation). Water vapor rises and hits the cooler plastic at the top. The vapor cools and turns back into droplets (condensation). If enough collects, it drips back down (precipitation). You've created a miniature water cycle!",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Put the 3 stages of the water cycle in order: precipitation, evaporation, condensation.",
                "expected_type": "text",
                "correct_answer": "evaporation, condensation, precipitation",
                "hints": [
                    "First, water goes UP (becomes vapor). Then it forms clouds (water vapor → droplets). Then it falls back down (rain/snow)."
                ],
                "explanation": "Correct order: (1) Evaporation — sun heats water, it becomes vapor and rises. (2) Condensation — water vapor cools and forms cloud droplets. (3) Precipitation — water droplets in clouds get heavy and fall as rain, snow, sleet, or hail. Then the cycle repeats!",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Draw and label the complete water cycle. Include: the sun, evaporation, condensation, clouds, precipitation, and a body of water. Add arrows showing the direction water moves.",
                "expected_type": "text",
                "hints": [
                    "Start with water at the bottom (ocean/lake). Arrows going UP = evaporation. Cloud in the middle = condensation. Arrows coming DOWN = precipitation. Arrows flowing back to the water = collection."
                ],
                "explanation": "A complete water cycle diagram shows: a body of water at the bottom, the sun providing energy, upward arrows labeled 'evaporation,' a cloud labeled 'condensation,' downward arrows labeled 'precipitation,' and water collecting and flowing back (rivers to oceans). Arrows should form a circular pattern showing the cycle never ends.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Draw and label the water cycle.",
                "type": "open_response",
                "target_concept": "water_cycle_diagram",
                "rubric": "Mastery: all 3 stages labeled with arrows showing cycle. Proficient: 2 stages. Developing: cannot draw the cycle.",
            },
            {
                "prompt": "Tell me the story of a water droplet traveling through the water cycle.",
                "type": "open_response",
                "target_concept": "water_cycle_narration",
                "rubric": "Mastery: narrates all 3 stages in correct order with vocabulary. Proficient: covers 2 stages. Developing: only describes rain falling.",
            },
        ],
        "resource_guidance": {
            "required": [
                "zip-lock bags for water cycle experiment",
                "glass for condensation observation",
                "science notebook",
            ],
            "recommended": ["chalk for puddle marking", "kettle or pot for demonstrating steam (parent-supervised)"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Water cycle experiments are hands-on and visual — no reading required. Draw the cycle rather than writing about it. Oral explanation of observations. Water cycle story narrated aloud.",
            "adhd": "Experiments are exciting and produce visible results quickly. Puddle watching involves going outside. Cold glass condensation is almost magical. Keep explanations to 10 minutes; let experiments run longer.",
            "gifted": "Introduce states of matter (solid, liquid, gas) in connection with the water cycle. Research what happens in different climates (tropical vs arctic water cycles). Track rainfall data over months.",
            "visual_learner": "Water cycle diagram is the core visual tool. Watch water cycle videos. Observe real evaporation and condensation. Color-coded diagram.",
            "kinesthetic_learner": "All experiments are hands-on. Go outside to observe puddles, dew, and rain. Act out the water cycle: be a water droplet traveling through each stage.",
            "auditory_learner": "Narrate the water cycle as a story. Discuss each experiment: 'What happened? Why?' Listen to the sounds of rain and running water.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Water moves in a never-ending cycle. The sun heats water and it rises as invisible vapor: that is evaporation. High up, the vapor cools and gathers into clouds of tiny droplets: that is condensation. The droplets grow heavy and fall as rain or snow: that is precipitation. Then the cycle begins again. Today we learn the three stages, show evaporation and condensation with simple experiments, and explain where rain comes from and where it goes.",
                "gradual_release": {
                    "i_do": "Mark the edge of a puddle and think aloud about where the water goes as it dries: it evaporates. Hold a cold plate over steam and watch droplets form: that is condensation. Draw the cycle, naming each stage, and tell the journey of a single water droplet from the ocean to the cloud and back.",
                    "we_do": "Set up the water-cycle-in-a-bag experiment together, watch evaporation and condensation happen, name each stage, and draw and label the full cycle.",
                    "you_do": "Child names the three stages of the water cycle in order, demonstrates evaporation and condensation, and explains where rain comes from in their own words.",
                },
                "guided_practice": [
                    "Watch a puddle evaporate, or set up the water-cycle-in-a-bag experiment",
                    "Name the three stages in order: evaporation, condensation, precipitation",
                    "Draw and label the water cycle with arrows showing the direction water moves",
                ],
                "independent_practice": [
                    "Demonstrate evaporation and condensation with a household experiment and explain each",
                    "Narrate the journey of a water droplet through the whole cycle",
                ],
                "mastery_check": [
                    "Describe the three stages of the water cycle with correct vocabulary",
                    "Demonstrate evaporation and condensation with a simple experiment",
                    "Explain where rain comes from and where it goes",
                ],
                "spiral_review": [
                    "Revisit the daily weather and the clouds, which the water cycle forms and fills",
                ],
            },
            "classical": {
                "narrative_introduction": "The same water has been upon the Earth since the beginning, never lost, never made anew, but forever moving in a circle. The sun lifts it unseen from the sea, the cold air gathers it into clouds, the clouds let it fall again as rain, and the rivers carry it back to the sea. To know the water cycle is to know one of the great unbroken patterns that keep the world.",
                "memory_work": {
                    "chants": [
                        "Chant the water cycle in order: evaporation, condensation, precipitation, and round again",
                        "Chant what each stage means: evaporation rises, condensation gathers, precipitation falls",
                    ],
                    "recitations": [
                        "Recite that water is never lost but only changes its form, rising as vapor, gathering as cloud, and falling as rain",
                    ],
                },
                "copywork": [
                    "Copy the three stages of the water cycle in order, each with a few words of meaning",
                ],
                "recitation_routine": "Begin each lesson by reciting the three stages of the water cycle in order before any new work or experiment.",
                "history_integration": "Tell that whole civilizations rose and fell by the water cycle, that the yearly flood of the Nile, fed by far-off rain, made Egypt rich, and that people have always settled where the cycle brings water to the land.",
                "read_aloud_suggestions": [
                    "A living account that follows a drop of water on its journey from sea to cloud to rain and back, read aloud so the child hears the cycle told as a story",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A beautifully illustrated living book that tells the journey of water through its cycle, with true artwork and never a workbook",
                ],
                "short_lesson_flow": "Let the lesson be the real water cycle, met out of doors and about the house. Watch a puddle shrink in the sun, find dew on the morning grass, see a cold glass grow wet, notice the steam from the kettle. Each is a stage of the cycle, observed and quietly named. The child records what they truly see in the nature notebook.",
                "narration_prompt": "Tell me about the puddle, or the dew, or the wet glass. What happened to the water, and which stage of the cycle was it?",
                "real_world_objects": [
                    "A real puddle, marked and watched as it evaporates",
                    "A cold glass that gathers condensation, the morning dew, the kettle's steam",
                    "A nature notebook for recording the cycle observed",
                    "A sealed bag of water at a sunny window, a small water cycle to watch",
                ],
                "nature_connection": "The water cycle is met directly in nature: the rain, the dew, the fog, the drying puddle, the river running to the sea, and the child learns it by watching the real water moving around them.",
                "habit_focus": "The habit of attention: noticing the water cycle quietly at work in the puddle, the dew, and the rain of ordinary days.",
            },
            "montessori": {
                "prepared_materials": [
                    "A water cycle experiment tray: sealed bags, a glass, and water, for the child to set up alone",
                    "Three-part nomenclature cards for the stages of the water cycle",
                    "A water cycle diagram for the child to build and label",
                    "A magnifying glass for observing droplets of condensation",
                ],
                "presentation": {
                    "three_period_lesson": "With the water cycle cards: this stage is evaporation, the water rises as vapor; show me evaporation; which stage of the cycle is this?",
                    "steps": [
                        "The child sets up the water-cycle-in-a-bag experiment on the tray and observes it over hours",
                        "The child names each stage as it appears: evaporation, condensation, precipitation",
                        "The child works the nomenclature cards and builds the labeled water cycle diagram",
                    ],
                },
                "control_of_error": "The experiment is the control: in the sealed bag the child sees evaporation, condensation, and precipitation happen for themselves, and the three-part cards match the stages in one true way, so a misnamed stage does not fit.",
                "abstraction_pathway": "From watching the real cycle in the sealed-bag experiment, to matching the nomenclature cards and building the diagram, toward explaining the whole cycle and the journey of water without the materials.",
                "extensions": [
                    "Connect the cycle to the three states of water: solid, liquid, and gas",
                    "Measure how long a puddle takes to evaporate",
                    "Compare the water cycle in a warm climate and a cold one",
                ],
                "observation_focus": "Watch for the child naming the stages in correct order and understanding that water is not lost when it evaporates but only changed in form.",
            },
            "unschooling": {
                "invitations": [
                    "Keep sealed bags, a clear glass, and chalk available for water cycle experiments",
                    "Leave out books about water, rain, and weather",
                    "Let the cycle be noticed in the everyday: the kettle, the puddle, the dew",
                ],
                "real_world_contexts": [
                    "Watching puddles shrink and dry on a sunny day",
                    "Noticing dew on the morning grass and fog on a cool morning",
                    "Seeing the kettle steam, and water beads on a cold drink",
                    "Watching rain fall, run into drains, and feed the rivers",
                ],
                "conversation_starters": [
                    "The puddle was here this morning, where did the water go?",
                    "There is no water in the bag but droplets on the side, where did they come from?",
                    "Where do you think the rain goes after it falls?",
                ],
                "resource_bank": [
                    "Sealed bags and a clear glass for simple experiments",
                    "Books about water, weather, and rivers",
                    "The everyday water cycle: kettles, puddles, dew, and rain",
                ],
                "parent_role": "Wonder aloud at the water cycle wherever it shows itself, the drying puddle, the steaming kettle, the wet cold glass, the falling rain, and follow the child's questions into a simple experiment if they wish. Let the real, everyday movement of water, rather than a worksheet, do the teaching.",
                "observation_documentation": "Over time, note whether the child can tell the stages of the water cycle, recognizes evaporation and condensation when they see them, and understands where rain comes from and where it goes. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Water cycle vocabulary builds science literacy: evaporation, condensation, precipitation, vapor, cycle",
            "math": "Measuring rainfall in a rain gauge. Timing how long a puddle takes to evaporate. Temperature at which water boils (212°F/100°C) and freezes (32°F/0°C).",
            "history": "Water supply shaped every civilization: the water cycle determines where rain falls, where rivers flow, and where people can live. The Nile's annual flood IS the water cycle in action.",
        },
    },
    "sf-09": {
        "enriched": True,
        "learning_objectives": [
            "Collect, observe, and sort rocks by at least 3 properties: color, texture, hardness, and size",
            "Explain that soil is made from broken-down rocks mixed with decomposed living material",
            "Identify rocks as igneous (from volcanoes), sedimentary (layers), or metamorphic (changed by heat/pressure) at a basic level",
            "Describe weathering: the process that breaks rocks into smaller pieces and eventually into soil",
        ],
        "teaching_guidance": {
            "introduction": "Rocks are the story of Earth written in stone — literally. Every rock was formed by a process: volcanic eruptions (igneous), layers of sediment pressing together (sedimentary), or extreme heat and pressure changing existing rock (metamorphic). Soil, the dirt beneath our feet, is mostly tiny pieces of rock mixed with decomposed plants and animals. Rock collecting is one of the most naturally engaging science activities: children love finding, sorting, and classifying rocks. It combines outdoor exploration, careful observation, and the thrill of a treasure hunt.",
            "scaffolding_sequence": [
                "Go on a rock collecting walk: gather 10-15 rocks of different colors, sizes, and textures from the yard, a park, or a trail",
                "Observe each rock using the five senses (except taste!): What color? What texture? Is it heavy or light? Rough or smooth? Shiny or dull?",
                "Sort rocks by ONE property at a time: first by color, then by texture (rough/smooth), then by size, then by hardness (can you scratch it with a fingernail?)",
                "Introduce the 3 rock types: igneous (formed from cooled lava — often dark, may have holes), sedimentary (formed from layers — often has visible layers or grains), metamorphic (changed by heat/pressure — often shiny or banded)",
                "Examine soil: what is it made of? Look closely with a magnifying glass. You'll see tiny rock pieces, sand, clay, and bits of dead plants.",
                "Discuss weathering: water, wind, ice, and plant roots break big rocks into smaller pieces over time. This is how mountains become soil — very slowly.",
                "Create a rock collection display: label each rock with its properties and (if identifiable) its type",
                "Connect rock types to the rock cycle: rocks change form over millions of years — sedimentary can become metamorphic, which can melt and become igneous",
            ],
            "socratic_questions": [
                "These two rocks look very different — one is smooth and one is rough. Why might rocks have such different textures?",
                "This rock has layers in it, like a layer cake. How do you think those layers got there?",
                "Soil looks like just dirt, but it's actually made of something. If you look at it with a magnifying glass, what do you see?",
                "Big rocks eventually become tiny pieces. What breaks them apart? Think about water, ice, wind, and even tree roots.",
            ],
            "practice_activities": [
                "Rock collection and classification: collect 10+ rocks. Sort by color, then texture, then hardness. Display and label your collection.",
                "Scratch test: try scratching each rock with a fingernail (soft), a penny (medium), and a nail (hard). Sort by hardness.",
                "Soil investigation: take a spoonful of soil and examine it with a magnifying glass. What do you see? Tiny rocks, sand, clay, dead plant material?",
                "Sugar cube weathering: put a sugar cube in water and watch it dissolve. This demonstrates how water weathers rock — very slowly in nature, but the same principle.",
            ],
            "real_world_connections": [
                "Buildings and roads are made from rocks: granite countertops, marble floors, sandstone walls, gravel roads. We use different rocks for different purposes.",
                "Soil grows our food: everything we eat from farms grew in soil, which is broken-down rock + organic matter. No soil, no food.",
                "Mountains are being slowly worn down by weathering RIGHT NOW: rain, wind, ice, and plant roots are breaking rock into soil constantly",
                "Fossils are found in sedimentary rock: layers of sediment buried and preserved ancient organisms. Finding a fossil is finding ancient life in stone.",
            ],
            "common_misconceptions": [
                "Thinking rocks are all the same — rocks vary enormously in color, texture, hardness, and formation. Each rock has a unique story.",
                "Believing soil is 'just dirt' with no value — soil is a complex mixture of minerals, organic matter, water, and air that supports ALL terrestrial life",
                "Assuming rock formation happens quickly — most rocks form over thousands to millions of years. Geological time is vastly different from human time.",
                "Thinking weathering only means weather — weathering includes ANY process that breaks down rock: water, ice, wind, temperature changes, plant roots, and even chemical reactions",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Sorts rocks by 3+ properties with accurate descriptions",
                "Explains that soil comes from broken-down rocks plus organic material",
                "Identifies basic rock types with some accuracy",
            ],
            "proficiency_indicators": [
                "Sorts by 2 properties",
                "Knows soil contains rock but cannot explain further",
            ],
            "developing_indicators": [
                "Sorts by 1 property (usually color)",
                "Cannot explain soil composition",
            ],
            "assessment_methods": ["rock sorting and classification", "soil investigation", "rock type identification"],
            "sample_assessment_prompts": [
                "Sort these rocks 3 different ways. Explain your sorting.",
                "What is soil made of? Use the magnifying glass to show me.",
                "This rock has layers. What type of rock might it be?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which of these is NOT a way to sort rocks?",
                "expected_type": "multiple_choice",
                "options": ["By color", "By texture (smooth or rough)", "By how funny they look", "By hardness"],
                "correct_answer": "By how funny they look",
                "hints": ["Scientific sorting uses observable PROPERTIES: things you can see, feel, or test."],
                "explanation": "Scientists sort rocks by measurable properties: color, texture, hardness, size, weight, and type. 'How funny they look' is a personal opinion, not a scientific property.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "True or false: Soil is made mostly from broken-down rocks.",
                "expected_type": "true_false",
                "correct_answer": "true",
                "hints": ["Look at soil with a magnifying glass. What do the tiny pieces look like?"],
                "explanation": "True. Soil is primarily made of tiny rock fragments (sand, silt, clay) mixed with decomposed organic matter (dead plants and animals). Weathering breaks rocks down over thousands of years into the fine particles that make up soil.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Collect 5 rocks from outside. For each one, describe its color, texture (rough or smooth), and relative hardness (can you scratch it with your fingernail?). Record your observations in your science notebook.",
                "expected_type": "text",
                "hints": [
                    "For each rock: look at it (color, pattern), feel it (rough, smooth, bumpy), and test it (scratch with fingernail — if it scratches, it's soft; if not, it's hard)."
                ],
                "explanation": "A good collection record describes each rock specifically: 'Rock 1: Gray with white speckles, rough texture, cannot scratch with fingernail (hard). Rock 2: Reddish-brown, smooth, crumbles slightly when scratched (soft).' Specific observations are the foundation of rock classification.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "A rock has visible layers, like a stack of pancakes. What type of rock is it most likely?",
                "expected_type": "multiple_choice",
                "options": ["Igneous", "Sedimentary", "Metamorphic"],
                "correct_answer": "Sedimentary",
                "hints": [
                    "Layers form when material settles in layers over time — like sand at the bottom of a lake building up year after year."
                ],
                "explanation": "Sedimentary rock forms from layers of sediment (sand, mud, shells) that are pressed together over millions of years. The visible layers are the key identifying feature. Sandstone, limestone, and shale are common sedimentary rocks.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Take a spoonful of soil and examine it with a magnifying glass. Draw what you see and describe at least 3 different materials you can identify in the soil.",
                "expected_type": "text",
                "hints": [
                    "Look for: tiny rock pieces, sand grains, bits of dead leaves or roots, clay, small insects, and possibly tiny worms. Soil is a MIXTURE."
                ],
                "explanation": "Through a magnifying glass, soil reveals its complexity: tiny rock fragments (sand and gravel), fine clay particles, pieces of decomposed leaves and roots (organic matter), possibly small organisms (insects, worms), and air pockets. This shows that soil is not 'just dirt' — it's a rich, complex mixture that supports life.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Sort your rock collection by 3 different properties.",
                "type": "open_response",
                "target_concept": "rock_classification",
                "rubric": "Mastery: sorts by 3+ properties with accurate descriptions. Proficient: 2 properties. Developing: 1 property.",
            },
            {
                "prompt": "Examine soil with a magnifying glass and tell me what it's made of.",
                "type": "open_response",
                "target_concept": "soil_composition",
                "rubric": "Mastery: identifies rock fragments, organic matter, and possibly organisms. Proficient: identifies 1-2 components. Developing: says 'just dirt.'",
            },
        ],
        "resource_guidance": {
            "required": ["rocks collected from outdoors", "magnifying glass", "soil sample", "science notebook"],
            "recommended": ["rock identification guide", "penny and nail for scratch testing"],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 20, "assessment": 10},
        "accommodations": {
            "dyslexia": "Rock collecting and sorting are entirely hands-on — no reading required. Draw rocks instead of writing descriptions. Oral explanations of sorting criteria. Magnifying glass observation is visual.",
            "adhd": "Outdoor rock collecting is a treasure hunt with movement. Sorting and scratch testing are hands-on. Soil investigation with a magnifying glass is engaging. Each activity is self-contained (15 minutes).",
            "gifted": "Research the rock cycle in detail. Investigate local geology: what rocks are common in your area and why? Begin a labeled rock collection with proper identification. Study fossils as a rock science extension.",
            "visual_learner": "Rock displays with labels. Magnified views of soil. Rock type comparison charts with photographs.",
            "kinesthetic_learner": "Handle every rock. Scratch testing. Dig for soil samples. Build a rock collection display.",
            "auditory_learner": "Describe rocks aloud while observing. Discuss sorting criteria. Tell the 'story' of how each rock type formed.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Rocks are the solid stuff of the Earth, and each was made by a process: cooled from melted rock, pressed from layers of sediment, or changed by heat and pressure. Soil is rock broken into tiny pieces and mixed with decomposed plants and animals. Today we collect and sort rocks by their properties, learn the three rock types, and learn how weathering breaks rock down, slowly, into soil.",
                "gradual_release": {
                    "i_do": "Hold up two rocks and observe them aloud: this one is gray and rough, this one reddish and smooth; I sort them by color, then by texture, then by hardness, scratching with a fingernail. Show a layered rock and name it sedimentary, and crumble a little soil to show the tiny rock pieces within.",
                    "we_do": "Sort a rock collection together by one property at a time, color, texture, size, hardness, examine soil with a magnifying glass, and name the three rock types.",
                    "you_do": "Child sorts rocks by at least three properties, explains that soil is broken-down rock plus decomposed living material, and identifies rocks as igneous, sedimentary, or metamorphic at a basic level.",
                },
                "guided_practice": [
                    "Collect rocks and sort them by one property at a time: color, texture, size, hardness",
                    "Examine a spoonful of soil with a magnifying glass and name what it is made of",
                    "Sort rocks toward the three types: igneous, sedimentary, metamorphic",
                ],
                "independent_practice": [
                    "Build and label a rock collection display, recording each rock's properties",
                    "Investigate weathering: watch how water slowly breaks something down",
                ],
                "mastery_check": [
                    "Sort rocks by at least three properties with accurate descriptions",
                    "Explain that soil is broken-down rock mixed with decomposed living material",
                    "Identify rocks as igneous, sedimentary, or metamorphic at a basic level",
                ],
                "spiral_review": [
                    "Revisit sorting and classifying by attribute, the skill rock classification depends on",
                ],
            },
            "classical": {
                "narrative_introduction": "The rocks beneath our feet are the oldest record on the Earth, the planet's history written in stone. Some were born of fire, cooled from melted rock; some were laid down in patient layers at the bottom of ancient seas; some were changed, deep underground, by heat and crushing weight. And all rock, given ages enough, is broken by weather into the soil that feeds the living world.",
                "memory_work": {
                    "chants": [
                        "Chant the three kinds of rock: igneous from fire, sedimentary from layers, metamorphic from heat and pressure",
                        "Chant what makes soil: broken rock and decayed life, mixed together over long ages",
                    ],
                    "recitations": [
                        "Recite that weathering, by water, ice, wind, and root, breaks the great rocks slowly into soil",
                    ],
                },
                "copywork": [
                    "Copy the three rock types, each with a few words of how it forms, and the words weathering, mineral, sediment",
                ],
                "recitation_routine": "Begin each lesson by reciting the three rock types and how each is formed before any new sorting or study.",
                "history_integration": "Tell that the first tools were stone, that whole ages of mankind are named for the rock they worked, and that the pyramids, the cathedrals, and the old roads were all built from the rock of the Earth.",
                "read_aloud_suggestions": [
                    "A living account of how a mountain rises and is slowly worn to soil, read aloud so the child hears the long story of stone",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A beautifully illustrated living book about rocks, mountains, or the Earth, with true artwork and never a dry textbook",
                ],
                "short_lesson_flow": "Go out and let the child gather rocks that catch their eye, a real treasure hunt. Back home, look at each one closely and quietly, and the child draws a favorite in the nature notebook with careful observations. Examine a little garden soil with a magnifying glass. Let the wonder of real stone, handled and looked at, be the lesson.",
                "narration_prompt": "Tell me about the rocks you found. How are they different from one another? What did you see in the soil?",
                "real_world_objects": [
                    "A collection of real rocks gathered on a walk",
                    "A magnifying glass for close looking",
                    "A spoonful of garden soil to examine",
                    "A nature notebook for drawing rocks and recording observations",
                ],
                "nature_connection": "Geology is met out of doors: the child gathers rocks on walks, digs in the garden soil, sees the layered stone of a cliff or a creek bank, and comes to know the Earth's materials by handling them.",
                "habit_focus": "The habit of attention: looking closely and patiently at a rock to see its true color, texture, and the story of how it was made.",
            },
            "montessori": {
                "prepared_materials": [
                    "Rock sorting trays and a magnifying glass",
                    "A collection of real rocks of the three types",
                    "Three-part nomenclature cards for igneous, sedimentary, and metamorphic rock",
                    "A soil sample for examination, and a penny and nail for scratch testing",
                ],
                "presentation": {
                    "three_period_lesson": "With the rock cards and specimens: this rock is sedimentary, see its layers; show me a sedimentary rock; which type of rock is this?",
                    "steps": [
                        "The child sorts a rock collection on the trays by one property at a time",
                        "The child tests hardness with the scratch test and matches rocks to the nomenclature cards",
                        "The child examines soil with the magnifying glass and finds the rock and the organic matter within",
                    ],
                },
                "control_of_error": "The nomenclature cards match each rock type to its name and picture in one true way, and the rock's own properties, its layers, its texture, its hardness, are the control: a rock placed in the wrong group does not match its evidence.",
                "abstraction_pathway": "From handling, sorting, and scratch-testing real rocks, to matching them to the nomenclature cards of the three types, toward understanding how rock forms and weathers into soil without the materials.",
                "extensions": [
                    "Connect the rock types in the rock cycle, one becoming another over ages",
                    "Investigate the local geology: what rocks are common nearby and why",
                    "Study fossils as ancient life preserved in sedimentary rock",
                ],
                "observation_focus": "Watch for the child sorting by true, observable properties, testing hardness carefully, and seeing soil as a mixture of broken rock and decayed life.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a tray or shelf for the child's growing rock collection",
                    "Leave out a magnifying glass, a rock guide, and a penny and nail for scratch testing",
                    "Let digging in the garden and the soil be part of ordinary play",
                ],
                "real_world_contexts": [
                    "Collecting interesting rocks on walks, at the beach, by the creek",
                    "Digging in the garden and noticing what the soil is made of",
                    "Noticing the stone in buildings, walls, gravel roads, and countertops",
                    "Seeing layered rock in a road cut, a cliff, or a creek bank",
                ],
                "conversation_starters": [
                    "Why do you think these two rocks look so different?",
                    "This rock has stripes like a layer cake, how do you think those got there?",
                    "What do you see when you look at the soil up close?",
                ],
                "resource_bank": [
                    "The child's own rock collection, kept where it can be sorted",
                    "A magnifying glass and a rock identification guide",
                    "The out-of-doors, full of rocks, soil, and stone",
                ],
                "parent_role": "Welcome the rocks the child gathers and give them a place to keep and sort them, and wonder aloud at how different each one is. Look at the soil together when the child digs, and let real rock-hunting and real digging, rather than a worksheet, teach the science of the Earth's materials.",
                "observation_documentation": "Over time, note whether the child sorts rocks by their properties, knows that soil is broken-down rock mixed with decayed life, and begins to tell the three rock types apart. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Geology vocabulary builds science literacy: igneous, sedimentary, metamorphic, weathering, erosion, mineral",
            "math": "Sorting and classifying are mathematical skills. Measuring rock dimensions. Counting and graphing rocks by type.",
            "history": "Ancient humans used rocks as tools (Stone Age). Pyramids are limestone (sedimentary). Understanding rocks IS understanding the material of civilization.",
        },
    },
    "sf-10": {
        "enriched": True,
        "learning_objectives": [
            "Predict and test which materials a magnet will attract and which it will not",
            "Demonstrate that magnets have two poles (north and south) and that like poles repel while opposite poles attract",
            "Explain that magnetism is an invisible force that can act through air and some materials",
            "Discover that magnets attract objects made of iron, nickel, and cobalt — not all metals",
        ],
        "teaching_guidance": {
            "introduction": "Magnets are magical — or at least they seem that way. An invisible force reaches through the air and pulls a paperclip right to the magnet without touching it. But it's not magic; it's physics. Magnets are a child's first encounter with invisible forces, and the experiments are endlessly engaging: What sticks to a magnet? What doesn't? What happens when you put two magnets together? Can a magnet work through paper? Through water? The answers are surprising and teach the child that the world is governed by forces they can investigate but not see.",
            "scaffolding_sequence": [
                "Give the child a magnet and let them explore: 'Go around the house and find out what sticks to your magnet and what doesn't.' No instruction first — just discovery.",
                "Sort the results: make two columns — 'attracted' and 'not attracted.' What do the attracted items have in common? (Most are metal — specifically iron, steel, nickel, cobalt.)",
                "Test the surprising exceptions: not ALL metals are magnetic. Aluminum foil, copper pennies, and gold jewelry are NOT attracted. Magnetic = iron-containing metals.",
                "Introduce poles: hold two magnets near each other. One way they snap together (attract). Flip one magnet and they push apart (repel). This is poles: north attracts south, north repels north.",
                "Test invisible force through materials: can a magnet attract a paperclip through a piece of paper? Through a book? Through water? Through your hand?",
                "Make iron filings visible: sprinkle iron filings (or fine steel wool shavings) on paper over a magnet. See the magnetic field pattern!",
                "Introduce the compass: a floating magnet that always points north. Earth itself is a giant magnet!",
                "Design a magnet experiment: the child creates their own question, predicts the answer, tests it, and records results",
            ],
            "socratic_questions": [
                "You found that a paperclip sticks but a plastic toy doesn't. What's different about the paperclip? What is it made of?",
                "A penny is metal, but the magnet doesn't attract it. Why not? Aren't all metals magnetic?",
                "The two magnets push each other away — you can feel the force but you can't see it. What invisible force is doing this?",
                "Can a magnet pull a paperclip through a piece of paper? Make a prediction, then test it. Were you right?",
            ],
            "practice_activities": [
                "Magnet scavenger hunt: test 20 items in the house. Record which are attracted and which are not. Look for patterns in the results.",
                "Pole exploration: hold two magnets together. Feel them attract. Now flip one. Feel them repel. Explore how the force changes with distance.",
                "Magnet through materials: test if a magnet can attract a paperclip through paper, cardboard, fabric, a plastic plate, a wooden cutting board, and water. Record results.",
                "Floating compass: magnetize a needle by rubbing it on a magnet 50 times in one direction. Float it on a small piece of cork in water. It points north — you built a compass!",
            ],
            "real_world_connections": [
                "Refrigerator magnets: the most familiar magnet in the house. They work because the fridge door is made of steel (iron-containing).",
                "Compasses use magnets: the needle is a tiny magnet that aligns with Earth's magnetic field to point north. Hikers, sailors, and explorers depend on this.",
                "Credit card stripes and hard drives store information using magnetism. Every time you use a computer, magnets are at work.",
                "MRI machines in hospitals use incredibly powerful magnets to see inside the human body without surgery — medical magnetism.",
            ],
            "common_misconceptions": [
                "Thinking all metals are magnetic — only metals containing iron, nickel, or cobalt are magnetic. Aluminum, copper, gold, and silver are NOT magnetic.",
                "Believing magnets work on everything — magnets only attract specific materials. Wood, plastic, glass, paper, and most metals are NOT attracted.",
                "Thinking bigger magnets are always stronger — strength depends on the material and how the magnet was made, not just its size. A small neodymium magnet can be far stronger than a large ceramic one.",
                "Assuming magnetic force requires contact — magnetism acts at a DISTANCE through air and even through some solid materials. This is what makes it seem like magic.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Predicts and tests magnetic attraction with 90%+ accuracy for common materials",
                "Demonstrates attraction and repulsion with two magnets and explains poles",
                "Explains that magnetism is an invisible force acting at a distance",
            ],
            "proficiency_indicators": [
                "Correctly identifies most magnetic vs non-magnetic items",
                "Demonstrates attraction/repulsion but struggles to explain why",
            ],
            "developing_indicators": [
                "Thinks all metals are magnetic",
                "Cannot explain the concept of magnetic poles",
            ],
            "assessment_methods": ["prediction and testing", "pole demonstration", "force-at-distance explanation"],
            "sample_assessment_prompts": [
                "Test these 10 items. Which will the magnet attract? Predict first, then test.",
                "Show me what happens when you put two magnets together both ways.",
                "Can a magnet pull a paperclip through a piece of cardboard? Show me.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which of these will a magnet attract?",
                "expected_type": "multiple_choice",
                "options": ["A wooden block", "A steel paperclip", "A rubber ball", "A plastic cup"],
                "correct_answer": "A steel paperclip",
                "hints": ["Magnets attract objects made of iron or steel. Which item is made of metal?"],
                "explanation": "A steel paperclip is attracted to a magnet because steel contains iron. Wood, rubber, and plastic are not magnetic materials. Remember: not all metals are magnetic — only iron-containing metals.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "True or false: All metals are attracted to magnets.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["Try a magnet on aluminum foil or a copper penny. Are they attracted?"],
                "explanation": "False. Only metals containing iron, nickel, or cobalt are magnetic. Aluminum, copper, gold, silver, and many other metals are NOT attracted to magnets. 'Metal' does not automatically mean 'magnetic.'",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Test 10 items in your house with a magnet. Record which ones are attracted and which are not. What pattern do you notice?",
                "expected_type": "text",
                "hints": [
                    "Test things like: spoons, coins, foil, cans, scissors, toys, doorknobs, screws. Record each result. What do the attracted items have in common?"
                ],
                "explanation": "The pattern: attracted items are made of iron or steel (paperclips, some cans, nails, screws, refrigerator door). Non-attracted items are wood, plastic, glass, aluminum, copper, paper, and fabric. The key insight is that magnetism depends on the MATERIAL, specifically iron content.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Hold two magnets near each other. What happens? Now flip one magnet and try again. What changes? Why?",
                "expected_type": "text",
                "hints": [
                    "One way they snap together (attract). The other way they push apart (repel). This has to do with the magnet's POLES."
                ],
                "explanation": "When opposite poles (north-south) face each other, magnets attract — they pull together. When same poles (north-north or south-south) face each other, magnets repel — they push apart. This is the fundamental rule of magnetism: opposites attract, likes repel.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Design your own magnet experiment. Write a question, a prediction, what you did, and what happened. Example question: 'Can a magnet attract a paperclip through water?'",
                "expected_type": "text",
                "hints": [
                    "Steps: (1) Ask a question. (2) Predict the answer. (3) Test it. (4) Record what happened. (5) Was your prediction right?"
                ],
                "explanation": "A well-designed experiment has: a clear question (Can a magnet work through water?), a prediction (I think yes/no because...), a test procedure (put a paperclip in water, hold a magnet against the glass), observed results (the paperclip moved toward the magnet!), and a conclusion (magnetism DOES work through water). This is the scientific method at its simplest and most powerful.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Predict which of these 10 items a magnet will attract. Then test. How accurate were your predictions?",
                "type": "open_response",
                "target_concept": "magnetic_materials",
                "rubric": "Mastery: 9-10 correct predictions. Proficient: 7-8. Developing: random guessing.",
            },
            {
                "prompt": "Show me attraction and repulsion with two magnets. Explain why.",
                "type": "open_response",
                "target_concept": "magnetic_poles",
                "rubric": "Mastery: demonstrates both and explains opposite/like poles. Proficient: demonstrates but cannot explain. Developing: cannot demonstrate.",
            },
        ],
        "resource_guidance": {
            "required": [
                "bar magnets (at least 2)",
                "collection of items to test (paperclips, coins, foil, wood, plastic)",
            ],
            "recommended": [
                "iron filings for visualizing magnetic fields",
                "compass for demonstrating Earth's magnetism",
            ],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 20, "assessment": 10},
        "accommodations": {
            "dyslexia": "Magnet experiments are entirely hands-on — no reading required. Record results with check marks (attracted) and X marks (not attracted). Oral explanations of discoveries.",
            "adhd": "Magnet exploration is inherently fascinating and hands-on. The scavenger hunt involves movement around the house. Each experiment produces an immediate, visible result. Self-directed exploration for 20 minutes is typical.",
            "gifted": "Introduce electromagnets (battery + wire + nail). Research how MRI machines work. Explore Earth's magnetic field and its effect on navigation. Design experiments testing magnetic strength through different materials and distances.",
            "visual_learner": "Iron filings on paper over a magnet make the invisible magnetic field VISIBLE. Charts recording attracted vs not attracted. Compass needle visibly pointing north.",
            "kinesthetic_learner": "Handling magnets and test objects is the core activity. Feel the pull of attraction. Feel the push of repulsion. Build a compass. Magnetic fishing game.",
            "auditory_learner": "Discuss predictions before testing: 'What do you think will happen? Why?' Talk through results. Verbal explanations of the rules of magnetism.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "A magnet pulls certain objects toward it with an invisible force. That force is magnetism. Magnets attract only metals that contain iron, nickel, or cobalt, not all metals and nothing else. Every magnet has two poles, a north and a south; opposite poles attract, like poles repel. Today we predict and test what magnets attract, explore the poles, and learn that magnetism reaches through air and some materials.",
                "gradual_release": {
                    "i_do": "Hold a magnet to several objects and think aloud: the steel paperclip is pulled, the plastic toy is not, the copper penny is not, so it is not all metal but iron-containing metal. Bring two magnets together one way to feel them attract, flip one to feel them repel, and pull a paperclip through paper to show the force reaching across.",
                    "we_do": "Predict and test together what a magnet will attract, sort the results, explore attraction and repulsion with two magnets, and test the force through paper, cloth, and water.",
                    "you_do": "Child predicts and tests which materials a magnet attracts, demonstrates attraction and repulsion with the poles, and explains that magnetism is an invisible force acting through air and some materials.",
                },
                "guided_practice": [
                    "Predict, then test, which household objects a magnet attracts, and sort the results",
                    "Bring two magnets together both ways to feel attraction and repulsion",
                    "Test whether a magnet's force reaches through paper, cloth, and water",
                ],
                "independent_practice": [
                    "Go on a magnet scavenger hunt, recording attracted and not-attracted, and look for the pattern",
                    "Design and carry out an original magnet experiment",
                ],
                "mastery_check": [
                    "Predict and test magnetic attraction accurately for common materials",
                    "Demonstrate attraction and repulsion with two magnets and explain the poles",
                    "Explain that magnetism is an invisible force that acts through air and some materials",
                ],
                "spiral_review": [
                    "Revisit sorting objects by a property, the skill used to sort the attracted from the not-attracted",
                ],
            },
            "classical": {
                "narrative_introduction": "There are forces in the world that the eye cannot see, and magnetism is the first of them a child may meet and master. An unseen power reaches out from a magnet, across the empty air, and draws iron to itself. It is not magic but a law of nature, with rules as sure as any: opposite poles draw together, like poles drive apart, and only certain metals answer the call.",
                "memory_work": {
                    "chants": [
                        "Chant the rule of the poles: opposite poles attract, like poles repel",
                        "Chant what a magnet attracts: iron, nickel, and cobalt, and not all metals besides",
                    ],
                    "recitations": [
                        "Recite that magnetism is an invisible force, that it acts at a distance through air and through some materials, and that every magnet has a north pole and a south",
                    ],
                },
                "copywork": [
                    "Copy the rule of the poles and the words magnet, attract, repel, pole, and magnetic field",
                ],
                "recitation_routine": "Begin each lesson by reciting the rule of the poles and what a magnet attracts before any new testing.",
                "history_integration": "Tell that the ancients found stones, called lodestones, that drew iron of themselves, that the Chinese made the first compass from such a stone, and that this small invisible force opened the seas to navigators and changed the map of the world.",
                "read_aloud_suggestions": [
                    "An account of the compass and how it guided explorers across unknown seas, read aloud so the child hears magnetism put to great use",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A living book about magnets, the compass, or invisible forces, written with wonder and never as a dry reader",
                ],
                "short_lesson_flow": "Give the child a magnet and let them simply explore, with no instruction first: go about the house and discover what the magnet pulls and what it does not. Let wonder come before any word like pole or force. Afterward, the child tells what they found and records a few discoveries in the science notebook. Stop while the magic is still fresh.",
                "narration_prompt": "Tell me what you discovered with the magnet. What did it pull toward itself, and what did it leave alone?",
                "real_world_objects": [
                    "A magnet, and the whole house full of things to test",
                    "Two magnets for feeling attraction and repulsion",
                    "A compass, a tiny magnet that finds the north",
                    "A science notebook for recording discoveries",
                ],
                "nature_connection": "Carry the magnet outdoors: test the iron in sand or soil, and speak of the Earth itself as a vast magnet, with its own north and south, that the compass needle feels and obeys.",
                "habit_focus": "The habit of wonder and of attention: marveling at an unseen force and watching closely what it does.",
            },
            "montessori": {
                "prepared_materials": [
                    "A magnet experiment tray with bar magnets, a collection of test objects, and a recording sheet",
                    "Two magnets for exploring the poles",
                    "A compass for the practical-life extension",
                    "Iron filings for making the magnetic field visible",
                ],
                "presentation": {
                    "three_period_lesson": "With two magnets: this is attraction, the poles pull together, this is repulsion, they push apart; show me repulsion; is this attraction or repulsion?",
                    "steps": [
                        "The child works through the tray, predicting and then testing each object, and recording attracted or not attracted",
                        "The child explores the two magnets, feeling attraction and repulsion, and naming the poles",
                        "The child tests the force through materials and may make the field visible with iron filings",
                    ],
                },
                "control_of_error": "The magnet itself is the control: a prediction is confirmed or corrected the instant the object is brought near, with no need of an adult, so the child checks every guess against the real force.",
                "abstraction_pathway": "From freely testing real objects with a real magnet, to recording the results and finding the pattern, toward understanding magnetism as an invisible force with sure laws, acting at a distance.",
                "extensions": [
                    "Make the magnetic field visible with iron filings on paper",
                    "Build a floating compass from a magnetized needle",
                    "Investigate how the force changes with distance and through different materials",
                ],
                "observation_focus": "Watch for the child predicting before testing, noticing that only iron-containing metals are attracted, and grasping that the force reaches across a distance.",
            },
            "unschooling": {
                "invitations": [
                    "Keep magnets of different kinds within easy reach for free play",
                    "Leave out a compass, a box of varied objects to test, and iron filings",
                    "Have a magnetic board or the refrigerator for everyday magnet play",
                ],
                "real_world_contexts": [
                    "Discovering what around the house sticks to a magnet and what does not",
                    "Using refrigerator magnets and noticing why they hold to the door",
                    "Playing with a compass and watching the needle always find the north",
                    "Building toys and games that use magnets",
                ],
                "conversation_starters": [
                    "The paperclip sticks but the plastic toy does not, what is different about them?",
                    "This penny is metal, why does the magnet not pull it?",
                    "Can the magnet pull the paperclip through the paper? What do you predict?",
                ],
                "resource_bank": [
                    "A set of magnets and a compass kept available",
                    "A box of varied objects, metal and not, to test",
                    "Books about magnets, the compass, and invisible forces",
                ],
                "parent_role": "Hand the child magnets and let them discover freely what magnetism does, welcoming every surprise. Wonder aloud about the poles and the unseen force, answer the questions that arise, and let real play with real magnets, rather than a worksheet, do the teaching.",
                "observation_documentation": "Over time, note whether the child can predict and test what a magnet attracts, knows the rule of the poles, and understands that magnetism is an invisible force acting at a distance. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Magnet vocabulary builds science literacy: attract, repel, poles, magnetic field, force, compass",
            "math": "Measuring magnetic force: how many paperclips can a magnet hold? Does distance affect force? Graphing attraction strength.",
            "history": "Ancient Chinese invented the compass using natural magnets (lodestones). Navigation with compasses changed exploration and trade forever.",
        },
    },
    "sf-11": {
        "enriched": True,
        "learning_objectives": [
            "Name at least 5 sources of light including the sun, fire, light bulbs, and screens",
            "Explain that shadows form when an opaque object blocks light traveling in a straight line",
            "Predict how shadow size and position change as the light source moves",
            "Classify materials as opaque (blocks light), translucent (lets some through), or transparent (lets all through)",
        ],
        "teaching_guidance": {
            "introduction": "Light is energy we can see, and shadows are the dark shapes that form when something blocks that light. Children are fascinated by shadows — they chase them on the playground, make shadow puppets on the wall, and notice their shadow changing length during the day. These everyday observations are the starting point for understanding how light works: it travels in straight lines, it comes from sources (the sun, light bulbs, fire), and when an opaque object blocks it, a shadow forms on the other side.",
            "scaffolding_sequence": [
                "Go outside on a sunny day and explore shadows: step on your shadow, make shapes, notice which direction all shadows point",
                "Introduce light sources: the sun (natural), light bulbs, candles, flashlights, screens. List as many as you can.",
                "Demonstrate that light travels in a straight line: shine a flashlight — the beam goes straight. Bend a tube — the light doesn't follow the curve.",
                "Shadow formation: in a dark room, shine a flashlight at a toy. The shadow appears on the wall behind it. Why? The toy BLOCKS the light.",
                "Experiment with shadow size: move the flashlight closer to the toy (bigger shadow) and farther away (smaller shadow). Why does size change?",
                "Classify materials: hold different objects in front of the flashlight. Opaque (cardboard — blocks all light), translucent (wax paper — lets some through), transparent (clear glass — lets all through).",
                "Shadow tracing: trace your shadow at 9am, noon, and 3pm. Notice how it changes position and length as the sun moves across the sky.",
                "Shadow puppets: create a shadow puppet show using cut-out shapes and a flashlight — applied light science as art!",
            ],
            "socratic_questions": [
                "Your shadow is long in the morning and short at noon. Why does it change? What is the sun doing differently?",
                "I moved the flashlight closer to the puppet and the shadow got bigger. Why do you think that happens?",
                "This piece of wax paper lets SOME light through but not all. What happens to the shadow behind it?",
                "Why don't transparent things like glass windows make shadows?",
            ],
            "practice_activities": [
                "Shadow tracing: at 9am, noon, and 3pm, go outside and trace your shadow on the sidewalk with chalk. How did it change?",
                "Material sorting: test 10 household items with a flashlight. Sort into opaque, translucent, and transparent.",
                "Shadow puppet theater: cut shapes from cardboard, tape to sticks, and perform a shadow puppet show using a flashlight and a white sheet.",
                "Light source scavenger hunt: find and list every source of light in your home (lamps, screens, candles, oven light, nightlight, etc.).",
            ],
            "real_world_connections": [
                "Sundials tell time using shadows — one of the oldest clocks in human history, and the child can build one",
                "Sunglasses block light to protect your eyes. Window blinds control how much light enters a room. We manage light every day.",
                "X-rays work because bones are opaque to X-ray light while soft tissue is more transparent — medical light science",
                "Photography literally means 'writing with light' — cameras capture light bouncing off objects",
            ],
            "common_misconceptions": [
                "Thinking shadows are objects or substances — shadows are simply the ABSENCE of light where an object blocks it. They have no substance.",
                "Believing your shadow is always the same size — shadow size changes with the angle and distance of the light source throughout the day",
                "Thinking light bends around corners — light travels in straight lines. Shadows prove this: if light curved around objects, there would be no shadows.",
                "Confusing translucent with transparent — translucent lets SOME light through (frosted glass, wax paper), while transparent lets NEARLY ALL light through (clear glass, water)",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Names 5+ light sources",
                "Explains shadow formation using 'light travels in straight lines' and 'opaque objects block light'",
                "Predicts shadow size changes when light source distance changes",
            ],
            "proficiency_indicators": [
                "Names 3-4 light sources",
                "Knows shadows form when light is blocked but cannot explain the mechanism",
            ],
            "developing_indicators": [
                "Names 1-2 light sources (usually sun and light bulb)",
                "Cannot explain why shadows form",
            ],
            "assessment_methods": ["light source listing", "shadow experiment", "material classification"],
            "sample_assessment_prompts": [
                "Name 5 things that produce light.",
                "Why does a shadow form? Show me with the flashlight.",
                "Is this material opaque, translucent, or transparent? How do you know?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which of these is NOT a source of light?",
                "expected_type": "multiple_choice",
                "options": ["The sun", "A flashlight", "A rock", "A candle"],
                "correct_answer": "A rock",
                "hints": ["A light source produces its own light. Which item does NOT glow or shine?"],
                "explanation": "A rock does not produce light — it is not a light source. The sun, flashlights, and candles all produce their own light. A rock can only be SEEN when light from another source bounces off it.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "True or false: Shadows form because an object blocks light.",
                "expected_type": "true_false",
                "correct_answer": "true",
                "hints": ["What happens when you stand between a light and a wall?"],
                "explanation": "True. Shadows form when an opaque object blocks light traveling in a straight line. The area behind the object doesn't receive light, creating a dark shape — the shadow.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Go outside and trace your shadow with chalk at three different times today (morning, midday, and afternoon). Describe how your shadow changed.",
                "expected_type": "text",
                "hints": [
                    "Look at: the LENGTH of your shadow and the DIRECTION it points. How does the sun's position affect both?"
                ],
                "explanation": "In the morning (sun low in east), your shadow is long and points west. At midday (sun high overhead), your shadow is short and points north (in the Northern Hemisphere). In the afternoon (sun low in west), your shadow is long and points east. The sun's position directly determines shadow length and direction.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You move a flashlight closer to a toy and the shadow on the wall gets bigger. Why?",
                "expected_type": "text",
                "hints": [
                    "Think about the light spreading out from the flashlight. When the flashlight is close, does the toy block more or less of that spreading light?"
                ],
                "explanation": "When the flashlight is close, the light rays spread at a wider angle around the toy, making the shadow larger. When the flashlight is far away, the rays are more parallel and the shadow is closer to the toy's actual size. Distance between light and object affects shadow size.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Test 5 items with a flashlight: hold each one between the flashlight and a wall. Sort them into opaque (blocks all light), translucent (lets some through), and transparent (lets all through). Record your results.",
                "expected_type": "text",
                "hints": [
                    "Try: cardboard, wax paper, clear glass, your hand, a thin cloth. What happens to the light with each one?"
                ],
                "explanation": "Example results: Cardboard = opaque (blocks all light, dark shadow). Wax paper = translucent (dim light passes through, soft shadow). Clear glass = transparent (light passes through, almost no shadow). Your hand = opaque. Thin white cloth = translucent. Classifying materials by light transmission is a fundamental physics skill.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Explain why shadows form. Use the flashlight to demonstrate.",
                "type": "open_response",
                "target_concept": "shadow_formation",
                "rubric": "Mastery: explains straight-line travel and blocking. Proficient: says object blocks light. Developing: cannot explain.",
            },
            {
                "prompt": "Sort 5 materials into opaque, translucent, and transparent.",
                "type": "open_response",
                "target_concept": "material_classification",
                "rubric": "Mastery: all correct with explanations. Proficient: most correct. Developing: confuses categories.",
            },
        ],
        "resource_guidance": {
            "required": ["flashlight", "various objects for shadow experiments", "chalk for outdoor shadow tracing"],
            "recommended": [
                "materials for opacity testing (cardboard, wax paper, clear plastic)",
                "shadow puppet supplies",
            ],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Light experiments are entirely visual and hands-on. Shadow tracing requires no reading. Oral descriptions of observations. Drawing shadows rather than writing about them.",
            "adhd": "Shadow tracing outdoors involves movement. Flashlight experiments in a dark room are exciting. Shadow puppet show is creative and performative. Each experiment is self-contained (10 minutes).",
            "gifted": "Explore reflection (mirrors) and refraction (bending light through water). Research how lenses work. Build a simple periscope. Discuss the speed of light.",
            "visual_learner": "Light and shadow are inherently visual topics. Shadow tracing, material testing, and puppet shows are all visual activities.",
            "kinesthetic_learner": "Move the flashlight and objects. Trace shadows outdoors. Build shadow puppets. Physical manipulation of light.",
            "auditory_learner": "Discuss observations: 'What happened when I moved the light closer?' Verbal predictions before each test.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Light is energy we can see, and it travels in straight lines from a source: the sun, a flame, a bulb, a screen. When an opaque object stands in the light's path, it blocks the light and a shadow forms behind it. Today we name sources of light, learn how and why shadows form, predict how a shadow changes as the light moves, and sort materials as opaque, translucent, or transparent.",
                "gradual_release": {
                    "i_do": "Name several sources of light, then shine a flashlight in a dark room and think aloud: the light travels straight; when I put a toy in its path, the toy blocks the light and a shadow falls behind it. Move the flashlight closer to make the shadow grow, and hold up card, wax paper, and clear plastic to show opaque, translucent, and transparent.",
                    "we_do": "Name light sources together, make shadows with a flashlight and explain why they form, change the shadow's size by moving the light, and sort materials by how much light they let through.",
                    "you_do": "Child names sources of light, explains how a shadow forms, predicts how a shadow changes as the light moves, and classifies materials as opaque, translucent, or transparent.",
                },
                "guided_practice": [
                    "List sources of light around the home and outdoors",
                    "Make a shadow with a flashlight and explain why it forms",
                    "Move the light source and predict, then check, how the shadow changes",
                ],
                "independent_practice": [
                    "Trace a shadow outdoors at three times of day and describe how it changed",
                    "Test materials with a flashlight and sort them into opaque, translucent, and transparent",
                ],
                "mastery_check": [
                    "Name at least five sources of light",
                    "Explain that a shadow forms when an opaque object blocks light traveling in a straight line",
                    "Classify materials as opaque, translucent, or transparent",
                ],
                "spiral_review": [
                    "Revisit the sun's path across the sky, which moves a shadow through the day",
                ],
            },
            "classical": {
                "narrative_introduction": "Light pours from the sun and from every flame and lamp, and it travels always in straight lines, never bending round a corner. Where a solid thing stands in its path, the light is stopped, and behind the thing lies a shadow, a shape of darkness that is simply the place the light could not reach. To study light and shadow is to learn one of the plainest and surest laws of nature.",
                "memory_work": {
                    "chants": [
                        "Chant the law of light: light comes from a source and travels in straight lines",
                        "Chant the three kinds of material: opaque blocks the light, translucent lets some through, transparent lets it all through",
                    ],
                    "recitations": [
                        "Recite that a shadow forms when an opaque object blocks light traveling in a straight line, and that the shadow is not a thing but the absence of light",
                    ],
                },
                "copywork": [
                    "Copy the three kinds of material with their meanings, and the words source, shadow, opaque, translucent, transparent",
                ],
                "recitation_routine": "Begin each lesson by reciting the law of light and the three kinds of material before any new experiment.",
                "history_integration": "Tell that long before clocks people told the hours by shadow, that the sundial is among the oldest of instruments, and that the shadow play of ancient China and the far East turned the science of light into an art.",
                "read_aloud_suggestions": [
                    "A tale in which a shadow or the changing light is told with care and wonder, read aloud so the child hears light described",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A beautifully illustrated living book about light, shadows, or the sun, with true artwork and never a workbook",
                ],
                "short_lesson_flow": "Go out on a sunny day and let the child play with their own shadow: step on it, stretch it, make shapes, notice which way it falls. Trace it once with chalk, and come back hours later to find it has moved and changed. Indoors, a flashlight and a few objects let the wonder continue. Let delighted play be the lesson.",
                "narration_prompt": "Tell me about your shadow today. How was it different in the morning and the afternoon, and why?",
                "real_world_objects": [
                    "The child's own shadow, and chalk to trace it through the day",
                    "A flashlight and household objects for indoor shadow play",
                    "Materials to hold to the light: card, wax paper, clear glass",
                    "A science notebook for recording shadow observations",
                ],
                "nature_connection": "The sun and the child's own shadow are the lesson: out of doors the child watches the shadow lengthen and shorten and swing about as the sun travels the sky, learning light from the living day.",
                "habit_focus": "The habit of attention: noticing how a shadow changes through the day and asking why.",
            },
            "montessori": {
                "prepared_materials": [
                    "A light experiment tray with a flashlight and objects to cast shadows",
                    "Materials sorted for testing: opaque, translucent, and transparent",
                    "Classification cards for the three kinds of material",
                    "Chalk for outdoor shadow tracing, and materials for a sundial",
                ],
                "presentation": {
                    "three_period_lesson": "With the test materials: this card is opaque, it blocks the light; show me a material that is translucent; is this opaque, translucent, or transparent?",
                    "steps": [
                        "The child makes shadows with the flashlight and an object, seeing that the object blocks the straight-traveling light",
                        "The child moves the light and watches the shadow grow and shrink",
                        "The child tests materials against the light and sorts them into opaque, translucent, and transparent",
                    ],
                },
                "control_of_error": "The light is the control: a material sorted as transparent will plainly pass the light, and one sorted as opaque will plainly block it, so the flashlight itself shows the child any mistake.",
                "abstraction_pathway": "From making and changing real shadows with the flashlight, to sorting materials by how they meet the light, toward understanding that light travels straight and a shadow is where it is blocked.",
                "extensions": [
                    "Build and use a sundial, telling time by shadow",
                    "Explore reflection with a mirror",
                    "Make a shadow puppet theater",
                ],
                "observation_focus": "Watch for the child connecting the shadow to the blocked light, predicting how the shadow will change, and sorting materials accurately by their opacity.",
            },
            "unschooling": {
                "invitations": [
                    "Keep flashlights and a torch within reach for free shadow play",
                    "Leave out chalk for tracing shadows outdoors",
                    "Have materials of every kind, card, wax paper, glass, near a light for testing",
                ],
                "real_world_contexts": [
                    "Playing with shadows outdoors on a sunny day",
                    "Making shadow puppets on the wall at night",
                    "Noticing how a shadow is long in the morning and short at noon",
                    "Seeing how sunglasses, blinds, and curtains block and let through light",
                ],
                "conversation_starters": [
                    "Why is your shadow so long right now? What was the sun doing this morning?",
                    "I moved the light closer and the shadow grew, why do you think that happened?",
                    "Does light go through this? What about this?",
                ],
                "resource_bank": [
                    "Flashlights, a torch, and chalk kept available",
                    "Materials of all kinds to hold up to the light",
                    "The sun and the child's own shadow, free every sunny day",
                ],
                "parent_role": "Play with shadows alongside the child, make puppets, chase shadows, notice them lengthen, and wonder aloud about the light that makes them. Welcome the child's experiments with the flashlight, and let real shadow play, rather than a worksheet, teach how light behaves.",
                "observation_documentation": "Over time, note whether the child names sources of light, understands that a shadow forms where an object blocks the light, and can tell opaque, translucent, and transparent apart. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Light vocabulary: opaque, translucent, transparent, source, shadow, reflect. Stories about shadows (Peter Pan's shadow, Groundhog Day).",
            "math": "Measuring shadow length at different times. Comparing shadow sizes. Angles of light and shadow.",
            "history": "Sundials are ancient timekeeping devices using shadows. Shadow puppets originated in ancient China and Southeast Asia — thousands of years of shadow art.",
        },
    },
    "sf-12": {
        "enriched": True,
        "learning_objectives": [
            "Explain that sound is caused by vibration — an object must vibrate to produce sound",
            "Demonstrate how pitch changes with the length, tension, or thickness of a vibrating object",
            "Describe how sound travels from a source through the air to the ear",
            "Make a simple instrument and explain how it produces sound through vibration",
        ],
        "teaching_guidance": {
            "introduction": "Every sound you hear is caused by something vibrating. A guitar string vibrates, a drum skin vibrates, your vocal cords vibrate when you speak. The vibrations travel through the air as invisible waves and reach your ear, which turns them into signals your brain interprets as sound. Children can SEE vibration and FEEL it: touch your throat while humming, watch a rubber band vibrate when plucked, see water ripple when a tuning fork touches it. Sound is physics you can hear.",
            "scaffolding_sequence": [
                "Explore vibration: put your hand on your throat and hum. Feel the vibration? That's your vocal cords making sound.",
                "Visualize vibration: stretch a rubber band between two pencils and pluck it. WATCH it vibrate. HEAR the sound. The vibration IS the sound.",
                "Experiment with pitch: stretch the rubber band tighter and pluck again. Higher pitch! Loosen it — lower pitch. Tension changes pitch.",
                "Experiment with length: fill glasses with different amounts of water. Tap with a spoon. More water = lower pitch. Less water = higher pitch.",
                "Explore volume: tap a drum softly (quiet) and hard (loud). Volume depends on how much energy goes into the vibration.",
                "Sound travel: put your ear on a table and have someone tap the other end. Sound travels through the table! Sound travels through solids, liquids, AND air.",
                "Build a simple instrument: rubber band guitar (box + rubber bands), water glass xylophone, or tin can drum",
                "Sound walk: go outside and listen. List every sound you hear. For each one, identify what is vibrating to make that sound.",
            ],
            "socratic_questions": [
                "You plucked the rubber band and heard a sound. What did you SEE the rubber band doing? Is there a connection between the vibrating and the sound?",
                "You made the rubber band tighter and the sound changed. What changed — the pitch or the volume? Why?",
                "If sound needs vibration, can there be sound in outer space where there's no air to vibrate?",
                "You put your ear on the table and heard tapping louder than through the air. Why might sound travel better through a solid?",
            ],
            "practice_activities": [
                "Rubber band guitar: stretch rubber bands of different thicknesses over an open box. Pluck them and compare the sounds. Which is higher? Which is lower?",
                "Water glass xylophone: fill 5 glasses with different amounts of water. Tap each with a spoon. Arrange them from lowest to highest pitch.",
                "String telephone: connect two cups with a tight string. Talk into one and listen with the other. Sound vibrations travel along the string!",
                "Sound walk: go outside, close your eyes for 1 minute, and list every sound you hear. Then identify what is vibrating to make each sound.",
            ],
            "real_world_connections": [
                "Musical instruments ALL work through vibration: guitar strings, drum skins, piano hammers hitting strings, flute air columns. Music IS vibration.",
                "Your voice is a musical instrument: vocal cords vibrate, and you change pitch by tightening or loosening them (just like a guitar string).",
                "Noise pollution is unwanted sound vibration: loud sounds can damage hearing. That's why we wear ear protection around loud machines.",
                "Whales communicate through sound vibrations in water — sound travels 4 times faster in water than in air!",
            ],
            "common_misconceptions": [
                "Thinking sound travels through empty space — sound NEEDS a medium (air, water, or solid) to travel through. There is no sound in the vacuum of space.",
                "Believing louder sounds are higher pitched — volume and pitch are DIFFERENT properties. A bass drum is loud AND low-pitched. A quiet whistle is soft AND high-pitched.",
                "Thinking only musical instruments make sound through vibration — ALL sounds are vibrations: speech, clapping, wind, thunder, creaking doors. Everything.",
                "Assuming sound travels instantly — sound takes time to travel. Thunder follows lightning because light travels faster than sound. Count seconds between flash and boom to estimate distance.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Explains that all sound is caused by vibration",
                "Demonstrates pitch changes by changing tension, length, or thickness",
                "Describes sound traveling from vibrating source through air to ear",
            ],
            "proficiency_indicators": [
                "Knows sound involves vibration but cannot explain the mechanism",
                "Demonstrates pitch change without explaining why",
            ],
            "developing_indicators": [
                "Cannot connect vibration to sound",
                "Confuses pitch and volume",
            ],
            "assessment_methods": ["vibration demonstration", "pitch experiment", "sound travel explanation"],
            "sample_assessment_prompts": [
                "What causes sound? Show me with the rubber band.",
                "Make the rubber band sound higher. Now lower. What are you changing?",
                "How does sound get from the guitar to your ear?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What causes all sounds?",
                "expected_type": "multiple_choice",
                "options": ["Light", "Vibration", "Gravity", "Temperature"],
                "correct_answer": "Vibration",
                "hints": ["Touch your throat while humming. What do you feel? That's what makes the sound."],
                "explanation": "All sounds are caused by vibration. When an object vibrates (moves back and forth rapidly), it pushes air molecules, creating sound waves that travel to your ears.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "True or false: Sound can travel through outer space.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["Space is a vacuum — there's no air. Does sound need something to travel through?"],
                "explanation": "False. Sound needs a medium (air, water, or solid) to travel through. Space is a vacuum with no air, so sound cannot travel there. In space, no one can hear you scream — that's real physics!",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Stretch a rubber band between two pencils. Pluck it while it's loose. Then stretch it tight and pluck again. What changed about the sound? Why?",
                "expected_type": "text",
                "hints": [
                    "Listen to the pitch: is the tight rubber band higher or lower? Think about how tightness affects vibration speed."
                ],
                "explanation": "The tight rubber band produces a HIGHER pitch because it vibrates faster. The loose rubber band produces a LOWER pitch because it vibrates slower. Tension affects vibration speed, which determines pitch. This is exactly how guitar players tune their strings — tightening raises the pitch.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Fill 4 glasses with different amounts of water. Tap each with a spoon. Which has the highest pitch? Which has the lowest?",
                "expected_type": "text",
                "hints": [
                    "The glass with LESS water should have a different pitch than the one with MORE water. Try it and listen!"
                ],
                "explanation": "The glass with the LEAST water produces the HIGHEST pitch because the glass vibrates faster with less water dampening it. The glass with the MOST water produces the LOWEST pitch. This is why a water glass xylophone works — you 'tune' each glass by adding or removing water.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Build a simple string telephone with two cups and a string. Test it: can you hear someone talking through the string? Explain how the sound travels from one cup to the other.",
                "expected_type": "text",
                "hints": [
                    "The sound vibrations travel from the speaker's voice → cup → string → other cup → listener's ear. The string must be TIGHT for it to work."
                ],
                "explanation": "The string telephone works because: (1) Your voice makes air vibrate inside the cup. (2) The cup vibrates and transfers the vibration to the string. (3) The vibration travels along the tight string. (4) The other cup receives the vibration and converts it back to sound waves. The string must be tight because loose string doesn't transmit vibrations well. You built a sound transmission device!",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Show me that sound is caused by vibration. Use any object.",
                "type": "open_response",
                "target_concept": "vibration_sound",
                "rubric": "Mastery: demonstrates vibration and connects to sound with explanation. Proficient: shows vibration. Developing: cannot demonstrate.",
            },
            {
                "prompt": "Make a high sound and a low sound with the same object. Explain what you changed.",
                "type": "open_response",
                "target_concept": "pitch",
                "rubric": "Mastery: changes tension/length and explains why pitch changed. Proficient: changes pitch. Developing: confuses pitch and volume.",
            },
        ],
        "resource_guidance": {
            "required": ["rubber bands", "cups and string for telephone", "glasses and water for xylophone"],
            "recommended": [
                "tuning fork for visualizing vibration in water",
                "variety of materials for sound experiments",
            ],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 20, "assessment": 10},
        "accommodations": {
            "dyslexia": "Sound experiments are entirely hands-on and auditory — no reading required. Oral descriptions of observations. Drawing instruments rather than writing about them.",
            "adhd": "Instrument building is highly engaging. Making sounds is active and fun. Each experiment produces immediate audible results. Sound walks involve outdoor movement.",
            "gifted": "Research how different instruments produce sound. Explore frequency and wavelength. Investigate how sound-proofing works. Compare sound speed in air, water, and solids.",
            "visual_learner": "See vibrations: rubber band moving, water rippling from tuning fork. Draw sound wave diagrams.",
            "kinesthetic_learner": "Build instruments. Feel vibrations on throat, table, and rubber band. String telephone construction.",
            "auditory_learner": "Core strength area — the entire topic is about hearing. Sound walks. Instrument playing. Listening to pitch differences.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Every sound is made by something vibrating, moving quickly back and forth. The vibration travels out through the air as invisible waves and reaches the ear, which the brain hears as sound. A faster vibration makes a higher pitch; a stronger vibration makes a louder sound. Today we learn that sound comes from vibration, change pitch by changing a vibrating object, trace how sound travels to the ear, and build a simple instrument.",
                "gradual_release": {
                    "i_do": "Pluck a stretched rubber band and think aloud: I can see it vibrating and I can hear the sound, the vibration is the sound. Stretch it tighter and pluck again, the pitch rises. Hum with a hand on my throat to feel the vibration, and trace the sound from the band, through the air, to the ear.",
                    "we_do": "Make sounds with a rubber band and water glasses together, watching and feeling the vibration, and change the pitch by changing the tension, length, or thickness.",
                    "you_do": "Child explains that sound is caused by vibration, demonstrates a change in pitch, describes how sound travels to the ear, and builds a simple instrument.",
                },
                "guided_practice": [
                    "Pluck a rubber band and feel the throat while humming to connect vibration and sound",
                    "Change the pitch of a sound by changing tension, length, or thickness",
                    "Trace how sound travels from a vibrating object through the air to the ear",
                ],
                "independent_practice": [
                    "Build a simple instrument, a rubber band guitar or water glass xylophone, and explain how it makes sound",
                    "Take a sound walk and name what is vibrating to make each sound heard",
                ],
                "mastery_check": [
                    "Explain that sound is caused by vibration",
                    "Demonstrate how pitch changes with the length, tension, or thickness of a vibrating object",
                    "Describe how sound travels from its source through the air to the ear",
                ],
                "spiral_review": [
                    "Revisit careful listening and observation, the attentive senses sound study depends on",
                ],
            },
            "classical": {
                "narrative_introduction": "Listen, and every sound you hear, the voice, the bell, the wind, the drum, is born of one thing: something is trembling, vibrating swiftly back and forth. That trembling stirs the air, and the stir travels out in unseen waves until it reaches the ear. Sound is motion made audible, and to study it is to learn that even the music of the world obeys the laws of nature.",
                "memory_work": {
                    "chants": [
                        "Chant the first law of sound: every sound is made by something vibrating",
                        "Chant the rule of pitch: a faster vibration makes a higher sound, a slower one a lower sound",
                    ],
                    "recitations": [
                        "Recite that sound travels in waves through a medium, air, water, or solid, and that without a medium, as in the empty void of space, there is no sound",
                    ],
                },
                "copywork": [
                    "Copy the first law of sound and the rule of pitch, and the words vibration, pitch, volume, and medium",
                ],
                "recitation_routine": "Begin each lesson by reciting the first law of sound and the rule of pitch before any new experiment.",
                "history_integration": "Tell that music is among the most ancient of human arts, that flutes of bone were carved tens of thousands of years ago, and that every people on Earth has made instruments that sing by vibration.",
                "read_aloud_suggestions": [
                    "A living account of how an instrument or the human voice makes its sound, read aloud so the child hears the science of sound told",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A beautifully illustrated living book about sound, music, or instruments, with true artwork and never a dry reader",
                ],
                "short_lesson_flow": "Let the lesson be hands and ears. The child plucks a rubber band and watches it blur with vibration, hums with a hand on the throat, taps water glasses, and listens. Build one simple instrument together, gladly, and let the child play it. Then a quiet minute outdoors, listening to the sounds of the day. Keep it short and full of doing.",
                "narration_prompt": "Tell me what you saw and felt when the rubber band made its sound. What was moving?",
                "real_world_objects": [
                    "A stretched rubber band, to see vibration",
                    "Water glasses and a spoon, a simple xylophone",
                    "Two cups and a string for a telephone",
                    "The whole out-of-doors, full of sounds to listen for",
                ],
                "nature_connection": "On a quiet listening walk the child attends to the sounds of nature, the birdsong, the wind in the leaves, the running water, and for each one wonders what is vibrating to make it.",
                "habit_focus": "The habit of attention: listening closely to a sound and noticing what is vibrating to make it.",
            },
            "montessori": {
                "prepared_materials": [
                    "The sound cylinders for refining the discrimination of pitch and loudness",
                    "A sound experiment tray: rubber bands, cups and string, water glasses",
                    "Materials for building a simple instrument",
                    "A tuning fork for making vibration visible in water",
                ],
                "presentation": {
                    "three_period_lesson": "With two plucked rubber bands: this one sounds higher, this one lower; show me the higher sound; is this sound higher or lower?",
                    "steps": [
                        "The child explores the sound cylinders, matching and grading them by their sound",
                        "The child makes sounds with the rubber bands and water glasses, watching and feeling the vibration",
                        "The child changes the pitch by changing tension, length, or thickness, and builds a simple instrument",
                    ],
                },
                "control_of_error": "The sound cylinders pair and grade in one true order, audible to the attentive ear, and the rubber band is its own control: a child can both see it vibrate and hear the sound, so the link of vibration and sound checks itself.",
                "abstraction_pathway": "From refining the ear with the sound cylinders and seeing vibration in the rubber band, to changing pitch and building an instrument, toward understanding sound as vibration traveling in waves to the ear.",
                "extensions": [
                    "Compare how sound travels through air, water, and a solid",
                    "Build a fuller set of tuned instruments",
                    "Investigate how different instruments make their sound",
                ],
                "observation_focus": "Watch for the child connecting the seen and felt vibration to the heard sound, and keeping pitch and volume distinct.",
            },
            "unschooling": {
                "invitations": [
                    "Keep rubber bands, cups and string, and materials for instruments within reach",
                    "Leave out real instruments to play and explore",
                    "Let making sound and music be a welcome part of ordinary days",
                ],
                "real_world_contexts": [
                    "Playing instruments and making music",
                    "Feeling the throat vibrate while singing and humming",
                    "Tapping, drumming, and plucking household objects to hear their sounds",
                    "Listening, on a walk, for all the sounds of the world and what makes them",
                ],
                "conversation_starters": [
                    "When you plucked it you heard a sound, what did you see it doing?",
                    "How could you make that sound higher? What about lower?",
                    "Put your hand on your throat and hum, what do you feel?",
                ],
                "resource_bank": [
                    "Rubber bands, cups, string, and water glasses for sound play",
                    "Real instruments to explore and play",
                    "The whole world of everyday sound to listen to",
                ],
                "parent_role": "Make and enjoy sound and music with the child, and wonder aloud at what is vibrating whenever a sound is heard. Welcome the child's homemade instruments and noisy experiments, and let real playing, listening, and building, rather than a worksheet, teach the science of sound.",
                "observation_documentation": "Over time, note whether the child understands that sound comes from vibration, can change a sound's pitch, and knows that sound travels through the air to the ear. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Sound vocabulary: vibration, pitch, volume, frequency, medium, wave. Onomatopoeia in reading: words that sound like sounds (buzz, crash, whisper).",
            "math": "Patterns in pitch: mathematical relationships between string length and pitch. Counting beats. Rhythm is mathematical pattern.",
            "history": "Musical instruments have ancient origins: drums in every culture, flutes found in caves 40,000 years old. Sound science is embedded in cultural history.",
        },
    },
    "sf-13": {
        "enriched": True,
        "learning_objectives": [
            "Identify all 6 simple machines: lever, wheel and axle, pulley, inclined plane, wedge, and screw",
            "Find real-world examples of each simple machine in daily life",
            "Explain that simple machines make work easier by changing the direction or amount of force needed",
            "Demonstrate how at least one simple machine reduces effort through a hands-on experiment",
        ],
        "teaching_guidance": {
            "introduction": "Simple machines are everywhere — and most children use them every day without realizing it. A door handle is a lever. A wheelchair ramp is an inclined plane. A jar lid is a screw. A knife blade is a wedge. Bicycle wheels are wheels and axles. A flagpole rope is a pulley. These six devices are the building blocks of ALL machines, and they all do the same fundamental thing: make work easier by changing the amount or direction of force you need to apply.",
            "scaffolding_sequence": [
                "Start with the child's body: 'Your arm is a lever! Your elbow is the fulcrum. Watch how your arm lifts things.'",
                "Introduce all 6 with household examples: lever (bottle opener), wheel and axle (doorknob), pulley (blinds cord), inclined plane (ramp), wedge (knife), screw (jar lid)",
                "For each machine, demonstrate how it makes work EASIER: compare lifting a box straight up vs rolling it up a ramp (inclined plane makes it easier)",
                "Simple machine scavenger hunt: walk through the house and find 3 examples of EACH type. There are dozens!",
                "Build a lever: use a ruler balanced on a pencil. Place a weight on one end and push down on the other. The lever multiplies your force!",
                "Build a ramp experiment: set up a board on books. Roll objects down. Steeper ramp = faster roll. Ramps trade distance for force.",
                "Introduce the concept of force: a push or pull. Simple machines don't eliminate force — they redirect it or spread it over a longer distance.",
                "Design challenge: given a heavy object to lift, the child designs a solution using at least one simple machine",
            ],
            "socratic_questions": [
                "It's easier to roll a heavy box up a ramp than to lift it straight up. Why? Did the ramp make the box lighter?",
                "A bottle opener is a lever. Where is the fulcrum? Where do you push? Where does it lift the cap?",
                "You use a doorknob every day. If you removed the knob and just had the thin axle, could you turn it? Why is the knob important?",
                "The ancient Egyptians built pyramids using ramps, levers, and rollers. How could simple machines move blocks weighing tons?",
            ],
            "practice_activities": [
                "Simple machine scavenger hunt: find 3 examples of each simple machine in your house. Draw and label each one.",
                "Lever experiment: balance a ruler on a pencil (fulcrum). Place a coin on one end. How little force on the other end lifts the coin? Move the fulcrum and try again.",
                "Ramp experiment: set up a ramp with a board and books. Roll a toy car down at different ramp angles. Measure how far it travels. Steeper = farther.",
                "Build a pulley: thread string over a doorknob or curtain rod. Attach a small bucket. Use the pulley to lift objects. Compare lifting WITH the pulley vs WITHOUT.",
            ],
            "real_world_connections": [
                "Playgrounds are full of simple machines: the seesaw is a lever, the slide is an inclined plane, the merry-go-round is a wheel and axle",
                "Kitchen tools use simple machines: knife (wedge), can opener (lever + wheel), corkscrew (screw), rolling pin (wheel and axle)",
                "Construction equipment uses simple machines at larger scale: cranes use pulleys, bulldozer blades are wedges, access ramps are inclined planes",
                "Your body uses simple machines: your arm is a lever, your teeth are wedges, your spine is a series of joints acting as fulcrums",
            ],
            "common_misconceptions": [
                "Thinking simple machines 'reduce' the work — they don't reduce TOTAL work. They change HOW the work is done: less force over a longer distance, or different direction of force.",
                "Believing simple machines are old-fashioned — every modern complex machine is made of simple machines combined. A bicycle has wheels, axles, levers, and screws.",
                "Confusing the 6 simple machines with powered machines — simple machines have no motor or engine. They redirect human force.",
                "Thinking a screw is just for holding things together — a screw is an inclined plane wrapped around a cylinder. It converts rotational force into linear force.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Identifies all 6 simple machines by name",
                "Finds real-world examples of each in daily life",
                "Explains how at least one simple machine makes work easier",
            ],
            "proficiency_indicators": [
                "Identifies 4-5 simple machines",
                "Finds examples for most but not all",
            ],
            "developing_indicators": [
                "Identifies 1-3 simple machines",
                "Cannot explain how they make work easier",
            ],
            "assessment_methods": ["identification quiz", "scavenger hunt results", "experiment demonstration"],
            "sample_assessment_prompts": [
                "Name all 6 simple machines.",
                "Find 2 examples of simple machines in this room.",
                "Show me how a ramp makes it easier to move a heavy object.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which of these is a simple machine?",
                "expected_type": "multiple_choice",
                "options": ["A computer", "A lever", "A battery", "A light bulb"],
                "correct_answer": "A lever",
                "hints": [
                    "Simple machines are basic devices: lever, wheel and axle, pulley, inclined plane, wedge, screw. Which is on this list?"
                ],
                "explanation": "A lever is one of the 6 simple machines. Computers, batteries, and light bulbs are complex devices or components, not simple machines.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "True or false: A knife blade is a type of simple machine called a wedge.",
                "expected_type": "true_false",
                "correct_answer": "true",
                "hints": [
                    "A wedge is a triangular shape that splits things apart or pushes things aside. Look at a knife blade's shape."
                ],
                "explanation": "True. A knife blade is a wedge — a simple machine with a triangular shape that splits material apart. The sharp edge concentrates force into a thin line, making it easy to cut through food.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Find 3 simple machines in your house. For each one, name the type and explain how it makes work easier.",
                "expected_type": "text",
                "hints": [
                    "Look in the kitchen, at doors, in the garage, on bikes. Levers, wheels, screws, wedges, ramps, and pulleys are everywhere!"
                ],
                "explanation": "Examples: (1) Door handle = lever — it amplifies the small turning force of your hand into enough force to pull back the latch. (2) Wheelchair ramp = inclined plane — it lets you go UP without lifting straight up, trading distance for reduced force. (3) Jar lid = screw — turning the lid converts rotational force into the linear force that seals the jar.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Set up a ramp with a board and books. Roll a toy car down at a gentle slope, then make it steeper. What happens? Why?",
                "expected_type": "text",
                "hints": [
                    "Compare: the car's speed and the distance it travels after leaving the ramp. What changed when you made the ramp steeper?"
                ],
                "explanation": "The steeper ramp makes the car go faster and travel farther. A steeper ramp converts more gravitational potential energy into kinetic energy (speed). The gentle ramp provides less acceleration. This demonstrates how inclined planes trade slope angle for force — a gentle ramp requires less effort to push something up, but a steep ramp accelerates things coming down.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "The ancient Egyptians moved massive stone blocks using ramps, levers, and rollers. Explain how each of these simple machines helped them move blocks that weighed several tons.",
                "expected_type": "text",
                "hints": [
                    "Ramp: instead of lifting straight up, slide up a gentle slope. Lever: pry under the block to lift one edge. Rollers (wheel and axle): reduce friction so the block slides more easily."
                ],
                "explanation": "Ramps (inclined planes) let workers push blocks upward along a gentle slope instead of lifting them straight up — trading distance for reduced force. Levers (long poles placed under the block edge) multiplied the workers' force to lift block edges. Rollers (logs placed under the block) reduced friction, making it easier to slide the block along the ground. Together, these simple machines made it possible for human labor to move stones weighing 2-70 tons — no modern machinery needed!",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Name all 6 simple machines and give one example of each.",
                "type": "open_response",
                "target_concept": "simple_machine_id",
                "rubric": "Mastery: all 6 named with examples. Proficient: 4-5. Developing: 1-3.",
            },
            {
                "prompt": "Demonstrate with a ramp and lever how simple machines make work easier.",
                "type": "open_response",
                "target_concept": "simple_machine_demo",
                "rubric": "Mastery: demonstrates AND explains force reduction. Proficient: demonstrates. Developing: cannot demonstrate.",
            },
        ],
        "resource_guidance": {
            "required": [
                "ruler and pencil for lever",
                "board and books for ramp",
                "household items for scavenger hunt",
            ],
            "recommended": [
                "simple pulley setup",
                "collection of simple machine examples (bottle opener, jar, screws)",
            ],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 20, "assessment": 10},
        "accommodations": {
            "dyslexia": "Simple machine identification is hands-on and visual. Scavenger hunts require no reading. Draw and label machines rather than writing descriptions. Oral explanations.",
            "adhd": "Scavenger hunts involve movement. Building levers and ramps is hands-on. Each machine can be a separate 10-minute session. The playground is a simple machines lab — combine with outdoor time.",
            "gifted": "Research compound machines (combinations of simple machines). Calculate mechanical advantage. Design and build a Rube Goldberg machine using multiple simple machines in sequence.",
            "visual_learner": "Diagrams of each simple machine. Photographs of real-world examples. Drawing and labeling machines found during scavenger hunt.",
            "kinesthetic_learner": "Build every machine. Test lever positions. Roll objects down ramps. Pull with pulleys. Cut with wedges. Turn screws.",
            "auditory_learner": "Discuss how each machine works. Chant the 6 machine names. Verbal scavenger hunt: name machines as you walk through the house.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Simple machines are the basic devices that make work easier. There are six: the lever, the wheel and axle, the pulley, the inclined plane, the wedge, and the screw. A machine does not make work disappear; it changes the force you need, making it smaller or pointing it in a more useful direction. Today we name all six, find them everywhere in daily life, and show with a hands-on experiment how one of them reduces effort.",
                "gradual_release": {
                    "i_do": "Name the six simple machines and hold up a household example of each: a bottle opener is a lever, a doorknob a wheel and axle, a jar lid a screw. Lift a heavy book straight up, then roll it up a ramp, and think aloud: the ramp did not make the book lighter, it let me use less force over a longer distance.",
                    "we_do": "Go through the six machines together, finding examples of each around the house, and set up a ramp or a lever to feel how it reduces the effort needed.",
                    "you_do": "Child names all six simple machines, finds real examples of each, explains that a simple machine makes work easier, and demonstrates one reducing effort.",
                },
                "guided_practice": [
                    "Name the six simple machines and a household example of each",
                    "Go on a scavenger hunt and find simple machines around the home",
                    "Set up a ramp or a lever and feel how it makes lifting easier",
                ],
                "independent_practice": [
                    "Build a lever or a ramp and test how it changes the force needed",
                    "Find and label three examples of each simple machine in the home",
                ],
                "mastery_check": [
                    "Identify all six simple machines by name",
                    "Find real-world examples of each simple machine",
                    "Explain that simple machines make work easier by changing the force needed, and demonstrate one",
                ],
                "spiral_review": [
                    "Revisit the idea of a force as a push or a pull, which simple machines redirect and reduce",
                ],
            },
            "classical": {
                "narrative_introduction": "Long ago people learned that a clever device could do what bare strength could not. From this learning came the six simple machines, the lever, the wheel and axle, the pulley, the inclined plane, the wedge, and the screw. They are the alphabet of all mechanism: every complex machine, however grand, is built of these six. To know them is to understand how human ingenuity has multiplied human strength.",
                "memory_work": {
                    "chants": [
                        "Chant the six simple machines: lever, wheel and axle, pulley, inclined plane, wedge, and screw",
                        "Chant the law of the machine: it does not lessen the work, but changes the force, in size or in direction",
                    ],
                    "recitations": [
                        "Recite that a simple machine makes work easier by changing the amount or the direction of the force, and that the six are the parts of every machine",
                    ],
                },
                "copywork": [
                    "Copy the names of the six simple machines, each with a few words of what it does, and the words force, fulcrum, effort, and load",
                ],
                "recitation_routine": "Begin each lesson by reciting the six simple machines and the law of the machine before any new study.",
                "history_integration": "Tell that the ancient Egyptians raised their pyramids with ramps and levers and rollers, that Archimedes of old declared he could move the Earth itself given a lever and a place to stand, and that the simple machines are the beginning of all the history of technology.",
                "read_aloud_suggestions": [
                    "An account of how the great builders of antiquity moved mountains of stone with ramp and lever, read aloud so the child hears the simple machines at work in history",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A beautifully illustrated living book about machines, building, or the great works of engineering, with true artwork and never a dry textbook",
                ],
                "short_lesson_flow": "Let the lesson be discovery, not instruction. Walk through the house, the kitchen, the garage, the playground, and find the simple machines hiding in plain sight: the door handle, the scissors, the seesaw, the ramp. Name each one gladly as it is found, and the child draws a favorite in the science notebook. Stop while the hunt is still a delight.",
                "narration_prompt": "Tell me about the simple machines you found today. Which one surprised you most, and how does it make work easier?",
                "real_world_objects": [
                    "The household itself, full of levers, wheels, screws, wedges, ramps, and pulleys",
                    "A bottle opener, a jar, a doorknob, real machines to handle",
                    "A board and books for a ramp, a ruler and pencil for a lever",
                    "A science notebook for drawing the machines found",
                ],
                "nature_connection": "Notice the simple machines in the child's own body and in nature: the arm is a lever with the elbow as its fulcrum, the front teeth are wedges, and a bird's beak, too, is a clever natural tool.",
                "habit_focus": "The habit of attention: looking at an ordinary object closely enough to see the simple machine within it.",
            },
            "montessori": {
                "prepared_materials": [
                    "Simple machine experiment trays: a lever tray, a ramp tray, a pulley tray",
                    "Real examples of each of the six simple machines for handling",
                    "Nomenclature cards matching each machine to its real-world examples",
                    "A board, books, weights, string, and a ruler for building and testing",
                ],
                "presentation": {
                    "three_period_lesson": "With the machine examples: this is a lever, the bottle opener; show me a lever; which simple machine is this?",
                    "steps": [
                        "The child handles each of the six simple machines and learns its name",
                        "The child works a tray, building a lever or a ramp and feeling how it reduces the effort",
                        "The child matches the nomenclature cards, machine to name to real-world example",
                    ],
                },
                "control_of_error": "The machine itself is the control: the child feels directly that pushing up a ramp takes less effort than lifting straight up, and a nomenclature card mismatched to a machine does not fit its example, so the work checks itself.",
                "abstraction_pathway": "From handling and building the real machines and feeling the effort change, to matching them to the nomenclature cards, toward recognizing the six simple machines within every complex machine.",
                "extensions": [
                    "Find the simple machines hidden inside a complex machine, a bicycle or a pair of scissors",
                    "Measure how a lever or pulley changes the force needed",
                    "Build a chain of machines that work together",
                ],
                "observation_focus": "Watch for the child feeling the change in effort for themselves, and recognizing a simple machine by what it does rather than by its appearance.",
            },
            "unschooling": {
                "invitations": [
                    "Keep real tools and gadgets that are simple machines within reach to handle and use",
                    "Leave out boards, ramps, string, and pulleys for free building",
                    "Have books about machines, building, and how things work available",
                ],
                "real_world_contexts": [
                    "Using simple machines in daily life: opening jars, turning doorknobs, riding a bike, cutting with scissors",
                    "Playing on the playground: the seesaw, the slide, the merry-go-round",
                    "Helping with real work that uses ramps, levers, and wheels",
                    "Taking apart or fixing things and finding the simple machines inside",
                ],
                "conversation_starters": [
                    "It is easier to roll the box up a ramp than to lift it, why do you think that is?",
                    "Where is the fulcrum on this bottle opener? Where do you push?",
                    "How many simple machines can you find on your bicycle?",
                ],
                "resource_bank": [
                    "Real tools and gadgets that are simple machines",
                    "Boards, ramps, string, and pulleys for building",
                    "Books about machines and how things work, and a nearby playground",
                ],
                "parent_role": "Bring the child into real work and play that uses simple machines, and wonder aloud at how a ramp, a lever, or a wheel makes a hard job easy. Welcome the child's building and tinkering, and let real machines, used and taken apart, rather than a worksheet, teach how they work.",
                "observation_documentation": "Over time, note whether the child recognizes the six simple machines, finds them in daily life, and understands that a machine makes work easier by changing the force. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Simple machine vocabulary: lever, fulcrum, inclined plane, pulley, wedge, screw, force, effort, load. Technical reading skills.",
            "math": "Force, distance, and mechanical advantage involve multiplication and division. Measuring ramp angles and distances. Counting machines found.",
            "history": "Every ancient civilization used simple machines: Egyptian ramps and levers, Roman pulleys, Greek screws (Archimedes' screw for water). Technology history begins with simple machines.",
        },
    },
    "sf-14": {
        "enriched": True,
        "learning_objectives": [
            "Describe the steps of the scientific method: observe, ask a question, predict, test, and describe results",
            "Ask a testable question based on a real observation",
            "Make a prediction (hypothesis) before conducting an experiment",
            "Record experimental results accurately and compare them to the prediction",
        ],
        "teaching_guidance": {
            "introduction": "The scientific method is not a rigid checklist — it is a way of THINKING. It starts with curiosity: you notice something and wonder WHY. Then you make a guess (prediction) about the answer. Then you TEST your guess with an experiment. Then you look at what actually happened and compare it to what you predicted. Was your guess right? Wrong? Partially right? Every answer leads to more questions. At the foundational level, the child learns this pattern by doing simple experiments: 'Which ball bounces highest? I predict the tennis ball. Let's test it. The rubber ball actually bounced highest! My prediction was wrong — and that's okay, because now I know something new.'",
            "scaffolding_sequence": [
                "Start with observation: 'Look at these three balls. What do you notice? What do you WONDER about them?'",
                "Model asking a testable question: 'I wonder which ball bounces the highest. That's something we can TEST.'",
                "Make a prediction: 'Before we test, what do YOU think will happen? Which ball do you predict will bounce highest? Why?'",
                "Test: drop each ball from the same height. Observe and record which bounces highest.",
                "Describe results: 'The rubber ball bounced highest. The tennis ball was second. The basketball was last.'",
                "Compare to prediction: 'Were you right? If not, what surprised you? What did you learn?'",
                "Repeat with a new question: 'What else could we test? Does the drop height change the result? Let's find out!'",
                "The child designs their OWN experiment: choose a question, predict, test 3 times, record, and conclude",
            ],
            "socratic_questions": [
                "You said 'I wonder if plants grow better with music.' Is that something we could test? How would we set up the experiment?",
                "Your prediction was wrong — the heavy ball didn't fall faster. How does it feel to have a wrong prediction? Is a wrong prediction a failure?",
                "We tested this once. Should we test it again? Why might ONE test not be enough?",
                "You said the blue car went faster. But did you drop both cars from the SAME height? Why does that matter?",
            ],
            "practice_activities": [
                "Ball bounce experiment: drop 3 different balls from the same height. Predict which bounces highest. Test 3 times. Record results. Was your prediction right?",
                "Sink or float: collect 10 objects. Predict: will each sink or float? Test in a bowl of water. Record results in a chart. How accurate were your predictions?",
                "Paper airplane experiment: fold 3 different airplane designs. Predict which flies farthest. Test each 3 times. Measure distances. Which design won?",
                "Design your own: the child chooses a question, makes a prediction, designs a fair test, conducts the experiment, records results, and presents findings to the family",
            ],
            "real_world_connections": [
                "Cooking is applied scientific method: you follow a recipe (procedure), observe what happens (did it rise?), and adjust next time (more flour next time)",
                "Doctors use the scientific method: observe symptoms, hypothesize the cause, test (run diagnostics), treat based on results",
                "Weather forecasters observe patterns, predict tomorrow's weather, and check their predictions against what actually happens",
                "Every invention started with a question, a prediction, and lots of testing: Edison tested thousands of materials for the light bulb filament",
            ],
            "common_misconceptions": [
                "Thinking a wrong prediction means you failed — a wrong prediction is a DISCOVERY. You learned something you didn't know before. All scientists get predictions wrong regularly.",
                "Believing you should only test once — real scientists test multiple times to make sure results are consistent, not just a fluke",
                "Thinking the scientific method is a strict, rigid sequence — in practice, scientists often jump between steps, revisit earlier steps, or start over with new questions",
                "Assuming science requires expensive equipment — the best science at this level uses household items: balls, water, paper, ramps, flashlights",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Names the steps of the scientific method in order",
                "Asks testable questions and makes predictions before experiments",
                "Records results accurately and compares to predictions",
            ],
            "proficiency_indicators": [
                "Knows the steps but may skip prediction or recording",
                "Conducts experiments but doesn't always compare results to predictions",
            ],
            "developing_indicators": [
                "Cannot articulate the steps of the scientific method",
                "Tests things randomly without making predictions first",
            ],
            "assessment_methods": ["experiment walk-through", "question formulation", "result recording review"],
            "sample_assessment_prompts": [
                "What are the steps of the scientific method? Walk me through them.",
                "Here are 3 different paper towel brands. Ask a question, make a prediction, and design a test.",
                "Show me your experiment results. Was your prediction right? What did you learn?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Put the scientific method steps in order: Test, Observe, Predict, Ask a Question, Describe Results.",
                "expected_type": "text",
                "correct_answer": "Observe, Ask a Question, Predict, Test, Describe Results",
                "hints": [
                    "Start with noticing something. Then wonder about it. Then guess. Then try. Then tell what happened."
                ],
                "explanation": "Correct order: (1) Observe — notice something interesting. (2) Ask a question — 'I wonder why...' (3) Predict — 'I think... because...' (4) Test — try it out. (5) Describe results — what actually happened? Compare to prediction.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "True or false: If your prediction is wrong, your experiment was a failure.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["What did you LEARN when your prediction was wrong? Is learning a failure?"],
                "explanation": "False! A wrong prediction is a DISCOVERY. You learned something you didn't expect. Many of the greatest scientific discoveries happened when predictions were wrong. The experiment is only a failure if you don't learn from it.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Pick a question you can test at home. Write your question, your prediction, how you would test it, and what you would look for.",
                "expected_type": "text",
                "hints": [
                    "Example questions: Which paper towel brand absorbs the most water? Does hot water freeze faster than cold? Which type of soil do plants grow best in?"
                ],
                "explanation": "A good experiment plan includes: (1) A specific, testable question. (2) A clear prediction with reasoning. (3) A fair test (change only ONE thing, keep everything else the same). (4) What you will observe or measure. Example: Question: 'Which brand of paper towel absorbs the most water?' Prediction: 'I think Brand A because it's thicker.' Test: 'Pour the same amount of water on each. See which absorbs most.' Measure: 'Count how many drops each absorbs.'",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You want to test whether plants grow better with or without music. How would you make this a FAIR test?",
                "expected_type": "text",
                "hints": ["A fair test changes only ONE thing (the variable). Everything else must stay the SAME."],
                "explanation": "Fair test: Plant two identical seeds in identical pots with the same soil, same water, same sunlight, same temperature. Play music for one plant and keep the other in silence. The ONLY difference is music. If one grows better, you know it's because of the music, not some other factor. This is called controlling variables.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Conduct a complete mini-experiment: (1) Pick a question. (2) Write your prediction. (3) Test it 3 times. (4) Record what happened. (5) Was your prediction right? What did you learn?",
                "expected_type": "text",
                "hints": [
                    "Choose something simple you can test right now: which object falls fastest? Which paper airplane design flies farthest? Does ice melt faster in the sun or shade?"
                ],
                "explanation": "A complete experiment report includes all 5 steps. Example: Question: 'Does ice melt faster in sunlight or shade?' Prediction: 'I think sunlight because it's warmer.' Test: 'Put identical ice cubes in sun and shade. Check every 5 minutes.' Results: 'Sun cube melted in 20 minutes. Shade cube took 45 minutes.' Conclusion: 'My prediction was right — sunlight melts ice faster because it provides heat energy.' Testing 3 times and recording data are the hallmarks of careful science.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Walk me through the scientific method using an experiment you've done.",
                "type": "open_response",
                "target_concept": "scientific_method",
                "rubric": "Mastery: names all steps and connects to a real experiment. Proficient: names most steps. Developing: cannot describe the process.",
            },
            {
                "prompt": "Design an experiment to answer this question: 'Which type of ball bounces highest?'",
                "type": "open_response",
                "target_concept": "experiment_design",
                "rubric": "Mastery: includes question, prediction, fair test, measurement plan. Proficient: includes 3 of 4. Developing: no clear plan.",
            },
        ],
        "resource_guidance": {
            "required": ["household items for experiments (balls, paper, water)", "science notebook for recording"],
            "recommended": ["measuring tape or ruler", "timer or clock for timed experiments"],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 20, "assessment": 15},
        "accommodations": {
            "dyslexia": "Experiments are hands-on — no reading required. Record results with drawings, check marks, and numbers rather than sentences. Oral descriptions of predictions and results. Parent scribes the experiment report if needed.",
            "adhd": "Experiments produce immediate, visible results — inherently engaging. Each experiment is self-contained (15-20 minutes). The prediction step adds exciting suspense: 'Was I right?' Physical experiments channel energy.",
            "gifted": "Introduce formal hypothesis writing ('If... then... because...'). Discuss variables and controls. Design multi-step experiments. Keep a long-term experiment journal. Research famous experiments and what they discovered.",
            "visual_learner": "Experiment charts and diagrams. Before/after photographs. Visual recording of results.",
            "kinesthetic_learner": "The entire scientific method is hands-on at this level. Build, test, measure, compare. Physical experiments are the core activity.",
            "auditory_learner": "Discuss predictions and results as conversations. 'What do you think will happen? Why?' Verbal experiment reports.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "The scientific method is the orderly way of answering a question about the world. It runs through steps: observe something, ask a question you can test, predict what you think will happen, test it with an experiment, and describe the results. Then compare the results to the prediction. A wrong prediction is not a failure; it is something learned. Today we learn the steps, ask a testable question, make a prediction, and record and compare our results.",
                "gradual_release": {
                    "i_do": "Take three balls and think aloud through the method: I observe them, I ask which bounces highest, I predict the tennis ball and say why, I test by dropping each from the same height, and I describe what happened. Show that comparing the result to the prediction, even when the prediction was wrong, is where the learning is.",
                    "we_do": "Work through a simple experiment together, naming each step as we reach it: observe, question, predict, test, and describe the results, then compare them to the prediction.",
                    "you_do": "Child names the steps of the scientific method, asks a testable question, makes a prediction, conducts the test, and records and compares the results.",
                },
                "guided_practice": [
                    "Name the steps of the scientific method in order",
                    "Turn a real observation into a testable question and a prediction",
                    "Conduct a simple experiment and record the results in the science notebook",
                ],
                "independent_practice": [
                    "Design and carry out a complete mini-experiment, testing it more than once",
                    "Plan a fair test: change only one thing and keep the rest the same",
                ],
                "mastery_check": [
                    "Describe the steps of the scientific method: observe, question, predict, test, describe results",
                    "Ask a testable question and make a prediction before an experiment",
                    "Record results accurately and compare them to the prediction",
                ],
                "spiral_review": [
                    "Revisit careful observation, the first step on which every later step of the method depends",
                ],
            },
            "classical": {
                "narrative_introduction": "How does anyone come to know a thing for certain about the world? Not by guessing and not merely by being told, but by a disciplined way of reasoning: to observe carefully, to ask a clear question, to form a supposition, to put that supposition to the test of experiment, and to judge it honestly by what truly happens. This is the scientific method, the great instrument by which knowledge of nature is won.",
                "memory_work": {
                    "chants": [
                        "Chant the steps of the method: observe, question, predict, test, and describe the results",
                        "Chant the honest rule: a prediction proven wrong is not a failure but a thing discovered",
                    ],
                    "recitations": [
                        "Recite that a prediction is a supposition put to the test, and that the careful reasoner judges it by the evidence, not by hope",
                    ],
                },
                "copywork": [
                    "Copy the steps of the scientific method in order, and the form of a hypothesis: if this, then that, because",
                ],
                "recitation_routine": "Begin each lesson by reciting the steps of the scientific method in order before any new experiment is undertaken.",
                "history_integration": "Tell that the scientific method was forged over many centuries, that Aristotle observed, that Ibn al-Haytham of old insisted on experiment, that Galileo tested and Bacon set down the method in words, and that to follow these steps is to take up the great inheritance of natural philosophy.",
                "read_aloud_suggestions": [
                    "An account of a famous experiment and the question it answered, read aloud so the child hears the scientific method at work in history",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A living book that tells the story of a scientist's discovery, the wondering, the trying, the finding out, never a dry method textbook",
                ],
                "short_lesson_flow": "There is no method to memorize first. Begin with a real wondering, the child's own or one you share, and follow it: what do we notice, what do we want to know, what do we think, let us try and see. Do the simple experiment together, gladly, and let the child tell what happened. The method is learned by living it, not by reciting it.",
                "narration_prompt": "Tell me what we wondered and what we did to find out. What did you think would happen, and what really happened?",
                "real_world_objects": [
                    "Simple household things for real experiments: balls, water, paper, ramps",
                    "A science notebook for recording the wondering and the result",
                    "The whole world, full of things that prompt a genuine question",
                ],
                "nature_connection": "Out of doors the child's wonderings come thick and fast, why does the moss grow on one side, which seeds float, and each is a question to try, so that nature study itself becomes the practice of the method.",
                "habit_focus": "The habit of attention and of an honest mind: observing truly, supposing thoughtfully, and accepting gladly what the experiment shows.",
            },
            "montessori": {
                "prepared_materials": [
                    "Experiment trays the child sets up and works through independently: a sink-or-float tray, a ball-bounce tray, a ramp tray",
                    "A science journal for recording the question, the prediction, and the result",
                    "Prediction-and-result recording sheets",
                    "Simple, repeatable materials so a test may be run more than once",
                ],
                "presentation": {
                    "three_period_lesson": "With an experiment tray: this is the prediction, what we think will happen before we test; show me the prediction; which part of the experiment is this?",
                    "steps": [
                        "The child observes the materials on the tray and frames a question they can test",
                        "The child writes a prediction, then carries out the experiment, repeating it to be sure",
                        "The child records the result and compares it honestly to the prediction",
                    ],
                },
                "control_of_error": "The experiment is the control: the result is what it is, plain for the child to see, and it confirms or corrects the prediction with no need of an adult's word.",
                "abstraction_pathway": "From working a prepared experiment tray with the question and prediction supplied, to framing one's own question and prediction, toward conducting independent inquiry and judging it by the evidence.",
                "extensions": [
                    "Design an original experiment and carry it through",
                    "Plan a fair test, changing only one thing at a time",
                    "Keep an ongoing journal of questions, predictions, and results",
                ],
                "observation_focus": "Watch for the child predicting before testing, repeating a test rather than trusting one result, and accepting the evidence even when it surprises them.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a rich supply of stuff to tinker with, things to drop, float, mix, build, and take apart",
                    "Leave out a notebook and let the child record their wonderings and findings however they wish",
                    "Let questions and experiments arise freely, with no fixed time or procedure",
                ],
                "real_world_contexts": [
                    "The child's own constant experiments: what happens if I mix these, drop this, build it taller",
                    "Cooking, where a guess is made, tried, and tasted, and changed next time",
                    "Tinkering and building, testing what works and what does not",
                    "Wondering aloud at everyday puzzles and trying things to find out",
                ],
                "conversation_starters": [
                    "That is a good question, what do you think the answer is? How could we find out?",
                    "Before we try it, what do you think will happen? Why?",
                    "You changed two things at once, how will we know which one made the difference?",
                ],
                "resource_bank": [
                    "Open-ended materials for tinkering and experimenting",
                    "A notebook, kept available, for recording wonderings and discoveries",
                    "Books about scientists, inventions, and curious questions",
                ],
                "parent_role": "Treat the child as the natural scientist they already are: welcome their endless what-if questions, and rather than teaching steps, wonder alongside them, ask what they predict before they try, and help them notice when a test was muddled. Let real curiosity and real tinkering, never a worksheet, be where the method is lived.",
                "observation_documentation": "Over time, note whether the child asks questions they can test, makes a guess before trying, observes honestly what happens, and learns gladly from a surprise. This lived noticing of a curious mind at work replaces any test.",
            },
        },
        "connections": {
            "reading": "Scientific method vocabulary: observe, hypothesis, predict, experiment, variable, control, conclusion, evidence",
            "math": "Measurement, counting, graphing results, comparing numbers, calculating averages — math is the language of experimental data",
            "history": "The scientific method developed over centuries: Aristotle observed, Ibn al-Haytham experimented, Galileo tested, Newton theorized. The history of science IS the history of this method.",
        },
    },
    "sf-15": {
        "enriched": True,
        "learning_objectives": [
            "Maintain a nature journal with weekly entries for at least 6 weeks",
            "Draw plants, animals, weather, and seasonal changes from direct observation with increasing detail",
            "Write observations alongside drawings using specific descriptive language",
            "Develop the habit of careful, sustained attention to the natural world",
        ],
        "teaching_guidance": {
            "introduction": "A nature journal is the most powerful science tool a homeschool family can use, and it costs almost nothing: a blank notebook and a pencil. The child goes outside, finds something interesting — a flower, a bird, a cloud, an insect — and draws it carefully while looking at the REAL thing (not from memory, not from a photo). Then they add written observations: date, weather, what they noticed, what they wondered. Over weeks and months, the journal becomes a record of the child's growing ability to observe, and a beautiful document of nature in their own backyard.",
            "scaffolding_sequence": [
                "First entry: go outside together. Find ONE thing to observe: a leaf, a flower, a rock. Sit down and draw it from life. Take your time.",
                "Add written labels: 'green leaf,' 'rough bark,' 'brown soil.' Just a few words at first.",
                "Add the date and weather to every entry: this is scientific record-keeping",
                "Progress to more detailed drawings: 'Can you draw the veins on this leaf? The spots on this beetle? The shape of that cloud?'",
                "Add written observations: 1-2 sentences. 'The petals are soft and pink. There are 5 of them arranged in a circle.'",
                "Visit the same spot weekly: draw the same tree or garden patch and notice how it changes over time (seasonal observation)",
                "Add questions and wonderings: 'I wonder why the leaves are turning yellow. I wonder where that bird goes in winter.'",
                "Review and celebrate: look through the whole journal. Notice how the drawings improved. Notice what changed in nature over the weeks.",
            ],
            "socratic_questions": [
                "You drew a flower. How many petals does it actually have? Can you count and add them accurately to your drawing?",
                "You drew this tree last month and today. What changed? Why do you think it changed?",
                "You noticed ants carrying food. Where are they taking it? What question does that make you wonder about?",
                "Look at your first journal entry and your most recent one. What is different about your drawings now?",
            ],
            "practice_activities": [
                "Weekly nature observation: visit the same outdoor spot every week. Draw what you see. Record date and weather. Notice changes over time.",
                "Close-up drawing: use a magnifying glass to observe something small (a flower center, bark texture, an insect). Draw what you see magnified.",
                "Weather page: each day, draw a small weather icon and write the temperature. At the end of the month, look for patterns.",
                "Wonder page: after each observation, write one question that the observation made you wonder about. No need to answer it — just wonder!",
            ],
            "real_world_connections": [
                "Professional naturalists and scientists keep field journals: Darwin, Audubon, Beatrix Potter, and Jane Goodall all kept detailed observation notebooks",
                "Nature journals are personal records of a place and time — the child is documenting their own backyard's ecology",
                "Artists use sketchbooks the same way: drawing from life builds observation skills that transfer to all art and science",
                "The journal becomes a reference: 'When did we first see robins this spring? Let me check my journal — March 15!'",
            ],
            "common_misconceptions": [
                "Thinking the drawings must be perfect — nature journal drawings are for OBSERVATION, not art competitions. Accuracy matters more than beauty.",
                "Believing they need to go somewhere special — the backyard, a window box, even a crack in the sidewalk with weeds growing provides observation material",
                "Rushing through entries — careful observation takes time. 15-20 minutes for one entry is appropriate. Quality over quantity.",
                "Drawing from memory or photos instead of from life — the point is DIRECT observation. Looking at the real thing while drawing trains the eye in ways photos cannot.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Maintains journal with weekly entries for 6+ weeks",
                "Drawings show increasing detail and accuracy over time",
                "Written observations use specific descriptive language",
            ],
            "proficiency_indicators": [
                "Maintains journal with some entries, not consistently weekly",
                "Drawings are recognizable but lack detail",
            ],
            "developing_indicators": [
                "Journal has few entries",
                "Drawings are from memory, not from life",
            ],
            "assessment_methods": [
                "journal review over time",
                "drawing detail comparison",
                "observation language quality",
            ],
            "sample_assessment_prompts": [
                "Show me your nature journal. What's your favorite entry?",
                "Compare your first drawing to your most recent. What improved?",
                "Go draw something you see right now. I'll watch your observation process.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Go outside and find something interesting to observe. Draw it in your science notebook from LIFE (looking at the real thing while you draw). Add the date and today's weather.",
                "expected_type": "text",
                "hints": [
                    "Find a plant, insect, rock, cloud, or anything natural. Sit near it. Look carefully. Draw what you SEE, not what you think it should look like."
                ],
                "explanation": "A good nature journal entry includes: a drawing from direct observation (not memory), the date, weather conditions, and at least a few labels or descriptive words. This is the core practice of nature journaling — it gets better with every entry.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Why should you draw from LIFE (looking at the real thing) instead of from memory?",
                "expected_type": "multiple_choice",
                "options": [
                    "Because memory drawings are always ugly",
                    "Because looking at the real thing helps you notice details you would miss from memory",
                    "Because your teacher said so",
                    "There's no difference",
                ],
                "correct_answer": "Because looking at the real thing helps you notice details you would miss from memory",
                "hints": [
                    "When you draw from life, you keep looking back at the object. Each time you look, you notice something new."
                ],
                "explanation": "Drawing from life forces you to OBSERVE carefully. Each time you look at the real object, you notice new details: the number of petals, the pattern of veins, the exact shape of a leaf. Memory fills in generalities; direct observation reveals specifics.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Look at your nature journal entries from the past few weeks. What has changed in nature since your first entry? Write 2 sentences about the changes you've observed.",
                "expected_type": "text",
                "hints": [
                    "Look at: plants (growing? blooming? losing leaves?), animals (new ones appearing? old ones gone?), weather (warmer? cooler? more rain?)."
                ],
                "explanation": "Tracking changes over time IS science. Example: 'When I started, the trees were bare. Now they have small green buds and a few flowers are blooming.' Seasonal observation builds long-term thinking and data collection skills.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: Nature journal drawings must be perfect and beautiful.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["Is a nature journal an art portfolio or a science record?"],
                "explanation": "False. Nature journal drawings are for ACCURACY and OBSERVATION, not art competitions. A rough but accurate drawing that captures the number of petals, the shape of the leaf, and the branching pattern is more valuable than a 'pretty' but inaccurate drawing. Detail and accuracy matter more than artistic beauty.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Visit a spot outdoors. Draw what you see AND write: (1) the date and weather, (2) what you observe using at least 3 senses, and (3) one question that your observation makes you wonder about.",
                "expected_type": "text",
                "hints": [
                    "Draw carefully from life. Write specific observations: 'The bark is rough and gray with green moss on the north side.' End with a genuine wonder: 'I wonder why the moss only grows on one side.'"
                ],
                "explanation": "A complete nature journal entry combines: visual record (drawing), data (date and weather), multi-sense observations (written), and scientific curiosity (a question). This entry shows the child IS a scientist: observing carefully, recording precisely, and asking questions about what they see.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Show me your nature journal. Let's look at how your observations have grown over time.",
                "type": "open_response",
                "target_concept": "journal_growth",
                "rubric": "Mastery: 6+ weeks of entries with growing detail and accuracy. Proficient: some entries with improvement. Developing: few entries, little growth.",
            },
            {
                "prompt": "Create a nature journal entry right now. Draw from life, add date/weather, write observations.",
                "type": "open_response",
                "target_concept": "observation_skills",
                "rubric": "Mastery: detailed drawing from life with date, weather, observations, and a question. Proficient: drawing with some labels. Developing: quick sketch without observation details.",
            },
        ],
        "resource_guidance": {
            "required": ["blank science notebook or journal", "pencils (regular and colored)"],
            "recommended": ["magnifying glass for close-up observation", "field guide for local plants and animals"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 20, "assessment": 10},
        "accommodations": {
            "dyslexia": "Nature journaling is primarily DRAWING — a visual-spatial strength for many dyslexic learners. Written observations can be dictated to a parent or kept to single-word labels. The drawing IS the observation record.",
            "adhd": "Outdoor journaling combines nature time with focused attention. Keep entries to 15 minutes. Allow the child to choose what to observe (autonomy increases engagement). Drawing is a calming, focusing activity for many children with ADHD.",
            "gifted": "Detailed scientific illustrations with measurements and labeled parts. Year-long observation projects (same tree, same garden, same bird feeder). Research what they observe using field guides. Begin nature photography alongside drawing.",
            "visual_learner": "Core strength area: observation and drawing. Detailed, colorful illustrations. Close-up views with magnifying glass.",
            "kinesthetic_learner": "The outdoor walk TO the observation spot is movement. Collecting specimens (leaves, seeds) to draw later. Building a nature collection alongside the journal.",
            "auditory_learner": "Describe what you see aloud before drawing. Discuss observations with a partner. Listen to birdsong and try to identify the species.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "A nature journal is a notebook in which the child draws and writes what they observe in the natural world. The drawing is made from life, looking at the real thing, not from memory. Beside the drawing go the date, the weather, and observations in specific words. Kept faithfully week by week, the journal records both the natural world and the child's growing power of careful attention. Today we begin and build this habit.",
                "gradual_release": {
                    "i_do": "Go outside, choose one thing, a leaf or a flower, sit down, and draw it slowly while looking at the real thing, thinking aloud: I keep looking back, and each time I see something new, a vein, a notch, a spot. Add the date, the weather, and a few exact describing words.",
                    "we_do": "Make a journal entry side by side: choose something to observe, draw it from life, add the date and weather, and write observations together, pressing for specific words.",
                    "you_do": "Child makes a nature journal entry, drawing from direct observation, recording the date and weather, and writing observations in specific descriptive language.",
                },
                "guided_practice": [
                    "Draw one natural object from life, looking closely at the real thing",
                    "Record the date and weather, and add specific describing words to the drawing",
                    "Visit the same outdoor spot and note what has changed since the last entry",
                ],
                "independent_practice": [
                    "Keep a weekly nature journal entry for several weeks running",
                    "Make a close-up entry, drawing something small observed through a magnifying glass",
                ],
                "mastery_check": [
                    "Maintain a nature journal with weekly entries for at least six weeks",
                    "Draw from direct observation with increasing detail and accuracy",
                    "Write observations in specific descriptive language alongside the drawings",
                ],
                "spiral_review": [
                    "Revisit multi-sense observation, the careful looking the journal records",
                ],
            },
            "classical": {
                "narrative_introduction": "The naturalists of old, before the camera, knew the world by drawing it. To set down a leaf or a bird truly on the page, the eye must look long and the hand must be honest. A nature journal is the discipline of that looking. Kept faithfully, it becomes both a record of the living world and a record of a mind being trained to attend.",
                "memory_work": {
                    "chants": [
                        "Chant what every entry must carry: the date, the weather, a drawing from life, and observations in true words",
                        "Chant the naturalist's rule: draw the thing before you, not the thing in your memory",
                    ],
                    "recitations": [
                        "Recite that careful observation drawn and described is the beginning of natural knowledge, and that the journal is kept faithfully, week upon week",
                    ],
                },
                "copywork": [
                    "Copy a sentence of fine naturalist's description into the journal, and a list of exact words for color, shape, and texture",
                ],
                "recitation_routine": "Begin each session by looking back over the past entries and recalling what was observed before, so the journal is reviewed as it grows.",
                "history_integration": "Tell that the great naturalists, Darwin aboard the Beagle, Audubon among the birds, kept just such journals, that their notebooks of drawings and observations were the seed of their discoveries, and that the child keeping a nature journal follows in their hand.",
                "read_aloud_suggestions": [
                    "A passage from a naturalist's own journal or writing, read aloud so the child hears how a careful observer sets down what they see",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A beautiful nature book or a naturalist's illustrated journal, with true artwork that shows the child what loving observation looks like",
                ],
                "short_lesson_flow": "Go out of doors unhurried and let the child choose what to attend to. They sit before the real thing, a flower, a beetle, a branch, and draw it from life, taking all the time it asks. The date, the weather, and a few true words are added. Week by week the journal fills. This is not an exercise but a way of meeting the world.",
                "narration_prompt": "Tell me about what you drew today. What did you notice that you would have missed if you had not looked so closely?",
                "real_world_objects": [
                    "A blank nature notebook and pencils, plain and colored",
                    "The whole out-of-doors, the journal's only subject",
                    "A magnifying glass for close looking",
                    "One spot returned to week after week, watched through the seasons",
                ],
                "nature_connection": "The nature notebook is the very heart of this lesson and of nature study itself: the child goes out, observes a living thing, and records it with love and care, building a personal record of their own corner of the natural world.",
                "habit_focus": "The habit of attention: the slow, faithful, loving looking at a real thing that nature journaling cultivates above all.",
            },
            "montessori": {
                "prepared_materials": [
                    "A nature journal kept as the child's own ongoing work",
                    "Pencils, colored pencils, and a magnifying glass on a prepared shelf",
                    "A field guide for naming what is observed",
                    "A basket for specimens, leaves and seeds, gathered to draw",
                ],
                "presentation": {
                    "three_period_lesson": "With a journal entry: this is an observation drawn from life, looking at the real thing; show me a drawing made from life; was this drawn from life or from memory?",
                    "steps": [
                        "The child goes outdoors with the journal and chooses, freely, what to observe",
                        "The child draws the chosen thing from life and adds the date, the weather, and observations",
                        "The child reviews the journal periodically, seeing their own observation grow more careful over time",
                    ],
                },
                "control_of_error": "The real object is the control: the child checks every drawn detail against the thing itself, and a field guide confirms a name, so the journal is corrected by nature, not by an adult.",
                "abstraction_pathway": "From drawing a single object from life with care, to recording detailed observations week upon week, toward the settled habit of careful, sustained attention to the natural world.",
                "extensions": [
                    "Keep a year-long study of one tree, one garden, or one bird feeder",
                    "Add measurements and labeled diagrams to the entries",
                    "Use the field guide to name and research what is observed",
                ],
                "observation_focus": "Watch for the child drawing from life rather than memory, recording specific detail, and choosing their own subjects with growing care.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a lovely blank notebook and good pencils where the child can reach them",
                    "Leave out a magnifying glass and field guides beside the door",
                    "Let drawing and noting the natural world be a free, welcome thing, never assigned",
                ],
                "real_world_contexts": [
                    "Drawing a flower, a bug, or a cloud simply because it caught the child's eye",
                    "Recording a treasure found on a walk: a feather, a shell, an interesting leaf",
                    "Noting the weather or the season's change because it is worth remembering",
                    "Keeping a record of a beloved place, a tree, a creek, a garden corner",
                ],
                "conversation_starters": [
                    "That is beautiful, would you like to draw it so we can remember it?",
                    "What do you notice about it when you look really closely?",
                    "How has our tree changed since you drew it last?",
                ],
                "resource_bank": [
                    "A blank notebook and good drawing materials, kept available",
                    "A magnifying glass and field guides for the curious",
                    "The out-of-doors itself, free and full of things worth drawing",
                ],
                "parent_role": "Keep a nature journal of your own and draw with the child for the pleasure of it, never as a task. Welcome whatever they choose to record, marvel at what they notice, and let the journal be the child's own loved keepsake of the natural world rather than an exercise.",
                "observation_documentation": "Over time, note whether the child draws from life with growing care, records what they observe in specific words, and is forming the habit of attending closely to the natural world. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Nature journal writing builds descriptive language: specific vocabulary for colors, shapes, textures, and behaviors observed in nature",
            "math": "Counting petals, measuring heights, recording temperatures, tracking data over time — nature journaling IS applied math",
            "history": "Famous scientists kept nature journals: Darwin's Beagle notebooks, Leonardo da Vinci's observation sketches, John Muir's Sierra journals. The child follows in their footsteps.",
        },
    },
    "sf-16": {
        "enriched": True,
        "learning_objectives": [
            "Sort 15 or more items into categories using observable characteristics",
            "Explain the reasoning behind chosen grouping criteria",
            "Understand that the same objects can be classified in different ways depending on the criteria chosen",
            "Recognize that classification is how scientists organize knowledge about the natural world",
        ],
        "teaching_guidance": {
            "introduction": "Classification is how scientists organize the overwhelming variety of the natural world into manageable groups. When a child sorts a pile of leaves by shape, they are doing what Carl Linnaeus did when he organized all living things into a system. Classification is a THINKING skill: you observe characteristics, choose criteria, and group accordingly. The same collection can be sorted different ways — leaves sorted by color give different groups than leaves sorted by shape. Both are valid. The key is being able to EXPLAIN your reasoning.",
            "scaffolding_sequence": [
                "Start with a familiar sorting task: sort a bag of mixed buttons by color. Now re-sort by size. Same buttons, different groups!",
                "Sort natural objects: collect 15 items from outdoors (leaves, rocks, seeds, sticks, shells). Sort by one characteristic (color).",
                "Re-sort by a different characteristic: sort the same collection by texture (rough vs smooth), then by size, then by type (plant vs mineral).",
                "Discuss: 'The groups changed when we changed the rule. Which way of sorting told us the most useful information?'",
                "Introduce scientific classification: 'Scientists sort ALL living things into groups: plants, animals, fungi. Within animals: mammals, birds, fish, reptiles, insects.'",
                "Practice multi-level classification: sort animals into vertebrates and invertebrates, then sort vertebrates into mammals, birds, fish, reptiles, amphibians",
                "Create a classification key: 'Does it have legs? Yes → Does it have wings? Yes → Bird. No → Mammal or reptile.'",
                "Apply to a real collection: the child classifies their rock collection, nature collection, or a set of pictures using self-chosen criteria",
            ],
            "socratic_questions": [
                "You sorted these leaves by color. Can you think of another way to sort the exact same leaves?",
                "Two people sorted the same collection differently. Who is right? Can BOTH be right?",
                "Why do scientists put animals into groups? What does classification help us DO?",
                "A whale lives in the ocean and looks like a fish. Why do scientists classify it as a mammal instead?",
            ],
            "practice_activities": [
                "Button sort challenge: sort a bag of buttons 3 different ways (color, size, number of holes). How many groups each time?",
                "Nature collection classification: collect 15+ natural objects and create at least 3 different classification systems for the same collection",
                "Animal sorting: given 20 animal pictures, sort into vertebrate/invertebrate, then into the 5 vertebrate groups",
                "Classification key creation: build a simple yes/no question tree that sorts 8 animals into correct groups",
            ],
            "real_world_connections": [
                "Libraries classify books using the Dewey Decimal System — every book has a category and a number. This is classification applied to knowledge.",
                "Grocery stores classify food: produce, dairy, meat, bakery, frozen. This classification helps shoppers find what they need.",
                "Recycling is classification: sort waste into paper, plastic, glass, and compost based on material properties",
                "Your clothes are classified in your dresser: socks in one drawer, shirts in another. Organization IS classification.",
            ],
            "common_misconceptions": [
                "Thinking there is only ONE right way to classify — the same objects can be validly classified in many ways depending on the criteria chosen",
                "Classifying by only one property (usually color or size) — scientists use MULTIPLE properties to classify accurately",
                "Thinking classification is just for scientists — everyone classifies daily: organizing rooms, sorting laundry, grouping groceries",
                "Believing animals that look similar must be in the same group — a whale looks like a fish but is a mammal. Classification is based on characteristics (warm-blooded, nursing young), not appearance alone.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Sorts 15+ items using 3 different classification criteria",
                "Explains reasoning for each grouping",
                "Understands that the same items can be classified differently",
            ],
            "proficiency_indicators": [
                "Sorts by 2 criteria with explanations",
                "Recognizes multiple classification possibilities when prompted",
            ],
            "developing_indicators": [
                "Sorts by 1 criterion only (usually color)",
                "Cannot explain sorting reasoning",
            ],
            "assessment_methods": ["multi-criteria sorting", "reasoning explanation", "classification key creation"],
            "sample_assessment_prompts": [
                "Sort these 15 items. Now sort them again a different way.",
                "Explain why you put those items in the same group.",
                "Can you think of a third way to sort this same collection?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "You have 10 leaves. Name two different ways you could sort them into groups.",
                "expected_type": "text",
                "hints": [
                    "Think about what you can OBSERVE: color, shape, size, texture, number of points, smooth vs jagged edges..."
                ],
                "explanation": "Two ways: (1) By color — green leaves in one group, brown in another, yellow in a third. (2) By shape — round leaves together, long narrow leaves together, lobed (oak-shaped) together. Same leaves, different groups, both valid!",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Why do scientists classify living things into groups?",
                "expected_type": "multiple_choice",
                "options": [
                    "Because they like making lists",
                    "To organize the millions of species into a system that helps us understand and study them",
                    "Because every animal needs a name",
                    "Classification is not important in science",
                ],
                "correct_answer": "To organize the millions of species into a system that helps us understand and study them",
                "hints": [
                    "There are millions of different living things. How would you study them all without a system?"
                ],
                "explanation": "Scientists classify to ORGANIZE knowledge. With millions of species, classification creates a system where related organisms are grouped together, making it possible to study, compare, and understand the natural world.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: A whale should be classified as a fish because it lives in the ocean and has fins.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": [
                    "Classification is based on body characteristics, not just where an animal lives. Is a whale warm-blooded? Does it nurse its young?"
                ],
                "explanation": "False. Despite living in water and having fins, a whale is a MAMMAL: it's warm-blooded, breathes air with lungs, gives live birth, and nurses its young with milk. Classification uses internal characteristics, not just appearance or habitat.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Collect 10 objects from your house. Sort them into groups using a rule YOU choose. Then re-sort them using a DIFFERENT rule. Describe both sorting systems.",
                "expected_type": "text",
                "hints": [
                    "First sort: maybe by material (wood, metal, plastic). Second sort: maybe by size (big, medium, small). Same objects, different groups!"
                ],
                "explanation": "Good answers show two distinct classification systems for the same objects and explain the criteria. Example: '10 kitchen items. Sort 1: by material — 3 metal, 4 plastic, 3 wood. Sort 2: by function — 5 for cooking, 3 for eating, 2 for storing.' The child demonstrates that classification depends on the criteria chosen.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Create a classification key for 6 animals: dog, eagle, goldfish, frog, snake, and butterfly. Write yes/no questions that sort them into the correct group.",
                "expected_type": "text",
                "hints": [
                    "Start with: 'Does it have a backbone?' Then: 'Does it have feathers? Fur? Scales? Wings?' Each question narrows the options."
                ],
                "explanation": "Example key: 'Has backbone? No → butterfly (invertebrate/insect). Yes → Has feathers? Yes → eagle (bird). No → Has fur? Yes → dog (mammal). No → Lives in water as adult? Yes → goldfish (fish). No → Has moist skin? Yes → frog (amphibian). No → snake (reptile).' This dichotomous key uses observable characteristics to classify step by step.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Sort this collection 3 different ways and explain each.",
                "type": "open_response",
                "target_concept": "multi_criteria_classification",
                "rubric": "Mastery: 3 distinct criteria with clear explanations. Proficient: 2 criteria. Developing: 1 criterion.",
            },
            {
                "prompt": "Create a classification key for 5 animals.",
                "type": "open_response",
                "target_concept": "classification_key",
                "rubric": "Mastery: working key that correctly sorts all 5. Proficient: key works for most. Developing: cannot create a systematic key.",
            },
        ],
        "resource_guidance": {
            "required": [
                "collection of natural objects or pictures for sorting",
                "paper for creating classification charts",
            ],
            "recommended": ["animal picture cards", "button collection for sorting practice"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Sorting physical objects is hands-on and visual. No reading required. Oral explanations of groupings. Picture cards instead of text labels.",
            "adhd": "Sorting races: who can sort fastest? Re-sorting the same collection adds variety. Nature collection sorting involves outdoor gathering. Each sorting activity is self-contained (10 minutes).",
            "gifted": "Introduce the full Linnaean classification system (kingdom, phylum, class, order, family, genus, species). Research how scientists classify newly discovered species. Explore dichotomous keys used by professional biologists.",
            "visual_learner": "Color-coded sorting mats. Classification charts with pictures. Visual dichotomous keys.",
            "kinesthetic_learner": "Sort physical objects by moving them into groups. Nature collecting walks. Handle specimens.",
            "auditory_learner": "Discuss sorting criteria before sorting. Explain groupings aloud. Debate classification choices.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Classification is sorting things into groups by their observable characteristics. The same collection can be classified in more than one way: leaves sorted by color make different groups than leaves sorted by shape, and both are correct. What matters is choosing a clear rule, a criterion, and being able to explain it. Today we sort fifteen or more items by various criteria, explain our reasoning, and learn that classification is how scientists organize knowledge of the natural world.",
                "gradual_release": {
                    "i_do": "Take a mixed collection and sort it by one characteristic, thinking aloud: my criterion is color. Then re-sort the very same collection by shape, and by size. Show that the groups change with the criterion, and that scientists sort all living things into groups in just this way.",
                    "we_do": "Sort a collection together by one criterion, name and explain the rule, then re-sort the same collection by a different criterion, and build a simple classification key.",
                    "you_do": "Child sorts fifteen or more items by several criteria, explains the reasoning behind each grouping, and recognizes that the same items can be classified in different ways.",
                },
                "guided_practice": [
                    "Sort a collection of fifteen or more items by an observable characteristic",
                    "Re-sort the same collection by a different criterion and explain both",
                    "Build a simple yes-or-no classification key",
                ],
                "independent_practice": [
                    "Classify a real collection three ways, recording the criterion and groups each time",
                    "Make a classification key that sorts a set of animals into their groups",
                ],
                "mastery_check": [
                    "Sort fifteen or more items into categories by observable characteristics",
                    "Explain the reasoning behind the chosen grouping criteria",
                    "Recognize that the same objects can be classified in different ways, and that classification organizes scientific knowledge",
                ],
                "spiral_review": [
                    "Revisit careful observation, since classification rests on the characteristics observed",
                ],
            },
            "classical": {
                "narrative_introduction": "The natural world holds a bewildering multitude of things, and the mind cannot hold a multitude. So it does what the ordered mind always does: it divides, it groups, it classifies. To classify is to find the kinds within the many, and it is the foundation of all systematic knowledge. The scholar who sorts wisely has begun to understand.",
                "memory_work": {
                    "chants": [
                        "Chant the classifier's question: by what characteristic shall these be grouped",
                        "Chant the great kingdoms of living things: the plants, the animals, the fungi, and the rest",
                    ],
                    "recitations": [
                        "Recite that one collection may be truly classified in many ways, each by its own criterion, and that classification is how knowledge is set in order",
                    ],
                },
                "copywork": [
                    "Copy the major groups of living things in order, and the words classify, criterion, characteristic, category",
                ],
                "recitation_routine": "Begin each lesson by reciting the classifier's question and the great groups of living things before any new sorting.",
                "history_integration": "Tell that Aristotle of old first set the animals into their kinds, that Linnaeus in later centuries built the great system of classification still used today, and that to classify is to join a labor of ordering the world that has gone on for thousands of years.",
                "read_aloud_suggestions": [
                    "An account of how Linnaeus, or another great classifier, brought order to the multitude of living things, read aloud so the child hears classification as a great work of the mind",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A beautifully illustrated living book about the variety of the natural world, animals or plants in their kinds, with true artwork and never a workbook",
                ],
                "short_lesson_flow": "Let the lesson grow out of a real collection, the leaves, stones, or shells the child has gathered on a walk. Spread them out and let the child group them however they see fit, then ask gently what the rule was. Wonder together whether they could be grouped another way. The child discovers classification by doing it with things they have loved enough to gather.",
                "narration_prompt": "Tell me how you grouped your collection, and what your rule was. Could the same things be grouped a different way?",
                "real_world_objects": [
                    "A real collection gathered on a nature walk: leaves, stones, shells, seeds",
                    "Sorting trays or small bowls to hold the groups",
                    "A nature notebook for recording the groupings",
                    "Living things observed out of doors, sorted into their kinds",
                ],
                "nature_connection": "Classification is met directly in nature study: the child notices that the trees, the birds, the flowers fall into kinds, and the sorting of a gathered collection is simply that noticing made deliberate.",
                "habit_focus": "The habit of attention and of order: looking closely enough to see how things are alike and unlike, and arranging them thoughtfully.",
            },
            "montessori": {
                "prepared_materials": [
                    "Sorting trays and baskets of natural objects to classify",
                    "Classification cards offering several sorting criteria",
                    "Animal picture cards for sorting into the vertebrate groups",
                    "Materials for building a classification key",
                ],
                "presentation": {
                    "three_period_lesson": "With a sorted collection: this group is sorted by texture; show me a group sorted by texture; by what criterion is this group sorted?",
                    "steps": [
                        "The child sorts a collection of fifteen or more objects by a single criterion",
                        "The child names and explains the criterion, then re-sorts the same collection a different way",
                        "The child builds a classification key, a chain of yes-or-no questions that sorts a set into its groups",
                    ],
                },
                "control_of_error": "The collection is the control: an object that does not share the group's chosen characteristic stands out plainly, and a classification key tested against the real objects reveals at once any question that does not sort them truly.",
                "abstraction_pathway": "From sorting concrete objects by one plain criterion, to classifying by several criteria and seeing the groups change, toward grasping classification as the system by which scientific knowledge is ordered.",
                "extensions": [
                    "Sort living things through the levels: vertebrate and invertebrate, then the vertebrate classes",
                    "Build a dichotomous key like a biologist's",
                    "Investigate how a surprising creature, the whale, is truly classified",
                ],
                "observation_focus": "Watch for the child holding to one criterion through a whole sort, explaining the rule, and seeing that the same collection can be classified in many true ways.",
            },
            "unschooling": {
                "invitations": [
                    "Keep the child's own collections, rocks, shells, cards, figures, where they can be sorted and re-sorted freely",
                    "Leave out trays, bowls, and bins that invite grouping",
                    "Have books and picture cards about animals and the kinds of living things available",
                ],
                "real_world_contexts": [
                    "Organizing a beloved collection in whatever way makes sense to the child",
                    "Sorting the household: the cutlery drawer, the recycling, the bookshelf, the toy bins",
                    "Noticing the kinds of things in the world: kinds of birds, kinds of trees, kinds of trucks",
                    "Finding how shops, libraries, and apps group things to make them findable",
                ],
                "conversation_starters": [
                    "How did you decide which things go together? What is your rule?",
                    "Could you group these a completely different way?",
                    "A whale lives in the sea and looks like a fish, but scientists call it a mammal, why might that be?",
                ],
                "resource_bank": [
                    "The child's own collections, kept where they can be sorted",
                    "Trays, bowls, and bins for grouping",
                    "Books and cards about the kinds of animals and living things",
                ],
                "parent_role": "Welcome the child's own ways of grouping their collections and their world, and ask about their reasoning with genuine curiosity rather than correcting it. Wonder aloud about other ways the same things could be sorted, and let real collections and the real ordering of daily life, rather than a worksheet, teach classification.",
                "observation_documentation": "Over time, note whether the child sorts things by observable characteristics, can explain the rule, sees that one collection may be grouped many ways, and understands that classification brings order. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Classification vocabulary: classify, category, criteria, characteristics, group, sort, organize, kingdom, species",
            "math": "Sorting and grouping are mathematical skills. Venn diagrams compare groups. Counting items per category. Creating data tables.",
            "history": "Linnaeus created the classification system in the 1700s. Ancient Greeks (Aristotle) also classified animals. Classification has a rich history.",
        },
    },
    "sf-17": {
        "enriched": True,
        "learning_objectives": [
            "Label the 3 body parts of an insect: head, thorax, and abdomen",
            "Describe complete metamorphosis (egg, larva, pupa, adult) using the butterfly as an example",
            "Explain at least 2 ways insects help ecosystems: pollination and decomposition",
            "Distinguish insects (6 legs, 3 body parts) from other small creatures like spiders (8 legs, 2 body parts)",
        ],
        "teaching_guidance": {
            "introduction": "Insects are the most successful group of animals on Earth — there are more species of insects than all other animal groups combined. Children are naturally fascinated (and sometimes afraid) of bugs, making insects a perfect study topic. The key facts: insects have 6 legs, 3 body parts (head, thorax, abdomen), and most have wings. Many go through metamorphosis — the incredible transformation from caterpillar to butterfly is one of the most dramatic events in nature, and families can watch it happen at home with a caterpillar kit or by finding a chrysalis outdoors.",
            "scaffolding_sequence": [
                "Go on a bug hunt: find and observe insects outdoors. How many legs? How many body sections? Use a magnifying glass.",
                "Introduce insect anatomy: head (eyes, antennae, mouth), thorax (legs and wings attach here), abdomen (digestion and reproduction). Label on a diagram.",
                "Distinguish insects from non-insects: a spider has 8 legs and 2 body parts — NOT an insect. A pill bug has 14 legs — NOT an insect. Insects have exactly 6 legs and 3 body parts.",
                "Study complete metamorphosis: egg → larva (caterpillar) → pupa (chrysalis) → adult (butterfly). Four completely different forms!",
                "Compare to incomplete metamorphosis: egg → nymph → adult (grasshopper). The nymph looks like a small adult.",
                "Discuss insect roles in ecosystems: pollination (bees carry pollen between flowers), decomposition (beetles break down dead material), food source (birds eat insects)",
                "Observe or raise caterpillars: watch metamorphosis happen in real time over 2-3 weeks",
                "Create an insect field guide page: the child draws an insect from life, labels its body parts, and writes 3 facts about it",
            ],
            "socratic_questions": [
                "You found a spider. It has 8 legs. Is it an insect? Why or why not?",
                "A caterpillar and a butterfly look COMPLETELY different. How can they be the same animal?",
                "What would happen to gardens if all the bees disappeared? Why are pollinators important?",
                "You said bugs are gross. But what would happen to the world if ALL insects disappeared? Would that be good or bad?",
            ],
            "practice_activities": [
                "Bug hunt with magnifying glass: find 5 insects outdoors. Count legs to confirm they are insects (6 legs). Draw each one in science notebook.",
                "Insect anatomy diagram: draw a large insect and label head, thorax, abdomen, legs (6), wings, antennae, and eyes.",
                "Metamorphosis sequence: draw or arrange 4 cards showing egg, caterpillar, chrysalis, and butterfly in correct order.",
                "Insect vs not-insect sorting: given pictures of insects, spiders, centipedes, and pill bugs, sort into 'insect' and 'not an insect' with reasoning.",
            ],
            "real_world_connections": [
                "Bees pollinate about one-third of the food we eat: apples, almonds, berries, squash. Without bees, our food supply would collapse.",
                "Butterflies in your garden started as caterpillars eating your plants — the same creature in two wildly different forms",
                "Fireflies use bioluminescence (living light) to attract mates — chemistry and biology combined in one insect",
                "Ants build complex colonies with queens, workers, and soldiers — insect societies that fascinate scientists",
            ],
            "common_misconceptions": [
                "Calling all small crawling things 'bugs' or 'insects' — spiders, centipedes, pill bugs, and worms are NOT insects. Insects specifically have 6 legs and 3 body parts.",
                "Thinking caterpillars and butterflies are different animals — they are the SAME animal at different life stages, connected by metamorphosis",
                "Believing all insects are harmful pests — most insects are beneficial: pollinating plants, decomposing dead material, and serving as food for birds and fish",
                "Thinking metamorphosis is like growing bigger — complete metamorphosis involves a total body restructuring inside the chrysalis. The caterpillar essentially dissolves and rebuilds as a butterfly.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Labels insect body parts correctly on a diagram",
                "Describes complete metamorphosis with all 4 stages",
                "Explains 2+ ways insects benefit ecosystems",
            ],
            "proficiency_indicators": [
                "Identifies insects by 6-leg rule",
                "Knows butterfly stages but may confuse the order",
            ],
            "developing_indicators": [
                "Cannot distinguish insects from spiders",
                "Does not know metamorphosis stages",
            ],
            "assessment_methods": ["diagram labeling", "metamorphosis sequencing", "insect vs non-insect sorting"],
            "sample_assessment_prompts": [
                "Label the 3 body parts of this insect diagram.",
                "Put these 4 metamorphosis stages in order: adult, egg, pupa, larva.",
                "Is a spider an insect? Why or why not?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "How many legs does an insect have?",
                "expected_type": "multiple_choice",
                "options": ["4", "6", "8", "10"],
                "correct_answer": "6",
                "hints": ["This number is the key identifier for insects. Spiders have 8, but insects have..."],
                "explanation": "All insects have exactly 6 legs. This is the quickest way to identify whether a creature is an insect. Spiders have 8 legs (arachnids), centipedes have many legs, but insects always have 6.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "True or false: A spider is an insect.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["Count the spider's legs. How many body parts does it have?"],
                "explanation": "False. A spider has 8 legs and 2 body parts — it is an arachnid, not an insect. Insects have 6 legs and 3 body parts (head, thorax, abdomen). Spiders and insects are BOTH arthropods, but they are different groups.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Put the butterfly metamorphosis stages in correct order: adult butterfly, chrysalis (pupa), caterpillar (larva), egg.",
                "expected_type": "text",
                "correct_answer": "egg, caterpillar (larva), chrysalis (pupa), adult butterfly",
                "hints": [
                    "Start with the smallest stage. What comes out of the egg? What does the caterpillar become?"
                ],
                "explanation": "Correct order: (1) Egg — laid on a plant. (2) Caterpillar (larva) — hatches and eats constantly. (3) Chrysalis (pupa) — caterpillar forms a protective case and transforms inside. (4) Adult butterfly — emerges and flies. This is complete metamorphosis: four totally different forms!",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Go outside with a magnifying glass. Find an insect. Draw it in your science notebook and label: head, thorax, abdomen, and legs. How many legs did you count?",
                "expected_type": "text",
                "hints": [
                    "Look under rocks, on plants, near flowers, or on the ground. Any creature with 6 legs and 3 body sections is an insect."
                ],
                "explanation": "A good entry includes a drawing from life with labeled body parts: head (with eyes and antennae), thorax (middle section where 6 legs and wings attach), and abdomen (largest back section). Counting exactly 6 legs confirms it is an insect.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Name 2 ways insects help the natural world. What would happen if all insects disappeared?",
                "expected_type": "text",
                "hints": ["Think about: bees and flowers, beetles and dead leaves, birds that eat insects for food."],
                "explanation": "Insects help through: (1) Pollination — bees, butterflies, and other insects carry pollen between flowers, enabling plants to reproduce. About 1/3 of human food depends on insect pollination. (2) Decomposition — beetles, ants, and fly larvae break down dead plants and animals, recycling nutrients into the soil. Without insects, dead material would pile up and plants would stop reproducing. Birds, fish, and other animals that eat insects would also starve. Insects are essential to life on Earth.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Label an insect diagram with all 3 body parts and other features.",
                "type": "open_response",
                "target_concept": "insect_anatomy",
                "rubric": "Mastery: all parts labeled correctly with additional features (antennae, wings). Proficient: 3 body parts labeled. Developing: cannot label correctly.",
            },
            {
                "prompt": "Describe the life cycle of a butterfly from egg to adult.",
                "type": "open_response",
                "target_concept": "metamorphosis",
                "rubric": "Mastery: all 4 stages in order with descriptions. Proficient: names stages. Developing: cannot sequence stages.",
            },
        ],
        "resource_guidance": {
            "required": ["magnifying glass for insect observation", "science notebook for drawings"],
            "recommended": ["butterfly raising kit or outdoor chrysalis observation", "insect field guide"],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 20, "assessment": 10},
        "accommodations": {
            "dyslexia": "Insect study is observational and visual. Drawing insects from life requires no reading. Label diagrams with single words. Oral descriptions of metamorphosis.",
            "adhd": "Bug hunts outdoors are exciting and active. Raising caterpillars provides daily 2-minute check-ins over weeks. Drawing insects with magnifying glass is focused and engaging.",
            "gifted": "Compare complete and incomplete metamorphosis in detail. Research social insects (ant colonies, bee hives). Study insect adaptations: camouflage, mimicry, bioluminescence. Begin an insect collection with proper identification.",
            "visual_learner": "Magnified insect observation. Detailed drawings. Metamorphosis diagrams and photographs.",
            "kinesthetic_learner": "Bug hunts with collection jars. Handling (safe) insects. Building insect models from clay.",
            "auditory_learner": "Discuss insect behaviors. Listen to insect sounds (crickets, cicadas). Narrate metamorphosis as a story.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Insects are the most numerous animals on Earth, and they are easy to tell from other small creatures by two sure marks: an insect has six legs and three body parts, a head, a thorax, and an abdomen. Many insects change form completely as they grow, in a process called metamorphosis. Today we label the insect's body parts, learn the butterfly's metamorphosis, learn how insects help ecosystems, and tell insects from spiders and other creatures.",
                "gradual_release": {
                    "i_do": "With a magnifying glass on a real insect or a clear picture, count aloud: six legs, three body parts, head, thorax, abdomen, so this is an insect. Set a spider beside it, eight legs, two body parts, not an insect. Lay out the four stages of the butterfly, egg, larva, pupa, adult, and name how insects pollinate and decompose.",
                    "we_do": "Examine insects together, labeling the body parts and counting the legs, sequence the metamorphosis stages, and sort small creatures into insects and not-insects.",
                    "you_do": "Child labels the insect's three body parts, describes complete metamorphosis, explains two ways insects help ecosystems, and distinguishes insects from spiders and other creatures.",
                },
                "guided_practice": [
                    "Label the head, thorax, and abdomen on an insect diagram and count the six legs",
                    "Put the four stages of butterfly metamorphosis in order",
                    "Sort small creatures into insects and not-insects by leg and body-part count",
                ],
                "independent_practice": [
                    "Go on a bug hunt and draw insects from life, labeling their body parts",
                    "Observe metamorphosis over weeks by raising caterpillars or watching a chrysalis",
                ],
                "mastery_check": [
                    "Label the three body parts of an insect: head, thorax, and abdomen",
                    "Describe complete metamorphosis using the butterfly's four stages",
                    "Explain two ways insects help ecosystems and tell an insect from a spider",
                ],
                "spiral_review": [
                    "Revisit the characteristics of living things, since insects show them all, growing, feeding, reproducing, responding",
                ],
            },
            "classical": {
                "narrative_introduction": "Of all the animals upon the Earth, the insects are the most numerous, more kinds than all the rest together. They are known by sure marks: six legs and a body in three parts. And many of them work a wonder as they grow, the complete remaking called metamorphosis, by which a crawling caterpillar becomes a winged butterfly. Small though they are, the insects hold the living world together.",
                "memory_work": {
                    "chants": [
                        "Chant the marks of an insect: six legs and three body parts, the head, the thorax, and the abdomen",
                        "Chant the four stages of metamorphosis: egg, larva, pupa, and adult",
                    ],
                    "recitations": [
                        "Recite that an insect has six legs and a spider eight, and that the insects serve the living world by pollination and by decomposition",
                    ],
                },
                "copywork": [
                    "Copy the three body parts of an insect and the four stages of metamorphosis, each in order and neatly set down",
                ],
                "recitation_routine": "Begin each lesson by reciting the marks of an insect and the stages of metamorphosis before any new study.",
                "history_integration": "Tell that the silkworm, an insect, spun the thread that built the great Silk Road of trade, that honey bees have been kept by people for thousands of years, and that swarms of locusts brought famine to whole nations, so that the small insect has shaped human history.",
                "read_aloud_suggestions": [
                    "A living account of the life of a bee, an ant colony, or a butterfly's metamorphosis, read aloud so the child hears the insect's story told",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A beautifully illustrated living book about the life of insects, written with knowledge and wonder, never a dry fact reader",
                ],
                "short_lesson_flow": "Go out on a bug hunt, unhurried, with a magnifying glass. Find a real insect and watch it quietly going about its life. Count its legs, see its three body parts, and the child draws it from life in the nature notebook. If a caterpillar can be raised at home, let the child witness the wonder of metamorphosis over the weeks. Let real creatures, watched, be the lesson.",
                "narration_prompt": "Tell me about the insect you watched. What was it doing, and how did you know it was an insect?",
                "real_world_objects": [
                    "A magnifying glass for close insect observation",
                    "Real insects met on a bug hunt outdoors",
                    "A caterpillar raised at home, or a chrysalis found and watched",
                    "A nature notebook for drawing insects from life",
                ],
                "nature_connection": "Insects are met everywhere in nature study, the bee on the flower, the beetle under the log, the ant on its errand, and the child comes to know them by patient watching out of doors, season after season.",
                "habit_focus": "The habit of attention: watching a small creature long enough and closely enough to see how it is made and how it lives.",
            },
            "montessori": {
                "prepared_materials": [
                    "A parts-of-an-insect puzzle with the body parts labeled",
                    "Metamorphosis sequence cards and butterfly life-cycle figures",
                    "Insect and other-creature nomenclature cards for sorting",
                    "A magnifying glass and real insect specimens for observation",
                ],
                "presentation": {
                    "three_period_lesson": "With the insect puzzle: this part is the thorax, where the legs attach; show me the thorax; which body part is this?",
                    "steps": [
                        "The child works the parts-of-an-insect puzzle, naming the head, thorax, and abdomen",
                        "The child arranges the metamorphosis sequence cards in order, egg, larva, pupa, adult",
                        "The child sorts creature cards into insects and not-insects, counting legs and body parts",
                    ],
                },
                "control_of_error": "The puzzle and the sequence cards carry their own control: each puzzle piece fits only its place, and the metamorphosis cards run true only in one order, while a real insect, with its countable six legs, settles whether a creature belongs.",
                "abstraction_pathway": "From handling the insect puzzle and the life-cycle figures, to sorting real and pictured creatures by their marks, toward knowing the insect by its definition and its place in the living world without the materials.",
                "extensions": [
                    "Compare complete metamorphosis with the incomplete metamorphosis of the grasshopper",
                    "Study the social insects, the ant colony and the bee hive",
                    "Investigate how insects pollinate and decompose, the work they do for the world",
                ],
                "observation_focus": "Watch for the child counting legs and body parts to identify an insect truly, and grasping that caterpillar and butterfly are one creature in two forms.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a magnifying glass and bug-viewing jars within easy reach",
                    "Leave out insect books, field guides, and a notebook for drawing",
                    "Have a butterfly-raising kit or a watched chrysalis available if the child is keen",
                ],
                "real_world_contexts": [
                    "Finding and watching insects in the yard, the garden, and the park",
                    "Watching bees at flowers and wondering at the work they do",
                    "Raising caterpillars and witnessing metamorphosis unfold",
                    "Noticing the insects, and the spiders, that share the home and the outdoors",
                ],
                "conversation_starters": [
                    "You found a spider, it has eight legs, do you think it is an insect?",
                    "The caterpillar and the butterfly look so different, how can they be the same animal?",
                    "What do you think would happen to the garden if there were no bees?",
                ],
                "resource_bank": [
                    "A magnifying glass, bug jars, and a notebook",
                    "Insect books and field guides",
                    "The yard and garden, full of insects to find and watch",
                ],
                "parent_role": "Follow the child's fascination with bugs wherever it leads, into the garden, into books, into raising a caterpillar, and wonder aloud at how insects are made and what they do for the world. Welcome every bug brought to you, and let real creatures, found and watched, rather than a worksheet, teach insect science.",
                "observation_documentation": "Over time, note whether the child tells an insect by its six legs and three body parts, knows the stages of metamorphosis, and understands how insects help the living world. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Insect vocabulary: metamorphosis, larva, pupa, chrysalis, thorax, abdomen, antenna, pollination, exoskeleton",
            "math": "Counting legs (6 for insects, 8 for spiders). Measuring wingspan. Timing metamorphosis stages in days.",
            "history": "Silkworms (insects) produced silk that drove the ancient Silk Road trade route. Honey bees have been kept by humans for thousands of years. Locusts caused famines throughout history.",
        },
    },
    "sf-18": {
        "enriched": True,
        "learning_objectives": [
            "Identify at least 5 local birds by sight or sound",
            "Explain how beak shape relates to diet: seed-cracking beaks, insect-probing beaks, fish-catching beaks",
            "Describe the bird life cycle from egg to adult, including nesting and fledging",
            "Understand key bird characteristics: feathers, hollow bones, warm-blooded, egg-laying",
        ],
        "teaching_guidance": {
            "introduction": "Birds are everywhere — in backyards, parks, forests, and cities — making them the most accessible wildlife for daily observation. A bird feeder outside a window becomes a living laboratory. The child learns to identify species, observe feeding behaviors, notice seasonal changes (migration, nesting), and discover the remarkable adaptations that make flight possible: feathers for lift and warmth, hollow bones for lightness, powerful chest muscles for wing power. Beak shape reveals diet: a cardinal's thick beak cracks seeds; a woodpecker's chisel beak drills into wood; a heron's long beak spears fish.",
            "scaffolding_sequence": [
                "Set up a bird feeder or birdbath visible from a window. Observe which birds visit and when.",
                "Learn to identify 5 common local birds by their appearance: color, size, shape, behavior",
                "Introduce bird characteristics: feathers, wings, hollow bones, warm-blooded, lay eggs. What makes a bird a BIRD?",
                "Study beak adaptations: show pictures of different beaks and match to diet (thick/seed, thin/insect, long/fish, hooked/meat)",
                "Observe nesting behavior if possible. Discuss the life cycle: nest building → egg laying → incubation → hatching → feeding → fledging",
                "Listen for bird songs: can you recognize any birds by their SOUND without seeing them?",
                "Discuss migration: why do some birds fly south? How do they know when and where to go?",
                "Bird field guide page: the child draws a bird from life, labels key features, and writes 3 observations about its behavior",
            ],
            "socratic_questions": [
                "This bird has a thick, strong beak. What do you think it eats? Why would it need a beak like that?",
                "Some birds fly south for winter. Why don't ALL birds migrate? What do the ones that stay do for food?",
                "You've been watching the feeder for a week. Which birds visit most often? What time of day?",
                "Feathers keep birds warm AND help them fly. How does one feature serve two purposes?",
            ],
            "practice_activities": [
                "Bird feeder observations: keep a daily log of which birds visit, how many, and what time. Look for patterns over a week.",
                "Beak matching game: match bird pictures to food pictures based on beak shape. Cardinal → seeds. Hummingbird → nectar. Eagle → meat.",
                "Bird drawing from life: sit quietly near a feeder or in a park. Draw a bird you observe. Label key features: beak, wings, tail, feet.",
                "Bird song identification: go outside, close your eyes, and listen. How many different bird songs can you hear? Try to match songs to the birds you know.",
            ],
            "real_world_connections": [
                "Bird feeders attract wildlife to your yard and provide daily science observation opportunities year-round",
                "Migration patterns track the seasons: when robins arrive in spring, spring has arrived. Birds are living calendars.",
                "Chickens are domesticated birds: eggs for breakfast connect to bird biology every morning",
                "Birdwatching (birding) is one of the most popular hobbies in the world: millions of people observe and identify birds",
            ],
            "common_misconceptions": [
                "Thinking all birds can fly — ostriches, penguins, emus, and kiwis are all flightless birds. They are still birds (feathers, eggs, warm-blooded).",
                "Believing birds 'teach' their babies to fly — fledglings are driven by instinct to jump and practice. Parents encourage but don't give flying lessons.",
                "Thinking touching a baby bird means the parents will abandon it — most birds have a poor sense of smell. If you find a baby bird, the parents will usually continue caring for it.",
                "Assuming all birds eat seeds — bird diets are enormously diverse: seeds, insects, fish, fruit, nectar, rodents, carrion. Beak shape is the clue to diet.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Identifies 5+ local birds by sight or sound",
                "Connects beak shape to diet with 3 examples",
                "Describes bird life cycle from egg to adult",
            ],
            "proficiency_indicators": [
                "Identifies 3-4 birds",
                "Knows beaks relate to diet but gives limited examples",
            ],
            "developing_indicators": [
                "Identifies 1-2 birds",
                "Cannot connect beak shape to diet",
            ],
            "assessment_methods": ["bird identification", "beak-diet matching", "life cycle description"],
            "sample_assessment_prompts": [
                "Name 5 birds you can identify. How do you recognize each one?",
                "This bird has a long, thin beak. What do you think it eats?",
                "Describe how a bird goes from egg to flying adult.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which of these is a characteristic that ALL birds share?",
                "expected_type": "multiple_choice",
                "options": [
                    "They can all fly",
                    "They all have feathers",
                    "They all eat seeds",
                    "They all live in trees",
                ],
                "correct_answer": "They all have feathers",
                "hints": [
                    "Not all birds fly (penguins, ostriches). Not all eat seeds. Not all live in trees. But one feature is universal..."
                ],
                "explanation": "ALL birds have feathers — it is the defining characteristic of birds. Not all birds fly (penguins, ostriches), not all eat seeds, and not all live in trees. But every bird, from hummingbird to ostrich, has feathers.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "A bird has a thick, strong, cone-shaped beak. What does it probably eat?",
                "expected_type": "multiple_choice",
                "options": ["Fish", "Nectar", "Seeds", "Mice"],
                "correct_answer": "Seeds",
                "hints": ["A thick, strong beak is good for CRACKING something hard. What food has a hard shell?"],
                "explanation": "A thick, cone-shaped beak is designed for cracking seeds. Cardinals, finches, and sparrows have this beak type. The strong beak can apply enough force to crack open tough seed shells.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Set up a bird observation station (near a window looking at a feeder or yard). Watch for 15 minutes. Record: how many birds you see, what species (if you know), and what they are doing.",
                "expected_type": "text",
                "hints": [
                    "Note: the species (or describe it: 'small brown bird with a red chest'), the number, and the behavior (eating, singing, hopping, flying, chasing)."
                ],
                "explanation": "A good observation record includes: date, time, weather, number of birds, species identification (or description), and behavior notes. Example: 'April 16, 9am, sunny. 3 cardinals eating seeds. 2 blue jays chasing each other. 1 robin pulling a worm from the lawn.' Over days and weeks, patterns emerge.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: If you touch a baby bird that fell from its nest, the parents will abandon it because of your smell.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["Most birds have a very poor sense of smell. Would they really detect a human scent?"],
                "explanation": "False. Most birds have a poor sense of smell and will NOT abandon a chick because of human scent. If you find a baby bird on the ground, you can gently place it back in the nest if reachable. If not, leave it nearby — the parents are probably watching and will continue feeding it.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Choose a bird you see regularly. Draw it from life in your science notebook. Label: beak shape, wing shape, tail shape, and feet. Based on its features, describe what it eats and where it lives.",
                "expected_type": "text",
                "hints": [
                    "Observe carefully before drawing. What beak shape? (thick=seeds, thin=insects, hooked=meat). What feet? (perching=songbird, webbed=swimmer, talons=predator)."
                ],
                "explanation": "A complete bird study includes: accurate drawing from observation, labeled body parts, and inferences about diet and habitat based on those features. Example: 'Robin: medium bird, orange breast, thin pointed beak (eats worms and insects), perching feet (lives in trees and on lawns), short rounded wings (doesn't migrate far).' The child connects form to function — anatomy reveals lifestyle.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Identify 5 birds you know. For each, describe one identifying feature.",
                "type": "open_response",
                "target_concept": "bird_identification",
                "rubric": "Mastery: 5 birds with specific features. Proficient: 3-4 birds. Developing: 1-2 birds.",
            },
            {
                "prompt": "Match 3 beak types to their diets.",
                "type": "open_response",
                "target_concept": "beak_adaptation",
                "rubric": "Mastery: 3 correct matches with reasoning. Proficient: 2 correct. Developing: cannot connect beak to diet.",
            },
        ],
        "resource_guidance": {
            "required": [
                "bird feeder or birdbath (even a plate of seeds works)",
                "science notebook for bird observations",
            ],
            "recommended": ["bird field guide for your region", "binoculars for distance observation"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Bird watching is visual and auditory — no reading required. Draw birds from life. Oral identification. Bird song recognition is an auditory strength activity.",
            "adhd": "Bird watching outdoors combines nature time with focused observation. The surprise of which bird appears next maintains engagement. Keep observation sessions to 15 minutes. Bird drawing focuses attention.",
            "gifted": "Learn bird songs and calls. Research migration routes and patterns. Study flight mechanics and aerodynamics. Keep a year-long bird log with seasonal patterns. Participate in citizen science bird counts.",
            "visual_learner": "Bird identification is visual. Detailed drawings from life. Photographs for comparison. Color-coded field notes.",
            "kinesthetic_learner": "Build and maintain a bird feeder. Walk outdoors for bird observation. Mimic bird movements and behaviors.",
            "auditory_learner": "Bird song identification is a natural strength. Listen to recorded bird songs and match to species. Early morning birding (dawn chorus) is the best listening time.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Birds are found nearly everywhere, which makes them the easiest wild animals to observe. Every bird shares four marks: feathers, hollow bones, warm blood, and eggs. A bird's beak reveals its diet, a thick beak for cracking seeds, a thin beak for probing insects, a long beak for catching fish. Today we identify local birds by sight and sound, connect beak shape to diet, describe the bird life cycle, and learn the characteristics of birds.",
                "gradual_release": {
                    "i_do": "Watch a bird at the feeder and think aloud: feathers, so it is a bird; a thick cone-shaped beak, so it eats seeds. Name a few local birds by their color, size, and behavior, and trace the life cycle: the nest, the eggs, the hatching, the parents feeding, the fledging.",
                    "we_do": "Watch birds together and identify the local ones, match beak shapes to diets, and describe the bird life cycle from egg to flying adult.",
                    "you_do": "Child identifies at least five local birds by sight or sound, explains how beak shape relates to diet, describes the bird life cycle, and names the characteristics of birds.",
                },
                "guided_practice": [
                    "Identify local birds by their color, size, shape, and behavior",
                    "Match beak shapes to the diets they suit: seeds, insects, fish, meat",
                    "Describe the bird life cycle: nesting, eggs, hatching, feeding, fledging",
                ],
                "independent_practice": [
                    "Keep a daily bird-feeder log of which birds visit and when",
                    "Draw a bird from life and label its beak, wings, tail, and feet",
                ],
                "mastery_check": [
                    "Identify at least five local birds by sight or sound",
                    "Explain how beak shape relates to diet with three examples",
                    "Describe the bird life cycle and name the key characteristics of birds",
                ],
                "spiral_review": [
                    "Revisit how an animal is adapted to its habitat, since the beak is an adaptation to a bird's food",
                ],
            },
            "classical": {
                "narrative_introduction": "Birds are the masters of the air, and they are known by one sure mark above all: feathers, which no other creature wears. Light hollow bones, warm blood, and eggs complete the kind. Look closely and a bird reveals its life in its very shape: the beak tells what it eats, the foot tells where it lives. To study birds is to read the fitness of a creature to its world.",
                "memory_work": {
                    "chants": [
                        "Chant the marks of a bird: feathers and hollow bones, warm blood and eggs",
                        "Chant the beaks and their food: thick for seeds, thin for insects, long for fish, hooked for meat",
                    ],
                    "recitations": [
                        "Recite that not every bird flies, the ostrich and the penguin do not, but every bird wears feathers, and that the beak is shaped to the food",
                    ],
                },
                "copywork": [
                    "Copy the four characteristics of birds, and the names of the local birds the child has come to know",
                ],
                "recitation_routine": "Begin each lesson by reciting the marks of a bird and the beaks and their foods before any new observation.",
                "history_integration": "Tell that people have always watched the birds, that sailors followed them to land and farmers read the seasons by their coming and going, and that the keeping of the domestic fowl has fed humankind for thousands of years.",
                "read_aloud_suggestions": [
                    "A living account of the life of a particular bird, its nesting, its feeding, its long migration, read aloud so the child hears the bird's story told",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A beautifully illustrated living book about birds, written by one who clearly loves and knows them, never a dry reader",
                ],
                "short_lesson_flow": "Set a feeder where it can be seen from a window, and let watching the birds become a quiet, glad habit. The child observes who comes and what they do, learns a few by name, and draws one from life in the nature notebook. Outdoors, the child listens for bird song. Over weeks the child becomes, simply, a birdwatcher.",
                "narration_prompt": "Tell me about the birds you watched today. Which ones came, what were they doing, and how did you know them?",
                "real_world_objects": [
                    "A bird feeder or birdbath set where it can be watched",
                    "Binoculars for watching birds at a distance",
                    "A nature notebook for drawing birds from life",
                    "A field guide for naming the local birds",
                ],
                "nature_connection": "Bird-watching is nature study at its finest: the child comes to know the birds of their own place by patient watching and listening, season upon season, and marks the year by their nesting and their migration.",
                "habit_focus": "The habit of attention: watching and listening patiently until a bird is truly known by its look, its song, and its ways.",
            },
            "montessori": {
                "prepared_materials": [
                    "A parts-of-a-bird puzzle with the features labeled",
                    "Bird identification cards with photographs of local species",
                    "Beak-and-diet matching cards",
                    "A bird feeder the child tends as a practical-life work, and binoculars",
                ],
                "presentation": {
                    "three_period_lesson": "With the bird cards: this beak is thick and strong, a seed-cracker; show me a seed-cracking beak; what does a bird with this beak eat?",
                    "steps": [
                        "The child tends the bird feeder and observes which birds come, identifying them with the cards",
                        "The child works the parts-of-a-bird puzzle and the beak-and-diet matching cards",
                        "The child draws a bird from life and records its features and behavior",
                    ],
                },
                "control_of_error": "The puzzle and the matching cards carry their own control, fitting and pairing in one true way, and the real birds at the feeder are the deeper control: the field guide and the living bird confirm or correct an identification.",
                "abstraction_pathway": "From handling the bird puzzle and matching beaks to foods, to identifying real birds at the feeder, toward reading a bird's diet and habits from its shape without the materials.",
                "extensions": [
                    "Keep a long bird-feeder log and look for the patterns across the seasons",
                    "Learn the songs and calls of the local birds",
                    "Study migration, and which birds stay and which depart",
                ],
                "observation_focus": "Watch for the child connecting a bird's beak and feet to its diet and home, and identifying local birds by sight and by sound.",
            },
            "unschooling": {
                "invitations": [
                    "Set up a bird feeder or birdbath the child can watch from a window",
                    "Keep binoculars, a bird field guide, and a notebook within reach",
                    "Have recordings of bird songs available to listen to",
                ],
                "real_world_contexts": [
                    "Watching the birds that come to the feeder, the yard, and the park",
                    "Noticing birds and their songs on walks and outings",
                    "Marking the seasons by the birds: the robins of spring, the geese of autumn",
                    "Meeting birds up close, the family's chickens, the ducks at the pond",
                ],
                "conversation_starters": [
                    "That bird has a long thin beak, what do you think it eats?",
                    "Which birds come to our feeder most? What time of day?",
                    "Can you tell which bird is singing without looking?",
                ],
                "resource_bank": [
                    "A bird feeder, binoculars, and a field guide",
                    "Recordings of bird songs and books about birds",
                    "The yard, the park, and the pond, full of real birds to watch",
                ],
                "parent_role": "Make bird-watching a shared pleasure: keep the feeder filled, notice aloud who comes, and follow the child's interest in the birds they grow to love. Wonder together about beaks, songs, and migration, and let the real, watched birds, rather than a worksheet, teach their science.",
                "observation_documentation": "Over time, note whether the child knows several local birds by sight or sound, connects a beak to a diet, and understands the bird life cycle and the marks of a bird. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Bird vocabulary: ornithology, plumage, migration, raptor, songbird, waterfowl, fledgling, incubation",
            "math": "Counting birds at feeders. Graphing species frequency. Measuring wingspan. Migration distances.",
            "history": "Carrier pigeons delivered messages in wars. Falconry is an ancient hunting practice. The bald eagle symbolizes America. Birds have been part of human culture for millennia.",
        },
    },
    "sf-19": {
        "enriched": True,
        "learning_objectives": [
            "List 5 characteristics that define mammals: warm-blooded, fur or hair, live birth (usually), nurse young with milk, breathe air",
            "Compare mammals from at least 3 different habitats and describe their adaptations",
            "Explain how a specific mammal is adapted to its environment with evidence",
            "Recognize that humans are mammals and share all mammalian characteristics",
        ],
        "teaching_guidance": {
            "introduction": "Mammals are the animal group that includes US — humans are mammals. What makes a mammal? Warm-blooded (body temperature stays constant), hair or fur (even whales have a few hairs!), mothers nurse babies with milk, most give live birth (except the platypus and echidna, which lay eggs), and all breathe air with lungs. From the tiny bumblebee bat to the enormous blue whale, mammals live in every habitat on Earth: forests, deserts, oceans, mountains, cities, and polar ice. The child already knows their most familiar mammals: family pets, farm animals, and zoo favorites.",
            "scaffolding_sequence": [
                "Start with the child's own body: 'You are a mammal! Do you have hair? Are you warm-blooded? Did your mom feed you milk as a baby? Yes, yes, yes — you're a mammal!'",
                "List the 5 characteristics of mammals: warm-blooded, hair/fur, milk for young, live birth (usually), breathe air with lungs",
                "Identify familiar mammals: dogs, cats, horses, cows, whales, bats, elephants, mice — all mammals despite looking very different",
                "Compare mammals across habitats: polar bear (Arctic), camel (desert), dolphin (ocean), monkey (rainforest), mole (underground)",
                "Study adaptations: 'The polar bear has thick white fur for warmth and camouflage. The camel stores fat in its hump. The dolphin has flippers for swimming.'",
                "Discuss surprising mammals: bats FLY but are mammals (fur, milk, live birth). Whales live in water but are mammals (breathe air, nurse young).",
                "Compare mammals to other groups: birds have feathers and lay eggs. Fish have scales and breathe water. Reptiles are cold-blooded. What makes mammals different?",
                "Mammal field guide page: the child draws a mammal, labels key mammalian features, and describes its habitat and adaptations",
            ],
            "socratic_questions": [
                "A whale lives in the ocean, has flippers, and looks like a fish. Why is it classified as a mammal instead of a fish?",
                "Your dog and an elephant look NOTHING alike. What do they have in common that makes them both mammals?",
                "Bats fly like birds. Why aren't bats classified as birds? What characteristics make them mammals?",
                "How is a polar bear different from a camel? They're both mammals, but they live in VERY different places. How did each one adapt?",
            ],
            "practice_activities": [
                "Mammal or not? Sort 20 animal pictures into mammals and non-mammals. For each mammal, check: warm-blooded? Fur/hair? Milk? Live birth?",
                "Habitat comparison chart: draw 3 mammals from different habitats. For each, describe the habitat and 2 adaptations that help the mammal survive there.",
                "Pet study (if applicable): observe your pet for 10 minutes. Record mammalian characteristics you can observe: fur, breathing, warmth, nursing (if young are present).",
                "Mammal vs bird vs reptile: compare one animal from each group. What's different about their body covering, birth, and body temperature?",
            ],
            "real_world_connections": [
                "Pets are mammals: dogs, cats, hamsters, rabbits — understanding mammalian needs (warmth, food, water, social connection) makes better pet owners",
                "Farm animals are mammals: cows give milk (a mammalian trait!), sheep grow wool (hair), horses give live birth. Agriculture depends on mammal biology.",
                "YOU are a mammal: your body temperature stays at 98.6°F, you have hair, you breathed air from birth, and you were nursed as a baby. Biology is personal.",
                "Zoos organize animals by classification: the mammal house, the reptile house, the bird aviary. Classification determines how they're cared for.",
            ],
            "common_misconceptions": [
                "Thinking whales and dolphins are fish — they breathe air, nurse their young, and are warm-blooded: they are mammals that live in water",
                "Believing bats are birds — bats have fur (not feathers), give live birth, and nurse young: they are the only mammals that truly fly",
                "Thinking all mammals are large — the bumblebee bat is smaller than a thumb. Many mammals (shrews, mice, voles) are tiny.",
                "Assuming all mammals look similar — mammals range from microscopic-seeming shrews to 100-foot blue whales. The group is incredibly diverse despite sharing core characteristics.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Lists 5 mammalian characteristics correctly",
                "Compares mammals from 3 habitats with specific adaptations",
                "Explains why a specific animal IS or ISN'T a mammal using characteristics",
            ],
            "proficiency_indicators": [
                "Lists 3-4 characteristics",
                "Compares mammals from 1-2 habitats",
            ],
            "developing_indicators": [
                "Lists 1-2 characteristics",
                "Cannot distinguish mammals from other animal groups",
            ],
            "assessment_methods": ["characteristics listing", "habitat comparison", "classification reasoning"],
            "sample_assessment_prompts": [
                "What makes an animal a mammal? Name 5 characteristics.",
                "Compare a polar bear, a camel, and a dolphin. How is each adapted to its habitat?",
                "A bat flies. Why is it a mammal and not a bird?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which of these is NOT a characteristic of mammals?",
                "expected_type": "multiple_choice",
                "options": ["Warm-blooded", "Lay eggs in water", "Have fur or hair", "Nurse young with milk"],
                "correct_answer": "Lay eggs in water",
                "hints": ["Fish lay eggs in water. Most mammals give LIVE birth. Which option doesn't fit?"],
                "explanation": "Laying eggs in water is a characteristic of fish, not mammals. Mammals are warm-blooded, have fur or hair, and nurse young with milk. Most mammals give live birth (with rare exceptions like the platypus).",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "True or false: Humans are mammals.",
                "expected_type": "true_false",
                "correct_answer": "true",
                "hints": ["Check: Are humans warm-blooded? Do they have hair? Were they nursed as babies?"],
                "explanation": "True! Humans are mammals. We are warm-blooded, have hair, give live birth, nurse babies with milk, and breathe air with lungs. We share these characteristics with dogs, elephants, whales, and all other mammals.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "A dolphin lives in the ocean, swims with fins, and looks like a fish. Give 3 reasons why it is classified as a mammal, not a fish.",
                "expected_type": "text",
                "hints": [
                    "Think about: how it breathes, how its babies are born, and whether it's warm or cold-blooded."
                ],
                "explanation": "Three reasons: (1) Dolphins breathe air with lungs — they must come to the surface to breathe (fish breathe water with gills). (2) Dolphins give live birth and nurse their calves with milk (fish lay eggs). (3) Dolphins are warm-blooded — their body temperature stays constant (fish are cold-blooded). Despite living in water and having flippers, dolphins are mammals.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Pick a mammal you know well (a pet, a zoo animal, or a wild animal). Describe its habitat and 2 ways its body is adapted to survive there.",
                "expected_type": "text",
                "hints": [
                    "Think about: fur thickness, body size, feet/paws, speed, diet, and behaviors. How does each help the animal survive in its specific habitat?"
                ],
                "explanation": "Example for a rabbit: 'Rabbits live in meadows and fields (grassland habitat). Adaptation 1: long ears that can rotate to hear predators from far away. Adaptation 2: powerful back legs for running and jumping to escape. Both adaptations help them survive in open areas where predators can see them.'",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Compare three mammals from three different habitats: a polar bear (Arctic), a camel (desert), and a monkey (rainforest). For each, describe one adaptation to their habitat. What characteristic do ALL three share that makes them mammals?",
                "expected_type": "text",
                "hints": [
                    "Each animal's body is adapted to its specific environment. But despite living in completely different places, all three share mammalian characteristics."
                ],
                "explanation": "Polar bear: thick white fur for warmth and camouflage in snow. Camel: hump stores fat for energy during long desert journeys without food. Monkey: grasping hands and a prehensile tail for swinging through tree canopy. Despite these different adaptations, ALL three are warm-blooded, have fur/hair, give live birth, and nurse their young — the defining characteristics of mammals.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "List 5 characteristics of mammals with examples.",
                "type": "open_response",
                "target_concept": "mammal_characteristics",
                "rubric": "Mastery: all 5 with examples. Proficient: 3-4. Developing: 1-2.",
            },
            {
                "prompt": "Compare a mammal from your area to one from a very different habitat.",
                "type": "open_response",
                "target_concept": "mammal_comparison",
                "rubric": "Mastery: clear comparison with adaptation details. Proficient: basic comparison. Developing: cannot compare.",
            },
        ],
        "resource_guidance": {
            "required": ["animal pictures or cards for sorting", "science notebook for comparisons"],
            "recommended": ["living books about mammals", "zoo visit or nature documentary"],
            "philosophy_specific": {
                "classical": "Mammal classification memorized: 5 characteristics. Major mammal orders named. Vocabulary: mammary, warm-blooded, vertebrate, adaptation, habitat.",
                "charlotte_mason": "Living books about mammals with narration. Observing local mammals (squirrels, rabbits, pets) in their natural behavior. Drawing mammals in the nature notebook.",
                "montessori": "Mammal cards sorted by habitat. Parts-of-a-mammal nomenclature cards. Animal classification work with physical figures sorted into groups.",
            },
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Animal sorting with picture cards — no reading. Oral descriptions of adaptations. Drawing mammals rather than writing reports. Video documentaries for visual learning.",
            "adhd": "Animal sorting is hands-on. Zoo visits or nature documentaries are engaging. Pet observation is personal and motivating. Each mammal studied in a separate session.",
            "gifted": "Research mammal orders (primates, rodents, carnivores, cetaceans). Study convergent evolution: why do dolphins and sharks look similar despite being very different? Explore endangered mammals and conservation.",
            "visual_learner": "Animal photographs. Comparison charts. Adaptation diagrams. Documentary videos.",
            "kinesthetic_learner": "Sort physical animal figures. Pet observation. Act out mammal behaviors. Build habitat dioramas.",
            "auditory_learner": "Discuss adaptations as conversations. Listen to nature documentaries. Describe mammals aloud before drawing.",
        },
        "connections": {
            "reading": "Mammal vocabulary: vertebrate, warm-blooded, adaptation, mammary, habitat, endangered, species, evolution",
            "math": "Comparing mammal sizes (weight, length). Graphing populations. Calculating gestation periods. Speed comparisons.",
            "history": "Humans domesticated mammals 10,000+ years ago: dogs, cats, cattle, horses, sheep. Mammal domestication shaped human civilization.",
        },
    },
    "sf-20": {
        "enriched": True,
        "learning_objectives": [
            "Present a nature journal showing at least 6 months of observations with growing detail",
            "Narrate 3 science concepts from memory accurately: one from life science, one from earth science, one from physical science",
            "Demonstrate a simple experiment and explain the results using scientific thinking",
            "Show readiness for the developing science level through observation, narration, and demonstration skills",
        ],
        "teaching_guidance": {
            "introduction": "This capstone assessment celebrates everything the child has learned about science. It is not a test of memorized facts — it is a demonstration of scientific THINKING. The child shows their nature journal (evidence of sustained observation), narrates what they know about science topics (evidence of understanding), and performs a simple experiment (evidence of scientific method skills). This should feel like a science fair presentation to the family, not an exam. The child is sharing what they've discovered, what they wonder about, and how they think like a scientist.",
            "scaffolding_sequence": [
                "Nature journal review: the child and parent look through the journal together. Celebrate growth in observation detail and drawing accuracy.",
                "Narration: the child chooses 3 topics they feel confident about and narrates each one. Topics should span life, earth, and physical science.",
                "Experiment demonstration: the child performs a simple experiment (any from the year) and explains: question, prediction, test, results.",
                "Identification activities: identify 3 rock types, 5 birds, insect body parts, cloud types — demonstrating classification skills",
                "Science vocabulary: use key terms correctly in conversation: habitat, adaptation, metamorphosis, evaporation, vibration, force",
                "Self-reflection: 'What was the most interesting thing you learned? What do you want to study next? What scientific question do you still have?'",
                "Goal setting: the child sets 3 science goals for the developing level: 'I want to learn about space,' 'I want to do more experiments,' 'I want to identify more birds'",
                "Celebrate: a family science night where the child presents their best work, experiments, and discoveries",
            ],
            "socratic_questions": [
                "Show me your nature journal. What entry are you most proud of? Why?",
                "If you could study any science topic for a whole year, what would it be? What makes you curious about it?",
                "You've done many experiments this year. Which one surprised you the most? What did you learn that you didn't expect?",
                "What does it mean to think like a scientist? How is scientific thinking different from just guessing?",
            ],
            "practice_activities": [
                "Science portfolio assembly: gather the best work from the year — journal entries, experiment records, drawings, diagrams — into a portfolio",
                "Family science night: the child sets up 3 'stations' showing different things they learned. Family members visit each station and the child explains.",
                "Best experiment re-do: the child picks their favorite experiment from the year and performs it again, this time with better recording and explanation",
                "Science wonder list: the child writes 5 questions they still want to answer — carrying curiosity forward into the next level",
            ],
            "real_world_connections": [
                "The child can now observe nature with scientific eyes: every walk, every garden visit, every weather change is a science moment",
                "Scientific thinking — observing, questioning, predicting, testing — applies to every subject and every area of life",
                "The nature journal is a personal record of a year of discovery: it will be treasured for decades as a record of what they saw and learned",
                "The child has the foundation to engage with any science topic going forward: biology, earth science, physics, chemistry all build on these skills",
            ],
            "common_misconceptions": [
                "Treating the assessment as a high-pressure test — this should feel like a celebration and sharing, not an examination",
                "Expecting the child to remember every fact from every topic — the goal is to demonstrate THINKING skills (observation, narration, experimentation), not encyclopedic recall",
                "Comparing to grade-level standards — the child's progress is measured against their OWN starting point, not external benchmarks",
                "Believing foundational science is 'done' — these skills (observation, classification, experimentation) deepen at every level. Foundation means BEGINNING, not ending.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Presents a nature journal with 6+ months of observations showing growing detail",
                "Narrates 3 science concepts from memory with accuracy and confidence",
                "Demonstrates an experiment with clear explanation of method and results",
            ],
            "proficiency_indicators": [
                "Journal has consistent entries but detail growth is modest",
                "Narrates 2 topics accurately",
                "Demonstrates experiment but explanation is incomplete",
            ],
            "developing_indicators": [
                "Journal has few entries or little growth",
                "Cannot narrate a science concept from memory",
                "Cannot demonstrate an experiment independently",
            ],
            "assessment_methods": [
                "nature journal portfolio review",
                "oral narration of 3 science concepts",
                "experiment demonstration with explanation",
                "identification activities (rocks, birds, insects, clouds)",
            ],
            "sample_assessment_prompts": [
                "Show me your nature journal. What has changed in your drawings over the year?",
                "Tell me everything you know about the water cycle (or plant life cycle, or magnets, or any topic you choose).",
                "Perform an experiment for me. Tell me your question, prediction, test, and results.",
                "Look at these cloud photos. What types are they?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Name one thing you learned from EACH area of science this year: (1) something about living things, (2) something about Earth, (3) something about how things work (physics).",
                "expected_type": "text",
                "hints": [
                    "Living things: plants, animals, insects, human body. Earth: weather, water cycle, rocks, seasons. Physics: magnets, light, sound, simple machines."
                ],
                "explanation": "Example: (1) Living things: plants need sunlight, water, and soil to grow. (2) Earth: the water cycle has 3 stages — evaporation, condensation, precipitation. (3) Physics: magnets attract objects made of iron but not all metals. Each answer shows knowledge across the three main branches of foundational science.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is the most important skill a scientist needs?",
                "expected_type": "multiple_choice",
                "options": [
                    "Expensive equipment",
                    "Careful observation — paying close attention to what is really there",
                    "A white lab coat",
                    "A loud voice",
                ],
                "correct_answer": "Careful observation — paying close attention to what is really there",
                "hints": ["What was the very FIRST science skill you learned this year?"],
                "explanation": "Careful observation is the foundation of ALL science. Before you can ask questions, make predictions, or design experiments, you must learn to LOOK carefully at the world. Every science topic this year started with observation.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Look through your nature journal. Compare your first entry to your most recent. What improved? What do you notice differently now than you did at the beginning?",
                "expected_type": "text",
                "hints": [
                    "Compare: drawing detail, written observations, types of things observed, vocabulary used, questions asked."
                ],
                "explanation": "A reflective answer identifies specific improvements: 'My drawings have more detail now — I draw individual leaves instead of just a green blob. I write longer observations. I notice things I wouldn't have seen before, like the veins on a leaf or the way ants follow a trail.' This metacognition — thinking about your own learning — is a sign of scientific maturity.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: Once you finish foundational science, you know everything about science.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["Do professional scientists ever stop learning? Is there always more to discover?"],
                "explanation": "False! Foundational science is just the BEGINNING. There are entire fields to explore: chemistry, astronomy, geology, marine biology, ecology, and more. Even professional scientists never stop learning — new discoveries happen every day. The foundation gives you the SKILLS (observation, questioning, experimentation) to keep learning for the rest of your life.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Perform your favorite experiment from this year for your family. Explain: What was your question? What did you predict? What did you do? What happened? What did you learn?",
                "expected_type": "text",
                "hints": [
                    "Choose an experiment you enjoyed and remember well. Walk through ALL 5 scientific method steps. Show your family what you discovered."
                ],
                "explanation": "A complete experiment presentation includes all scientific method steps: (1) Question (what I wanted to find out), (2) Prediction (what I thought would happen and why), (3) Procedure (what I did to test it), (4) Results (what actually happened), (5) Conclusion (what I learned). Presenting to family makes it a real scientific communication — sharing discoveries is what scientists do.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Present your nature journal. Walk me through your growth as an observer this year.",
                "type": "open_response",
                "target_concept": "observation_growth",
                "rubric": "Mastery: shows clear growth in detail, accuracy, and scientific language over 6+ months. Proficient: some growth visible. Developing: little change.",
            },
            {
                "prompt": "Narrate 3 science concepts you learned — one from life science, one from earth science, one from physical science.",
                "type": "open_response",
                "target_concept": "science_narration",
                "rubric": "Mastery: 3 accurate narrations with vocabulary and detail. Proficient: 2 accurate. Developing: 0-1 accurate.",
            },
            {
                "prompt": "Demonstrate an experiment. Explain your question, prediction, method, and results.",
                "type": "open_response",
                "target_concept": "experiment_demonstration",
                "rubric": "Mastery: complete experiment with all scientific method steps explained. Proficient: performs experiment but explanation incomplete. Developing: cannot demonstrate independently.",
            },
            {
                "prompt": "What scientific question do you most want to explore next year?",
                "type": "open_response",
                "target_concept": "scientific_curiosity",
                "rubric": "Mastery: asks a specific, thoughtful question showing genuine curiosity. Proficient: asks a general question. Developing: has no questions.",
            },
        ],
        "resource_guidance": {
            "required": ["completed nature journal from the year", "materials for one experiment demonstration"],
            "recommended": ["science portfolio folder", "celebration supplies for family science night"],
            "philosophy_specific": {
                "classical": "Comprehensive assessment: narration of concepts, identification drills, experiment demonstration. The child proves knowledge through performance across all science areas studied.",
                "charlotte_mason": "Examination by narration and demonstration: the child tells what they know, shows what they can do, and shares their nature journal. No standardized tests — the work itself is the evidence.",
                "montessori": "Observation-based assessment: the teacher reviews the child's work portfolio, experiment records, and nature journal. The child participates in self-assessment. Mastery shown through daily work, not a single test.",
            },
        },
        "time_estimates": {"first_exposure": 30, "practice_session": 20, "assessment": 30},
        "accommodations": {
            "dyslexia": "The entire assessment can be oral and hands-on: narrate science concepts aloud, demonstrate experiments physically, present the nature journal visually. No reading or writing required for any assessment component.",
            "adhd": "Break into 3 short sessions: journal review (15 min), narration (15 min), experiment (15 min). Family science night adds excitement and audience. Allow movement during narration. Celebrate strengths enthusiastically.",
            "gifted": "Extended narrations with depth. Design a NEW experiment for the assessment. Present a science research project. Discuss what they want to study at the developing level. Begin planning a long-term investigation.",
            "visual_learner": "Nature journal IS the visual portfolio. Drawing and diagramming as primary evidence. Experiment demonstration is visual.",
            "kinesthetic_learner": "Experiment demonstration is physical. Setting up a science fair display. Handling specimens and materials during identification activities.",
            "auditory_learner": "Narration is the primary assessment mode. Family science night presentation is oral. Discussing science concepts in conversation format.",
        },
        "connections": {
            "reading": "Science vocabulary built throughout the year enables reading science books independently at the developing level",
            "math": "Measurement, data recording, graphing, and counting — math skills practiced through science all year transfer to math studies",
            "history": "Science history connections: ancient civilizations' inventions, the agricultural revolution, navigation with compasses, and the development of the scientific method itself",
        },
    },
}
