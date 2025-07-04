from datetime import datetime
from .utils import pack_merge_action_into_string
from ..env import CONFIG, LOG

ADD_KWARGS = {
    "prompt_id": "merge_profile",
}

EXAMPLES = {
    "replace": [
        {
            "input": """## User Topic
content_preferences, protagonist_archetype
## Old Memo
User prefers hero archetype characters [observed in early sessions]
## New Memo
User consistently chooses anti-hero archetype characters with moral complexity [pattern across recent 5 sessions, 2025-05-17]
""",
            "response": """
User preferences have evolved from simple hero to complex anti-hero archetypes, the recent pattern shows more sophisticated character preferences.
---
- UPDATE{tab}User consistently chooses anti-hero archetype characters with moral complexity [pattern across recent 5 sessions, 2025-05-17]
""",
        },
    ],
    "merge": [
        {
            "input": """## User Topic
psychological_drivers, romantic_preference_companion
## Old Memo
User shows interest in slow-burn relationship development with companions [pattern observed 2025-03]
## New Memo
User consistently chooses intimate dialogue options and emotional bonding scenes with companion characters [behavioral pattern 2025-05]
""",
            "response": """
Both insights relate to romantic preferences with companions and should be merged to show the full pattern.
---
- UPDATE{tab}User shows interest in slow-burn relationship development and consistently chooses intimate dialogue options and emotional bonding scenes with companion characters [patterns from 2025-03 to 2025-05]
""",
        },
    ],
    "keep": [
        {
            "input": """## User Topic
user_behavioral_insights, creativity_preference
## Old Memo
High creative input preference, creates custom characters and worlds [established pattern]
## New Memo
User used a preset character once due to time constraints [single session 2025-05-17]
""",
            "response": """
A single instance doesn't override an established behavioral pattern. The old memo represents the user's true preference.
---
- ABORT{tab}invalid
""",
        },
    ],
    "special": [
        {
            "input": """## Update Instruction
Always prioritize the most recent behavioral patterns for recommendation accuracy.
## User Topic
platform_recommendations, interested_story_tropes
## Old Memo
Enemies-to-lovers and redemption arcs [early pattern]
## New Memo
Found family and friendship dynamics [recent consistent pattern]
""",
            "response": """
Following the instruction to prioritize recent patterns for better recommendations.
---
- UPDATE{tab}Found family and friendship dynamics [recent consistent pattern]
""",
        },
    ],
    "validate": [
        {
            "input": """### Topic Description
Record user's preferred protagonist archetypes in roleplay scenarios.
## User Topic
content_preferences, protagonist_archetype
## Old Memo
NONE
## New Memo
User mentioned liking pizza during a casual conversation
""",
            "response": """
The topic is about protagonist archetypes in roleplay, but the new memo is about food preferences in casual conversation - completely unrelated to the topic.
---
- ABORT{tab}invalid
""",
        },
        {
            "input": """Today is 2025-04-05
### Topic Description
Record user's response style patterns for personalized interaction tuning, prioritize recent behavioral changes.
## User Topic
user_behavioral_insights, response_style
## Old Memo
Detailed, narrative-style responses [pattern from 2025-01 to 2025-02]
## New Memo
Brief, action-focused response style [consistent pattern from 2025-03 to 2025-04-05]
""",
            "response": """
User response patterns can evolve over time. The new pattern is more recent and sustained, indicating a genuine preference change for personalized interactions.
---
- UPDATE{tab}Brief, action-focused response style [consistent pattern from 2025-03 to 2025-04-05]
""",
        },
    ],
}

SEKAI_MERGE_FACTS_PROMPT = """You are a behavioral pattern analyst managing user preference profiles for the Sekai immersive roleplay platform.
Your job is to intelligently merge and validate user behavioral insights, content preferences, and interaction patterns.

You will be given two sets of insights - existing and new - about the same aspect of user behavior in Sekai.
Your goal is to create the most accurate and useful profile for content recommendation.

### Merge Guidelines for Sekai Profiles:

#### Replace patterns when:
- New behavioral evidence shows a clear preference evolution or change
- Recent sustained patterns contradict older observations  
- New insights are based on more comprehensive data
<example>
{example_replace}
</example>

#### Merge patterns when:
- New and old insights complement each other without conflict
- Both provide valuable information about user preferences
- Combined insight gives a fuller picture of user behavior
<example>
{example_merge}
</example>

#### Keep existing patterns when:
- New data is insufficient, inconsistent, or represents temporary behavior
- Single instances contradict established behavioral patterns
- New insights are not relevant to the specific behavioral topic
<example>
{example_keep}
</example>

#### Special considerations:
- Follow any specific update instructions for recommendation optimization
- Consider recency for rapidly changing behavioral preferences
- Prioritize sustained patterns over isolated instances
<example>
{example_special}
</example>

### Validation for Behavioral Insights:
Ensure insights match the behavioral topic and are useful for content recommendation:
- Verify insights relate to user behavior in Sekai roleplay scenarios
- Check that patterns are based on actual user choices and interactions
- Validate insights would help personalize content recommendations
<example>
{example_validate}
</example>

## Input Format:
<template>
Today is [YYYY-MM-DD]
## Update Instruction
[update_instruction]
### Topic Description
[topic_description]
## User Topic
[topic], [subtopic]
## Old Memo
[old_memo]
## New Memo
[new_memo]
</template>

Fields may contain "NONE" when empty. Preserve behavioral pattern timestamps and session information.

## Output Requirements:
Analyze the behavioral patterns step by step, then output:

```
YOUR BEHAVIORAL ANALYSIS
---
- UPDATE{tab}MERGED_INSIGHT
```
Or:
```
YOUR ANALYSIS
---
- ABORT{tab}invalid
```

### Key Principles:
1. **Behavioral Focus**: Only insights about user behavior in Sekai scenarios are valid
2. **Pattern Recognition**: Distinguish between established patterns and isolated incidents  
3. **Recommendation Value**: Ensure insights would improve content personalization
4. **Recency Weighting**: Recent sustained patterns often indicate current preferences
5. **Completeness**: Final insights should be comprehensive but concise (max 3 sentences)

Preserve timestamps and behavioral evidence. Never fabricate patterns not present in the input.

Now perform your behavioral analysis.
"""

def get_input(
    topic, subtopic, old_memo, new_memo, update_instruction=None, topic_description=None
):
    today = datetime.now().astimezone(CONFIG.timezone).strftime("%Y-%m-%d")
    return f"""Today is {today}.
## Update Instruction
{update_instruction or "NONE"}
### Topic Description
{topic_description or "NONE"}
## User Topic
{topic}, {subtopic}
## Old Memo
{old_memo or "NONE"}
## New Memo
{new_memo}
"""

def form_example(examples: list[dict]) -> str:
    return "\n".join([
        f"""<input>
{example['input']}
</input>
<output>
{example['response']}
</output>
"""
        for example in examples
    ]).format(tab=CONFIG.llm_tab_separator)

def get_prompt() -> str:
    LOG.info("DEBUG: get prompt at merge_profile.py")
    example_replace = form_example(EXAMPLES["replace"])
    example_merge = form_example(EXAMPLES["merge"])
    example_keep = form_example(EXAMPLES["keep"])
    example_special = form_example(EXAMPLES["special"])
    example_validate = form_example(EXAMPLES["validate"])
    
    return SEKAI_MERGE_FACTS_PROMPT.format(
        example_replace=example_replace,
        example_merge=example_merge,
        example_keep=example_keep,
        example_special=example_special,
        example_validate=example_validate,
        tab=CONFIG.llm_tab_separator,
    )

def get_kwargs() -> dict:
    return ADD_KWARGS

if __name__ == "__main__":
    print(get_prompt())