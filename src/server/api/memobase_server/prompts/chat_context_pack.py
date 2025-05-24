from typing import Callable

ContextPromptFunc = Callable[[str, str], str]


def en_context_prompt(profile_section: str, event_section: str) -> str:
    return f"""---
# Memory
## User Background:
{profile_section}

## Latest Events:
{event_section}

Unless the user has relevant queries, do not actively mention those memories in the conversation.
---
"""


def zh_context_prompt(profile_section: str, event_section: str) -> str:
    return f"""---
# 记忆
## 用户背景：
{profile_section}

## 部分过去事件：
{event_section}

除非用户有相关的需求，否则不要主动在对话中提到这些记忆.
---
"""


CONTEXT_PROMPT_PACK: dict[str, ContextPromptFunc] = {
    "en": en_context_prompt,
    "zh": zh_context_prompt,
}
