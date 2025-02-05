import requests
import json

# 定义 Ollama API 的 URL，Ollama 默认端口是 11434
url = "http://localhost:11434/api/generate"

# 定义请求数据
data = {
    "model": "deepseek-r1:7b",  # 你本地部署的具体模型名称
    "prompt": "介绍一下中国的长城",
    "stream": False  # 是否使用流式响应
}

# 发送 POST 请求
try:
    response = requests.post(url, json=data)
    response.raise_for_status()
    result = response.json()
    print(result.get("response", "未获取到有效回复"))
except requests.exceptions.RequestException as e:
    print(f"请求出错: {e}")
except json.JSONDecodeError:
    print("无法解析响应为 JSON 格式")