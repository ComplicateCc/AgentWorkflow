import requests
import json

# 定义 Ollama API 的 URL，Ollama 默认端口是 11434
url = "http://localhost:11434/api/generate"

problem = """
这是一道FBI心理测试题目，你需要尽可能发挥想象空间

有个男人开车去机场赶班机,在到了一个三岔口时,看见一个男孩蹲在地上哭泣.
男人下车询问男孩为什么哭,男孩说他迷路了.于是男人带着小男马孩朝他描述的大致方向找去,
在开了很久的车之后,男孩说看见了自己的家,便跳下车.
这时,男人发现自己已经误了班机的起飞时间.男人在车里沮丧起来,突然又吓的直冒汗,然后又欣慰的笑了.
是什么事造成男人这样的情感变化?
"""

# 定义请求数据
data = {
    "model": "deepseek-r1:7b",  # 你本地部署的具体模型名称
    "prompt": problem,
    "stream": True  # 是否使用流式响应
}

# 发送 POST 请求
# try:
#     response = requests.post(url, json=data)
#     response.raise_for_status()
#     result = response.json()
#     print(result.get("response", "未获取到有效回复"))
# except requests.exceptions.RequestException as e:
#     print(f"请求出错: {e}")
# except json.JSONDecodeError:
#     print("无法解析响应为 JSON 格式")
    

try:
    response = requests.post(url, json=data, stream=True)
    response.raise_for_status()
    for line in response.iter_lines():
        if line:
            result = json.loads(line)
            if "response" in result:
                print(result["response"], end="", flush=True)
except requests.exceptions.RequestException as e:
    print(f"请求出错: {e}")
except json.JSONDecodeError:
    print("无法解析响应为 JSON 格式")