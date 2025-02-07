from openai import OpenAI
import requests
import os
import json
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

api_key = os.getenv('Deepseek_API_Key')
api_url = os.getenv('Deepseek_API_URL')
client = OpenAI(api_key=api_key, base_url=api_url)

def check_balance():
    """
    检查用户的余额信息。

    该函数向 DeepSeek API 发送 GET 请求以获取用户的余额信息，并解析返回的 JSON 数据。
    如果余额信息可用，则打印剩余余额；否则，打印错误信息。

    请求头：
        - Accept: application/json
        - Authorization: Bearer <api_key>

    返回的 JSON 示例：
    {
        "is_available": true,
        "balance_infos": [
            {
                "currency": "CNY",
                "total_balance": "19.95",
                "granted_balance": "0.00",
                "topped_up_balance": "19.95"
            }
        ]
    }

    打印：
        - 剩余余额（例如：剩余19.95元）
        - 如果无法获取余额信息，则打印错误信息。

    Raises:
        - requests.exceptions.RequestException: 如果请求失败。
        - json.JSONDecodeError: 如果响应不是有效的 JSON。
    """
    url = "https://api.deepseek.com/user/balance"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_key}' 
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        response.raise_for_status()  # 检查请求是否成功

        # 解析 JSON 响应
        response_data = json.loads(response.text)

        # 提取余额信息
        if response_data.get("is_available"):
            balance_info = response_data.get("balance_infos", [])[0]
            total_balance = balance_info.get("total_balance", "0.00")
            print(f"剩余{total_balance}元")
        else:
            print("无法获取余额信息")
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON 解析错误: {e}")

# 调用函数以检查余额
# check_balance()


system_prompt = """
用户将提供一段关于游戏开发的描述，其中包含游戏名称、游戏类型、游戏的主要玩法以及游戏的目标受众。请解析这些信息并以 JSON 格式输出。

示例输入: 
《王者荣耀》是一款多人在线战术竞技手游，玩家操控英雄与队友配合，在地图上进行战斗，推掉对方的水晶即可获胜。主要面向广大的手机游戏爱好者。

示例 JSON 输出:
{
    "game_name": "王者荣耀",
    "game_type": "多人在线战术竞技手游",
    "game_play": "玩家操控英雄与队友配合，在地图上进行战斗，推掉对方的水晶即可获胜。",
    "target_audience": "广大的手机游戏爱好者"
}
"""

def json_object_test():
    user_prompt = "《原神》是一款开放世界角色扮演游戏，玩家扮演旅行者在提瓦特大陆展开冒险，探索各种秘境、完成任务、收集资源等。主要面向喜欢奇幻冒险题材的玩家。"

    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}]

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        response_format={
            'type': 'json_object'
        },
        # 合理设置 max_tokens 参数，防止 JSON 字符串被中途截断
        max_tokens=4000
    )
    
    """
    Error code: 400 - {'error': {'message': 'This model does not support Json Output.', 'type': 'invalid_request_error', 'param': None, 'code': 'invalid_request_error'}}
    """
    # R1不支持Json输出
    # print("Reasoning_Content: " + response.choices[0].message.reasoning_content)
    # 打印响应内容
    # 测试下来倒是直接输出 更符合Json格式  不需要json.loads多此一举的解析了
    print("Response:  " + response.choices[0].message.content)

    try:
        result = json.loads(response.choices[0].message.content)
        print(result)
    except json.JSONDecodeError:
        print("解析 JSON 时出错，请检查模型输出或尝试修改提示信息。")
    except AttributeError:
        print("模型返回的内容为空，请尝试修改提示信息。")

    """
    回答：
    {
        'game_name': '原神',
        'game_type': '开放世界角色扮演游戏',
        'game_play': '玩家扮演旅行者在提瓦特大陆展开冒险，探索各种秘境、完成任务、收集资源等。',
        'target_audience': '喜欢奇幻冒险题材的玩家'
    }
    """
    
json_object_test()