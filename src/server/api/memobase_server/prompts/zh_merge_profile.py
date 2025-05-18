from datetime import datetime
from .utils import pack_merge_action_into_string
from ..env import CONFIG

ADD_KWARGS = {
    "prompt_id": "zh_merge_profile",
}
EXAMPLES = {
    "replace": [
        {
            "input": """## 用户主题
基本信息, 年龄
## 旧备忘录
用户39岁
## 新备忘录
用户40岁[提及于2025-05-17]
""",
            "response": """
年龄只能有一个真实值，旧的已过时，所以用新的替换。
---
- UPDATE{tab}用户40岁[提及于2025-05-17]
""",
        },
    ],
    "merge": [
        {
            "input": """## 用户主题
兴趣, 食物
## 旧备忘录
喜欢芝士披萨[提及于2025-03]
## 新备忘录
喜欢鸡肉披萨[提及于2025-05] 吃了鸡肉披萨[提及于2025-05]
""",
            "response": """
食物兴趣不是互斥的，所以合并两条备忘录。并且我需要保持最终memo的简洁。
---
- UPDATE{tab}喜欢芝士[提及于2025-03]和鸡肉披萨[提及于2025-05]
""",
        },
    ],
    "keep": [
        {
            "input": """## 用户主题
基本信息, 生日
## 旧备忘录
1999/04/30
## 新备忘录
用户没有提及生日
""",
            "response": """
生日是唯一值，新备忘录没有提供有价值的信息，所以保留旧的。
---
- ABORT{tab}invalid
""",
        },
    ],
    "special": [
        {
            "input": """## 更新说明
总是保持最新的目标并删除旧的目标。
## 用户主题
工作, 目标
## 旧备忘录
想成为一名软件工程师
## 新备忘录
想创办一家初创公司
""",
            "response": """
目标通常可以有多个，但根据指令要求保留最新目标并删除旧目标。
所以用新的替换旧的。
---
- UPDATE{tab}想创办一家初创公司
""",
        },
    ],
    "validate": [
        {
            "input": """### 主题描述
记录用户的长期学习目标。
## 用户主题
学习, 目标
## 旧备忘录
NONE
## 新备忘录
我想在下周末玩电子游戏
""",
            "response": """验证新备忘录。
主题是关于用户的学习目标，但内容是关于玩游戏的计划。
而且这个主题是关于长期目标，但内容是短期计划。
---
- ABORT{tab}invalid
""",
        },
        {
            "input": """今天是 2025-04-05
### 主题描述
记录用户当前的工作计划，忽略过期的计划
## 用户主题
工作, 当前计划
## 旧备忘录
用户需要在2025-03-21准备面试[提及于2025-03-11]
## 新备忘录
用户需要在2025-05-01之前开发一个Memobase Playground应用[提及于2025-04-05]
""",
            "response": """用户可以有多个当前工作计划，我可以合并这两个计划。
但是根据要求，旧备忘录已经过期了（今天是04-05，但面试在03-21），所以我需要丢弃旧的备忘录。
---
- UPDATE{tab}用户需要在2025-05-01之前开发一个Memobase Playground应用[提及于2025-04-05]
""",
        },
    ],
}

MERGE_FACTS_PROMPT = """你是一个智能备忘录管理器，负责控制用户的备忘录的维护。
你的工作是验证新的备忘录然后更新旧的备忘录。
你将收到两条关于用户同一主题/方面的备忘录，一条是旧的，一条是新的。
你应该根据输入更新备忘录。

以下是如何更新备忘录的指导原则：
### 替换旧备忘录
如果旧备忘录已过时应该被新备忘录替换，或者新备忘录与旧备忘录冲突：
<example>
{example_replace}
</example>

### 合并备忘录
注意，只要旧备忘录中包含新备忘录中未包含的信息，就应该选择合并。
新旧备忘录讲述了同一故事的不同部分，应该合并在一起：
<example>
{example_merge}
</example>

### 保持旧备忘录
如果新备忘录没有添加信息或不包含任何有用信息， 或者不合格，你应该保持旧备忘录放弃这次更新（输出`- ABORT{tab}invalid`）。
<example>
{example_keep}
</example>

### 特殊情况
用户可能会在'## 更新说明'部分给出更新备忘录的特定指令。
你需要理解这些指令并按照指令更新备忘录。
<example>
{example_special}
</example>

### 无旧备忘录
`## 旧备忘录`并不总是提供，如果为空，你只需要根据主题描述验证新备忘录。

## 保存符合有效要求的最终备忘录
最终备忘录（无论是否有旧备忘录）都应该符合主题描述。
主题描述可能包含一些对备忘录的要求：
- 值应该是特定类型、格式、在特定范围内等
- 值应该只记录特定信息，例如用户的姓名、邮箱、学习的长期目标等
你需要判断主题的值是否符合描述，如果不符合，你应该修改备忘录中的有效内容或决定放弃此操作（输出`- ABORT{tab}invalid`）。
如果没有特定的描述，你应该接受任何相关的备忘录，除非他是完全不相关的。
遇到格式问题时，你应该判断是否可以通过修改备忘录来解决，如果可以，更新备忘录，否则放弃此操作。

<example>
{example_validate}
</example>

## 输入格式
以下是输入格式：
<template>
今天是 [YYYY-MM-DD]
## 更新说明
[update_instruction]
### 主题描述
[topic_description]
## 用户主题
[topic], [subtopic]
## 旧备忘录
[old_memo]
## 新备忘录
[new_memo]
</template>
- [update_instruction]、[topic_description]、[old_memo] 可能为空。当为空时，将显示`NONE`。
- 留意并且保留新旧备忘录中的时间标注（例如： XXX[提及于 2025/05/05, 发生于 2022]）。

## 输出要求
在更新备忘录之前需要逐步思考。
根据上述说明，你需要逐步思考并按以下格式输出最终结果：
```
YOUR THOUGHT
---
- UPDATE{tab}MEMO
```
或者
```
YOUR THOUGHT
---
- ABORT{tab}invalid
```

你首先需要逐步思考要求以及主题的值是否适合这个主题。
然后在`---`之后输出你对主题值的结果。
### 结果
如果主题可以修改以符合描述的要求，输出：
- UPDATE{tab}MEMO
新行必须以`- UPDATE{tab}`开头，然后输出主题的修改后的值
如果新旧备忘录都无效，你需要放弃这次操作，在`---`后输出`- ABORT{tab}invalid`即可
如果没有特定的描述，你应该接受任何相关的备忘录，除非他是完全不相关的。

确保你理解主题描述（在`### 主题描述`部分）如果存在的话，并相应地更新最终备忘录。
明智地理解备忘录，你可以从新备忘录和旧备忘录中推断信息以决定最终备忘录。
遵循以下说明：
- 不要返回上面提供的自定义示例中的任何内容。
- 严格遵守正确的输出格式。
- 确保最终备忘录不超过5句话。始终保持简洁并输出备忘录的要点。
- 不要在备忘录中做任何解释，只输出与主题相关的最终值。
- 永远不要编造输入中未提到的内容。
- 如果输入的备忘录与主题描述不符，你应该直接输出`- ABORT{tab}invalid`。
- 保留新旧备忘录中的时间标注（例如： XXX[提及于 2025/05/05, 发生于 2022]）。
- 如果决定更新，确保最终备忘录简洁且没有冗余信息。（例如："User is sad; User's mood is sad" -> "User is sad"）

以上就是全部内容，现在执行你的工作。
"""


def get_input(
    topic, subtopic, old_memo, new_memo, update_instruction=None, topic_description=None
):
    today = datetime.now().astimezone(CONFIG.timezone).strftime("%Y-%m-%d")
    return f"""今天是{today}。
## 更新说明
{update_instruction or "NONE"}
### 主题描述
{topic_description or "NONE"}
## 用户主题
{topic}, {subtopic}
## 旧备忘录
{old_memo or "NONE"}
## 新备忘录
{new_memo}
"""


def form_example(examples: list[dict]) -> str:
    return "\n".join(
        [
            f"""<input>
{example['input']}
</input>
<output>
{example['response']}
</output>
"""
            for example in examples
        ]
    ).format(tab=CONFIG.llm_tab_separator)


def get_prompt() -> str:
    example_replace = form_example(EXAMPLES["replace"])
    example_merge = form_example(EXAMPLES["merge"])
    example_keep = form_example(EXAMPLES["keep"])
    example_special = form_example(EXAMPLES["special"])
    example_validate = form_example(EXAMPLES["validate"])
    return MERGE_FACTS_PROMPT.format(
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
