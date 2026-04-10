"""Pre-enriched content for Mathematics Foundational template nodes."""

MATH_FOUNDATIONAL_CONTENT = {
    "mf-01": {
        "enriched": True,
        "learning_objectives": ["Count objects to 20 with one-to-one correspondence", "Recognize and write numerals 0-20", "Count forward and backward from any number within 20", "Answer 'how many' questions after counting a set"],
        "teaching_guidance": {
            "introduction": "Begin with physical objects the child can touch and move: blocks, buttons, coins, or natural objects like acorns. Counting is a physical activity before it is an abstract one. Have the child touch each object as they say the number aloud.",
            "scaffolding_sequence": ["Count collections of 5 objects, touching each one", "Count collections of 10, grouping into fives", "Count collections of 15, grouping into fives and tens", "Count to 20 objects, then count backward from 20", "Match numeral cards to collections of objects", "Write numerals 0-20 from memory"],
            "socratic_questions": ["How do you know you counted every one?", "If I add one more, how many will there be?", "What number comes just before 15?", "Can you show me 12 with your blocks?"],
            "practice_activities": ["Count items during a nature walk and record the total", "Play counting games: hide objects and count to find them all", "Sort a collection and count each group separately"],
            "real_world_connections": ["Counting items at the grocery store", "Counting steps on a staircase", "Setting the table: one plate for each person"],
            "common_misconceptions": ["Skipping objects or counting the same object twice", "Confusing the last number with a label rather than the total", "Believing that rearranging objects changes the count"],
        },
        "assessment_criteria": {
            "mastery_indicators": ["Counts 20 objects accurately with 1:1 correspondence every time", "Writes numerals 0-20 without a model", "Counts backward from any number within 20"],
            "assessment_methods": ["oral counting", "object counting", "numeral writing"],
            "sample_assessment_prompts": ["Count these 18 buttons, touching each one", "Write the numbers from 0 to 20", "Start at 14 and count backward to 1"],
        },
        "practice_items": [
            {"type": "problem", "difficulty": 1, "prompt": "Count the stars: \u2b50\u2b50\u2b50\u2b50\u2b50\u2b50\u2b50 How many are there?", "expected_type": "number", "correct_answer": "7", "hints": ["Touch each star as you count it", "Start from the left and go to the right"], "explanation": "There are 7 stars. Counting each one: 1, 2, 3, 4, 5, 6, 7."},
            {"type": "problem", "difficulty": 1, "prompt": "What number comes after 9?", "expected_type": "number", "correct_answer": "10", "hints": ["Count: 7, 8, 9, ..."], "explanation": "After 9 comes 10."},
            {"type": "problem", "difficulty": 1, "prompt": "What number comes before 6?", "expected_type": "number", "correct_answer": "5", "hints": ["Count backward: 8, 7, 6, ..."], "explanation": "Before 6 is 5."},
            {"type": "problem", "difficulty": 2, "prompt": "Count backward from 12 to 7. What numbers did you say?", "expected_type": "text", "hints": ["Start at 12 and go down one at a time"], "explanation": "12, 11, 10, 9, 8, 7"},
            {"type": "problem", "difficulty": 2, "prompt": "I have 13 blocks. I get 1 more. How many do I have now?", "expected_type": "number", "correct_answer": "14", "hints": ["Start at 13 and count one more"], "explanation": "13 + 1 = 14. When you add one more to 13, you get 14."},
            {"type": "problem", "difficulty": 2, "prompt": "What number is between 15 and 17?", "expected_type": "number", "correct_answer": "16", "hints": ["Count: 15, ?, 17"], "explanation": "16 is between 15 and 17."},
            {"type": "problem", "difficulty": 3, "prompt": "Start at 4 and count to 19. How many numbers did you say?", "expected_type": "number", "correct_answer": "16", "hints": ["Count each one: 4, 5, 6, ... all the way to 19", "You can count on your fingers or use tally marks"], "explanation": "From 4 to 19 is 16 numbers: 4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19."},
            {"type": "problem", "difficulty": 3, "prompt": "Write the even numbers from 2 to 20.", "expected_type": "text", "hints": ["Even numbers: 2, 4, 6, ..."], "explanation": "2, 4, 6, 8, 10, 12, 14, 16, 18, 20"},
        ],
        "assessment_items": [
            {"prompt": "Count these objects and write the number: \U0001f535\U0001f535\U0001f535\U0001f535\U0001f535\U0001f535\U0001f535\U0001f535\U0001f535\U0001f535\U0001f535\U0001f535\U0001f535\U0001f535\U0001f535", "type": "number", "correct_answer": "15", "target_concept": "counting_to_20"},
            {"prompt": "Start at 20 and count backward to 10.", "type": "text", "rubric": "Mastery: counts 20,19,18...10 without errors. Proficient: one self-correction. Developing: needs help beyond 15.", "target_concept": "backward_counting"},
            {"prompt": "Write the numeral for 'seventeen'.", "type": "number", "correct_answer": "17", "target_concept": "numeral_writing"},
            {"prompt": "What is the number that is one more than 18?", "type": "number", "correct_answer": "19", "target_concept": "one_more"},
            {"prompt": "How do you know you counted every object without skipping any?", "type": "open_response", "rubric": "Mastery: explains touching each one and counting in order. Proficient: mentions being careful. Developing: cannot explain strategy.", "target_concept": "counting_strategy"},
        ],
        "resource_guidance": {"required": ["counting objects", "numeral cards 0-20"], "recommended": ["number line", "ten-frame boards"]},
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
    },
    "mf-02": {
        "enriched": True,
        "learning_objectives": ["Identify and read numerals from 0 to 100", "Understand the difference between a number and a numeral", "Begin to understand place value conceptually"],
        "teaching_guidance": {
            "introduction": "Numbers are ideas. Numerals are the symbols we write to represent those ideas. The numeral '5' represents the idea of five things. Now we extend from 20 all the way to 100. Use a hundred chart as a visual anchor.",
            "scaffolding_sequence": ["Read numerals 0-50 from a hundred chart", "Read numerals 51-100", "Point to any named numeral on the chart", "Write numerals to 50 from memory", "Identify numerals in real-world contexts (addresses, prices, page numbers)"],
            "socratic_questions": ["What patterns do you see in the hundred chart?", "What changes when we go from 19 to 20?", "If I cover up a number, can you figure out what it is from the numbers around it?"],
            "practice_activities": ["Hundred chart puzzles: fill in missing numbers", "Number scavenger hunt: find numbers in books, signs, and packages", "Write numbers from 1 to 50 as fast as you can"],
            "real_world_connections": ["House numbers on your street", "Page numbers in a book", "Prices at a store"],
            "common_misconceptions": ["Reversing digits: writing 31 as 13", "Not understanding that 40 means 'four tens'", "Thinking numbers end at some point"],
        },
        "assessment_criteria": {
            "mastery_indicators": ["Reads any numeral 0-100 on sight", "Points to correct numeral when given orally", "Writes numerals to 50 from memory"],
            "assessment_methods": ["numeral identification", "hundred chart activities", "numeral writing"],
            "sample_assessment_prompts": ["Read these numbers: 47, 82, 15, 63, 90", "Write the number sixty-three", "Point to 78 on the hundred chart"],
        },
        "practice_items": [
            {"type": "problem", "difficulty": 1, "prompt": "What number is this: 25?", "expected_type": "text", "correct_answer": "twenty-five", "hints": ["The 2 means two tens, the 5 means five ones"], "explanation": "25 is read as twenty-five."},
            {"type": "problem", "difficulty": 1, "prompt": "Write the numeral for 'thirty-four'.", "expected_type": "number", "correct_answer": "34", "hints": ["Thirty means 3 tens, four means 4 ones"], "explanation": "Thirty-four is written as 34."},
            {"type": "problem", "difficulty": 2, "prompt": "What number comes right after 49?", "expected_type": "number", "correct_answer": "50", "hints": ["Count: 47, 48, 49, ..."], "explanation": "After 49 comes 50."},
            {"type": "problem", "difficulty": 2, "prompt": "What number is 10 more than 35?", "expected_type": "number", "correct_answer": "45", "hints": ["On the hundred chart, go down one row"], "explanation": "35 + 10 = 45. Adding 10 changes the tens digit by 1."},
            {"type": "problem", "difficulty": 3, "prompt": "Write all the numbers from 88 to 100.", "expected_type": "text", "hints": ["Start at 88 and keep counting"], "explanation": "88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100"},
        ],
        "assessment_items": [
            {"prompt": "Read this number: 76", "type": "text", "correct_answer": "seventy-six", "target_concept": "numeral_reading"},
            {"prompt": "Write the numeral for 'ninety-one'.", "type": "number", "correct_answer": "91", "target_concept": "numeral_writing"},
            {"prompt": "What number is between 59 and 61?", "type": "number", "correct_answer": "60", "target_concept": "number_sequence"},
        ],
        "resource_guidance": {"required": ["hundred chart", "numeral cards"], "recommended": ["number line to 100"]},
        "time_estimates": {"first_exposure": 20, "practice_session": 15, "assessment": 10},
    },
}
