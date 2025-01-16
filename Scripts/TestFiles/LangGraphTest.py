import json
from langchain_openai import ChatOpenAI
import openai
from langgraph.graph import StateGraph, START, END
import os
# 定义传递的信息结构
from typing import TypedDict, Optional
from dotenv import load_dotenv

flag = "do not reflect"
max_iterations = 3

# 加载.env文件中的环境变量
load_dotenv()

api_key = os.getenv('Deepseek_API_Key')
api_url = os.getenv('Deepseek_API_URL')
default_model = os.getenv('Deepseek_Default_Model')

# 创建一个OpenAI客户端
client = openai.OpenAI(
    api_key=api_key,
    base_url=api_url
)

llm = ChatOpenAI(model="deepseek-chat", api_key=api_key, base_url=api_url)

class State(TypedDict):
    step_index: int
    steps_msg : list
    steps_response: list
    history: list

# 创建一个工作流
workflow = StateGraph(State)

def planning_part(state):
    print("Planning part")
    pass

def code_learning_part(state):
    print("Code learning part")
    pass

def code_generation_part(state):
    print("Code generation part")
    pass

def code_testing_part(state):
    print("Code testing part")
    pass

# 代码验收模块
def code_acceptance_part(state):
    pass

def code_generation_review_part(state):
    pass

def decide_to_finish(state):
    """
    Determines whether to finish.

    Args:
        state (dict): The current graph state

    Returns:
        str: Next node to call
    """
    error = state["error"]
    iterations = state["iterations"]

    if error == "no" or iterations == max_iterations:
        print("---DECISION: FINISH---")
        return "end"
    else:
        print("---DECISION: RE-TRY SOLUTION---")
        if flag == "reflect":
            return "reflect"
        else:
            return "generate"

def memory_load_part(state):
    pass

def memory_save_part(state):
    pass

def memory_retrieve_part(state):
    pass

workflow.add_node("Planning模块", planning_part)
workflow.add_node("参考代码查询模块", code_learning_part)
workflow.add_node("代码生成模块", code_generation_part)
workflow.add_node("代码测试模块", code_testing_part)
workflow.add_node("代码验收模块", code_acceptance_part)
workflow.add_node("代码生成审查模块", code_generation_review_part)
workflow.add_node("记忆加载模块", memory_load_part)
workflow.add_node("记忆保存模块", memory_save_part)
workflow.add_node("记忆检索模块", memory_retrieve_part)
workflow.add_node("决定是否完成", decide_to_finish)

workflow.set_entry_point("Planning模块")
workflow.add_edge("Planning模块", "参考代码查询模块")
workflow.add_edge("参考代码查询模块", "代码生成模块")
workflow.add_edge("代码生成模块", "代码测试模块")
workflow.add_conditional_edges(
    "代码测试模块",
    decide_to_finish,
    {
        "end": END,
        "reflect": "代码生成审查模块",
        "generate": "代码生成模块",
    },
)
app = workflow.compile()

# app.get_graph().draw_mermaid_png(output_file_path="1.png")
print(app.get_graph())
# # 绘制流程图
# from mermaid import Mermaid
# Mermaid(app.get_graph().draw_mermaid())
