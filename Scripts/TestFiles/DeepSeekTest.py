# -*- coding: utf-8 -*-

import datetime
import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
from openai import APIError, Timeout, RateLimitError, AuthenticationError, OpenAIError

# 加载.env文件中的环境变量
load_dotenv()

# api_key = os.getenv('Deepseek_API_Key')
# api_url = os.getenv('Deepseek_API_URL')


api_key = os.getenv('SILICONFLOW_API_KEY')
api_url = os.getenv('SILICONFLOW_API_URL')
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

problem5 = """
我是一个游戏开发引擎开发工程师，在写年度OKR。我希望你帮忙写一些PCG相关的OKR。公司当前没有PCG相关基础，需要从0搭建。
希望你写出一些有挑战性的OKR，一步一步的
"""

problem6 = """
<使用AST解析器提取Shader关键数学函数>   其中AST解析器是什么？
<开发DNN代理模型>   DNN代理模型是什么？
<网络架构：采用SIREN网络（隐式神经表示）捕获高频细节>   获取的是什么信息？
"""

problem = """
我在用提示词加首帧的方式 用可灵AI生成视频 这是我原来的Prompt: “伴随着风起云涌，大雨落下，天空电闪雷鸣，乌云被闪电点亮 女孩缓缓抬手，头部位置保持不动，轻柔抚过发丝，镜头拉远然后上移，镜头主题保持在女孩的上半身并缓缓的向右侧推进，女孩慢慢砖头看向镜头，背景渐渐模糊” 我希望你帮我修改成可灵AI建议的提示词模式： 主体+运动 ； 背景 + 运动的方式 如果涉及多主体，依次举例即可
"""

client = OpenAI(api_key=api_key, base_url=api_url)

# 记录请求发送时间
start_time = datetime.datetime.now()

response = None  # 确保 response 变量在异常情况下也被定义

try:
    response = client.chat.completions.create(
        # model="deepseek-reasoner",
        model= "Pro/deepseek-ai/DeepSeek-V3",
        messages=[
            {"role": "user", "content": problem},
        ],
        stream=False,
        timeout=300  # 设置超时时间为300秒
    )
    # 打印原始响应内容
    print("Raw response:", response)
except Timeout as e:
    print(f"Request timed out: {e}")
except APIError as e:
    print(f"API 服务端出现错误: {e}")
except RateLimitError as e:
    print(f"请求频率超出速率限制: {e}")
except AuthenticationError as e:
    print(f"认证错误: {e}")
except OpenAIError as e:
    # 捕获其他 OpenAI 相关的错误
    print(f"发生了 OpenAI 错误: {e}")
except Exception as e:
    # 捕获其他未知错误
    print(f"发生了未知错误: {e}")

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


if response:
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
    print("response is None!!!")