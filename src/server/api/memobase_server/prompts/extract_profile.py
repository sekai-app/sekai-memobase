from . import user_profile_topics
from .utils import pack_profiles_into_string
from ..models.response import AIUserProfiles
from ..env import CONFIG, LOG

ADD_KWARGS = {
    "prompt_id": "extract_profile",
}

EXAMPLES = [
    (
        """- User consistently chooses hero archetype characters who overcome challenges through determination [observed across multiple sessions]
""",
        AIUserProfiles(**{
            "facts": [
                {
                    "topic": "content_preferences",
                    "sub_topic": "protagonist_archetype",
                    "memo": "hero archetype characters who overcome challenges through determination",
                }
            ]
        }),
    ),
    (
        """- User created 3 custom characters instead of using presets [session 2024/1/23]
- User spent 15 minutes customizing character appearance and background [session 2024/1/23]
""",
        AIUserProfiles(**{
            "facts": [
                {
                    "topic": "user_behavioral_insights", 
                    "sub_topic": "creativity_preference",
                    "memo": "high creative input preference, creates custom characters and spends significant time on customization [session 2024/1/23]",
                }
            ]
        }),
    ),
    (
        """- User always chooses romantic dialogue options with companion character Aria [pattern across 5 sessions]
- User shows preference for slow-burn relationship development with companions [behavioral pattern]
""",
        AIUserProfiles(**{
            "facts": [
                {
                    "topic": "psychological_drivers",
                    "sub_topic": "romantic_preference_companion", 
                    "memo": "prefers romantic storylines with slow-burn development, particularly with companion Aria [pattern across 5 sessions]",
                }
            ]
        }),
    ),
    (
        """- User responds with detailed, narrative-style messages averaging 50+ words [interaction pattern]
- User takes active role in driving story progression through choices [behavioral pattern observed]
""",
        AIUserProfiles(**{
            "facts": [
                {
                    "topic": "user_behavioral_insights",
                    "sub_topic": "response_style", 
                    "memo": "detailed, narrative-style responses averaging 50+ words",
                },
                {
                    "topic": "user_behavioral_insights",
                    "sub_topic": "narrative_agency",
                    "memo": "active participation in story progression through deliberate choices",
                }
            ]
        }),
    ),
    (
        """- User shows interest in enemies-to-lovers romance tropes [pattern observed across sessions] 
- User prefers fantasy and supernatural story elements [behavioral pattern]
""",
        AIUserProfiles(**{
            "facts": [
                {
                    "topic": "platform_recommendations",
                    "sub_topic": "interested_story_tropes",
                    "memo": "enemies-to-lovers romance tropes [pattern observed across sessions]",
                },
                {
                    "topic": "platform_recommendations", 
                    "sub_topic": "inferred_elements",
                    "memo": "fantasy and supernatural story elements",
                }
            ]
        }),
    ),
    (
        """- User consistently chooses conflict resolution through dialogue rather than combat [behavioral pattern]
- User avoids aggressive or violent story paths [preference pattern observed]
""",
        AIUserProfiles(**{
            "facts": [
                {
                    "topic": "psychological_drivers",
                    "sub_topic": "conflict_engagement",
                    "memo": "prefers peaceful conflict resolution through dialogue, avoids violent story paths",
                }
            ]
        }),
    ),
    (
        """- User shows strong emotional attachment to companion characters [behavioral pattern]
- User tends to develop deep, protective relationships with companions [interaction pattern]
""",
        AIUserProfiles(**{
            "facts": [
                {
                    "topic": "psychological_drivers",
                    "sub_topic": "attachment_style_companion",
                    "memo": "strong emotional attachment with tendency to develop deep, protective relationships",
                }
            ]
        }),
    ),
    (
        """- User consistently chooses female companion characters for romantic interactions [pattern across sessions]
- User shows preference for heterosexual romantic storylines [behavioral pattern]
""",
        AIUserProfiles(**{
            "facts": [
                {
                    "topic": "platform_recommendations",
                    "sub_topic": "gender_orientation_preference",
                    "memo": "preference for female companions in heterosexual romantic storylines",
                }
            ]
        }),
    ),
]

DEFAULT_JOB = """You are a specialist in analyzing immersive roleplay interactions and user behavior patterns.
Your responsibility is to carefully analyze user interaction logs from Sekai and extract content preferences, behavioral insights, and psychological drivers that reveal user preferences for personalized content recommendation.
You will extract both explicit preferences and implicit patterns shown through user choices, dialogue styles, and interaction behaviors.
You will use the same language as the user's input to record the insights.
"""

SEKAI_FACT_RETRIEVAL_PROMPT = """{system_prompt}

## Formatting
### Input Context
#### Topics Guidelines
You'll be given topics and subtopics focused on content preferences, behavioral insights, psychological drivers, and interaction patterns specific to immersive roleplay experiences.

Focus on extracting:
- **Content Preferences**: World types, character archetypes, story genres, customization patterns
- **Behavioral Insights**: Creativity levels, response styles, narrative participation patterns  
- **Psychological Drivers**: Power fantasies, conflict preferences, relationship dynamics
- **Interaction Patterns**: Communication style, decision-making, emotional expression

Don't extract general personal information unrelated to content consumption and roleplay behavior.

#### User Existing Profiles
You will be given existing user profiles to consider for consistency and evolution of preferences.

#### Behavioral Analysis Logs  
You will receive analysis of user interactions in roleplay scenarios, including:
- Choice patterns in different worlds and with different characters
- Creative input and customization behaviors
- Dialogue and relationship building patterns
- Narrative participation and decision-making styles

### Output
Extract insights and place them in the format:
- TOPIC{tab}SUB_TOPIC{tab}MEMO

For example:
- content_preferences{tab}world_type{tab}fantasy and sci-fi settings
- psychological_drivers{tab}romantic_preferences{tab}slow-burn relationship development

Each line represents a behavioral insight or preference pattern containing:
1. TOPIC: main category of the insight
2. SUB_TOPIC: specific aspect within the category  
3. MEMO: the extracted behavioral pattern or preference

## Examples
Here are examples of behavioral analysis extraction:
{examples}

## Guidelines
- Focus on patterns that emerge from user behavior rather than one-time events
- Infer preferences from choices and interaction styles
- Look for consistency across multiple sessions when possible
- Extract insights that would be useful for content recommendation
- If multiple related patterns exist, combine them into a single comprehensive memo
- Only extract insights with actual behavioral evidence

If you find no relevant behavioral patterns or preferences, return "NONE" or "NO INSIGHTS".

#### Topics Guidelines
Below are the topics and subtopics to focus on:
{topic_examples}

Now perform your analysis.
"""

def pack_input(already_input, memo_str, strict_mode: bool = False):
    header = ""
    if strict_mode:
        header = "Focus only on topics/subtopics listed in Topics Guidelines that relate to content preferences and roleplay behavior patterns!"
    return f"""{header}
#### User Existing Profiles
{already_input}

#### Behavioral Analysis Logs
{memo_str}
"""

def get_default_profiles() -> str:
    return user_profile_topics.get_prompt()

def get_prompt(topic_examples: str) -> str:
    LOG.info("DEBUG: get prompt at extract_profile.py")
    sys_prompt = CONFIG.system_prompt or DEFAULT_JOB
    examples = "\n\n".join([
        f"""<example>
<input>{p[0]}</input>
<output>
{pack_profiles_into_string(p[1])}
</output>
</example>
"""
        for p in EXAMPLES
    ])
    return SEKAI_FACT_RETRIEVAL_PROMPT.format(
        system_prompt=sys_prompt,
        examples=examples,
        tab=CONFIG.llm_tab_separator,
        topic_examples=topic_examples,
    )

def get_kwargs() -> dict:
    return ADD_KWARGS

if __name__ == "__main__":
    print(get_prompt(get_default_profiles()))