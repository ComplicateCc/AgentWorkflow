# -*- coding: utf-8 -*-
from typing import TypedDict
from pydantic import BaseModel

### State部分
class State(TypedDict):
    """
    Graph的状态结构
    
    ori_prompt: 原始的prompt
    step_index: 步骤索引
    steps_msg: 步骤信息
    steps_response: 步骤回复
    history: 历史记录
    review_result: 代码审查结果
    review_advice: 代码审查建议
    """
    ori_prompt: str
    code_reference: str
    step_index: int
    steps_msg : list
    steps_response: list
    review_result: bool
    review_advice: str
    generated_code: str
    
class CodeGenerationResponse(BaseModel):
    generated_code: str
    

class CodeReviewResponse(BaseModel):
    review_result: bool
    review_advice: str
