# -*- coding: utf-8 -*-

import datetime
import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

api_key = os.getenv('Deepseek_API_Key')
api_url = os.getenv('Deepseek_API_URL')

# api_key = ""
# api_url = "http://localhost:11434/api/chat"
# api_url = "http://192.168.218.85:11434/api/generate"

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

problem2 = """
我是游戏开发引擎的岗位 TA技术美术方向 ，我现在在写OKR。希望结合游戏开发方面和AI结合应用的方向，编写OKR。 
你可以尽可能发挥想象力。  描绘下结合大模型，游戏开发的新方向
"""

problem3 = """
开发工具，实现AI辅助算法模拟，通过AI拟合算法曲线，实现可接受的有损优化，评估有损百分比，提升Shader渲染效率，优化GPU。

帮忙扩展下这个KR
"""

problem4 = """
我现在在尝试用AI-Agent工作流来嵌入现有的游戏开发流程中。希望用AI替代部分工作流程，比如根据策划需求实现代码生成、自动化测试等。
你能帮我想想有什么好的方向吗？ 并以OKR的形式输出
"""

problem = """
我是一个游戏开发引擎开发工程师，在写年度OKR。我希望你帮忙写一些PCG相关的OKR。公司当前没有PCG相关基础，需要从0搭建。
希望你写出一些有挑战性的OKR，一步一步的
"""

client = OpenAI(api_key=api_key, base_url=api_url)

# 记录请求发送时间
start_time = datetime.datetime.now()

response = client.chat.completions.create(
    model= "deepseek-reasoner",
    messages=[
        # {"role": "system", "content": "你是一个经验丰富的数学家，请用中文思考和输出。"},
        {"role": "user", "content": problem},
    ],
    stream=False
    # stream=True
)

# 记录响应接收时间
end_time = datetime.datetime.now()

# 计算时间间隔
time_interval = end_time - start_time

# 打印响应时间间隔
print("Response time interval:", time_interval)


reasoning_content = ""
content = ""

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