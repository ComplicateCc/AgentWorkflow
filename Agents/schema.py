# -*- coding: utf-8 -*-
from typing import TypedDict


### State部分
class State(TypedDict):
    """
    Graph的状态结构
    
    ori_prompt: 原始的prompt
    step_index: 步骤索引
    steps_msg: 步骤信息
    steps_response: 步骤回复
    history: 历史记录
    """
    ori_prompt: str
    step_index: int
    steps_msg : list
    steps_response: list
    history: list