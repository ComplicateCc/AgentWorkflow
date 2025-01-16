# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as Soup
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader

# LCEL 文档
url = "https://python.langchain.com/docs/concepts/lcel/"
loader = RecursiveUrlLoader(
    url=url, max_depth=20, extractor=lambda x: Soup(x, "html.parser").text
)
docs = loader.load()

# 根据URL排序列表并获取文本
d_sorted = sorted(docs, key=lambda x: x.metadata["source"])
d_reversed = list(reversed(d_sorted))
concatenated_content = "\n\n\n --- \n\n\n".join(
    [doc.page_content for doc in d_reversed]
)

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

api_key = os.getenv('Deepseek_API_Key')
api_url = os.getenv('Deepseek_API_URL')
default_model = os.getenv('Deepseek_Default_Model')


### OpenAI

# 评分提示
code_gen_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """你是一个具有LCEL（LangChain expression language）专业知识的编码助手。\n 
    这里是一整套LCEL文档：\n ------- \n  {context} \n ------- \n 根据上述提供的文档回答用户问题。确保你提供的任何代码都可以执行，\n 
    并且定义了所有需要的导入和变量。将你的答案结构化为代码解决方案的描述。\n
    然后列出导入。最后列出功能代码块。这里是用户的问题：""",
        ),
        ("placeholder", "{messages}"),
    ]
)


# 数据模型
class code(BaseModel):
    """关于LCEL问题的代码解决方案的模式。"""

    prefix: str = Field(description="问题和方法的描述")
    imports: str = Field(description="代码块的import语句")
    code: str = Field(description="不包括import语句的代码块")

llm = ChatOpenAI(model="deepseek-chat", api_key=api_key, base_url=api_url)
code_gen_chain_oai = code_gen_prompt | llm.with_structured_output(code)
question = "如何在LCEL中构建RAG链？"
solution = code_gen_chain_oai.invoke(
    {"context": concatenated_content, "messages": [("user", question)]}
)
solution



pass

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

### Anthropic

# 强制使用工具的提示
code_gen_prompt_deepseek = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """<instructions> 你是一个具有LCEL（LangChain表达语言）专业知识的编码助手。\n 
    这里是LCEL文档：\n ------- \n  {context} \n ------- \n 根据上述提供的文档回答用户问题。\n 
    确保你提供的任何代码都可以执行，并且定义了所有需要的导入和变量。\n
    将你的答案结构化为：1）描述代码解决方案的前缀，2）导入，3）功能代码块。\n
    调用代码工具以正确地结构化输出。 </instructions> \n 这里是用户的问题：""",
        ),
        ("placeholder", "{messages}"),
    ]
)

from dotenv import load_dotenv
import os
import openai

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

# LLM
expt_llm = "claude-3-opus-20240229"
llm = ChatAnthropic(
    model=expt_llm,
    default_headers={"anthropic-beta": "tools-2024-04-04"},
)

structured_llm_claude = llm.with_structured_output(code, include_raw=True)


# 可选：检查工具使用是否有错误
def check_claude_output(tool_output):
    """检查解析错误或工具调用失败"""

    # 解析错误
    if tool_output["parsing_error"]:
        # 报告输出和解析错误
        print("解析错误！")
        raw_output = str(tool_output["raw"].content)
        error = tool_output["parsing_error"]
        raise ValueError(
            f"解析输出时出错！请确保调用了工具。输出：{raw_output}。\n 解析错误：{error}"
        )

    # 工具未被调用
    elif not tool_output["parsed"]:
        print("工具调用失败！")
        raise ValueError(
            "你没有使用提供的工具！请确保调用工具以结构化输出。"
        )
    return tool_output


# 带输出检查的链
code_chain_claude_raw = (
    code_gen_prompt_deepseek | structured_llm_claude | check_claude_output
)


def insert_errors(inputs):
    """在消息中插入工具解析错误"""

    # 获取错误
    error = inputs["error"]
    messages = inputs["messages"]
    messages += [
        (
            "assistant",
            f"重试。你需要修复解析错误：{error} \n\n 你必须调用提供的工具。",
        )
    ]
    return {
        "messages": messages,
        "context": inputs["context"],
    }


# 这将作为回退链运行
fallback_chain = insert_errors | code_chain_claude_raw
N = 3  # 最大重试次数
code_gen_chain_re_try = code_chain_claude_raw.with_fallbacks(
    fallbacks=[fallback_chain] * N, exception_key="error"
)


def parse_output(solution):
    """当我们添加 'include_raw=True' 到结构化输出时，
    它将返回一个包含 'raw', 'parsed', 'parsing_error' 的字典。"""

    return solution["parsed"]


# 可选：带重试以纠正工具调用失败
code_gen_chain = code_gen_chain_re_try | parse_output

# 无重试
code_gen_chain = code_gen_prompt_deepseek | structured_llm_claude | parse_output

# 测试
# question = "如何在LCEL中构建RAG链？"
# solution = code_gen_chain.invoke(
#     {"context": concatenated_content, "messages": [("user", question)]}
# )
# solution

from typing import List
from typing_extensions import TypedDict


class GraphState(TypedDict):
    """
    表示我们图的状态。

    属性:
        error : 控制流的二进制标志，指示是否触发了测试错误
        messages : 包含用户问题、错误消息、推理
        generation : 代码解决方案
        iterations : 尝试次数
    """

    error: str
    messages: List
    generation: str
    iterations: int
    
### 参数

# 最大尝试次数
max_iterations = 3
# 反思
# flag = 'reflect'
flag = "do not reflect"

### 节点


def generate(state: GraphState):
    """
    生成代码解决方案

    参数:
        state (dict): 当前图状态

    返回:
        state (dict): 新键添加到状态，生成
    """

    print("---生成代码解决方案---")

    # 状态
    messages = state["messages"]
    iterations = state["iterations"]
    error = state["error"]

    # 我们因错误被重新路由到生成
    if error == "yes":
        messages += [
            (
                "user",
                "现在，再试一次。调用代码工具以结构化输出，包含前缀、导入和代码块：",
            )
        ]

    # 解决方案
    code_solution = code_gen_chain.invoke(
        {"context": concatenated_content, "messages": messages}
    )
    messages += [
        (
            "assistant",
            f"{code_solution.prefix} \n 导入: {code_solution.imports} \n 代码: {code_solution.code}",
        )
    ]

    # 增量
    iterations = iterations + 1
    return {"generation": code_solution, "messages": messages, "iterations": iterations}


def code_check(state: GraphState):
    """
    检查代码

    参数:
        state (dict): 当前图状态

    返回:
        state (dict): 新键添加到状态，错误
    """

    print("---检查代码---")

    # 状态
    messages = state["messages"]
    code_solution = state["generation"]
    iterations = state["iterations"]

    # 获取解决方案组件
    imports = code_solution.imports
    code = code_solution.code

    # 检查导入
    try:
        exec(imports)
    except Exception as e:
        print("---代码导入检查：失败---")
        error_message = [("user", f"你的解决方案未通过导入测试：{e}")]
        messages += error_message
        return {
            "generation": code_solution,
            "messages": messages,
            "iterations": iterations,
            "error": "yes",
        }

    # 检查执行
    try:
        exec(imports + "\n" + code)
    except Exception as e:
        print("---代码块检查：失败---")
        error_message = [("user", f"你的解决方案未通过代码执行测试：{e}")]
        messages += error_message
        return {
            "generation": code_solution,
            "messages": messages,
            "iterations": iterations,
            "error": "yes",
        }

    # 无错误
    print("---无代码测试失败---")
    return {
        "generation": code_solution,
        "messages": messages,
        "iterations": iterations,
        "error": "no",
    }


def reflect(state: GraphState):
    """
    反思错误

    参数:
        state (dict): 当前图状态

    返回:
        state (dict): 新键添加到状态，生成
    """

    print("---生成代码解决方案---")

    # 状态
    messages = state["messages"]
    iterations = state["iterations"]
    code_solution = state["generation"]

    # 提示反思

    # 添加反思
    reflections = code_gen_chain.invoke(
        {"context": concatenated_content, "messages": messages}
    )
    messages += [("assistant", f"这里是对错误的反思：{reflections}")]
    return {"generation": code_solution, "messages": messages, "iterations": iterations}


### 边


def decide_to_finish(state: GraphState):
    """
    决定是否完成。

    参数:
        state (dict): 当前图状态

    返回:
        str: 下一个要调用的节点
    """
    error = state["error"]
    iterations = state["iterations"]

    if error == "no" or iterations == max_iterations:
        print("---决定：完成---")
        return "end"
    else:
        print("---决定：重试解决方案---")
        if flag == "reflect":
            return "reflect"
        else:
            return "generate"
        
from langgraph.graph import END, StateGraph, START

workflow = StateGraph(GraphState)

# 定义节点
workflow.add_node("generate", generate)  # 生成解决方案
workflow.add_node("check_code", code_check)  # 检查代码
workflow.add_node("reflect", reflect)  # 反思

# 构建图
workflow.add_edge(START, "generate")
workflow.add_edge("generate", "check_code")
workflow.add_conditional_edges(
    "check_code",
    decide_to_finish,
    {
        "end": END,
        "reflect": "reflect",
        "generate": "generate",
    },
)
workflow.add_edge("reflect", "generate")
app = workflow.compile()


question = "如何直接将字符串传递给可运行对象并使用它来构建我的提示所需的输入？"
solution = app.invoke({"messages": [("user", question)], "iterations": 0, "error": ""})