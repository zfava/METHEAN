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
            "philosophy_specific": {
                "classical": "Structured observation with scientific vocabulary: classify observations by sense, record systematically, memorize the five senses and their functions.",
                "charlotte_mason": "Nature study begins here: the child learns to LOOK at the world with attention and wonder. Original drawings from life in the nature notebook. Outdoor observation is primary.",
                "montessori": "Sensorial materials refine each sense: rough/smooth boards, color tablets, sound cylinders, smelling bottles. Then apply refined senses to nature observation.",
            },
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
            "philosophy_specific": {
                "classical": "Classification as the first great act of scientific thinking. Memorize the characteristics of life. Systematic sorting with proper vocabulary.",
                "charlotte_mason": "Nature walks to observe living and nonliving things in their natural setting. The child discovers the difference through direct observation before formal definitions.",
                "montessori": "Nomenclature cards: living and nonliving things with photographs. Sorting trays for physical classification. Real specimens (plants, shells, rocks) for hands-on exploration.",
            },
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
            "philosophy_specific": {
                "classical": "Plant life cycle memorized as a sequence. Vocabulary drilled: germination, photosynthesis, dispersal. Structured observation logs.",
                "charlotte_mason": "The child plants seeds, tends them daily, draws what they see in their nature notebook. Direct observation is primary — textbooks are secondary. The garden IS the classroom.",
                "montessori": "Botany nomenclature cards: parts of a plant with three-part matching. Seed sprouting trays. Practical life: watering and caring for classroom/home plants.",
            },
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
            "philosophy_specific": {
                "classical": "Habitat classification: memorize 6 habitats and key animals. Vocabulary: habitat, adaptation, ecosystem. Systematic study with flashcards and drill.",
                "charlotte_mason": "Living books about animals in their homes. Nature walks to observe local habitats. The child draws animals they see and describes the habitat in their nature notebook.",
                "montessori": "Continent animal cards sorted by habitat. Habitat diorama as a hands-on project. Nomenclature cards matching animals to habitats.",
            },
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
            "philosophy_specific": {
                "classical": "Memorize major organs and their functions. Vocabulary: skeleton, cardiac, respiratory, digestive. Systematic body systems study.",
                "charlotte_mason": "The child's own body as the subject of wonder. Outdoor play IS body science. Living books about the body read with fascination, not clinical detachment.",
                "montessori": "Human body puzzle with removable organs. Nomenclature cards for body parts. Practical life: nutrition preparation, hygiene routines as body care.",
            },
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
            "philosophy_specific": {
                "classical": "Systematic daily recording. Memorize cloud types and weather vocabulary. Structured observation logs with correct terminology.",
                "charlotte_mason": "Daily weather observation is a cornerstone of Charlotte Mason nature study. The child records weather in their nature notebook alongside seasonal observations. Weather calendar posted in the learning space.",
                "montessori": "Weather station as practical life: the child checks instruments, records data, and reports to the family. Weather cards for classification. Hands-on instrument building.",
            },
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
            "philosophy_specific": {
                "classical": "Memorize seasonal characteristics and the Earth's tilt explanation. Vocabulary: equinox, solstice, hemisphere, axis. Structured seasonal observation records.",
                "charlotte_mason": "Seasonal nature study is CENTRAL to Charlotte Mason science. Visit the same outdoor spot monthly and draw what you see. The child's nature notebook becomes a year-long seasonal record.",
                "montessori": "Seasonal table: a display that changes with the season, with natural objects collected by the child. Globe work: physical demonstration of Earth's tilt and seasons.",
            },
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
            "philosophy_specific": {
                "classical": "Water cycle memorized as a three-stage process. Vocabulary drilled: evaporation, condensation, precipitation. Diagram drawn and labeled from memory.",
                "charlotte_mason": "Direct observation: the child watches puddles evaporate, sees dew form, feels rain fall. The science notebook records real observations of the water cycle happening around them.",
                "montessori": "Water cycle experiment tray: the child sets up and observes the zip-lock bag experiment independently. Three-part nomenclature cards for water cycle stages.",
            },
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
            "philosophy_specific": {
                "classical": "Rock classification using proper terminology: igneous, sedimentary, metamorphic. Memorize properties. Structured observation and sorting logs.",
                "charlotte_mason": "Rock collections from nature walks. The child draws rocks in their nature notebook with detailed observations. Soil investigation in the garden. Geology discovered outdoors.",
                "montessori": "Rock sorting trays with magnifying glass. Three-part nomenclature cards for rock types. Practical life: gardening connects soil science to real work.",
            },
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
            "philosophy_specific": {
                "classical": "Magnetism as the child's first encounter with invisible forces. Vocabulary: attract, repel, poles, magnetic field. Systematic testing and recording.",
                "charlotte_mason": "Hands-on discovery: the child experiments freely with magnets before formal instruction. Wonder first, terminology second. Record discoveries in the science notebook.",
                "montessori": "Magnet experiment tray: magnets, test materials, and a recording sheet. The child works independently, testing and recording. Compass work as a practical life extension.",
            },
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
            "philosophy_specific": {
                "classical": "Light properties memorized: straight-line travel, reflection, shadow formation. Vocabulary: opaque, translucent, transparent, source, shadow. Structured experiments.",
                "charlotte_mason": "Shadow play and sundials: the child discovers light behavior through outdoor observation. Drawing shadows in the nature notebook. Shadow puppets as art meets science.",
                "montessori": "Light experiment tray: flashlight, objects, and classification cards. The child tests materials independently and sorts into categories. Sundial construction as practical work.",
            },
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
            "philosophy_specific": {
                "classical": "Sound properties memorized: vibration, pitch, volume, medium. Vocabulary drill. Structured experiment recording.",
                "charlotte_mason": "Hands-on sound experiments: the child discovers vibration, pitch, and volume through building and playing instruments. Nature sounds during outdoor time. Drawing instruments in the science notebook.",
                "montessori": "Sound cylinders for pitch discrimination. Instrument-building as practical work. Sound experiment tray: rubber bands, cups, strings, water glasses.",
            },
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
            "philosophy_specific": {
                "classical": "Memorize all 6 simple machines and their definitions. Identify in daily life systematically. Vocabulary: fulcrum, force, load, effort, mechanical advantage.",
                "charlotte_mason": "Finding simple machines everywhere: the child sees physics in the playground, kitchen, and workshop. Drawing simple machines in the science notebook with labels.",
                "montessori": "Simple machine experiment trays: lever tray, ramp tray, pulley tray. The child tests each independently. Nomenclature cards matching machines to real-world examples.",
            },
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
            "philosophy_specific": {
                "classical": "The scientific method memorized as a formal sequence. Structured experiment reports with each step labeled. Vocabulary: hypothesis, variable, control, observation, conclusion.",
                "charlotte_mason": "The child as natural scientist: wondering, guessing, testing, discovering. Science notebook records the process. The method is learned through DOING, not memorizing steps.",
                "montessori": "Experiment trays set up for the child to work through independently. The child records observations in a science journal. Self-directed inquiry with teacher guidance.",
            },
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
            "philosophy_specific": {
                "classical": "Nature journaling as systematic scientific recording. Date, weather, location, and observation on every entry. Structured format with labeled diagrams.",
                "charlotte_mason": "The nature notebook is THE central tool of Charlotte Mason science education. Draw from life, never from photos. Weekly outdoor observation is non-negotiable. The journal grows into a beautiful personal record of the natural world.",
                "montessori": "Nature journal as independent work: the child goes outdoors with their journal and chooses what to observe. The journal is the child's own project, reviewed periodically with the teacher.",
            },
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
            "philosophy_specific": {
                "classical": "Classification as the foundational scientific thinking skill. Memorize major taxonomic groups. Systematic sorting with proper terminology. Linnaeus as the father of classification.",
                "charlotte_mason": "Classification discovered through nature walks: the child sorts what they collect and discovers groupings naturally. Formal classification confirms what observation reveals.",
                "montessori": "Sorting trays with natural objects. Classification cards with multiple sorting criteria. The child works independently to discover grouping systems.",
            },
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
            "philosophy_specific": {
                "classical": "Insect anatomy memorized: head, thorax, abdomen, 6 legs. Metamorphosis stages drilled. Classification: insects within arthropods. Vocabulary: metamorphosis, larva, pupa, pollination.",
                "charlotte_mason": "Observing insects in nature: watching caterpillars, finding beetles under logs, drawing bees on flowers. The nature notebook is full of insect observations. Living books about insect life.",
                "montessori": "Insect puzzle with labeled body parts. Metamorphosis sequence cards. Butterfly life cycle figures. Real specimen observation with magnifying glass.",
            },
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
            "philosophy_specific": {
                "classical": "Bird classification and anatomy memorized. 10 local species identified by name and features. Vocabulary: ornithology, plumage, migration, adaptation, fledgling.",
                "charlotte_mason": "Bird watching IS Charlotte Mason nature study at its best. Weekly bird observation. Drawing birds from life. Identifying songs. The child becomes a genuine birdwatcher.",
                "montessori": "Bird cards with photographs for identification. Parts-of-a-bird puzzle. Bird feeder as a practical life station the child maintains.",
            },
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
