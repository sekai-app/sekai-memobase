from typing import Callable

ContextPromptFunc = Callable[[str, str], str]


def en_context_prompt(profile_section: str, event_section: str) -> str:
    return f"""<memory>
# Below is the user profile:
{profile_section}

# Below is the latest events of the user:
{event_section}
</memory>
Unless the user has relevant queries, do not actively mention those memories in the conversation.
"""


def zh_context_prompt(profile_section: str, event_section: str) -> str:
    return f"""<memory>
# 以下是用户的用户画像：
{profile_section}

# 以下是用户的最近事件：
{event_section}
</memory>
除非用户有相关的需求，否则不要主动在对话中提到这些memory.
"""


CONTEXT_PROMPT_PACK: dict[str, ContextPromptFunc] = {
    "en": en_context_prompt,
    "zh": zh_context_prompt,
}
