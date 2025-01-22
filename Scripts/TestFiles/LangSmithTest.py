# -*- coding: utf-8 -*-

import datetime
import os
from openai import OpenAI
from dotenv import load_dotenv

import openai
from langsmith.wrappers import wrap_openai
from langsmith import traceable
from langsmith.client import Client

input_content1 = """
评价下下面两个的翻译结果
原语句：”落霞与孤鹜齐飞，秋水共长天一色“

翻译后：
1. Rosy clouds in sunset fly with a lone wild duck;
The autumn waters merge with the boundless sky in one hue.

2. The evening glow and the lone wild duck fly together; the autumn water and the vast sky share the same color.

哪个翻译比较好，从意境、意象和文化内涵上考虑
"""

input_content = """
以你的经验  我想将LLM 和 Houdini相结合，在游戏行业方向
能有什么好的创意或者发展方向呢
"""

problem1 = """
J、O、I、N、T分别代表一个不同的数字，满足下面的等式：
（J+O+I+N+T）*（J+O+I+N+T）*（J+O+I+N+T）=JOINT
其中，JOINT代表一个五位数，问JOINT是多少？
"""

# 一个简单的数学问题
problem2 = """
一张方桌,砍掉一个角还剩下几个角
"""

problem3 = """
桌子上有10只鸟，猎人开枪打死了了一只，还剩几只？
"""

problem4 = """
有一个人是殡仪馆停尸间的看尸人，有一天他起床刷牙的时候发
现自己的牙齿是绿色的，然后他就自杀了，为什么?
提示:绿色为染料所染且颜色种类与题目无关系，看尸人有预感会发生这个事情
"""

problem5 = """
马戏团里有两个侏儒，瞎子侏儒比另一个侏儒矮。马戏团只需要一个侏儒，
马戏团的侏儒当然是越矮越好了。可是，在约定比个子的前一天，
瞎子侏儒，也就是那个矮的侏儒已经在家里自杀死了，地上残留着许多碎木屑。他为什么自杀?
提示:高矮侏儒之间并没有作任何身体接触，也没有语言接触
"""

# 加载.env文件中的环境变量
load_dotenv()

api_key = os.getenv('Deepseek_API_Key')
api_url = os.getenv('Deepseek_API_URL')
lanchain_api = os.getenv('LANGCHAIN_API_KEY')

##临时设置环境变量
###LANGCHAIN_TRACING_V2是设置LangChain是否开启日志跟踪模式。
os.environ['LANGCHAIN_TRACING_V2'] = "true"
###LANGCHAIN_API_KEY就是上面生成的LangSmith的key。
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_ENDPOINT'] = "https://api.smith.langchain.com"
###LANGCHAIN_PROJECT 跟踪项目名称
os.environ['LANGCHAIN_PROJECT'] = "test_"+datetime.datetime.now().strftime("%Y%m%d%H")


client = OpenAI(api_key=api_key, base_url=api_url)
client = wrap_openai(client)

@traceable # Auto-trace this function
def pipeline(user_input: str):
    # 记录请求发送时间
    start_time = datetime.datetime.now()

    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[
            {"role": "system", "content": "你是一个经验丰富的数学家，请用中文思考和输出。"},
            {"role": "user", "content": user_input},
        ],
        stream=False
    )

    # 记录响应接收时间
    end_time = datetime.datetime.now()

    # 计算时间间隔
    time_interval = end_time - start_time

    # 打印响应时间间隔
    print("Response time interval:", time_interval)


    # reasoning_content = ""
    # content = ""

    # for chunk in response:
    #     if chunk.choices[0].delta.reasoning_content:
    #         reasoning_content += chunk.choices[0].delta.reasoning_content
    #         print("Reasoning_Content: " + reasoning_content)
    #     else:
    #         content += chunk.choices[0].delta.content
    #         print("Response:  " + content)


    # 打印思维链内容
    print("Reasoning_Content: " + response.choices[0].message.reasoning_content)
    # 打印响应内容
    print("Response:  " + response.choices[0].message.content)



    # 打印 usage 中的 prompt_cache_hit_tokens 和 prompt_cache_miss_tokens
    usage = response.usage
    if usage:
        print("Completion tokens:", usage.completion_tokens)
        print("Prompt tokens:", usage.prompt_tokens)
        print("Total tokens:", usage.total_tokens)
        if usage.model_extra:
            print("Prompt cache hit tokens:", usage.model_extra['prompt_cache_hit_tokens'])
            print("Prompt cache miss tokens:", usage.model_extra['prompt_cache_miss_tokens'])
    else:
        print("No usage information available.")

pipeline(problem5)

