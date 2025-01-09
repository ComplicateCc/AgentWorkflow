# -*- coding: utf-8 -*-

import datetime
import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

api_key = os.getenv('Deepseek_API_Key')
api_url = os.getenv('Deepseek_API_URL')

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
你好!~
"""

client = OpenAI(api_key=api_key, base_url=api_url)

# 记录请求发送时间
start_time = datetime.datetime.now()

response = client.chat.completions.create(
    model= "deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": input_content},
    ],
    stream=False
)

# 记录响应接收时间
end_time = datetime.datetime.now()

# 计算时间间隔
time_interval = end_time - start_time

# 打印响应时间间隔
print("Response time interval:", time_interval)

# 打印响应内容
print(response.choices[0].message.content)

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