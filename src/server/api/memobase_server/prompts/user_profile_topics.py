from ..env import CONFIG, LOG
from .profile_init_utils import (
    UserProfileTopic,
    formate_profile_topic,
    modify_default_user_profile,
)


CANDIDATE_PROFILE_TOPICS: list[UserProfileTopic] = [
    UserProfileTopic(
        "content_preferences",
        sub_topics=[
            {
                "name": "protagonist_archetype",
                "description": "preferred character archetypes for protagonist roles (hero, anti-hero, scholar, warrior, trickster, etc.)",
            },
        ],
    ),
    UserProfileTopic(
        "user_behavioral_insights",
        sub_topics=[
            {
                "name": "creativity_preference",
                "description": "high vs low creative input preference in world and character creation",
            },
            {
                "name": "response_style",
                "description": "brief vs detailed response patterns in roleplay conversations",
            },
            {
                "name": "narrative_agency",
                "description": "active vs passive participation in story progression and decision-making",
            },
        ],
    ),
    UserProfileTopic(
        "psychological_drivers",
        sub_topics=[
            {
                "name": "power_fantasy_type",
                "description": "types of empowerment scenarios and power dynamics preferred",
            },
            {
                "name": "conflict_engagement",
                "description": "preference for conflict vs harmony in narratives and problem-solving approaches",
            },
            {
                "name": "romantic_preference_companion",
                "description": "romantic storyline preferences specifically with companion characters",
            },
            {
                "name": "attachment_style_companion",
                "description": "emotional attachment and bonding patterns with companion characters",
            },
            {
                "name": "social_dynamics_preference_companion",
                "description": "preferred social interaction dynamics and relationship types with companions",
            },
            {
                "name": "relationship_preference",
                "description": "overall relationship preferences and interpersonal dynamics across all characters",
            },
        ],
    ),
    UserProfileTopic(
        "platform_recommendations",
        sub_topics=[
            {
                "name": "preference_summary",
                "description": "comprehensive summary of user's content and interaction preferences",
            },
            {
                "name": "inferred_elements",
                "description": "story and world elements inferred from user behavior and choices",
            },
            {
                "name": "interested_story_tropes",
                "description": "specific narrative tropes and storytelling patterns user gravitates toward",
            },
            {
                "name": "interested_ip_tags",
                "description": "intellectual property, franchise, and fandom preferences",
            },
            {
                "name": "gender_orientation_preference",
                "description": "character gender preferences for romantic and social interactions",
            },
        ],
    ),
]

CANDIDATE_PROFILE_TOPICS = modify_default_user_profile(CANDIDATE_PROFILE_TOPICS)

def get_prompt(profiles: list[UserProfileTopic] = CANDIDATE_PROFILE_TOPICS):
    LOG.info("DEBUG: get prompt at user_profile_topics.py")
    return "\n".join([formate_profile_topic(up) for up in profiles]) + "\n..."

if CONFIG.language == "en":
    LOG.info(f"Sekai User profiles: \n{get_prompt()}")

if __name__ == "__main__":
    print(get_prompt())