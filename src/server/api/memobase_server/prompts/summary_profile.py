from ..env import CONFIG, LOG

ADD_KWARGS = {
    "prompt_id": "summary_profile",
}
SUMMARY_PROMPT = """You are given a user profile with some information about the user. Summarize it into shorter form.

## Requirement
Summary the given context in concise form, not more than 3 sentences.
Remove the redundant information and keep the most important information.
Look for the dates on infos, and always Keep the latest infos in the profile

The result should use the same language as the input.
"""


def get_prompt() -> str:
    LOG.info("DEBUG: get prompt at summary_profile.py")
    return SUMMARY_PROMPT


def get_kwargs() -> dict:
    return ADD_KWARGS


if __name__ == "__main__":
    print(get_prompt())
