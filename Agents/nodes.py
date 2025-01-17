import os
# import sys
# sys.path.append('G:/Project/AgentWorkflow')
from Models.Factory import ChatModelFactory
from config import max_iterations, use_reflect, use_code_testing
from schema import State
from prompts import *
import subprocess

### State部分
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

def compose_promt(state:State):
    prompt = state["ori_prompt"]
    agent_scratchpad = state["history"]
    base_task = base_tast_prompt
    
    llm = ChatModelFactory.get_model("deepseek")
    file_path = "./Datas"
    #读取file_path路径下的所有文件 并整合成字符串
    with open(file_path, 'r', encoding='utf-8') as f:
        reference_content = f.read()
    print(reference_content)
    
    pass


# 以下是你的其他代码逻辑
def main():
    compose_promt(
        {
            "ori_prompt":"请编写一个函数，实现一个简单的任务系统",
            "step_index":0,
            "steps_msg":[],
            "steps_response":[],
            "history":[]
        }
    )

if __name__ == "__main__":
    main()


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
        # 清理临时文件
        if os.path.exists("temp.lua"):
            os.remove("temp.lua")

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



