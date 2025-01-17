import os
import time
import sys
sys.path.append('G:/Project/AgentWorkflow')
from Models.Factory import ChatModelFactory
from config import max_iterations, use_reflect, use_code_testing
from schema import State, CodeGenerationResponse
from prompts import *
import subprocess
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.chat_models.base import BaseChatModel

from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI


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

def compose_promt_from_clocal_files(state:State):
    
    directory_path = "./Datas/"
    references = ""
    try:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                    references += f"<{filename}>\n{file_content}\n</{filename}>\n\n"
    except Exception as e:
        print(f"发生错误: {e}")
    # base_task = base_tast_prompt.format(reference_content=references)
    # # print(base_task)
    # prompt = main_promt.format(base_task=base_task, agent_scratchpad=agent_scratchpad)
    # print(prompt)
    
    return {"ori_prompt":"","code_reference":references, "step_index":0, "steps_msg":[], "steps_response":[], "history":[]}


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

# llm : BaseChatModel = ChatModelFactory.get_model("DeepSeek")
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

deepseek_api_key = os.getenv('Deepseek_API_Key')
deepseek_api_url = os.getenv('Deepseek_API_URL')

llm = ChatOpenAI(model="deepseek-chat", api_key=deepseek_api_key, base_url=deepseek_api_url)

### 模块部分
def planning_part(state):
    print("======Planning模块======")
    return state

def code_learning_part(state):
    print("======参考代码查询模块======")
    
    #TODO 大模型总结API文档并筛选   未验证有用性  会增加Token成本
    
    return compose_promt_from_clocal_files(state)


def code_generation_part(state):
    print("======代码生成模块======")

    reference_content = state["code_reference"]
    agent_scratchpad = state["history"]
    
    tool_names = []
    
    # 创建提示模板
    base_task = base_task_prompt.format(reference_content=reference_content)
    prompt_template = main_promt.format(base_task=base_task, agent_scratchpad=agent_scratchpad, tool_names=','.join(tool_names))
    # print(prompt_template)
    
    # 创建 ChatPromptTemplate
    chat_prompt = ChatPromptTemplate.from_template(prompt_template)
    # print(chat_prompt)
    
    # 创建 LLMChain
    # code_generation_chain =  chat_prompt | llm.with_structured_output(CodeGenerationResponse, include_raw=False)
    code_generation_chain = llm.with_structured_output(CodeGenerationResponse, include_raw=False)
    
    message = [
    HumanMessage(content=prompt_template)
    ]
    
    # 生成代码
    response = code_generation_chain.invoke(
        message
    )
    
    print(response.generated_code)
        
    return {
        "ori_prompt":prompt_template,
        "code_reference":state["code_reference"],
        "step_index":state["step_index"],
        "steps_msg":state["steps_msg"],
        "steps_response":response
    }


### Test Code
# result = code_learning_part(
#     {
#         "ori_prompt":"",
#         "code_reference":"",
#         "step_index":0,
#         "steps_msg":[],
#         "steps_response":[],
#         "history":[]
#     }
# )
# code_generation_part(result)


def code_testing_part(state):
    print("======代码运行测试模块======")
    
    # 延迟1s
    time.sleep(1)
    
    return state

# 代码验收模块
def code_acceptance_part(state):
    print("======代码验收模块======")
    
    

def code_generation_review_part(state):
    print("======代码生成审查模块======")
    # 延迟1s
    time.sleep(1)
    
    return state

def decide_to_finish(state):
    """
    完成决策部分

    Args:
        state (State): 当前状态
    """
    # error = state["error"]
    error = "no"
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



# # 以下是你的其他代码逻辑
# def main():
#     compose_promt(
#         {
#             "ori_prompt":"请编写一个函数，实现一个简单的任务系统",
#             "step_index":0,
#             "steps_msg":[],
#             "steps_response":[],
#             "history":[]
#         }
#     )

# if __name__ == "__main__":
#     main()
