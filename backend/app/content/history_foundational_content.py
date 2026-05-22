"""Pre-enriched content for History Foundational template nodes."""

HISTORY_FOUNDATIONAL_CONTENT = {
    "hf-01": {
        "enriched": True,
        "learning_objectives": [
            "Understand that events happen in sequence over time: past, present, and future",
            "Build a personal timeline with at least 8 events from the child's own life",
            "Place events in correct chronological order on a timeline",
            "Use time vocabulary accurately: yesterday, last year, long ago, before, after, ancient",
        ],
        "teaching_guidance": {
            "introduction": "History is the story of people who came before us. Before a child can understand ancient Egypt or the American Revolution, they need to understand TIME — that things happen in order, that some things happened long ago and some things happened recently. A personal timeline is the perfect starting point because every event on it is meaningful and real to the child. 'First you were born, then you learned to walk, then your sister was born, then you started reading.' This is history — YOUR history.",
            "scaffolding_sequence": [
                "Gather family photos from the child's life and sort them by 'when this happened' — physically handling pictures makes time concrete",
                "Introduce the words past, present, and future with examples from the child's day: 'Breakfast was in the past. We are reading now in the present. Dinner is in the future.'",
                "Build a personal timeline on a long strip of paper: birth on the left, today on the right. Add 5-8 key events (lost first tooth, got a pet, moved houses, started reading).",
                "Extend the timeline backward to before the child was born: 'Mom and Dad got married. Grandma was born. Great-grandpa came to America.'",
                "Introduce the concept of a century and how to place events on a longer timeline",
                "Practice placing historical events on a timeline: 'The pyramids were built here. Columbus sailed here. You were born here.'",
                "Use timeline vocabulary in daily conversation: before, after, first, then, finally, long ago, recently",
                "The child creates their own timeline of a historical period they've been learning about",
            ],
            "socratic_questions": [
                "What happened in your life BEFORE you could read? What happened AFTER?",
                "Your birthday is in the past. Can you change the past? Why or why not?",
                "If I told you something happened 'long ago,' how long ago do you think that means?",
                "Why do you think we put events in order on a timeline instead of just listing them?",
            ],
            "practice_activities": [
                "Photo timeline: print or draw pictures of 8-10 life events and arrange them on a paper strip in order",
                "Family interview: ask a grandparent or parent about 3 things that happened before you were born, then add them to the timeline",
                "Daily timeline: at the end of each day, draw the three most important things that happened in order (morning, afternoon, evening)",
                "Historical timeline game: write events on index cards (dinosaurs, pyramids, Columbus, moon landing, your birthday) and race to put them in order",
            ],
            "real_world_connections": [
                "Family photo albums are personal history books — looking through them with the child and narrating the events",
                "Birthdays mark the passage of time: 'You are 6. Last year you were 5. That's one year of your personal history.'",
                "Seasons show time passing: 'Last winter we built a snowman. That was in the past. Next winter is in the future.'",
                "Calendar and clock: daily tools for organizing time, which is what history does on a larger scale",
            ],
            "common_misconceptions": [
                "Thinking 'long ago' means the same thing for all events — a child may think the 1990s are as distant as ancient Egypt. Use concrete comparisons: 'Your parents were alive then. Your great-great-great grandparents were NOT alive when the pyramids were built.'",
                "Confusing the ORDER of events with how IMPORTANT they are — the most exciting event didn't necessarily happen first",
                "Thinking history only means very old things — yesterday is already history, and the child's own life is part of history",
                "Not understanding that people in the past were real people with real lives, not characters in a made-up story",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Places 5 or more events in correct chronological order on a timeline",
                "Creates a personal timeline with at least 8 events from their life",
                "Uses past, present, and future vocabulary correctly in conversation",
            ],
            "proficiency_indicators": [
                "Places most events correctly with one or two ordering errors",
                "Creates a personal timeline with 5-7 events",
            ],
            "developing_indicators": [
                "Struggles to order events chronologically without help",
                "Confuses past and future vocabulary",
            ],
            "assessment_methods": ["timeline creation", "event ordering", "oral narration using time vocabulary"],
            "sample_assessment_prompts": [
                "Put these 5 events from your life in order on the timeline.",
                "Tell me something that happened in the past, something happening now, and something that will happen in the future.",
                "Where would the pyramids go on this timeline? Before or after your birthday?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which happened FIRST: you learned to walk, or you started school?",
                "expected_type": "multiple_choice",
                "options": ["I learned to walk", "I started school"],
                "correct_answer": "I learned to walk",
                "hints": ["Think about how old you were for each. Babies learn to walk around age 1."],
                "explanation": "You learned to walk first (around age 1) and started school later (around age 5-6). On a timeline, walking comes before school.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Is your breakfast this morning in the past, present, or future?",
                "expected_type": "multiple_choice",
                "options": ["past", "present", "future"],
                "correct_answer": "past",
                "hints": ["Did breakfast already happen, or is it happening now, or hasn't it happened yet?"],
                "explanation": "Breakfast already happened, so it is in the past. The past is everything that has already occurred.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Put these events in order from LONGEST ago to MOST recent: your last birthday, the day you were born, yesterday.",
                "expected_type": "text",
                "correct_answer": "the day you were born, your last birthday, yesterday",
                "hints": ["Which happened first? Which happened most recently?"],
                "explanation": "The day you were born happened first (longest ago), then your last birthday, then yesterday (most recent). A timeline goes from long ago on the left to recent on the right.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: The ancient Egyptians built the pyramids AFTER your grandparents were born.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["The pyramids are thousands of years old. How old are your grandparents?"],
                "explanation": "False. The pyramids were built about 4,500 years ago — thousands of years before your grandparents were born. On a timeline, the pyramids are far to the left.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Name 5 events from your own life and put them in chronological order (from first to most recent).",
                "expected_type": "text",
                "hints": [
                    "Start with when you were very little. What are some big events that happened as you grew up?"
                ],
                "explanation": "A good answer includes 5 real events in correct time order. Example: I was born, I learned to walk, my sister was born, I lost my first tooth, I started reading. Each event should come after the one before it in real time.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Create a timeline of your life with at least 8 events.",
                "type": "open_response",
                "target_concept": "personal_timeline",
                "rubric": "Mastery: 8+ events in correct order with dates or ages. Proficient: 5-7 events mostly in order. Developing: fewer than 5 events or out of order.",
            },
            {
                "prompt": "Tell me something from the past, something happening in the present, and something in the future.",
                "type": "open_response",
                "target_concept": "time_vocabulary",
                "rubric": "Mastery: gives clear examples for all three with correct vocabulary. Proficient: gives examples but may confuse terms. Developing: cannot distinguish past/present/future.",
            },
            {
                "prompt": "Where would dinosaurs go on this timeline — before the pyramids or after your birthday?",
                "type": "text",
                "correct_answer": "before the pyramids",
                "target_concept": "deep_time",
            },
        ],
        "resource_guidance": {
            "required": ["long strip of paper for timeline", "family photos or drawings of key events"],
            "recommended": ["timeline cards with historical events", "Book of Centuries notebook"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Read all content aloud. Use photo timelines rather than text-heavy timelines. Oral narration of events rather than written. Large, image-heavy timeline cards.",
            "adhd": "Keep timeline sessions to 15-20 minutes. Hands-on: physically cut, arrange, and glue timeline events. Interview a grandparent for movement and engagement. Build the timeline on the floor for large-muscle involvement.",
            "gifted": "Extend to geological time (dinosaurs, ice ages). Introduce BC/AD or BCE/CE notation. Research family genealogy as a project. Compare personal timeline to a historical timeline side by side.",
            "visual_learner": "Color-coded timeline with different colors for different eras. Illustrated events. Large wall display.",
            "kinesthetic_learner": "Floor timeline you can walk along. Movable event cards. Build timeline with blocks or LEGOs.",
            "auditory_learner": "Narrate the timeline aloud as you build it. Family storytelling sessions. Chant era names in order.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "History is the story of people who came before us, and it begins with time itself. Things happen in order: some long ago, some recently, some yet to come. Before a child can study ancient Egypt or any far-off age, they must grasp that events fall in sequence, past, present, and future. Today we build a personal timeline of the child's own life, place events in their true order, and use the words of time: yesterday, last year, long ago, before, after, ancient.",
                "gradual_release": {
                    "i_do": "Lay out a few family photos and think aloud, sorting them by when they happened: this was first, this came after. Mark a strip of paper, birth on the left, today on the right, and place events along it. Use the words of time plainly: this was long ago, this was recent.",
                    "we_do": "Build a personal timeline together: gather the child's life events, decide the order of each, place them on the strip, and name each with the right word of time.",
                    "you_do": "Child builds a personal timeline of at least eight events, places events in correct chronological order, and uses time vocabulary accurately.",
                },
                "guided_practice": [
                    "Sort family photos or event cards by when each happened",
                    "Place events on a timeline strip from long ago on the left to today on the right",
                    "Use the words of time, before and after, long ago and recently, in describing events",
                ],
                "independent_practice": [
                    "Build a personal timeline of eight or more events from the child's own life",
                    "Place a set of historical events in order on a longer timeline",
                ],
                "mastery_check": [
                    "Build a personal timeline with at least eight events from the child's life",
                    "Place events in correct chronological order on a timeline",
                    "Use past, present, and future and the words of time accurately",
                ],
                "spiral_review": [
                    "Revisit ordering the events of a single day, the smallest timeline, before working with longer spans",
                ],
            },
            "classical": {
                "narrative_introduction": "All of history is laid upon one foundation: time, and the order of events within it. Before the child can be told the story of any age, they must hold the great truth that events fall in sequence, the one before, the next after, stretching from the ancient past, through the present moment, toward the future. The timeline is the spine on which every later story of history will be hung.",
                "memory_work": {
                    "chants": [
                        "Chant the order of time: the past behind, the present now, the future yet to come",
                        "Chant the words of time: long ago and ancient, before and after, yesterday and last year",
                    ],
                    "recitations": [
                        "Recite that events fall in sequence, each in its own place, and that the timeline runs from long ago on the left to today on the right",
                    ],
                },
                "copywork": [
                    "Copy the words of time, before and after, long ago and ancient, and a few dated events set in their order",
                ],
                "recitation_routine": "Begin each lesson by reciting the order of time and the words of time before any new work, so the foundation is rehearsed before the building.",
                "history_integration": "This is the first stone of the chronological spine itself: the personal timeline the child builds now will grow, year by year, to hold the pyramids, the empires, and the whole story of humankind, each event placed in its true and ordered spot.",
                "read_aloud_suggestions": [
                    "A story that moves clearly through time, from a character's early days to later ones, read aloud so the child hears events fall in order",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A beautifully illustrated book that follows a life or a family across the years, with true artwork, the kind that makes the passage of time felt",
                ],
                "short_lesson_flow": "Gather real family photographs and look through them together, unhurried, wondering when each one happened and what came before and after. Begin a Book of Centuries or a simple timeline, and let the child add an event of their own life, drawn in their own hand. A few minutes is enough; the timeline grows slowly, over the years.",
                "narration_prompt": "Tell me about your life so far, in order. What happened first, what came after, and what is happening now?",
                "real_world_objects": [
                    "Real family photographs, sorted and ordered",
                    "A Book of Centuries or a long timeline strip the child adds to over time",
                    "A calendar and the turning seasons, time felt in the living year",
                ],
                "nature_connection": "The seasons are a timeline the child can watch: last winter's snowman, this spring's buds, the summer to come, the year itself teaching that events fall in order and time moves on.",
                "habit_focus": "The habit of attention: noticing the order in which things happen, in a day, a year, and a life.",
            },
            "montessori": {
                "prepared_materials": [
                    "A long timeline strip, the personal timeline, with movable event cards",
                    "Family photographs the child orders by hand",
                    "The Montessori timeline of life, the long strip showing Earth's vast history",
                    "Cards of time vocabulary: before, after, long ago, ancient",
                ],
                "presentation": {
                    "three_period_lesson": "With the event cards on the timeline: this event came before, this one after; show me the event that came before; did this event come before or after?",
                    "steps": [
                        "The child handles real photographs and event cards and orders them by when each happened",
                        "The child places the ordered events along the personal timeline strip, left to right",
                        "The child names each event with the right word of time and may set their life against the long timeline of life",
                    ],
                },
                "control_of_error": "The true order of events is the control: the child checks each placement against what really happened, and an event set out of order is felt at once to be wrong, for a baby cannot crawl after they walk.",
                "abstraction_pathway": "From handling and ordering concrete photographs and event cards, to placing them on the timeline strip, toward grasping time as an ordered line stretching far beyond the child's own life.",
                "extensions": [
                    "Extend the timeline back before the child's birth, to parents and grandparents",
                    "Place historical events on a longer timeline",
                    "Work with the timeline of life and the vastness of deep time",
                ],
                "observation_focus": "Watch for the child ordering events by when they truly happened rather than by how exciting they were, and using the words of time with growing precision.",
            },
            "unschooling": {
                "invitations": [
                    "Keep family photo albums and a box of photographs within easy reach to look through",
                    "Leave out a long strip of paper and markers for a timeline the child may build",
                    "Have books and documentaries about long-ago times available",
                ],
                "real_world_contexts": [
                    "Looking through family photos and wondering when each was taken",
                    "Marking time by birthdays, holidays, and the turning seasons",
                    "Hearing grandparents and elders tell of the days before the child was born",
                    "Using the calendar and the clock, the everyday tools of time",
                ],
                "conversation_starters": [
                    "What happened in your life before you can remember? Who could tell us?",
                    "Was that a long time ago, or just recently? How can you tell?",
                    "Do you think the pyramids were built before or after Grandma was born?",
                ],
                "resource_bank": [
                    "Family photo albums and old photographs",
                    "A long roll of paper for a timeline kept available",
                    "Books, documentaries, and grandparents' stories about times past",
                ],
                "parent_role": "Look through old photographs with the child and tell the family stories, wondering aloud about when things happened and what came before and after. Let the child build a timeline if they wish, and let real photos, real memories, and real elders, rather than a worksheet, give them a feel for time.",
                "observation_documentation": "Over time, note whether the child orders events by when they happened, uses the words of time, and senses that the past stretches far back beyond their own life. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Sequence and chronological order in stories — beginning, middle, end is a timeline of a story",
            "math": "Number lines are timelines with numbers. Counting forward is like moving forward in time.",
            "science": "Seasons cycle in order through the year. Plant growth follows a timeline: seed, sprout, plant, flower.",
        },
    },
    "hf-02": {
        "enriched": True,
        "learning_objectives": [
            "Define what a civilization is using at least 5 characteristics: food supply, social structure, government, religion, arts, technology, writing",
            "Name and locate the four major ancient river valley civilizations on a map",
            "Explain why early civilizations developed near rivers",
            "Compare two ancient civilizations on at least two characteristics",
        ],
        "teaching_guidance": {
            "introduction": "History is the story of people who came before us, and civilizations are the biggest chapters in that story. A civilization is what happens when people stop wandering and start building: they grow food in one place, create rules for living together, develop art and writing, and pass their knowledge to their children. The first civilizations all grew beside great rivers — the Nile, the Tigris and Euphrates, the Indus, and the Yellow River — because water meant food, and food meant people could stay.",
            "scaffolding_sequence": [
                "Start with the concept of needs: 'What do people need to survive? Food, water, shelter. Where would YOU choose to live if you had no stores or faucets?'",
                "Introduce the idea of farming: people discovered they could GROW food instead of hunting and gathering. This changed everything.",
                "Show a world map and point to the four river valleys: Nile (Egypt), Tigris-Euphrates (Mesopotamia), Indus (India), Yellow River (China)",
                "Define civilization with 5 characteristics: stable food supply, social structure, government, religion/culture, arts/technology/writing",
                "For each characteristic, give a concrete example from any ancient civilization the child can picture",
                "Compare two civilizations: 'Both Egypt and Mesopotamia farmed near rivers. But they built different things: pyramids vs ziggurats.'",
                "Place all four civilizations on the timeline: they are roughly the same age (3000-2000 BC), which is remarkable",
                "The child draws a simple world map from memory, marking the four river valley civilizations",
            ],
            "socratic_questions": [
                "Why do you think ALL the first civilizations grew up near rivers? What's so special about rivers?",
                "If you were starting a new civilization, what would you need first: a king, food, or writing? Why?",
                "People lived for thousands of years as hunters and gatherers. What changed that made them want to farm instead?",
                "Do we still live in a civilization today? Which of the 5 characteristics does our society have?",
            ],
            "practice_activities": [
                "Civilization checklist: look at your own community and check off which civilization characteristics it has (food supply? government? writing? arts?)",
                "Map drawing: draw the world's major rivers and mark where civilizations grew. Label each one.",
                "River valley experiment: pour water on sand and observe where it collects. That's where people would farm. That's where civilizations began.",
                "Civilization comparison chart: pick two civilizations and fill in a chart comparing their food, buildings, writing, and government",
            ],
            "real_world_connections": [
                "Your own town or city is near a water source — rivers, lakes, or underground aquifers. Civilization still needs water.",
                "Farming is still the foundation: everything you eat was grown or raised somewhere. Ancient farmers figured this out first.",
                "Writing is a civilization marker: you are learning to read and write, just as ancient scribes did thousands of years ago",
                "Government exists in your town: police, fire departments, leaders who make rules. Ancient civilizations invented this.",
            ],
            "common_misconceptions": [
                "Thinking ancient people were 'primitive' or less intelligent — they were just as smart as us, working with different technology",
                "Assuming all four civilizations knew about each other — they developed mostly independently, which makes the similarities even more remarkable",
                "Confusing civilization with 'city' — a civilization is broader, encompassing culture, technology, government, and social structure across an entire region",
                "Thinking civilization started everywhere at the same time — it began in specific river valleys and spread from there over thousands of years",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Lists 5 characteristics of a civilization and gives examples",
                "Names and locates all 4 ancient river valley civilizations on a map",
                "Explains why rivers were essential for early civilizations",
            ],
            "proficiency_indicators": [
                "Lists 3-4 characteristics of civilization",
                "Names and locates 2-3 civilizations on a map",
            ],
            "developing_indicators": [
                "Can describe what a civilization is in general terms but not the specific characteristics",
                "Cannot locate civilizations on a map without help",
            ],
            "assessment_methods": ["oral narration", "map labeling", "comparison chart"],
            "sample_assessment_prompts": [
                "What makes a group of people a civilization? Name at least 5 things.",
                "Show me on this map where the first civilizations grew. Why did they grow there?",
                "How were ancient Egypt and ancient Mesopotamia alike? How were they different?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Why did the first civilizations develop near rivers?",
                "expected_type": "multiple_choice",
                "options": [
                    "Rivers were pretty to look at",
                    "Rivers provided water for drinking and farming",
                    "People liked to swim",
                    "Rivers kept enemies away",
                ],
                "correct_answer": "Rivers provided water for drinking and farming",
                "hints": ["Think about what people need most to survive and grow food."],
                "explanation": "Rivers provided water for drinking, cooking, and most importantly, farming. Farming near rivers let people grow enough food to stay in one place, which is how civilizations began.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which of these is NOT one of the characteristics of a civilization?",
                "expected_type": "multiple_choice",
                "options": ["Government", "Writing", "Stable food supply", "Having pets"],
                "correct_answer": "Having pets",
                "hints": [
                    "Think about the 5 key characteristics: food, government, social structure, religion/culture, arts/technology/writing."
                ],
                "explanation": "The 5 characteristics of civilization are: stable food supply, social structure, government, religion/culture, and arts/technology/writing. Having pets is not one of the defining characteristics.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Name the four great rivers where ancient civilizations developed.",
                "expected_type": "text",
                "hints": ["One is in Africa, two are in the Middle East, one is in India, and one is in China."],
                "explanation": "The Nile (Egypt), the Tigris and Euphrates (Mesopotamia), the Indus (India), and the Yellow River (China). These four river valleys are where the first civilizations grew.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: Ancient people were less intelligent than people today.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["Think about what ancient people invented: farming, writing, pyramids, mathematics..."],
                "explanation": "False. Ancient people were just as intelligent as modern people. They invented farming, writing, mathematics, architecture, and government. They simply had different technology and knowledge than we do.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Pick two ancient civilizations and compare them. How were they alike? How were they different?",
                "expected_type": "text",
                "hints": [
                    "Choose two (Egypt, Mesopotamia, China, India). Think about their rivers, buildings, writing, and government."
                ],
                "explanation": "A good comparison might note: Egypt and Mesopotamia both grew near rivers and developed writing. But Egypt had hieroglyphics while Mesopotamia had cuneiform. Egypt built pyramids; Mesopotamia built ziggurats. Egypt had pharaohs; Mesopotamia had city-state kings.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Draw a map showing where the four ancient civilizations grew. Label each one and its river.",
                "type": "open_response",
                "target_concept": "civilization_geography",
                "rubric": "Mastery: all 4 correctly placed with rivers labeled. Proficient: 2-3 correct. Developing: cannot locate on map.",
            },
            {
                "prompt": "What are 5 things that make a group of people a civilization?",
                "type": "open_response",
                "target_concept": "civilization_definition",
                "rubric": "Mastery: names all 5 with examples. Proficient: names 3-4. Developing: names 1-2.",
            },
            {
                "prompt": "Why were rivers so important for the first civilizations?",
                "type": "open_response",
                "target_concept": "river_valley_importance",
                "rubric": "Mastery: explains water for farming, drinking, trade, and staying in one place. Proficient: mentions farming. Developing: vague answer.",
            },
        ],
        "resource_guidance": {
            "required": ["world map or globe", "paper for drawing maps"],
            "recommended": [
                "timeline cards for ancient civilizations",
                "picture books or living books about ancient civilizations",
            ],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Read all content aloud. Use image-heavy resources: pictures of pyramids, ziggurats, the Great Wall. Map activities are visual and tactile, requiring no reading. Oral narration of civilizations rather than written.",
            "adhd": "Keep sessions to 15-20 minutes. Build a model of a river valley with sand and water. Draw maps with colored markers. Act out scenes from ancient life (farmer, pharaoh, scribe).",
            "gifted": "Compare all four civilizations on a detailed chart. Research what happened to each one. Discuss why civilizations rise and fall. Introduce the concept of the Agricultural Revolution as a turning point.",
            "visual_learner": "Map work is a natural strength. Use illustrated timelines. Picture books with photographs of ancient sites.",
            "kinesthetic_learner": "Build a river valley in a sandbox. Create clay tablets like Mesopotamian scribes. Construct miniature pyramids.",
            "auditory_learner": "Listen to stories about ancient civilizations. Discuss and debate: 'Which civilization would you want to live in?' Chant civilization names and rivers.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "A civilization is what arises when people settle in one place and build a shared life: a steady food supply, a social order, a government, a religion and culture, and the arts, technology, and writing. The first civilizations all grew beside great rivers, the Nile, the Tigris and Euphrates, the Indus, and the Yellow River, because water meant farming, and farming meant people could stay. Today we define a civilization by its characteristics, locate the four river valleys, explain why rivers mattered, and compare two civilizations.",
                "gradual_release": {
                    "i_do": "Name the characteristics of a civilization and give a plain example of each. Point on the map to the four river valleys and think aloud: water for farming, farming for a steady food supply, a steady food supply so people could stay and build. Compare two civilizations on a chart.",
                    "we_do": "List the characteristics of a civilization together, locate the four river valleys on the map, and fill in a chart comparing two of them.",
                    "you_do": "Child defines a civilization by at least five characteristics, names and locates the four river valley civilizations, explains why they grew near rivers, and compares two of them.",
                },
                "guided_practice": [
                    "List the characteristics of a civilization and give an example of each",
                    "Locate the four river valley civilizations on a map",
                    "Compare two civilizations on a chart of their characteristics",
                ],
                "independent_practice": [
                    "Draw a world map from memory, marking the four river valley civilizations",
                    "Write a comparison of two ancient civilizations, alike and different",
                ],
                "mastery_check": [
                    "Define a civilization using at least five characteristics",
                    "Name and locate the four river valley civilizations on a map",
                    "Explain why early civilizations grew near rivers and compare two of them",
                ],
                "spiral_review": [
                    "Revisit placing events and ages on the timeline, since the four civilizations are set there together",
                ],
            },
            "classical": {
                "narrative_introduction": "There came a turning in the long story of humankind: people who had wandered as hunters learned to farm, and farming let them settle, and settling let them build. From this rose civilization, marked by a steady food supply, a social order, a government, a faith, and the arts and writing. And it rose first, remarkably, in four river valleys at once, the Nile, the Tigris and Euphrates, the Indus, the Yellow River, each unknown to the others.",
                "memory_work": {
                    "chants": [
                        "Chant the characteristics of a civilization: a food supply, a social order, a government, a religion, and the arts and writing",
                        "Chant the four river valleys: the Nile, the Tigris and Euphrates, the Indus, and the Yellow River",
                    ],
                    "recitations": [
                        "Recite that civilization rose where rivers gave water for farming, so that people could settle, gather, and build",
                    ],
                },
                "copywork": [
                    "Copy the characteristics of a civilization and the names of the four great rivers and their lands",
                ],
                "recitation_routine": "Begin each lesson by reciting the characteristics of a civilization and the four river valleys before any new study.",
                "history_integration": "Place the four river valley civilizations together on the chronological spine, near the dawn of recorded history, and see that Egypt, Mesopotamia, India, and China all begin at roughly the same point, the gateway through which all later history flows.",
                "read_aloud_suggestions": [
                    "A living account of how a wandering people first settled, farmed, and built a city, read aloud so the child hears civilization begin",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A beautifully illustrated living book about how the first civilizations arose along their rivers, with true artwork and never a dry textbook",
                ],
                "short_lesson_flow": "Read a living portion about the first civilizations aloud, unhurried, and let the child narrate it back. Spread a map and let the child trace the four great rivers with a finger. The child may draw the map into a Book of Centuries. Wonder together why people chose to settle by water. Keep it warm and unhurried.",
                "narration_prompt": "Tell me about the first civilizations. Why did people settle by the rivers, and what did they build there?",
                "real_world_objects": [
                    "A globe or world map, the four river valleys traced by hand",
                    "A Book of Centuries for the child's own drawn map",
                    "Living books about the ancient civilizations",
                ],
                "nature_connection": "Notice the rivers and water of the child's own region, and how a town grows where water flows, the very reason the first civilizations rose where they did, observed close to home.",
                "habit_focus": "The habit of attention: listening to the story of a far-off people closely enough to tell it back and to wonder why they lived as they did.",
            },
            "montessori": {
                "prepared_materials": [
                    "A globe and map of the world for locating the river valleys",
                    "Continent folders with photographs of the ancient civilizations",
                    "The fundamental needs of humans chart, applied to each civilization",
                    "Timeline cards of the civilizations with movable pieces",
                ],
                "presentation": {
                    "three_period_lesson": "With the river valley cards: this is the Nile, the river of Egypt; show me the Nile; which river valley civilization is this?",
                    "steps": [
                        "The child locates the four river valleys on the globe and map",
                        "The child explores each civilization through its continent folder and the fundamental needs of humans, food, shelter, government, and the rest",
                        "The child sets the four civilizations on the timeline and compares two of them",
                    ],
                },
                "control_of_error": "The map and globe are the control for location, and the fundamental needs framework is the control for the definition: a settlement that lacks a food supply, an order, or a government is felt not yet to be a civilization, so the framework checks the child's reasoning.",
                "abstraction_pathway": "From locating the concrete river valleys on the globe and exploring real photographs, to checking each against the fundamental needs of humans, toward grasping civilization as a pattern of shared life that may be defined and compared.",
                "extensions": [
                    "Apply the fundamental needs of humans to all four civilizations",
                    "Compare what became of each civilization over time",
                    "Investigate why all four rose by rivers at the same point in history",
                ],
                "observation_focus": "Watch for the child connecting a civilization to the river that fed it, and defining civilization by its characteristics rather than by a single city or building.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a globe and world map within reach for free exploring",
                    "Leave out richly illustrated books about the ancient civilizations",
                    "Have documentaries about ancient Egypt, Mesopotamia, India, and China available",
                ],
                "real_world_contexts": [
                    "Noticing how the child's own town depends on water, food, rules, and shared work",
                    "Visiting a museum with artifacts from the ancient civilizations",
                    "Finding the great rivers and their lands on a map or globe",
                    "Wondering, while reading or watching, why people long ago lived as they did",
                ],
                "conversation_starters": [
                    "Why do you think the first cities all grew up next to rivers?",
                    "What does our town need to keep everyone fed and safe? Did ancient cities need the same?",
                    "If you were starting a new place to live, what would you build first?",
                ],
                "resource_bank": [
                    "A globe, a world map, and atlases",
                    "Illustrated books and documentaries about the ancient civilizations",
                    "Museums with ancient artifacts",
                ],
                "parent_role": "Follow the child's curiosity about the ancient world into books, documentaries, and museums, and wonder aloud about why people settled where they did and what makes a civilization. Let real maps, real artifacts, and real stories, rather than a worksheet, teach how civilization began.",
                "observation_documentation": "Over time, note whether the child can say what makes a civilization, locate the great river valleys, explain why rivers mattered, and compare two ancient civilizations. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Living books about ancient civilizations build both reading skills and historical knowledge simultaneously",
            "math": "Ancient civilizations invented mathematics: counting, measurement, geometry for building pyramids",
            "science": "Farming is applied science: understanding seasons, water, soil, and plants. Ancient civilizations figured this out through observation.",
        },
    },
    "hf-03": {
        "enriched": True,
        "learning_objectives": [
            "Narrate the story of ancient Egypt covering the Nile, pharaohs, pyramids, and daily life",
            "Explain how the annual flooding of the Nile made Egyptian civilization possible",
            "Draw and label a simple map of Egypt showing the Nile, the delta, the desert, and the pyramids",
            "Describe at least 3 aspects of daily life in ancient Egypt",
        ],
        "teaching_guidance": {
            "introduction": "Ancient Egypt is one of the most fascinating civilizations in all of history, and children are naturally drawn to it — the pyramids, the mummies, the pharaohs, the mysterious hieroglyphics. Egypt lasted for over 3,000 years along the banks of the Nile River. Every year, the Nile flooded and left behind rich, dark soil perfect for farming. This gift of the Nile made everything else possible: food, cities, temples, art, and the incredible pyramids that still stand today.",
            "scaffolding_sequence": [
                "Start with the Nile: show it on a map. Explain the annual flooding and why it was a gift, not a disaster.",
                "Introduce pharaohs: the rulers of Egypt who were considered living gods. Name a few: Khufu (built the Great Pyramid), Hatshepsut (female pharaoh), Tutankhamun (the boy king).",
                "Explore the pyramids: how they were built (ramps, human labor, incredible engineering), why they were built (tombs for pharaohs), and how long they took (about 20 years each).",
                "Introduce hieroglyphics: picture-writing that took years to learn. Scribes were the educated class.",
                "Discuss daily life: farmers, craftspeople, scribes, priests, and the pharaoh. What did ordinary people eat, wear, and do?",
                "Touch on mummification: why Egyptians preserved the dead (belief in the afterlife) and the basic process.",
                "Draw a map of Egypt from memory: Nile running through desert, delta at the top, pyramids near Cairo.",
                "Compare Egypt to another civilization the child knows (Mesopotamia or modern life): what's similar, what's different?",
            ],
            "socratic_questions": [
                "The Nile flooded every year and the Egyptians were HAPPY about it. Why would a flood be good news?",
                "The pharaoh was considered a god on earth. How would life be different if your leader were considered a god?",
                "It took about 20 years and thousands of workers to build one pyramid. Why would a civilization spend so much time and effort on a building?",
                "If you lived in ancient Egypt, would you rather be a pharaoh, a scribe, or a farmer? Why?",
            ],
            "practice_activities": [
                "Build a pyramid: use sugar cubes, blocks, or sand to build a small pyramid. Discuss the engineering challenge.",
                "Write your name in hieroglyphics using a simple alphabet chart — experience what ancient Egyptian writing felt like",
                "Map of Egypt: draw the Nile running through desert, add the delta, pyramids, and labels",
                "Egyptian daily life roleplay: each family member takes a role (pharaoh, scribe, farmer, priest) and describes their day",
            ],
            "real_world_connections": [
                "The pyramids still exist today — they are nearly 4,500 years old, making them the oldest major structures on Earth",
                "The Nile is still the lifeline of Egypt: modern Egyptian farming still depends on Nile water",
                "Writing changed the world: hieroglyphics were one of the first writing systems. You are using the same concept every time you write.",
                "Museums often have Egyptian artifacts: mummy cases, statues, jewelry. A museum visit makes Egypt real.",
            ],
            "common_misconceptions": [
                "Thinking slaves built the pyramids — current evidence suggests paid workers built them, not slaves. They were organized in teams and took pride in the work.",
                "Believing all Egyptians were rich and lived in palaces — most Egyptians were farmers who lived simple lives in mud-brick houses",
                "Thinking mummies were scary — for Egyptians, mummification was a loving, sacred act preparing someone for eternal life",
                "Assuming Egypt is only about the past — Egypt is a modern country with 100+ million people living there today",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Narrates ancient Egypt with Nile flooding, pharaohs, pyramids, and daily life",
                "Draws and labels a map of Egypt from memory",
                "Explains how the Nile made civilization possible",
            ],
            "proficiency_indicators": [
                "Narrates several facts about Egypt but may not connect them to the Nile",
                "Draws a partial map with some labels",
            ],
            "developing_indicators": [
                "Knows about pyramids and mummies but cannot narrate a connected story of Egypt",
                "Cannot explain why the Nile was important",
            ],
            "assessment_methods": ["oral narration", "map drawing", "comparison to another civilization"],
            "sample_assessment_prompts": [
                "Tell me the story of ancient Egypt. Start with the Nile and include at least 5 important things.",
                "Draw a map of Egypt and label the most important features.",
                "How did the Nile River help the Egyptians build their civilization?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Why was the Nile River so important to ancient Egypt?",
                "expected_type": "multiple_choice",
                "options": [
                    "It was good for swimming",
                    "Its annual floods left rich soil for farming",
                    "It kept enemies away",
                    "Egyptians used it to make pyramids",
                ],
                "correct_answer": "Its annual floods left rich soil for farming",
                "hints": ["Think about what people need most: food. How does a river help with that?"],
                "explanation": "The Nile flooded every year, leaving behind rich, dark soil perfect for farming. This reliable food supply let Egyptians build cities, temples, and pyramids.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What were the pyramids built for?",
                "expected_type": "multiple_choice",
                "options": ["Homes for families", "Tombs for pharaohs", "Schools", "Grain storage"],
                "correct_answer": "Tombs for pharaohs",
                "hints": [
                    "Pharaohs were buried with treasure for the afterlife. Where did they put all that treasure?"
                ],
                "explanation": "The pyramids were massive tombs built for pharaohs. Egyptians believed pharaohs needed their bodies and treasures preserved for the afterlife.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is the Egyptian picture-writing system called?",
                "expected_type": "text",
                "correct_answer": "hieroglyphics",
                "hints": ["It starts with 'hiero-' and uses pictures instead of letters."],
                "explanation": "Hieroglyphics was the Egyptian writing system using picture symbols. Only specially trained scribes could read and write hieroglyphics.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: Most ancient Egyptians lived in palaces and were very wealthy.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["Think about what you know about farming. Were most people in ancient times rich?"],
                "explanation": "False. Most ancient Egyptians were farmers who lived in simple mud-brick houses. Only the pharaoh and nobles lived in luxury. Ordinary life was hard work in the fields.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "In your own words, tell the story of ancient Egypt. Include the Nile, pharaohs, pyramids, and what daily life was like.",
                "expected_type": "text",
                "hints": [
                    "Start with the Nile and farming. Then talk about who ruled, what they built, and how ordinary people lived."
                ],
                "explanation": "A good narration covers: the Nile's floods creating farmland, pharaohs ruling as god-kings, pyramids built as tombs, hieroglyphics as writing, and daily life for farmers, scribes, and craftspeople. It should sound like telling a story, not listing facts.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Narrate the story of ancient Egypt in your own words.",
                "type": "open_response",
                "target_concept": "egypt_narration",
                "rubric": "Mastery: covers Nile, pharaohs, pyramids, daily life, and writing. Proficient: covers 3-4 topics. Developing: knows only 1-2 facts.",
            },
            {
                "prompt": "Draw and label a map of ancient Egypt.",
                "type": "open_response",
                "target_concept": "egypt_map",
                "rubric": "Mastery: Nile, delta, desert, pyramids labeled. Proficient: Nile and pyramids. Developing: cannot draw from memory.",
            },
        ],
        "resource_guidance": {
            "required": ["map of Egypt", "pictures of pyramids, hieroglyphics, and daily life"],
            "recommended": ["living books about ancient Egypt", "model-building supplies for pyramids"],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 20, "assessment": 10},
        "accommodations": {
            "dyslexia": "Read all Egypt content aloud. Use documentaries and image-heavy books. Oral narration of the Egypt story rather than written. Hands-on pyramid building and map drawing.",
            "adhd": "Build a pyramid (hands-on). Act out scenes from Egyptian life. Watch a short documentary. Keep sessions to 15-20 minutes with a different Egypt subtopic each session.",
            "gifted": "Research Howard Carter's discovery of Tutankhamun's tomb. Compare Egyptian government to modern government. Explore how hieroglyphics were decoded (the Rosetta Stone).",
            "visual_learner": "Photographs of real Egyptian sites. Illustrated cross-sections of pyramids. Map drawing is a core activity.",
            "kinesthetic_learner": "Build pyramids, write hieroglyphics, make a shaduf model, create a Nile flood simulation with sand and water.",
            "auditory_learner": "Listen to stories about pharaohs and scribes. Discuss and debate Egyptian topics. Audio documentaries about ancient Egypt.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Ancient Egypt rose along the Nile and lasted more than three thousand years. Each year the Nile flooded and left rich dark soil, a gift that made farming, and so cities, temples, and the pyramids, possible. Egypt was ruled by pharaohs, written in hieroglyphics by scribes, and worked by farmers and craftspeople. Today we narrate the story of ancient Egypt, explain how the Nile flood made it possible, draw a map of Egypt, and describe daily life there.",
                "gradual_release": {
                    "i_do": "Tell the story of Egypt aloud in order: the Nile and its yearly flood, the farms it fed, the pharaohs who ruled as god-kings, the pyramids built as their tombs, the scribes and their hieroglyphics, the farmers in their mud-brick houses. Draw the map as I go, the Nile, the delta, the desert, the pyramids.",
                    "we_do": "Retell the story of Egypt together, draw and label the map of Egypt, and name several aspects of daily life there.",
                    "you_do": "Child narrates the story of ancient Egypt, explains how the Nile flood made the civilization possible, draws and labels a map of Egypt, and describes at least three aspects of daily life.",
                },
                "guided_practice": [
                    "Retell the story of Egypt in order: the Nile, the pharaohs, the pyramids, daily life",
                    "Draw and label a map of Egypt: the Nile, the delta, the desert, the pyramids",
                    "Describe aspects of daily life for farmers, scribes, and craftspeople",
                ],
                "independent_practice": [
                    "Narrate the full story of ancient Egypt from memory",
                    "Compare ancient Egypt to another civilization the child has studied",
                ],
                "mastery_check": [
                    "Narrate ancient Egypt covering the Nile, pharaohs, pyramids, and daily life",
                    "Explain how the annual flooding of the Nile made Egyptian civilization possible",
                    "Draw and label a map of Egypt and describe three aspects of daily life",
                ],
                "spiral_review": [
                    "Revisit the characteristics of a civilization, and find each one in ancient Egypt",
                ],
            },
            "classical": {
                "narrative_introduction": "Of all the ancient civilizations, none captures the mind like Egypt: the pyramids rising from the desert, the pharaohs ruled as living gods, the scribes setting down hieroglyphics, the mummies prepared for eternity. And all of it was the gift of one river. Each year the Nile rose and flooded, and each year it left behind the black soil that fed a civilization for three thousand years.",
                "memory_work": {
                    "chants": [
                        "Chant the gift of the Nile: it floods, it leaves rich soil, it feeds the farms, it makes Egypt",
                        "Chant the orders of Egypt: the pharaoh above, then the scribes and priests, then the craftspeople, then the farmers",
                    ],
                    "recitations": [
                        "Recite that the Nile flooded each year and left rich soil, and that this gift made Egyptian civilization possible",
                    ],
                },
                "copywork": [
                    "Copy a few key facts of ancient Egypt, neatly, and the words pharaoh, pyramid, hieroglyphics, and Nile",
                ],
                "recitation_routine": "Begin each lesson by reciting the gift of the Nile and narrating yesterday's portion of the Egypt story before adding the next.",
                "history_integration": "Place ancient Egypt on the chronological spine: it begins among the first river valley civilizations and endures, remarkably, for three thousand years, longer than the whole span from the Roman Empire to today, a vast and steady stretch of the spine.",
                "read_aloud_suggestions": [
                    "A living book that tells the story of ancient Egypt with vividness and truth, read aloud for narration",
                    "A tale set in ancient Egypt, in the life of a scribe, a farmer, or a young pharaoh, read aloud so the child meets the age through a story",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A beautifully illustrated living book about ancient Egypt, written with knowledge and wonder, never a dry fact reader",
                ],
                "short_lesson_flow": "Read a single portion of a living book about ancient Egypt aloud, unhurried, and let the child narrate it back in their own words. The child may draw a scene or a map of Egypt into the Book of Centuries. Let the great river, the pyramids, and the people come alive through the story, not through a list of facts. Stop while interest is high.",
                "narration_prompt": "Tell me the part of the Egypt story we just heard. What was life like along the Nile?",
                "real_world_objects": [
                    "A living book about ancient Egypt, returned to portion by portion",
                    "A Book of Centuries for the child's drawn map and scenes of Egypt",
                    "Pictures of real Egyptian artifacts, the pyramids, hieroglyphics, a museum visit if one is near",
                ],
                "nature_connection": "Consider the Nile as a river of nature study: its yearly flood, the seasons of rainfall far upstream, the green farmland against the desert, the way a whole people lived by the rhythm of one river.",
                "habit_focus": "The habit of attention: hearing the story of Egypt closely enough to tell it back as a living tale, not a string of facts.",
            },
            "montessori": {
                "prepared_materials": [
                    "An Egypt folder in the continent collection, with photographs and fact cards",
                    "A map of Egypt and the Nile to label",
                    "Materials for building a pyramid and a hieroglyphic stamp set",
                    "The fundamental needs of humans chart applied to ancient Egypt",
                ],
                "presentation": {
                    "three_period_lesson": "With the Egypt fact cards: this is a pharaoh, the ruler of Egypt; show me the pharaoh; who is this?",
                    "steps": [
                        "The child explores the Egypt folder, its photographs and fact cards, and locates Egypt and the Nile on the map",
                        "The child examines ancient Egypt through the fundamental needs of humans, how the Egyptians fed, housed, governed, and clothed themselves",
                        "The child builds a pyramid, tries the hieroglyphic stamps, and narrates the story of Egypt",
                    ],
                },
                "control_of_error": "The fact cards and the map carry their own control, matching and locating in one true way, and the fundamental needs framework is the control for understanding: an account of Egypt that leaves out food, shelter, or government is felt to be incomplete.",
                "abstraction_pathway": "From handling the concrete Egypt folder, the map, and the pyramid model, to studying Egypt through the fundamental needs of humans, toward narrating the whole civilization and its place in history without the materials.",
                "extensions": [
                    "Compare how Egypt met the fundamental needs of humans with how another civilization met them",
                    "Investigate the work of the scribe and the discovery of Tutankhamun's tomb",
                    "Place Egypt's three-thousand-year span on the long timeline",
                ],
                "observation_focus": "Watch for the child connecting every part of Egyptian life back to the gift of the Nile, and narrating Egypt as a connected story rather than scattered facts.",
            },
            "unschooling": {
                "invitations": [
                    "Keep richly illustrated books about ancient Egypt within reach",
                    "Leave out materials for building pyramids and trying hieroglyphics",
                    "Have documentaries about Egypt, the pyramids, and the pharaohs available",
                ],
                "real_world_contexts": [
                    "Visiting a museum with Egyptian artifacts, mummies, statues, jewelry",
                    "Watching a documentary about the pyramids or the discovery of a tomb",
                    "Building a pyramid or writing a name in hieroglyphics for the fun of it",
                    "Following a child's fascination with mummies, pharaohs, or pyramids wherever it leads",
                ],
                "conversation_starters": [
                    "The Nile flooded every year and the Egyptians were glad of it, why would a flood be good news?",
                    "Why do you think the Egyptians spent twenty years building one pyramid?",
                    "If you lived in ancient Egypt, would you rather be a pharaoh, a scribe, or a farmer?",
                ],
                "resource_bank": [
                    "Illustrated books and documentaries about ancient Egypt",
                    "Materials for pyramid-building and hieroglyphic writing",
                    "Museums with Egyptian collections",
                ],
                "parent_role": "Follow the child's fascination with ancient Egypt, the mummies, the pyramids, the pharaohs, into books, documentaries, and museums, and wonder aloud at how a whole civilization lived by one river. Let real artifacts and vivid stories, rather than a worksheet, bring Egypt to life.",
                "observation_documentation": "Over time, note whether the child can narrate the story of ancient Egypt, explain the gift of the Nile, picture daily life there, and place Egypt in the ancient world. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Hieroglyphics are a writing system — compare to our alphabet. Reading about Egypt builds vocabulary (pharaoh, pyramid, hieroglyphics).",
            "math": "Pyramids required geometry and measurement. Egyptians used a base-10 number system. Calendar math: 365-day year.",
            "science": "The Nile flood cycle is science: seasonal rainfall in the mountains causes downstream flooding. Mummification involves chemistry.",
        },
    },
    "hf-04": {
        "enriched": True,
        "learning_objectives": [
            "Narrate the story of ancient Mesopotamia including the Tigris and Euphrates rivers, Sumer, and Babylon",
            "Explain what cuneiform is and why the invention of writing changed history",
            "Describe Hammurabi's Code and why having written laws was revolutionary",
            "Compare Mesopotamian civilization to ancient Egypt on at least 3 characteristics",
        ],
        "teaching_guidance": {
            "introduction": "Mesopotamia means 'the land between the rivers' — the Tigris and the Euphrates. This is where civilization arguably began: the first cities, the first writing (cuneiform), the first written laws (Hammurabi's Code), and the first schools. Unlike Egypt's predictable Nile, the Tigris and Euphrates flooded unpredictably, making life harder and forcing people to build irrigation canals and work together. This cooperation built the world's first complex societies.",
            "scaffolding_sequence": [
                "Show the Tigris and Euphrates on a map. The land between them (modern Iraq) is called Mesopotamia.",
                "Tell the story of Sumer: the first cities, the first wheel, the first plow. These were inventors.",
                "Introduce cuneiform: wedge-shaped writing pressed into wet clay tablets. Demonstrate by pressing shapes into clay or playdough.",
                "Tell the story of Hammurabi's Code: a king who wrote down 282 laws so everyone knew the rules. 'If a man breaks another man's bone, his bone shall be broken.' Discuss whether this is fair.",
                "Compare unpredictable Mesopotamian floods to Egypt's predictable floods — how did this difference affect each civilization?",
                "Introduce ziggurats: massive temple-towers in every Mesopotamian city. Compare to pyramids.",
                "Compare Egypt and Mesopotamia on a chart: rivers, writing, buildings, government, farming",
                "The child narrates the Mesopotamia story from memory, placing it on the timeline",
            ],
            "socratic_questions": [
                "The Tigris and Euphrates flooded unpredictably, unlike the Nile. How would unpredictable floods change how you farmed?",
                "Hammurabi wrote all his laws on a big stone pillar. Why was it important that laws were written down where everyone could see them?",
                "Cuneiform was pressed into wet clay tablets. What happens to clay when it dries? Why is that useful for keeping records?",
                "If you could make one law for your family, what would it be? How would you make sure everyone knew about it?",
            ],
            "practice_activities": [
                "Cuneiform writing: press wedge-shaped marks into a flattened ball of clay or playdough using a craft stick — experience what scribes did",
                "Hammurabi's Code discussion: read a few of the simpler laws and discuss whether they are fair. Write 3 family rules in the style of Hammurabi.",
                "Egypt vs Mesopotamia comparison chart: draw two columns and compare rivers, buildings, writing, and government",
                "Map drawing: draw the Tigris and Euphrates rivers with Mesopotamia between them. Label Sumer and Babylon.",
            ],
            "real_world_connections": [
                "Written laws still matter: every country has a constitution or legal code, just like Hammurabi's Code was the first.",
                "The wheel was invented in Mesopotamia: every car, bicycle, and skateboard uses this ancient invention",
                "Schools began in Mesopotamia: young boys went to scribe school to learn cuneiform. Education has been valued for 5,000 years.",
                "Iraq today sits where Mesopotamia was — the ancient ruins are still there beneath modern cities",
            ],
            "common_misconceptions": [
                "Thinking Mesopotamia is one country — it was actually many city-states (like Sumer, Babylon, Assyria) in the same region, often fighting each other",
                "Believing cuneiform is like our alphabet — cuneiform symbols represent syllables and whole words, not individual letters",
                "Thinking Hammurabi's Code was perfectly fair by modern standards — some laws were harsh and unequal (different punishments for rich and poor). Discuss this honestly.",
                "Confusing pyramids (Egypt) with ziggurats (Mesopotamia) — both are large structures, but pyramids were tombs and ziggurats were temples",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Narrates Mesopotamia covering rivers, Sumer, cuneiform, Hammurabi's Code, and ziggurats",
                "Explains why written laws and writing were revolutionary inventions",
                "Compares Egypt and Mesopotamia on 3+ characteristics",
            ],
            "proficiency_indicators": [
                "Narrates several facts about Mesopotamia but may not connect them",
                "Compares Egypt and Mesopotamia on 1-2 characteristics",
            ],
            "developing_indicators": [
                "Knows Mesopotamia is 'between rivers' but cannot narrate the civilization's story",
                "Cannot compare Mesopotamia to Egypt without help",
            ],
            "assessment_methods": ["oral narration", "comparison chart", "map drawing"],
            "sample_assessment_prompts": [
                "Tell me the story of ancient Mesopotamia. Include the rivers, writing, laws, and buildings.",
                "Why was Hammurabi's Code important? What did it do that had never been done before?",
                "How was Mesopotamia different from Egypt?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What does 'Mesopotamia' mean?",
                "expected_type": "multiple_choice",
                "options": ["Land of the pharaohs", "The land between the rivers", "The great desert", "City of gods"],
                "correct_answer": "The land between the rivers",
                "hints": ["The name refers to two rivers. The land is BETWEEN them."],
                "explanation": "Mesopotamia means 'the land between the rivers' — the Tigris and Euphrates rivers. This area is in modern-day Iraq.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What was cuneiform?",
                "expected_type": "multiple_choice",
                "options": [
                    "A type of food",
                    "A weapon",
                    "A writing system using wedge-shaped marks",
                    "A kind of building",
                ],
                "correct_answer": "A writing system using wedge-shaped marks",
                "hints": ["It was pressed into clay tablets. It was used to record things."],
                "explanation": "Cuneiform was the world's first writing system. Scribes pressed wedge-shaped marks into wet clay tablets to record laws, stories, and business transactions.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Why was Hammurabi's Code so important?",
                "expected_type": "text",
                "hints": ["Think about what happens when there are NO written rules. How do people know what's fair?"],
                "explanation": "Hammurabi's Code was important because it was one of the first written sets of laws. When laws are written down, everyone knows the rules and can see if they are being applied fairly. Before this, rules were based on whoever was most powerful.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: Pyramids and ziggurats served the same purpose.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["One was a tomb. The other was a temple. What's the difference?"],
                "explanation": "False. Pyramids were tombs for pharaohs (Egypt). Ziggurats were temples for worshiping gods (Mesopotamia). They look somewhat similar but served very different purposes.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Compare ancient Egypt and Mesopotamia. Name two ways they were alike and two ways they were different.",
                "expected_type": "text",
                "hints": ["Think about: rivers, writing, buildings, government, farming."],
                "explanation": "Alike: both developed near rivers, both invented writing. Different: Egypt had one long river (Nile) with predictable floods; Mesopotamia had two rivers with unpredictable floods. Egypt built pyramids (tombs); Mesopotamia built ziggurats (temples). Egypt had pharaohs ruling the whole land; Mesopotamia had many separate city-states.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Narrate the story of ancient Mesopotamia.",
                "type": "open_response",
                "target_concept": "mesopotamia_narration",
                "rubric": "Mastery: covers rivers, Sumer, cuneiform, Hammurabi, and ziggurats. Proficient: covers 3 topics. Developing: 1-2 facts only.",
            },
            {
                "prompt": "Make your own cuneiform tablet and write a message.",
                "type": "open_response",
                "target_concept": "cuneiform_experience",
                "rubric": "Mastery: creates tablet with recognizable marks and explains the concept. Proficient: creates tablet. Developing: needs significant help.",
            },
        ],
        "resource_guidance": {
            "required": ["map of the Middle East", "clay or playdough for cuneiform activity"],
            "recommended": ["living books about Mesopotamia", "pictures of ziggurats and cuneiform tablets"],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 20, "assessment": 10},
        "accommodations": {
            "dyslexia": "Read all content aloud. Cuneiform clay activity is tactile and requires no reading. Use pictures of real artifacts. Oral narration rather than written responses.",
            "adhd": "Cuneiform clay pressing is highly engaging. Act out Hammurabi announcing his laws. Build a ziggurat with blocks. 15-20 minute sessions.",
            "gifted": "Read actual translated excerpts from Hammurabi's Code and debate fairness. Compare Mesopotamian and Egyptian number systems. Research the Epic of Gilgamesh as one of the first stories ever written.",
            "visual_learner": "Photographs of cuneiform tablets and ziggurat ruins. Map drawing. Comparison charts with illustrations.",
            "kinesthetic_learner": "Clay cuneiform writing. Ziggurat building with blocks. Act out Mesopotamian daily life.",
            "auditory_learner": "Listen to the Epic of Gilgamesh retold. Discuss Hammurabi's laws as a conversation. Oral comparisons between civilizations.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Mesopotamia means the land between the rivers, the Tigris and the Euphrates. Here, many hold, civilization began: the first cities of Sumer, the first writing in cuneiform, the first written laws in Hammurabi's Code. The rivers flooded unpredictably, so the people built irrigation canals and learned to work together. Today we narrate the story of Mesopotamia, learn what cuneiform was and why writing changed history, learn Hammurabi's Code and why written law was revolutionary, and compare Mesopotamia to Egypt.",
                "gradual_release": {
                    "i_do": "Tell the story of Mesopotamia in order: the two rivers and their hard floods, the first cities of Sumer, cuneiform pressed into wet clay, Hammurabi's two hundred and eighty-two written laws, the ziggurats. Think aloud about why writing things down changes everything, and compare Mesopotamia point by point with Egypt.",
                    "we_do": "Retell the story of Mesopotamia together, press cuneiform marks into clay, talk through why written law mattered, and fill a chart comparing Mesopotamia and Egypt.",
                    "you_do": "Child narrates the story of Mesopotamia, explains cuneiform and why writing changed history, describes Hammurabi's Code, and compares Mesopotamia to Egypt on three characteristics.",
                },
                "guided_practice": [
                    "Retell the story of Mesopotamia: the rivers, Sumer, cuneiform, Hammurabi's Code, ziggurats",
                    "Press cuneiform marks into clay and explain why writing mattered",
                    "Compare Mesopotamia and Egypt on a chart of their characteristics",
                ],
                "independent_practice": [
                    "Narrate the full story of Mesopotamia from memory",
                    "Write a comparison of Mesopotamia and Egypt, alike and different",
                ],
                "mastery_check": [
                    "Narrate Mesopotamia including the rivers, Sumer, Babylon, cuneiform, and ziggurats",
                    "Explain what cuneiform was, and why writing and written law changed history",
                    "Compare Mesopotamian civilization to Egypt on at least three characteristics",
                ],
                "spiral_review": [
                    "Revisit the story of Egypt, set beside Mesopotamia, so the two are held and compared",
                ],
            },
            "classical": {
                "narrative_introduction": "In the land between two rivers, the Tigris and the Euphrates, civilization took some of its first and greatest steps. Here rose the cities of Sumer, and here a people pressed the first writing, cuneiform, into wet clay, and here a king named Hammurabi set down his laws in writing for all to see. Writing made memory permanent; written law made justice public. Mesopotamia gave the world both.",
                "memory_work": {
                    "chants": [
                        "Chant the land between the rivers: the Tigris and the Euphrates, and the cities of Sumer between them",
                        "Chant the gifts of Mesopotamia: the wheel, the first writing, the first written laws",
                    ],
                    "recitations": [
                        "Recite that cuneiform was the first writing, pressed into clay, and that Hammurabi was first to set the laws in writing for all to see",
                    ],
                },
                "copywork": [
                    "Copy a simple law in the manner of Hammurabi's Code, and the words cuneiform, ziggurat, Sumer, and Babylon",
                ],
                "recitation_routine": "Begin each lesson by reciting the gifts of Mesopotamia and narrating yesterday's portion of the story before adding the next.",
                "history_integration": "Place Mesopotamia on the chronological spine beside Egypt, among the very first river valley civilizations, and mark it as the point where writing itself begins, the invention that turns the unrecorded past into history that can be read.",
                "read_aloud_suggestions": [
                    "A living account of life in Sumer or Babylon, the scribe at the clay tablet, the king and his laws, read aloud for narration",
                    "The Epic of Gilgamesh retold for children, one of the oldest stories ever written, read aloud",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A beautifully illustrated living book about ancient Mesopotamia, written with knowledge and wonder, never a dry fact reader",
                ],
                "short_lesson_flow": "Read a portion of a living book about Mesopotamia aloud, unhurried, and let the child narrate it back. Then let the child press cuneiform marks into a flattened ball of clay, feeling for themselves what a Sumerian scribe did. The map and a Book of Centuries entry may follow. Let the story and the clay, not a list of facts, teach Mesopotamia.",
                "narration_prompt": "Tell me the part of the Mesopotamia story we just heard. What was it like to be a scribe pressing words into clay?",
                "real_world_objects": [
                    "A living book about ancient Mesopotamia",
                    "Clay or playdough for pressing cuneiform marks by hand",
                    "A Book of Centuries and a map of the Tigris and Euphrates",
                    "Pictures of real cuneiform tablets and ziggurat ruins",
                ],
                "nature_connection": "Consider the two rivers as nature itself shaping a people: their unpredictable floods, so unlike the gentle Nile, forced the Mesopotamians to read the water, dig canals, and work together against nature's uncertainty.",
                "habit_focus": "The habit of attention: hearing the story of Mesopotamia closely enough to narrate it, and pressing the clay carefully enough to feel the scribe's craft.",
            },
            "montessori": {
                "prepared_materials": [
                    "A Mesopotamia folder in the continent collection, with photographs and fact cards",
                    "Clay tablets and a stylus for cuneiform work",
                    "A map of the Tigris and Euphrates and materials for a ziggurat model",
                    "The fundamental needs of humans chart applied to Mesopotamia",
                ],
                "presentation": {
                    "three_period_lesson": "With the fact cards: this is cuneiform, the first writing, pressed into clay; show me cuneiform; what is this writing called?",
                    "steps": [
                        "The child explores the Mesopotamia folder and locates the two rivers on the map",
                        "The child presses cuneiform into a clay tablet, the hands learning the scribe's work",
                        "The child studies Mesopotamia through the fundamental needs of humans and narrates its story",
                    ],
                },
                "control_of_error": "The clay tablet is a vivid control: marks pressed carelessly cannot be read back, so the child sees the scribe's need for care; the fact cards and map confirm the rest in one true way.",
                "abstraction_pathway": "From pressing real cuneiform into clay and handling the concrete folder, to studying Mesopotamia through the fundamental needs of humans, toward narrating the civilization and grasping why writing and written law changed history.",
                "extensions": [
                    "Compare how Mesopotamia and Egypt each met the fundamental needs of humans",
                    "Read and weigh a few of Hammurabi's laws",
                    "Investigate the wheel, the canal, and the other Sumerian inventions",
                ],
                "observation_focus": "Watch for the child grasping that writing made records permanent, and that written law made the rules public and the same for all to see.",
            },
            "unschooling": {
                "invitations": [
                    "Keep illustrated books about ancient Mesopotamia within reach",
                    "Leave out clay and a stylus for pressing cuneiform whenever the child wishes",
                    "Have documentaries and retold tales like the Epic of Gilgamesh available",
                ],
                "real_world_contexts": [
                    "Pressing marks into clay and discovering how hard early writing was",
                    "Visiting a museum with cuneiform tablets or Mesopotamian artifacts",
                    "Noticing the written rules and laws all around in daily life",
                    "Wondering at the wheel, a Mesopotamian invention, on every car and bike",
                ],
                "conversation_starters": [
                    "The Mesopotamians wrote their laws on a great stone for everyone to see, why did that matter?",
                    "What happens when there are no written rules, and whoever is strongest decides?",
                    "If you could make one written rule for our family, what would it be?",
                ],
                "resource_bank": [
                    "Illustrated books and documentaries about Mesopotamia",
                    "Clay and a stylus for cuneiform play",
                    "Museums with Mesopotamian artifacts, and retellings of the Epic of Gilgamesh",
                ],
                "parent_role": "Follow the child's curiosity about the land between the rivers into books, clay, and museums, and wonder aloud at why writing and written law were such powerful inventions. Let real clay tablets, real artifacts, and vivid stories, rather than a worksheet, bring Mesopotamia to life.",
                "observation_documentation": "Over time, note whether the child can narrate the story of Mesopotamia, explain why writing and written law mattered, and compare Mesopotamia with Egypt. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Cuneiform was one of the first writing systems — compare to hieroglyphics and our alphabet",
            "math": "Mesopotamians used a base-60 number system — that's why we have 60 seconds in a minute and 360 degrees in a circle",
            "science": "Irrigation canals were engineering: Mesopotamians controlled water flow through channels they dug by hand",
        },
    },
    "hf-05": {
        "enriched": True,
        "learning_objectives": [
            "Narrate key facts about ancient China including the Yellow River, the Great Wall, and early dynasties",
            "Name the four great inventions of ancient China: paper, printing, compass, gunpowder",
            "Describe Confucius's main teaching about respect, order, and duty",
            "Locate China and the Yellow River on a map",
        ],
        "teaching_guidance": {
            "introduction": "Ancient China is the oldest civilization that has continued without interruption to the present day. It began along the Yellow River (also called the Huang He), where farmers grew millet and rice in the fertile flood plains. China gave the world paper, printing, the compass, and gunpowder — four inventions that changed everything. And a teacher named Confucius taught lessons about respect, honesty, and duty that shaped Chinese culture for over 2,500 years and still influence it today.",
            "scaffolding_sequence": [
                "Show China on a map and trace the Yellow River. Explain that this river earned its name from the yellowish silt it carries.",
                "Tell the story of the first Chinese farmers along the Yellow River — similar to Egypt and Mesopotamia but on the other side of the world",
                "Introduce the concept of dynasties: powerful families that ruled China in succession. Each dynasty rose, ruled, and eventually fell.",
                "Tell the story of the Great Wall: built over centuries to protect China from northern invaders. It's so long it can be seen from space. (It took hundreds of years and millions of workers.)",
                "Introduce the four great inventions one by one: paper (writing on!), printing (copying books!), compass (navigation!), gunpowder (fireworks first, then weapons)",
                "Tell the story of Confucius: a teacher who said children should respect parents, people should be honest, and everyone has a duty to their family and community",
                "Place ancient China on the timeline alongside Egypt and Mesopotamia — they existed at roughly the same time!",
                "The child narrates what they know about ancient China and adds it to their timeline or Book of Centuries",
            ],
            "socratic_questions": [
                "China invented paper. Before paper, people wrote on clay, stone, or animal skins. How did paper change things?",
                "The Great Wall is thousands of miles long. Why would an entire civilization spend centuries building one wall?",
                "Confucius said children should respect and obey their parents. Do you agree? Why or why not?",
                "China, Egypt, and Mesopotamia all began around the same time but on different continents. Why do you think that happened?",
            ],
            "practice_activities": [
                "Paper making: make simple paper from torn-up newspaper and water (papier-mache technique) to experience the invention of paper",
                "Great Wall building: use blocks, LEGOs, or cardboard boxes to build a section of the Great Wall, discussing why it was built",
                "Chinese brush painting: use water and a paintbrush on dark construction paper to practice the style of Chinese calligraphy",
                "Compass exploration: use a real compass outdoors and discuss how this Chinese invention helped explorers navigate the world",
            ],
            "real_world_connections": [
                "Paper is everywhere: books, packaging, money. China invented it around 100 AD, and it changed how humans store knowledge.",
                "Fireworks were invented in China using gunpowder. Every Fourth of July display connects to ancient Chinese chemistry.",
                "The compass in your phone or car traces its ancestry to ancient Chinese lodestones that pointed north",
                "Chinese food, martial arts, and New Year celebrations are part of a cultural tradition thousands of years old",
            ],
            "common_misconceptions": [
                "Thinking the Great Wall was built all at once — it was built, rebuilt, and extended over about 2,000 years by many different dynasties",
                "Believing gunpowder was invented for war — it was originally used for fireworks and only later adapted for weapons",
                "Thinking ancient China was isolated — Chinese silk was traded along the Silk Road to Rome and the Middle East",
                "Confusing Confucius's teachings with a religion — Confucianism is more of a philosophy about how to live a good life than a religion with gods and worship",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Narrates ancient China covering the Yellow River, Great Wall, four inventions, and Confucius",
                "Names all four great inventions and explains why each mattered",
                "Locates China and the Yellow River on a map",
            ],
            "proficiency_indicators": [
                "Narrates several facts about China but may not remember all four inventions",
                "Locates China on a map but not the Yellow River specifically",
            ],
            "developing_indicators": [
                "Knows about the Great Wall but cannot narrate a connected story of Chinese civilization",
                "Cannot name the four inventions",
            ],
            "assessment_methods": ["oral narration", "map labeling", "invention identification"],
            "sample_assessment_prompts": [
                "Tell me the story of ancient China. Include the river, the Wall, the inventions, and Confucius.",
                "Name the four great inventions of China and tell me why each one was important.",
                "Show me where China is on the map. Where is the Yellow River?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which of these was NOT one of China's four great inventions?",
                "expected_type": "multiple_choice",
                "options": ["Paper", "Compass", "Telescope", "Gunpowder"],
                "correct_answer": "Telescope",
                "hints": ["The four inventions are: paper, printing, compass, and gunpowder."],
                "explanation": "The telescope was NOT one of China's four great inventions. The four are paper, printing, the compass, and gunpowder. The telescope was invented in Europe.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What river was the cradle of Chinese civilization?",
                "expected_type": "multiple_choice",
                "options": ["Nile", "Amazon", "Yellow River", "Mississippi"],
                "correct_answer": "Yellow River",
                "hints": ["It's named after the color of the silt it carries."],
                "explanation": "The Yellow River (Huang He) is where Chinese civilization began, just as the Nile was for Egypt and the Tigris-Euphrates for Mesopotamia.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What did Confucius teach?",
                "expected_type": "text",
                "hints": ["Think about how people should treat each other: parents, children, rulers, and subjects."],
                "explanation": "Confucius taught that people should respect their parents and elders, be honest, fulfill their duties to family and community, and that rulers should govern fairly. His ideas shaped Chinese culture for over 2,500 years.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: The Great Wall of China was built in just one year.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["Think about how long the Wall is — thousands of miles. Could that be built quickly?"],
                "explanation": "False. The Great Wall was built over about 2,000 years by many different dynasties. It was continuously extended and rebuilt to protect China's northern border.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Pick one of China's four great inventions and explain how it changed the world.",
                "expected_type": "text",
                "hints": [
                    "Choose paper, printing, compass, or gunpowder. Think about what the world was like BEFORE this invention."
                ],
                "explanation": "Example for paper: Before paper, people wrote on clay tablets, animal skins, or bamboo strips — all heavy and expensive. Paper made writing cheap and portable, which meant more people could learn to read and write, and knowledge could spread faster.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Narrate the story of ancient China in your own words.",
                "type": "open_response",
                "target_concept": "china_narration",
                "rubric": "Mastery: covers river, Great Wall, inventions, Confucius. Proficient: covers 2-3 topics. Developing: 1-2 facts.",
            },
            {
                "prompt": "Name China's four great inventions.",
                "type": "open_response",
                "target_concept": "four_inventions",
                "rubric": "Mastery: names all 4 and explains importance. Proficient: names 3-4. Developing: names 1-2.",
            },
        ],
        "resource_guidance": {
            "required": ["world map or globe", "pictures of the Great Wall, Chinese inventions"],
            "recommended": ["living books about ancient China", "compass for hands-on exploration"],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 20, "assessment": 10},
        "accommodations": {
            "dyslexia": "Read all content aloud. Use documentaries about China. Hands-on: build the Great Wall, make paper, use a compass. Oral narration rather than written.",
            "adhd": "Highly hands-on: build, paint, explore with compass. Each session focuses on one subtopic (15 minutes). Chinese martial arts movements as a brain break.",
            "gifted": "Research the Silk Road and how Chinese inventions spread to Europe. Compare Chinese and Roman civilizations (they existed at the same time!). Read about Chinese mythology.",
            "visual_learner": "Photographs of the Great Wall, terracotta warriors, Chinese calligraphy. Map drawing with colors.",
            "kinesthetic_learner": "Build the Great Wall. Make paper. Practice calligraphy with a brush. Use a compass on a nature walk.",
            "auditory_learner": "Listen to stories about Confucius and ancient Chinese legends. Discuss inventions and their impact.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Ancient China is the oldest civilization that has continued unbroken to the present day. It began along the Yellow River, was ruled by a succession of dynasties, and built the Great Wall over centuries to guard its northern border. China gave the world four great inventions, paper, printing, the compass, and gunpowder, and a teacher named Confucius whose lessons on respect, order, and duty shaped the culture for over two thousand years. Today we narrate ancient China, name the four inventions, describe Confucius's teaching, and locate China and the Yellow River.",
                "gradual_release": {
                    "i_do": "Tell the story of ancient China in order: the Yellow River and its first farmers, the dynasties that rose and fell, the Great Wall built over centuries, the four great inventions and what each changed, and Confucius and his teaching on respect and duty. Point to China and the Yellow River on the map.",
                    "we_do": "Retell the story of ancient China together, name and explain the four great inventions, and locate China and the Yellow River on the map.",
                    "you_do": "Child narrates ancient China, names the four great inventions and why each mattered, describes Confucius's teaching, and locates China and the Yellow River.",
                },
                "guided_practice": [
                    "Retell the story of ancient China: the Yellow River, the dynasties, the Great Wall",
                    "Name the four great inventions and explain why each one mattered",
                    "Locate China and the Yellow River on a map",
                ],
                "independent_practice": [
                    "Narrate the full story of ancient China from memory",
                    "Explain how one of the four great inventions changed the world",
                ],
                "mastery_check": [
                    "Narrate ancient China including the Yellow River, the Great Wall, and the dynasties",
                    "Name the four great inventions of ancient China and why each mattered",
                    "Describe Confucius's teaching and locate China and the Yellow River on a map",
                ],
                "spiral_review": [
                    "Revisit the other river valley civilizations, and set ancient China beside them on the timeline",
                ],
            },
            "classical": {
                "narrative_introduction": "Ancient China is the oldest of the living civilizations, unbroken from its beginning on the Yellow River to the present day. Ruled by dynasties that rose and fell in turn, it guarded itself with the Great Wall, raised over centuries of labor. It gave the world four inventions that changed all of history, paper and printing, the compass and gunpowder, and a teacher, Confucius, whose words on respect and duty have guided a people for more than two thousand years.",
                "memory_work": {
                    "chants": [
                        "Chant the four great inventions of China: paper, printing, the compass, and gunpowder",
                        "Chant the way of Confucius: respect your parents, be honest, and do your duty to family and community",
                    ],
                    "recitations": [
                        "Recite that ancient China began on the Yellow River, was ruled by dynasties, and is the oldest civilization living still",
                    ],
                },
                "copywork": [
                    "Copy the four great inventions of China, and a short saying of Confucius on respect or honesty",
                ],
                "recitation_routine": "Begin each lesson by reciting the four great inventions and a saying of Confucius before narrating the next portion of the story.",
                "history_integration": "Place ancient China on the chronological spine beside Egypt, Mesopotamia, and India, all begun at the dawn of civilization, and mark that while those others ended, China endures, its dynasties an unbroken thread along the spine to the present day.",
                "read_aloud_suggestions": [
                    "A living account of life in ancient China, the farmer by the Yellow River, the builder of the Wall, the scholar of Confucius, read aloud for narration",
                    "A retelling of an ancient Chinese legend or a story of Confucius, read aloud",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A beautifully illustrated living book about ancient China, written with knowledge and wonder, never a dry fact reader",
                ],
                "short_lesson_flow": "Read a portion of a living book about ancient China aloud, unhurried, and let the child narrate it back. The child may try Chinese brush painting, or draw the map and the Great Wall into the Book of Centuries. Let the river, the Wall, the inventions, and Confucius come alive through the story. Stop while interest holds.",
                "narration_prompt": "Tell me the part of the China story we just heard. Which of the inventions do you think changed the world the most?",
                "real_world_objects": [
                    "A living book about ancient China",
                    "A brush and water for trying Chinese calligraphy",
                    "A real compass, a Chinese invention, to use",
                    "A Book of Centuries and a map for the child's drawn work",
                ],
                "nature_connection": "Consider the Yellow River, named for the yellow silt it carries, and how, like the Nile and the Tigris, a river of nature gave a people their farmland and their beginning.",
                "habit_focus": "The habit of attention: hearing the story of ancient China closely enough to narrate it, and forming, with Confucius, the habits of respect and duty.",
            },
            "montessori": {
                "prepared_materials": [
                    "A China folder in the continent collection, with photographs and fact cards",
                    "A real compass for practical geography",
                    "Materials for paper-making and Chinese brush painting",
                    "The fundamental needs of humans chart applied to ancient China",
                ],
                "presentation": {
                    "three_period_lesson": "With the invention cards: this is paper, a great invention of China; show me paper; which of the four great inventions is this?",
                    "steps": [
                        "The child explores the China folder and locates China and the Yellow River on the map",
                        "The child meets the four great inventions, making paper, using the compass, by hand",
                        "The child studies ancient China through the fundamental needs of humans and narrates its story",
                    ],
                },
                "control_of_error": "The compass is a vivid self-checking control, always finding the north for the child to verify; the fact cards and map confirm the rest, matching and locating in one true way.",
                "abstraction_pathway": "From handling the concrete China folder and working the real inventions, the paper, the compass, to studying China through the fundamental needs of humans, toward narrating the civilization and its long, unbroken history.",
                "extensions": [
                    "Trace how the four inventions spread along the Silk Road to the wider world",
                    "Compare how ancient China met the fundamental needs of humans with another civilization",
                    "Investigate the dynasties and the long building of the Great Wall",
                ],
                "observation_focus": "Watch for the child grasping why each invention mattered, and connecting Confucius's teaching of respect and duty to how a society holds together.",
            },
            "unschooling": {
                "invitations": [
                    "Keep illustrated books about ancient China within reach",
                    "Leave out a compass, brushes, and paper-making materials to explore",
                    "Have documentaries about the Great Wall, the dynasties, and the inventions available",
                ],
                "real_world_contexts": [
                    "Using a compass and discovering how this Chinese invention finds the north",
                    "Noticing paper everywhere, in every book and box, a Chinese invention",
                    "Watching fireworks and connecting them to Chinese gunpowder",
                    "Sharing a meal of Chinese food, or marking the Chinese New Year, living traditions thousands of years old",
                ],
                "conversation_starters": [
                    "China invented paper, what did people write on before there was paper?",
                    "Why would a whole civilization spend centuries building one wall?",
                    "Confucius said children should respect their parents, what do you think of that?",
                ],
                "resource_bank": [
                    "Illustrated books and documentaries about ancient China",
                    "A compass, brushes, and paper-making materials",
                    "Chinese food, festivals, and museums with Chinese artifacts",
                ],
                "parent_role": "Follow the child's curiosity about ancient China into books, documentaries, and the inventions themselves, and wonder aloud at how paper, printing, the compass, and gunpowder changed the world. Let real inventions, real stories, and living Chinese traditions, rather than a worksheet, bring ancient China to life.",
                "observation_documentation": "Over time, note whether the child can narrate the story of ancient China, name the four great inventions, describe Confucius's teaching, and find China on a map. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Chinese invented paper and printing — the two technologies that make books possible",
            "math": "Chinese mathematicians contributed to number theory and the abacus (one of the first calculators)",
            "science": "Gunpowder is chemistry. The compass uses magnetism. Paper-making is a manufacturing process. All are science.",
        },
    },
    "hf-06": {
        "enriched": True,
        "learning_objectives": [
            "Narrate the story of the Indus Valley civilization and its advanced cities",
            "Retell a Hindu myth and the story of the Buddha's life",
            "Explain India's contribution of the concept of zero and the decimal number system",
            "Locate the Indus River and India on a map",
        ],
        "teaching_guidance": {
            "introduction": "Ancient India produced one of the most mysterious civilizations in history. The cities of Mohenjo-daro and Harappa in the Indus Valley were remarkably advanced: grid-planned streets, indoor plumbing, and public baths — 4,500 years ago! After this civilization faded, India became the birthplace of two great religions (Hinduism and Buddhism), invented the concept of zero (without which modern mathematics would be impossible), and developed a rich tradition of stories, art, and philosophy that continues to this day.",
            "scaffolding_sequence": [
                "Show India and the Indus River on a map. The Indus Valley is in what is now Pakistan and northwestern India.",
                "Tell the story of Mohenjo-daro: a city with straight streets, brick houses, indoor bathrooms, and a great public bath — all built 4,500 years ago",
                "Introduce Hinduism through its stories: the great epics (Ramayana, Mahabharata) are full of heroes, gods, and adventures",
                "Tell the story of Siddhartha Gautama who became the Buddha: a prince who left his palace to understand suffering and found a path to peace",
                "Introduce the caste system as a way ancient Indian society was organized — acknowledge its complexity and unfairness",
                "Celebrate India's gift of zero: before zero, mathematics could not advance. The decimal system (1-10, then repeat) came from India too.",
                "Place ancient India on the timeline alongside other civilizations studied",
                "The child narrates ancient India from memory, covering cities, religion, and mathematics",
            ],
            "socratic_questions": [
                "Mohenjo-daro had indoor plumbing 4,500 years ago. Many modern cities didn't have plumbing until 200 years ago. What does that tell you about how advanced this civilization was?",
                "The Buddha was a rich prince who gave up everything to help others. What would make someone leave comfort for hardship?",
                "Before zero was invented, how would you write the number 105? Why is zero so important?",
                "Hinduism has many gods, while Buddhism focuses on a path to peace. How can two very different ideas come from the same place?",
            ],
            "practice_activities": [
                "Build Mohenjo-daro: use blocks or LEGOs to create a city with grid streets, a great bath, and brick houses",
                "Zero exploration: try doing math problems without the digit zero — how hard is it? This shows why India's invention was so important.",
                "Hindu myth retelling: read a simple version of a Hindu myth (such as Rama and Sita) and the child narrates it back",
                "Map drawing: draw India with the Indus River, and mark where Mohenjo-daro and Harappa were located",
            ],
            "real_world_connections": [
                "Every number you write uses the decimal system invented in India: 0, 1, 2, 3... This is called Hindu-Arabic numerals.",
                "Yoga originated in ancient India and is practiced by millions of people worldwide today",
                "Indian food, festivals (like Diwali), and traditions are celebrated around the world",
                "Buddhism spread from India to China, Japan, and Southeast Asia — it's now one of the world's major religions",
            ],
            "common_misconceptions": [
                "Thinking the Indus Valley civilization was primitive — Mohenjo-daro was MORE advanced than many cities built thousands of years later",
                "Confusing India and Indiana, or India and Indonesia — use the map consistently to build geographic accuracy",
                "Assuming ancient India was just one culture — it was incredibly diverse with many languages, religions, and traditions across a huge subcontinent",
                "Thinking zero is 'nothing' and therefore unimportant — zero is one of the most revolutionary ideas in human history, enabling all modern mathematics and computing",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Narrates ancient India covering Indus Valley cities, Hinduism, Buddhism, and zero",
                "Retells a Hindu myth and the Buddha's story",
                "Explains why zero was such an important invention",
            ],
            "proficiency_indicators": [
                "Narrates 2-3 aspects of ancient India",
                "Can identify India on a map and name one contribution",
            ],
            "developing_indicators": [
                "Knows India is an ancient civilization but cannot narrate its story",
                "Cannot explain the importance of zero",
            ],
            "assessment_methods": ["oral narration", "myth retelling", "map labeling"],
            "sample_assessment_prompts": [
                "Tell me about ancient India. What were the Indus Valley cities like?",
                "Retell the story of the Buddha.",
                "Why is the number zero important? Where was it invented?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which ancient civilization invented the number zero?",
                "expected_type": "multiple_choice",
                "options": ["Egypt", "Greece", "India", "China"],
                "correct_answer": "India",
                "hints": ["This civilization also gave us the decimal number system (0-9)."],
                "explanation": "India invented the concept of zero and the decimal number system. Every number you write uses this Indian invention.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What river was the Indus Valley civilization built near?",
                "expected_type": "text",
                "correct_answer": "the Indus River",
                "hints": ["The civilization is literally named after this river."],
                "explanation": "The Indus Valley civilization was built along the Indus River, in what is now Pakistan and northwestern India.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What made the cities of Mohenjo-daro and Harappa so remarkable for their time?",
                "expected_type": "text",
                "hints": ["Think about the streets, the houses, and the plumbing. How modern were they?"],
                "explanation": "These cities had grid-planned streets, brick houses, indoor plumbing, and public baths — 4,500 years ago. This level of urban planning wouldn't be matched in Europe for thousands of years.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: Buddhism and Hinduism both originated in ancient India.",
                "expected_type": "true_false",
                "correct_answer": "true",
                "hints": ["Both religions began on the Indian subcontinent, though at different times."],
                "explanation": "True. Hinduism is one of the world's oldest religions, developing over thousands of years in India. Buddhism was founded by Siddhartha Gautama (the Buddha) in India around 500 BC.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Tell the story of the Buddha in your own words. Who was he before he became the Buddha? What did he discover?",
                "expected_type": "text",
                "hints": ["He started as a prince. He left his palace. He wanted to understand why people suffer."],
                "explanation": "Siddhartha Gautama was a rich prince sheltered from all suffering. When he left his palace and saw sickness, old age, and death, he gave up his wealth to find an answer to human suffering. After years of searching, he meditated under a Bodhi tree and achieved enlightenment, becoming the Buddha ('the awakened one'). He taught a path to peace through compassion, mindfulness, and letting go of desire.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Narrate the story of ancient India in your own words.",
                "type": "open_response",
                "target_concept": "india_narration",
                "rubric": "Mastery: covers Indus cities, religions, and zero. Proficient: covers 2 topics. Developing: 1 fact only.",
            },
            {
                "prompt": "Why is zero important? Try doing a math problem without it.",
                "type": "open_response",
                "target_concept": "zero_importance",
                "rubric": "Mastery: explains with example. Proficient: says it's important for math. Developing: cannot explain.",
            },
        ],
        "resource_guidance": {
            "required": ["world map or globe", "pictures of Mohenjo-daro and Indian artifacts"],
            "recommended": ["living books about ancient India", "simple Hindu myth collections for children"],
        },
        "time_estimates": {"first_exposure": 25, "practice_session": 20, "assessment": 10},
        "accommodations": {
            "dyslexia": "Read all content aloud. Use documentaries and image-heavy books. Hindu myths make excellent oral storytelling. Zero exploration is a math activity, not a reading one.",
            "adhd": "Build Mohenjo-daro. Act out the Buddha's story. Math games exploring zero. Each subtopic in a separate 15-minute session.",
            "gifted": "Research the Indus Valley script (still undeciphered!). Compare Indian and Western mathematics. Read longer versions of Hindu epics. Explore the spread of Buddhism across Asia.",
            "visual_learner": "Photographs of Indus Valley ruins. Illustrated Hindu myths. Map drawing.",
            "kinesthetic_learner": "Build Indus Valley cities. Practice yoga poses (ancient Indian origin). Use blocks to demonstrate place value with zero.",
            "auditory_learner": "Listen to Hindu myths told as stories. Discuss the Buddha's journey. Verbal math games with zero.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Ancient India holds one of history's most remarkable civilizations. In the Indus Valley, the cities of Mohenjo-daro and Harappa had grid-planned streets, brick houses, and indoor plumbing four and a half thousand years ago. India became the birthplace of Hinduism and Buddhism, and it gave the world the number zero and the decimal system, without which modern mathematics could not exist. Today we narrate the Indus Valley civilization, retell a Hindu myth and the Buddha's story, explain the gift of zero, and locate the Indus River and India.",
                "gradual_release": {
                    "i_do": "Tell the story of ancient India in order: the advanced cities of the Indus Valley with their planned streets and plumbing, the great stories of Hinduism, the prince Siddhartha who became the Buddha, and the invention of zero. Think aloud about why zero matters, and point to India and the Indus River on the map.",
                    "we_do": "Retell the story of ancient India together, retell a Hindu myth and the Buddha's story, and try writing numbers with and without zero to feel its importance.",
                    "you_do": "Child narrates the Indus Valley civilization, retells a Hindu myth and the Buddha's life, explains why zero was important, and locates the Indus River and India.",
                },
                "guided_practice": [
                    "Retell the story of the Indus Valley cities and what made them advanced",
                    "Retell a Hindu myth and the story of the Buddha's life",
                    "Locate India and the Indus River on a map",
                ],
                "independent_practice": [
                    "Narrate the full story of ancient India from memory",
                    "Explain why the invention of zero was so important to mathematics",
                ],
                "mastery_check": [
                    "Narrate the Indus Valley civilization and its advanced cities",
                    "Retell a Hindu myth and the story of the Buddha's life",
                    "Explain India's contribution of zero and the decimal system, and locate India on a map",
                ],
                "spiral_review": [
                    "Revisit the other river valley civilizations, and set ancient India beside them on the timeline",
                ],
            },
            "classical": {
                "narrative_introduction": "Ancient India was a civilization of quiet wonders. In the Indus Valley, the cities of Mohenjo-daro and Harappa were laid out in planned streets, with brick houses and running water, an age before most of the world had dreamed of such order. From this land came two great religions, Hinduism with its vast store of stories, and Buddhism, founded by a prince who sought the end of suffering, and from this land came the number zero, the small sign that made all of mathematics possible.",
                "memory_work": {
                    "chants": [
                        "Chant the gifts of ancient India: the planned cities of the Indus, the great religions, and the number zero",
                        "Chant the marvel of Mohenjo-daro: straight streets, brick houses, and water running indoors, four and a half thousand years ago",
                    ],
                    "recitations": [
                        "Recite that India gave the world the number zero and the decimal system, without which modern mathematics could not stand",
                    ],
                },
                "copywork": [
                    "Copy the contributions of ancient India, and the names Mohenjo-daro, Indus, Hinduism, and Buddhism",
                ],
                "recitation_routine": "Begin each lesson by reciting the gifts of ancient India and narrating yesterday's portion of the story before adding the next.",
                "history_integration": "Place ancient India on the chronological spine among the four river valley civilizations, all begun together, and mark that India's gifts, its religions and its zero, reach down the whole length of the spine to shape the mathematics and the faith of the present day.",
                "read_aloud_suggestions": [
                    "A retelling of a Hindu myth or epic, the Ramayana or a tale of the gods, read aloud for narration",
                    "A living account of the life of the Buddha, the prince who left his palace to seek the end of suffering, read aloud",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A beautifully illustrated living book about ancient India, or a finely told collection of Hindu myths for children, never a dry fact reader",
                ],
                "short_lesson_flow": "Read a Hindu myth or a portion of the Buddha's story aloud, told with wonder, and let the child narrate it back. Another day, read of the planned cities of the Indus Valley. The child may draw a scene or a map into the Book of Centuries. Let the great stories of India, told well, be the lesson. Stop while interest is high.",
                "narration_prompt": "Tell me the story we just heard. What happened to the prince who became the Buddha?",
                "real_world_objects": [
                    "A living book of Hindu myths and a living book about ancient India",
                    "A Book of Centuries and a map for the child's drawn work",
                    "Pictures of the Indus Valley ruins and Indian artifacts",
                ],
                "nature_connection": "Consider the Indus River, like the Nile and the Yellow River, a river of nature that gave a people their farmland, and notice how the Indus cities planned their streets and water with the care of careful observers of the natural world.",
                "habit_focus": "The habit of attention: hearing the great stories of India closely enough to retell them as living tales.",
            },
            "montessori": {
                "prepared_materials": [
                    "An India folder in the continent collection, with photographs and fact cards",
                    "Materials for building Mohenjo-daro with its grid streets",
                    "Number materials for exploring zero and the decimal system",
                    "The fundamental needs of humans chart applied to ancient India",
                ],
                "presentation": {
                    "three_period_lesson": "With the fact cards: this is Mohenjo-daro, a planned city of the Indus Valley; show me Mohenjo-daro; which ancient city is this?",
                    "steps": [
                        "The child explores the India folder and locates India and the Indus River on the map",
                        "The child builds Mohenjo-daro with its grid streets and studies India through the fundamental needs of humans",
                        "The child explores zero and the decimal system with the number materials, and retells a story of India",
                    ],
                },
                "control_of_error": "The number materials are a precise control: a child trying to write or build numbers without zero finds plainly that the system breaks, and the fact cards and map confirm the rest in one true way.",
                "abstraction_pathway": "From handling the concrete India folder, building Mohenjo-daro, and working the number materials, to studying India through the fundamental needs of humans, toward narrating the civilization and grasping the power of its gift of zero.",
                "extensions": [
                    "Trace how the decimal system and zero spread from India to the wider world",
                    "Compare how ancient India met the fundamental needs of humans with another civilization",
                    "Follow the spread of Buddhism from India across Asia",
                ],
                "observation_focus": "Watch for the child grasping how advanced the Indus cities were for their age, and why zero, far from being nothing, made all later mathematics possible.",
            },
            "unschooling": {
                "invitations": [
                    "Keep illustrated books of Hindu myths and books about ancient India within reach",
                    "Leave out blocks for building the planned cities of the Indus Valley",
                    "Have documentaries about ancient India and simple math materials for exploring zero available",
                ],
                "real_world_contexts": [
                    "Hearing and retelling the great Hindu myths as stories",
                    "Noticing that every number written uses the zero and the digits India gave the world",
                    "Trying yoga, which began in ancient India and is practiced everywhere today",
                    "Sharing Indian food, or marking a festival like Diwali, living traditions of an ancient land",
                ],
                "conversation_starters": [
                    "Mohenjo-daro had running water indoors four and a half thousand years ago, what does that tell you about the people who built it?",
                    "The Buddha was a rich prince who gave everything away, what would make someone do that?",
                    "How would you write the number one hundred and five without using zero?",
                ],
                "resource_bank": [
                    "Illustrated Hindu myth collections and books about ancient India",
                    "Documentaries about the Indus Valley and the Buddha",
                    "Indian food, festivals, yoga, and museums with Indian artifacts",
                ],
                "parent_role": "Follow the child's curiosity about ancient India into its great stories, its planned cities, and its gift of zero, and wonder aloud at a people so far ahead of their age. Let vivid myths, real documentaries, and living Indian traditions, rather than a worksheet, bring ancient India to life.",
                "observation_documentation": "Over time, note whether the child can narrate the Indus Valley civilization, retell a Hindu myth and the Buddha's story, explain the importance of zero, and find India on a map. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Hindu myths are rich stories with heroes, villains, and moral lessons — perfect for narration practice",
            "math": "India invented zero and the decimal system — the foundation of ALL modern mathematics",
            "science": "Ancient Indian astronomers mapped the stars. Indian metallurgists created rust-resistant iron pillars that still stand today.",
        },
    },
    "hf-07": {
        "enriched": True,
        "learning_objectives": [
            "Compare Athens and Sparta as two different Greek city-states with different values",
            "Explain what democracy means and how Athens practiced it",
            "Retell at least 3 Greek myths and explain what they taught the Greeks",
            "Describe the Olympic Games and their role in Greek culture",
        ],
        "teaching_guidance": {
            "introduction": "Ancient Greece is where democracy, philosophy, theater, and the Olympic Games were born. Greece wasn't one country — it was a collection of independent city-states, each with its own government and character. Athens valued education, art, and democracy (citizens voting on laws). Sparta valued military strength, discipline, and courage. Greek mythology — the stories of Zeus, Athena, Hercules, and Odysseus — taught lessons about bravery, wisdom, pride, and the dangers of hubris. These stories are still told today because they speak to something universal about human nature.",
            "scaffolding_sequence": [
                "Show Greece on a map: a mountainous peninsula with many islands. The mountains separated city-states and made each one independent.",
                "Introduce Athens: the birthplace of democracy. Citizens gathered on a hill (the Pnyx) and voted on laws directly — no representatives, just citizens voting.",
                "Introduce Sparta: a city built around its army. Spartan boys left home at age 7 to begin military training. Spartans valued strength, endurance, and obedience.",
                "Tell 3 Greek myths: Zeus and the Olympians, the Odyssey (Odysseus's long journey home), and a myth of your choosing (Icarus, Theseus, Persephone)",
                "Introduce the Olympic Games: held every 4 years in Olympia. All wars stopped for the Games. Athletes competed in wrestling, running, discus, and javelin.",
                "Discuss Greek philosophy briefly: Socrates asked questions to find truth. 'The unexamined life is not worth living.'",
                "Place Greece on the timeline: after Egypt and Mesopotamia, before Rome",
                "Compare Athens and Sparta on a chart: government, education, values, role of women",
            ],
            "socratic_questions": [
                "Athens let citizens vote on every law. What would be good about that? What might be hard about it?",
                "Spartan boys left their families at age 7 for military training. What do you think about that? Would you have wanted to be Spartan?",
                "Greek myths often show what happens when humans are too proud. Why did the Greeks think pride was dangerous?",
                "The Greeks stopped all wars for the Olympic Games. Why was athletics important enough to stop fighting for?",
            ],
            "practice_activities": [
                "Greek Olympic Games: hold a family mini-Olympics with running, jumping, and throwing events",
                "Athens vs Sparta debate: each family member argues for one city-state. Which was better to live in? Why?",
                "Myth retelling: read a Greek myth and the child narrates it back, then draws the most exciting scene",
                "Democracy in action: hold a family vote on something real (what to have for dinner, what to do this weekend) to experience Athenian democracy",
            ],
            "real_world_connections": [
                "Democracy: the United States and many other countries use democratic government, inspired by Athens",
                "The Olympic Games: held every 4 years just like in ancient Greece, now with athletes from around the world",
                "Greek words in English: 'democracy' (people-power), 'philosophy' (love of wisdom), 'athletics' (from the Greek word for contest)",
                "Greek myths appear everywhere: movies, books, video games, and even planet and constellation names (Mars, Jupiter, Orion)",
            ],
            "common_misconceptions": [
                "Thinking Athenian democracy included everyone — only adult male citizens could vote. Women, slaves, and foreigners could not. This is important to acknowledge honestly.",
                "Believing Sparta was 'bad' and Athens was 'good' — each had strengths and serious flaws. Sparta's discipline won the Peloponnesian War; Athens's creativity gave us philosophy and theater.",
                "Thinking Greek myths are just made-up stories — for the Greeks, these were their religion, their explanation of the world, and their moral instruction",
                "Assuming all Greek city-states were alike — there were hundreds, each with its own character. Athens and Sparta are just the most famous.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Compares Athens and Sparta on government, values, and education",
                "Retells 3 Greek myths with key details",
                "Explains Athenian democracy in child-friendly language",
            ],
            "proficiency_indicators": [
                "Describes Athens OR Sparta but has difficulty comparing them",
                "Retells 1-2 myths with some details",
            ],
            "developing_indicators": [
                "Knows Greece is ancient but cannot distinguish city-states",
                "Cannot retell a myth without significant prompting",
            ],
            "assessment_methods": ["oral narration", "comparison chart", "myth retelling"],
            "sample_assessment_prompts": [
                "How were Athens and Sparta different? Which would you rather live in?",
                "Tell me the myth of Odysseus (or another myth you learned).",
                "What is democracy? How did the Athenians practice it?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which Greek city-state is known as the birthplace of democracy?",
                "expected_type": "multiple_choice",
                "options": ["Sparta", "Athens", "Troy", "Olympia"],
                "correct_answer": "Athens",
                "hints": ["This city-state let its citizens vote on laws."],
                "explanation": "Athens is the birthplace of democracy. Athenian citizens gathered and voted directly on laws — the first known democracy in history.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What were Spartan boys trained to be?",
                "expected_type": "multiple_choice",
                "options": ["Artists", "Soldiers", "Philosophers", "Farmers"],
                "correct_answer": "Soldiers",
                "hints": ["Sparta valued military strength above everything else."],
                "explanation": "Spartan boys left home at age 7 to begin military training. Sparta was a warrior society that valued strength, discipline, and courage.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Name two ways Athens and Sparta were different.",
                "expected_type": "text",
                "hints": ["Think about government and what they valued most."],
                "explanation": "Athens had a democracy where citizens voted; Sparta had two kings and a military government. Athens valued education, arts, and philosophy; Sparta valued military training and physical strength.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: In Athenian democracy, every person living in Athens could vote.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["Think about who was considered a 'citizen' in ancient Athens."],
                "explanation": "False. Only adult male citizens could vote. Women, slaves, and foreigners were excluded. This is an important limitation of Athenian democracy.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Retell a Greek myth you have learned. Include the main characters, what happened, and what lesson the myth teaches.",
                "expected_type": "text",
                "hints": [
                    "Pick a myth: Icarus, Odysseus, Theseus, Persephone, or another you know. Who is in it? What happens? What is the message?"
                ],
                "explanation": "A good retelling includes characters, key events in order, and the lesson. Example for Icarus: Daedalus made wings of feathers and wax for himself and his son Icarus. He warned Icarus not to fly too close to the sun. Icarus was thrilled and flew higher and higher. The sun melted the wax and Icarus fell into the sea. The lesson: listen to wise advice and don't let excitement overrule caution.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Compare Athens and Sparta. How were they alike? How were they different?",
                "type": "open_response",
                "target_concept": "athens_sparta",
                "rubric": "Mastery: compares on 3+ characteristics with specifics. Proficient: compares on 1-2. Developing: cannot compare.",
            },
            {
                "prompt": "What is democracy? How did Athens practice it?",
                "type": "open_response",
                "target_concept": "democracy",
                "rubric": "Mastery: defines democracy and explains Athenian voting. Proficient: defines democracy. Developing: cannot explain.",
            },
            {
                "prompt": "Retell a Greek myth.",
                "type": "open_response",
                "target_concept": "myth_retelling",
                "rubric": "Mastery: characters, events, and lesson included. Proficient: events only. Developing: cannot retell without heavy prompting.",
            },
        ],
        "resource_guidance": {
            "required": ["map of Greece and the Mediterranean", "collection of Greek myths for children"],
            "recommended": [
                "living books about ancient Greece",
                "pictures of the Parthenon, Greek pottery, and Olympic events",
            ],
        },
        "time_estimates": {"first_exposure": 30, "practice_session": 20, "assessment": 15},
        "accommodations": {
            "dyslexia": "Greek myths are ideal for audiobook listening. Oral narration of myths. Map drawing is visual. Family Olympic Games are physical, not text-based.",
            "adhd": "Greek myths are exciting and action-packed — natural attention holders. Family Olympics channel energy. Athens vs Sparta debate is interactive. 15-20 minute sessions per subtopic.",
            "gifted": "Read longer versions of the Iliad and Odyssey. Research the Peloponnesian War (Athens vs Sparta). Compare Athenian democracy to modern democracy. Discuss Greek philosophy: Socrates, Plato, Aristotle.",
            "visual_learner": "Photographs of Greek ruins and pottery. Illustrated myth books. Maps of city-states.",
            "kinesthetic_learner": "Family Olympics. Act out myths. Build the Parthenon with blocks. Sculpt with clay.",
            "auditory_learner": "Listen to myths told as stories. Discuss and debate Athens vs Sparta. Oral retelling of myths is the primary activity.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Ancient Greece was not one country but many independent city-states, and an honest telling shows both their brilliance and their hard sides. Athens prized education, art, and democracy, where citizens voted directly on the laws, though only free adult men counted as citizens; women, foreigners, and the enslaved did not. Sparta prized military strength, and its way of life rested on a large enslaved population, the helots, held down by force. The city-states often warred on one another, and Greek life across the land relied in part on enslaved labor. Greece also gave the world democracy, philosophy, theater, the Olympic Games, and the myths of gods and heroes. Today we compare Athens and Sparta, explain democracy, retell Greek myths, and describe the Olympics.",
                "gradual_release": {
                    "i_do": "Set Athens and Sparta side by side and think aloud, telling the whole truth of each: Athens, democracy and art and learning, but a democracy only for free men; Sparta, discipline and courage, but a society resting on the enslaved helots. Note that the city-states warred on one another. Tell a Greek myth in order and name what it taught, and describe the Olympic Games.",
                    "we_do": "Compare Athens and Sparta on a chart together, the achievements and the hard facts of each, retell a myth and name its lesson, and describe the Olympic Games and their place in Greek life.",
                    "you_do": "Child compares Athens and Sparta truthfully, explains what democracy means and how Athens practiced it and whom it left out, retells three Greek myths with their lessons, and describes the Olympic Games.",
                },
                "guided_practice": [
                    "Compare Athens and Sparta on a chart: government, values, education, and whom each left unfree",
                    "Retell a Greek myth and name the lesson it taught the Greeks",
                    "Describe the Olympic Games and explain why the Greeks paused their wars with one another for them",
                ],
                "independent_practice": [
                    "Retell three Greek myths from memory with their lessons",
                    "Hold a family vote to experience Athenian democracy, then describe how it worked and whom it left out",
                ],
                "mastery_check": [
                    "Compare Athens and Sparta on government, values, education, and the unfree people each relied on",
                    "Explain what democracy means and how Athens practiced it, including who could and could not vote",
                    "Retell three Greek myths and describe the Olympic Games",
                ],
                "spiral_review": [
                    "Revisit the earlier civilizations and set ancient Greece beside them on the timeline, after Egypt, before Rome",
                ],
            },
            "classical": {
                "narrative_introduction": "Ancient Greece is the birthplace of much that the classical mind treasures: democracy, philosophy, the theater, and the Olympic Games. Greece was many city-states, and two stand out: Athens, which gave the world the rule of citizens and the love of wisdom, and Sparta, which gave it discipline and the soldier's courage. The honest student holds the whole of Greece: its democracy was for free men only; its city-states warred on one another; and Greek life, in Athens and above all in Sparta with its helots, rested on the labor of the enslaved. Greece is to be admired and reckoned with truthfully, both at once.",
                "memory_work": {
                    "chants": [
                        "Chant the two great city-states and their gifts: Athens of democracy and learning, Sparta of discipline and arms",
                        "Chant the Greek gifts to the world: democracy, philosophy, the theater, and the Olympic Games",
                    ],
                    "recitations": [
                        "Recite that democracy means rule by the citizens, and that in Athens only free men were citizens, while women, foreigners, and the enslaved were not",
                        "Recite that the Greek city-states warred on one another, and that Greek life, and Sparta most of all with its helots, rested on the labor of enslaved people",
                    ],
                },
                "copywork": [
                    "Copy the names of the chief Greek gods and heroes, and a line from a Greek myth that carries its lesson",
                ],
                "recitation_routine": "Begin each lesson by reciting the gifts of Greece and retelling the previous myth before a new one is met, so the gallery of myths grows cumulatively.",
                "history_integration": "Place ancient Greece on the chronological spine after Egypt and Mesopotamia and before Rome, and mark it as the source from which Rome, and the long Western tradition after Rome, would draw their philosophy, their stories, and the idea of the citizen, an inheritance both brilliant and, in its slavery and its wars, deeply flawed.",
                "read_aloud_suggestions": [
                    "A fine collection of Greek myths for children, read aloud for narration",
                    "A children's retelling of the Odyssey, the long journey of Odysseus home, read aloud for its language and its story",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A beautifully told collection of Greek myths, the kind that has delighted children for generations, never a dry summary",
                    "A living book about daily life in Athens and Sparta, honest about both their achievements and the enslaved people their life depended on",
                ],
                "short_lesson_flow": "Read a Greek myth aloud, told with all its drama, and let the child narrate it back and draw the most striking scene. Another day, read of Athens and Sparta, their brilliance and their hard truths together, and wonder with the child which city they would choose, and why. Tell the whole truth, the democracy and the slavery, and let the child weigh it. Stop while interest is high.",
                "narration_prompt": "Tell me the myth we just heard. What happened, and what did it teach the Greeks who told it?",
                "real_world_objects": [
                    "A living book of Greek myths, returned to again and again",
                    "A map of Greece, its mountains and islands traced by hand",
                    "A Book of Centuries for the child's drawn scenes of Greece",
                    "A real or improvised set of Olympic events to run outdoors",
                ],
                "nature_connection": "Notice how the mountains and the sea of Greece shaped its people: the mountains divided the land into separate city-states, and the sea made the Greeks sailors and traders, geography itself a teacher of history.",
                "habit_focus": "The habit of attention: hearing a myth closely enough to retell it whole, and weighing Athens and Sparta, their gifts and their wrongs, with a fair and thoughtful mind.",
            },
            "montessori": {
                "prepared_materials": [
                    "A Greece folder in the continent collection, with photographs and fact cards",
                    "Greek mythology cards for matching gods, heroes, and their stories",
                    "An Athens-and-Sparta comparison work",
                    "Materials for Greek pottery and an Olympic Games role play",
                ],
                "presentation": {
                    "three_period_lesson": "With the city-state cards: this is Athens, the city of democracy; show me Athens; which city-state is this, and what did it prize?",
                    "steps": [
                        "The child explores the Greece folder and locates Greece on the map",
                        "The child works the mythology cards, matching each god or hero to their story and its lesson",
                        "The child compares Athens and Sparta on a chart: how each was governed, who could take part, and the enslaved people each relied on",
                    ],
                },
                "control_of_error": "The matched mythology and fact cards are the control, pairing in one true way, and the comparison chart checks the child's reasoning: a trait or a hard fact set under the wrong city-state does not match the cards' evidence.",
                "abstraction_pathway": "From handling the concrete Greece folder and the mythology cards, to comparing Athens and Sparta, toward grasping democracy as an idea and Greece's place in the larger story of history.",
                "extensions": [
                    "Investigate the Peloponnesian War, when Athens and Sparta warred on each other",
                    "Compare Athenian democracy with the government of the child's own country",
                    "Study the Greek philosophers and the Socratic way of questioning",
                ],
                "observation_focus": "Watch for the child comparing Athens and Sparta fairly, neither cast as simply good or bad, grasping both the achievement of Athenian democracy and its limits, and the courage of Sparta and the enslaved helots its life rested on.",
            },
            "unschooling": {
                "invitations": [
                    "Keep beautifully illustrated collections of Greek myths within reach",
                    "Leave out clay for Greek pottery and materials for staging an Olympic Games",
                    "Have documentaries and films about ancient Greece available",
                ],
                "real_world_contexts": [
                    "Watching the modern Olympic Games and tracing them back to ancient Greece",
                    "Meeting Greek myths in books, films, and games, and recognizing the old stories",
                    "Noticing Greek words in English: democracy, philosophy, athletics",
                    "Holding a real family vote and feeling what direct democracy is like",
                ],
                "conversation_starters": [
                    "Athens let its citizens vote on the laws, but only free men were citizens, and Greek life relied on enslaved people; what do you think of that?",
                    "Spartan boys left home at seven for army training, and Sparta held the helots unfree by force; would you have wanted to be Spartan?",
                    "The Greek city-states often warred on one another; what might it have been like to live in a land of rival cities?",
                ],
                "resource_bank": [
                    "Illustrated collections of Greek myths and books about ancient Greece",
                    "Documentaries and films about Greece, and the modern Olympic Games",
                    "Museums with Greek art and pottery",
                ],
                "parent_role": "Follow the child's delight in the Greek myths into books, films, and play, and wonder aloud about Athens and Sparta and what each got right and wrong. Be honest about the whole of Greece, its democracy and philosophy alongside its slavery, its wars, and the people it left unfree, and let the child weigh it; let real stories and real conversation, rather than a worksheet, teach ancient Greece.",
                "observation_documentation": "Over time, note whether the child can compare Athens and Sparta, explain what democracy is and whom Athens included and excluded, recognize that Greek life rested in part on the enslaved, retell Greek myths, and describe the Olympics. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Greek myths are foundational stories in Western literature — references appear in books throughout life",
            "math": "Greek mathematicians like Pythagoras and Euclid laid the foundations of geometry",
            "science": "Greek thinkers asked 'why?' about nature: Aristotle classified animals, Hippocrates founded medicine, Archimedes discovered buoyancy",
        },
    },
    "hf-08": {
        "enriched": True,
        "learning_objectives": [
            "Narrate the story of Rome from its founding through the Republic, Empire, and Fall",
            "Explain the difference between a republic and an empire",
            "Name at least 4 Roman contributions to the modern world: roads, aqueducts, law, architecture",
            "Place Rome on the timeline after Greece and describe how Rome borrowed from Greek culture",
        ],
        "teaching_guidance": {
            "introduction": "Rome is one of the greatest stories in all of history: from a tiny village on seven hills to an empire that ruled the entire Mediterranean world. Rome borrowed brilliantly from Greece — their gods, their architecture, their philosophy — and then added their own genius: roads that connected the empire, aqueducts that carried water to cities, laws that became the foundation of Western legal systems, and an army that conquered the known world. The story of Rome's rise AND fall teaches us that even the most powerful civilizations don't last forever.",
            "scaffolding_sequence": [
                "Tell the founding myth: Romulus and Remus, twin brothers raised by a wolf. Romulus founded Rome on the Palatine Hill.",
                "Explain the Roman Republic: instead of a king, Romans elected leaders called consuls. The Senate debated laws. Citizens had a voice.",
                "Tell the story of Julius Caesar: a brilliant general who became dictator, was loved by the people but feared by the Senate, and was assassinated on the Ides of March.",
                "Explain the shift from Republic to Empire: Augustus Caesar became the first emperor. The Empire expanded to cover the Mediterranean.",
                "Tour Roman engineering: roads (straight, paved, lasting 2000 years), aqueducts (carrying water miles to cities), the Colosseum (50,000 seats!), concrete (a Roman invention).",
                "Discuss the Fall of Rome: too large, invasions from the north, divided into East and West, the Western Empire fell in 476 AD.",
                "Compare Rome to Greece: Romans borrowed Greek gods (Zeus became Jupiter), architecture (columns), and ideas, but added engineering, law, and military organization.",
                "Place Rome on the timeline and narrate its story from founding to fall.",
            ],
            "socratic_questions": [
                "Rome changed from a Republic (elected leaders) to an Empire (one ruler with total power). Why do you think the Romans gave up their republic?",
                "Roman roads were so well built that some are still used today, 2,000 years later. What does that tell you about Roman engineering?",
                "The Colosseum held 50,000 people for entertainment, including gladiator fights. What does that tell you about Roman culture?",
                "Why do empires fall? Rome lasted almost 1,000 years but eventually collapsed. What causes something that big and powerful to end?",
            ],
            "practice_activities": [
                "Roman road building: build a model road with layers of gravel, sand, and stones to understand Roman engineering",
                "Aqueduct model: use cardboard tubes or straws to build an aqueduct that actually carries water downhill",
                "Roman Senate debate: hold a family debate on a topic. Each person is a Senator arguing their position. Vote on the outcome.",
                "Map of the Roman Empire: draw the Mediterranean and shade in the entire territory Rome controlled at its peak — it's enormous",
            ],
            "real_world_connections": [
                "Romance languages (Spanish, French, Italian, Portuguese, Romanian) all descend from Latin, the language of Rome",
                "The U.S. government was modeled on the Roman Republic: the Senate, the idea of a republic, checks and balances",
                "Roman roads connected the empire — modern highways serve the same purpose. Some European highways follow Roman road routes.",
                "Concrete was a Roman invention. Every building, bridge, and sidewalk uses a descendant of Roman concrete technology.",
            ],
            "common_misconceptions": [
                "Thinking all gladiators died in the arena — many were professionals who survived multiple fights. Not every contest was to the death.",
                "Believing Rome fell in a single dramatic event — the fall was a gradual process over centuries, not one sudden collapse",
                "Confusing the Roman Republic with modern republics — the Roman system was very different, with power concentrated among wealthy families",
                "Thinking Romans invented everything they used — Romans were great borrowers. They took Greek ideas and improved them with engineering.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Narrates Rome from founding through Republic, Empire, and Fall",
                "Explains republic vs empire clearly",
                "Names 4+ Roman contributions to the modern world",
            ],
            "proficiency_indicators": [
                "Narrates several facts about Rome but may not cover the full arc",
                "Names 2-3 Roman contributions",
            ],
            "developing_indicators": [
                "Knows Rome was important but cannot narrate its story",
                "Confuses Roman and Greek facts",
            ],
            "assessment_methods": ["oral narration", "map drawing", "contribution identification"],
            "sample_assessment_prompts": [
                "Tell me the story of Rome from beginning to end.",
                "What is the difference between a republic and an empire?",
                "Name four things Rome gave to the modern world.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is the difference between a republic and an empire?",
                "expected_type": "multiple_choice",
                "options": [
                    "A republic has elected leaders; an empire has one ruler with total power",
                    "A republic is bigger than an empire",
                    "An empire has elected leaders; a republic has a king",
                    "There is no difference",
                ],
                "correct_answer": "A republic has elected leaders; an empire has one ruler with total power",
                "hints": [
                    "In a republic, citizens choose their leaders. In an empire, one person rules over everyone."
                ],
                "explanation": "In a republic, leaders are elected by citizens (like the Roman Senate and consuls). In an empire, one person (the emperor) holds supreme power. Rome started as a republic and became an empire.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Who was the first Roman emperor?",
                "expected_type": "multiple_choice",
                "options": ["Julius Caesar", "Augustus Caesar", "Nero", "Romulus"],
                "correct_answer": "Augustus Caesar",
                "hints": ["Julius Caesar was assassinated before becoming emperor. Who came after him?"],
                "explanation": "Augustus Caesar (Octavian) was the first Roman emperor. Julius Caesar was a dictator but was killed before Rome officially became an empire. Augustus transformed the Republic into the Empire.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Name three things the Romans contributed to the modern world.",
                "expected_type": "text",
                "hints": ["Think about: roads, water systems, buildings, laws, language, government ideas..."],
                "explanation": "Roman contributions include: roads (straight, paved, durable), aqueducts (carrying water to cities), concrete, arches in architecture, the legal system (innocent until proven guilty), the idea of a republic, and Latin (the root of Romance languages).",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: Rome fell because of a single big battle that it lost.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["The decline of Rome happened over many years. Was it sudden or gradual?"],
                "explanation": "False. The fall of Rome was gradual, happening over centuries. Causes included: the empire became too large to govern, invasions by Germanic tribes, economic problems, and internal corruption. The Western Roman Empire officially ended in 476 AD.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "In your own words, tell the story of Rome from its beginning to its fall. Include the founding, the Republic, the Empire, and why it fell.",
                "expected_type": "text",
                "hints": [
                    "Start with Romulus. Then the Republic with the Senate. Then Julius and Augustus Caesar and the Empire. Then the fall."
                ],
                "explanation": "A complete narration covers: founding by Romulus (753 BC), the Republic with elected consuls and Senate, Julius Caesar's rise and assassination, Augustus as first emperor, the Empire's expansion around the Mediterranean, Roman achievements (roads, aqueducts, law), and the gradual fall (too large, invasions, 476 AD).",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Narrate the story of Rome from founding to fall.",
                "type": "open_response",
                "target_concept": "rome_narration",
                "rubric": "Mastery: covers founding, Republic, Empire, contributions, and fall. Proficient: covers 3 phases. Developing: knows scattered facts.",
            },
            {
                "prompt": "Draw a map showing the Roman Empire at its largest.",
                "type": "open_response",
                "target_concept": "rome_map",
                "rubric": "Mastery: Mediterranean surrounded by Roman territory. Proficient: partially correct borders. Developing: cannot approximate.",
            },
        ],
        "resource_guidance": {
            "required": ["map of the Mediterranean world", "pictures of Roman roads, aqueducts, and the Colosseum"],
            "recommended": ["living books about ancient Rome", "building supplies for road/aqueduct models"],
        },
        "time_estimates": {"first_exposure": 30, "practice_session": 20, "assessment": 15},
        "accommodations": {
            "dyslexia": "Read all content aloud. Roman history is ideal for storytelling. Hands-on road and aqueduct building. Map drawing. Oral narration only.",
            "adhd": "Build roads and aqueducts (hands-on). Roman Senate debate (interactive). Colosseum drama (act out a gladiator entry). 15-20 minute sessions per subtopic.",
            "gifted": "Compare Roman Republic to U.S. government. Research Pompeii (preserved by volcanic ash). Read about daily life in Rome. Discuss why empires rise and fall as a pattern in history.",
            "visual_learner": "Photographs of Roman ruins, roads, aqueducts. Maps showing the Empire's growth. Illustrated timelines.",
            "kinesthetic_learner": "Build Roman roads, aqueducts, and arches. Act out the Senate. Walk a Roman road pattern on the floor.",
            "auditory_learner": "Listen to the story of Rome told as a dramatic narrative. Discuss and debate Roman decisions. Roman Senate role play.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Rome grew from a small village on seven hills to an empire ruling the whole Mediterranean world. It began as a republic, where leaders called consuls were elected and a Senate debated the laws, though only free men had a vote, not women or the enslaved. Later it became an empire ruled by one emperor. An honest telling holds all of Rome: it grew by conquest, held many people in slavery, and staged games in which captives and the enslaved were forced to fight for the crowd, and it also left the world roads, aqueducts, law, and lasting architecture. Today we narrate Rome from founding through Republic, Empire, and Fall, explain republic and empire, name Rome's contributions, and see how Rome borrowed from Greece.",
                "gradual_release": {
                    "i_do": "Tell the story of Rome in order and whole: the founding myth of Romulus, the Republic with its elected consuls and Senate in which only free men voted, Julius Caesar and the turn to one-man rule, Augustus the first emperor, the empire spread by conquest and worked by the enslaved, and the slow fall. Name the contributions and the cruelties together, the law and the roads beside the conquest, the slavery, and the games.",
                    "we_do": "Retell the story of Rome together, name the contributions Rome left the world and the hard truths beside them, compare a republic and an empire, and trace what Rome borrowed from Greece.",
                    "you_do": "Child narrates Rome from founding through Republic, Empire, and Fall, explains republic versus empire, names four Roman contributions, describes how Rome borrowed from Greece, and tells the hard truths of conquest and slavery honestly.",
                },
                "guided_practice": [
                    "Retell the story of Rome: founding, Republic, Empire, and Fall",
                    "Explain the difference between a republic and an empire, and note who could vote in the Republic",
                    "Name Roman contributions, the roads, aqueducts, law, and architecture, beside the conquest and slavery the empire rested on",
                ],
                "independent_practice": [
                    "Narrate the full story of Rome from founding to fall, the achievements and the wrongs together",
                    "Build a model Roman road or aqueduct and explain the engineering",
                ],
                "mastery_check": [
                    "Narrate Rome from its founding through the Republic, the Empire, and the Fall",
                    "Explain the difference between a republic and an empire",
                    "Name at least four Roman contributions and tell honestly the conquest and slavery the empire also rested on",
                ],
                "spiral_review": [
                    "Revisit ancient Greece, and set Rome beside it on the timeline, the heir that borrowed and built on what Greece began",
                ],
            },
            "classical": {
                "narrative_introduction": "Rome is one of the grandest stories in all of history: a village that became an empire ruling the known world. It began as a republic, where free male citizens chose their leaders, and became an empire under one ruler. Rome was a borrower of genius, taking the gods, the art, and the philosophy of Greece and adding its own: the road, the aqueduct, the law, the legion. The honest student holds all of Rome at once: its empire was won by conquest and worked by the enslaved, and its games forced captives and the enslaved to fight for the crowd, even as it gave the world its law and its engineering. Its long rise and fall is a lesson that no power, however great, endures forever.",
                "memory_work": {
                    "chants": [
                        "Chant the ages of Rome: the founding, the Republic, the Empire, and the Fall",
                        "Chant the gifts of Rome, and the hard truths beside them: the roads, the aqueducts, and the law, and the conquest, the slavery, and the games",
                    ],
                    "recitations": [
                        "Recite that a republic is ruled by leaders the citizens elect, and an empire by one ruler with supreme power",
                        "Recite that Rome's grandeur was won by conquest and rested on the enslaved, and that an honest history tells the gifts and the wrongs together",
                    ],
                },
                "copywork": [
                    "Copy the four ages of Rome and the Roman numerals, and a Latin word or two with the English words descended from it",
                ],
                "recitation_routine": "Begin each lesson by reciting the ages of Rome and narrating yesterday's portion of the story before adding the next.",
                "history_integration": "Place Rome on the chronological spine directly after Greece, and mark it as the great bridge of the spine: it carried the inheritance of Greece, brilliant and flawed alike, across a thousand years and handed it, when it fell, to the Europe that came after.",
                "read_aloud_suggestions": [
                    "A living account of the story of Rome, the founding, the Republic, the Caesars, and the fall, read aloud for narration",
                    "A children's retelling of a Roman tale, of a soldier, a senator, or a citizen, read aloud so the child meets the age through a story",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A beautifully told living book about the story of Rome, written with knowledge and wonder, never a dry textbook",
                    "A living book of Roman daily life, honest about both its grandeur and the enslaved people the city depended on",
                ],
                "short_lesson_flow": "Read a portion of the story of Rome aloud, told with all its drama, and let the child narrate it back. The child may build a Roman road or arch, or draw the empire's reach onto a map in the Book of Centuries. Let the long story unfold portion by portion. Tell the conquest, the slavery, and the games as honestly as the law and the engineering, and let the child weigh them. Stop while interest holds.",
                "narration_prompt": "Tell me the part of the Roman story we just heard. How did Rome change as it grew?",
                "real_world_objects": [
                    "A living book about ancient Rome",
                    "Materials for building a model Roman road, arch, or aqueduct",
                    "A map of the Mediterranean for the empire's reach, and a Book of Centuries",
                    "Pictures of real Roman roads, aqueducts, and the Colosseum",
                ],
                "nature_connection": "Consider how Roman engineers worked with nature rather than against it: aqueducts carried water downhill by the gentlest of slopes for many miles, the steady pull of gravity harnessed by careful observation.",
                "habit_focus": "The habit of attention: following the long story of Rome closely enough to narrate its rise and its fall, and weighing its grandeur and its cruelty with a fair mind.",
            },
            "montessori": {
                "prepared_materials": [
                    "A Rome folder in the continent collection, with photographs and fact cards",
                    "Materials for building a Roman road, arch, and aqueduct",
                    "Roman numeral materials connecting math and history",
                    "A timeline of Rome with movable cards for the Republic, the Empire, and the Fall",
                ],
                "presentation": {
                    "three_period_lesson": "With the timeline cards: this is the Republic, when free male citizens elected their leaders; show me the Republic; which age of Rome is this?",
                    "steps": [
                        "The child explores the Rome folder and locates Rome and the Mediterranean on the map",
                        "The child builds a Roman road, arch, or aqueduct, the hands learning the engineering",
                        "The child sets the ages of Rome on the timeline and traces both what Rome built and what its empire rested on, conquest and slavery alike",
                    ],
                },
                "control_of_error": "The aqueduct built with too steep or too flat a slope will not carry its water, an exact engineering control; the fact cards and timeline confirm the rest, matching and ordering in one true way, and an account that tells only Rome's glory or only its cruelty is checked against the record and found one-sided.",
                "abstraction_pathway": "From handling the concrete Rome folder and building the real engineering, to ordering the ages of Rome on the timeline, toward narrating the whole story of Rome and grasping the difference between a republic and an empire.",
                "extensions": [
                    "Compare the Roman Republic with the government of the child's own country",
                    "Investigate how Rome's roads and aqueducts were engineered",
                    "Trace what Rome borrowed from Greece, the brilliance and the slavery alike, and what it added of its own",
                ],
                "observation_focus": "Watch for the child grasping the turn from republic to empire, and seeing Rome whole, its engineering and its law alongside its conquest, its slavery, and its games.",
            },
            "unschooling": {
                "invitations": [
                    "Keep illustrated books about ancient Rome within reach",
                    "Leave out building materials for Roman roads, arches, and aqueducts",
                    "Have documentaries and films about Rome, the Caesars, and the Colosseum available",
                ],
                "real_world_contexts": [
                    "Noticing Roman numerals on clocks, in book chapters, and at the end of films",
                    "Hearing the Latin roots inside everyday English words",
                    "Visiting a museum with Roman artifacts, or seeing photographs of Roman ruins still standing",
                    "Wondering, while reading or watching, how a small city came to rule a whole sea",
                ],
                "conversation_starters": [
                    "Rome changed from a republic, where free men chose their leaders, to an empire under one ruler; why might a people give that up?",
                    "Roman roads still exist after two thousand years; what does that tell you about how they were built?",
                    "Rome gave the world its law and its roads, and it also conquered other peoples, held many in slavery, and forced captives to fight in its games; how do you hold all of that together?",
                ],
                "resource_bank": [
                    "Illustrated books and documentaries about ancient Rome",
                    "Building materials for Roman roads, arches, and aqueducts",
                    "Museums with Roman artifacts",
                ],
                "parent_role": "Follow the child's interest in Rome, the engineering, the Caesars, the legions, into books, documentaries, and building, and wonder aloud at how Rome rose and why it fell. Tell the hard parts honestly, the conquest, the slavery, the games, beside the achievements, and let the child reason about them rather than handing them a verdict.",
                "observation_documentation": "Over time, note whether the child can narrate the story of Rome, tell a republic from an empire, name Rome's contributions, and see both Rome's achievements and the conquest and slavery it rested on. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Latin is the root of many English words. Roman mythology (borrowed from Greece) appears throughout Western literature.",
            "math": "Roman numerals (I, V, X, L, C, D, M) are still used on clocks, in outlines, and for Super Bowl numbering",
            "science": "Roman engineering: concrete, arches, aqueducts, and roads demonstrate applied physics and materials science",
        },
    },
    "hf-09": {
        "enriched": True,
        "learning_objectives": [
            "Narrate at least 5 key stories from American history: exploration, Pilgrims, American Indians, the Revolution, and key figures",
            "Identify key historical figures: Columbus, Pocahontas, Washington, Franklin, Lincoln, Tubman",
            "Place major American history events on a timeline in correct chronological order",
            "Describe the concepts of courage, freedom, and character through the lives of historical figures",
        ],
        "teaching_guidance": {
            "introduction": "American history is a story of courage, struggle, and the pursuit of freedom. It begins with the Native peoples who lived here for thousands of years, continues through European exploration and colonization, the fight for independence, the tragedy of slavery, and the ongoing effort to live up to the promise that 'all men are created equal.' At the foundational level, we tell this story through PEOPLE — real individuals whose choices shaped the nation. This is history as biography: the story of Washington's bravery, Franklin's curiosity, Lincoln's determination, and Tubman's courage.",
            "scaffolding_sequence": [
                "Start with the land itself: Native peoples lived in North America for thousands of years before Europeans arrived. They had diverse cultures, languages, and ways of life.",
                "Tell the exploration story: Columbus sailed west looking for Asia and reached the Americas instead. Other explorers followed.",
                "Tell the Pilgrim story: people who crossed the Atlantic for religious freedom. The first Thanksgiving as a moment of cooperation between Pilgrims and Wampanoag.",
                "Tell the story of the American Revolution through George Washington: a leader who fought for independence and became the first president.",
                "Introduce Benjamin Franklin: inventor, writer, diplomat. A man of endless curiosity who helped found a nation.",
                "Tell the story of slavery and Abraham Lincoln: the great moral crisis of America and the president who ended slavery.",
                "Tell the story of Harriet Tubman: a woman who escaped slavery and returned again and again to free others through the Underground Railroad.",
                "Place all events on an American history timeline: Native peoples → Exploration → Colonies → Revolution → Constitution → Civil War → today",
            ],
            "socratic_questions": [
                "Native peoples lived here for thousands of years before Columbus. What does that tell us about who 'discovered' America?",
                "George Washington could have become a king after winning the war. He chose to be president instead and then gave up power after two terms. Why was that important?",
                "Harriet Tubman risked her life many times to free others from slavery. What kind of courage does that take?",
                "The Declaration of Independence says 'all men are created equal.' At the time it was written, did America treat everyone equally? What needed to change?",
            ],
            "practice_activities": [
                "American history timeline: create a large paper timeline and add each person and event as you study them",
                "Living biography: pick one historical figure, read about them, then dress up and 'become' them for a presentation to the family",
                "Map the colonies: draw the 13 original colonies on a map and label them. This is where America started.",
                "Freedom discussion: what does freedom mean to you? How is your freedom different from what the colonists wanted? From what enslaved people wanted?",
            ],
            "real_world_connections": [
                "The Fourth of July celebrates the Declaration of Independence — the birthday of America as a nation",
                "Presidents' Day honors Washington and Lincoln — the leader who founded the nation and the leader who preserved it",
                "The American flag has 13 stripes for the original colonies and 50 stars for the current states — history is embedded in the flag",
                "The Statue of Liberty represents the freedom that people have sought in America for centuries",
            ],
            "common_misconceptions": [
                "Thinking Columbus 'discovered' America — millions of people already lived here. Columbus was the first European to make sustained contact, but he was not the first human to find it.",
                "Romanticizing the first Thanksgiving — the relationship between colonists and Native peoples was complex and often tragic. The Thanksgiving story is one moment in a longer, harder history.",
                "Thinking the Founding Fathers were perfect — they were brilliant but flawed. Many owned slaves while writing about freedom. This contradiction is an important part of the story.",
                "Believing slavery ended easily — it took a devastating Civil War and the lives of 600,000+ soldiers. And the struggle for racial equality continued long after slavery ended.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Narrates 5+ American history stories with key details",
                "Identifies 6+ historical figures and their contributions",
                "Places major events on a timeline in correct order",
            ],
            "proficiency_indicators": [
                "Narrates 3-4 stories with some details",
                "Identifies 3-5 historical figures",
            ],
            "developing_indicators": [
                "Knows a few names but cannot narrate connected stories",
                "Cannot place events in chronological order",
            ],
            "assessment_methods": ["oral narration", "timeline ordering", "figure identification"],
            "sample_assessment_prompts": [
                "Tell me the story of how America began. Start with the Native peoples and go through the Revolution.",
                "Who was Harriet Tubman and why is she important?",
                "Put these events in order: Civil War, Pilgrims land, American Revolution, Columbus sails.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Who was the first president of the United States?",
                "expected_type": "multiple_choice",
                "options": ["Abraham Lincoln", "George Washington", "Benjamin Franklin", "Thomas Jefferson"],
                "correct_answer": "George Washington",
                "hints": [
                    "He was the leader of the army during the Revolution and then became the country's first leader."
                ],
                "explanation": "George Washington was the first president. He led the Continental Army during the American Revolution and was unanimously elected as the nation's first president in 1789.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What did Harriet Tubman do?",
                "expected_type": "multiple_choice",
                "options": [
                    "She wrote the Declaration of Independence",
                    "She led people to freedom through the Underground Railroad",
                    "She was the first female president",
                    "She invented the telephone",
                ],
                "correct_answer": "She led people to freedom through the Underground Railroad",
                "hints": ["She escaped slavery and then went back many times to rescue others."],
                "explanation": "Harriet Tubman escaped slavery and then risked her life at least 13 times to return south and lead about 70 enslaved people to freedom through the Underground Railroad.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Put these events in chronological order: American Revolution, Columbus's voyage, Civil War, Pilgrims land at Plymouth.",
                "expected_type": "text",
                "correct_answer": "Columbus's voyage, Pilgrims land at Plymouth, American Revolution, Civil War",
                "hints": ["Columbus: 1492. Pilgrims: 1620. Revolution: 1776. Civil War: 1861."],
                "explanation": "Correct order: Columbus (1492), Pilgrims (1620), American Revolution (1776), Civil War (1861-1865). Each event built on what came before.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: The Pilgrims were the first people to live in North America.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["Think about who was already living in North America when the Pilgrims arrived."],
                "explanation": "False. Native peoples had lived in North America for at least 15,000 years before the Pilgrims arrived in 1620. The Pilgrims were among the first EUROPEAN settlers, not the first people.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Choose one American historical figure and tell their story. Include what challenges they faced, what they accomplished, and why they are remembered.",
                "expected_type": "text",
                "hints": [
                    "Pick someone: Washington, Franklin, Lincoln, Tubman, or another figure you've learned about. Tell their story like you're telling it to a friend."
                ],
                "explanation": "A good response tells a story with details: who they were, what they faced, what they did, and why it mattered. Example for Lincoln: Abraham Lincoln grew up poor in a log cabin. He taught himself to read. He became president during the worst crisis in American history — the Civil War. He freed the enslaved people with the Emancipation Proclamation and held the nation together, but was assassinated before he could see peace.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Narrate the story of America from Native peoples through the Civil War.",
                "type": "open_response",
                "target_concept": "american_history_narration",
                "rubric": "Mastery: covers Native peoples, exploration, colonies, revolution, slavery, and Civil War. Proficient: covers 3-4 eras. Developing: scattered facts.",
            },
            {
                "prompt": "Tell me about George Washington. Why is he important?",
                "type": "open_response",
                "target_concept": "washington_biography",
                "rubric": "Mastery: Revolution leadership, first president, character. Proficient: knows he was first president. Developing: name recognition only.",
            },
        ],
        "resource_guidance": {
            "required": ["map of North America", "timeline paper or wall timeline"],
            "recommended": [
                "living biographies of American historical figures",
                "pictures of historical events and figures",
            ],
        },
        "time_estimates": {"first_exposure": 30, "practice_session": 20, "assessment": 15},
        "accommodations": {
            "dyslexia": "Read all biographies aloud. Use audiobooks. Historical figures come alive through storytelling, not reading. Draw timeline events rather than writing them. Oral narration for all assessments.",
            "adhd": "Dramatic storytelling: act out scenes from history. 15-minute sessions focused on one person or event. Build a log cabin model (Lincoln). Create a map of Tubman's escape route. Physical engagement with every topic.",
            "gifted": "Read primary sources (simplified excerpts). Compare perspectives: how would a Pilgrim, a Wampanoag person, and a modern historian each tell the Thanksgiving story? Research lesser-known figures. Begin discussing causes and consequences, not just events.",
            "visual_learner": "Portraits of historical figures. Maps of colonies, exploration routes, and the Underground Railroad. Illustrated timelines.",
            "kinesthetic_learner": "Build models (log cabin, colonial village). Act out scenes. Walk the Underground Railroad route on a floor map.",
            "auditory_learner": "Stories told dramatically. Discuss motivations and character. Listen to historical speeches (simplified). Debate historical decisions.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "American history is a long story, and an honest telling shows every people in it as fully human, with both noble deeds and cruel ones. Native peoples lived across North America for many thousands of years, in hundreds of nations with their own languages, governments, cultures, and deep knowledge of the land; those nations also made war on and raided one another and took captives in war. Europeans came, explored, and settled. As settlers pushed onto Native land there was violence both ways: Native warriors raided settler families, and settlers and soldiers attacked and destroyed Native villages. The new nation signed many treaties with Native nations and broke many of them, forcing whole peoples from their lands. And many Africans were carried to America in chains and enslaved, a brutal wrong ended only by a vast and deadly Civil War. Today we narrate these key stories truthfully, name the central figures, and place the events in order.",
                "gradual_release": {
                    "i_do": "Tell the story in order, plainly and truthfully, and show every people in full: the Native nations with their cultures and deep knowledge, and also their wars and raids against one another and against settlers; the settlers and the new nation with their ideals and their founding of a republic, and also their broken treaties, their massacres of Native villages, the forced removals, and their holding of enslaved people. State what is documented fact, and say plainly where people still reason differently about what it means.",
                    "we_do": "Retell the key stories together and place them on a timeline, naming the people in each. For each conflict, ask what each side actually did, the brave and the cruel alike, so that no people is left a cartoon hero or a cartoon villain.",
                    "you_do": "Child narrates at least five key stories of American history, identifies the central figures, places the events in chronological order, and can speak honestly about the deeds, noble and cruel, of every people in the story.",
                },
                "guided_practice": [
                    "Retell the key stories of American history in order: the Native nations, exploration and settlement, the Revolution, slavery, the Civil War",
                    "For a conflict on the frontier, name what each side, Native and settler, actually did",
                    "Place the major events and figures on a timeline in correct chronological order",
                ],
                "independent_practice": [
                    "Narrate a chosen figure's life, including both what they achieved and the hard truths of their time",
                    "Build an American history timeline and add each people, person, and event studied",
                ],
                "mastery_check": [
                    "Narrate at least five key stories of American history truthfully, showing every people in full",
                    "Identify the central historical figures and place major events in chronological order",
                    "Speak honestly about both the achievements and the wrongs of Native nations and of settlers, casting no people as wholly noble or wholly villainous",
                ],
                "spiral_review": [
                    "Revisit the timeline often, so the child holds the order of events, from the Native nations through exploration, the Revolution, and the Civil War",
                ],
            },
            "classical": {
                "narrative_introduction": "The classical mind studies history through narration and through the lives of real people, and it does not flinch from the truth, nor does it make any people wholly noble or wholly wicked. American history is told here as it was. Native peoples lived across the land for thousands of years in hundreds of nations, with rich cultures and deep knowledge of the land, and those nations also warred upon and raided one another and took captives in war. Europeans came and settled, founding a nation on the words that all are created equal, and that same nation broke many of its treaties with the Native nations, drove whole peoples from their lands, and held millions in slavery, until a vast Civil War ended it. The classical study weighs the courage and the cruelty of every people, and asks the hard questions honestly.",
                "memory_work": {
                    "chants": [
                        "Chant the order of the story: the Native nations, the explorers and settlers, the colonies, the Revolution, and the Civil War",
                        "Chant the even-handed rule of history: every people has done both noble and cruel things, and the honest student tells both",
                    ],
                    "recitations": [
                        "Recite the opening words of the Declaration of Independence, that all are created equal, and recite that the nation did not at first live up to them",
                        "Recite that no child today is to blame for what their ancestors did, and that the student's task is to know the truth, not to carry guilt",
                    ],
                },
                "copywork": [
                    "Copy the words from the Declaration of Independence that all men are created equal, and the names and dates of the central figures and events",
                ],
                "recitation_routine": "Begin each lesson by retelling the previous portion of the story, in order, and reciting the even-handed rule of history before reasoning further about it.",
                "history_integration": "Place American history on the chronological spine far down from the ancient civilizations, recent in the long story of humankind, and mark that the meeting of Native nations, European settlers, and enslaved Africans, with all the courage and all the wrong of each, set in motion a struggle over freedom and land that reaches forward from the spine into the present day.",
                "read_aloud_suggestions": [
                    "A living biography of an American historical figure, told honestly, with both the achievements and the flaws of the person and their age",
                    "Honest children's accounts told from more than one side: of a Native nation, of a settler family, and of the enslaved and those who freed them",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "Living biographies and accounts told honestly from more than one side: the Native nations, the settler families, the enslaved and those who resisted slavery, never a version that makes one people all good and another all bad",
                    "A living book that shows a Native nation's culture, knowledge, and grievances, and also, truthfully, the wars and raids between nations and on the frontier",
                ],
                "short_lesson_flow": "Read a portion of a living biography or a true account aloud, told with feeling and without flinching, and let the child narrate it back. Charlotte Mason held that children can meet real history, including its sorrows; the parent tells the truth about every people in it, the noble and the cruel alike, preaches no verdict, and lets the child form their own response in the narration. Keep it warm, honest, and unhurried.",
                "narration_prompt": "Tell me the story we just heard. What did each people in it do that was brave, and what did each do that was cruel? What does it make you wonder?",
                "real_world_objects": [
                    "Living biographies and true accounts of American history, told from more than one side",
                    "A Book of Centuries and a timeline the child adds peoples, figures, and events to",
                    "Maps of North America: the lands of the Native nations, the colonies, the routes of the Underground Railroad and of the forced removals",
                    "Museums, historic sites, and memorials, where the real past can be met",
                ],
                "nature_connection": "Notice the land itself, the rivers, forests, and plains that the Native nations knew and tended with deep skill for thousands of years, that settlers also farmed and changed, and that whole peoples were forced across when their lands were taken, geography woven through the whole story.",
                "habit_focus": "The habit of attention and of truthfulness: hearing hard history closely and honestly about every people, neither looking away from it nor being told what to conclude.",
            },
            "montessori": {
                "prepared_materials": [
                    "An American history timeline with movable cards for the peoples and events",
                    "Living biographies and true accounts told honestly from more than one side",
                    "Maps of the Native nations, the colonies, the Underground Railroad, and the routes of forced removal",
                    "A research and presentation space for the child to study a chosen people or figure",
                ],
                "presentation": {
                    "three_period_lesson": "With the timeline cards: this is the founding of the nation, this the Civil War that ended slavery; show me the Civil War; which event is this?",
                    "steps": [
                        "The child places the peoples and events of American history on the timeline in order",
                        "The child studies a people or a story through honest accounts that show both achievement and wrong, the Native nations' cultures and their wars, the settlers' ideals and their broken treaties and slavery",
                        "The child narrates or presents what they have learned and adds it to the timeline",
                    ],
                },
                "control_of_error": "The documented record is the control: an event set out of order does not match the dates, and an account that leaves out a people's achievements, or its wrongs, the Native nations' warfare, the settlers' broken treaties and massacres, the brutality of slavery, is checked against the honest record and found incomplete or one-sided.",
                "abstraction_pathway": "From handling the concrete timeline cards and the honest accounts, to placing the peoples and events in order, toward grasping American history as one long, connected story in which every people acted with both nobility and cruelty.",
                "extensions": [
                    "Compare how a Native nation, a settler family, an enslaved person, and a modern historian would each tell the same event",
                    "Trace on the map both a route of the Underground Railroad and a route of a forced removal",
                    "Research a people or a figure, famous or little-known, and present them honestly, the achievements and the wrongs together",
                ],
                "observation_focus": "Watch for the child holding the whole story, the courage and the wrong of every people together, placing events truly in time, and asking honest questions rather than reaching for a tidy verdict or a single villain.",
            },
            "unschooling": {
                "invitations": [
                    "Keep honest, well-told books about American history and its many peoples, told from more than one side, within reach",
                    "Leave out maps, a long timeline strip, and materials for the child's own projects",
                    "Have documentaries, historic sites, and museums available to explore",
                ],
                "real_world_contexts": [
                    "Visiting historic sites, museums, and memorials, those of the Native nations, of the colonists, and of the enslaved alike",
                    "Noticing the history in holidays, the Fourth of July, Presidents' Day, Thanksgiving, and asking what each one truly marks, and for whom",
                    "Hearing the family's own history, who came from where, and when, and why",
                    "Meeting American history in biographies, historical fiction, and documentaries that show more than one side",
                ],
                "conversation_starters": [
                    "Native nations lived here for thousands of years before Columbus, and they had wars and raids among themselves too; what does it mean to say he discovered America?",
                    "On the frontier, Native warriors raided settler families and settlers and soldiers destroyed Native villages; how do you make sense of violence on both sides?",
                    "The Declaration says all are created equal, yet many people were enslaved and the nation broke many treaties; how do you hold the ideals and the wrongs together?",
                ],
                "resource_bank": [
                    "Honest, varied books and documentaries told from more than one side",
                    "Historic sites, museums, and memorials of every people in the story",
                    "Maps and a timeline, and the family's own stories and elders",
                ],
                "parent_role": "Follow the child's curiosity about the American past into books, documentaries, and historic places, and tell the story truthfully, the courage and the cruelty of every people alike, without softening the hard parts or turning any people into the sole hero or the sole villain of the tale. Share the facts honestly and the contested questions openly, make plain that no child is to blame for what their ancestors did, and let the child reason about what it all means rather than handing them a conclusion.",
                "observation_documentation": "Over time, note whether the child can narrate the key stories of American history, knows its central figures, places events in order, and can speak honestly about the achievements and the wrongs of every people in the story. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Historical fiction and biographies build both reading skills and historical knowledge. American history vocabulary: liberty, independence, constitution, democracy.",
            "math": "Timeline math: how many years between events? How long ago was 1776? Elapsed time calculations.",
            "science": "Benjamin Franklin's experiments with electricity. Lewis and Clark's scientific observations. Colonial farming techniques.",
        },
    },
    "hf-10": {
        "enriched": True,
        "learning_objectives": [
            "Describe what a community is and identify the communities the child belongs to",
            "Explain why laws and rules exist and how they help people live together",
            "Describe at least 3 responsibilities of a citizen: respect, participation, service",
            "Explain the basic purpose of government: making rules, keeping people safe, providing services",
        ],
        "teaching_guidance": {
            "introduction": "Before a child can understand the Constitution or democratic government, they need to understand the simpler concept underneath: COMMUNITY. A community is a group of people who live near each other, help each other, and follow shared rules. Your family is a community. Your neighborhood is a community. Your town is a community. Your country is a community. Rules exist in every community because people need to know how to treat each other fairly. Citizenship means being a responsible member of your community — not just following rules, but actively contributing to the common good.",
            "scaffolding_sequence": [
                "Start with the family as a community: 'We have rules in our family. What are they? Why do we have them? What would happen without them?'",
                "Expand to the neighborhood: 'Who lives near us? How do neighbors help each other? What rules do we follow?'",
                "Introduce the town or city: 'Who keeps our roads clean? Who puts out fires? Who teaches at the library? These are community services.'",
                "Discuss why laws exist: 'Imagine a road with no traffic rules. What would happen? Laws keep people safe and treat everyone fairly.'",
                "Introduce citizenship responsibilities: respect (treat others well), participation (vote, attend meetings, contribute), service (help your community)",
                "Explain basic government: people choose leaders who make laws, provide services (police, fire, roads, schools), and protect citizens",
                "Connect to the child's life: 'You are already a citizen of your family, your neighborhood, and your country. What can YOU do to be a good citizen?'",
                "Compare community rules to ancient laws: Hammurabi's Code was a community's attempt to be fair, just like our laws today",
            ],
            "socratic_questions": [
                "What would happen if our family had no rules at all?",
                "You see a neighbor struggling to carry groceries. What could you do? Why would that matter?",
                "What is the difference between a rule and a law? Who makes each one?",
                "Can you think of a community service you use every day that someone else provides? (Roads, clean water, mail delivery...)",
            ],
            "practice_activities": [
                "Community map: draw a map of your neighborhood showing homes, shops, parks, and services (fire station, library, post office)",
                "Family rules discussion: list your family's rules and explain why each one exists. Are they fair? Would you change any?",
                "Community service project: do something kind for a neighbor or the community (pick up litter, deliver cookies, help at a food bank)",
                "Government role play: the family creates a 'government' for an evening — elect a leader, propose rules, vote on them, follow them",
            ],
            "real_world_connections": [
                "Traffic lights are community rules: everyone follows them so everyone is safe. Without them, chaos.",
                "Libraries are a community service: free books for everyone, funded by the community through taxes",
                "Voting: when children are old enough (18 in the US), they get to help choose community leaders. Until then, they can participate by being good citizens.",
                "Community helpers: firefighters, mail carriers, librarians, teachers — all serve the community. The child interacts with community helpers regularly.",
            ],
            "common_misconceptions": [
                "Thinking rules exist only to restrict freedom — rules actually PROTECT freedom by preventing stronger people from taking advantage of weaker ones",
                "Believing government is something distant and irrelevant — government affects the child every day: roads, water, schools, parks, safety",
                "Thinking citizenship only means following rules — citizenship also means CONTRIBUTING: helping neighbors, participating in community life, being kind and responsible",
                "Assuming all communities are the same — communities vary enormously in size, culture, and organization, but all share the basic need for cooperation and rules",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Describes what a community is and names the communities they belong to",
                "Explains why laws exist with specific examples",
                "Names 3+ responsibilities of a citizen and gives examples",
            ],
            "proficiency_indicators": [
                "Describes community in general terms",
                "Knows laws are important but cannot give specific examples of why",
            ],
            "developing_indicators": [
                "Has a vague sense of community but cannot articulate it",
                "Does not connect rules to fairness or safety",
            ],
            "assessment_methods": ["oral discussion", "community map", "citizenship demonstration"],
            "sample_assessment_prompts": [
                "What is a community? What communities do you belong to?",
                "Why do we have laws? What would happen without them?",
                "What does it mean to be a good citizen? Give me three examples.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which of these is a community?",
                "expected_type": "multiple_choice",
                "options": [
                    "A rock",
                    "A neighborhood where people live and help each other",
                    "A single tree",
                    "A cloud",
                ],
                "correct_answer": "A neighborhood where people live and help each other",
                "hints": ["A community is a group of PEOPLE who live together and share rules and responsibilities."],
                "explanation": "A community is a group of people who live near each other, share rules, and help each other. A neighborhood is a community. So is a family, a town, and a country.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Why do communities have rules?",
                "expected_type": "multiple_choice",
                "options": [
                    "To make life boring",
                    "To keep people safe and treat everyone fairly",
                    "Because adults like telling children what to do",
                    "Rules are not important",
                ],
                "correct_answer": "To keep people safe and treat everyone fairly",
                "hints": ["Think about traffic rules. What would happen at an intersection without them?"],
                "explanation": "Rules keep people safe and ensure fairness. Without traffic rules, accidents would happen constantly. Without rules against stealing, no one's belongings would be safe.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Name three ways you can be a good citizen in your community.",
                "expected_type": "text",
                "hints": [
                    "Think about: following rules, helping others, taking care of shared spaces, being kind and respectful."
                ],
                "explanation": "Examples: follow the rules (including family rules and laws), help neighbors (carry groceries, share tools), take care of shared spaces (don't litter, help clean up), vote when you're old enough, treat everyone with respect, volunteer for community service.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: The only responsibility of a citizen is to follow the law.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["Following the law is important, but is that ALL a good citizen does?"],
                "explanation": "False. Good citizenship includes following laws, but also: helping neighbors, participating in community life, voting (when old enough), respecting others, taking care of shared spaces, and contributing to the common good.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Think about your family as a small community. What rules does your family have? Why does each rule exist? Are the rules fair? Would you add or change any?",
                "expected_type": "text",
                "hints": [
                    "Family rules might include: bedtime, chores, screen time, how to treat siblings. Think about WHY each rule exists."
                ],
                "explanation": "A thoughtful answer lists specific family rules, explains their purpose (safety, fairness, health, respect), and evaluates whether they are fair. This exercise connects the abstract concept of 'laws' to the child's lived experience. If the child suggests changes, discuss them — this is democratic participation!",
            },
        ],
        "assessment_items": [
            {
                "prompt": "What is a community? What communities do you belong to?",
                "type": "open_response",
                "target_concept": "community_definition",
                "rubric": "Mastery: defines community and names 3+ they belong to. Proficient: general definition, names 1-2. Developing: vague understanding.",
            },
            {
                "prompt": "Why do we need laws? Give an example of what would happen without a specific law.",
                "type": "open_response",
                "target_concept": "purpose_of_laws",
                "rubric": "Mastery: explains with specific example. Proficient: general explanation. Developing: cannot explain.",
            },
            {
                "prompt": "Draw a map of your community and label the services (fire station, library, roads, etc.).",
                "type": "open_response",
                "target_concept": "community_map",
                "rubric": "Mastery: includes 5+ labeled features. Proficient: 3-4 features. Developing: 1-2 features.",
            },
        ],
        "resource_guidance": {
            "required": ["paper for community map drawing", "discussion time with the family"],
            "recommended": [
                "books about community helpers and citizenship",
                "visit to a local government building or fire station",
            ],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "This topic requires almost no reading — it's discussion-based. Community map drawing is visual. Community service projects are physical. All assessment is oral.",
            "adhd": "Community service project provides hands-on action. Family government role play is interactive and fun. Community map drawing with colors. Keep discussions to 15 minutes.",
            "gifted": "Compare different types of government (democracy, monarchy, dictatorship). Research how your local government works. Attend a town meeting or city council session. Discuss the social contract: why do people agree to follow rules?",
            "visual_learner": "Community map drawing. Pictures of community services and helpers. Comparison charts of different communities.",
            "kinesthetic_learner": "Community service projects (hands-on). Government role play. Walk through the neighborhood identifying community features.",
            "auditory_learner": "Discussion-based learning is the core here. Interview a community helper (firefighter, librarian). Family debates about rules and fairness.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "A community is a group of people who live near one another, help one another, and follow shared rules. A family is a community, and so is a neighborhood, a town, and a country. Rules and laws exist so that people can live together fairly and safely. A good citizen does more than follow the rules: a good citizen shows respect, takes part, and serves the community. Government is the way a community chooses leaders, makes its rules, keeps people safe, and provides shared services. Today we learn all of this.",
                "gradual_release": {
                    "i_do": "Start with the family as a community and think aloud: here are our rules, here is why each one exists, here is what would happen without them. Name the communities I belong to, name the responsibilities of a citizen, respect, participation, service, and describe what government does: make rules, keep people safe, provide services.",
                    "we_do": "List the communities the child belongs to together, talk through why particular laws exist, name the responsibilities of a citizen, and describe the basic purpose of government.",
                    "you_do": "Child describes what a community is and the communities they belong to, explains why laws and rules exist, names three responsibilities of a citizen, and explains the basic purpose of government.",
                },
                "guided_practice": [
                    "Name the communities the child belongs to, from the family outward",
                    "Explain why a particular rule or law exists and what would happen without it",
                    "Name and give an example of the responsibilities of a citizen: respect, participation, service",
                ],
                "independent_practice": [
                    "Draw a map of the community and label its shared services",
                    "Carry out a small act of community service and describe how it helped",
                ],
                "mastery_check": [
                    "Describe what a community is and identify the communities the child belongs to",
                    "Explain why laws and rules exist and how they help people live together",
                    "Describe three responsibilities of a citizen and explain the basic purpose of government",
                ],
                "spiral_review": [
                    "Revisit how earlier civilizations made rules to live together, such as Hammurabi's written Code",
                ],
            },
            "classical": {
                "narrative_introduction": "Long before a child can study a constitution, they can grasp the idea beneath it: the community, a group of people who share a place, a set of rules, and a care for one another. The classical tradition has always held that the good person is also the good citizen, that to live well is to take one's part in the shared life. Rules and laws exist so that people may live together in fairness and safety, and government is the community's way of ordering that shared life.",
                "memory_work": {
                    "chants": [
                        "Chant the widening communities: the family, the neighborhood, the town, the country",
                        "Chant the responsibilities of a citizen: to show respect, to take part, and to serve",
                    ],
                    "recitations": [
                        "Recite that laws and rules exist so that people may live together fairly and safely, and that government makes the rules, keeps people safe, and provides shared services",
                    ],
                },
                "copywork": [
                    "Copy the responsibilities of a citizen, and the words community, law, citizen, government, and service",
                ],
                "recitation_routine": "Begin each lesson by reciting the widening communities and the responsibilities of a citizen before any new work.",
                "history_integration": "Tie this study to the chronological spine the child has been building: the Greek idea of the citizen who governs, the Roman republic of elected leaders, Hammurabi's written laws, all are earlier chapters of the long human effort to live well together, of which the child's own community is the latest.",
                "read_aloud_suggestions": [
                    "A living book about community helpers and the shared work of a town, read aloud so the child sees citizenship in action",
                    "A story of a person who served their community well, read aloud as an example of civic virtue",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A beautifully illustrated living book about a community and the people who serve it, with true artwork, never a dry civics text",
                ],
                "short_lesson_flow": "Let the lesson live in the real community. Walk the neighborhood and notice who keeps it running, the firefighter, the librarian, the road crew. Talk over the family's own rules and why they exist. Do one real act of kindness for a neighbor. Citizenship, in the Charlotte Mason way, is a daily habit formed by living it, not a lesson recited.",
                "narration_prompt": "Tell me about our community. Who helps keep it running, and what could you do to be a good member of it?",
                "real_world_objects": [
                    "The real neighborhood and town, walked and observed",
                    "The family's own rules, talked over together",
                    "The community's shared places: the library, the park, the fire station",
                    "A real chance to serve, a kindness done for a neighbor",
                ],
                "nature_connection": "Notice that the community shares not only rules but a place: the same air, the same water, the same parks and trees, so that caring for the natural surroundings is itself a part of good citizenship.",
                "habit_focus": "The habit of service and of respect: being, in small daily ways, a good and helpful member of every community the child belongs to.",
            },
            "montessori": {
                "prepared_materials": [
                    "The practical-life materials, through which the child does real, contributing work for the community of the home",
                    "A map of the local community for the child to build and label",
                    "The peace materials: the peace rose or peace table for resolving conflict, and grace-and-courtesy lessons",
                    "Cards of community helpers and the services they provide",
                ],
                "presentation": {
                    "three_period_lesson": "With the community helper cards: this is a firefighter, who keeps the community safe; show me a community helper; what service does this person provide?",
                    "steps": [
                        "The child does real practical-life work that contributes to the community of the home or classroom",
                        "The child maps the local community and names its shared services and helpers",
                        "The child practices grace and courtesy and the peaceful resolution of conflict as the daily work of a citizen",
                    ],
                },
                "control_of_error": "The community itself is the control: practical-life work left undone is plainly felt by all, and a conflict left unresolved keeps the peace from holding, so the child sees directly how each member's care upholds the shared life.",
                "abstraction_pathway": "From doing real, concrete work for the community of the home, to mapping and naming the wider community and its services, toward grasping citizenship and the purpose of government as ideas.",
                "extensions": [
                    "Compare different kinds of government: who makes the rules, and how",
                    "Visit and learn how the local government works",
                    "Take on an ongoing role of service in the home or wider community",
                ],
                "observation_focus": "Watch for the child contributing to the shared life without being asked, resolving conflict peaceably, and grasping that rules exist for fairness and safety.",
            },
            "unschooling": {
                "invitations": [
                    "Bring the child into the real work and decisions of the household community",
                    "Keep books about community, citizenship, and how things work within reach",
                    "Leave room for real chances to help neighbors and take part in community life",
                ],
                "real_world_contexts": [
                    "Sharing in the real chores and decisions of the family",
                    "Helping a neighbor, joining a community clean-up, or volunteering together",
                    "Noticing the shared services of daily life: the roads, the library, the water, the mail",
                    "Taking part in how the family decides things together, hearing every voice",
                ],
                "conversation_starters": [
                    "What would happen if our family, or our town, had no rules at all?",
                    "Who keeps our streets clean and our water safe? How do you think that gets done?",
                    "What is one thing you could do that would make our community a little better?",
                ],
                "resource_bank": [
                    "The real household and neighborhood, with their shared work and rules",
                    "Books about community, citizenship, and community helpers",
                    "Real chances to serve: neighbors, clean-ups, volunteering",
                ],
                "parent_role": "Welcome the child into the genuine work and decisions of the family and the wider community, and wonder aloud about why rules exist and what a good neighbor does. Let real helping, real belonging, and real conversation about fairness, rather than a worksheet, teach what community and citizenship mean.",
                "observation_documentation": "Over time, note whether the child names the communities they belong to, understands why rules and laws exist, takes part and serves, and grasps what government is for. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Reading about communities and citizenship builds civic vocabulary: law, vote, citizen, service, respect, government",
            "math": "Community math: how much does a fire truck cost? How many people live in our town? Budgets are community math.",
            "science": "Communities depend on clean water, waste management, and food supply — all science topics with civic implications",
        },
    },
    "hf-11": {
        "enriched": True,
        "learning_objectives": [
            "Label all 7 continents and 5 oceans on a world map from memory",
            "Use a compass rose to identify the four cardinal directions on a map",
            "Read a simple map key and explain what its symbols mean",
            "Create a simple map of a familiar place with a key and compass rose",
        ],
        "teaching_guidance": {
            "introduction": "Maps are the language of geography, and geography is the stage on which all of history takes place. Before a child can understand WHY civilizations grew by rivers or WHY armies marched certain routes, they need to understand HOW to read a map. A compass rose shows direction. A key explains symbols. Continents and oceans divide the world. A globe shows the Earth as it truly is — round. Maps are not just for history; they are tools for navigating the real world every day.",
            "scaffolding_sequence": [
                "Start with a globe: feel its roundness. Show the child where they live. Show the equator, the poles, the hemispheres.",
                "Introduce the 7 continents with a song or chant: North America, South America, Europe, Asia, Africa, Australia, Antarctica",
                "Introduce the 5 oceans: Pacific, Atlantic, Indian, Southern, Arctic. Find each one on the globe.",
                "Move to a flat world map. Discuss why flat maps distort shapes (Greenland looks huge but isn't).",
                "Introduce the compass rose: North, South, East, West. Practice: 'Point north. Which continent is south of Europe?'",
                "Introduce a map key: symbols that represent roads, rivers, mountains, cities. Practice reading a simple map.",
                "The child draws a map of their house or yard with a key and compass rose",
                "The child draws a world map from memory, labeling all continents and oceans",
            ],
            "socratic_questions": [
                "If you wanted to travel from North America to Africa, which direction would you go and which ocean would you cross?",
                "Why does a flat map make Greenland look as big as Africa, even though Africa is 14 times larger?",
                "You are making a map of your neighborhood. What symbols would you use for houses, roads, and trees?",
                "Why is it important for everyone reading a map to agree on what the symbols mean?",
            ],
            "practice_activities": [
                "Continent and ocean labeling: print a blank world map and label all continents and oceans from memory",
                "Neighborhood map: draw a map of your street or yard with a compass rose and at least 5 map symbols with a key",
                "Globe scavenger hunt: parent names a place, child finds it on the globe as fast as possible. Track how many they can find in 2 minutes.",
                "Direction games: stand in the yard, find north with a compass, then identify what is north, south, east, and west of you",
            ],
            "real_world_connections": [
                "Phone maps and GPS use the same principles: symbols, direction, scale. Understanding maps makes digital navigation meaningful.",
                "Road trips: follow the route on a paper map while traveling. The child is the family navigator.",
                "Weather maps on the news use keys and symbols — understanding map reading unlocks weather forecasts",
                "Delivery tracking maps show packages moving across real geography — the child can trace the route",
            ],
            "common_misconceptions": [
                "Thinking north is always 'up' in real life — on a map north is at the top, but in the real world north is a compass direction, not an elevation",
                "Confusing continents with countries — Africa is a continent with 54 countries; Australia is both a continent and a country",
                "Not understanding that flat maps distort the globe — Mercator projection makes high-latitude areas look much larger than they are",
                "Thinking all maps show the same thing — different maps show different information (political boundaries, physical features, weather, population)",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Labels all 7 continents and 5 oceans from memory on a blank map",
                "Uses compass rose to give and follow directions",
                "Creates a map with compass rose and key",
            ],
            "proficiency_indicators": [
                "Labels 5-6 continents and 3-4 oceans from memory",
                "Uses compass rose with occasional confusion of east/west",
            ],
            "developing_indicators": [
                "Names some continents but cannot place them on a map",
                "Needs help using a compass rose for directions",
            ],
            "assessment_methods": ["blank map labeling", "compass rose directions", "map creation"],
            "sample_assessment_prompts": [
                "Label all the continents and oceans on this blank map.",
                "Using the compass rose, which direction is South America from North America?",
                "Draw a map of your bedroom with a key and compass rose.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "How many continents are there?",
                "expected_type": "number",
                "correct_answer": "7",
                "hints": [
                    "Can you name them? North America, South America, Europe, Asia, Africa, Australia, Antarctica."
                ],
                "explanation": "There are 7 continents: North America, South America, Europe, Asia, Africa, Australia (Oceania), and Antarctica.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "On a compass rose, which direction is at the top?",
                "expected_type": "multiple_choice",
                "options": ["East", "West", "North", "South"],
                "correct_answer": "North",
                "hints": ["The compass rose always puts this direction at the top of the map."],
                "explanation": "North is at the top of a compass rose. South is at the bottom, East is on the right, and West is on the left.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Which ocean separates North America from Europe?",
                "expected_type": "multiple_choice",
                "options": ["Pacific Ocean", "Atlantic Ocean", "Indian Ocean", "Arctic Ocean"],
                "correct_answer": "Atlantic Ocean",
                "hints": ["Look at a map. Which body of water is between the Americas and Europe/Africa?"],
                "explanation": "The Atlantic Ocean separates the Americas from Europe and Africa. The Pacific Ocean is on the other side of the Americas.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "What is a map key used for?",
                "expected_type": "text",
                "hints": [
                    "A map uses small pictures or symbols instead of words. How does the reader know what they mean?"
                ],
                "explanation": "A map key (or legend) explains what the symbols on the map mean. For example, a small blue line might mean a river, a black dot might mean a city, and a green area might mean a forest. Without the key, you cannot read the map correctly.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Draw a simple map of your house or yard. Include a compass rose showing north and a key with at least 3 symbols.",
                "expected_type": "text",
                "hints": [
                    "First decide what symbols you'll use (square = room, circle = tree, wavy line = path). Then draw the map. Add the compass rose and key."
                ],
                "explanation": "A good map includes: a bird's-eye view of the area, a compass rose showing at least N/S/E/W, and a key explaining at least 3 symbols used. This demonstrates understanding of all three core map skills.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Label all continents and oceans on a blank world map.",
                "type": "open_response",
                "target_concept": "world_geography",
                "rubric": "Mastery: all 7 continents and 5 oceans correctly placed. Proficient: 10+ correct. Developing: fewer than 8 correct.",
            },
            {
                "prompt": "Create a map of a familiar place with key and compass rose.",
                "type": "open_response",
                "target_concept": "map_creation",
                "rubric": "Mastery: includes compass rose, key with 3+ symbols, and accurate layout. Proficient: has 2 of 3 elements. Developing: map without key or compass rose.",
            },
        ],
        "resource_guidance": {
            "required": ["globe or world map", "blank world map for labeling", "compass"],
            "recommended": ["atlas for children", "large paper for drawing maps"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Map work is visual and spatial — a natural strength area. Use hands-on globe and puzzle maps. Oral directions practice. No reading required for core map skills.",
            "adhd": "Compass direction games outdoors with real movement. Globe scavenger hunt races. Draw maps with colored markers. Physical puzzle maps to assemble.",
            "gifted": "Introduce latitude and longitude. Study map projections and why they distort differently. Research how maps have changed through history (Ptolemy to GPS). Create maps with accurate scale.",
            "visual_learner": "Core strength area. Color-coded maps. Large wall maps for reference. Atlas browsing.",
            "kinesthetic_learner": "Puzzle maps to assemble physically. Outdoor compass work. Floor-sized world map to walk on.",
            "auditory_learner": "Continent and ocean songs/chants. Verbal direction games. Discuss maps while pointing.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Maps are the language of geography, and geography is the ground on which all of history happens. A map shows the world from above. The seven continents and five oceans divide the world; a compass rose shows direction, north, south, east, and west; and a map key explains what the map's symbols mean. Today we label the continents and oceans from memory, use a compass rose, read a map key, and make a map of our own.",
                "gradual_release": {
                    "i_do": "On the globe and the map, name the seven continents and five oceans, pointing to each. Show the compass rose and read the four directions. Read a map key aloud, this symbol is a river, this a city. Then draw a small map of a familiar place with a key and a compass rose.",
                    "we_do": "Name and locate the continents and oceans together, practice giving directions with the compass rose, and read a simple map's key as a pair.",
                    "you_do": "Child labels the seven continents and five oceans from memory, uses a compass rose for the four directions, reads a map key, and creates a simple map of a familiar place with a key and compass rose.",
                },
                "guided_practice": [
                    "Label the seven continents and five oceans on a blank map",
                    "Use a compass rose to name the four cardinal directions and give directions",
                    "Read a simple map key and explain what its symbols mean",
                ],
                "independent_practice": [
                    "Draw a world map from memory, labeling all continents and oceans",
                    "Create a map of a familiar place with a key and a compass rose",
                ],
                "mastery_check": [
                    "Label all seven continents and five oceans from memory on a world map",
                    "Use a compass rose to identify the four cardinal directions",
                    "Read a map key and create a simple map with a key and compass rose",
                ],
                "spiral_review": [
                    "Revisit the locations of the ancient civilizations and their rivers, found again on the map",
                ],
            },
            "classical": {
                "narrative_introduction": "Geography is the handmaid of history: every story the child will study happened in a place, and the map is how a place is known. To carry the shape of the world in the mind, the seven continents and the five oceans, the directions and the symbols, is to hold the stage on which all of history is played. The classical scholar draws the map until it is known by heart.",
                "memory_work": {
                    "chants": [
                        "Chant the seven continents: North America, South America, Europe, Asia, Africa, Australia, Antarctica",
                        "Chant the five oceans, and the four directions: north, south, east, and west",
                    ],
                    "recitations": [
                        "Recite that a map shows the world from above, that the compass rose gives direction, and that the key explains the symbols",
                    ],
                },
                "copywork": [
                    "Copy the names of the seven continents and five oceans, and the four cardinal directions",
                ],
                "recitation_routine": "Begin each lesson by chanting the continents and oceans and reciting the cardinal directions before any new map work.",
                "history_integration": "Geography underlies the whole chronological spine: place every civilization the child has studied, Egypt, Mesopotamia, Greece, Rome, on the map, and see that to know history one must first know the world it happened in.",
                "read_aloud_suggestions": [
                    "A living book of geography that journeys across the continents and oceans, read aloud so the child travels the world in the mind",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A beautifully illustrated book of geography or travel, with true artwork that makes the child long to see the wide world",
                ],
                "short_lesson_flow": "Study a map together, quietly, for a few minutes, noticing its continents, its oceans, its shapes. Then put it away, and let the child draw it from memory, as well as they can. This is the heart of the Charlotte Mason geography method: the map drawn from memory grows truer and fuller week by week. Keep it short and unhurried.",
                "narration_prompt": "Tell me about the world map. Which continents did you draw, and which oceans lie between them?",
                "real_world_objects": [
                    "A globe, handled and turned",
                    "A beautiful wall map and an atlas to study",
                    "A blank notebook for drawing maps from memory",
                    "A real compass, used out of doors to find north",
                ],
                "nature_connection": "Carry the compass outdoors and find north by the real sun and the real land, and notice the lie of the local geography, the hills, the streams, the way the ground itself can be mapped.",
                "habit_focus": "The habit of attention: studying a map closely enough to carry it in the mind and draw it true from memory.",
            },
            "montessori": {
                "prepared_materials": [
                    "The Montessori puzzle maps of the world and of each continent",
                    "A globe, including the sandpaper globe for tactile learning of land and water",
                    "Pin maps for marking the places the child has studied",
                    "A compass and materials for the child to draw a map with a key and compass rose",
                ],
                "presentation": {
                    "three_period_lesson": "With the puzzle map: this continent is Africa; show me Africa; which continent is this?",
                    "steps": [
                        "The child works the puzzle maps of the world and the continents, learning each by hand",
                        "The child names the oceans and uses the compass rose for the four directions",
                        "The child reads a map key and draws a map of a familiar place with a key and a compass rose",
                    ],
                },
                "control_of_error": "The puzzle map is the control: each continent piece fits only its own place, so a piece set wrongly will not seat, and the child corrects it without a word from the adult.",
                "abstraction_pathway": "From handling the concrete puzzle maps and the globe, to naming and locating the continents and oceans, toward carrying the map of the world in the mind and drawing one of the child's own.",
                "extensions": [
                    "Use pin maps to mark every place studied in history",
                    "Introduce latitude and longitude",
                    "Compare different map projections and how each one distorts the round Earth",
                ],
                "observation_focus": "Watch for the child placing the continents and oceans truly, using the compass rose without confusing east and west, and reading a key with understanding.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a globe, a world map, and an atlas where the child can pore over them freely",
                    "Leave out a compass and good paper for drawing maps",
                    "Have puzzle maps and books of travel and geography available",
                ],
                "real_world_contexts": [
                    "Following the route on a map during a real car trip, as the family navigator",
                    "Using the maps on a phone or a screen and noticing their symbols and directions",
                    "Tracking a package, a storm, or a journey across the real geography of the world",
                    "Finding on the globe the places that come up in books, news, and family stories",
                ],
                "conversation_starters": [
                    "If you sailed from our continent to Africa, which way would you go and which ocean would you cross?",
                    "What symbols would you use to draw a map of our neighborhood?",
                    "Why do you think everyone reading a map needs to agree on what the symbols mean?",
                ],
                "resource_bank": [
                    "A globe, a world map, an atlas, and puzzle maps",
                    "A compass and paper for map-making",
                    "The real maps of daily life: road maps, phone maps, weather maps",
                ],
                "parent_role": "Keep maps and a globe around the house and use them in real life, on trips, with the weather, when a far place comes up, and wonder aloud about the continents, the oceans, and the way. Let the child be the family navigator, and let real maps put to real use, rather than a worksheet, teach geography.",
                "observation_documentation": "Over time, note whether the child knows the continents and oceans, uses a compass rose and a map key, and can draw a map of their own. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Map keys use symbols that represent words — reading a map is a form of reading. Geography vocabulary: continent, ocean, hemisphere, equator.",
            "math": "Scale on maps involves ratios. Compass directions use degrees. Distance measurement on maps connects to measurement units.",
            "science": "Weather maps, habitat maps, and ecosystem maps all use the same skills. Understanding where animals live requires map literacy.",
        },
    },
    "hf-12": {
        "enriched": True,
        "learning_objectives": [
            "Narrate short biographies of at least 3 historical figures from different time periods and cultures",
            "Identify character traits (courage, curiosity, perseverance, kindness) in historical figures using evidence from their lives",
            "Explain how individual choices and actions shaped historical events",
            "Place biographical figures on a timeline to understand when they lived relative to each other",
        ],
        "teaching_guidance": {
            "introduction": "History is not just dates and events — it is the story of PEOPLE. Every historical event was shaped by individuals who made choices, took risks, and changed the world. Biography is the most natural way for young children to learn history because it turns abstract events into personal stories. A child who knows George Washington as a real person — a farmer who became a general, who was afraid but fought anyway, who could have been king but chose to go home — understands the American Revolution far better than one who memorizes a date.",
            "scaffolding_sequence": [
                "Start with a figure the child already knows and build a fuller picture: 'You know George Washington was the first president. But did you know he was also a farmer? And that he almost lost the war before he won it?'",
                "Read a short biography aloud and have the child narrate it back, focusing on: what was this person like? What did they do? Why do we remember them?",
                "Introduce character traits vocabulary: courage, curiosity, perseverance, kindness, honesty, wisdom. Find these traits in the figures studied.",
                "Study a figure from a different culture or time period: Cleopatra, Confucius, Harriet Tubman, Leonardo da Vinci — history is global",
                "Compare two figures: How were they alike? How were they different? What traits did they share?",
                "Discuss the idea that historical figures were not perfect — they were human, with flaws and contradictions",
                "Place each figure on the class timeline: seeing when different people lived helps the child build a sense of historical periods",
                "The child chooses a favorite figure and presents their story to the family: a living biography presentation",
            ],
            "socratic_questions": [
                "What character trait best describes this person? What evidence from their life supports that?",
                "This person faced a huge obstacle. What would YOU have done in their situation?",
                "We've studied people from Egypt, Greece, China, and America. What trait do they ALL share?",
                "If this person had made a different choice at the key moment, how might history be different?",
            ],
            "practice_activities": [
                "Living biography: the child dresses up as a historical figure and tells their story in first person ('I am Leonardo da Vinci...')",
                "Character trait matching: write traits on cards (brave, curious, determined) and match them to historical figures with evidence",
                "Biography comparison: pick two figures and create a Venn diagram showing similarities and differences",
                "Timeline placement: add each new figure to the growing classroom timeline with a portrait and key facts",
            ],
            "real_world_connections": [
                "The child's own family has historical figures: grandparents and great-grandparents who made choices that shaped the family's story",
                "Community heroes: local firefighters, teachers, and volunteers show the same traits as historical figures — courage, service, perseverance",
                "Modern leaders and inventors continue the tradition: every person who changes the world started as someone's child, just like the child studying them",
                "Character traits in the child's own life: 'You showed perseverance when you kept trying that hard math problem. That's the same trait Lincoln showed.'",
            ],
            "common_misconceptions": [
                "Thinking historical figures were born great — most faced enormous obstacles and became great through their choices and effort",
                "Believing history is only about famous people — ordinary people also shaped history, and the child's own ancestors are part of the story",
                "Idealizing historical figures as perfect — honest biography includes flaws. Washington owned slaves. Columbus caused suffering. These truths matter.",
                "Thinking biography is just memorizing facts about a person — the goal is to understand their character, their choices, and their impact",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Narrates 3+ biographies from different eras with key details",
                "Identifies character traits in figures using evidence from their lives",
                "Explains how individual choices shaped historical events",
            ],
            "proficiency_indicators": [
                "Narrates 1-2 biographies with some details",
                "Identifies traits but may not cite specific evidence",
            ],
            "developing_indicators": [
                "Recognizes names of historical figures but cannot narrate their stories",
                "Cannot identify character traits in historical figures",
            ],
            "assessment_methods": ["biography narration", "character trait identification", "timeline placement"],
            "sample_assessment_prompts": [
                "Tell me about a historical figure you admire. What were they like? What did they do?",
                "What character trait best describes Harriet Tubman? Give me evidence.",
                "How did this person's choices change history?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What does 'biography' mean?",
                "expected_type": "multiple_choice",
                "options": [
                    "A made-up story",
                    "The story of a real person's life",
                    "A map of the world",
                    "A list of dates",
                ],
                "correct_answer": "The story of a real person's life",
                "hints": ["Bio means 'life' and graph means 'writing.' A biography is..."],
                "explanation": "A biography is the story of a real person's life. It tells who they were, what they did, and why they are remembered.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which character trait best describes someone who keeps trying even when things are very hard?",
                "expected_type": "multiple_choice",
                "options": ["Laziness", "Perseverance", "Shyness", "Anger"],
                "correct_answer": "Perseverance",
                "hints": ["This trait means never giving up, even when it's difficult."],
                "explanation": "Perseverance means continuing to try even when things are difficult. Abraham Lincoln lost many elections before becoming president — that is perseverance.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Choose a historical figure you have studied. Name one character trait they showed and give evidence from their life.",
                "expected_type": "text",
                "hints": [
                    "Pick someone: Washington, Lincoln, Tubman, Confucius, Cleopatra. What trait defined them? What did they DO that shows that trait?"
                ],
                "explanation": "A good answer names the person, states a trait, and gives specific evidence. Example: Harriet Tubman showed courage because she returned to the South 13 times to free enslaved people, risking her own freedom and life each time.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: Historical figures were all perfect people who never made mistakes.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["Think about real people you know. Is anyone perfect?"],
                "explanation": "False. Historical figures were real people with real flaws. Washington owned slaves. Columbus caused suffering to Native peoples. Honest history includes both achievements and failures.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Pick two historical figures from different time periods. How were they similar? How were they different? What trait did they share?",
                "expected_type": "text",
                "hints": [
                    "Compare someone ancient (like a pharaoh or Greek hero) with someone more recent (like Lincoln or Tubman). What do they have in common despite living thousands of years apart?"
                ],
                "explanation": "A strong comparison finds both similarities and differences. Example: Hatshepsut (Egyptian pharaoh) and Harriet Tubman both showed extraordinary courage as women in male-dominated worlds. But Hatshepsut ruled a kingdom while Tubman fought against a kingdom of slavery. Both changed history through their determination.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Narrate the biography of a historical figure you admire.",
                "type": "open_response",
                "target_concept": "biography_narration",
                "rubric": "Mastery: tells full life story with traits and impact. Proficient: key facts and one trait. Developing: only name and one fact.",
            },
            {
                "prompt": "What character traits do great historical figures share?",
                "type": "open_response",
                "target_concept": "character_traits",
                "rubric": "Mastery: names 3+ traits with examples from different figures. Proficient: names 1-2 traits. Developing: cannot identify traits.",
            },
        ],
        "resource_guidance": {
            "required": [
                "biographies of historical figures (picture book or read-aloud level)",
                "timeline for placing figures",
            ],
            "recommended": [
                "costume props for living biography presentations",
                "portrait prints of historical figures",
            ],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Read biographies aloud. Living biography presentations are oral, not written. Draw portraits of figures. Timeline placement is visual.",
            "adhd": "Living biography dress-up is highly engaging. Short biographies (one per session). Act out key scenes from the person's life. Compare figures through debate.",
            "gifted": "Read longer biographies. Research lesser-known figures independently. Discuss moral complexity: can someone do great things AND terrible things? Primary source excerpts (letters, speeches).",
            "visual_learner": "Portraits and illustrations. Illustrated biographies. Timeline with pictures.",
            "kinesthetic_learner": "Living biography costume presentations. Act out scenes. Place physical cards on timeline.",
            "auditory_learner": "Listen to biographies told as stories. Discuss character traits in conversation. Present biographies orally.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "History is not only dates and events; it is the story of people. Every event was shaped by individuals who made choices. A biography is the story of one real person's life. An honest biography tells both what a person achieved and where they fell short, for historical figures were real people, with courage and flaws together. Today we narrate biographies of figures from different times and cultures, name their character traits with evidence, and see how one person's choices can shape history.",
                "gradual_release": {
                    "i_do": "Tell a short biography aloud: who the person was, what obstacles they faced, what they chose to do, and why they are remembered. Name a character trait, courage or perseverance, and point to the evidence in their life. Say plainly where the person also fell short, for an honest biography holds both.",
                    "we_do": "Read a short biography together, narrate it back, name the person's traits with evidence, and place them on the timeline.",
                    "you_do": "Child narrates biographies of at least three figures from different periods and cultures, identifies their character traits with evidence, explains how their choices shaped events, and places them on a timeline.",
                },
                "guided_practice": [
                    "Narrate a short biography: who the person was, what they faced, what they did, why they are remembered",
                    "Name a character trait of a figure and give evidence from their life",
                    "Place each figure studied on a timeline",
                ],
                "independent_practice": [
                    "Prepare and present a living biography of a chosen figure, honestly told",
                    "Compare two figures from different times: their traits, their choices, their impact",
                ],
                "mastery_check": [
                    "Narrate at least three biographies from different periods and cultures",
                    "Identify character traits in historical figures using evidence from their lives",
                    "Explain how individual choices shaped historical events, and place figures on a timeline",
                ],
                "spiral_review": [
                    "Revisit the figures already studied across history, placing them together on the timeline",
                ],
            },
            "classical": {
                "narrative_introduction": "The classical tradition has always taught history through the lives of real people, for a life well told carries more than any list of dates. Biography is moral instruction: in it the child meets both virtue and vice, courage and its failures, and learns by the example of others. An honest biography never makes its subject perfect; it tells the whole person, and lets the child weigh the good and the ill.",
                "memory_work": {
                    "chants": [
                        "Chant the questions of a biography: who was the person, what did they face, what did they choose, and why are they remembered",
                        "Chant a list of character traits: courage and curiosity, perseverance and kindness, honesty and wisdom",
                    ],
                    "recitations": [
                        "Recite that a historical figure was a real person, with both virtues and faults, and that an honest biography tells both",
                    ],
                },
                "copywork": [
                    "Copy a memorable saying of a historical figure studied, and a list of the character traits a worthy life shows",
                ],
                "recitation_routine": "Begin each lesson by recalling the figures studied before and the trait each one showed, so the gallery of lives is rehearsed cumulatively.",
                "history_integration": "Place each figure studied on the chronological spine, so the child sees when each person lived in relation to the others, and grasps that the great lives are threaded all along the spine of history.",
                "read_aloud_suggestions": [
                    "A living biography of a worthy figure, read aloud honestly, with both achievements and flaws",
                    "Plutarch's lives, or another classic collection of biographies, retold for children and read aloud",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A living biography written with vividness and truth, the kind that makes a historical figure feel like a real person met",
                    "An honest biography that includes its subject's flaws as well as their greatness, never a flattering, sanitized portrait",
                ],
                "short_lesson_flow": "Read a portion of a living biography aloud, told as a real and compelling life, and let the child narrate it back. Charlotte Mason held biography to be the finest way to teach young children history, for it gives them a real person to know. Tell the life honestly, flaws and all, and let the child form their own judgment in the telling-back.",
                "narration_prompt": "Tell me about the life we just heard. What was this person like, what did they do, and what do you think of the choices they made?",
                "real_world_objects": [
                    "Living biographies of figures from many times and places",
                    "A Book of Centuries and a timeline for placing each figure",
                    "Portraits of the historical figures studied",
                    "Simple costume props for a living biography presentation",
                ],
                "nature_connection": "Notice that many historical figures were close observers of nature, the inventor, the explorer, the scientist, and that their curiosity about the natural world is itself a thread of nature study within their lives.",
                "habit_focus": "The habit of attention and of fair judgment: knowing a historical person by the whole of their life, their courage and their failings together.",
            },
            "montessori": {
                "prepared_materials": [
                    "Biography cards with portraits and key facts of historical figures",
                    "A timeline for placing the figures chronologically",
                    "Living biographies told honestly, including their subjects' flaws",
                    "A research and presentation space for the child to study a chosen figure",
                ],
                "presentation": {
                    "three_period_lesson": "With the trait cards and a figure's biography: this person showed perseverance, see how they kept on; show me a figure who showed perseverance; what trait did this person show?",
                    "steps": [
                        "The child studies a figure through an honest biography and a biography card",
                        "The child names the figure's character traits and finds the evidence in their life",
                        "The child places the figure on the timeline and presents their life, the achievements and the flaws together",
                    ],
                },
                "control_of_error": "The biography itself is the control: a trait claimed for a figure must be supported by something they truly did, and the timeline checks the placement, so the child's account is held to the evidence of the real life.",
                "abstraction_pathway": "From studying concrete biography cards and portraits, to naming traits with evidence and placing figures on the timeline, toward grasping how the choices of individuals shape the whole course of history.",
                "extensions": [
                    "Compare figures from different times and cultures and the traits they share",
                    "Research a lesser-known figure and present their life",
                    "Weigh a figure who did both great and harmful things, and discuss the complexity honestly",
                ],
                "observation_focus": "Watch for the child supporting a named trait with real evidence, and seeing a historical figure whole, neither idol nor villain but a real and complicated person.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a rich shelf of biographies of all sorts of people, from many times and places",
                    "Leave out costume props and materials for the child to act out or present a life",
                    "Have documentaries and films about real historical figures available",
                ],
                "real_world_contexts": [
                    "Hearing the life stories of grandparents and elders, the family's own historical figures",
                    "Meeting real people whose work the child admires, and learning their stories",
                    "Discovering, in books, films, and museums, the lives behind the famous names",
                    "Noticing the same character traits, courage, perseverance, kindness, in real people the child knows",
                ],
                "conversation_starters": [
                    "What character trait best describes this person? What did they do that shows it?",
                    "This person faced a hard choice; what would you have done?",
                    "This person did both admirable things and harmful things; how do you hold both together?",
                ],
                "resource_bank": [
                    "A wide shelf of honest biographies for children",
                    "Documentaries and films about historical figures",
                    "The family's own elders and their life stories",
                ],
                "parent_role": "Follow the child's admiration for particular people into their life stories, told honestly, the courage and the flaws together, and wonder aloud about the choices each one made. Welcome the child's own judgments, and let real lives, honestly met, rather than a worksheet, teach what character is.",
                "observation_documentation": "Over time, note whether the child can narrate biographies, name character traits with evidence, see how a person's choices shaped events, and meet historical figures honestly as whole people. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Biographies build reading comprehension, vocabulary, and narrative skills simultaneously",
            "math": "Timeline math: how many years between two figures? How long ago did they live?",
            "science": "Many historical figures were scientists or inventors: Franklin, da Vinci, Archimedes. Their biographies are science stories too.",
        },
    },
    "hf-13": {
        "enriched": True,
        "learning_objectives": [
            "Explain the historical origins of at least 5 major holidays",
            "Connect each holiday to the event, person, or idea it commemorates",
            "Describe how celebrations and traditions help communities remember important events",
            "Place holidays on the annual calendar and on the historical timeline",
        ],
        "teaching_guidance": {
            "introduction": "Holidays are living history. Every time we celebrate the Fourth of July, Thanksgiving, or Martin Luther King Jr. Day, we are remembering a real event or a real person from the past. Holidays are how communities say 'this matters — we must never forget.' Understanding WHY we celebrate transforms holidays from days off into days of meaning. For a homeschool family, holidays are natural history lessons that arrive on the calendar year after year.",
            "scaffolding_sequence": [
                "Start with the next holiday on the calendar: 'Do you know WHY we celebrate this day? Let's find out.'",
                "Tell the origin story of a familiar holiday: the Fourth of July celebrates when America declared independence in 1776",
                "Compare a civic holiday (Memorial Day — remembering soldiers) with a cultural holiday (Thanksgiving — giving thanks for the harvest)",
                "Study the origins of 5 holidays: Independence Day, Thanksgiving, Presidents' Day, Memorial Day, Martin Luther King Jr. Day",
                "Discuss how OTHER countries have holidays for different reasons — holidays reflect what a culture values",
                "Place each holiday's origin event on the historical timeline: 'Thanksgiving started in 1621. That's before the Revolution.'",
                "Discuss how holiday traditions change over time: Thanksgiving didn't become a national holiday until 1863",
                "The child creates a 'Holiday History Book' with a page for each holiday showing its origin, date, and how the family celebrates it",
            ],
            "socratic_questions": [
                "Why do you think communities create holidays? What purpose do they serve?",
                "Memorial Day honors soldiers who died. Why is it important to remember people who sacrificed for others?",
                "Thanksgiving was about the Pilgrims and Wampanoag sharing a harvest meal. What does that tell us about what the holiday is really about?",
                "If you could create a new holiday, what event or person would it celebrate? Why?",
            ],
            "practice_activities": [
                "Holiday origin research: for the next upcoming holiday, research its origin and present the story to the family",
                "Holiday timeline: create a year-long calendar strip showing when each holiday falls and its origin date",
                "Holiday comparison: compare how two different holidays celebrate similar ideas (Memorial Day and Veterans Day both honor soldiers but in different ways)",
                "Create a holiday: the child invents a family holiday commemorating something meaningful to them, with traditions and a date",
            ],
            "real_world_connections": [
                "Every holiday has decorations, foods, and traditions — these are cultural artifacts that carry meaning from the past",
                "Community celebrations (parades, fireworks, gatherings) show how history becomes a shared, lived experience",
                "Family traditions during holidays connect the child to their own family's history and values",
                "Different families celebrate the same holiday differently — traditions are diverse even within one community",
            ],
            "common_misconceptions": [
                "Thinking holidays have always existed in their current form — most holidays evolved over centuries. Thanksgiving wasn't a national holiday until Abraham Lincoln declared it in 1863.",
                "Believing holidays are just days off from work or school — each has a deeper meaning rooted in historical events or values",
                "Assuming everyone celebrates the same holidays — different cultures, religions, and countries have different holidays reflecting their own histories",
                "Romanticizing holiday origins — the first Thanksgiving was a complex event between cultures with very different power dynamics, not a simple happy gathering",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Explains the origin of 5 holidays with specific historical details",
                "Connects each holiday to the event or person it commemorates",
                "Describes how celebrations preserve historical memory",
            ],
            "proficiency_indicators": [
                "Explains origins of 3-4 holidays",
                "Makes basic connections between holidays and their origins",
            ],
            "developing_indicators": [
                "Knows when holidays occur but not why",
                "Cannot explain the historical origin of holidays",
            ],
            "assessment_methods": [
                "oral explanation of origins",
                "holiday timeline",
                "connection to historical events",
            ],
            "sample_assessment_prompts": [
                "Why do we celebrate the Fourth of July? What happened on that day?",
                "Which holiday remembers soldiers who died serving their country?",
                "Tell me the origin story of Thanksgiving.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What does the Fourth of July celebrate?",
                "expected_type": "multiple_choice",
                "options": [
                    "The end of the Civil War",
                    "The signing of the Declaration of Independence",
                    "George Washington's birthday",
                    "The first Thanksgiving",
                ],
                "correct_answer": "The signing of the Declaration of Independence",
                "hints": ["It happened in 1776. America declared itself free from British rule."],
                "explanation": "The Fourth of July celebrates the adoption of the Declaration of Independence on July 4, 1776 — the day America officially declared its independence from Britain.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which holiday honors the memory of Dr. Martin Luther King Jr.?",
                "expected_type": "text",
                "correct_answer": "Martin Luther King Jr. Day",
                "hints": ["This holiday is in January. It celebrates a civil rights leader who dreamed of equality."],
                "explanation": "Martin Luther King Jr. Day, celebrated on the third Monday of January, honors Dr. King's life and his work fighting for civil rights and equality through nonviolent protest.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: Thanksgiving has always been a national holiday in the United States.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["The Pilgrims' feast was in 1621. When do you think it became an official holiday?"],
                "explanation": "False. The first harvest feast between Pilgrims and Wampanoag was in 1621, but Thanksgiving didn't become an official national holiday until 1863, when President Abraham Lincoln declared it during the Civil War.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Why do communities create holidays? What purpose do they serve?",
                "expected_type": "text",
                "hints": ["Think about: remembering, honoring, celebrating, bringing people together."],
                "explanation": "Holidays serve to remember important events and people, honor sacrifices, celebrate shared values, and bring communities together. They ensure that important history is not forgotten — each generation passes the memory to the next.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "If you could create a new holiday, what would it celebrate? Why? What traditions would it have?",
                "expected_type": "text",
                "hints": [
                    "Think about something important that deserves to be remembered. What event, person, or value would your holiday honor?"
                ],
                "explanation": "A thoughtful answer names something meaningful (a family event, a historical figure, a value like kindness), explains why it deserves a holiday, and describes how it would be celebrated. This demonstrates understanding that holidays are created to preserve what a community values most.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Name 5 holidays and explain what each one commemorates.",
                "type": "open_response",
                "target_concept": "holiday_origins",
                "rubric": "Mastery: 5 holidays with accurate origins. Proficient: 3-4 with origins. Developing: names holidays but not origins.",
            },
            {
                "prompt": "How do holiday celebrations help us remember history?",
                "type": "open_response",
                "target_concept": "memory_preservation",
                "rubric": "Mastery: explains how traditions preserve memory with examples. Proficient: general explanation. Developing: cannot connect.",
            },
        ],
        "resource_guidance": {
            "required": ["calendar showing major holidays", "books about holiday origins"],
            "recommended": ["family traditions journal", "historical photographs of holiday celebrations"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Holiday stories are ideal for oral retelling. Use holiday-themed picture books. Create a visual holiday calendar with images rather than text.",
            "adhd": "Study each holiday as it approaches naturally. Cooking traditional foods is hands-on. Holiday crafts connected to origins. Short focused sessions on one holiday at a time.",
            "gifted": "Research how the same holiday is celebrated differently around the world. Investigate holidays that have been discontinued and why. Create a family history holiday celebrating an ancestor.",
            "visual_learner": "Holiday photo collections. Illustrated timeline of holiday origins. Decorated calendar.",
            "kinesthetic_learner": "Cook traditional foods. Make holiday crafts. Act out origin stories.",
            "auditory_learner": "Hear holiday origin stories told aloud. Sing patriotic songs. Discuss holiday meanings in conversation.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Holidays are living history. Every Fourth of July, Thanksgiving, or Martin Luther King Jr. Day remembers a real event or a real person, and a holiday is how a community says, this matters, we must not forget. Some holiday stories are remembered simply, but the true history behind them is often fuller: the first Thanksgiving was a real harvest feast shared by the Plymouth colonists and the Wampanoag, and the longer history between the English settlers and the Wampanoag was also marked by sickness, lost land, and war. Today we learn the origins of at least five holidays, connect each to what it commemorates, and place them on the calendar and the timeline, telling the histories truthfully.",
                "gradual_release": {
                    "i_do": "Take a holiday and tell its origin in order: what happened, when, and why it is remembered. For Thanksgiving, tell the real harvest feast of 1621, and tell honestly that the wider story between the settlers and the Wampanoag held hardship and conflict as well. Place the holiday on the calendar and on the historical timeline.",
                    "we_do": "Study the origins of several holidays together, connect each to the event or person it commemorates, and place each on the calendar and the timeline.",
                    "you_do": "Child explains the origins of at least five holidays, connects each to what it commemorates, describes how celebrations preserve memory, and places the holidays on the calendar and the timeline.",
                },
                "guided_practice": [
                    "Tell the origin story of a holiday: the event or person, the date, and why it is remembered",
                    "Connect each holiday studied to the event, person, or idea it commemorates",
                    "Place each holiday on the annual calendar and on the historical timeline",
                ],
                "independent_practice": [
                    "Research the origin of an upcoming holiday and present it to the family",
                    "Make a Holiday History Book with a page for each holiday's origin, date, and family traditions",
                ],
                "mastery_check": [
                    "Explain the historical origins of at least five major holidays",
                    "Connect each holiday to the event, person, or idea it commemorates",
                    "Describe how celebrations and traditions help communities remember important events",
                ],
                "spiral_review": [
                    "Revisit the historical timeline, placing each holiday's origin event in its true spot",
                ],
            },
            "classical": {
                "narrative_introduction": "A holiday is a community's act of memory: a day set apart so that an event or a person from the past is not forgotten. The classical mind asks of each holiday, what is the true history beneath it, and tells that history honestly. Some holidays carry simple stories that the fuller record makes more complex, as the harvest feast of the Plymouth colonists and the Wampanoag stands within a longer and harder history between those peoples. To know a holiday well is to know the real events it marks.",
                "memory_work": {
                    "chants": [
                        "Chant the holidays and what each marks: Independence Day the Declaration, Thanksgiving a harvest, Memorial Day the fallen soldiers, Presidents' Day the leaders, Martin Luther King Jr. Day the work for equal rights",
                        "Chant the purpose of a holiday: to remember, to honor, and to hand the memory on",
                    ],
                    "recitations": [
                        "Recite that a holiday marks a real event or person, and that the honest student learns the true history beneath the celebration",
                    ],
                },
                "copywork": [
                    "Copy the names of several holidays beside their dates and the events they commemorate",
                ],
                "recitation_routine": "Begin each lesson by reciting the holidays studied and what each one marks before any new study.",
                "history_integration": "Place each holiday's origin event on the chronological spine, so the child sees that Thanksgiving's harvest feast, the Declaration of Independence, and the work of Dr. King fall at very different points along the long story of history.",
                "read_aloud_suggestions": [
                    "A living account of the true origin of a holiday, told honestly with its fuller history",
                    "A children's history of a holiday and the people, all of them, whose story it marks",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A beautifully illustrated living book about the true origin of a holiday, honest about the fuller history rather than a tidy legend",
                    "A living book that tells, truthfully, the story of the peoples behind a holiday such as Thanksgiving",
                ],
                "short_lesson_flow": "Let the calendar set the lesson: as a holiday draws near, read its true origin story aloud, and let the child narrate it back. Tell the history honestly, the harvest feast and also the harder history between the settlers and the Wampanoag, and let the child sit with the whole of it. Mark the day, and keep the family's own traditions gladly.",
                "narration_prompt": "Tell me the real story behind this holiday. What does it remember, and what is the fuller history beneath it?",
                "real_world_objects": [
                    "The calendar, with the holidays marked through the year",
                    "A Book of Centuries where each holiday's origin event is placed",
                    "The family's own holiday traditions, foods, decorations, and gatherings",
                    "Living books and historical pictures of holiday celebrations",
                ],
                "nature_connection": "Notice that many holidays follow the turning year, the harvest of Thanksgiving, the seasons of planting and gathering, so that the calendar of holidays is woven into the calendar of nature.",
                "habit_focus": "The habit of attention and of truthfulness: learning the real history a holiday marks, the glad parts and the hard parts together.",
            },
            "montessori": {
                "prepared_materials": [
                    "A holiday calendar with movable cards for the year's holidays",
                    "Cultural and civic celebration folders with photographs and honest origin accounts",
                    "A timeline for placing each holiday's origin event",
                    "Materials for the child to research and present a holiday's history",
                ],
                "presentation": {
                    "three_period_lesson": "With the holiday cards: this is Independence Day, marking the Declaration of Independence; show me Independence Day; which holiday is this, and what does it mark?",
                    "steps": [
                        "The child places the year's holidays on the calendar and learns what each one marks",
                        "The child studies the true origin of a holiday through an honest account, including its fuller history",
                        "The child places each holiday's origin event on the timeline and presents what they learned",
                    ],
                },
                "control_of_error": "The calendar and the timeline are the control: a holiday placed on the wrong date or its origin set in the wrong era does not match the record, and an account that tells only a tidy legend is checked against the honest history and found incomplete.",
                "abstraction_pathway": "From handling the concrete holiday cards and calendar, to studying the true origin of each holiday, toward grasping that holidays are a community's way of keeping real history in living memory.",
                "extensions": [
                    "Research how the same holiday is kept differently in different families and places",
                    "Investigate the fuller history behind a holiday's familiar story",
                    "Compare a civic holiday and a cultural holiday and what each preserves",
                ],
                "observation_focus": "Watch for the child connecting each holiday to the real event it marks, and meeting the fuller history honestly rather than resting on a simple legend.",
            },
            "unschooling": {
                "invitations": [
                    "Keep books about the true origins of holidays within reach",
                    "Mark the year's holidays on a family calendar to wonder about as each draws near",
                    "Have the family's own holiday traditions, foods, and stories alive in the home",
                ],
                "real_world_contexts": [
                    "Keeping the family's holidays and asking, as each comes, what it truly marks and for whom",
                    "Noticing the decorations, foods, and traditions of a holiday and where they came from",
                    "Hearing how grandparents and elders kept the same holidays in their day",
                    "Seeing how friends and neighbors of different backgrounds keep different holidays",
                ],
                "conversation_starters": [
                    "Why do you think people set aside a whole day to remember this?",
                    "The Thanksgiving story is often told simply; the real history between the settlers and the Wampanoag was fuller and harder. What do you make of that?",
                    "If you could make a holiday, what would it remember, and how would you keep it?",
                ],
                "resource_bank": [
                    "Books and documentaries about the true origins of holidays",
                    "A family calendar marking the year's holidays",
                    "The family's own elders, traditions, and stories",
                ],
                "parent_role": "As each holiday comes round, wonder aloud with the child about what it truly marks, and tell its origin honestly, the glad parts and the hard parts alike, as with the fuller history behind Thanksgiving. Keep the family's traditions with joy, share the documented history openly, and let the child reason about its meaning rather than handing them a tidy verdict.",
                "observation_documentation": "Over time, note whether the child knows the origins of the holidays the family keeps, connects each to what it marks, and can meet the fuller history honestly. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Holiday books build reading skills. Origin stories are compelling narratives for narration practice.",
            "math": "Calendar math: how many days until the next holiday? How many years since the first Thanksgiving?",
            "science": "Harvest festivals connect to agricultural science. Solstice holidays connect to astronomy and Earth's tilt.",
        },
    },
    "hf-14": {
        "enriched": True,
        "learning_objectives": [
            "Describe daily life in at least 3 different cultures around the world: food, housing, clothing, and customs",
            "Identify universal human needs (food, shelter, community, stories) shared across all cultures",
            "Show curiosity and respect toward unfamiliar traditions and ways of life",
            "Locate the cultures studied on a world map",
        ],
        "teaching_guidance": {
            "introduction": "People around the world eat different foods, wear different clothes, build different homes, tell different stories, and celebrate in different ways — but underneath all that diversity, every culture is solving the same basic problems: how to feed people, how to shelter them, how to raise children, how to live together, and how to make meaning out of life. Studying world cultures builds both knowledge and empathy. The child discovers that 'different' does not mean 'wrong' and that every culture has beauty, wisdom, and something to teach us.",
            "scaffolding_sequence": [
                "Start with the child's own culture: 'What do we eat? What does our home look like? What holidays do we celebrate? These are OUR cultural traditions.'",
                "Study a culture from a different continent: what do families eat, where do they live, what do children do, what stories do they tell?",
                "Study a second culture from yet another continent: expand the child's understanding that culture varies enormously",
                "Study a third culture: by now the child sees both the diversity and the shared humanity",
                "Identify universal needs: every culture has food traditions, shelter, family structures, stories/music, and celebrations",
                "Discuss respect: 'When something seems strange to us, it's normal to someone else. How would we feel if someone called OUR traditions strange?'",
                "Locate each culture on the world map — geography and culture are connected",
                "Compare: what do all these cultures have in common? What makes each one unique?",
            ],
            "socratic_questions": [
                "People in Japan take off their shoes before entering a house. Why might they do that? Do we have similar customs?",
                "Every culture has stories they tell children. Why do you think stories are so important to EVERY group of people?",
                "People in different places eat very different foods. But what does EVERY culture need food to do? What's universal?",
                "If a child from another country visited your home, what would seem normal to you but surprising to them?",
            ],
            "practice_activities": [
                "World culture dinner: cook a simple meal from another culture and learn about the food traditions behind it",
                "Culture comparison chart: for 3 cultures, list food, housing, clothing, games, and celebrations in columns and compare",
                "Cultural story time: read a folktale from another culture and discuss what it teaches about that culture's values",
                "Pen pal project (or imaginary): write a letter to an imaginary child in another country describing your daily life and asking about theirs",
            ],
            "real_world_connections": [
                "The food in your kitchen comes from many cultures: pasta (Italy), tacos (Mexico), stir-fry (China), curry (India). Culture is already in your home.",
                "Music from around the world is available to listen to: African drumming, Indian sitar, Irish fiddle, Japanese koto. Each sound carries culture.",
                "Your neighborhood probably includes people from different cultural backgrounds — each family brings traditions from their heritage",
                "Fairy tales and folk stories from around the world share themes: heroes, villains, cleverness, kindness. Stories connect all humans.",
            ],
            "common_misconceptions": [
                "Thinking other cultures are 'weird' or 'backward' — every culture's traditions make sense in context and deserve respect",
                "Believing one culture is 'better' than others — cultures are different, not ranked. Each has strengths and challenges.",
                "Assuming people in other countries all live the same way — there is as much diversity within a country as between countries",
                "Thinking cultural traditions are fixed and unchanging — cultures evolve over time, borrowing and adapting from each other",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Describes daily life in 3 cultures with specific details about food, housing, and customs",
                "Identifies universal human needs shared across cultures",
                "Shows curiosity and respect in discussing unfamiliar traditions",
            ],
            "proficiency_indicators": [
                "Describes 1-2 cultures with some details",
                "Recognizes that people are different but may not articulate universal needs",
            ],
            "developing_indicators": [
                "Knows that other cultures exist but cannot describe them",
                "May express that different traditions are 'weird' rather than showing curiosity",
            ],
            "assessment_methods": ["culture description", "comparison chart", "map placement"],
            "sample_assessment_prompts": [
                "Tell me about daily life in a culture different from ours.",
                "What do ALL cultures have in common, even when their traditions are very different?",
                "Show me on the map where the cultures we studied are located.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which of these is something ALL cultures share?",
                "expected_type": "multiple_choice",
                "options": [
                    "Everyone eats pizza",
                    "Every culture has food traditions",
                    "Everyone speaks English",
                    "All houses look the same",
                ],
                "correct_answer": "Every culture has food traditions",
                "hints": ["Every group of people needs to eat. But do they all eat the same things?"],
                "explanation": "Every culture has food traditions — ways of growing, preparing, and sharing food. But the specific foods vary enormously: rice in Asia, tortillas in Mexico, bread in Europe, injera in Ethiopia.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Why is it important to learn about other cultures?",
                "expected_type": "text",
                "hints": [
                    "Think about: understanding, respect, learning new things, seeing the world through different eyes."
                ],
                "explanation": "Learning about other cultures helps us understand that there are many good ways to live, builds respect for people who are different from us, and teaches us new ideas. It also shows us what all humans share despite our differences.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Name one way your family's daily life is similar to a family in another country, and one way it is different.",
                "expected_type": "text",
                "hints": [
                    "Think about meals, homes, school, play, celebrations. What do families everywhere do? What varies?"
                ],
                "explanation": "Good answers identify both a similarity (all families eat meals together, all children play) and a difference (foods differ, homes look different, celebrations vary). This shows understanding that cultures are both universal and unique.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: People in all countries live the same way.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": [
                    "Think about the different cultures you've learned about. Do they all eat the same food? Live in the same kind of homes?"
                ],
                "explanation": "False. People around the world have incredibly diverse ways of living: different foods, homes, clothing, languages, and traditions. But they all share basic human needs: food, shelter, family, community, and stories.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Choose a culture from another part of the world. Describe what daily life is like for a child there: what they eat, where they live, what they do for fun, and one tradition their family has.",
                "expected_type": "text",
                "hints": [
                    "Pick a culture you've studied or are curious about. Describe a typical day for a child living there."
                ],
                "explanation": "A rich answer includes specific details, not generalizations. Example for Japan: 'A child in Japan might eat rice and miso soup for breakfast. They live in a home where they take off shoes at the door. After school, they might practice calligraphy or play with friends. Their family celebrates New Year by cleaning the house and eating special foods.' Specific details show real understanding.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Describe daily life in a culture different from yours. Include food, housing, and customs.",
                "type": "open_response",
                "target_concept": "cultural_description",
                "rubric": "Mastery: specific details about food, housing, and customs. Proficient: general description. Developing: vague or stereotypical.",
            },
            {
                "prompt": "What do all cultures share? What makes each one unique?",
                "type": "open_response",
                "target_concept": "universal_vs_unique",
                "rubric": "Mastery: identifies universals AND specifics. Proficient: identifies one. Developing: cannot articulate.",
            },
        ],
        "resource_guidance": {
            "required": ["world map or globe", "books about daily life in other cultures"],
            "recommended": ["cooking supplies for international recipes", "music from different cultures"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Picture books and documentaries about world cultures. Cooking and tasting are multisensory, not text-dependent. Oral discussion is the primary mode.",
            "adhd": "Cook international foods (hands-on). Listen to world music and dance. Each culture studied in a separate 15-minute session. Art projects inspired by cultural traditions.",
            "gifted": "Research a culture in depth: language basics, history, art, and geography. Compare cultural responses to the same human need (how do 5 cultures celebrate a new baby?). Explore cultural exchange and how cultures influence each other.",
            "visual_learner": "Photographs of daily life worldwide. Illustrated books. Cultural artifact pictures.",
            "kinesthetic_learner": "Cook, dance, build models of different types of housing. Hands-on cultural experiences.",
            "auditory_learner": "Listen to music and stories from each culture. Discuss cultural practices. Audio documentaries.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "People around the world eat different foods, build different homes, wear different clothes, and keep different customs, yet every culture is meeting the same human needs: to feed and shelter its people, to raise its children, to live together, and to make meaning. Studying world cultures builds both knowledge and respect. Each culture has its own beauty and wisdom, and each is made of real people; none stands above or below another. Today we describe daily life in at least three cultures, name the universal human needs all cultures share, locate the cultures on a world map, and meet unfamiliar ways of life with curiosity and respect.",
                "gradual_release": {
                    "i_do": "Start with our own culture and think aloud: our food, our home, our customs. Then describe daily life in a culture from another continent, the food, the housing, the clothing, the customs, plainly and respectfully. Name the universal need beneath each, and locate the culture on the map. Show that different does not mean wrong.",
                    "we_do": "Describe daily life in cultures together, build a comparison chart of food, housing, clothing, and customs, name the universal needs all share, and locate each culture on the world map.",
                    "you_do": "Child describes daily life in at least three cultures, identifies the universal human needs all cultures share, locates the cultures on a world map, and discusses unfamiliar traditions with curiosity and respect.",
                },
                "guided_practice": [
                    "Describe daily life in a culture: food, housing, clothing, and customs",
                    "Name the universal human need beneath a custom from another culture",
                    "Locate the cultures studied on a world map",
                ],
                "independent_practice": [
                    "Make a comparison chart of daily life across three cultures",
                    "Cook a meal, read a folktale, or learn a custom from another culture, and describe what it shows about that culture",
                ],
                "mastery_check": [
                    "Describe daily life in at least three cultures, with specific details of food, housing, clothing, and customs",
                    "Identify the universal human needs shared across all cultures",
                    "Locate the cultures studied on a world map and discuss unfamiliar traditions with curiosity and respect",
                ],
                "spiral_review": [
                    "Revisit the world map and the continents, placing each culture studied in its true location",
                ],
            },
            "classical": {
                "narrative_introduction": "The world holds a great many cultures, and the classical mind studies them with both knowledge and a fair and curious eye. Beneath all the variety of food, dress, shelter, and custom, every culture is answering the same human questions: how to feed its people, how to shelter and raise them, how to live together, and how to make meaning. Each culture has its own beauty and its own wisdom, and each is made of real people; the honest student ranks none above another and idealizes none.",
                "memory_work": {
                    "chants": [
                        "Chant the universal human needs every culture meets: food and shelter, family and community, and stories that carry meaning",
                        "Chant the fair-minded rule: different is not wrong, and every culture has both beauty and wisdom",
                    ],
                    "recitations": [
                        "Recite that all cultures share the same human needs, and that each one meets them in its own way, none above and none below",
                    ],
                },
                "copywork": [
                    "Copy the universal human needs all cultures share, and the names of the cultures studied beside their continents",
                ],
                "recitation_routine": "Begin each lesson by reciting the universal human needs before studying a new culture.",
                "history_integration": "Place the cultures studied across both the map and the chronological spine, and mark that the great civilizations the child has met, Egypt, China, Greece, Rome, were themselves cultures meeting these same human needs, each in its own way and its own age.",
                "read_aloud_suggestions": [
                    "A living book that shows the daily life of a family in another culture, told with knowledge and respect",
                    "A collection of folktales from around the world, read aloud so the child meets each culture through its own stories",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A beautifully illustrated living book about the daily life of a family in another culture, with true artwork and real respect",
                    "A finely told collection of folktales from the cultures studied, each culture met through its own stories",
                ],
                "short_lesson_flow": "Let the child meet a culture, not merely read about it: cook one of its foods, hear its music, read one of its folktales, look long at pictures of its homes and daily life. Then the child narrates what they have learned. Wonder together at what is the same and what is different, and meet every custom with curiosity and respect.",
                "narration_prompt": "Tell me about the daily life of a child in the culture we met. What is the same as your life, and what is different?",
                "real_world_objects": [
                    "A globe or world map for locating each culture",
                    "Real foods, music, and objects from the cultures studied",
                    "Living books and folktale collections from around the world",
                    "A Book of Centuries or notebook for the child's drawn records of each culture",
                ],
                "nature_connection": "Notice how the land and climate shape a culture: the homes, foods, and clothing of a desert people, a mountain people, an Arctic people, each fitted to the natural world they live in.",
                "habit_focus": "The habit of attention and of respect: looking closely and kindly at a way of life unlike one's own, with curiosity rather than judgment.",
            },
            "montessori": {
                "prepared_materials": [
                    "Continent folders with photographs, flags, and cultural artifacts",
                    "Real objects, foods, and music from the cultures studied",
                    "A globe and pin map for locating each culture",
                    "A comparison work for daily life across cultures: food, housing, clothing, customs",
                ],
                "presentation": {
                    "three_period_lesson": "With the continent folders: this is a home from this culture; show me a home from this culture; which culture's daily life is this?",
                    "steps": [
                        "The child explores a culture's continent folder and its real objects, foods, and music",
                        "The child locates the culture on the globe and pin map",
                        "The child compares the daily life of several cultures and names the universal needs each one meets",
                    ],
                },
                "control_of_error": "The globe and the continent folders are the control: a culture pinned to the wrong place does not match the map, and the comparison work shows the child plainly when a universal need has been left out of an account.",
                "abstraction_pathway": "From handling the concrete continent folders and real cultural objects, to comparing the daily life of several cultures, toward grasping that all cultures meet the same human needs, each in its own way.",
                "extensions": [
                    "Study a single culture in depth: its language, art, geography, and history",
                    "Compare how several cultures each meet one human need, such as welcoming a new baby",
                    "Investigate how cultures borrow from and influence one another over time",
                ],
                "observation_focus": "Watch for the child describing a culture with specific, accurate detail, meeting unfamiliar customs with curiosity rather than judgment, and seeing the shared human needs beneath the variety.",
            },
            "unschooling": {
                "invitations": [
                    "Keep books, folktales, music, and films from many cultures within reach",
                    "Leave out cooking materials for trying foods from around the world",
                    "Have a globe and an atlas available for the curious",
                ],
                "real_world_contexts": [
                    "Eating foods from many cultures, the family's own and others', and learning where each comes from",
                    "Hearing music and stories from around the world",
                    "Meeting people of different backgrounds in the neighborhood and community",
                    "Noticing the customs of friends, neighbors, and relatives, and asking about them with interest",
                ],
                "conversation_starters": [
                    "A custom from another culture can seem strange to us; how do you think one of our customs might seem to them?",
                    "People everywhere need food, shelter, family, and stories; why do you think they meet those needs so differently?",
                    "What is something you have learned from another culture that you would like to try?",
                ],
                "resource_bank": [
                    "Books, folktales, music, and films from many cultures",
                    "Cooking materials for foods from around the world",
                    "A globe and atlas, and the family's own and neighbors' traditions",
                ],
                "parent_role": "Follow the child's curiosity about other ways of life into food, music, stories, and real friendships, and wonder aloud at both the variety and the shared humanity. Meet every culture with respect, neither ranking one above another nor idealizing any, and let real experience, rather than a worksheet, teach the child about the wider world.",
                "observation_documentation": "Over time, note whether the child can describe daily life in different cultures, sees the universal needs all cultures share, locates them on a map, and meets unfamiliar ways of life with curiosity and respect. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Folktales from around the world build reading and comprehension. Cultural vocabulary expands language.",
            "math": "Different cultures developed different number systems. Counting in another language. Currency comparison.",
            "science": "How geography and climate shape culture: Arctic peoples, desert peoples, tropical peoples all adapted to their environment.",
        },
    },
    "hf-15": {
        "enriched": True,
        "learning_objectives": [
            "Prepare at least 5 thoughtful interview questions for an oral history conversation",
            "Conduct a simple interview with a grandparent, elder, or community member and retell their story",
            "Explain why personal memories and stories are valuable sources of history",
            "Compare oral history to written history and describe the strengths of each",
        ],
        "teaching_guidance": {
            "introduction": "History is not only found in books — it lives in the memories of people around us. Grandparents remember what life was like decades ago. Neighbors remember events that shaped the community. These personal stories ARE history, and the child can be the one to collect and preserve them. Oral history turns the child into a historian: they prepare questions, listen carefully, and retell what they heard. This is one of the most powerful homeschool activities because it connects the child to their own family and community while teaching real historical thinking skills.",
            "scaffolding_sequence": [
                "Discuss what oral history is: 'Before writing existed, ALL history was oral — stories told from person to person. We can still do this today.'",
                "Model interviewing: the parent interviews the child about a memorable event. Show how good questions bring out interesting answers.",
                "Prepare for an interview together: help the child write 5 questions for a grandparent or older family member",
                "Teach good interview skills: listen carefully, don't interrupt, ask follow-up questions like 'What happened next?' and 'How did that make you feel?'",
                "Conduct the interview: the child asks questions and the parent helps record (write down or audio record) the answers",
                "Retell the story: the child narrates what they learned from the interview",
                "Discuss: 'Why is this person's memory important? What would be lost if no one ever asked them about their life?'",
                "Compare: how is hearing someone's story different from reading about an event in a book? What are the advantages of each?",
            ],
            "socratic_questions": [
                "What do you want to know about Grandma's childhood that you can't find in a book?",
                "Why might someone's memory of an event be different from what a history book says? Does that make it less valuable?",
                "What would happen to all of Grandpa's stories if nobody ever asked him to tell them?",
                "How is listening to someone's story different from reading a book about the same topic?",
            ],
            "practice_activities": [
                "Family interview: interview a grandparent or older relative about their childhood. Record or write down 3 stories they share.",
                "Question crafting workshop: practice writing open-ended questions (not yes/no) that will produce interesting stories",
                "Retelling practice: after the interview, the child retells the best story to someone who wasn't there",
                "Family history book: compile interview stories into a simple book with drawings and the interviewee's words",
            ],
            "real_world_connections": [
                "Every family has stories that no book contains — the only way to preserve them is to ask and listen",
                "Oral history is used by professional historians: interviews with World War II veterans, civil rights activists, and immigrants preserve memories that written records miss",
                "Podcasts and documentaries often use oral history: people telling their own stories in their own words",
                "Community elders carry knowledge about local history that may not be written down anywhere",
            ],
            "common_misconceptions": [
                "Thinking only 'important' people have stories worth recording — everyone's life experiences contain history",
                "Believing memory is perfectly accurate — memories can be incomplete or shaped by time, but they are still valuable as personal perspectives",
                "Assuming oral history is less valid than written history — oral accounts provide detail, emotion, and perspective that documents often lack",
                "Thinking interviews are easy — good interviewing requires preparation, patience, and genuine curiosity",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Prepares 5+ thoughtful, open-ended interview questions",
                "Conducts an interview and retells the story coherently",
                "Explains why personal memories are valuable historical sources",
            ],
            "proficiency_indicators": [
                "Prepares 3-4 questions, some of which are open-ended",
                "Retells the interview story with help from notes",
            ],
            "developing_indicators": [
                "Prepares only yes/no questions",
                "Cannot retell the interview story without significant prompting",
            ],
            "assessment_methods": ["question quality review", "interview observation", "story retelling"],
            "sample_assessment_prompts": [
                "Show me the questions you prepared. Which one do you think will get the best story?",
                "Tell me what you learned from your interview.",
                "Why are Grandma's stories important even if they're not in any history book?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which is a better interview question?",
                "expected_type": "multiple_choice",
                "options": [
                    "Did you like school? (yes/no)",
                    "What was school like when you were my age? Tell me about a day you remember.",
                    "Was your childhood good?",
                    "Do you remember anything?",
                ],
                "correct_answer": "What was school like when you were my age? Tell me about a day you remember.",
                "hints": ["Good interview questions invite the person to TELL A STORY, not just say yes or no."],
                "explanation": "Open-ended questions that invite stories produce the best oral history. 'What was school like?' invites a detailed answer. 'Did you like school?' only gets yes or no.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is oral history?",
                "expected_type": "text",
                "hints": ["Think about where the word 'oral' comes from — it relates to speaking and listening."],
                "explanation": "Oral history is history collected by listening to people tell their own stories. Instead of reading about events in a book, you hear about them from someone who experienced them. It preserves memories that might otherwise be lost.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Write 3 interview questions you would ask a grandparent about their childhood.",
                "expected_type": "text",
                "hints": [
                    "Make them open-ended: 'Tell me about...' or 'What was it like when...' Avoid yes/no questions."
                ],
                "explanation": "Good questions: 'What was your favorite thing to do as a child?' 'Tell me about the house you grew up in.' 'What is the biggest change you've seen in the world since you were young?' These invite stories, not one-word answers.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: Oral history is less important than written history because people's memories can be wrong.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": [
                    "Written records can have mistakes too. What does oral history provide that written records don't?"
                ],
                "explanation": "False. Oral history provides personal perspective, emotion, and details that written records often miss. Yes, memories can be imperfect, but they offer something unique: what it FELT like to live through an event, from the person who was there.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "After interviewing a family member, retell one story they shared. Include who it was about, when it happened, what happened, and why it matters.",
                "expected_type": "text",
                "hints": [
                    "Retell it as if you're telling a friend. Include the details that made the story interesting and meaningful."
                ],
                "explanation": "A good retelling captures the essence of the person's story: the setting, the events, the feelings, and why this memory mattered to them. This is the core skill of oral history: listening, understanding, and passing the story on.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Show me your interview questions and tell me what you learned from the interview.",
                "type": "open_response",
                "target_concept": "oral_history_practice",
                "rubric": "Mastery: 5+ open-ended questions and coherent retelling. Proficient: 3-4 questions and partial retelling. Developing: yes/no questions and vague retelling.",
            },
            {
                "prompt": "Why are personal stories important even when we have history books?",
                "type": "open_response",
                "target_concept": "oral_history_value",
                "rubric": "Mastery: explains personal perspective, emotion, and unique details. Proficient: says stories are important. Developing: cannot explain.",
            },
        ],
        "resource_guidance": {
            "required": [
                "paper and pencil for interview questions",
                "a willing interviewee (grandparent, neighbor, elder)",
            ],
            "recommended": [
                "audio recorder or phone for recording interviews",
                "family photo albums to prompt memories during interview",
            ],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 30, "assessment": 10},
        "accommodations": {
            "dyslexia": "Questions can be prepared orally or with parent scribing. The interview is entirely oral. Retelling is oral. No reading or writing required for the core activity.",
            "adhd": "The interview is a real-world social interaction — engaging and meaningful. Keep the interview to 15-20 minutes. The child can draw while listening. Movement break before retelling.",
            "gifted": "Interview multiple people about the same event and compare perspectives. Begin a family history research project. Introduce the concept of bias in historical accounts.",
            "visual_learner": "Use family photos during the interview to prompt stories. Draw scenes from the stories heard.",
            "kinesthetic_learner": "The act of interviewing IS active learning. Assemble a physical family history book afterward.",
            "auditory_learner": "Natural strength: listening to stories. Record the interview and play it back. Retelling is an oral performance.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "History is not found only in books; it lives in the memories of the people around us. Grandparents and elders remember what life was like decades ago, and those personal stories are real history. Oral history turns the child into a historian: they prepare good questions, listen carefully, and retell what they heard. Today we prepare at least five thoughtful interview questions, conduct an interview with a grandparent or elder, retell their story, explain why personal memories matter, and compare oral history with written history.",
                "gradual_release": {
                    "i_do": "Model an interview: ask the child open questions about a memory of their own, and show how a good open question, what was it like, what happened next, brings out a real story, while a yes-or-no question does not. Then write a few model questions and retell a short story honestly, just as it was told.",
                    "we_do": "Prepare interview questions together for a grandparent or elder, practice listening and asking follow-up questions, and retell a story afterward.",
                    "you_do": "Child prepares at least five thoughtful, open-ended questions, conducts an interview with an elder, retells their story, explains why personal memories are valuable history, and compares oral and written history.",
                },
                "guided_practice": [
                    "Write open-ended interview questions that invite a story rather than a yes or no",
                    "Practice listening well: ask follow-up questions and do not interrupt",
                    "Retell a story heard in an interview, faithfully, in the teller's spirit",
                ],
                "independent_practice": [
                    "Conduct a real interview with a grandparent or elder and record or write their answers",
                    "Compile interview stories into a simple family history book",
                ],
                "mastery_check": [
                    "Prepare at least five thoughtful, open-ended interview questions",
                    "Conduct an interview with an elder and retell their story coherently",
                    "Explain why personal memories are valuable history, and compare the strengths of oral and written history",
                ],
                "spiral_review": [
                    "Revisit retelling a story faithfully and in order, the skill the interview retelling depends on",
                ],
            },
            "classical": {
                "narrative_introduction": "Before there were books, all of history was oral: stories carried from voice to voice, from the old to the young. Oral history is that ancient practice still alive today. To interview an elder is to gather a primary source with one's own ears, to hear what it felt like to live through a time from the person who was there. The written record and the spoken memory each have their strengths, and the honest historian values both.",
                "memory_work": {
                    "chants": [
                        "Chant the work of the oral historian: prepare good questions, listen with care, and retell the story true",
                        "Chant the marks of a good question: it asks not yes or no, but tell me, and what was it like",
                    ],
                    "recitations": [
                        "Recite that oral history is gathered from those who were there, and that the spoken memory and the written record each have their own strengths",
                    ],
                },
                "copywork": [
                    "Copy the interview questions neatly before the interview, and a saying on how memory and the spoken word carry history",
                ],
                "recitation_routine": "Begin each lesson by reciting the work of the oral historian and recalling the story from the last interview before preparing the next.",
                "history_integration": "Mark that oral history reaches the most recent stretch of the chronological spine, the living memory of grandparents and elders, and that it joins the child's own family to the long story of history the spine records.",
                "read_aloud_suggestions": [
                    "A living account drawn from oral history, the remembered words of people who lived through an age, read aloud",
                    "A book in which an elder tells the story of their own life and times, read aloud for narration",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A living book in which a real person tells the story of their own life and times, the kind that shows what a remembered life sounds like",
                ],
                "short_lesson_flow": "The real lesson is a real conversation. Help the child prepare a few open questions, then sit them down with a grandparent or elder, unhurried, and let them ask and listen. Afterward, the child narrates the story they heard. Charlotte Mason's narration here is applied to a living primary source: a real person, remembering.",
                "narration_prompt": "Tell me the story you heard from your interview. What was the most surprising or moving thing the person remembered?",
                "real_world_objects": [
                    "A grandparent, elder, or community member willing to be interviewed",
                    "Paper for the child's prepared questions, and a recorder for the elder's own words",
                    "Family photo albums to bring out memories during the interview",
                    "A notebook for the family history the interviews build",
                ],
                "nature_connection": "Among the interview questions, include some about the natural world of the elder's childhood: the weather, the animals, the land, and how it has changed, so that memory becomes a record of nature too.",
                "habit_focus": "The habit of attention: listening so closely and respectfully to a person's story that it can be carried and told again.",
            },
            "montessori": {
                "prepared_materials": [
                    "A space and materials for preparing written interview questions",
                    "A recorder for capturing an elder's words",
                    "Family photographs to prompt memories",
                    "A family history notebook the child builds and keeps",
                ],
                "presentation": {
                    "three_period_lesson": "With question cards: this is an open question, it invites a story; show me an open question; is this question open or a yes-or-no question?",
                    "steps": [
                        "The child prepares open-ended interview questions and arranges them in order",
                        "The child conducts the interview, listening with care and asking follow-up questions",
                        "The child retells the elder's story and records it in the family history notebook",
                    ],
                },
                "control_of_error": "The interview itself is the control: a yes-or-no question is answered in a word and the child hears that it brought no story, so the child learns to ask the open question that does; the elder's own words, recorded, are the measure of a faithful retelling.",
                "abstraction_pathway": "From preparing and asking concrete questions of a real person, to retelling and recording their story, toward grasping oral history as a way of knowing the past that stands beside the written record.",
                "extensions": [
                    "Interview several people about the same time or event and compare what each remembers",
                    "Build an ongoing family history from many interviews",
                    "Compare an elder's memory of an event with a written account of it",
                ],
                "observation_focus": "Watch for the child asking open questions, listening without interrupting, and retelling the elder's story faithfully and with respect.",
            },
            "unschooling": {
                "invitations": [
                    "Keep recordings, photo albums, and a notebook handy for capturing family stories",
                    "Let real conversations with grandparents and elders be a welcome part of family life",
                    "Have books and podcasts of people telling their own life stories available",
                ],
                "real_world_contexts": [
                    "Asking grandparents and elders about their childhoods and the times they lived through",
                    "Listening to the family's own stories told at the table and on visits",
                    "Hearing neighbors and community elders tell of the local past",
                    "Meeting oral history in podcasts and documentaries where people tell their own stories",
                ],
                "conversation_starters": [
                    "What would you love to know about Grandma's life that no book could tell you?",
                    "Why might one person's memory of a day differ from a history book's account, and does that make it less worth hearing?",
                    "What would be lost if no one ever asked the elders to tell their stories?",
                ],
                "resource_bank": [
                    "Willing grandparents, elders, and community members",
                    "A recorder, photo albums, and a family history notebook",
                    "Podcasts and documentaries built from oral history",
                ],
                "parent_role": "Welcome the child into the family's real storytelling, and help them prepare good questions and sit with an elder to listen. Treat memory as the precious and human thing it is, gather the stories before they are lost, and let real interviews, rather than a worksheet, teach the child to be a historian.",
                "observation_documentation": "Over time, note whether the child asks open questions, listens with care, retells an elder's story faithfully, and understands why personal memory is a valuable kind of history. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Interview preparation builds writing skills. Retelling an oral story is narration. Transcribing an interview is a literacy activity.",
            "math": "Timeline math: when did the events in the stories happen? How long ago? How old was the person?",
            "science": "Interview questions can include: 'What was the weather like? What animals did you see? How has the land changed?' — connecting personal memory to environmental observation.",
        },
    },
    "hf-16": {
        "enriched": True,
        "learning_objectives": [
            "Distinguish between a primary source (from the time of an event) and a secondary source (about an event, written later)",
            "Examine a historical photograph, letter, or artifact and describe what it reveals about the past",
            "Ask analytical questions about primary sources: Who made this? When? Why? What does it tell us?",
            "Draw conclusions from evidence rather than just guessing",
        ],
        "teaching_guidance": {
            "introduction": "A primary source is something that comes directly from the past: a photograph taken at the time, a letter written by a real person, a tool someone used, a newspaper from the day of an event. A secondary source is something written ABOUT the past later, like a history book or biography. Teaching children to examine primary sources is teaching them to think like historians — to look at evidence carefully, ask questions, and draw conclusions. Even a 5-year-old can examine an old photograph and say 'The clothes are different. There are no cars. This must be from a long time ago.'",
            "scaffolding_sequence": [
                "Show the child an old family photograph (grandparent's era): 'What do you notice? What's different from today? What can you figure out about when this was taken?'",
                "Introduce the terms: 'This photograph is a PRIMARY source — it comes directly from the past. A book about this time period would be a SECONDARY source.'",
                "Practice with 3 different primary sources: a photograph, a letter or document, and a physical object (old tool, coin, postcard)",
                "Teach the question framework: Who made/used this? When? Where? Why? What does it tell us about life back then?",
                "Model drawing conclusions from evidence: 'I see a horse and buggy in this photo. There are no cars. So this was probably before cars were common — maybe the early 1900s.'",
                "Compare a primary source to a secondary source about the same topic: how is reading about the event different from seeing an artifact from it?",
                "The child examines a new primary source independently, asks questions, and shares conclusions",
                "Visit a museum (in person or virtually) to see real artifacts and practice the observation skills",
            ],
            "socratic_questions": [
                "Look at this old photograph. What is the FIRST thing you notice? What else do you see if you look more carefully?",
                "This letter was written in 1865. What can you figure out about the person who wrote it just from looking at the handwriting and the paper?",
                "If you found this old tool in your grandma's attic, how would you figure out what it was used for?",
                "What's the difference between looking at a real artifact from ancient Egypt and reading about ancient Egypt in a book?",
            ],
            "practice_activities": [
                "Photo detective: examine an old photograph (family or historical) using the question framework. Write or tell 3 things the photo reveals.",
                "Artifact investigation: examine a household object (a kitchen tool, an old coin, a piece of clothing) as if it were from the past. What does it tell you about the people who used it?",
                "Primary vs secondary sorting: sort a collection of items into primary sources (old letters, photos, artifacts) and secondary sources (textbooks, biographies, encyclopedia entries)",
                "Museum at home: collect 5 'artifacts' from the house, label them, and give a museum tour explaining what each reveals",
            ],
            "real_world_connections": [
                "Family photo albums are collections of primary sources documenting your family's history",
                "Museums are full of primary sources: the actual objects and documents from the past",
                "Old coins, stamps, and postcards found at antique shops or in family drawers are real primary sources a child can hold",
                "Historical documents like the Declaration of Independence are primary sources — the actual paper with the actual signatures",
            ],
            "common_misconceptions": [
                "Thinking primary sources are 'better' than secondary sources — both are valuable. Primary sources provide direct evidence; secondary sources provide interpretation and context.",
                "Believing every detail in a primary source is perfectly accurate — photographs only show one angle, letters reflect one person's view, artifacts can be misinterpreted",
                "Thinking only old things are primary sources — a newspaper from yesterday is a primary source for yesterday's events",
                "Assuming primary source analysis is too advanced for young children — even very young children can observe, describe, and draw simple conclusions from photographs and objects",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Distinguishes primary from secondary sources with examples",
                "Asks analytical questions about a primary source using the framework",
                "Draws conclusions from evidence with supporting reasoning",
            ],
            "proficiency_indicators": [
                "Identifies primary sources with help but may confuse with secondary",
                "Describes what they see but doesn't yet draw conclusions",
            ],
            "developing_indicators": [
                "Cannot distinguish primary from secondary sources",
                "Describes primary sources only superficially",
            ],
            "assessment_methods": ["source identification", "artifact analysis", "conclusion drawing"],
            "sample_assessment_prompts": [
                "Is this a primary source or a secondary source? How do you know?",
                "Look at this old photograph. Tell me 3 things you notice and what they tell you about the past.",
                "What questions would you ask about this artifact to learn more about the people who used it?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which of these is a primary source?",
                "expected_type": "multiple_choice",
                "options": [
                    "A history textbook written in 2020",
                    "A letter written by a soldier during the Civil War",
                    "A biography of Abraham Lincoln",
                    "A Wikipedia article about ancient Egypt",
                ],
                "correct_answer": "A letter written by a soldier during the Civil War",
                "hints": [
                    "A primary source comes directly from the time of the event. Which one was created DURING the historical event?"
                ],
                "explanation": "The soldier's letter is a primary source because it was written during the Civil War by someone who was there. The other options were all written AFTER the events, making them secondary sources.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is the difference between a primary source and a secondary source?",
                "expected_type": "text",
                "hints": ["Primary = from the time. Secondary = about the time, written later."],
                "explanation": "A primary source comes from the actual time of an event: a diary, a photograph, a tool, a letter. A secondary source is created later by someone studying the event: a textbook, a biography, a documentary. Both are useful, but they provide different kinds of information.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You are looking at an old photograph from 1900. You see people wearing long dresses and suits, a horse and wagon on a dirt road, and no electric lights. What can you conclude about life in 1900?",
                "expected_type": "text",
                "hints": ["Look at the clothing, transportation, and technology. What do they tell you?"],
                "explanation": "From this evidence: people dressed formally even in daily life (long dresses, suits). Transportation was horse-powered, not motorized. Roads were not paved. Electric lighting was not yet common. Life was very different from today in terms of technology and transportation.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: A newspaper from 1776 is a primary source.",
                "expected_type": "true_false",
                "correct_answer": "true",
                "hints": ["Was the newspaper created during the time period it describes?"],
                "explanation": "True. A newspaper printed in 1776 is a primary source because it was created at the time of the events it reports. It provides a direct window into what people knew, thought, and cared about in that moment.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Examine an object in your home as if you were a historian from the future finding it in 200 years. Describe it, explain what it was used for, and say what it reveals about life in our time.",
                "expected_type": "text",
                "hints": [
                    "Choose any everyday object: a phone, a fork, a shoe, a book. Describe it as if you've never seen one before. What does it tell you about our civilization?"
                ],
                "explanation": "This exercise builds the analytical thinking at the heart of primary source study. A smartphone, for example, reveals: our civilization used advanced technology daily, we communicated electronically, we valued information access, and we carried powerful computers in our pockets. This is exactly how historians analyze artifacts from the past.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Sort these items into primary and secondary sources.",
                "type": "open_response",
                "target_concept": "source_identification",
                "rubric": "Mastery: correctly sorts all items with explanations. Proficient: mostly correct. Developing: cannot distinguish.",
            },
            {
                "prompt": "Examine this photograph and tell me 3 things it reveals about the past.",
                "type": "open_response",
                "target_concept": "artifact_analysis",
                "rubric": "Mastery: 3 observations with conclusions drawn. Proficient: 2 observations. Developing: surface description only.",
            },
        ],
        "resource_guidance": {
            "required": [
                "old family photographs or historical photographs",
                "a physical object to examine as an 'artifact'",
            ],
            "recommended": ["museum visit (in person or virtual)", "collection of reproduced primary source documents"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Primary source analysis is largely visual: examining photographs, objects, and artifacts. No reading required for core skills. Oral descriptions and conclusions.",
            "adhd": "Handling real objects is engaging. Photo detective games add excitement. Keep analysis sessions to 10-15 minutes per source. Rotate between different types of sources.",
            "gifted": "Introduce the idea that sources can be biased. Compare two primary sources about the same event. Begin analyzing written primary sources (letters, diaries). Discuss how historians evaluate reliability.",
            "visual_learner": "Core strength: visual analysis of photographs and artifacts. Use magnifying glasses for detail work.",
            "kinesthetic_learner": "Handle physical objects. Create a 'museum exhibit' with artifacts and labels.",
            "auditory_learner": "Describe what you see aloud. Discuss conclusions as a conversation. Listen to audio primary sources (speeches, oral histories).",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "A primary source comes straight from the past: a photograph taken at the time, a letter written by someone who was there, a tool that was used, a newspaper from the day of an event. A secondary source is made later, about the past, like a history book or a biography. Examining primary sources is how a historian thinks: looking at the evidence, asking questions, and drawing conclusions. A source also shows one angle, one person's view, so a careful historian weighs evidence from more than one source. Today we tell primary from secondary sources, examine real evidence, ask analytical questions, and draw conclusions from what we find.",
                "gradual_release": {
                    "i_do": "Hold up an old photograph and think aloud: this is a primary source, made at the time; I ask who made it, when, where, and why, and what it shows. I see a horse and wagon and no cars, so this was likely long ago. Note that the photograph shows only one angle, one moment, so I would seek other sources too.",
                    "we_do": "Examine primary sources together, a photograph, a letter, an object, ask the questions who, when, where, why, and what it reveals, and draw conclusions from the evidence.",
                    "you_do": "Child distinguishes primary from secondary sources, examines a primary source and describes what it reveals, asks analytical questions about it, and draws conclusions from the evidence.",
                },
                "guided_practice": [
                    "Sort sources into primary, from the time, and secondary, made later",
                    "Examine a primary source with the questions: who made this, when, where, why, and what does it tell us",
                    "Draw a conclusion from a primary source and give the evidence for it",
                ],
                "independent_practice": [
                    "Examine a photograph, letter, or artifact and record three things it reveals about the past",
                    "Set up a museum at home: label household objects as artifacts and explain what each reveals",
                ],
                "mastery_check": [
                    "Distinguish a primary source from a secondary source, with examples",
                    "Examine a primary source and describe what it reveals about the past",
                    "Ask analytical questions about a source and draw conclusions from evidence rather than guessing",
                ],
                "spiral_review": [
                    "Revisit careful observation, the skill that examining a primary source depends on",
                ],
            },
            "classical": {
                "narrative_introduction": "To think like a historian is to reason from evidence. A primary source is evidence straight from the past, a letter, a photograph, an artifact; a secondary source is the later study of that evidence. The classical student examines the source closely, asks of it who, when, where, and why, and draws conclusions only from what the evidence shows. And the student remembers that each source carries one perspective, so the truth is best sought from many sources, not one.",
                "memory_work": {
                    "chants": [
                        "Chant the two kinds of source: the primary source from the time, the secondary source made later",
                        "Chant the historian's questions for a source: who made it, when, where, why, and what does it tell",
                    ],
                    "recitations": [
                        "Recite that a primary source is evidence from the time of an event, and that each source shows one perspective, so the careful historian weighs many",
                    ],
                },
                "copywork": [
                    "Copy the meanings of primary source and secondary source, and the historian's questions: who, when, where, why",
                ],
                "recitation_routine": "Begin each lesson by reciting the two kinds of source and the historian's questions before examining a new source.",
                "history_integration": "Mark that the chronological spine itself is built from primary sources: every date and event the child has placed on it was learned by historians who examined the evidence the past left behind.",
                "read_aloud_suggestions": [
                    "A book that shows historians at work, examining the evidence of the past and reasoning from it",
                    "A collection of reproduced primary sources, letters, photographs, documents, looked at and read aloud together",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 15,
                "living_book_suggestions": [
                    "A beautifully made book of historical photographs and documents, real evidence of the past to pore over",
                    "A living book that shows a historian or a curious person reading the clues an old object or photograph holds",
                ],
                "short_lesson_flow": "Set a real thing before the child, an old family photograph, a letter, an object, and let them look long and closely before a word is said. Then ask gently what they notice, and what it tells them. The child describes what they see and draws a conclusion from it. Charlotte Mason's object lesson: the real thing first, the questions next, the meaning last.",
                "narration_prompt": "Tell me about the photograph or object we examined. What did you notice, and what does it reveal about the past?",
                "real_world_objects": [
                    "Real old family photographs, letters, and documents",
                    "A physical object from the past, a tool, a coin, a postcard, to handle and examine",
                    "A magnifying glass for close looking",
                    "A museum, where real artifacts and primary sources can be met",
                ],
                "nature_connection": "An old photograph or letter can be a record of nature too: the trees, the weather, the animals, the look of the land then, and the child can read in it how the natural world has changed.",
                "habit_focus": "The habit of attention: looking at a real piece of the past closely and patiently enough to read the evidence it holds.",
            },
            "montessori": {
                "prepared_materials": [
                    "Real primary sources to examine: old photographs, letters, and artifacts",
                    "Source-sorting cards for separating primary from secondary sources",
                    "Observation-question cards: who, when, where, why, what does it reveal",
                    "A magnifying glass and a museum-style space for labeling and displaying artifacts",
                ],
                "presentation": {
                    "three_period_lesson": "With the source cards: this is a primary source, made at the time of the event; show me a primary source; is this source primary or secondary?",
                    "steps": [
                        "The child sorts a set of sources into primary and secondary",
                        "The child examines a primary source closely with the observation-question cards",
                        "The child draws a conclusion from the evidence and may label and display the source as a museum artifact",
                    ],
                },
                "control_of_error": "The source itself is the control: the date it was made settles whether it is primary or secondary, and a conclusion that the evidence does not support is checked against the source and found to be a guess, not a finding.",
                "abstraction_pathway": "From handling and examining concrete primary sources, to sorting and questioning them, toward reasoning from historical evidence and grasping that every source carries one perspective.",
                "extensions": [
                    "Compare two primary sources about the same event and notice how their perspectives differ",
                    "Examine a written primary source, a letter or a diary, in depth",
                    "Investigate how historians judge whether a source is reliable",
                ],
                "observation_focus": "Watch for the child drawing conclusions only from the evidence rather than guessing, and beginning to see that a single source shows one angle of the truth.",
            },
            "unschooling": {
                "invitations": [
                    "Keep old family photographs, letters, and objects where the child can examine them",
                    "Leave out a magnifying glass and a box of curious old things, coins, postcards, tools",
                    "Have books of historical photographs and documents available",
                ],
                "real_world_contexts": [
                    "Looking through the family's old photographs and wondering what each one shows",
                    "Examining old objects found in an attic, a drawer, or an antique shop",
                    "Visiting a museum and meeting the real evidence of the past",
                    "Noticing that a newspaper or a photo from today will one day be a primary source of this time",
                ],
                "conversation_starters": [
                    "What is the first thing you notice in this old photograph, and what else if you look closely?",
                    "How could you figure out, from this old object, what it was used for and who used it?",
                    "This letter shows one person's view of an event; how could we learn what others saw?",
                ],
                "resource_bank": [
                    "The family's own photographs, letters, and old objects",
                    "A magnifying glass and a collection of curious historical things",
                    "Museums and books of reproduced primary sources",
                ],
                "parent_role": "Bring out the family's old photographs and objects and wonder at them together, looking closely and asking what each one reveals. Show that a real thing from the past is evidence to be read, that each source shows one angle, and let real artifacts and real museums, rather than a worksheet, teach the child to think like a historian.",
                "observation_documentation": "Over time, note whether the child tells primary from secondary sources, examines real evidence closely, asks good questions of it, and draws conclusions from evidence rather than guessing. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Analyzing a primary source is close reading: careful observation, questioning, and drawing conclusions from evidence",
            "math": "Dating artifacts involves number sense: 'This coin is from 1803. How many years ago is that?'",
            "science": "Scientific observation skills transfer directly: look carefully, describe accurately, ask questions, draw conclusions from evidence",
        },
    },
    "hf-17": {
        "enriched": True,
        "learning_objectives": [
            "Read or listen to historical fiction and identify which parts are historically accurate and which are invented by the author",
            "Describe what the book taught about the historical period: daily life, customs, challenges, and values",
            "Develop empathy for people who lived in different times by experiencing their world through story",
            "Distinguish between historical fiction (story set in a real time period) and pure fantasy or modern fiction",
        ],
        "teaching_guidance": {
            "introduction": "Historical fiction is one of the most powerful tools for teaching history to children. A well-written historical novel drops the reader into another time and place so vividly that they FEEL what it was like to live there. The child who reads about a colonial child churning butter, hauling water, and sleeping in a loft understands colonial life far more deeply than one who memorizes dates. The key skill is learning to separate what is REAL history from what the author INVENTED for the story — the setting and customs are usually accurate, but the specific characters and plot are often fictional.",
            "scaffolding_sequence": [
                "Read a short historical fiction picture book aloud. Before reading, tell the child: 'This story takes place in a real time period, but the characters are made up.'",
                "After reading, discuss: 'What did you learn about life in that time? What was real history and what was the author's invention?'",
                "Introduce the concept of setting as history: the place, the time, the clothing, the food, the technology — these details are researched to be accurate",
                "Discuss what the author invented: the specific characters, the exact plot, the dialogue — these are fictional, set against a real historical backdrop",
                "Read a second historical fiction book set in a different time period. Compare: 'How was life different in these two periods?'",
                "Practice identifying facts vs fiction: make two columns and sort story elements into 'probably true for the time' and 'made up by the author'",
                "Discuss empathy: 'How did this character feel? Could you feel what they felt? That's empathy across time.'",
                "The child recommends a historical fiction book to someone and explains what they would learn about history from it",
            ],
            "socratic_questions": [
                "The characters in this book wore long dresses and rode horses. Is that part real history or made up? How do you know?",
                "After reading this book, what do you know about life in that time period that you didn't know before?",
                "The main character is a fictional girl named Sarah. But the world she lives in is real. How can a made-up character teach us real history?",
                "Would you have wanted to live in the time and place of this story? Why or why not?",
            ],
            "practice_activities": [
                "Fact vs fiction chart: after reading, list story elements in two columns — 'Real for the time period' and 'Made up by the author'",
                "Historical fiction book talk: the child presents a historical fiction book to the family, explaining the time period and what they learned",
                "Write a scene: the child writes a short historical fiction scene set in a time period they've studied, using accurate historical details",
                "Compare fiction to facts: after reading a historical novel about ancient Egypt, compare the book's portrayal to what you studied about real ancient Egypt",
            ],
            "real_world_connections": [
                "Movies and TV shows set in the past are a form of historical fiction — the child can practice identifying fact vs invention in shows they watch",
                "Historical fiction makes museum visits more meaningful: 'This is the kind of dress the character wore!'",
                "Family stories told by grandparents are similar — real settings and feelings with details that may have shifted over time",
                "Historical reenactments at living history museums bring historical fiction to life in three dimensions",
            ],
            "common_misconceptions": [
                "Thinking everything in a historical novel is true — the setting is usually accurate, but the characters and plot are typically invented",
                "Believing historical fiction is 'not real reading' or 'not real history' — it is one of the most effective ways to develop historical empathy and understanding",
                "Assuming the author got everything right — even well-researched historical fiction may contain inaccuracies or reflect modern biases",
                "Thinking historical fiction is only for older readers — excellent picture books exist for every historical period, suitable for young children",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Identifies 3+ historically accurate elements in a work of historical fiction",
                "Explains what the author invented for the story",
                "Describes what the book taught about the historical period",
            ],
            "proficiency_indicators": [
                "Identifies some accurate elements but has difficulty separating fact from fiction",
                "Describes the story but not the historical learning",
            ],
            "developing_indicators": [
                "Cannot distinguish historical fiction from other genres",
                "Does not recognize which elements are historically accurate",
            ],
            "assessment_methods": [
                "fact vs fiction analysis",
                "historical learning discussion",
                "genre identification",
            ],
            "sample_assessment_prompts": [
                "What parts of this book were real history and what parts did the author make up?",
                "What did you learn about life in that time period from this story?",
                "Is this book historical fiction, fantasy, or realistic fiction? How do you know?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "What is historical fiction?",
                "expected_type": "multiple_choice",
                "options": [
                    "A true story about real people",
                    "A made-up story set in a real historical time period",
                    "A fantasy story with magic",
                    "A science fiction story about the future",
                ],
                "correct_answer": "A made-up story set in a real historical time period",
                "hints": ["Historical = real time period. Fiction = made-up story. Put them together."],
                "explanation": "Historical fiction is a made-up story set in a real historical time period. The setting, customs, and historical events are usually accurate, but the main characters and plot are invented by the author.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "In a historical fiction book about colonial America, a girl named Hannah milks cows and makes candles. Is Hannah a real historical person?",
                "expected_type": "multiple_choice",
                "options": ["Yes, she's real", "No, she's invented by the author", "Maybe — we can't tell"],
                "correct_answer": "No, she's invented by the author",
                "hints": ["The SETTING (colonial America) is real. But the specific CHARACTER is usually..."],
                "explanation": "Hannah is a fictional character invented by the author. But the activities she does (milking cows, making candles) are historically accurate — real colonial children did these things. The setting is real; the character is invented.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "After reading a historical fiction book, what is something you learned about the real time period it was set in?",
                "expected_type": "text",
                "hints": [
                    "Think about the setting: what people wore, ate, did for work, how they traveled, what their homes looked like."
                ],
                "explanation": "A good answer names specific historical details from the book's setting. Example: 'I learned that in colonial times, children had to help with farm work every day. They didn't have running water, so they carried it from a well. They made their own candles because there was no electricity.'",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: Everything in a historical fiction book is historically accurate.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["The setting is usually accurate, but what about the characters and the exact plot?"],
                "explanation": "False. Historical fiction authors research the time period carefully to make the setting accurate, but the characters, dialogue, and plot are invented. Even the historical details may not be perfectly accurate — authors sometimes simplify or adjust for storytelling.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Think of a historical fiction book you've read or heard. Make a chart with two columns: 'Real History' and 'Made Up by the Author.' List at least 2 items in each column.",
                "expected_type": "text",
                "hints": [
                    "Real history: setting, clothing, technology, customs, real events mentioned. Made up: the main character, the specific plot, the dialogue."
                ],
                "explanation": "A strong chart clearly separates historical facts (the time period is real, the clothing is accurate, the events happened) from fiction (the main character is invented, the specific conversations are imagined, the plot is the author's creation). This demonstrates critical thinking about sources.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "What parts of this historical fiction book were real and what parts were invented?",
                "type": "open_response",
                "target_concept": "fact_vs_fiction",
                "rubric": "Mastery: identifies 3+ real and 2+ invented elements. Proficient: identifies some of each. Developing: cannot distinguish.",
            },
            {
                "prompt": "What did this book teach you about the historical period?",
                "type": "open_response",
                "target_concept": "historical_learning",
                "rubric": "Mastery: names 3+ specific historical details learned. Proficient: 1-2 details. Developing: only remembers the plot, not the history.",
            },
        ],
        "resource_guidance": {
            "required": ["historical fiction picture books or chapter books at the child's level"],
            "recommended": ["fact vs fiction chart template", "companion nonfiction book about the same time period"],
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Read historical fiction aloud — the story is engaging and the child comprehends through listening. Audiobooks of historical fiction are excellent. Fact vs fiction discussion is oral.",
            "adhd": "Historical fiction is inherently engaging: it has characters, conflict, and suspense. Choose action-packed historical adventures. Discuss in short bursts rather than lengthy analysis.",
            "gifted": "Compare multiple historical fiction books set in the same period. Research which details the author got right and which they changed. Begin writing original historical fiction.",
            "visual_learner": "Illustrated historical fiction. Look at pictures for historical details. Draw scenes from the book.",
            "kinesthetic_learner": "Act out scenes from historical fiction. Build or create something from the time period depicted.",
            "auditory_learner": "Audiobooks of historical fiction. Read-aloud with discussion. Retell the story emphasizing the historical elements.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "Historical fiction is a made-up story set in a real time and place. A well-written historical novel makes the reader feel what it was like to live in another age. The key skill is telling apart what is real history from what the author invented: the setting, the customs, the technology are usually researched to be accurate, while the particular characters and plot are made up. A careful reader also remembers that even researched fiction can carry mistakes or a modern view. Today we read historical fiction, sort the real history from the invention, describe what the book taught about the period, and tell historical fiction from fantasy and modern fiction.",
                "gradual_release": {
                    "i_do": "Read a passage of historical fiction aloud and think aloud: the long dresses and the horse and wagon are real history, researched to be accurate; the girl named Sarah and her exact adventure are the author's invention. Name what the book teaches about the time, and notice anything that might be the author's guess or modern view.",
                    "we_do": "Read a work of historical fiction together, sort its parts into real history and the author's invention, and name what it taught about the period.",
                    "you_do": "Child reads or hears historical fiction, identifies which parts are historically accurate and which are invented, describes what the book taught about the period, and tells historical fiction from fantasy and modern fiction.",
                },
                "guided_practice": [
                    "Sort the elements of a historical fiction story into real history and the author's invention",
                    "Describe what a work of historical fiction taught about daily life, customs, and challenges of its period",
                    "Tell historical fiction apart from fantasy and from modern realistic fiction",
                ],
                "independent_practice": [
                    "Make a two-column chart, real history and made up by the author, for a historical fiction book",
                    "Compare a historical fiction book with a nonfiction account of the same period",
                ],
                "mastery_check": [
                    "Identify which parts of a work of historical fiction are historically accurate and which are invented",
                    "Describe what the book taught about the historical period",
                    "Distinguish historical fiction from fantasy and from modern fiction",
                ],
                "spiral_review": [
                    "Revisit telling fact from fiction, the same careful reading used with primary sources",
                ],
            },
            "classical": {
                "narrative_introduction": "Historical fiction is a story invented and set within a real and researched past. It is a powerful teacher, for it lets the reader feel another age from the inside. Yet the classical reader keeps a clear mind: the setting and the customs are drawn from real history, while the characters and the plot are the author's making, and even careful fiction may hold a mistake or a modern view. To read historical fiction well is to enjoy the story and weigh its history both.",
                "memory_work": {
                    "chants": [
                        "Chant the parts of historical fiction: the setting and customs are real history, the characters and plot are the author's invention",
                        "Chant the reader's caution: even a researched story may carry a mistake or a modern view",
                    ],
                    "recitations": [
                        "Recite that historical fiction is an invented story in a real and researched past, and that the wise reader weighs its history while enjoying its tale",
                    ],
                },
                "copywork": [
                    "Copy the distinction between real history and an author's invention, and a vivid sentence from a work of historical fiction",
                ],
                "recitation_routine": "Begin each lesson by reciting the parts of historical fiction, the real and the invented, before reading a new book.",
                "history_integration": "Set each work of historical fiction on the chronological spine by its period, so the child sees where a colonial tale or a story of ancient Rome falls in the long order of history.",
                "read_aloud_suggestions": [
                    "A finely written work of historical fiction set in a period the child has studied, read aloud for narration",
                    "A companion account of the same period, read alongside the story so the child can weigh the fiction against the history",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 20,
                "living_book_suggestions": [
                    "A living work of historical fiction that carries the child fully into another time, with a real and researched setting and a story worth narrating",
                    "A well-told historical novel honest about its period, not one that flatters or sanitizes the age it portrays",
                ],
                "short_lesson_flow": "Read a portion of a living work of historical fiction aloud, and let the child narrate it back. Afterward, wonder together: what here was real history, and what did the author invent? Let the story carry the child into the age and build empathy for the people who lived then, and let the narration show what was understood.",
                "narration_prompt": "Tell me the part of the story we just heard. What did it show you about life in that time, and how do you think the people felt?",
                "real_world_objects": [
                    "Living works of historical fiction at the child's level",
                    "A companion nonfiction book or pictures of the same period",
                    "A Book of Centuries for placing the story's period",
                    "A simple two-column record of real history and the author's invention",
                ],
                "nature_connection": "Notice the natural world inside a historical story: the crops, the weather, the animals, the unlit nights, and how the people of that age lived close to nature in ways a modern child may not.",
                "habit_focus": "The habit of attention and of sympathy: entering another age through a story closely enough to feel what its people felt.",
            },
            "montessori": {
                "prepared_materials": [
                    "Historical fiction books organized by time period in the reading area",
                    "Companion nonfiction books about the same periods",
                    "Fact-and-fiction sorting cards for the elements of a story",
                    "A timeline for placing each story's period",
                ],
                "presentation": {
                    "three_period_lesson": "With story-element cards: this element is real history, the clothing of the time; this element is the author's invention, the main character; show me an element of real history; is this element real history or invention?",
                    "steps": [
                        "The child reads or hears a work of historical fiction set in a studied period",
                        "The child sorts the story's elements into real history and the author's invention",
                        "The child places the story's period on the timeline and names what the book taught about the age",
                    ],
                },
                "control_of_error": "The companion nonfiction and the studied history are the control: an element sorted as real history can be checked against the record, and the child sees when something the author invented has been mistaken for fact.",
                "abstraction_pathway": "From reading a concrete story and sorting its elements with the cards, to checking them against the historical record, toward reading any historical fiction with both enjoyment and a discerning eye.",
                "extensions": [
                    "Compare two works of historical fiction set in the same period",
                    "Check which of a story's details the historical record confirms",
                    "Write a short historical fiction scene using accurate details of a studied period",
                ],
                "observation_focus": "Watch for the child separating the researched setting from the invented characters and plot, and growing in empathy for the people of the age the story portrays.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a rich shelf of historical fiction for many periods within reach",
                    "Have audiobooks of historical fiction available",
                    "Leave out companion nonfiction and pictures about the periods the stories are set in",
                ],
                "real_world_contexts": [
                    "Reading or hearing historical fiction simply for the love of the story",
                    "Noticing that films and shows set in the past are historical fiction too, and asking what is real and what is invented",
                    "Visiting a museum or a historic site and recognizing it from a story",
                    "Wondering, after a story, what it would truly have been like to live then",
                ],
                "conversation_starters": [
                    "The character wore long dresses and rode a horse; do you think that part is real history or made up?",
                    "What did this story show you about life in that time that you did not know before?",
                    "How can a made-up character teach us something true about the past?",
                ],
                "resource_bank": [
                    "A wide shelf of historical fiction and audiobooks",
                    "Companion nonfiction about the periods",
                    "Films, museums, and historic sites that bring the periods to life",
                ],
                "parent_role": "Follow the child's love of a good story into historical fiction, and read it together for the pleasure of it. Wonder aloud about what is real history and what the author invented, note that even careful authors can be mistaken, and let real stories, rather than a worksheet, carry the child into other ages.",
                "observation_documentation": "Over time, note whether the child enjoys historical fiction, can tell its real history from its invention, describes what a book taught about its period, and feels empathy for people of other times. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "Historical fiction builds reading comprehension while teaching history — two subjects in one book",
            "math": "Historical fiction set in different eras shows how math was used: trade, navigation, building, farming calculations",
            "science": "Historical fiction reveals historical technology and scientific understanding: medicine, transportation, tools of each era",
        },
    },
    "hf-18": {
        "enriched": True,
        "learning_objectives": [
            "Maintain an ongoing timeline or Book of Centuries with 20 or more events placed in correct chronological order",
            "Add new events, figures, and civilizations to the timeline as they are studied",
            "Trace connections between events on different parts of the timeline",
            "Illustrate key events on the timeline with drawings or pictures",
        ],
        "teaching_guidance": {
            "introduction": "A timeline is the backbone of historical understanding. It is not a one-time project but an ongoing, living document that grows throughout the child's education. Every civilization studied, every figure met, every event learned gets placed on the timeline. Over time, the child begins to SEE patterns: 'Egypt and China existed at the SAME TIME!' 'The pyramids were already ancient when Rome was founded!' A Book of Centuries — a notebook with pages for each century — serves the same purpose in a more portable format. The timeline connects everything.",
            "scaffolding_sequence": [
                "Review the personal timeline created in hf-01: 'Remember your life timeline? Now we're building a WORLD history timeline.'",
                "Set up a wall timeline or Book of Centuries: mark major era divisions (ancient, medieval, modern) with plenty of space",
                "Add every civilization already studied: Egypt, Mesopotamia, China, India, Greece, Rome. Place them correctly relative to each other.",
                "Add key figures: Confucius, Cleopatra, Julius Caesar, Washington, Lincoln. Show when they lived.",
                "Point out surprising connections: 'Look — Confucius and the Buddha lived at almost the same time, on different sides of the world!'",
                "Make adding to the timeline a HABIT: every time a new topic is studied, it goes on the timeline",
                "Periodically review the whole timeline: the child narrates the story of history by walking along it",
                "The child independently places new events on the timeline and explains their reasoning for the placement",
            ],
            "socratic_questions": [
                "The pyramids were built around 2500 BC. Rome was founded around 750 BC. How many years apart is that? Were the pyramids already ancient when Rome was new?",
                "You just learned about the American Revolution in 1776. Where does that go on our timeline? Is it near the beginning, middle, or end?",
                "Looking at the timeline, what do you notice about how many civilizations existed at the same time?",
                "If someone walked along our timeline from left to right, what story would it tell?",
            ],
            "practice_activities": [
                "Timeline walk-and-talk: the child walks along the wall timeline and narrates history in chronological order",
                "Timeline additions: after every history lesson, add the new person, event, or civilization to the timeline with a small illustration",
                "Connection discovery: the child draws lines between events on the timeline that are connected (Greece influenced Rome, Rome influenced America)",
                "Century book entry: for each new topic, the child draws a picture and writes a sentence on the appropriate century page",
            ],
            "real_world_connections": [
                "Museum timelines display history visually — the child can compare their own timeline to a museum's",
                "Family timelines: add family history events (immigration, births, marriages) to see where your family fits in the larger story",
                "News events can be added to the modern end of the timeline: history is happening right now",
                "The timeline is a reference tool: when reading a book set in a historical period, check the timeline to see what else was happening at that time",
            ],
            "common_misconceptions": [
                "Thinking the timeline is a one-time project to be completed and put away — it should grow continuously throughout the child's education",
                "Placing events based on when they were STUDIED rather than when they HAPPENED — always check chronological accuracy",
                "Assuming all of history can fit on one strip of paper — ancient history covers thousands of years; modern history is compressed into centuries. Scale matters.",
                "Not realizing that events on different continents were happening simultaneously — the timeline reveals global connections that topic-by-topic study can miss",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Maintains a timeline with 20+ events in correct chronological order",
                "Traces connections between events across different civilizations and time periods",
                "Independently places new events on the timeline with correct reasoning",
            ],
            "proficiency_indicators": [
                "Has 10-19 events on timeline, mostly in correct order",
                "Can trace 1-2 connections between events",
            ],
            "developing_indicators": [
                "Has fewer than 10 events on timeline",
                "Needs help placing events in the correct position",
            ],
            "assessment_methods": ["timeline review", "chronological ordering", "connection identification"],
            "sample_assessment_prompts": [
                "Walk me along your timeline and tell me the story of history.",
                "Where would you place the invention of paper on this timeline? Why there?",
                "Can you find two events on your timeline that are connected? How are they connected?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Put these in chronological order: Ancient Rome, Ancient Egypt, the American Revolution.",
                "expected_type": "text",
                "correct_answer": "Ancient Egypt, Ancient Rome, the American Revolution",
                "hints": [
                    "Egypt is the oldest (3000+ BC). Rome came next (750 BC - 476 AD). The American Revolution is the most recent (1776)."
                ],
                "explanation": "Ancient Egypt (3000+ BC) came first, then Ancient Rome (750 BC - 476 AD), then the American Revolution (1776). A timeline helps you see these relationships at a glance.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Why is a timeline useful for learning history?",
                "expected_type": "multiple_choice",
                "options": [
                    "It makes the wall look nice",
                    "It helps you see when events happened and how they connect to each other",
                    "It replaces reading books",
                    "It is only useful for memorizing dates",
                ],
                "correct_answer": "It helps you see when events happened and how they connect to each other",
                "hints": [
                    "A timeline shows the ORDER of events and lets you see what was happening at the same time in different places."
                ],
                "explanation": "A timeline shows chronological order and reveals connections: events that happened at the same time, events that caused other events, and the flow of history from ancient to modern.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: The ancient Egyptians and ancient Chinese civilizations existed at roughly the same time.",
                "expected_type": "true_false",
                "correct_answer": "true",
                "hints": ["Both began around 3000-2000 BC. Check your timeline!"],
                "explanation": "True! Both Egyptian and Chinese civilizations began around 3000-2000 BC. A timeline reveals this surprising fact — great civilizations were developing simultaneously on different continents.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "You just learned about Marco Polo, who traveled from Italy to China around 1270 AD. Where would you place him on your timeline? What else was happening around that time?",
                "expected_type": "text",
                "hints": ["1270 AD is in the medieval period — after Rome fell (476 AD) but before Columbus (1492)."],
                "explanation": "Marco Polo goes in the medieval period, roughly in the middle of the timeline between the fall of Rome and the age of exploration. Around the same time: the Crusades, the Mongol Empire, and medieval European cathedral building. The timeline shows how these events are connected.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Look at your timeline and find two events or civilizations that you think are connected. Explain the connection.",
                "expected_type": "text",
                "hints": [
                    "Look for: one event that caused another, one civilization that influenced another, or two things that happened at the same time."
                ],
                "explanation": "A strong answer identifies a real historical connection. Example: 'Ancient Greece and Ancient Rome are connected because Rome admired Greek culture and copied many Greek ideas: their gods, their architecture, and their philosophy. You can see on the timeline that Rome came after Greece and was influenced by it.'",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Walk me through your timeline from beginning to end, narrating the story of history.",
                "type": "open_response",
                "target_concept": "timeline_narration",
                "rubric": "Mastery: narrates chronologically with connections and 20+ events. Proficient: narrates 10+ events in order. Developing: fewer than 10 events, some out of order.",
            },
            {
                "prompt": "Find a connection between two events on your timeline and explain it.",
                "type": "open_response",
                "target_concept": "timeline_connections",
                "rubric": "Mastery: identifies connection with evidence and reasoning. Proficient: identifies connection. Developing: cannot find connections.",
            },
        ],
        "resource_guidance": {
            "required": [
                "wall space for timeline or a Book of Centuries notebook",
                "markers or colored pencils for illustrations",
            ],
            "recommended": ["printed timeline figures to paste", "reference timeline for checking accuracy"],
        },
        "time_estimates": {"first_exposure": 15, "practice_session": 10, "assessment": 15},
        "accommodations": {
            "dyslexia": "Use pictures and drawings on the timeline rather than text. Oral narration of the timeline rather than written labels. Pre-printed timeline figures the child can paste.",
            "adhd": "Adding to the timeline is a quick, hands-on activity (5 minutes). Walking along the wall timeline adds movement. Drawing illustrations keeps hands busy. Review as a game: 'Point to where the Greeks lived!'",
            "gifted": "Create a detailed timeline with precise dates. Add parallel timelines showing what was happening on different continents simultaneously. Research exact dates for events previously placed approximately.",
            "visual_learner": "Illustrated timeline is a core strength. Color-code by civilization or era. Large, beautiful wall display.",
            "kinesthetic_learner": "Physical timeline cards to arrange. Walking along the timeline. Cutting and pasting figures.",
            "auditory_learner": "Narrate the timeline aloud regularly. Chant key dates in order. Discuss connections verbally.",
        },
        "philosophy_specific": {
            "traditional": {
                "introduction": "A timeline is the backbone of historical understanding. It is not a one-time project but a living document that grows throughout a child's education: every civilization, figure, and event studied is placed on it. Over time the child begins to see patterns, that Egypt and China existed at the same time, that the pyramids were already ancient when Rome was founded. A Book of Centuries, a notebook with a page for each century, does the same in a portable form. Today we build and maintain a timeline of twenty or more events, add to it, trace connections across it, and illustrate it.",
                "gradual_release": {
                    "i_do": "Set up the timeline or Book of Centuries and think aloud while placing events: this one is older, it goes to the left; this one is recent, it goes to the right. Add the civilizations and figures already studied, point out a surprising connection, and draw a small picture for a key event.",
                    "we_do": "Place studied civilizations, figures, and events on the timeline together, in correct order, and trace a connection between two of them.",
                    "you_do": "Child maintains a timeline or Book of Centuries with twenty or more events in correct chronological order, adds new events and figures, traces connections across it, and illustrates key events.",
                },
                "guided_practice": [
                    "Place studied civilizations, figures, and events on the timeline in correct chronological order",
                    "Add a newly studied event or figure to the timeline and explain the placement",
                    "Trace a connection between two events on different parts of the timeline",
                ],
                "independent_practice": [
                    "Maintain the timeline as a habit, adding each new topic as it is studied",
                    "Walk the timeline and narrate the story of history from beginning to end",
                ],
                "mastery_check": [
                    "Maintain a timeline or Book of Centuries with twenty or more events in correct chronological order",
                    "Add new events, figures, and civilizations to the timeline as they are studied",
                    "Trace connections between events on different parts of the timeline and illustrate key events",
                ],
                "spiral_review": [
                    "Revisit the whole timeline regularly, narrating it in order so the sequence of history stays firm",
                ],
            },
            "classical": {
                "narrative_introduction": "The timeline is the master tool of the classical study of history: the chronological spine made visible. Upon it every civilization, every figure, every event finds its true and ordered place, and from it the child reads the whole story of history at a glance. A Book of Centuries serves the same end, a page for each century, filled in as study goes on. To keep the timeline faithfully is to hold the order of history itself.",
                "memory_work": {
                    "chants": [
                        "Chant the great divisions of the timeline: the ancient, the medieval, and the modern",
                        "Chant the rule of the timeline: each event in its true place, the old to the left, the recent to the right",
                    ],
                    "recitations": [
                        "Recite that the timeline is the chronological spine made visible, and that every study finds its place upon it",
                    ],
                },
                "copywork": [
                    "Copy the key dates and events of the timeline in their order, and the names of the great divisions of history",
                ],
                "recitation_routine": "Begin each lesson by walking the timeline and reciting the order of events placed on it before adding the next.",
                "history_integration": "This node is the chronological spine itself: the timeline the child keeps holds every civilization and figure studied across all of history, and every future study will find its place upon it.",
                "read_aloud_suggestions": [
                    "A living account of the sweep of history from the ancient world to the present, read aloud so the child hears the order the timeline records",
                ],
            },
            "charlotte_mason": {
                "lesson_length_minutes": 10,
                "living_book_suggestions": [
                    "A beautifully illustrated book of the sweep of history, with true artwork, that shows the order of the ages",
                ],
                "short_lesson_flow": "Keep a Book of Centuries, a notebook with a page for each century. There is no separate lesson: whenever a person or event is studied, the child turns to the right century and adds a small drawing and a line or two. Slowly, over years, the book fills, and it becomes the child's own beautiful record of all the history they have met.",
                "narration_prompt": "Walk along your timeline, or turn through your Book of Centuries, and tell me the story of history in order.",
                "real_world_objects": [
                    "A Book of Centuries, a notebook with a page for each century",
                    "A long wall timeline the child adds to over the years",
                    "Colored pencils for illustrating the events",
                    "Printed figures and pictures of historical people and events to add",
                ],
                "nature_connection": "Add to the timeline the great changes in the natural world the child has studied, so that history and the long story of the Earth are seen to run together.",
                "habit_focus": "The habit of faithful, ongoing work: adding to the timeline a little at a time, year upon year, so that it grows into a record of all the child knows.",
            },
            "montessori": {
                "prepared_materials": [
                    "A long wall timeline with movable cards for civilizations, figures, and events",
                    "The Montessori timelines from the Great Lessons: the timeline of life and of human beings",
                    "Printed timeline figures the child places and illustrates",
                    "A Book of Centuries or personal timeline notebook",
                ],
                "presentation": {
                    "three_period_lesson": "With the timeline cards: this is ancient Egypt, near the beginning; this is the modern age, near the end; show me ancient Egypt; which part of the timeline is this?",
                    "steps": [
                        "The child places the studied civilizations, figures, and events on the timeline in correct order",
                        "The child traces connections between events on different parts of the timeline",
                        "The child illustrates key events and adds each new topic as it is studied",
                    ],
                },
                "control_of_error": "The dates are the control: an event placed out of its true order does not match the dates of the events around it, and the child, checking, sets it right.",
                "abstraction_pathway": "From handling and placing the concrete timeline cards, to tracing the connections between them, toward carrying in the mind the whole ordered sweep of history.",
                "extensions": [
                    "Add parallel rows to the timeline for what was happening on different continents at the same time",
                    "Research exact dates for events placed only approximately",
                    "Connect the history timeline to the Great Lessons' timeline of life",
                ],
                "observation_focus": "Watch for the child placing events by when they truly happened rather than when they were studied, and noticing the connections the timeline reveals.",
            },
            "unschooling": {
                "invitations": [
                    "Keep a long roll of paper or a Book of Centuries notebook within reach, and add to it freely",
                    "Leave out printed timeline figures, pictures, and colored pencils",
                    "Have books about the sweep of history available",
                ],
                "real_world_contexts": [
                    "Adding to the timeline whatever history the child has met, in books, films, museums, or family stories",
                    "Placing the family's own history, births, journeys, on the timeline alongside the wider story",
                    "Adding events from the news to the timeline's recent end, history happening now",
                    "Checking the timeline when a historical period comes up to see what else was happening then",
                ],
                "conversation_starters": [
                    "The pyramids were built long before Rome began; how many years apart do you think that is?",
                    "Where on our timeline does this new story go, near the beginning, the middle, or the end?",
                    "Can you find two things on the timeline that happened at the same time in different places?",
                ],
                "resource_bank": [
                    "A long timeline or Book of Centuries kept available",
                    "Printed timeline figures, pictures, and colored pencils",
                    "Books about the whole sweep of history, and the family's own history",
                ],
                "parent_role": "Keep a timeline or Book of Centuries somewhere in the home and add to it together whenever history comes up, in a book, a film, a museum, or a family story. Wonder aloud about the order of events and the connections between them, and let the growing timeline, rather than a worksheet, give the child a feel for the shape of history.",
                "observation_documentation": "Over time, note whether the child places events in true chronological order, adds new history to the timeline, traces connections across it, and is building a feel for the whole sweep of the past. This noticing replaces any test.",
            },
        },
        "connections": {
            "reading": "The timeline shows when books were written and when stories are set — connecting literature to history",
            "math": "Timeline math: calculating years between events, understanding BC/AD numbering, working with large numbers",
            "science": "Science timelines (geological eras, invention timelines) follow the same principles as history timelines",
        },
    },
    "hf-19": {
        "enriched": True,
        "learning_objectives": [
            "Explain how geography shaped at least 2 ancient civilizations: why they arose where they did",
            "Draw a map showing ancient trade routes and explain why trade followed those paths",
            "Identify geographic features as either barriers (mountains, deserts) or highways (rivers, seas) for human movement",
            "Connect every historical topic studied to its geographic location on a map",
        ],
        "teaching_guidance": {
            "introduction": "Geography is not separate from history — it IS history's stage. Every civilization we have studied arose where it did because of geography: rivers for farming, harbors for trade, mountains for defense. The Nile made Egypt possible. The Mediterranean made Greek trade possible. The Alps protected Italy. Understanding geography means understanding WHY history happened WHERE it happened. Every history lesson should begin with a map.",
            "scaffolding_sequence": [
                "Review the world map: locate every civilization studied so far. Ask 'Why HERE and not somewhere else?'",
                "Introduce the concept of geographic features as barriers or highways: rivers and seas help movement; mountains and deserts block it",
                "Study the Nile as a geographic example: why did Egypt grow HERE? Because the river provided water, transportation, and fertile soil.",
                "Study the Mediterranean Sea: it connected Greece, Rome, Egypt, and the Middle East. It was a highway, not a barrier.",
                "Introduce trade routes: the Silk Road connected China to Rome. Follow it on a map — notice what geographic features it followed and avoided.",
                "Discuss geographic barriers: the Sahara Desert separated North Africa from Sub-Saharan Africa. The Himalayas isolated India from China. How did this shape their histories?",
                "Draw a map showing 2 trade routes and explaining why they followed those paths (rivers, valleys, passes through mountains)",
                "Apply the principle to a NEW location: 'If you were founding a civilization, where on this map would you build it? Why?'",
            ],
            "socratic_questions": [
                "Every ancient civilization started near a river. Is that a coincidence, or does geography explain it?",
                "The Mediterranean Sea is surrounded by Europe, Africa, and Asia. How did this body of water shape the history of all three continents?",
                "Mountains can protect a civilization from invaders. But they also isolate it from trade. Is a mountain range good or bad for a civilization?",
                "If the Sahara Desert didn't exist, how might African history be different?",
            ],
            "practice_activities": [
                "Geography detective: for each civilization studied, mark its location on a map and write WHY geography made that location a good place for a civilization",
                "Trade route mapping: draw the Silk Road on a map, marking the geographic features it passed through (deserts, mountains, rivers) and why traders chose that path",
                "Barrier vs highway sorting: label geographic features on a map as either barriers (blocking movement) or highways (enabling movement)",
                "Civilization placement game: given a blank map with only geographic features (rivers, mountains, coastlines), the child predicts where civilizations would arise — then checks against real history",
            ],
            "real_world_connections": [
                "Your own town or city exists where it does for geographic reasons: near a river, harbor, crossroads, or resource. Research why your town was founded where it was.",
                "Modern highways and railroads often follow the same paths as ancient trade routes — the geography hasn't changed",
                "Farming still depends on geography: fertile valleys, water access, and climate determine what grows where",
                "Wars throughout history have been fought over geographic control: rivers, mountain passes, harbors, and straits",
            ],
            "common_misconceptions": [
                "Thinking geography only matters for ancient civilizations — geography shapes modern life too: cities, trade, agriculture, and conflict",
                "Believing civilizations arose randomly — geographic determinism shows that human settlements follow predictable patterns based on resources and terrain",
                "Assuming rivers are always helpful — rivers flood, change course, and can divide as well as connect. Geography is complex.",
                "Thinking all trade was overland — sea trade was often faster and cheaper. The Mediterranean, Indian Ocean, and Pacific were major trade highways.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Explains how geography shaped 2+ civilizations with specific geographic features cited",
                "Draws a map showing trade routes and explains the geographic logic behind them",
                "Classifies geographic features as barriers or highways with examples",
            ],
            "proficiency_indicators": [
                "Connects geography to 1 civilization",
                "Knows that geography matters but cannot give specific examples of how",
            ],
            "developing_indicators": [
                "Cannot explain why civilizations arose in certain locations",
                "Does not connect geography to history",
            ],
            "assessment_methods": [
                "map drawing with explanations",
                "geographic analysis of civilizations",
                "trade route mapping",
            ],
            "sample_assessment_prompts": [
                "Why did ancient Egypt develop along the Nile River and not in the Sahara Desert?",
                "Draw a trade route and explain why it follows the geographic path it does.",
                "Is a mountain range a barrier or a highway? Can it be both? Explain.",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Why did ancient civilizations develop near rivers?",
                "expected_type": "multiple_choice",
                "options": [
                    "Rivers are pretty to look at",
                    "Rivers provided water for farming, drinking, and transportation",
                    "Rivers kept enemies away",
                    "People liked to swim",
                ],
                "correct_answer": "Rivers provided water for farming, drinking, and transportation",
                "hints": ["Think about what people need to survive and how rivers help provide those things."],
                "explanation": "Rivers provided water for drinking and farming (the most basic needs), transportation for trade, and fertile soil from flooding. Without rivers, early civilizations could not have sustained large populations.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Is a mountain range a barrier or a highway for human movement?",
                "expected_type": "multiple_choice",
                "options": ["Barrier", "Highway", "Neither"],
                "correct_answer": "Barrier",
                "hints": ["Are mountains easy or hard to cross?"],
                "explanation": "Mountains are barriers — they are difficult to cross and slow down travel and trade. The Alps protected Italy from northern invasion. The Himalayas separated India from China. However, mountain passes can serve as narrow highways through the barrier.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "The Mediterranean Sea was surrounded by Europe, Africa, and Asia. Was it a barrier or a highway? Explain.",
                "expected_type": "text",
                "hints": ["Think about what the Greeks, Romans, and Egyptians used the Mediterranean for."],
                "explanation": "The Mediterranean was a HIGHWAY — it connected civilizations rather than separating them. Greeks, Phoenicians, Romans, and Egyptians all used it for trade, communication, and military campaigns. Rome called it 'Mare Nostrum' (Our Sea) because they controlled all the land around it.",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: The Sahara Desert helped ancient North African and Sub-Saharan African civilizations trade with each other easily.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["Deserts are extremely hard to cross. How would that affect trade?"],
                "explanation": "False. The Sahara Desert was a massive BARRIER between North Africa and Sub-Saharan Africa. Trade across it was difficult and dangerous, requiring camel caravans and knowledge of oasis locations. It significantly limited contact between the two regions for thousands of years.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "Choose a civilization you've studied. Explain how at least 2 geographic features shaped its history. What would be different if the geography were different?",
                "expected_type": "text",
                "hints": [
                    "Pick Egypt, Greece, Rome, China, or another. Think about rivers, mountains, seas, deserts, and climate."
                ],
                "explanation": "Example for Greece: (1) Mountains divided Greece into independent city-states because travel between valleys was difficult — this is why Greece was never one unified country like Egypt. (2) The long coastline with many harbors made Greece a seafaring culture — Greeks became traders and colonizers across the Mediterranean. If Greece were flat like Egypt, it might have been one unified kingdom instead of many competing city-states.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Explain how geography shaped one civilization we studied.",
                "type": "open_response",
                "target_concept": "geography_shapes_history",
                "rubric": "Mastery: cites 2+ geographic features with specific effects. Proficient: 1 feature. Developing: cannot connect geography to history.",
            },
            {
                "prompt": "Draw a trade route and explain the geographic logic.",
                "type": "open_response",
                "target_concept": "trade_route_geography",
                "rubric": "Mastery: accurate route with geographic reasoning. Proficient: route drawn but reasoning unclear. Developing: cannot draw a meaningful route.",
            },
        ],
        "resource_guidance": {
            "required": [
                "world map with physical features (mountains, rivers, deserts visible)",
                "paper for drawing maps",
            ],
            "recommended": ["physical/topographic globe", "atlas showing trade routes"],
            "philosophy_specific": {
                "classical": "Geography as the indispensable companion to history. Every history lesson begins with 'where on the map?' Memorize key geographic features and their historical significance.",
                "charlotte_mason": "Map drawing from memory is the core method. After studying a civilization, the child draws its geographic setting from memory. Geography and history are never separated.",
                "montessori": "Physical geography materials: land and water forms. Pin maps marking civilizations on geographic features. Hands-on topographic models.",
            },
        },
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
        "accommodations": {
            "dyslexia": "Map work is visual and spatial — a natural strength for many dyslexic learners. Oral discussion of geographic connections. Drawing maps rather than writing about geography.",
            "adhd": "Build topographic maps with salt dough or clay — highly tactile. Outdoor compass and map exploration. Geography games with timer-based challenges.",
            "gifted": "Analyze how geography shaped modern geopolitics: why do certain countries control trade routes? Why are certain regions still in conflict? Introduce the concept of geographic determinism vs human agency.",
            "visual_learner": "Physical feature maps with color-coded terrain. Satellite images showing real geography. Illustrated trade route maps.",
            "kinesthetic_learner": "Build 3D terrain models. Walk trade routes on a floor map. Use sand and water to simulate rivers and barriers.",
            "auditory_learner": "Discuss geographic connections in conversation. Explain map features aloud. Debate whether geography determines history or people overcome geography.",
        },
        "connections": {
            "reading": "Understanding geographic setting enriches reading comprehension — knowing WHY a story is set where it is deepens understanding",
            "math": "Map scale, distance calculation, and area measurement are math skills applied to geography",
            "science": "Physical geography IS earth science: rivers, mountains, deserts, climate, and ecosystems. Geography integration connects history to the natural world.",
        },
    },
    "hf-20": {
        "enriched": True,
        "learning_objectives": [
            "Narrate the story of at least 3 ancient civilizations from memory, covering key details of each",
            "Place major events and civilizations on a timeline in correct chronological order",
            "Locate studied civilizations on a world map and explain how geography shaped each one",
            "Demonstrate readiness for the developing history level through narration, timeline, and map skills",
        ],
        "teaching_guidance": {
            "introduction": "This is the capstone assessment for foundational history. It is not a test to fear but a celebration of everything the child has learned. The child tells the story of the ancient world IN THEIR OWN WORDS, using their timeline and maps as reference. A child who can narrate Egypt, Greece, and Rome — placing them on a timeline and a map, connecting them to geography, and describing the people who lived there — has a genuine foundation in historical thinking. This assessment should feel like a conversation, not an exam.",
            "scaffolding_sequence": [
                "Begin with a warm-up: 'Tell me about your favorite civilization we studied. What do you remember about it?'",
                "Walk the timeline together: the child narrates the story of history by moving chronologically through their timeline",
                "Map review: the child locates each civilization on the world map and explains one geographic feature that shaped it",
                "Civilization comparison: 'Pick two civilizations. How were they alike? How were they different?'",
                "Historical figures review: 'Tell me about one person from history whose story you remember well.'",
                "Skills check: primary source analysis (show a photograph), timeline placement (add a new event), map reading",
                "Self-reflection: 'What was the most interesting thing you learned in history this year? What do you want to learn more about?'",
                "Celebrate: acknowledge growth, highlight strengths, and set goals for the next level of history study",
            ],
            "socratic_questions": [
                "If you could travel back in time to any civilization we studied, which one would you visit? Why?",
                "Looking at your timeline, what surprised you most about when different civilizations existed?",
                "Pick two civilizations we studied. What was the biggest difference between them? What did they have in common?",
                "What is the most important thing you learned about history this year? Not a fact — but a BIG idea.",
            ],
            "practice_activities": [
                "Grand narration: the child tells the story of history from the earliest civilizations to the most recent topic studied, using the timeline as a guide",
                "Map tour: the child gives a guided tour of the world map, pointing to each civilization and sharing what they know about it",
                "Civilization comparison essay (oral or drawn): pick two civilizations and compare them on 3 characteristics",
                "History museum: the child sets up a display of drawings, timelines, maps, and artifacts from the year's study and gives a museum tour to the family",
            ],
            "real_world_connections": [
                "Everything studied this year connects to the modern world: democracy from Greece, law from Rome, writing from Mesopotamia, mathematics from India",
                "The child can now recognize historical references in books, movies, and conversations — history literacy is a life skill",
                "Understanding the past helps understand the present: why countries exist where they do, why certain languages are spoken, why certain traditions persist",
                "The child's own family history is part of the larger story of human history",
            ],
            "common_misconceptions": [
                "Treating the assessment as a high-stakes test — it should feel like a conversation and a celebration, not an exam",
                "Expecting the child to remember every detail — the goal is to narrate the BIG story with key details, not recite every fact",
                "Comparing the child's knowledge to arbitrary grade-level standards — homeschool allows children to go deeper in areas of interest and move at their own pace",
                "Thinking foundational history is 'done' — history is cyclical in classical education and cumulative in all approaches. These topics will be revisited at deeper levels.",
            ],
        },
        "assessment_criteria": {
            "mastery_indicators": [
                "Narrates 3+ civilizations from memory with key details about government, daily life, and contributions",
                "Places events on the timeline in correct chronological order",
                "Locates civilizations on the world map and connects geography to history",
                "Compares civilizations on multiple characteristics",
            ],
            "proficiency_indicators": [
                "Narrates 2 civilizations with some details",
                "Places most events correctly on the timeline",
                "Locates most civilizations on the map",
            ],
            "developing_indicators": [
                "Narrates 1 civilization or remembers scattered facts without a connected narrative",
                "Has difficulty with chronological ordering",
                "Cannot connect geography to history",
            ],
            "assessment_methods": [
                "oral narration of civilizations",
                "timeline review and ordering",
                "world map labeling and geographic analysis",
                "civilization comparison discussion",
            ],
            "sample_assessment_prompts": [
                "Tell me the story of ancient Egypt. Include the Nile, the pharaohs, and at least 3 other things you remember.",
                "Walk me through your timeline from the oldest events to the newest.",
                "Show me on the map where Greece and Rome were. Why did each civilization develop where it did?",
                "Pick two civilizations we studied. How were they similar? How were they different?",
            ],
        },
        "practice_items": [
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Name three ancient civilizations we studied and one important thing about each.",
                "expected_type": "text",
                "hints": ["Think about: Egypt, Mesopotamia, China, India, Greece, Rome. What is each one known for?"],
                "explanation": "Example: Egypt — built the pyramids along the Nile. Greece — invented democracy in Athens. China — invented paper, printing, compass, and gunpowder. Each civilization made unique contributions to human history.",
            },
            {
                "type": "problem",
                "difficulty": 1,
                "prompt": "Which civilization came first: Ancient Greece or Ancient Egypt?",
                "expected_type": "multiple_choice",
                "options": ["Ancient Greece", "Ancient Egypt", "They started at the same time"],
                "correct_answer": "Ancient Egypt",
                "hints": ["Check the dates: Egypt began around 3000 BC. Greece's golden age was around 500 BC."],
                "explanation": "Ancient Egypt began around 3000 BC — about 2,500 years before Greece's golden age around 500 BC. The pyramids were already ancient when the Parthenon was built!",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "Pick two civilizations we studied. How were they similar? How were they different?",
                "expected_type": "text",
                "hints": [
                    "Choose any two: Egypt, Mesopotamia, China, India, Greece, Rome. Compare: rivers, government, writing, buildings, contributions."
                ],
                "explanation": "A strong comparison finds both similarities and differences. Example: Egypt and Mesopotamia were both river valley civilizations that invented writing, but Egypt had hieroglyphics while Mesopotamia had cuneiform. Egypt was unified under pharaohs; Mesopotamia had competing city-states. Egypt built pyramids (tombs); Mesopotamia built ziggurats (temples).",
            },
            {
                "type": "problem",
                "difficulty": 2,
                "prompt": "True or false: All ancient civilizations developed completely independently with no contact with each other.",
                "expected_type": "true_false",
                "correct_answer": "false",
                "hints": ["Think about trade routes like the Silk Road. Did civilizations trade and communicate?"],
                "explanation": "False. While some civilizations developed independently at first, many eventually traded and communicated. The Silk Road connected China to Rome. Greeks traded across the Mediterranean. Egyptian goods reached Mesopotamia. Trade, war, and migration connected civilizations.",
            },
            {
                "type": "problem",
                "difficulty": 3,
                "prompt": "If you could travel back in time to any civilization we studied, which one would you visit? Why? What would daily life be like for you there?",
                "expected_type": "text",
                "hints": [
                    "Pick a civilization, explain why it interests you, and describe what you know about daily life there. Use what you've learned!"
                ],
                "explanation": "A thoughtful answer shows real historical knowledge applied creatively. The child should name specific details about daily life in their chosen civilization: what they would eat, where they would live, what work they might do, and what they would find most interesting or challenging. This demonstrates comprehension beyond fact recall.",
            },
        ],
        "assessment_items": [
            {
                "prompt": "Narrate the story of one ancient civilization from memory: who they were, where they lived, what they built, and what they contributed.",
                "type": "open_response",
                "target_concept": "civilization_narration",
                "rubric": "Mastery: detailed narration covering location, government, daily life, achievements, and contributions. Proficient: covers 3 topics. Developing: scattered facts.",
            },
            {
                "prompt": "Walk me through your timeline from the oldest to the newest events.",
                "type": "open_response",
                "target_concept": "timeline_mastery",
                "rubric": "Mastery: narrates chronologically with 15+ events and connections. Proficient: 8-14 events in order. Developing: fewer than 8 events or incorrect order.",
            },
            {
                "prompt": "Show me on the world map where each civilization we studied was located. For one of them, explain how geography shaped their civilization.",
                "type": "open_response",
                "target_concept": "geographic_understanding",
                "rubric": "Mastery: locates all civilizations and explains geography's role with specifics. Proficient: locates most and gives general geographic explanation. Developing: cannot locate on map.",
            },
            {
                "prompt": "Compare two civilizations we studied. How were they alike and different?",
                "type": "open_response",
                "target_concept": "comparative_thinking",
                "rubric": "Mastery: 3+ similarities and differences with specifics. Proficient: 1-2 of each. Developing: cannot compare.",
            },
        ],
        "resource_guidance": {
            "required": ["completed timeline from the year's study", "world map", "comfortable assessment environment"],
            "recommended": [
                "the child's Book of Centuries or history notebook for reference during review",
                "drawing supplies for map work",
            ],
            "philosophy_specific": {
                "classical": "Comprehensive assessment through narration, timeline review, map drill, and comparison. The child demonstrates command of the chronological framework and key facts.",
                "charlotte_mason": "Examination by narration: the child tells everything they know, in their own words, without prompting. No multiple-choice tests. The quality of narration IS the assessment.",
                "montessori": "Observation-based assessment: the child demonstrates knowledge through daily work with timelines, maps, and cultural materials. No formal test — the teacher observes mastery in practice.",
            },
        },
        "time_estimates": {"first_exposure": 30, "practice_session": 20, "assessment": 30},
        "accommodations": {
            "dyslexia": "Entire assessment is oral: narration, map pointing, timeline walking, and discussion. No reading or writing required. Allow extra time. The child's knowledge is in their head, not on paper.",
            "adhd": "Break the assessment into 3 short sessions (timeline, maps, narration) rather than one long session. Allow movement between sections. Make it conversational, not test-like. Celebrate strengths first.",
            "gifted": "Extend with analytical questions: 'Why do civilizations rise and fall? What patterns do you see?' Challenge with connections across civilizations. Discuss historiography: 'How do historians decide what to include?'",
            "visual_learner": "Use the timeline and maps as visual aids during narration. Drawing maps from memory as part of assessment.",
            "kinesthetic_learner": "Walk along the wall timeline. Point to maps. Handle timeline cards. Move around during the assessment.",
            "auditory_learner": "Oral narration is the natural assessment mode. Discussion-based comparison. Verbal timeline tour.",
        },
        "connections": {
            "reading": "Historical knowledge enriches reading comprehension. The child can now understand historical references in literature.",
            "math": "Timeline math (calculating years between events), map scale, and population numbers — history is full of math.",
            "science": "Geography, climate, agriculture, engineering, and invention — history and science are inseparable. Ancient civilizations were built on scientific understanding of the natural world.",
        },
    },
}
