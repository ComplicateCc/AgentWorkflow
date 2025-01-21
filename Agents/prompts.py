# -*- coding: utf-8 -*-

from pydantic import BaseModel, Field

###
# 你需要的所有文件资料都在以下目录:
# dir_path={work_dir}
# 访问文件时请确保文件路径完整。
###

main_promt = """
你是一个经验丰富的游戏开发者，擅长Lua编程语言，可以使用工具与指令自动化解决问题。

你的任务是：
<task>
{base_task}
</task>

你必须遵循以下约束来完成任务。
1. 每次你的决策只使用一种工具，你可以使用任意多次。
2. 确保你调用的指令或使用的工具在给定的工具列表中, {tool_names}。
3. 确保你的回答不会包含违法或有侵犯性的信息。
4. 如果你已经完成所有任务，确保以"FINISH"指令结束。
5. 用中文思考和输出。
6. 如果执行某个指令或工具失败，尝试改变参数或参数格式再次调用。
7. 已经得到的信息，不要反复查询。
8. 生成一个自然语言查询时，请在查询中包含全部的已知信息。
9. 不要向用户提问。

当前的任务执行记录:
<history>
{agent_scratchpad}
</history>

你的执行记录

"""

error_code_prompt = """

"""

planning_prompt = """

"""

base_task_prompt = """
你需要用Lua实现，读取用户写入内容，创建一个新文档并保存，最后读取文件内容并打印文件大小。

你可以参考的代码如下：
<reference>
{reference_content}
</reference>

如果参考文档中有的代码逻辑，直接应用，不要新建方法
"""

review_prompt = """
这是原始的需求：
<ori_requirement>
{ori_requirement}
</ori_requirement>

这是你生成的代码：
<generated_code>
{generated_code}
</generated_code>

Let's think step by step.

请对你的代码进行审查，判断是否符合需求，如果不符合，请提出改进建议。
请检查你的代码是否可以优化性能。
请按照一下格式输出

"review_result": "True/False",
"review_comment": "Your comment",
"review_advice": "Your advice"

如果需要重新优化代码True  否则为False
你对代码的评价部分填写到review_comment中
如果无需修改代码，review_advice为空即可
"""
    
code_regneration_prompt = """
这是原始的需求：
<ori_requirement>
{ori_requirement}
</ori_requirement>

这是你原来生成的代码：
<generated_code>
{generated_code}
</generated_code>

这是对于你提供代码的修改建议：
<review_advice>
{review_advice}
</review_advice>

请根据修改建议，修改你的代码，并重新生成代码。
仅提供代码即可
新生成的代码要保留代码格式，应用Lua的代码缩进规范
"""
