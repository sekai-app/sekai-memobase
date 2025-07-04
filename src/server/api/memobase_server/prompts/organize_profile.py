from . import user_profile_topics
from .utils import pack_profiles_into_string
from ..models.response import AIUserProfiles
from ..env import CONFIG, LOG

ADD_KWARGS = {
    "prompt_id": "organize_profile",
}

EXAMPLES = [
    (
        """topic: psychological_drivers 
- romantic_interest{tab}User consistently chooses romantic dialogue options with companions [pattern across sessions]
- emotional_bonding{tab}User shows strong emotional attachment to companion characters [behavioral pattern]
- relationship_depth{tab}User prefers deep, meaningful relationships over casual interactions [choice pattern]
- companion_loyalty{tab}User demonstrates protective behavior toward companion characters [session patterns]
- intimacy_preference{tab}User gravitates toward intimate emotional scenes and vulnerability [pattern observed]
- social_dynamics{tab}User prefers one-on-one interactions over group dynamics with companions [behavioral preference]
""",
        """- romantic_preference_companion{tab}User consistently chooses romantic dialogue options and gravitates toward intimate emotional scenes with companions [pattern across sessions]
- attachment_style_companion{tab}User shows strong emotional attachment and demonstrates protective behavior toward companion characters [behavioral pattern]
- social_dynamics_preference_companion{tab}User prefers deep, meaningful one-on-one interactions over casual group dynamics with companions [choice pattern]
""",
    )
]

SEKAI_ORGANIZE_PROMPT = """You will organize behavioral insights and content preferences for Sekai users.
The insights are all within the same topic category but may have fragmented or overlapping sub-topics.
You need to consolidate them into no more than {max_subtopics} coherent sub_topics for better content recommendation.

Your goal is to create a clean, organized profile that effectively captures user preferences for personalized Sekai content.

## Sekai-Specific Considerations:
- **Content Preferences**: Focus on world types, character archetypes, story genres that drive recommendations
- **Behavioral Insights**: Capture patterns in creativity, response style, and narrative participation  
- **Psychological Drivers**: Understand emotional and relationship preferences for character matching
- **Interaction Patterns**: Identify communication and decision-making styles for experience personalization

## Organization Principles:
- **Consolidate Related Patterns**: Merge similar behavioral insights (e.g., multiple romance preferences)
- **Preserve Key Details**: Keep specific evidence like session dates and pattern descriptions
- **Prioritize Recommendation Value**: Focus on insights most useful for content personalization
- **Remove Redundancy**: Eliminate duplicate or conflicting information
- **Maintain Behavioral Context**: Keep the relationship between choices and underlying preferences

## Reference Sub-topics:
Use these established sub-topics when possible, create new ones only when necessary:
{user_profile_topics}

## Input/Output Format:
### Input:
```
topic: TOPIC
- SUBTOPIC{tab}MEMO
- ...
```

### Output:
```
- NEW_SUB_TOPIC{tab}CONSOLIDATED_MEMO
- ...
```

Each consolidated memo should:
1. **NEW_SUB_TOPIC**: Clear, descriptive sub-topic name
2. **CONSOLIDATED_MEMO**: Combined insights with preserved evidence and patterns

## Example:
{examples}

## Guidelines:
- **Maximum {max_subtopics} sub-topics** in final result
- **Discard irrelevant insights** that don't contribute to content recommendation
- **Prioritize most impactful patterns** that strongly indicate user preferences
- **Preserve behavioral evidence** like session dates and pattern descriptions
- **Use same language** as input insights
- **Focus on actionable insights** for Sekai content recommendation

Your output should create a clean, organized profile that Sekai's recommendation system can effectively use to personalize user experiences.
"""

def get_prompt(max_subtopics: int, suggest_subtopics: str) -> str:
    LOG.info("DEBUG: get prompt at organize_profile.py")
    examples = "\n\n".join([f"Input:\n{p[0]}Output:\n{p[1]}" for p in EXAMPLES])
    return SEKAI_ORGANIZE_PROMPT.format(
        max_subtopics=max_subtopics,
        examples=examples.format(tab=CONFIG.llm_tab_separator),
        tab=CONFIG.llm_tab_separator,
        user_profile_topics=suggest_subtopics,
    )

def get_kwargs() -> dict:
    return ADD_KWARGS

if __name__ == "__main__":
    print(
        get_prompt(
            6,
            suggest_subtopics="""- world_type
- protagonist_archetype  
- romantic_preferences
- creativity_preference
- response_style
- conflict_engagement
""",
        )
    )