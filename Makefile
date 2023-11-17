JSON_DIR	=	jsons
PY_DIR		=	py

PROBLEM_PY							=	$(PY_DIR)/problem.py
SCRAPE_LEETCODE_PARTIAL_TAGS_PY		=	$(PY_DIR)/scrape_leetcode_partial_tags.py
SCRAPE_LEETCODE_COMPLETE_TAGS_PY	=	$(PY_DIR)/scrape_leetcode_complete_tags.py
SCRAPE_CODECHEF_PY					=	$(PY_DIR)/scrape_codechef.py
RANDOM_SAMPLE_PY					=	$(PY_DIR)/random_sample.py

LEETCODE_PARTIAL_TAGS_JSON			=	$(JSON_DIR)/leetcode_problems_partial_tags.json
LEETCODE_COMPLETE_TAGS_JSON			=	$(JSON_DIR)/leetcode_problems_complete_tags.json
CODECHEF_PROBLEMS_JSON				=	$(JSON_DIR)/codechef_problems.json
RANDOM_SAMPLE_JSON					=	$(JSON_DIR)/random_sample.json

SAMPLE_SIZE			=	2
SAMPLE_TAGS 		= 	"Array" "Bit Manipulation" "Linked List" "Math" \
						"Stack" "String" "Queue" "Recursion" "Sorting"
SAMPLE_DIFFICULTIES	=	Easy Medium Beginner Intermediate

$(RANDOM_SAMPLE_JSON):	$(RANDOM_SAMPLE_PY) $(LEETCODE_COMPLETE_TAGS_JSON) \
						$(CODECHEF_PROBLEMS_JSON)
	python3 $(RANDOM_SAMPLE_PY) \
		--json_files $(LEETCODE_COMPLETE_TAGS_JSON) $(CODECHEF_PROBLEMS_JSON) \
		-k=$(SAMPLE_SIZE) \
		--tags $(SAMPLE_TAGS) \
		--difficulties $(SAMPLE_DIFFICULTIES) \
		--output=$(RANDOM_SAMPLE_JSON)

$(LEETCODE_COMPLETE_TAGS_JSON):	$(LEETCODE_PARTIAL_TAGS_JSON) \
								$(SCRAPE_LEETCODE_COMPLETE_TAGS_PY) $(PROBLEM_PY)
	python3 $(SCRAPE_LEETCODE_COMPLETE_TAGS_PY) \
		--problems_json=$(LEETCODE_PARTIAL_TAGS_JSON) \
		--output=$(LEETCODE_COMPLETE_TAGS_JSON)

$(LEETCODE_PARTIAL_TAGS_JSON):	$(SCRAPE_LEETCODE_PARTIAL_TAGS_PY) $(PROBLEM_PY)
	python3 $(SCRAPE_LEETCODE_PARTIAL_TAGS_PY) \
		--output=$(LEETCODE_PARTIAL_TAGS_JSON)

$(CODECHEF_PROBLEMS_JSON):	$(SCRAPE_CODECHEF_PY) $(PROBLEM_PY)
	python3 $(SCRAPE_CODECHEF_PY) \
		--output=$(CODECHEF_PROBLEMS_JSON)
