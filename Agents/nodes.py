import os
import time
import sys
sys.path.append('G:/Project/AgentWorkflow')
from Models.Factory import ChatModelFactory
from config import max_iterations, use_reflect, use_code_testing
from schema import *
from prompts import *
import subprocess
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.chat_models.base import BaseChatModel

from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

import itertools
import threading

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
    
    references = references.replace('{', '\\{')
    references = references.replace('}', '\\}')
    
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
def show_loading_message():
    for message in itertools.cycle(["正在生成代码.", "正在生成代码..", "正在生成代码...","正在生成代码....","正在生成代码.....","正在生成代码......"]):
        if not loading:
            break
        print(message, end='\r')
        time.sleep(0.5)
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

model_params = {
    "temperature": 0,
    "streaming": True
}
# llm = ChatOpenAI(model="deepseek-chat", api_key=deepseek_api_key, base_url=deepseek_api_url)
llm = ChatModelFactory.get_model("deepseek-chat", model_params)

### 模块部分
def planning_part(state):
    print("======Planning模块======")
    return state

def code_learning_part(state):
    print("======参考代码查询模块======")
    
    # 延迟1s
    time.sleep(1)
    
    #TODO 大模型总结API文档并筛选   未验证有用性  会增加Token成本
    
    return compose_promt_from_clocal_files(state)


def code_generation_part(state):
    print("======代码生成模块======")
    
    ori_prompt = state["ori_prompt"]
    review_result = state["review_result"]
    review_advice = state["review_advice"]
    generated_code = state["generated_code"]
    
    if review_result == "True" or review_result == True:
        prompt = code_regneration_prompt.format(ori_requirement=ori_prompt, generated_code=generated_code, review_advice=review_advice)
        print("=====原代码=====")
        print(generated_code)
        
        code_regeneration_chain = llm.with_structured_output(code_generation_model, include_raw=False)
        message = [
            HumanMessage(content=prompt)
        ]
        
        #流式输出
        previous_output = ""
        for response in code_regeneration_chain.stream(message):
            new_output = response.generated_code[len(previous_output):]
            print(new_output, end='')  # 使用 end='' 确保不会重复打印换行符
            previous_output = response.generated_code
        
        # llm生成代码
        # response = code_regeneration_chain.invoke(
        #     message
        # )
        print(response.generated_code)
        
        state["generated_code"] = response.generated_code
        state["review_result"] = False
        state["review_advice"] = ""
        return state
    
    reference_content = state["code_reference"]
    # agent_scratchpad = state["history"]
    
    tool_names = []
    
    # 创建提示模板
    base_task = base_task_prompt.format(reference_content=reference_content)
    prompt_template = main_promt.format(base_task=base_task, agent_scratchpad="", tool_names=','.join(tool_names))
    print(prompt_template)
        
    print("正在生成代码...")
    # # 启动加载提示线程
    # global loading
    # loading = True
    # loading_thread = threading.Thread(target=show_loading_message)
    # loading_thread.start()
    
    # 创建 ChatPromptTemplate
    # chat_prompt = ChatPromptTemplate.from_template(prompt_template)
    # print(chat_prompt)
    
    # 创建 LLMChain
    # code_generation_chain =  chat_prompt | llm.with_structured_output(CodeGenerationResponse, include_raw=False)
    code_generation_chain = llm.with_structured_output(code_generation_model, include_raw=False)
    
    message = [
        HumanMessage(content=prompt_template)
    ]
    
    # llm生成代码
    # response = code_generation_chain.invoke(
    #     message
    # )
    
    # # 停止加载提示
    # loading = False
    # loading_thread.join()
    
    # print(response.generated_code)
    
    # 流式生成代码并打印 增量输出
    previous_output = ""
    for response in code_generation_chain.stream(message):
        new_output = response.generated_code[len(previous_output):]
        print(new_output, end='')  # 使用 end='' 确保不会重复打印换行符
        previous_output = response.generated_code
    
    generated_code = response.generated_code
    # step_response.append(response)
    
    return {
        "ori_prompt":prompt_template,
        "code_reference":state["code_reference"],
        "step_index":state["step_index"],
        "steps_msg":state["steps_msg"],
        "steps_response":response,
        "review_result":False,
        "review_advice":"",
        "generated_code":generated_code
    }


## Test Code
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


# 暂时移除
def code_testing_part(state):
    print("======代码运行测试模块======")
    
    # 延迟1s
    time.sleep(1)
    
    return state

# 代码验收模块
def code_acceptance_part(state):
    print("======代码验收模块======")
    
    ori_prompt = state["ori_prompt"]
    generated_code = state["generated_code"]
    step_index = state["step_index"]
    
    prompt = review_prompt.format(ori_requirement=ori_prompt, generated_code=generated_code)
    
    code_review_chain = llm.with_structured_output(review_model)
    
    message = [
        HumanMessage(content=prompt)
    ]
    
    # llm生成代码
    response = code_review_chain.invoke(
        message
    )
    print("是否需要修改代码？ ：" + response.review_result)
    print("审查评论" + response.review_comment)
    print("修改建议：" + response.review_advice)
    
    step_index += 1
    
    state["review_result"] = response.review_result
    state["review_advice"] = response.review_advice
    state["step_index"] = step_index
    
    return state
    

def code_generation_review_part(state):
    print("======代码生成审查模块======")
    
    ori_prompt = state["ori_prompt"]
    generated_code = state["generated_code"]
    step_index = state["step_index"]
    
    prompt = review_prompt.format(ori_requirement=ori_prompt, generated_code=generated_code)
    
    code_review_chain = llm.with_structured_output(review_model)
    
    message = [
        HumanMessage(content=prompt)
    ]
    
    # llm生成代码
    response = code_review_chain.invoke(
        message
    )
    
    review_result = response.review_result and response.review_advice != ""
    print("是否需要修改代码 ：" + str(review_result))
    print("审查评论: " + response.review_comment)
    print("修改建议：" + response.review_advice)
    
    step_index += 1
    
    if review_result == False or review_result == "False":
        try:
            user_approval = input("是否希望人工提改进建议? (yes/no): ")
        except:
            user_approval = "no"
        
        user_approval = user_approval.lower()
        
        if user_approval == "yes":
            user_advice = input("请输入你的建议: ")
            state["review_result"] = True
            state["review_advice"] = user_advice
            state["step_index"] = step_index
            return state
    
    state["review_result"] = review_result
    state["review_advice"] = response.review_advice
    state["step_index"] = step_index
    return state

def decide_to_finish(state):
    
    review_result = state["review_result"]
    review_advice = state["review_advice"]
    step_index = state["step_index"]
    
    if review_result == "False" or review_result == False or step_index >= max_iterations:
        print("---DECISION: FINISH---")
        return "审核通过"
    else:
        print("---DECISION: RE-TRY SOLUTION---")
        # if use_reflect == "reflect":
        #     return "reflect"
        # else:
        return "代码改进"

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
    print("正在保存文件...")
    
    code = state["generated_code"]
    
    with open("generated_code.lua", "w") as f:
        f.write(code)
    
    # 延迟1s
    time.sleep(1)
    
    print("文件已保存")
    



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
