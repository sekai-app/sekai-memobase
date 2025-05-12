from ..env import CONFIG

ADD_KWARGS = {
    "prompt_id": "summary_profile",
}
SUMMARY_PROMPT = """You are given a user profile with some information about the user. Summarize it into shorter form.

## Requirement
Summary the given context in concise form, not more than 3 sentences.
Remove the redundant information and keep the most important information.
Look for the dates on infos, and always Keep the latest infos in the profile
总结给定的上下文，简洁形式，不超过3句话。
去除重复相似的信息，保留最重要的信息。
留意日期，总是保留最新的信息。

The result should use the same language as the input.
结果应该使用与输入相同的语言。
"""


def get_prompt() -> str:
    return SUMMARY_PROMPT


def get_kwargs() -> dict:
    return ADD_KWARGS


if __name__ == "__main__":
    print(get_prompt())
