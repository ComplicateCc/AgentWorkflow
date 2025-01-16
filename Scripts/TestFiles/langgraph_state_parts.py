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
    

def compose_promt(state:State):
    
    
    pass


import subprocess

def check_lua_compilability(lua_code):
    # 定义一个临时文件来存储 Lua 代码
    with open('temp.lua', 'w') as f:
        f.write(lua_code)
    try:
        # 调用 luac 命令行工具，使用 subprocess 模块
        # result = subprocess.run(['./Luac/x64/luac.exe', '-p', 'temp.lua'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, capture_output=True)
        result = subprocess.run(['./Luac/x64/lua.exe', 'temp.lua'], capture_output=True, text=True)
        if result.returncode == 0:
            print("Lua代码编译成功")
            return True
        else:
            print("Lua代码编译失败，错误信息如下:")
            print(result.stderr)
            return False
    except FileNotFoundError:
        print("luac command not found. Please ensure that Lua is installed and luac is in the system path.")
        return False
    finally:
        pass
        # 清理临时文件
        # import os
        # if os.path.exists('temp.lua'):
        #     os.remove('temp.lua')

test_lua_code = """
function TaskSystem:ctor()
    self.tasks = {}
    self.taskApi = GameAPIManager.getAPI("TaskAPI")
end
"""

### TestCode
# result = check_lua_compilability(test_lua_code)

# print("==================")
# print(result)
