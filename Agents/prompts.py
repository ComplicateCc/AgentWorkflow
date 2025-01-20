# -*- coding: utf-8 -*-

from pydantic import BaseModel, Field

###
# 你需要的所有文件资料都在以下目录:
# dir_path={work_dir}
# 访问文件时请确保文件路径完整。
###

###
# 你必须遵循以下约束来完成任务。
# 1. 每次你的决策只使用一种工具，你可以使用任意多次。
# 2. 确保你调用的指令或使用的工具在给定的工具列表中, {tool_names}。
# 3. 确保你的回答不会包含违法或有侵犯性的信息。
# 4. 如果你已经完成所有任务，确保以"FINISH"指令结束。
# 5. 用中文思考和输出。
# 6. 如果执行某个指令或工具失败，尝试改变参数或参数格式再次调用。
# 7. 已经得到的信息，不要反复查询。
# 8. 生成一个自然语言查询时，请在查询中包含全部的已知信息。
# 9. 不要向用户提问。
###

main_promt = """
你是一个经验丰富的游戏开发者，擅长Lua编程语言，可以使用工具与指令自动化解决问题。

你的任务是：
<task>
{base_task}
</task>

当前的任务执行记录:
<history>
{agent_scratchpad}
</history>

"""

error_code_prompt = """

"""

planning_prompt = """

"""

base_task_prompt1 = """
你需要用Lua实现，读取用户写入内容，创建一个新文档并保存，最后读取文件内容并打印文件大小。

你可以参考的代码如下：
<reference>
{reference_content}
</reference>

如果参考文档中有的代码逻辑，直接应用，不要新建方法
"""

base_task_prompt = """
<Desgin>
任务1：和男人对话
- 任务目标：与雪狼冰原(4000)坐标为495,736的男人对话
- 任务奖励：无
- 任务接取方式：玩家成神后，进入雪狼冰原ID：4000坐标551,473半径为5格的圆形范围内触发任务，自动播放Timeline ID:21801后接取
- 任务完成方式：玩家点击任务面板，自动寻路到指定位置并与男人对话

NPC信息：
- NPC名称：男人
- lookface：11124（暂定）
- 朝向：7
- X：495
- Y：736
- 正式名：无
- 小头像：无
- 寻路坐标X：493
- 寻路坐标Y：737
- NPC交互结果：
  - 处于任务1状态：
    - 播放Timeline：玩家到达指定位置附近10格圆形范围内，播放Timeline ID:21802，NPC旁边有一只狼的幻影，在玩家靠近后消失，玩家到达指定位置后触发对话

任务2：回到狼牙部落
- 任务目标：寻路到雪狼冰原(4000)，并与狼牙部落中村民NPC对话
- 任务奖励：无
- 任务接取方式：完成任务1后接取
- 任务完成方式：玩家点击任务面板寻路到指定地点，并与村民NPC对话

NPC信息：
- NPC名称：村民
- lookface：11121（暂定）
- 朝向：6
- X：587
- Y：525
- 正式名：无
- 小头像：无
- 寻路坐标X：588
- 寻路坐标Y：522
- NPC交互结果：
  - 处于任务2状态：
    - 对话相关情况：
      - 对话内容：无
      - 对话出现条件：玩家到达指定位置
      - 选项内容及对应点击效果、出现条件如下：无

任务3：男人失踪的原因
- 任务目标：寻路到雪狼冰原（4000）坐标628,527处，打开与男人的Timeline(221803)
- 任务奖励：无
- 任务接取方式：完成任务2后接取
- 任务完成方式：玩家点击任务面板寻路到指定位置并打开相应Timeline

NPC信息：
- NPC名称：男人
- lookface：11124（暂定）
- 朝向：8
- X：628
- Y：527
- 正式名：无
- 小头像：无
- 寻路坐标X：626
- 寻路坐标Y：529
- NPC交互结果：
  - 处于任务3状态：
    - 播放Timeline：Timeline ID:221803
</Design>

你可以参考的代码如下：
<reference>
{reference_content}
</reference>

使用Lua实现<Desgin>中的功能，要求
1. 符合<SampleCode>游戏功能脚本的框架规范
2. 如果没有明确列出某些数据的ID，例如任务ID，人物ID，物品ID等，这些ID全部定义为整数类型，然后定义在代码文件的开头
3. 不用新建枚举。枚举直接使用示例枚举类型脚本<condition_enum>中的内容即可
4. 不同的功能段落用注释标明
5. 如果有实现任务相关的功能，任务面板的代码也需要一起实现。任务面板表示任务未完成或在进行中的点击效果
6. 如果<Desgin>中有提及怪物的物品掉落，则列出掉落逻辑的代码，示例代码参考rwtMonsterDrop。没有怪物就不要列出代码
7. 涉及奖励发放的代码在<award>中
8. 如果有不能实现的功能，将其以注释的形式列在代码文件的最后
9. 如果使用了<SampleCode>中没有的方法、变量或枚举。将其以注释的形式列在代码文件的最后并说明使用原因
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
# Data model
class review_model(BaseModel):
    """代码审查输出格式"""
    review_result: str = Field(description="是否需要重新生成代码")
    review_comment: str = Field(description="审查评论")
    review_advice: str = Field(description="重新生成代码建议")
    
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
新生成的代码要保留代码格式
"""
