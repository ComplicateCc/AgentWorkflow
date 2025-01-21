# -*- coding: utf-8 -*-
from typing import TypedDict
from pydantic import BaseModel, Field

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
    generated_code: 当前生成的代码
    """
    ori_prompt: str
    code_reference: str
    step_index: int
    steps_msg : list
    steps_response: list
    review_result: bool
    review_advice: str
    generated_code: str
    
class code_generation_model(BaseModel):
    generated_code: str

class review_model(BaseModel):
    """代码审查输出格式"""
    review_result: str = Field(description="是否需要重新生成代码")
    review_comment: str = Field(description="审查评论")
    review_advice: str = Field(description="重新生成代码建议")