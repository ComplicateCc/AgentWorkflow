# -*- coding: utf-8 -*-

import json
import os
import openai
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Optional
from dotenv import load_dotenv

### 参数部分
use_reflect = "no reflect"
max_iterations = 3


### 环境部分
# 加载.env文件中的环境变量
load_dotenv()

api_key = os.getenv('Deepseek_API_Key')
api_url = os.getenv('Deepseek_API_URL')
default_model = os.getenv('Deepseek_Default_Model')


### 模型部分
# 创建一个OpenAI客户端
client = openai.OpenAI(
    api_key=api_key,
    base_url=api_url
)

llm = ChatOpenAI(model="deepseek-chat", api_key=api_key, base_url=api_url)


# ### State部分
# class State(TypedDict):
#     """
#     Graph的状态结构
    
#     ori_prompt: 原始的prompt
#     step_index: 步骤索引
#     steps_msg: 步骤信息
#     steps_response: 步骤回复
#     history: 历史记录
#     """
#     ori_prompt: str
#     step_index: int
#     steps_msg : list
#     steps_response: list
#     history: list

from langgraph_state_parts import State 

# 创建一个工作流
workflow = StateGraph(State)


### 模块部分
def planning_part(state):
    print("======Planning模块======")
    pass

def code_learning_part(state):
    print("======参考代码查询模块======")
    pass

def code_generation_part(state):
    print("======代码生成模块======")
    pass

def code_testing_part(state):
    print("======代码运行测试模块======")
    pass

# 代码验收模块
def code_acceptance_part(state):
    print("======代码验收模块======")
    pass

def code_generation_review_part(state):
    print("======代码生成审查模块======")
    pass

def decide_to_finish(state):
    """
    完成决策部分

    Args:
        state (State): 当前状态
    """
    error = state["error"]
    iterations = state["iterations"]

    if error == "no" or iterations == max_iterations:
        print("---DECISION: FINISH---")
        return "end"
    else:
        print("---DECISION: RE-TRY SOLUTION---")
        if use_reflect == "reflect":
            return "reflect"
        else:
            return "generate"

def memory_load_part(state):
    print("======记忆加载模块======")
    pass

def memory_save_part(state):
    print("======记忆保存模块======")
    pass

def memory_retrieve_part(state):
    print("======记忆检索模块======")
    pass

def pre_END_part(state):
    print("======结束前模块======")
    pass


### 构建工作流
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
workflow.add_node("结束前模块", pre_END_part)

workflow.set_entry_point("Planning模块")
workflow.add_edge("Planning模块", "参考代码查询模块")
workflow.add_edge("参考代码查询模块", "代码生成模块")
workflow.add_edge("代码生成模块", "代码测试模块")
workflow.add_conditional_edges(
    "代码测试模块",
    decide_to_finish,
    {
        "end": "结束前模块",
        "reflect": "代码生成审查模块",
        "generate": "代码生成模块",
    },
)
workflow.add_edge("结束前模块", END)
app = workflow.compile()

# app.get_graph().draw_mermaid_png(output_file_path="1.png")
print(app.get_graph())
# # 绘制流程图
# from mermaid import Mermaid
# Mermaid(app.get_graph().draw_mermaid())
