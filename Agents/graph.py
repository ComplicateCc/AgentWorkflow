# -*- coding: utf-8 -*-

from langgraph.graph import StateGraph, START, END
from schema import State 
from nodes import planning_part, code_learning_part, code_generation_part, code_testing_part, code_acceptance_part, code_generation_review_part, memory_load_part, memory_save_part, memory_retrieve_part, decide_to_finish, pre_END_part

# 创建一个工作流
workflow = StateGraph(State)


### 构建工作流
# workflow.add_node("Planning模块", planning_part)
workflow.add_node("参考代码查询模块", code_learning_part)
workflow.add_node("代码生成模块", code_generation_part)
workflow.add_node("代码测试模块", code_testing_part)
workflow.add_node("代码验收模块", code_acceptance_part)
workflow.add_node("代码生成审查模块", code_generation_review_part)
# workflow.add_node("记忆加载模块", memory_load_part)
# workflow.add_node("记忆保存模块", memory_save_part)
# workflow.add_node("记忆检索模块", memory_retrieve_part)
workflow.add_node("决定是否完成", decide_to_finish)
workflow.add_node("结束前模块", pre_END_part)

workflow.set_entry_point("参考代码查询模块")
workflow.add_edge("参考代码查询模块", "代码生成模块")
workflow.add_edge("代码生成模块", "代码生成审查模块")
workflow.add_conditional_edges(
    "代码生成审查模块",
    decide_to_finish,
    {
        "审核通过": "结束前模块",
        "改进建议": "代码生成模块",
    },
)
# workflow.add_edge("代码生成审查模块", "代码生成模块")
workflow.add_edge("结束前模块", END)
app = workflow.compile()

# app.get_graph().draw_mermaid_png(output_file_path="1.png")
print(app.get_graph())
# 绘制流程图
# from mermaid import Mermaid
# Mermaid(app.get_graph().draw_mermaid())

# try:
#     app.get_graph().draw_mermaid_png(output_file_path="1.png")
# except ValueError as e:
#     print(f"Error occurred: {e}")

# def draw_mermaid_png(output_file_path):
#     import subprocess
#     # 保存 Mermaid 图定义到文件
#     mermaid_definition = app.get_graph().draw_mermaid()
#     with open('graph_definition.mmd', 'w') as f:
#         f.write(mermaid_definition)
#     # 使用 Mermaid CLI 生成 PNG 图像
#     subprocess.run(['mmdc', '-i', 'graph_definition.mmd', '-o', output_file_path], check=True)
#     print("Mermaid graph has been generated as 1.png")

# draw_mermaid_png("1.png")
